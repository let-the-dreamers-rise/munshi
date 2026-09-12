"""The card in Hindi: written from the same facts, not translated from the English."""

from munshi import hindi
from munshi.inbox import Inbox
from munshi.runner import Runner
from munshi.witness import Household
from tests.fixtures import NOW, double_charge, netflix, phone, scam_afternoon
from tests.scripted import Scripted


def only(*groups):
    household = Household.from_messages("meera", phone(*groups), now=NOW)
    return household.events[0], household.ledger


def test_the_scam_headline_carries_the_real_numbers_in_hindi():
    event, ledger = only(scam_afternoon())
    headline = hindi.headline(event)
    assert "₹12,000" in headline  # the rupee sign and Indian grouping
    assert "kyc.update9@ybl" in headline
    assert "9 मिनट" in headline  # "9 minutes"
    # Devanagari, ASCII (the payee is a UPI id), and typography we use on purpose.
    assert all(ord(c) < 128 or "ऀ" <= c <= "ॿ" or c in "₹—’" for c in headline)


def test_the_facts_are_hindi_sentences_with_the_same_numbers():
    event, ledger = only(scam_afternoon())
    facts = hindi.facts(event, ledger)
    assert len(facts) == len(__import__("munshi.verdict", fromlist=["x"]).facts_for(event, ledger))
    assert any("+919811234567" in f for f in facts)
    assert any("₹12,000" in f for f in facts)


def test_every_kind_has_hindi_options_and_steps():
    for groups, choice in (((scam_afternoon(),), "report"), ((double_charge(),), "dispute"), ((netflix(),), "keep")):
        event, ledger = only(*groups)
        options = hindi.options(event.kind)
        assert options and all(len(o) == 2 and o[1].strip() for o in options)
        steps = hindi.steps(event, choice)
        assert steps and all(s.strip() for s in steps)
    assert "1930" in " ".join(hindi.steps(only(scam_afternoon())[0], "report"))


def test_a_card_carries_its_hindi_with_it(tmp_path):
    household = Household.from_messages("meera", phone(scam_afternoon()), now=NOW)
    event = household.events[0]
    runner = Runner(tmp_path, household, model=Scripted([
        ("tool", "investigate_payment", {"event_id": event.id}),
        ("tool", "ask_household", {"event_id": event.id})]))
    runner.handle(event)
    (card,) = Inbox(tmp_path / "inbox.json").pending()
    assert "₹12,000" in card.hi["headline"]
    assert card.hi["evidence"] and len(card.hi["options"]) == len(card.options)

    done = Runner(tmp_path, household, model=Scripted([("text", "ok")])).decide(card.id, "report")
    assert "1930" in done.hi["outcome"]
    assert "अभी" in done.hi["outcome"]  # "abhi": call now
