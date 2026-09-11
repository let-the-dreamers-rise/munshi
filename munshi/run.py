"""Munshi from a terminal.

    python -m munshi.run demo            Meera's phone, scanned now; cards land in .munshi/
    python -m munshi.run cards           what is waiting for the family
    python -m munshi.run decide CARD CHOICE
    python -m munshi.run serve           the inbox at http://127.0.0.1:8765
    python -m munshi.run payload         what the phone sends to AgentCore, as a scan request

--model playbook runs with no credentials; bedrock (default) and ollama use a real model.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

from .demo import demo_household
from .money import rs
from .service import Service


def _print_card(card):
    mark = "*" if card["status"] == "pending" else " "
    print("{0} {1}  {2}".format(mark, card["id"], card["headline"]))
    for line in card["evidence"]:
        print("      - " + line)
    if card["status"] == "pending":
        print("      choose: " + " | ".join("{0} ({1})".format(k, label) for k, label in card["options"]))
    else:
        print("      decided: {0}\n      ".format(card["decision"]) + card["outcome"].replace("\n", "\n      "))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="munshi", description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["demo", "cards", "decide", "serve", "payload"])
    parser.add_argument("args", nargs="*")
    parser.add_argument("--home", default=".munshi")
    parser.add_argument("--model", default=None, help="bedrock (default), ollama or playbook")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--days", type=int, default=0, help="payload: only the last N days of the ledger")
    opts = parser.parse_args(argv)
    home = Path(opts.home)
    if opts.command == "payload":
        body = demo_household().to_payload()
        if opts.days:
            since = (datetime.strptime(body["now"], "%Y-%m-%d %H:%M") - timedelta(days=opts.days)).strftime("%Y-%m-%d %H:%M")
            body = {**body, "ledger": [r for r in body["ledger"] if r["when"] >= since]}
        print(json.dumps({"action": "scan", "household": body}, separators=(",", ":")))
        return 0
    if opts.command == "serve":
        from .serve import serve
        return serve(home, opts.model, opts.port)
    if opts.command == "demo":
        service = Service(home, household=demo_household(), model_kind=opts.model)
        ledger = service.household.ledger
        print("Watched {0} payments over {1} days. Events: {2}".format(
            len(ledger.rows), ledger.history_days(), len(service.household.events)))
        for event_id, what in service.scan().items():
            print("  {0}: {1}".format(event_id, what))
    else:
        service = Service(home, model_kind=opts.model)
    if opts.command == "decide":
        if len(opts.args) != 2:
            parser.error("decide takes CARD CHOICE")
        try:
            card = service.decide(*opts.args)
        except (KeyError, ValueError) as error:
            print("error: " + str(error), file=sys.stderr)
            return 2
        _print_card(card)
        return 0
    for card in service.cards():
        _print_card(card)
    return 0


if __name__ == "__main__":
    sys.exit(main())
