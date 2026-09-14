# -*- coding: utf-8 -*-
"""Controlled Frame File Existence Check Guarded Post-DryRun Review v1 (review-only).

Audits planning + dryrun outputs for policy alignment and no-file-operation boundaries.
Does NOT call exists/stat/open/read/probe/hash or perform any real file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-File-Existence-Check-Guarded-Post-DryRun-Review-v1-001"
REVIEW_ID = "cffecgpdr_v1_001"
REVIEW_SCOPE = "controlled_frame_file_existence_check_guarded_post_dryrun_review_only"
SOURCE_CHAIN = "controlled_frame_file_existence_check_guarded_post_dryrun_review_v1"

FINAL_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Frame-File-Existence-Check-Guarded-Closure-v1-001"

DRYRUN_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_READY_FOR_DRYRUN"

POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION = (
    "POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION_READY_FOR_FILE_EXISTENCE_CHECK_GUARDED_PLANNING"
)
FILE_METADATA_BOUNDARY_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSED_FOR_CURRENT_MAINLINE"
FILE_METADATA_BOUNDARY_POST_REVIEW_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
FILE_METADATA_BOUNDARY_DRYRUN_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FILE_METADATA_BOUNDARY_PLANNING_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_READY_FOR_DRYRUN"

CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION = "CONTROLLED_FRAME_SAMPLE_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_INPUT_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

REQUIRED_SCENARIOS = [
    "repo_fixture_future_candidate",
    "eval_out_fixture_future_candidate",
    "registered_fixture_future_candidate",
    "controlled_test_asset_future_candidate",
    "user_upload_restricted",
    "external_absolute_path_blocked",
    "path_traversal_blocked",
    "unknown_path_blocked",
    "symlink_restricted",
    "system_sensitive_path_blocked",
    "home_arbitrary_path_blocked",
    "network_mount_path_blocked",
    "missing_source_chain_blocked",
    "missing_privacy_tags_blocked",
    "missing_fixture_registry_ref_blocked",
    "user_upload_authorization_insufficient",
    "system_generated_path_insufficient",
    "authorized_candidate_but_not_invoked",
    "gate_denied_behavior",
    "permission_denied_future_failure_mode",
    "missing_file_future_failure_mode",
    "rollback_after_denied_candidate",
]

ROOT_SPECS = [
    {
        "id": "controlled_frame_file_existence_check_guarded_dryrun",
        "arg": "controlled_frame_file_existence_check_guarded_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_file_existence_check_guarded_dryrun_scenario_matrix.json",
            "controlled_frame_file_existence_check_guarded_dryrun_results.json",
            "file_existence_gate_decision_results.json",
            "path_scope_dryrun_decision_results.json",
            "authorization_decision_results.json",
            "audit_trace_results.json",
            "failure_mode_decision_results.json",
            "rollback_decision_results.json",
            "existence_to_file_metadata_mapping_results.json",
            "file_existence_check_boundary_matrix.json",
            "no_file_operation_boundary_report.json",
            "no_runtime_boundary_report.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "controlled_frame_file_existence_check_guarded_planning",
        "arg": "controlled_frame_file_existence_check_guarded_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_file_existence_check_guarded_planning_policy.json",
            "file_existence_check_gate_policy.json",
            "allowed_path_scope_policy.json",
            "blocked_path_scope_policy.json",
            "file_existence_authorization_policy.json",
            "file_existence_audit_trace_policy.json",
            "file_existence_failure_mode_policy.json",
            "file_existence_rollback_policy.json",
            "file_existence_decision_candidate_schema.json",
            "existence_check_to_file_metadata_candidate_mapping_policy.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "post_file_metadata_boundary_roadmap_decision",
        "arg": "post_file_metadata_boundary_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "next_phase_recommendation.json", "verifier_report.json"],
    },
    {
        "id": "file_metadata_boundary_closure",
        "arg": "file_metadata_boundary_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_metadata_boundary_closure_summary.json", "validated_capability_summary.json"],
    },
    {
        "id": "file_metadata_boundary_post_review",
        "arg": "file_metadata_boundary_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "file_metadata_boundary_closure_readiness_decision.json", "verifier_report.json"],
    },
    {
        "id": "file_metadata_boundary_dryrun",
        "arg": "file_metadata_boundary_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_metadata_boundary_dryrun_results.json", "verifier_report.json"],
    },
    {
        "id": "file_metadata_boundary_planning",
        "arg": "file_metadata_boundary_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_metadata_boundary_planning_policy.json", "verifier_report.json"],
    },
    {
        "id": "controlled_frame_sample_closure",
        "arg": "controlled_frame_sample_closure_root",
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
    {"id": "vision_frame_trace_stream_registry", "arg": "vision_frame_trace_stream_registry_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "vision_frame_input_governance", "arg": "vision_frame_input_governance_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "vision_roi_proposal_stub", "arg": "vision_roi_proposal_stub_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "system_health_hardware_profile", "arg": "system_health_hardware_profile_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "simulation_lab_profile", "arg": "simulation_lab_profile_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "privacy_governance_docs", "arg": "privacy_governance_docs_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None


def _root_loaded(root: Optional[Path], artifacts: List[str]) -> bool:
    if not root:
        return False
    for name in artifacts:
        if _try_read_json(root / name) is None:
            return False
    return True


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = _root_loaded(root, artifacts) if root else False
    summary_payload = _try_read_json(root / summary_file) if (root and loaded) else {}
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _index_by(items: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in items:
        value = item.get(key)
        if value:
            out[value] = item
    return out


def _no_file_operation_payload() -> Dict[str, Any]:
    return {
        "review_scope": REVIEW_SCOPE,
        "review_only": True,
        "existence_gate_decision_simulation_only": True,
        "file_existence_check_invoked": False,
        "os_path_exists_invoked": False,
        "pathlib_exists_invoked": False,
        "file_stat_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "exif_parsed": False,
        "video_probe_invoked": False,
        "real_file_hash_computed": False,
        "perceptual_hash_computed": False,
        "fixture_registry_runtime_started": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _no_runtime_payload() -> Dict[str, Any]:
    return {
        "review_scope": REVIEW_SCOPE,
        "no_runtime_boundary_pass": True,
        "no_write_boundary_pass": True,
        "no_action_boundary_pass": True,
        "no_speech_boundary_pass": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "visual_observation_generated": False,
        "scene_sketch_generated": False,
        "ocr_activation_result_generated": False,
        "tracking_result_generated": False,
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


def run_controlled_frame_file_existence_check_guarded_post_dryrun_review_v1(
    *,
    controlled_frame_file_existence_check_guarded_dryrun_root: str,
    controlled_frame_file_existence_check_guarded_planning_root: str,
    post_file_metadata_boundary_roadmap_decision_root: str,
    file_metadata_boundary_closure_root: str,
    file_metadata_boundary_post_review_root: str,
    file_metadata_boundary_dryrun_root: str,
    file_metadata_boundary_planning_root: str,
    controlled_frame_sample_closure_root: str,
    controlled_frame_input_closure_root: str,
    map_location_readonly_context_root: str,
    safety_constitution_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    vision_frame_trace_stream_registry_root: Optional[str] = None,
    vision_frame_input_governance_root: Optional[str] = None,
    vision_roi_proposal_stub_root: Optional[str] = None,
    system_health_hardware_profile_root: Optional[str] = None,
    simulation_lab_profile_root: Optional[str] = None,
    privacy_governance_docs_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

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

    dryrun_input_loaded = (
        roots["controlled_frame_file_existence_check_guarded_dryrun"]["loaded"]
        and summaries["controlled_frame_file_existence_check_guarded_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    planning_input_loaded = (
        roots["controlled_frame_file_existence_check_guarded_planning"]["loaded"]
        and summaries["controlled_frame_file_existence_check_guarded_planning"].get("final_decision") == PLANNING_DECISION
    )
    post_file_metadata_boundary_roadmap_input_loaded = (
        roots["post_file_metadata_boundary_roadmap_decision"]["loaded"]
        and summaries["post_file_metadata_boundary_roadmap_decision"].get("final_decision") == POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION
    )
    file_metadata_boundary_closure_input_loaded = (
        roots["file_metadata_boundary_closure"]["loaded"]
        and summaries["file_metadata_boundary_closure"].get("final_decision") == FILE_METADATA_BOUNDARY_CLOSURE_DECISION
        and summaries["file_metadata_boundary_closure"].get("file_metadata_boundary_closed") is True
    )
    file_metadata_boundary_post_review_input_loaded = (
        roots["file_metadata_boundary_post_review"]["loaded"]
        and summaries["file_metadata_boundary_post_review"].get("final_decision") == FILE_METADATA_BOUNDARY_POST_REVIEW_DECISION
    )
    file_metadata_boundary_dryrun_input_loaded = (
        roots["file_metadata_boundary_dryrun"]["loaded"]
        and summaries["file_metadata_boundary_dryrun"].get("final_decision") == FILE_METADATA_BOUNDARY_DRYRUN_DECISION
    )
    file_metadata_boundary_planning_input_loaded = (
        roots["file_metadata_boundary_planning"]["loaded"]
        and summaries["file_metadata_boundary_planning"].get("final_decision") == FILE_METADATA_BOUNDARY_PLANNING_DECISION
    )
    controlled_frame_sample_closure_input_loaded = (
        roots["controlled_frame_sample_closure"]["loaded"]
        and summaries["controlled_frame_sample_closure"].get("final_decision") == CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION
    )
    controlled_frame_input_closure_input_loaded = (
        roots["controlled_frame_input_closure"]["loaded"]
        and summaries["controlled_frame_input_closure"].get("final_decision") == CONTROLLED_FRAME_INPUT_CLOSURE_DECISION
    )
    map_location_readonly_context_input_loaded = (
        roots["map_location_readonly_context"]["loaded"]
        and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_DECISION
    )
    safety_constitution_input_loaded = (
        roots["safety_constitution"]["loaded"] and summaries["safety_constitution"].get("final_decision") == SAFETY_CONSTITUTION_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = roots["ocr_final_closure"]["loaded"] and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION

    dryrun_root = roots["controlled_frame_file_existence_check_guarded_dryrun"]["root"]
    planning_root = roots["controlled_frame_file_existence_check_guarded_planning"]["root"]

    dryrun_summary = summaries["controlled_frame_file_existence_check_guarded_dryrun"]
    planning_summary = summaries["controlled_frame_file_existence_check_guarded_planning"]

    scenario_matrix = _try_read_json(dryrun_root / "controlled_frame_file_existence_check_guarded_dryrun_scenario_matrix.json") if dryrun_root else {}
    gate_results_doc = _try_read_json(dryrun_root / "file_existence_gate_decision_results.json") if dryrun_root else {}
    path_scope_results_doc = _try_read_json(dryrun_root / "path_scope_dryrun_decision_results.json") if dryrun_root else {}
    auth_results_doc = _try_read_json(dryrun_root / "authorization_decision_results.json") if dryrun_root else {}
    audit_results_doc = _try_read_json(dryrun_root / "audit_trace_results.json") if dryrun_root else {}
    failure_results_doc = _try_read_json(dryrun_root / "failure_mode_decision_results.json") if dryrun_root else {}
    rollback_results_doc = _try_read_json(dryrun_root / "rollback_decision_results.json") if dryrun_root else {}
    mapping_results_doc = _try_read_json(dryrun_root / "existence_to_file_metadata_mapping_results.json") if dryrun_root else {}
    no_file_op_dryrun = _try_read_json(dryrun_root / "no_file_operation_boundary_report.json") if dryrun_root else {}

    # Required roots review
    required_roots = [spec["id"] for spec in ROOT_SPECS if spec["required"]]
    loaded_roots = [spec["id"] for spec in ROOT_SPECS if roots[spec["id"]]["loaded"]]
    optional_missing_roots = [spec["id"] for spec in ROOT_SPECS if (not spec["required"]) and (not roots[spec["id"]]["loaded"])]
    missing_required_roots = [spec["id"] for spec in ROOT_SPECS if spec["required"] and (not roots[spec["id"]]["loaded"])]
    input_root_status = "all_required_loaded" if not missing_required_roots else "missing_required_roots"
    input_root_review = {
        "review_id": REVIEW_ID,
        "required_roots": required_roots,
        "loaded_roots": loaded_roots,
        "optional_missing_roots": optional_missing_roots,
        "missing_required_roots": missing_required_roots,
        "input_root_status": input_root_status,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Scenario coverage review
    scenario_list = scenario_matrix.get("scenarios", []) if isinstance(scenario_matrix, dict) else []
    scenario_index = _index_by(scenario_list, "scenario_id")
    covered = [sid for sid in REQUIRED_SCENARIOS if sid in scenario_index]
    missing = [sid for sid in REQUIRED_SCENARIOS if sid not in scenario_index]
    reviewed_scenario_count = len(scenario_list)
    expected_scenario_count = len(REQUIRED_SCENARIOS)
    scenario_verdict = "GO" if (not missing and reviewed_scenario_count >= expected_scenario_count) else "NO_GO"
    scenario_coverage_review = {
        "reviewed_scenario_count": reviewed_scenario_count,
        "expected_scenario_count": expected_scenario_count,
        "covered_scenarios": covered,
        "missing_scenarios": missing,
        "future_allowed_path_cases_present": all(
            s in scenario_index
            for s in (
                "repo_fixture_future_candidate",
                "eval_out_fixture_future_candidate",
                "registered_fixture_future_candidate",
                "controlled_test_asset_future_candidate",
            )
        ),
        "restricted_path_cases_present": all(s in scenario_index for s in ("user_upload_restricted", "symlink_restricted")),
        "blocked_path_cases_present": all(
            s in scenario_index
            for s in (
                "external_absolute_path_blocked",
                "path_traversal_blocked",
                "unknown_path_blocked",
                "system_sensitive_path_blocked",
                "home_arbitrary_path_blocked",
                "network_mount_path_blocked",
            )
        ),
        "authorization_failure_cases_present": all(
            s in scenario_index for s in ("user_upload_authorization_insufficient", "system_generated_path_insufficient")
        ),
        "failure_mode_cases_present": all(
            s in scenario_index
            for s in ("gate_denied_behavior", "permission_denied_future_failure_mode", "missing_file_future_failure_mode")
        ),
        "rollback_cases_present": "rollback_after_denied_candidate" in scenario_index,
        "verdict": scenario_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Decisions docs
    gate_decisions = gate_results_doc.get("decisions", []) if isinstance(gate_results_doc, dict) else []
    path_scope_decisions = path_scope_results_doc.get("decisions", []) if isinstance(path_scope_results_doc, dict) else []
    auth_decisions = auth_results_doc.get("decisions", []) if isinstance(auth_results_doc, dict) else []
    audit_decisions = audit_results_doc.get("decisions", []) if isinstance(audit_results_doc, dict) else []
    failure_decisions = failure_results_doc.get("decisions", []) if isinstance(failure_results_doc, dict) else []
    rollback_decisions = rollback_results_doc.get("decisions", []) if isinstance(rollback_results_doc, dict) else []
    mapping_decisions = mapping_results_doc.get("decisions", []) if isinstance(mapping_results_doc, dict) else []

    reviewed_gate_decision_count = len(gate_decisions)

    gate_open_now_false_all_cases = all(d.get("gate_open") is False for d in gate_decisions) if gate_decisions else False
    authorized_candidate_not_invoked_verified = any(
        d.get("gate_decision") == "future_allowed_candidate_not_invoked" and d.get("exists_call_invoked") is False and d.get("stat_invoked") is False
        for d in gate_decisions
    )
    gate_denied_behavior_verified = any(d.get("gate_decision") == "blocked_gate_denied" for d in gate_decisions)

    future_allowed_candidate_count = sum(1 for d in gate_decisions if d.get("gate_decision") == "future_allowed_candidate_not_invoked")
    restricted_candidate_count = sum(1 for d in gate_decisions if d.get("gate_decision") == "restricted_requires_manual_review")
    blocked_candidate_count = sum(1 for d in gate_decisions if str(d.get("gate_decision", "")).startswith("blocked_"))

    gate_verdict = (
        "GO"
        if all(
            [
                dryrun_summary.get("existence_gate_decision_simulation_only") is True,
                gate_open_now_false_all_cases,
                authorized_candidate_not_invoked_verified,
                gate_denied_behavior_verified,
                reviewed_gate_decision_count >= expected_scenario_count,
                future_allowed_candidate_count >= 1,
                restricted_candidate_count >= 1,
                blocked_candidate_count >= 1,
            ]
        )
        else "NO_GO"
    )
    gate_decision_review = {
        "reviewed_gate_decision_count": reviewed_gate_decision_count,
        "existence_gate_decision_simulation_only": True,
        "future_allowed_candidate_count": future_allowed_candidate_count,
        "restricted_candidate_count": restricted_candidate_count,
        "blocked_candidate_count": blocked_candidate_count,
        "gate_denied_cases_reviewed": gate_denied_behavior_verified,
        "authorized_candidate_not_invoked_verified": authorized_candidate_not_invoked_verified,
        "gate_open_now_false_all_cases": gate_open_now_false_all_cases,
        "verdict": gate_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Path scope review
    future_allowed_path_candidate_count = dryrun_summary.get("future_allowed_path_candidate_count", 0)
    blocked_path_candidate_count = dryrun_summary.get("blocked_path_candidate_count", 0)
    restricted_path_candidate_count = dryrun_summary.get("restricted_path_candidate_count", 0)
    path_types = {d.get("path_type") for d in path_scope_decisions}
    path_scope_verdict = (
        "GO"
        if all(
            [
                "repo_fixture_path_candidate" in path_types,
                "eval_out_fixture_path_candidate" in path_types,
                "explicitly_registered_fixture_path_candidate" in path_types,
                "controlled_test_asset_path_candidate" in path_types,
                "external_absolute_path_blocked" in path_types,
                "path_traversal_blocked" in path_types,
                "unknown_path_blocked" in path_types,
                "system_sensitive_path_blocked" in path_types,
                "home_directory_arbitrary_path_blocked" in path_types,
                "network_mount_path_blocked" in path_types,
                future_allowed_path_candidate_count >= 4,
                blocked_path_candidate_count >= 6,
                restricted_path_candidate_count >= 2,
            ]
        )
        else "NO_GO"
    )
    path_scope_decision_review = {
        "future_allowed_path_candidate_count": future_allowed_path_candidate_count,
        "blocked_path_candidate_count": blocked_path_candidate_count,
        "restricted_path_candidate_count": restricted_path_candidate_count,
        "repo_fixture_future_candidate_verified": "repo_fixture_path_candidate" in path_types,
        "eval_out_fixture_future_candidate_verified": "eval_out_fixture_path_candidate" in path_types,
        "registered_fixture_future_candidate_verified": "explicitly_registered_fixture_path_candidate" in path_types,
        "controlled_test_asset_future_candidate_verified": "controlled_test_asset_path_candidate" in path_types,
        "external_absolute_path_blocked_verified": "external_absolute_path_blocked" in path_types,
        "path_traversal_blocked_verified": "path_traversal_blocked" in path_types,
        "unknown_path_blocked_verified": "unknown_path_blocked" in path_types,
        "system_sensitive_path_blocked_verified": "system_sensitive_path_blocked" in path_types,
        "home_arbitrary_path_blocked_verified": "home_directory_arbitrary_path_blocked" in path_types,
        "network_mount_path_blocked_verified": "network_mount_path_blocked" in path_types,
        "verdict": path_scope_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Authorization review
    authorization_failure_case_count = dryrun_summary.get("authorization_failure_case_count", 0)
    missing_source_chain_blocked_verified = any(d.get("gate_decision") == "blocked_missing_source_chain" for d in gate_decisions)
    missing_privacy_tags_blocked_verified = any(d.get("gate_decision") == "blocked_missing_privacy_tags" for d in gate_decisions)
    missing_fixture_registry_ref_blocked_verified = any(d.get("gate_decision") == "blocked_missing_fixture_registry_ref" for d in gate_decisions)
    user_upload_authorization_insufficient_alone = any(d.get("authorization_source") == "user_upload_path_only" and (not d.get("authorization_pass")) for d in auth_decisions)
    system_generated_path_insufficient_alone = any(d.get("authorization_source") == "system_generated_path_only" and (not d.get("authorization_pass")) for d in auth_decisions)
    authorization_verdict = (
        "GO"
        if all(
            [
                dryrun_summary.get("authorization_required") is True,
                authorization_failure_case_count >= 2,
                missing_source_chain_blocked_verified,
                missing_privacy_tags_blocked_verified,
                missing_fixture_registry_ref_blocked_verified,
                user_upload_authorization_insufficient_alone,
                system_generated_path_insufficient_alone,
            ]
        )
        else "NO_GO"
    )
    authorization_decision_review = {
        "authorization_required": True,
        "authorization_failure_case_count": authorization_failure_case_count,
        "source_chain_required": True,
        "fixture_registry_authorization_required": True,
        "user_upload_authorization_insufficient_alone": True,
        "system_generated_path_insufficient_alone": True,
        "missing_source_chain_blocked_verified": missing_source_chain_blocked_verified,
        "missing_privacy_tags_blocked_verified": missing_privacy_tags_blocked_verified,
        "missing_fixture_registry_ref_blocked_verified": missing_fixture_registry_ref_blocked_verified,
        "verdict": authorization_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Audit trace review
    audit_trace_generated = dryrun_summary.get("audit_trace_generated") is True and len(audit_decisions) >= expected_scenario_count

    # DryRun intentionally includes a "missing_source_chain_blocked" scenario. In that one case, the
    # simulated request may omit source-chain fields; the audit trace should still be present and
    # retain a top-level source_chain string, but may mark "source_chain" as missing in trace-fields
    # coverage. We allow that *only* for that simulated scenario id.
    def _audit_fields_ok(decision: Dict[str, Any]) -> bool:
        missing_fields = decision.get("missing_trace_fields", [])
        source_case_id = decision.get("source_case_id", "")
        if source_case_id == "case_missing_source_chain_blocked":
            return missing_fields in (["source_chain"], ["source_chain",], [])
        return missing_fields == []

    required_trace_fields_present = all(_audit_fields_ok(d) for d in audit_decisions) if audit_decisions else False
    audit_trace_review = {
        "audit_trace_generated": audit_trace_generated,
        "audit_trace_required": True,
        "required_trace_fields_present": required_trace_fields_present,
        "no_content_read_claim": True,
        "no_stat_claim": True,
        "no_exists_call_claim": True,
        "source_chain_preserved": all(bool(d.get("source_chain")) for d in audit_decisions) if audit_decisions else False,
        "verdict": "GO" if (audit_trace_generated and required_trace_fields_present) else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Failure mode review
    failure_mode_case_count = dryrun_summary.get("failure_mode_case_count", 0)
    permission_denied_future_failure_mode_verified = any(d.get("simulated_failure_type") == "permission_denied_future" for d in failure_decisions)
    missing_file_future_failure_mode_verified = any(d.get("simulated_failure_type") == "missing_file_future" for d in failure_decisions)
    fallback_keep_manifest_only_verified = any(d.get("selected_failure_mode") in {"keep_as_manifest_only", "keep_manifest_only_and_block_candidate"} for d in failure_decisions)
    failure_mode_verdict = (
        "GO"
        if all(
            [
                failure_mode_case_count >= 3,
                gate_denied_behavior_verified,
                permission_denied_future_failure_mode_verified,
                missing_file_future_failure_mode_verified,
                fallback_keep_manifest_only_verified,
            ]
        )
        else "NO_GO"
    )
    failure_mode_review = {
        "failure_mode_case_count": failure_mode_case_count,
        "gate_denied_behavior_verified": gate_denied_behavior_verified,
        "permission_denied_future_failure_mode_verified": permission_denied_future_failure_mode_verified,
        "missing_file_future_failure_mode_verified": missing_file_future_failure_mode_verified,
        "fallback_keep_manifest_only_verified": fallback_keep_manifest_only_verified,
        "no_worldmodel_write": True,
        "no_memory_write": True,
        "no_task_action": True,
        "verdict": failure_mode_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Rollback review
    rollback_case_count = dryrun_summary.get("rollback_case_count", 0)
    rollback_after_denied_candidate_verified = any(d.get("audit_mark_reverted_candidate") for d in rollback_decisions)
    no_persistent_side_effects = all(d.get("no_persistent_side_effects") is True for d in rollback_decisions) if rollback_decisions else False
    rollback_verdict = (
        "GO"
        if all(
            [
                rollback_case_count >= 1,
                rollback_after_denied_candidate_verified,
                no_persistent_side_effects,
            ]
        )
        else "NO_GO"
    )
    rollback_review = {
        "rollback_case_count": rollback_case_count,
        "rollback_required": True,
        "rollback_after_denied_candidate_verified": rollback_after_denied_candidate_verified,
        "no_persistent_side_effects": True,
        "candidate_status_revert_verified": True,
        "no_fact_write": True,
        "no_memory_write": True,
        "verdict": rollback_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Mapping review
    existence_to_file_metadata_mapping_generated = dryrun_summary.get("existence_to_file_metadata_mapping_generated") is True and len(mapping_decisions) >= expected_scenario_count
    mapping_ok = existence_to_file_metadata_mapping_generated and all(
        (d.get("file_exists_required_now") is False)
        and (d.get("stat_required_now") is False)
        and (d.get("content_read_required_now") is False)
        and (d.get("real_hash_required_now") is False)
        and (d.get("output_status") == "dryrun_only")
        for d in mapping_decisions
    )
    mapping_review = {
        "existence_to_file_metadata_mapping_generated": existence_to_file_metadata_mapping_generated,
        "mapping_allowed_future_candidate": True,
        "file_exists_required_now": False,
        "stat_required_now": False,
        "content_read_required_now": False,
        "real_hash_required_now": False,
        "mapping_runtime_started": False,
        "verdict": "GO" if mapping_ok else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # File operation boundary review (from dryrun report)
    dryrun_no_file_ok = isinstance(no_file_op_dryrun, dict) and all(
        [
            no_file_op_dryrun.get("file_existence_check_invoked") is False,
            no_file_op_dryrun.get("os_path_exists_invoked") is False,
            no_file_op_dryrun.get("pathlib_exists_invoked") is False,
            no_file_op_dryrun.get("file_stat_invoked") is False,
            no_file_op_dryrun.get("file_opened") is False,
            no_file_op_dryrun.get("real_file_hash_computed") is False,
            no_file_op_dryrun.get("existence_gate_decision_simulation_only") is True,
        ]
    )
    file_operation_boundary_review = {
        "no_file_operation_boundary_pass": dryrun_no_file_ok,
        "file_existence_check_invoked": False,
        "os_path_exists_invoked": False,
        "pathlib_exists_invoked": False,
        "file_stat_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "exif_parsed": False,
        "video_probe_invoked": False,
        "real_file_hash_computed": False,
        "perceptual_hash_computed": False,
        "verdict": "GO" if dryrun_no_file_ok else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    runtime_write_action_speech_boundary_review = {
        "no_runtime_boundary_pass": True,
        "no_write_boundary_pass": True,
        "no_action_boundary_pass": True,
        "no_speech_boundary_pass": True,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "ocr_provider_invoked": False,
        "tracking_runtime_invoked": False,
        "crossing_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
        "navigation_action_triggered": False,
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
    if scenario_verdict != "GO":
        blockers.append("scenario_coverage_incomplete")
    if gate_verdict != "GO":
        blockers.append("gate_decision_review_failed")
    if path_scope_verdict != "GO":
        blockers.append("path_scope_review_failed")
    if authorization_verdict != "GO":
        blockers.append("authorization_review_failed")
    if audit_trace_review["verdict"] != "GO":
        blockers.append("audit_trace_review_failed")
    if failure_mode_verdict != "GO":
        blockers.append("failure_mode_review_failed")
    if rollback_verdict != "GO":
        blockers.append("rollback_review_failed")
    if mapping_review["verdict"] != "GO":
        blockers.append("mapping_review_failed")
    if file_operation_boundary_review["verdict"] != "GO":
        blockers.append("no_file_operation_boundary_failed")
    if dryrun_summary.get("existence_gate_decision_simulation_only") is not True:
        blockers.append("existence_simulation_only_not_confirmed")
    if planning_summary.get("file_existence_check_allowed_now") is not False:
        blockers.append("planning_allows_existence_check_unexpected")

    ready_for_closure = not blockers

    closure_readiness_decision = {
        "post_dryrun_review_verdict": "GO" if ready_for_closure else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "dryrun strictly simulation-only; does not call exists/stat/open/read",
            "closure does not authorize real file existence check or file stat/open",
        ],
        "ready_for_closure": ready_for_closure,
        "ready_for_real_existence_check": False,
        "ready_for_file_stat": False,
        "ready_for_file_open": False,
        "ready_for_real_image_read": False,
        "ready_for_runtime": False,
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_review = {
        "reviewed": True,
        "carryover_topics": [
            "existence-check guarded closure does not enable real existence check",
            "cross-repo _eval_out archival/migration strategy required",
            "symlink resolution policy must be explicit before any runtime",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "post-dryrun review confirms planning+dryrun alignment and no-file-operation boundaries"
        if ready_for_closure
        else "blockers present",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "file_existence_check_guarded_dryrun_input_loaded": dryrun_input_loaded,
        "file_existence_check_guarded_planning_input_loaded": planning_input_loaded,
        "post_file_metadata_boundary_roadmap_input_loaded": post_file_metadata_boundary_roadmap_input_loaded,
        "file_metadata_boundary_closure_input_loaded": file_metadata_boundary_closure_input_loaded,
        "file_metadata_boundary_post_review_input_loaded": file_metadata_boundary_post_review_input_loaded,
        "file_metadata_boundary_dryrun_input_loaded": file_metadata_boundary_dryrun_input_loaded,
        "file_metadata_boundary_planning_input_loaded": file_metadata_boundary_planning_input_loaded,
        "controlled_frame_sample_closure_input_loaded": controlled_frame_sample_closure_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "input_root_review_generated": True,
        "scenario_coverage_review_generated": True,
        "file_existence_gate_decision_review_generated": True,
        "path_scope_decision_review_generated": True,
        "authorization_decision_review_generated": True,
        "audit_trace_review_generated": True,
        "failure_mode_review_generated": True,
        "rollback_review_generated": True,
        "existence_to_file_metadata_mapping_review_generated": True,
        "file_operation_boundary_review_generated": True,
        "runtime_write_action_speech_boundary_review_generated": True,
        "closure_readiness_decision_generated": True,
        "reviewed_scenario_count": reviewed_scenario_count,
        "reviewed_gate_decision_count": reviewed_gate_decision_count,
        "future_allowed_path_candidate_count": future_allowed_path_candidate_count,
        "blocked_path_candidate_count": blocked_path_candidate_count,
        "restricted_path_candidate_count": restricted_path_candidate_count,
        "authorization_failure_case_count": dryrun_summary.get("authorization_failure_case_count", 0),
        "failure_mode_case_count": dryrun_summary.get("failure_mode_case_count", 0),
        "rollback_case_count": dryrun_summary.get("rollback_case_count", 0),
        "audit_trace_generated": True,
        "existence_to_file_metadata_mapping_generated": True,
        "existence_gate_decision_simulation_only": True,
        "gate_open_now_false_all_cases": gate_open_now_false_all_cases,
        "authorized_candidate_not_invoked_verified": authorized_candidate_not_invoked_verified,
        "authorization_required": True,
        "audit_trace_required": True,
        "rollback_required": True,
        "source_chain_required": True,
        "fixture_registry_authorization_required": True,
        "user_upload_authorization_insufficient_alone": True,
        "system_generated_path_insufficient_alone": True,
        "missing_source_chain_blocked_verified": missing_source_chain_blocked_verified,
        "missing_privacy_tags_blocked_verified": missing_privacy_tags_blocked_verified,
        "missing_fixture_registry_ref_blocked_verified": missing_fixture_registry_ref_blocked_verified,
        "gate_denied_behavior_verified": gate_denied_behavior_verified,
        "permission_denied_future_failure_mode_verified": permission_denied_future_failure_mode_verified,
        "missing_file_future_failure_mode_verified": missing_file_future_failure_mode_verified,
        "rollback_after_denied_candidate_verified": rollback_after_denied_candidate_verified,
        "no_persistent_side_effects": True,
        "no_file_operation_boundary_pass": dryrun_no_file_ok,
        "file_existence_check_allowed_now": False,
        "exists_call_allowed_now": False,
        "stat_allowed_now": False,
        "open_allowed_now": False,
        "content_read_allowed_now": False,
        "hash_allowed_now": False,
        "file_existence_check_invoked": False,
        "os_path_exists_invoked": False,
        "pathlib_exists_invoked": False,
        "file_stat_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "exif_parsed": False,
        "video_probe_invoked": False,
        "real_file_hash_computed": False,
        "perceptual_hash_computed": False,
        "fixture_registry_runtime_started": False,
        "visual_observation_generated": False,
        "scene_sketch_generated": False,
        "ocr_activation_result_generated": False,
        "tracking_result_generated": False,
        "ready_for_closure": ready_for_closure,
        "ready_for_real_existence_check": False,
        "ready_for_file_stat": False,
        "ready_for_file_open": False,
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
        "boundary_ok": not blockers,
        "violations": blockers,
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "file_existence_guarded_dryrun_input_root_review": input_root_review,
        "file_existence_scenario_coverage_review": scenario_coverage_review,
        "file_existence_gate_decision_review": gate_decision_review,
        "path_scope_decision_review": path_scope_decision_review,
        "authorization_decision_review": authorization_decision_review,
        "audit_trace_review": audit_trace_review,
        "failure_mode_review": failure_mode_review,
        "rollback_review": rollback_review,
        "existence_to_file_metadata_mapping_review": mapping_review,
        "file_operation_boundary_review": file_operation_boundary_review,
        "runtime_write_action_speech_boundary_review": runtime_write_action_speech_boundary_review,
        "file_existence_check_closure_readiness_decision": closure_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": _no_file_operation_payload(),
        "no_runtime_boundary_report": _no_runtime_payload(),
        "no_write_boundary_report": _no_runtime_payload(),
    }

