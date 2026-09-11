"""The policy is code, not a prompt.

Munshi can only name things: an event id, a payee, a number of days. No tool
takes free text, so no argument can carry an instruction to move money, and
no tool exists that could. The hook refuses anything outside that shape
before it runs, and the audit hook writes every call, refused or not, to a
file a person can read.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from strands.hooks import AfterToolCallEvent, BeforeToolCallEvent, HookProvider

MAX_DAYS = 90
MAX_ARG = 80

ALLOWED = {
    "payee_history": {"party": str},
    "recent_transactions": {"days": int, "party": str},
    "investigate_payment": {"event_id": str},
    "draft_cybercrime_report": {"event_id": str},
    "draft_bank_dispute": {"event_id": str},
    "draft_upi_help_complaint": {"event_id": str},
    "ask_household": {"event_id": str},
    "remember_trusted_payee": {"party": str},
}
# The investigator sub-agent may only answer, through its structured output tool.
INVESTIGATOR = {"Verdict": None}

REFUSAL = "Munshi never moves money and only calls its own tools. Refused: {0}."


def refusal(name, args, allowed=None):
    """Why this call is refused, or None if it may run."""
    allowed = ALLOWED if allowed is None else allowed
    if name not in allowed:
        return "'{0}' is not one of Munshi's tools".format(name)
    spec = allowed[name]
    if spec is None:
        return None
    if not isinstance(args, dict):
        return "arguments must be named"
    extra = sorted(set(args) - set(spec))
    if extra:
        return "'{0}' does not take {1}".format(name, ", ".join(extra))
    for key, kind in spec.items():
        if key in args and (not isinstance(args[key], kind) or isinstance(args[key], bool)):
            return "'{0}' must be a {1}".format(key, kind.__name__)
    if "days" in args and not 1 <= args["days"] <= MAX_DAYS:
        return "'days' must be between 1 and {0}".format(MAX_DAYS)
    if any(isinstance(v, str) and len(v) > MAX_ARG for v in args.values()):
        return "an argument is too long to be an id or a name"
    return None


class PolicyHook(HookProvider):
    def __init__(self, allowed=None):
        self.allowed = dict(ALLOWED if allowed is None else allowed)

    def register_hooks(self, registry, **kwargs):
        registry.add_callback(BeforeToolCallEvent, self.check)

    def check(self, event):
        use = event.tool_use or {}
        reason = refusal(use.get("name", ""), use.get("input") or {}, self.allowed)
        if reason:
            event.cancel_tool = REFUSAL.format(reason)


def _text(result):
    if not isinstance(result, dict):
        return str(result or "")
    parts = []
    for block in result.get("content") or ():
        if isinstance(block, dict):
            parts.append(block.get("text") or json.dumps(block.get("json", ""), default=str))
    return " ".join(p for p in parts if p)


class AuditHook(HookProvider):
    """One line per tool call, append-only."""

    def __init__(self, path, agent_name="munshi"):
        self.path = Path(path)
        self.agent_name = agent_name

    def register_hooks(self, registry, **kwargs):
        registry.add_callback(AfterToolCallEvent, self.record)

    def record(self, event):
        use = event.tool_use or {}
        result = event.result if isinstance(event.result, dict) else {}
        self.write(use.get("name"), use.get("input"), result.get("status"), _text(result),
                   refused=event.cancel_message, ms=round((event.duration or 0) * 1000, 1))

    def write(self, tool, args, status, result, refused=None, ms=0.0):
        """Also used for the one moment Strands has no after-call event for: a tool that interrupted."""
        row = {"at": datetime.now().isoformat(timespec="seconds"), "agent": self.agent_name,
               "tool": tool, "input": args, "status": status, "refused": refused,
               "result": (result or "")[:400], "ms": ms}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, default=str) + "\n")
