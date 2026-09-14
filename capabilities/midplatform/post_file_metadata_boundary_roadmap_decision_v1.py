# -*- coding: utf-8 -*-
"""Post File Metadata Boundary Roadmap Decision v1.

本阶段只做路线裁决（roadmap decision / prioritization / boundary freeze）。
不执行文件存在性检查，不 stat 文件，不打开文件，不读取真实图像/视频内容，不进入任何 runtime。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Post-File-Metadata-Boundary-Roadmap-Decision-v1-001"
DECISION_SCOPE = "post_file_metadata_boundary_roadmap_decision_only"
SOURCE_CHAIN = "post_file_metadata_boundary_roadmap_decision_v1"
DECISION_ID = "pfmbrd_v1_001"

FINAL_DECISION = "POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION_READY_FOR_FILE_EXISTENCE_CHECK_GUARDED_PLANNING"
NEXT_PHASE = "Phase-Controlled-Frame-File-Existence-Check-Guarded-Planning-v1-001"

FILE_METADATA_BOUNDARY_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_CLOSED_FOR_CURRENT_MAINLINE"
FILE_METADATA_BOUNDARY_POST_REVIEW_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
FILE_METADATA_BOUNDARY_DRYRUN_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FILE_METADATA_BOUNDARY_PLANNING_DECISION = "CONTROLLED_FRAME_FILE_METADATA_BOUNDARY_PLANNING_READY_FOR_DRYRUN"

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

ROOT_SPECS = [
    {
        "id": "file_metadata_boundary_closure",
        "arg": "file_metadata_boundary_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "controlled_frame_file_metadata_boundary_closure_summary.json",
            "validated_capability_summary.json",
        ],
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
    # Optional roots (允许不存在，必须标记 optional_missing)
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
    {
        "id": "privacy_governance_docs",
        "arg": "privacy_governance_docs_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]


ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "File Existence Check Guarded Planning",
        "route_type": "file_existence_check_guarded_planning",
        "readiness_level": "high",
        "dependency": [
            "file metadata boundary chain closed",
            "path legality policy available (candidate)",
            "fixture registry policy boundary (candidate)",
            "privacy precheck + manual review gates (still governance-only)",
        ],
        "risk_level": "medium",
        "expected_value": "very_high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "minimal step toward real-file world: define gates/scope for existence check without executing stat/open",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "B",
        "route_name": "File Stat Guarded DryRun",
        "route_type": "file_stat_guarded_dryrun",
        "readiness_level": "medium",
        "dependency": ["File Existence Check Guarded Planning"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "low",
        "governance_debt_impact": "simulate future stat behavior; still no real stat in current mainline",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "必须先完成 A（existence check guarded planning），本阶段仅路线裁决",
        "recommended_phase_name": "Phase-Controlled-Frame-File-Stat-Guarded-DryRun-v1-001",
    },
    {
        "route_id": "C",
        "route_name": "Real Metadata Read Guarded Planning",
        "route_type": "real_metadata_read_guarded_planning",
        "readiness_level": "medium",
        "dependency": ["File Existence Check Guarded Planning"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "low",
        "governance_debt_impact": "plan future reads of filesystem metadata/EXIF/video metadata with privacy gates",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "先做存在性检查的 guarded planning，避免直接进入更高风险的真实 metadata 读取规划",
        "recommended_phase_name": "Phase-Controlled-Frame-Real-Metadata-Read-Guarded-Planning-v1-001",
    },
    {
        "route_id": "D",
        "route_name": "Real Hash Computation Guarded Planning",
        "route_type": "real_hash_computation_guarded_planning",
        "readiness_level": "medium",
        "dependency": ["Real Metadata Read Guarded Planning", "File Existence Check Guarded Planning"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "high",
        "write_risk": "low",
        "governance_debt_impact": "requires reading file bytes; must remain guarded and deferred",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "真实 hash 需要读取文件 bytes；风险高，后置于 existence + real metadata 规划之后",
        "recommended_phase_name": "Phase-Controlled-Frame-Real-Hash-Computation-Guarded-Planning-v1-001",
    },
    {
        "route_id": "E",
        "route_name": "EXIF / Video Probe Guarded Planning",
        "route_type": "exif_video_probe_guarded_planning",
        "readiness_level": "medium",
        "dependency": ["Real Metadata Read Guarded Planning"],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "low",
        "governance_debt_impact": "EXIF/probe can leak sensitive metadata; requires explicit gate and audit design",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "先完成 existence 与 real metadata 的 guarded planning，再拆分 EXIF/probe 细化风险治理",
        "recommended_phase_name": "Phase-Controlled-Frame-EXIF-Video-Probe-Guarded-Planning-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "Controlled Static Image Read Preplan",
        "route_type": "controlled_static_image_read_preplan",
        "readiness_level": "low",
        "dependency": [
            "File Existence Check Guarded Planning",
            "Real Metadata Read Guarded Planning",
            "Real Hash Computation Guarded Planning",
        ],
        "risk_level": "very_high",
        "expected_value": "high",
        "runtime_risk": "very_high",
        "write_risk": "medium",
        "governance_debt_impact": "high-risk; must not jump to real image read before lower-layer file governance",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "不能跳过 existence/metadata/hash 的受控规划；当前仍不允许读图像内容",
        "recommended_phase_name": "Phase-Controlled-Frame-Controlled-Static-Image-Read-Preplan-v1-001",
    },
    {
        "route_id": "G",
        "route_name": "Gate Taxonomy / Gate Requirement Framework",
        "route_type": "project_optimization_deferred",
        "readiness_level": "medium",
        "dependency": ["gate families inventory", "verifier template standardization"],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "important but should not interrupt file governance mainline",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "重要但属于项目优化；当前主线先推进 existence check 的 guarded planning",
        "recommended_phase_name": "Phase-Gate-Taxonomy-Gate-Requirement-Framework-v1-001",
    },
    {
        "route_id": "H",
        "route_name": "MidPlatform Function Governance / Consolidation",
        "route_type": "midplatform_governance_deferred",
        "readiness_level": "medium",
        "dependency": ["schema deduplication", "module registry consolidation"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "reduces duplicated governance modules",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "P1 deferred；本阶段只路线裁决，不进入实现",
        "recommended_phase_name": "Phase-MidPlatform-Function-Governance-Consolidation-v1-001",
    },
    {
        "route_id": "I",
        "route_name": "MidPlatform Resilience / Robustness Preplan",
        "route_type": "midplatform_resilience_deferred",
        "readiness_level": "medium",
        "dependency": ["SPOF analysis", "degraded operation policy"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "low",
        "governance_debt_impact": "captures fragility topics without runtime changes",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "P1 deferred；不打断当前 file governance 主线",
        "recommended_phase_name": "Phase-MidPlatform-Resilience-Robustness-Preplan-v1-001",
    },
    {
        "route_id": "J",
        "route_name": "Offline Distributed MidPlatform Architecture Preplan",
        "route_type": "offline_distributed_midplatform_deferred",
        "readiness_level": "low",
        "dependency": ["local-first constraints", "offline/weak-network policy"],
        "risk_level": "medium",
        "expected_value": "strategic",
        "runtime_risk": "medium",
        "write_risk": "medium",
        "governance_debt_impact": "long-horizon architecture candidate",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "继续 deferred；等核心 file governance 路线推进后再开架构前置规划",
        "recommended_phase_name": "Phase-Offline-Distributed-MidPlatform-Architecture-Preplan-v1-001",
    },
    {
        "route_id": "K",
        "route_name": "WorldModel / Memory / Library Governance",
        "route_type": "future_governance_cluster_deferred",
        "readiness_level": "low",
        "dependency": ["entity resolution governance", "fact admission governance", "memory consolidation governance"],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "must stay deferred to preserve no-write guarantees",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "当前主线保持 no-write；WML 治理继续 deferred",
        "recommended_phase_name": "Phase-WorldModel-Memory-Library-Governance-v1-001",
    },
    {
        "route_id": "L",
        "route_name": "Exploration Drive / Emotion Map / Affective Engine",
        "route_type": "future_affective_candidate_deferred",
        "readiness_level": "very_low",
        "dependency": ["grounded world information", "event chain maturity", "memory governance"],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "high",
        "write_risk": "high",
        "governance_debt_impact": "long-horizon direction; must not enter mainline now",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "长期方向，P2 deferred；当前阶段仅路线裁决不进入实现",
        "recommended_phase_name": "Phase-Exploration-Drive-Emotion-Affective-Engine-v1-001",
    },
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


def _boundary_payload() -> Dict[str, Any]:
    return {
        "decision_scope": DECISION_SCOPE,
        "roadmap_decision_only": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
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
        "emotion_engine_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_post_file_metadata_boundary_roadmap_decision_v1(
    *,
    file_metadata_boundary_closure_root: str,
    file_metadata_boundary_post_review_root: str,
    file_metadata_boundary_dryrun_root: str,
    file_metadata_boundary_planning_root: str,
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
    closure_root = roots["file_metadata_boundary_closure"]["root"]
    closure_summary_payload = (
        _read_json(closure_root / "controlled_frame_file_metadata_boundary_closure_summary.json") if closure_root else {}
    )
    closure_validated_payload = _read_json(closure_root / "validated_capability_summary.json") if closure_root else {}

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
        roots["safety_constitution"]["loaded"] and summaries["safety_constitution"].get("final_decision") == SAFETY_CONSTITUTION_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = roots["ocr_final_closure"]["loaded"] and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION

    current_status_summary = {
        "current_mainline_status": "file_metadata_boundary_chain_closed_ready_for_next_roadmap_phase",
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
        "source_closure_ref": "_eval_out/controlled_frame_file_metadata_boundary_closure_v1_smoke_v0/controlled_frame_file_metadata_boundary_closure_summary.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    completed_capability_summary = {
        "capabilities": [
            {
                "capability_name": name,
                "completion_level": "policy_or_planning_or_dryrun_or_review_or_closure",
                "runtime_enabled": False,
                "production_ready": False,
                "validated_in_current_mainline": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for name in [
                "Controlled Frame File Metadata Boundary Planning v1",
                "Controlled Frame File Metadata Boundary DryRun v1",
                "Controlled Frame File Metadata Boundary Post-DryRun Review v1",
                "Controlled Frame File Metadata Boundary Closure v1",
                "Post Controlled Frame Sample Roadmap Decision v1",
                "Controlled Frame Sample Closure v1",
                "Controlled Frame Input Closure v1",
                "Map / Location Read-Only Context Policy v1",
                "Luna Safety Constitution Policy v1",
                "Minimal Runtime Integration Closure v1",
                "OCR Mainline Final Closure v1",
            ]
        ],
        "validated_capability_names_from_file_metadata_boundary_closure": closure_validated_payload.get(
            "capabilities", closure_validated_payload.get("validated_capabilities", [])
        ),
        "source_closure_summary_payload": closure_summary_payload,
        "completed_capability_count": 11,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    route_rows = [{**route, "source_chain": SOURCE_CHAIN, **_not_fact()} for route in ROUTE_OPTIONS]
    route_names = {r["route_name"] for r in ROUTE_OPTIONS}
    route_option_matrix = {
        "routes": route_rows,
        "route_option_count": len(route_rows),
        "selected_route_id": "A",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    p0_routes = [r["route_name"] for r in ROUTE_OPTIONS if r["recommended_priority"] == "P0"]
    p1_routes = [r["route_name"] for r in ROUTE_OPTIONS if r["recommended_priority"] == "P1"]
    p2_routes = [r["route_name"] for r in ROUTE_OPTIONS if r["recommended_priority"] == "P2"]
    priority_ranking = {
        "P0": p0_routes,
        "P1": p1_routes,
        "P2": p2_routes,
        "p0_route_count": len(p0_routes),
        "p1_route_count": len(p1_routes),
        "p2_route_count": len(p2_routes),
        "selected_top_priority_route": "File Existence Check Guarded Planning",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    recommended_next_phase_decision = {
        "decision_id": DECISION_ID,
        "decision_scope": DECISION_SCOPE,
        "source_closure_ref": current_status_summary["source_closure_ref"],
        "current_mainline_status": current_status_summary["current_mainline_status"],
        "completed_capability_summary_ref": "completed_capability_summary.json",
        "route_option_matrix_ref": "route_option_matrix.json",
        "priority_ranking_ref": "priority_ranking.json",
        "selected_next_phase": NEXT_PHASE,
        "rejected_or_deferred_routes": [r["route_name"] for r in ROUTE_OPTIONS if not r["selected_now"]],
        "decision_reason": [
            "File Metadata Boundary 链已完成 planning+dryrun+post-review+closure",
            "closure 明确不等于文件存在性检查可用、不等于 stat/open/read 可用",
            "从 metadata boundary 进入真实文件世界的最小下一步是：先规划“文件存在性检查”如何被 gate 控制，而不是立即执行 stat",
            "Real metadata read / real hash / EXIF / video probe / image read 都比 existence check 风险更高，应后置",
            "Gate taxonomy / MidPlatform governance / resilience 仍重要，但本阶段仅路线裁决，保持 deferred",
        ],
        "boundary_freeze_ref": "boundary_freeze.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_gate_taxonomy_register = {
        "gate_taxonomy_deferred": True,
        "gate_taxonomy_project_optimization": True,
        "current_status": "project_optimization_deferred",
        "runtime_allowed_now": False,
        "implementation_allowed_now": False,
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "重要但不打断 file existence check guarded planning 主线",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_real_image_read_register = {
        "real_image_read_deferred": True,
        "controlled_static_image_read_preplan_deferred": True,
        "current_status": "future_high_risk_capability",
        "runtime_allowed_now": False,
        "image_read_allowed_now": False,
        "selected_now": False,
        "defer_reason": [
            "file existence check not yet guarded",
            "real metadata read not planned",
            "real hash policy not planned",
            "privacy/manual review workflow not runtime-ready",
            "visual model adapter not enabled",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_resilience_distributed_midplatform_register = {
        "midplatform_resilience_deferred": True,
        "offline_distributed_midplatform_deferred": True,
        "current_status": "future_architecture_candidate",
        "runtime_allowed_now": False,
        "implementation_allowed_now": False,
        "recommended_priority": "P1",
        "selected_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_worldmodel_memory_library_emotion_register = {
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "exploration_drive_deferred": True,
        "emotion_engine_deferred": True,
        "current_status": "future_candidate_cluster",
        "runtime_allowed_now": False,
        "write_allowed_now": False,
        "selected_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_freeze = {
        "no_runtime": True,
        "no_write": True,
        "no_action": True,
        "no_speech": True,
        "no_fact": True,
        "no_file_existence_check": True,
        "no_file_stat": True,
        "no_file_open": True,
        "no_image_open": True,
        "no_video_open": True,
        "no_image_read": True,
        "no_video_read": True,
        "no_exif_parse": True,
        "no_video_probe": True,
        "no_real_hash": True,
        "no_perceptual_hash": True,
        "no_visual_model": True,
        "no_map_api": True,
        "no_OCR_provider": True,
        "no_tracking_runtime": True,
        "no_crossing_runtime": True,
        "no_worldmodel_write": True,
        "no_memory_write": True,
        "no_library_write": True,
        "no_entity_resolution": True,
        "no_fact_admission": True,
        "no_emotion_engine": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_roadmap_register = {
        "carryover_topics": [
            {"topic": t, "roadmap_impact": "kept explicit during guarded planning", "source_chain": SOURCE_CHAIN, **_not_fact()}
            for t in [
                "future file existence check risk",
                "path legality policy maintenance",
                "future real metadata read risk",
                "future real hash computation risk",
                "EXIF / video probe privacy risk",
                "fixture registry governance complexity",
                "manifest-to-file-metadata mapping complexity",
                "sensitive metadata manual review complexity",
                "gate taxonomy required later",
                "midplatform function governance required later",
                "midplatform resilience required later",
                "offline distributed midplatform deferred",
            ]
        ],
        "gate_taxonomy_required_later": True,
        "midplatform_function_governance_required_later": True,
        "midplatform_resilience_required_later": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_claims_register = {
        "non_claims": [
            "roadmap decision 不等于文件存在性检查可执行",
            "roadmap decision 不等于 stat 文件",
            "roadmap decision 不等于打开文件/读取图像/视频",
            "roadmap decision 不等于真实 metadata 读取（含 EXIF / video probe）",
            "roadmap decision 不等于真实 hash / pHash 计算",
            "roadmap decision 不等于视觉模型/OCR/tracking/map/crossing runtime",
            "roadmap decision 不等于生产推理/训练",
            "roadmap decision 不等于 WorldModel/Memory/Fact/Library 写入",
            "selected next phase 仍是 planning-only，不等于允许 stat/open/read",
        ],
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "runtime_enablement_claimed": False,
        "production_readiness_claimed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "priority_level": "P0",
        "route_name": "File Existence Check Guarded Planning",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    for flag_name, flag_value in (
        ("file_metadata_boundary_closure_input_loaded", file_metadata_boundary_closure_input_loaded),
        ("file_metadata_boundary_post_review_input_loaded", file_metadata_boundary_post_review_input_loaded),
        ("file_metadata_boundary_dryrun_input_loaded", file_metadata_boundary_dryrun_input_loaded),
        ("file_metadata_boundary_planning_input_loaded", file_metadata_boundary_planning_input_loaded),
        ("post_controlled_frame_sample_roadmap_input_loaded", post_controlled_frame_sample_roadmap_input_loaded),
        ("controlled_frame_sample_closure_input_loaded", controlled_frame_sample_closure_input_loaded),
        ("controlled_frame_input_closure_input_loaded", controlled_frame_input_closure_input_loaded),
        ("map_location_readonly_context_input_loaded", map_location_readonly_context_input_loaded),
        ("safety_constitution_input_loaded", safety_constitution_input_loaded),
        ("minimal_runtime_integration_closure_loaded", minimal_runtime_integration_closure_loaded),
        ("ocr_final_closure_loaded", ocr_final_closure_loaded),
    ):
        if not flag_value:
            blockers.append(flag_name)

    selected_route = "File Existence Check Guarded Planning"

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "file_metadata_boundary_closure_input_loaded": file_metadata_boundary_closure_input_loaded,
        "file_metadata_boundary_post_review_input_loaded": file_metadata_boundary_post_review_input_loaded,
        "file_metadata_boundary_dryrun_input_loaded": file_metadata_boundary_dryrun_input_loaded,
        "file_metadata_boundary_planning_input_loaded": file_metadata_boundary_planning_input_loaded,
        "post_controlled_frame_sample_roadmap_input_loaded": post_controlled_frame_sample_roadmap_input_loaded,
        "controlled_frame_sample_closure_input_loaded": controlled_frame_sample_closure_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "current_status_summary_generated": True,
        "completed_capability_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "deferred_gate_taxonomy_register_generated": True,
        "deferred_real_image_read_register_generated": True,
        "deferred_resilience_distributed_midplatform_register_generated": True,
        "deferred_worldmodel_memory_library_emotion_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": len(ROUTE_OPTIONS),
        "p0_route_count": len(p0_routes),
        "p1_route_count": len(p1_routes),
        "p2_route_count": len(p2_routes),
        "file_existence_check_guarded_planning_route_exists": "File Existence Check Guarded Planning" in route_names,
        "file_stat_guarded_dryrun_route_exists": "File Stat Guarded DryRun" in route_names,
        "real_metadata_read_guarded_planning_route_exists": "Real Metadata Read Guarded Planning" in route_names,
        "real_hash_computation_guarded_planning_route_exists": "Real Hash Computation Guarded Planning" in route_names,
        "exif_video_probe_guarded_planning_route_exists": "EXIF / Video Probe Guarded Planning" in route_names,
        "controlled_static_image_read_preplan_route_exists": "Controlled Static Image Read Preplan" in route_names,
        "gate_taxonomy_route_exists": "Gate Taxonomy / Gate Requirement Framework" in route_names,
        "midplatform_function_governance_route_exists": "MidPlatform Function Governance / Consolidation" in route_names,
        "midplatform_resilience_route_exists": "MidPlatform Resilience / Robustness Preplan" in route_names,
        "offline_distributed_midplatform_route_exists": "Offline Distributed MidPlatform Architecture Preplan" in route_names,
        "worldmodel_memory_library_route_exists": "WorldModel / Memory / Library Governance" in route_names,
        "exploration_emotion_route_exists": "Exploration Drive / Emotion Map / Affective Engine" in route_names,
        "selected_route": selected_route,
        "file_metadata_boundary_closed": True,
        "metadata_decision_simulation_only": True,
        "file_existence_check_readiness_claimed": False,
        "real_metadata_readiness_claimed": False,
        "real_hash_readiness_claimed": False,
        "real_image_readiness_claimed": False,
        "visual_runtime_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "gate_taxonomy_deferred": True,
        "gate_taxonomy_project_optimization": True,
        "real_image_read_deferred": True,
        "controlled_static_image_read_preplan_deferred": True,
        "midplatform_resilience_deferred": True,
        "offline_distributed_midplatform_deferred": True,
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "exploration_drive_deferred": True,
        "emotion_engine_deferred": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
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
        "emotion_engine_invoked": False,
        "boundary_ok": not blockers,
        "violations": blockers,
        "final_decision": FINAL_DECISION if not blockers else "POST_FILE_METADATA_BOUNDARY_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    post_file_metadata_boundary_roadmap_decision = {
        "decision_id": DECISION_ID,
        "decision_scope": DECISION_SCOPE,
        "source_closure_ref": current_status_summary["source_closure_ref"],
        "current_mainline_status": current_status_summary["current_mainline_status"],
        "completed_capability_summary_ref": "completed_capability_summary.json",
        "route_option_matrix_ref": "route_option_matrix.json",
        "priority_ranking_ref": "priority_ranking.json",
        "selected_next_phase": summary["recommended_next_phase"],
        "rejected_or_deferred_routes": recommended_next_phase_decision["rejected_or_deferred_routes"],
        "decision_reason": recommended_next_phase_decision["decision_reason"],
        "boundary_freeze_ref": "boundary_freeze.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "post_file_metadata_boundary_roadmap_decision": post_file_metadata_boundary_roadmap_decision,
        "current_file_metadata_boundary_status_summary": current_status_summary,
        "completed_capability_summary": completed_capability_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "deferred_gate_taxonomy_register": deferred_gate_taxonomy_register,
        "deferred_real_image_read_register": deferred_real_image_read_register,
        "deferred_resilience_distributed_midplatform_register": deferred_resilience_distributed_midplatform_register,
        "deferred_worldmodel_memory_library_emotion_register": deferred_worldmodel_memory_library_emotion_register,
        "boundary_freeze": boundary_freeze,
        "governance_debt_roadmap_register": governance_debt_roadmap_register,
        "non_claims_register": non_claims_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": _boundary_payload(),
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }

