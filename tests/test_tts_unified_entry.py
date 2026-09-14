# -*- coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path

import yaml

from capabilities.voice.observations.provider_selection_observation import ProviderSelectionObservation
from capabilities.voice.output.tts_provider_runtime import TTSFailure, TTSProviderResult
from capabilities.voice.providers.tts_fallback_manager import TTSChainResult
from capabilities.voice.runtime.tts_unified_entry import run_tts_unified_entry
from capabilities.voice.schemas.speech_request import SpeechRequest


def _write_cfg(tmp_path: Path, *, cutover_enabled: bool = True) -> tuple[str, str]:
    cfg = {
        "active_provider": "piper",
        "fallback_provider": "piper",
        "provider_order": ["piper"],
        "fallback": {"enabled": True},
        "timeouts": {"piper_ms": 1000},
        "presets": {"default": "calm_female_v1", "available": ["calm_female_v1"]},
        "backend_override": {"enabled": True, "source": "reserved"},
        "cutover": {
            "enabled": cutover_enabled,
            "mode": "provider_chain_first",
            "rollback_to_legacy_on_failure": True,
            "rollback_on_selector_failure": True,
            "rollback_on_provider_chain_failure": True,
            "observe_rollbacks": True,
        },
        "legacy_fallback": {"enabled": True, "mode": "current_main_chain", "reason_tag": "legacy_voice_runtime"},
    }
    presets = {
        "calm_female_v1": {
            "display_name": "Calm Female v1",
            "description": "test",
            "provider": "piper",
            "speed": 1.0,
            "volume": 1.0,
            "text_style_hints": ["short_sentences"],
            "model_params": {},
            "intended_use": "default",
        }
    }
    c = tmp_path / "voice_tts_config.yaml"
    p = tmp_path / "voice_presets.yaml"
    c.write_text(yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8")
    p.write_text(yaml.safe_dump(presets, allow_unicode=True), encoding="utf-8")
    return str(c), str(p)


def _req() -> SpeechRequest:
    return SpeechRequest(
        request_id="r1",
        source_module="test",
        output_category="interaction_result",
        text_candidate="hello",
        metadata={"preset": "calm_female_v1"},
    )


def test_unified_entry_provider_chain_success(monkeypatch, tmp_path: Path) -> None:
    cfg, presets = _write_cfg(tmp_path, cutover_enabled=True)
    chain = TTSChainResult(
        ok=True,
        final_result=TTSProviderResult(
            ok=True,
            provider_name="piper",
            preset_name="calm_female_v1",
            audio_bytes=b"audio",
            latency_ms=1,
        ),
        selection_observation=ProviderSelectionObservation(
            request_id="r1",
            timestamp=1.0,
            chosen_provider="piper",
            preset_name="calm_female_v1",
            provider_order=["piper"],
            selection_reason="ACTIVE_PROVIDER",
        ),
    )

    monkeypatch.setattr(
        "capabilities.voice.runtime.tts_unified_entry.execute_provider_chain",
        lambda **kwargs: chain,
    )
    called = {"legacy": 0}

    def legacy_submit(_: str) -> bool:
        called["legacy"] += 1
        return True

    out = run_tts_unified_entry(request=_req(), legacy_submit=legacy_submit, config_path=cfg, presets_path=presets)
    assert out.ok is True
    assert out.final_execution_mode == "provider_chain"
    assert called["legacy"] == 1


def test_unified_entry_chain_fail_rollback_legacy(monkeypatch, tmp_path: Path) -> None:
    cfg, presets = _write_cfg(tmp_path, cutover_enabled=True)
    chain = TTSChainResult(
        ok=False,
        final_result=TTSProviderResult(
            ok=False,
            provider_name="piper",
            preset_name="calm_female_v1",
            failure=TTSFailure(failure_type="timeout", reason="timeout"),
            latency_ms=2,
        ),
        selection_observation=ProviderSelectionObservation(
            request_id="r1",
            timestamp=1.0,
            chosen_provider="piper",
            preset_name="calm_female_v1",
            provider_order=["piper"],
            selection_reason="ACTIVE_PROVIDER",
        ),
    )
    monkeypatch.setattr(
        "capabilities.voice.runtime.tts_unified_entry.execute_provider_chain",
        lambda **kwargs: chain,
    )
    out = run_tts_unified_entry(request=_req(), legacy_submit=lambda _: True, config_path=cfg, presets_path=presets)
    assert out.ok is True
    assert out.final_execution_mode == "legacy_fallback"
    assert out.rollback_observation is not None
    assert out.rollback_observation.rollback_trigger == "timeout_chain"


def test_unified_entry_cutover_disabled_goes_legacy(tmp_path: Path) -> None:
    cfg, presets = _write_cfg(tmp_path, cutover_enabled=False)
    out = run_tts_unified_entry(request=_req(), legacy_submit=lambda _: True, config_path=cfg, presets_path=presets)
    assert out.ok is True
    assert out.final_execution_mode == "legacy_fallback"
    assert out.cutover_observation.selector_hit is False
