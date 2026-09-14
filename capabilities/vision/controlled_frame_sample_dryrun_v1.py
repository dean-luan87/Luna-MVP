# -*- coding: utf-8 -*-
"""Controlled Frame Sample DryRun v1 (manifest-metadata-only).

This phase performs a strict manifest-level dry-run:
- ONLY constructs/loads sample manifest metadata stubs
- DOES NOT open/read any image/video files
- DOES NOT decode video / extract frames
- DOES NOT invoke vision/OCR/map/tracking runtime
- Produces decision candidates and mapping stubs (no content read)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Controlled-Frame-Sample-DryRun-v1-001"
DRYRUN_ID = "cfsdr_v1_001"
DRYRUN_SCOPE = "controlled_frame_sample_dryrun_only"
SOURCE_CHAIN = "controlled_frame_sample_dryrun_v1"
FINAL_DECISION = "CONTROLLED_FRAME_SAMPLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001"

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

PRIVACY_SENSITIVE_TAGS = {
    "private_home",
    "face_possible",
    "child_or_school_possible",
    "medical_context_possible",
    "screen_or_document_possible",
    "commercial_sensitive_possible",
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


def _field(name: str, field_type: str, required: bool, **extras: Any) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"name": name, "type": field_type, "required": required}
    payload.update(extras)
    return payload


def _boundary_payload() -> Dict[str, Any]:
    return {
        "dryrun_scope": DRYRUN_SCOPE,
        "manifest_metadata_only": True,
        "sample_manifest_loaded": True,
        "manifest_only_processing": True,
        "sample_manifest_not_sample_processing": True,
        "controlled_sample_runtime_started": False,
        "real_file_hash_computed": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "file_opened": False,
        "image_opened": False,
        "video_opened": False,
        "video_decoded": False,
        "frame_extracted": False,
        "visual_observation_generated": False,
        "scene_sketch_generated": False,
        "ocr_activation_result_generated": False,
        "tracking_result_generated": False,
        "navigation_action_triggered": False,
        "crossing_runtime_invoked": False,
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
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "task_state_committed_now": False,
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


def _privacy_risk_level(tags: List[str]) -> str:
    if not tags:
        return "missing_tags"
    if "unknown_privacy" in tags:
        return "unknown"
    if any(tag in PRIVACY_SENSITIVE_TAGS for tag in tags):
        return "sensitive"
    return "low"


def _manual_review_required(tags: List[str], *, source_unknown: bool, missing_source_chain: bool, missing_timestamp: bool, crossing_related: bool) -> Tuple[bool, str]:
    if missing_source_chain:
        return True, "missing_source_chain"
    if source_unknown:
        return True, "unknown_source"
    if missing_timestamp:
        return True, "missing_timestamp"
    if crossing_related:
        return True, "crossing_related_sample"
    if not tags or "unknown_privacy" in tags:
        return True, "privacy_unknown"
    if "private_home" in tags:
        return True, "private_home"
    if any(tag in PRIVACY_SENSITIVE_TAGS for tag in tags):
        return True, "privacy_sensitive_tag"
    return False, ""


def _source_status(sample_type: str, *, source_chain_present: bool, privacy_tags_present: bool) -> Tuple[str, str]:
    blocked_reason = ""
    if not source_chain_present:
        return "blocked_missing_source_chain", "missing_source_chain"
    if not privacy_tags_present:
        return "blocked_missing_privacy_precheck", "missing_privacy_precheck"
    if sample_type in {"unknown_source_sample"}:
        return "blocked_unknown_source", "unknown_source"
    if sample_type in {"live_camera_sample_placeholder", "device_camera_sample_placeholder"}:
        return "blocked_live_camera_sample", "live_camera_sample_blocked"
    if sample_type in {"external_stream_sample_placeholder"}:
        return "blocked_external_stream_sample", "external_stream_sample_blocked"
    if sample_type in {
        "static_image_file_placeholder",
        "prerecorded_video_file_placeholder",
        "extracted_frame_file_placeholder",
        "simulation_frame_file_placeholder",
        "synthetic_image_placeholder",
    }:
        return "allowed_candidate", blocked_reason
    if sample_type in {"controlled_uploaded_image_placeholder", "controlled_uploaded_video_placeholder"}:
        return "restricted_candidate", blocked_reason
    if sample_type in {
        "home_private_space_sample_placeholder",
        "medical_context_sample_placeholder",
        "child_or_school_context_sample_placeholder",
        "screen_document_sample_placeholder",
    }:
        return "restricted_candidate", blocked_reason
    # Default conservative
    return "blocked_unknown_source", "unknown_source"


def run_controlled_frame_sample_dryrun_v1(
    *,
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

    # Schemas (dryrun contracts)
    dryrun_case_schema = {
        "schema_name": "ControlledFrameSampleDryRunCase",
        "schema_version": "v1",
        "field_specs": [
            _field("dryrun_case_id", "string", True),
            _field("sample_manifest_stub", "object", True),
            _field("expected_source_decision", "string", True),
            _field("expected_file_boundary_decision", "string", True),
            _field("expected_privacy_precheck_decision", "string", True),
            _field("expected_manual_review_decision", "string", True),
            _field("expected_usage_decision", "string", True),
            _field("expected_mapping_decision", "string", True),
            _field("expected_boundary_flags", "object", True),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    sample_manifest_metadata_stub_schema = {
        "schema_name": "SampleManifestMetadataStub",
        "schema_version": "v1",
        "field_specs": [
            _field("sample_id", "string", True),
            _field("sample_type", "string", True),
            _field("sample_origin", "string", True),
            _field("file_path_placeholder", "string", True),
            _field("file_hash_placeholder", "string", True),
            _field("source_chain", "string", True),
            _field("capture_context_placeholder", "string", False),
            _field("timestamp_placeholder", "string", False),
            _field("location_context_placeholder", "string", False),
            _field("task_context_placeholder", "string", False),
            _field("privacy_precheck_tags", "list", True),
            _field("expected_usage_scope", "string", True),
            _field("manual_review_required_expected", "boolean", True),
            _field("content_read_allowed_now", "boolean", True, default=False),
            _field("file_open_allowed_now", "boolean", True, default=False),
            _field("fact_status", "string", True, default="not_fact"),
        ],
        "invariants": {"content_read_allowed_now": False, "file_open_allowed_now": False},
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    sample_source_decision_candidate_schema = {
        "schema_name": "SampleSourceDecisionCandidate",
        "schema_version": "v1",
        "source_status_values": [
            "allowed_candidate",
            "restricted_candidate",
            "blocked_missing_source_chain",
            "blocked_missing_privacy_precheck",
            "blocked_unknown_source",
            "blocked_live_camera_sample",
            "blocked_external_stream_sample",
        ],
        "field_specs": [
            _field("source_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("sample_id", "string", True),
            _field("sample_type", "string", True),
            _field("source_status", "string", True),
            _field("allowed_for_future_dryrun_candidate", "boolean", True),
            _field("restricted_use_required", "boolean", True),
            _field("blocked_reason", "string", False),
            _field("source_chain_valid", "boolean", True),
            _field("privacy_precheck_required", "boolean", True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_boundary_decision_candidate_schema = {
        "schema_name": "FileBoundaryDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("file_boundary_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("sample_id", "string", True),
            _field("file_content_read", "boolean", True, default=False),
            _field("image_content_read", "boolean", True, default=False),
            _field("video_content_read", "boolean", True, default=False),
            _field("file_opened", "boolean", True, default=False),
            _field("image_opened", "boolean", True, default=False),
            _field("video_opened", "boolean", True, default=False),
            _field("video_decoded", "boolean", True, default=False),
            _field("frame_extracted", "boolean", True, default=False),
            _field("manifest_only_processing", "boolean", True, default=True),
            _field("violation_count", "integer", True, default=0),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    privacy_precheck_decision_candidate_schema = {
        "schema_name": "PrivacyPrecheckDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("privacy_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("sample_id", "string", True),
            _field("privacy_tags_present", "boolean", True),
            _field("privacy_risk_level", "string", True),
            _field("restricted_use_required", "boolean", True),
            _field("manual_review_required", "boolean", True),
            _field("downstream_allowed_candidate", "boolean", True),
            _field("long_term_use_allowed", "boolean", True, default=False),
            _field("no_identity_inference", "boolean", True, default=True),
            _field("no_emotion_inference", "boolean", True, default=True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    manual_review_decision_candidate_schema = {
        "schema_name": "ManualReviewDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("manual_review_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("sample_id", "string", True),
            _field("manual_review_required", "boolean", True),
            _field("review_reason", "string", False),
            _field("allowed_for_future_dryrun_after_review_candidate", "boolean", True),
            _field("blocked_until_review", "boolean", True),
            _field("no_runtime_allowed", "boolean", True, default=True),
            _field("fact_status", "string", True, default="not_fact"),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    sample_usage_decision_candidate_schema = {
        "schema_name": "SampleUsageDecisionCandidate",
        "schema_version": "v1",
        "field_specs": [
            _field("usage_decision_id", "string", True),
            _field("source_case_id", "string", True),
            _field("sample_id", "string", True),
            _field("allowed_usage_modes", "list", True),
            _field("forbidden_usage_modes", "list", True),
            _field("production_inference_allowed", "boolean", True, default=False),
            _field("model_training_allowed", "boolean", True, default=False),
            _field("live_navigation_allowed", "boolean", True, default=False),
            _field("crossing_runtime_allowed", "boolean", True, default=False),
            _field("ocr_provider_runtime_allowed", "boolean", True, default=False),
            _field("tracking_runtime_allowed", "boolean", True, default=False),
            _field("worldmodel_write_allowed", "boolean", True, default=False),
            _field("memory_write_allowed", "boolean", True, default=False),
            _field("fact_write_allowed", "boolean", True, default=False),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    sample_to_frame_candidate_mapping_stub_schema = {
        "schema_name": "SampleToFrameCandidateMappingStub",
        "schema_version": "v1",
        "field_specs": [
            _field("mapping_stub_id", "string", True),
            _field("source_case_id", "string", True),
            _field("sample_id", "string", True),
            _field("future_frame_source_candidate_type", "string", True),
            _field("controlled_frame_input_candidate_stub_allowed", "boolean", True),
            _field("timestamp_mapping_policy", "string", True),
            _field("source_chain_mapping_policy", "string", True),
            _field("privacy_tag_mapping_policy", "string", True),
            _field("task_context_mapping_policy", "string", True),
            _field("location_context_mapping_policy", "string", True),
            _field("content_read_required", "boolean", True, default=False),
            _field("visual_observation_generated", "boolean", True, default=False),
            _field("scene_sketch_generated", "boolean", True, default=False),
            _field("ocr_activation_result_generated", "boolean", True, default=False),
            _field("tracking_result_generated", "boolean", True, default=False),
            _field("mapping_status", "string", True),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_sample_dryrun_result_schema = {
        "schema_name": "ControlledFrameSampleDryRunResult",
        "schema_version": "v1",
        "field_specs": [
            _field("result_id", "string", True),
            _field("source_case_id", "string", True),
            _field("sample_id", "string", True),
            _field("source_decision_ref", "string", True),
            _field("file_boundary_decision_ref", "string", True),
            _field("privacy_decision_ref", "string", True),
            _field("manual_review_decision_ref", "string", True),
            _field("usage_decision_ref", "string", True),
            _field("mapping_stub_ref", "string", True),
            _field("dryrun_status", "string", True),
            _field("violations", "list", True),
            _field("source_chain", "string", True, default=SOURCE_CHAIN),
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Scenario matrix: 16 cases (must include the 16 enumerated)
    scenarios = [
        {
            "scenario_id": "static_image_manifest_allowed",
            "sample_type": "static_image_file_placeholder",
            "privacy_tags": ["public_space"],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "prerecorded_video_manifest_allowed",
            "sample_type": "prerecorded_video_file_placeholder",
            "privacy_tags": ["public_space"],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "simulation_frame_manifest_allowed",
            "sample_type": "simulation_frame_file_placeholder",
            "privacy_tags": ["public_space"],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "synthetic_image_manifest_allowed",
            "sample_type": "synthetic_image_placeholder",
            "privacy_tags": ["public_space"],
            "source_chain_present": True,
            "timestamp_present": False,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "controlled_uploaded_image_restricted",
            "sample_type": "controlled_uploaded_image_placeholder",
            "privacy_tags": ["bystander_possible"],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "private_home_sample_restricted",
            "sample_type": "home_private_space_sample_placeholder",
            "privacy_tags": ["private_home"],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "screen_document_sample_restricted",
            "sample_type": "screen_document_sample_placeholder",
            "privacy_tags": ["screen_or_document_possible"],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "child_or_school_sample_restricted",
            "sample_type": "child_or_school_context_sample_placeholder",
            "privacy_tags": ["child_or_school_possible"],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "live_camera_sample_blocked",
            "sample_type": "live_camera_sample_placeholder",
            "privacy_tags": ["unknown_privacy"],
            "source_chain_present": True,
            "timestamp_present": False,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "external_stream_sample_blocked",
            "sample_type": "external_stream_sample_placeholder",
            "privacy_tags": ["unknown_privacy"],
            "source_chain_present": True,
            "timestamp_present": False,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "missing_source_chain_blocked",
            "sample_type": "static_image_file_placeholder",
            "privacy_tags": ["public_space"],
            "source_chain_present": False,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "missing_privacy_precheck_blocked",
            "sample_type": "static_image_file_placeholder",
            "privacy_tags": [],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "crossing_related_sample_requires_review",
            "sample_type": "extracted_frame_file_placeholder",
            "privacy_tags": ["public_space", "bystander_possible"],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": True,
        },
        {
            "scenario_id": "unknown_source_sample_blocked",
            "sample_type": "unknown_source_sample",
            "privacy_tags": ["unknown_privacy"],
            "source_chain_present": False,
            "timestamp_present": False,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "medical_context_sample_restricted",
            "sample_type": "medical_context_sample_placeholder",
            "privacy_tags": ["medical_context_possible"],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
        {
            "scenario_id": "workplace_sensitive_sample_restricted",
            "sample_type": "screen_document_sample_placeholder",
            "privacy_tags": ["commercial_sensitive_possible", "workplace_possible"],
            "source_chain_present": True,
            "timestamp_present": True,
            "crossing_related_sample": False,
        },
    ]

    controlled_frame_sample_dryrun_scenario_matrix = {
        "scenarios": [
            {
                **row,
                "manifest_metadata_only": True,
                "file_opened": False,
                "image_opened": False,
                "video_opened": False,
                "video_decoded": False,
                "frame_extracted": False,
                "real_file_hash_computed": False,
                "visual_observation_generated": False,
                "scene_sketch_generated": False,
                "ocr_activation_result_generated": False,
                "tracking_result_generated": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for row in scenarios
        ],
        "scenario_count": len(scenarios),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # Decision execution per scenario (metadata-only)
    allowed_count = 0
    restricted_count = 0
    blocked_count = 0
    manual_review_required_count = 0

    dryrun_results: List[Dict[str, Any]] = []
    source_results: List[Dict[str, Any]] = []
    boundary_results: List[Dict[str, Any]] = []
    privacy_results: List[Dict[str, Any]] = []
    manual_review_results: List[Dict[str, Any]] = []
    usage_results: List[Dict[str, Any]] = []
    mapping_results: List[Dict[str, Any]] = []

    allowed_usage_modes = [
        "schema_validation",
        "manifest_dryrun",
        "future_controlled_frame_sample_dryrun",
        "quality_gate_metadata_test",
        "privacy_precheck_dryrun",
        "source_chain_trace_test",
    ]
    forbidden_usage_modes = [
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
    ]

    for i, row in enumerate(scenarios, start=1):
        case_id = f"c{i:02d}"
        sample_id = f"sample_{row['scenario_id']}"
        sample_type = row["sample_type"]
        tags = list(row.get("privacy_tags", []))
        source_chain_present = bool(row.get("source_chain_present"))
        timestamp_present = bool(row.get("timestamp_present"))
        crossing_related = bool(row.get("crossing_related_sample"))

        manifest_stub = {
            "sample_id": sample_id,
            "sample_type": sample_type,
            "sample_origin": "dryrun_manifest_stub",
            "file_path_placeholder": f"(placeholder)/{sample_id}",
            "file_hash_placeholder": "(placeholder_hash)",
            "source_chain": SOURCE_CHAIN if source_chain_present else "",
            "capture_context_placeholder": "(stub)",
            "timestamp_placeholder": "T+stub" if timestamp_present else "",
            "location_context_placeholder": "(stub)",
            "task_context_placeholder": "(stub)",
            "privacy_precheck_tags": tags,
            "expected_usage_scope": "manifest_dryrun_only",
            "manual_review_required_expected": False,  # computed below
            "content_read_allowed_now": False,
            "file_open_allowed_now": False,
            "fact_status": "not_fact",
        }

        privacy_tags_present = bool(tags)
        status, blocked_reason = _source_status(sample_type, source_chain_present=source_chain_present, privacy_tags_present=privacy_tags_present)
        source_unknown = sample_type == "unknown_source_sample"
        missing_source_chain = not source_chain_present
        missing_timestamp = not timestamp_present

        manual_review_required, review_reason = _manual_review_required(
            tags,
            source_unknown=source_unknown,
            missing_source_chain=missing_source_chain,
            missing_timestamp=missing_timestamp,
            crossing_related=crossing_related,
        )
        manifest_stub["manual_review_required_expected"] = manual_review_required

        # Counters
        if status == "allowed_candidate":
            allowed_count += 1
        elif status == "restricted_candidate":
            restricted_count += 1
        else:
            blocked_count += 1
        if manual_review_required:
            manual_review_required_count += 1

        # Candidate ids
        source_decision_id = f"sd_{case_id}"
        file_boundary_decision_id = f"fb_{case_id}"
        privacy_decision_id = f"pd_{case_id}"
        manual_review_decision_id = f"mr_{case_id}"
        usage_decision_id = f"ud_{case_id}"
        mapping_stub_id = f"ms_{case_id}"
        result_id = f"r_{case_id}"

        source_chain_valid = bool(source_chain_present)
        source_candidate = {
            "source_decision_id": source_decision_id,
            "source_case_id": case_id,
            "sample_id": sample_id,
            "sample_type": sample_type,
            "source_status": status,
            "allowed_for_future_dryrun_candidate": status in {"allowed_candidate", "restricted_candidate"},
            "restricted_use_required": status == "restricted_candidate",
            "blocked_reason": blocked_reason,
            "source_chain_valid": source_chain_valid,
            "privacy_precheck_required": True,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        source_results.append(source_candidate)

        boundary_candidate = {
            "file_boundary_decision_id": file_boundary_decision_id,
            "source_case_id": case_id,
            "sample_id": sample_id,
            "file_content_read": False,
            "image_content_read": False,
            "video_content_read": False,
            "file_opened": False,
            "image_opened": False,
            "video_opened": False,
            "video_decoded": False,
            "frame_extracted": False,
            "manifest_only_processing": True,
            "violation_count": 0,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        boundary_results.append(boundary_candidate)

        risk_level = _privacy_risk_level(tags)
        restricted_use_required = status == "restricted_candidate" or risk_level in {"sensitive", "unknown"}
        downstream_allowed = status in {"allowed_candidate", "restricted_candidate"} and privacy_tags_present
        privacy_candidate = {
            "privacy_decision_id": privacy_decision_id,
            "source_case_id": case_id,
            "sample_id": sample_id,
            "privacy_tags_present": privacy_tags_present,
            "privacy_risk_level": risk_level,
            "restricted_use_required": restricted_use_required,
            "manual_review_required": manual_review_required,
            "downstream_allowed_candidate": downstream_allowed,
            "long_term_use_allowed": False,
            "no_identity_inference": True,
            "no_emotion_inference": True,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        privacy_results.append(privacy_candidate)

        blocked_until_review = manual_review_required
        manual_review_candidate = {
            "manual_review_decision_id": manual_review_decision_id,
            "source_case_id": case_id,
            "sample_id": sample_id,
            "manual_review_required": manual_review_required,
            "review_reason": review_reason,
            "allowed_for_future_dryrun_after_review_candidate": manual_review_required,
            "blocked_until_review": blocked_until_review,
            "no_runtime_allowed": True,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        manual_review_results.append(manual_review_candidate)

        usage_candidate = {
            "usage_decision_id": usage_decision_id,
            "source_case_id": case_id,
            "sample_id": sample_id,
            "allowed_usage_modes": allowed_usage_modes,
            "forbidden_usage_modes": forbidden_usage_modes,
            "production_inference_allowed": False,
            "model_training_allowed": False,
            "live_navigation_allowed": False,
            "crossing_runtime_allowed": False,
            "ocr_provider_runtime_allowed": False,
            "tracking_runtime_allowed": False,
            "worldmodel_write_allowed": False,
            "memory_write_allowed": False,
            "fact_write_allowed": False,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        usage_results.append(usage_candidate)

        if status.startswith("blocked_"):
            mapping_status = "blocked"
        elif manual_review_required:
            mapping_status = "requires_manual_review"
        else:
            mapping_status = "mapped_stub"
        mapping_candidate = {
            "mapping_stub_id": mapping_stub_id,
            "source_case_id": case_id,
            "sample_id": sample_id,
            "future_frame_source_candidate_type": f"from_sample::{sample_type}",
            "controlled_frame_input_candidate_stub_allowed": True,
            "timestamp_mapping_policy": "placeholder_only_or_manifest_timestamp_stub",
            "source_chain_mapping_policy": "carryover_source_chain_only",
            "privacy_tag_mapping_policy": "carryover_privacy_precheck_tags_only",
            "task_context_mapping_policy": "carryover_task_context_placeholder_only",
            "location_context_mapping_policy": "carryover_location_context_placeholder_only",
            "content_read_required": False,
            "visual_observation_generated": False,
            "scene_sketch_generated": False,
            "ocr_activation_result_generated": False,
            "tracking_result_generated": False,
            "mapping_status": mapping_status,
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        mapping_results.append(mapping_candidate)

        violations: List[str] = []
        dryrun_status = "blocked" if status.startswith("blocked_") else ("requires_manual_review" if manual_review_required else "allowed")

        dryrun_results.append(
            {
                "result_id": result_id,
                "source_case_id": case_id,
                "sample_id": sample_id,
                "source_decision_ref": source_decision_id,
                "file_boundary_decision_ref": file_boundary_decision_id,
                "privacy_decision_ref": privacy_decision_id,
                "manual_review_decision_ref": manual_review_decision_id,
                "usage_decision_ref": usage_decision_id,
                "mapping_stub_ref": mapping_stub_id,
                "dryrun_status": dryrun_status,
                "violations": violations,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    controlled_frame_sample_dryrun_results = {
        "results": dryrun_results,
        "result_count": len(dryrun_results),
        "allowed_result_count": sum(1 for r in dryrun_results if r.get("dryrun_status") == "allowed"),
        "blocked_result_count": sum(1 for r in dryrun_results if r.get("dryrun_status") == "blocked"),
        "manual_review_result_count": sum(1 for r in dryrun_results if r.get("dryrun_status") == "requires_manual_review"),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    sample_file_boundary_check_results = {"rows": boundary_results, "row_count": len(boundary_results), "source_chain": SOURCE_CHAIN, **_not_fact()}
    sample_privacy_precheck_results = {"rows": privacy_results, "row_count": len(privacy_results), "source_chain": SOURCE_CHAIN, **_not_fact()}
    manual_review_gate_results = {"rows": manual_review_results, "row_count": len(manual_review_results), "source_chain": SOURCE_CHAIN, **_not_fact()}
    sample_to_frame_mapping_stub_results = {"rows": mapping_results, "row_count": len(mapping_results), "source_chain": SOURCE_CHAIN, **_not_fact()}

    sample_dryrun_boundary_matrix = {
        "dryrun_scope": DRYRUN_SCOPE,
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
        "live_camera_sample_blocked": True,
        "external_stream_sample_blocked": True,
        "missing_source_chain_blocked": True,
        "missing_privacy_precheck_blocked": True,
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

    governance_debt_register = {
        "carryover_topics": [
            {
                "topic": "manual review scaling debt for sensitive samples",
                "impact": "requires stable review workflow before widening sample intake",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "topic": "source_chain normalization debt for cross-device / cross-origin samples",
                "impact": "must be stable before any future real file boundary relaxation",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "topic": "mapping stub to ControlledFrameInputCandidate alignment debt",
                "impact": "future Controlled Frame Sample Post-Review must verify stub alignment without content read",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "manifest-level dryrun produced source/privacy/manual-review/usage/mapping stub decisions without content read; next is post-dryrun review",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not all(
        [
            controlled_frame_sample_planning_input_loaded,
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
    if len(scenarios) < 16:
        blockers.append("scenario_matrix_insufficient")
    if allowed_count < 4 or restricted_count < 5 or blocked_count < 4 or manual_review_required_count < 5:
        blockers.append("scenario_count_threshold_not_met")

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
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
        "dryrun_case_schema_defined": True,
        "sample_manifest_metadata_stub_schema_defined": True,
        "sample_source_decision_candidate_schema_defined": True,
        "file_boundary_decision_candidate_schema_defined": True,
        "privacy_precheck_decision_candidate_schema_defined": True,
        "manual_review_decision_candidate_schema_defined": True,
        "sample_usage_decision_candidate_schema_defined": True,
        "sample_to_frame_candidate_mapping_stub_schema_defined": True,
        "controlled_frame_sample_dryrun_result_schema_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(scenarios),
        "dryrun_results_generated": True,
        "allowed_sample_candidate_count": allowed_count,
        "restricted_sample_candidate_count": restricted_count,
        "blocked_sample_candidate_count": blocked_count,
        "manual_review_required_case_count": manual_review_required_count,
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
        "live_camera_sample_blocked": True,
        "external_stream_sample_blocked": True,
        "missing_source_chain_blocked": True,
        "missing_privacy_precheck_blocked": True,
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
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_SAMPLE_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "dryrun_case_schema": dryrun_case_schema,
        "sample_manifest_metadata_stub_schema": sample_manifest_metadata_stub_schema,
        "sample_source_decision_candidate_schema": sample_source_decision_candidate_schema,
        "file_boundary_decision_candidate_schema": file_boundary_decision_candidate_schema,
        "privacy_precheck_decision_candidate_schema": privacy_precheck_decision_candidate_schema,
        "manual_review_decision_candidate_schema": manual_review_decision_candidate_schema,
        "sample_usage_decision_candidate_schema": sample_usage_decision_candidate_schema,
        "sample_to_frame_candidate_mapping_stub_schema": sample_to_frame_candidate_mapping_stub_schema,
        "controlled_frame_sample_dryrun_result_schema": controlled_frame_sample_dryrun_result_schema,
        "controlled_frame_sample_dryrun_scenario_matrix": controlled_frame_sample_dryrun_scenario_matrix,
        "controlled_frame_sample_dryrun_results": controlled_frame_sample_dryrun_results,
        "sample_file_boundary_check_results": sample_file_boundary_check_results,
        "sample_privacy_precheck_results": sample_privacy_precheck_results,
        "manual_review_gate_results": manual_review_gate_results,
        "sample_to_frame_mapping_stub_results": sample_to_frame_mapping_stub_results,
        "sample_dryrun_boundary_matrix": sample_dryrun_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }

