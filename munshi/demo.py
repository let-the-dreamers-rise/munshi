"""Meera's phone, for the demo.

Her ordinary hundred days (chai, groceries, rent, a friend who keeps asking
for cab money) come from `nyaya.money.sources.demo_messages`, the author's
earlier MIT project. Its own scam, twelve days old, is removed. In its place
Munshi adds the afternoon the demo is about, dated from the real clock: a
KYC threat, and nine minutes later Rs 12,000 to a stranger, five minutes ago.
Also a Zomato order charged twice last week and a Netflix renewal that went up.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from nyaya.money.sources import demo_messages as ordinary_months

from .witness import Household

BANK = "VM-HDFCBK"
SCAMMER = "+919811234567"
OLD_SCAM = ("kyc.update9@ybl", SCAMMER)


def _msg(when, sender, body):
    return {"when": when, "sender": sender, "body": body}


def _upi(when, amount, party, ref):
    return _msg(when, BANK, ("Sent Rs.{0:.2f} From HDFC Bank A/C *4521 To {1} On {2} Ref {3} "
                             "Not You? Call 18002586161/SMS BLOCK UPI to 7308080808").format(
        amount, party, when.strftime("%d/%m/%y"), ref))


def _card(when, amount, merchant):
    return _msg(when, BANK, "Rs.{0:.2f} spent on HDFC Bank Card x9012 at {1} on {2}. Avl limit Rs.1,20,000".format(
        amount, merchant, when.strftime("%d-%m-%y")))


def bad_afternoon(now):
    paid = now - timedelta(minutes=5)
    return [
        _msg(paid - timedelta(minutes=9), SCAMMER,
             "Dear customer your SBI account will be BLOCKED today. Update KYC immediately at "
             "http://sbi-kyc-update.in or call 9811234567"),
        _upi(paid, 12000, "kyc.update9@ybl", 624511873920),
    ]


def last_week(now):
    first = (now - timedelta(days=8)).replace(hour=20, minute=14, second=0, microsecond=0)
    return [_card(first, 540, "ZOMATO"), _card(first + timedelta(minutes=2), 540, "ZOMATO")]


def netflix(now):
    day = now.replace(hour=9, minute=0, second=0, microsecond=0)
    return [_card(day - timedelta(days=91), 499, "NETFLIX"), _card(day - timedelta(days=61), 499, "NETFLIX"),
            _card(day - timedelta(days=30), 649, "NETFLIX")]


def demo_messages(now=None, seed=7):
    now = (now or datetime.now()).replace(second=0, microsecond=0)
    months = [m for m in ordinary_months(100, now, seed)
              if m["when"] <= now and not any(s in m["body"] or s == m["sender"] for s in OLD_SCAM)]
    return sorted(months + last_week(now) + netflix(now) + bad_afternoon(now), key=lambda m: m["when"])


def demo_household(now=None, name="meera"):
    now = (now or datetime.now()).replace(second=0, microsecond=0)
    return Household.from_messages(name, demo_messages(now), now=now)
