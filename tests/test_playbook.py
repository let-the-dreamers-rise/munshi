"""The playbook model runs the real loop with no credentials, and follows the system prompt's steps."""

import json

from munshi.inbox import Inbox
from munshi.playbook import Playbook
from munshi.runner import Runner
from munshi.witness import Household
from tests.fixtures import NOW, double_charge, netflix, phone, scam_afternoon


def runner_for(tmp_path, *groups):
    household = Household.from_messages("meera", phone(*groups), now=NOW)
    return Runner(tmp_path, household, model=Playbook()), household


def tools_called(tmp_path):
    rows = (tmp_path / "audit.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(r)["tool"] for r in rows]


def test_a_scam_gets_all_three_drafts_then_one_card(tmp_path):
    runner, household = runner_for(tmp_path, scam_afternoon())
    (event,) = household.events
    assert runner.handle(event) == "asked"
    assert tools_called(tmp_path) == ["investigate_payment", "draft_cybercrime_report", "draft_bank_dispute",
                                      "draft_upi_help_complaint", "ask_household"]
    (card,) = Inbox(tmp_path / "inbox.json").pending()
    assert set(card.drafts) == {"cybercrime_report", "bank_dispute", "upi_help"}
    done = runner.decide(card.id, "report")
    assert "1930" in done.outcome and "18002586161" in done.outcome


def test_fine_on_a_scam_card_trusts_the_payee_through_the_agent(tmp_path):
    runner, household = runner_for(tmp_path, scam_afternoon())
    (event,) = household.events
    runner.handle(event)
    (card,) = Inbox(tmp_path / "inbox.json").pending()
    fresh = Runner(tmp_path, Household.from_payload(household.to_payload()), model=Playbook())
    fresh.decide(card.id, "fine")
    assert tools_called(tmp_path)[-1] == "remember_trusted_payee"
    prefs = json.loads((tmp_path / "prefs.json").read_text(encoding="utf-8"))
    assert prefs["trusted"] == ["kyc.update9@ybl"]


def test_a_double_charge_gets_a_dispute_and_no_police_report(tmp_path):
    runner, household = runner_for(tmp_path, double_charge())
    (event,) = household.events
    runner.handle(event)
    (card,) = Inbox(tmp_path / "inbox.json").pending()
    assert set(card.drafts) == {"bank_dispute", "upi_help"}
    assert [o[0] for o in card.options] == ["dispute", "fine"]


def test_a_renewal_is_only_a_question(tmp_path):
    runner, household = runner_for(tmp_path, netflix())
    (event,) = household.events
    runner.handle(event)
    (card,) = Inbox(tmp_path / "inbox.json").pending()
    assert card.drafts == {} and card.kind == "renewal_due"
    assert runner.decide(card.id, "keep").status == "decided"
    assert "remember_trusted_payee" not in tools_called(tmp_path)
