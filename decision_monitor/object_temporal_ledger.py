# -*- coding: utf-8 -*-
"""
对象时空账本 M0/M1：Object Temporal Ledger。

M0：最小单对象载体（位置、可见性、容器候选、事件链）。
M1：事件链增强、容器状态、用户确认写回、最后可信位置与当前候选位置分离。
不做多对象全场账本、不做复杂 re-id、不做持久化多对象库、不做经验沉淀。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

from .evidence_ledger import EvidenceLedger
from .hypothesis_layer import HypothesisLayer
from .local_goal_spatial_map import LocalGoalSpatialMap
from .recheck_planner import RecheckPlannerResult
from .spatial_memory_pools import SpatialMemoryPools

VISIBILITY_STATUSES = ("visible", "occluded", "lost", "container_candidate", "unknown", "confirmed_visible")
CONTAINER_STATES = (
    "none",
    "container_open_candidate",
    "container_closed_candidate",
    "object_inside_candidate",
    "object_inside_confirmed",
)
CANDIDATE_LOCATION_TYPES = ("direct_location", "container_candidate", "unknown")
EVENT_TYPES = (
    "object_seen",
    "object_picked",
    "object_carried",
    "object_placed",
    "object_lost_visibility",
    "container_opened",
    "container_closed",
    "object_candidate_in_container",
    "user_confirmed_location",
    "user_denied_location",
)


@dataclass
class LedgerEvent:
    """账本事件（M1 扩展类型）。"""
    event_type: str  # one of EVENT_TYPES
    timestamp: Optional[float] = None
    summary: Optional[str] = None


@dataclass
class ObjectTemporalEntry:
    """单对象时空条目（M1.5：容器逻辑增强；最后可信与当前候选分离）。"""
    object_label: str
    object_profile_summary: Optional[str] = None
    # 最后可信位置（仅用户确认或强支持更新，不被弱候选覆盖）
    last_confirmed_location: Optional[str] = None
    last_confirmed_ts: Optional[float] = None
    # 当前候选位置（假设/推断，不写回 last_confirmed）
    current_candidate_location: Optional[str] = None
    current_candidate_ts: Optional[float] = None
    # 兼容 M0
    last_seen_ts: Optional[float] = None
    visibility_status: str = "unknown"
    current_container_candidate: Optional[str] = None
    current_container_confidence: float = 0.0
    container_state: str = "none"  # one of CONTAINER_STATES
    container_last_event_ts: Optional[float] = None
    candidate_location_type: str = "unknown"  # one of CANDIDATE_LOCATION_TYPES
    current_hypothesis_summary: Optional[str] = None
    ledger_confidence: float = 0.0
    # 用户确认写回（M1）
    user_confirmed_location: Optional[str] = None
    user_confirmed_ts: Optional[float] = None


@dataclass
class ObjectTemporalLedger:
    """对象时空账本：单对象条目 + 事件链 + 状态摘要（M1）。"""
    focus_object_entry: Optional[ObjectTemporalEntry] = None
    events: List[LedgerEvent] = field(default_factory=list)
    ledger_reason: Optional[str] = None
    ledger_state_summary: Optional[str] = None  # M1：可读状态摘要


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _location_from_smap(smap: Optional[LocalGoalSpatialMap]) -> Optional[str]:
    """从 smap 取位置摘要（focus/confirm 区域 sector+band）。"""
    if not smap:
        return None
    focus = getattr(smap, "focus_region", None) or []
    confirm = getattr(smap, "confirm_region", None) or []
    for r in (focus[:1] + confirm[:1]):
        sector = getattr(r, "sector", None) or "—"
        band = getattr(r, "distance_band", None) or "—"
        return f"{sector}/{band}"
    return None


def build_object_temporal_ledger(
    focus_object_label: Optional[str],
    smap: Optional[LocalGoalSpatialMap],
    ledger: Optional[EvidenceLedger],
    hypothesis_layer: Optional[HypothesisLayer],
    recheck_planner: Optional[RecheckPlannerResult],
    pools: Optional[SpatialMemoryPools],
    current_ts: float,
    prev_last_confirmed_location: Optional[str] = None,
    prev_last_confirmed_ts: Optional[float] = None,
    prev_container_candidate: Optional[str] = None,
    prev_container_confidence: Optional[float] = None,
    prev_container_state: Optional[str] = None,
    prev_container_last_event_ts: Optional[float] = None,
    prev_visibility_status: Optional[str] = None,
    object_user_confirmed_location: Optional[str] = None,
    object_user_denied_location: Optional[str] = None,
) -> ObjectTemporalLedger:
    """
    M1.5：在 M1 基础上增强最小容器逻辑：
    - 容器状态表达（container_state / container_last_event_ts）
    - 对象进入容器候选规则与置信度更新
    - 用户否认后的容器候选回退
    - 最后可信位置与容器候选位置叙事一致（last_confirmed 不被容器候选覆盖）
    """
    label = (focus_object_label or "").strip() or "current_focus"
    events: List[LedgerEvent] = []
    reason_parts: List[str] = []

    location_from_smap = _location_from_smap(smap)
    working_n = len(getattr(pools, "working_memory_items", None) or [])

    # 从 hypothesis 推 visibility、容器候选、候选位置（容器状态从上一帧延续）
    visibility = "unknown"
    container_candidate: Optional[str] = prev_container_candidate
    container_confidence = float(prev_container_confidence or 0.0)
    container_state = (prev_container_state or "none") if (prev_container_state in CONTAINER_STATES) else "none"
    container_last_event_ts: Optional[float] = prev_container_last_event_ts
    hypothesis_summary: Optional[str] = None
    candidate_location: Optional[str] = None
    candidate_ts: Optional[float] = None
    candidate_location_type: str = "unknown"

    if hypothesis_layer and getattr(hypothesis_layer, "hypotheses", None):
        first_h = hypothesis_layer.hypotheses[0]
        hyp_type = _get(first_h, "hypothesis_type")
        hypothesis_summary = _get(first_h, "hypothesis_summary")
        if hyp_type == "occluded_object_candidate":
            visibility = "lost" if (working_n == 0 and not location_from_smap) else "occluded"
            events.append(LedgerEvent("object_lost_visibility", current_ts, hypothesis_summary))
        elif hyp_type == "container_candidate":
            visibility = "container_candidate"
            if hypothesis_summary:
                container_candidate = hypothesis_summary
            base_conf = getattr(first_h, "hypothesis_confidence", 0.3) or 0.3
            container_confidence = min(1.0, max(container_confidence, base_conf))
            candidate_location = container_candidate or (f"container:{hypothesis_summary[:40]}" if hypothesis_summary else "container")
            candidate_ts = current_ts
            candidate_location_type = "container_candidate"
            events.append(LedgerEvent("object_candidate_in_container", current_ts, hypothesis_summary))
            # 弱规则：出现容器候选 => 容器打开候选
            if container_state in ("none", "container_closed_candidate"):
                container_state = "container_open_candidate"
                container_last_event_ts = current_ts
                events.append(LedgerEvent("container_opened", current_ts, "container_open_candidate"))
            # 容器候选优先：进入“对象在容器内候选”
            container_state = "object_inside_candidate"
            container_last_event_ts = current_ts
        elif hyp_type == "path_continuation_candidate":
            visibility = "visible" if (location_from_smap and working_n > 0) else "unknown"
            candidate_location = location_from_smap
            candidate_ts = current_ts if location_from_smap else None
            candidate_location_type = "direct_location" if candidate_location else "unknown"
            events.append(LedgerEvent("object_seen", current_ts, candidate_location or "path_continuation"))
        elif hyp_type == "interaction_target_candidate":
            visibility = "visible"
            candidate_location = location_from_smap or "interaction_target"
            candidate_ts = current_ts
            candidate_location_type = "direct_location" if (candidate_location and candidate_location != "interaction_target") else "unknown"
            events.append(LedgerEvent("object_seen", current_ts, candidate_location))
        else:
            candidate_location = location_from_smap
            candidate_ts = current_ts if location_from_smap else None
            candidate_location_type = "direct_location" if candidate_location else "unknown"
            events.append(LedgerEvent("object_seen", current_ts, candidate_location or "unknown"))

    if not events:
        candidate_location = location_from_smap
        candidate_ts = current_ts if location_from_smap else None
        candidate_location_type = "direct_location" if candidate_location else "unknown"
        events.append(LedgerEvent("object_seen", current_ts, candidate_location or "no_hypothesis"))

    # 用户确认写回：更新 last_confirmed_*，追加事件
    last_confirmed_location: Optional[str] = prev_last_confirmed_location
    last_confirmed_ts: Optional[float] = prev_last_confirmed_ts
    user_confirmed_location: Optional[str] = None
    user_confirmed_ts: Optional[float] = None

    if object_user_confirmed_location:
        last_confirmed_location = object_user_confirmed_location
        last_confirmed_ts = current_ts
        user_confirmed_location = object_user_confirmed_location
        user_confirmed_ts = current_ts
        visibility = "confirmed_visible" if visibility == "unknown" else visibility
        events.append(LedgerEvent("user_confirmed_location", current_ts, object_user_confirmed_location))
        # 用户确认增强：若确认指向“容器型位置”，提升容器候选并可进入 inside_confirmed（允许占位）
        if any(k in object_user_confirmed_location for k in ("抽屉", "柜", "盒", "包", "口袋", "箱")):
            container_candidate = object_user_confirmed_location
            container_confidence = min(1.0, max(container_confidence, 0.8))
            candidate_location = container_candidate
            candidate_ts = current_ts
            candidate_location_type = "container_candidate"
            container_state = "object_inside_confirmed"
            container_last_event_ts = current_ts

    # 用户否认写回：与候选/容器冲突时降权或清空候选
    if object_user_denied_location:
        events.append(LedgerEvent("user_denied_location", current_ts, object_user_denied_location))
        conflict_with_candidate = object_user_denied_location == candidate_location
        conflict_with_container = bool(container_candidate and (object_user_denied_location == container_candidate or object_user_denied_location in container_candidate))
        if conflict_with_candidate or conflict_with_container:
            # 最小回退：降低置信度/清空候选，并回退容器状态
            container_confidence = max(0.0, container_confidence - 0.4)
            if container_confidence <= 0.15:
                container_candidate = None
                container_confidence = 0.0
            if container_state == "object_inside_candidate":
                container_state = "container_closed_candidate" if (prev_container_state in ("container_open_candidate", "object_inside_candidate")) else "none"
                container_last_event_ts = current_ts
            if conflict_with_candidate:
                candidate_location = None
                candidate_ts = None
                candidate_location_type = "unknown"
            if conflict_with_container and candidate_location_type == "container_candidate":
                candidate_location = None
                candidate_ts = None
                candidate_location_type = "unknown"

    # 弱规则：若已 container_open_candidate 且对象持续不可见 / recheck 后仍未在外部看到，则生成 container_closed_candidate
    if container_candidate and container_state in ("container_open_candidate", "object_inside_candidate"):
        still_not_visible = visibility in ("lost", "occluded", "container_candidate")
        rechecked = bool(recheck_planner and getattr(recheck_planner, "recheck_applied", None) is True)
        if still_not_visible and rechecked and container_state != "container_closed_candidate":
            container_state = "container_closed_candidate"
            container_last_event_ts = current_ts
            events.append(LedgerEvent("container_closed", current_ts, "container_closed_candidate"))

    # 无用户确认时：last_confirmed 沿用上一帧；仅当无 prev 且当前强支持（visible + location）时用 smap 位置作为首帧确认
    if last_confirmed_location is None and not object_user_confirmed_location:
        if visibility == "visible" and location_from_smap and working_n > 0:
            last_confirmed_location = location_from_smap
            last_confirmed_ts = current_ts

    # 置信度
    conf = 0.3
    if ledger and getattr(ledger, "entries", None):
        conf = max(conf, getattr(ledger.entries[0], "evidence_confidence", 0) or 0)
    if hypothesis_layer and getattr(hypothesis_layer, "hypotheses", None):
        conf = max(conf, getattr(hypothesis_layer.hypotheses[0], "hypothesis_confidence", 0) or 0)

    reason_parts.append(f"label={label} visibility={visibility}")
    if recheck_planner and getattr(recheck_planner, "recheck_action", None):
        reason_parts.append(f"recheck={recheck_planner.recheck_action}")

    # 候选位置类型：容器候选优先（lost/occluded 时，container_candidate 让位于普通弱位置候选）
    if container_candidate and visibility in ("lost", "occluded", "container_candidate"):
        if candidate_location_type != "container_candidate":
            candidate_location = container_candidate
            candidate_ts = current_ts if candidate_ts is None else candidate_ts
            candidate_location_type = "container_candidate"

    # 若仍未知，按 location_from_smap 兜底
    if candidate_location_type == "unknown" and candidate_location:
        candidate_location_type = "container_candidate" if candidate_location.startswith("container:") else "direct_location"

    # 状态摘要：最后可信 | 当前候选 | 候选类型 | 容器状态 | 可见性 | 事实已确认/候选中
    if last_confirmed_location:
        state_kind = "事实已确认"
    else:
        state_kind = "候选中"
    conf_band = "低"
    if container_confidence >= 0.75:
        conf_band = "高"
    elif container_confidence >= 0.4:
        conf_band = "中"
    state_summary = (
        f"最后可信: {last_confirmed_location or '—'}"
        f" | 候选: {candidate_location or '—'}"
        f" | 候选类型: {candidate_location_type}"
        f" | 容器状态: {container_state}"
        f" | 可见性: {visibility}"
        f" | 状态: {state_kind}"
    )
    if container_candidate:
        state_summary += f" | 容器候选: {container_candidate[:24]}({conf_band})"

    entry = ObjectTemporalEntry(
        object_label=label,
        object_profile_summary=(
            f"last_confirmed={last_confirmed_location or '—'} "
            f"candidate={candidate_location or '—'}({candidate_location_type}) "
            f"container={container_candidate or '—'}({container_state}) "
            f"working={working_n}"
        ),
        last_confirmed_location=last_confirmed_location,
        last_confirmed_ts=last_confirmed_ts,
        current_candidate_location=candidate_location,
        current_candidate_ts=candidate_ts,
        last_seen_ts=current_ts if (location_from_smap or working_n > 0) else None,
        visibility_status=visibility,
        current_container_candidate=container_candidate,
        current_container_confidence=container_confidence,
        container_state=container_state,
        container_last_event_ts=container_last_event_ts,
        candidate_location_type=candidate_location_type,
        current_hypothesis_summary=hypothesis_summary,
        ledger_confidence=min(1.0, conf),
        user_confirmed_location=user_confirmed_location,
        user_confirmed_ts=user_confirmed_ts,
    )

    return ObjectTemporalLedger(
        focus_object_entry=entry,
        events=events[-8:],  # M1：最多保留 8 条
        ledger_reason="; ".join(reason_parts),
        ledger_state_summary=state_summary,
    )
