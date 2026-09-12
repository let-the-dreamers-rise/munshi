window.MUNSHI_REPLAY = {
 "recorded_at": "12 Sep 2026, 12:31",
 "initial": {
  "household": "meera",
  "now": "2026-09-12 12:31",
  "watched": {
   "payments": 212,
   "days": 99
  },
  "cards": [
   {
    "id": "card-927c79716f5b",
    "event_id": "927c79716f5b",
    "kind": "scam_shaped_payment",
    "headline": "Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown number. This is how the KYC scam works.",
    "evidence": [
     "kyc.update9@ybl had never been paid before: this is the first payment in 99 days of history.",
     "The payment came 9 minutes after a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'.",
     "Rs 12,000 is 54 times the household's usual payment of Rs 221."
    ],
    "options": [
     [
      "report",
      "Report it now"
     ],
     [
      "fine",
      "I made this payment on purpose"
     ]
    ],
    "party": "kyc.update9@ybl",
    "amount": 12000.0,
    "when": "2026-09-12 12:26",
    "drafts": {
     "cybercrime_report": {
      "where": "1930 and https://cybercrime.gov.in",
      "call_before": "13:26 on 12 Sep 2026",
      "text": "Call 1930 now, before 13:26. The first hour is when a bank can still hold the money. Read them the fields below, then file the same details at cybercrime.gov.in under financial fraud and keep the acknowledgement number.",
      "fields": {
       "Category": "Online Financial Fraud",
       "Sub-category": "UPI related fraud",
       "Date and time of transaction": "12 Sep 2026, 12:26",
       "Amount (Rs)": "12,000",
       "Transaction ID / UTR": "624511873920",
       "Bank": "HDFC Bank",
       "Account (last digits)": "4521",
       "Suspect UPI ID": "kyc.update9@ybl",
       "Suspect phone": "+919811234567",
       "What happened": "I received a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'. 9 minutes later, Rs 12,000 left my HDFC Bank account ending 4521 to kyc.update9@ybl on 12 Sep 2026, 12:26 (reference 624511873920). I had never paid this recipient before."
      }
     },
     "bank_dispute": {
      "subject": "Unauthorised UPI debit of Rs 12,000 on 12 Sep 2026, 12:26, reference 624511873920",
      "body": "To the dispute desk, HDFC Bank\n\nAccount ending 4521\nAmount: Rs 12,000\nDate and time: 12 Sep 2026, 12:26\nReference: 624511873920\nRecipient: kyc.update9@ybl\n\nI did not knowingly authorise this payment to kyc.update9@ybl. Please block further debits to this recipient, raise a dispute, and ask the receiving bank to hold the amount. I am reporting it to 1930 and cybercrime.gov.in.\n\nThank you.",
      "helpline": "18002586161",
      "bank": "HDFC Bank"
     },
     "upi_help": {
      "applies": true,
      "issue": "Fraud or unauthorised transaction",
      "transaction_ref": "624511873920",
      "amount": "12,000",
      "date": "12 Sep 2026, 12:26",
      "recipient": "kyc.update9@ybl",
      "note": "In the UPI app you paid from, open UPI Help (or Help, then report an issue) on this payment."
     }
    },
    "interrupt_id": "v1:tool_call:playbook-d57b8d4fbafd:a03c9326-dd4c-5878-95a5-2d96fbe58668",
    "session_id": "meera-927c79716f5b",
    "decided_by": "rules",
    "created": "2026-09-12T12:31:13",
    "status": "pending",
    "decision": "",
    "outcome": "",
    "decided": ""
   },
   {
    "id": "card-7aae1c1a494d",
    "event_id": "7aae1c1a494d",
    "kind": "renewal_due",
    "headline": "Netflix renews tomorrow at Rs 649. It was Rs 499.",
    "evidence": [
     "Netflix has charged you 3 times, every 31 days. The next charge is due tomorrow, 13 Sep.",
     "The last charge was Rs 649, up from Rs 499."
    ],
    "options": [
     [
      "keep",
      "Keep it"
     ],
     [
      "cancel",
      "Remind me to cancel it first"
     ]
    ],
    "party": "Netflix",
    "amount": 649.0,
    "when": "2026-08-13 09:00",
    "drafts": {},
    "interrupt_id": "v1:tool_call:playbook-b10ce312fef9:a03c9326-dd4c-5878-95a5-2d96fbe58668",
    "session_id": "meera-7aae1c1a494d",
    "decided_by": "rules",
    "created": "2026-09-12T12:31:13",
    "status": "pending",
    "decision": "",
    "outcome": "",
    "decided": ""
   },
   {
    "id": "card-7265498325d2",
    "event_id": "7265498325d2",
    "kind": "double_charge",
    "headline": "You may be owed Rs 540: Zomato charged you twice and has not refunded it.",
    "evidence": [
     "Zomato charged Rs 540 twice, 2 minutes apart, on 4 Sep.",
     "No refund of Rs 540 has arrived in the 7 days since."
    ],
    "options": [
     [
      "dispute",
      "Dispute the second charge"
     ],
     [
      "fine",
      "It was two orders"
     ]
    ],
    "party": "Zomato",
    "amount": 540.0,
    "when": "2026-09-04 20:16",
    "drafts": {
     "bank_dispute": {
      "subject": "Amount debited twice: Rs 540 at Zomato on 04 Sep 2026, 20:16",
      "body": "To the dispute desk, HDFC Bank\n\nAccount ending 9012\nAmount: Rs 540\nDate and time: 04 Sep 2026, 20:16\nReference: not in the message\nRecipient: Zomato\n\nThe same amount was charged twice, 2 minutes apart (first reference not in the message, second reference not in the message). I authorised one payment. Please reverse the second charge.\n\nThank you.",
      "helpline": "",
      "bank": "HDFC Bank"
     },
     "upi_help": {
      "applies": false,
      "issue": "Amount debited twice",
      "transaction_ref": "",
      "amount": "540",
      "date": "04 Sep 2026, 20:16",
      "recipient": "Zomato",
      "note": "This was a card payment, so UPI Help does not apply. Use the bank dispute."
     }
    },
    "interrupt_id": "v1:tool_call:playbook-cea6814682aa:a03c9326-dd4c-5878-95a5-2d96fbe58668",
    "session_id": "meera-7265498325d2",
    "decided_by": "rules",
    "created": "2026-09-12T12:31:13",
    "status": "pending",
    "decision": "",
    "outcome": "",
    "decided": ""
   }
  ],
  "audit": [
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "investigate_payment",
    "input": {
     "event_id": "927c79716f5b"
    },
    "status": "success",
    "refused": null,
    "result": "{\"verdict\": {\"kind\": \"likely_scam\", \"confidence\": 0.9, \"headline\": \"Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown number. This is how the KYC scam works.\", \"recommended\": \"report_now\"}, \"facts\": [\"kyc.update9@ybl had never been paid before: this is the first payment in 99 days of history.\", \"The payment came 9 minutes after a message from ",
    "ms": 1.2
   },
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "draft_cybercrime_report",
    "input": {
     "event_id": "927c79716f5b"
    },
    "status": "success",
    "refused": null,
    "result": "{\"where\": \"1930 and https://cybercrime.gov.in\", \"call_before\": \"13:26 on 12 Sep 2026\", \"text\": \"Call 1930 now, before 13:26. The first hour is when a bank can still hold the money. Read them the fields below, then file the same details at cybercrime.gov.in under financial fraud and keep the acknowledgement number.\", \"fields\": {\"Category\": \"Online Financial Fraud\", \"Sub-category\": \"UPI related frau",
    "ms": 1.5
   },
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "draft_bank_dispute",
    "input": {
     "event_id": "927c79716f5b"
    },
    "status": "success",
    "refused": null,
    "result": "{\"subject\": \"Unauthorised UPI debit of Rs 12,000 on 12 Sep 2026, 12:26, reference 624511873920\", \"body\": \"To the dispute desk, HDFC Bank\\n\\nAccount ending 4521\\nAmount: Rs 12,000\\nDate and time: 12 Sep 2026, 12:26\\nReference: 624511873920\\nRecipient: kyc.update9@ybl\\n\\nI did not knowingly authorise this payment to kyc.update9@ybl. Please block further debits to this recipient, raise a dispute, and",
    "ms": 1.1
   },
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "draft_upi_help_complaint",
    "input": {
     "event_id": "927c79716f5b"
    },
    "status": "success",
    "refused": null,
    "result": "{\"applies\": true, \"issue\": \"Fraud or unauthorised transaction\", \"transaction_ref\": \"624511873920\", \"amount\": \"12,000\", \"date\": \"12 Sep 2026, 12:26\", \"recipient\": \"kyc.update9@ybl\", \"note\": \"In the UPI app you paid from, open UPI Help (or Help, then report an issue) on this payment.\"}",
    "ms": 1.4
   },
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "ask_household",
    "input": {
     "event_id": "927c79716f5b"
    },
    "status": "waiting for the household",
    "refused": null,
    "result": "Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown number. This is how the KYC scam works.",
    "ms": 0.0
   },
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "investigate_payment",
    "input": {
     "event_id": "7aae1c1a494d"
    },
    "status": "success",
    "refused": null,
    "result": "{\"verdict\": {\"kind\": \"renewal\", \"confidence\": 0.9, \"headline\": \"Netflix renews tomorrow at Rs 649. It was Rs 499.\", \"recommended\": \"remind\"}, \"facts\": [\"Netflix has charged you 3 times, every 31 days. The next charge is due tomorrow, 13 Sep.\", \"The last charge was Rs 649, up from Rs 499.\"], \"decided_by\": \"rules\"}",
    "ms": 1.2
   },
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "ask_household",
    "input": {
     "event_id": "7aae1c1a494d"
    },
    "status": "waiting for the household",
    "refused": null,
    "result": "Netflix renews tomorrow at Rs 649. It was Rs 499.",
    "ms": 0.0
   },
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "investigate_payment",
    "input": {
     "event_id": "7265498325d2"
    },
    "status": "success",
    "refused": null,
    "result": "{\"verdict\": {\"kind\": \"double_charge\", \"confidence\": 0.8, \"headline\": \"You may be owed Rs 540: Zomato charged you twice and has not refunded it.\", \"recommended\": \"dispute\"}, \"facts\": [\"Zomato charged Rs 540 twice, 2 minutes apart, on 4 Sep.\", \"No refund of Rs 540 has arrived in the 7 days since.\"], \"decided_by\": \"rules\"}",
    "ms": 1.2
   },
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "draft_bank_dispute",
    "input": {
     "event_id": "7265498325d2"
    },
    "status": "success",
    "refused": null,
    "result": "{\"subject\": \"Amount debited twice: Rs 540 at Zomato on 04 Sep 2026, 20:16\", \"body\": \"To the dispute desk, HDFC Bank\\n\\nAccount ending 9012\\nAmount: Rs 540\\nDate and time: 04 Sep 2026, 20:16\\nReference: not in the message\\nRecipient: Zomato\\n\\nThe same amount was charged twice, 2 minutes apart (first reference not in the message, second reference not in the message). I authorised one payment. Pleas",
    "ms": 1.1
   },
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "draft_upi_help_complaint",
    "input": {
     "event_id": "7265498325d2"
    },
    "status": "success",
    "refused": null,
    "result": "{\"applies\": false, \"issue\": \"Amount debited twice\", \"transaction_ref\": \"\", \"amount\": \"540\", \"date\": \"04 Sep 2026, 20:16\", \"recipient\": \"Zomato\", \"note\": \"This was a card payment, so UPI Help does not apply. Use the bank dispute.\"}",
    "ms": 2.3
   },
   {
    "at": "2026-09-12T12:31:13",
    "agent": "munshi",
    "tool": "ask_household",
    "input": {
     "event_id": "7265498325d2"
    },
    "status": "waiting for the household",
    "refused": null,
    "result": "You may be owed Rs 540: Zomato charged you twice and has not refunded it.",
    "ms": 0.0
   }
  ]
 },
 "outcomes": {
  "card-927c79716f5b": {
   "report": {
    "card": {
     "id": "card-927c79716f5b",
     "event_id": "927c79716f5b",
     "kind": "scam_shaped_payment",
     "headline": "Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown number. This is how the KYC scam works.",
     "evidence": [
      "kyc.update9@ybl had never been paid before: this is the first payment in 99 days of history.",
      "The payment came 9 minutes after a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'.",
      "Rs 12,000 is 54 times the household's usual payment of Rs 221."
     ],
     "options": [
      [
       "report",
       "Report it now"
      ],
      [
       "fine",
       "I made this payment on purpose"
      ]
     ],
     "party": "kyc.update9@ybl",
     "amount": 12000.0,
     "when": "2026-09-12 12:26",
     "drafts": {
      "cybercrime_report": {
       "where": "1930 and https://cybercrime.gov.in",
       "call_before": "13:26 on 12 Sep 2026",
       "text": "Call 1930 now, before 13:26. The first hour is when a bank can still hold the money. Read them the fields below, then file the same details at cybercrime.gov.in under financial fraud and keep the acknowledgement number.",
       "fields": {
        "Category": "Online Financial Fraud",
        "Sub-category": "UPI related fraud",
        "Date and time of transaction": "12 Sep 2026, 12:26",
        "Amount (Rs)": "12,000",
        "Transaction ID / UTR": "624511873920",
        "Bank": "HDFC Bank",
        "Account (last digits)": "4521",
        "Suspect UPI ID": "kyc.update9@ybl",
        "Suspect phone": "+919811234567",
        "What happened": "I received a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'. 9 minutes later, Rs 12,000 left my HDFC Bank account ending 4521 to kyc.update9@ybl on 12 Sep 2026, 12:26 (reference 624511873920). I had never paid this recipient before."
       }
      },
      "bank_dispute": {
       "subject": "Unauthorised UPI debit of Rs 12,000 on 12 Sep 2026, 12:26, reference 624511873920",
       "body": "To the dispute desk, HDFC Bank\n\nAccount ending 4521\nAmount: Rs 12,000\nDate and time: 12 Sep 2026, 12:26\nReference: 624511873920\nRecipient: kyc.update9@ybl\n\nI did not knowingly authorise this payment to kyc.update9@ybl. Please block further debits to this recipient, raise a dispute, and ask the receiving bank to hold the amount. I am reporting it to 1930 and cybercrime.gov.in.\n\nThank you.",
       "helpline": "18002586161",
       "bank": "HDFC Bank"
      },
      "upi_help": {
       "applies": true,
       "issue": "Fraud or unauthorised transaction",
       "transaction_ref": "624511873920",
       "amount": "12,000",
       "date": "12 Sep 2026, 12:26",
       "recipient": "kyc.update9@ybl",
       "note": "In the UPI app you paid from, open UPI Help (or Help, then report an issue) on this payment."
      }
     },
     "interrupt_id": "v1:tool_call:playbook-d57b8d4fbafd:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-927c79716f5b",
     "decided_by": "rules",
     "created": "2026-09-12T12:31:13",
     "status": "decided",
     "decision": "report",
     "outcome": "Call 1930 now, inside the first hour, and read them the report fields.\nFile the same details at cybercrime.gov.in and keep the acknowledgement number.\nCall HDFC Bank on 18002586161 and ask them to block the recipient and raise a dispute.",
     "decided": "2026-09-12T12:31:13"
    },
    "audit": [
     {
      "at": "2026-09-12T12:31:13",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "927c79716f5b"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"927c79716f5b\", \"party\": \"kyc.update9@ybl\", \"decision\": \"report\", \"next_steps\": [\"Call 1930 now, inside the first hour, and read them the report fields.\", \"File the same details at cybercrime.gov.in and keep the acknowledgement number.\", \"Call HDFC Bank on 18002586161 and ask them to block the recipient and raise a dispute.\"]}",
      "ms": 0.9
     }
    ]
   },
   "fine": {
    "card": {
     "id": "card-927c79716f5b",
     "event_id": "927c79716f5b",
     "kind": "scam_shaped_payment",
     "headline": "Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown number. This is how the KYC scam works.",
     "evidence": [
      "kyc.update9@ybl had never been paid before: this is the first payment in 99 days of history.",
      "The payment came 9 minutes after a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'.",
      "Rs 12,000 is 54 times the household's usual payment of Rs 221."
     ],
     "options": [
      [
       "report",
       "Report it now"
      ],
      [
       "fine",
       "I made this payment on purpose"
      ]
     ],
     "party": "kyc.update9@ybl",
     "amount": 12000.0,
     "when": "2026-09-12 12:26",
     "drafts": {
      "cybercrime_report": {
       "where": "1930 and https://cybercrime.gov.in",
       "call_before": "13:26 on 12 Sep 2026",
       "text": "Call 1930 now, before 13:26. The first hour is when a bank can still hold the money. Read them the fields below, then file the same details at cybercrime.gov.in under financial fraud and keep the acknowledgement number.",
       "fields": {
        "Category": "Online Financial Fraud",
        "Sub-category": "UPI related fraud",
        "Date and time of transaction": "12 Sep 2026, 12:26",
        "Amount (Rs)": "12,000",
        "Transaction ID / UTR": "624511873920",
        "Bank": "HDFC Bank",
        "Account (last digits)": "4521",
        "Suspect UPI ID": "kyc.update9@ybl",
        "Suspect phone": "+919811234567",
        "What happened": "I received a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'. 9 minutes later, Rs 12,000 left my HDFC Bank account ending 4521 to kyc.update9@ybl on 12 Sep 2026, 12:26 (reference 624511873920). I had never paid this recipient before."
       }
      },
      "bank_dispute": {
       "subject": "Unauthorised UPI debit of Rs 12,000 on 12 Sep 2026, 12:26, reference 624511873920",
       "body": "To the dispute desk, HDFC Bank\n\nAccount ending 4521\nAmount: Rs 12,000\nDate and time: 12 Sep 2026, 12:26\nReference: 624511873920\nRecipient: kyc.update9@ybl\n\nI did not knowingly authorise this payment to kyc.update9@ybl. Please block further debits to this recipient, raise a dispute, and ask the receiving bank to hold the amount. I am reporting it to 1930 and cybercrime.gov.in.\n\nThank you.",
       "helpline": "18002586161",
       "bank": "HDFC Bank"
      },
      "upi_help": {
       "applies": true,
       "issue": "Fraud or unauthorised transaction",
       "transaction_ref": "624511873920",
       "amount": "12,000",
       "date": "12 Sep 2026, 12:26",
       "recipient": "kyc.update9@ybl",
       "note": "In the UPI app you paid from, open UPI Help (or Help, then report an issue) on this payment."
      }
     },
     "interrupt_id": "v1:tool_call:playbook-d57b8d4fbafd:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-927c79716f5b",
     "decided_by": "rules",
     "created": "2026-09-12T12:31:13",
     "status": "decided",
     "decision": "fine",
     "outcome": "Noted. Munshi will not ask about this payee again.",
     "decided": "2026-09-12T12:31:14"
    },
    "audit": [
     {
      "at": "2026-09-12T12:31:13",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "927c79716f5b"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"927c79716f5b\", \"party\": \"kyc.update9@ybl\", \"decision\": \"fine\", \"next_steps\": [\"Noted. Munshi will not ask about this payee again.\"]}",
      "ms": 1.4
     },
     {
      "at": "2026-09-12T12:31:13",
      "agent": "munshi",
      "tool": "remember_trusted_payee",
      "input": {
       "party": "kyc.update9@ybl"
      },
      "status": "success",
      "refused": null,
      "result": "{\"trusted\": \"kyc.update9@ybl\"}",
      "ms": 9.5
     }
    ]
   }
  },
  "card-7aae1c1a494d": {
   "keep": {
    "card": {
     "id": "card-7aae1c1a494d",
     "event_id": "7aae1c1a494d",
     "kind": "renewal_due",
     "headline": "Netflix renews tomorrow at Rs 649. It was Rs 499.",
     "evidence": [
      "Netflix has charged you 3 times, every 31 days. The next charge is due tomorrow, 13 Sep.",
      "The last charge was Rs 649, up from Rs 499."
     ],
     "options": [
      [
       "keep",
       "Keep it"
      ],
      [
       "cancel",
       "Remind me to cancel it first"
      ]
     ],
     "party": "Netflix",
     "amount": 649.0,
     "when": "2026-08-13 09:00",
     "drafts": {},
     "interrupt_id": "v1:tool_call:playbook-b10ce312fef9:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-7aae1c1a494d",
     "decided_by": "rules",
     "created": "2026-09-12T12:31:13",
     "status": "decided",
     "decision": "keep",
     "outcome": "Kept. Munshi will not remind you about this renewal.",
     "decided": "2026-09-12T12:31:14"
    },
    "audit": [
     {
      "at": "2026-09-12T12:31:14",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "7aae1c1a494d"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"7aae1c1a494d\", \"party\": \"Netflix\", \"decision\": \"keep\", \"next_steps\": [\"Kept. Munshi will not remind you about this renewal.\"]}",
      "ms": 1.0
     }
    ]
   },
   "cancel": {
    "card": {
     "id": "card-7aae1c1a494d",
     "event_id": "7aae1c1a494d",
     "kind": "renewal_due",
     "headline": "Netflix renews tomorrow at Rs 649. It was Rs 499.",
     "evidence": [
      "Netflix has charged you 3 times, every 31 days. The next charge is due tomorrow, 13 Sep.",
      "The last charge was Rs 649, up from Rs 499."
     ],
     "options": [
      [
       "keep",
       "Keep it"
      ],
      [
       "cancel",
       "Remind me to cancel it first"
      ]
     ],
     "party": "Netflix",
     "amount": 649.0,
     "when": "2026-08-13 09:00",
     "drafts": {},
     "interrupt_id": "v1:tool_call:playbook-b10ce312fef9:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-7aae1c1a494d",
     "decided_by": "rules",
     "created": "2026-09-12T12:31:13",
     "status": "decided",
     "decision": "cancel",
     "outcome": "Cancel it in the app or on the website before the due date. Munshi cannot cancel for you.",
     "decided": "2026-09-12T12:31:14"
    },
    "audit": [
     {
      "at": "2026-09-12T12:31:14",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "7aae1c1a494d"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"7aae1c1a494d\", \"party\": \"Netflix\", \"decision\": \"cancel\", \"next_steps\": [\"Cancel it in the app or on the website before the due date. Munshi cannot cancel for you.\"]}",
      "ms": 1.1
     }
    ]
   }
  },
  "card-7265498325d2": {
   "dispute": {
    "card": {
     "id": "card-7265498325d2",
     "event_id": "7265498325d2",
     "kind": "double_charge",
     "headline": "You may be owed Rs 540: Zomato charged you twice and has not refunded it.",
     "evidence": [
      "Zomato charged Rs 540 twice, 2 minutes apart, on 4 Sep.",
      "No refund of Rs 540 has arrived in the 7 days since."
     ],
     "options": [
      [
       "dispute",
       "Dispute the second charge"
      ],
      [
       "fine",
       "It was two orders"
      ]
     ],
     "party": "Zomato",
     "amount": 540.0,
     "when": "2026-09-04 20:16",
     "drafts": {
      "bank_dispute": {
       "subject": "Amount debited twice: Rs 540 at Zomato on 04 Sep 2026, 20:16",
       "body": "To the dispute desk, HDFC Bank\n\nAccount ending 9012\nAmount: Rs 540\nDate and time: 04 Sep 2026, 20:16\nReference: not in the message\nRecipient: Zomato\n\nThe same amount was charged twice, 2 minutes apart (first reference not in the message, second reference not in the message). I authorised one payment. Please reverse the second charge.\n\nThank you.",
       "helpline": "",
       "bank": "HDFC Bank"
      },
      "upi_help": {
       "applies": false,
       "issue": "Amount debited twice",
       "transaction_ref": "",
       "amount": "540",
       "date": "04 Sep 2026, 20:16",
       "recipient": "Zomato",
       "note": "This was a card payment, so UPI Help does not apply. Use the bank dispute."
      }
     },
     "interrupt_id": "v1:tool_call:playbook-cea6814682aa:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-7265498325d2",
     "decided_by": "rules",
     "created": "2026-09-12T12:31:13",
     "status": "decided",
     "decision": "dispute",
     "outcome": "Send the dispute letter to your bank, or read it to the helpline.",
     "decided": "2026-09-12T12:31:14"
    },
    "audit": [
     {
      "at": "2026-09-12T12:31:14",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "7265498325d2"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"7265498325d2\", \"party\": \"Zomato\", \"decision\": \"dispute\", \"next_steps\": [\"Send the dispute letter to your bank, or read it to the helpline.\"]}",
      "ms": 1.0
     }
    ]
   },
   "fine": {
    "card": {
     "id": "card-7265498325d2",
     "event_id": "7265498325d2",
     "kind": "double_charge",
     "headline": "You may be owed Rs 540: Zomato charged you twice and has not refunded it.",
     "evidence": [
      "Zomato charged Rs 540 twice, 2 minutes apart, on 4 Sep.",
      "No refund of Rs 540 has arrived in the 7 days since."
     ],
     "options": [
      [
       "dispute",
       "Dispute the second charge"
      ],
      [
       "fine",
       "It was two orders"
      ]
     ],
     "party": "Zomato",
     "amount": 540.0,
     "when": "2026-09-04 20:16",
     "drafts": {
      "bank_dispute": {
       "subject": "Amount debited twice: Rs 540 at Zomato on 04 Sep 2026, 20:16",
       "body": "To the dispute desk, HDFC Bank\n\nAccount ending 9012\nAmount: Rs 540\nDate and time: 04 Sep 2026, 20:16\nReference: not in the message\nRecipient: Zomato\n\nThe same amount was charged twice, 2 minutes apart (first reference not in the message, second reference not in the message). I authorised one payment. Please reverse the second charge.\n\nThank you.",
       "helpline": "",
       "bank": "HDFC Bank"
      },
      "upi_help": {
       "applies": false,
       "issue": "Amount debited twice",
       "transaction_ref": "",
       "amount": "540",
       "date": "04 Sep 2026, 20:16",
       "recipient": "Zomato",
       "note": "This was a card payment, so UPI Help does not apply. Use the bank dispute."
      }
     },
     "interrupt_id": "v1:tool_call:playbook-cea6814682aa:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-7265498325d2",
     "decided_by": "rules",
     "created": "2026-09-12T12:31:13",
     "status": "decided",
     "decision": "fine",
     "outcome": "Noted. Munshi will not ask about this payee again.",
     "decided": "2026-09-12T12:31:15"
    },
    "audit": [
     {
      "at": "2026-09-12T12:31:15",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "7265498325d2"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"7265498325d2\", \"party\": \"Zomato\", \"decision\": \"fine\", \"next_steps\": [\"Noted. Munshi will not ask about this payee again.\"]}",
      "ms": 1.0
     }
    ]
   }
  }
 }
};
