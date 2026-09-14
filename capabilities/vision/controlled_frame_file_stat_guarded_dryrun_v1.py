# -*- coding: utf-8 -*-
"""Controlled Frame File Stat Guarded DryRun v1 (gate decision simulation only).

This phase simulates the file-stat gate decisions and related governance outputs.

Hard boundary (this phase):
- MUST NOT call os.stat / pathlib.Path.stat / lstat
- MUST NOT call os.path.exists / pathlib.Path.exists
- MUST NOT open/read files, images, videos, bytes
- MUST NOT compute hashes / parse EXIF / probe video / decode / extract frames
- MUST NOT enter runtime, MUST NOT write WorldModel/Memory/Fact/Library
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001"
DRYRUN_ID = "cffsgdr_v1_001"
DRYRUN_SCOPE = "controlled_frame_file_stat_guarded_dryrun_only"
SOURCE_CHAIN = "controlled_frame_file_stat_guarded_dryrun_v1"

FINAL_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001"

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


ROOT_SPECS = [
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


def _field(name: str, field_type: str, required: bool, **extras: Any) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"name": name, "type": field_type, "required": required}
    payload.update(extras)
    return payload


def _no_boundary_payload() -> Dict[str, Any]:
    return {
        "dryrun_scope": DRYRUN_SCOPE,
        "stat_gate_decision_simulation_only": True,
        "stat_allowed_now": False,
        "os_stat_allowed_now": False,
        "pathlib_stat_allowed_now": False,
        "lstat_allowed_now": False,
        "exists_allowed_now": False,
        "open_allowed_now": False,
        "content_read_allowed_now": False,
        "hash_allowed_now": False,
        "authorization_required": True,
        "audit_trace_required": True,
        "rollback_required": True,
        "source_chain_required": True,
        "fixture_registry_authorization_required": True,
        "user_upload_authorization_insufficient_alone": True,
        "system_generated_path_insufficient_alone": True,
        "existence_check_pass_insufficient_alone": True,
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
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _path_scope_decision(path_type: str) -> Tuple[str, bool, bool, bool, str, bool]:
    """Returns scope_decision, future_allowed, restricted, blocked, blocked_reason, manual_review_required."""
    mapping = {
        "repo_fixture_path_candidate": ("future_allowed_candidate", True, False, False, "", False),
        "eval_out_fixture_path_candidate": ("future_allowed_candidate", True, False, False, "", False),
        "explicitly_registered_fixture_path_candidate": ("future_allowed_candidate", True, False, False, "", False),
        "controlled_test_asset_path_candidate": ("future_allowed_candidate", True, False, False, "", False),
        "user_uploaded_path_restricted_not_allowed_by_default": ("restricted_requires_manual_review", False, True, False, "", True),
        "symlink_unresolved_blocked_or_restricted": ("restricted_requires_manual_review", False, True, False, "", True),
        "external_absolute_path_blocked": ("blocked_path_scope", False, False, True, "external_absolute_path_blocked", False),
        "path_traversal_blocked": ("blocked_path_scope", False, False, True, "path_traversal_blocked", False),
        "unknown_path_blocked": ("blocked_path_scope", False, False, True, "unknown_path_blocked", False),
        "system_sensitive_path_blocked": ("blocked_path_scope", False, False, True, "system_sensitive_path_blocked", False),
        "home_directory_arbitrary_path_blocked": ("blocked_path_scope", False, False, True, "home_arbitrary_path_blocked", False),
        "network_mount_path_blocked": ("blocked_path_scope", False, False, True, "network_mount_path_blocked", False),
    }
    return mapping.get(path_type, ("blocked_path_scope", False, False, True, "unknown_path_blocked", False))


def _metadata_exposure_decision(requested: List[str]) -> Tuple[List[str], List[str], List[str], str, bool]:
    allowed_set = {
        "size_bytes_candidate",
        "modified_time_candidate",
        "created_time_candidate_if_available",
        "file_type_candidate",
        "is_regular_file_candidate",
    }
    restricted_set = {
        "permissions_mode_candidate",
        "owner_group_candidate",
        "inode_candidate",
        "device_id_candidate",
        "symlink_target_candidate",
        "access_time_candidate",
    }
    blocked_set = {
        "raw_permission_detail_for_user_home",
        "symlink_target_resolution",
        "full_owner_identity",
        "extended_attributes",
        "filesystem_specific_metadata",
        "content_derived_metadata",
    }
    allowed = [m for m in requested if m in allowed_set]
    restricted = [m for m in requested if m in restricted_set]
    blocked = [m for m in requested if m in blocked_set or (m not in allowed_set and m not in restricted_set)]
    privacy_risk_level = "high" if (restricted or blocked) else "medium"
    manual_review_required = bool(restricted or blocked)
    return allowed, restricted, blocked, privacy_risk_level, manual_review_required


def _simulate_case(spec: Dict[str, Any]) -> Dict[str, Any]:
    sid = spec["scenario_id"]
    dryrun_case_id = f"case_{sid}"

    path_type = spec.get("path_type", "repo_fixture_path_candidate")
    request_has_source_chain = spec.get("source_chain_present", True)
    request_has_privacy_tags = spec.get("privacy_tags_present", True)
    request_has_fixture_registry_ref = spec.get("fixture_registry_ref_present", True)
    request_has_authorization = spec.get("authorization_ref_present", True)
    authorization_source = spec.get("authorization_source", "fixture_registry_entry_signed")
    review_status = spec.get("review_status", "not_required")
    requested_stat_metadata = spec.get(
        "requested_stat_metadata",
        ["size_bytes_candidate", "modified_time_candidate", "file_type_candidate"],
    )
    simulated_failure_type = spec.get("simulated_failure_type", "")
    case_type = spec.get("case_type", "path_scope_gate")

    scope_decision, future_allowed, restricted, blocked, blocked_reason, manual_review_required = _path_scope_decision(path_type)

    # Metadata exposure decision simulation
    allowed_md, restricted_md, blocked_md, privacy_risk_level, md_manual_review_required = _metadata_exposure_decision(
        requested_stat_metadata
    )
    stat_metadata_boundary_pass = not bool(blocked_md)

    # Authorization decision simulation
    authorization_required = True
    authorization_pass = bool(request_has_authorization) and authorization_source not in {
        "path_string_only",
        "user_upload_path_only",
        "system_generated_path_only",
        "llm_suggestion_only",
    }
    authorization_insufficient_reason = ""
    if not request_has_authorization:
        authorization_pass = False
        authorization_insufficient_reason = "authorization_missing"
    if authorization_source in {"user_upload_path_only", "system_generated_path_only"}:
        authorization_pass = False
        authorization_insufficient_reason = "authorization_insufficient_alone"

    # Gate decision simulation (gate is closed in this dry-run)
    required_inputs_pass = True
    if not request_has_source_chain:
        required_inputs_pass = False
    if not request_has_privacy_tags:
        required_inputs_pass = False
    if not request_has_fixture_registry_ref:
        required_inputs_pass = False

    gate_open = False
    gate_decision = "future_stat_allowed_candidate_not_invoked"
    gate_block_reason = ""

    if blocked:
        gate_decision = "blocked_path_scope"
        gate_block_reason = blocked_reason or "path_blocked"
    elif not request_has_source_chain:
        gate_decision = "blocked_missing_source_chain"
        gate_block_reason = "missing_source_chain"
    elif not request_has_privacy_tags:
        gate_decision = "blocked_missing_privacy_tags"
        gate_block_reason = "missing_privacy_tags"
    elif not request_has_fixture_registry_ref:
        gate_decision = "blocked_missing_fixture_registry_ref"
        gate_block_reason = "missing_fixture_registry_ref"
    elif not authorization_pass:
        gate_decision = "blocked_authorization_insufficient"
        gate_block_reason = authorization_insufficient_reason or "authorization_insufficient"
    elif spec.get("exists_gate_pass_insufficient_for_stat", False):
        gate_decision = "blocked_exists_gate_pass_insufficient"
        gate_block_reason = "existence_check_pass_insufficient_alone"
    elif not stat_metadata_boundary_pass:
        gate_decision = "blocked_metadata_boundary"
        gate_block_reason = "metadata_boundary_denied"
    elif restricted or manual_review_required or md_manual_review_required:
        gate_decision = "restricted_requires_manual_review"
        gate_block_reason = "manual_review_required"

    if case_type == "gate_denied_behavior":
        gate_decision = "blocked_gate_denied"
        gate_block_reason = "gate_closed"

    # Audit trace candidate
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
    trace_fields_present = [
        f for f in required_trace_fields if not (f == "source_chain" and not request_has_source_chain)
    ]
    missing_trace_fields = [f for f in required_trace_fields if f not in trace_fields_present]

    # Failure mode decision
    selected_failure_mode = ""
    fallback_candidate = []
    if simulated_failure_type:
        mapping = {
            "stat_permission_denied_future": "require_manual_review_and_re_registration",
            "stat_missing_file_future": "keep_as_existence_candidate_only_and_block_stat_candidate",
            "stat_symlink_detected_future": "restrict_and_require_manual_review",
            "stat_path_untrusted": "block_candidate",
            "stat_source_chain_missing": "block_candidate",
            "stat_privacy_tags_missing": "block_candidate",
            "stat_fixture_registry_missing": "block_candidate",
            "stat_gate_denied": "keep_as_manifest_only",
            "stat_metadata_boundary_denied": "keep_as_manifest_only",
        }
        selected_failure_mode = mapping.get(simulated_failure_type, "block_candidate")
        fallback_candidate = [
            "keep_as_existence_candidate_only",
            "keep_as_manifest_only",
            "block_candidate",
            "require_manual_review",
            "require_re_registration",
        ]
    else:
        selected_failure_mode = "not_applicable"
        fallback_candidate = []

    # Rollback decision
    rollback_required = True
    rollback_scope = "dryrun_only_no_side_effect"
    rollback_selected = spec.get("rollback_selected", True)

    # Mapping decision (stat -> file metadata)
    mapping_allowed_future_candidate = True
    mapping_output_status = "dryrun_only"

    request_stub = {
        "request_stub_id": f"req_{sid}",
        "file_ref_placeholder": f"file_ref_{sid}",
        "path_placeholder": f"placeholder://{path_type}/{sid}",
        "path_type": path_type,
        "source_chain_present": request_has_source_chain,
        "privacy_tags_present": request_has_privacy_tags,
        "fixture_registry_ref_present": request_has_fixture_registry_ref,
        "authorization_ref_present": request_has_authorization,
        "review_status": review_status,
        "requested_operation": "file_stat",
        "requested_stat_metadata": requested_stat_metadata,
        "current_stat_allowed": False,
        "current_exists_allowed": False,
        "current_open_allowed": False,
        "fact_status": "not_fact",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    gate_decision_candidate = {
        "gate_decision_id": f"gate_{sid}",
        "source_case_id": dryrun_case_id,
        "request_stub_ref": request_stub["request_stub_id"],
        "gate_open": gate_open,
        "future_gate_candidate": True,
        "gate_decision": gate_decision,
        "gate_block_reason": gate_block_reason,
        "required_inputs_pass": required_inputs_pass,
        "authorization_pass": authorization_pass,
        "path_scope_pass": not blocked,
        "privacy_precheck_pass": request_has_privacy_tags,
        "fixture_registry_pass": request_has_fixture_registry_ref,
        "stat_metadata_boundary_pass": stat_metadata_boundary_pass,
        "audit_trace_required": True,
        "rollback_required": True,
        "stat_invoked": False,
        "os_stat_invoked": False,
        "pathlib_stat_invoked": False,
        "lstat_invoked": False,
        "file_stat_verified": False,
        "fact_status": "not_fact",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    path_scope_decision_candidate = {
        "path_scope_decision_id": f"scope_{sid}",
        "source_case_id": dryrun_case_id,
        "path_type": path_type,
        "future_allowed_stat_path_candidate": future_allowed,
        "restricted_stat_path_candidate": restricted,
        "blocked_stat_path_candidate": blocked,
        "blocked_reason": blocked_reason,
        "manual_review_required": manual_review_required or md_manual_review_required,
        "allowed_now": False,
        "stat_operation_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    metadata_exposure_decision_candidate = {
        "metadata_exposure_decision_id": f"md_{sid}",
        "source_case_id": dryrun_case_id,
        "requested_stat_metadata": requested_stat_metadata,
        "allowed_stat_metadata_candidate": allowed_md,
        "restricted_stat_metadata_candidate": restricted_md,
        "blocked_or_deferred_stat_metadata": blocked_md,
        "privacy_risk_level": privacy_risk_level,
        "manual_review_required": bool(restricted_md or blocked_md),
        "output_candidate_only": True,
        "fact_status": "not_fact",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    authorization_decision_candidate = {
        "authorization_decision_id": f"auth_{sid}",
        "source_case_id": dryrun_case_id,
        "authorization_required": authorization_required,
        "authorization_source": authorization_source,
        "authorization_pass": authorization_pass,
        "authorization_insufficient_reason": authorization_insufficient_reason,
        "fixture_registry_authorization_required": True,
        "user_upload_authorization_insufficient_alone": True,
        "system_generated_path_insufficient_alone": True,
        "existence_check_pass_insufficient_alone": True,
        "source_chain_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    audit_trace_candidate = {
        "audit_trace_id": f"audit_{sid}",
        "source_case_id": dryrun_case_id,
        "trace_required": True,
        "trace_fields_present": trace_fields_present,
        "missing_trace_fields": missing_trace_fields,
        "gate_decision_ref": gate_decision_candidate["gate_decision_id"],
        "path_classification_ref": path_scope_decision_candidate["path_scope_decision_id"],
        "authorization_ref": authorization_decision_candidate["authorization_decision_id"],
        "privacy_precheck_ref": "privacy_precheck_placeholder",
        "manual_review_ref": "manual_review_placeholder" if path_scope_decision_candidate["manual_review_required"] else "",
        "metadata_boundary_ref": metadata_exposure_decision_candidate["metadata_exposure_decision_id"],
        "no_content_read_claim": True,
        "no_open_claim": True,
        "no_stat_call_claim": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    failure_mode_decision_candidate = {
        "failure_mode_decision_id": f"fail_{sid}",
        "source_case_id": dryrun_case_id,
        "simulated_failure_type": simulated_failure_type or "none",
        "selected_failure_mode": selected_failure_mode,
        "fallback_candidate": fallback_candidate,
        "no_worldmodel_write": True,
        "no_memory_write": True,
        "no_task_action": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rollback_decision_candidate = {
        "rollback_decision_id": f"rb_{sid}",
        "source_case_id": dryrun_case_id,
        "rollback_required": rollback_required,
        "rollback_scope": rollback_scope,
        "no_persistent_side_effects": True,
        "candidate_status_revert": True,
        "audit_mark_reverted_candidate": rollback_selected,
        "no_fact_write": True,
        "no_memory_write": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    mapping_decision_candidate = {
        "mapping_decision_id": f"map_{sid}",
        "source_case_id": dryrun_case_id,
        "stat_decision_candidate_ref": gate_decision_candidate["gate_decision_id"],
        "file_metadata_candidate_ref": "file_metadata_boundary:file_metadata_candidate_schema.json",
        "mapping_allowed_future_candidate": mapping_allowed_future_candidate,
        "stat_required_now": False,
        "exists_required_now": False,
        "content_read_required_now": False,
        "real_hash_required_now": False,
        "output_status": mapping_output_status,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    violations: List[str] = []
    if gate_decision.startswith("blocked_"):
        violations.append(gate_block_reason or "blocked")
    if gate_decision.startswith("restricted_"):
        violations.append("restricted_requires_manual_review")
    dryrun_status = "pass" if not violations else "simulated_restriction_or_block_expected"

    dryrun_result = {
        "result_id": f"result_{sid}",
        "source_case_id": dryrun_case_id,
        "request_stub_ref": request_stub["request_stub_id"],
        "gate_decision_ref": gate_decision_candidate["gate_decision_id"],
        "path_scope_decision_ref": path_scope_decision_candidate["path_scope_decision_id"],
        "metadata_exposure_decision_ref": metadata_exposure_decision_candidate["metadata_exposure_decision_id"],
        "authorization_decision_ref": authorization_decision_candidate["authorization_decision_id"],
        "audit_trace_ref": audit_trace_candidate["audit_trace_id"],
        "failure_mode_decision_ref": failure_mode_decision_candidate["failure_mode_decision_id"],
        "rollback_decision_ref": rollback_decision_candidate["rollback_decision_id"],
        "mapping_decision_ref": mapping_decision_candidate["mapping_decision_id"],
        "dryrun_status": dryrun_status,
        "violations": violations,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    dryrun_case = {
        "dryrun_case_id": dryrun_case_id,
        "case_type": case_type,
        "simulated_file_ref": request_stub,
        "simulated_path_scope": path_type,
        "simulated_authorization": authorization_source if request_has_authorization else "(missing)",
        "simulated_source_chain": request_has_source_chain,
        "simulated_privacy_tags": request_has_privacy_tags,
        "simulated_fixture_registry_ref": request_has_fixture_registry_ref,
        "simulated_stat_metadata_request": requested_stat_metadata,
        "expected_gate_decision": spec.get("expected_gate_decision", gate_decision),
        "expected_path_scope_decision": spec.get("expected_path_scope_decision", scope_decision),
        "expected_authorization_decision": "pass" if authorization_pass else "fail",
        "expected_metadata_exposure_decision": spec.get("expected_metadata_exposure_decision", "candidate_only"),
        "expected_failure_mode": selected_failure_mode,
        "expected_rollback_decision": rollback_scope,
        "expected_boundary_flags": {
            "stat_invoked": False,
            "os_stat_invoked": False,
            "pathlib_stat_invoked": False,
            "lstat_invoked": False,
            "file_stat_verified": False,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    authorization_failed = not authorization_pass
    failure_mode_case = bool(simulated_failure_type)
    rollback_case = bool(rollback_selected)
    path_category = "blocked" if blocked else ("restricted" if restricted or manual_review_required or md_manual_review_required else "future_allowed")

    return {
        "dryrun_case": dryrun_case,
        "request_stub": request_stub,
        "gate_decision": gate_decision_candidate,
        "path_scope_decision": path_scope_decision_candidate,
        "metadata_exposure_decision": metadata_exposure_decision_candidate,
        "authorization_decision": authorization_decision_candidate,
        "audit_trace": audit_trace_candidate,
        "failure_mode": failure_mode_decision_candidate,
        "rollback_decision": rollback_decision_candidate,
        "mapping_decision": mapping_decision_candidate,
        "dryrun_result": dryrun_result,
        "path_category": path_category,
        "authorization_failed": authorization_failed,
        "failure_mode_case": failure_mode_case,
        "rollback_case": rollback_case,
    }


def run_controlled_frame_file_stat_guarded_dryrun_v1(
    *,
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

    input_rows: List[Dict[str, Any]] = []
    cross_repo_input_roots_observed = False
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        path_str = str(meta["root"]) if meta["root"] else "(not_provided)"
        if "Luna-Workspace-Min" in path_str:
            cross_repo_input_roots_observed = True
        input_rows.append(
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

    planning_input_loaded = (
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

    # ---- Schemas ----
    dryrun_case_schema = {
        "schema_name": "ControlledFrameFileStatGuardedDryRunCase",
        "schema_version": "v1",
        "field_specs": [
            _field("dryrun_case_id", "string", True),
            _field("case_type", "string", True),
            _field("simulated_file_ref", "object", True),
            _field("simulated_path_scope", "string", True),
            _field("simulated_authorization", "string", True),
            _field("simulated_source_chain", "boolean", True),
            _field("simulated_privacy_tags", "boolean", True),
            _field("simulated_fixture_registry_ref", "boolean", True),
            _field("simulated_stat_metadata_request", "list", True),
            _field("expected_gate_decision", "string", True),
            _field("expected_path_scope_decision", "string", True),
            _field("expected_authorization_decision", "string", True),
            _field("expected_metadata_exposure_decision", "string", True),
            _field("expected_failure_mode", "string", True),
            _field("expected_rollback_decision", "string", True),
            _field("expected_boundary_flags", "object", True),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    simulated_request_stub_schema = {
        "schema_name": "SimulatedFileStatRequestStub",
        "schema_version": "v1",
        "field_specs": [
            _field("request_stub_id", "string", True),
            _field("file_ref_placeholder", "string", True),
            _field("path_placeholder", "string", True),
            _field("path_type", "string", True),
            _field("source_chain_present", "boolean", True),
            _field("privacy_tags_present", "boolean", True),
            _field("fixture_registry_ref_present", "boolean", True),
            _field("authorization_ref_present", "boolean", True),
            _field("review_status", "string", True),
            _field("requested_operation", "string", True),
            _field("requested_stat_metadata", "list", True),
            _field("current_stat_allowed", "boolean", True, default=False),
            _field("current_exists_allowed", "boolean", True, default=False),
            _field("current_open_allowed", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True),
        ],
        "invariants": {
            "current_stat_allowed": False,
            "current_exists_allowed": False,
            "current_open_allowed": False,
            "fact_status": "not_fact",
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_gate_decision_candidate_schema = {
        "schema_name": "FileStatGateDecisionCandidate",
        "schema_version": "v1",
        "gate_decision_values": [
            "future_stat_allowed_candidate_not_invoked",
            "restricted_requires_manual_review",
            "blocked_path_scope",
            "blocked_missing_source_chain",
            "blocked_missing_privacy_tags",
            "blocked_missing_fixture_registry_ref",
            "blocked_authorization_insufficient",
            "blocked_exists_gate_pass_insufficient",
            "blocked_metadata_boundary",
            "blocked_gate_denied",
            "fallback_keep_existence_candidate_only",
            "fallback_keep_manifest_only",
        ],
        "field_specs": [
            _field("gate_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("request_stub_ref", "string", True),
            _field("gate_open", "boolean", True, default=False),
            _field("future_gate_candidate", "boolean", True),
            _field("gate_decision", "string", True),
            _field("gate_block_reason", "string", False),
            _field("required_inputs_pass", "boolean", True),
            _field("authorization_pass", "boolean", True),
            _field("path_scope_pass", "boolean", True),
            _field("privacy_precheck_pass", "boolean", True),
            _field("fixture_registry_pass", "boolean", True),
            _field("stat_metadata_boundary_pass", "boolean", True),
            _field("audit_trace_required", "boolean", True),
            _field("rollback_required", "boolean", True),
            _field("stat_invoked", "boolean", True, default=False),
            _field("os_stat_invoked", "boolean", True, default=False),
            _field("pathlib_stat_invoked", "boolean", True, default=False),
            _field("lstat_invoked", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True),
        ],
        "invariants": {"stat_invoked": False, "os_stat_invoked": False, "pathlib_stat_invoked": False, "lstat_invoked": False, "fact_status": "not_fact"},
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    stat_path_scope_decision_candidate_schema = {
        "schema_name": "StatPathScopeDryRunDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("path_scope_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("path_type", "string", True),
            _field("future_allowed_stat_path_candidate", "boolean", True),
            _field("restricted_stat_path_candidate", "boolean", True),
            _field("blocked_stat_path_candidate", "boolean", True),
            _field("blocked_reason", "string", False),
            _field("manual_review_required", "boolean", True),
            _field("allowed_now", "boolean", True, default=False),
            _field("stat_operation_allowed", "boolean", True, default=False),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    stat_metadata_exposure_decision_candidate_schema = {
        "schema_name": "StatMetadataExposureDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("metadata_exposure_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("requested_stat_metadata", "list", True),
            _field("allowed_stat_metadata_candidate", "list", True),
            _field("restricted_stat_metadata_candidate", "list", True),
            _field("blocked_or_deferred_stat_metadata", "list", True),
            _field("privacy_risk_level", "string", True),
            _field("manual_review_required", "boolean", True),
            _field("output_candidate_only", "boolean", True, default=True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_authorization_decision_candidate_schema = {
        "schema_name": "FileStatAuthorizationDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("authorization_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("authorization_required", "boolean", True),
            _field("authorization_source", "string", True),
            _field("authorization_pass", "boolean", True),
            _field("authorization_insufficient_reason", "string", False),
            _field("fixture_registry_authorization_required", "boolean", True),
            _field("user_upload_authorization_insufficient_alone", "boolean", True),
            _field("system_generated_path_insufficient_alone", "boolean", True),
            _field("existence_check_pass_insufficient_alone", "boolean", True),
            _field("source_chain_required", "boolean", True),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_audit_trace_candidate_schema = {
        "schema_name": "FileStatAuditTraceCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("audit_trace_id", "string", True),
            _field("source_case_id", "string", True),
            _field("trace_required", "boolean", True),
            _field("trace_fields_present", "list", True),
            _field("missing_trace_fields", "list", True),
            _field("gate_decision_ref", "string", True),
            _field("path_classification_ref", "string", True),
            _field("authorization_ref", "string", True),
            _field("privacy_precheck_ref", "string", True),
            _field("manual_review_ref", "string", True),
            _field("metadata_boundary_ref", "string", True),
            _field("no_content_read_claim", "boolean", True, default=True),
            _field("no_open_claim", "boolean", True, default=True),
            _field("no_stat_call_claim", "boolean", True, default=True),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_failure_mode_decision_candidate_schema = {
        "schema_name": "FileStatFailureModeDecisionCandidate",
        "schema_version": "v1",
        "failure_types": [
            "stat_permission_denied_future",
            "stat_missing_file_future",
            "stat_symlink_detected_future",
            "stat_path_untrusted",
            "stat_source_chain_missing",
            "stat_privacy_tags_missing",
            "stat_fixture_registry_missing",
            "stat_gate_denied",
            "stat_metadata_boundary_denied",
        ],
        "field_specs": [
            _field("failure_mode_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("simulated_failure_type", "string", True),
            _field("selected_failure_mode", "string", True),
            _field("fallback_candidate", "list", True),
            _field("no_worldmodel_write", "boolean", True, default=True),
            _field("no_memory_write", "boolean", True, default=True),
            _field("no_task_action", "boolean", True, default=True),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_rollback_decision_candidate_schema = {
        "schema_name": "FileStatRollbackDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("rollback_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("rollback_required", "boolean", True),
            _field("rollback_scope", "string", True),
            _field("no_persistent_side_effects", "boolean", True, default=True),
            _field("candidate_status_revert", "boolean", True),
            _field("audit_mark_reverted_candidate", "boolean", True),
            _field("no_fact_write", "boolean", True, default=True),
            _field("no_memory_write", "boolean", True, default=True),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    stat_to_file_metadata_mapping_decision_candidate_schema = {
        "schema_name": "StatToFileMetadataMappingDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("mapping_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("stat_decision_candidate_ref", "string", True),
            _field("file_metadata_candidate_ref", "string", True),
            _field("mapping_allowed_future_candidate", "boolean", True),
            _field("stat_required_now", "boolean", True, default=False),
            _field("exists_required_now", "boolean", True, default=False),
            _field("content_read_required_now", "boolean", True, default=False),
            _field("real_hash_required_now", "boolean", True, default=False),
            _field("output_status", "string", True),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    dryrun_result_schema = {
        "schema_name": "FileStatGuardedDryRunResult",
        "schema_version": "v1",
        "field_specs": [
            _field("result_id", "string", True),
            _field("source_case_id", "string", True),
            _field("request_stub_ref", "string", True),
            _field("gate_decision_ref", "string", True),
            _field("path_scope_decision_ref", "string", True),
            _field("metadata_exposure_decision_ref", "string", True),
            _field("authorization_decision_ref", "string", True),
            _field("audit_trace_ref", "string", True),
            _field("failure_mode_decision_ref", "string", True),
            _field("rollback_decision_ref", "string", True),
            _field("mapping_decision_ref", "string", True),
            _field("dryrun_status", "string", True),
            _field("violations", "list", True),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # ---- Scenario matrix (>=28) ----
    scenario_specs = [
        {"scenario_id": "repo_fixture_stat_future_candidate", "path_type": "repo_fixture_path_candidate"},
        {"scenario_id": "eval_out_fixture_stat_future_candidate", "path_type": "eval_out_fixture_path_candidate"},
        {"scenario_id": "registered_fixture_stat_future_candidate", "path_type": "explicitly_registered_fixture_path_candidate"},
        {"scenario_id": "controlled_test_asset_stat_future_candidate", "path_type": "controlled_test_asset_path_candidate"},
        {"scenario_id": "user_upload_stat_restricted", "path_type": "user_uploaded_path_restricted_not_allowed_by_default", "review_status": "pending_review"},
        {"scenario_id": "external_absolute_path_stat_blocked", "path_type": "external_absolute_path_blocked"},
        {"scenario_id": "path_traversal_stat_blocked", "path_type": "path_traversal_blocked"},
        {"scenario_id": "unknown_path_stat_blocked", "path_type": "unknown_path_blocked"},
        {"scenario_id": "symlink_stat_restricted", "path_type": "symlink_unresolved_blocked_or_restricted", "review_status": "pending_review"},
        {"scenario_id": "system_sensitive_path_stat_blocked", "path_type": "system_sensitive_path_blocked"},
        {"scenario_id": "home_arbitrary_path_stat_blocked", "path_type": "home_directory_arbitrary_path_blocked"},
        {"scenario_id": "network_mount_path_stat_blocked", "path_type": "network_mount_path_blocked"},
        {"scenario_id": "missing_source_chain_stat_blocked", "path_type": "repo_fixture_path_candidate", "source_chain_present": False},
        {"scenario_id": "missing_privacy_tags_stat_blocked", "path_type": "repo_fixture_path_candidate", "privacy_tags_present": False},
        {"scenario_id": "missing_fixture_registry_ref_stat_blocked", "path_type": "repo_fixture_path_candidate", "fixture_registry_ref_present": False},
        {"scenario_id": "exists_gate_pass_insufficient_for_stat", "path_type": "repo_fixture_path_candidate", "exists_gate_pass_insufficient_for_stat": True},
        {
            "scenario_id": "user_upload_authorization_insufficient_for_stat",
            "path_type": "user_uploaded_path_restricted_not_allowed_by_default",
            "authorization_source": "user_upload_path_only",
            "review_status": "pending_review",
        },
        {
            "scenario_id": "system_generated_path_insufficient_for_stat",
            "path_type": "repo_fixture_path_candidate",
            "authorization_source": "system_generated_path_only",
        },
        {
            "scenario_id": "authorization_missing_for_stat",
            "path_type": "repo_fixture_path_candidate",
            "authorization_ref_present": False,
        },
        {"scenario_id": "authorized_stat_candidate_but_not_invoked", "path_type": "repo_fixture_path_candidate"},
        {"scenario_id": "stat_metadata_allowed_candidate", "path_type": "repo_fixture_path_candidate", "requested_stat_metadata": ["size_bytes_candidate", "modified_time_candidate", "file_type_candidate"]},
        {"scenario_id": "stat_metadata_restricted_candidate", "path_type": "repo_fixture_path_candidate", "requested_stat_metadata": ["inode_candidate", "permissions_mode_candidate", "owner_group_candidate"]},
        {"scenario_id": "stat_metadata_restricted_candidate_device", "path_type": "repo_fixture_path_candidate", "requested_stat_metadata": ["device_id_candidate"]},
        {"scenario_id": "stat_metadata_restricted_candidate_access_time", "path_type": "repo_fixture_path_candidate", "requested_stat_metadata": ["access_time_candidate"]},
        {"scenario_id": "stat_metadata_blocked_or_deferred", "path_type": "repo_fixture_path_candidate", "requested_stat_metadata": ["extended_attributes", "content_derived_metadata"]},
        {"scenario_id": "stat_permission_denied_future_failure_mode", "path_type": "repo_fixture_path_candidate", "simulated_failure_type": "stat_permission_denied_future"},
        {"scenario_id": "stat_missing_file_future_failure_mode", "path_type": "repo_fixture_path_candidate", "simulated_failure_type": "stat_missing_file_future"},
        {"scenario_id": "stat_symlink_detected_future_failure_mode", "path_type": "repo_fixture_path_candidate", "simulated_failure_type": "stat_symlink_detected_future"},
        {"scenario_id": "stat_gate_denied_behavior", "case_type": "gate_denied_behavior", "path_type": "repo_fixture_path_candidate", "simulated_failure_type": "stat_gate_denied"},
        {"scenario_id": "stat_rollback_after_denied_candidate", "case_type": "gate_denied_behavior", "path_type": "repo_fixture_path_candidate", "rollback_selected": True},
        {
            "scenario_id": "stat_metadata_boundary_denied",
            "path_type": "repo_fixture_path_candidate",
            "requested_stat_metadata": ["filesystem_specific_metadata", "full_owner_identity"],
        },
        {"scenario_id": "stat_to_file_metadata_mapping_candidate", "path_type": "repo_fixture_path_candidate"},
    ]

    scenario_matrix_rows = [
        {
            **spec,
            "stat_gate_decision_simulation_only": True,
            "stat_invoked": False,
            "exists_call_invoked": False,
            "file_opened": False,
            "content_read": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for spec in scenario_specs
    ]
    scenario_matrix = {
        "scenarios": scenario_matrix_rows,
        "scenario_count": len(scenario_matrix_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    simulated = [_simulate_case(spec) for spec in scenario_specs]
    dryrun_cases = [r["dryrun_case"] for r in simulated]
    request_stubs = [r["request_stub"] for r in simulated]
    gate_decisions = [r["gate_decision"] for r in simulated]
    path_scope_decisions = [r["path_scope_decision"] for r in simulated]
    metadata_exposure_decisions = [r["metadata_exposure_decision"] for r in simulated]
    authorization_decisions = [r["authorization_decision"] for r in simulated]
    audit_traces = [r["audit_trace"] for r in simulated]
    failure_modes = [r["failure_mode"] for r in simulated]
    rollback_decisions = [r["rollback_decision"] for r in simulated]
    mapping_decisions = [r["mapping_decision"] for r in simulated]
    dryrun_results = [r["dryrun_result"] for r in simulated]

    future_allowed_stat_path_candidate_count = sum(1 for r in simulated if r["path_category"] == "future_allowed")
    blocked_stat_path_candidate_count = sum(1 for r in simulated if r["path_category"] == "blocked")
    restricted_stat_path_candidate_count = sum(1 for r in simulated if r["path_category"] == "restricted")
    authorization_failure_case_count = sum(1 for r in simulated if r["authorization_failed"])
    stat_metadata_allowed_candidate_count = sum(1 for d in metadata_exposure_decisions if len(d.get("allowed_stat_metadata_candidate", [])) > 0)
    stat_metadata_restricted_candidate_count = sum(1 for d in metadata_exposure_decisions if len(d.get("restricted_stat_metadata_candidate", [])) > 0)
    stat_metadata_blocked_or_deferred_count = sum(1 for d in metadata_exposure_decisions if len(d.get("blocked_or_deferred_stat_metadata", [])) > 0)
    failure_mode_case_count = sum(1 for r in simulated if r["failure_mode_case"])
    rollback_case_count = sum(1 for r in simulated if r["rollback_case"])

    file_stat_boundary_matrix = {
        "frozen_boundaries": [
            "dryrun-only",
            "stat-gate-decision-simulation-only",
            "no-exists-call",
            "no-stat",
            "no-open",
            "no-content-read",
            "no-exif-parse",
            "no-video-probe",
            "no-real-hash",
            "no-perceptual-hash",
            "no-runtime",
            "no-write",
            "no-action",
            "no-speech",
        ],
        "simulated_now": {
            "path_scope_decision": True,
            "authorization_decision": True,
            "metadata_exposure_decision": True,
            "gate_decision": True,
            "audit_trace_candidate": True,
            "failure_mode_decision": True,
            "rollback_decision": True,
            "stat_to_file_metadata_mapping": True,
        },
        "blocked_now": {
            "file_stat": True,
            "os_stat": True,
            "pathlib_stat": True,
            "lstat": True,
            "file_existence_check": True,
            "os_path_exists": True,
            "pathlib_path_exists": True,
            "file_open": True,
            "content_read": True,
            "real_hash_computation": True,
            "exif_parse": True,
            "video_probe": True,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "carryover_topics": [
            {"topic": "post-dryrun review must verify stat gate decisions are stable", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "metadata exposure boundary enforcement must be explicit before any guarded stat", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "symlink policy must prevent scope escape", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "cross-repo _eval_out archival/migration strategy required", "source_chain": SOURCE_CHAIN, **_not_fact()},
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "file stat gate decision dry-run simulation completed; next step is post-dryrun review (review-only)",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not planning_input_loaded:
        blockers.append("planning_missing_or_invalid")
    if not all(
        [
            post_file_existence_check_roadmap_input_loaded,
            file_existence_check_guarded_closure_input_loaded,
            file_existence_check_guarded_post_review_input_loaded,
            file_existence_check_guarded_dryrun_input_loaded,
            file_existence_check_guarded_planning_input_loaded,
            file_metadata_boundary_closure_input_loaded,
            file_metadata_boundary_post_review_input_loaded,
            file_metadata_boundary_dryrun_input_loaded,
            file_metadata_boundary_planning_input_loaded,
            controlled_frame_sample_closure_input_loaded,
            controlled_frame_input_closure_input_loaded,
            map_location_readonly_context_input_loaded,
            safety_constitution_input_loaded,
            minimal_runtime_integration_closure_loaded,
            ocr_final_closure_loaded,
        ]
    ):
        blockers.append("required_root_missing_or_invalid")
    if len(scenario_specs) < 28:
        blockers.append("scenario_matrix_insufficient")

    output_root_fixed_to_luna_core = True

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "file_stat_guarded_planning_input_loaded": planning_input_loaded,
        "post_file_existence_check_roadmap_input_loaded": post_file_existence_check_roadmap_input_loaded,
        "file_existence_check_guarded_closure_input_loaded": file_existence_check_guarded_closure_input_loaded,
        "file_existence_check_guarded_post_review_input_loaded": file_existence_check_guarded_post_review_input_loaded,
        "file_existence_check_guarded_dryrun_input_loaded": file_existence_check_guarded_dryrun_input_loaded,
        "file_existence_check_guarded_planning_input_loaded": file_existence_check_guarded_planning_input_loaded,
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
        "dryrun_case_schema_defined": True,
        "simulated_file_stat_request_stub_schema_defined": True,
        "file_stat_gate_decision_candidate_schema_defined": True,
        "stat_path_scope_dryrun_decision_candidate_schema_defined": True,
        "stat_metadata_exposure_decision_candidate_schema_defined": True,
        "file_stat_authorization_decision_candidate_schema_defined": True,
        "file_stat_audit_trace_candidate_schema_defined": True,
        "file_stat_failure_mode_decision_candidate_schema_defined": True,
        "file_stat_rollback_decision_candidate_schema_defined": True,
        "stat_to_file_metadata_mapping_decision_candidate_schema_defined": True,
        "file_stat_guarded_dryrun_result_schema_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(scenario_specs),
        "dryrun_results_generated": True,
        "future_allowed_stat_path_candidate_count": future_allowed_stat_path_candidate_count,
        "blocked_stat_path_candidate_count": blocked_stat_path_candidate_count,
        "restricted_stat_path_candidate_count": restricted_stat_path_candidate_count,
        "authorization_failure_case_count": authorization_failure_case_count,
        "stat_metadata_allowed_candidate_count": stat_metadata_allowed_candidate_count,
        "stat_metadata_restricted_candidate_count": stat_metadata_restricted_candidate_count,
        "stat_metadata_blocked_or_deferred_count": stat_metadata_blocked_or_deferred_count,
        "failure_mode_case_count": failure_mode_case_count,
        "rollback_case_count": rollback_case_count,
        "audit_trace_generated": True,
        "stat_to_file_metadata_mapping_generated": True,
        "stat_gate_decision_simulation_only": True,
        "stat_allowed_now": False,
        "os_stat_allowed_now": False,
        "pathlib_stat_allowed_now": False,
        "lstat_allowed_now": False,
        "exists_allowed_now": False,
        "open_allowed_now": False,
        "content_read_allowed_now": False,
        "hash_allowed_now": False,
        "authorization_required": True,
        "audit_trace_required": True,
        "rollback_required": True,
        "source_chain_required": True,
        "fixture_registry_authorization_required": True,
        "user_upload_authorization_insufficient_alone": True,
        "system_generated_path_insufficient_alone": True,
        "existence_check_pass_insufficient_alone": True,
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
        "output_root_fixed_to_luna_core": output_root_fixed_to_luna_core,
        "boundary_ok": not blockers,
        "violations": blockers,
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_FILE_STAT_GUARDED_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "dryrun_case_schema": dryrun_case_schema,
        "simulated_file_stat_request_stub_schema": simulated_request_stub_schema,
        "file_stat_gate_decision_candidate_schema": file_stat_gate_decision_candidate_schema,
        "stat_path_scope_dryrun_decision_candidate_schema": stat_path_scope_decision_candidate_schema,
        "stat_metadata_exposure_decision_candidate_schema": stat_metadata_exposure_decision_candidate_schema,
        "file_stat_authorization_decision_candidate_schema": file_stat_authorization_decision_candidate_schema,
        "file_stat_audit_trace_candidate_schema": file_stat_audit_trace_candidate_schema,
        "file_stat_failure_mode_decision_candidate_schema": file_stat_failure_mode_decision_candidate_schema,
        "file_stat_rollback_decision_candidate_schema": file_stat_rollback_decision_candidate_schema,
        "stat_to_file_metadata_mapping_decision_candidate_schema": stat_to_file_metadata_mapping_decision_candidate_schema,
        "file_stat_guarded_dryrun_result_schema": dryrun_result_schema,
        "controlled_frame_file_stat_guarded_dryrun_scenario_matrix": scenario_matrix,
        "controlled_frame_file_stat_guarded_dryrun_results": {"results": dryrun_results, "result_count": len(dryrun_results), "cases": dryrun_cases, "source_chain": SOURCE_CHAIN, **_not_fact()},
        "file_stat_gate_decision_results": {"decisions": gate_decisions, "decision_count": len(gate_decisions), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "stat_path_scope_dryrun_decision_results": {"decisions": path_scope_decisions, "decision_count": len(path_scope_decisions), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "stat_metadata_exposure_decision_results": {"decisions": metadata_exposure_decisions, "decision_count": len(metadata_exposure_decisions), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "authorization_decision_results": {"decisions": authorization_decisions, "decision_count": len(authorization_decisions), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "audit_trace_results": {"decisions": audit_traces, "decision_count": len(audit_traces), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "failure_mode_decision_results": {"decisions": failure_modes, "decision_count": len(failure_modes), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "rollback_decision_results": {"decisions": rollback_decisions, "decision_count": len(rollback_decisions), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "stat_to_file_metadata_mapping_results": {"decisions": mapping_decisions, "decision_count": len(mapping_decisions), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "simulated_request_stub_results": {"requests": request_stubs, "request_count": len(request_stubs), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "file_stat_boundary_matrix": file_stat_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": _no_boundary_payload(),
        "no_runtime_boundary_report": _no_boundary_payload(),
        "no_write_boundary_report": _no_boundary_payload(),
    }

