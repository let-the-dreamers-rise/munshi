"""A small, readable phone for tests: a few bank messages and one bad afternoon."""

from datetime import datetime, timedelta

NOW = datetime(2026, 9, 12, 15, 0)
HDFC = "VM-HDFCBK"


def msg(when, sender, body):
    return {"when": when, "sender": sender, "body": body}


def sent(when, amount, party, ref):
    return msg(when, HDFC, (
        "Sent Rs.{0:.2f} From HDFC Bank A/C *4521 To {1} On {2} Ref {3} "
        "Not You? Call 18002586161/SMS BLOCK UPI to 7308080808").format(
        amount, party, when.strftime("%d/%m/%y"), ref))


def card(when, amount, merchant):
    return msg(when, HDFC, "Rs.{0:.2f} spent on HDFC Bank Card x9012 at {1} on {2}. Avl limit Rs.1,20,000".format(
        amount, merchant, when.strftime("%d-%m-%y")))


def credit(when, amount, party):
    return msg(when, HDFC, "Rs.{0:.2f} credited to a/c XX4521 on {1} by NEFT {2}. Avl bal Rs.40,000.00".format(
        amount, when.strftime("%d-%m-%y"), party))


def everyday(days=60):
    """Chai every weekday and groceries on Saturdays, so the ledger has a usual."""
    out = []
    start = NOW - timedelta(days=days)
    ref = 500000
    for i in range(days):
        day = (start + timedelta(days=i)).replace(hour=8, minute=10)
        if day.weekday() < 5:
            ref += 1
            out.append(sent(day, 30, "chaiwala@ybl", ref))
        if day.weekday() == 5:
            out.append(card(day.replace(hour=11), 1800, "BIGBASKET"))
    return out


def scam_afternoon(minutes_ago=5):
    paid = NOW - timedelta(minutes=minutes_ago)
    return [
        msg(paid - timedelta(minutes=9), "+919811234567",
            "Dear customer your SBI account will be BLOCKED today. Update KYC immediately at "
            "http://sbi-kyc-update.in or call 9811234567"),
        sent(paid, 12000, "kyc.update9@ybl", 777001),
    ]


def double_charge(days_ago=8):
    first = (NOW - timedelta(days=days_ago)).replace(hour=20, minute=14)
    return [card(first, 540, "ZOMATO"), card(first + timedelta(minutes=2), 540, "ZOMATO")]


def netflix():
    return [card(datetime(2026, 6, 13, 9, 0), 499, "NETFLIX"),
            card(datetime(2026, 7, 13, 9, 0), 499, "NETFLIX"),
            card(datetime(2026, 8, 13, 9, 0), 649, "NETFLIX")]


def atm_every_month():
    """Cash on the 15th: regular, but nobody can cancel an ATM."""
    return [msg(datetime(2026, m, 15, 13, 10), HDFC,
                "Rs.10000.00 withdrawn from HDFC Bank A/C *4521 at ATM MG ROAD on 15/{0:02d}/26. "
                "Avl bal Rs.30,412.10".format(m)) for m in (6, 7, 8)]


def phone(*extra):
    rows = everyday()
    for group in extra:
        rows.extend(group)
    return sorted(rows, key=lambda m: m["when"])
