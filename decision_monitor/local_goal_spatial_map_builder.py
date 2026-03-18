# -*- coding: utf-8 -*-
"""
主线 2 第二阶段 M0/M1.5：Local Goal Spatial Map builder。

M1.5：接入宪法最小精确标尺与派生标尺；方向扇区仅用 BASE_SECTORS（无 near_front 混维）；
近场表达由 sector=front + distance_band=immediate/near 组合。
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .local_goal_spatial_map import (
    BASE_SECTORS,
    DISTANCE_BANDS,
    OFFSET_BANDS,
    SPEED_BANDS,
    SCENE_PROFILES,
    LocalGoalSpatialMap,
    SpatialRegion,
)
from .schema import InputsLayer, LocalGoalState, SpatialScaleContext, StateLayer


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _clamp01(x: float) -> float:
    if x < 0:
        return 0.0
    if x > 1:
        return 1.0
    return float(x)


# 宪法 4.1：仅基础方向扇区；近场用 front + distance_band 表达
def _sector_from_focus_region(focus_region: Optional[str]) -> str:
    s = str(focus_region or "")
    if "左" in s:
        return "front_left"
    if "右" in s:
        return "front_right"
    return "front"


def _is_close_range_focus(focus_region: Optional[str]) -> bool:
    """近场关注时用 front + distance_band=immediate/near，不写 near_front。"""
    return "近场" in str(focus_region or "")


def _bearing_deg_for_sector(sector: str) -> float:
    """宪法 3.1：relative_bearing_deg 相对当前行动前向。"""
    m = {"front": 0.0, "front_right": 30.0, "right": 90.0, "rear": 180.0, "front_left": -30.0, "left": -90.0}
    return m.get(sector, 0.0)


def _distance_cm_and_band_for_focus(is_near: bool) -> tuple[Optional[float], str]:
    if is_near:
        return (80.0, "immediate")
    return (200.0, "mid")


def _distance_cm_and_band_for_sector(sector: str, is_confirm_close: bool) -> tuple[Optional[float], str]:
    if is_confirm_close or sector == "front":
        return (120.0, "near")
    return (250.0, "mid")


def _stability_score(state: StateLayer, staleness_ms: Optional[float]) -> float:
    """
    M1 规则型稳定度：基于现有字段生成可比较的 0~1 分值。
    输入特征（只读）：state_trend / staleness / predictive_hold_active / runtime_domain_state / view_misaligned / vision_degraded。
    """
    score = 0.75
    trend = _get(state, "state_trend")
    domain = _get(state, "runtime_domain_state")
    if trend in ("worsening", "shifting"):
        score -= 0.15
    elif trend == "recovering":
        score -= 0.05
    if domain == "degraded":
        score -= 0.15
    elif domain == "frozen":
        score -= 0.35
    if _get(state, "view_misaligned") is True:
        score -= 0.15
    if _get(state, "vision_degraded") is True:
        score -= 0.10
    if _get(state, "predictive_hold_active") is True:
        score -= 0.08
    if staleness_ms is not None:
        if staleness_ms >= 3000:
            score -= 0.20
        elif staleness_ms >= 1500:
            score -= 0.10
    return _clamp01(score)


def _scene_profile_from_state(state: StateLayer, ctx: Dict[str, Any]) -> str:
    """M1.5：室内/室外最小区分；室外优先角度，室内保守覆盖。"""
    scene_type = _get(state, "scene_type") or ""
    if "close_range" in scene_type or "stationary" in scene_type:
        return "indoor"
    if "normal_walk" in scene_type or "cautious" in scene_type:
        return "outdoor"
    # 默认 outdoor；ctx 可覆盖
    return ctx.get("scene_profile") or "outdoor"


def _mk(
    region_type: str,
    sector: str,
    confidence: float,
    priority_rank: int,
    state: StateLayer,
    staleness_ms: Optional[float],
    reason: Optional[str] = None,
    ttl_ms: Optional[float] = None,
    distance_cm: Optional[float] = None,
    distance_band: Optional[str] = None,
    offset_band: Optional[str] = None,
) -> SpatialRegion:
    sector = sector if sector in BASE_SECTORS else "front"
    return SpatialRegion(
        region_type=region_type,
        sector=sector,
        confidence=_clamp01(confidence),
        priority_rank=priority_rank,
        reason=reason,
        ttl_ms=ttl_ms,
        stability_score=_stability_score(state, staleness_ms),
        relative_bearing_deg=_bearing_deg_for_sector(sector),
        distance_cm=distance_cm,
        staleness_ms=staleness_ms,
        distance_band=distance_band or "mid",
        offset_band=offset_band or "aligned",
    )


def _build_spatial_scale(ctx: Dict[str, Any], state: StateLayer, scene_profile: str) -> SpatialScaleContext:
    """M1.5：用户包络 + 速度；宪法默认有效宽度 70cm，高度可默认 profile。"""
    width = ctx.get("effective_body_width_cm")
    if width is None:
        width = 70.0  # 宪法 default_effective_body_width_cm
    height = ctx.get("effective_body_height_cm")
    if height is None:
        height = 170.0  # 默认高度 profile
    clearance = ctx.get("clearance_required_cm")
    if clearance is None:
        clearance = width + 20.0  # 最小通过间隙
    speed = ctx.get("forward_speed_cm_s")
    if speed is None:
        speed = 0.0
    band = ctx.get("speed_band")
    if band is None:
        if speed <= 0:
            band = "stopped"
        elif speed < 30:
            band = "slow"
        elif speed < 80:
            band = "normal"
        else:
            band = "fast"
    if band not in SPEED_BANDS:
        band = "stopped"
    horizon = ctx.get("reaction_horizon_ms")
    if horizon is None:
        horizon = 500.0 if band != "stopped" else 200.0
    return SpatialScaleContext(
        scene_profile=scene_profile,
        effective_body_width_cm=float(width),
        effective_body_height_cm=float(height),
        clearance_required_cm=float(clearance),
        forward_speed_cm_s=float(speed),
        speed_band=band,
        reaction_horizon_ms=float(horizon),
    )


def build(
    ctx: Dict[str, Any],
    local_goal_state: LocalGoalState,
    state: StateLayer,
    inputs: InputsLayer,
) -> LocalGoalSpatialMap:
    goal_id = _get(local_goal_state, "goal_id")
    goal_type = _get(local_goal_state, "goal_type")
    produced_ts = _get(inputs, "produced_ts") or _get(inputs, "current_ts") or ctx.get("current_ts")
    staleness_ms = _get(local_goal_state, "state_staleness_ms") or _get(inputs, "delta_t_ms")

    focus_region = _get(local_goal_state, "goal_focus_region")
    next_best = _get(local_goal_state, "next_best_action")
    recheck_required = _get(local_goal_state, "recheck_required") is True

    focus_sector = _sector_from_focus_region(focus_region)
    is_close_range = _is_close_range_focus(focus_region)
    d_cm_focus, d_band_focus = _distance_cm_and_band_for_focus(is_close_range)

    scene_profile = _scene_profile_from_state(state, ctx)

    # 1) focus_region（仅 BASE_SECTORS；近场用 front + distance_band）
    focus: List[SpatialRegion] = []
    focus.append(
        _mk(
            region_type="focus_region",
            sector=focus_sector,
            confidence=0.82 if focus_region else 0.6,
            priority_rank=1,
            state=state,
            staleness_ms=staleness_ms,
            reason=f"goal_focus_region={focus_region}" if focus_region else "default_focus",
            ttl_ms=3000.0,
            distance_cm=d_cm_focus,
            distance_band=d_band_focus,
        )
    )
    if str(focus_region or "").find("前向") >= 0 or focus_sector == "front":
        focus.append(
            _mk(
                region_type="focus_region",
                sector="front_left",
                confidence=0.56,
                priority_rank=2,
                state=state,
                staleness_ms=staleness_ms,
                reason="secondary_focus_candidate",
                ttl_ms=1500.0,
                distance_cm=200.0,
                distance_band="mid",
            )
        )

    domain = _get(state, "runtime_domain_state")
    trav_state = _get(state, "traversability_state")
    traversable: List[SpatialRegion] = []
    if domain == "frozen":
        traversable.append(
            _mk("traversable_region", "front", 0.35, 1, state, staleness_ms, "runtime_domain_frozen", 1500.0, 200.0, "mid")
        )
    elif domain == "degraded":
        if _get(state, "view_misaligned") is True:
            traversable.append(
                _mk("traversable_region", "front_left", 0.62, 1, state, staleness_ms, "domain_degraded_view_misaligned", 1500.0, 220.0, "mid")
            )
            traversable.append(
                _mk("traversable_region", "front", 0.52, 2, state, staleness_ms, "secondary_front_candidate", 1500.0, 200.0, "mid")
            )
        else:
            traversable.append(
                _mk("traversable_region", "front", 0.65, 1, state, staleness_ms, "runtime_domain_degraded", 1500.0, 200.0, "mid")
            )
            traversable.append(
                _mk("traversable_region", "front_left", 0.55, 2, state, staleness_ms, "secondary_left_candidate", 1500.0, 220.0, "mid")
            )
    else:
        if is_close_range:
            traversable.append(
                _mk("traversable_region", "front", 0.74, 1, state, staleness_ms, "close_range_focus", 2000.0, 80.0, "immediate")
            )
        else:
            traversable.append(
                _mk(
                    "traversable_region",
                    "front",
                    0.76 if trav_state else 0.70,
                    1,
                    state,
                    staleness_ms,
                    f"traversability_state={trav_state}" if trav_state else "default_traversable",
                    3000.0,
                    200.0,
                    "mid",
                )
            )
            traversable.append(
                _mk("traversable_region", "front_left", 0.58, 2, state, staleness_ms, "secondary_left_candidate", 3000.0, 220.0, "mid")
            )

    risk_score = _get(state, "risk_score")
    view_misaligned = _get(state, "view_misaligned") is True
    vision_degraded = _get(state, "vision_degraded") is True
    risk: List[SpatialRegion] = []
    if view_misaligned:
        risk.append(_mk("risk_region", "front_right", 0.63, 1, state, staleness_ms, "view_misaligned", 1500.0, 180.0, "near"))
        risk.append(_mk("risk_region", "front", 0.52, 2, state, staleness_ms, "secondary_front_due_to_misaligned", 1500.0, 200.0, "mid"))
    elif vision_degraded:
        risk.append(_mk("risk_region", "front", 0.60, 1, state, staleness_ms, "vision_degraded", 1500.0, 100.0, "near"))
        risk.append(_mk("risk_region", "front_left", 0.50, 2, state, staleness_ms, "secondary_due_to_vision", 1500.0, 200.0, "mid"))
    else:
        base = 0.45
        conf = _clamp01(0.4 + float(risk_score)) if risk_score is not None else base
        risk.append(_mk("risk_region", "front", conf, 1, state, staleness_ms, "risk_score", 1500.0, 200.0, "mid"))
        if risk_score is not None and float(risk_score) >= 0.5:
            risk.append(_mk("risk_region", "front_right", 0.58, 2, state, staleness_ms, "risk_score_high_secondary", 1500.0, 220.0, "mid"))

    confirm: List[SpatialRegion] = []
    if recheck_required or next_best in ("recheck_close_range", "recheck_environment", "hold_and_confirm"):
        if next_best == "recheck_close_range":
            c_sector = "front"
            c_reason = "next_best_action=recheck_close_range"
            c_d_cm, c_d_band = 80.0, "immediate"
        elif next_best == "recheck_environment":
            c_sector = "front"
            c_reason = "next_best_action=recheck_environment"
            c_d_cm, c_d_band = 200.0, "mid"
        else:
            c_sector = focus_sector
            c_reason = f"next_best_action={next_best or 'hold'}"
            c_d_cm, c_d_band = _distance_cm_and_band_for_sector(c_sector, False)
        confirm.append(_mk("confirm_region", c_sector, 0.71, 1, state, staleness_ms, c_reason, 1500.0, c_d_cm, c_d_band))
        alt = "front_left" if c_sector == "front" else "front"
        confirm.append(_mk("confirm_region", alt, 0.56, 2, state, staleness_ms, "secondary_confirm_candidate", 1500.0, 200.0, "mid"))

    for reg in focus + traversable + risk + confirm:
        if reg.sector not in BASE_SECTORS:
            reg.sector = "front"

    summary = f"focus={focus_sector} next={next_best} domain={domain} profile={scene_profile}"
    return LocalGoalSpatialMap(
        goal_id=goal_id,
        goal_type=goal_type,
        produced_ts=produced_ts,
        staleness_ms=staleness_ms,
        scene_profile=scene_profile,
        focus_region=focus[:3] if focus else None,
        traversable_region=traversable[:3] if traversable else None,
        risk_region=risk[:3] if risk else None,
        confirm_region=confirm[:3] if confirm else None,
        summary=summary,
    )


def build_spatial_scale(ctx: Dict[str, Any], state: StateLayer, scene_profile: str) -> SpatialScaleContext:
    """M1.5：供 builder 调用的标尺上下文；与 build() 使用相同 scene_profile。"""
    return _build_spatial_scale(ctx, state, scene_profile)

