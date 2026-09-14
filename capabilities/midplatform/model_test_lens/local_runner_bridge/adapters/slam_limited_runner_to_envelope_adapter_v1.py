# -*- coding: utf-8 -*-
"""SLAM limited runner output → model_test_result_envelope_v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_skeleton_execution_types_v1 import (
    PHASE_ID,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_storage_v1 import (
    boundary_flags,
    readiness_effect,
)


def build_slam_limited_envelope(
    *,
    job: Dict[str, Any],
    runner_result: Dict[str, Any],
    test_board_refs: List[str],
) -> Dict[str, Any]:
    asset_manifest = job.get("asset_manifest") or {}
    return {
        "envelope_id": f"slam_limited_envelope_{job['job_id']}_{uuid4().hex[:8]}",
        "phase_ref": PHASE_ID,
        "job_ref": job["job_id"],
        "test_case_id": f"slam_limited_{job['job_id']}",
        "model_id": job.get("requested_model_id", "orb_slam_or_vins_placeholder"),
        "model_category": "slam_vio",
        "input_asset_refs": [asset_manifest.get("local_path", asset_manifest.get("manifest_id", ""))],
        "candidate_outputs": [],
        "visualization_layers": [],
        "metrics": {
            "slam": {
                "limited_mode": True,
                "no_gt_limited_mode": True,
                "no_ate": True,
                "not_comparable_to_gt_benchmark": True,
                "runner_note": runner_result.get("runner_note"),
            }
        },
        "failure_modes": ["slam_backend_not_connected"],
        "quality_summary": {
            "human_review_required": True,
            "suitable_for_runtime_admission": False,
            "not_semantic_fact": True,
            "aggregate_note": runner_result.get("message", ""),
            "limited_mode": True,
        },
        "test_board_refs": test_board_refs,
        "boundary_flags": boundary_flags(),
        "readiness_effect": readiness_effect(),
        "limited_mode": True,
        "no_gt_limited_mode": True,
        "no_ate": True,
        "not_comparable_to_gt_benchmark": True,
        "runner_note": runner_result.get("runner_note"),
        "adapter_id": "slam_limited_runner_to_envelope_adapter_v1",
        "diagnostics": runner_result.get("diagnostics") or {},
    }
