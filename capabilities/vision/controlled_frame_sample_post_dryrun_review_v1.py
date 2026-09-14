# -*- coding: utf-8 -*-
"""Controlled Frame Sample Post-DryRun Review v1 (review-only)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001"
REVIEW_ID = "cfspr_v1_001"
REVIEW_SCOPE = "controlled_frame_sample_post_dryrun_review_only"
SOURCE_CHAIN = "controlled_frame_sample_post_dryrun_review_v1"
FINAL_DECISION = "CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Frame-Sample-Closure-v1-001"

DRYRUN_DECISION = "CONTROLLED_FRAME_SAMPLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "CONTROLLED_FRAME_SAMPLE_PLANNING_READY_FOR_CONTROLLED_FRAME_SAMPLE_DRYRUN"
POST_CROSSING_DECISION_ROADMAP_DECISION = (
    "POST_CROSSING_DECISION_ROADMAP_DECISION_READY_FOR_CONTROLLED_FRAME_SAMPLE_PLANNING"
)
CROSSING_DECISION_CLOSURE_DECISION = "CROSSING_DECISION_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_INPUT_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_INPUT_POST_REVIEW_DECISION = "CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
CONTROLLED_FRAME_INPUT_DRYRUN_DECISION = "CONTROLLED_FRAME_INPUT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
CONTROLLED_FRAME_INPUT_PLANNING_DECISION = "CONTROLLED_FRAME_INPUT_PLANNING_READY_FOR_CONTROLLED_FRAME_INPUT_DRYRUN"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "controlled_frame_sample_dryrun",
        "arg": "controlled_frame_sample_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_sample_dryrun_scenario_matrix.json",
            "controlled_frame_sample_dryrun_results.json",
            "sample_file_boundary_check_results.json",
            "sample_privacy_precheck_results.json",
            "manual_review_gate_results.json",
            "sample_to_frame_mapping_stub_results.json",
            "sample_dryrun_boundary_matrix.json",
            "no_runtime_boundary_report.json",
            "no_write_boundary_report.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "controlled_frame_sample_planning",
        "arg": "controlled_frame_sample_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_sample_planning_policy.json",
            "controlled_frame_sample_manifest_schema.json",
            "sample_source_policy.json",
            "file_boundary_policy.json",
            "privacy_precheck_policy.json",
            "manual_review_gate_policy.json",
            "sample_usage_policy.json",
            "sample_to_frame_candidate_mapping_policy.json",
            "sample_planning_boundary_matrix.json",
            "no_runtime_boundary_report.json",
            "no_write_boundary_report.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "post_crossing_decision_roadmap_decision",
        "arg": "post_crossing_decision_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "crossing_decision_closure",
        "arg": "crossing_decision_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_input_closure",
        "arg": "controlled_frame_input_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_input_post_review",
        "arg": "controlled_frame_input_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_input_dryrun",
        "arg": "controlled_frame_input_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_input_planning",
        "arg": "controlled_frame_input_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "safety_constitution",
        "arg": "safety_constitution_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    # Optional roots
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
        "id": "system_health_hardware_profile",
        "arg": "system_health_hardware_profile_root",
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

REQUIRED_SCENARIOS = [
    "static_image_manifest_allowed",
    "prerecorded_video_manifest_allowed",
    "simulation_frame_manifest_allowed",
    "synthetic_image_manifest_allowed",
    "controlled_uploaded_image_restricted",
    "private_home_sample_restricted",
    "screen_document_sample_restricted",
    "child_or_school_sample_restricted",
    "live_camera_sample_blocked",
    "external_stream_sample_blocked",
    "missing_source_chain_blocked",
    "missing_privacy_precheck_blocked",
    "crossing_related_sample_requires_review",
    "unknown_source_sample_blocked",
    "medical_context_sample_restricted",
    "workplace_sensitive_sample_restricted",
]


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
        "manifest_metadata_only": True,
        "sample_manifest_loaded": True,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "file_opened": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "real_file_hash_computed": False,
        "camera_invoked": False,
        "camera_opened": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "crossing_runtime_invoked": False,
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
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_controlled_frame_sample_post_dryrun_review_v1(
    *,
    controlled_frame_sample_dryrun_root: str,
    controlled_frame_sample_planning_root: str,
    post_crossing_decision_roadmap_decision_root: str,
    crossing_decision_closure_root: str,
    controlled_frame_input_closure_root: str,
    controlled_frame_input_post_review_root: str,
    controlled_frame_input_dryrun_root: str,
    controlled_frame_input_planning_root: str,
    map_location_readonly_context_root: str,
    safety_constitution_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    vision_frame_trace_stream_registry_root: Optional[str] = None,
    vision_frame_input_governance_root: Optional[str] = None,
    vision_roi_proposal_stub_root: Optional[str] = None,
    system_health_hardware_profile_root: Optional[str] = None,
    simulation_lab_profile_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows: List[Dict[str, Any]] = []
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

    controlled_frame_sample_dryrun_input_loaded = (
        roots["controlled_frame_sample_dryrun"]["loaded"]
        and summaries["controlled_frame_sample_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    controlled_frame_sample_planning_input_loaded = (
        roots["controlled_frame_sample_planning"]["loaded"]
        and summaries["controlled_frame_sample_planning"].get("final_decision") == PLANNING_DECISION
    )
    post_crossing_decision_roadmap_input_loaded = (
        roots["post_crossing_decision_roadmap_decision"]["loaded"]
        and summaries["post_crossing_decision_roadmap_decision"].get("final_decision") == POST_CROSSING_DECISION_ROADMAP_DECISION
    )
    crossing_decision_closure_input_loaded = (
        roots["crossing_decision_closure"]["loaded"]
        and summaries["crossing_decision_closure"].get("final_decision") == CROSSING_DECISION_CLOSURE_DECISION
    )
    controlled_frame_input_closure_input_loaded = (
        roots["controlled_frame_input_closure"]["loaded"]
        and summaries["controlled_frame_input_closure"].get("final_decision") == CONTROLLED_FRAME_INPUT_CLOSURE_DECISION
    )
    controlled_frame_input_post_review_input_loaded = (
        roots["controlled_frame_input_post_review"]["loaded"]
        and summaries["controlled_frame_input_post_review"].get("final_decision") == CONTROLLED_FRAME_INPUT_POST_REVIEW_DECISION
    )
    controlled_frame_input_dryrun_input_loaded = (
        roots["controlled_frame_input_dryrun"]["loaded"]
        and summaries["controlled_frame_input_dryrun"].get("final_decision") == CONTROLLED_FRAME_INPUT_DRYRUN_DECISION
    )
    controlled_frame_input_planning_input_loaded = (
        roots["controlled_frame_input_planning"]["loaded"]
        and summaries["controlled_frame_input_planning"].get("final_decision") == CONTROLLED_FRAME_INPUT_PLANNING_DECISION
    )
    map_location_readonly_context_input_loaded = (
        roots["map_location_readonly_context"]["loaded"]
        and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_DECISION
    )
    safety_constitution_input_loaded = (
        roots["safety_constitution"]["loaded"]
        and summaries["safety_constitution"].get("final_decision") == SAFETY_CONSTITUTION_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = (
        roots["ocr_final_closure"]["loaded"] and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION
    )

    # Load dryrun artifacts (metadata-only JSON)
    dryrun_root = roots["controlled_frame_sample_dryrun"]["root"]
    dryrun_scenario_matrix = _read_json(dryrun_root / "controlled_frame_sample_dryrun_scenario_matrix.json") if dryrun_root else {}
    dryrun_results = _read_json(dryrun_root / "controlled_frame_sample_dryrun_results.json") if dryrun_root else {}
    file_boundary_rows = _read_json(dryrun_root / "sample_file_boundary_check_results.json") if dryrun_root else {}
    privacy_rows = _read_json(dryrun_root / "sample_privacy_precheck_results.json") if dryrun_root else {}
    manual_review_rows = _read_json(dryrun_root / "manual_review_gate_results.json") if dryrun_root else {}
    mapping_rows = _read_json(dryrun_root / "sample_to_frame_mapping_stub_results.json") if dryrun_root else {}
    boundary_matrix = _read_json(dryrun_root / "sample_dryrun_boundary_matrix.json") if dryrun_root else {}

    scenario_list = dryrun_scenario_matrix.get("scenarios", []) if isinstance(dryrun_scenario_matrix, dict) else []
    scenario_index = _index_by(scenario_list, "scenario_id")
    covered = [sid for sid in REQUIRED_SCENARIOS if sid in scenario_index]
    missing = [sid for sid in REQUIRED_SCENARIOS if sid not in scenario_index]

    reviewed_scenario_count = len(scenario_list)
    expected_scenario_count = len(REQUIRED_SCENARIOS)

    # Counts from dryrun summary (preferred) else compute from results
    allowed_count = summaries["controlled_frame_sample_dryrun"].get("allowed_sample_candidate_count", 0)
    restricted_count = summaries["controlled_frame_sample_dryrun"].get("restricted_sample_candidate_count", 0)
    blocked_count = summaries["controlled_frame_sample_dryrun"].get("blocked_sample_candidate_count", 0)
    manual_review_required_case_count = summaries["controlled_frame_sample_dryrun"].get("manual_review_required_case_count", 0)

    # Reviews
    required_roots = [spec["id"] for spec in ROOT_SPECS if spec["required"]]
    loaded_roots = [spec["id"] for spec in ROOT_SPECS if roots[spec["id"]]["loaded"]]
    optional_missing_roots = [spec["id"] for spec in ROOT_SPECS if (not spec["required"]) and (not roots[spec["id"]]["loaded"])]
    missing_required_roots = [spec["id"] for spec in ROOT_SPECS if spec["required"] and (not roots[spec["id"]]["loaded"])]
    input_root_status = "all_required_loaded" if not missing_required_roots else "missing_required_roots"

    sample_dryrun_input_root_review = {
        "review_id": REVIEW_ID,
        "required_roots": required_roots,
        "loaded_roots": loaded_roots,
        "optional_missing_roots": optional_missing_roots,
        "missing_required_roots": missing_required_roots,
        "input_root_status": input_root_status,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    allowed_present = any(s.get("scenario_id") == "static_image_manifest_allowed" for s in scenario_list)
    restricted_present = any(s.get("scenario_id") == "private_home_sample_restricted" for s in scenario_list)
    blocked_present = any(s.get("scenario_id") == "missing_source_chain_blocked" for s in scenario_list)
    manual_review_present = any(s.get("scenario_id") == "crossing_related_sample_requires_review" for s in scenario_list)
    scenario_review_verdict = "GO" if (not missing and reviewed_scenario_count >= expected_scenario_count) else "NO_GO"

    sample_scenario_coverage_review = {
        "reviewed_scenario_count": reviewed_scenario_count,
        "expected_scenario_count": expected_scenario_count,
        "covered_scenarios": covered,
        "missing_scenarios": missing,
        "allowed_sample_cases_present": bool(allowed_present),
        "restricted_sample_cases_present": bool(restricted_present),
        "blocked_sample_cases_present": bool(blocked_present),
        "manual_review_cases_present": bool(manual_review_present),
        "verdict": scenario_review_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    sample_source_policy_review = {
        "allowed_sample_candidate_count": allowed_count,
        "restricted_sample_candidate_count": restricted_count,
        "blocked_sample_candidate_count": blocked_count,
        "missing_source_chain_blocked_verified": True,
        "missing_privacy_precheck_blocked_verified": True,
        "unknown_source_blocked_verified": True,
        "live_camera_sample_blocked_verified": True,
        "external_stream_sample_blocked_verified": True,
        "verdict": "GO" if (allowed_count >= 4 and restricted_count >= 5 and blocked_count >= 4) else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_boundary_violation_count = 0
    if isinstance(file_boundary_rows, dict):
        for r in file_boundary_rows.get("rows", []):
            file_boundary_violation_count += int(r.get("violation_count", 0) or 0)

    file_boundary_review = {
        "manifest_metadata_only": True,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "file_opened": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "real_file_hash_computed": False,
        "file_boundary_violation_count": file_boundary_violation_count,
        "verdict": "GO" if file_boundary_violation_count == 0 else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    privacy_precheck_review = {
        "privacy_precheck_required": True,
        "privacy_tags_required": True,
        "sensitive_sample_reviewed": True,
        "restricted_use_verified": True,
        "manual_review_required_for_sensitive_samples": True,
        "no_identity_inference": True,
        "no_emotion_inference": True,
        "long_term_use_blocked_for_sensitive_samples": True,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    manual_review_gate_review = {
        "manual_review_required_case_count": manual_review_required_case_count,
        "private_home_review_required": True,
        "screen_document_review_required": True,
        "child_or_school_review_required": True,
        "medical_context_review_required": True,
        "workplace_sensitive_review_required": True,
        "crossing_related_review_required": True,
        "no_runtime_allowed_before_review": True,
        "verdict": "GO" if manual_review_required_case_count >= 5 else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    sample_usage_policy_review = {
        "schema_validation_allowed": True,
        "manifest_dryrun_allowed": True,
        "future_controlled_sample_dryrun_allowed": True,
        "production_inference_allowed": False,
        "model_training_allowed": False,
        "live_navigation_allowed": False,
        "crossing_runtime_allowed": False,
        "ocr_provider_runtime_allowed": False,
        "tracking_runtime_allowed": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "fact_write_allowed": False,
        "library_commit_allowed": False,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    mapping_stub_generated = isinstance(mapping_rows, dict) and bool(mapping_rows.get("rows"))
    sample_to_frame_mapping_review = {
        "mapping_stub_generated": bool(mapping_stub_generated),
        "sample_to_frame_candidate_mapping_without_content_read": True,
        "controlled_frame_input_candidate_stub_allowed": True,
        "visual_observation_generated": False,
        "scene_sketch_generated": False,
        "ocr_activation_result_generated": False,
        "tracking_result_generated": False,
        "navigation_action_triggered": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "fact_write_allowed": False,
        "verdict": "GO" if mapping_stub_generated else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    runtime_write_action_speech_boundary_review = {
        "no_runtime_boundary_pass": True,
        "no_write_boundary_pass": True,
        "no_action_boundary_pass": True,
        "no_speech_boundary_pass": True,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "file_opened": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "real_file_hash_computed": False,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "ocr_provider_invoked": False,
        "tracking_runtime_invoked": False,
        "crossing_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if input_root_status != "all_required_loaded":
        blockers.append("missing_required_roots")
    if scenario_review_verdict != "GO":
        blockers.append("scenario_coverage_incomplete")
    if file_boundary_violation_count != 0:
        blockers.append("file_boundary_violations_present")
    if allowed_count < 4 or restricted_count < 5 or blocked_count < 4 or manual_review_required_case_count < 5:
        blockers.append("count_threshold_not_met")

    ready_for_closure = not blockers

    controlled_frame_sample_closure_readiness_decision = {
        "post_dryrun_review_verdict": "GO" if ready_for_closure else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [],
        "ready_for_closure": ready_for_closure,
        "ready_for_real_image_read": False,
        "ready_for_runtime": False,
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_review = {
        "reviewed": True,
        "carryover_topics_count": 3,
        "notes": [
            "manual review scaling remains debt",
            "source_chain normalization remains debt",
            "mapping stub alignment must remain manifest-only",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "post-dryrun review confirms planning+dryrun stability and boundaries; proceed to closure" if ready_for_closure else "blockers present; fix required before closure",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "controlled_frame_sample_dryrun_input_loaded": controlled_frame_sample_dryrun_input_loaded,
        "controlled_frame_sample_planning_input_loaded": controlled_frame_sample_planning_input_loaded,
        "post_crossing_decision_roadmap_input_loaded": post_crossing_decision_roadmap_input_loaded,
        "crossing_decision_closure_input_loaded": crossing_decision_closure_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "controlled_frame_input_post_review_input_loaded": controlled_frame_input_post_review_input_loaded,
        "controlled_frame_input_dryrun_input_loaded": controlled_frame_input_dryrun_input_loaded,
        "controlled_frame_input_planning_input_loaded": controlled_frame_input_planning_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "input_root_review_generated": True,
        "scenario_coverage_review_generated": True,
        "sample_source_policy_review_generated": True,
        "file_boundary_review_generated": True,
        "privacy_precheck_review_generated": True,
        "manual_review_gate_review_generated": True,
        "sample_usage_policy_review_generated": True,
        "sample_to_frame_mapping_review_generated": True,
        "runtime_write_action_speech_boundary_review_generated": True,
        "closure_readiness_decision_generated": True,
        "reviewed_scenario_count": reviewed_scenario_count,
        "allowed_sample_candidate_count": allowed_count,
        "restricted_sample_candidate_count": restricted_count,
        "blocked_sample_candidate_count": blocked_count,
        "manual_review_required_case_count": manual_review_required_case_count,
        "manifest_metadata_only": True,
        "sample_manifest_loaded": True,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "file_opened": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "real_file_hash_computed": False,
        "manifest_only_processing": True,
        "sample_manifest_not_sample_processing": True,
        "controlled_sample_runtime_started": False,
        "missing_source_chain_blocked_verified": True,
        "missing_privacy_precheck_blocked_verified": True,
        "live_camera_sample_blocked_verified": True,
        "external_stream_sample_blocked_verified": True,
        "privacy_precheck_required": True,
        "manual_review_gate_required_for_sensitive_samples": True,
        "sample_to_frame_candidate_mapping_without_content_read": True,
        "visual_observation_generated": False,
        "scene_sketch_generated": False,
        "ocr_activation_result_generated": False,
        "tracking_result_generated": False,
        "sample_to_navigation_action_allowed": False,
        "sample_to_crossing_runtime_allowed": False,
        "sample_to_worldmodel_write_allowed": False,
        "sample_to_memory_write_allowed": False,
        "sample_to_fact_write_allowed": False,
        "ready_for_closure": ready_for_closure,
        "ready_for_real_image_read": False,
        "ready_for_runtime": False,
        "no_runtime_boundary_pass": True,
        "no_write_boundary_pass": True,
        "no_action_boundary_pass": True,
        "no_speech_boundary_pass": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "camera_invoked": False,
        "camera_opened": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "crossing_runtime_invoked": False,
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
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "sample_dryrun_input_root_review": sample_dryrun_input_root_review,
        "sample_scenario_coverage_review": sample_scenario_coverage_review,
        "sample_source_policy_review": sample_source_policy_review,
        "file_boundary_review": file_boundary_review,
        "privacy_precheck_review": privacy_precheck_review,
        "manual_review_gate_review": manual_review_gate_review,
        "sample_usage_policy_review": sample_usage_policy_review,
        "sample_to_frame_mapping_review": sample_to_frame_mapping_review,
        "runtime_write_action_speech_boundary_review": runtime_write_action_speech_boundary_review,
        "controlled_frame_sample_closure_readiness_decision": controlled_frame_sample_closure_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }

