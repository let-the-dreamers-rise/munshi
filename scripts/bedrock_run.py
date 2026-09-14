"""Run Munshi on Amazon Bedrock for real, and write down what happened.

    python scripts/bedrock_run.py [--region us-east-1] [--model us.amazon.nova-pro-v1:0]

One command: the demo household, the real orchestrator, the interrupt, the family's answer, the
resume -- all on Bedrock -- and then `docs/bedrock-run.md` with the audit log exactly as the run
wrote it. If the account cannot call the model yet, it says so in the account's own words and
changes nothing.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from munshi.brain import DEFAULT_BEDROCK  # noqa: E402
from munshi.demo import demo_household  # noqa: E402
from munshi.service import Service  # noqa: E402

URGENT = "scam_shaped_payment"


def table(rows):
    out = ["| # | tool | status | result |", "|---|---|---|---|"]
    for i, row in enumerate(rows, 1):
        result = (row.get("result") or "").replace("|", "\\|").replace("\n", " ")[:110]
        refused = row.get("refused")
        out.append("| {0} | `{1}` | {2} | {3} |".format(
            i, row.get("tool"), row.get("refused") and "**refused**" or row.get("status"),
            refused or result))
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", default=os.environ.get("AWS_REGION", "us-east-1"))
    parser.add_argument("--model", default=os.environ.get("MUNSHI_BEDROCK_MODEL", DEFAULT_BEDROCK))
    parser.add_argument("--out", default=str(ROOT / "docs" / "bedrock-run.md"))
    opts = parser.parse_args()
    os.environ["AWS_REGION"], os.environ["MUNSHI_BEDROCK_MODEL"] = opts.region, opts.model

    household = demo_household()
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / "home"
        service = Service(home, household=household, model_kind="bedrock")
        try:
            outcomes = service.scan()
        except Exception as error:  # noqa: BLE001 -- the point of this script is to report it plainly
            print("Bedrock refused the run: {0}: {1}".format(type(error).__name__, error))
            return 2
        cards = [c for c in service.cards() if c["kind"] == URGENT]
        if not cards:
            print("No scam card was raised; nothing to write down.")
            return 1
        card = cards[0]
        decided = service.decide(card["id"], "report")
        audit = service.audit()

    text = """# A run on Amazon Bedrock

Munshi's orchestrator driven by **{model}** on Amazon Bedrock in `{region}`, on the demo household's
scam event, {when}. Nothing here is scripted: the model chose these steps from the system prompt, and
this is the `audit.jsonl` the run wrote, trimmed to the first 110 characters of each result.

{table}

- The card the family saw: *{headline}*
- The verdict was written by: `{who}`
- The family answered **report**, which resumed the same Strands session from the interrupt, and the
  run finished with: *{outcome}*
- Events handled in this run: {outcomes}
""".format(model=opts.model, region=opts.region, when=datetime.now().strftime("%d %b %Y"),
           table=table(audit), headline=card["headline"], who=card.get("decided_by", "unknown"),
           outcome=(decided.get("outcome") or "").splitlines()[0] if decided.get("outcome") else "-",
           outcomes=json.dumps(outcomes))
    Path(opts.out).write_text(text, encoding="utf-8", newline="\n")
    print(text)
    print("\nWritten to " + opts.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
