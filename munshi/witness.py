"""The witness: bank and UPI messages in, events out. No model, no network, $0.

Parsing a single message is done by `nyaya.money`, the author's earlier MIT
project, and is disclosed in the README. What is new here is the event
contract, because it is the only thing that ever leaves the phone. Message
bodies never cross it: only the fields a report needs (amount, payee, time,
bank, reference, the bank's own helpline) and, for a scam, the number the
threat came from and which of our own scam words it used.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from nyaya.money.sources import transactions as _parse
from nyaya.money.witness import SCAM_WORDS

from .ledger import Ledger, Row
from .payload import check_payload

SCAM_WINDOW = timedelta(minutes=30)
DOUBLE_WINDOW = timedelta(minutes=15)
DOUBLE_FLOOR = 100.0
REFUND_WINDOW = timedelta(days=10)
NO_REFUND_AFTER = timedelta(days=7)
RECENT = timedelta(days=30)
DUE_AHEAD_DAYS = 3
UNUSUAL_MULTIPLE = 5
UNUSUAL_FLOOR = 2000.0
NOT_RENEWABLE = frozenset({"atm", "cash"})  # regular, but there is nothing to cancel
TIME = "%Y-%m-%d %H:%M"

_REF = re.compile(r"\b(?:ref(?:erence)?(?:\s*no)?|utr|upi)\s*[:.#-]?\s*([0-9]{6,})", re.I)
_HELPLINE = re.compile(r"\bcall\s+([0-9]{8,12})\b", re.I)
_BANKS = {"HDFCBK": "HDFC Bank", "ICICIB": "ICICI Bank", "SBIINB": "SBI", "SBIPSG": "SBI",
          "AXISBK": "Axis Bank", "KOTAKB": "Kotak Mahindra Bank", "PNBSMS": "Punjab National Bank",
          "YESBNK": "Yes Bank", "IDFCFB": "IDFC First Bank", "BOBTXN": "Bank of Baroda"}


def bank_of(sender):
    code = (sender or "").strip().upper().split("-")[-1]
    return _BANKS.get(code, code)


def _first(pattern, text):
    m = pattern.search(text or "")
    return m.group(1) if m else ""


def rows_from(messages):
    """Every movement of money, as a Row that carries no message text."""
    return [Row(t.when, t.amount, t.direction, t.party, t.channel, t.account,
                bank_of(t.sender), _first(_REF, t.body), _first(_HELPLINE, t.body))
            for t in _parse(messages)]


@dataclass(frozen=True)
class Event:
    """One thing the household may need to decide about."""

    id: str
    kind: str  # scam_shaped_payment | unusual_payment | double_charge | renewal_due
    when: datetime
    amount: float
    party: str
    channel: str
    account: str
    bank: str
    ref: str
    helpline: str
    flags: tuple = ()
    evidence: dict = field(default_factory=dict)

    def as_dict(self):
        return {"id": self.id, "kind": self.kind, "when": self.when.strftime(TIME), "amount": self.amount,
                "party": self.party, "channel": self.channel, "account": self.account, "bank": self.bank,
                "ref": self.ref, "helpline": self.helpline, "flags": list(self.flags),
                "evidence": dict(self.evidence)}

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["kind"], datetime.strptime(d["when"], TIME), float(d["amount"]), d["party"],
                   d["channel"], d["account"], d["bank"], d["ref"], d["helpline"],
                   tuple(d.get("flags", ())), dict(d.get("evidence", {})))


def _event(kind, row, flags, evidence):
    key = "{0}|{1}|{2}|{3:.2f}".format(kind, row.when.strftime("%Y%m%d%H%M"), row.party, row.amount)
    return Event(hashlib.sha1(key.encode("utf-8")).hexdigest()[:12], kind, row.when, row.amount, row.party,
                 row.channel, row.account, row.bank, row.ref, row.helpline, tuple(flags), dict(evidence))


def _is_person(sender):
    s = (sender or "").strip().lstrip("+").replace("-", "").replace(" ", "")
    return s == "" or s.isdigit()


def scam_words_in(body):
    low = (body or "").lower()
    hits = [w for w in SCAM_WORDS if w in low]
    return [h for h in hits if not any(h != o and h in o for o in hits)]


def _median(values):
    values = sorted(values)
    return values[len(values) // 2] if values else 0.0


def _scam_context(row, people):
    """The nearest message from a phone number, within the window before the payment, with scam words."""
    best = None
    for m in people:
        if row.when - SCAM_WINDOW <= m["when"] <= row.when:
            words = scam_words_in(m["body"])
            if words and (best is None or m["when"] > best[0]["when"]):
                best = (m, words)
    return best


def _payments(rows, messages, now):
    outs = sorted((r for r in rows if r.direction == "out"), key=lambda r: r.when)
    usual = _median([r.amount for r in outs])
    people = [m for m in messages if _is_person(m.get("sender"))]
    paid_before = set()
    events = []
    for r in outs:
        first = r.party not in paid_before  # first time as of this payment, not over all history
        paid_before.add(r.party)
        recent = timedelta(0) <= now - r.when <= RECENT
        if not recent or not r.party or not first or r.channel == "atm":
            continue
        times = round(r.amount / usual, 1) if usual else None
        hit = _scam_context(r, people)
        if hit:
            m, words = hit
            events.append(_event("scam_shaped_payment", r,
                                 ("first_time_payee", "scam_words_within_30m", "from_unknown_number"),
                                 {"minutes_after_message": int((r.when - m["when"]).total_seconds() // 60),
                                  "scam_words": words, "suspect_contact": m["sender"],
                                  "usual_amount": usual, "times_usual": times}))
        elif usual and r.amount >= UNUSUAL_MULTIPLE * usual and r.amount >= UNUSUAL_FLOOR:
            events.append(_event("unusual_payment", r, ("first_time_payee", "unusual_amount"),
                                 {"usual_amount": usual, "times_usual": times}))
    return events


def _double_charges(rows, now):
    outs = sorted((r for r in rows if r.direction == "out"), key=lambda r: r.when)
    events = []
    for i, a in enumerate(outs):
        for b in outs[i + 1:]:
            if b.when - a.when > DOUBLE_WINDOW:
                break
            same = b.party == a.party and abs(b.amount - a.amount) < 0.5
            if not same or not a.party or a.channel == "atm" or a.amount < DOUBLE_FLOOR:
                continue
            if now - b.when > RECENT:
                continue
            refunded = any(r.direction == "in" and abs(r.amount - a.amount) < 0.5
                           and b.when <= r.when <= b.when + REFUND_WINDOW for r in rows)
            if refunded:
                continue
            flags = ("same_amount_same_party_within_15m",)
            if now - b.when >= NO_REFUND_AFTER:
                flags += ("no_refund_after_7_days",)
            events.append(_event("double_charge", b, flags, {
                "minutes_apart": int((b.when - a.when).total_seconds() // 60),
                "first_ref": a.ref, "first_time": a.when.strftime(TIME),
                "days_since": (now - b.when).days}))
    return events


def _renewals(rows, now):
    by = {}
    for r in rows:
        if r.direction == "out" and r.party and r.channel not in NOT_RENEWABLE:
            by.setdefault(r.party, []).append(r)
    events = []
    for party, rs in by.items():
        if len(rs) < 3:
            continue
        gaps = [(b.when - a.when).days for a, b in zip(rs, rs[1:])]
        gap = _median(gaps)
        if not 20 <= gap <= 40 or any(abs(g - gap) > 4 for g in gaps):
            continue
        earlier = [r.amount for r in rs[:-1]]
        usual = _median(earlier)
        if any(abs(a - usual) > 0.1 * usual for a in earlier):
            continue
        last = rs[-1]
        due = (last.when + timedelta(days=gap)).date()
        due_in = (due - now.date()).days
        if not 0 <= due_in <= DUE_AHEAD_DAYS:
            continue
        flags = ("renews_in_{0}_days".format(due_in),)
        if last.amount > usual * 1.1:
            flags += ("price_up",)
        events.append(_event("renewal_due", last, flags, {
            "due_on": due.isoformat(), "due_in_days": due_in, "usual_amount": usual,
            "last_amount": last.amount, "times_seen": len(rs), "every_days": gap}))
    return events


def detect(messages, now=None, prefs=None):
    """Every event worth a decision, oldest first. Trusted payees and handled events are skipped."""
    rows = rows_from(messages)
    if not rows:
        return []
    now = now or max(m["when"] for m in messages)
    prefs = prefs or {}
    trusted = set(prefs.get("trusted", ()))
    handled = set(prefs.get("handled", ()))
    payments = _payments(rows, messages, now)
    flagged = {e.party for e in payments}
    # Paying a scammer twice is not a merchant's double charge; the scam event covers it.
    doubles = [e for e in _double_charges(rows, now) if e.party not in flagged]
    events = payments + doubles + _renewals(rows, now)
    kept = [e for e in events if e.party not in trusted and e.id not in handled]
    return sorted(kept, key=lambda e: e.when)


@dataclass(frozen=True)
class Household:
    """What the cloud agent is allowed to know: the ledger without text, and the events."""

    name: str
    ledger: Ledger
    events: tuple
    now: datetime

    @classmethod
    def from_messages(cls, name, messages, now=None, prefs=None):
        now = now or (max(m["when"] for m in messages) if messages else datetime.now())
        return cls(name, Ledger(rows_from(messages)), tuple(detect(messages, now=now, prefs=prefs)), now)

    def event(self, event_id):
        for e in self.events:
            if e.id == event_id:
                return e
        raise KeyError("no event {0!r} in this household".format(event_id))

    def to_payload(self):
        return {"household": self.name, "now": self.now.strftime(TIME),
                "ledger": [r.as_dict() for r in self.ledger.rows],
                "events": [e.as_dict() for e in self.events]}

    @classmethod
    def from_payload(cls, payload):
        """Refuses anything the witness could not have produced. See payload.py."""
        check_payload(payload)
        return cls(payload["household"], Ledger(Row.from_dict(r) for r in payload.get("ledger", ())),
                   tuple(Event.from_dict(e) for e in payload.get("events", ())),
                   datetime.strptime(payload["now"], TIME))
