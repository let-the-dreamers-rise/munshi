"""A model with no weights: it follows Munshi's system prompt step by step.

It exists so anyone can run the real agent (the Strands event loop, the
policy and audit hooks, the interrupt, the session on disk) without an AWS
account or a GPU. It reads the conversation so far and picks the next step
the way the prompt says to. It never writes the headline or any number:
those come from the investigator, which falls back to rules here. With
Bedrock or Ollama the same loop runs with a real model choosing the steps.
"""

from __future__ import annotations

import json
import re
import uuid

from strands.models.model import Model

DRAFTS = {
    "report_now": ("draft_cybercrime_report", "draft_bank_dispute", "draft_upi_help_complaint"),
    "dispute": ("draft_bank_dispute", "draft_upi_help_complaint"),
}
TRUST_AFTER_FINE = ("likely_scam", "unusual_payment")
_EVENT = re.compile(r"New event ([0-9a-f]{6,}):")


def _blocks(messages, key):
    for m in messages:
        for block in m.get("content") or ():
            if key in block:
                yield m["role"], block[key]


def _read(result):
    for part in result.get("content") or ():
        if "json" in part:
            return part["json"]
        try:
            return json.loads(part.get("text", ""))
        except ValueError:
            continue
    return {}


def next_step(messages):
    """('tool', name, input) or ('text', words), from the conversation so far."""
    prompt = next((b for role, b in _blocks(messages, "text") if role == "user"), "")
    found = _EVENT.search(prompt)
    if not found:
        return ("text", "There is no event to handle.")
    event_id = found.group(1)
    names = {u["toolUseId"]: u["name"] for _, u in _blocks(messages, "toolUse")}
    results = {names.get(r["toolUseId"]): _read(r) for _, r in _blocks(messages, "toolResult")
               if r.get("status") == "success"}
    if "investigate_payment" not in results:
        return ("tool", "investigate_payment", {"event_id": event_id})
    verdict = results["investigate_payment"].get("verdict", {})
    for name in DRAFTS.get(verdict.get("recommended"), ()):
        if name not in results:
            return ("tool", name, {"event_id": event_id})
    if "ask_household" not in results:
        return ("tool", "ask_household", {"event_id": event_id})
    answer = results["ask_household"]
    trust = answer.get("decision") == "fine" and verdict.get("kind") in TRUST_AFTER_FINE
    if trust and "remember_trusted_payee" not in results:
        return ("tool", "remember_trusted_payee", {"party": answer.get("party", "")})
    steps = answer.get("next_steps") or ["Done."]
    return ("text", steps[0])


class Playbook(Model):
    def update_config(self, **model_config):
        return None

    def get_config(self):
        return {"model_id": "munshi-playbook"}

    async def structured_output(self, output_model, prompt, system_prompt=None, **kwargs):
        raise NotImplementedError("the playbook does not write verdicts; the rules do")
        yield  # pragma: no cover

    async def stream(self, messages, tool_specs=None, system_prompt=None, **kwargs):
        kind, *rest = next_step(messages)
        yield {"messageStart": {"role": "assistant"}}
        if kind == "tool":
            name, args = rest
            use = {"toolUseId": "playbook-" + uuid.uuid4().hex[:12], "name": name}
            yield {"contentBlockStart": {"start": {"toolUse": use}}}
            yield {"contentBlockDelta": {"delta": {"toolUse": {"input": json.dumps(args)}}}}
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "tool_use"}}
        else:
            yield {"contentBlockStart": {"start": {}}}
            yield {"contentBlockDelta": {"delta": {"text": rest[0]}}}
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "end_turn"}}
