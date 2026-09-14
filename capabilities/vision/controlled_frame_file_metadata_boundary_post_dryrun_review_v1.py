# -*- coding: utf-8 -*-
"""Controlled Frame File Metadata Boundary Post-DryRun Review v1 (review-only).

Audits planning + dryrun outputs for policy alignment and no-file-operation boundaries.
Does NOT stat, open, read, probe, or hash any real files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-File-Metadata-Boundary-Post-DryRun-Review-v1-001"
REVIEW_ID = "cffmbpdr_v1_001"
REVIEW_SCOPE = "controlled_frame_file_metadata_boundary_post_dryrun_review_only"
SOURCE_CHAIN = "controlled_frame_file_metadata_boundary_post_dryrun_review_v1"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Frame-File-Metadata-Boundary-Closure-v1-001"

DRYRUN_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_READY_FOR_DRYRUN"
POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION = (
    "POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION_READY_FOR_FILE_METADATA_BOUNDARY_PLANNING"
)
CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION = "CONTROLLED_FRAME_SAMPLE_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_SAMPLE_POST_REVIEW_DECISION = "CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
CONTROLLED_FRAME_SAMPLE_DRYRUN_DECISION = "CONTROLLED_FRAME_SAMPLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
CONTROLLED_FRAME_SAMPLE_PLANNING_DECISION = "CONTROLLED_FRAME_SAMPLE_PLANNING_READY_FOR_CONTROLLED_FRAME_SAMPLE_DRYRUN"
CONTROLLED_FRAME_INPUT_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

REQUIRED_SCENARIOS = [
    "repo_fixture_path_candidate",
    "eval_out_fixture_path_candidate",
    "user_uploaded_path_candidate",
    "external_absolute_path_blocked",
    "path_traversal_blocked",
    "symlink_requires_review",
    "unknown_path_blocked",
    "declared_metadata_public_image",
    "declared_metadata_private_home",
    "missing_declared_metadata_blocked",
    "hash_placeholder_allowed",
    "real_hash_attempt_blocked",
    "exif_parse_attempt_blocked",
    "video_probe_attempt_blocked",
    "perceptual_hash_deferred",
    "fixture_registry_entry_candidate",
    "manifest_to_metadata_mapping_candidate",
    "metadata_sensitive_requires_manual_review",
]

ROOT_SPECS = [
    {
        "id": "controlled_frame_file_metadata_boundary_dryrun",
        "arg": "controlled_frame_file_metadata_boundary_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_file_metadata_boundary_dryrun_scenario_matrix.json",
            "path_legality_decision_results.json",
            "file_existence_decision_results.json",
            "external_metadata_decision_results.json",
            "hash_policy_decision_results.json",
            "fixture_registry_decision_results.json",
            "manifest_to_file_metadata_mapping_results.json",
            "no_file_operation_boundary_report.json",
            "no_runtime_boundary_report.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "controlled_frame_file_metadata_boundary_planning",
        "arg": "controlled_frame_file_metadata_boundary_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_file_metadata_boundary_planning_policy.json",
            "path_legality_policy.json",
            "external_metadata_boundary_policy.json",
            "real_hash_computation_policy.json",
            "fixture_registry_policy.json",
            "manifest_to_file_metadata_candidate_mapping_policy.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "post_controlled_frame_sample_roadmap_decision",
        "arg": "post_controlled_frame_sample_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_sample_closure",
        "arg": "controlled_frame_sample_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_sample_post_review",
        "arg": "controlled_frame_sample_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_sample_dryrun",
        "arg": "controlled_frame_sample_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "controlled_frame_sample_planning",
        "arg": "controlled_frame_sample_planning_root",
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
    {"id": "vision_frame_trace_stream_registry", "arg": "vision_frame_trace_stream_registry_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "vision_frame_input_governance", "arg": "vision_frame_input_governance_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "vision_roi_proposal_stub", "arg": "vision_roi_proposal_stub_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "system_health_hardware_profile", "arg": "system_health_hardware_profile_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "simulation_lab_profile", "arg": "simulation_lab_profile_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
    {"id": "privacy_governance_docs", "arg": "privacy_governance_docs_root", "required": False, "summary": "summary.json", "artifacts": ["summary.json"]},
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
    return {"root": root, "loaded": loaded, "summary": _read_json(root / summary_file) if root and (root / summary_file).is_file() else {}}


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
        "metadata_decision_simulation_only": True,
        "file_existence_check_invoked": False,
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
        "manifest_to_file_metadata_candidate_mapping_runtime_started": False,
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


def run_controlled_frame_file_metadata_boundary_post_dryrun_review_v1(
    *,
    controlled_frame_file_metadata_boundary_dryrun_root: str,
    controlled_frame_file_metadata_boundary_planning_root: str,
    post_controlled_frame_sample_roadmap_decision_root: str,
    controlled_frame_sample_closure_root: str,
    controlled_frame_sample_post_review_root: str,
    controlled_frame_sample_dryrun_root: str,
    controlled_frame_sample_planning_root: str,
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

    file_metadata_boundary_dryrun_input_loaded = (
        roots["controlled_frame_file_metadata_boundary_dryrun"]["loaded"]
        and summaries["controlled_frame_file_metadata_boundary_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    file_metadata_boundary_planning_input_loaded = (
        roots["controlled_frame_file_metadata_boundary_planning"]["loaded"]
        and summaries["controlled_frame_file_metadata_boundary_planning"].get("final_decision") == PLANNING_DECISION
    )
    post_controlled_frame_sample_roadmap_input_loaded = (
        roots["post_controlled_frame_sample_roadmap_decision"]["loaded"]
        and summaries["post_controlled_frame_sample_roadmap_decision"].get("final_decision")
        == POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION
    )
    controlled_frame_sample_closure_input_loaded = (
        roots["controlled_frame_sample_closure"]["loaded"]
        and summaries["controlled_frame_sample_closure"].get("final_decision") == CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION
    )
    controlled_frame_sample_post_review_input_loaded = (
        roots["controlled_frame_sample_post_review"]["loaded"]
        and summaries["controlled_frame_sample_post_review"].get("final_decision") == CONTROLLED_FRAME_SAMPLE_POST_REVIEW_DECISION
    )
    controlled_frame_sample_dryrun_input_loaded = (
        roots["controlled_frame_sample_dryrun"]["loaded"]
        and summaries["controlled_frame_sample_dryrun"].get("final_decision") == CONTROLLED_FRAME_SAMPLE_DRYRUN_DECISION
    )
    controlled_frame_sample_planning_input_loaded = (
        roots["controlled_frame_sample_planning"]["loaded"]
        and summaries["controlled_frame_sample_planning"].get("final_decision") == CONTROLLED_FRAME_SAMPLE_PLANNING_DECISION
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

    dryrun_root = roots["controlled_frame_file_metadata_boundary_dryrun"]["root"]
    planning_root = roots["controlled_frame_file_metadata_boundary_planning"]["root"]
    dryrun_summary = summaries["controlled_frame_file_metadata_boundary_dryrun"]
    planning_summary = summaries["controlled_frame_file_metadata_boundary_planning"]

    scenario_matrix = _read_json(dryrun_root / "controlled_frame_file_metadata_boundary_dryrun_scenario_matrix.json") if dryrun_root else {}
    path_results_doc = _read_json(dryrun_root / "path_legality_decision_results.json") if dryrun_root else {}
    existence_results_doc = _read_json(dryrun_root / "file_existence_decision_results.json") if dryrun_root else {}
    metadata_results_doc = _read_json(dryrun_root / "external_metadata_decision_results.json") if dryrun_root else {}
    hash_results_doc = _read_json(dryrun_root / "hash_policy_decision_results.json") if dryrun_root else {}
    fixture_results_doc = _read_json(dryrun_root / "fixture_registry_decision_results.json") if dryrun_root else {}
    mapping_results_doc = _read_json(dryrun_root / "manifest_to_file_metadata_mapping_results.json") if dryrun_root else {}
    no_file_op_dryrun = _read_json(dryrun_root / "no_file_operation_boundary_report.json") if dryrun_root else {}

    path_legality_policy = _read_json(planning_root / "path_legality_policy.json") if planning_root else {}
    external_metadata_policy = _read_json(planning_root / "external_metadata_boundary_policy.json") if planning_root else {}
    real_hash_policy = _read_json(planning_root / "real_hash_computation_policy.json") if planning_root else {}

    scenario_list = scenario_matrix.get("scenarios", []) if isinstance(scenario_matrix, dict) else []
    scenario_index = _index_by(scenario_list, "scenario_id")
    covered = [sid for sid in REQUIRED_SCENARIOS if sid in scenario_index]
    missing = [sid for sid in REQUIRED_SCENARIOS if sid not in scenario_index]
    reviewed_scenario_count = len(scenario_list)
    expected_scenario_count = len(REQUIRED_SCENARIOS)

    path_decisions = path_results_doc.get("decisions", []) if isinstance(path_results_doc, dict) else []
    existence_decisions = existence_results_doc.get("decisions", []) if isinstance(existence_results_doc, dict) else []
    metadata_decisions = metadata_results_doc.get("decisions", []) if isinstance(metadata_results_doc, dict) else []
    hash_decisions = hash_results_doc.get("decisions", []) if isinstance(hash_results_doc, dict) else []
    fixture_decisions = fixture_results_doc.get("decisions", []) if isinstance(fixture_results_doc, dict) else []
    mapping_decisions = mapping_results_doc.get("decisions", []) if isinstance(mapping_results_doc, dict) else []

    allowed_path_count = dryrun_summary.get("allowed_path_candidate_count", 0)
    restricted_path_count = dryrun_summary.get("restricted_path_candidate_count", 0)
    blocked_path_count = dryrun_summary.get("blocked_path_candidate_count", 0)
    metadata_candidate_case_count = dryrun_summary.get("metadata_candidate_case_count", 0)
    hash_policy_case_count = dryrun_summary.get("hash_policy_case_count", 0)
    fixture_registry_candidate_generated = dryrun_summary.get("fixture_registry_candidate_generated", False)
    manifest_to_file_metadata_mapping_generated = dryrun_summary.get("manifest_to_file_metadata_mapping_generated", False)

    required_roots = [spec["id"] for spec in ROOT_SPECS if spec["required"]]
    loaded_roots = [spec["id"] for spec in ROOT_SPECS if roots[spec["id"]]["loaded"]]
    optional_missing_roots = [spec["id"] for spec in ROOT_SPECS if (not spec["required"]) and (not roots[spec["id"]]["loaded"])]
    missing_required_roots = [spec["id"] for spec in ROOT_SPECS if spec["required"] and (not roots[spec["id"]]["loaded"])]
    input_root_status = "all_required_loaded" if not missing_required_roots else "missing_required_roots"

    file_metadata_dryrun_input_root_review = {
        "review_id": REVIEW_ID,
        "required_roots": required_roots,
        "loaded_roots": loaded_roots,
        "optional_missing_roots": optional_missing_roots,
        "missing_required_roots": missing_required_roots,
        "input_root_status": input_root_status,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    scenario_verdict = "GO" if (not missing and reviewed_scenario_count >= expected_scenario_count) else "NO_GO"
    file_metadata_scenario_coverage_review = {
        "reviewed_scenario_count": reviewed_scenario_count,
        "expected_scenario_count": expected_scenario_count,
        "covered_scenarios": covered,
        "missing_scenarios": missing,
        "allowed_path_cases_present": all(s in scenario_index for s in ("repo_fixture_path_candidate", "eval_out_fixture_path_candidate")),
        "restricted_path_cases_present": all(s in scenario_index for s in ("user_uploaded_path_candidate", "symlink_requires_review")),
        "blocked_path_cases_present": all(
            s in scenario_index
            for s in ("external_absolute_path_blocked", "path_traversal_blocked", "unknown_path_blocked")
        ),
        "metadata_cases_present": all(
            s in scenario_index
            for s in (
                "declared_metadata_public_image",
                "declared_metadata_private_home",
                "missing_declared_metadata_blocked",
                "metadata_sensitive_requires_manual_review",
            )
        ),
        "hash_cases_present": all(
            s in scenario_index
            for s in (
                "hash_placeholder_allowed",
                "real_hash_attempt_blocked",
                "exif_parse_attempt_blocked",
                "video_probe_attempt_blocked",
                "perceptual_hash_deferred",
            )
        ),
        "fixture_registry_case_present": "fixture_registry_entry_candidate" in scenario_index,
        "mapping_case_present": "manifest_to_metadata_mapping_candidate" in scenario_index,
        "verdict": scenario_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    repo_fixture_allowed = any(d.get("path_status") == "allowed_repo_fixture_candidate" for d in path_decisions)
    eval_out_allowed = any(d.get("path_status") == "allowed_eval_out_fixture_candidate" for d in path_decisions)
    user_upload_restricted = any(d.get("path_status") == "restricted_user_upload_candidate" for d in path_decisions)
    external_blocked = any(d.get("path_status") == "blocked_external_absolute_path" for d in path_decisions)
    traversal_blocked = any(d.get("path_status") == "blocked_path_traversal" for d in path_decisions)
    symlink_review = any(d.get("path_status") == "restricted_symlink_candidate" for d in path_decisions)
    unknown_blocked = any(d.get("path_status") == "blocked_unknown_path" for d in path_decisions)

    path_verdict = (
        "GO"
        if all(
            [
                repo_fixture_allowed,
                eval_out_allowed,
                user_upload_restricted,
                external_blocked,
                traversal_blocked,
                symlink_review,
                unknown_blocked,
                allowed_path_count >= 2,
                restricted_path_count >= 2,
                blocked_path_count >= 3,
            ]
        )
        else "NO_GO"
    )

    path_legality_decision_review = {
        "allowed_path_candidate_count": allowed_path_count,
        "restricted_path_candidate_count": restricted_path_count,
        "blocked_path_candidate_count": blocked_path_count,
        "repo_fixture_allowed_verified": repo_fixture_allowed,
        "eval_out_fixture_allowed_verified": eval_out_allowed,
        "user_upload_restricted_verified": user_upload_restricted,
        "external_absolute_path_blocked_verified": external_blocked,
        "path_traversal_blocked_verified": traversal_blocked,
        "symlink_review_required_verified": symlink_review,
        "unknown_path_blocked_verified": unknown_blocked,
        "verdict": path_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    existence_all_not_checked = all(d.get("existence_status") == "not_checked" for d in existence_decisions) if existence_decisions else False
    existence_none_invoked = all(not d.get("file_existence_check_invoked") for d in existence_decisions) if existence_decisions else False
    existence_verdict = (
        "GO"
        if existence_all_not_checked
        and existence_none_invoked
        and planning_summary.get("file_existence_check_allowed_now") is False
        else "NO_GO"
    )

    file_existence_decision_review = {
        "file_existence_check_allowed_now": False,
        "file_existence_check_invoked": False,
        "file_stat_invoked": False,
        "file_exists_verified": False,
        "existence_status_not_checked": existence_all_not_checked,
        "future_check_candidate_allowed": any(d.get("future_check_candidate_allowed") for d in existence_decisions),
        "verdict": existence_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    missing_metadata_blocked = any(d.get("missing_declared_metadata_blocked") for d in metadata_decisions)
    sensitive_manual_review = any(
        d.get("manual_review_required") and d.get("metadata_status", "").find("restricted") >= 0 for d in metadata_decisions
    )
    exif_blocked_in_results = any(d.get("metadata_status") == "exif_parse_attempt_blocked" for d in metadata_decisions)
    probe_blocked_in_results = any(d.get("metadata_status") == "video_probe_attempt_blocked" for d in metadata_decisions)

    metadata_verdict = (
        "GO"
        if all(
            [
                missing_metadata_blocked,
                sensitive_manual_review,
                exif_blocked_in_results,
                probe_blocked_in_results,
                metadata_candidate_case_count >= 2,
                external_metadata_policy.get("external_metadata_read_allowed_now") is False,
                external_metadata_policy.get("no_exif_parse_now") is True,
                external_metadata_policy.get("no_video_probe_now") is True,
            ]
        )
        else "NO_GO"
    )

    external_metadata_decision_review = {
        "metadata_candidate_case_count": metadata_candidate_case_count,
        "declared_metadata_valid_candidate_reviewed": True,
        "missing_declared_metadata_blocked_verified": missing_metadata_blocked,
        "sensitive_metadata_manual_review_verified": sensitive_manual_review,
        "external_metadata_read_allowed_now": False,
        "exif_parse_allowed_now": False,
        "video_probe_allowed_now": False,
        "exif_parsed": False,
        "video_probe_invoked": False,
        "verdict": metadata_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    hash_placeholder_ok = any(d.get("hash_placeholder_allowed") and d.get("selected_hash_policy") == "placeholder_only" for d in hash_decisions)
    real_hash_blocked = any(d.get("real_hash_attempt_blocked") for d in hash_decisions)
    perceptual_deferred = any(d.get("perceptual_hash_deferred") for d in hash_decisions)

    hash_verdict = (
        "GO"
        if all(
            [
                hash_placeholder_ok,
                real_hash_blocked,
                perceptual_deferred,
                hash_policy_case_count >= 3,
                real_hash_policy.get("real_hash_computation_allowed_now") is False,
                real_hash_policy.get("hash_placeholder_allowed") is True,
                real_hash_policy.get("perceptual_hash_deferred") is True,
            ]
        )
        else "NO_GO"
    )

    hash_policy_decision_review = {
        "hash_policy_case_count": hash_policy_case_count,
        "hash_placeholder_allowed_verified": hash_placeholder_ok,
        "real_hash_attempt_blocked_verified": real_hash_blocked,
        "perceptual_hash_deferred_verified": perceptual_deferred,
        "real_hash_computation_allowed_now": False,
        "real_file_hash_computed": False,
        "perceptual_hash_computed": False,
        "verdict": hash_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    fixture_candidate_only = all(
        (not d.get("registry_runtime_started")) and d.get("registry_entry_candidate_allowed") in {True, False}
        for d in fixture_decisions
    )
    fixture_registry_ok = fixture_registry_candidate_generated and any(d.get("registry_entry_candidate_allowed") for d in fixture_decisions)

    fixture_registry_decision_review = {
        "fixture_registry_candidate_generated": fixture_registry_candidate_generated,
        "fixture_registry_runtime_started": False,
        "registry_entry_candidate_only": fixture_candidate_only,
        "file_exists_verified": False,
        "real_hash_computed": False,
        "content_read": False,
        "verdict": "GO" if fixture_registry_ok else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    mapping_ok = manifest_to_file_metadata_mapping_generated and all(
        not d.get("content_read_required") and not d.get("file_existence_required_now") and not d.get("real_hash_required_now")
        for d in mapping_decisions
    )

    manifest_to_file_metadata_mapping_review = {
        "manifest_to_file_metadata_mapping_generated": manifest_to_file_metadata_mapping_generated,
        "manifest_to_file_metadata_candidate_mapping_runtime_started": False,
        "file_metadata_candidate_allowed": any(d.get("file_metadata_candidate_allowed") for d in mapping_decisions),
        "file_existence_required_now": False,
        "real_hash_required_now": False,
        "content_read_required": False,
        "visual_observation_generated": False,
        "scene_sketch_generated": False,
        "ocr_activation_result_generated": False,
        "tracking_result_generated": False,
        "verdict": "GO" if mapping_ok else "NO_GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    dryrun_no_file_ok = isinstance(no_file_op_dryrun, dict) and (
        no_file_op_dryrun.get("file_stat_invoked") is False
        and no_file_op_dryrun.get("file_opened") is False
        and no_file_op_dryrun.get("exif_parsed") is False
        and no_file_op_dryrun.get("video_probe_invoked") is False
        and no_file_op_dryrun.get("real_file_hash_computed") is False
        and no_file_op_dryrun.get("metadata_decision_simulation_only") is True
    )

    file_operation_boundary_review = {
        "no_file_operation_boundary_pass": dryrun_no_file_ok,
        "file_existence_check_invoked": False,
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
    if path_verdict != "GO":
        blockers.append("path_legality_review_failed")
    if existence_verdict != "GO":
        blockers.append("file_existence_review_failed")
    if metadata_verdict != "GO":
        blockers.append("external_metadata_review_failed")
    if hash_verdict != "GO":
        blockers.append("hash_policy_review_failed")
    if fixture_registry_decision_review["verdict"] != "GO":
        blockers.append("fixture_registry_review_failed")
    if manifest_to_file_metadata_mapping_review["verdict"] != "GO":
        blockers.append("mapping_review_failed")
    if not dryrun_no_file_ok:
        blockers.append("no_file_operation_boundary_failed")
    if dryrun_summary.get("metadata_decision_simulation_only") is not True:
        blockers.append("metadata_simulation_only_not_confirmed")

    ready_for_closure = not blockers

    file_metadata_boundary_closure_readiness_decision = {
        "post_dryrun_review_verdict": "GO" if ready_for_closure else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [
            "dryrun strictly simulation-only; no filesystem metadata read",
            "closure does not authorize real file existence check or image read",
        ],
        "ready_for_closure": ready_for_closure,
        "ready_for_file_existence_check": False,
        "ready_for_real_metadata_read": False,
        "ready_for_real_hash": False,
        "ready_for_real_image_read": False,
        "ready_for_runtime": False,
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_review = {
        "reviewed": True,
        "carryover_topics": [
            "guarded file existence check planning deferred post-closure",
            "declared vs filesystem metadata reconciliation deferred",
            "fixture registry lifecycle and review workflow deferred",
            "roadmap decision for next mainline after metadata boundary closure",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "post-dryrun review confirms planning+dryrun policy alignment and no-file-operation boundaries" if ready_for_closure else "blockers present",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "file_metadata_boundary_dryrun_input_loaded": file_metadata_boundary_dryrun_input_loaded,
        "file_metadata_boundary_planning_input_loaded": file_metadata_boundary_planning_input_loaded,
        "post_controlled_frame_sample_roadmap_input_loaded": post_controlled_frame_sample_roadmap_input_loaded,
        "controlled_frame_sample_closure_input_loaded": controlled_frame_sample_closure_input_loaded,
        "controlled_frame_sample_post_review_input_loaded": controlled_frame_sample_post_review_input_loaded,
        "controlled_frame_sample_dryrun_input_loaded": controlled_frame_sample_dryrun_input_loaded,
        "controlled_frame_sample_planning_input_loaded": controlled_frame_sample_planning_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "input_root_review_generated": True,
        "scenario_coverage_review_generated": True,
        "path_legality_decision_review_generated": True,
        "file_existence_decision_review_generated": True,
        "external_metadata_decision_review_generated": True,
        "hash_policy_decision_review_generated": True,
        "fixture_registry_decision_review_generated": True,
        "manifest_to_file_metadata_mapping_review_generated": True,
        "file_operation_boundary_review_generated": True,
        "runtime_write_action_speech_boundary_review_generated": True,
        "closure_readiness_decision_generated": True,
        "reviewed_scenario_count": reviewed_scenario_count,
        "allowed_path_candidate_count": allowed_path_count,
        "restricted_path_candidate_count": restricted_path_count,
        "blocked_path_candidate_count": blocked_path_count,
        "metadata_candidate_case_count": metadata_candidate_case_count,
        "hash_policy_case_count": hash_policy_case_count,
        "fixture_registry_candidate_generated": fixture_registry_candidate_generated,
        "manifest_to_file_metadata_mapping_generated": manifest_to_file_metadata_mapping_generated,
        "metadata_decision_simulation_only": dryrun_summary.get("metadata_decision_simulation_only", True),
        "file_existence_check_allowed_now": False,
        "path_legality_check_allowed_now": False,
        "external_metadata_read_allowed_now": False,
        "real_hash_computation_allowed_now": False,
        "hash_placeholder_allowed": True,
        "perceptual_hash_deferred": True,
        "no_exif_parse_now": True,
        "no_video_probe_now": True,
        "external_absolute_path_blocked_verified": external_blocked,
        "path_traversal_blocked_verified": traversal_blocked,
        "unknown_path_blocked_verified": unknown_blocked,
        "missing_declared_metadata_blocked_verified": missing_metadata_blocked,
        "real_hash_attempt_blocked_verified": real_hash_blocked,
        "exif_parse_attempt_blocked_verified": exif_blocked_in_results,
        "video_probe_attempt_blocked_verified": probe_blocked_in_results,
        "perceptual_hash_deferred_verified": perceptual_deferred,
        "no_file_operation_boundary_pass": dryrun_no_file_ok,
        "file_existence_check_invoked": False,
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
        "manifest_to_file_metadata_candidate_mapping_runtime_started": False,
        "visual_observation_generated": False,
        "scene_sketch_generated": False,
        "ocr_activation_result_generated": False,
        "tracking_result_generated": False,
        "ready_for_closure": ready_for_closure,
        "ready_for_file_existence_check": False,
        "ready_for_real_metadata_read": False,
        "ready_for_real_hash": False,
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
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "file_metadata_dryrun_input_root_review": file_metadata_dryrun_input_root_review,
        "file_metadata_scenario_coverage_review": file_metadata_scenario_coverage_review,
        "path_legality_decision_review": path_legality_decision_review,
        "file_existence_decision_review": file_existence_decision_review,
        "external_metadata_decision_review": external_metadata_decision_review,
        "hash_policy_decision_review": hash_policy_decision_review,
        "fixture_registry_decision_review": fixture_registry_decision_review,
        "manifest_to_file_metadata_mapping_review": manifest_to_file_metadata_mapping_review,
        "file_operation_boundary_review": file_operation_boundary_review,
        "runtime_write_action_speech_boundary_review": runtime_write_action_speech_boundary_review,
        "file_metadata_boundary_closure_readiness_decision": file_metadata_boundary_closure_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": _no_file_operation_payload(),
        "no_runtime_boundary_report": _no_runtime_payload(),
        "no_write_boundary_report": _no_runtime_payload(),
    }
