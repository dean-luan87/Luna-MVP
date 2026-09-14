# -*- coding: utf-8 -*-
"""
VoiceOutputPlane minimal implementation (V1).

目标：
- 提供真实可调用的 VoiceOutputPlane.submit()（闭环锚点）
- 默认关闭；启用时仅服务“原主链稳定输出”的提示/确认类短文本（调用方负责限制）
- 不接 speaking/runtime 真源；仅落最小 observation 以便 request_id 抽链验证
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from capabilities.voice.interfaces.voice_output_plane import VoiceOutputPlane
from capabilities.voice.observations.output_submit_observation import OutputSubmitObservation
from capabilities.voice.observations.provider_fallback_observation import ProviderFallbackObservation
from capabilities.voice.observations.provider_selection_observation import ProviderSelectionObservation
from capabilities.voice.observations.request_runtime_observation import RequestRuntimeObservation
from capabilities.voice.observations.tts_cutover_observation import TTSCutoverObservation
from capabilities.voice.observations.tts_rollback_observation import TTSRollbackObservation
from capabilities.voice.output.playback_executor_v1 import run_playback_executor_v1
from capabilities.voice.output.playback_plane_v1 import get_playback_plane_v1
from capabilities.voice.runtime.tts_unified_entry import run_tts_unified_entry
from capabilities.voice.schemas.speech_request import SpeechRequest


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes")


def _now() -> float:
    return time.time()


def _append_jsonl(path: str, obj: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _jsonl_path() -> str:
    return os.getenv("LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL", "logs/real_output_submit_v1.jsonl")


def _emit_envelope(typ: str, data: Dict[str, Any]) -> None:
    _append_jsonl(_jsonl_path(), {"type": typ, "data": data})


class VoiceOutputPlaneV1(VoiceOutputPlane):
    """
    最小输出平面实现：
    - submit() 必须可被主线调用（证明闭环）
    - 默认 dry-run（不依赖本地 TTS 可执行文件）
    - 可选执行 run_tts_unified_entry（通过开关）
    """

    def __init__(self) -> None:
        # 注意：force_* 开关在测试脚本中可能在运行中切换，因此不要在 __init__ 固化。
        self.execute_tts = _env_truthy("LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS")

    def submit(self, request: SpeechRequest) -> Tuple[bool, str]:
        ts = _now()

        # 运行时读取（允许测试中切换）
        force_reject = _env_truthy("LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_REJECT")
        force_fail = _env_truthy("LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_FAIL")

        # Phase-Mainline-RuntimeReadiness-004: guarded trial gate hook-in (default-off no-op).
        # Must not change submit behavior; we attach as debug metadata only.
        hook_meta: Optional[Dict[str, Any]] = None
        try:
            from capabilities.runtime_readiness.qwen_voice_guarded_trial_hook_v0 import (
                evaluate_qwen_voice_guarded_trial_hook_v0,
            )

            hook_meta = evaluate_qwen_voice_guarded_trial_hook_v0(
                request_id=str(request.request_id or ""),
                trace_id=str(request.trace_id or "") if request.trace_id is not None else None,
                trw_payload={
                    "request_id": str(request.request_id or ""),
                    "trace_id": str(request.trace_id or "") if request.trace_id is not None else "",
                    "hard_audit": {"real_qwen_invoked": False, "real_tts_invoked": False},
                    "runtime_run_id": "voice_output_plane_v1_submit",
                    "pending_ref": True,
                },
            )
        except Exception:
            hook_meta = None

        rr_submitted = RequestRuntimeObservation(
            request_id=request.request_id,
            timestamp=ts,
            event="request_submitted",
            status="ok",
            reason="voice_output_plane_submit_called",
            metadata={"execute_tts": bool(self.execute_tts), "guarded_trial_hook": hook_meta},
        )
        _emit_envelope("request_runtime", asdict(rr_submitted))

        if force_reject:
            rr_rej = RequestRuntimeObservation(
                request_id=request.request_id,
                timestamp=_now(),
                event="request_submit_rejected",
                status="rejected",
                reason="forced_reject_v1",
                terminal_mode="unknown",
            )
            _emit_envelope("request_runtime", asdict(rr_rej))
            return False, "forced_reject_v1"

        if force_fail:
            rr_fail = RequestRuntimeObservation(
                request_id=request.request_id,
                timestamp=_now(),
                event="request_submit_failed",
                status="fail",
                reason="forced_fail_v1",
                terminal_mode="failed_no_output",
            )
            _emit_envelope("request_runtime", asdict(rr_fail))
            return False, "forced_fail_v1"

        sub = OutputSubmitObservation(
            request_id=request.request_id,
            timestamp=ts,
            accepted=True,
            reason="submit_invoked",
            metadata={
                "source_module": request.source_module,
                "output_category": request.output_category,
                "dry_run": (not self.execute_tts),
            },
        )
        _emit_envelope("submit_invoked", asdict(sub))

        if not self.execute_tts:
            sel = ProviderSelectionObservation(
                request_id=request.request_id,
                timestamp=_now(),
                chosen_provider="piper",
                preset_name=str((request.metadata or {}).get("preset") or "default"),
                provider_order=["piper"],
                selection_reason="dry_run_v1",
                metadata={"dry_run": True},
            )
            cut = TTSCutoverObservation(
                request_id=request.request_id,
                timestamp=_now(),
                cutover_enabled=True,
                cutover_mode="dry_run_v1",
                selector_hit=True,
                provider_chain_ok=True,
                final_execution_mode="provider_chain",
                final_executor="dry_run_executor",
                metadata={"dry_run": True},
            )
            _emit_envelope("selection", asdict(sel))
            _emit_envelope("cutover", asdict(cut))
            rr_term = RequestRuntimeObservation(
                request_id=request.request_id,
                timestamp=_now(),
                event="request_terminal_observed",
                status="ok",
                reason="dry_run_terminal",
                terminal_mode="provider_chain",
                metadata={"dry_run": True},
            )
            _emit_envelope("request_runtime", asdict(rr_term))
            return True, "dry_run_ok"

        # execute_tts=1：调用现有 unified entry（仍不接 speech_gate/audio_worker）
        res = run_tts_unified_entry(
            request=request,
            legacy_submit=lambda _text: False,
        )
        if res.selection_observation is not None:
            _emit_envelope("selection", asdict(res.selection_observation))
        if res.fallback_observation is not None:
            _emit_envelope("fallback", asdict(res.fallback_observation))
        if res.rollback_observation is not None:
            _emit_envelope("rollback", asdict(res.rollback_observation))
        _emit_envelope("cutover", asdict(res.cutover_observation))

        # playback 真源（V1）：
        # - 默认走旧锚点 playback_executor_v1
        # - 开启 LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1=1 后，改为走 Playback Plane + Audio Worker（单线程/单队列）
        audio_bytes = None
        if res.provider_result is not None and res.provider_result.ok:
            audio_bytes = res.provider_result.audio_bytes
        if _env_truthy("LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1"):
            plane = get_playback_plane_v1()
            _ = plane.submit(
                request_id=request.request_id,
                audio_bytes=audio_bytes,
                metadata={
                    "final_execution_mode": res.final_execution_mode,
                    "provider": (res.provider_result.provider_name if res.provider_result is not None else None),
                },
                emit=_emit_envelope,
            )
        else:
            _ = run_playback_executor_v1(
                request_id=request.request_id,
                audio_bytes=audio_bytes,
                emit=_emit_envelope,
            )
        rr_term2 = RequestRuntimeObservation(
            request_id=request.request_id,
            timestamp=_now(),
            event="request_terminal_observed",
            status="ok" if res.ok else "fail",
            reason=f"tts_unified_entry_terminal:{res.final_execution_mode}",
            terminal_mode=str(res.final_execution_mode or "unknown"),
        )
        _emit_envelope("request_runtime", asdict(rr_term2))
        return bool(res.ok), f"tts_unified_entry:{res.final_execution_mode}"


_PLANE_SINGLETON: Optional[VoiceOutputPlaneV1] = None


def get_voice_output_plane_v1() -> VoiceOutputPlaneV1:
    global _PLANE_SINGLETON
    if _PLANE_SINGLETON is None:
        _PLANE_SINGLETON = VoiceOutputPlaneV1()
    return _PLANE_SINGLETON

