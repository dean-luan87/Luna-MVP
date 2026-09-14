# -*- coding: utf-8 -*-
"""Controlled Frame File Metadata Boundary Planning v1 (planning-only).

Defines future file existence / path legality / external metadata / real hash / fixture registry
boundaries WITHOUT stat, open, read, decode, probe, or hash computation in this phase.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001"
PLANNING_ID = "cffmbp_v1_001"
PLANNING_SCOPE = "controlled_frame_file_metadata_boundary_planning_only"
SOURCE_CHAIN = "controlled_frame_file_metadata_boundary_planning_v1"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001"

POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION = (
    "POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION_READY_FOR_FILE_METADATA_BOUNDARY_PLANNING"
)
CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION = "CONTROLLED_FRAME_SAMPLE_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_SAMPLE_POST_REVIEW_DECISION = "CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
CONTROLLED_FRAME_SAMPLE_DRYRUN_DECISION = "CONTROLLED_FRAME_SAMPLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
CONTROLLED_FRAME_SAMPLE_PLANNING_DECISION = "CONTROLLED_FRAME_SAMPLE_PLANNING_READY_FOR_CONTROLLED_FRAME_SAMPLE_DRYRUN"
POST_CROSSING_DECISION_ROADMAP_DECISION = (
    "POST_CROSSING_DECISION_ROADMAP_DECISION_READY_FOR_CONTROLLED_FRAME_SAMPLE_PLANNING"
)
CROSSING_DECISION_CLOSURE_DECISION = "CROSSING_DECISION_CLOSED_FOR_CURRENT_MAINLINE"
CONTROLLED_FRAME_INPUT_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "post_controlled_frame_sample_roadmap_decision",
        "arg": "post_controlled_frame_sample_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "recommended_next_phase_decision.json"],
    },
    {
        "id": "controlled_frame_sample_closure",
        "arg": "controlled_frame_sample_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_sample_closure_summary.json"],
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
        "artifacts": ["summary.json", "controlled_frame_sample_manifest_schema.json", "file_boundary_policy.json"],
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

METADATA_FIELDS_CANDIDATE = [
    "declared_file_name",
    "declared_extension",
    "declared_mime_type",
    "declared_size_bytes",
    "declared_created_at",
    "declared_modified_at",
    "declared_source",
    "declared_capture_context",
    "declared_privacy_tags",
]

FORBIDDEN_METADATA_FIELDS = [
    "exif_gps_coordinates",
    "exif_device_serial",
    "embedded_thumbnail_bytes",
    "raw_video_codec_probe",
    "filesystem_inode",
    "actual_file_stat_mtime",
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
        "planning_scope": PLANNING_SCOPE,
        "planning_only": True,
        "no_file_stat": True,
        "no_file_open": True,
        "no_image_read": True,
        "no_video_read": True,
        "no_video_decode": True,
        "no_frame_extract": True,
        "no_real_hash_computation": True,
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
        "planning_scope": PLANNING_SCOPE,
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


def run_controlled_frame_file_metadata_boundary_planning_v1(
    *,
    post_controlled_frame_sample_roadmap_decision_root: str,
    controlled_frame_sample_closure_root: str,
    controlled_frame_sample_post_review_root: str,
    controlled_frame_sample_dryrun_root: str,
    controlled_frame_sample_planning_root: str,
    post_crossing_decision_roadmap_decision_root: str,
    crossing_decision_closure_root: str,
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

    file_existence_check_policy = {
        "policy_name": "FileExistenceCheckPolicy",
        "file_existence_check_allowed_now": False,
        "future_file_existence_check_allowed_candidate": True,
        "required_gate": [
            "FileBoundaryGate",
            "PathLegalityGate",
            "PrivacyPrecheckGate",
            "ManualReviewGateIfSensitive",
            "FixtureRegistryAuthorizationGate",
        ],
        "required_user_or_fixture_registry_authorization": True,
        "allowed_input": ["manifest_declared_path_placeholder", "fixture_registry_entry"],
        "blocked_input": ["arbitrary_absolute_path", "unregistered_user_upload_without_review"],
        "output_candidate_type": "FileExistenceCheckCandidate",
        "no_content_read_guarantee": True,
        "failure_mode": "block_if_gate_missing_or_path_not_allowed",
        "notes": ["current phase does not execute file exists / stat / open"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    path_legality_policy = {
        "policy_name": "PathLegalityPolicy",
        "path_legality_check_allowed_now": False,
        "allowed_path_pattern_candidate": [
            "repo_fixture_path_candidate",
            "eval_out_fixture_path_candidate",
        ],
        "blocked_path_pattern_candidate": [
            "external_absolute_path_blocked",
            "path_traversal_blocked",
            "unknown_path_blocked",
        ],
        "restricted_path_pattern_candidate": [
            "user_uploaded_path_candidate",
            "symlink_requires_review",
        ],
        "sandbox_required": True,
        "repository_fixture_dir_candidate": "fixtures/controlled_samples/",
        "absolute_path_policy": "blocked_unless_explicitly_registered_fixture",
        "relative_path_policy": "allowed_only_within_registered_fixture_roots",
        "symlink_policy": "restricted_requires_manual_review",
        "external_path_policy": "blocked",
        "user_upload_path_policy": "restricted_requires_manual_review_if_sensitive",
        "path_traversal_block_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    external_metadata_boundary_policy = {
        "policy_name": "ExternalMetadataBoundaryPolicy",
        "external_metadata_read_allowed_now": False,
        "metadata_fields_candidate": METADATA_FIELDS_CANDIDATE,
        "metadata_source_policy": "declared_manifest_metadata_only",
        "privacy_precheck_required": True,
        "manual_review_required_if_sensitive": True,
        "forbidden_metadata_fields": FORBIDDEN_METADATA_FIELDS,
        "no_image_decode": True,
        "no_exif_parse_now": True,
        "no_video_probe_now": True,
        "notes": [
            "current phase uses declared metadata / manifest metadata only",
            "does not read filesystem metadata",
            "does not parse EXIF",
            "does not probe video",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    real_hash_computation_policy = {
        "policy_name": "RealHashComputationPolicy",
        "real_hash_computation_allowed_now": False,
        "hash_placeholder_allowed": True,
        "future_hash_algorithm_candidate": ["sha256", "blake3"],
        "perceptual_hash_deferred": True,
        "required_file_boundary_gate": True,
        "required_privacy_precheck": True,
        "required_manual_review_if_sensitive": True,
        "hash_does_not_imply_content_analysis": True,
        "hash_currently_not_computed": True,
        "notes": ["perceptual hash is content analysis and must remain deferred"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    fixture_registry_entry_schema = {
        "schema_name": "FixtureRegistryEntrySchema",
        "schema_version": "v1",
        "field_specs": [
            _field("fixture_id", "string", True),
            _field("sample_id", "string", True),
            _field("file_ref_placeholder", "string", True),
            _field("path_placeholder", "string", True),
            _field("declared_metadata", "object", True),
            _field("hash_placeholder", "string", True),
            _field("privacy_tags", "list", True),
            _field("review_status", "string", True),
            _field("allowed_usage_scope", "string", True),
            _field("source_chain", "string", True),
            _field("lifecycle_status", "string", True),
            _field("file_exists_verified", "boolean", True, default=False),
            _field("real_hash_computed", "boolean", True, default=False),
            _field("content_read", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
        ],
        "invariants": {
            "file_exists_verified": False,
            "real_hash_computed": False,
            "content_read": False,
            "fact_status": "not_fact",
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    fixture_registry_policy = {
        "policy_name": "FixtureRegistryPolicy",
        "fixture_registry_defined": True,
        "registry_runtime_allowed": False,
        "registry_entry_schema_ref": "fixture_registry_entry_schema.json",
        "allowed_fixture_source_types": ["repo_fixture", "eval_out_fixture", "simulation_fixture"],
        "restricted_fixture_source_types": ["user_uploaded_fixture"],
        "blocked_fixture_source_types": ["external_absolute_path", "unknown_source"],
        "required_fields": [
            "fixture_id",
            "sample_id",
            "path_placeholder",
            "declared_metadata",
            "hash_placeholder",
            "privacy_tags",
            "review_status",
            "source_chain",
        ],
        "review_status_policy": "manual_review_required_for_restricted_tags",
        "lifecycle_policy": "candidate_only_until_future_dryrun",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    manifest_to_file_metadata_candidate_mapping_policy = {
        "policy_name": "ManifestToFileMetadataCandidateMappingPolicy",
        "sample_manifest_ref": "controlled_frame_sample_manifest_schema.json",
        "file_metadata_candidate_allowed": True,
        "source_chain_mapping_required": True,
        "privacy_tag_mapping_required": True,
        "declared_metadata_mapping_required": True,
        "manual_review_status_mapping_required": True,
        "file_existence_required_now": False,
        "real_hash_required_now": False,
        "content_read_required": False,
        "output_candidate_type": "FileMetadataCandidate",
        "mapping_principles": [
            "upgrade manifest placeholders to file metadata candidate without file operations",
            "inherit privacy precheck and manual review gate from sample planning",
            "path legality evaluated as candidate only",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_metadata_candidate_schema = {
        "schema_name": "FileMetadataCandidateSchema",
        "schema_version": "v1",
        "field_specs": [
            _field("file_metadata_candidate_id", "string", True),
            _field("sample_id", "string", True),
            _field("file_ref_placeholder", "string", True),
            _field("path_legality_candidate", "string", True),
            _field("declared_metadata", "object", True),
            _field("hash_placeholder", "string", True),
            _field("fixture_registry_ref", "string", False),
            _field("privacy_precheck_ref", "string", True),
            _field("manual_review_ref", "string", False),
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
            "fact_status": "not_fact",
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_file_metadata_boundary_planning_policy = {
        "policy_id": PLANNING_ID,
        "policy_scope": PLANNING_SCOPE,
        "planning_only": True,
        "no_file_stat": True,
        "no_file_open": True,
        "no_image_read": True,
        "no_video_read": True,
        "no_video_decode": True,
        "no_frame_extract": True,
        "no_real_hash_computation": True,
        "file_existence_policy_ref": "file_existence_check_policy.json",
        "path_legality_policy_ref": "path_legality_policy.json",
        "external_metadata_boundary_ref": "external_metadata_boundary_policy.json",
        "real_hash_policy_ref": "real_hash_computation_policy.json",
        "fixture_registry_policy_ref": "fixture_registry_policy.json",
        "manifest_to_file_metadata_candidate_mapping_ref": "manifest_to_file_metadata_candidate_mapping_policy.json",
        "privacy_precheck_inheritance_ref": "controlled_frame_sample_planning:privacy_precheck_policy.json",
        "manual_review_gate_inheritance_ref": "controlled_frame_sample_planning:manual_review_gate_policy.json",
        "no_file_operation_boundary_ref": "no_file_operation_boundary_report.json",
        "no_runtime_boundary_ref": "no_runtime_boundary_report.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    scenario_specs = [
        {
            "scenario_id": "repo_fixture_path_candidate",
            "category": "allowed_path",
            "path_type": "repo_fixture",
            "file_stat_invoked": False,
            "metadata_candidate_allowed": True,
        },
        {
            "scenario_id": "eval_out_fixture_path_candidate",
            "category": "allowed_path",
            "path_type": "eval_out_fixture",
            "file_stat_invoked": False,
            "metadata_candidate_allowed": True,
        },
        {
            "scenario_id": "user_uploaded_path_candidate",
            "category": "restricted_path",
            "path_type": "user_upload",
            "manual_review_required_if_sensitive": True,
            "file_stat_invoked": False,
        },
        {
            "scenario_id": "external_absolute_path_blocked",
            "category": "blocked_path",
            "path_type": "external_absolute",
            "blocked": True,
        },
        {
            "scenario_id": "path_traversal_blocked",
            "category": "blocked_path",
            "path_type": "path_traversal",
            "blocked": True,
        },
        {
            "scenario_id": "symlink_requires_review",
            "category": "restricted_path",
            "path_type": "symlink",
            "manual_review_required": True,
        },
        {
            "scenario_id": "unknown_path_blocked",
            "category": "blocked_path",
            "path_type": "unknown",
            "blocked": True,
        },
        {
            "scenario_id": "declared_metadata_public_image",
            "category": "metadata_candidate",
            "privacy_tags": ["public_space"],
            "metadata_candidate_allowed": True,
            "declared_metadata_complete": True,
        },
        {
            "scenario_id": "declared_metadata_private_home",
            "category": "metadata_candidate",
            "privacy_tags": ["private_home"],
            "metadata_candidate_allowed": "restricted",
            "manual_review_required": True,
        },
        {
            "scenario_id": "missing_declared_metadata_blocked",
            "category": "metadata_candidate",
            "declared_metadata_complete": False,
            "blocked": True,
        },
        {
            "scenario_id": "hash_placeholder_allowed",
            "category": "hash_policy",
            "hash_placeholder_present": True,
            "real_hash_computed": False,
        },
        {
            "scenario_id": "real_hash_attempt_blocked",
            "category": "hash_policy",
            "real_hash_attempt": True,
            "blocked": True,
            "real_hash_computation_allowed_now": False,
        },
        {
            "scenario_id": "exif_parse_attempt_blocked",
            "category": "metadata_probe",
            "exif_parse_attempt": True,
            "blocked": True,
            "no_exif_parse_now": True,
        },
        {
            "scenario_id": "video_probe_attempt_blocked",
            "category": "metadata_probe",
            "video_probe_attempt": True,
            "blocked": True,
            "no_video_probe_now": True,
        },
        {
            "scenario_id": "perceptual_hash_deferred",
            "category": "hash_policy",
            "perceptual_hash_request": True,
            "deferred": True,
            "perceptual_hash_deferred": True,
        },
        {
            "scenario_id": "fixture_registry_entry_candidate",
            "category": "fixture_registry",
            "fixture_registry_entry_generated": True,
            "registry_runtime_allowed": False,
        },
    ]

    scenario_rows = [
        {
            **spec,
            "planning_only": True,
            "file_existence_check_invoked": False,
            "file_stat_invoked": spec.get("file_stat_invoked", False),
            "file_opened": False,
            "content_read": False,
            "real_hash_computed": spec.get("real_hash_computed", False),
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for spec in scenario_specs
    ]

    controlled_frame_file_metadata_boundary_planning_scenario_matrix = {
        "scenarios": scenario_rows,
        "scenario_count": len(scenario_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    allowed_path_count = sum(1 for s in scenario_specs if s.get("category") == "allowed_path")
    restricted_path_count = sum(1 for s in scenario_specs if s.get("category") == "restricted_path")
    blocked_path_count = sum(1 for s in scenario_specs if s.get("category") == "blocked_path")
    metadata_candidate_case_count = sum(1 for s in scenario_specs if s.get("category") == "metadata_candidate")
    hash_policy_case_count = sum(1 for s in scenario_specs if s.get("category") in {"hash_policy", "metadata_probe"})

    file_metadata_boundary_matrix = {
        "frozen_boundaries": [
            "no-file-stat",
            "no-file-open",
            "no-image-read",
            "no-video-read",
            "no-video-decode",
            "no-frame-extract",
            "no-exif-parse",
            "no-video-probe",
            "no-real-hash",
            "no-perceptual-hash",
            "declared-metadata-only",
            "fixture-registry-candidate-only",
            "manifest-to-file-metadata-candidate-stub-only",
            "no-runtime",
            "no-write",
            "no-action",
            "no-speech",
        ],
        "allowed_now": {
            "path_legality_planning": True,
            "external_metadata_boundary_planning": True,
            "hash_placeholder": True,
            "fixture_registry_schema": True,
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
            {"topic": "future file existence gate implementation", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "path sandbox normalization for fixture roots", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "declared vs filesystem metadata reconciliation", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "real hash computation policy vs privacy review", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "fixture registry lifecycle and review workflow", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "guarded image read preplan deferred", "source_chain": SOURCE_CHAIN, **_not_fact()},
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "file/metadata boundary policies and schemas defined; next step is metadata-only dry-run without real file operations",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
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
    if len(scenario_specs) < 16:
        blockers.append("scenario_matrix_insufficient")

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
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
        "controlled_frame_file_metadata_boundary_policy_defined": True,
        "file_existence_check_policy_defined": True,
        "path_legality_policy_defined": True,
        "external_metadata_boundary_policy_defined": True,
        "real_hash_computation_policy_defined": True,
        "fixture_registry_policy_defined": True,
        "fixture_registry_entry_schema_defined": True,
        "manifest_to_file_metadata_candidate_mapping_policy_defined": True,
        "file_metadata_candidate_schema_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(scenario_specs),
        "allowed_path_candidate_count": allowed_path_count,
        "restricted_path_candidate_count": restricted_path_count,
        "blocked_path_candidate_count": blocked_path_count,
        "metadata_candidate_case_count": metadata_candidate_case_count,
        "hash_policy_case_count": hash_policy_case_count,
        "fixture_registry_candidate_defined": True,
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
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_frame_file_metadata_boundary_planning_policy": controlled_frame_file_metadata_boundary_planning_policy,
        "file_existence_check_policy": file_existence_check_policy,
        "path_legality_policy": path_legality_policy,
        "external_metadata_boundary_policy": external_metadata_boundary_policy,
        "real_hash_computation_policy": real_hash_computation_policy,
        "fixture_registry_policy": fixture_registry_policy,
        "fixture_registry_entry_schema": fixture_registry_entry_schema,
        "manifest_to_file_metadata_candidate_mapping_policy": manifest_to_file_metadata_candidate_mapping_policy,
        "file_metadata_candidate_schema": file_metadata_candidate_schema,
        "controlled_frame_file_metadata_boundary_planning_scenario_matrix": controlled_frame_file_metadata_boundary_planning_scenario_matrix,
        "file_metadata_boundary_matrix": file_metadata_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": _no_file_operation_payload(),
        "no_runtime_boundary_report": _no_runtime_payload(),
        "no_write_boundary_report": _no_runtime_payload(),
    }
