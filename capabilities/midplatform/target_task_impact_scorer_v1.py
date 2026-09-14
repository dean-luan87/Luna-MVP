# -*- coding: utf-8 -*-
"""Target task impact scorer v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from capabilities.midplatform.static_dynamic_target_locking_tracking_planning_items_v1 import (
    DYNAMIC_TARGET_LABELS,
    STATIC_TARGET_LABELS,
    TASK_IMPACT_HINT_POLICY,
)

P0_LABELS = set(TASK_IMPACT_HINT_POLICY["priorities"]["P0"]) | {"moving_obstacle"}
P1_LABELS = set(TASK_IMPACT_HINT_POLICY["priorities"]["P1"])
P2_LABELS = set(TASK_IMPACT_HINT_POLICY["priorities"]["P2"])


def score_target_task_impact(
    *,
    target_ref: str,
    label: str,
    field_zone: str = "unknown",
    visibility_status: str = "visible",
    motion_status: str = "unknown",
    risk_hint: Optional[str] = None,
    task_relevance_hint: Optional[str] = None,
) -> Dict[str, Any]:
    hint_map = TASK_IMPACT_HINT_POLICY.get("label_to_hint") or {}
    extra = {"shelf": "find_object_relevant", "table": "background_only", "chair": "background_only"}
    hint = task_relevance_hint or extra.get(label) or hint_map.get(label, "unknown")
    if label in P0_LABELS or field_zone == "inner_zone" and label == "obstacle":
        priority = "P0"
        safety = True
        task_rel = label in P1_LABELS
    elif label in P1_LABELS:
        priority = "P1"
        safety = False
        task_rel = True
    elif label in P2_LABELS:
        priority = "P2"
        safety = False
        task_rel = False
    else:
        priority = "P3"
        safety = False
        task_rel = False
    if risk_hint == "near_collision":
        priority, safety, hint = "P0", True, "route_blocker_candidate"
    if label == "vehicle":
        hint = "road_crossing_relevant"
    return {
        "impact_candidate_id": f"tic_{uuid.uuid4().hex[:12]}",
        "target_ref": target_ref,
        "label": label,
        "priority_level": priority,
        "task_impact_hint": hint,
        "safety_relevant": safety,
        "task_relevant": task_rel,
        "background_only": priority == "P3",
        "reason_codes": [f"priority_{priority}", f"hint_{hint}"],
        "candidate_only": True,
    }


def is_static_label(label: str) -> bool:
    return label in STATIC_TARGET_LABELS


def is_dynamic_label(label: str) -> bool:
    return label in DYNAMIC_TARGET_LABELS
