window.MUNSHI_REPLAY = {
 "recorded_at": "11 Sep 2026, 21:08",
 "initial": {
  "household": "meera",
  "now": "2026-09-11 21:08",
  "watched": {
   "payments": 216,
   "days": 99
  },
  "cards": [
   {
    "id": "card-83d992230c78",
    "event_id": "83d992230c78",
    "kind": "scam_shaped_payment",
    "headline": "Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown number. This is how the KYC scam works.",
    "evidence": [
     "kyc.update9@ybl had never been paid before: this is the first payment in 99 days of history.",
     "The payment came 9 minutes after a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'.",
     "Rs 12,000 is 58 times the household's usual payment of Rs 208."
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
    "when": "2026-09-11 21:03",
    "drafts": {
     "cybercrime_report": {
      "where": "1930 and https://cybercrime.gov.in",
      "call_before": "22:03 on 11 Sep 2026",
      "text": "Call 1930 now, before 22:03. The first hour is when a bank can still hold the money. Read them the fields below, then file the same details at cybercrime.gov.in under financial fraud and keep the acknowledgement number.",
      "fields": {
       "Category": "Online Financial Fraud",
       "Sub-category": "UPI related fraud",
       "Date and time of transaction": "11 Sep 2026, 21:03",
       "Amount (Rs)": "12,000",
       "Transaction ID / UTR": "624511873920",
       "Bank": "HDFC Bank",
       "Account (last digits)": "4521",
       "Suspect UPI ID": "kyc.update9@ybl",
       "Suspect phone": "+919811234567",
       "What happened": "I received a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'. 9 minutes later, Rs 12,000 left my HDFC Bank account ending 4521 to kyc.update9@ybl on 11 Sep 2026, 21:03 (reference 624511873920). I had never paid this recipient before."
      }
     },
     "bank_dispute": {
      "subject": "Unauthorised UPI debit of Rs 12,000 on 11 Sep 2026, 21:03, reference 624511873920",
      "body": "To the dispute desk, HDFC Bank\n\nAccount ending 4521\nAmount: Rs 12,000\nDate and time: 11 Sep 2026, 21:03\nReference: 624511873920\nRecipient: kyc.update9@ybl\n\nI did not knowingly authorise this payment to kyc.update9@ybl. Please block further debits to this recipient, raise a dispute, and ask the receiving bank to hold the amount. I am reporting it to 1930 and cybercrime.gov.in.\n\nThank you.",
      "helpline": "18002586161",
      "bank": "HDFC Bank"
     },
     "upi_help": {
      "applies": true,
      "issue": "Fraud or unauthorised transaction",
      "transaction_ref": "624511873920",
      "amount": "12,000",
      "date": "11 Sep 2026, 21:03",
      "recipient": "kyc.update9@ybl",
      "note": "In the UPI app you paid from, open UPI Help (or Help, then report an issue) on this payment."
     }
    },
    "interrupt_id": "v1:tool_call:playbook-ab6c3563ba91:a03c9326-dd4c-5878-95a5-2d96fbe58668",
    "session_id": "meera-83d992230c78",
    "decided_by": "rules",
    "created": "2026-09-11T21:08:00",
    "status": "pending",
    "decision": "",
    "outcome": "",
    "decided": ""
   },
   {
    "id": "card-12b5f59f576c",
    "event_id": "12b5f59f576c",
    "kind": "renewal_due",
    "headline": "Netflix renews tomorrow at Rs 649. It was Rs 499.",
    "evidence": [
     "Netflix has charged you 3 times, every 31 days. The next charge is due tomorrow, 12 Sep.",
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
    "when": "2026-08-12 09:00",
    "drafts": {},
    "interrupt_id": "v1:tool_call:playbook-2249764fba49:a03c9326-dd4c-5878-95a5-2d96fbe58668",
    "session_id": "meera-12b5f59f576c",
    "decided_by": "rules",
    "created": "2026-09-11T21:08:00",
    "status": "pending",
    "decision": "",
    "outcome": "",
    "decided": ""
   },
   {
    "id": "card-71d94f8d7f06",
    "event_id": "71d94f8d7f06",
    "kind": "double_charge",
    "headline": "You may be owed Rs 540: Zomato charged you twice and has not refunded it.",
    "evidence": [
     "Zomato charged Rs 540 twice, 2 minutes apart, on 3 Sep.",
     "No refund of Rs 540 has arrived in the 8 days since."
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
    "when": "2026-09-03 20:16",
    "drafts": {
     "bank_dispute": {
      "subject": "Amount debited twice: Rs 540 at Zomato on 03 Sep 2026, 20:16",
      "body": "To the dispute desk, HDFC Bank\n\nAccount ending 9012\nAmount: Rs 540\nDate and time: 03 Sep 2026, 20:16\nReference: not in the message\nRecipient: Zomato\n\nThe same amount was charged twice, 2 minutes apart (first reference not in the message, second reference not in the message). I authorised one payment. Please reverse the second charge.\n\nThank you.",
      "helpline": "",
      "bank": "HDFC Bank"
     },
     "upi_help": {
      "applies": false,
      "issue": "Amount debited twice",
      "transaction_ref": "",
      "amount": "540",
      "date": "03 Sep 2026, 20:16",
      "recipient": "Zomato",
      "note": "This was a card payment, so UPI Help does not apply. Use the bank dispute."
     }
    },
    "interrupt_id": "v1:tool_call:playbook-08158a7bc45f:a03c9326-dd4c-5878-95a5-2d96fbe58668",
    "session_id": "meera-71d94f8d7f06",
    "decided_by": "rules",
    "created": "2026-09-11T21:08:00",
    "status": "pending",
    "decision": "",
    "outcome": "",
    "decided": ""
   }
  ],
  "audit": [
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "investigate_payment",
    "input": {
     "event_id": "83d992230c78"
    },
    "status": "success",
    "refused": null,
    "result": "{\"verdict\": {\"kind\": \"likely_scam\", \"confidence\": 0.9, \"headline\": \"Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown number. This is how the KYC scam works.\", \"recommended\": \"report_now\"}, \"facts\": [\"kyc.update9@ybl had never been paid before: this is the first payment in 99 days of history.\", \"The payment came 9 minutes after a message from ",
    "ms": 0.9
   },
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "draft_cybercrime_report",
    "input": {
     "event_id": "83d992230c78"
    },
    "status": "success",
    "refused": null,
    "result": "{\"where\": \"1930 and https://cybercrime.gov.in\", \"call_before\": \"22:03 on 11 Sep 2026\", \"text\": \"Call 1930 now, before 22:03. The first hour is when a bank can still hold the money. Read them the fields below, then file the same details at cybercrime.gov.in under financial fraud and keep the acknowledgement number.\", \"fields\": {\"Category\": \"Online Financial Fraud\", \"Sub-category\": \"UPI related frau",
    "ms": 0.8
   },
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "draft_bank_dispute",
    "input": {
     "event_id": "83d992230c78"
    },
    "status": "success",
    "refused": null,
    "result": "{\"subject\": \"Unauthorised UPI debit of Rs 12,000 on 11 Sep 2026, 21:03, reference 624511873920\", \"body\": \"To the dispute desk, HDFC Bank\\n\\nAccount ending 4521\\nAmount: Rs 12,000\\nDate and time: 11 Sep 2026, 21:03\\nReference: 624511873920\\nRecipient: kyc.update9@ybl\\n\\nI did not knowingly authorise this payment to kyc.update9@ybl. Please block further debits to this recipient, raise a dispute, and",
    "ms": 0.6
   },
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "draft_upi_help_complaint",
    "input": {
     "event_id": "83d992230c78"
    },
    "status": "success",
    "refused": null,
    "result": "{\"applies\": true, \"issue\": \"Fraud or unauthorised transaction\", \"transaction_ref\": \"624511873920\", \"amount\": \"12,000\", \"date\": \"11 Sep 2026, 21:03\", \"recipient\": \"kyc.update9@ybl\", \"note\": \"In the UPI app you paid from, open UPI Help (or Help, then report an issue) on this payment.\"}",
    "ms": 0.8
   },
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "ask_household",
    "input": {
     "event_id": "83d992230c78"
    },
    "status": "waiting for the household",
    "refused": null,
    "result": "Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown number. This is how the KYC scam works.",
    "ms": 0.0
   },
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "investigate_payment",
    "input": {
     "event_id": "12b5f59f576c"
    },
    "status": "success",
    "refused": null,
    "result": "{\"verdict\": {\"kind\": \"renewal\", \"confidence\": 0.9, \"headline\": \"Netflix renews tomorrow at Rs 649. It was Rs 499.\", \"recommended\": \"remind\"}, \"facts\": [\"Netflix has charged you 3 times, every 31 days. The next charge is due tomorrow, 12 Sep.\", \"The last charge was Rs 649, up from Rs 499.\"], \"decided_by\": \"rules\"}",
    "ms": 0.6
   },
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "ask_household",
    "input": {
     "event_id": "12b5f59f576c"
    },
    "status": "waiting for the household",
    "refused": null,
    "result": "Netflix renews tomorrow at Rs 649. It was Rs 499.",
    "ms": 0.0
   },
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "investigate_payment",
    "input": {
     "event_id": "71d94f8d7f06"
    },
    "status": "success",
    "refused": null,
    "result": "{\"verdict\": {\"kind\": \"double_charge\", \"confidence\": 0.8, \"headline\": \"You may be owed Rs 540: Zomato charged you twice and has not refunded it.\", \"recommended\": \"dispute\"}, \"facts\": [\"Zomato charged Rs 540 twice, 2 minutes apart, on 3 Sep.\", \"No refund of Rs 540 has arrived in the 8 days since.\"], \"decided_by\": \"rules\"}",
    "ms": 0.5
   },
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "draft_bank_dispute",
    "input": {
     "event_id": "71d94f8d7f06"
    },
    "status": "success",
    "refused": null,
    "result": "{\"subject\": \"Amount debited twice: Rs 540 at Zomato on 03 Sep 2026, 20:16\", \"body\": \"To the dispute desk, HDFC Bank\\n\\nAccount ending 9012\\nAmount: Rs 540\\nDate and time: 03 Sep 2026, 20:16\\nReference: not in the message\\nRecipient: Zomato\\n\\nThe same amount was charged twice, 2 minutes apart (first reference not in the message, second reference not in the message). I authorised one payment. Pleas",
    "ms": 0.6
   },
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "draft_upi_help_complaint",
    "input": {
     "event_id": "71d94f8d7f06"
    },
    "status": "success",
    "refused": null,
    "result": "{\"applies\": false, \"issue\": \"Amount debited twice\", \"transaction_ref\": \"\", \"amount\": \"540\", \"date\": \"03 Sep 2026, 20:16\", \"recipient\": \"Zomato\", \"note\": \"This was a card payment, so UPI Help does not apply. Use the bank dispute.\"}",
    "ms": 0.5
   },
   {
    "at": "2026-09-11T21:08:00",
    "agent": "munshi",
    "tool": "ask_household",
    "input": {
     "event_id": "71d94f8d7f06"
    },
    "status": "waiting for the household",
    "refused": null,
    "result": "You may be owed Rs 540: Zomato charged you twice and has not refunded it.",
    "ms": 0.0
   }
  ]
 },
 "outcomes": {
  "card-83d992230c78": {
   "report": {
    "card": {
     "id": "card-83d992230c78",
     "event_id": "83d992230c78",
     "kind": "scam_shaped_payment",
     "headline": "Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown number. This is how the KYC scam works.",
     "evidence": [
      "kyc.update9@ybl had never been paid before: this is the first payment in 99 days of history.",
      "The payment came 9 minutes after a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'.",
      "Rs 12,000 is 58 times the household's usual payment of Rs 208."
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
     "when": "2026-09-11 21:03",
     "drafts": {
      "cybercrime_report": {
       "where": "1930 and https://cybercrime.gov.in",
       "call_before": "22:03 on 11 Sep 2026",
       "text": "Call 1930 now, before 22:03. The first hour is when a bank can still hold the money. Read them the fields below, then file the same details at cybercrime.gov.in under financial fraud and keep the acknowledgement number.",
       "fields": {
        "Category": "Online Financial Fraud",
        "Sub-category": "UPI related fraud",
        "Date and time of transaction": "11 Sep 2026, 21:03",
        "Amount (Rs)": "12,000",
        "Transaction ID / UTR": "624511873920",
        "Bank": "HDFC Bank",
        "Account (last digits)": "4521",
        "Suspect UPI ID": "kyc.update9@ybl",
        "Suspect phone": "+919811234567",
        "What happened": "I received a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'. 9 minutes later, Rs 12,000 left my HDFC Bank account ending 4521 to kyc.update9@ybl on 11 Sep 2026, 21:03 (reference 624511873920). I had never paid this recipient before."
       }
      },
      "bank_dispute": {
       "subject": "Unauthorised UPI debit of Rs 12,000 on 11 Sep 2026, 21:03, reference 624511873920",
       "body": "To the dispute desk, HDFC Bank\n\nAccount ending 4521\nAmount: Rs 12,000\nDate and time: 11 Sep 2026, 21:03\nReference: 624511873920\nRecipient: kyc.update9@ybl\n\nI did not knowingly authorise this payment to kyc.update9@ybl. Please block further debits to this recipient, raise a dispute, and ask the receiving bank to hold the amount. I am reporting it to 1930 and cybercrime.gov.in.\n\nThank you.",
       "helpline": "18002586161",
       "bank": "HDFC Bank"
      },
      "upi_help": {
       "applies": true,
       "issue": "Fraud or unauthorised transaction",
       "transaction_ref": "624511873920",
       "amount": "12,000",
       "date": "11 Sep 2026, 21:03",
       "recipient": "kyc.update9@ybl",
       "note": "In the UPI app you paid from, open UPI Help (or Help, then report an issue) on this payment."
      }
     },
     "interrupt_id": "v1:tool_call:playbook-ab6c3563ba91:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-83d992230c78",
     "decided_by": "rules",
     "created": "2026-09-11T21:08:00",
     "status": "decided",
     "decision": "report",
     "outcome": "Call 1930 now, inside the first hour, and read them the report fields.\nFile the same details at cybercrime.gov.in and keep the acknowledgement number.\nCall HDFC Bank on 18002586161 and ask them to block the recipient and raise a dispute.",
     "decided": "2026-09-11T21:08:00"
    },
    "audit": [
     {
      "at": "2026-09-11T21:08:00",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "83d992230c78"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"83d992230c78\", \"party\": \"kyc.update9@ybl\", \"decision\": \"report\", \"next_steps\": [\"Call 1930 now, inside the first hour, and read them the report fields.\", \"File the same details at cybercrime.gov.in and keep the acknowledgement number.\", \"Call HDFC Bank on 18002586161 and ask them to block the recipient and raise a dispute.\"]}",
      "ms": 0.8
     }
    ]
   },
   "fine": {
    "card": {
     "id": "card-83d992230c78",
     "event_id": "83d992230c78",
     "kind": "scam_shaped_payment",
     "headline": "Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown number. This is how the KYC scam works.",
     "evidence": [
      "kyc.update9@ybl had never been paid before: this is the first payment in 99 days of history.",
      "The payment came 9 minutes after a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'.",
      "Rs 12,000 is 58 times the household's usual payment of Rs 208."
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
     "when": "2026-09-11 21:03",
     "drafts": {
      "cybercrime_report": {
       "where": "1930 and https://cybercrime.gov.in",
       "call_before": "22:03 on 11 Sep 2026",
       "text": "Call 1930 now, before 22:03. The first hour is when a bank can still hold the money. Read them the fields below, then file the same details at cybercrime.gov.in under financial fraud and keep the acknowledgement number.",
       "fields": {
        "Category": "Online Financial Fraud",
        "Sub-category": "UPI related fraud",
        "Date and time of transaction": "11 Sep 2026, 21:03",
        "Amount (Rs)": "12,000",
        "Transaction ID / UTR": "624511873920",
        "Bank": "HDFC Bank",
        "Account (last digits)": "4521",
        "Suspect UPI ID": "kyc.update9@ybl",
        "Suspect phone": "+919811234567",
        "What happened": "I received a message from +919811234567 containing 'kyc', 'blocked' and 'immediately'. 9 minutes later, Rs 12,000 left my HDFC Bank account ending 4521 to kyc.update9@ybl on 11 Sep 2026, 21:03 (reference 624511873920). I had never paid this recipient before."
       }
      },
      "bank_dispute": {
       "subject": "Unauthorised UPI debit of Rs 12,000 on 11 Sep 2026, 21:03, reference 624511873920",
       "body": "To the dispute desk, HDFC Bank\n\nAccount ending 4521\nAmount: Rs 12,000\nDate and time: 11 Sep 2026, 21:03\nReference: 624511873920\nRecipient: kyc.update9@ybl\n\nI did not knowingly authorise this payment to kyc.update9@ybl. Please block further debits to this recipient, raise a dispute, and ask the receiving bank to hold the amount. I am reporting it to 1930 and cybercrime.gov.in.\n\nThank you.",
       "helpline": "18002586161",
       "bank": "HDFC Bank"
      },
      "upi_help": {
       "applies": true,
       "issue": "Fraud or unauthorised transaction",
       "transaction_ref": "624511873920",
       "amount": "12,000",
       "date": "11 Sep 2026, 21:03",
       "recipient": "kyc.update9@ybl",
       "note": "In the UPI app you paid from, open UPI Help (or Help, then report an issue) on this payment."
      }
     },
     "interrupt_id": "v1:tool_call:playbook-ab6c3563ba91:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-83d992230c78",
     "decided_by": "rules",
     "created": "2026-09-11T21:08:00",
     "status": "decided",
     "decision": "fine",
     "outcome": "Noted. Munshi will not ask about this payee again.",
     "decided": "2026-09-11T21:08:00"
    },
    "audit": [
     {
      "at": "2026-09-11T21:08:00",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "83d992230c78"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"83d992230c78\", \"party\": \"kyc.update9@ybl\", \"decision\": \"fine\", \"next_steps\": [\"Noted. Munshi will not ask about this payee again.\"]}",
      "ms": 0.7
     },
     {
      "at": "2026-09-11T21:08:00",
      "agent": "munshi",
      "tool": "remember_trusted_payee",
      "input": {
       "party": "kyc.update9@ybl"
      },
      "status": "success",
      "refused": null,
      "result": "{\"trusted\": \"kyc.update9@ybl\"}",
      "ms": 3.7
     }
    ]
   }
  },
  "card-12b5f59f576c": {
   "keep": {
    "card": {
     "id": "card-12b5f59f576c",
     "event_id": "12b5f59f576c",
     "kind": "renewal_due",
     "headline": "Netflix renews tomorrow at Rs 649. It was Rs 499.",
     "evidence": [
      "Netflix has charged you 3 times, every 31 days. The next charge is due tomorrow, 12 Sep.",
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
     "when": "2026-08-12 09:00",
     "drafts": {},
     "interrupt_id": "v1:tool_call:playbook-2249764fba49:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-12b5f59f576c",
     "decided_by": "rules",
     "created": "2026-09-11T21:08:00",
     "status": "decided",
     "decision": "keep",
     "outcome": "Kept. Munshi will not remind you about this renewal.",
     "decided": "2026-09-11T21:08:00"
    },
    "audit": [
     {
      "at": "2026-09-11T21:08:00",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "12b5f59f576c"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"12b5f59f576c\", \"party\": \"Netflix\", \"decision\": \"keep\", \"next_steps\": [\"Kept. Munshi will not remind you about this renewal.\"]}",
      "ms": 0.7
     }
    ]
   },
   "cancel": {
    "card": {
     "id": "card-12b5f59f576c",
     "event_id": "12b5f59f576c",
     "kind": "renewal_due",
     "headline": "Netflix renews tomorrow at Rs 649. It was Rs 499.",
     "evidence": [
      "Netflix has charged you 3 times, every 31 days. The next charge is due tomorrow, 12 Sep.",
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
     "when": "2026-08-12 09:00",
     "drafts": {},
     "interrupt_id": "v1:tool_call:playbook-2249764fba49:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-12b5f59f576c",
     "decided_by": "rules",
     "created": "2026-09-11T21:08:00",
     "status": "decided",
     "decision": "cancel",
     "outcome": "Cancel it in the app or on the website before the due date. Munshi cannot cancel for you.",
     "decided": "2026-09-11T21:08:01"
    },
    "audit": [
     {
      "at": "2026-09-11T21:08:01",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "12b5f59f576c"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"12b5f59f576c\", \"party\": \"Netflix\", \"decision\": \"cancel\", \"next_steps\": [\"Cancel it in the app or on the website before the due date. Munshi cannot cancel for you.\"]}",
      "ms": 0.6
     }
    ]
   }
  },
  "card-71d94f8d7f06": {
   "dispute": {
    "card": {
     "id": "card-71d94f8d7f06",
     "event_id": "71d94f8d7f06",
     "kind": "double_charge",
     "headline": "You may be owed Rs 540: Zomato charged you twice and has not refunded it.",
     "evidence": [
      "Zomato charged Rs 540 twice, 2 minutes apart, on 3 Sep.",
      "No refund of Rs 540 has arrived in the 8 days since."
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
     "when": "2026-09-03 20:16",
     "drafts": {
      "bank_dispute": {
       "subject": "Amount debited twice: Rs 540 at Zomato on 03 Sep 2026, 20:16",
       "body": "To the dispute desk, HDFC Bank\n\nAccount ending 9012\nAmount: Rs 540\nDate and time: 03 Sep 2026, 20:16\nReference: not in the message\nRecipient: Zomato\n\nThe same amount was charged twice, 2 minutes apart (first reference not in the message, second reference not in the message). I authorised one payment. Please reverse the second charge.\n\nThank you.",
       "helpline": "",
       "bank": "HDFC Bank"
      },
      "upi_help": {
       "applies": false,
       "issue": "Amount debited twice",
       "transaction_ref": "",
       "amount": "540",
       "date": "03 Sep 2026, 20:16",
       "recipient": "Zomato",
       "note": "This was a card payment, so UPI Help does not apply. Use the bank dispute."
      }
     },
     "interrupt_id": "v1:tool_call:playbook-08158a7bc45f:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-71d94f8d7f06",
     "decided_by": "rules",
     "created": "2026-09-11T21:08:00",
     "status": "decided",
     "decision": "dispute",
     "outcome": "Send the dispute letter to your bank, or read it to the helpline.",
     "decided": "2026-09-11T21:08:01"
    },
    "audit": [
     {
      "at": "2026-09-11T21:08:01",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "71d94f8d7f06"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"71d94f8d7f06\", \"party\": \"Zomato\", \"decision\": \"dispute\", \"next_steps\": [\"Send the dispute letter to your bank, or read it to the helpline.\"]}",
      "ms": 0.8
     }
    ]
   },
   "fine": {
    "card": {
     "id": "card-71d94f8d7f06",
     "event_id": "71d94f8d7f06",
     "kind": "double_charge",
     "headline": "You may be owed Rs 540: Zomato charged you twice and has not refunded it.",
     "evidence": [
      "Zomato charged Rs 540 twice, 2 minutes apart, on 3 Sep.",
      "No refund of Rs 540 has arrived in the 8 days since."
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
     "when": "2026-09-03 20:16",
     "drafts": {
      "bank_dispute": {
       "subject": "Amount debited twice: Rs 540 at Zomato on 03 Sep 2026, 20:16",
       "body": "To the dispute desk, HDFC Bank\n\nAccount ending 9012\nAmount: Rs 540\nDate and time: 03 Sep 2026, 20:16\nReference: not in the message\nRecipient: Zomato\n\nThe same amount was charged twice, 2 minutes apart (first reference not in the message, second reference not in the message). I authorised one payment. Please reverse the second charge.\n\nThank you.",
       "helpline": "",
       "bank": "HDFC Bank"
      },
      "upi_help": {
       "applies": false,
       "issue": "Amount debited twice",
       "transaction_ref": "",
       "amount": "540",
       "date": "03 Sep 2026, 20:16",
       "recipient": "Zomato",
       "note": "This was a card payment, so UPI Help does not apply. Use the bank dispute."
      }
     },
     "interrupt_id": "v1:tool_call:playbook-08158a7bc45f:a03c9326-dd4c-5878-95a5-2d96fbe58668",
     "session_id": "meera-71d94f8d7f06",
     "decided_by": "rules",
     "created": "2026-09-11T21:08:00",
     "status": "decided",
     "decision": "fine",
     "outcome": "Noted. Munshi will not ask about this payee again.",
     "decided": "2026-09-11T21:08:01"
    },
    "audit": [
     {
      "at": "2026-09-11T21:08:01",
      "agent": "munshi",
      "tool": "ask_household",
      "input": {
       "event_id": "71d94f8d7f06"
      },
      "status": "success",
      "refused": null,
      "result": "{\"event_id\": \"71d94f8d7f06\", \"party\": \"Zomato\", \"decision\": \"fine\", \"next_steps\": [\"Noted. Munshi will not ask about this payee again.\"]}",
      "ms": 2.0
     }
    ]
   }
  }
 }
};
