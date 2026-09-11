"""Which model thinks. Bedrock in production; a local Ollama model on a laptop."""

from __future__ import annotations

import os

DEFAULT_BEDROCK = "us.amazon.nova-pro-v1:0"
DEFAULT_OLLAMA = "qwen2.5:3b"  # calls tools natively through Ollama; granite3.2:8b writes them as text


def bedrock_settings():
    """Model, region, and an Amazon Bedrock Guardrail if MUNSHI_GUARDRAIL_ID is set. The guardrail
    screens what the model reads and writes; the policy hook still decides what it may call."""
    settings = {"model_id": os.environ.get("MUNSHI_BEDROCK_MODEL", DEFAULT_BEDROCK),
                "region_name": os.environ.get("AWS_REGION", "us-east-1"), "temperature": 0.2}
    guardrail = os.environ.get("MUNSHI_GUARDRAIL_ID")
    if guardrail:
        settings.update(guardrail_id=guardrail, guardrail_version=os.environ.get("MUNSHI_GUARDRAIL_VERSION", "DRAFT"),
                        guardrail_trace="enabled")
    return settings


def make_model(kind=None):
    kind = (kind or os.environ.get("MUNSHI_MODEL") or "bedrock").lower()
    if kind == "playbook":
        from .playbook import Playbook
        return Playbook()
    if kind == "bedrock":
        from strands.models import BedrockModel
        return BedrockModel(**bedrock_settings())
    if kind == "ollama":
        from strands.models.ollama import OllamaModel
        return OllamaModel(os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
                           model_id=os.environ.get("MUNSHI_OLLAMA_MODEL", DEFAULT_OLLAMA), temperature=0.2)
    raise ValueError("MUNSHI_MODEL must be 'bedrock', 'ollama' or 'playbook', not {0!r}".format(kind))


def make_investigator(kind=None):
    """The investigator uses the same provider, except the playbook, which leaves verdicts to rules."""
    kind = (kind or os.environ.get("MUNSHI_MODEL") or "bedrock").lower()
    return None if kind == "playbook" else make_model(kind)
