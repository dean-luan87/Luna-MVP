# -*- coding: utf-8 -*-
"""
unified_env_summary_v1 最小构建（V1）

边界：
- 仅产出统一环境摘要 dict（不接主线、不替换 sidewalk/retail）
- 与 risk_summary_v1 / find_item_intent_summary_v1 / ocr_summary_v1 零耦合（本模块不 import、不读取）
- scene_family 第一版仅：walkway | retail | unknown
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Literal, Optional, Tuple

SummaryFreshnessV1 = Literal["fresh", "stale", "ambiguous"]
SceneFamilyV1 = Literal["walkway", "retail", "unknown"]


def default_unified_ttl_ms_v1() -> int:
    raw = os.getenv("LUNA_UNIFIED_ENV_SUMMARY_TTL_MS", "").strip()
    if not raw:
        return 6000
    try:
        v = int(raw)
        return max(100, v)
    except ValueError:
        return 6000


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _norm_scene(s: str) -> str:
    return (s or "").strip().lower() or "unknown"


def _classify_scene_family(
    *,
    raw_scene_candidate: str,
    raw_family_hint: Optional[str],
) -> Tuple[SceneFamilyV1, List[str]]:
    """
    将原始 scene 与可选 hint 归一为 walkway | retail | unknown。
    hint 仅在 scene 本身无法判定为 walkway/retail 时作为弱提示（不得覆盖明确冲突）。
    """
    notes: List[str] = []
    s = _norm_scene(raw_scene_candidate)

    retail_markers = ("retail_shelf", "retail_aisle", "retail_shop", "retail_store", "grocery_aisle")
    walkway_markers = ("outdoor_walkway", "walkway", "sidewalk", "pedestrian", "path_outdoor")

    def _has_any(hay: str, needles: tuple[str, ...]) -> bool:
        return any(n in hay for n in needles)

    hint = (raw_family_hint or "").strip().lower()

    is_retail = _has_any(s, retail_markers) or (
        "retail" in s and "walk" not in s and "walkway" not in s
    )
    is_walkway = _has_any(s, walkway_markers) or (s == "outdoor" and "retail" not in s)

    if is_retail and is_walkway:
        notes.append("family_keyword_conflict")
        fam: SceneFamilyV1 = "unknown"
        return fam, notes

    # Guardrail: hint 只补缺，但当 hint 与关键词强命中冲突时，不允许“硬定类”，回落 unknown。
    # 目的：避免跨域字符串污染导致的过早定类（candidate 激进，family 必须保守）。
    if hint in ("walkway", "retail"):
        if is_retail and hint == "walkway":
            notes.append("family_hint_conflict_retail_vs_walkway")
            return "unknown", notes
        if is_walkway and hint == "retail":
            notes.append("family_hint_conflict_walkway_vs_retail")
            return "unknown", notes

    if is_retail:
        return "retail", notes
    if is_walkway:
        return "walkway", notes

    if hint in ("walkway", "retail"):
        notes.append("family_hint_disambiguation")
        return hint, notes  # type: ignore[return-value]

    return "unknown", notes


def _classify_freshness(
    *,
    age_ms: float,
    ttl_ms: int,
    env_confidence: float,
    scene_family: SceneFamilyV1,
    family_notes: List[str],
) -> Tuple[SummaryFreshnessV1, List[str]]:
    notes = list(family_notes)
    if age_ms >= float(ttl_ms):
        notes.append("ttl_expired")
        return "stale", notes

    ec = _clamp01(env_confidence)
    if ec < 0.2:
        notes.append("low_environment_confidence")
        return "ambiguous", notes

    if "family_keyword_conflict" in family_notes:
        notes.append("ambiguous_family")
        return "ambiguous", notes

    if scene_family == "unknown" and ec < 0.45:
        notes.append("unknown_family_low_confidence")
        return "ambiguous", notes

    return "fresh", notes


def _confidence_weight(
    *,
    freshness: SummaryFreshnessV1,
    env_confidence: float,
    age_ms: float,
    ttl_ms: int,
) -> float:
    if freshness == "stale":
        return 0.0
    decay = max(0.0, min(1.0, 1.0 - (age_ms / float(ttl_ms))))
    base = _clamp01(env_confidence) * decay
    if freshness == "ambiguous":
        return _clamp01(base * 0.5)
    return _clamp01(base)


def build_unified_env_summary_v1(
    *,
    raw_scene_candidate: str = "unknown",
    raw_environment_confidence: float = 0.0,
    event_timestamp: float,
    source: str = "unified_env_summary_builder_v1",
    raw_family_hint: Optional[str] = None,
    ttl_override_ms: Optional[int] = None,
    now: Optional[float] = None,
) -> Dict[str, Any]:
    """
    从最小原始环境信号生成 unified_env_summary_v1（dict）。

    :param event_timestamp: 观测时间（秒，与 time.time() 同口径）
    :param now: 当前时间（秒）；默认 time.time()
    :param ttl_override_ms: TTL；默认 env LUNA_UNIFIED_ENV_SUMMARY_TTL_MS 或 6000
    :param source: 摘要来源标记（白盒 / 对账用）
    """
    t_now = float(now if now is not None else time.time())
    t_evt = float(event_timestamp)
    ttl = int(ttl_override_ms if ttl_override_ms is not None else default_unified_ttl_ms_v1())

    age_ms = max(0.0, (t_now - t_evt) * 1000.0)
    scene_candidate = str(raw_scene_candidate or "unknown").strip() or "unknown"
    env_conf = float(raw_environment_confidence or 0.0)

    scene_family, family_notes = _classify_scene_family(
        raw_scene_candidate=scene_candidate,
        raw_family_hint=raw_family_hint,
    )
    freshness, inference_notes = _classify_freshness(
        age_ms=age_ms,
        ttl_ms=ttl,
        env_confidence=env_conf,
        scene_family=scene_family,
        family_notes=family_notes,
    )
    weight = _confidence_weight(
        freshness=freshness,
        env_confidence=env_conf,
        age_ms=age_ms,
        ttl_ms=ttl,
    )

    return {
        "scene_family": scene_family,
        "scene_candidate": scene_candidate,
        "environment_confidence": float(env_conf),
        "event_timestamp": t_evt,
        "summary_freshness": freshness,
        "ttl_ms": ttl,
        "confidence_weight": float(weight),
        "source": str(source or "unified_env_summary_builder_v1"),
        "summary_schema_version": "unified_env_summary_v1/1",
        "age_ms": float(age_ms),
        "inference_notes": list(inference_notes),
    }


__all__ = [
    "SceneFamilyV1",
    "SummaryFreshnessV1",
    "build_unified_env_summary_v1",
    "default_unified_ttl_ms_v1",
]
