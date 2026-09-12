"""Turns events into decision cards, and decisions back into agent runs.

Each event gets its own Strands session. When the agent calls ask_household,
Strands raises an interrupt and the run stops; the session manager writes
the conversation and the interrupt to disk; the card goes to the inbox with
the interrupt id. When the family taps a choice, possibly hours later and in
another process, the same session is reopened and the agent resumes from the
exact tool call that asked.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from strands.session.file_session_manager import FileSessionManager

from . import hindi
from .agent import DECISION, build_agent, card_reason, next_steps
from .complaints import drafts_for
from .filelock import locked
from .inbox import CARD_ID, Card, Inbox, card_id
from .policy import AuditHook, PolicyHook
from .prefs import Prefs
from .verdict import rule_verdict

PROMPT = "New event {0}: {1}, {2} to {3} at {4}. Handle it now."
TRUST_ON_FINE = ("scam_shaped_payment", "unusual_payment")


def pending_decisions(agent):
    """Decisions a saved session is still waiting on. The session manager restores them onto the
    agent's interrupt state, which Strands does not expose publicly yet."""
    state = getattr(agent, "_interrupt_state", None)
    if state is None or not state.activated:
        return []
    return [i for i in state.interrupts.values() if i.name == DECISION and i.response is None]


def card_from(reason, interrupt_id="", session_id=""):
    return Card(id=card_id(reason["event_id"]), event_id=reason["event_id"], kind=reason["kind"],
                headline=reason["headline"], evidence=tuple(reason["evidence"]),
                options=tuple(tuple(o) for o in reason["options"]), party=reason["party"],
                amount=reason["amount"], when=reason["when"], drafts=dict(reason.get("drafts", {})),
                hi=dict(reason.get("hi", {})),
                interrupt_id=interrupt_id, session_id=session_id, decided_by=reason.get("decided_by", "rules"))


class Runner:
    def __init__(self, home, household, model=None, investigator_model=None):
        self.home = Path(home)
        self.home.mkdir(parents=True, exist_ok=True)
        self.household = household
        if model is None:
            from .brain import make_model
            model = make_model()
        self.model = model
        self.investigator_model = investigator_model
        self.inbox = Inbox(self.home / "inbox.json")
        self.prefs = Prefs(self.home / "prefs.json")
        self.audit = AuditHook(self.home / "audit.jsonl")
        (self.home / "household.json").write_text(json.dumps(household.to_payload()), encoding="utf-8")

    def _session(self, session_id):
        bucket = os.environ.get("MUNSHI_S3_BUCKET")
        if bucket:
            from strands.session import S3SessionManager
            return S3SessionManager(session_id=session_id, bucket=bucket, prefix="munshi/sessions/")
        return FileSessionManager(session_id=session_id, storage_dir=str(self.home / "sessions"))

    def _agent(self, session_id):
        session = self._session(session_id)
        hooks = [PolicyHook(), self.audit]
        return build_agent(self.household, self.prefs, self.model, hooks=hooks, session_manager=session,
                           investigator_model=self.investigator_model)

    def session_id(self, event):
        return "{0}-{1}".format(self.household.name, event.id)

    def handle(self, event):
        """Run the agent on one event. Every event reaches the family exactly once, even across a crash."""
        with locked(self.home / "locks" / event.id):
            if self.inbox.has_event(event.id):
                return "already asked"
            sid = self.session_id(event)
            agent = self._agent(sid)
            waiting = pending_decisions(agent)
            if waiting:  # the agent asked, then the process died before the card was saved
                self._file_cards(waiting, sid)
                return "asked (recovered from the saved session)"
            result = agent(PROMPT.format(event.id, event.kind, event.amount, event.party,
                                         event.when.strftime("%d %b %H:%M")))
            if result.stop_reason == "interrupt" and result.interrupts:
                self._file_cards(result.interrupts, sid)
                return "asked"
            if not self.inbox.has_event(event.id):
                return self._safety_net(event, sid)
            return "done"

    def _file_cards(self, interrupts, sid):
        for itr in interrupts:
            card = self.inbox.put(card_from(itr.reason, interrupt_id=itr.id, session_id=sid))
            self.audit.write("ask_household", {"event_id": card.event_id}, "waiting for the household",
                             card.headline)

    def _safety_net(self, event, sid):
        """The model finished without asking. The witness raised this event for a reason, so the
        family sees it anyway, with the rules' verdict and the paperwork that verdict calls for."""
        verdict = rule_verdict(event)
        reason = card_reason(event, self.household.ledger, verdict, drafts_for(event, verdict.recommended),
                             "rules (safety net)")
        card = self.inbox.put(card_from(reason, session_id=sid))
        self.audit.write("safety_net", {"event_id": event.id}, "waiting for the household", card.headline)
        return "asked by the safety net"

    def decide(self, cid, choice):
        if not CARD_ID.match(cid or ""):
            raise KeyError("no card {0!r}".format(cid))
        with locked(self.home / "locks" / cid):
            card = self.inbox.get(cid)
            if card.status != "pending":
                raise ValueError("card {0} was already decided: {1}".format(cid, card.decision))
            if choice not in [o[0] for o in card.options]:
                raise ValueError("{0!r} is not an option on this card: {1}".format(
                    choice, ", ".join(o[0] for o in card.options)))
            event = self.household.event(card.event_id)
            said = self._resume(card, choice) if card.interrupt_id else ""
            if choice == "fine" and card.kind in TRUST_ON_FINE:
                self.prefs.trust(card.party)  # the family's word, not the model's
            self.prefs.handle(card.event_id)
            steps = next_steps(event, choice)
            repeats = not said or any(step in said for step in steps)
            outcome = "\n".join(steps + ([] if repeats else [said]))
            return self.inbox.decide(cid, choice, outcome, "\n".join(hindi.steps(event, choice)))

    def _resume(self, card, choice):
        agent = self._agent(card.session_id)
        if card.interrupt_id not in {i.id for i in pending_decisions(agent)}:
            return ""  # resumed before a crash; close the card without running the model twice
        result = agent([{"interruptResponse": {"interruptId": card.interrupt_id, "response": choice}}])
        return str(result).strip()
