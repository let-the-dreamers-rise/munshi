"""Text pasted by a person, read the way people actually paste it."""

from datetime import datetime

import pytest

from munshi.paste import messages_from_text
from munshi.witness import detect

NOW = datetime(2026, 9, 12, 15, 0)
THREAT = "Dear customer your SBI account will be BLOCKED today. Update KYC immediately."
PAID = ("Sent Rs.12000.00 From HDFC Bank A/C *4521 To kyc.update9@ybl On 12/09/26 Ref 624511873920 "
        "Not You? Call 18002586161")


def test_messages_pasted_on_consecutive_lines_are_still_two_messages():
    """Nobody puts a blank line between two SMS they just copied off a phone."""
    messages = messages_from_text(THREAT + "\n" + PAID, now=NOW)
    assert len(messages) == 2
    assert messages[0]["sender"].startswith("+")  # the threat came from a person
    assert detect(messages, now=NOW)[0].kind == "scam_shaped_payment"


def test_a_blank_line_between_them_works_the_same_way():
    messages = messages_from_text(THREAT + "\n\n" + PAID, now=NOW)
    assert len(messages) == 2
    assert detect(messages, now=NOW)[0].kind == "scam_shaped_payment"


def test_one_message_wrapped_over_two_lines_stays_one_message():
    wrapped = "Sent Rs.12000.00 From HDFC Bank A/C *4521 To kyc.update9@ybl\nOn 12/09/26 Ref 624511873920"
    messages = messages_from_text(wrapped, now=NOW)
    assert len(messages) == 1
    assert "624511873920" in messages[0]["body"]


def test_the_from_and_at_lines_still_work_on_a_single_block():
    messages = messages_from_text("from: +919811234567\n" + THREAT + "\n\n" + PAID, now=NOW)
    assert messages[0]["sender"] == "+919811234567"


def test_junk_says_so():
    with pytest.raises(ValueError):
        messages_from_text("hello how are you", now=NOW)
