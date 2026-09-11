"""The model may weigh the facts and write a headline; it may not invent numbers or leak codes."""

from munshi.verdict import investigate, rule_verdict
from munshi.witness import Household
from tests.fixtures import NOW, phone, scam_afternoon
from tests.scripted import Scripted


def scam():
    household = Household.from_messages("meera", phone(scam_afternoon()), now=NOW)
    return household.events[0], household.ledger


def verdict_says(headline):
    return Scripted([("tool", "Verdict", {"kind": "likely_scam", "confidence": 0.9,
                                          "headline": headline, "recommended": "report_now"})])


def test_a_good_model_headline_is_kept():
    event, ledger = scam()
    headline = "Rs 12,000 went to a stranger nine minutes after a KYC threat. Report it now."
    verdict, _, who = investigate(event, ledger, verdict_says(headline))
    assert verdict.headline == headline and who == "model"


def test_a_headline_that_leaks_a_code_falls_back_to_the_rules():
    event, ledger = scam()
    verdict, _, who = investigate(event, ledger, verdict_says("Rs 12,000 to a first-time payee: report_now."))
    assert verdict.headline == rule_verdict(event).headline
    assert verdict.recommended == "report_now" and who == "model (headline from rules)"


def test_a_model_that_fails_is_named_in_the_audit_trail():
    event, ledger = scam()
    verdict, _, who = investigate(event, ledger, Scripted([("text", "I think it is a scam.")]))
    assert verdict == rule_verdict(event)
    assert who.startswith("rules (the model failed: ") and who.endswith("Exception)")


def test_a_headline_with_the_wrong_amount_falls_back_to_the_rules():
    event, ledger = scam()
    verdict, _, _ = investigate(event, ledger, verdict_says("Rs 21,000 went to a stranger. Report it."))
    assert verdict.headline == rule_verdict(event).headline
