# -*- coding: utf-8 -*-
"""Risk projection builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List


def build_risk_projection_candidates(
    *,
    task_impacts: List[Dict[str, Any]],
    trajectories: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    risks: List[Dict[str, Any]] = []
    traj_by_id = {t.get("trajectory_candidate_id"): t for t in trajectories}
    for impact in task_impacts:
        impact_type = impact.get("task_impact_type", "unknown")
        if impact_type in ("background_only", "unknown", "static_anchor_relevant"):
            continue
        traj = traj_by_id.get(impact.get("trajectory_ref")) if impact.get("trajectory_ref") else None
        motion = impact.get("motion_pattern") or (traj.get("motion_pattern") if traj else None)
        if impact_type == "safety_risk":
            risk_type, risk_level = "collision_candidate", "high"
        elif impact_type == "crossing_risk":
            risk_type, risk_level = "crossing_risk", "high"
        elif impact_type == "route_blocker":
            risk_type, risk_level = "navigation_risk", "medium"
        elif impact_type == "reading_blocker":
            risk_type, risk_level = "navigation_risk", "medium"
        else:
            risk_type, risk_level = impact_type, "medium"
        affects_path = motion in (
            "approaching_user", "crossing_user_path_candidate", "blocking_route_candidate", "entering_risk_zone",
        ) or impact_type in ("route_blocker", "crossing_risk", "collision_candidate")
        risks.append({
            "risk_projection_id": f"rp_{uuid.uuid4().hex[:12]}",
            "target_ref": impact.get("target_ref"),
            "trajectory_ref": impact.get("trajectory_ref"),
            "risk_type": risk_type,
            "risk_level": risk_level,
            "time_horizon_hint": "short_term",
            "risk_zone_hint": impact.get("field_zone", "unknown"),
            "affects_user_path_candidate": affects_path,
            "requires_recheck": risk_level == "high",
            "reason_codes": [f"risk_from_{impact_type}"],
            "candidate_only": True,
        })
    return risks
