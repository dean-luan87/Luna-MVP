# -*- coding: utf-8 -*-
"""Tracking / Optical Flow adapter result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.tracking_opticalflow_adapter_types_v1 import NON_EXECUTION_FLAGS


def assemble_tracking_opticalflow_adapter_result(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    tracks: List[Dict[str, Any]],
    persistences: List[Dict[str, Any]],
    motions: List[Dict[str, Any]],
    qualities: List[Dict[str, Any]],
    warnings: List[str],
    failure_points: List[str],
) -> Dict[str, Any]:
    """Assemble TrackingOpticalFlowAdapterResultCandidate."""
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    accepted = len(tracks) + len(persistences) + len(motions) + len(qualities)
    rejected = len(failure_points)

    has_tracking_evidence = bool(tracks or motions)
    has_persistence = bool(persistences)
    later_wm_ready = (has_tracking_evidence or has_persistence) and not raw_output.get("_blocked")
    task_ready = later_wm_ready and execution_mode not in (
        "blocked_by_authorization", "blocked_by_missing_dependency", "blocked_by_missing_weight",
    )

    flags = dict(NON_EXECUTION_FLAGS)
    if execution_mode == "cached_output":
        flags["cached_output_not_marked_as_real_run"] = True
    if execution_mode == "adapter_stub":
        flags["adapter_stub_not_marked_as_real_run"] = True

    return {
        "adapter_result_id": f"toar_{uuid.uuid4().hex[:12]}",
        "adapter_input_ref": adapter_input.get("adapter_input_id"),
        "smoke_run_ref": adapter_input.get("smoke_run_ref"),
        "io_inspection_ref": adapter_input.get("io_inspection_ref"),
        "execution_mode": execution_mode,
        "object_track_candidates": tracks,
        "object_persistence_candidates": persistences,
        "motion_candidates": motions,
        "tracking_quality_candidates": qualities,
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
            t.get("object_track_candidate_id") for t in tracks
        ] + [p.get("object_persistence_candidate_id") for p in persistences],
        "candidate_only": True,
        "world_model_candidate_generated": False,
        "world_model_entry_created": False,
        "world_entity_candidate_generated": False,
        "fact_admission_executed": False,
        "task_action_output": False,
        "navigation_suggestion_output": False,
    }
