# -*- coding: utf-8 -*-
"""Spatial mapping adapter result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.slam_spatial_mapping_adapter_types_v1 import NON_EXECUTION_FLAGS


def assemble_spatial_mapping_adapter_result(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    poses: List[Dict[str, Any]],
    trajectories: List[Dict[str, Any]],
    anchors: List[Dict[str, Any]],
    local_maps: List[Dict[str, Any]],
    map_qualities: List[Dict[str, Any]],
    warnings: List[str],
    failure_points: List[str],
) -> Dict[str, Any]:
    """Assemble SpatialMappingAdapterResultCandidate."""
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    accepted = len(poses) + len(trajectories) + len(anchors) + len(local_maps) + len(map_qualities)
    rejected = len(failure_points)

    later_wm_ready = bool(poses and local_maps and (anchors or trajectories)) and not raw_output.get("_blocked")
    task_ready = later_wm_ready and execution_mode not in ("blocked_by_authorization", "blocked_by_missing_dependency", "blocked_by_missing_weight")

    flags = dict(NON_EXECUTION_FLAGS)
    if execution_mode == "cached_output":
        flags["cached_output_not_marked_as_real_run"] = True
    if execution_mode == "adapter_stub":
        flags["adapter_stub_not_marked_as_real_run"] = True

    return {
        "adapter_result_id": f"smar_{uuid.uuid4().hex[:12]}",
        "adapter_input_ref": adapter_input.get("adapter_input_id"),
        "smoke_run_ref": adapter_input.get("smoke_run_ref"),
        "io_inspection_ref": adapter_input.get("io_inspection_ref"),
        "execution_mode": execution_mode,
        "camera_pose_candidates": poses,
        "camera_trajectory_candidates": trajectories,
        "spatial_anchor_candidates": anchors,
        "local_map_candidates": local_maps,
        "map_quality_candidates": map_qualities,
        "accepted_output_count": accepted,
        "rejected_output_count": rejected,
        "missing_information": [w for w in warnings if "missing" in w or "blocked" in w],
        "warning_summary": {"warnings": sorted(set(warnings))},
        "conflict_summary": [],
        "readiness_for_midplatform_task_collaboration": task_ready,
        "readiness_for_later_world_model_candidate_assembly": later_wm_ready,
        "non_execution_flags": flags,
        "source_refs": list(adapter_input.get("source_refs") or []),
        "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [
            p.get("camera_pose_candidate_id") for p in poses
        ] + [m.get("local_map_candidate_id") for m in local_maps],
        "candidate_only": True,
        "world_model_candidate_generated": False,
        "world_model_entry_created": False,
        "fact_admission_executed": False,
    }
