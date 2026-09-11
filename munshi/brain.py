"""Which model thinks. Bedrock in production; a local Ollama model on a laptop."""

from __future__ import annotations

import os

DEFAULT_BEDROCK = "us.amazon.nova-pro-v1:0"
DEFAULT_OLLAMA = "granite3.2:8b"


def make_model(kind=None):
    kind = (kind or os.environ.get("MUNSHI_MODEL") or "bedrock").lower()
    if kind == "playbook":
        from .playbook import Playbook
        return Playbook()
    if kind == "bedrock":
        from strands.models import BedrockModel
        return BedrockModel(model_id=os.environ.get("MUNSHI_BEDROCK_MODEL", DEFAULT_BEDROCK),
                            region_name=os.environ.get("AWS_REGION", "us-east-1"), temperature=0.2)
    if kind == "ollama":
        from strands.models.ollama import OllamaModel
        return OllamaModel(os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
                           model_id=os.environ.get("MUNSHI_OLLAMA_MODEL", DEFAULT_OLLAMA), temperature=0.2)
    raise ValueError("MUNSHI_MODEL must be 'bedrock', 'ollama' or 'playbook', not {0!r}".format(kind))


def make_investigator(kind=None):
    """The investigator uses the same provider, except the playbook, which leaves verdicts to rules."""
    kind = (kind or os.environ.get("MUNSHI_MODEL") or "bedrock").lower()
    return None if kind == "playbook" else make_model(kind)
