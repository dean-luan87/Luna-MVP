# -*- coding: utf-8 -*-
"""
TTS unified entry (Stage-2.1).

唯一入口目标：
- 接收 SpeechRequest
- 命中 selector（唯一公开入口）
- provider chain 失败时按配置回滚 legacy
- 记录 cutover / rollback observation

边界：
- 不替代 speech_gate（gate）
- 不替代 audio_worker（async execution）
- 不负责生成文本
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

import os
import subprocess
import yaml

from capabilities.model_paths_v1 import resolve_model_path, resolve_preset_model_params
from capabilities.voice.runtime.tts_latency_policy_v0 import LatencyPolicyV0
from capabilities.voice.runtime.tts_provider_health_v0 import CircuitBreakerConfig, PROVIDER_HEALTH_V0
from capabilities.voice.runtime.tts_runtime_controls_v0 import get_tts_speed, get_tts_speed_control_meta
from capabilities.voice.tts_model_constants_v0 import (
    DEFAULT_TTS_MODEL,
    emit_tts_model_warnings,
    resolve_tts_model,
)
from capabilities.voice.observations.tts_cutover_observation import TTSCutoverObservation
from capabilities.voice.observations.tts_rollback_observation import TTSRollbackObservation
from capabilities.voice.observations.provider_fallback_observation import ProviderFallbackObservation
from capabilities.voice.observations.provider_selection_observation import ProviderSelectionObservation
from capabilities.voice.output.tts_provider_runtime import TTSProviderResult
from capabilities.voice.providers.piper_tts_provider import PiperTTSProvider
from capabilities.voice.providers.qwen_tts_provider import QwenTTSProvider
from capabilities.voice.providers.tts_provider_selector import execute_provider_chain
from capabilities.voice.schemas.speech_request import SpeechRequest


LegacySubmitFn = Callable[[str], bool]


@dataclass(frozen=True)
class TTSUnifiedEntryResult:
    ok: bool
    final_execution_mode: str  # provider_chain | legacy_fallback | failed_no_output
    cutover_observation: TTSCutoverObservation
    rollback_observation: Optional[TTSRollbackObservation] = None
    provider_result: Optional[TTSProviderResult] = None
    selection_observation: Optional[ProviderSelectionObservation] = None
    fallback_observation: Optional[ProviderFallbackObservation] = None
    chain_attempts: Optional[list] = None


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}


def _now() -> float:
    return time.time()


def _resolve_qwen_tts_model(configured: Any) -> str:
    explicit = str(configured or "").strip() or None
    resolved = resolve_tts_model(explicit=explicit)
    emit_tts_model_warnings(resolved)
    return str(resolved.model or DEFAULT_TTS_MODEL)


def _resolved_model_ref(ref: Optional[str]) -> Optional[str]:
    if not ref:
        return None
    resolved = resolve_model_path(str(ref))
    return str(resolved) if resolved is not None else str(ref)


def _speed_to_piper_length_scale(speed: float) -> float:
    """
    Map global TTS speed tier (0.25~1.0) to Piper length_scale.
    Piper semantics: larger length_scale => slower speech.
    Keep mapping conservative to avoid extreme artifacts.
    """
    try:
        s = float(speed)
    except Exception:
        s = 0.75
    # snap+clamp style is handled by runtime controls; be defensive here
    if s < 0.25:
        s = 0.25
    if s > 1.0:
        s = 1.0
    # anchor: speed=0.75 -> length_scale=1.0
    # speed=1.0  -> ~0.85 (slightly faster)
    # speed=0.5  -> ~1.2  (slower)
    # speed=0.25 -> ~1.45 (slowest)
    return float(max(0.7, min(1.6, 1.0 + (0.75 - s) * 0.8)))


def _speed_to_macos_say_rate(speed: float) -> int:
    """
    Map global TTS speed tier (0.25~1.0) to macOS say rate (wpm-ish).
    Default Voice rate in this repo is 180; keep within a safe band.
    """
    try:
        s = float(speed)
    except Exception:
        s = 0.75
    if s < 0.25:
        s = 0.25
    if s > 1.0:
        s = 1.0
    base = 180.0
    # 0.75 -> 180, 1.0 -> ~210, 0.5 -> ~150, 0.25 -> ~120
    rate = base + (s - 0.75) * 120.0
    return int(max(110, min(240, round(rate))))


def _looks_like_wav(b: bytes) -> bool:
    return bool(b) and len(b) >= 12 and b[:4] == b"RIFF" and b[8:12] == b"WAVE"


def _try_play_audio_bytes_via_afplay(*, request_id: str, audio_bytes: bytes) -> bool:
    """
    Online-prefer-qwen runtime: if provider produced WAV bytes, play via macOS afplay.
    This is intentionally non-blocking and does NOT route through audio_worker (text-only legacy base).
    Fail-closed: returns False on any error so caller can fallback to legacy text TTS.
    """
    try:
        if not audio_bytes or len(audio_bytes) < 64:
            return False
        if not _looks_like_wav(audio_bytes):
            return False
        out_dir = Path("logs") / "qwen_tts_runtime_audio_cache"
        out_dir.mkdir(parents=True, exist_ok=True)
        wav_path = out_dir / f"{request_id}.wav"
        wav_path.write_bytes(audio_bytes)
        # Non-blocking playback
        subprocess.Popen(
            ["afplay", str(wav_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=os.environ.copy(),
        )
        return True
    except Exception:
        return False


def _rollback_trigger_from_failure(failure_type: str) -> str:
    if failure_type == "timeout":
        return "timeout_chain"
    if failure_type == "invalid_audio":
        return "invalid_audio_chain"
    return "provider_chain_failure"


def run_tts_unified_entry(
    *,
    request: SpeechRequest,
    legacy_submit: LegacySubmitFn,
    config_path: str = "capabilities/voice/config/voice_tts_config.yaml",
    presets_path: str = "capabilities/voice/config/voice_presets.yaml",
) -> TTSUnifiedEntryResult:
    cfg = _load_yaml(Path(config_path))
    presets = _load_yaml(Path(presets_path))

    cutover_cfg = cfg.get("cutover") if isinstance(cfg.get("cutover"), dict) else {}
    legacy_cfg = cfg.get("legacy_fallback") if isinstance(cfg.get("legacy_fallback"), dict) else {}
    fallback_cfg = cfg.get("fallback") if isinstance(cfg.get("fallback"), dict) else {}

    # runtime mode profile (does NOT delete offline-only baseline)
    runtime_mode = str(cfg.get("tts_runtime_mode") or "offline_only")
    runtime_modes = cfg.get("runtime_modes") if isinstance(cfg.get("runtime_modes"), dict) else {}
    mode_cfg = runtime_modes.get(runtime_mode) if isinstance(runtime_modes.get(runtime_mode), dict) else {}

    # Phase-VoiceTTS-Policy-002: controlled online runtime policy (default disabled)
    online_runtime_cfg = cfg.get("online_runtime") if isinstance(cfg.get("online_runtime"), dict) else {}
    online_runtime_enabled_cfg = bool(online_runtime_cfg.get("enabled", False))
    online_runtime_enabled_env = str(os.environ.get("LUNA_TTS_ONLINE_RUNTIME_ENABLED", "")).lower() in ("1", "true", "yes", "on")
    online_runtime_enabled = bool(online_runtime_enabled_cfg or online_runtime_enabled_env)
    policy_id = str(online_runtime_cfg.get("policy_id") or "")

    cutover_enabled = bool(cutover_cfg.get("enabled", True))
    cutover_mode = str(cutover_cfg.get("mode", "provider_chain_first"))
    legacy_enabled = bool(legacy_cfg.get("enabled", True))
    rollback_on_selector_failure = bool(cutover_cfg.get("rollback_on_selector_failure", True))
    rollback_on_chain_failure = bool(cutover_cfg.get("rollback_on_provider_chain_failure", True))
    rollback_on_any_failure = bool(cutover_cfg.get("rollback_to_legacy_on_failure", True))

    # cutover 关闭：直接 legacy
    if not cutover_enabled:
        legacy_ok = legacy_submit(request.text_candidate)
        cut = TTSCutoverObservation(
            request_id=request.request_id,
            timestamp=_now(),
            cutover_enabled=False,
            cutover_mode=cutover_mode,
            selector_hit=False,
            provider_chain_ok=False,
            final_execution_mode="legacy_fallback" if legacy_ok else "failed_no_output",
            final_executor="legacy_main_chain",
        )
        return TTSUnifiedEntryResult(ok=legacy_ok, final_execution_mode=cut.final_execution_mode, cutover_observation=cut)

    preset_name = (request.metadata.get("preset") if isinstance(request.metadata, dict) else None) or (cfg.get("presets", {}) or {}).get("default", "calm_female_v1")
    preset = presets.get(preset_name) if isinstance(presets, dict) else {}
    if not isinstance(preset, dict):
        preset = {}
    preset = resolve_preset_model_params(preset)
    # Global runtime speed tier (0.25~1.0, step 0.25)
    tts_speed = get_tts_speed()
    speed_meta = get_tts_speed_control_meta()
    # Apply speed to Piper via preset overlay (runtime-only, non-persistent)
    try:
        mp = preset.get("model_params") if isinstance(preset.get("model_params"), dict) else {}
        mp2 = dict(mp)
        mp2.setdefault("length_scale", _speed_to_piper_length_scale(tts_speed))
        preset = {**preset, "model_params": mp2}
    except Exception:
        # fail-closed: do not break TTS entry on tuning overlay
        pass
    piper_length_scale_effective = None
    try:
        piper_length_scale_effective = float((preset.get("model_params") or {}).get("length_scale"))
    except Exception:
        piper_length_scale_effective = None

    # merge cfg with runtime mode overrides (only for runtime)
    provider_order = (mode_cfg.get("provider_order") if isinstance(mode_cfg.get("provider_order"), list) else None) or (cfg.get("provider_order") or ["piper"])
    if not isinstance(provider_order, list):
        provider_order = ["piper"]
    active_provider = str(mode_cfg.get("active_provider") or cfg.get("active_provider") or "piper")
    fallback_provider = str(mode_cfg.get("fallback_provider") or cfg.get("fallback_provider") or "piper")
    base_timeouts = cfg.get("timeouts") if isinstance(cfg.get("timeouts"), dict) else {"piper_ms": 5000, "qwen_ms": 5000}
    mode_timeouts = mode_cfg.get("timeouts") if isinstance(mode_cfg.get("timeouts"), dict) else {}
    timeouts = {**{str(k): v for k, v in base_timeouts.items()}, **{str(k): v for k, v in mode_timeouts.items()}}
    fallback_enabled = bool(fallback_cfg.get("enabled", True))

    local_runtime = cfg.get("local_runtime") if isinstance(cfg.get("local_runtime"), dict) else {}
    piper_rt = local_runtime.get("piper") if isinstance(local_runtime.get("piper"), dict) else {}
    qwen_rt = local_runtime.get("qwen") if isinstance(local_runtime.get("qwen"), dict) else {}

    offline_only = bool(mode_cfg.get("offline_only", cfg.get("offline_only", True)))
    allow_online = bool(mode_cfg.get("allow_online", False))

    # If controlled online runtime is enabled, allow online and set preferred order.
    # This does NOT delete offline-only baseline; it is a runtime overlay.
    if online_runtime_enabled:
        runtime_mode = "online_prefer_qwen"
        offline_only = False
        allow_online = True
        po = online_runtime_cfg.get("provider_order") if isinstance(online_runtime_cfg.get("provider_order"), list) else None
        if po:
            provider_order = [str(x) for x in po if str(x) in ("qwen", "piper")]
        if "qwen" in provider_order:
            active_provider = "qwen"
            fallback_provider = "piper"

    latency_cfg = online_runtime_cfg.get("latency") if (online_runtime_enabled and isinstance(online_runtime_cfg.get("latency"), dict)) else (mode_cfg.get("latency") if isinstance(mode_cfg.get("latency"), dict) else {})
    lp = LatencyPolicyV0(
        soft_latency_warning_ms=int(latency_cfg.get("soft_latency_warning_ms") or 800),
        first_response_budget_ms=int(latency_cfg.get("first_response_budget_ms") or 1200),
        hard_timeout_ms=int(latency_cfg.get("hard_timeout_ms") or int(timeouts.get("qwen_ms") or 2000)),
    )
    soft_latency_warning_ms = lp.soft_latency_warning_ms
    first_response_budget_ms = lp.first_response_budget_ms
    hard_timeout_ms = lp.hard_timeout_ms

    cb_cfg_raw = online_runtime_cfg.get("circuit_breaker") if isinstance(online_runtime_cfg.get("circuit_breaker"), dict) else {}
    cb_cfg = CircuitBreakerConfig(
        failure_count_threshold=int(cb_cfg_raw.get("failure_count_threshold") or 3),
        failure_window_ms=int(cb_cfg_raw.get("failure_window_ms") or 300000),
        open_duration_ms=int(cb_cfg_raw.get("open_duration_ms") or 300000),
        half_open_probe_count=int(cb_cfg_raw.get("half_open_probe_count") or 1),
    )

    # offline-only gate: filter out any provider that requires network.
    def _requires_network(name: str) -> bool:
        if name == "qwen":
            return bool(qwen_rt.get("requires_network", True))
        if name == "piper":
            return False
        return False

    filtered_out = []
    effective_order = []
    for n in [str(x) for x in provider_order]:
        if (offline_only or (not allow_online)) and _requires_network(n):
            filtered_out.append(n)
            continue
        effective_order.append(n)
    provider_order = effective_order or ["piper"]
    if (offline_only or (not allow_online)) and _requires_network(active_provider):
        # Keep system running: force active to first effective provider.
        active_provider = provider_order[0]

    # circuit breaker: if open, skip qwen (only applies in controlled online runtime)
    circuit_state = None
    if online_runtime_enabled and "qwen" in provider_order:
        circuit_state = PROVIDER_HEALTH_V0.qwen.state
        if PROVIDER_HEALTH_V0.should_skip_qwen(cfg=cb_cfg):
            provider_order = [p for p in provider_order if p != "qwen"] or ["piper"]
            filtered_out.append("qwen_circuit_open")
            active_provider = provider_order[0]

    providers = {
        "piper": PiperTTSProvider(
            command=str(piper_rt.get("executable") or "piper"),
            enabled=bool(piper_rt.get("enabled", True)),
            model_path=_resolved_model_ref(piper_rt.get("voice_path")),
        ),
        "qwen": QwenTTSProvider(
            enabled=bool(qwen_rt.get("enabled", False) or online_runtime_enabled),
            api_key_env=str(qwen_rt.get("api_key_env") or "DASHSCOPE_API_KEY"),
            model=_resolve_qwen_tts_model(qwen_rt.get("model")),
            voice=str(qwen_rt.get("voice") or "Serena"),
            sample_rate=int(qwen_rt.get("sample_rate") or 16000),
            audio_format=str(qwen_rt.get("format") or "wav"),
            requires_network=bool(qwen_rt.get("requires_network", True)),
            speed=tts_speed,
        ),
    }

    try:
        chain = execute_provider_chain(
            request_id=request.request_id,
            text=request.text_candidate,
            preset_name=str(preset_name),
            preset=preset,
            provider_order=[str(x) for x in provider_order],
            active_provider=active_provider,
            fallback_provider=fallback_provider,
            providers=providers,
            timeouts_ms={str(k): int(v) for k, v in timeouts.items()},
            fallback_enabled=fallback_enabled,
        )
    except Exception as e:
        # selector/public entry 层失败
        legacy_ok = False
        if legacy_enabled and rollback_on_any_failure and rollback_on_selector_failure:
            legacy_ok = legacy_submit(request.text_candidate)
        cut = TTSCutoverObservation(
            request_id=request.request_id,
            timestamp=_now(),
            cutover_enabled=True,
            cutover_mode=cutover_mode,
            selector_hit=False,
            provider_chain_ok=False,
            final_execution_mode="legacy_fallback" if legacy_ok else "failed_no_output",
            final_executor="legacy_main_chain" if legacy_ok else "none",
            metadata={
                "tts_runtime_mode": runtime_mode,
                "offline_only": offline_only,
                "allow_online": allow_online,
                "provider_order_filtered_out": filtered_out,
                "provider_order_effective": provider_order,
                "effective_order_runtime": (provider_order + ["legacy_macos_say"]),
                "active_provider_effective": active_provider,
                "latency_policy_ms": {
                    "soft_latency_warning_ms": soft_latency_warning_ms,
                    "first_response_budget_ms": first_response_budget_ms,
                    "hard_timeout_ms": hard_timeout_ms,
                },
            },
        )
        rb = TTSRollbackObservation(
            request_id=request.request_id,
            timestamp=_now(),
            rollback_trigger="selector_failure",
            rollback_reason=str(e),
            provider_chain_status="selector_error",
            final_execution_mode=cut.final_execution_mode,
        )
        return TTSUnifiedEntryResult(ok=legacy_ok, final_execution_mode=cut.final_execution_mode, cutover_observation=cut, rollback_observation=rb)

    # provider chain 成功：若 provider 返回 WAV bytes，优先播放音频；否则回退 legacy(text)
    if chain.ok and chain.final_result and chain.final_result.audio_bytes:
        selected = chain.final_result.provider_name
        # circuit breaker book-keeping (probe decrement in half-open)
        if online_runtime_enabled and selected == "qwen":
            PROVIDER_HEALTH_V0.note_qwen_probe_attempt()

        audio_played = _try_play_audio_bytes_via_afplay(
            request_id=request.request_id,
            audio_bytes=chain.final_result.audio_bytes,
        )
        say_rate_effective = None
        if not audio_played:
            # Apply speed tier to legacy macOS say rate (best-effort) before speaking.
            try:
                say_rate_effective = _speed_to_macos_say_rate(tts_speed)
                if hasattr(legacy_submit, "__self__") and hasattr(legacy_submit.__self__, "voice"):
                    v = legacy_submit.__self__.voice
                    if hasattr(v, "set_rate"):
                        v.set_rate(say_rate_effective)
            except Exception:
                pass
        legacy_ok = True if audio_played else legacy_submit(request.text_candidate)
        latency_ms = int(chain.final_result.latency_ms or 0)
        latency_class = lp.classify_total_latency(latency_ms)

        # circuit breaker: treat high-latency fallback and failures as failures
        if online_runtime_enabled and selected == "qwen":
            if latency_class == "hard_timeout_exceeded" or (not audio_played):
                PROVIDER_HEALTH_V0.note_qwen_failure(cfg=cb_cfg, reason=f"qwen_success_but_audio_not_played:{latency_class}")
            else:
                PROVIDER_HEALTH_V0.note_qwen_success()
        cut = TTSCutoverObservation(
            request_id=request.request_id,
            timestamp=_now(),
            cutover_enabled=True,
            cutover_mode=cutover_mode,
            selector_hit=True,
            provider_chain_ok=True,
            final_execution_mode="provider_chain" if legacy_ok else "failed_no_output",
            final_executor=("afplay_audio_bytes" if audio_played else "legacy_main_chain_execution_base") if legacy_ok else "none",
            metadata={
                "selected_provider": chain.final_result.provider_name,
                "provider_latency_ms": latency_ms,
                "provider_latency_class": latency_class,
                "audio_played": audio_played,
                "tts_runtime_mode": runtime_mode,
                "online_runtime_enabled": online_runtime_enabled,
                "policy_id": policy_id,
                "offline_only": offline_only,
                "allow_online": allow_online,
                # Speed control whitebox
                **speed_meta,
                "speed_control_applied": True,
                "provider_speed_param": (
                    {"qwen.speed": float(tts_speed)}
                    if chain.final_result.provider_name == "qwen"
                    else (
                        {"piper.length_scale": piper_length_scale_effective}
                        if chain.final_result.provider_name == "piper"
                        else (
                            {"macos_say.rate": say_rate_effective}
                            if (not audio_played)
                            else None
                        )
                    )
                ),
                "fallback_used": bool(isinstance(getattr(chain, "attempts", None), list) and len(getattr(chain, "attempts", None)) > 1),
                "provider_order_filtered_out": filtered_out,
                "provider_order_effective": provider_order,
                "effective_order_runtime": (provider_order + ["legacy_macos_say"]),
                "active_provider_effective": active_provider,
                "latency_policy_ms": {
                    "soft_latency_warning_ms": soft_latency_warning_ms,
                    "first_response_budget_ms": first_response_budget_ms,
                    "hard_timeout_ms": hard_timeout_ms,
                },
                "circuit_state": (PROVIDER_HEALTH_V0.qwen.state if online_runtime_enabled else None),
            },
        )
        return TTSUnifiedEntryResult(
            ok=legacy_ok,
            final_execution_mode=cut.final_execution_mode,
            cutover_observation=cut,
            provider_result=chain.final_result,
            selection_observation=chain.selection_observation,
            fallback_observation=chain.fallback_observation,
            chain_attempts=getattr(chain, "attempts", None),
        )

    # provider chain 失败：按配置回滚 legacy
    legacy_ok = False
    rollback_observation = None
    failure_type = (
        chain.final_result.failure.failure_type
        if chain.final_result and chain.final_result.failure
        else "unknown"
    )
    # circuit breaker accounting: if qwen was attempted and failed/timeout/invalid_audio => failure
    if online_runtime_enabled:
        attempts = getattr(chain, "attempts", None)
        if isinstance(attempts, list):
            for a in attempts:
                if isinstance(a, dict) and a.get("provider") == "qwen" and not a.get("ok"):
                    PROVIDER_HEALTH_V0.note_qwen_failure(cfg=cb_cfg, reason=str(a.get("failure_reason") or "qwen_failed"))
                    break
    if legacy_enabled and rollback_on_any_failure and rollback_on_chain_failure:
        # Apply speed tier to legacy macOS say rate (best-effort).
        try:
            if hasattr(legacy_submit, "__self__") and hasattr(legacy_submit.__self__, "voice"):
                v = legacy_submit.__self__.voice
                if hasattr(v, "set_rate"):
                    v.set_rate(_speed_to_macos_say_rate(tts_speed))
        except Exception:
            pass
        legacy_ok = legacy_submit(request.text_candidate)
        rollback_observation = TTSRollbackObservation(
            request_id=request.request_id,
            timestamp=_now(),
            rollback_trigger=_rollback_trigger_from_failure(failure_type),
            rollback_reason=(chain.final_result.failure.reason if chain.final_result and chain.final_result.failure else "provider_chain_failed"),
            provider_chain_status="failed",
            final_execution_mode="legacy_fallback" if legacy_ok else "failed_no_output",
        )

    cut = TTSCutoverObservation(
        request_id=request.request_id,
        timestamp=_now(),
        cutover_enabled=True,
        cutover_mode=cutover_mode,
        selector_hit=True,
        provider_chain_ok=False,
        final_execution_mode="legacy_fallback" if legacy_ok else "failed_no_output",
        final_executor="legacy_main_chain" if legacy_ok else "none",
        metadata={
            "failure_type": failure_type,
            "tts_runtime_mode": runtime_mode,
            "online_runtime_enabled": online_runtime_enabled,
            "policy_id": policy_id,
            "offline_only": offline_only,
            "allow_online": allow_online,
            **speed_meta,
            "speed_control_applied": True,
            "provider_speed_param": {"piper.length_scale": piper_length_scale_effective},
            "fallback_used": True,
            "provider_order_filtered_out": filtered_out,
            "provider_order_effective": provider_order,
            "effective_order_runtime": (provider_order + ["legacy_macos_say"]),
            "active_provider_effective": active_provider,
            "latency_policy_ms": {
                "soft_latency_warning_ms": soft_latency_warning_ms,
                "first_response_budget_ms": first_response_budget_ms,
                "hard_timeout_ms": hard_timeout_ms,
            },
            "circuit_state": (PROVIDER_HEALTH_V0.qwen.state if online_runtime_enabled else None),
        },
    )
    return TTSUnifiedEntryResult(
        ok=legacy_ok,
        final_execution_mode=cut.final_execution_mode,
        cutover_observation=cut,
        rollback_observation=rollback_observation,
        provider_result=chain.final_result,
        selection_observation=chain.selection_observation,
        fallback_observation=chain.fallback_observation,
        chain_attempts=getattr(chain, "attempts", None),
    )

