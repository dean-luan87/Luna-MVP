# -*- coding: utf-8 -*-
"""
sidewalk_env_summary_v1 最小构建 / 稳定化（V1）

边界：
- 仅产出可并入 VoiceRuntimeContext.metadata["sidewalk_env_summary_v1"] 的 dict
- 与 risk_summary_v1 零耦合（本模块不 import、不读取 risk）
- 不修改 sidewalk_nav_v1 / orchestrator / 主链
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Literal, Optional, Tuple

SummaryFreshnessV1 = Literal["fresh", "stale", "ambiguous"]


def default_ttl_ms_v1() -> int:
    raw = os.getenv("LUNA_SIDEWALK_ENV_SUMMARY_TTL_MS", "").strip()
    if not raw:
        return 5000
    try:
        v = int(raw)
        return max(100, v)
    except ValueError:
        return 5000


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _norm_scene(s: str) -> str:
    return (s or "").strip().lower() or "unknown"


def _classify_freshness(
    *,
    age_ms: float,
    ttl_ms: int,
    path_confidence: float,
    scene_norm: str,
    is_outdoor: bool,
) -> Tuple[SummaryFreshnessV1, List[str]]:
    notes: List[str] = []
    if age_ms >= float(ttl_ms):
        notes.append("ttl_expired")
        return "stale", notes

    pc = _clamp01(path_confidence)
    # ambiguous：TTL 内但证据偏弱（与稳定化方案「低置信 / 输入不足」对齐）
    if pc < 0.2:
        notes.append("low_path_confidence")
        return "ambiguous", notes
    if scene_norm == "unknown" and pc < 0.45:
        notes.append("unknown_scene_low_path_confidence")
        return "ambiguous", notes
    if scene_norm == "unknown" and not is_outdoor and pc < 0.65:
        notes.append("unknown_scene_not_outdoor")
        return "ambiguous", notes

    return "fresh", notes


def _confidence_weight(
    *,
    freshness: SummaryFreshnessV1,
    path_confidence: float,
    age_ms: float,
    ttl_ms: int,
) -> float:
    if freshness == "stale":
        return 0.0
    decay = max(0.0, min(1.0, 1.0 - (age_ms / float(ttl_ms))))
    base = _clamp01(path_confidence) * decay
    if freshness == "ambiguous":
        return _clamp01(base * 0.5)
    return _clamp01(base)


def build_sidewalk_env_summary_v1(
    *,
    scene_candidate: str = "unknown",
    path_confidence: float = 0.0,
    is_outdoor: bool = False,
    event_timestamp: float,
    now: Optional[float] = None,
    ttl_ms: Optional[int] = None,
    source: str = "sidewalk_env_summary_builder_v1",
) -> Dict[str, Any]:
    """
    从最小原始信号生成稳定化后的 sidewalk_env_summary_v1（dict）。

    :param event_timestamp: 观测时间（秒，与 time.time() 同口径）
    :param now: 当前时间（秒）；默认 time.time()
    :param ttl_ms: TTL；默认 env LUNA_SIDEWALK_ENV_SUMMARY_TTL_MS 或 5000
    :param source: 摘要来源标记（白盒 / 对账用）
    """
    t_now = float(now if now is not None else time.time())
    t_evt = float(event_timestamp)
    ttl = int(ttl_ms if ttl_ms is not None else default_ttl_ms_v1())

    age_ms = max(0.0, (t_now - t_evt) * 1000.0)
    scene_norm = _norm_scene(scene_candidate)
    freshness, inference_notes = _classify_freshness(
        age_ms=age_ms,
        ttl_ms=ttl,
        path_confidence=float(path_confidence or 0.0),
        scene_norm=scene_norm,
        is_outdoor=bool(is_outdoor),
    )
    weight = _confidence_weight(
        freshness=freshness,
        path_confidence=float(path_confidence or 0.0),
        age_ms=age_ms,
        ttl_ms=ttl,
    )

    return {
        "scene_candidate": str(scene_candidate or "unknown").strip() or "unknown",
        "path_confidence": float(path_confidence or 0.0),
        "is_outdoor": bool(is_outdoor),
        "summary_freshness": freshness,
        "event_timestamp": t_evt,
        "ttl_ms": ttl,
        "confidence_weight": float(weight),
        "summary_schema_version": "sidewalk_env_summary_v1/1",
        "source": str(source or "sidewalk_env_summary_builder_v1"),
        "age_ms": float(age_ms),
        "inference_notes": list(inference_notes),
    }
