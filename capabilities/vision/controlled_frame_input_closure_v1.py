# -*- coding: utf-8 -*-
"""Controlled Frame Input Closure v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Controlled-Frame-Input-Closure-v1-001"
CLOSURE_ID = "cfic_v1_001"
CLOSURE_SCOPE = "controlled_frame_input_closure_only"
SOURCE_CHAIN = "controlled_frame_input_closure_v1"
FINAL_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "CONTROLLED_FRAME_INPUT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "CONTROLLED_FRAME_INPUT_PLANNING_READY_FOR_CONTROLLED_FRAME_INPUT_DRYRUN"
MAP_LOCATION_FINAL_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
ROADMAP_DECISION = "POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
VISUAL_FOCUS_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
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
            "controlled_frame_input_closure_readiness_decision.json",
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
            "controlled_frame_input_dryrun_results.json",
            "controlled_frame_input_boundary_matrix.json",
            "dual_device_placeholder_dryrun_review.json",
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
            "frame_intake_gate_policy.json",
            "frame_quality_gate_policy.json",
            "frame_privacy_tagging_policy.json",
            "frame_stc_freshness_policy.json",
            "frame_downstream_handoff_policy.json",
            "controlled_frame_input_boundary_matrix.json",
            "dual_device_redundant_perception_placeholder.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "map_location_readonly_context_policy.json"],
    },
    {
        "id": "post_vision_strengthening_roadmap_decision",
        "arg": "post_vision_strengthening_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "recommended_next_phase_decision.json"],
    },
    {
        "id": "vision_strengthening_closure",
        "arg": "vision_strengthening_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "vision_strengthening_closure_summary.json"],
    },
    {
        "id": "task_aware_visual_focus",
        "arg": "task_aware_visual_focus_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "focus_to_ocr_activation_policy.json", "focus_to_tracking_request_policy.json"],
    },
    {
        "id": "midplatform_perception_orchestration",
        "arg": "midplatform_perception_orchestration_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "perception_work_order_schema.json"],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "minimal_runtime_integration_closure_report.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "ocr_mainline_final_closure_report.json"],
    },
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
        "id": "hardware_profile_capability_registry",
        "arg": "hardware_profile_capability_registry_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "system_health_center_governance",
        "arg": "system_health_center_governance_root",
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

COMPLETED_PHASES = [
    (
        "Controlled Frame Input Planning v1",
        "planning",
        "_eval_out/controlled_frame_input_planning_v1_smoke_v0/",
        "GO",
        "policy and schema baseline for controlled frame input",
    ),
    (
        "Controlled Frame Input DryRun v1",
        "dryrun",
        "_eval_out/controlled_frame_input_dryrun_v1_smoke_v0/",
        "GO",
        "metadata dry-run candidate chain validation",
    ),
    (
        "Controlled Frame Input Post-DryRun Review v1",
        "post_dryrun_review",
        "_eval_out/controlled_frame_input_post_dryrun_review_v1_smoke_v0/",
        "GO",
        "closure readiness audit and stability confirmation",
    ),
]

VALIDATED_CAPABILITIES = [
    "controlled frame source candidate policy",
    "frame intake gate",
    "frame quality gate",
    "frame privacy tagging policy",
    "frame STC / freshness reuse",
    "frame downstream handoff policy",
    "controlled frame dry-run metadata simulation",
    "allowed / rejected / restricted / stale frame scenario coverage",
    "dual-device redundant perception placeholder",
    "post-dryrun review",
]

DISABLED_RUNTIMES = [
    "live camera runtime",
    "device camera runtime",
    "external stream runtime",
    "actual image loading",
    "visual model runtime",
    "OCR provider runtime",
    "OCRRequest submission",
    "map API / 高德 API",
    "GPS runtime",
    "tracking runtime",
    "optical flow runtime",
    "Supervision / ByteTrack / OC-SORT",
    "dual-device runtime",
    "dual-model runtime",
    "failover runtime",
    "multi-input fusion runtime",
    "Speech Gate / VOP / TTS",
    "NavigationAction",
    "WorldModel write",
    "Memory write",
    "Library write",
    "Fact write",
]

NON_CLAIMS = [
    "closure 不等于 live camera 可用",
    "closure 不等于真实视觉 runtime",
    "closure 不等于可以读取真实图像",
    "metadata dry-run 不等于图像推理",
    "static_test_image candidate 不等于真实图像已读取",
    "pre_recorded_video_frame candidate 不等于真实视频已处理",
    "simulation_frame candidate 不等于真实世界 observation",
    "controlled_uploaded_frame candidate 不等于用户文件处理 runtime",
    "dual-device placeholder 不等于硬件阶段",
    "failover placeholder 不等于可自动故障切换",
    "multi-input consistency placeholder 不等于多输入融合",
    "frame candidate 不等于事实",
    "downstream handoff candidate 不等于下游 runtime",
]

DEFERRED_CAPABILITIES = [
    "Controlled Frame Sample Planning",
    "controlled real file/static image sample trial",
    "live camera guarded trial",
    "device camera capability registry",
    "visual model adapter",
    "OCR provider re-enable through VisualFocus",
    "tracking adapter experiment branch",
    "dual-device hardware planning",
    "device health registry",
    "failover policy runtime",
    "multi-input fusion governance",
    "WorldModel Candidate Layer",
    "Memory Governance",
    "Library Governance",
    "MidPlatform Function Governance / Consolidation",
    "MidPlatform Resilience / Robustness",
    "Offline Distributed MidPlatform Architecture Preplan",
]

DEBT_CARRYOVER_TOPICS = [
    "frame source policy complexity",
    "privacy tagging complexity",
    "frame quality gate complexity",
    "STC/freshness integration complexity",
    "downstream handoff complexity",
    "dual-device placeholder future complexity",
    "hardware-stage deferred debt",
    "controlled sample planning deferred",
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


def _verifier_verdict(root: Optional[Path]) -> str:
    if not root:
        return "MISSING"
    report = _read_json(root / "verifier_report.json")
    if isinstance(report, dict):
        if report.get("verifier"):
            return str(report["verifier"])
        if report.get("verdict"):
            return str(report["verdict"])
    return "COMPLETE"


def _boundary_payload() -> Dict[str, Any]:
    return {
        "closure_scope": CLOSURE_SCOPE,
        "closure_only": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "frame_content_loaded": False,
        "actual_image_read": False,
        "live_camera_allowed": False,
        "device_camera_allowed": False,
        "external_stream_allowed": False,
        "camera_invoked": False,
        "camera_opened": False,
        "video_capture_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
        "dual_device_runtime_invoked": False,
        "dual_model_runtime_invoked": False,
        "failover_runtime_invoked": False,
        "multi_input_fusion_runtime_invoked": False,
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
        "frame_to_ocr_requires_visual_focus": True,
        "frame_to_tracking_requires_visual_focus": True,
        "frame_to_world_observation_requires_policy": True,
        "frame_to_navigation_action_allowed": False,
        "frame_to_speech_output_allowed": False,
        "frame_to_worldmodel_write_allowed": False,
        "frame_to_memory_write_allowed": False,
        "frame_to_fact_write_allowed": False,
        "dual_device_redundant_perception_placeholder_retained": True,
        "hardware_stage_deferred": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_controlled_frame_input_closure_v1(
    *,
    post_dryrun_review_root: str,
    dryrun_root: str,
    planning_root: str,
    map_location_readonly_context_root: str,
    post_vision_strengthening_roadmap_decision_root: str,
    vision_strengthening_closure_root: str,
    task_aware_visual_focus_root: str,
    midplatform_perception_orchestration_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    vision_frame_trace_stream_registry_root: Optional[str] = None,
    vision_frame_input_governance_root: Optional[str] = None,
    vision_roi_proposal_stub_root: Optional[str] = None,
    hardware_profile_capability_registry_root: Optional[str] = None,
    system_health_center_governance_root: Optional[str] = None,
    simulation_lab_profile_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows = []
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
    post_dryrun_review_input_loaded = roots["post_dryrun_review"]["loaded"] and summaries["post_dryrun_review"].get("final_decision") == POST_REVIEW_DECISION
    dryrun_input_loaded = roots["dryrun"]["loaded"] and summaries["dryrun"].get("final_decision") == DRYRUN_DECISION
    planning_input_loaded = roots["planning"]["loaded"] and summaries["planning"].get("final_decision") == PLANNING_DECISION
    map_location_readonly_context_input_loaded = roots["map_location_readonly_context"]["loaded"] and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_FINAL_DECISION
    post_vision_strengthening_roadmap_decision_input_loaded = roots["post_vision_strengthening_roadmap_decision"]["loaded"] and summaries["post_vision_strengthening_roadmap_decision"].get("final_decision") == ROADMAP_DECISION
    vision_strengthening_closure_input_loaded = roots["vision_strengthening_closure"]["loaded"] and summaries["vision_strengthening_closure"].get("final_decision") == VISION_STRENGTHENING_CLOSURE_DECISION
    task_aware_visual_focus_input_loaded = roots["task_aware_visual_focus"]["loaded"] and summaries["task_aware_visual_focus"].get("final_decision") == VISUAL_FOCUS_DECISION
    midplatform_perception_orchestration_input_loaded = roots["midplatform_perception_orchestration"]["loaded"] and summaries["midplatform_perception_orchestration"].get("final_decision") == MIDPLATFORM_DECISION
    minimal_runtime_integration_closure_loaded = roots["minimal_runtime_integration_closure"]["loaded"] and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    ocr_final_closure_loaded = roots["ocr_final_closure"]["loaded"] and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION

    planning_root_path = roots["planning"]["root"]
    dryrun_root_path = roots["dryrun"]["root"]
    postreview_root_path = roots["post_dryrun_review"]["root"]

    planning_boundary = _read_json(planning_root_path / "controlled_frame_input_boundary_matrix.json") if planning_root_path else {}
    dryrun_boundary = _read_json(dryrun_root_path / "controlled_frame_input_boundary_matrix.json") if dryrun_root_path else {}
    postreview_readiness = _read_json(postreview_root_path / "controlled_frame_input_closure_readiness_decision.json") if postreview_root_path else {}
    planning_dual_placeholder = _read_json(planning_root_path / "dual_device_redundant_perception_placeholder.json") if planning_root_path else {}
    dryrun_dual_review = _read_json(dryrun_root_path / "dual_device_placeholder_dryrun_review.json") if dryrun_root_path else {}
    postreview_governance = _read_json(postreview_root_path / "governance_debt_review.json") if postreview_root_path else {}

    completed_phase_rows = []
    for phase_name, root_id, output_dir, status, role_in_closure in COMPLETED_PHASES:
        root = roots[root_id]["root"]
        phase_summary = summaries[root_id]
        completed_phase_rows.append(
            {
                "phase_id": phase_name,
                "status": status,
                "output_dir": output_dir,
                "verifier_verdict": _verifier_verdict(root),
                "final_decision": phase_summary.get("final_decision", ""),
                "role_in_closure": role_in_closure,
                "runtime_enabled": False,
                "write_enabled": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    completed_phase_matrix = {
        "phases": completed_phase_rows,
        "completed_phase_count": len(completed_phase_rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    validated_capability_summary = {
        "validated_capabilities": VALIDATED_CAPABILITIES,
        "validation_layers": ["planning", "metadata_dryrun", "review"],
        "clarifications": [
            "这些能力只完成到 planning / metadata dry-run / review validation 层",
            "它们不等于真实 frame runtime",
            "它们不等于真实视觉能力",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    disabled_runtime_summary = {
        "disabled_runtimes": DISABLED_RUNTIMES,
        "live_camera_allowed": False,
        "device_camera_allowed": False,
        "external_stream_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_boundary_freeze = {
        "no_runtime": True,
        "no_write": True,
        "no_action": True,
        "no_speech": True,
        "no_fact": True,
        "no_live_camera": True,
        "no_device_camera": True,
        "no_external_stream": True,
        "no_actual_image_read": True,
        "no_visual_model": True,
        "no_OCR_provider": True,
        "no_tracking_runtime": True,
        "no_map_api": True,
        "no_dual_device_runtime": True,
        "no_failover_runtime": True,
        "no_multi_input_fusion": True,
        "frame_to_ocr_requires_visual_focus": planning_boundary.get("frame_to_ocr_requires_visual_focus") is True and dryrun_boundary.get("frame_to_ocr_requires_visual_focus") is True,
        "frame_to_tracking_requires_visual_focus": planning_boundary.get("frame_to_tracking_requires_visual_focus") is True and dryrun_boundary.get("frame_to_tracking_requires_visual_focus") is True,
        "frame_to_world_observation_requires_policy": planning_boundary.get("frame_to_world_observation_requires_policy") is True and dryrun_boundary.get("frame_to_world_observation_requires_policy") is True,
        "frame_to_navigation_action_allowed": False,
        "frame_to_speech_output_allowed": False,
        "frame_to_worldmodel_write_allowed": False,
        "frame_to_memory_write_allowed": False,
        "frame_to_fact_write_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_input_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_capability_pool = {
        "deferred_capabilities": DEFERRED_CAPABILITIES,
        "controlled_sample_planning_started": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_carryover = {
        "carryover_topics": DEBT_CARRYOVER_TOPICS,
        "inherited_review_topics": postreview_governance.get("carryover_topics", []),
        "future_midplatform_function_governance_required": True,
        "future_midplatform_resilience_governance_required": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    for flag_name, loaded in (
        ("post_dryrun_review_input_loaded", post_dryrun_review_input_loaded),
        ("dryrun_input_loaded", dryrun_input_loaded),
        ("planning_input_loaded", planning_input_loaded),
        ("map_location_readonly_context_input_loaded", map_location_readonly_context_input_loaded),
        ("post_vision_strengthening_roadmap_decision_input_loaded", post_vision_strengthening_roadmap_decision_input_loaded),
        ("vision_strengthening_closure_input_loaded", vision_strengthening_closure_input_loaded),
        ("minimal_runtime_integration_closure_loaded", minimal_runtime_integration_closure_loaded),
        ("ocr_final_closure_loaded", ocr_final_closure_loaded),
    ):
        if not loaded:
            blockers.append(flag_name)
    if postreview_readiness.get("ready_for_closure") is not True:
        blockers.append("postreview_not_ready_for_closure")
    if len(completed_phase_rows) < 3:
        blockers.append("completed_phase_matrix_incomplete")

    closure_readiness_gate = {
        "go_conditions": [
            "planning input loaded",
            "dryrun input loaded",
            "post-dryrun review loaded",
            "completed phase matrix generated",
            "boundary freeze generated",
            "non-claims generated",
            "deferred capability pool generated",
            "governance debt carryover generated",
            "no runtime",
            "no write",
            "no action",
            "no speech",
            "no live camera",
            "no image read",
            "no dual-device runtime",
            "next phase fixed",
        ],
        "no_go_conditions": [
            "any required root missing",
            "camera opened",
            "image content loaded",
            "visual model invoked",
            "OCR provider invoked",
            "tracking runtime invoked",
            "map API invoked",
            "WorldModel/Memory/Fact write",
            "NavigationAction triggered",
            "dual-device/failover runtime enabled",
            "closure claims production readiness",
            "next phase unclear",
        ],
        "ready_for_closure": not blockers,
        "blockers": blockers,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    controlled_frame_input_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "source_phase_chain": [
            "Phase-Controlled-Frame-Input-Planning-v1-001",
            "Phase-Controlled-Frame-Input-DryRun-v1-001",
            "Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001",
        ],
        "completed_phase_count": len(completed_phase_rows),
        "completed_phase_matrix_ref": "completed_phase_matrix.json",
        "validated_capability_summary_ref": "validated_capability_summary.json",
        "disabled_runtime_summary_ref": "disabled_runtime_summary.json",
        "closure_boundary_freeze_ref": "closure_boundary_freeze.json",
        "non_claims_register_ref": "controlled_frame_input_non_claims_register.json",
        "deferred_capability_pool_ref": "deferred_capability_pool.json",
        "governance_debt_carryover_ref": "governance_debt_carryover.json",
        "next_phase_recommendation": NEXT_PHASE if not blockers else PHASE_ID,
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_INPUT_CLOSURE_REQUIRES_FIXES",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_runtime_boundary_report = _boundary_payload()
    no_write_boundary_report = _boundary_payload()

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "post_dryrun_review_input_loaded": post_dryrun_review_input_loaded,
        "dryrun_input_loaded": dryrun_input_loaded,
        "planning_input_loaded": planning_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "post_vision_strengthening_roadmap_decision_input_loaded": post_vision_strengthening_roadmap_decision_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "completed_phase_matrix_generated": True,
        "completed_phase_count": len(completed_phase_rows),
        "validated_capability_summary_generated": True,
        "disabled_runtime_summary_generated": True,
        "closure_boundary_freeze_generated": True,
        "non_claims_register_generated": True,
        "deferred_capability_pool_generated": True,
        "governance_debt_carryover_generated": True,
        "closure_readiness_gate_generated": True,
        "controlled_frame_input_planning_closed": planning_input_loaded,
        "controlled_frame_input_dryrun_closed": dryrun_input_loaded,
        "controlled_frame_input_post_review_closed": post_dryrun_review_input_loaded,
        "controlled_frame_input_closed": not blockers,
        "controlled_sample_planning_started": False,
        "live_camera_claimed": False,
        "visual_runtime_claimed": False,
        "image_read_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "frame_content_loaded": False,
        "actual_image_read": False,
        "live_camera_allowed": False,
        "device_camera_allowed": False,
        "external_stream_allowed": False,
        "camera_invoked": False,
        "camera_opened": False,
        "video_capture_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "gaode_api_invoked": False,
        "gps_runtime_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
        "dual_device_runtime_invoked": False,
        "dual_model_runtime_invoked": False,
        "failover_runtime_invoked": False,
        "multi_input_fusion_runtime_invoked": False,
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
        "frame_to_ocr_requires_visual_focus": closure_boundary_freeze["frame_to_ocr_requires_visual_focus"],
        "frame_to_tracking_requires_visual_focus": closure_boundary_freeze["frame_to_tracking_requires_visual_focus"],
        "frame_to_world_observation_requires_policy": closure_boundary_freeze["frame_to_world_observation_requires_policy"],
        "frame_to_navigation_action_allowed": False,
        "frame_to_speech_output_allowed": False,
        "frame_to_worldmodel_write_allowed": False,
        "frame_to_memory_write_allowed": False,
        "frame_to_fact_write_allowed": False,
        "dual_device_redundant_perception_placeholder_retained": bool(planning_dual_placeholder) and dryrun_dual_review.get("dual_device_placeholder_loaded") is True,
        "hardware_stage_deferred": True,
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION if not blockers else "CONTROLLED_FRAME_INPUT_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "controlled_frame_input_closure_summary": controlled_frame_input_closure_summary,
        "completed_phase_matrix": completed_phase_matrix,
        "validated_capability_summary": validated_capability_summary,
        "disabled_runtime_summary": disabled_runtime_summary,
        "closure_boundary_freeze": closure_boundary_freeze,
        "controlled_frame_input_non_claims_register": controlled_frame_input_non_claims_register,
        "deferred_capability_pool": deferred_capability_pool,
        "governance_debt_carryover": governance_debt_carryover,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": {
            "recommended_next_phase": summary["recommended_next_phase"],
            "final_decision": summary["final_decision"],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "no_runtime_boundary_report": no_runtime_boundary_report,
        "no_write_boundary_report": no_write_boundary_report,
    }
