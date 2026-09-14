# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass

from capabilities.voice.output.tts_provider_runtime import TTSFailure, TTSProviderResult
from capabilities.voice.providers.tts_fallback_manager import run_tts_chain


@dataclass
class _StubProvider:
    name: str
    result: TTSProviderResult

    def synthesize(self, *, text: str, preset_name: str, preset: dict, timeout_ms: int) -> TTSProviderResult:
        return self.result


def test_fallback_to_secondary_when_primary_fails() -> None:
    primary_fail = TTSProviderResult(
        ok=False,
        provider_name="qwen",
        preset_name="calm_female_v1",
        failure=TTSFailure(failure_type="exception", reason="boom"),
        latency_ms=10,
    )
    piper_ok = TTSProviderResult(
        ok=True,
        provider_name="piper",
        preset_name="calm_female_v1",
        audio_bytes=b"RIFF....WAVE",
        latency_ms=20,
    )

    chain = run_tts_chain(
        request_id="r1",
        text="hello",
        preset_name="calm_female_v1",
        preset={},
        provider_order=["qwen", "piper"],
        active_provider="qwen",
        fallback_provider="piper",
        providers={
            "qwen": _StubProvider("qwen", primary_fail),
            "piper": _StubProvider("piper", piper_ok),
        },
        timeouts_ms={"qwen_ms": 1, "piper_ms": 1},
        fallback_enabled=True,
    )
    assert chain.ok is True
    assert chain.final_result is not None
    assert chain.final_result.provider_name == "piper"
    assert chain.fallback_observation is not None


def test_no_fallback_when_disabled() -> None:
    primary_fail = TTSProviderResult(
        ok=False,
        provider_name="qwen",
        preset_name="calm_female_v1",
        failure=TTSFailure(failure_type="timeout", reason="timeout"),
        latency_ms=10,
    )
    chain = run_tts_chain(
        request_id="r2",
        text="hello",
        preset_name="calm_female_v1",
        preset={},
        provider_order=["qwen", "piper"],
        active_provider="qwen",
        fallback_provider="piper",
        providers={"qwen": _StubProvider("qwen", primary_fail)},
        timeouts_ms={"qwen_ms": 1, "piper_ms": 1},
        fallback_enabled=False,
    )
    assert chain.ok is False
    assert chain.final_result is not None
    assert chain.final_result.provider_name == "qwen"
