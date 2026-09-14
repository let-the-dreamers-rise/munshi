"""The paperwork, filled in: 1930 and cybercrime.gov.in, the bank, and UPI Help.

Pure templates. No model writes these, because a complaint with a wrong
reference number is worse than no complaint. Every field comes from the
event, which came from the bank's own message.
"""

from __future__ import annotations

from datetime import timedelta

from .money import quoted, rs, rupees
from .scams import named

GOLDEN_HOUR = timedelta(hours=1)


def _when(event):
    return event.when.strftime("%d %b %Y, %H:%M")


def _words(event):
    return quoted((event.evidence.get("scam_words") or [])[:3]) or "no scam words"


def cybercrime_report(event):
    """What to say on 1930 and type into cybercrime.gov.in, inside the golden hour."""
    deadline = event.when + GOLDEN_HOUR
    suspect = event.evidence.get("suspect_contact", "")
    minutes = event.evidence.get("minutes_after_message")
    story = "{0} left my {1} account ending {2} to {3} on {4} (reference {5}). I had never paid this recipient before.".format(
        rs(event.amount), event.bank, event.account, event.party, _when(event), event.ref)
    if suspect:
        story = "I received a message from {0} containing {1}. {2} minutes later, {3}".format(
            suspect, _words(event), minutes, story)
    pattern = named(event.evidence)
    if pattern:
        story += " The message follows the pattern of {0}.".format(pattern.en)
    fields = {
        "Category": "Online Financial Fraud",
        "Sub-category": "UPI related fraud" if event.channel == "upi" or "@" in event.party else "Other financial fraud",
        "Date and time of transaction": _when(event),
        "Amount (Rs)": rupees(event.amount),
        "Transaction ID / UTR": event.ref,
        "Bank": event.bank,
        "Account (last digits)": event.account,
        "Suspect UPI ID": event.party if "@" in event.party else "",
        "Suspect phone": suspect,
        "What happened": story,
    }
    text = ("Call 1930 now, before {0}. The first hour is when a bank can still hold the money. "
            "Read them the fields below, then file the same details at cybercrime.gov.in under financial fraud "
            "and keep the acknowledgement number.").format(deadline.strftime("%H:%M"))
    return {"where": "1930 and https://cybercrime.gov.in", "call_before": deadline.strftime("%H:%M on %d %b %Y"),
            "text": text, "fields": fields}


def bank_dispute(event):
    """A letter for the bank's dispute desk, and the helpline printed in the bank's own message."""
    if event.kind == "double_charge":
        subject = "Amount debited twice: {0} at {1} on {2}".format(rs(event.amount), event.party, _when(event))
        ask = ("The same amount was charged twice, {0} minutes apart (first reference {1}, second reference {2}). "
               "I authorised one payment. Please reverse the second charge.").format(
            event.evidence.get("minutes_apart"), event.evidence.get("first_ref") or "not in the message",
            event.ref or "not in the message")
    else:
        subject = "Unauthorised UPI debit of {0} on {1}, reference {2}".format(rs(event.amount), _when(event), event.ref)
        ask = ("I did not knowingly authorise this payment to {0}. Please block further debits to this recipient, "
               "raise a dispute, and ask the receiving bank to hold the amount. I am reporting it to 1930 and "
               "cybercrime.gov.in.").format(event.party)
    body = ("To the dispute desk, {0}\n\nAccount ending {1}\nAmount: {2}\nDate and time: {3}\nReference: {4}\n"
            "Recipient: {5}\n\n{6}\n\nThank you.").format(
        event.bank, event.account, rs(event.amount), _when(event), event.ref or "not in the message",
        event.party, ask)
    return {"subject": subject, "body": body, "helpline": event.helpline, "bank": event.bank}


MAKERS = {"cybercrime_report": lambda e: cybercrime_report(e), "bank_dispute": lambda e: bank_dispute(e),
          "upi_help": lambda e: upi_help_complaint(e)}
FOR_RECOMMENDATION = {"report_now": ("cybercrime_report", "bank_dispute", "upi_help"),
                      "dispute": ("bank_dispute", "upi_help")}


def drafts_for(event, recommended):
    """Every draft a recommendation calls for. Pure templates, so the safety net can use them too."""
    return {name: MAKERS[name](event) for name in FOR_RECOMMENDATION.get(recommended, ())}


def upi_help_complaint(event):
    """The fields UPI Help asks for. It only applies to UPI payments."""
    applies = event.channel == "upi" or "@" in event.party
    issue = "Amount debited twice" if event.kind == "double_charge" else "Fraud or unauthorised transaction"
    note = ("In the UPI app you paid from, open UPI Help (or Help, then report an issue) on this payment."
            if applies else "This was a {0} payment, so UPI Help does not apply. Use the bank dispute.".format(event.channel))
    return {"applies": applies, "issue": issue, "transaction_ref": event.ref, "amount": rupees(event.amount),
            "date": _when(event), "recipient": event.party, "note": note}
