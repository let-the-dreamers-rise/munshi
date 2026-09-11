"""The ledger the agent may query: every movement of money, with no message text in it."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

TIME = "%Y-%m-%d %H:%M"


@dataclass(frozen=True)
class Row:
    when: datetime
    amount: float
    direction: str  # 'out' or 'in'
    party: str
    channel: str
    account: str
    bank: str
    ref: str
    helpline: str

    def as_dict(self):
        return {"when": self.when.strftime(TIME), "amount": self.amount, "direction": self.direction,
                "party": self.party, "channel": self.channel, "account": self.account,
                "bank": self.bank, "ref": self.ref, "helpline": self.helpline}

    @classmethod
    def from_dict(cls, d):
        return cls(datetime.strptime(d["when"], TIME), float(d["amount"]), d["direction"], d.get("party", ""),
                   d.get("channel", "other"), d.get("account", ""), d.get("bank", ""), d.get("ref", ""),
                   d.get("helpline", ""))


class Ledger:
    def __init__(self, rows):
        self.rows = tuple(sorted(rows, key=lambda r: r.when))

    def _out(self, party=None):
        return [r for r in self.rows if r.direction == "out" and (party is None or r.party == party)]

    def payee_history(self, party):
        """Everything the ledger knows about paying one party."""
        rows = self._out(party)
        return {
            "party": party,
            "times_paid": len(rows),
            "total_paid": round(sum(r.amount for r in rows), 2),
            "first_paid": rows[0].when.strftime(TIME) if rows else None,
            "last_paid": rows[-1].when.strftime(TIME) if rows else None,
            "last_amounts": [r.amount for r in rows[-5:]],
            "channels": sorted({r.channel for r in rows}),
        }

    def recent(self, days=7, party="", now=None):
        now = now or (self.rows[-1].when if self.rows else datetime.now())
        lo = now - timedelta(days=days)
        return [r.as_dict() for r in self.rows
                if lo <= r.when <= now and (not party or r.party == party)]

    def usual_payment(self):
        amounts = sorted(r.amount for r in self._out())
        return amounts[len(amounts) // 2] if amounts else 0.0

    def history_days(self):
        return (self.rows[-1].when - self.rows[0].when).days if self.rows else 0
