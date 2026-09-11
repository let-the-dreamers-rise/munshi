"""The whole loop, offline: investigate, draft, ask the household, stop, resume in a new process."""

import json

from munshi.inbox import Inbox
from munshi.runner import Runner
from munshi.witness import Household
from tests.fixtures import NOW, phone, scam_afternoon
from tests.scripted import Scripted

VERDICT = {"kind": "likely_scam", "confidence": 0.93,
           "headline": "This looks like the KYC scam: a stranger, nine minutes after a threat.",
           "recommended": "report_now"}


def setup(tmp_path):
    household = Household.from_messages("meera", phone(scam_afternoon()), now=NOW)
    event = [e for e in household.events if e.kind == "scam_shaped_payment"][0]
    return household, event


def first_half(event_id):
    return [
        ("tool", "investigate_payment", {"event_id": event_id}),
        ("tool", "send_money", {"to": "kyc.update9@ybl", "amount": 12000}),
        ("tool", "draft_cybercrime_report", {"event_id": event_id}),
        ("tool", "draft_bank_dispute", {"event_id": event_id}),
        ("tool", "ask_household", {"event_id": event_id}),
    ]


def test_the_agent_stops_at_a_decision_and_resumes_in_a_new_process(tmp_path):
    household, event = setup(tmp_path)
    investigator = Scripted([("tool", "Verdict", VERDICT)])
    runner = Runner(tmp_path, household, model=Scripted(first_half(event.id)), investigator_model=investigator)

    outcome = runner.handle(event)
    assert outcome == "asked"
    inbox = Inbox(tmp_path / "inbox.json")
    cards = inbox.pending()
    assert len(cards) == 1
    c = cards[0]
    assert c.event_id == event.id and c.interrupt_id
    assert [o[0] for o in c.options] == ["report", "fine"]
    assert "KYC scam" in c.headline
    assert any("9 minutes" in line for line in c.evidence)
    assert set(c.drafts) == {"cybercrime_report", "bank_dispute"}

    audit = [json.loads(l) for l in (tmp_path / "audit.jsonl").read_text(encoding="utf-8").splitlines()]
    refused = [a for a in audit if a["refused"]]
    assert [a["tool"] for a in refused] == ["send_money"]

    # A new process: fresh objects, only the files on disk carry the state.
    later = Runner(tmp_path, Household.from_payload(household.to_payload()),
                   model=Scripted([("text", "Reported. Call 1930 now.")]))
    done = later.decide(c.id, "report")
    assert done.status == "decided" and done.decision == "report"
    assert "1930" in done.outcome
    assert Inbox(tmp_path / "inbox.json").pending() == []


def test_a_scam_is_never_left_unasked_even_if_the_model_forgets(tmp_path):
    household, event = setup(tmp_path)
    runner = Runner(tmp_path, household, model=Scripted([("text", "Looks fine to me.")]))
    assert runner.handle(event) == "asked by the safety net"
    cards = Inbox(tmp_path / "inbox.json").pending()
    assert len(cards) == 1 and cards[0].event_id == event.id


def test_choosing_fine_trusts_the_payee(tmp_path):
    household, event = setup(tmp_path)
    runner = Runner(tmp_path, household, model=Scripted(first_half(event.id)),
                    investigator_model=Scripted([("tool", "Verdict", VERDICT)]))
    runner.handle(event)
    card = Inbox(tmp_path / "inbox.json").pending()[0]
    later = Runner(tmp_path, household, model=Scripted([
        ("tool", "remember_trusted_payee", {"party": "kyc.update9@ybl"}),
        ("text", "Noted, I will not ask about this payee again.")]))
    later.decide(card.id, "fine")
    prefs = json.loads((tmp_path / "prefs.json").read_text(encoding="utf-8"))
    assert "kyc.update9@ybl" in prefs["trusted"]
    assert event.id in prefs["handled"]


def test_a_choice_that_is_not_on_the_card_is_refused(tmp_path):
    household, event = setup(tmp_path)
    runner = Runner(tmp_path, household, model=Scripted([("text", "ok")]))
    runner.handle(event)
    card = Inbox(tmp_path / "inbox.json").pending()[0]
    try:
        runner.decide(card.id, "send the money back")
    except ValueError as error:
        assert "not an option" in str(error)
    else:
        raise AssertionError("expected a ValueError")
