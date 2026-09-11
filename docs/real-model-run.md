# A run with a real model

Munshi's orchestrator driven by **qwen2.5:3b** through Ollama on a laptop, on the demo household's scam
event, 11 Sep 2026. No script chose these steps: the model did, from the system prompt. This is the
`audit.jsonl` the run wrote, trimmed to the first 110 characters of each result.

| # | tool | status | result |
|---|---|---|---|
| 1 | `investigate_payment` | success | {"verdict": {"kind": "likely_scam", "confidence": 0.9, "headline": "Rs 12,000 went to kyc.update9@ybl, someone |
| 2 | `draft_cybercrime_report` | success | {"where": "1930 and https://cybercrime.gov.in", "call_before": "22:39 on 11 Sep 2026", "text": "Call 1930 now, |
| 3 | `draft_bank_dispute` | success | {"subject": "Unauthorised UPI debit of Rs 12,000 on 11 Sep 2026, 21:39, reference 624511873920", "body": "To t |
| 4 | `draft_upi_help_complaint` | success | {"applies": true, "issue": "Fraud or unauthorised transaction", "transaction_ref": "624511873920", "amount": " |
| 5 | `ask_household` | waiting for the household | Rs 12,000 went to kyc.update9@ybl, someone you have never paid, 9 minutes after a threat from an unknown numbe |
| 6 | `ask_household` | success | {"event_id": "33548fa85689", "party": "kyc.update9@ybl", "decision": "report", "next_steps": ["Call 1930 now,  |

What it shows:

- The model called `investigate_payment`, all three `draft_*` tools and `ask_household`, in the order the
  system prompt gives. `ask_household` raised a Strands interrupt; the card was filed with interrupt id
  `v1:tool_call:tooluse_a5ba0aadaf2242df94b...`.
- The family's answer (`report`) resumed the same session from disk, and `ask_household` completed.
- The investigator sub-agent on the same 3B model failed to produce a structured `Verdict`. The card's
  verdict came from the rules, and the card says so: `decided_by` is `rules (the model failed: StructuredOutputException)`.
- On an earlier run the same model did return a `Verdict`, but its headline leaked the code `report_now`.
  Since then a model's headline reaches the card only if it quotes the exact amount and no codes.

Bedrock (Nova Pro by default) is the intended model; this run exists because it needs no account.
