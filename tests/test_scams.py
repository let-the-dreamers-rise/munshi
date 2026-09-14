# -*- coding: utf-8 -*-
"""Munshi names the scam it is looking at, in both languages and on the report."""

from munshi import hindi, scams
from munshi.complaints import cybercrime_report
from munshi.verdict import rule_verdict
from munshi.witness import Household, detect
from tests.fixtures import NOW, digital_arrest_afternoon, phone, scam_afternoon

DIGITAL_ARREST = ("Mumbai Cyber Cell. A parcel in your name contains narcotics. An FIR is registered and you "
                  "are under DIGITAL ARREST. Do not disconnect the video call.")
ELECTRICITY = ("Dear consumer your electricity will be disconnected tonight at 9.30 pm because your previous "
               "month bill is not updated. Contact our officer immediately.")
COURIER = "Your FedEx parcel is held at customs. Pay the customs duty to release the shipment today."
JOB = "Part time job from home. Complete a simple task on Telegram and earn daily income of Rs 3000."
PLAIN_THREAT = "Your account will be blocked immediately. Click the link to verify."


def test_the_digital_arrest_script_is_named():
    words = scams.words_in(DIGITAL_ARREST)
    assert "digital arrest" in words
    pattern = scams.classify(words)
    assert pattern.name == "digital_arrest"
    assert pattern.en == "the digital arrest scam"


def test_a_longer_hit_swallows_the_word_inside_it():
    assert "arrest" not in scams.words_in(DIGITAL_ARREST)  # 'digital arrest' already says it


def test_electricity_and_courier_and_job_scripts_are_named():
    assert scams.classify(scams.words_in(ELECTRICITY)).name == "electricity"
    assert scams.classify(scams.words_in(COURIER)).name == "courier"
    assert scams.classify(scams.words_in(JOB)).name == "job_task"


def test_a_threat_with_no_script_is_left_unnamed():
    words = scams.words_in(PLAIN_THREAT)
    assert words and scams.classify(words) is None  # still evidence, just not a named script


def test_every_pattern_word_is_in_the_vocabulary_the_witness_looks_for():
    for pattern in scams.PATTERNS:
        assert set(pattern.words) <= scams.VOCABULARY


def test_the_witness_records_which_scam_it_is():
    events = detect(phone(digital_arrest_afternoon()), now=NOW)
    scam = [e for e in events if e.kind == "scam_shaped_payment"]
    assert len(scam) == 1
    assert scam[0].evidence["scam_pattern"] == "digital_arrest"
    assert scam[0].amount == 85000 and scam[0].party == "verify.rbi41@okaxis"


def test_the_named_scam_survives_the_payload_check():
    house = Household.from_messages("meera", phone(digital_arrest_afternoon()), now=NOW)
    back = Household.from_payload(house.to_payload())
    assert back.events[0].evidence["scam_pattern"] == "digital_arrest"


def test_the_card_names_the_scam_in_english_and_hindi():
    event = detect(phone(digital_arrest_afternoon()), now=NOW)[0]
    assert "digital arrest scam" in rule_verdict(event).headline
    assert "डिजिटल अरेस्ट" in hindi.headline(event)


def test_the_kyc_card_still_says_kyc():
    event = detect(phone(scam_afternoon()), now=NOW)[0]
    assert "KYC scam" in rule_verdict(event).headline
    assert "KYC" in hindi.headline(event)


def test_one_pasted_payment_is_not_compared_with_itself():
    """A paste of two messages has no 'usual payment', so the card must not invent one."""
    events = detect(digital_arrest_afternoon(), now=NOW)
    assert len(events) == 1
    assert events[0].evidence["times_usual"] is None


def test_the_police_report_says_which_script_the_message_followed():
    event = detect(phone(digital_arrest_afternoon()), now=NOW)[0]
    story = cybercrime_report(event)["fields"]["What happened"]
    assert "the pattern of the digital arrest scam" in story
    assert "85,000" in story


def test_one_ordinary_word_is_not_enough_to_name_a_script():
    """A friend asking about a parcel must not be called the courier scam."""
    words = scams.words_in("Please send 500 for the parcel today, urgent")
    assert "parcel" in words and "urgent" in words
    assert scams.classify(words) is None


def test_one_distinctive_word_is_enough():
    assert scams.classify(scams.words_in("Update your KYC today")).name == "kyc"
