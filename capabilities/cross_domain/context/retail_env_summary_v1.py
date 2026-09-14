# -*- coding: utf-8 -*-
"""
retail_env_summary_v1 最小构建 / 稳定化（V1）

边界：
- 仅产出可并入 VoiceRuntimeContext.metadata["retail_env_summary_v1"] 的 dict
- 不并入 OCR（独立 ocr_summary_v1）；不与 find_item_intent_summary_v1 / risk_summary_v1 耦合
- 不修改 retail_find_item_v1 / orchestrator / 主链
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Literal, Optional, Tuple

SummaryFreshnessV1 = Literal["fresh", "stale", "ambiguous"]


def default_retail_ttl_ms_v1() -> int:
    raw = os.getenv("LUNA_RETAIL_ENV_SUMMARY_TTL_MS", "").strip()
    if not raw:
        return 8000
    try:
        v = int(raw)
        return max(100, v)
    except ValueError:
        return 8000


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _norm_retail_scene(scene_type: str, scene_type_candidate: str) -> str:
    s = (scene_type or scene_type_candidate or "").strip().lower() or "unknown"
    if s in ("retail_shelf", "retail_aisle"):
        return s
    return "unknown"


def _classify_freshness(
    *,
    age_ms: float,
    ttl_ms: int,
    retail_conf: float,
    scene_norm: str,
    shelf_visible: bool,
    gating_passed: Optional[bool],
) -> Tuple[SummaryFreshnessV1, List[str]]:
    notes: List[str] = []
    if age_ms >= float(ttl_ms):
        notes.append("ttl_expired")
        return "stale", notes

    rc = _clamp01(retail_conf)

    if rc < 0.22:
        notes.append("low_retail_context_confidence")
        return "ambiguous", notes

    if scene_norm == "unknown" and rc < 0.48:
        notes.append("unknown_scene_low_confidence")
        return "ambiguous", notes

    if scene_norm in ("retail_shelf", "retail_aisle") and (not shelf_visible) and rc < 0.52:
        notes.append("retail_scene_low_visibility")
        return "ambiguous", notes

    if gating_passed is True and scene_norm == "unknown" and rc < 0.55:
        notes.append("gating_scene_mismatch")
        return "ambiguous", notes

    return "fresh", notes


def _confidence_weight(
    *,
    freshness: SummaryFreshnessV1,
    retail_conf: float,
    age_ms: float,
    ttl_ms: int,
) -> float:
    if freshness == "stale":
        return 0.0
    decay = max(0.0, min(1.0, 1.0 - (age_ms / float(ttl_ms))))
    base = _clamp01(retail_conf) * decay
    if freshness == "ambiguous":
        return _clamp01(base * 0.5)
    return _clamp01(base)


def build_retail_env_summary_v1(
    *,
    scene_type: str = "",
    scene_type_candidate: str = "",
    retail_context_confidence: float = 0.0,
    shelf_visible: bool = False,
    gating_passed: Optional[bool] = None,
    event_timestamp: float,
    now: Optional[float] = None,
    ttl_ms: Optional[int] = None,
    source: str = "retail_env_summary_builder_v1",
) -> Dict[str, Any]:
    """
    从最小原始信号生成稳定化后的 retail_env_summary_v1（dict）。

    :param event_timestamp: 观测时间（秒，与 time.time() 同口径）
    :param scene_type / scene_type_candidate: 二者取其一即可；规范化为 retail_shelf | retail_aisle | unknown
    """
    t_now = float(now if now is not None else time.time())
    t_evt = float(event_timestamp)
    ttl = int(ttl_ms if ttl_ms is not None else default_retail_ttl_ms_v1())

    age_ms = max(0.0, (t_now - t_evt) * 1000.0)
    scene_norm = _norm_retail_scene(scene_type, scene_type_candidate)
    rc_in = float(retail_context_confidence or 0.0)
    sv = bool(shelf_visible)

    freshness, inference_notes = _classify_freshness(
        age_ms=age_ms,
        ttl_ms=ttl,
        retail_conf=rc_in,
        scene_norm=scene_norm,
        shelf_visible=sv,
        gating_passed=gating_passed,
    )
    weight = _confidence_weight(
        freshness=freshness,
        retail_conf=rc_in,
        age_ms=age_ms,
        ttl_ms=ttl,
    )

    return {
        "scene_type": scene_norm,
        "scene_type_candidate": scene_norm,
        "retail_context_confidence": rc_in,
        "shelf_visible": sv,
        "gating_passed": gating_passed,
        "summary_freshness": freshness,
        "event_timestamp": t_evt,
        "ttl_ms": ttl,
        "confidence_weight": float(weight),
        "summary_schema_version": "retail_env_summary_v1/1",
        "source": str(source or "retail_env_summary_builder_v1"),
        "age_ms": float(age_ms),
        "inference_notes": list(inference_notes),
    }
