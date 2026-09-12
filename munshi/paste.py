"""Someone's own messages, pasted into a web page.

On a phone the witness reads the SMS inbox, where every message has a sender
and a time. In a browser there is only text, so this reads what it can: blocks
separated by blank lines, an optional `from:` and `at:` line, and otherwise a
guess — a message that parses as a bank message gets a bank sender, anything
else is treated as coming from a person. Times are spread a few minutes apart,
ending now, so the last message is the one that just happened.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta

from .readers import read

BANK = "VM-HDFCBK"
STRANGER = "+910000000000"
# A pasted message has no sender id, but it usually signs itself. The complaint names the bank, so guessing
# HDFC for everyone would put the wrong bank on a police report.
BANKS = (("sbi", "AD-SBIINB"), ("state bank", "AD-SBIINB"), ("hdfc", "VM-HDFCBK"), ("icici", "JD-ICICIB"),
         ("axis", "AD-AXISBK"), ("kotak", "VM-KOTAKB"), ("bank of baroda", "AD-BOBTXN"),
         ("punjab national", "AD-PNBSMS"), ("pnb", "AD-PNBSMS"), ("yes bank", "VM-YESBNK"),
         ("idfc", "VM-IDFCFB"))
MAX_TEXT = 20_000
MAX_BLOCKS = 40
SPACING = timedelta(minutes=9)

_FROM = re.compile(r"^\s*from\s*:\s*(\S{1,20})\s*$", re.I | re.M)
_AT = re.compile(r"^\s*at\s*:\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4}\s+[0-9]{1,2}:[0-9]{2})\s*$", re.I | re.M)
_FORMATS = ("%d/%m/%Y %H:%M", "%d/%m/%y %H:%M", "%d-%m-%Y %H:%M", "%d-%m-%y %H:%M")


def _time(text):
    for fmt in _FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _bank_of(body):
    """The bank this message signs itself as, so the complaint names the right one."""
    low = body.lower()
    found = [(low.find(word), sender) for word, sender in BANKS if word in low]
    return min(found)[1] if found else BANK


def _block(text, when):
    sender = (_FROM.search(text) or [None, ""])[1] if _FROM.search(text) else ""
    stamp = _AT.search(text)
    said = _time(stamp.group(1)) if stamp else None
    body = _AT.sub("", _FROM.sub("", text)).strip()
    if not sender:
        sender = _bank_of(body) if read(when, BANK, body) else STRANGER
    return {"when": said or when, "sender": sender, "body": body}


def messages_from_text(text, now=None):
    """The pasted thread, as the witness's messages. Raises if nothing in it moves money."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("paste a bank message first")
    if len(text) > MAX_TEXT:
        raise ValueError("that is too long to paste; a few messages is enough")
    now = (now or datetime.now()).replace(second=0, microsecond=0)
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]
    if len(blocks) > MAX_BLOCKS:
        raise ValueError("that is too long to paste; a few messages is enough")
    messages = []
    for i, block in enumerate(reversed(blocks)):  # the last pasted message is the most recent
        messages.insert(0, _block(block, now - SPACING * i))
    if not any(read(m["when"], m["sender"], m["body"]) for m in messages):
        raise ValueError("none of that reads as a bank message about a payment")
    return messages
