"""The shape of everything that crosses from the phone to the agent.

The witness only ever produces these shapes. Anything else arriving at the
agent (a hand-built payload, a tampered one, a payee name written to look like
an instruction) is refused here, field by field, before a model sees it.
"""

from __future__ import annotations

import re
from datetime import date, datetime

from nyaya.money.witness import SCAM_WORDS

TIME = "%Y-%m-%d %H:%M"
KINDS = frozenset({"scam_shaped_payment", "unusual_payment", "double_charge", "renewal_due"})
MAX_ROWS = 20000
MAX_EVENTS = 200
MAX_AMOUNT = 1e9

_PARTY = re.compile(r"^[A-Za-z0-9@._&' -]{0,90}$")  # a UPI id or a merchant name, as the parser emits them
_BANK = re.compile(r"^[A-Za-z0-9 &.]{0,40}$")
_WORD = re.compile(r"^[a-z_]{1,16}$")
_FLAG = re.compile(r"^[a-z0-9_]{1,40}$")
_ID = re.compile(r"^[0-9a-f]{12}$")
_NAME = re.compile(r"^[A-Za-z0-9_-]{1,40}$")
_PHONE = re.compile(r"^(\+?[0-9]{6,15})?$")


def _digits(n):
    return re.compile(r"^[0-9]{0,%d}$" % n)


def _fail(where, field, why):
    raise ValueError("{0}: '{1}' {2}".format(where, field, why))


def _text(where, field, value, pattern, why):
    if not isinstance(value, str) or not pattern.match(value):
        _fail(where, field, why)
    return value


def _number(where, field, value, lo=0, hi=MAX_AMOUNT, whole=False):
    kinds = (int,) if whole else (int, float)
    if isinstance(value, bool) or not isinstance(value, kinds) or not lo <= value <= hi:
        _fail(where, field, "must be a number from {0} to {1}".format(lo, hi))
    return value


def _time(where, field, value):
    try:
        return datetime.strptime(value, TIME)
    except (TypeError, ValueError):
        _fail(where, field, "must look like 2026-09-12 15:00")


def _money_fields(where, d):
    _time(where, "when", d.get("when"))
    _number(where, "amount", d.get("amount"))
    _text(where, "party", d.get("party", ""), _PARTY, "is not a payee name or UPI id")
    _text(where, "channel", d.get("channel", "other"), _WORD, "is not a payment channel")
    _text(where, "account", d.get("account", ""), _digits(6), "must be the last digits of an account")
    _text(where, "bank", d.get("bank", ""), _BANK, "is not a bank name")
    _text(where, "ref", d.get("ref", ""), _digits(24), "must be digits")
    _text(where, "helpline", d.get("helpline", ""), _digits(14), "must be digits")


def check_row(d, i=0):
    where = "ledger row {0}".format(i)
    if not isinstance(d, dict):
        _fail(where, "row", "must be an object")
    _money_fields(where, d)
    if d.get("direction") not in ("in", "out"):
        _fail(where, "direction", "must be 'in' or 'out'")
    return d


def _words(where, field, value):
    if not isinstance(value, list) or len(value) > 12 or not all(w in SCAM_WORDS for w in value):
        _fail(where, field, "must be words from Munshi's own scam list")
    return value


def _maybe_number(where, field, value):
    return value if value is None else _number(where, field, value, hi=1e6)


EVIDENCE = {
    "minutes_after_message": lambda w, f, v: _number(w, f, v, hi=60, whole=True),
    "scam_words": _words,
    "suspect_contact": lambda w, f, v: _text(w, f, v, _PHONE, "must be a phone number"),
    "usual_amount": lambda w, f, v: _number(w, f, v),
    "times_usual": _maybe_number,
    "minutes_apart": lambda w, f, v: _number(w, f, v, hi=60, whole=True),
    "first_ref": lambda w, f, v: _text(w, f, v, _digits(24), "must be digits"),
    "first_time": _time,
    "days_since": lambda w, f, v: _number(w, f, v, hi=400, whole=True),
    "due_on": lambda w, f, v: _date(w, f, v),
    "due_in_days": lambda w, f, v: _number(w, f, v, hi=31, whole=True),
    "last_amount": lambda w, f, v: _number(w, f, v),
    "times_seen": lambda w, f, v: _number(w, f, v, hi=10000, whole=True),
    "every_days": lambda w, f, v: _number(w, f, v, hi=400),
}


def _date(where, field, value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        _fail(where, field, "must be a date like 2026-09-12")


def check_event(d, i=0):
    where = "event {0}".format(i)
    if not isinstance(d, dict):
        _fail(where, "event", "must be an object")
    _text(where, "id", d.get("id"), _ID, "must be a 12-character event id")
    if d.get("kind") not in KINDS:
        _fail(where, "kind", "must be one of " + ", ".join(sorted(KINDS)))
    _money_fields(where, d)
    flags = d.get("flags", [])
    if not isinstance(flags, list) or len(flags) > 8 or not all(isinstance(f, str) and _FLAG.match(f) for f in flags):
        _fail(where, "flags", "must be up to 8 short flags")
    evidence = d.get("evidence", {})
    if not isinstance(evidence, dict) or set(evidence) - set(EVIDENCE):
        _fail(where, "evidence", "has a field Munshi does not know")
    for key, value in evidence.items():
        EVIDENCE[key](where, key, value)
    return d


def check_payload(p):
    if not isinstance(p, dict):
        raise ValueError("the household payload must be an object")
    _text("household", "household", p.get("household"), _NAME, "must be a short name")
    _time("household", "now", p.get("now"))
    ledger, events = p.get("ledger", []), p.get("events", [])
    if not isinstance(ledger, list) or not isinstance(events, list):
        raise ValueError("household: 'ledger' and 'events' must be lists")
    if len(ledger) > MAX_ROWS or len(events) > MAX_EVENTS:
        raise ValueError("household payload is too large")
    for i, row in enumerate(ledger):
        check_row(row, i)
    for i, event in enumerate(events):
        check_event(event, i)
    return p
