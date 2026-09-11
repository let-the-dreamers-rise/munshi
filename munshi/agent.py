"""The orchestrator: one Strands agent per event, with tools that can only read and draft."""

from __future__ import annotations

from strands import Agent, tool
from strands.types.tools import ToolContext

from .complaints import bank_dispute, cybercrime_report, upi_help_complaint
from .inbox import OPTIONS
from .verdict import facts_for, investigate, rule_verdict

SYSTEM = """You are Munshi, a household's bookkeeper in India. You run in the
background and receive one event at a time from the witness on the family's
phone. Handle it completely, then stop.

1. Call investigate_payment with the event id.
2. If the verdict recommends report_now, call draft_cybercrime_report,
   draft_bank_dispute and draft_upi_help_complaint. If it recommends dispute,
   call draft_bank_dispute and draft_upi_help_complaint.
3. Call ask_household with the event id, exactly once. It shows the family one
   card and returns their decision.
4. If the decision is 'fine', call remember_trusted_payee with the payee.
5. Reply with one short sentence saying what happens next.

You cannot move money: no tool can. You speak to the family only through
ask_household."""

NEXT = {
    "report": ["Call 1930 now, inside the first hour, and read them the report fields.",
               "File the same details at cybercrime.gov.in and keep the acknowledgement number.",
               "Call your bank's helpline and ask them to block the recipient and raise a dispute."],
    "dispute": ["Send the dispute letter to your bank, or read it to the helpline."],
    "fine": ["Noted. Munshi will not ask about this payee again."],
    "keep": ["Kept. Munshi will not remind you about this renewal."],
    "cancel": ["Cancel it in the app or on the website before the due date. Munshi cannot cancel for you."],
}


def next_steps(event, choice):
    steps = list(NEXT.get(choice, []))
    if choice == "report" and event.helpline:
        steps[-1] = "Call {0} on {1} and ask them to block the recipient and raise a dispute.".format(
            event.bank, event.helpline)
    return steps


def card_reason(event, ledger, verdict, drafts, decided_by):
    """Everything the household sees, as plain data, so it survives a restart."""
    return {"event_id": event.id, "kind": event.kind, "headline": verdict.headline,
            "evidence": facts_for(event, ledger), "options": [list(o) for o in OPTIONS[event.kind]],
            "party": event.party, "amount": event.amount, "when": event.when.strftime("%Y-%m-%d %H:%M"),
            "drafts": dict(drafts), "decided_by": decided_by, "recommended": verdict.recommended}


def build_tools(household, prefs, investigator_model=None):
    notes = {}  # per-run scratch: verdicts and drafts, keyed by event id

    def _note(event_id, key, value):
        notes.setdefault(event_id, {})[key] = value
        return value

    @tool
    def payee_history(party: str) -> dict:
        """Everything the ledger knows about paying one payee: how many times, first and last
        payment, total, the last five amounts. Use it to tell a regular from a stranger."""
        return household.ledger.payee_history(party)

    @tool
    def recent_transactions(days: int = 7, party: str = "") -> list:
        """Money in and out over the last `days` days, optionally for one payee only."""
        return household.ledger.recent(days, party, now=household.now)

    @tool
    def investigate_payment(event_id: str) -> dict:
        """Investigate one event. Returns a verdict (kind, confidence, headline, recommended action)
        and the facts it rests on. Always call this first."""
        event = household.event(event_id)
        verdict, facts, who = investigate(event, household.ledger, investigator_model)
        _note(event_id, "verdict", (verdict, who))
        return {"verdict": verdict.model_dump(), "facts": facts, "decided_by": who}

    def _draft(event_id, name, make):
        drafts = notes.setdefault(event_id, {}).setdefault("drafts", {})
        drafts[name] = make(household.event(event_id))
        return drafts[name]

    @tool
    def draft_cybercrime_report(event_id: str) -> dict:
        """Fill in the 1930 and cybercrime.gov.in report for a suspected scam, with the golden-hour deadline."""
        return _draft(event_id, "cybercrime_report", cybercrime_report)

    @tool
    def draft_bank_dispute(event_id: str) -> dict:
        """Write the dispute letter for the bank, with the reference and the bank's own helpline."""
        return _draft(event_id, "bank_dispute", bank_dispute)

    @tool
    def draft_upi_help_complaint(event_id: str) -> dict:
        """Fill in the UPI Help complaint fields. Says so if the payment was not UPI."""
        return _draft(event_id, "upi_help", upi_help_complaint)

    @tool(context=True)
    def ask_household(event_id: str, tool_context: ToolContext) -> dict:
        """Show the family one decision card for this event and wait for their answer. Call it once,
        after investigating and drafting. Returns their decision and the next steps."""
        event = household.event(event_id)
        verdict, who = notes.get(event_id, {}).get("verdict") or (rule_verdict(event), "rules")
        reason = card_reason(event, household.ledger, verdict, notes.get(event_id, {}).get("drafts", {}), who)
        choice = tool_context.interrupt("munshi-decision", reason=reason)
        return {"event_id": event_id, "party": event.party, "decision": choice,
                "next_steps": next_steps(event, choice)}

    @tool
    def remember_trusted_payee(party: str) -> dict:
        """Remember that the family trusts this payee, so Munshi never asks about them again."""
        prefs.trust(party)
        return {"trusted": party}

    return [payee_history, recent_transactions, investigate_payment, draft_cybercrime_report,
            draft_bank_dispute, draft_upi_help_complaint, ask_household, remember_trusted_payee]


def build_agent(household, prefs, model, hooks=(), session_manager=None, investigator_model=None):
    return Agent(model=model, system_prompt=SYSTEM, tools=build_tools(household, prefs, investigator_model),
                 hooks=list(hooks), session_manager=session_manager, callback_handler=None, name="munshi")
