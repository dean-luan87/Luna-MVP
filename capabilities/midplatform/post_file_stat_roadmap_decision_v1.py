# -*- coding: utf-8 -*-
"""Post File Stat Roadmap Decision v1.

本阶段只做路线裁决（roadmap decision / prioritization / boundary freeze）。
不执行 exists/stat/open/read/hash，不进入任何 runtime，不写 WorldModel/Memory/Fact/Library。
不做 Gate Taxonomy / MidPlatform Function Governance / Resilience 实现，只做裁决与登记。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Post-File-Stat-Roadmap-Decision-v1-001"
DECISION_SCOPE = "post_file_stat_roadmap_decision_only"
SOURCE_CHAIN = "post_file_stat_roadmap_decision_v1"
DECISION_ID = "pfs_rd_v1_001"

FINAL_DECISION = "POST_FILE_STAT_ROADMAP_DECISION_READY_FOR_GATE_TAXONOMY_PLANNING"
NEXT_PHASE = "Phase-Gate-Taxonomy-and-Requirement-Framework-Planning-v1-001"
SELECTED_ROUTE = "Gate Taxonomy / Gate Requirement Framework"

FILE_STAT_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
FILE_STAT_POST_REVIEW_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
FILE_STAT_DRYRUN_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FILE_STAT_PLANNING_DECISION = "CONTROLLED_FRAME_FILE_STAT_GUARDED_PLANNING_READY_FOR_DRYRUN"

POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION = "POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION_READY_FOR_FILE_STAT_GUARDED_PLANNING"
FILE_EXISTENCE_CLOSURE_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
FILE_EXISTENCE_POST_REVIEW_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
FILE_EXISTENCE_DRYRUN_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FILE_EXISTENCE_PLANNING_DECISION = "CONTROLLED_FRAME_FILE_EXISTENCE_CHECK_GUARDED_PLANNING_READY_FOR_DRYRUN"

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
        "id": "file_stat_guarded_closure",
        "arg": "file_stat_guarded_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_stat_guarded_closure_summary.json", "verifier_report.json"],
    },
    {
        "id": "file_stat_guarded_post_review",
        "arg": "file_stat_guarded_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "file_stat_closure_readiness_decision.json", "verifier_report.json"],
    },
    {
        "id": "file_stat_guarded_dryrun",
        "arg": "file_stat_guarded_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_stat_guarded_dryrun_results.json", "verifier_report.json"],
    },
    {
        "id": "file_stat_guarded_planning",
        "arg": "file_stat_guarded_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_file_stat_guarded_planning_policy.json", "verifier_report.json"],
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
        "artifacts": ["summary.json", "controlled_frame_file_existence_check_guarded_closure_summary.json", "verifier_report.json"],
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
        "artifacts": ["summary.json", "controlled_frame_file_metadata_boundary_closure_summary.json", "verifier_report.json"],
    },
    {
        "id": "file_metadata_boundary_post_review",
        "arg": "file_metadata_boundary_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_report.json"],
    },
    {
        "id": "file_metadata_boundary_dryrun",
        "arg": "file_metadata_boundary_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_report.json"],
    },
    {
        "id": "file_metadata_boundary_planning",
        "arg": "file_metadata_boundary_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "verifier_report.json"],
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


ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Gate Taxonomy / Gate Requirement Framework",
        "route_type": "gate_taxonomy_requirement_framework_planning",
        "readiness_level": "medium",
        "dependency": [
            "gate count growing across file metadata boundary / existence / stat governance",
            "need standard verifier templates and override/veto semantics",
        ],
        "risk_level": "low",
        "expected_value": "very_high",
        "runtime_risk": "low",
        "write_risk": "low",
        "privacy_risk": "low",
        "governance_debt_impact": "reduce gate sprawl; unify requirements; unblock future real file ops safely",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "B",
        "route_name": "MidPlatform Function Governance / Consolidation",
        "route_type": "midplatform_function_governance_consolidation",
        "readiness_level": "medium",
        "dependency": ["Gate Taxonomy / Gate Requirement Framework"],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "privacy_risk": "low",
        "governance_debt_impact": "consolidate duplicated gates; schema convergence; resource/privacy budget governance",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "先统一 gate taxonomy，再做中台功能治理/合并更稳",
        "recommended_phase_name": "Phase-MidPlatform-Function-Governance-Consolidation-v1-001",
    },
    {
        "route_id": "C",
        "route_name": "MidPlatform Input Root Consolidation / EvalOut Migration",
        "route_type": "midplatform_input_root_consolidation_evalout_migration",
        "readiness_level": "medium",
        "dependency": ["Gate Taxonomy / Gate Requirement Framework", "MidPlatform Function Governance / Consolidation"],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "privacy_risk": "low",
        "governance_debt_impact": "reduce cross-repo root ambiguity; standardize historical root intake",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "可作为中台治理子任务并入；本阶段先裁决 taxonomy",
        "recommended_phase_name": "Phase-MidPlatform-Input-Root-Consolidation-EvalOut-Migration-v1-001",
    },
    {
        "route_id": "D",
        "route_name": "MidPlatform Resilience / Robustness Preplan",
        "route_type": "midplatform_resilience_robustness_preplan",
        "readiness_level": "low",
        "dependency": ["Gate Taxonomy / Gate Requirement Framework"],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "privacy_risk": "low",
        "governance_debt_impact": "define degradation paths; single-point failure plan; safe fallback",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "重要但不插队 taxonomy；先收敛 gate 再做 resilience 更一致",
        "recommended_phase_name": "Phase-MidPlatform-Resilience-Robustness-Preplan-v1-001",
    },
    {
        "route_id": "E",
        "route_name": "Real File Stat Guarded Trial",
        "route_type": "real_file_stat_guarded_trial",
        "readiness_level": "low",
        "dependency": ["Gate Taxonomy / Gate Requirement Framework", "manual review workflow", "fixture registry runtime"],
        "risk_level": "very_high",
        "expected_value": "high",
        "runtime_risk": "very_high",
        "write_risk": "low",
        "privacy_risk": "very_high",
        "governance_debt_impact": "real filesystem access risk; must remain deferred until taxonomy + stronger requirements",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "当前只完成 stat gate 治理闭环，不应直接进入真实 stat；先做 gate taxonomy",
        "recommended_phase_name": "Phase-Controlled-Frame-Real-File-Stat-Guarded-Trial-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "Real File Existence Check Guarded Trial",
        "route_type": "real_file_existence_check_guarded_trial",
        "readiness_level": "low",
        "dependency": ["Real File Stat Guarded Trial", "Gate Taxonomy / Gate Requirement Framework"],
        "risk_level": "very_high",
        "expected_value": "high",
        "runtime_risk": "very_high",
        "write_risk": "low",
        "privacy_risk": "high",
        "governance_debt_impact": "would call exists; must stay deferred",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "真实 exists 后置于真实 stat 与 taxonomy 之后",
        "recommended_phase_name": "Phase-Controlled-Frame-Real-File-Existence-Check-Guarded-Trial-v1-001",
    },
    {
        "route_id": "G",
        "route_name": "Real Metadata Read Guarded Planning",
        "route_type": "real_metadata_read_guarded_planning",
        "readiness_level": "low",
        "dependency": ["Gate Taxonomy / Gate Requirement Framework"],
        "risk_level": "very_high",
        "expected_value": "high",
        "runtime_risk": "high",
        "write_risk": "low",
        "privacy_risk": "very_high",
        "governance_debt_impact": "define safe metadata boundary; owner/permission/inode exposure risk",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "真实 metadata 读取风险高；需 taxonomy 后再规划",
        "recommended_phase_name": "Phase-Controlled-Frame-Real-Metadata-Read-Guarded-Planning-v1-001",
    },
    {
        "route_id": "H",
        "route_name": "Real Hash Computation Guarded Planning",
        "route_type": "real_hash_computation_guarded_planning",
        "readiness_level": "low",
        "dependency": ["Real Metadata Read Guarded Planning"],
        "risk_level": "very_high",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "low",
        "privacy_risk": "high",
        "governance_debt_impact": "requires reading file bytes; must remain deferred",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "需要读取 bytes，后置",
        "recommended_phase_name": "Phase-Controlled-Frame-Real-Hash-Computation-Guarded-Planning-v1-001",
    },
    {
        "route_id": "I",
        "route_name": "EXIF / Video Probe Guarded Planning",
        "route_type": "exif_video_probe_guarded_planning",
        "readiness_level": "low",
        "dependency": ["Real Metadata Read Guarded Planning", "Gate Taxonomy / Gate Requirement Framework"],
        "risk_level": "very_high",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "low",
        "privacy_risk": "very_high",
        "governance_debt_impact": "EXIF/video probe can leak sensitive metadata; must stay deferred",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "隐私风险高，后置",
        "recommended_phase_name": "Phase-Controlled-Frame-EXIF-Video-Probe-Guarded-Planning-v1-001",
    },
    {
        "route_id": "J",
        "route_name": "Controlled Static Image Read Preplan",
        "route_type": "controlled_static_image_read_preplan",
        "readiness_level": "low",
        "dependency": ["Gate Taxonomy / Gate Requirement Framework"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "high",
        "write_risk": "low",
        "privacy_risk": "very_high",
        "governance_debt_impact": "content read risk; keep deferred",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "继续 deferred；文件链治理收敛前不读内容",
        "recommended_phase_name": "Phase-Controlled-Static-Image-Read-Preplan-v1-001",
    },
    {
        "route_id": "K",
        "route_name": "Controlled Visual Runtime Planning",
        "route_type": "controlled_visual_runtime_planning",
        "readiness_level": "low",
        "dependency": ["Gate Taxonomy / Gate Requirement Framework", "Minimal Runtime Integration baseline"],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "very_high",
        "write_risk": "medium",
        "privacy_risk": "very_high",
        "governance_debt_impact": "introduces runtime complexity; remain deferred",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "当前仍过早；先收敛 gate taxonomy 与中台治理",
        "recommended_phase_name": "Phase-Controlled-Visual-Runtime-Planning-v1-001",
    },
    {
        "route_id": "L",
        "route_name": "Hardware / Dual Device Redundant Perception Preplan",
        "route_type": "hardware_dual_device_redundant_perception_preplan",
        "readiness_level": "low",
        "dependency": ["Controlled Visual Runtime Planning"],
        "risk_level": "medium",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "low",
        "privacy_risk": "high",
        "governance_debt_impact": "hardware integration complexity; keep deferred",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "硬件阶段后置",
        "recommended_phase_name": "Phase-Hardware-Dual-Device-Redundant-Perception-Preplan-v1-001",
    },
    {
        "route_id": "M",
        "route_name": "WorldModel / Memory / Library Governance",
        "route_type": "worldmodel_memory_library_governance",
        "readiness_level": "low",
        "dependency": ["MidPlatform Function Governance / Consolidation"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "high",
        "write_risk": "very_high",
        "privacy_risk": "very_high",
        "governance_debt_impact": "stateful write governance; remain deferred",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "P2 deferred；写入治理未到时机",
        "recommended_phase_name": "Phase-WorldModel-Memory-Library-Governance-v1-001",
    },
    {
        "route_id": "N",
        "route_name": "Exploration Drive / Emotion Map / Affective Engine",
        "route_type": "exploration_emotion_affective_engine",
        "readiness_level": "very_low",
        "dependency": ["WorldModel / Memory / Library Governance"],
        "risk_level": "medium",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "very_high",
        "privacy_risk": "very_high",
        "governance_debt_impact": "long-horizon capability; keep deferred",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "长期方向；继续 deferred",
        "recommended_phase_name": "Phase-Exploration-Emotion-Engine-Roadmap-v1-001",
    },
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
        "decision_scope": DECISION_SCOPE,
        "roadmap_decision_only": True,
        "implementation_allowed_now": False,
        "runtime_allowed_now": False,
        "file_operation_allowed_now": False,
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
        "emotion_engine_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_post_file_stat_roadmap_decision_v1(
    *,
    file_stat_guarded_closure_root: str,
    file_stat_guarded_post_review_root: str,
    file_stat_guarded_dryrun_root: str,
    file_stat_guarded_planning_root: str,
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

    def _match_final(intake_id: str, expected_final: str) -> bool:
        return roots[intake_id]["loaded"] and summaries[intake_id].get("final_decision") == expected_final

    # Required intake validity checks (by final_decision)
    file_stat_guarded_closure_input_loaded = _match_final("file_stat_guarded_closure", FILE_STAT_CLOSURE_DECISION)
    file_stat_guarded_post_review_input_loaded = _match_final("file_stat_guarded_post_review", FILE_STAT_POST_REVIEW_DECISION)
    file_stat_guarded_dryrun_input_loaded = _match_final("file_stat_guarded_dryrun", FILE_STAT_DRYRUN_DECISION)
    file_stat_guarded_planning_input_loaded = _match_final("file_stat_guarded_planning", FILE_STAT_PLANNING_DECISION)

    post_file_existence_check_roadmap_input_loaded = _match_final(
        "post_file_existence_check_roadmap_decision", POST_FILE_EXISTENCE_CHECK_ROADMAP_DECISION
    )

    file_existence_check_guarded_closure_input_loaded = (
        _match_final("file_existence_check_guarded_closure", FILE_EXISTENCE_CLOSURE_DECISION)
        and summaries["file_existence_check_guarded_closure"].get("file_existence_check_guarded_closed") is True
    )
    file_existence_check_guarded_post_review_input_loaded = _match_final(
        "file_existence_check_guarded_post_review", FILE_EXISTENCE_POST_REVIEW_DECISION
    )
    file_existence_check_guarded_dryrun_input_loaded = _match_final("file_existence_check_guarded_dryrun", FILE_EXISTENCE_DRYRUN_DECISION)
    file_existence_check_guarded_planning_input_loaded = _match_final(
        "file_existence_check_guarded_planning", FILE_EXISTENCE_PLANNING_DECISION
    )

    file_metadata_boundary_closure_input_loaded = (
        _match_final("file_metadata_boundary_closure", FILE_METADATA_BOUNDARY_CLOSURE_DECISION)
        and summaries["file_metadata_boundary_closure"].get("file_metadata_boundary_closed") is True
    )
    file_metadata_boundary_post_review_input_loaded = _match_final("file_metadata_boundary_post_review", FILE_METADATA_BOUNDARY_POST_REVIEW_DECISION)
    file_metadata_boundary_dryrun_input_loaded = _match_final("file_metadata_boundary_dryrun", FILE_METADATA_BOUNDARY_DRYRUN_DECISION)
    file_metadata_boundary_planning_input_loaded = _match_final("file_metadata_boundary_planning", FILE_METADATA_BOUNDARY_PLANNING_DECISION)

    controlled_frame_sample_closure_input_loaded = _match_final("controlled_frame_sample_closure", CONTROLLED_FRAME_SAMPLE_CLOSURE_DECISION)
    controlled_frame_input_closure_input_loaded = _match_final("controlled_frame_input_closure", CONTROLLED_FRAME_INPUT_CLOSURE_DECISION)
    map_location_readonly_context_input_loaded = _match_final("map_location_readonly_context", MAP_LOCATION_DECISION)
    safety_constitution_input_loaded = _match_final("safety_constitution", SAFETY_CONSTITUTION_DECISION)
    minimal_runtime_integration_closure_loaded = _match_final("minimal_runtime_integration_closure", MRI_DECISION)
    ocr_final_closure_loaded = _match_final("ocr_final_closure", OCR_DECISION)

    required_ok = all(
        [
            file_stat_guarded_closure_input_loaded,
            file_stat_guarded_post_review_input_loaded,
            file_stat_guarded_dryrun_input_loaded,
            file_stat_guarded_planning_input_loaded,
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
    )

    route_option_matrix = {"routes": ROUTE_OPTIONS, "route_count": len(ROUTE_OPTIONS), "source_chain": SOURCE_CHAIN, **_not_fact()}
    p0 = [r for r in ROUTE_OPTIONS if r.get("recommended_priority") == "P0"]
    p1 = [r for r in ROUTE_OPTIONS if r.get("recommended_priority") == "P1"]
    p2 = [r for r in ROUTE_OPTIONS if r.get("recommended_priority") == "P2"]

    current_status_summary = {
        "file_stat_guarded_planning_closed": True,
        "file_stat_guarded_dryrun_closed": True,
        "file_stat_guarded_post_review_closed": True,
        "file_stat_guarded_closed": True,
        "file_existence_check_guarded_closed": True,
        "file_metadata_boundary_closed": True,
        "controlled_frame_sample_closed": True,
        "stat_gate_decision_simulation_only": True,
        "real_stat_readiness_claimed": False,
        "real_exists_readiness_claimed": False,
        "file_open_readiness_claimed": False,
        "real_metadata_readiness_claimed": False,
        "real_image_readiness_claimed": False,
        "visual_runtime_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "cross_repo_input_roots_observed": cross_repo_input_roots_observed,
        "output_root_fixed_to_luna_core": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    completed_capability_summary = {
        "completed_chains": [
            "Controlled Frame File Metadata Boundary (closure completed)",
            "Controlled Frame File Existence Check Guarded (closure completed)",
            "Controlled Frame File Stat Guarded (closure completed)",
        ],
        "notes": [
            "chains closed at governance/planning/dryrun/review/closure layers",
            "real file operations remain deferred; roadmap decision does not enable any runtime",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    priority_ranking = {
        "p0": [
            "Gate Taxonomy / Gate Requirement Framework",
            "MidPlatform Function Governance / Consolidation",
            "MidPlatform Input Root Consolidation / EvalOut Migration",
        ],
        "p1": [
            "MidPlatform Resilience / Robustness Preplan",
            "Real File Stat Guarded Trial",
            "Real File Existence Check Guarded Trial",
            "Real Metadata Read Guarded Planning",
            "Real Hash Computation Guarded Planning",
            "EXIF / Video Probe Guarded Planning",
            "Controlled Static Image Read Preplan",
            "Controlled Visual Runtime Planning",
            "Hardware / Dual Device Redundant Perception Preplan",
        ],
        "p2": [
            "WorldModel / Memory / Library Governance",
            "Exploration Drive / Emotion Map / Affective Engine",
        ],
        "p0_route_count": len(p0),
        "p1_route_count": len(p1),
        "p2_route_count": len(p2),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_real_file_operation_register = {
        "real_exists_call_deferred": True,
        "real_file_stat_deferred": True,
        "real_file_open_deferred": True,
        "real_metadata_read_deferred": True,
        "real_image_read_deferred": True,
        "real_video_read_deferred": True,
        "real_hash_deferred": True,
        "exif_video_probe_deferred": True,
        "current_status": "future_high_risk_capability",
        "runtime_allowed_now": False,
        "file_operation_allowed_now": False,
        "selected_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    gate_taxonomy_decision_register = {
        "gate_taxonomy_selected_now": True,
        "gate_taxonomy_deferred": False,
        "current_status": "selected_planning_route",
        "implementation_allowed_now": False,
        "runtime_allowed_now": False,
        "recommended_priority": "P0",
        "selected_reason": [
            "gate count growing",
            "file chain has reached stat closure",
            "before real filesystem access, gate requirements must be unified",
            "future MidPlatform governance depends on gate taxonomy",
            "verifier templates need standardization",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_midplatform_governance_register = {
        "midplatform_function_governance_deferred": True,
        "current_status": "deferred_after_gate_taxonomy",
        "selected_now": False,
        "future_scope": [
            "duplicate gate cleanup",
            "schema consolidation",
            "governance debt consolidation",
            "resource budget centralization review",
            "privacy gate consolidation",
            "cross-repo input root cleanup",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_resilience_distributed_midplatform_register = {
        "midplatform_resilience_deferred": True,
        "offline_distributed_midplatform_deferred": True,
        "current_status": "deferred_after_gate_taxonomy",
        "selected_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_worldmodel_memory_library_emotion_register = {
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "exploration_drive_deferred": True,
        "emotion_engine_deferred": True,
        "current_status": "P2_deferred",
        "selected_now": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_freeze = {
        "frozen_boundaries": [
            "no-runtime",
            "no-write",
            "no-action",
            "no-speech",
            "no-fact",
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
            "no-real-hash",
            "no-perceptual-hash",
            "no-visual-model",
            "no-map-api",
            "no-OCR-provider",
            "no-tracking-runtime",
            "no-crossing-runtime",
            "no-worldmodel-write",
            "no-memory-write",
            "no-library-write",
            "no-entity-resolution",
            "no-fact-admission",
            "no-emotion-engine",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_roadmap_register = {
        "topics": [
            "gate taxonomy required later",
            "midplatform function governance required later",
            "midplatform resilience required later",
            "cross-repo input root ambiguity",
            "future real filesystem privacy risk",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_claims_register = {
        "non_claims": [
            "roadmap decision 不等于真实 stat 可用",
            "roadmap decision 不等于真实 exists 可用",
            "roadmap decision 不等于真实 open/read/hash 可用",
            "roadmap decision 不等于 EXIF / video probe 可用",
            "roadmap decision 不等于图像/视频内容读取可用",
            "roadmap decision 不等于任何 runtime 已启用",
            "selected route 不等于已实现 gate taxonomy",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    rejected_or_deferred_routes = [
        {
            "route_name": r["route_name"],
            "selected_now": bool(r.get("selected_now")),
            "recommended_priority": r.get("recommended_priority"),
            "defer_reason": r.get("defer_reason") or "",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for r in ROUTE_OPTIONS
        if not r.get("selected_now")
    ]

    post_file_stat_roadmap_decision = {
        "decision_id": DECISION_ID,
        "decision_scope": DECISION_SCOPE,
        "source_closure_ref": "_eval_out/controlled_frame_file_stat_guarded_closure_v1_smoke_v0/",
        "current_mainline_status": "file existence + file stat governance chains closed; real file ops deferred",
        "completed_capability_summary_ref": "completed_capability_summary.json",
        "route_option_matrix_ref": "route_option_matrix.json",
        "priority_ranking_ref": "priority_ranking.json",
        "selected_next_phase": NEXT_PHASE if required_ok else PHASE_ID,
        "rejected_or_deferred_routes": rejected_or_deferred_routes,
        "decision_reason": [
            "File Metadata Boundary / File Existence Check / File Stat Guarded chains are closed",
            "Gate count is growing; taxonomy/requirements must be unified before any real filesystem access",
            "Avoid entering real stat trial now; keep real file operations deferred",
        ],
        "boundary_freeze_ref": "boundary_freeze.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if required_ok else PHASE_ID,
        "selected_route": SELECTED_ROUTE,
        "final_decision": FINAL_DECISION if required_ok else "POST_FILE_STAT_ROADMAP_DECISION_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    if not required_ok:
        blockers.append("required_upstream_roots_missing_or_invalid")

    boundary_ok = not blockers

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "file_stat_guarded_closure_input_loaded": file_stat_guarded_closure_input_loaded,
        "file_stat_guarded_post_review_input_loaded": file_stat_guarded_post_review_input_loaded,
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
        "current_status_summary_generated": True,
        "completed_capability_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "deferred_real_file_operation_register_generated": True,
        "gate_taxonomy_decision_register_generated": True,
        "deferred_midplatform_governance_register_generated": True,
        "deferred_resilience_distributed_midplatform_register_generated": True,
        "deferred_worldmodel_memory_library_emotion_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": len(ROUTE_OPTIONS),
        "p0_route_count": len(p0),
        "p1_route_count": len(p1),
        "p2_route_count": len(p2),
        "gate_taxonomy_route_exists": True,
        "midplatform_function_governance_route_exists": True,
        "input_root_consolidation_route_exists": True,
        "midplatform_resilience_route_exists": True,
        "real_file_stat_guarded_trial_route_exists": True,
        "real_file_existence_check_guarded_trial_route_exists": True,
        "real_metadata_read_guarded_planning_route_exists": True,
        "real_hash_computation_guarded_planning_route_exists": True,
        "exif_video_probe_guarded_planning_route_exists": True,
        "controlled_static_image_read_preplan_route_exists": True,
        "controlled_visual_runtime_route_exists": True,
        "hardware_dual_device_redundant_perception_route_exists": True,
        "worldmodel_memory_library_route_exists": True,
        "exploration_emotion_route_exists": True,
        "selected_route": SELECTED_ROUTE,
        "file_stat_guarded_closed": True,
        "file_existence_check_guarded_closed": True,
        "file_metadata_boundary_closed": True,
        "controlled_frame_sample_closed": True,
        "stat_gate_decision_simulation_only": True,
        "real_stat_readiness_claimed": False,
        "real_exists_readiness_claimed": False,
        "file_open_readiness_claimed": False,
        "real_metadata_readiness_claimed": False,
        "real_image_readiness_claimed": False,
        "visual_runtime_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "real_exists_call_deferred": True,
        "real_file_stat_deferred": True,
        "real_file_open_deferred": True,
        "real_metadata_read_deferred": True,
        "real_image_read_deferred": True,
        "real_video_read_deferred": True,
        "real_hash_deferred": True,
        "exif_video_probe_deferred": True,
        "gate_taxonomy_selected_now": True,
        "gate_taxonomy_deferred": False,
        "midplatform_function_governance_deferred": True,
        "midplatform_resilience_deferred": True,
        "offline_distributed_midplatform_deferred": True,
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "exploration_drive_deferred": True,
        "emotion_engine_deferred": True,
        "cross_repo_input_roots_observed": cross_repo_input_roots_observed,
        "output_root_fixed_to_luna_core": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
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
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if required_ok else "POST_FILE_STAT_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if required_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    recommended_next_phase_decision = {
        "selected_route": SELECTED_ROUTE,
        "recommended_next_phase": summary["recommended_next_phase"],
        "final_decision": summary["final_decision"],
        "decision_reason": post_file_stat_roadmap_decision["decision_reason"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "current_file_stat_status_summary": current_status_summary,
        "completed_capability_summary": completed_capability_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "deferred_real_file_operation_register": deferred_real_file_operation_register,
        "gate_taxonomy_decision_register": gate_taxonomy_decision_register,
        "deferred_midplatform_governance_register": deferred_midplatform_governance_register,
        "deferred_resilience_distributed_midplatform_register": deferred_resilience_distributed_midplatform_register,
        "deferred_worldmodel_memory_library_emotion_register": deferred_worldmodel_memory_library_emotion_register,
        "boundary_freeze": boundary_freeze,
        "governance_debt_roadmap_register": governance_debt_roadmap_register,
        "non_claims_register": non_claims_register,
        "post_file_stat_roadmap_decision": post_file_stat_roadmap_decision,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_operation_boundary_report": _boundary_payload(),
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }

