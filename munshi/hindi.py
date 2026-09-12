# -*- coding: utf-8 -*-
"""The card in Hindi.

Not a translation of the English sentence: the same facts, written again. A
household that reads Hindi should get the same numbers, the same payee and the
same choice, in the language the family argues about money in. The paperwork
itself stays in English, because that is what 1930 and the bank's dispute desk
read.
"""

from __future__ import annotations

from datetime import date

from .money import rupees

RS = "₹"  # the rupee sign; "Rs" in the English card
MONTHS = ("जनवरी", "फरवरी", "मार्च",
          "अप्रैल", "मई", "जून", "जुलाई",
          "अगस्त", "सितंबर", "अक्टूबर",
          "नवंबर", "दिसंबर")


def rs(amount):
    return RS + rupees(amount)


def day(iso):
    d = date.fromisoformat(iso) if isinstance(iso, str) else iso
    return "{0} {1}".format(d.day, MONTHS[d.month - 1])


def in_days(n):
    return {0: "आज", 1: "कल"}.get(n, "{0} दिन में".format(n))


def quoted(words):
    q = ["'{0}'".format(w) for w in words]
    if not q:
        return ""
    return q[0] if len(q) == 1 else ", ".join(q[:-1]) + " और " + q[-1]


def headline(event):
    ev = event.evidence
    if event.kind == "scam_shaped_payment":
        scam = ("यह KYC ठगी का तरीका है।"
                if "kyc" in ev.get("scam_words", []) else
                "यह ठगी जैसा लगता है।")
        return ("{0} {1} को गए, जिन्हें आपने "
                "पहले कभी पैसे नहीं "
                "भेजे — किसी अनजान "
                "नंबर से आए धमकी भरे "
                "मैसेज के {2} मिनट बाद। "
                "{3}").format(rs(event.amount), event.party, ev.get("minutes_after_message"), scam)
    if event.kind == "double_charge":
        return ("आपके {0} वापस मिलने "
                "चाहिए: {1} ने दो बार "
                "पैसे काटे और अब तक "
                "वापस नहीं किए।").format(
            rs(event.amount), event.party)
    if event.kind == "renewal_due":
        was = (" पहले {0} था।".format(rs(ev.get("usual_amount", 0)))
               if "price_up" in event.flags else "")
        return "{0} {1} {2} में रिन्यू होगा।{3}".format(
            event.party, in_days(ev.get("due_in_days", 0)), rs(event.amount), was)
    return ("{0} किसी नए व्यक्ति को "
            "गए — आपके आम भुगतान "
            "से {1} गुना। क्या यह "
            "आपने किया था?").format(
        rs(event.amount), ev.get("times_usual"))


def facts(event, ledger):
    """The same sentences as facts_for, in the same order, in Hindi."""
    ev = event.evidence
    history = ledger.payee_history(event.party)
    before = history["times_paid"] - 1 if event.kind in ("scam_shaped_payment", "unusual_payment") else None
    out = []
    if before == 0:
        days = ledger.history_days()
        out.append(
            ("{0} को पहले कभी पैसे "
             "नहीं भेजे गए: {1} दिन "
             "के रिकॉर्ड में यह "
             "पहला भुगतान है।").format(event.party, days)
            if days >= 2 else
            ("इन मैसेजों में {0} को "
             "कोई पुराना भुगतान "
             "नहीं है।").format(event.party))
    if event.kind == "scam_shaped_payment":
        out.append(("यह भुगतान {0} से आए "
                    "मैसेज के {1} मिनट बाद "
                    "हुआ, जिसमें {2} शब्द "
                    "थे।").format(
            ev.get("suspect_contact") or "एक अनजान नंबर",
            ev.get("minutes_after_message"), quoted(ev.get("scam_words", [])[:3])))
    if ev.get("times_usual"):
        out.append(("{0} आपके आम भुगतान {1} "
                    "से {2} गुना है।").format(
            rs(event.amount), rs(ev.get("usual_amount", 0)), _times(ev["times_usual"])))
    if event.kind == "double_charge":
        out.append(("{0} ने {1} को {2} दो बार, {3} "
                    "मिनट के अंतर पर "
                    "काटे।").format(
            event.party, day(event.when.date()), rs(event.amount), ev.get("minutes_apart")))
        out.append(("इन {0} दिनों में {1} का "
                    "कोई रिफंड नहीं "
                    "आया।").format(ev.get("days_since"), rs(event.amount)))
    if event.kind == "renewal_due":
        out.append(("{0} ने {1} बार, हर {2} दिन में "
                    "पैसे काटे हैं। "
                    "अगला भुगतान {3}, {4} को "
                    "है।").format(
            event.party, ev.get("times_seen"), ev.get("every_days"), in_days(ev.get("due_in_days", 0)),
            day(ev.get("due_on"))))
        if "price_up" in event.flags:
            out.append(("पिछली बार {0} कटे, "
                        "पहले {1} थे।").format(
                rs(ev.get("last_amount", 0)), rs(ev.get("usual_amount", 0))))
    return out


def _times(x):
    return str(int(round(x))) if x >= 10 or float(x).is_integer() else "{0:.1f}".format(x)


OPTIONS = {
    "scam_shaped_payment": (("report", "अभी रिपोर्ट करें"),
                            ("fine", "यह भुगतान मैंने "
                                     "खुद किया था")),
    "unusual_payment": (("fine", "यह मैंने किया था"),
                        ("report", "यह मैंने नहीं "
                                   "किया")),
    "double_charge": (("dispute", "दूसरी कटौती पर "
                                  "शिकायत करें"),
                      ("fine", "दो अलग ऑर्डर थे")),
    "renewal_due": (("keep", "चालू रहने दें"),
                    ("cancel", "बंद करने की याद "
                               "दिलाएँ")),
}


def options(kind):
    return [list(o) for o in OPTIONS.get(kind, OPTIONS["unusual_payment"])]


STEPS = {
    "report": ("अभी 1930 पर कॉल करें, पहले "
               "घंटे के अंदर, और उन्हें "
               "रिपोर्ट की जानकारी "
               "बताएँ।",
               "वही जानकारी cybercrime.gov.in पर "
               "दर्ज करें और acknowledgement नंबर "
               "सँभालकर रखें।",
               "अपने बैंक की हेल्पलाइन "
               "पर कॉल करके कहें कि "
               "इस रिसीवर को ब्लॉक "
               "करके शिकायत दर्ज "
               "करें।"),
    "dispute": ("बैंक को शिकायत पत्र "
                "भेजें, या हेल्पलाइन "
                "पर पढ़कर सुनाएँ।",),
    "fine": ("ठीक है। मुंशी अब इस "
             "पेयी के बारे में दोबारा "
             "नहीं पूछेगा।",),
    "keep": ("ठीक है। मुंशी इस "
             "रिन्यूअल की याद नहीं "
             "दिलाएगा।",),
    "cancel": ("आखिरी तारीख से पहले "
               "ऐप या वेबसाइट पर जाकर "
               "बंद करें। मुंशी आपके "
               "लिए बंद नहीं कर सकता।",),
}


def steps(event, choice):
    out = list(STEPS.get(choice, ()))
    if choice == "report" and event.helpline:
        out[-1] = ("{0} को {1} पर कॉल करके कहें "
                   "कि इस रिसीवर को ब्लॉक "
                   "करके शिकायत दर्ज "
                   "करें।").format(event.bank, event.helpline)
    return out


def card(event, ledger):
    return {"headline": headline(event), "evidence": facts(event, ledger), "options": options(event.kind)}
