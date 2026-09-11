"""Munshi on Amazon Bedrock AgentCore Runtime.

The phone runs the witness and sends only the household payload: ledger rows
and events, never a message. Each household is one AgentCore runtime session,
so its inbox and the paused agent sessions live together; set MUNSHI_S3_BUCKET
to keep the agent sessions in S3 as well.

    {"action": "scan", "household": {...payload...}}
    {"action": "cards"}
    {"action": "decide", "card": "card-...", "choice": "report"}
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from bedrock_agentcore.runtime import BedrockAgentCoreApp

from .service import Service
from .witness import Household

app = BedrockAgentCoreApp()
ROOT = Path(os.environ.get("MUNSHI_HOME", "/tmp/munshi"))
SAFE = re.compile(r"[^A-Za-z0-9_-]")
MAX_ROWS = 20000
MAX_EVENTS = 200


def _home(context):
    session = getattr(context, "session_id", None) or "local"
    return ROOT / SAFE.sub("_", session)[:64]


def _household(payload):
    body = payload.get("household")
    if not isinstance(body, dict):
        raise ValueError("scan needs a household payload")
    if len(body.get("ledger", ())) > MAX_ROWS or len(body.get("events", ())) > MAX_EVENTS:
        raise ValueError("household payload is too large")
    return Household.from_payload(body)


def handle(payload, context=None):
    action = (payload or {}).get("action")
    home = _home(context)
    if action == "scan":
        service = Service(home, household=_household(payload))
        return {"ok": True, "data": {"scan": service.scan(), "cards": service.cards()}, "error": None}
    if action == "cards":
        return {"ok": True, "data": Service(home).cards(), "error": None}
    if action == "decide":
        card = Service(home).decide(str(payload.get("card", "")), str(payload.get("choice", "")))
        return {"ok": True, "data": card, "error": None}
    raise ValueError("action must be scan, cards or decide")


@app.entrypoint
def invoke(payload, context=None):
    try:
        return handle(payload, context)
    except (KeyError, ValueError, FileNotFoundError) as error:
        return {"ok": False, "data": None, "error": str(error)}


if __name__ == "__main__":
    app.run()
