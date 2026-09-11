"""Drafts carry every field a report needs, the golden-hour deadline, and no message text."""

import json

from munshi.complaints import bank_dispute, cybercrime_report, upi_help_complaint
from munshi.witness import detect
from tests.fixtures import NOW, double_charge, phone, scam_afternoon


def scam():
    return [e for e in detect(phone(scam_afternoon()), now=NOW) if e.kind == "scam_shaped_payment"][0]


def test_cybercrime_report_has_the_golden_hour_and_the_fields():
    r = cybercrime_report(scam())
    assert "1930" in r["text"]
    assert r["call_before"].startswith("15:55")  # paid 14:55, one hour later
    f = r["fields"]
    assert f["Amount (Rs)"] == "12,000"
    assert f["Transaction ID / UTR"] == "777001"
    assert f["Suspect UPI ID"] == "kyc.update9@ybl"
    assert f["Suspect phone"] == "+919811234567"
    assert f["Bank"] == "HDFC Bank" and f["Account (last digits)"] == "4521"


def test_bank_dispute_is_a_letter_with_the_reference():
    d = bank_dispute(scam())
    assert "777001" in d["body"] and "4521" in d["body"] and "12,000" in d["body"]
    assert d["helpline"] == "18002586161"
    assert d["subject"].startswith("Unauthorised UPI")


def test_double_charge_dispute_says_debited_twice():
    e = detect(phone(double_charge()), now=NOW)[0]
    d = bank_dispute(e)
    assert "twice" in d["subject"].lower()
    u = upi_help_complaint(e)
    assert u["issue"] == "Amount debited twice"


def test_no_draft_carries_message_text():
    e = scam()
    blob = json.dumps([cybercrime_report(e), bank_dispute(e), upi_help_complaint(e)])
    assert "KYC immediately" not in blob and "sbi-kyc-update" not in blob
