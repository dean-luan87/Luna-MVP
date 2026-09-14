# -*- coding: utf-8 -*-
"""
TTS fallback manager (Stage-2, internal).

原则：
- 优先 Fish；失败后切 Piper
- fallback 必须结构化、可观察、可留痕
- 不允许静默 fallback

注意：
- 本模块是 selector 的内部机制，不应作为外部公开主调用入口。
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import concurrent.futures

from capabilities.voice.observations.provider_fallback_observation import ProviderFallbackObservation
from capabilities.voice.observations.provider_selection_observation import ProviderSelectionObservation
from capabilities.voice.output.tts_provider_runtime import TTSFailure, TTSProviderResult
from capabilities.voice.providers.provider_types import LocalTTSProvider


@dataclass(frozen=True)
class TTSChainResult:
    ok: bool
    final_result: Optional[TTSProviderResult]
    selection_observation: ProviderSelectionObservation
    fallback_observation: Optional[ProviderFallbackObservation] = None
    # attempts: ordered list of provider attempts for audit/debug (experimental-safe)
    attempts: Optional[List[Dict[str, Any]]] = None


def _now_ts() -> float:
    return time.time()


def _run_tts_chain_internal(
    *,
    request_id: str,
    text: str,
    preset_name: str,
    preset: Dict,
    provider_order: List[str],
    active_provider: str,
    fallback_provider: str,
    providers: Dict[str, LocalTTSProvider],
    timeouts_ms: Dict[str, int],
    fallback_enabled: bool = True,
) -> TTSChainResult:
    chosen = active_provider if active_provider in provider_order else (provider_order[0] if provider_order else "")
    sel_obs = ProviderSelectionObservation(
        request_id=request_id,
        timestamp=_now_ts(),
        chosen_provider=chosen,
        preset_name=preset_name,
        provider_order=provider_order,
        selection_reason="ACTIVE_PROVIDER",
    )

    def _timeout_for(name: str) -> int:
        return int(timeouts_ms.get(f"{name}_ms") or timeouts_ms.get(name) or 4000)

    tried: List[str] = []
    attempts: List[Dict[str, Any]] = []
    last_fail: Optional[TTSProviderResult] = None
    if not provider_order or not chosen:
        return TTSChainResult(ok=False, final_result=None, selection_observation=sel_obs, attempts=attempts)

    start_idx = 0
    if chosen in provider_order:
        start_idx = provider_order.index(chosen)

    chain = provider_order[start_idx:]
    if fallback_enabled and start_idx > 0:
        # 如果 chosen 不在 0 号位，仍然只从 chosen 开始（系统主权），不回头尝试更早 provider
        pass

    for name in chain:
        if not name:
            continue
        if name not in providers:
            continue

        tried.append(name)
        timeout_ms = _timeout_for(name)
        # Enforce hard timeout for network/unknown providers (qwen) even if SDK doesn't support it.
        if name == "qwen":
            start_call = _now_ts()
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
                    fut = ex.submit(providers[name].synthesize, text=text, preset_name=preset_name, preset=preset, timeout_ms=timeout_ms)
                    r = fut.result(timeout=max(0.001, timeout_ms / 1000.0))
            except concurrent.futures.TimeoutError:
                elapsed_ms = int((time.time() - start_call) * 1000)
                # Construct without importing TTSFailure here (keep module deps minimal)
                r = TTSProviderResult(
                    ok=False,
                    provider_name="qwen",
                    preset_name=preset_name,
                    audio_bytes=None,
                    latency_ms=elapsed_ms,
                    failure=TTSFailure(
                        failure_type="timeout",
                        reason="QWEN_HARD_TIMEOUT",
                        detail={"timeout_ms": timeout_ms, "elapsed_ms": elapsed_ms},
                    ),
                )
            except Exception:
                r = providers[name].synthesize(text=text, preset_name=preset_name, preset=preset, timeout_ms=timeout_ms)
        else:
            r = providers[name].synthesize(text=text, preset_name=preset_name, preset=preset, timeout_ms=timeout_ms)
        attempts.append(
            {
                "provider": name,
                "ok": bool(r.ok),
                "latency_ms": int(r.latency_ms or 0),
                "has_audio_bytes": bool(r.audio_bytes),
                "audio_bytes_size": int(len(r.audio_bytes)) if r.audio_bytes else 0,
                "failure_type": (r.failure.failure_type if r.failure else None),
                "failure_reason": (r.failure.reason if r.failure else None),
                "failure_detail": (dict(r.failure.detail or {}) if (r.failure and isinstance(r.failure.detail, dict)) else {}),
            }
        )
        if r.ok and r.audio_bytes:
            if len(tried) == 1:
                return TTSChainResult(ok=True, final_result=r, selection_observation=sel_obs, attempts=attempts)
            fb_obs = ProviderFallbackObservation(
                request_id=request_id,
                timestamp=_now_ts(),
                primary_provider=tried[0],
                fallback_provider=name,
                fallback_reason="PRIMARY_FAILED_FALLBACK_USED",
                failure_type=(last_fail.failure.failure_type if last_fail and last_fail.failure else "unknown"),
                final_provider_used=name,
                latency_ms=r.latency_ms,
                output_valid=True,
                metadata=(
                    {
                        "failure_reason": last_fail.failure.reason,
                        "failure_detail": dict(last_fail.failure.detail or {}),
                        "failure_signature": (last_fail.failure.detail or {}).get("failure_signature"),
                        "exception_type": (last_fail.failure.detail or {}).get("exception_type"),
                        "exit_code": (last_fail.failure.detail or {}).get("exit_code"),
                    }
                    if last_fail and last_fail.failure
                    else {}
                ),
            )
            return TTSChainResult(ok=True, final_result=r, selection_observation=sel_obs, fallback_observation=fb_obs, attempts=attempts)

        last_fail = r
        if not fallback_enabled:
            break

    # 全失败
    fb_obs = None
    if len(tried) >= 2 and last_fail is not None:
        fb_obs = ProviderFallbackObservation(
            request_id=request_id,
            timestamp=_now_ts(),
            primary_provider=tried[0],
            fallback_provider=tried[-1],
            fallback_reason="FALLBACK_FAILED",
            failure_type=(last_fail.failure.failure_type if last_fail.failure else "unknown"),
            final_provider_used=tried[-1],
            latency_ms=last_fail.latency_ms,
            output_valid=False,
            metadata=(
                {
                    "failure_reason": last_fail.failure.reason,
                    "failure_detail": dict(last_fail.failure.detail or {}),
                    "failure_signature": (last_fail.failure.detail or {}).get("failure_signature"),
                    "exception_type": (last_fail.failure.detail or {}).get("exception_type"),
                    "exit_code": (last_fail.failure.detail or {}).get("exit_code"),
                }
                if last_fail and last_fail.failure
                else {}
            ),
        )
    return TTSChainResult(ok=False, final_result=last_fail, selection_observation=sel_obs, fallback_observation=fb_obs, attempts=attempts)


# Backward-compatible alias for existing tests/tools.
# 外部业务请改用 tts_provider_selector.execute_provider_chain()
def run_tts_chain(**kwargs) -> TTSChainResult:  # type: ignore[no-untyped-def]
    return _run_tts_chain_internal(**kwargs)

