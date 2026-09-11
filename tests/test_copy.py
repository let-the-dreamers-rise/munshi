"""What a tired parent reads. Plain sentences, real numbers, no machine phrasing."""

from munshi.complaints import cybercrime_report
from munshi.verdict import facts_for, rule_verdict
from munshi.witness import Household
from tests.fixtures import NOW, double_charge, netflix, phone, scam_afternoon


def only(*groups):
    household = Household.from_messages("meera", phone(*groups), now=NOW)
    (event,) = household.events
    return event, household.ledger


def test_the_scam_headline_names_the_scam_without_repeating_the_evidence():
    event, ledger = only(scam_afternoon())
    headline = rule_verdict(event).headline
    assert headline.startswith("Rs 12,000 went to kyc.update9@ybl, someone you have never paid")
    assert "KYC scam" in headline and "'" not in headline
    assert any("58 times" in f or "times the household" in f for f in facts_for(event, ledger))
    assert not any(".0 times" in f for f in facts_for(event, ledger))


def test_the_story_on_the_police_report_reads_as_one_person_speaking():
    event, _ = only(scam_afternoon())
    story = cybercrime_report(event)["fields"]["What happened"]
    assert "Rs 12,000 left my HDFC Bank account" in story
    assert "'kyc', 'blocked' and 'immediately'" in story or "'kyc' and 'blocked'" in story
    assert "rs 12" not in story


def test_a_double_charge_headline_says_what_you_are_owed():
    event, ledger = only(double_charge())
    assert rule_verdict(event).headline.startswith("You may be owed Rs 540")


def test_renewal_copy_uses_words_for_days_and_dates():
    event, ledger = only(netflix())
    text = rule_verdict(event).headline + " ".join(facts_for(event, ledger))
    assert "day(s)" not in text and "2026-" not in text
    assert "Rs 649" in text and "Rs 499" in text
