"""Decision cards: the only way Munshi ever speaks to a person."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path

OPTIONS = {
    "scam_shaped_payment": (("report", "Report it now"), ("fine", "I made this payment on purpose")),
    "unusual_payment": (("fine", "It was me"), ("report", "I did not make this")),
    "double_charge": (("dispute", "Dispute the second charge"), ("fine", "It was two orders")),
    "renewal_due": (("keep", "Keep it"), ("cancel", "Remind me to cancel it first")),
}


@dataclass(frozen=True)
class Card:
    id: str
    event_id: str
    kind: str
    headline: str
    evidence: tuple
    options: tuple
    party: str
    amount: float
    when: str
    drafts: dict = field(default_factory=dict)
    interrupt_id: str = ""
    session_id: str = ""
    decided_by: str = "rules"
    created: str = ""
    status: str = "pending"
    decision: str = ""
    outcome: str = ""
    decided: str = ""

    def as_dict(self):
        d = dict(self.__dict__)
        d["evidence"] = list(self.evidence)
        d["options"] = [list(o) for o in self.options]
        return d

    @classmethod
    def from_dict(cls, d):
        data = dict(d)
        data["evidence"] = tuple(data.get("evidence", ()))
        data["options"] = tuple(tuple(o) for o in data.get("options", ()))
        return cls(**data)


def card_id(event_id):
    return "card-" + event_id


class Inbox:
    def __init__(self, path):
        self.path = Path(path)

    def _load(self):
        if not self.path.exists():
            return []
        return [Card.from_dict(d) for d in json.loads(self.path.read_text(encoding="utf-8") or "[]")]

    def _save(self, cards):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps([c.as_dict() for c in cards], indent=1), encoding="utf-8")
        os.replace(tmp, self.path)

    def all(self):
        return self._load()

    def pending(self):
        return [c for c in self._load() if c.status == "pending"]

    def get(self, cid):
        for c in self._load():
            if c.id == cid:
                return c
        raise KeyError("no card {0!r}".format(cid))

    def has_event(self, event_id):
        return any(c.event_id == event_id for c in self._load())

    def put(self, card):
        stamped = card if card.created else replace(card, created=datetime.now().isoformat(timespec="seconds"))
        self._save([c for c in self._load() if c.id != stamped.id] + [stamped])
        return stamped

    def decide(self, cid, decision, outcome):
        done = replace(self.get(cid), status="decided", decision=decision, outcome=outcome,
                       decided=datetime.now().isoformat(timespec="seconds"))
        self._save([done if c.id == cid else c for c in self._load()])
        return done
