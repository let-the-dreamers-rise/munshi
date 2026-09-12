# -*- coding: utf-8 -*-
"""Which scam script the message is running.

The words are already evidence: a threatening message from a phone number,
minutes before a payment to a stranger, is what makes an event at all. But
Indian families are not robbed by one scam, they are robbed by a handful of
scripts, and naming the script is what lets the card say something a household
recognises -- and what 1930 asks for on the phone. So the vocabulary is
grouped. The words are matched, and the group with the most hits names the
script. If no group fits, the message is still evidence; it is simply unnamed.

Nothing here is a model. It is a list, kept in one place so it can be argued
with, added to, and tested.
"""

from __future__ import annotations

from dataclasses import dataclass

from nyaya.money.witness import SCAM_WORDS


@dataclass(frozen=True)
class Pattern:
    """One scam script, its words, and how to name it to a household."""

    name: str
    words: tuple
    en: str
    hi: str

    @property
    def en_line(self):
        return "This is how {0} works.".format(self.en)

    @property
    def hi_line(self):
        return "यह {0} का तरीका है।".format(self.hi)


# Most specific first: on a tie, the earlier script wins.
PATTERNS = (
    Pattern("digital_arrest",
            ("digital arrest", "cyber cell", "money laundering", "narcotics", "warrant", "summons",
             "video call", "cbi", "police", "arrest"),
            "the digital arrest scam", "डिजिटल अरेस्ट ठगी"),
    Pattern("screen_share",
            ("anydesk", "teamviewer", "quick support", "screen share", "screen sharing", "apk file"),
            "the screen-sharing scam", "स्क्रीन शेयर वाली ठगी"),
    Pattern("electricity",
            ("electricity", "bijli", "disconnect", "power supply", "meter"),
            "the electricity disconnection scam", "बिजली काटने वाली ठगी"),
    Pattern("courier",
            ("courier", "parcel", "customs", "customs duty", "fedex", "dhl", "shipment"),
            "the courier and customs scam", "कूरियर-कस्टम ठगी"),
    Pattern("sim_block",
            ("trai", "sim will be", "sim card will be", "mobile number will be"),
            "the SIM disconnection scam", "सिम बंद होने वाली ठगी"),
    Pattern("job_task",
            ("part time job", "work from home", "telegram", "daily income", "earn daily", "task"),
            "the task and part-time job scam", "टास्क-जॉब ठगी"),
    Pattern("investment",
            ("guaranteed return", "stock tips", "trading account", "demat", "ipo allotment", "double your money"),
            "the investment scam", "निवेश-ट्रेडिंग ठगी"),
    Pattern("loan",
            ("loan approved", "instant loan", "pre-approved loan", "processing fee"),
            "the instant loan scam", "इंस्टेंट लोन ठगी"),
    Pattern("prize",
            ("lottery", "lucky draw", "scratch card", "prize", "winner", "gift voucher"),
            "the prize and lottery scam", "लॉटरी-इनाम ठगी"),
    Pattern("refund",
            ("refund", "reversal", "cashback", "claim your amount"),
            "the fake refund scam", "नकली रिफंड ठगी"),
    Pattern("kyc",
            ("kyc", "re-kyc", "pan card", "aadhaar"),
            "the KYC scam", "KYC ठगी"),
    Pattern("otp",
            ("share otp", "otp", "cvv", "pin number", "password"),
            "the OTP theft scam", "OTP चोरी वाली ठगी"),
)

BY_NAME = {p.name: p for p in PATTERNS}

# Words that belong to no script: real evidence of a threat, but they name nothing on their own.
GENERIC = frozenset({"urgent", "immediately", "turant", "expire", "expiring", "verify", "link", "suspend",
                     "block", "blocked", "last warning", "final notice", "account will be blocked",
                     "will be deactivated"})

VOCABULARY = frozenset(GENERIC | set(SCAM_WORDS) | {w for p in PATTERNS for w in p.words})


def words_in(body):
    """Every word of Munshi's vocabulary in this message, longest hit first, none inside another."""
    low = (body or "").lower()
    hits = [w for w in VOCABULARY if w in low]
    kept = [h for h in hits if not any(h != o and h in o for o in hits)]
    return sorted(kept, key=lambda w: (-len(w), w))


def classify(words):
    """The script these words follow, or None when they follow none we know."""
    words = set(words or ())
    best, score = None, 0
    for pattern in PATTERNS:
        hits = len(words & set(pattern.words))
        if hits > score:
            best, score = pattern, hits
    return best


def named(evidence):
    """The Pattern an event's evidence names, or None. Evidence is data; unknown names are ignored."""
    return BY_NAME.get((evidence or {}).get("scam_pattern"))
