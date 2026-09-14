# -*- coding: utf-8 -*-
"""Controlled Frame File Stat Guarded Closure v1 (closure-only).

Closes the governance chain:
Planning -> DryRun -> Post-DryRun Review.

CRITICAL: This closure does NOT enable real filesystem access.
Real stat/exists/open/read/hash remain DISABLED.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-File-Stat-Guarded-Closure-v1-001"
CLOSURE_ID = "cffsgc_v1_001"
CLOSURE_SCOPE = "controlled_frame_file_stat_guarded_closure_only"
SOURCE_CHAIN = "controlled_frame_file_stat_guarded_closure_v1"

FINAL_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-File-Stat-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
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

ROOT_SPECS = [
    {
        "id": "post_dryrun_review",
        "arg": "post_dryrun_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "file_stat_closure_readiness_decision.json", "verifier_report.json"],
    },
    {
        "id": "dryrun",
        "arg": "dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_stat_guarded_dryrun_results.json", "no_file_operation_boundary_report.json", "verifier_report.json"],
    },
    {
        "id": "planning",
        "arg": "planning_root",
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
        "artifacts": ["summary.json", "verifier_report.json"],
    },
    {
        "id": "file_existence_check_guarded_closure",
        "arg": "file_existence_check_guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_existence_check_guarded_closure_summary.json", "validated_capability_summary.json", "verifier_report.json"],
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
        "artifacts": ["summary.json", "controlled_frame_file_metadata_boundary_closure_summary.json", "validated_capability_summary.json", "verifier_report.json"],
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

COMPLETED_PHASES = [
    (
        "Controlled Frame File Stat Guarded Planning v1",
        "Phase-Controlled-Frame-File-Stat-Guarded-Planning-v1-001",
        "planning",
        "_eval_out/controlled_frame_file_stat_guarded_planning_v1_smoke_v0/",
        "GO",
        "gate policies + schemas for future guarded file stat (planning-only)",
    ),
    (
        "Controlled Frame File Stat Guarded DryRun v1",
        "Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001",
        "dryrun",
        "_eval_out/controlled_frame_file_stat_guarded_dryrun_v1_smoke_v0/",
        "GO",
        "simulation-only gate decisions; no stat/exists/open/read/hash",
    ),
    (
        "Controlled Frame File Stat Guarded Post-DryRun Review v1",
        "Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001",
        "post_dryrun_review",
        "_eval_out/controlled_frame_file_stat_guarded_post_dryrun_review_v1_smoke_v0/",
        "GO",
        "review-only audit confirming dry-run stability and boundary conformance",
    ),
]

VALIDATED_CAPABILITIES = [
    "file stat gate policy",
    "stat path scope policy",
    "stat metadata exposure boundary",
    "stat authorization policy",
    "stat audit trace policy",
    "stat failure mode policy",
    "stat rollback policy",
    "stat decision candidate schema",
    "stat-to-file-metadata mapping policy",
    "future allowed / restricted / blocked stat path classification",
    "exists gate pass insufficient for stat",
    "missing source_chain / privacy tags / fixture registry blocking",
    "stat metadata allowed / restricted / blocked classification",
    "authorization insufficiency detection",
    "stat permission denied future failure mode",
    "stat missing file future failure mode",
    "stat gate denied behavior",
    "stat metadata boundary denied behavior",
    "rollback after denied candidate",
    "dry-run simulation",
    "post-dryrun review",
]

DISABLED_FILE_OPERATIONS = [
    "os.stat",
    "pathlib.Path.stat",
    "lstat",
    "file stat",
    "os.path.exists",
    "pathlib.Path.exists",
    "file existence check",
    "file open",
    "file content read",
    "image content read",
    "video content read",
    "image open",
    "video open",
    "video decode",
    "frame extraction",
    "EXIF parse",
    "video probe",
    "real file hash computation",
    "perceptual hash computation",
    "real metadata read",
]

DISABLED_RUNTIMES = [
    "camera runtime",
    "visual model runtime",
    "OCR provider runtime",
    "OCRRequest submission",
    "map API / 高德 API",
    "GPS runtime",
    "tracking runtime",
    "optical flow runtime",
    "crossing runtime",
    "Speech Gate / VOP / TTS",
    "NavigationAction",
    "TaskState commit",
    "WorldModel write",
    "Memory write",
    "Library write",
    "Fact write",
    "SceneDelta",
]

NON_CLAIMS = [
    "closure 不等于 os.stat 可用",
    "closure 不等于 pathlib.Path.stat 可用",
    "closure 不等于 lstat 可用",
    "closure 不等于真实 stat 可用",
    "closure 不等于 exists 可用",
    "closure 不等于文件打开可用",
    "closure 不等于真实 metadata 读取",
    "closure 不等于权限/owner/inode 等真实系统 metadata 可用",
    "closure 不等于图像读取",
    "closure 不等于视频读取",
    "closure 不等于真实 hash",
    "closure 不等于 EXIF / video probe",
    "closure 不等于视觉模型 runtime",
    "closure 不等于 OCR/tracking/map/crossing runtime",
    "stat decision candidate 不等于文件事实",
    "stat gate dry-run 不等于 production readiness",
]

DEFERRED_CAPABILITIES = [
    "Real File Stat Guarded Trial",
    "Real File Existence Check Guarded Trial",
    "Real Metadata Read Guarded Planning",
    "Real Hash Computation Guarded Planning",
    "EXIF Parse Guarded Planning",
    "Video Probe Guarded Planning",
    "Controlled Static Image Read Preplan",
    "Controlled Image Content Read Guarded Trial",
    "Controlled Video Decode Guarded Trial",
    "Controlled Frame Extraction Guarded Trial",
    "Real Fixture Registry Runtime",
    "Visual Model Adapter DryRun",
    "OCR Provider Re-enable through VisualFocus",
    "Tracking Adapter Experiment Branch",
    "Real VisualObservation generation",
    "Real SceneSketch generation",
    "Real OCRActivationResult generation",
    "Real TrackingResult generation",
    "Gate Taxonomy / Gate Requirement Framework",
    "MidPlatform Function Governance / Consolidation",
    "MidPlatform Resilience / Robustness",
    "Offline Distributed MidPlatform",
    "WorldModel / Memory / Library Governance",
]

GOVERNANCE_DEBT = [
    "file stat gate governance complexity",
    "stat metadata exposure boundary complexity",
    "future real stat risk",
    "future filesystem metadata privacy risk",
    "owner / permission / inode exposure risk",
    "symlink handling risk",
    "cross-repo input root ambiguity",
    "fixture registry governance complexity",
    "gate taxonomy required later",
    "midplatform function governance required later",
    "resilience governance required later",
    "no_duplicate_governance_module_allowed=true",
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


def _boundary_payload() -> Dict[str, Any]:
    return {
        "closure_scope": CLOSURE_SCOPE,
        "closure_only": True,
        "stat_gate_decision_simulation_only": True,
        "real_stat_readiness_claimed": False,
        "real_exists_readiness_claimed": False,
        "file_open_readiness_claimed": False,
        "real_metadata_readiness_claimed": False,
        "real_image_readiness_claimed": False,
        "visual_runtime_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
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


def run_controlled_frame_file_stat_guarded_closure_v1(
    *,
    post_dryrun_review_root: str,
    dryrun_root: str,
    planning_root: str,
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

    post_dryrun_review_input_loaded = (
        roots["post_dryrun_review"]["loaded"] and summaries["post_dryrun_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    dryrun_input_loaded = roots["dryrun"]["loaded"] and summaries["dryrun"].get("final_decision") == DRYRUN_DECISION
    planning_input_loaded = roots["planning"]["loaded"] and summaries["planning"].get("final_decision") == PLANNING_DECISION

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

    completed_phase_matrix = {
        "phases": [
            {
                "phase_name": phase_name,
                "phase_id": phase_id,
                "status": "completed",
                "output_dir": output_dir,
                "verifier_verdict": verifier_verdict,
                "final_decision": summaries.get(role, {}).get("final_decision", ""),
                "role_in_closure": role,
                "file_operation_enabled": False,
                "runtime_enabled": False,
                "write_enabled": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for (phase_name, phase_id, role, output_dir, verifier_verdict, _notes) in COMPLETED_PHASES
        ],
        "phase_count": len(COMPLETED_PHASES),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    validated_capability_summary = {
        "validated_capabilities": VALIDATED_CAPABILITIES,
        "capability_count": len(VALIDATED_CAPABILITIES),
        "notes": [
            "validated capabilities are governance-only for stat gate planning/dryrun/review",
            "this does not enable real stat or real filesystem metadata access",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    disabled_file_operation_summary = {
        "disabled_file_operations": DISABLED_FILE_OPERATIONS,
        "disabled_count": len(DISABLED_FILE_OPERATIONS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    disabled_runtime_summary = {
        "disabled_runtimes": DISABLED_RUNTIMES,
        "disabled_count": len(DISABLED_RUNTIMES),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_boundary_freeze = {
        "frozen_boundaries": [
            "no-stat-call",
            "no-os-stat",
            "no-pathlib-stat",
            "no-lstat",
            "no-exists-call",
            "no-os-path-exists",
            "no-pathlib-exists",
            "no-file-open",
            "no-image-open",
            "no-video-open",
            "no-image-read",
            "no-video-read",
            "no-exif-parse",
            "no-video-probe",
            "no-video-decode",
            "no-frame-extract",
            "no-real-hash",
            "no-perceptual-hash",
            "no-real-metadata-read",
            "no-runtime",
            "no-write",
            "no-action",
            "no-speech",
            "no-fact",
            "candidate-only",
            "stat-gate-simulation-only",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_claims_register = {
        "non_claims": NON_CLAIMS,
        "count": len(NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_capability_pool = {
        "deferred_capabilities": DEFERRED_CAPABILITIES,
        "count": len(DEFERRED_CAPABILITIES),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_carryover = {
        "carryover_topics": [{"topic": t, "source_chain": SOURCE_CHAIN, **_not_fact()} for t in GOVERNANCE_DEBT],
        "gate_taxonomy_required_later": True,
        "midplatform_function_governance_required_later": True,
        "midplatform_resilience_required_later": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_readiness_gate = {
        "go_conditions": [
            "planning input loaded",
            "dryrun input loaded",
            "post-review input loaded",
            "completed phase matrix generated",
            "validated capability summary generated",
            "disabled file operation summary generated",
            "disabled runtime summary generated",
            "boundary freeze generated",
            "non-claims register generated",
            "deferred capability pool generated",
            "governance debt carryover generated",
            "stat gate decision simulation only",
            "no stat/exists/open/read/hash/probe",
            "no runtime",
            "no write",
            "no action",
            "no speech",
            "next phase fixed",
        ],
        "no_go_conditions": [
            "any required root missing",
            "os.stat invoked",
            "pathlib.Path.stat invoked",
            "lstat invoked",
            "os.path.exists invoked",
            "pathlib.Path.exists invoked",
            "file opened",
            "image/video content read",
            "EXIF parsed",
            "video probed",
            "real hash computed",
            "pHash computed",
            "visual model invoked",
            "OCR provider invoked",
            "tracking runtime invoked",
            "map API invoked",
            "WorldModel/Memory/Fact write",
            "NavigationAction triggered",
            "Speech/TTS invoked",
            "closure claims real stat readiness",
            "closure claims real metadata readiness",
            "closure claims runtime readiness",
            "next phase unclear",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not (post_dryrun_review_input_loaded and dryrun_input_loaded and planning_input_loaded):
        blockers.append("phase_chain_inputs_missing_or_invalid")
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
        blockers.append("required_upstream_roots_missing_or_invalid")

    boundary_ok = not blockers

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "post_dryrun_review_input_loaded": post_dryrun_review_input_loaded,
        "dryrun_input_loaded": dryrun_input_loaded,
        "planning_input_loaded": planning_input_loaded,
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
        "completed_phase_matrix_generated": True,
        "completed_phase_count": len(COMPLETED_PHASES),
        "validated_capability_summary_generated": True,
        "disabled_file_operation_summary_generated": True,
        "disabled_runtime_summary_generated": True,
        "closure_boundary_freeze_generated": True,
        "non_claims_register_generated": True,
        "deferred_capability_pool_generated": True,
        "governance_debt_carryover_generated": True,
        "closure_readiness_gate_generated": True,
        "file_stat_guarded_planning_closed": True,
        "file_stat_guarded_dryrun_closed": True,
        "file_stat_guarded_post_review_closed": True,
        "file_stat_guarded_closed": True,
        "stat_gate_decision_simulation_only": True,
        "real_stat_readiness_claimed": False,
        "real_exists_readiness_claimed": False,
        "file_open_readiness_claimed": False,
        "real_metadata_readiness_claimed": False,
        "real_image_readiness_claimed": False,
        "visual_runtime_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
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
        "output_root_fixed_to_luna_core": True,
        "gate_taxonomy_required_later": True,
        "midplatform_function_governance_required_later": True,
        "midplatform_resilience_required_later": True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "CONTROLLED_FRAME_FILE_STAT_GUARDED_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_file_stat_guarded_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "source_phase_chain": [
            "Phase-Controlled-Frame-File-Stat-Guarded-Planning-v1-001",
            "Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001",
            "Phase-Controlled-Frame-File-Stat-Guarded-Post-DryRun-Review-v1-001",
        ],
        "completed_phase_count": len(COMPLETED_PHASES),
        "completed_phase_matrix_ref": "completed_phase_matrix.json",
        "validated_capability_summary_ref": "validated_capability_summary.json",
        "disabled_file_operation_summary_ref": "disabled_file_operation_summary.json",
        "disabled_runtime_summary_ref": "disabled_runtime_summary.json",
        "closure_boundary_freeze_ref": "closure_boundary_freeze.json",
        "non_claims_register_ref": "file_stat_non_claims_register.json",
        "deferred_capability_pool_ref": "deferred_capability_pool.json",
        "governance_debt_carryover_ref": "governance_debt_carryover.json",
        "next_phase_recommendation": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": summary["final_decision"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": summary["recommended_next_phase"],
        "final_decision": summary["final_decision"],
        "reason": "file stat gate chain closed; next step is roadmap-decision-only (no runtime/no file ops enabled)",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_frame_file_stat_guarded_closure_summary": controlled_frame_file_stat_guarded_closure_summary,
        "completed_phase_matrix": completed_phase_matrix,
        "validated_capability_summary": validated_capability_summary,
        "disabled_file_operation_summary": disabled_file_operation_summary,
        "disabled_runtime_summary": disabled_runtime_summary,
        "closure_boundary_freeze": closure_boundary_freeze,
        "file_stat_non_claims_register": non_claims_register,
        "deferred_capability_pool": deferred_capability_pool,
        "governance_debt_carryover": governance_debt_carryover,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": _boundary_payload(),
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }

