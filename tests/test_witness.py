"""The witness turns messages into events, and nothing else crosses the wire."""

import json

from munshi.witness import Household, detect
from tests.fixtures import NOW, atm_every_month, double_charge, netflix, phone, scam_afternoon


def kinds(events):
    return sorted(e.kind for e in events)


def test_monthly_cash_withdrawal_is_not_a_renewal():
    assert detect(phone(atm_every_month()), now=NOW) == []


def test_scam_shaped_payment_is_an_event_with_the_fields_a_report_needs():
    events = detect(phone(scam_afternoon()), now=NOW)
    scam = [e for e in events if e.kind == "scam_shaped_payment"]
    assert len(scam) == 1
    e = scam[0]
    assert e.amount == 12000 and e.party == "kyc.update9@ybl"
    assert e.ref == "777001" and e.bank == "HDFC Bank" and e.account == "4521"
    assert e.helpline == "18002586161"
    assert "first_time_payee" in e.flags and "scam_words_within_30m" in e.flags
    assert e.evidence["minutes_after_message"] == 9
    assert e.evidence["suspect_contact"] == "+919811234567"
    assert set(e.evidence["scam_words"]) >= {"kyc", "account will be blocked"}  # the longer phrase wins
    assert e.evidence["scam_pattern"] == "kyc"


def test_quiet_phone_raises_nothing():
    assert detect(phone(), now=NOW) == []


def test_double_charge_without_refund_is_an_event():
    events = detect(phone(double_charge()), now=NOW)
    assert kinds(events) == ["double_charge"]
    e = events[0]
    assert e.amount == 540 and e.party == "Zomato"  # nyaya title-cases card merchants
    assert e.evidence["minutes_apart"] == 2
    assert "no_refund_after_7_days" in e.flags


def test_refunded_double_charge_is_not_an_event():
    from datetime import timedelta
    from tests.fixtures import credit
    charges = double_charge()
    refund = [credit(charges[1]["when"] + timedelta(days=2), 540, "ZOMATO REFUND")]
    assert detect(phone(charges, refund), now=NOW) == []


def test_renewal_due_with_a_price_rise():
    events = detect(phone(netflix()), now=NOW)
    assert kinds(events) == ["renewal_due"]
    e = events[0]
    assert e.party == "Netflix" and e.amount == 649
    assert e.evidence["usual_amount"] == 499
    assert 0 <= e.evidence["due_in_days"] <= 3
    assert "price_up" in e.flags


def test_trusted_payee_is_not_raised_again():
    events = detect(phone(scam_afternoon()), now=NOW, prefs={"trusted": ["kyc.update9@ybl"]})
    assert events == []


def test_handled_event_is_not_raised_again():
    first = detect(phone(scam_afternoon()), now=NOW)
    again = detect(phone(scam_afternoon()), now=NOW, prefs={"handled": [first[0].id]})
    assert again == []


def test_event_ids_are_stable():
    a = detect(phone(scam_afternoon(), double_charge()), now=NOW)
    b = detect(phone(scam_afternoon(), double_charge()), now=NOW)
    assert [e.id for e in a] == [e.id for e in b]


def test_the_payload_that_leaves_the_phone_carries_no_message_text():
    household = Household.from_messages("meera", phone(scam_afternoon(), double_charge()), now=NOW)
    wire = json.dumps(household.to_payload())
    assert "KYC immediately" not in wire
    assert "sbi-kyc-update" not in wire
    assert "Not You?" not in wire
    assert "Avl limit" not in wire
    back = Household.from_payload(json.loads(wire))
    assert [e.id for e in back.events] == [e.id for e in household.events]
    assert back.ledger.payee_history("chaiwala@ybl")["times_paid"] > 30


def test_payee_history_of_a_stranger():
    household = Household.from_messages("meera", phone(scam_afternoon()), now=NOW)
    h = household.ledger.payee_history("kyc.update9@ybl")
    assert h["times_paid"] == 1 and h["total_paid"] == 12000
    assert household.ledger.payee_history("nobody@ybl")["times_paid"] == 0
