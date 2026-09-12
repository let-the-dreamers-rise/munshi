"""The hosted demo: no install, no server-side state, and it works on a real pasted SMS."""

import json
from datetime import datetime, timedelta, timezone

import pytest

from munshi.paste import messages_from_text
from munshi.portable import dump_home, load_home
from munshi.web import handle

NOW = datetime(2026, 9, 12, 15, 0)

REAL_PASTE = """from: +919811234567
Dear customer your SBI account will be BLOCKED today. Update KYC immediately at http://sbi-kyc-update.in

Sent Rs.12000.00 From HDFC Bank A/C *4521 To kyc.update9@ybl On 12/09/26 Ref 624511873920
Not You? Call 18002586161/SMS BLOCK UPI to 7308080808
"""


def test_a_pasted_thread_becomes_messages_with_a_bank_and_a_stranger():
    messages = messages_from_text(REAL_PASTE, now=NOW)
    assert len(messages) == 2
    threat, debit = messages
    assert threat["sender"] == "+919811234567" and "KYC" in threat["body"]
    assert threat["when"] < debit["when"] <= NOW
    assert debit["sender"].endswith("HDFCBK")  # inferred: it parses as a bank message


def test_an_explicit_time_is_kept():
    messages = messages_from_text("at: 12/09/2026 14:55\nSent Rs.500.00 To x@ybl Ref 9001", now=NOW)
    assert messages[0]["when"] == datetime(2026, 9, 12, 14, 55)


def test_nothing_usable_is_a_clear_error():
    with pytest.raises(ValueError, match="bank message"):
        messages_from_text("hello how are you", now=NOW)


def test_the_clock_follows_the_reader_not_the_server():
    """A server in UTC must still date the cards in the reader's own wall clock, or the
    first-hour countdown is hours wrong for everyone who is not on UTC."""
    ist = handle({"action": "start", "offset_minutes": -330})  # India, UTC+5:30
    utc = handle({"action": "start", "offset_minutes": 0})
    scam = lambda out: [c for c in out["state"]["cards"] if c["kind"] == "scam_shaped_payment"][0]
    apart = datetime.strptime(scam(ist)["when"], "%Y-%m-%d %H:%M") - datetime.strptime(scam(utc)["when"], "%Y-%m-%d %H:%M")
    assert apart == timedelta(minutes=330)


def test_the_audit_log_is_stamped_in_the_reader_s_clock_too():
    out = handle({"action": "start", "offset_minutes": -330})
    rows = out["state"]["audit"]
    assert rows
    server = datetime.now(timezone.utc).replace(tzinfo=None)
    stamped = datetime.fromisoformat(rows[0]["at"])
    assert timedelta(minutes=320) < stamped - server < timedelta(minutes=340)


def test_a_silly_offset_is_ignored():
    out = handle({"action": "start", "offset_minutes": 99999})
    assert out["state"]["cards"]


def test_a_pasted_scam_produces_a_card_with_the_real_reference():
    out = handle({"action": "start", "sms": REAL_PASTE})
    (card,) = [c for c in out["state"]["cards"] if c["kind"] == "scam_shaped_payment"]
    assert card["drafts"]["cybercrime_report"]["fields"]["Transaction ID / UTR"] == "624511873920"
    assert card["drafts"]["bank_dispute"]["helpline"] == "18002586161"
    assert "12,000" in card["headline"]


def test_the_session_travels_to_the_browser_and_back(tmp_path):
    started = handle({"action": "start"})
    blob = started["session"]
    assert isinstance(blob, str) and len(blob) < 200_000
    (card,) = [c for c in started["state"]["cards"] if c["kind"] == "scam_shaped_payment"]
    assert card["interrupt_id"]

    # A different request, with nothing kept on the server but what the browser sent back.
    done = handle({"action": "decide", "session": blob, "card": card["id"], "choice": "report"})
    after = [c for c in done["state"]["cards"] if c["id"] == card["id"]][0]
    assert after["status"] == "decided" and "1930" in after["outcome"]
    assert done["session"] != blob


def test_a_home_survives_a_round_trip(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "b.json").write_text('{"x": 1}', encoding="utf-8")
    (tmp_path / "top.jsonl").write_text('{"y": 2}\n', encoding="utf-8")
    back = tmp_path / "back"
    load_home(dump_home(tmp_path), back)
    assert json.loads((back / "a" / "b.json").read_text(encoding="utf-8")) == {"x": 1}
    assert (back / "top.jsonl").read_text(encoding="utf-8") == '{"y": 2}\n'


def test_a_tampered_session_is_refused():
    with pytest.raises(ValueError, match="session"):
        handle({"action": "decide", "session": "not-a-session", "card": "card-000000000000", "choice": "report"})


def test_a_session_cannot_write_outside_its_home():
    poisoned = dump_home_with({"../../escape.json": "{}"})
    with pytest.raises(ValueError, match="path"):
        handle({"action": "decide", "session": poisoned, "card": "card-000000000000", "choice": "report"})


def dump_home_with(files):
    from munshi.portable import pack
    return pack(files)


def test_messages_with_nothing_wrong_are_a_quiet_answer_not_an_error():
    """Ordinary messages get the empty state, not a red line: finding nothing is good news."""
    sms = ("Sent Rs.250.00 From HDFC Bank A/C *4521 To chaiwala@ybl On 12/09/26 Ref 624511873900\n\n"
           "Rs.540.00 spent on HDFC Bank Card x9012 at BIGBASKET on 12-09-26. Avl limit Rs.1,20,000")
    out = handle({"action": "start", "sms": sms})
    assert out["state"]["cards"] == []
    assert out["state"]["watched"]["payments"] == 2


def test_a_ping_wakes_the_function_and_says_nothing_else():
    assert handle({"action": "ping"}) == {"ready": True}


def test_a_giant_paste_is_refused():
    with pytest.raises(ValueError, match="too long"):
        handle({"action": "start", "sms": "x" * 200_000})
