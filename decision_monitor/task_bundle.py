# -*- coding: utf-8 -*-
"""
联合任务包 M0：Task Bundle（最小版）。

在 Task Arbitration M0 基础上，将 merge_into_bundle 从“可合并判断”推进为“真正存在的联合任务包结构”，
用于承载同环境、可共享骨架与感知的任务集合。不做正式执行器、不正式改 Task Chain。
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, List, Optional

from .task_arbitration import TaskArbitrationResult

BUNDLE_STATUSES = ("proposed", "active", "blocked", "closed")
BUNDLE_TASK_TYPES_ALLOWED = (
    "object_search",
    "recheck",
    "observation",
    "navigation",
    "interaction_confirm",
    "safety_guard",
)
MAX_BUNDLE_TASK_TYPES = 6


@dataclass
class TaskBundleResult:
    """联合任务包 M0：最小 bundle 结构（仅表达存在与摘要，不做执行图）。"""
    bundle_id: Optional[str] = None
    bundle_zone: Optional[str] = None
    bundle_task_types: List[str] = field(default_factory=list)
    bundle_dominant_skeleton: Optional[str] = None
    bundle_shared_focus: Optional[str] = None
    bundle_reason: Optional[str] = None
    bundle_status: str = "closed"  # one of BUNDLE_STATUSES
    bundle_created: bool = False
    bundle_applied: bool = False
    bundle_block_reason: Optional[str] = None


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _focus_summary_from_smap(smap: Any) -> Optional[str]:
    """从 local_goal_spatial_map 取 focus/confirm 区域摘要。"""
    if not smap:
        return None
    focus = _get(smap, "focus_region") or []
    confirm = _get(smap, "confirm_region") or []
    parts = []
    for r in (list(focus)[:1] + list(confirm)[:1]):
        sector = _get(r, "sector") or _get(r, "region_type")
        band = _get(r, "distance_band")
        if sector or band:
            parts.append(f"{sector or 'region'}/{band or '—'}")
    return " ".join(parts) if parts else None


def build_task_bundle(
    task_arbitration: Optional[TaskArbitrationResult],
    state: Any,
    skeleton_mix: Any,
    local_goal_spatial_map: Any,
    object_search_interaction: Any,
    recheck_planner: Any,
    object_temporal_ledger: Any,
    incoming_task_type: Optional[str] = None,
    incoming_task_zone: Optional[str] = None,
    frame_seq: Optional[int] = None,
) -> TaskBundleResult:
    """
    M0：仅当 arbitration_action == merge_into_bundle 时生成 bundle；
    否则 bundle_created=False，bundle_status=closed/proposed 占位。
    守底条件阻断时 bundle_applied=False，bundle_status=blocked。
    """
    # 阻断条件（与仲裁一致）
    minimum_mode = _get(state, "minimum_mode_active") is True
    runtime_domain = (_get(state, "runtime_domain_state") or "").strip()
    scene_gate = (_get(state, "scene_gate_action") or "").strip()
    high_level_suppressed = _get(state, "high_level_output_suppressed") is True
    human_check_pending = _get(state, "human_check_pending") is True

    is_blocked = (
        minimum_mode
        or runtime_domain == "frozen"
        or scene_gate == "freeze_to_minimum_mode"
        or high_level_suppressed
        or human_check_pending
    )
    block_reason = None
    if minimum_mode:
        block_reason = "minimum_mode_active"
    elif runtime_domain == "frozen":
        block_reason = "runtime_domain_state=frozen"
    elif scene_gate == "freeze_to_minimum_mode":
        block_reason = "scene_gate_action=freeze"
    elif high_level_suppressed:
        block_reason = "high_level_output_suppressed"
    elif human_check_pending:
        block_reason = "human_check_pending"

    arb_action = _get(task_arbitration, "arbitration_action") or "continue_current"
    merge_requested = arb_action == "merge_into_bundle"

    if not merge_requested or is_blocked:
        return TaskBundleResult(
            bundle_id=None,
            bundle_zone=None,
            bundle_task_types=[],
            bundle_dominant_skeleton=None,
            bundle_shared_focus=None,
            bundle_reason="未触发合并" if not merge_requested else f"阻断:{block_reason}",
            bundle_status="blocked" if is_blocked and merge_requested else "closed",
            bundle_created=False,
            bundle_applied=False,
            bundle_block_reason=block_reason if is_blocked else None,
        )

    # --------- 生成 bundle ---------
    seq = frame_seq if frame_seq is not None else int(time.time() * 1000) % 100000
    bundle_id = f"bundle_{seq}"

    # 任务类型：foreground + incoming + 候选，去重，最多 MAX_BUNDLE_TASK_TYPES
    foreground = _get(task_arbitration, "foreground_task_type")
    candidates = list(_get(task_arbitration, "candidate_task_types") or [])
    types_set = []
    for t in ([foreground] if foreground else []) + ([incoming_task_type] if incoming_task_type else []) + candidates:
        t = (t or "").strip()
        if t and t in BUNDLE_TASK_TYPES_ALLOWED and t not in types_set:
            types_set.append(t)
    bundle_task_types = types_set[:MAX_BUNDLE_TASK_TYPES]

    # 主导骨架：优先 skeleton_mix.dominant_skeleton
    bundle_dominant_skeleton = _get(skeleton_mix, "dominant_skeleton")

    # 共享焦点：smap focus / suggested_search_zone / current_candidate / container / incoming_task_zone
    focus_parts = []
    smap_focus = _focus_summary_from_smap(local_goal_spatial_map)
    if smap_focus:
        focus_parts.append(smap_focus)
    if object_search_interaction:
        zone = _get(object_search_interaction, "suggested_search_zone")
        if zone:
            focus_parts.append(zone)
    entry = None
    if object_temporal_ledger and _get(object_temporal_ledger, "focus_object_entry"):
        entry = object_temporal_ledger.focus_object_entry
    if entry:
        cand = _get(entry, "current_candidate_location")
        if cand:
            focus_parts.append(cand)
        cont = _get(entry, "current_container_candidate")
        if cont:
            focus_parts.append(f"容器:{cont[:24]}")
    if incoming_task_zone:
        focus_parts.append(incoming_task_zone)
    bundle_shared_focus = " / ".join(focus_parts) if focus_parts else None

    # zone：与 shared_focus 一致或取其一
    bundle_zone = incoming_task_zone or _get(object_search_interaction, "suggested_search_zone") if object_search_interaction else None
    if not bundle_zone and bundle_shared_focus:
        bundle_zone = bundle_shared_focus[:60]

    # 合并原因
    reason_parts = ["同环境任务合并"]
    if bundle_shared_focus:
        if "容器" in (bundle_shared_focus or ""):
            reason_parts.append("共享容器候选")
        elif object_search_interaction and _get(object_search_interaction, "suggested_search_zone"):
            reason_parts.append("共享搜索区域")
        if recheck_planner and _get(recheck_planner, "recheck_action"):
            reason_parts.append("共享近场复核")
        if smap_focus:
            reason_parts.append("共享路径/锚点")
    bundle_reason = "；".join(reason_parts)

    return TaskBundleResult(
        bundle_id=bundle_id,
        bundle_zone=bundle_zone,
        bundle_task_types=bundle_task_types,
        bundle_dominant_skeleton=bundle_dominant_skeleton,
        bundle_shared_focus=bundle_shared_focus,
        bundle_reason=bundle_reason,
        bundle_status="active",
        bundle_created=True,
        bundle_applied=True,
        bundle_block_reason=None,
    )
