"""The hosted demo's brain: one function, no server-side state.

Every request carries everything it needs. A run's files go back to the
browser packed (see portable.py) and come back with the family's answer, so
two requests can be served by two different machines and the paused Strands
session still resumes from exactly where it stopped.
"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime
from pathlib import Path

from .demo import demo_household
from .paste import messages_from_text
from .portable import dump_home, load_home
from .service import Service
from .witness import Household

MAX_CHOICE = 12


def model_kind():
    """The hosted demo runs the playbook model unless it is given something better."""
    return os.environ.get("MUNSHI_MODEL", "playbook")


def _start(request):
    sms = request.get("sms")
    now = datetime.now().replace(second=0, microsecond=0)
    if sms:
        household = Household.from_messages("you", messages_from_text(sms, now), now=now)
        if not household.events:
            raise ValueError("Munshi read those messages and found nothing worth asking about.")
    else:
        household = demo_household(now=now)
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / "home"
        service = Service(home, household=household, model_kind=model_kind())
        service.scan()
        return {"state": service.state(), "session": dump_home(home)}


def _decide(request):
    choice = str(request.get("choice", ""))
    if not choice.isalpha() or len(choice) > MAX_CHOICE:
        raise ValueError("that is not one of the buttons")
    with tempfile.TemporaryDirectory() as tmp:
        home = load_home(request.get("session"), Path(tmp) / "home")
        service = Service(home, model_kind=model_kind())
        service.decide(str(request.get("card", "")), choice)
        return {"state": service.state(), "session": dump_home(home)}


def handle(request):
    """'start' (optionally with pasted `sms`) or 'decide' (with `session`, `card`, `choice`)."""
    action = (request or {}).get("action")
    if action == "start":
        return _start(request)
    if action == "decide":
        return _decide(request)
    raise ValueError("action must be start or decide")
