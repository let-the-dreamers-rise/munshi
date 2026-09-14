"""The bank formats `nyaya.money` cannot read on its own.

The parser Munshi builds on reads most Indian bank SMS, but not all of them,
and a family whose bank is not covered is a family Munshi cannot help. So this
module is a thin repair layer over it, kept separate so the dependency stays
pinned and unmodified:

* an amount with no currency mark at all -- SBI's UPI alert says
  "debited by 2500.0", and SBI is the largest bank in the country;
* a payee the bank's template hides -- "trf to RAMESH KUMAR Refno ...",
  or a card line that puts the merchant between the time and "Avl Lmt";
* a payee name with the template's own words stuck to it;
* and a mandate notice, which says "will be debited" and is a warning about
  Tuesday, not money that has moved.

tests/test_readers.py holds the corpus of real formats this is judged against.
"""

from __future__ import annotations

import re

from nyaya.money.parse import Transaction, account_of, channel_of, is_bank_sender, parse_message

FUTURE = re.compile(r"\bwill\s+be\s+(?:debited|credited|deducted|charged)\b", re.I)
_SENTENCE = re.compile(r"[^.;\n]+[.;\n]?")

# An amount with no Rs/INR in front of it. The number must follow the direction
# word immediately, so a reference number ("debited by UPI:6245...") cannot pass.
BARE = (
    (re.compile(r"\b(?:debited|debit|withdrawn)\s+(?:by|for|with)\s+([0-9][0-9,]*(?:\.[0-9]{1,2})?)\b", re.I), "out"),
    (re.compile(r"\b(?:credited|credit)\s+(?:by|with)\s+([0-9][0-9,]*(?:\.[0-9]{1,2})?)\b", re.I), "in"),
)

# Payees the templates hide. Tried in order, first hit wins.
PARTIES = (
    re.compile(r"\btrf\s+to\s+([A-Za-z][A-Za-z0-9 .&'-]{2,40}?)(?=\s+(?:ref|upi|on|dt|bal)|[.,;(]|$)", re.I),
    re.compile(r"\b\d{1,2}:\d{2}\s+([A-Z][A-Z0-9 .&'-]{2,30}?)\s+(?=avl\b)", re.I),  # Axis card line
    re.compile(r"\bto\s+([A-Za-z][A-Za-z0-9 .&'-]{2,40}?)(?=\s+(?:ref|upi|txn|on|dt)|[.,;(]|$)", re.I),
)

# Template words that end a payee name: everything from here on belongs to the bank, not the payee.
TRAILING = re.compile(r"\s+(?:from|via|on|ref|refno|upi|vpa|avl|txn|bal|dt|not)\b.*$", re.I)
NOISE = frozenset({"vpa", "upi", "a/c", "ac", "account", "bank", "the", "you", "your"})


def _titled(name):
    name = " ".join(name.split()).strip(" .-")
    return name.title() if name.isupper() else name


def _clean(party):
    """A payee name with the bank's own words taken off the end."""
    if "@" in party:
        return party
    name = _titled(TRAILING.sub("", party))
    return "" if name.lower() in NOISE or len(name) < 3 else name


def _party(body):
    for pattern in PARTIES:
        found = pattern.search(body)
        if found:
            name = _clean(found.group(1))
            if name:
                return name
    return ""


def _bare(when, sender, body):
    """A payment whose amount the message never marks as money."""
    for pattern, direction in BARE:
        found = pattern.search(body)
        if not found:
            continue
        try:
            amount = float(found.group(1).replace(",", ""))
        except ValueError:
            continue
        if amount <= 0:
            continue
        return Transaction(when, amount, direction, _party(body), channel_of(body), account_of(body), sender, body)
    return None


def _with_party(txn, party):
    return Transaction(txn.when, txn.amount, txn.direction, party, txn.channel, txn.account, txn.sender, txn.body)


def _now_not_later(body):
    """The message without the sentence that warns about a future charge.

    One SMS often carries both -- money that has just gone, and a mandate due on Tuesday. Dropping
    the whole message would hide the payment; keeping it whole would invent one.
    """
    if not FUTURE.search(body):
        return body
    return "".join(s for s in _SENTENCE.findall(body) if not FUTURE.search(s))


def read(when, sender, body):
    """One message as a Transaction, or None if no money moved."""
    body = _now_not_later(body or "")
    if not body.strip():
        return None
    if not is_bank_sender(sender, body):
        return None
    txn = parse_message(when, sender, body)
    if txn is None:
        txn = _bare(when, sender, body)
    if txn is None:
        return None
    party = _clean(txn.party) if txn.party else _party(body)
    return txn if party == txn.party else _with_party(txn, party)


def transactions(messages):
    """Every message that records money moving, oldest first."""
    out = []
    for m in messages:
        txn = read(m["when"], m["sender"], m["body"])
        if txn is not None:
            out.append(txn)
    return out
