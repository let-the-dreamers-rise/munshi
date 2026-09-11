"""A model that plays a script, so the whole agent loop runs offline in tests.

Each turn is ("tool", name, input) or ("text", words). It speaks the same
stream events every Strands provider emits, so the event loop, hooks,
interrupts and session persistence are the real ones.
"""

import json

from strands.models.model import Model


class Scripted(Model):
    def __init__(self, turns):
        self.turns = list(turns)
        self.seen = []

    def update_config(self, **model_config):
        return None

    def get_config(self):
        return {}

    async def structured_output(self, output_model, prompt, system_prompt=None, **kwargs):
        raise NotImplementedError("structured output goes through the tool path")
        yield  # pragma: no cover

    async def stream(self, messages, tool_specs=None, system_prompt=None, **kwargs):
        self.seen.append([t["name"] for t in (tool_specs or [])])
        if not self.turns:
            raise AssertionError("the script ran out")
        kind, *rest = self.turns.pop(0)
        yield {"messageStart": {"role": "assistant"}}
        if kind == "tool":
            name, args = rest
            yield {"contentBlockStart": {"start": {"toolUse": {"toolUseId": "use-{0}-{1}".format(name, len(self.seen)),
                                                              "name": name}}}}
            yield {"contentBlockDelta": {"delta": {"toolUse": {"input": json.dumps(args)}}}}
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "tool_use"}}
        else:
            yield {"contentBlockStart": {"start": {}}}
            yield {"contentBlockDelta": {"delta": {"text": rest[0]}}}
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "end_turn"}}
