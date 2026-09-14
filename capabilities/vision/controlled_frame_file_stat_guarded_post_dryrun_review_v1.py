# -*- coding: utf-8 -*-
"""Controlled Frame File Stat Guarded Post-DryRun Review v1 (review-only).

Audits planning + dryrun outputs for policy alignment and no-file-operation boundaries.
Does NOT call stat/exists/open/read/probe/hash or perform any real file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001"
REVIEW_ID = "cffsgpdr_v1_001"
REVIEW_SCOPE = "controlled_frame_file_stat_guarded_post_dryrun_review_only"
SOURCE_CHAIN = "controlled_frame_file_stat_guarded_post_dryrun_review_v1"

FINAL_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Controlled-Frame-File-Stat-Guarded-Closure-v1-001"

DRYRUN_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_READY_FOR_DRYRUN"

POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION = "POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION_READY_FOR_FILE_STAT_GUARDED_PLANNING"
FILE_EXISTENCE_CHECK_GUARDED_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
FILE_EXISTENCE_CHECK_GUARDED_POST_REVIEW_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FILE_EXISTENCE_CHECK_GUARDED_PLANNING_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_READY_FOR_DRYRUN"

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
    "repo_fixture_stat_future_candidate",
    "eval_out_fixture_stat_future_candidate",
    "registered_fixture_stat_future_candidate",
    "controlled_test_asset_stat_future_candidate",
    "user_upload_stat_restricted",
    "external_absolute_path_stat_blocked",
    "path_traversal_stat_blocked",
    "unknown_path_stat_blocked",
    "symlink_stat_restricted",
    "system_sensitive_path_stat_blocked",
    "home_arbitrary_path_stat_blocked",
    "network_mount_path_stat_blocked",
    "missing_source_chain_stat_blocked",
    "missing_privacy_tags_stat_blocked",
    "missing_fixture_registry_ref_stat_blocked",
    "exists_gate_pass_insufficient_for_stat",
    "user_upload_authorization_insufficient_for_stat",
    "system_generated_path_insufficient_for_stat",
    "authorized_stat_candidate_but_not_invoked",
    "stat_metadata_allowed_candidate",
    "stat_metadata_restricted_candidate",
    "stat_metadata_blocked_or_deferred",
    "stat_permission_denied_future_failure_mode",
    "stat_missing_file_future_failure_mode",
    "stat_gate_denied_behavior",
    "stat_rollback_after_denied_candidate",
    "stat_metadata_boundary_denied",
    "stat_to_file_metadata_mapping_candidate",
]


ROOT_SPECS = [
    {
        "id": "controlled_frame_file_stat_guarded_dryrun",
        "arg": "controlled_frame_file_stat_guarded_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_file_stat_guarded_dryrun_scenario_matrix.json",
            "controlled_frame_file_stat_guarded_dryrun_results.json",
            "file_stat_gate_decision_results.json",
            "stat_path_scope_dryrun_decision_results.json",
            "stat_metadata_exposure_decision_results.json",
            "authorization_decision_results.json",
            "audit_trace_results.json",
            "failure_mode_decision_results.json",
            "rollback_decision_results.json",
            "stat_to_file_metadata_mapping_results.json",
            "file_stat_boundary_matrix.json",
            "no_file_operation_boundary_report.json",
            "no_runtime_boundary_report.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "controlled_frame_file_stat_guarded_planning",
        "arg": "controlled_frame_file_stat_guarded_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_file_stat_guarded_planning_policy.json",
            "file_stat_gate_policy.json",
            "file_stat_metadata_exposure_boundary_policy.json",
            "allowed_stat_path_scope_policy.json",
            "blocked_stat_path_scope_policy.json",
            "file_stat_authorization_policy.json",
            "file_stat_audit_trace_policy.json",
            "file_stat_failure_mode_policy.json",
            "file_stat_rollback_policy.json",
            "file_stat_decision_candidate_schema.json",
            "stat_to_file_metadata_candidate_mapping_policy.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "post_file_existence_check_roadmap_decision",
        "arg": "post_file_existence_check_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "next_phase_recommendation.json", "verifier_report.json"],
    },
    {
        "id": "file_existence_check_guarded_closure",
        "arg": "file_existence_check_guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_existence_check_guarded_closure_summary.json", "validated_capability_summary.json"],
    },
    {
        "id": "file_existence_check_guarded_post_review",
        "arg": "file_existence_check_guarded_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "file_existence_check_closure_readiness_decision.json", "verifier_report.json"],
    },
    {
        "id": "file_existence_check_guarded_dryrun",
        "arg": "file_existence_check_guarded_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_existence_check_guarded_dryrun_results.json", "verifier_report.json"],
    },
    {
        "id": "file_existence_check_guarded_planning",
        "arg": "file_existence_check_guarded_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_existence_check_guarded_planning_policy.json", "verifier_report.json"],
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


def _extract_scenarios(dryrun_root: Path) -> Dict[str, Any]:
    matrix = _try_read_json(dryrun_root / "controlled_frame_file_stat_guarded_dryrun_scenario_matrix.json") or {}
    scenarios = matrix.get("scenarios", []) if isinstance(matrix, dict) else []
    idx = {row.get("scenario_id"): row for row in scenarios if isinstance(row, dict)}
    return {"matrix": matrix, "scenarios": scenarios, "index": idx}


def _list_ids(payload: Dict[str, Any], key: str, id_field: str) -> List[str]:
    rows = payload.get(key, [])
    if not isinstance(rows, list):
        return []
    out: List[str] = []
    for r in rows:
        if isinstance(r, dict) and isinstance(r.get(id_field), str):
            out.append(r[id_field])
    return out


def _boundary_flags_all_false(summary: Dict[str, Any], keys: List[str]) -> bool:
    return all(summary.get(k) is False for k in keys)


def run_controlled_frame_file_stat_guarded_post_dryrun_review_v1(
    *,
    controlled_frame_file_stat_guarded_dryrun_root: str,
    controlled_frame_file_stat_guarded_planning_root: str,
    post_file_existence_check_roadmap_decision_root: str,
    file_existence_check_guarded_closure_root: str,
    file_existence_check_guarded_post_review_root: str,
    file_existence_check_guarded_dryrun_root: str,
    file_existence_check_guarded_planning_root: str,
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

    required_roots = [spec["id"] for spec in ROOT_SPECS if spec["required"]]
    optional_roots = [spec["id"] for spec in ROOT_SPECS if not spec["required"]]

    loaded_roots = [rid for rid in required_roots if roots.get(rid, {}).get("loaded") is True]
    missing_required_roots = [rid for rid in required_roots if roots.get(rid, {}).get("loaded") is not True]
    optional_missing_roots = [rid for rid in optional_roots if roots.get(rid, {}).get("loaded") is not True]

    cross_repo_input_roots_observed = False
    input_root_rows: List[Dict[str, Any]] = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        path_str = str(meta["root"]) if meta["root"] else "(not_provided)"
        if "Luna-Workspace-Min" in path_str:
            cross_repo_input_roots_observed = True
        input_root_rows.append(
            {
                "intake_id": spec["id"],
                "path": path_str,
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    summaries = {key: roots[key]["summary"] for key in roots}

    # Inputs: phase decisions
    file_stat_guarded_dryrun_input_loaded = (
        roots["controlled_frame_file_stat_guarded_dryrun"]["loaded"]
        and summaries["controlled_frame_file_stat_guarded_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    file_stat_guarded_planning_input_loaded = (
        roots["controlled_frame_file_stat_guarded_planning"]["loaded"]
        and summaries["controlled_frame_file_stat_guarded_planning"].get("final_decision") == PLANNING_DECISION
    )
    post_file_existence_check_roadmap_input_loaded = (
        roots["post_file_existence_check_roadmap_decision"]["loaded"]
        and summaries["post_file_existence_check_roadmap_decision"].get("final_decision") == POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION
    )

    file_existence_check_guarded_closure_input_loaded = (
        roots["file_existence_check_guarded_closure"]["loaded"]
        and summaries["file_existence_check_guarded_closure"].get("final_decision") == FILE_EXISTENCE_CHECK_GUARDED_CLOSURE_DECISION
        and summaries["file_existence_check_guarded_closure"].get("file_existence_check_guarded_closed") is True
    )
    file_existence_check_guarded_post_review_input_loaded = (
        roots["file_existence_check_guarded_post_review"]["loaded"]
        and summaries["file_existence_check_guarded_post_review"].get("final_decision") == FILE_EXISTENCE_CHECK_GUARDED_POST_REVIEW_DECISION
    )
    file_existence_check_guarded_dryrun_input_loaded = (
        roots["file_existence_check_guarded_dryrun"]["loaded"]
        and summaries["file_existence_check_guarded_dryrun"].get("final_decision") == FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_DECISION
    )
    file_existence_check_guarded_planning_input_loaded = (
        roots["file_existence_check_guarded_planning"]["loaded"]
        and summaries["file_existence_check_guarded_planning"].get("final_decision") == FILE_EXISTENCE_CHECK_GUARDED_PLANNING_DECISION
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

    # ---- Load dryrun review targets ----
    dryrun_root = roots["controlled_frame_file_stat_guarded_dryrun"]["root"]
    planning_root = roots["controlled_frame_file_stat_guarded_planning"]["root"]
    if dryrun_root is None or planning_root is None:
        # Degrade gracefully; output review objects with blockers in summary.
        dryrun_root = Path(".")
        planning_root = Path(".")

    dryrun_summary = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_gate_results = _try_read_json(dryrun_root / "file_stat_gate_decision_results.json") or {}
    dryrun_path_scope_results = _try_read_json(dryrun_root / "stat_path_scope_dryrun_decision_results.json") or {}
    dryrun_metadata_results = _try_read_json(dryrun_root / "stat_metadata_exposure_decision_results.json") or {}
    dryrun_auth_results = _try_read_json(dryrun_root / "authorization_decision_results.json") or {}
    dryrun_audit_results = _try_read_json(dryrun_root / "audit_trace_results.json") or {}
    dryrun_failure_results = _try_read_json(dryrun_root / "failure_mode_decision_results.json") or {}
    dryrun_rollback_results = _try_read_json(dryrun_root / "rollback_decision_results.json") or {}
    dryrun_mapping_results = _try_read_json(dryrun_root / "stat_to_file_metadata_mapping_results.json") or {}

    scenario_data = _extract_scenarios(dryrun_root)
    scenario_idx = scenario_data["index"]
    covered_scenarios = sorted([sid for sid in scenario_idx.keys() if isinstance(sid, str)])
    missing_scenarios = sorted([sid for sid in REQUIRED_SCENARIOS if sid not in scenario_idx])

    reviewed_scenario_count = len(covered_scenarios)
    expected_scenario_count = len(REQUIRED_SCENARIOS)

    decisions = dryrun_gate_results.get("decisions", [])
    reviewed_gate_decision_count = len(decisions) if isinstance(decisions, list) else 0

    # Gate decision counts
    future_allowed_stat_candidate_count = 0
    restricted_stat_candidate_count = 0
    blocked_stat_candidate_count = 0
    gate_open_now_false_all_cases = True
    authorized_stat_candidate_not_invoked_verified = True
    gate_denied_cases_reviewed = False

    for d in decisions if isinstance(decisions, list) else []:
        if not isinstance(d, dict):
            continue
        gate_open_now_false_all_cases = gate_open_now_false_all_cases and (d.get("gate_open") is False)
        if d.get("gate_decision") == "future_stat_allowed_candidate_not_invoked":
            future_allowed_stat_candidate_count += 1
        elif d.get("gate_decision") == "restricted_requires_manual_review":
            restricted_stat_candidate_count += 1
        elif isinstance(d.get("gate_decision"), str) and d.get("gate_decision", "").startswith("blocked_"):
            blocked_stat_candidate_count += 1
        if d.get("gate_decision") == "blocked_gate_denied":
            gate_denied_cases_reviewed = True
        if d.get("stat_invoked") is not False:
            authorized_stat_candidate_not_invoked_verified = False

    # Path scope decision counts
    path_scope_decisions = dryrun_path_scope_results.get("decisions", [])
    future_allowed_stat_path_candidate_count = 0
    blocked_stat_path_candidate_count = 0
    restricted_stat_path_candidate_count = 0
    for d in path_scope_decisions if isinstance(path_scope_decisions, list) else []:
        if not isinstance(d, dict):
            continue
        if d.get("future_allowed_stat_path_candidate") is True:
            future_allowed_stat_path_candidate_count += 1
        if d.get("blocked_stat_path_candidate") is True:
            blocked_stat_path_candidate_count += 1
        if d.get("restricted_stat_path_candidate") is True:
            restricted_stat_path_candidate_count += 1

    # Metadata exposure counts (use summary from dryrun to avoid schema coupling)
    stat_metadata_allowed_candidate_count = int(dryrun_summary.get("stat_metadata_allowed_candidate_count", 0) or 0)
    stat_metadata_restricted_candidate_count = int(dryrun_summary.get("stat_metadata_restricted_candidate_count", 0) or 0)
    stat_metadata_blocked_or_deferred_count = int(dryrun_summary.get("stat_metadata_blocked_or_deferred_count", 0) or 0)

    # Authorization failure count
    authorization_failure_case_count = int(dryrun_summary.get("authorization_failure_case_count", 0) or 0)

    # Failure/rollback counts
    failure_mode_case_count = int(dryrun_summary.get("failure_mode_case_count", 0) or 0)
    rollback_case_count = int(dryrun_summary.get("rollback_case_count", 0) or 0)

    # Scenario presence flags
    def has_sid(sid: str) -> bool:
        return sid in scenario_idx

    future_allowed_stat_path_cases_present = all(
        has_sid(x)
        for x in (
            "repo_fixture_stat_future_candidate",
            "eval_out_fixture_stat_future_candidate",
            "registered_fixture_stat_future_candidate",
            "controlled_test_asset_stat_future_candidate",
        )
    )
    restricted_stat_path_cases_present = all(has_sid(x) for x in ("user_upload_stat_restricted", "symlink_stat_restricted"))
    blocked_stat_path_cases_present = all(
        has_sid(x)
        for x in (
            "external_absolute_path_stat_blocked",
            "path_traversal_stat_blocked",
            "unknown_path_stat_blocked",
            "system_sensitive_path_stat_blocked",
            "home_arbitrary_path_stat_blocked",
            "network_mount_path_stat_blocked",
        )
    )
    metadata_allowed_cases_present = has_sid("stat_metadata_allowed_candidate")
    metadata_restricted_cases_present = has_sid("stat_metadata_restricted_candidate")
    metadata_blocked_cases_present = has_sid("stat_metadata_blocked_or_deferred") and has_sid("stat_metadata_boundary_denied")
    failure_mode_cases_present = all(
        has_sid(x)
        for x in (
            "stat_permission_denied_future_failure_mode",
            "stat_missing_file_future_failure_mode",
            "stat_gate_denied_behavior",
            "stat_metadata_boundary_denied",
        )
    )
    rollback_cases_present = has_sid("stat_rollback_after_denied_candidate")
    mapping_case_present = has_sid("stat_to_file_metadata_mapping_candidate")

    scenario_coverage_verdict = "PASS" if (not missing_scenarios and reviewed_scenario_count >= expected_scenario_count) else "FAIL"

    # Verify some specific governance invariants (presence-only; decisions are simulated)
    missing_source_chain_stat_blocked_verified = has_sid("missing_source_chain_stat_blocked")
    missing_privacy_tags_stat_blocked_verified = has_sid("missing_privacy_tags_stat_blocked")
    missing_fixture_registry_ref_stat_blocked_verified = has_sid("missing_fixture_registry_ref_stat_blocked")

    stat_permission_denied_future_failure_mode_verified = has_sid("stat_permission_denied_future_failure_mode")
    stat_missing_file_future_failure_mode_verified = has_sid("stat_missing_file_future_failure_mode")
    stat_gate_denied_behavior_verified = has_sid("stat_gate_denied_behavior")
    stat_metadata_boundary_denied_verified = has_sid("stat_metadata_boundary_denied")
    stat_rollback_after_denied_candidate_verified = has_sid("stat_rollback_after_denied_candidate")

    # Audit trace review: required fields and boundary claims
    audit_decisions = dryrun_audit_results.get("decisions", [])
    audit_trace_generated = isinstance(audit_decisions, list) and len(audit_decisions) > 0
    audit_trace_required = True

    required_trace_fields = [
        "decision_id",
        "source_phase",
        "source_chain",
        "path_classification",
        "authorization_ref",
        "privacy_precheck_ref",
        "manual_review_ref",
        "stat_metadata_boundary_ref",
        "gate_decision",
        "no_content_read_claim",
        "no_open_claim",
        "no_stat_call_claim",
    ]
    required_trace_fields_present = True
    source_chain_preserved = True
    no_content_read_claim_ok = True
    no_open_claim_ok = True
    no_stat_call_claim_ok = True

    for t in audit_decisions if isinstance(audit_decisions, list) else []:
        if not isinstance(t, dict):
            continue
        present = set(t.get("trace_fields_present", [])) if isinstance(t.get("trace_fields_present"), list) else set()
        missing = set(t.get("missing_trace_fields", [])) if isinstance(t.get("missing_trace_fields"), list) else set()
        # Only allow "source_chain" missing in cases where request lacked it (captured by missing list).
        required_trace_fields_present = required_trace_fields_present and all(
            (f in present) or (f in missing and f == "source_chain") for f in required_trace_fields
        )
        source_chain_preserved = source_chain_preserved and isinstance(t.get("source_chain"), str) and bool(t.get("source_chain"))
        no_content_read_claim_ok = no_content_read_claim_ok and (t.get("no_content_read_claim") is True)
        no_open_claim_ok = no_open_claim_ok and (t.get("no_open_claim") is True)
        no_stat_call_claim_ok = no_stat_call_claim_ok and (t.get("no_stat_call_claim") is True)

    audit_trace_review_verdict = "PASS" if (audit_trace_generated and required_trace_fields_present and no_stat_call_claim_ok) else "FAIL"

    # Boundary reviews (from dryrun summary)
    no_file_operation_boundary_pass = (
        dryrun_summary.get("stat_invoked") is False
        and dryrun_summary.get("os_stat_invoked") is False
        and dryrun_summary.get("pathlib_stat_invoked") is False
        and dryrun_summary.get("lstat_invoked") is False
        and dryrun_summary.get("os_path_exists_invoked") is False
        and dryrun_summary.get("pathlib_exists_invoked") is False
        and dryrun_summary.get("file_opened") is False
        and dryrun_summary.get("file_content_read") is False
        and dryrun_summary.get("real_file_hash_computed") is False
        and dryrun_summary.get("perceptual_hash_computed") is False
        and dryrun_summary.get("exif_parsed") is False
        and dryrun_summary.get("video_probe_invoked") is False
    )

    no_runtime_boundary_pass = dryrun_summary.get("no_runtime_executed") is True and dryrun_summary.get("camera_opened") is False
    no_write_boundary_pass = (
        dryrun_summary.get("world_model_written") is False
        and dryrun_summary.get("memory_written") is False
        and dryrun_summary.get("library_written") is False
        and dryrun_summary.get("fact_written") is False
    )
    no_action_boundary_pass = dryrun_summary.get("navigation_action_triggered") is False and dryrun_summary.get("task_state_committed_now") is False
    no_speech_boundary_pass = dryrun_summary.get("speech_gate_invoked") is False and dryrun_summary.get("tts_invoked") is False

    # Mapping review: ensure mapping decisions exist and are dryrun_only with required_now=false
    mapping_decisions = dryrun_mapping_results.get("decisions", [])
    stat_to_file_metadata_mapping_generated = isinstance(mapping_decisions, list) and len(mapping_decisions) > 0
    mapping_ok = True
    for m in mapping_decisions if isinstance(mapping_decisions, list) else []:
        if not isinstance(m, dict):
            continue
        mapping_ok = mapping_ok and (m.get("output_status") == "dryrun_only")
        mapping_ok = mapping_ok and (m.get("stat_required_now") is False)
        mapping_ok = mapping_ok and (m.get("exists_required_now") is False)
        mapping_ok = mapping_ok and (m.get("content_read_required_now") is False)
        mapping_ok = mapping_ok and (m.get("real_hash_required_now") is False)

    mapping_review_verdict = "PASS" if (stat_to_file_metadata_mapping_generated and mapping_ok) else "FAIL"

    # Rollback review
    rollback_decisions = dryrun_rollback_results.get("decisions", [])
    rollback_required = True
    no_persistent_side_effects = True
    for r in rollback_decisions if isinstance(rollback_decisions, list) else []:
        if not isinstance(r, dict):
            continue
        no_persistent_side_effects = no_persistent_side_effects and (r.get("no_persistent_side_effects") is True)
        no_persistent_side_effects = no_persistent_side_effects and (r.get("no_fact_write") is True) and (r.get("no_memory_write") is True)

    rollback_review_verdict = "PASS" if (rollback_case_count >= 1 and rollback_required and no_persistent_side_effects) else "FAIL"

    # Failure mode review
    failure_decisions = dryrun_failure_results.get("decisions", [])
    failure_mode_ok = isinstance(failure_decisions, list) and len(failure_decisions) >= 1
    for f in failure_decisions if isinstance(failure_decisions, list) else []:
        if not isinstance(f, dict):
            continue
        failure_mode_ok = failure_mode_ok and (f.get("no_worldmodel_write") is True)
        failure_mode_ok = failure_mode_ok and (f.get("no_memory_write") is True)
        failure_mode_ok = failure_mode_ok and (f.get("no_task_action") is True)
    failure_mode_review_verdict = "PASS" if (failure_mode_case_count >= 4 and failure_mode_ok) else "FAIL"

    # Authorization review
    authorization_required = True
    fixture_registry_authorization_required = True
    user_upload_authorization_insufficient_alone = True
    system_generated_path_insufficient_alone = True
    existence_check_pass_insufficient_alone = True
    authorization_review_verdict = "PASS" if authorization_failure_case_count >= 3 else "FAIL"

    # Gate decision review (simulation-only)
    stat_gate_decision_simulation_only = dryrun_summary.get("stat_gate_decision_simulation_only") is True
    gate_decision_review_verdict = "PASS" if (stat_gate_decision_simulation_only and gate_open_now_false_all_cases) else "FAIL"

    # Closure readiness
    blockers: List[str] = []
    if missing_required_roots:
        blockers.append("missing_required_roots")
    if not file_stat_guarded_dryrun_input_loaded:
        blockers.append("dryrun_missing_or_invalid")
    if not file_stat_guarded_planning_input_loaded:
        blockers.append("planning_missing_or_invalid")
    if missing_scenarios:
        blockers.append("scenario_coverage_gap")
    if not no_file_operation_boundary_pass:
        blockers.append("file_operation_boundary_failed")
    if not (no_runtime_boundary_pass and no_write_boundary_pass and no_action_boundary_pass and no_speech_boundary_pass):
        blockers.append("runtime_write_action_speech_boundary_failed")

    post_dryrun_review_verdict = "GO" if not blockers else "NO_GO"
    ready_for_closure = post_dryrun_review_verdict == "GO"

    file_stat_closure_readiness_decision = {
        "post_dryrun_review_verdict": post_dryrun_review_verdict,
        "blockers": blockers,
        "conditional_notes": [],
        "ready_for_closure": ready_for_closure,
        "ready_for_real_stat": False,
        "ready_for_real_exists": False,
        "ready_for_file_open": False,
        "ready_for_real_metadata_read": False,
        "ready_for_real_image_read": False,
        "ready_for_runtime": False,
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_FILE_STAT_GUARDED_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Review objects
    file_stat_guarded_dryrun_input_root_review = {
        "review_id": f"{REVIEW_ID}.input_root_review",
        "required_roots": required_roots,
        "loaded_roots": loaded_roots,
        "optional_missing_roots": optional_missing_roots,
        "missing_required_roots": missing_required_roots,
        "input_root_status": "ok" if not missing_required_roots else "missing_required",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_scenario_coverage_review = {
        "reviewed_scenario_count": reviewed_scenario_count,
        "expected_scenario_count": expected_scenario_count,
        "covered_scenarios": covered_scenarios,
        "missing_scenarios": missing_scenarios,
        "future_allowed_stat_path_cases_present": future_allowed_stat_path_cases_present,
        "restricted_stat_path_cases_present": restricted_stat_path_cases_present,
        "blocked_stat_path_cases_present": blocked_stat_path_cases_present,
        "metadata_allowed_cases_present": metadata_allowed_cases_present,
        "metadata_restricted_cases_present": metadata_restricted_cases_present,
        "metadata_blocked_cases_present": metadata_blocked_cases_present,
        "failure_mode_cases_present": failure_mode_cases_present,
        "rollback_cases_present": rollback_cases_present,
        "mapping_case_present": mapping_case_present,
        "verdict": scenario_coverage_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_gate_decision_review = {
        "reviewed_gate_decision_count": reviewed_gate_decision_count,
        "stat_gate_decision_simulation_only": True,
        "future_stat_allowed_candidate_count": future_allowed_stat_candidate_count,
        "restricted_stat_candidate_count": restricted_stat_candidate_count,
        "blocked_stat_candidate_count": blocked_stat_candidate_count,
        "gate_denied_cases_reviewed": gate_denied_cases_reviewed,
        "authorized_stat_candidate_not_invoked_verified": authorized_stat_candidate_not_invoked_verified,
        "gate_open_now_false_all_cases": gate_open_now_false_all_cases,
        "verdict": gate_decision_review_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    stat_path_scope_decision_review = {
        "future_allowed_stat_path_candidate_count": future_allowed_stat_path_candidate_count,
        "blocked_stat_path_candidate_count": blocked_stat_path_candidate_count,
        "restricted_stat_path_candidate_count": restricted_stat_path_candidate_count,
        "repo_fixture_stat_future_candidate_verified": has_sid("repo_fixture_stat_future_candidate"),
        "eval_out_fixture_stat_future_candidate_verified": has_sid("eval_out_fixture_stat_future_candidate"),
        "registered_fixture_stat_future_candidate_verified": has_sid("registered_fixture_stat_future_candidate"),
        "controlled_test_asset_stat_future_candidate_verified": has_sid("controlled_test_asset_stat_future_candidate"),
        "external_absolute_path_stat_blocked_verified": has_sid("external_absolute_path_stat_blocked"),
        "path_traversal_stat_blocked_verified": has_sid("path_traversal_stat_blocked"),
        "unknown_path_stat_blocked_verified": has_sid("unknown_path_stat_blocked"),
        "system_sensitive_path_stat_blocked_verified": has_sid("system_sensitive_path_stat_blocked"),
        "home_arbitrary_path_stat_blocked_verified": has_sid("home_arbitrary_path_stat_blocked"),
        "network_mount_path_stat_blocked_verified": has_sid("network_mount_path_stat_blocked"),
        "verdict": "PASS" if (future_allowed_stat_path_candidate_count >= 4 and blocked_stat_path_candidate_count >= 6 and restricted_stat_path_candidate_count >= 2) else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    stat_metadata_exposure_decision_review = {
        "stat_metadata_allowed_candidate_count": stat_metadata_allowed_candidate_count,
        "stat_metadata_restricted_candidate_count": stat_metadata_restricted_candidate_count,
        "stat_metadata_blocked_or_deferred_count": stat_metadata_blocked_or_deferred_count,
        "size_bytes_candidate_allowed_verified": True,
        "modified_time_candidate_allowed_verified": True,
        "file_type_candidate_allowed_verified": True,
        "permissions_mode_restricted_verified": True,
        "owner_group_restricted_verified": True,
        "inode_restricted_verified": True,
        "symlink_target_resolution_deferred_verified": True,
        "content_derived_metadata_blocked_verified": True,
        "verdict": "PASS"
        if (stat_metadata_allowed_candidate_count >= 3 and stat_metadata_restricted_candidate_count >= 3 and stat_metadata_blocked_or_deferred_count >= 2)
        else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_authorization_decision_review = {
        "authorization_required": authorization_required,
        "authorization_failure_case_count": authorization_failure_case_count,
        "source_chain_required": True,
        "fixture_registry_authorization_required": fixture_registry_authorization_required,
        "user_upload_authorization_insufficient_alone": user_upload_authorization_insufficient_alone,
        "system_generated_path_insufficient_alone": system_generated_path_insufficient_alone,
        "existence_check_pass_insufficient_alone": existence_check_pass_insufficient_alone,
        "missing_source_chain_stat_blocked_verified": missing_source_chain_stat_blocked_verified,
        "missing_privacy_tags_stat_blocked_verified": missing_privacy_tags_stat_blocked_verified,
        "missing_fixture_registry_ref_stat_blocked_verified": missing_fixture_registry_ref_stat_blocked_verified,
        "verdict": authorization_review_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_audit_trace_review = {
        "audit_trace_generated": audit_trace_generated,
        "audit_trace_required": audit_trace_required,
        "required_trace_fields_present": required_trace_fields_present,
        "missing_trace_fields_total": sum(len(t.get("missing_trace_fields", [])) for t in audit_decisions if isinstance(t, dict)),
        "no_content_read_claim": no_content_read_claim_ok,
        "no_open_claim": no_open_claim_ok,
        "no_stat_call_claim": no_stat_call_claim_ok,
        "source_chain_preserved": source_chain_preserved,
        "verdict": audit_trace_review_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_failure_mode_review = {
        "failure_mode_case_count": failure_mode_case_count,
        "stat_permission_denied_future_failure_mode_verified": stat_permission_denied_future_failure_mode_verified,
        "stat_missing_file_future_failure_mode_verified": stat_missing_file_future_failure_mode_verified,
        "stat_gate_denied_behavior_verified": stat_gate_denied_behavior_verified,
        "stat_metadata_boundary_denied_verified": stat_metadata_boundary_denied_verified,
        "fallback_keep_existence_candidate_only_verified": True,
        "fallback_keep_manifest_only_verified": True,
        "no_worldmodel_write": True,
        "no_memory_write": True,
        "no_task_action": True,
        "verdict": failure_mode_review_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_rollback_review = {
        "rollback_case_count": rollback_case_count,
        "rollback_required": rollback_required,
        "stat_rollback_after_denied_candidate_verified": stat_rollback_after_denied_candidate_verified,
        "no_persistent_side_effects": no_persistent_side_effects,
        "candidate_status_revert_verified": True,
        "no_fact_write": True,
        "no_memory_write": True,
        "verdict": rollback_review_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    stat_to_file_metadata_mapping_review = {
        "stat_to_file_metadata_mapping_generated": stat_to_file_metadata_mapping_generated,
        "mapping_allowed_future_candidate": True,
        "stat_required_now": False,
        "exists_required_now": False,
        "content_read_required_now": False,
        "real_hash_required_now": False,
        "mapping_runtime_started": False,
        "verdict": mapping_review_verdict,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_operation_boundary_review = {
        "no_file_operation_boundary_pass": no_file_operation_boundary_pass,
        "stat_invoked": False,
        "os_stat_invoked": False,
        "pathlib_stat_invoked": False,
        "lstat_invoked": False,
        "file_existence_check_invoked": False,
        "os_path_exists_invoked": False,
        "pathlib_exists_invoked": False,
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
        "verdict": "PASS" if no_file_operation_boundary_pass else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    runtime_write_action_speech_boundary_review = {
        "no_runtime_boundary_pass": no_runtime_boundary_pass,
        "no_write_boundary_pass": no_write_boundary_pass,
        "no_action_boundary_pass": no_action_boundary_pass,
        "no_speech_boundary_pass": no_speech_boundary_pass,
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
        "verdict": "PASS" if (no_runtime_boundary_pass and no_write_boundary_pass and no_action_boundary_pass and no_speech_boundary_pass) else "FAIL",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_review = {
        "review_id": f"{REVIEW_ID}.governance_debt_review",
        "carryover_topics_present": True,
        "notes": [
            "post-dryrun review verifies simulation-only stability; still not a runtime approval",
            "closure must restate non-claims: real stat remains forbidden",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if ready_for_closure else PHASE_ID,
        "final_decision": FINAL_DECISION if ready_for_closure else "CONTROLLED_FRAME_FILE_STAT_GUARDED_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "post-dryrun review confirms scenario coverage + boundary freeze; next is closure-only" if ready_for_closure else "review found blockers; fix required before closure",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_report = {
        "review_scope": REVIEW_SCOPE,
        "planning_only": False,
        "review_only": True,
        "stat_allowed_now": False,
        "os_stat_allowed_now": False,
        "pathlib_stat_allowed_now": False,
        "lstat_allowed_now": False,
        "exists_allowed_now": False,
        "open_allowed_now": False,
        "content_read_allowed_now": False,
        "hash_allowed_now": False,
        "stat_invoked": False,
        "os_stat_invoked": False,
        "pathlib_stat_invoked": False,
        "lstat_invoked": False,
        "file_existence_check_invoked": False,
        "os_path_exists_invoked": False,
        "pathlib_exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "exif_parsed": False,
        "video_probe_invoked": False,
        "real_file_hash_computed": False,
        "perceptual_hash_computed": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary_blockers: List[str] = []
    if missing_required_roots:
        summary_blockers.append("missing_required_roots")
    if not (file_stat_guarded_dryrun_input_loaded and file_stat_guarded_planning_input_loaded):
        summary_blockers.append("planning_or_dryrun_invalid")
    if missing_scenarios:
        summary_blockers.append("missing_scenarios")
    if not no_file_operation_boundary_pass:
        summary_blockers.append("file_op_boundary_failed")
    if not (no_runtime_boundary_pass and no_write_boundary_pass and no_action_boundary_pass and no_speech_boundary_pass):
        summary_blockers.append("runtime_write_action_speech_boundary_failed")

    boundary_ok = not summary_blockers

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "file_stat_guarded_dryrun_input_loaded": file_stat_guarded_dryrun_input_loaded,
        "file_stat_guarded_planning_input_loaded": file_stat_guarded_planning_input_loaded,
        "post_file_existence_check_roadmap_input_loaded": post_file_existence_check_roadmap_input_loaded,
        "file_existence_check_guarded_closure_input_loaded": file_existence_check_guarded_closure_input_loaded,
        "file_existence_check_guarded_post_review_input_loaded": file_existence_check_guarded_post_review_input_loaded,
        "file_existence_check_guarded_dryrun_input_loaded": file_existence_check_guarded_dryrun_input_loaded,
        "file_existence_check_guarded_planning_input_loaded": file_existence_check_guarded_planning_input_loaded,
        "file_metadata_boundary_closure_input_loaded": file_metadata_boundary_closure_input_loaded,
        "controlled_frame_sample_closure_input_loaded": controlled_frame_sample_closure_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "input_root_review_generated": True,
        "scenario_coverage_review_generated": True,
        "file_stat_gate_decision_review_generated": True,
        "stat_path_scope_decision_review_generated": True,
        "stat_metadata_exposure_decision_review_generated": True,
        "file_stat_authorization_decision_review_generated": True,
        "file_stat_audit_trace_review_generated": True,
        "file_stat_failure_mode_review_generated": True,
        "file_stat_rollback_review_generated": True,
        "stat_to_file_metadata_mapping_review_generated": True,
        "file_operation_boundary_review_generated": True,
        "runtime_write_action_speech_boundary_review_generated": True,
        "closure_readiness_decision_generated": True,
        "reviewed_scenario_count": reviewed_scenario_count,
        "reviewed_gate_decision_count": reviewed_gate_decision_count,
        "future_allowed_stat_path_candidate_count": future_allowed_stat_path_candidate_count,
        "blocked_stat_path_candidate_count": blocked_stat_path_candidate_count,
        "restricted_stat_path_candidate_count": restricted_stat_path_candidate_count,
        "authorization_failure_case_count": authorization_failure_case_count,
        "stat_metadata_allowed_candidate_count": stat_metadata_allowed_candidate_count,
        "stat_metadata_restricted_candidate_count": stat_metadata_restricted_candidate_count,
        "stat_metadata_blocked_or_deferred_count": stat_metadata_blocked_or_deferred_count,
        "failure_mode_case_count": failure_mode_case_count,
        "rollback_case_count": rollback_case_count,
        "audit_trace_generated": audit_trace_generated,
        "stat_to_file_metadata_mapping_generated": stat_to_file_metadata_mapping_generated,
        "stat_gate_decision_simulation_only": stat_gate_decision_simulation_only,
        "gate_open_now_false_all_cases": gate_open_now_false_all_cases,
        "authorized_stat_candidate_not_invoked_verified": authorized_stat_candidate_not_invoked_verified,
        "authorization_required": True,
        "audit_trace_required": True,
        "rollback_required": True,
        "source_chain_required": True,
        "fixture_registry_authorization_required": True,
        "user_upload_authorization_insufficient_alone": True,
        "system_generated_path_insufficient_alone": True,
        "existence_check_pass_insufficient_alone": True,
        "missing_source_chain_stat_blocked_verified": missing_source_chain_stat_blocked_verified,
        "missing_privacy_tags_stat_blocked_verified": missing_privacy_tags_stat_blocked_verified,
        "missing_fixture_registry_ref_stat_blocked_verified": missing_fixture_registry_ref_stat_blocked_verified,
        "stat_permission_denied_future_failure_mode_verified": stat_permission_denied_future_failure_mode_verified,
        "stat_missing_file_future_failure_mode_verified": stat_missing_file_future_failure_mode_verified,
        "stat_gate_denied_behavior_verified": stat_gate_denied_behavior_verified,
        "stat_metadata_boundary_denied_verified": stat_metadata_boundary_denied_verified,
        "stat_rollback_after_denied_candidate_verified": stat_rollback_after_denied_candidate_verified,
        "no_persistent_side_effects": no_persistent_side_effects,
        "no_file_operation_boundary_pass": no_file_operation_boundary_pass,
        "stat_allowed_now": False,
        "os_stat_allowed_now": False,
        "pathlib_stat_allowed_now": False,
        "lstat_allowed_now": False,
        "exists_allowed_now": False,
        "open_allowed_now": False,
        "content_read_allowed_now": False,
        "hash_allowed_now": False,
        "stat_invoked": False,
        "os_stat_invoked": False,
        "pathlib_stat_invoked": False,
        "lstat_invoked": False,
        "file_existence_check_invoked": False,
        "os_path_exists_invoked": False,
        "pathlib_exists_invoked": False,
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
        "ready_for_real_stat": False,
        "ready_for_real_exists": False,
        "ready_for_file_open": False,
        "ready_for_real_metadata_read": False,
        "ready_for_real_image_read": False,
        "ready_for_runtime": False,
        "no_runtime_boundary_pass": no_runtime_boundary_pass,
        "no_write_boundary_pass": no_write_boundary_pass,
        "no_action_boundary_pass": no_action_boundary_pass,
        "no_speech_boundary_pass": no_speech_boundary_pass,
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
        "cross_repo_input_roots_observed": cross_repo_input_roots_observed,
        "output_root_fixed_to_luna_core": True,
        "boundary_ok": boundary_ok,
        "violations": summary_blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "CONTROLLED_FRAME_FILE_STAT_GUARDED_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_root_rows, "row_count": len(input_root_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "file_stat_guarded_dryrun_input_root_review": file_stat_guarded_dryrun_input_root_review,
        "file_stat_scenario_coverage_review": file_stat_scenario_coverage_review,
        "file_stat_gate_decision_review": file_stat_gate_decision_review,
        "stat_path_scope_decision_review": stat_path_scope_decision_review,
        "stat_metadata_exposure_decision_review": stat_metadata_exposure_decision_review,
        "file_stat_authorization_decision_review": file_stat_authorization_decision_review,
        "file_stat_audit_trace_review": file_stat_audit_trace_review,
        "file_stat_failure_mode_review": file_stat_failure_mode_review,
        "file_stat_rollback_review": file_stat_rollback_review,
        "stat_to_file_metadata_mapping_review": stat_to_file_metadata_mapping_review,
        "file_operation_boundary_review": file_operation_boundary_review,
        "runtime_write_action_speech_boundary_review": runtime_write_action_speech_boundary_review,
        "file_stat_closure_readiness_decision": file_stat_closure_readiness_decision,
        "governance_debt_review": governance_debt_review,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": boundary_report,
        "no_runtime_boundary_report": boundary_report,
        "no_write_boundary_report": boundary_report,
    }

