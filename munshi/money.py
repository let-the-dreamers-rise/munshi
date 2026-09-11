"""Rupees the way an Indian reader writes them: Rs 1,20,000."""


def rupees(amount):
    whole = int(round(amount))
    s = str(abs(whole))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return ("-" if whole < 0 else "") + s


def rs(amount):
    return "Rs " + rupees(amount)


def times(x):
    """58.0 -> '58', 2.5 -> '2.5'."""
    return str(int(round(x))) if x >= 10 or float(x).is_integer() else "{0:.1f}".format(x)


def in_days(n):
    return {0: "today", 1: "tomorrow"}.get(n, "in {0} days".format(n))


def quoted(words):
    """['kyc', 'blocked', 'immediately'] -> "'kyc', 'blocked' and 'immediately'"."""
    q = ["'{0}'".format(w) for w in words]
    return q[0] if len(q) == 1 else ", ".join(q[:-1]) + " and " + q[-1] if q else ""


def day(iso):
    """'2026-09-12' -> '12 Sep'."""
    from datetime import date
    return date.fromisoformat(iso).strftime("%d %b").lstrip("0")
