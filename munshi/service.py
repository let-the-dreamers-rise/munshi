"""One household's Munshi: scan for events, list cards, record a decision. Used by the CLI, the
loopback inbox and the AgentCore entrypoint, so all three behave the same."""

from __future__ import annotations

import json
from pathlib import Path

from .brain import make_investigator, make_model
from .runner import Runner
from .witness import Household

URGENT = ("scam_shaped_payment", "unusual_payment")


def _order(event):
    return (0 if event.kind in URGENT else 1, event.when)


class Service:
    def __init__(self, home, household=None, model_kind=None, model=None, investigator_model=None):
        self.home = Path(home)
        if household is None:
            household = Household.from_payload(json.loads((self.home / "household.json").read_text(encoding="utf-8")))
        if model is None:
            model, investigator_model = make_model(model_kind), make_investigator(model_kind)
        self.runner = Runner(self.home, household, model=model, investigator_model=investigator_model)

    @property
    def household(self):
        return self.runner.household

    def scan(self):
        """Hand every event to the agent, the urgent ones first. Returns what happened to each."""
        return {e.id: self.runner.handle(e) for e in sorted(self.household.events, key=_order)}

    def cards(self):
        return [c.as_dict() for c in self.runner.inbox.all()]

    def decide(self, card_id, choice):
        return self.runner.decide(card_id, choice).as_dict()

    def audit(self, last=60):
        path = self.home / "audit.jsonl"
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()[-last:]]

    def state(self):
        ledger = self.household.ledger
        return {"household": self.household.name, "now": self.household.now.strftime("%Y-%m-%d %H:%M"),
                "watched": {"payments": len(ledger.rows), "days": ledger.history_days()},
                "cards": self.cards(), "audit": self.audit()}
