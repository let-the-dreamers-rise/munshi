"""The hosted demo's brain: one function, no server-side state.

Every request carries everything it needs. A run's files go back to the
browser packed (see portable.py) and come back with the family's answer, so
two requests can be served by two different machines and the paused Strands
session still resumes from exactly where it stopped.
"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .demo import demo_household
from .paste import messages_from_text
from .portable import dump_home, load_home
from .service import Service
from .witness import Household

MAX_CHOICE = 12
MAX_OFFSET = 840  # minutes; beyond any real timezone


def model_kind():
    """The hosted demo runs the playbook model unless it is given something better."""
    return os.environ.get("MUNSHI_MODEL", "playbook")


def _now(request):
    """The reader's wall clock. The browser sends its offset, because a server in UTC dating a
    card three hours in the past would break the one thing the card is about: the first hour."""
    offset = request.get("offset_minutes")
    if not isinstance(offset, (int, float)) or isinstance(offset, bool) or abs(offset) > MAX_OFFSET:
        return datetime.now().replace(second=0, microsecond=0)
    return (datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=offset)).replace(second=0, microsecond=0)


def _in_readers_clock(state, request):
    """The audit log is stamped by the server's clock; show it in the same clock as the cards."""
    shift = _now(request) - datetime.now().replace(second=0, microsecond=0)
    if abs(shift) < timedelta(minutes=1):
        return state
    rows = []
    for row in state.get("audit", ()):
        try:
            at = (datetime.fromisoformat(row["at"]) + shift).isoformat(timespec="seconds")
        except (KeyError, TypeError, ValueError):
            at = row.get("at")
        rows.append({**row, "at": at})
    return {**state, "audit": rows}


def _model_for(request):
    """The demo page can ask for the tempted playbook: the same loop with a model that reaches for a
    tool to move money, so a visitor can watch the policy hook refuse it. Never a default."""
    return "tempted" if request.get("tempt") else model_kind()


def _start(request):
    sms = request.get("sms")
    now = _now(request)
    if sms:
        # No events is a good answer, not an error: the page says so quietly and shows what was read.
        household = Household.from_messages("you", messages_from_text(sms, now), now=now)
    else:
        household = demo_household(now=now)
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / "home"
        service = Service(home, household=household, model_kind=_model_for(request))
        service.scan()
        return {"state": _in_readers_clock(service.state(), request), "session": dump_home(home)}


def _decide(request):
    choice = str(request.get("choice", ""))
    if not choice.isalpha() or len(choice) > MAX_CHOICE:
        raise ValueError("that is not one of the buttons")
    with tempfile.TemporaryDirectory() as tmp:
        home = load_home(request.get("session"), Path(tmp) / "home")
        service = Service(home, model_kind=model_kind())
        service.decide(str(request.get("card", "")), choice)
        return {"state": _in_readers_clock(service.state(), request), "session": dump_home(home)}


def handle(request):
    """'start' (optionally with pasted `sms`), 'decide' (`session`, `card`, `choice`), or 'ping'."""
    action = (request or {}).get("action")
    if action == "ping":
        return {"ready": True}  # the page wakes the function while someone is still reading
    if action == "start":
        return _start(request)
    if action == "decide":
        return _decide(request)
    raise ValueError("action must be start or decide")
