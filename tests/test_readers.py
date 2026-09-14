"""Real bank SMS formats, as Indian phones actually receive them.

Each line here is a template a bank really sends. `nyaya.money` reads most of
them; the ones it cannot are why munshi/readers.py exists. The corpus is the
regression test for both.
"""

from datetime import datetime

import pytest

from munshi.readers import read

NOW = datetime(2026, 9, 12, 15, 0)
HDFC = "VM-HDFCBK"

CORPUS = [
    ("hdfc_upi_sent", HDFC,
     "Sent Rs.12000.00 From HDFC Bank A/C *4521 To kyc.update9@ybl On 12/09/26 Ref 624511873920 "
     "Not You? Call 18002586161",
     ("out", 12000.0, "kyc.update9@ybl", "upi", "4521")),
    ("icici_upi", "JD-ICICIB",
     "Dear Customer, Acct XX521 is debited with Rs 5000.00 on 12-Sep-26; ramesh@okicici credited. "
     "UPI:624511873920. Call 18002662 for dispute.",
     ("out", 5000.0, "ramesh@okicici", "upi", "521")),
    ("sbi_upi_no_currency_mark", "AD-SBIINB",
     "Dear UPI user A/C X4521 debited by 2500.0 on date 12Sep26 trf to RAMESH KUMAR Refno 624511873920. "
     "If not u? call 1800111109. -SBI",
     ("out", 2500.0, "Ramesh Kumar", "upi", "4521")),
    ("axis_card_spend", "AD-AXISBK",
     "Spent Card no. XX9012 INR 1499 12-09-26 13:20 AMAZON Avl Lmt INR 120000 SMS BLOCK 9012 - Axis Bank",
     ("out", 1499.0, "Amazon", "card", "9012")),
    ("kotak_upi", "VM-KOTAKB",
     "Sent Rs.750.00 from Kotak Bank AC X1234 to zomato@paytm on 12-09-26.UPI Ref 624511873921.",
     ("out", 750.0, "zomato@paytm", "upi", "1234")),
    ("paytm_wallet", "VM-PAYTMB",
     "Paid Rs.199 to SWIGGY from Paytm Wallet on 12/09/2026. Txn ID 624511873922.",
     ("out", 199.0, "Swiggy", "other", "")),
    ("phonepe_vpa", HDFC,
     "Rs.1,200 debited from A/c XX4521 on 12-09-26 to VPA merchant@upi. UPI Ref No 624511873923.",
     ("out", 1200.0, "merchant@upi", "upi", "4521")),
    ("pnb_upi_no_payee", "AD-PNBSMS",
     "Dear Customer, Rs.3000.00 debited from A/c XXXX4521 on 12/09/26 by UPI:624511873924. Bal Rs.10000. -PNB",
     ("out", 3000.0, "", "upi", "4521")),
    ("neft_out", HDFC,
     "Rs.25000.00 transferred from A/c XX4521 to A/c XX9999 via NEFT on 12-09-26. Ref N123456789. -HDFC Bank",
     ("out", 25000.0, "", "transfer", "4521")),
    ("imps_to_a_person", HDFC,
     "Rs 8000 sent from HDFC Bank A/c **4521 via IMPS Ref 624511873925 on 12-09-26 to ANITA SHARMA",
     ("out", 8000.0, "Anita Sharma", "transfer", "4521")),
    ("atm_cash", HDFC,
     "Rs.10000.00 withdrawn from HDFC Bank A/C *4521 at ATM MG ROAD on 15/08/26. Avl bal Rs.30412.10",
     ("out", 10000.0, "Atm Mg Road", "atm", "4521")),
    ("credit_card_spend", HDFC,
     "Rs.540.00 spent on HDFC Bank Card x9012 at ZOMATO on 12-09-26. Avl limit Rs.1,20,000",
     ("out", 540.0, "Zomato", "card", "9012")),
    ("salary_in", HDFC,
     "Rs.40000.00 credited to a/c XX4521 on 01-09-26 by NEFT SALARY. Avl bal Rs.70000.00",
     ("in", 40000.0, "Salary", "transfer", "4521")),
    ("bob_upi", "AD-BOBTXN",
     "Dear Customer, your A/c XX4521 is debited for Rs.1500.00 on 12-09-2026 and credited to VPA shop@ybl "
     "(UPI Ref 624511873926) - Bank of Baroda",
     ("out", 1500.0, "shop@ybl", "upi", "4521")),
]

DROPPED = [
    ("autopay_notice", HDFC, "Rs.649.00 will be debited from A/c XX4521 on 15-09-26 towards NETFLIX UPI AutoPay "
                             "mandate."),
    ("otp", HDFC, "123456 is the OTP for your transaction of Rs.5000 at AMAZON. Do not share it with anyone."),
    ("balance", HDFC, "Your A/c XX4521 balance is Rs.70000.00 as on 12-09-26."),
    ("phishing_from_a_phone", "+919811234567",
     "Dear customer Rs.12000 debited from your account. Update KYC immediately at http://sbi-kyc-update.in"),
]


@pytest.mark.parametrize("name,sender,body,expected", CORPUS, ids=[c[0] for c in CORPUS])
def test_the_corpus_of_real_formats_reads(name, sender, body, expected):
    txn = read(NOW, sender, body)
    assert txn is not None, "not read at all"
    assert (txn.direction, txn.amount, txn.party, txn.channel, txn.account) == expected


@pytest.mark.parametrize("name,sender,body", DROPPED, ids=[d[0] for d in DROPPED])
def test_what_is_not_a_payment_is_dropped(name, sender, body):
    assert read(NOW, sender, body) is None


def test_a_pasted_message_is_credited_to_the_bank_that_signed_it():
    """The complaint names a bank, so pasted SBI text must not become an HDFC complaint."""
    from munshi.paste import messages_from_text
    from munshi.witness import Household

    text = ("Dear customer your account will be BLOCKED. Update KYC immediately.\n\n"
            "Dear UPI user A/C X4521 debited by 2500.0 on date 12Sep26 trf to RAMESH KUMAR "
            "Refno 624511873920. If not u? call 1800111109. -SBI")
    house = Household.from_messages("paste", messages_from_text(text, now=NOW), now=NOW)
    assert house.events[0].bank == "SBI"


def test_a_mandate_notice_is_not_a_payment_yet():
    """'will be debited' is a warning about Tuesday, not money that moved."""
    assert read(NOW, HDFC, "Rs.649.00 will be debited from A/c XX4521 on 15-09-26 towards NETFLIX mandate.") is None
    assert read(NOW, HDFC, "Rs.649.00 debited from A/c XX4521 on 15-09-26 towards NETFLIX.") is not None


def test_a_real_debit_is_not_lost_because_the_same_message_warns_of_a_future_one():
    """Banks put both in one SMS. Dropping the whole message would hide money that has gone."""
    body = ("Rs.12000.00 debited from A/c XX4521 on 12-09-26 to kyc.update9@ybl UPI Ref 624511873920. "
            "Your NETFLIX mandate of Rs.649.00 will be debited on 15-09-26.")
    txn = read(NOW, HDFC, body)
    assert txn is not None
    assert txn.amount == 12000.0 and txn.party == "kyc.update9@ybl"
