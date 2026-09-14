# -*- coding: utf-8 -*-
"""Controlled Frame File Stat Guarded Planning v1 (planning-only).

This phase defines how a future *guarded file stat* might be allowed under
strict governance, WITHOUT invoking any real stat/exists/open/read/hash/runtime.

Hard boundary (this phase):
- MUST NOT call os.stat / pathlib.Path.stat / lstat
- MUST NOT call os.path.exists / pathlib.Path.exists
- MUST NOT open/read files, images, videos, bytes
- MUST NOT compute hashes / parse EXIF / probe video / decode / extract frames
- MUST NOT enter runtime, MUST NOT write WorldModel/Memory/Fact/Library

The module only loads prior phase evaluation artifacts (JSON) for linkage.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Controlled-Frame-File-Stat-Guarded-Planning-v1-001"
PLANNING_ID = "cffsgp_v1_001"
PLANNING_SCOPE = "controlled_frame_file_stat_guarded_planning_only"
SOURCE_CHAIN = "controlled_frame_file_stat_guarded_planning_v1"

FINAL_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001"

# Upstream decision constants (verified via prior summaries).
POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION = (
    "POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION_READY_FOR_FILE_STAT_GUARDED_PLANNING"
)
FILE_EXISTENCE_CHECK_GUARDED_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
FILE_EXISTENCE_CHECK_GUARDED_POST_REVIEW_DECISION = (
    "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
)
FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FILE_EXISTENCE_CHECK_GUARDED_PLANNING_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_READY_FOR_DRYRUN"

POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION = "POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION_READY_FOR_FILE_EXISTENCE_CHECK_GUARDED_PLANNING"
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
    # Avoid explicit exists/stat calls; attempt read directly.
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


def _boundary_payload() -> Dict[str, Any]:
    return {
        "planning_scope": PLANNING_SCOPE,
        "planning_only": True,
        # Current-phase allow-list (must remain false)
        "stat_allowed_now": False,
        "os_stat_allowed_now": False,
        "pathlib_stat_allowed_now": False,
        "lstat_allowed_now": False,
        "exists_allowed_now": False,
        "open_allowed_now": False,
        "content_read_allowed_now": False,
        "hash_allowed_now": False,
        # Current-phase invocation (must remain false)
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
        "entity_resolution_runtime_invoked": False,
        "fact_admission_runtime_invoked": False,
        "memory_consolidation_invoked": False,
        "library_experience_commit_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _candidate_counts_from_allowed_scope(allowed_scope_policy: Dict[str, Any]) -> Tuple[int, int, int]:
    allowed_entries = allowed_scope_policy.get("allowed_for_future_stat_candidate", [])
    future_allowed = sum(1 for e in allowed_entries if e.get("allowed_for_future_stat_candidate") is True)
    blocked = 0
    restricted = 0
    return future_allowed, blocked, restricted


def run_controlled_frame_file_stat_guarded_planning_v1(
    *,
    post_file_existence_check_roadmap_decision_root: str,
    file_existence_check_guarded_closure_root: str,
    file_existence_check_guarded_post_review_root: str,
    file_existence_check_guarded_dryrun_root: str,
    file_existence_check_guarded_planning_root: str,
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

    post_file_existence_check_roadmap_input_loaded = (
        roots["post_file_existence_check_roadmap_decision"]["loaded"]
        and summaries["post_file_existence_check_roadmap_decision"].get("final_decision") == POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION
        and summaries["post_file_existence_check_roadmap_decision"].get("recommended_next_phase") == PHASE_ID
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
    post_file_metadata_boundary_roadmap_input_loaded = (
        roots["post_file_metadata_boundary_roadmap_decision"]["loaded"]
        and summaries["post_file_metadata_boundary_roadmap_decision"].get("final_decision") == POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION
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

    # ---- Core policies (planning-only) ----
    file_stat_gate_policy = {
        "gate_id": "file_stat_gate_v1",
        "gate_scope": "ControlledFrameFileStat",
        "gate_type": "CapabilityRuntimePreGate",
        "current_phase_gate_open": False,
        "future_gate_candidate": True,
        "required_inputs": [
            "file_ref_placeholder",
            "path_classification_ref",
            "fixture_registry_ref_or_equivalent",
            "source_chain",
        ],
        "required_authorization": True,
        "required_path_classification": True,
        "required_privacy_precheck": True,
        "required_manual_review_if_sensitive": True,
        "required_audit_trace": True,
        "required_source_chain": True,
        "output_candidate_type": "FileStatDecisionCandidate",
        "veto_conditions": [
            "path_blocked",
            "path_traversal_detected",
            "unknown_path",
            "missing_source_chain",
            "missing_privacy_tags",
            "missing_fixture_registry_ref",
            "authorization_missing",
            "gate_closed",
            "metadata_boundary_missing",
        ],
        "risk_notes": [
            "stat is higher-risk than existence check; it can expose size/time/permissions/inode metadata",
            "stat gate must be separate; existence-check gate pass is insufficient",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    allowed_stat_path_scope_policy = {
        "path_scope_id": "allowed_stat_path_scope_policy_v1",
        "policy_scope": "allowed_path_scope_for_future_guarded_stat",
        "planning_only": True,
        "allowed_now": False,
        "allowed_for_future_stat_candidate": [
            {
                "path_type": "repo_fixture_path_candidate",
                "allowed_for_future_stat_candidate": True,
                "allowed_now": False,
                "required_registry_ref": True,
                "required_source_chain": True,
                "required_privacy_tags": True,
                "required_review_status": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "path_type": "eval_out_fixture_path_candidate",
                "allowed_for_future_stat_candidate": True,
                "allowed_now": False,
                "required_registry_ref": True,
                "required_source_chain": True,
                "required_privacy_tags": True,
                "required_review_status": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "path_type": "explicitly_registered_fixture_path_candidate",
                "allowed_for_future_stat_candidate": True,
                "allowed_now": False,
                "required_registry_ref": True,
                "required_source_chain": True,
                "required_privacy_tags": True,
                "required_review_status": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "path_type": "controlled_test_asset_path_candidate",
                "allowed_for_future_stat_candidate": True,
                "allowed_now": False,
                "required_registry_ref": True,
                "required_source_chain": True,
                "required_privacy_tags": True,
                "required_review_status": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blocked_stat_path_scope_policy = {
        "path_scope_id": "blocked_stat_path_scope_policy_v1",
        "policy_scope": "blocked_path_scope_for_guarded_stat",
        "planning_only": True,
        "blocked_now": True,
        "blocked_path_types": [
            {
                "path_type": "external_absolute_path_blocked",
                "blocked_now": True,
                "future_allowed_candidate": False,
                "block_reason": "external absolute paths are untrusted; stat may leak system metadata",
                "manual_review_possible": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "path_type": "path_traversal_blocked",
                "blocked_now": True,
                "future_allowed_candidate": False,
                "block_reason": "path traversal must be blocked",
                "manual_review_possible": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "path_type": "unknown_path_blocked",
                "blocked_now": True,
                "future_allowed_candidate": False,
                "block_reason": "unknown path classification is blocked",
                "manual_review_possible": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "path_type": "system_sensitive_path_blocked",
                "blocked_now": True,
                "future_allowed_candidate": False,
                "block_reason": "system sensitive directories must never be stat'ed",
                "manual_review_possible": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "path_type": "home_directory_arbitrary_path_blocked",
                "blocked_now": True,
                "future_allowed_candidate": False,
                "block_reason": "arbitrary home directory paths are not allowed",
                "manual_review_possible": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "path_type": "network_mount_path_blocked",
                "blocked_now": True,
                "future_allowed_candidate": False,
                "block_reason": "network mounts are out-of-scope and high risk",
                "manual_review_possible": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "path_type": "live_device_stream_path_blocked",
                "blocked_now": True,
                "future_allowed_candidate": False,
                "block_reason": "live device streams are runtime; out of scope",
                "manual_review_possible": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ],
        "restricted_path_types": [
            {
                "path_type": "symlink_unresolved_blocked_or_restricted",
                "blocked_now": False,
                "future_allowed_candidate": "restricted",
                "block_reason": "symlink handling must be explicit; unresolved symlink is restricted",
                "manual_review_possible": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "path_type": "user_uploaded_path_restricted_not_allowed_by_default",
                "blocked_now": False,
                "future_allowed_candidate": "restricted",
                "block_reason": "user upload path is restricted; insufficient by default for stat",
                "manual_review_possible": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_metadata_exposure_boundary_policy = {
        "metadata_boundary_id": "file_stat_metadata_exposure_boundary_policy_v1",
        "policy_scope": "file_stat_metadata_exposure_boundary",
        "output_candidate_only": True,
        "manual_review_required_if_sensitive": True,
        "privacy_risk_level": "high",
        "allowed_stat_metadata_candidate": [
            {"name": "size_bytes_candidate", "allowed": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "modified_time_candidate", "allowed": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "created_time_candidate_if_available", "allowed": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "file_type_candidate", "allowed": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "is_regular_file_candidate", "allowed": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
        ],
        "restricted_stat_metadata_candidate": [
            {"name": "permissions_mode_candidate", "restricted": True, "reason": "permissions may leak user/system info", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "owner_group_candidate", "restricted": True, "reason": "owner identity is sensitive", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "inode_candidate", "restricted": True, "reason": "inode is filesystem-specific fingerprint", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "device_id_candidate", "restricted": True, "reason": "device id is system fingerprint", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "symlink_target_candidate", "restricted": True, "reason": "symlink targets may escape scopes", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "access_time_candidate", "restricted": True, "reason": "access time is privacy-sensitive", "source_chain": SOURCE_CHAIN, **_not_fact()},
        ],
        "blocked_stat_metadata_candidate": [
            {"name": "raw_permission_detail_for_user_home", "blocked": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "symlink_target_resolution", "blocked": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "full_owner_identity", "blocked": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "extended_attributes", "blocked": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "filesystem_specific_metadata", "blocked": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"name": "any_content_derived_metadata", "blocked": True, "source_chain": SOURCE_CHAIN, **_not_fact()},
        ],
        "fact_status": "not_fact",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_authorization_policy = {
        "authorization_required": True,
        "accepted_authorization_sources": [
            "fixture_registry_entry_signed",
            "explicit_operator_approval_ticket",
            "evaluation_runner_declared_fixture_allowlist",
        ],
        "rejected_authorization_sources": [
            "path_string_only",
            "user_upload_path_only",
            "system_generated_path_only",
            "llm_suggestion_only",
        ],
        "fixture_registry_authorization_required": True,
        "user_upload_authorization_insufficient_alone": True,
        "system_generated_path_insufficient_alone": True,
        "existence_check_pass_insufficient_alone": True,
        "review_status_required": True,
        "source_chain_required": True,
        "notes": ["exists gate pass != stat gate pass; stat needs separate gate + metadata exposure boundary"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_audit_trace_policy = {
        "audit_required": True,
        "trace_required": True,
        "required_trace_fields": [
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
            "no_stat_claim_current_phase",
        ],
        "audit_sink_candidate": ["jsonl_audit_log", "verifier_report_attachment"],
        "no_fact_from_audit": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_failure_mode_policy = {
        "stat_permission_denied_future_behavior": "require_manual_review_and_re_registration",
        "stat_missing_file_future_behavior": "keep_as_existence_candidate_only_and_block_stat_candidate",
        "stat_symlink_detected_future_behavior": "restrict_and_require_manual_review",
        "stat_path_untrusted_behavior": "block_candidate",
        "stat_source_chain_missing_behavior": "block_candidate",
        "stat_privacy_tags_missing_behavior": "block_candidate",
        "stat_gate_denied_behavior": "keep_as_manifest_only",
        "fallback_candidate": [
            "keep_as_existence_candidate_only",
            "keep_as_manifest_only",
            "block_candidate",
            "require_manual_review",
            "require_re_registration",
            "no_worldmodel_write",
            "no_task_action",
        ],
        "no_worldmodel_write": True,
        "no_task_action": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_rollback_policy = {
        "rollback_required": True,
        "rollback_scope": "planning_only_no_side_effect",
        "no_persistent_side_effects": True,
        "candidate_status_revert": True,
        "audit_mark_reverted": True,
        "no_fact_write": True,
        "no_memory_write": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    file_stat_decision_candidate_schema = {
        "stat_decision_candidate_id": "file_stat_decision_candidate_schema_v1",
        "schema_name": "FileStatDecisionCandidateSchema",
        "schema_version": "v1",
        "fields": [
            "stat_decision_candidate_id",
            "file_ref_placeholder",
            "path_classification_ref",
            "authorization_ref",
            "privacy_precheck_ref",
            "manual_review_ref",
            "stat_metadata_boundary_ref",
            "future_stat_allowed_candidate",
            "current_stat_invoked",
            "os_stat_invoked",
            "pathlib_stat_invoked",
            "lstat_invoked",
            "file_stat_verified",
            "stat_status",
            "allowed_stat_metadata_candidate",
            "restricted_stat_metadata_candidate",
            "blocked_stat_metadata_candidate",
            "fact_status",
            "source_chain",
        ],
        "invariants": {
            "future_stat_allowed_candidate": True,
            "current_stat_invoked": False,
            "os_stat_invoked": False,
            "pathlib_stat_invoked": False,
            "lstat_invoked": False,
            "file_stat_verified": False,
            "stat_status": "not_checked",
            "fact_status": "not_fact",
        },
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    stat_to_file_metadata_candidate_mapping_policy = {
        "policy_name": "StatToFileMetadataCandidateMappingPolicy",
        "stat_decision_candidate_ref": "file_stat_decision_candidate_schema.json",
        "file_metadata_candidate_ref": "file_metadata_boundary:file_metadata_candidate_schema.json",
        "mapping_allowed_future_candidate": True,
        "stat_required_now": False,
        "exists_required_now": False,
        "content_read_required_now": False,
        "real_hash_required_now": False,
        "output_status": "planning_only",
        "notes": ["mapping definition only; stat result is candidate metadata, never a fact in this chain"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_file_stat_guarded_planning_policy = {
        "policy_id": PLANNING_ID,
        "policy_scope": PLANNING_SCOPE,
        "planning_only": True,
        "stat_allowed_now": False,
        "os_stat_allowed_now": False,
        "pathlib_stat_allowed_now": False,
        "lstat_allowed_now": False,
        "exists_allowed_now": False,
        "open_allowed_now": False,
        "content_read_allowed_now": False,
        "hash_allowed_now": False,
        "inherited_file_existence_check_ref": "_eval_out/controlled_frame_file_existence_check_guarded_closure_v1_smoke_v0/controlled_frame_file_existence_check_guarded_closure_summary.json",
        "file_stat_gate_ref": "file_stat_gate_policy.json",
        "allowed_path_scope_policy_ref": "allowed_stat_path_scope_policy.json",
        "blocked_path_scope_policy_ref": "blocked_stat_path_scope_policy.json",
        "stat_metadata_exposure_boundary_ref": "file_stat_metadata_exposure_boundary_policy.json",
        "authorization_policy_ref": "file_stat_authorization_policy.json",
        "privacy_precheck_linkage_ref": "controlled_frame_sample_planning:privacy_precheck_policy.json",
        "manual_review_linkage_ref": "controlled_frame_sample_planning:manual_review_gate_policy.json",
        "audit_trace_policy_ref": "file_stat_audit_trace_policy.json",
        "failure_mode_policy_ref": "file_stat_failure_mode_policy.json",
        "rollback_policy_ref": "file_stat_rollback_policy.json",
        "stat_decision_candidate_schema_ref": "file_stat_decision_candidate_schema.json",
        "stat_to_file_metadata_candidate_mapping_ref": "stat_to_file_metadata_candidate_mapping_policy.json",
        "no_file_operation_boundary_ref": "no_file_operation_boundary_report.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    # ---- Scenario matrix (planning-only) ----
    scenario_specs = [
        {"scenario_id": "repo_fixture_stat_future_candidate", "category": "future_allowed", "path_type": "repo_fixture_path_candidate"},
        {"scenario_id": "eval_out_fixture_stat_future_candidate", "category": "future_allowed", "path_type": "eval_out_fixture_path_candidate"},
        {"scenario_id": "registered_fixture_stat_future_candidate", "category": "future_allowed", "path_type": "explicitly_registered_fixture_path_candidate"},
        {"scenario_id": "controlled_test_asset_stat_future_candidate", "category": "future_allowed", "path_type": "controlled_test_asset_path_candidate"},
        {"scenario_id": "user_upload_stat_restricted", "category": "restricted", "path_type": "user_uploaded_path_restricted_not_allowed_by_default"},
        {"scenario_id": "external_absolute_path_stat_blocked", "category": "blocked", "path_type": "external_absolute_path_blocked"},
        {"scenario_id": "path_traversal_stat_blocked", "category": "blocked", "path_type": "path_traversal_blocked"},
        {"scenario_id": "unknown_path_stat_blocked", "category": "blocked", "path_type": "unknown_path_blocked"},
        {"scenario_id": "symlink_stat_restricted", "category": "restricted", "path_type": "symlink_unresolved_blocked_or_restricted"},
        {"scenario_id": "system_sensitive_path_stat_blocked", "category": "blocked", "path_type": "system_sensitive_path_blocked"},
        {"scenario_id": "home_arbitrary_path_stat_blocked", "category": "blocked", "path_type": "home_directory_arbitrary_path_blocked"},
        {"scenario_id": "network_mount_path_stat_blocked", "category": "blocked", "path_type": "network_mount_path_blocked"},
        {"scenario_id": "missing_source_chain_stat_blocked", "category": "blocked", "reason": "missing_source_chain"},
        {"scenario_id": "missing_privacy_tags_stat_blocked", "category": "blocked", "reason": "missing_privacy_tags"},
        {"scenario_id": "missing_fixture_registry_ref_stat_blocked", "category": "blocked", "reason": "missing_fixture_registry_ref"},
        {"scenario_id": "exists_gate_pass_insufficient_for_stat", "category": "governance_invariant", "reason": "existence_check_pass_insufficient_alone"},
        {"scenario_id": "authorized_stat_candidate_but_not_invoked", "category": "authorized_but_not_invoked", "notes": "authorization present but planning-only prohibits execution"},
        {"scenario_id": "stat_metadata_allowed_candidate", "category": "metadata_allowed"},
        {"scenario_id": "stat_metadata_restricted_candidate", "category": "metadata_restricted"},
        {"scenario_id": "stat_metadata_blocked_or_deferred", "category": "metadata_blocked"},
        {"scenario_id": "stat_permission_denied_future_failure_mode", "category": "failure_mode", "failure_mode": "stat_permission_denied_future_behavior"},
        {"scenario_id": "stat_missing_file_future_failure_mode", "category": "failure_mode", "failure_mode": "stat_missing_file_future_behavior"},
        {"scenario_id": "stat_gate_denied_behavior", "category": "failure_mode", "failure_mode": "stat_gate_denied_behavior"},
        {"scenario_id": "stat_rollback_after_denied_candidate", "category": "rollback", "rollback_case": "rollback_after_denied_candidate"},
    ]

    scenario_rows = [
        {
            **spec,
            "planning_only": True,
            "future_stat_allowed_candidate": spec.get("category") in {"future_allowed", "authorized_but_not_invoked", "metadata_allowed"},
            "current_stat_invoked": False,
            "os_stat_invoked": False,
            "pathlib_stat_invoked": False,
            "lstat_invoked": False,
            "file_stat_verified": False,
            "stat_status": "not_checked",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for spec in scenario_specs
    ]
    controlled_frame_file_stat_guarded_planning_scenario_matrix = {
        "scenarios": scenario_rows,
        "scenario_count": len(scenario_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    future_allowed_stat_path_candidate_count = sum(1 for s in scenario_specs if s.get("category") == "future_allowed")
    blocked_stat_path_candidate_count = sum(1 for s in scenario_specs if s.get("category") == "blocked")
    restricted_stat_path_candidate_count = sum(1 for s in scenario_specs if s.get("category") == "restricted")

    stat_metadata_allowed_candidate_count = len(file_stat_metadata_exposure_boundary_policy.get("allowed_stat_metadata_candidate", []))
    stat_metadata_restricted_candidate_count = len(file_stat_metadata_exposure_boundary_policy.get("restricted_stat_metadata_candidate", []))
    stat_metadata_blocked_or_deferred_count = len(file_stat_metadata_exposure_boundary_policy.get("blocked_stat_metadata_candidate", []))
    failure_mode_case_count = sum(1 for s in scenario_specs if s.get("category") == "failure_mode")
    rollback_case_count = sum(1 for s in scenario_specs if s.get("category") == "rollback")

    file_stat_boundary_matrix = {
        "frozen_boundaries": [
            "planning-only",
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
            "no-worldmodel-memory-fact-library",
        ],
        "allowed_now": {
            "policy_definition": True,
            "schema_definition": True,
            "scenario_matrix_definition": True,
            "audit_trace_policy_definition": True,
            "metadata_exposure_boundary_definition": True,
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
            {"topic": "stat metadata exposure boundary hardening", "roadmap_impact": "must be explicit before any guarded stat trial", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "symlink and path normalization policy", "roadmap_impact": "must prevent scope escape via symlinks", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "authorization provenance and fixture registry lifecycle", "roadmap_impact": "stat requires registry-backed authorization", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "privacy precheck taxonomy for file system metadata", "roadmap_impact": "stat may leak time/size correlations; precheck must classify", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "audit trace schema alignment across file governance chain", "roadmap_impact": "must be consistent for dry-run and future guarded trial", "source_chain": SOURCE_CHAIN, **_not_fact()},
            {"topic": "failure-mode to rollback linkage", "roadmap_impact": "dry-run must simulate rollback with no side effects", "source_chain": SOURCE_CHAIN, **_not_fact()},
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "reason": "file stat guarded planning policies/schemas defined; next step is simulation-only dry-run of stat gate decisions without calling stat/exists/open",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    required_ok = all(
        [
            post_file_existence_check_roadmap_input_loaded,
            file_existence_check_guarded_closure_input_loaded,
            file_existence_check_guarded_post_review_input_loaded,
            file_existence_check_guarded_dryrun_input_loaded,
            file_existence_check_guarded_planning_input_loaded,
            post_file_metadata_boundary_roadmap_input_loaded,
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
    )
    if not required_ok:
        blockers.append("required_root_missing_or_invalid")
    if len(scenario_specs) < 24:
        blockers.append("scenario_matrix_insufficient")

    output_root_fixed_to_luna_core = True

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "post_file_existence_check_roadmap_input_loaded": post_file_existence_check_roadmap_input_loaded,
        "file_existence_check_guarded_closure_input_loaded": file_existence_check_guarded_closure_input_loaded,
        "file_existence_check_guarded_post_review_input_loaded": file_existence_check_guarded_post_review_input_loaded,
        "file_existence_check_guarded_dryrun_input_loaded": file_existence_check_guarded_dryrun_input_loaded,
        "file_existence_check_guarded_planning_input_loaded": file_existence_check_guarded_planning_input_loaded,
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
        "controlled_frame_file_stat_guarded_planning_policy_defined": True,
        "file_stat_gate_policy_defined": True,
        "file_stat_metadata_exposure_boundary_policy_defined": True,
        "allowed_stat_path_scope_policy_defined": True,
        "blocked_stat_path_scope_policy_defined": True,
        "file_stat_authorization_policy_defined": True,
        "file_stat_audit_trace_policy_defined": True,
        "file_stat_failure_mode_policy_defined": True,
        "file_stat_rollback_policy_defined": True,
        "file_stat_decision_candidate_schema_defined": True,
        "stat_to_file_metadata_candidate_mapping_policy_defined": True,
        "scenario_matrix_generated": True,
        "scenario_count": len(scenario_specs),
        "future_allowed_stat_path_candidate_count": future_allowed_stat_path_candidate_count,
        "blocked_stat_path_candidate_count": blocked_stat_path_candidate_count,
        "restricted_stat_path_candidate_count": restricted_stat_path_candidate_count,
        "stat_metadata_allowed_candidate_count": stat_metadata_allowed_candidate_count,
        "stat_metadata_restricted_candidate_count": stat_metadata_restricted_candidate_count,
        "stat_metadata_blocked_or_deferred_count": stat_metadata_blocked_or_deferred_count,
        "failure_mode_case_count": failure_mode_case_count,
        "rollback_case_count": rollback_case_count,
        "authorization_required": True,
        "audit_trace_required": True,
        "rollback_required": True,
        "source_chain_required": True,
        "fixture_registry_authorization_required": True,
        "user_upload_authorization_insufficient_alone": True,
        "system_generated_path_insufficient_alone": True,
        "existence_check_pass_insufficient_alone": True,
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
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_frame_file_stat_guarded_planning_policy": controlled_frame_file_stat_guarded_planning_policy,
        "file_stat_gate_policy": file_stat_gate_policy,
        "file_stat_metadata_exposure_boundary_policy": file_stat_metadata_exposure_boundary_policy,
        "allowed_stat_path_scope_policy": allowed_stat_path_scope_policy,
        "blocked_stat_path_scope_policy": blocked_stat_path_scope_policy,
        "file_stat_authorization_policy": file_stat_authorization_policy,
        "file_stat_audit_trace_policy": file_stat_audit_trace_policy,
        "file_stat_failure_mode_policy": file_stat_failure_mode_policy,
        "file_stat_rollback_policy": file_stat_rollback_policy,
        "file_stat_decision_candidate_schema": file_stat_decision_candidate_schema,
        "stat_to_file_metadata_candidate_mapping_policy": stat_to_file_metadata_candidate_mapping_policy,
        "controlled_frame_file_stat_guarded_planning_scenario_matrix": controlled_frame_file_stat_guarded_planning_scenario_matrix,
        "file_stat_boundary_matrix": file_stat_boundary_matrix,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": _boundary_payload(),
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }

