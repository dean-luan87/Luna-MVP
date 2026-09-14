# -*- coding: utf-8 -*-
"""Controlled Frame File Metadata Boundary DryRun v1 (decision simulation only).

Simulates file/metadata boundary decisions WITHOUT stat, open, read, decode, probe, or hash.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001"
DRYRUN_ID = "cffmbdr_v1_001"
DRYRUN_SCOPE = "controlled_frame_file_metadata_boundary_dryrun_only"
SOURCE_CHAIN = "controlled_frame_file_metadata_boundary_dryrun_v1"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Controlled-Frame-File-Metadata-Boundary-Post-DryRun-Review-v1-001"

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

PRIVACY_SENSITIVE_TAGS = {
    "private_home",
    "face_possible",
    "child_or_school_possible",
    "medical_context_possible",
    "screen_or_document_possible",
    "commercial_sensitive_possible",
}

ROOT_SPECS = [
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
        "artifacts": ["summary.json", "controlled_frame_sample_manifest_schema.json"],
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


def _field(name: str, field_type: str, required: bool, **extras: Any) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"name": name, "type": field_type, "required": required}
    payload.update(extras)
    return payload


def _no_file_operation_payload() -> Dict[str, Any]:
    return {
        "dryrun_scope": DRYRUN_SCOPE,
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
        "dryrun_scope": DRYRUN_SCOPE,
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


def _path_decision(path_type: str) -> Tuple[str, bool, bool, bool, str, bool, bool]:
    """Returns path_status, allowed, restricted, blocked, blocked_reason, review_required, traversal."""
    mapping = {
        "repo_fixture": ("allowed_repo_fixture_candidate", True, False, False, "", False, False),
        "eval_out_fixture": ("allowed_eval_out_fixture_candidate", True, False, False, "", False, False),
        "user_upload": ("restricted_user_upload_candidate", False, True, False, "", True, False),
        "external_absolute": ("blocked_external_absolute_path", False, False, True, "external_absolute_path_blocked", False, False),
        "path_traversal": ("blocked_path_traversal", False, False, True, "path_traversal_blocked", False, True),
        "symlink": ("restricted_symlink_candidate", False, True, False, "", True, False),
        "unknown": ("blocked_unknown_path", False, False, True, "unknown_path_blocked", False, False),
    }
    return mapping.get(path_type, mapping["unknown"])


def _declared_metadata(path_type: str, *, complete: bool = True, privacy_tags: Optional[List[str]] = None) -> Dict[str, Any]:
    if not complete:
        return {}
    tags = privacy_tags or ["public_space"]
    return {
        "declared_file_name": f"sim_{path_type}.jpg",
        "declared_extension": ".jpg",
        "declared_mime_type": "image/jpeg",
        "declared_size_bytes": 1024,
        "declared_created_at": "2026-01-01T00:00:00Z",
        "declared_modified_at": "2026-01-01T00:00:00Z",
        "declared_source": "manifest_stub",
        "declared_capture_context": "dryrun_simulation",
        "declared_privacy_tags": tags,
    }


def _simulate_case(spec: Dict[str, Any]) -> Dict[str, Any]:
    sid = spec["scenario_id"]
    case_type = spec.get("case_type", "path")
    path_type = spec.get("path_type", "repo_fixture")
    privacy_tags = spec.get("privacy_tags", ["public_space"])
    declared_complete = spec.get("declared_metadata_complete", True)
    hash_placeholder_present = spec.get("hash_placeholder_present", True)
    real_hash_attempt = spec.get("real_hash_attempt", False)
    exif_parse_attempt = spec.get("exif_parse_attempt", False)
    video_probe_attempt = spec.get("video_probe_attempt", False)
    perceptual_hash_request = spec.get("perceptual_hash_request", False)
    fixture_registry_entry = spec.get("fixture_registry_entry", case_type == "fixture_registry")
    manifest_mapping = spec.get("manifest_mapping", case_type == "manifest_mapping")

    path_status, allowed_path, restricted_path, blocked_path, blocked_reason, review_required, traversal = _path_decision(path_type)
    declared = _declared_metadata(path_type, complete=declared_complete, privacy_tags=privacy_tags)
    sensitive = any(t in PRIVACY_SENSITIVE_TAGS for t in privacy_tags)
    manual_review = review_required or sensitive or spec.get("manual_review_required", False)

    file_ref_id = f"file_ref_{sid}"
    dryrun_case_id = f"case_{sid}"

    stub = {
        "file_ref_id": file_ref_id,
        "sample_id": f"sample_{sid}",
        "path_placeholder": f"placeholder://{path_type}/{sid}",
        "path_type": path_type,
        "declared_metadata": declared,
        "hash_placeholder": "hash_placeholder_not_computed" if hash_placeholder_present else "",
        "privacy_tags": privacy_tags,
        "review_status": "pending_review" if manual_review else "not_required",
        "source_chain": SOURCE_CHAIN,
        "file_exists_verified": False,
        "file_stat_invoked": False,
        "file_opened": False,
        "content_read": False,
        "real_hash_computed": False,
        **_not_fact(),
    }

    path_decision = {
        "path_decision_id": f"path_dec_{sid}",
        "source_case_id": dryrun_case_id,
        "file_ref_id": file_ref_id,
        "path_type": path_type,
        "path_status": path_status,
        "allowed_path_candidate": allowed_path,
        "restricted_path_candidate": restricted_path,
        "blocked_path_candidate": blocked_path,
        "blocked_reason": blocked_reason,
        "review_required": review_required,
        "path_traversal_detected_candidate": traversal,
        "symlink_requires_review": path_type == "symlink",
        "file_operation_allowed": False,
        **_not_fact(),
    }

    existence_decision = {
        "existence_decision_id": f"exist_dec_{sid}",
        "source_case_id": dryrun_case_id,
        "file_ref_id": file_ref_id,
        "file_existence_check_allowed_now": False,
        "file_existence_check_invoked": False,
        "file_exists_verified": False,
        "existence_status": "not_checked",
        "future_check_candidate_allowed": allowed_path and not blocked_path,
        "required_gate": "FileBoundaryGate",
        "failure_mode": "block_if_gate_missing",
        **_not_fact(),
    }

    metadata_valid = bool(declared) and declared_complete
    metadata_blocked = not declared_complete
    if case_type == "metadata" and spec.get("scenario_id") == "missing_declared_metadata_blocked":
        metadata_blocked = True
        metadata_valid = False

    metadata_status = "metadata_candidate_allowed"
    if metadata_blocked:
        metadata_status = "missing_declared_metadata_blocked"
    elif sensitive or manual_review:
        metadata_status = "metadata_candidate_restricted"

    metadata_decision = {
        "metadata_decision_id": f"meta_dec_{sid}",
        "source_case_id": dryrun_case_id,
        "file_ref_id": file_ref_id,
        "declared_metadata_present": bool(declared),
        "declared_metadata_valid_candidate": metadata_valid and not metadata_blocked,
        "missing_declared_metadata_blocked": metadata_blocked,
        "external_metadata_read_allowed_now": False,
        "exif_parse_allowed_now": False,
        "video_probe_allowed_now": False,
        "metadata_status": metadata_status,
        "privacy_precheck_required": True,
        "manual_review_required": manual_review,
        **_not_fact(),
    }

    if exif_parse_attempt:
        metadata_decision["metadata_status"] = "exif_parse_attempt_blocked"
        metadata_decision["exif_parse_simulated_blocked"] = True
    if video_probe_attempt:
        metadata_decision["metadata_status"] = "video_probe_attempt_blocked"
        metadata_decision["video_probe_simulated_blocked"] = True

    hash_decision = {
        "hash_decision_id": f"hash_dec_{sid}",
        "source_case_id": dryrun_case_id,
        "file_ref_id": file_ref_id,
        "hash_placeholder_allowed": hash_placeholder_present and not real_hash_attempt,
        "real_hash_computation_allowed_now": False,
        "real_hash_attempt_blocked": real_hash_attempt,
        "perceptual_hash_deferred": perceptual_hash_request,
        "hash_currently_not_computed": True,
        "selected_hash_policy": "placeholder_only" if not real_hash_attempt else "real_hash_blocked",
        **_not_fact(),
    }
    if perceptual_hash_request:
        hash_decision["selected_hash_policy"] = "perceptual_hash_deferred"
    if real_hash_attempt:
        hash_decision["hash_placeholder_allowed"] = False

    fixture_decision = {
        "fixture_registry_decision_id": f"fixture_dec_{sid}",
        "source_case_id": dryrun_case_id,
        "fixture_id": f"fixture_{sid}" if fixture_registry_entry else "",
        "registry_entry_candidate_allowed": fixture_registry_entry,
        "registry_runtime_started": False,
        "file_exists_verified": False,
        "real_hash_computed": False,
        "content_read": False,
        "lifecycle_status_candidate": "candidate_only",
        "review_status": "pending_review" if manual_review else "not_required",
        **_not_fact(),
    }

    mapping_allowed = manifest_mapping or (metadata_valid and not blocked_path and not metadata_blocked)
    mapping_decision = {
        "mapping_decision_id": f"map_dec_{sid}",
        "source_case_id": dryrun_case_id,
        "sample_manifest_ref": "controlled_frame_sample_manifest_schema.json",
        "file_metadata_candidate_allowed": mapping_allowed,
        "source_chain_mapping_pass": True,
        "privacy_tag_mapping_pass": bool(privacy_tags),
        "declared_metadata_mapping_pass": metadata_valid,
        "manual_review_status_mapping_pass": not manual_review or review_required,
        "file_existence_required_now": False,
        "real_hash_required_now": False,
        "content_read_required": False,
        "output_candidate_ref": f"fmc_{sid}" if mapping_allowed else "",
        **_not_fact(),
    }

    violations: List[str] = []
    if real_hash_attempt:
        violations.append("real_hash_attempt_blocked")
    if exif_parse_attempt:
        violations.append("exif_parse_attempt_blocked")
    if video_probe_attempt:
        violations.append("video_probe_attempt_blocked")
    if blocked_path:
        violations.append(blocked_reason or "path_blocked")
    if metadata_blocked:
        violations.append("missing_declared_metadata")

    dryrun_status = "pass" if not violations or all(v.endswith("_blocked") or v == "real_hash_attempt_blocked" for v in violations) else "simulated_block"
    if blocked_path or metadata_blocked:
        dryrun_status = "simulated_block_expected"

    dryrun_result = {
        "result_id": f"result_{sid}",
        "source_case_id": dryrun_case_id,
        "path_decision_ref": path_decision["path_decision_id"],
        "existence_decision_ref": existence_decision["existence_decision_id"],
        "metadata_decision_ref": metadata_decision["metadata_decision_id"],
        "hash_decision_ref": hash_decision["hash_decision_id"],
        "fixture_registry_decision_ref": fixture_decision["fixture_registry_decision_id"],
        "mapping_decision_ref": mapping_decision["mapping_decision_id"],
        "dryrun_status": dryrun_status,
        "violations": violations,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    dryrun_case = {
        "dryrun_case_id": dryrun_case_id,
        "case_type": case_type,
        "simulated_file_ref": stub,
        "simulated_manifest_metadata": declared,
        "expected_path_legality_decision": path_status,
        "expected_file_existence_decision": "not_checked",
        "expected_external_metadata_decision": metadata_status,
        "expected_hash_policy_decision": hash_decision["selected_hash_policy"],
        "expected_fixture_registry_decision": "candidate_allowed" if fixture_registry_entry else "not_applicable",
        "expected_mapping_decision": "mapping_allowed" if mapping_allowed else "mapping_blocked",
        "expected_boundary_flags": {
            "file_stat_invoked": False,
            "file_opened": False,
            "content_read": False,
            "real_hash_computed": False,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "dryrun_case": dryrun_case,
        "stub": stub,
        "path_decision": path_decision,
        "existence_decision": existence_decision,
        "metadata_decision": metadata_decision,
        "hash_decision": hash_decision,
        "fixture_decision": fixture_decision,
        "mapping_decision": mapping_decision,
        "dryrun_result": dryrun_result,
        "path_category": "allowed_path" if allowed_path else ("restricted_path" if restricted_path else "blocked_path"),
        "metadata_category": "metadata_candidate" if case_type == "metadata" or spec.get("category") == "metadata_candidate" else "",
        "hash_category": case_type in {"hash_policy", "metadata_probe"} or spec.get("category") in {"hash_policy", "metadata_probe"},
    }


def run_controlled_frame_file_metadata_boundary_dryrun_v1(
    *,
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

    dryrun_case_schema = {
        "schema_name": "ControlledFrameFileMetadataBoundaryDryRunCase",
        "schema_version": "v1",
        "field_specs": [
            _field("dryrun_case_id", "string", True),
            _field("case_type", "string", True),
            _field("simulated_file_ref", "object", True),
            _field("simulated_manifest_metadata", "object", True),
            _field("expected_path_legality_decision", "string", True),
            _field("expected_file_existence_decision", "string", True),
            _field("expected_external_metadata_decision", "string", True),
            _field("expected_hash_policy_decision", "string", True),
            _field("expected_fixture_registry_decision", "string", True),
            _field("expected_mapping_decision", "string", True),
            _field("expected_boundary_flags", "object", True),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    simulated_file_ref_metadata_stub_schema = {
        "schema_name": "SimulatedFileRefMetadataStub",
        "schema_version": "v1",
        "field_specs": [
            _field("file_ref_id", "string", True),
            _field("sample_id", "string", True),
            _field("path_placeholder", "string", True),
            _field("path_type", "string", True),
            _field("declared_metadata", "object", True),
            _field("hash_placeholder", "string", True),
            _field("privacy_tags", "list", True),
            _field("review_status", "string", True),
            _field("source_chain", "string", True),
            _field("file_exists_verified", "boolean", True, default=False),
            _field("file_stat_invoked", "boolean", True, default=False),
            _field("file_opened", "boolean", True, default=False),
            _field("content_read", "boolean", True, default=False),
            _field("real_hash_computed", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
        ],
        "invariants": {
            "file_exists_verified": False,
            "file_stat_invoked": False,
            "file_opened": False,
            "content_read": False,
            "real_hash_computed": False,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    path_legality_decision_candidate_schema = {
        "schema_name": "PathLegalityDecisionCandidate",
        "schema_version": "v1",
        "path_status_values": [
            "allowed_repo_fixture_candidate",
            "allowed_eval_out_fixture_candidate",
            "restricted_user_upload_candidate",
            "restricted_symlink_candidate",
            "blocked_external_absolute_path",
            "blocked_path_traversal",
            "blocked_unknown_path",
        ],
        "field_specs": [
            _field("path_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("file_ref_id", "string", True),
            _field("path_type", "string", True),
            _field("path_status", "string", True),
            _field("allowed_path_candidate", "boolean", True),
            _field("restricted_path_candidate", "boolean", True),
            _field("blocked_path_candidate", "boolean", True),
            _field("blocked_reason", "string", False),
            _field("review_required", "boolean", True),
            _field("path_traversal_detected_candidate", "boolean", True),
            _field("symlink_requires_review", "boolean", True),
            _field("file_operation_allowed", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_existence_decision_candidate_schema = {
        "schema_name": "FileExistenceDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("existence_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("file_ref_id", "string", True),
            _field("file_existence_check_allowed_now", "boolean", True, default=False),
            _field("file_existence_check_invoked", "boolean", True, default=False),
            _field("file_exists_verified", "boolean", True, default=False),
            _field("existence_status", "string", True),
            _field("future_check_candidate_allowed", "boolean", True),
            _field("required_gate", "string", True),
            _field("failure_mode", "string", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    external_metadata_decision_candidate_schema = {
        "schema_name": "ExternalMetadataDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("metadata_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("file_ref_id", "string", True),
            _field("declared_metadata_present", "boolean", True),
            _field("declared_metadata_valid_candidate", "boolean", True),
            _field("missing_declared_metadata_blocked", "boolean", True),
            _field("external_metadata_read_allowed_now", "boolean", True, default=False),
            _field("exif_parse_allowed_now", "boolean", True, default=False),
            _field("video_probe_allowed_now", "boolean", True, default=False),
            _field("metadata_status", "string", True),
            _field("privacy_precheck_required", "boolean", True),
            _field("manual_review_required", "boolean", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    hash_policy_decision_candidate_schema = {
        "schema_name": "HashPolicyDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("hash_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("file_ref_id", "string", True),
            _field("hash_placeholder_allowed", "boolean", True),
            _field("real_hash_computation_allowed_now", "boolean", True, default=False),
            _field("real_hash_attempt_blocked", "boolean", True),
            _field("perceptual_hash_deferred", "boolean", True),
            _field("hash_currently_not_computed", "boolean", True, default=True),
            _field("selected_hash_policy", "string", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    fixture_registry_decision_candidate_schema = {
        "schema_name": "FixtureRegistryDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("fixture_registry_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("fixture_id", "string", True),
            _field("registry_entry_candidate_allowed", "boolean", True),
            _field("registry_runtime_started", "boolean", True, default=False),
            _field("file_exists_verified", "boolean", True, default=False),
            _field("real_hash_computed", "boolean", True, default=False),
            _field("content_read", "boolean", True, default=False),
            _field("lifecycle_status_candidate", "string", True),
            _field("review_status", "string", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    manifest_to_file_metadata_mapping_decision_candidate_schema = {
        "schema_name": "ManifestToFileMetadataMappingDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("mapping_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("sample_manifest_ref", "string", True),
            _field("file_metadata_candidate_allowed", "boolean", True),
            _field("source_chain_mapping_pass", "boolean", True),
            _field("privacy_tag_mapping_pass", "boolean", True),
            _field("declared_metadata_mapping_pass", "boolean", True),
            _field("manual_review_status_mapping_pass", "boolean", True),
            _field("file_existence_required_now", "boolean", True, default=False),
            _field("real_hash_required_now", "boolean", True, default=False),
            _field("content_read_required", "boolean", True, default=False),
            _field("output_candidate_ref", "string", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_metadata_boundary_dryrun_result_schema = {
        "schema_name": "FileMetadataBoundaryDryRunResult",
        "schema_version": "v1",
        "field_specs": [
            _field("result_id", "string", True),
            _field("source_case_id", "string", True),
            _field("path_decision_ref", "string", True),
            _field("existence_decision_ref", "string", True),
            _field("metadata_decision_ref", "string", True),
            _field("hash_decision_ref", "string", True),
            _field("fixture_registry_decision_ref", "string", True),
            _field("mapping_decision_ref", "string", True),
            _field("dryrun_status", "string", True),
            _field("violations", "list", True),
            _field("source_chain", "string", True),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    scenario_specs = [
        {"scenario_id": "repo_fixture_path_candidate", "case_type": "path", "path_type": "repo_fixture", "category": "allowed_path"},
        {"scenario_id": "eval_out_fixture_path_candidate", "case_type": "path", "path_type": "eval_out_fixture", "category": "allowed_path"},
        {"scenario_id": "user_uploaded_path_candidate", "case_type": "path", "path_type": "user_upload", "category": "restricted_path"},
        {"scenario_id": "external_absolute_path_blocked", "case_type": "path", "path_type": "external_absolute", "category": "blocked_path"},
        {"scenario_id": "path_traversal_blocked", "case_type": "path", "path_type": "path_traversal", "category": "blocked_path"},
        {"scenario_id": "symlink_requires_review", "case_type": "path", "path_type": "symlink", "category": "restricted_path"},
        {"scenario_id": "unknown_path_blocked", "case_type": "path", "path_type": "unknown", "category": "blocked_path"},
        {
            "scenario_id": "declared_metadata_public_image",
            "case_type": "metadata",
            "path_type": "repo_fixture",
            "category": "metadata_candidate",
            "privacy_tags": ["public_space"],
        },
        {
            "scenario_id": "declared_metadata_private_home",
            "case_type": "metadata",
            "path_type": "repo_fixture",
            "category": "metadata_candidate",
            "privacy_tags": ["private_home"],
            "manual_review_required": True,
        },
        {
            "scenario_id": "missing_declared_metadata_blocked",
            "case_type": "metadata",
            "path_type": "repo_fixture",
            "category": "metadata_candidate",
            "declared_metadata_complete": False,
        },
        {
            "scenario_id": "hash_placeholder_allowed",
            "case_type": "hash_policy",
            "path_type": "repo_fixture",
            "category": "hash_policy",
            "hash_placeholder_present": True,
        },
        {
            "scenario_id": "real_hash_attempt_blocked",
            "case_type": "hash_policy",
            "path_type": "repo_fixture",
            "category": "hash_policy",
            "real_hash_attempt": True,
        },
        {
            "scenario_id": "exif_parse_attempt_blocked",
            "case_type": "metadata_probe",
            "path_type": "repo_fixture",
            "category": "metadata_probe",
            "exif_parse_attempt": True,
        },
        {
            "scenario_id": "video_probe_attempt_blocked",
            "case_type": "metadata_probe",
            "path_type": "repo_fixture",
            "category": "metadata_probe",
            "video_probe_attempt": True,
        },
        {
            "scenario_id": "perceptual_hash_deferred",
            "case_type": "hash_policy",
            "path_type": "repo_fixture",
            "category": "hash_policy",
            "perceptual_hash_request": True,
        },
        {
            "scenario_id": "fixture_registry_entry_candidate",
            "case_type": "fixture_registry",
            "path_type": "repo_fixture",
            "fixture_registry_entry": True,
        },
        {
            "scenario_id": "manifest_to_metadata_mapping_candidate",
            "case_type": "manifest_mapping",
            "path_type": "repo_fixture",
            "manifest_mapping": True,
        },
        {
            "scenario_id": "metadata_sensitive_requires_manual_review",
            "case_type": "metadata",
            "path_type": "user_upload",
            "category": "metadata_candidate",
            "privacy_tags": ["medical_context_possible", "screen_or_document_possible"],
            "manual_review_required": True,
        },
    ]

    scenario_matrix_rows = [
        {
            **spec,
            "metadata_decision_simulation_only": True,
            "file_stat_invoked": False,
            "file_opened": False,
            "content_read": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for spec in scenario_specs
    ]

    controlled_frame_file_metadata_boundary_dryrun_scenario_matrix = {
        "scenarios": scenario_matrix_rows,
        "scenario_count": len(scenario_matrix_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    simulated_results = [_simulate_case(spec) for spec in scenario_specs]

    dryrun_cases = [r["dryrun_case"] for r in simulated_results]
    path_legality_decision_results = [r["path_decision"] for r in simulated_results]
    file_existence_decision_results = [r["existence_decision"] for r in simulated_results]
    external_metadata_decision_results = [r["metadata_decision"] for r in simulated_results]
    hash_policy_decision_results = [r["hash_decision"] for r in simulated_results]
    fixture_registry_decision_results = [r["fixture_decision"] for r in simulated_results]
    manifest_to_file_metadata_mapping_results = [r["mapping_decision"] for r in simulated_results]
    controlled_frame_file_metadata_boundary_dryrun_results = [r["dryrun_result"] for r in simulated_results]

    allowed_path_count = sum(1 for r in simulated_results if r["path_category"] == "allowed_path")
    restricted_path_count = sum(1 for r in simulated_results if r["path_category"] == "restricted_path")
    blocked_path_count = sum(1 for r in simulated_results if r["path_category"] == "blocked_path")
    metadata_candidate_case_count = sum(
        1 for s in scenario_specs if s.get("category") == "metadata_candidate" or s.get("case_type") == "metadata"
    )
    hash_policy_case_count = sum(
        1 for s in scenario_specs if s.get("category") in {"hash_policy", "metadata_probe"} or s.get("case_type") in {"hash_policy", "metadata_probe"}
    )
    fixture_registry_candidate_generated = any(s.get("fixture_registry_entry") for s in scenario_specs)
    manifest_to_file_metadata_mapping_generated = any(s.get("manifest_mapping") for s in scenario_specs)

    file_metadata_boundary_matrix = {
        "frozen_boundaries": [
            "no-file-stat",
            "no-file-open",
            "no-image-read",
            "no-video-read",
            "no-exif-parse",
            "no-video-probe",
            "no-real-hash",
            "no-perceptual-hash",
            "metadata-decision-simulation-only",
            "declared-metadata-only",
            "no-runtime",
            "no-write",
            "no-action",
            "no-speech",
        ],
        "simulated_now": {
            "path_legality_decision": True,
            "external_metadata_decision": True,
            "hash_policy_decision": True,
            "fixture_registry_candidate": True,
            "manifest_mapping_candidate": True,
        },
        "blocked_now": {
            "file_existence_check": True,
            "file_stat": True,
            "file_open": True,
            "real_hash_computation": True,
            "exif_parse": True,
            "video_probe": True,
            "content_read": True,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "carryover_topics": [
            {"topic": "post-dryrun review of metadata boundary simulation gaps", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "guarded file existence check planning deferred", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "filesystem vs declared metadata reconciliation", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "fixture registry lifecycle after dryrun review", "source_chain": SOURCE_CHAIN, **_not_fact()},
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "metadata/file-boundary dry-run simulation completed without real file operations",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not file_metadata_boundary_planning_input_loaded:
        blockers.append("file_metadata_boundary_planning_missing")
    if not all(
        [
            post_controlled_frame_sample_roadmap_input_loaded,
            controlled_frame_sample_closure_input_loaded,
            controlled_frame_sample_post_review_input_loaded,
            controlled_frame_sample_dryrun_input_loaded,
            controlled_frame_sample_planning_input_loaded,
            controlled_frame_input_closure_input_loaded,
            map_location_readonly_context_input_loaded,
            safety_constitution_input_loaded,
            minimal_runtime_integration_closure_loaded,
            ocr_final_closure_loaded,
        ]
    ):
        blockers.append("required_root_missing_or_invalid")
    if len(scenario_specs) < 18:
        blockers.append("scenario_matrix_insufficient")

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
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
        "dryrun_case_schema_defined": True,
        "simulated_file_ref_metadata_stub_schema_defined": True,
        "path_legality_decision_candidate_schema_defined": True,
        "file_existence_decision_candidate_schema_defined": True,
        "external_metadata_decision_candidate_schema_defined": True,
        "hash_policy_decision_candidate_schema_defined": True,
        "fixture_registry_decision_candidate_schema_defined": True,
        "manifest_to_file_metadata_mapping_decision_candidate_schema_defined": True,
        "file_metadata_boundary_dryrun_result_schema_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(scenario_specs),
        "dryrun_results_generated": True,
        "allowed_path_candidate_count": allowed_path_count,
        "restricted_path_candidate_count": restricted_path_count,
        "blocked_path_candidate_count": blocked_path_count,
        "metadata_candidate_case_count": metadata_candidate_case_count,
        "hash_policy_case_count": hash_policy_case_count,
        "fixture_registry_candidate_generated": fixture_registry_candidate_generated,
        "manifest_to_file_metadata_mapping_generated": manifest_to_file_metadata_mapping_generated,
        "metadata_decision_simulation_only": True,
        "file_existence_check_allowed_now": False,
        "path_legality_check_allowed_now": False,
        "external_metadata_read_allowed_now": False,
        "real_hash_computation_allowed_now": False,
        "hash_placeholder_allowed": True,
        "perceptual_hash_deferred": True,
        "no_exif_parse_now": True,
        "no_video_probe_now": True,
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
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "dryrun_case_schema": dryrun_case_schema,
        "simulated_file_ref_metadata_stub_schema": simulated_file_ref_metadata_stub_schema,
        "path_legality_decision_candidate_schema": path_legality_decision_candidate_schema,
        "file_existence_decision_candidate_schema": file_existence_decision_candidate_schema,
        "external_metadata_decision_candidate_schema": external_metadata_decision_candidate_schema,
        "hash_policy_decision_candidate_schema": hash_policy_decision_candidate_schema,
        "fixture_registry_decision_candidate_schema": fixture_registry_decision_candidate_schema,
        "manifest_to_file_metadata_mapping_decision_candidate_schema": manifest_to_file_metadata_mapping_decision_candidate_schema,
        "file_metadata_boundary_dryrun_result_schema": file_metadata_boundary_dryrun_result_schema,
        "controlled_frame_file_metadata_boundary_dryrun_scenario_matrix": controlled_frame_file_metadata_boundary_dryrun_scenario_matrix,
        "controlled_frame_file_metadata_boundary_dryrun_results": {
            "results": controlled_frame_file_metadata_boundary_dryrun_results,
            "result_count": len(controlled_frame_file_metadata_boundary_dryrun_results),
            "cases": dryrun_cases,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "path_legality_decision_results": {
            "decisions": path_legality_decision_results,
            "decision_count": len(path_legality_decision_results),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "file_existence_decision_results": {
            "decisions": file_existence_decision_results,
            "decision_count": len(file_existence_decision_results),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "external_metadata_decision_results": {
            "decisions": external_metadata_decision_results,
            "decision_count": len(external_metadata_decision_results),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "hash_policy_decision_results": {
            "decisions": hash_policy_decision_results,
            "decision_count": len(hash_policy_decision_results),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "fixture_registry_decision_results": {
            "decisions": fixture_registry_decision_results,
            "decision_count": len(fixture_registry_decision_results),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "manifest_to_file_metadata_mapping_results": {
            "decisions": manifest_to_file_metadata_mapping_results,
            "decision_count": len(manifest_to_file_metadata_mapping_results),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "file_metadata_boundary_matrix": file_metadata_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": _no_file_operation_payload(),
        "no_runtime_boundary_report": _no_runtime_payload(),
        "no_write_boundary_report": _no_runtime_payload(),
    }
