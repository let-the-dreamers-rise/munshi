"""Which model thinks, chosen by environment, with Guardrails when asked for."""

import pytest

from munshi import brain
from munshi.playbook import Playbook


def test_the_playbook_needs_nothing_and_leaves_verdicts_to_rules():
    assert isinstance(brain.make_model("playbook"), Playbook)
    assert brain.make_investigator("playbook") is None


def test_an_unknown_model_is_refused():
    with pytest.raises(ValueError, match="MUNSHI_MODEL"):
        brain.make_model("gpt")


def test_bedrock_settings_carry_the_guardrail(monkeypatch):
    monkeypatch.setenv("MUNSHI_GUARDRAIL_ID", "gr-123")
    monkeypatch.setenv("MUNSHI_GUARDRAIL_VERSION", "2")
    monkeypatch.setenv("MUNSHI_BEDROCK_MODEL", "us.anthropic.claude-sonnet-5")
    settings = brain.bedrock_settings()
    assert settings["model_id"] == "us.anthropic.claude-sonnet-5"
    assert settings["guardrail_id"] == "gr-123" and settings["guardrail_version"] == "2"


def test_bedrock_settings_without_a_guardrail_have_none(monkeypatch):
    monkeypatch.delenv("MUNSHI_GUARDRAIL_ID", raising=False)
    settings = brain.bedrock_settings()
    assert "guardrail_id" not in settings and settings["model_id"] == brain.DEFAULT_BEDROCK
