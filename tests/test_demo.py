"""The demo household: Meera's ordinary months from nyaya, and a bad afternoon that is happening now."""

from datetime import datetime, timedelta

from munshi.demo import demo_household, demo_messages

NOW = datetime(2026, 9, 14, 16, 40)


def test_the_demo_has_one_of_each_event_and_the_scam_is_fresh():
    household = demo_household(now=NOW)
    kinds = sorted(e.kind for e in household.events)
    assert kinds == ["double_charge", "renewal_due", "scam_shaped_payment"]
    scam = [e for e in household.events if e.kind == "scam_shaped_payment"][0]
    assert NOW - scam.when == timedelta(minutes=5)
    assert scam.evidence["minutes_after_message"] == 9


def test_the_demo_has_no_future_messages_and_months_of_history():
    messages = demo_messages(now=NOW)
    assert max(m["when"] for m in messages) <= NOW
    assert (NOW - min(m["when"] for m in messages)).days >= 90


def test_the_payload_that_leaves_the_phone_has_no_message_text():
    payload = str(demo_household(now=NOW).to_payload())
    assert "Update KYC" not in payload and "Avl bal" not in payload and "http" not in payload
