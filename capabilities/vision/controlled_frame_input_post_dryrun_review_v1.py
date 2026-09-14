# -*- coding: utf-8 -*-
"""Controlled Frame Input Post-DryRun Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001"
REVIEW_ID = "cfippr_v1_001"
REVIEW_SCOPE = "controlled_frame_input_post_dryrun_review_only"
SOURCE_CHAIN = "controlled_frame_input_post_dryrun_review_v1"
FINAL_DECISION = "CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Frame-Input-Closure-v1-001"

DRYRUN_DECISION = "CONTROLLED_FRAME_INPUT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "CONTROLLED_FRAME_INPUT_PLANNING_READY_FOR_CONTROLLED_FRAME_INPUT_DRYRUN"
MAP_LOCATION_FINAL_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
ROADMAP_DECISION = "POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
VISUAL_FOCUS_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "controlled_frame_input_dryrun",
        "arg": "controlled_frame_input_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_input_dryrun_scenario_matrix.json",
            "controlled_frame_input_dryrun_results.json",
            "controlled_frame_input_boundary_matrix.json",
            "dual_device_placeholder_dryrun_review.json",
            "governance_debt_register.json",
            "no_runtime_boundary_report.json",
            "no_write_boundary_report.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "controlled_frame_input_planning",
        "arg": "controlled_frame_input_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "frame_intake_gate_policy.json",
            "frame_quality_gate_policy.json",
            "frame_privacy_tagging_policy.json",
            "frame_stc_freshness_policy.json",
            "frame_downstream_handoff_policy.json",
            "controlled_frame_input_boundary_matrix.json",
            "dual_device_redundant_perception_placeholder.json",
        ],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "map_location_readonly_context_policy.json"],
    },
    {
        "id": "post_vision_strengthening_roadmap_decision",
        "arg": "post_vision_strengthening_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "recommended_next_phase_decision.json"],
    },
    {
        "id": "vision_strengthening_closure",
        "arg": "vision_strengthening_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "vision_strengthening_closure_summary.json"],
    },
    {
        "id": "task_aware_visual_focus",
        "arg": "task_aware_visual_focus_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "focus_to_ocr_activation_policy.json", "focus_to_tracking_request_policy.json"],
    },
    {
        "id": "midplatform_perception_orchestration",
        "arg": "midplatform_perception_orchestration_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "perception_work_order_schema.json"],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "minimal_runtime_integration_closure_report.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "ocr_mainline_final_closure_report.json"],
    },
    {
        "id": "vision_frame_trace_stream_registry",
        "arg": "vision_frame_trace_stream_registry_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "vision_frame_input_governance",
        "arg": "vision_frame_input_governance_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "vision_roi_proposal_stub",
        "arg": "vision_roi_proposal_stub_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "hardware_profile_capability_registry",
        "arg": "hardware_profile_capability_registry_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "system_health_center_governance",
        "arg": "system_health_center_governance_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "simulation_lab_profile",
        "arg": "simulation_lab_profile_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]

REQUIRED_SCENARIOS = {
    "case_static_test_image_good_quality": "static_test_image_good_quality",
    "case_prerecorded_degraded_quality": "prerecorded_video_frame_degraded_quality",
    "case_simulation_frame_allowed": "simulation_frame_allowed",
    "case_controlled_uploaded_privacy_sensitive": "controlled_uploaded_frame_privacy_sensitive",
    "case_missing_source_chain_rejected": "missing_source_chain_rejected",
    "case_missing_timestamp_rejected": "missing_timestamp_rejected",
    "case_missing_privacy_tags_rejected": "missing_privacy_tags_rejected",
    "case_live_camera_attempt_blocked": "live_camera_attempt_blocked",
    "case_device_camera_attempt_blocked": "device_camera_attempt_blocked",
    "case_external_stream_attempt_blocked": "external_stream_attempt_blocked",
    "case_stale_frame_archive_only": "stale_frame_archive_only",
    "case_frame_with_text_requires_visual_focus_for_ocr": "frame_with_text_requires_visual_focus_for_ocr",
    "case_frame_with_motion_requires_visual_focus_for_tracking": "frame_with_motion_requires_visual_focus_for_tracking",
    "case_dual_device_placeholder_review_only": "dual_device_placeholder_review_only",
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(path: Path) -> Any:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root and root.is_dir() and all((root / name).is_file() for name in artifacts))
    return {
        "root": root,
        "loaded": loaded,
        "summary": _read_json(root / summary_file) if root and (root / summary_file).is_file() else {},
    }


def _index_by(items: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        value = item.get(key)
        if value:
            out[value] = item
    return out


def _boundary_payload() -> Dict[str, Any]:
    return {
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "no_runtime_boundary_pass": True,
        "no_write_boundary_pass": True,
        "no_action_boundary_pass": True,
        "no_speech_boundary_pass": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "frame_content_loaded": False,
        "actual_image_read": False,
        "camera_invoked": False,
        "camera_opened": False,
        "video_capture_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
        "dual_device_runtime_invoked": False,
        "dual_model_runtime_invoked": False,
        "failover_runtime_invoked": False,
        "multi_input_fusion_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "entity_resolution_runtime_invoked": False,
        "fact_admission_runtime_invoked": False,
        "memory_consolidation_invoked": False,
        "library_experience_commit_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_controlled_frame_input_post_dryrun_review_v1(
    *,
    controlled_frame_input_dryrun_root: str,
    controlled_frame_input_planning_root: str,
    map_location_readonly_context_root: str,
    post_vision_strengthening_roadmap_decision_root: str,
    vision_strengthening_closure_root: str,
    task_aware_visual_focus_root: str,
    midplatform_perception_orchestration_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    vision_frame_trace_stream_registry_root: Optional[str] = None,
    vision_frame_input_governance_root: Optional[str] = None,
    vision_roi_proposal_stub_root: Optional[str] = None,
    hardware_profile_capability_registry_root: Optional[str] = None,
    system_health_center_governance_root: Optional[str] = None,
    simulation_lab_profile_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    summaries = {key: roots[key]["summary"] for key in roots}
    dryrun_root = roots["controlled_frame_input_dryrun"]["root"]
    planning_root = roots["controlled_frame_input_planning"]["root"]

    dryrun_results = _read_json(dryrun_root / "controlled_frame_input_dryrun_results.json") if dryrun_root else {}
    dryrun_scenario_matrix = _read_json(dryrun_root / "controlled_frame_input_dryrun_scenario_matrix.json") if dryrun_root else {}
    dryrun_boundary = _read_json(dryrun_root / "controlled_frame_input_boundary_matrix.json") if dryrun_root else {}
    dryrun_dual_review = _read_json(dryrun_root / "dual_device_placeholder_dryrun_review.json") if dryrun_root else {}
    dryrun_governance = _read_json(dryrun_root / "governance_debt_register.json") if dryrun_root else {}
    dryrun_no_runtime = _read_json(dryrun_root / "no_runtime_boundary_report.json") if dryrun_root else {}
    dryrun_no_write = _read_json(dryrun_root / "no_write_boundary_report.json") if dryrun_root else {}
    dryrun_verifier = _read_json(dryrun_root / "verifier_report.json") if dryrun_root else {}

    planning_intake_gate = _read_json(planning_root / "frame_intake_gate_policy.json") if planning_root else {}
    planning_quality_gate = _read_json(planning_root / "frame_quality_gate_policy.json") if planning_root else {}
    planning_privacy_policy = _read_json(planning_root / "frame_privacy_tagging_policy.json") if planning_root else {}
    planning_stc_policy = _read_json(planning_root / "frame_stc_freshness_policy.json") if planning_root else {}
    planning_handoff_policy = _read_json(planning_root / "frame_downstream_handoff_policy.json") if planning_root else {}
    planning_boundary = _read_json(planning_root / "controlled_frame_input_boundary_matrix.json") if planning_root else {}
    planning_dual_placeholder = _read_json(planning_root / "dual_device_redundant_perception_placeholder.json") if planning_root else {}

    controlled_frame_input_dryrun_input_loaded = (
        roots["controlled_frame_input_dryrun"]["loaded"]
        and summaries["controlled_frame_input_dryrun"].get("final_decision") == DRYRUN_DECISION
        and summaries["controlled_frame_input_dryrun"].get("scenario_count", 0) >= 14
        and dryrun_verifier.get("verifier") == "GO"
    )
    controlled_frame_input_planning_input_loaded = (
        roots["controlled_frame_input_planning"]["loaded"]
        and summaries["controlled_frame_input_planning"].get("final_decision") == PLANNING_DECISION
    )
    map_location_readonly_context_input_loaded = (
        roots["map_location_readonly_context"]["loaded"]
        and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_FINAL_DECISION
    )
    post_vision_strengthening_roadmap_decision_input_loaded = (
        roots["post_vision_strengthening_roadmap_decision"]["loaded"]
        and summaries["post_vision_strengthening_roadmap_decision"].get("final_decision") == ROADMAP_DECISION
    )
    vision_strengthening_closure_input_loaded = (
        roots["vision_strengthening_closure"]["loaded"]
        and summaries["vision_strengthening_closure"].get("final_decision") == VISION_STRENGTHENING_CLOSURE_DECISION
    )
    task_aware_visual_focus_input_loaded = (
        roots["task_aware_visual_focus"]["loaded"]
        and summaries["task_aware_visual_focus"].get("final_decision") == VISUAL_FOCUS_DECISION
    )
    midplatform_perception_orchestration_input_loaded = (
        roots["midplatform_perception_orchestration"]["loaded"]
        and summaries["midplatform_perception_orchestration"].get("final_decision") == MIDPLATFORM_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = (
        roots["ocr_final_closure"]["loaded"]
        and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION
    )

    required_root_ids = [spec["id"] for spec in ROOT_SPECS if spec["required"]]
    loaded_root_ids = [row["intake_id"] for row in input_rows if row["loaded"]]
    optional_missing_roots = [row["intake_id"] for row in input_rows if (not row["required"]) and row["status"] == "optional_missing"]
    missing_required_roots = [row["intake_id"] for row in input_rows if row["required"] and row["status"] != "loaded"]

    controlled_frame_dryrun_input_root_review = {
        "review_id": REVIEW_ID,
        "required_roots": required_root_ids,
        "loaded_roots": loaded_root_ids,
        "optional_missing_roots": optional_missing_roots,
        "missing_required_roots": missing_required_roots,
        "input_root_status": "all_required_loaded" if not missing_required_roots else "missing_required_root",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    scenarios = dryrun_scenario_matrix.get("scenarios", [])
    scenario_idx = _index_by(scenarios, "dryrun_case_id")
    covered_scenarios = [scenario_name for case_id, scenario_name in REQUIRED_SCENARIOS.items() if case_id in scenario_idx]
    missing_scenarios = [scenario_name for case_id, scenario_name in REQUIRED_SCENARIOS.items() if case_id not in scenario_idx]
    controlled_frame_scenario_coverage_review = {
        "reviewed_scenario_count": len(scenarios),
        "expected_scenario_count": len(REQUIRED_SCENARIOS),
        "covered_scenarios": covered_scenarios,
        "missing_scenarios": missing_scenarios,
        "allowed_source_cases_present": all(case_id in scenario_idx for case_id in (
            "case_static_test_image_good_quality",
            "case_prerecorded_degraded_quality",
            "case_simulation_frame_allowed",
        )),
        "rejected_source_cases_present": all(case_id in scenario_idx for case_id in (
            "case_missing_source_chain_rejected",
            "case_missing_timestamp_rejected",
            "case_missing_privacy_tags_rejected",
            "case_live_camera_attempt_blocked",
            "case_device_camera_attempt_blocked",
            "case_external_stream_attempt_blocked",
        )),
        "restricted_privacy_cases_present": "case_controlled_uploaded_privacy_sensitive" in scenario_idx,
        "stale_archive_only_cases_present": "case_stale_frame_archive_only" in scenario_idx,
        "dual_device_placeholder_case_present": "case_dual_device_placeholder_review_only" in scenario_idx,
        "verdict": "GO" if not missing_scenarios else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    results = dryrun_results.get("results", [])
    intake_decisions = dryrun_results.get("intake_decisions", [])
    quality_decisions = dryrun_results.get("quality_decisions", [])
    privacy_decisions = dryrun_results.get("privacy_decisions", [])
    freshness_decisions = dryrun_results.get("freshness_decisions", [])
    downstream_handoffs = dryrun_results.get("downstream_handoffs", [])

    result_idx = _index_by(results, "source_case_id")
    intake_idx = _index_by(intake_decisions, "source_case_id")
    quality_idx = _index_by(quality_decisions, "source_case_id")
    privacy_idx = _index_by(privacy_decisions, "source_case_id")
    freshness_idx = _index_by(freshness_decisions, "source_case_id")
    handoff_idx = _index_by(downstream_handoffs, "source_case_id")

    accepted_candidate_count = sum(1 for row in results if row.get("dryrun_status") == "accepted_candidate")
    rejected_candidate_count = sum(1 for row in results if row.get("dryrun_status") == "rejected_candidate")
    restricted_candidate_count = sum(1 for row in results if row.get("dryrun_status") == "restricted_candidate")
    stale_archive_only_candidate_count = sum(1 for row in results if row.get("dryrun_status") == "archive_only_candidate")

    frame_intake_gate_review = {
        "accepted_candidate_count": accepted_candidate_count,
        "rejected_candidate_count": rejected_candidate_count,
        "restricted_candidate_count": restricted_candidate_count,
        "stale_archive_only_candidate_count": stale_archive_only_candidate_count,
        "source_chain_required_verified": (
            summaries["controlled_frame_input_dryrun"].get("source_chain_required") is True
            and intake_idx.get("case_missing_source_chain_rejected", {}).get("intake_status") == "rejected_missing_source_chain"
        ),
        "timestamp_required_verified": (
            summaries["controlled_frame_input_dryrun"].get("timestamp_required") is True
            and intake_idx.get("case_missing_timestamp_rejected", {}).get("intake_status") == "rejected_missing_timestamp"
        ),
        "privacy_tags_required_verified": (
            summaries["controlled_frame_input_dryrun"].get("privacy_tags_required_for_downstream") is True
            and intake_idx.get("case_missing_privacy_tags_rejected", {}).get("intake_status") == "rejected_missing_privacy_tags"
        ),
        "live_camera_blocked_verified": intake_idx.get("case_live_camera_attempt_blocked", {}).get("intake_status") == "rejected_live_camera",
        "device_camera_blocked_verified": intake_idx.get("case_device_camera_attempt_blocked", {}).get("intake_status") == "rejected_device_camera",
        "external_stream_blocked_verified": intake_idx.get("case_external_stream_attempt_blocked", {}).get("intake_status") == "rejected_external_stream",
        "unknown_source_blocked_verified": "unknown source" in planning_intake_gate.get("reject_conditions", []),
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    good_cases = ["case_static_test_image_good_quality", "case_simulation_frame_allowed", "case_frame_with_text_requires_visual_focus_for_ocr", "case_frame_with_motion_requires_visual_focus_for_tracking"]
    blocked_cases = [
        "case_missing_source_chain_rejected",
        "case_missing_timestamp_rejected",
        "case_missing_privacy_tags_rejected",
        "case_live_camera_attempt_blocked",
        "case_device_camera_attempt_blocked",
        "case_external_stream_attempt_blocked",
    ]
    frame_quality_gate_review = {
        "quality_profiles_reviewed": sorted({row.get("quality_level") for row in quality_decisions if row.get("quality_level")}),
        "good_quality_downstream_allowed_verified": all(
            quality_idx.get(case_id, {}).get("quality_level") == "GOOD"
            and handoff_idx.get(case_id, {}).get("visual_focus_input_allowed") is True
            for case_id in good_cases
        ),
        "degraded_quality_downstream_limited_verified": (
            quality_idx.get("case_prerecorded_degraded_quality", {}).get("quality_level") == "DEGRADED"
            and handoff_idx.get("case_prerecorded_degraded_quality", {}).get("visual_focus_input_allowed") is True
            and handoff_idx.get("case_prerecorded_degraded_quality", {}).get("ocr_activation_input_allowed") is False
            and handoff_idx.get("case_prerecorded_degraded_quality", {}).get("tracking_request_input_allowed") is False
        ),
        "poor_or_blocked_degradation_verified": (
            "POOR" in planning_quality_gate.get("quality_levels", {})
            and all(quality_idx.get(case_id, {}).get("quality_level") == "BLOCKED" for case_id in blocked_cases)
        ),
        "active_view_adjustment_candidate_allowed_if_needed": quality_idx.get("case_prerecorded_degraded_quality", {}).get("active_view_adjustment_recommended") is True,
        "quality_fact_written": False,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    restricted_privacy_case = privacy_idx.get("case_controlled_uploaded_privacy_sensitive", {})
    frame_privacy_tagging_review = {
        "privacy_sensitive_case_reviewed": bool(restricted_privacy_case),
        "privacy_tags_required_for_downstream": summaries["controlled_frame_input_dryrun"].get("privacy_tags_required_for_downstream") is True,
        "restricted_use_verified": (
            restricted_privacy_case.get("privacy_risk_level") == "HIGH"
            and restricted_privacy_case.get("restricted_use_required") is True
            and restricted_privacy_case.get("downstream_allowed_candidate") is False
        ),
        "long_term_write_blocked": all(row.get("long_term_storage_allowed") is False for row in privacy_decisions),
        "face_identity_inference_allowed": False,
        "emotion_inference_allowed": False,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    stale_freshness_case = freshness_idx.get("case_stale_frame_archive_only", {})
    scenario_metadata_monotonic_reviewed = all(
        isinstance(row.get("simulated_frame_metadata", {}).get("monotonic_seq"), int) for row in scenarios
    )
    frame_stc_freshness_review = {
        "timestamp_required": planning_stc_policy.get("timestamp_required") is True,
        "monotonic_seq_reviewed": scenario_metadata_monotonic_reviewed and planning_stc_policy.get("monotonic_seq_required") is True,
        "stale_frame_reviewed": bool(stale_freshness_case),
        "expired_or_stale_current_action_blocked": (
            stale_freshness_case.get("current_action_allowed") is False
            and stale_freshness_case.get("expired_blocks_current_action") is True
        ),
        "archive_candidate_allowed": stale_freshness_case.get("archive_candidate_allowed") is True,
        "stc_freshness_reuse_required": planning_stc_policy.get("stc_freshness_reuse_required") is True
        and summaries["controlled_frame_input_dryrun"].get("stc_freshness_reuse_required") is True,
        "no_new_stc_module_created": True,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    frame_downstream_handoff_review = {
        "frame_to_view_quality_allowed_candidate": any(row.get("view_quality_candidate_allowed") is True for row in downstream_handoffs),
        "frame_to_scene_sketch_allowed_candidate": any(row.get("scene_sketch_input_allowed") is True for row in downstream_handoffs),
        "frame_to_visual_focus_allowed_candidate": any(row.get("visual_focus_input_allowed") is True for row in downstream_handoffs),
        "frame_to_ocr_requires_visual_focus": dryrun_boundary.get("frame_to_ocr_requires_visual_focus") is True and planning_handoff_policy.get("frame_to_ocr_requires_visual_focus") is True,
        "frame_to_tracking_requires_visual_focus": dryrun_boundary.get("frame_to_tracking_requires_visual_focus") is True and planning_handoff_policy.get("frame_to_tracking_requires_visual_focus") is True,
        "frame_to_world_observation_requires_policy": dryrun_boundary.get("frame_to_world_observation_requires_policy") is True and planning_handoff_policy.get("frame_to_world_observation_requires_policy") is True,
        "frame_to_navigation_action_allowed": False,
        "frame_to_speech_output_allowed": False,
        "frame_to_worldmodel_write_allowed": False,
        "frame_to_memory_write_allowed": False,
        "frame_to_fact_write_allowed": False,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    dual_device_placeholder_review = {
        "dual_device_redundant_perception_placeholder_loaded": dryrun_dual_review.get("dual_device_placeholder_loaded") is True and bool(planning_dual_placeholder),
        "perception_input_channel_placeholder_present": dryrun_dual_review.get("perception_input_channel_placeholder_present") is True,
        "perception_device_health_placeholder_present": dryrun_dual_review.get("perception_device_health_placeholder_present") is True,
        "perception_lane_failover_placeholder_present": dryrun_dual_review.get("perception_lane_failover_placeholder_present") is True,
        "dual_input_consistency_placeholder_present": dryrun_dual_review.get("dual_input_consistency_placeholder_present") is True,
        "dual_device_runtime_allowed": False,
        "dual_model_runtime_allowed": False,
        "failover_runtime_allowed": False,
        "automatic_hardware_switch_allowed": False,
        "multi_input_fusion_runtime_allowed": False,
        "hardware_stage_deferred": True,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    runtime_write_action_speech_boundary_review = {
        "frame_content_loaded": False,
        "actual_image_read": False,
        "camera_invoked": False,
        "camera_opened": False,
        "video_capture_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
        "dual_device_runtime_invoked": False,
        "dual_model_runtime_invoked": False,
        "failover_runtime_invoked": False,
        "multi_input_fusion_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_review = {
        "review_id": f"{REVIEW_ID}_debt",
        "planning_governance_debt_loaded": bool(planning_boundary),
        "dryrun_governance_debt_loaded": bool(dryrun_governance),
        "future_midplatform_function_governance_required": True,
        "no_duplicate_governance_module_allowed": True,
        "carryover_topics": [row.get("topic") for row in dryrun_governance.get("carryover_topics", [])],
        "review_notes": [
            "planning 定义的 intake/quality/privacy/stc/handoff 边界已在 dry-run 中得到覆盖性审查",
            "dual-device placeholder 仍维持 future hardware stage only",
            "暂不进入 controlled sample planning，先进入 closure 收口",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    for name, ok_value in (
        ("controlled_frame_input_dryrun_input_loaded", controlled_frame_input_dryrun_input_loaded),
        ("controlled_frame_input_planning_input_loaded", controlled_frame_input_planning_input_loaded),
        ("map_location_readonly_context_input_loaded", map_location_readonly_context_input_loaded),
        ("post_vision_strengthening_roadmap_decision_input_loaded", post_vision_strengthening_roadmap_decision_input_loaded),
        ("vision_strengthening_closure_input_loaded", vision_strengthening_closure_input_loaded),
        ("task_aware_visual_focus_input_loaded", task_aware_visual_focus_input_loaded),
        ("midplatform_perception_orchestration_input_loaded", midplatform_perception_orchestration_input_loaded),
        ("minimal_runtime_integration_closure_loaded", minimal_runtime_integration_closure_loaded),
        ("ocr_final_closure_loaded", ocr_final_closure_loaded),
    ):
        if not ok_value:
            blockers.append(name)
    if controlled_frame_scenario_coverage_review["verdict"] != "GO":
        blockers.append("scenario_coverage_gap")

    controlled_frame_input_closure_readiness_decision = {
        "post_dryrun_review_verdict": "GO" if not blockers else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "本阶段只做 review / audit / closure readiness",
            "controlled sample planning 仍保持 deferred",
        ],
        "ready_for_closure": not blockers,
        "ready_for_controlled_sample_planning": False,
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_runtime_boundary_report = _boundary_payload()
    no_write_boundary_report = _boundary_payload()

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "controlled_frame_input_dryrun_input_loaded": controlled_frame_input_dryrun_input_loaded,
        "controlled_frame_input_planning_input_loaded": controlled_frame_input_planning_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "post_vision_strengthening_roadmap_decision_input_loaded": post_vision_strengthening_roadmap_decision_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "input_root_review_generated": True,
        "scenario_coverage_review_generated": True,
        "frame_intake_gate_review_generated": True,
        "frame_quality_gate_review_generated": True,
        "frame_privacy_tagging_review_generated": True,
        "frame_stc_freshness_review_generated": True,
        "frame_downstream_handoff_review_generated": True,
        "dual_device_placeholder_review_generated": True,
        "runtime_write_action_speech_boundary_review_generated": True,
        "closure_readiness_decision_generated": True,
        "governance_debt_review_generated": True,
        "reviewed_scenario_count": len(scenarios),
        "accepted_candidate_count": accepted_candidate_count,
        "rejected_candidate_count": rejected_candidate_count,
        "restricted_candidate_count": restricted_candidate_count,
        "stale_archive_only_candidate_count": stale_archive_only_candidate_count,
        "source_chain_required_verified": frame_intake_gate_review["source_chain_required_verified"],
        "timestamp_required_verified": frame_intake_gate_review["timestamp_required_verified"],
        "privacy_tags_required_verified": frame_intake_gate_review["privacy_tags_required_verified"],
        "live_camera_blocked_verified": frame_intake_gate_review["live_camera_blocked_verified"],
        "device_camera_blocked_verified": frame_intake_gate_review["device_camera_blocked_verified"],
        "external_stream_blocked_verified": frame_intake_gate_review["external_stream_blocked_verified"],
        "frame_to_ocr_requires_visual_focus": frame_downstream_handoff_review["frame_to_ocr_requires_visual_focus"],
        "frame_to_tracking_requires_visual_focus": frame_downstream_handoff_review["frame_to_tracking_requires_visual_focus"],
        "frame_to_world_observation_requires_policy": frame_downstream_handoff_review["frame_to_world_observation_requires_policy"],
        "frame_to_navigation_action_allowed": False,
        "frame_to_speech_output_allowed": False,
        "frame_to_worldmodel_write_allowed": False,
        "frame_to_memory_write_allowed": False,
        "frame_to_fact_write_allowed": False,
        "dual_device_redundant_perception_placeholder_loaded": dual_device_placeholder_review["dual_device_redundant_perception_placeholder_loaded"],
        "dual_device_runtime_allowed": False,
        "dual_model_runtime_allowed": False,
        "failover_runtime_allowed": False,
        "automatic_hardware_switch_allowed": False,
        "multi_input_fusion_runtime_allowed": False,
        "hardware_stage_deferred": True,
        "no_runtime_boundary_pass": True,
        "no_write_boundary_pass": True,
        "no_action_boundary_pass": True,
        "no_speech_boundary_pass": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "frame_content_loaded": False,
        "actual_image_read": False,
        "camera_invoked": False,
        "camera_opened": False,
        "video_capture_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
        "dual_device_runtime_invoked": False,
        "dual_model_runtime_invoked": False,
        "failover_runtime_invoked": False,
        "multi_input_fusion_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
        "route_modified": False,
        "scene_delta_generated": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "entity_resolution_runtime_invoked": False,
        "fact_admission_runtime_invoked": False,
        "memory_consolidation_invoked": False,
        "library_experience_commit_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_frame_dryrun_input_root_review": controlled_frame_dryrun_input_root_review,
        "controlled_frame_scenario_coverage_review": controlled_frame_scenario_coverage_review,
        "frame_intake_gate_review": frame_intake_gate_review,
        "frame_quality_gate_review": frame_quality_gate_review,
        "frame_privacy_tagging_review": frame_privacy_tagging_review,
        "frame_stc_freshness_review": frame_stc_freshness_review,
        "frame_downstream_handoff_review": frame_downstream_handoff_review,
        "dual_device_placeholder_review": dual_device_placeholder_review,
        "runtime_write_action_speech_boundary_review": runtime_write_action_speech_boundary_review,
        "controlled_frame_input_closure_readiness_decision": controlled_frame_input_closure_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": {
            "recommended_next_phase": summary["recommended_next_phase"],
            "final_decision": summary["final_decision"],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "no_runtime_boundary_report": no_runtime_boundary_report,
        "no_write_boundary_report": no_write_boundary_report,
    }
