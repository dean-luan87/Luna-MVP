# -*- coding: utf-8 -*-
"""
Playback executor (V1 minimal).

边界：
- 本模块作为“playback/result 执行层锚点”的最小替代实现，用于产出 playback_* 真状态事件。
- 不接真实音频设备、不实现队列、不实现中断/恢复；仅证明 request_id 级 playback 事件可闭环。
"""

from __future__ import annotations

import os
import time
from dataclasses import asdict
from typing import Any, Dict, Optional

from capabilities.voice.observations.playback_runtime_observation import PlaybackRuntimeObservation


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes")


def _now() -> float:
    return time.time()


def run_playback_executor_v1(
    *,
    request_id: str,
    audio_bytes: Optional[bytes],
    emit: callable,  # emit(type, data)
) -> bool:
    """
    返回：是否“播放完成”（V1 语义：执行层已处理完成并给出终态）。
    """
    if not request_id:
        return False

    if _env_truthy("LUNA_PLAYBACK_RUNTIME_V1_FORCE_CANCEL"):
        obs = PlaybackRuntimeObservation(
            request_id=request_id,
            timestamp=_now(),
            event="playback_cancelled",
            status="cancelled",
            reason="forced_cancel_v1",
        )
        emit("playback_runtime", asdict(obs))
        return False

    if not audio_bytes:
        obs = PlaybackRuntimeObservation(
            request_id=request_id,
            timestamp=_now(),
            event="playback_failed",
            status="fail",
            reason="no_audio_bytes",
        )
        emit("playback_runtime", asdict(obs))
        return False

    obs_start = PlaybackRuntimeObservation(
        request_id=request_id,
        timestamp=_now(),
        event="playback_started",
        status="ok",
        reason="playback_executor_started",
        metadata={"audio_bytes_len": len(audio_bytes)},
    )
    emit("playback_runtime", asdict(obs_start))

    # V1：不接设备/队列，视为同步完成（真实播放接线在后续版本）
    obs_fin = PlaybackRuntimeObservation(
        request_id=request_id,
        timestamp=_now(),
        event="playback_finished",
        status="ok",
        reason="playback_executor_finished",
    )
    emit("playback_runtime", asdict(obs_fin))
    return True

