"""What the family has told Munshi: payees they trust, events already handled."""

from __future__ import annotations

import json
import os
from pathlib import Path

from .filelock import locked


class Prefs:
    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        if not self.path.exists():
            return {"trusted": [], "handled": []}
        data = json.loads(self.path.read_text(encoding="utf-8") or "{}")
        return {"trusted": list(data.get("trusted", [])), "handled": list(data.get("handled", []))}

    def _add(self, key, value):
        with locked(self.path):
            data = self.load()
            if value in data[key]:
                return data
            updated = {**data, key: data[key] + [value]}
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(updated, indent=1), encoding="utf-8")
            os.replace(tmp, self.path)
            return updated

    def trust(self, party):
        return self._add("trusted", party)

    def handle(self, event_id):
        return self._add("handled", event_id)
