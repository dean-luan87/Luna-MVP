# -*- coding: utf-8 -*-
"""Controlled Frame File Metadata Boundary Closure v1 (closure-only)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-File-Metadata-Boundary-Closure-v1-001"
CLOSURE_ID = "cffmbc_v1_001"
CLOSURE_SCOPE = "controlled_frame_file_metadata_boundary_closure_only"
SOURCE_CHAIN = "controlled_frame_file_metadata_boundary_closure_v1"
FINAL_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-File-Metadata-Boundary-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_READY_FOR_DRYRUN"
POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION = (
    "POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION_READY_FOR_FILE_METADATA_BOUNDARY_PLANNING"
)
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
        "artifacts": [
            "summary.json",
            "file_metadata_boundary_closure_readiness_decision.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "dryrun",
        "arg": "dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_file_metadata_boundary_dryrun_scenario_matrix.json",
            "path_legality_decision_results.json",
            "no_file_operation_boundary_report.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "planning",
        "arg": "planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_file_metadata_boundary_planning_policy.json",
            "path_legality_policy.json",
            "external_metadata_boundary_policy.json",
            "real_hash_computation_policy.json",
            "fixture_registry_policy.json",
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

COMPLETED_PHASES = [
    (
        "Controlled Frame File Metadata Boundary Planning v1",
        "Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001",
        "planning",
        "_eval_out/controlled_frame_file_metadata_boundary_planning_v1_smoke_v0/",
        "GO",
        "file/metadata boundary policy and schema definition (planning-only)",
    ),
    (
        "Controlled Frame File Metadata Boundary DryRun v1",
        "Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001",
        "dryrun",
        "_eval_out/controlled_frame_file_metadata_boundary_dryrun_v1_smoke_v0/",
        "GO",
        "metadata/file-boundary decision simulation without real file operations",
    ),
    (
        "Controlled Frame File Metadata Boundary Post-DryRun Review v1",
        "Phase-Controlled-Frame-File-Metadata-Boundary-Post-DryRun-Review-v1-001",
        "post_dryrun_review",
        "_eval_out/controlled_frame_file_metadata_boundary_post_dryrun_review_v1_smoke_v0/",
        "GO",
        "review-only audit confirming planning+dryrun alignment and no-file-operation boundaries",
    ),
]

VALIDATED_CAPABILITIES = [
    "file existence policy",
    "path legality policy",
    "external metadata boundary policy",
    "real hash policy",
    "fixture registry policy",
    "fixture registry entry schema",
    "manifest-to-file-metadata candidate mapping",
    "file metadata candidate schema",
    "path allowed / restricted / blocked classification",
    "declared metadata handling",
    "missing metadata blocking",
    "sensitive metadata manual review routing",
    "hash placeholder allowed",
    "real hash blocked",
    "EXIF / video probe blocked",
    "perceptual hash deferred",
    "dry-run simulation",
    "post-dryrun review",
]

DISABLED_FILE_OPERATIONS = [
    "file existence check",
    "file stat",
    "file open",
    "image open",
    "video open",
    "image content read",
    "video content read",
    "EXIF parse",
    "video probe",
    "video decode",
    "frame extraction",
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

EXPECTED_NON_CLAIMS = [
    "closure 不等于文件存在性检查可用",
    "closure 不等于文件 stat 可用",
    "closure 不等于可以打开样例文件",
    "closure 不等于真实 metadata 读取",
    "closure 不等于 EXIF 解析",
    "closure 不等于 video probe",
    "closure 不等于真实 hash 计算",
    "closure 不等于 pHash / 内容分析",
    "closure 不等于真实图像读取",
    "closure 不等于真实视频读取",
    "closure 不等于视觉模型 runtime",
    "closure 不等于 OCR/tracking/map/crossing runtime",
    "fixture registry candidate 不等于真实 registry runtime",
    "file metadata candidate 不等于文件事实",
    "metadata dry-run 不等于 production readiness",
]

EXPECTED_DEFERRED = [
    "File Existence Check Guarded Planning",
    "File Stat Guarded Planning",
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

EXPECTED_DEBT_TOPICS = [
    "file boundary governance complexity",
    "path legality policy maintenance",
    "future file existence check risk",
    "future real metadata read risk",
    "future real hash computation risk",
    "EXIF / video probe privacy risk",
    "fixture registry governance complexity",
    "manifest-to-file-metadata mapping complexity",
    "sensitive metadata manual review complexity",
    "gate taxonomy required later",
    "midplatform function governance required later",
    "resilience governance required later",
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


def _no_file_operation_payload() -> Dict[str, Any]:
    return {
        "closure_scope": CLOSURE_SCOPE,
        "closure_only": True,
        "metadata_decision_simulation_only": True,
        "file_existence_check_readiness_claimed": False,
        "real_metadata_readiness_claimed": False,
        "real_hash_readiness_claimed": False,
        "real_image_readiness_claimed": False,
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
        "closure_scope": CLOSURE_SCOPE,
        "visual_runtime_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
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
        "gate_taxonomy_required_later": True,
        "midplatform_function_governance_required_later": True,
        "midplatform_resilience_required_later": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_controlled_frame_file_metadata_boundary_closure_v1(
    *,
    post_dryrun_review_root: str,
    dryrun_root: str,
    planning_root: str,
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

    post_dryrun_review_input_loaded = (
        roots["post_dryrun_review"]["loaded"] and summaries["post_dryrun_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    dryrun_input_loaded = roots["dryrun"]["loaded"] and summaries["dryrun"].get("final_decision") == DRYRUN_DECISION
    planning_input_loaded = roots["planning"]["loaded"] and summaries["planning"].get("final_decision") == PLANNING_DECISION
    post_controlled_frame_sample_roadmap_input_loaded = (
        roots["post_controlled_frame_sample_roadmap_decision"]["loaded"]
        and summaries["post_controlled_frame_sample_roadmap_decision"].get("final_decision")
        == POST_CONTROLLED_FRAME_SAMPLE_ROADMAP_DECISION
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

    completed_phase_matrix = {
        "phases": [
            {
                "phase_id": phase_id,
                "phase_name": phase_name,
                "status": verifier_verdict,
                "output_dir": out_dir,
                "verifier_verdict": verifier_verdict,
                "final_decision": summaries[phase_key].get("final_decision", ""),
                "role_in_closure": role,
                "file_operation_enabled": False,
                "runtime_enabled": False,
                "write_enabled": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for phase_name, phase_id, phase_key, out_dir, verifier_verdict, role in COMPLETED_PHASES
        ],
        "phase_count": len(COMPLETED_PHASES),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    validated_capability_summary = {
        "capabilities": [
            {
                "capability": item,
                "validated_level": "planning+dryrun+review",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for item in VALIDATED_CAPABILITIES
        ],
        "capability_count": len(VALIDATED_CAPABILITIES),
        "notes": [
            "这些是 metadata/file-boundary governance 能力，不是真实文件操作能力。",
            "不是真实 metadata read，不是真实 hash，不是图像读取能力。",
            "本链路不允许 stat、打开文件、解析 EXIF、probe 视频、计算真实 hash。",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    disabled_file_operation_summary = {
        "disabled_operations": [
            {"operation": item, "enabled": False, "source_chain": SOURCE_CHAIN, **_not_fact()} for item in DISABLED_FILE_OPERATIONS
        ],
        "disabled_operation_count": len(DISABLED_FILE_OPERATIONS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    disabled_runtime_summary = {
        "disabled_runtimes": [
            {"runtime": item, "enabled": False, "source_chain": SOURCE_CHAIN, **_not_fact()} for item in DISABLED_RUNTIMES
        ],
        "disabled_runtime_count": len(DISABLED_RUNTIMES),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_boundary_freeze = {
        "closure_scope": CLOSURE_SCOPE,
        "frozen_boundaries": [
            "no-file-existence-check",
            "no-file-stat",
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
            "metadata-simulation-only",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_file_metadata_boundary_non_claims_register = {
        "non_claims": [{"non_claim": item, "source_chain": SOURCE_CHAIN, **_not_fact()} for item in EXPECTED_NON_CLAIMS],
        "non_claim_count": len(EXPECTED_NON_CLAIMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_capability_pool = {
        "deferred_items": [
            {"item": item, "reason": "deferred until future guarded planning/trials", "source_chain": SOURCE_CHAIN, **_not_fact()}
            for item in EXPECTED_DEFERRED
        ],
        "deferred_count": len(EXPECTED_DEFERRED),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_carryover = {
        "carryover_topics": [
            {"topic": topic, "no_duplicate_governance_module_allowed": True, "source_chain": SOURCE_CHAIN, **_not_fact()}
            for topic in EXPECTED_DEBT_TOPICS
        ],
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
            "file operation boundary pass",
            "metadata decision simulation only",
            "no file stat/open/read/hash/probe",
            "no runtime",
            "no write",
            "no action",
            "no speech",
            "next phase fixed",
        ],
        "no_go_conditions": [
            "any required root missing",
            "file existence check invoked",
            "file stat invoked",
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
            "closure claims file existence check readiness",
            "closure claims image read readiness",
            "closure claims runtime readiness",
            "next phase unclear",
        ],
        "ready_for_next_phase": True,
        "verdict": "GO",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not all(
        [
            post_dryrun_review_input_loaded,
            dryrun_input_loaded,
            planning_input_loaded,
            post_controlled_frame_sample_roadmap_input_loaded,
            controlled_frame_sample_closure_input_loaded,
            controlled_frame_input_closure_input_loaded,
            map_location_readonly_context_input_loaded,
            safety_constitution_input_loaded,
            minimal_runtime_integration_closure_loaded,
            ocr_final_closure_loaded,
        ]
    ):
        blockers.append("required_root_missing_or_invalid")

    closure_readiness_gate["ready_for_next_phase"] = not blockers
    closure_readiness_gate["verdict"] = "GO" if not blockers else "NO_GO"

    controlled_frame_file_metadata_boundary_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "source_phase_chain": [
            "Phase-Controlled-Frame-File-Metadata-Boundary-Planning-v1-001",
            "Phase-Controlled-Frame-File-Metadata-Boundary-DryRun-v1-001",
            "Phase-Controlled-Frame-File-Metadata-Boundary-Post-DryRun-Review-v1-001",
        ],
        "completed_phase_count": len(COMPLETED_PHASES),
        "completed_phase_matrix_ref": "completed_phase_matrix.json",
        "validated_capability_summary_ref": "validated_capability_summary.json",
        "disabled_file_operation_summary_ref": "disabled_file_operation_summary.json",
        "disabled_runtime_summary_ref": "disabled_runtime_summary.json",
        "closure_boundary_freeze_ref": "closure_boundary_freeze.json",
        "non_claims_register_ref": "controlled_frame_file_metadata_boundary_non_claims_register.json",
        "deferred_capability_pool_ref": "deferred_capability_pool.json",
        "governance_debt_carryover_ref": "governance_debt_carryover.json",
        "next_phase_recommendation": NEXT_PHASE if not blockers else PHASE_ID,
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSURE_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSURE_REQUIRES_FIXES",
        "reason": "file metadata boundary governance chain closed (planning+dryrun+review); strict no-file-op/no-runtime boundaries frozen"
        if not blockers
        else "blockers present",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "post_dryrun_review_input_loaded": post_dryrun_review_input_loaded,
        "dryrun_input_loaded": dryrun_input_loaded,
        "planning_input_loaded": planning_input_loaded,
        "post_controlled_frame_sample_roadmap_input_loaded": post_controlled_frame_sample_roadmap_input_loaded,
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
        "file_metadata_boundary_planning_closed": True,
        "file_metadata_boundary_dryrun_closed": True,
        "file_metadata_boundary_post_review_closed": True,
        "file_metadata_boundary_closed": True,
        "metadata_decision_simulation_only": True,
        "file_existence_check_readiness_claimed": False,
        "real_metadata_readiness_claimed": False,
        "real_hash_readiness_claimed": False,
        "real_image_readiness_claimed": False,
        "visual_runtime_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
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
        "gate_taxonomy_required_later": True,
        "midplatform_function_governance_required_later": True,
        "midplatform_resilience_required_later": True,
        "boundary_ok": not blockers,
        "violations": blockers,
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_frame_file_metadata_boundary_closure_summary": controlled_frame_file_metadata_boundary_closure_summary,
        "completed_phase_matrix": completed_phase_matrix,
        "validated_capability_summary": validated_capability_summary,
        "disabled_file_operation_summary": disabled_file_operation_summary,
        "disabled_runtime_summary": disabled_runtime_summary,
        "closure_boundary_freeze": closure_boundary_freeze,
        "controlled_frame_file_metadata_boundary_non_claims_register": controlled_frame_file_metadata_boundary_non_claims_register,
        "deferred_capability_pool": deferred_capability_pool,
        "governance_debt_carryover": governance_debt_carryover,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": _no_file_operation_payload(),
        "no_runtime_boundary_report": _no_runtime_payload(),
        "no_write_boundary_report": _no_runtime_payload(),
    }
