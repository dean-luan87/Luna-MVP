# -*- coding: utf-8 -*-
"""Post Controlled Frame Input Roadmap Decision v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Post-Controlled-Frame-Input-Roadmap-Decision-v1-001"
DECISION_SCOPE = "post_controlled_frame_input_roadmap_decision_only"
SOURCE_CHAIN = "post_controlled_frame_input_roadmap_decision_v1"
DECISION_ID = "pcfird_v1_001"
FINAL_DECISION = "POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY"
NEXT_PHASE = "Phase-Crossing-Decision-Safety-Governance-Policy-v1-001"

CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "CONTROLLED_FRAME_INPUT_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "CONTROLLED_FRAME_INPUT_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
PLANNING_DECISION = "CONTROLLED_FRAME_INPUT_PLANNING_READY_FOR_CONTROLLED_FRAME_INPUT_DRYRUN"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
POST_VISION_ROADMAP_DECISION = "POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
VISUAL_FOCUS_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "controlled_frame_input_closure",
        "arg": "controlled_frame_input_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_input_closure_summary.json", "validated_capability_summary.json"],
    },
    {
        "id": "controlled_frame_input_post_review",
        "arg": "controlled_frame_input_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_input_closure_readiness_decision.json"],
    },
    {
        "id": "controlled_frame_input_dryrun",
        "arg": "controlled_frame_input_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_input_dryrun_results.json"],
    },
    {
        "id": "controlled_frame_input_planning",
        "arg": "controlled_frame_input_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "frame_downstream_handoff_policy.json"],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "post_vision_strengthening_roadmap_decision",
        "arg": "post_vision_strengthening_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "vision_strengthening_closure",
        "arg": "vision_strengthening_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "task_aware_visual_focus",
        "arg": "task_aware_visual_focus_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "midplatform_perception_orchestration",
        "arg": "midplatform_perception_orchestration_root",
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
        "id": "safety_task_arbitration_policy",
        "arg": "safety_task_arbitration_policy_root",
        "required": False,
        "summary": "safety_task_arbitration_policy_v1_summary.json",
        "artifacts": ["safety_task_arbitration_policy_v1_summary.json"],
    },
    {
        "id": "crossing_decision_safety_governance_policy",
        "arg": "crossing_decision_safety_governance_policy_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "traffic_safety_semantics_stub",
        "arg": "traffic_safety_semantics_stub_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "midplatform_function_governance_consolidation",
        "arg": "midplatform_function_governance_consolidation_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]

COMPLETED_CAPABILITIES = [
    "Basic Navigation Loop Vision Strengthening Closure",
    "Post Vision Strengthening Roadmap Decision",
    "Map / Location Read-Only Context Policy",
    "MidPlatform Perception Orchestration Policy",
    "Task-Aware Visual Focus Policy",
    "Controlled Frame Input Planning",
    "Controlled Frame Input DryRun",
    "Controlled Frame Input Post-DryRun Review",
    "Controlled Frame Input Closure",
]

ROUTE_OPTIONS = [
    {
        "route_id": "A",
        "route_name": "Controlled Frame Sample Planning",
        "route_type": "sample_planning_policy",
        "readiness_level": "medium",
        "dependency": [
            "controlled frame input closure",
            "sample manifest definition",
            "sample source policy",
            "privacy precheck and file boundary",
        ],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "low",
        "governance_debt_impact": "clarifies future real file/static image sample governance but does not close the highest-risk navigation gap",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "controlled sample planning is now structurally possible, but crossing safety governance is the higher-risk safety gap and should land first",
        "recommended_phase_name": "Phase-Controlled-Frame-Sample-Planning-v1-001",
    },
    {
        "route_id": "B",
        "route_name": "Crossing Decision Safety Governance Policy",
        "route_type": "safety_governance_policy",
        "readiness_level": "high",
        "dependency": [
            "vision-strengthened navigation closure",
            "map/location readonly context",
            "controlled frame input closure",
            "navigation risk separation",
        ],
        "risk_level": "high",
        "expected_value": "very_high",
        "runtime_risk": "high",
        "write_risk": "low",
        "governance_debt_impact": "separates crossing / traffic / crowd / intersection judgments from ordinary navigation before any controlled sample or runtime expansion",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "C",
        "route_name": "MidPlatform Function Governance / Consolidation",
        "route_type": "governance_consolidation",
        "readiness_level": "medium",
        "dependency": [
            "governance debt carryover",
            "schema deduplication",
            "midplatform boundary freeze",
        ],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "directly reduces capability sprawl and duplicated governance modules",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "important but should follow crossing safety governance so the highest-risk safety contract is frozen before broader consolidation",
        "recommended_phase_name": "Phase-MidPlatform-Function-Governance-Consolidation-v1-001",
    },
    {
        "route_id": "D",
        "route_name": "MidPlatform Resilience / Robustness Preplan",
        "route_type": "resilience_preplan",
        "readiness_level": "medium",
        "dependency": [
            "midplatform topology review",
            "single point failure analysis",
            "degraded operation policy",
        ],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "low",
        "governance_debt_impact": "captures structural fragility topics without prematurely changing runtime architecture",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "valuable as a separate P1 track, but it is less urgent than crossing safety governance and sample/governance P0 items",
        "recommended_phase_name": "Phase-MidPlatform-Resilience-Robustness-Preplan-v1-001",
    },
    {
        "route_id": "E",
        "route_name": "Offline Distributed MidPlatform Architecture Preplan",
        "route_type": "future_architecture_preplan",
        "readiness_level": "low",
        "dependency": [
            "local-first constraints",
            "offline/weak-network mode policy",
            "distributed candidate sync policy",
        ],
        "risk_level": "medium",
        "expected_value": "strategic",
        "runtime_risk": "medium",
        "write_risk": "medium",
        "governance_debt_impact": "important long-horizon architecture exploration but not required before current safety governance gaps are addressed",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "should stay as a future architecture candidate after higher-priority safety and sample/governance decisions",
        "recommended_phase_name": "Phase-Offline-Distributed-MidPlatform-Architecture-Preplan-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "Minimal Controlled Visual Runtime Planning",
        "route_type": "runtime_planning",
        "readiness_level": "low",
        "dependency": [
            "controlled frame sample planning",
            "crossing safety governance",
            "stronger frame governance clarity",
        ],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "medium",
        "governance_debt_impact": "premature runtime planning would amplify unresolved safety and governance debt",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "must remain behind crossing safety governance and controlled sample planning because the mainline is still explicitly non-runtime",
        "recommended_phase_name": "Phase-Minimal-Controlled-Visual-Runtime-Planning-v1-001",
    },
    {
        "route_id": "G",
        "route_name": "Exploration Drive Policy",
        "route_type": "future_policy_candidate",
        "readiness_level": "low",
        "dependency": [
            "task-driven perception priority",
            "crossing safety governance",
            "worldmodel/memory governance maturity",
        ],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "high",
        "write_risk": "high",
        "governance_debt_impact": "would explode scope if introduced before safety, sample, and governance boundaries are stronger",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "kept as a future roadmap candidate while task-driven perception and safety governance remain the active priority",
        "recommended_phase_name": "Phase-Exploration-Drive-Policy-v1-001",
    },
    {
        "route_id": "H",
        "route_name": "WorldModel Candidate Layer / Memory / Library Governance",
        "route_type": "future_governance_cluster",
        "readiness_level": "low",
        "dependency": [
            "world observation maturity",
            "entity resolution governance",
            "fact admission governance",
            "memory consolidation governance",
        ],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "must stay deferred to preserve no-write guarantees and avoid premature WML coupling",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "worldmodel/memory/library governance remains deferred until stronger admission and memory controls exist",
        "recommended_phase_name": "Phase-WorldModel-Memory-Library-Governance-v1-001",
    },
    {
        "route_id": "I",
        "route_name": "Emotion Map / Affective Engine",
        "route_type": "future_affective_candidate",
        "readiness_level": "very_low",
        "dependency": [
            "grounded world information",
            "event chain maturity",
            "relationship context",
            "memory governance",
        ],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "affective modeling without grounded world and memory governance would be structurally unsound",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "must remain future-only until real world information, event chains, and memory governance are substantially more mature",
        "recommended_phase_name": "Phase-Emotion-Map-Affective-Engine-v1-001",
    },
]

DEFERRED_RESILIENCE_TOPICS = [
    "midplatform_single_point_failure",
    "local_minimum_safety_path",
    "module_autonomy",
    "degraded_operation",
    "failover_arbitration",
    "pressure_test",
    "resource_congestion_control",
    "local_first_midplatform",
    "cloud_enhanced_midplatform",
    "distributed_candidate_sync",
    "conflict_merge_rollback",
    "privacy_preserving_sync",
    "offline_weak_network_mode",
    "multi_device_coordination",
]

DEFERRED_EXPLORATION_DIRECTIONS = [
    "safety_exploration",
    "task_exploration",
    "worldmodel_gap_exploration",
    "conflict_validation_exploration",
    "resource_environment_adaptation_exploration",
    "emotion_map_precursor_exploration",
]

GOVERNANCE_DEBT_TOPICS = [
    "frame source policy complexity",
    "privacy tagging complexity",
    "frame quality gate complexity",
    "STC/freshness integration complexity",
    "downstream handoff complexity",
    "dual-device placeholder future complexity",
    "hardware-stage deferred debt",
    "controlled sample planning deferred",
    "crossing safety governance gap",
    "midplatform function governance accumulation",
    "midplatform resilience planning deferred",
    "offline distributed architecture deferred",
    "no duplicate governance module enforcement",
]

NON_CLAIMS = [
    "roadmap decision 不等于 runtime enablement",
    "roadmap decision 不等于 controlled sample planning 已开始",
    "roadmap decision 不等于真实图像读取",
    "roadmap decision 不等于 live camera 接入",
    "roadmap decision 不等于 map API 接入",
    "roadmap decision 不等于 OCR provider 接入",
    "roadmap decision 不等于 tracking runtime 接入",
    "selected next phase 不等于允许过马路动作",
    "Crossing Decision Safety Governance 不等于真实过街判断 runtime",
    "Controlled Frame Sample Planning 不等于读取真实样例内容",
    "MidPlatform Function Governance 不等于新增 runtime module",
    "MidPlatform Resilience / Robustness 不等于 failover runtime 已开放",
    "Offline Distributed MidPlatform 不等于多设备同步已开放",
    "Exploration Drive 当前不进入 runtime",
    "WorldModel Candidate Layer / Memory / Library Governance 当前不进入写路径",
    "Emotion Map / Affective Engine 当前不进入实现",
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


def _boundary_payload() -> Dict[str, Any]:
    return {
        "decision_scope": DECISION_SCOPE,
        "roadmap_decision_only": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "frame_content_loaded": False,
        "actual_image_read": False,
        "camera_invoked": False,
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
        "emotion_engine_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_post_controlled_frame_input_roadmap_decision_v1(
    *,
    controlled_frame_input_closure_root: str,
    controlled_frame_input_post_review_root: str,
    controlled_frame_input_dryrun_root: str,
    controlled_frame_input_planning_root: str,
    map_location_readonly_context_root: str,
    post_vision_strengthening_roadmap_decision_root: str,
    vision_strengthening_closure_root: str,
    task_aware_visual_focus_root: str,
    midplatform_perception_orchestration_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    hardware_profile_capability_registry_root: Optional[str] = None,
    system_health_center_governance_root: Optional[str] = None,
    vision_frame_trace_stream_registry_root: Optional[str] = None,
    vision_frame_input_governance_root: Optional[str] = None,
    safety_task_arbitration_policy_root: Optional[str] = None,
    crossing_decision_safety_governance_policy_root: Optional[str] = None,
    traffic_safety_semantics_stub_root: Optional[str] = None,
    midplatform_function_governance_consolidation_root: Optional[str] = None,
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
    closure_root = roots["controlled_frame_input_closure"]["root"]

    closure_summary_payload = _read_json(closure_root / "controlled_frame_input_closure_summary.json") if closure_root else {}
    closure_validated_summary = _read_json(closure_root / "validated_capability_summary.json") if closure_root else {}
    closure_governance_debt = _read_json(closure_root / "governance_debt_carryover.json") if closure_root else {}

    controlled_frame_input_closure_input_loaded = (
        roots["controlled_frame_input_closure"]["loaded"]
        and summaries["controlled_frame_input_closure"].get("final_decision") == CLOSURE_DECISION
    )
    controlled_frame_input_post_review_input_loaded = (
        roots["controlled_frame_input_post_review"]["loaded"]
        and summaries["controlled_frame_input_post_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    controlled_frame_input_dryrun_input_loaded = (
        roots["controlled_frame_input_dryrun"]["loaded"]
        and summaries["controlled_frame_input_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    controlled_frame_input_planning_input_loaded = (
        roots["controlled_frame_input_planning"]["loaded"]
        and summaries["controlled_frame_input_planning"].get("final_decision") == PLANNING_DECISION
    )
    map_location_readonly_context_input_loaded = (
        roots["map_location_readonly_context"]["loaded"]
        and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_DECISION
    )
    post_vision_strengthening_roadmap_decision_input_loaded = (
        roots["post_vision_strengthening_roadmap_decision"]["loaded"]
        and summaries["post_vision_strengthening_roadmap_decision"].get("final_decision") == POST_VISION_ROADMAP_DECISION
    )
    vision_strengthening_closure_input_loaded = (
        roots["vision_strengthening_closure"]["loaded"]
        and summaries["vision_strengthening_closure"].get("final_decision") == VISION_STRENGTHENING_CLOSURE_DECISION
    )
    task_aware_visual_focus_input_loaded = (
        roots["task_aware_visual_focus"]["loaded"]
        and summaries["task_aware_visual_focus"].get("final_decision") == VISUAL_FOCUS_DECISION
    )
    midplatform_perception_orchestration_input_loaded = (
        roots["midplatform_perception_orchestration"]["loaded"]
        and summaries["midplatform_perception_orchestration"].get("final_decision") == MIDPLATFORM_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = (
        roots["ocr_final_closure"]["loaded"]
        and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION
    )

    current_controlled_frame_input_status_summary = {
        "current_mainline_status": "controlled_frame_input_closed_waiting_for_next_policy_decision",
        "controlled_frame_input_planning_closed": bool(summaries["controlled_frame_input_closure"].get("controlled_frame_input_planning_closed")),
        "controlled_frame_input_dryrun_closed": bool(summaries["controlled_frame_input_closure"].get("controlled_frame_input_dryrun_closed")),
        "controlled_frame_input_post_review_closed": bool(summaries["controlled_frame_input_closure"].get("controlled_frame_input_post_review_closed")),
        "controlled_frame_input_closed": bool(summaries["controlled_frame_input_closure"].get("controlled_frame_input_closed")),
        "controlled_sample_planning_started": False,
        "live_camera_claimed": False,
        "visual_runtime_claimed": False,
        "image_read_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "source_closure_ref": "_eval_out/controlled_frame_input_closure_v1_smoke_v0/controlled_frame_input_closure_summary.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    validated_names = closure_validated_summary.get("validated_capabilities", [])
    completed_capability_summary = {
        "capabilities": [
            {
                "capability_name": name,
                "completion_level": "policy_or_planning_or_dryrun_or_review_or_closure",
                "runtime_enabled": False,
                "production_ready": False,
                "live_ready": False,
                "validated_in_current_mainline": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for name in COMPLETED_CAPABILITIES
        ],
        "validated_capability_names_from_closure": validated_names,
        "completed_capability_count": len(COMPLETED_CAPABILITIES),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    route_rows = [{**route, "source_chain": SOURCE_CHAIN, **_not_fact()} for route in ROUTE_OPTIONS]
    route_option_matrix = {
        "routes": route_rows,
        "route_option_count": len(route_rows),
        "selected_route_id": "B",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    p0_routes = [route["route_name"] for route in ROUTE_OPTIONS if route["recommended_priority"] == "P0"]
    p1_routes = [route["route_name"] for route in ROUTE_OPTIONS if route["recommended_priority"] == "P1"]
    p2_routes = [route["route_name"] for route in ROUTE_OPTIONS if route["recommended_priority"] == "P2"]
    priority_ranking = {
        "P0": p0_routes,
        "P1": p1_routes,
        "P2": p2_routes,
        "p0_route_count": len(p0_routes),
        "p1_route_count": len(p1_routes),
        "p2_route_count": len(p2_routes),
        "selected_top_priority_route": "Crossing Decision Safety Governance Policy",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    recommended_next_phase_decision = {
        "decision_id": DECISION_ID,
        "decision_scope": DECISION_SCOPE,
        "source_closure_ref": "_eval_out/controlled_frame_input_closure_v1_smoke_v0/controlled_frame_input_closure_summary.json",
        "current_mainline_status": current_controlled_frame_input_status_summary["current_mainline_status"],
        "completed_capability_summary_ref": "completed_capability_summary.json",
        "route_option_matrix_ref": "route_option_matrix.json",
        "priority_ranking_ref": "priority_ranking.json",
        "selected_next_phase": NEXT_PHASE,
        "rejected_or_deferred_routes": [route["route_name"] for route in ROUTE_OPTIONS if not route["selected_now"]],
        "decision_reason": [
            "视觉增强导航闭环、只读地图上下文、受控帧输入治理都已经完成到 closure 级别，主线可以转入下一条 policy 主线",
            "过街 / 红绿灯 / 车流 / 人流 / 路口判断属于最高风险缺口，不能混入普通导航链",
            "先冻结 crossing safety governance，能为后续 controlled sample planning 和任何受控视觉 runtime 提供硬安全边界",
            "当前 phase 仍保持 no-runtime / no-write / no-action / no-speech，不接 camera、不接 map API、不读真实图像",
            "controlled sample planning 现在虽然可评估，但应排在 crossing safety governance 之后",
        ],
        "boundary_freeze_ref": "boundary_freeze.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_resilience_distributed_midplatform_register = {
        "midplatform_resilience_deferred": True,
        "offline_distributed_midplatform_deferred": True,
        "current_status": "future_architecture_candidate",
        "runtime_allowed_now": False,
        "direct_action_allowed": False,
        "required_future_topics": DEFERRED_RESILIENCE_TOPICS,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_exploration_drive_register = {
        "exploration_drive_deferred": True,
        "current_status": "deferred_future_candidate",
        "priority": "P2",
        "runtime_allowed_now": False,
        "direct_action_allowed": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "fact_write_allowed": False,
        "exploration_directions": DEFERRED_EXPLORATION_DIRECTIONS,
        "defer_reason": [
            "task-driven perception 仍然是当前主线优先项",
            "crossing safety governance 尚未正式定义",
            "controlled visual sample stage 尚未启动",
            "worldmodel/memory/library governance 仍然 deferred",
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_worldmodel_memory_library_emotion_register = {
        "deferred_items": [
            {
                "capability_name": "WorldModel Candidate Layer",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "defer_reason": "worldmodel candidate aggregation must remain behind entity resolution and fact admission governance",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "capability_name": "Memory / Library Governance",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "defer_reason": "memory consolidation and library experience governance must stay deferred while the mainline remains no-write",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "capability_name": "Emotion Map / Affective Engine",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "defer_reason": "emotion modeling must wait for grounded world information, event chains, relationship context, and memory governance",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ],
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "emotion_engine_deferred": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    boundary_freeze = {
        "no_runtime": True,
        "no_write": True,
        "no_action": True,
        "no_speech": True,
        "no_fact": True,
        "no_live_camera": True,
        "no_image_read": True,
        "no_visual_model": True,
        "no_map_api": True,
        "no_OCR_provider": True,
        "no_tracking_runtime": True,
        "no_worldmodel_write": True,
        "no_memory_write": True,
        "no_library_write": True,
        "no_entity_resolution": True,
        "no_fact_admission": True,
        "no_emotion_engine": True,
        "no_dual_device_runtime": True,
        "no_failover_runtime": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_roadmap_register = {
        "carryover_topics": [
            {
                "topic": topic,
                "roadmap_impact": "must remain explicit during next-phase prioritization",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for topic in GOVERNANCE_DEBT_TOPICS
        ],
        "inherited_from_controlled_frame_input_closure": closure_governance_debt.get("carryover_topics", []),
        "future_midplatform_function_governance_required": True,
        "future_midplatform_resilience_governance_required": True,
        "no_duplicate_governance_module_allowed": True,
        "crossing_safety_governance_selected_for_p0": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_claims_register = {
        "non_claims": NON_CLAIMS,
        "controlled_sample_planning_started": False,
        "live_camera_claimed": False,
        "visual_runtime_claimed": False,
        "image_read_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "priority_level": "P0",
        "route_name": "Crossing Decision Safety Governance Policy",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers = []
    for flag_name, flag_value in (
        ("controlled_frame_input_closure_input_loaded", controlled_frame_input_closure_input_loaded),
        ("controlled_frame_input_post_review_input_loaded", controlled_frame_input_post_review_input_loaded),
        ("controlled_frame_input_dryrun_input_loaded", controlled_frame_input_dryrun_input_loaded),
        ("controlled_frame_input_planning_input_loaded", controlled_frame_input_planning_input_loaded),
        ("map_location_readonly_context_input_loaded", map_location_readonly_context_input_loaded),
        ("post_vision_strengthening_roadmap_decision_input_loaded", post_vision_strengthening_roadmap_decision_input_loaded),
        ("vision_strengthening_closure_input_loaded", vision_strengthening_closure_input_loaded),
        ("task_aware_visual_focus_input_loaded", task_aware_visual_focus_input_loaded),
        ("midplatform_perception_orchestration_input_loaded", midplatform_perception_orchestration_input_loaded),
        ("minimal_runtime_integration_closure_loaded", minimal_runtime_integration_closure_loaded),
        ("ocr_final_closure_loaded", ocr_final_closure_loaded),
    ):
        if not flag_value:
            blockers.append(flag_name)

    route_names = {route["route_name"] for route in ROUTE_OPTIONS}
    route_option_count = len(ROUTE_OPTIONS)
    p0_route_count = len(p0_routes)
    p1_route_count = len(p1_routes)
    p2_route_count = len(p2_routes)

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "controlled_frame_input_post_review_input_loaded": controlled_frame_input_post_review_input_loaded,
        "controlled_frame_input_dryrun_input_loaded": controlled_frame_input_dryrun_input_loaded,
        "controlled_frame_input_planning_input_loaded": controlled_frame_input_planning_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "post_vision_strengthening_roadmap_decision_input_loaded": post_vision_strengthening_roadmap_decision_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "current_status_summary_generated": True,
        "completed_capability_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "deferred_resilience_distributed_midplatform_register_generated": True,
        "deferred_exploration_drive_register_generated": True,
        "deferred_worldmodel_memory_library_emotion_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": route_option_count,
        "p0_route_count": p0_route_count,
        "p1_route_count": p1_route_count,
        "p2_route_count": p2_route_count,
        "crossing_decision_safety_governance_route_exists": "Crossing Decision Safety Governance Policy" in route_names,
        "controlled_frame_sample_planning_route_exists": "Controlled Frame Sample Planning" in route_names,
        "midplatform_function_governance_route_exists": "MidPlatform Function Governance / Consolidation" in route_names,
        "midplatform_resilience_route_exists": "MidPlatform Resilience / Robustness Preplan" in route_names,
        "offline_distributed_midplatform_route_exists": "Offline Distributed MidPlatform Architecture Preplan" in route_names,
        "exploration_drive_deferred": True,
        "midplatform_resilience_deferred": True,
        "offline_distributed_midplatform_deferred": True,
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "emotion_engine_deferred": True,
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
        "camera_invoked": False,
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
        "emotion_engine_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION if not blockers else "POST_CONTROLLED_FRAME_INPUT_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    post_controlled_frame_input_roadmap_decision = {
        "decision_id": DECISION_ID,
        "decision_scope": DECISION_SCOPE,
        "source_closure_ref": "_eval_out/controlled_frame_input_closure_v1_smoke_v0/controlled_frame_input_closure_summary.json",
        "current_mainline_status": current_controlled_frame_input_status_summary["current_mainline_status"],
        "completed_capability_summary_ref": "completed_capability_summary.json",
        "route_option_matrix_ref": "route_option_matrix.json",
        "priority_ranking_ref": "priority_ranking.json",
        "selected_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "rejected_or_deferred_routes": recommended_next_phase_decision["rejected_or_deferred_routes"],
        "decision_reason": recommended_next_phase_decision["decision_reason"],
        "boundary_freeze_ref": "boundary_freeze.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "post_controlled_frame_input_roadmap_decision": post_controlled_frame_input_roadmap_decision,
        "current_controlled_frame_input_status_summary": current_controlled_frame_input_status_summary,
        "completed_capability_summary": completed_capability_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "deferred_resilience_distributed_midplatform_register": deferred_resilience_distributed_midplatform_register,
        "deferred_exploration_drive_register": deferred_exploration_drive_register,
        "deferred_worldmodel_memory_library_emotion_register": deferred_worldmodel_memory_library_emotion_register,
        "boundary_freeze": boundary_freeze,
        "governance_debt_roadmap_register": governance_debt_roadmap_register,
        "non_claims_register": non_claims_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }
