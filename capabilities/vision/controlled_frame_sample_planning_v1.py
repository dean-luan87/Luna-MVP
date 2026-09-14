# -*- coding: utf-8 -*-
"""Controlled Frame Sample Planning v1 (planning-only).

This phase defines how controlled real files / static images / prerecorded frames
may later enter Luna evaluation chain via manifest-level governance, WITHOUT
opening or reading any image/video content in this phase.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-Sample-Planning-v1-001"
PLANNING_ID = "cfspp_v1_001"
PLANNING_SCOPE = "controlled_frame_sample_planning_only"
SOURCE_CHAIN = "controlled_frame_sample_planning_v1"
FINAL_DECISION = "CONTROLLED_FRAME_SAMPLE_PLANNING_READY_FOR_CONTROLLED_FRAME_SAMPLE_DRYRUN"
NEXT_PHASE = "Phase-Controlled-Frame-Sample-DryRun-v1-001"

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
    # Optional roots: present if exists, but must not fail if missing.
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

SAMPLE_TYPES = [
    "static_image_file_placeholder",
    "prerecorded_video_file_placeholder",
    "extracted_frame_file_placeholder",
    "simulation_frame_file_placeholder",
    "synthetic_image_placeholder",
    "controlled_uploaded_image_placeholder",
    "controlled_uploaded_video_placeholder",
    "live_camera_sample_placeholder",
    # Explicit governance-only placeholders
    "device_camera_sample_placeholder",
    "external_stream_sample_placeholder",
    "home_private_space_sample_placeholder",
    "medical_context_sample_placeholder",
    "child_or_school_context_sample_placeholder",
    "screen_document_sample_placeholder",
    "unknown_source_sample",
]

PRIVACY_TAGS = [
    "public_space",
    "private_home",
    "bystander_possible",
    "face_possible",
    "license_plate_possible",
    "screen_or_document_possible",
    "child_or_school_possible",
    "medical_context_possible",
    "workplace_possible",
    "commercial_sensitive_possible",
    "unknown_privacy",
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


def _field(name: str, field_type: str, required: bool, **extras: Any) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"name": name, "type": field_type, "required": required}
    payload.update(extras)
    return payload


def _no_runtime_payload() -> Dict[str, Any]:
    # Strict "planning only" boundary report; mirrors summary constraints.
    return {
        "planning_scope": PLANNING_SCOPE,
        "controlled_sample_dryrun_started": False,
        "manifest_only_processing": True,
        "sample_manifest_not_sample_processing": True,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "file_opened": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
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
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_controlled_frame_sample_planning_v1(
    *,
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

    controlled_frame_sample_planning_policy = {
        "policy_id": PLANNING_ID,
        "policy_scope": PLANNING_SCOPE,
        "allowed_sample_types": [
            "static_image_file_placeholder",
            "prerecorded_video_file_placeholder",
            "extracted_frame_file_placeholder",
            "simulation_frame_file_placeholder",
            "synthetic_image_placeholder",
        ],
        "blocked_sample_types": [
            "live_camera_sample_placeholder",
            "device_camera_sample_placeholder",
            "external_stream_sample_placeholder",
            "unknown_source_sample",
        ],
        "restricted_sample_types": [
            "controlled_uploaded_image_placeholder",
            "controlled_uploaded_video_placeholder",
            "home_private_space_sample_placeholder",
            "medical_context_sample_placeholder",
            "child_or_school_context_sample_placeholder",
            "screen_document_sample_placeholder",
        ],
        "sample_manifest_schema_ref": "controlled_frame_sample_manifest_schema.json",
        "sample_source_policy_ref": "sample_source_policy.json",
        "file_boundary_policy_ref": "file_boundary_policy.json",
        "privacy_precheck_policy_ref": "privacy_precheck_policy.json",
        "manual_review_gate_ref": "manual_review_gate_policy.json",
        "sample_usage_policy_ref": "sample_usage_policy.json",
        "sample_to_frame_candidate_mapping_ref": "sample_to_frame_candidate_mapping_policy.json",
        "no_runtime_boundary_ref": "no_runtime_boundary_report.json",
        "no_write_boundary_ref": "no_write_boundary_report.json",
        "planning_only": True,
        "no_file_content_read": True,
        "no_image_content_read": True,
        "no_video_decode": True,
        "no_model_inference": True,
        "manifest_only_processing": True,
        "sample_manifest_not_sample_processing": True,
        "source_chain": SOURCE_CHAIN,
        "non_claims": [
            "planning only",
            "no file content read",
            "no image content read",
            "no video decode",
            "no model inference",
            "sample manifest != sample processing",
        ],
        **_not_fact(),
    }

    controlled_frame_sample_manifest_schema = {
        "schema_name": "ControlledFrameSampleManifestSchema",
        "schema_version": "v1",
        "sample_type_enum": SAMPLE_TYPES,
        "privacy_tag_enum": PRIVACY_TAGS,
        "field_specs": [
            _field("sample_id", "string", True),
            _field("sample_type", "enum", True, allowed_values=SAMPLE_TYPES),
            _field("sample_origin", "string", True),
            _field("file_path_placeholder", "string", True),
            _field("file_hash_placeholder", "string", True),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
            _field("capture_context_placeholder", "string", False),
            _field("timestamp_placeholder", "string", False),
            _field("location_context_placeholder", "string", False),
            _field("task_context_placeholder", "string", False),
            _field("privacy_precheck_tags", "list", True, allowed_values=PRIVACY_TAGS),
            _field("expected_usage_scope", "string", True),
            _field("manual_review_required", "boolean", True),
            _field("sample_status", "string", True),
            _field("allowed_for_future_dryrun_candidate", "boolean", True),
            _field("allowed_for_runtime", "boolean", True, default=False),
            _field("content_read_allowed_now", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
        ],
        "invariants": {
            "allowed_for_runtime": False,
            "content_read_allowed_now": False,
            "manifest_only_processing": True,
            "sample_manifest_not_sample_processing": True,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    sample_source_policy = {
        "policy_name": "SampleSourcePolicy",
        "allowed_sample_types": [
            "static_image_file_placeholder",
            "prerecorded_video_file_placeholder",
            "extracted_frame_file_placeholder",
            "simulation_frame_file_placeholder",
            "synthetic_image_placeholder",
        ],
        "restricted_sample_types": [
            "controlled_uploaded_image_placeholder",
            "controlled_uploaded_video_placeholder",
            "home_private_space_sample_placeholder",
            "medical_context_sample_placeholder",
            "child_or_school_context_sample_placeholder",
            "screen_document_sample_placeholder",
        ],
        "blocked_sample_types": [
            "live_camera_sample_placeholder",
            "device_camera_sample_placeholder",
            "external_stream_sample_placeholder",
            "unknown_source_sample",
            "no_source_chain_sample",
            "no_privacy_precheck_sample",
        ],
        "source_chain_required": True,
        "privacy_precheck_required": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_boundary_policy = {
        "policy_name": "FileBoundaryPolicy",
        "file_existence_check_allowed": False,
        "file_open_allowed": False,
        "image_read_allowed": False,
        "video_decode_allowed": False,
        "frame_extract_allowed": False,
        "metadata_stub_allowed": True,
        "path_placeholder_allowed": True,
        "hash_placeholder_allowed": True,
        "manifest_only_processing": True,
        "sample_copy_allowed": False,
        "sample_upload_allowed": False,
        "sample_export_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    privacy_precheck_policy = {
        "policy_name": "PrivacyPrecheckPolicy",
        "privacy_precheck_required": True,
        "precheck_source": ["metadata_stub", "user_provided_tags", "directory_class", "sample_declaration"],
        "privacy_tag_required": True,
        "restricted_if_uncertain": True,
        "block_if_missing_privacy_tags": True,
        "manual_review_required_if_sensitive": True,
        "no_face_recognition": True,
        "no_identity_inference": True,
        "no_emotion_inference": True,
        "no_long_term_storage_decision": True,
        "privacy_tags": PRIVACY_TAGS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    manual_review_gate_policy = {
        "policy_name": "ManualReviewGatePolicy",
        "manual_review_required_if": [
            "privacy_unknown",
            "private_home",
            "face_possible",
            "child_or_school_possible",
            "medical_context_possible",
            "screen_or_document_possible",
            "unknown_source",
            "missing_source_chain",
            "missing_timestamp",
            "crossing_related_sample",
            "high_risk_navigation_sample",
        ],
        "outputs": [
            "ManualReviewRequiredCandidate",
            "SampleBlockedCandidate",
            "SampleAllowedForFutureDryRunCandidate",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    sample_usage_policy = {
        "policy_name": "SampleUsagePolicy",
        "allowed_uses": [
            "schema_validation",
            "manifest_dryrun",
            "future_controlled_frame_sample_dryrun",
            "quality_gate_metadata_test",
            "privacy_precheck_dryrun",
            "source_chain_trace_test",
        ],
        "forbidden_uses": [
            "model_training",
            "production_inference",
            "live_navigation",
            "crossing_decision_runtime",
            "ocr_provider_runtime",
            "tracking_runtime",
            "worldmodel_write",
            "memory_write",
            "fact_write",
            "library_commit",
            "external_export",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    sample_to_frame_candidate_mapping_policy = {
        "policy_name": "SampleToFrameCandidateMappingPolicy",
        "mapping_principles": [
            "manifest metadata can map to ControlledFrameInputCandidate stub",
            "no image/video content read",
            "no visual observation generated",
            "no scene sketch generated",
            "no visual focus result generated",
            "no OCR activation result generated",
            "no tracking request result generated",
        ],
        "content_read_required": False,
        "frame_input_candidate_stub_allowed": True,
        "timestamp_mapping_policy": "placeholder_only_or_manifest_timestamp_stub",
        "source_chain_mapping_policy": "carryover_source_chain_only",
        "privacy_tag_mapping_policy": "carryover_privacy_precheck_tags_only",
        "task_context_mapping_policy": "carryover_task_context_placeholder_only",
        "location_context_mapping_policy": "carryover_location_context_placeholder_only",
        "mapping_status_values": ["mapped_stub", "blocked", "requires_manual_review"],
        "mapping_boundaries": {
            "sample_to_visual_observation_allowed": False,
            "sample_to_scene_sketch_allowed": False,
            "sample_to_ocr_activation_result_allowed": False,
            "sample_to_tracking_result_allowed": False,
            "sample_to_navigation_action_allowed": False,
            "sample_to_crossing_runtime_allowed": False,
            "sample_to_worldmodel_write_allowed": False,
            "sample_to_memory_write_allowed": False,
            "sample_to_fact_write_allowed": False,
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    scenario_specs = [
        {
            "scenario_id": "static_image_manifest_allowed",
            "sample_type": "static_image_file_placeholder",
            "category": "allowed",
            "source_chain_present": True,
            "privacy_tags": ["public_space"],
            "manual_review_required": False,
            "allowed_for_future_dryrun_candidate": True,
            "content_read_allowed_now": False,
            "file_opened": False,
        },
        {
            "scenario_id": "prerecorded_video_manifest_allowed",
            "sample_type": "prerecorded_video_file_placeholder",
            "category": "allowed",
            "source_chain_present": True,
            "privacy_tags": ["public_space"],
            "manual_review_required": False,
            "allowed_for_future_dryrun_candidate": True,
            "content_read_allowed_now": False,
            "video_decoded": False,
        },
        {
            "scenario_id": "simulation_frame_manifest_allowed",
            "sample_type": "simulation_frame_file_placeholder",
            "category": "allowed",
            "source_chain_present": True,
            "privacy_tags": ["public_space"],
            "manual_review_required": False,
            "allowed_for_future_dryrun_candidate": True,
            "content_read_allowed_now": False,
        },
        {
            "scenario_id": "synthetic_image_manifest_allowed",
            "sample_type": "synthetic_image_placeholder",
            "category": "allowed",
            "source_chain_present": True,
            "privacy_tags": ["public_space"],
            "manual_review_required": False,
            "allowed_for_future_dryrun_candidate": True,
            "content_read_allowed_now": False,
        },
        {
            "scenario_id": "controlled_uploaded_image_restricted",
            "sample_type": "controlled_uploaded_image_placeholder",
            "category": "restricted",
            "source_chain_present": True,
            "privacy_tags": ["bystander_possible"],
            "manual_review_required": False,
            "allowed_for_future_dryrun_candidate": True,
            "content_read_allowed_now": False,
        },
        {
            "scenario_id": "private_home_sample_restricted",
            "sample_type": "home_private_space_sample_placeholder",
            "category": "restricted",
            "source_chain_present": True,
            "privacy_tags": ["private_home"],
            "manual_review_required": True,
            "allowed_for_future_dryrun_candidate": True,
            "content_read_allowed_now": False,
        },
        {
            "scenario_id": "screen_document_sample_restricted",
            "sample_type": "screen_document_sample_placeholder",
            "category": "restricted",
            "source_chain_present": True,
            "privacy_tags": ["screen_or_document_possible"],
            "manual_review_required": True,
            "allowed_for_future_dryrun_candidate": True,
            "content_read_allowed_now": False,
        },
        {
            "scenario_id": "child_or_school_sample_restricted",
            "sample_type": "child_or_school_context_sample_placeholder",
            "category": "restricted",
            "source_chain_present": True,
            "privacy_tags": ["child_or_school_possible"],
            "manual_review_required": True,
            "allowed_for_future_dryrun_candidate": True,
            "content_read_allowed_now": False,
        },
        {
            "scenario_id": "live_camera_sample_blocked",
            "sample_type": "live_camera_sample_placeholder",
            "category": "blocked",
            "source_chain_present": True,
            "privacy_tags": ["unknown_privacy"],
            "manual_review_required": False,
            "allowed_for_future_dryrun_candidate": False,
            "content_read_allowed_now": False,
        },
        {
            "scenario_id": "external_stream_sample_blocked",
            "sample_type": "external_stream_sample_placeholder",
            "category": "blocked",
            "source_chain_present": True,
            "privacy_tags": ["unknown_privacy"],
            "manual_review_required": False,
            "allowed_for_future_dryrun_candidate": False,
            "content_read_allowed_now": False,
        },
        {
            "scenario_id": "missing_source_chain_blocked",
            "sample_type": "static_image_file_placeholder",
            "category": "blocked",
            "source_chain_present": False,
            "privacy_tags": ["public_space"],
            "manual_review_required": False,
            "allowed_for_future_dryrun_candidate": False,
            "content_read_allowed_now": False,
        },
        {
            "scenario_id": "missing_privacy_precheck_blocked",
            "sample_type": "static_image_file_placeholder",
            "category": "blocked",
            "source_chain_present": True,
            "privacy_tags": [],
            "manual_review_required": False,
            "allowed_for_future_dryrun_candidate": False,
            "content_read_allowed_now": False,
        },
        {
            "scenario_id": "crossing_related_sample_requires_review",
            "sample_type": "extracted_frame_file_placeholder",
            "category": "restricted",
            "source_chain_present": True,
            "privacy_tags": ["public_space", "bystander_possible"],
            "manual_review_required": True,
            "allowed_for_future_dryrun_candidate": True,
            "content_read_allowed_now": False,
            "crossing_related_sample": True,
        },
        {
            "scenario_id": "unknown_source_sample_blocked",
            "sample_type": "unknown_source_sample",
            "category": "blocked",
            "source_chain_present": False,
            "privacy_tags": ["unknown_privacy"],
            "manual_review_required": False,
            "allowed_for_future_dryrun_candidate": False,
            "content_read_allowed_now": False,
        },
    ]

    controlled_frame_sample_planning_scenario_matrix = {
        "scenarios": [
            {
                **row,
                "allowed_for_runtime": False,
                "file_opened": False,
                "image_opened": False,
                "video_opened": False,
                "video_decoded": False,
                "frame_extracted": False,
                "visual_model_invoked": False,
                "manifest_only_processing": True,
                "sample_manifest_not_sample_processing": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for row in scenario_specs
        ],
        "scenario_count": len(scenario_specs),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    allowed_count = sum(1 for item in scenario_specs if item.get("category") == "allowed")
    restricted_count = sum(1 for item in scenario_specs if item.get("category") == "restricted")
    blocked_count = sum(1 for item in scenario_specs if item.get("category") == "blocked")
    manual_review_required_count = sum(1 for item in scenario_specs if item.get("manual_review_required") is True)

    sample_planning_boundary_matrix = {
        "planning_scope": PLANNING_SCOPE,
        "controlled_sample_dryrun_started": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "file_opened": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
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
        "manifest_only_processing": True,
        "sample_manifest_not_sample_processing": True,
        "privacy_precheck_required": True,
        "manual_review_gate_required_for_sensitive_samples": True,
        "live_camera_sample_blocked": True,
        "external_stream_sample_blocked": True,
        "missing_source_chain_blocked": True,
        "missing_privacy_precheck_blocked": True,
        "sample_to_frame_candidate_mapping_without_content_read": True,
        "sample_to_visual_observation_allowed": False,
        "sample_to_scene_sketch_allowed": False,
        "sample_to_ocr_activation_result_allowed": False,
        "sample_to_tracking_result_allowed": False,
        "sample_to_navigation_action_allowed": False,
        "sample_to_crossing_runtime_allowed": False,
        "sample_to_worldmodel_write_allowed": False,
        "sample_to_memory_write_allowed": False,
        "sample_to_fact_write_allowed": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "carryover_topics": [
            {
                "topic": "gate taxonomy / gate requirement framework deferred (P1 project optimization)",
                "impact": "must not block current sample planning; must be revisited before broadening governance gates",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "topic": "controlled sample privacy tag completeness debt",
                "impact": "privacy precheck relies on user-provided tags; uncertainty => restricted/manual review",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "topic": "sample source-chain provenance normalization debt",
                "impact": "hash/path are placeholders in planning; future needs stable source_chain format",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "topic": "sample-to-frame-candidate mapping debt",
                "impact": "mapping is stub-only now; future dryrun must keep manifest-only constraint",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ],
        "no_runtime_boundary_enforced": True,
        "no_write_boundary_enforced": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "sample manifest schema + governance boundaries defined; next step is manifest-level dryrun without image/video content read",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not all(
        [
            post_crossing_decision_roadmap_input_loaded,
            crossing_decision_closure_input_loaded,
            controlled_frame_input_closure_input_loaded,
            controlled_frame_input_post_review_input_loaded,
            controlled_frame_input_dryrun_input_loaded,
            controlled_frame_input_planning_input_loaded,
            map_location_readonly_context_input_loaded,
            safety_constitution_input_loaded,
            minimal_runtime_integration_closure_loaded,
            ocr_final_closure_loaded,
        ]
    ):
        blockers.append("required_root_missing_or_invalid")
    if len(scenario_specs) < 14:
        blockers.append("scenario_matrix_insufficient")
    if allowed_count < 4 or restricted_count < 4 or blocked_count < 4 or manual_review_required_count < 4:
        blockers.append("scenario_count_threshold_not_met")

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
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
        "controlled_frame_sample_planning_policy_defined": True,
        "controlled_frame_sample_manifest_schema_defined": True,
        "sample_source_policy_defined": True,
        "file_boundary_policy_defined": True,
        "privacy_precheck_policy_defined": True,
        "manual_review_gate_policy_defined": True,
        "sample_usage_policy_defined": True,
        "sample_to_frame_candidate_mapping_policy_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(scenario_specs),
        "allowed_sample_candidate_count": allowed_count,
        "restricted_sample_candidate_count": restricted_count,
        "blocked_sample_candidate_count": blocked_count,
        "manual_review_required_case_count": manual_review_required_count,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "file_opened": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "manifest_only_processing": True,
        "sample_manifest_not_sample_processing": True,
        "controlled_sample_dryrun_started": False,
        "live_camera_sample_blocked": True,
        "external_stream_sample_blocked": True,
        "missing_source_chain_blocked": True,
        "missing_privacy_precheck_blocked": True,
        "privacy_precheck_required": True,
        "manual_review_gate_required_for_sensitive_samples": True,
        "sample_to_frame_candidate_mapping_without_content_read": True,
        "sample_to_visual_observation_allowed": False,
        "sample_to_scene_sketch_allowed": False,
        "sample_to_ocr_activation_result_allowed": False,
        "sample_to_tracking_result_allowed": False,
        "sample_to_navigation_action_allowed": False,
        "sample_to_crossing_runtime_allowed": False,
        "sample_to_worldmodel_write_allowed": False,
        "sample_to_memory_write_allowed": False,
        "sample_to_fact_write_allowed": False,
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
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_SAMPLE_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_frame_sample_planning_policy": controlled_frame_sample_planning_policy,
        "controlled_frame_sample_manifest_schema": controlled_frame_sample_manifest_schema,
        "sample_source_policy": sample_source_policy,
        "file_boundary_policy": file_boundary_policy,
        "privacy_precheck_policy": privacy_precheck_policy,
        "manual_review_gate_policy": manual_review_gate_policy,
        "sample_usage_policy": sample_usage_policy,
        "sample_to_frame_candidate_mapping_policy": sample_to_frame_candidate_mapping_policy,
        "controlled_frame_sample_planning_scenario_matrix": controlled_frame_sample_planning_scenario_matrix,
        "sample_planning_boundary_matrix": sample_planning_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _no_runtime_payload(),
        "no_write_boundary_report": _no_runtime_payload(),
    }

