# -*- coding: utf-8 -*-
"""方案 B 接入准备：LUNA_VOICE_ENABLE_PREFILTER_ROUTING 与 dispatcher metadata（默认关）。"""

from __future__ import annotations

from capabilities.voice.runtime.voice_final_text_dispatcher import dispatch_voice_final_text
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent


def _long_event(text: str) -> VoiceInputEvent:
    return VoiceInputEvent(
        event_id="e1",
        request_id="r1",
        session_id="s1",
        router_decision="accept",
        raw_text=text,
        normalized_text=text,
        wake_word_stripped=text,
        is_task_mode=False,
        shortcut_id=None,
        wake_word_detected=False,
    )


def test_prefilter_routing_metadata_when_disabled(monkeypatch) -> None:
    monkeypatch.delenv("LUNA_VOICE_ENABLE_PREFILTER_ROUTING", raising=False)
    monkeypatch.delenv("LUNA_QWEN_USE_PRIMARY_BACKUP", raising=False)
    r = dispatch_voice_final_text(_long_event("导航到公司"))
    assert r.dispatch_type == "long_task_planning_input"
    m = r.metadata
    assert m.get("prefilter_routing_enabled") is False
    assert m.get("prefilter_routing_suggestion") == "disabled"
    assert m.get("selected_provider_model_id") == "legacy_default_no_bundle"


def test_prefilter_routing_enabled_turbo_path_metadata(monkeypatch) -> None:
    monkeypatch.setenv("LUNA_VOICE_ENABLE_PREFILTER_ROUTING", "1")
    monkeypatch.delenv("LUNA_QWEN_USE_PRIMARY_BACKUP", raising=False)
    r = dispatch_voice_final_text(_long_event("导航到公司"))
    m = r.metadata
    assert m.get("prefilter_routing_enabled") is True
    assert m.get("prefilter_routing_suggestion") == "route_to_turbo"
    assert m.get("prefilter_simple_or_complex") == "simple"
    assert m.get("selected_provider_model_id") in (
        "qwen-turbo",
        "rule_chain_only_unconfigured_qwen_external",
    )


def test_prefilter_routing_rule_or_reject_forces_rule_chain(monkeypatch) -> None:
    monkeypatch.setenv("LUNA_VOICE_ENABLE_PREFILTER_ROUTING", "1")
    r = dispatch_voice_final_text(_long_event("帮我自动挂号"))
    m = r.metadata
    assert m.get("prefilter_routing_suggestion") == "route_to_rule_or_reject"
    assert m.get("selected_provider_model_id") == "rule_chain_only"


def test_prefilter_routing_ignores_primary_backup_bundle(monkeypatch) -> None:
    """开启 prefilter 时不再走主备 bundle，即使 LUNA_QWEN_USE_PRIMARY_BACKUP=1。"""
    monkeypatch.setenv("LUNA_VOICE_ENABLE_PREFILTER_ROUTING", "1")
    monkeypatch.setenv("LUNA_QWEN_USE_PRIMARY_BACKUP", "1")
    monkeypatch.setenv("LUNA_EXTERNAL_LLM_PROVIDER", "")
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.delenv("LUNA_DASHSCOPE_API_KEY", raising=False)
    r = dispatch_voice_final_text(_long_event("导航到公司"))
    m = r.metadata
    assert m.get("prefilter_routing_suggestion") == "route_to_turbo"
    assert m.get("selected_provider_model_id") == "rule_chain_only_unconfigured_qwen_external"
