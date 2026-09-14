# -*- coding: utf-8 -*-
"""MobileSAM runner output → model_test_result_envelope_v1."""

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


def build_mobilesam_envelope(
    *,
    job: Dict[str, Any],
    runner_result: Dict[str, Any],
    test_board_refs: List[str],
) -> Dict[str, Any]:
    asset_manifest = job.get("asset_manifest") or {}
    metrics = dict(runner_result.get("metrics") or {})
    prompt_results = runner_result.get("prompt_results") or []
    per_cat = {}
    for pr in prompt_results:
        if pr.get("success"):
            label = pr.get("prompt_target_label", pr.get("prompt_id", "unknown"))
            per_cat[label] = pr.get("score", 0.0)
    if per_cat:
        metrics["per_category_average_score"] = per_cat

    viz_layers = []
    for out in runner_result.get("candidate_outputs") or []:
        if out.get("mask_ref"):
            viz_layers.append({
                "layer_id": out.get("output_id", "mask"),
                "layer_type": "mask",
                "source_artifact_ref": out["mask_ref"],
                "display_name": out.get("display_task_semantic") or out.get("output_id", "candidate_mask"),
                "label": out.get("output_id", "candidate_mask"),
                "source_prompt_hint": out.get("source_prompt_hint"),
                "display_task_semantic": out.get("display_task_semantic"),
                "prompt_is_not_fact": True,
                "ocr_route_candidate": bool(out.get("ocr_route_candidate")),
                "model_id": "mobile_sam",
                "candidate_only": True,
                "opacity": 0.55,
            })

    scene_profile = runner_result.get("scene_profile_candidate")
    prompt_policy = runner_result.get("segmentation_prompt_policy")

    status = runner_result.get("status")
    failure_modes: List[str] = []
    if status != "completed":
        failure_modes.append(runner_result.get("status_reason", "runner_failed"))

    return {
        "envelope_id": f"mobilesam_runner_envelope_{job['job_id']}_{uuid4().hex[:8]}",
        "phase_ref": PHASE_ID,
        "job_ref": job["job_id"],
        "test_case_id": f"mobilesam_local_runner_{job['job_id']}",
        "model_id": job.get("requested_model_id", "mobile_sam"),
        "model_category": "segmentation",
        "model_version_or_registry_ref": (
            "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
        ),
        "input_asset_refs": [asset_manifest.get("local_path", asset_manifest.get("manifest_id", ""))],
        "candidate_outputs": runner_result.get("candidate_outputs") or [],
        "visualization_layers": viz_layers,
        "scene_profile_candidate": scene_profile,
        "segmentation_prompt_policy": prompt_policy,
        "metrics": metrics,
        "failure_modes": failure_modes,
        "quality_summary": {
            "human_review_required": True,
            "suitable_for_runtime_admission": False,
            "suitable_for_quality_observation": status == "completed",
            "not_semantic_fact": True,
            "aggregate_note": runner_result.get("status_reason", ""),
            "candidate_only": True,
        },
        "test_board_refs": test_board_refs,
        "protected_artifact_refs": [],
        "boundary_flags": boundary_flags(),
        "readiness_effect": readiness_effect(),
        "runner_status": status,
        "adapter_id": "mobilesam_runner_to_envelope_adapter_v1",
    }
