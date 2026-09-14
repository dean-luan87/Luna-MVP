# -*- coding: utf-8 -*-
"""SLAM spatial mapping candidate mapping reviewer v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.slam_spatial_mapping_model_smoke_io_inspection_items_v1 import (
    CANDIDATE_MAPPING_TARGETS,
)


def review_slam_candidate_mapping_feasibility(
    *,
    smoke_run: Dict[str, Any],
    io_inspection: Dict[str, Any],
    focus_target: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Review how model outputs map to existing candidate definitions."""
    raw = smoke_run.get("_raw_output") or {}
    mode = smoke_run.get("execution_mode", "blocked_by_authorization")
    results: List[Dict[str, Any]] = []

    targets = CANDIDATE_MAPPING_TARGETS
    if focus_target:
        targets = tuple(t for t in CANDIDATE_MAPPING_TARGETS if t["target"] == focus_target)

    for target in targets:
        mapping_status = "blocked"
        blockers: List[str] = []
        source_refs = list(io_inspection.get("output_sample_refs") or [])

        if mode.startswith("blocked"):
            blockers.append(mode)
        elif mode == "cached_output":
            outputs = raw.get("outputs") or {}
            key_map = {
                "CameraPoseCandidate": "pose",
                "CameraTrajectoryCandidate": "trajectory",
                "SpatialAnchorCandidate": None,
                "LocalMapCandidate": "local_map",
                "MapQualityCandidate": "quality",
            }
            out_key = key_map.get(target["target"])
            if out_key and outputs.get(out_key):
                mapping_status = target["status"]
            elif target["target"] == "SpatialAnchorCandidate":
                mapping_status = "feasible_with_entity_hints"
                blockers.append("requires_field_entity_anchor_hints")
            else:
                blockers.append("output_key_missing")
        elif mode == "adapter_stub":
            mapping_status = "feasible"
        elif mode == "local_real_model" and target["target"] == "CameraPoseCandidate":
            mapping_status = "feasible"
        else:
            blockers.append("insufficient_output_for_target")

        results.append({
            "mapping_feasibility_id": f"mcf_{uuid.uuid4().hex[:12]}",
            "model_role": "slam_spatial_mapping",
            "source_output_refs": source_refs,
            "reusable_existing_candidates": [
                "RealFrameInputPackage",
                "EnhancedFieldSceneCandidate",
                "FieldGeometryCandidate",
            ],
            "candidate_mapping_targets": [target["target"]],
            "mapping_status": mapping_status,
            "mapping_blockers": blockers,
            "reason_if_new_candidate_needed": None,
            "owner_approval_required_for_new_protocol": False,
            "candidate_only": True,
            "_model_output": target["model_output"],
        })
    return results
