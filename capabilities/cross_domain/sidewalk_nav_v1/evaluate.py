#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人行道导航 V1：最小旁路评估（默认关闭）。

边界：
- 不 import 主链；不修改 risk_interrupt_v1
- 高风险或显式 risk_interrupt 抢占时压下普通导航提示
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def _env_truthy(name: str, *, default: bool = False) -> bool:
    raw = os.getenv(name, "")
    if raw == "":
        return bool(default)
    return raw.strip().lower() in ("1", "true", "yes")


def sidewalk_nav_enabled() -> bool:
    return _env_truthy("LUNA_ENABLE_SIDEWALK_NAV_V1", default=False)


def sidewalk_nav_whitebox_only() -> bool:
    return _env_truthy("LUNA_SIDEWALK_NAV_WHITEBOX_ONLY", default=True)


@dataclass(frozen=True)
class SidewalkEnvironmentInput:
    """最小环境输入（V1 可规则占位，后续再接管线）。"""

    scene_candidate: str = "unknown"
    path_confidence: float = 0.0
    is_outdoor: bool = False


@dataclass(frozen=True)
class RiskSummaryInput:
    """只读风险摘要（由上游风险快扫 / risk_interrupt 侧提供）。"""

    risk_level: str = "low"
    risk_type: str = ""
    safe_direction_hint: str = ""


def _normalize_level(level: str) -> str:
    return (level or "").strip().lower()


def _is_high_risk(risk_level: str) -> bool:
    return _normalize_level(risk_level) in ("high", "critical")


def _classify_scene(env: SidewalkEnvironmentInput) -> tuple[str, bool, float]:
    """
    返回 (scene_type, sidewalk_detected, sidewalk_confidence)。
    V1：规则极简，不调用视觉模型。
    """
    cand = (env.scene_candidate or "").strip().lower()
    pc = float(env.path_confidence or 0.0)
    if cand == "outdoor_walkway":
        return "outdoor_walkway", True, max(0.55, min(1.0, pc if pc > 0 else 0.72))
    if env.is_outdoor and pc >= 0.45:
        return "outdoor_walkway", True, max(0.45, min(1.0, pc))
    return "unknown", False, max(0.0, min(1.0, pc))


def _minimal_navigation_hint(*, scene_type: str, sidewalk_detected: bool) -> str:
    if scene_type != "outdoor_walkway" or not sidewalk_detected:
        return ""
    return "靠右直行，注意前方路况。"


@dataclass(frozen=True)
class SidewalkNavResult:
    scene_type: str
    sidewalk_detected: bool
    sidewalk_confidence: float
    navigation_hint: str
    output_suppressed_by_risk: bool
    final_spoken_output: str
    current_scene_type: str
    current_navigation_hint: str
    risk_override_active: bool
    last_risk_level: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def evaluate_sidewalk_nav_v1(
    *,
    environment: SidewalkEnvironmentInput,
    risk: RiskSummaryInput,
    timestamp_ms: Optional[int] = None,
    risk_interrupt_preempt: bool = False,
) -> SidewalkNavResult:
    """
    主入口：环境初判 + 风险压制 + 最小通行建议 + 白盒。

    risk_interrupt_preempt:
        当上层已判定 risk_interrupt_v1 本轮生效抢占时置 True，用于压下人行道导航外显。
    """
    ts = int(timestamp_ms if isinstance(timestamp_ms, int) else (time.time() * 1000.0))
    empty_meta: Dict[str, Any] = {}

    if not sidewalk_nav_enabled():
        scene_type, sd, sc = _classify_scene(environment)
        return SidewalkNavResult(
            scene_type=scene_type,
            sidewalk_detected=sd,
            sidewalk_confidence=sc,
            navigation_hint="",
            output_suppressed_by_risk=False,
            final_spoken_output="",
            current_scene_type=scene_type,
            current_navigation_hint="",
            risk_override_active=False,
            last_risk_level=_normalize_level(risk.risk_level) or "low",
            metadata=empty_meta,
        )

    scene_type, sidewalk_detected, sidewalk_confidence = _classify_scene(environment)
    last_risk = _normalize_level(risk.risk_level) or "low"
    high = _is_high_risk(risk.risk_level)
    risk_override_active = bool(high or risk_interrupt_preempt)
    output_suppressed_by_risk = risk_override_active

    nav_candidate = ""
    if not output_suppressed_by_risk:
        nav_candidate = _minimal_navigation_hint(
            scene_type=scene_type, sidewalk_detected=sidewalk_detected
        )

    whitebox_only = sidewalk_nav_whitebox_only()
    # 外显：非白盒、无风险压制、且有人行道提示时才播报
    final_spoken = ""
    if not whitebox_only and nav_candidate and not output_suppressed_by_risk:
        final_spoken = nav_candidate

    risk_summary_wb: Dict[str, Any] = {
        "risk_level": last_risk,
        "risk_type": str(risk.risk_type or ""),
        "safe_direction_hint": str(risk.safe_direction_hint or ""),
        "risk_interrupt_preempt": bool(risk_interrupt_preempt),
    }

    scene_summary = {
        "scene_candidate": environment.scene_candidate,
        "is_outdoor": bool(environment.is_outdoor),
        "path_confidence": float(environment.path_confidence or 0.0),
        "classified_scene_type": scene_type,
    }

    wb = {
        "scene_summary": scene_summary,
        "sidewalk_detected": bool(sidewalk_detected),
        "risk_summary": risk_summary_wb,
        "navigation_hint": nav_candidate,
        "output_suppressed_by_risk": bool(output_suppressed_by_risk),
        "final_spoken_output": final_spoken,
        "whitebox_only": bool(whitebox_only),
        "event_timestamp": ts,
    }

    meta = {"sidewalk_nav_v1": wb}

    return SidewalkNavResult(
        scene_type=scene_type,
        sidewalk_detected=sidewalk_detected,
        sidewalk_confidence=sidewalk_confidence,
        navigation_hint=nav_candidate,
        output_suppressed_by_risk=output_suppressed_by_risk,
        final_spoken_output=final_spoken,
        current_scene_type=scene_type,
        current_navigation_hint=nav_candidate,
        risk_override_active=risk_override_active,
        last_risk_level=last_risk,
        metadata=meta,
    )
