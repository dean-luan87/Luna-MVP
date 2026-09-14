# -*- coding: utf-8 -*-
"""Post Crossing Decision Roadmap Decision v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Post-Crossing-Decision-Roadmap-Decision-v1-001"
DECISION_SCOPE = "post_crossing_decision_roadmap_decision_only"
SOURCE_CHAIN = "post_crossing_decision_roadmap_decision_v1"
DECISION_ID = "pcdrd_v1_001"
FINAL_DECISION = "POST_CROSSING_DECISION_ROADMAP_DECISION_READY_FOR_CONTROLLED_FRAME_SAMPLE_PLANNING"
NEXT_PHASE = "Phase-Controlled-Frame-Sample-Planning-v1-001"

CLOSURE_DECISION = "CROSSING_DECISION_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "CROSSING_DECISION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "CROSSING_DECISION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
GOVERNANCE_DECISION = "CROSSING_DECISION_SAFETY_GOVERNANCE_POLICY_READY_FOR_CROSSING_DECISION_DRYRUN"
SAFETY_CONSTITUTION_DECISION = "LUNA_SAFETY_CONSTITUTION_POLICY_READY_FOR_CROSSING_DECISION_SAFETY_GOVERNANCE"
CONTROLLED_FRAME_CLOSURE_DECISION = "CONTROLLED_FRAME_INPUT_CLOSED_FOR_CURRENT_MAINLINE"
MAP_LOCATION_DECISION = "MAP_LOCATION_READONLY_CONTEXT_POLICY_READY_FOR_CONTROLLED_FRAME_INPUT_PLANNING"
VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "crossing_decision_closure",
        "arg": "crossing_decision_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "crossing_decision_closure_summary.json", "validated_capability_summary.json"],
    },
    {
        "id": "crossing_decision_post_review",
        "arg": "crossing_decision_post_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "crossing_closure_readiness_decision.json"],
    },
    {
        "id": "crossing_decision_dryrun",
        "arg": "crossing_decision_dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "forbidden_crossing_output_check_results.json"],
    },
    {
        "id": "crossing_safety_governance",
        "arg": "crossing_safety_governance_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "forbidden_crossing_output_register.json"],
    },
    {
        "id": "safety_constitution",
        "arg": "safety_constitution_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "crossing_safety_inheritance_policy.json"],
    },
    {
        "id": "post_controlled_frame_roadmap_decision",
        "arg": "post_controlled_frame_roadmap_decision_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "recommended_next_phase_decision.json"],
    },
    {
        "id": "controlled_frame_input_closure",
        "arg": "controlled_frame_input_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "controlled_frame_input_closure_summary.json"],
    },
    {
        "id": "map_location_readonly_context",
        "arg": "map_location_readonly_context_root",
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
        "id": "safety_task_arbitration_policy",
        "arg": "safety_task_arbitration_policy_root",
        "required": False,
        "summary": "safety_task_arbitration_policy_v1_summary.json",
        "artifacts": ["safety_task_arbitration_policy_v1_summary.json"],
    },
    {
        "id": "task_aware_visual_focus_policy",
        "arg": "task_aware_visual_focus_policy_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "selective_tracking_adapter_policy",
        "arg": "selective_tracking_adapter_policy_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "visual_ocr_map_task_feedback_dryrun",
        "arg": "visual_ocr_map_task_feedback_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_controlled_output_definition",
        "arg": "minimal_runtime_controlled_output_definition_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "minimal_runtime_text_only_output_post_review",
        "arg": "minimal_runtime_text_only_output_post_review_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "voice_command_ownership_gate_policy",
        "arg": "voice_command_ownership_gate_policy_root",
        "required": False,
        "summary": "voice_command_ownership_gate_policy_v1_summary.json",
        "artifacts": ["voice_command_ownership_gate_policy_v1_summary.json"],
    },
    {
        "id": "voice_interruption_governance_dryrun",
        "arg": "voice_interruption_governance_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]

COMPLETED_CAPABILITIES = [
    "Luna Safety Constitution Policy v1",
    "Crossing Decision Safety Governance Policy v1",
    "Crossing Decision DryRun v1",
    "Crossing Decision Post-DryRun Review v1",
    "Crossing Decision Closure v1",
    "Controlled Frame Input Closure v1",
    "Map / Location Read-Only Context Policy v1",
    "Basic Navigation Loop Vision Strengthening Closure v1",
    "Minimal Runtime Integration Closure v1",
    "OCR Mainline Final Closure v1",
]

ROUTE_OPTIONS = [
    {
        "route_id": "A",
        "route_name": "Controlled Frame Sample Planning",
        "route_type": "sample_planning_policy",
        "readiness_level": "high",
        "dependency": [
            "safety constitution established",
            "crossing decision closed",
            "controlled frame input closed",
            "map location readonly context",
        ],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "defines sample manifest and file boundary without reading image pixels",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "B",
        "route_name": "Gate Taxonomy / Gate Requirement Framework",
        "route_type": "project_optimization_governance",
        "readiness_level": "medium",
        "dependency": [
            "accumulated gate families across safety, crossing, OCR, frame, map, voice, memory",
            "verifier template standardization",
        ],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "reduces gate sprawl but should not interrupt current mainline progression",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "project optimization work; important P0/P1 governance track but does not block controlled sample planning",
        "recommended_phase_name": "Phase-Gate-Taxonomy-Gate-Requirement-Framework-v1-001",
    },
    {
        "route_id": "C",
        "route_name": "MidPlatform Function Governance / Consolidation",
        "route_type": "governance_consolidation",
        "readiness_level": "medium",
        "dependency": ["governance debt carryover", "schema deduplication"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "prevents midplatform capability sprawl",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "valuable consolidation after controlled sample planning establishes next concrete artifact boundary",
        "recommended_phase_name": "Phase-MidPlatform-Function-Governance-Consolidation-v1-001",
    },
    {
        "route_id": "D",
        "route_name": "MidPlatform Resilience / Robustness Preplan",
        "route_type": "resilience_preplan",
        "readiness_level": "medium",
        "dependency": ["midplatform topology review", "degraded operation policy"],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "low",
        "governance_debt_impact": "captures structural fragility without changing runtime architecture now",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "P1 architecture/governance track after P0 sample and gate consolidation planning",
        "recommended_phase_name": "Phase-MidPlatform-Resilience-Robustness-Preplan-v1-001",
    },
    {
        "route_id": "E",
        "route_name": "Offline Distributed MidPlatform Architecture Preplan",
        "route_type": "future_architecture_preplan",
        "readiness_level": "low",
        "dependency": ["local-first constraints", "offline sync policy"],
        "risk_level": "medium",
        "expected_value": "strategic",
        "runtime_risk": "medium",
        "write_risk": "medium",
        "governance_debt_impact": "long-horizon architecture candidate",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "future architecture candidate",
        "recommended_phase_name": "Phase-Offline-Distributed-MidPlatform-Architecture-Preplan-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "Minimal Controlled Visual Runtime Planning",
        "route_type": "runtime_planning",
        "readiness_level": "low",
        "dependency": ["controlled frame sample planning", "crossing decision closed"],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "medium",
        "governance_debt_impact": "premature before sample manifest clarity",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "must remain behind controlled sample planning",
        "recommended_phase_name": "Phase-Minimal-Controlled-Visual-Runtime-Planning-v1-001",
    },
    {
        "route_id": "G",
        "route_name": "WorldModel Candidate Layer / Memory / Library Governance",
        "route_type": "future_governance_cluster",
        "readiness_level": "low",
        "dependency": ["entity resolution governance", "fact admission governance"],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "must stay deferred to preserve no-write guarantees",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "deferred future governance cluster",
        "recommended_phase_name": "Phase-WorldModel-Memory-Library-Governance-v1-001",
    },
    {
        "route_id": "H",
        "route_name": "Exploration Drive Policy",
        "route_type": "future_policy_candidate",
        "readiness_level": "low",
        "dependency": ["task-driven perception priority", "safety and sample boundaries"],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "high",
        "write_risk": "high",
        "governance_debt_impact": "would explode scope before sample and gate work mature",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "future roadmap candidate only",
        "recommended_phase_name": "Phase-Exploration-Drive-Policy-v1-001",
    },
    {
        "route_id": "I",
        "route_name": "Emotion Map / Affective Engine",
        "route_type": "future_affective_candidate",
        "readiness_level": "very_low",
        "dependency": ["grounded world information", "memory governance"],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "structurally unsound without grounded world and memory maturity",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "must remain future-only",
        "recommended_phase_name": "Phase-Emotion-Map-Affective-Engine-v1-001",
    },
]

GATE_TAXONOMY_FUTURE_TOPICS = [
    "gate_type_taxonomy",
    "gate_level_definition",
    "gate_input_output_contract",
    "allow_block_degrade_fallback_standard",
    "veto_power_definition",
    "override_policy",
    "dependency_graph",
    "audit_trace_requirement",
    "failure_mode_requirement",
    "recovery_mode_requirement",
    "verifier_requirement_template",
    "safety_layering",
    "independent_safety_path",
]

GATE_FAMILIES = [
    "Safety Constitution Gate",
    "Crossing Decision Gate",
    "OCR Activation Gate",
    "Frame Input Gate",
    "Map ReadOnly Gate",
    "Voice Ownership Gate",
    "Speech/VOP Gate",
    "Memory/WorldModel/Fact Gate",
    "Resource/Health Gate",
    "Privacy Governance Gate",
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

GOVERNANCE_DEBT_TOPICS = [
    "crossing governance complexity",
    "high-risk domain gate taxonomy missing",
    "forbidden output maintenance",
    "Safety Constitution inheritance tracking",
    "future Survival Constitution upgrade",
    "human assistance governance complexity",
    "multimodal crossing evidence validation debt",
    "controlled sample planning deferred",
    "real crossing runtime deferred",
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
    "Crossing Decision closure 不等于 Luna 会过街",
    "Crossing Decision closure 不等于真实过街判断能力",
    "Controlled Frame Sample Planning 不等于读取真实样例内容",
    "Gate Taxonomy 当前不进入实现",
    "MidPlatform Function Governance 不等于新增 runtime module",
    "MidPlatform Resilience 不等于 failover runtime 已开放",
    "Offline Distributed MidPlatform 不等于多设备同步已开放",
    "Exploration Drive 当前不进入 runtime",
    "WorldModel / Memory / Library 当前不进入写路径",
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
        "crossing_runtime_invoked": False,
        "emotion_engine_invoked": False,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_post_crossing_decision_roadmap_decision_v1(
    *,
    crossing_decision_closure_root: str,
    crossing_decision_post_review_root: str,
    crossing_decision_dryrun_root: str,
    crossing_safety_governance_root: str,
    safety_constitution_root: str,
    post_controlled_frame_roadmap_decision_root: str,
    controlled_frame_input_closure_root: str,
    map_location_readonly_context_root: str,
    vision_strengthening_closure_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    safety_task_arbitration_policy_root: Optional[str] = None,
    task_aware_visual_focus_policy_root: Optional[str] = None,
    selective_tracking_adapter_policy_root: Optional[str] = None,
    visual_ocr_map_task_feedback_dryrun_root: Optional[str] = None,
    minimal_runtime_controlled_output_definition_root: Optional[str] = None,
    minimal_runtime_text_only_output_post_review_root: Optional[str] = None,
    voice_command_ownership_gate_policy_root: Optional[str] = None,
    voice_interruption_governance_dryrun_root: Optional[str] = None,
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
    closure_root = roots["crossing_decision_closure"]["root"]
    closure_governance_debt = _read_json(closure_root / "governance_debt_carryover.json") if closure_root else {}
    closure_validated = _read_json(closure_root / "validated_capability_summary.json") if closure_root else {}

    crossing_decision_closure_input_loaded = (
        roots["crossing_decision_closure"]["loaded"]
        and summaries["crossing_decision_closure"].get("final_decision") == CLOSURE_DECISION
        and summaries["crossing_decision_closure"].get("crossing_decision_closed") is True
    )
    crossing_decision_post_review_input_loaded = (
        roots["crossing_decision_post_review"]["loaded"]
        and summaries["crossing_decision_post_review"].get("final_decision") == POST_REVIEW_DECISION
    )
    crossing_decision_dryrun_input_loaded = (
        roots["crossing_decision_dryrun"]["loaded"]
        and summaries["crossing_decision_dryrun"].get("final_decision") == DRYRUN_DECISION
    )
    crossing_decision_governance_input_loaded = (
        roots["crossing_safety_governance"]["loaded"]
        and summaries["crossing_safety_governance"].get("final_decision") == GOVERNANCE_DECISION
    )
    safety_constitution_input_loaded = (
        roots["safety_constitution"]["loaded"]
        and summaries["safety_constitution"].get("final_decision") == SAFETY_CONSTITUTION_DECISION
    )
    controlled_frame_input_closure_input_loaded = (
        roots["controlled_frame_input_closure"]["loaded"]
        and summaries["controlled_frame_input_closure"].get("final_decision") == CONTROLLED_FRAME_CLOSURE_DECISION
    )
    map_location_readonly_context_input_loaded = (
        roots["map_location_readonly_context"]["loaded"]
        and summaries["map_location_readonly_context"].get("final_decision") == MAP_LOCATION_DECISION
    )
    vision_strengthening_closure_input_loaded = (
        roots["vision_strengthening_closure"]["loaded"]
        and summaries["vision_strengthening_closure"].get("final_decision") == VISION_STRENGTHENING_CLOSURE_DECISION
    )
    minimal_runtime_integration_closure_loaded = (
        roots["minimal_runtime_integration_closure"]["loaded"]
        and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    )
    ocr_final_closure_loaded = (
        roots["ocr_final_closure"]["loaded"]
        and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION
    )

    current_crossing_decision_status_summary = {
        "current_mainline_status": "crossing_decision_closed_ready_for_next_roadmap_phase",
        "safety_constitution_inheritance_closed": safety_constitution_input_loaded,
        "crossing_governance_policy_closed": crossing_decision_governance_input_loaded,
        "crossing_dryrun_closed": crossing_decision_dryrun_input_loaded,
        "crossing_post_review_closed": crossing_decision_post_review_input_loaded,
        "crossing_decision_closed": crossing_decision_closure_input_loaded,
        "forbidden_crossing_outputs_absent": summaries["crossing_decision_closure"].get("forbidden_crossing_outputs_absent") is True,
        "crossing_runtime_claimed": False,
        "real_crossing_judgment_claimed": False,
        "safe_to_cross_capability_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "source_closure_ref": "_eval_out/crossing_decision_closure_v1_smoke_v0/crossing_decision_closure_summary.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    completed_capability_summary = {
        "capabilities": [
            {
                "capability_name": name,
                "completion_level": "policy_or_dryrun_or_review_or_closure",
                "runtime_enabled": False,
                "production_ready": False,
                "real_crossing_judgment": False,
                "validated_in_current_mainline": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for name in COMPLETED_CAPABILITIES
        ],
        "validated_capability_names_from_closure": closure_validated.get("validated_capabilities", []),
        "clarification": "policy / schema / dry-run / review / closure validation only; not crossing runtime",
        "completed_capability_count": len(COMPLETED_CAPABILITIES),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    route_rows = [{**route, "source_chain": SOURCE_CHAIN, **_not_fact()} for route in ROUTE_OPTIONS]
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
        "selected_top_priority_route": "Controlled Frame Sample Planning",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    recommended_next_phase_decision = {
        "decision_id": DECISION_ID,
        "decision_scope": DECISION_SCOPE,
        "source_closure_ref": "_eval_out/crossing_decision_closure_v1_smoke_v0/crossing_decision_closure_summary.json",
        "current_mainline_status": current_crossing_decision_status_summary["current_mainline_status"],
        "completed_capability_summary_ref": "completed_capability_summary.json",
        "route_option_matrix_ref": "route_option_matrix.json",
        "priority_ranking_ref": "priority_ranking.json",
        "selected_next_phase": NEXT_PHASE,
        "rejected_or_deferred_routes": [r["route_name"] for r in ROUTE_OPTIONS if not r["selected_now"]],
        "decision_reason": [
            "Crossing Decision 安全治理链已正式 closure，当前主线禁止过街许可输出",
            "Controlled Frame Input 已完成 planning + dry-run + review + closure，具备回到受控样例规划的前置条件",
            "Safety Constitution 与 Map/Location readonly 已建立，可安全推进 sample manifest / source policy / privacy precheck",
            "Gate Taxonomy 记为后续项目优化，不打断当前主线",
            "本阶段仍保持 no-runtime / no-read-image / no-camera",
        ],
        "boundary_freeze_ref": "boundary_freeze.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_gate_taxonomy_register = {
        "gate_taxonomy_deferred": True,
        "current_status": "project_optimization_deferred",
        "runtime_allowed_now": False,
        "implementation_allowed_now": False,
        "recommended_priority": "P1",
        "required_future_topics": GATE_TAXONOMY_FUTURE_TOPICS,
        "included_gate_families": GATE_FAMILIES,
        "defer_reason": "gate taxonomy is important project optimization but should not interrupt controlled sample planning mainline",
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

    deferred_worldmodel_memory_library_emotion_register = {
        "deferred_items": [
            {
                "capability_name": "WorldModel Candidate Layer",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "defer_reason": "must remain behind entity resolution and fact admission governance",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "capability_name": "Memory / Library Governance",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "defer_reason": "memory consolidation and library experience governance stay deferred",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "capability_name": "Exploration Drive Policy",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "defer_reason": "exploration drive remains future roadmap candidate",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "capability_name": "Emotion Map / Affective Engine",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "defer_reason": "requires grounded world information and memory maturity",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
        ],
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "exploration_drive_deferred": True,
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
        "no_crossing_runtime": True,
        "no_safe_to_cross_claim": True,
        "no_crossing_permission_output": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_roadmap_register = {
        "carryover_topics": [
            {"topic": topic, "roadmap_impact": "explicit in next-phase prioritization", "source_chain": SOURCE_CHAIN, **_not_fact()}
            for topic in GOVERNANCE_DEBT_TOPICS
        ],
        "inherited_from_crossing_closure": closure_governance_debt.get("carryover_topics", []),
        "future_midplatform_function_governance_required": True,
        "future_gate_taxonomy_required": True,
        "future_survival_constitution_required": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_claims_register = {
        "non_claims": NON_CLAIMS,
        "controlled_sample_planning_started": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers: List[str] = []
    for flag_name, flag_value in (
        ("crossing_decision_closure_input_loaded", crossing_decision_closure_input_loaded),
        ("crossing_decision_post_review_input_loaded", crossing_decision_post_review_input_loaded),
        ("crossing_decision_dryrun_input_loaded", crossing_decision_dryrun_input_loaded),
        ("crossing_decision_governance_input_loaded", crossing_decision_governance_input_loaded),
        ("safety_constitution_input_loaded", safety_constitution_input_loaded),
        ("controlled_frame_input_closure_input_loaded", controlled_frame_input_closure_input_loaded),
        ("map_location_readonly_context_input_loaded", map_location_readonly_context_input_loaded),
        ("vision_strengthening_closure_input_loaded", vision_strengthening_closure_input_loaded),
        ("minimal_runtime_integration_closure_loaded", minimal_runtime_integration_closure_loaded),
        ("ocr_final_closure_loaded", ocr_final_closure_loaded),
    ):
        if not flag_value:
            blockers.append(flag_name)

    route_names = {r["route_name"] for r in ROUTE_OPTIONS}
    route_option_count = len(ROUTE_OPTIONS)
    p0_route_count = len(p0_routes)
    p1_route_count = len(p1_routes)
    p2_route_count = len(p2_routes)

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "crossing_decision_closure_input_loaded": crossing_decision_closure_input_loaded,
        "crossing_decision_post_review_input_loaded": crossing_decision_post_review_input_loaded,
        "crossing_decision_dryrun_input_loaded": crossing_decision_dryrun_input_loaded,
        "crossing_decision_governance_input_loaded": crossing_decision_governance_input_loaded,
        "safety_constitution_input_loaded": safety_constitution_input_loaded,
        "controlled_frame_input_closure_input_loaded": controlled_frame_input_closure_input_loaded,
        "map_location_readonly_context_input_loaded": map_location_readonly_context_input_loaded,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "current_status_summary_generated": True,
        "completed_capability_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "deferred_gate_taxonomy_register_generated": True,
        "deferred_resilience_distributed_midplatform_register_generated": True,
        "deferred_worldmodel_memory_library_emotion_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": route_option_count,
        "p0_route_count": p0_route_count,
        "p1_route_count": p1_route_count,
        "p2_route_count": p2_route_count,
        "controlled_frame_sample_planning_route_exists": "Controlled Frame Sample Planning" in route_names,
        "gate_taxonomy_route_exists": "Gate Taxonomy / Gate Requirement Framework" in route_names,
        "midplatform_function_governance_route_exists": "MidPlatform Function Governance / Consolidation" in route_names,
        "midplatform_resilience_route_exists": "MidPlatform Resilience / Robustness Preplan" in route_names,
        "offline_distributed_midplatform_route_exists": "Offline Distributed MidPlatform Architecture Preplan" in route_names,
        "worldmodel_memory_library_route_exists": "WorldModel Candidate Layer / Memory / Library Governance" in route_names,
        "exploration_drive_route_exists": "Exploration Drive Policy" in route_names,
        "emotion_engine_route_exists": "Emotion Map / Affective Engine" in route_names,
        "crossing_decision_closed": crossing_decision_closure_input_loaded,
        "forbidden_crossing_outputs_absent": summaries["crossing_decision_closure"].get("forbidden_crossing_outputs_absent") is True,
        "crossing_runtime_claimed": False,
        "real_crossing_judgment_claimed": False,
        "safe_to_cross_capability_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "gate_taxonomy_deferred": True,
        "gate_taxonomy_project_optimization": True,
        "midplatform_resilience_deferred": True,
        "offline_distributed_midplatform_deferred": True,
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "exploration_drive_deferred": True,
        "emotion_engine_deferred": True,
        "controlled_sample_planning_started": False,
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
        "crossing_runtime_invoked": False,
        "emotion_engine_invoked": False,
        "boundary_ok": not blockers,
        "violations": blockers,
        "final_decision": FINAL_DECISION if not blockers else "POST_CROSSING_DECISION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    post_crossing_decision_roadmap_decision = {
        "decision_id": DECISION_ID,
        "decision_scope": DECISION_SCOPE,
        "source_closure_ref": "_eval_out/crossing_decision_closure_v1_smoke_v0/crossing_decision_closure_summary.json",
        "current_mainline_status": current_crossing_decision_status_summary["current_mainline_status"],
        "completed_capability_summary_ref": "completed_capability_summary.json",
        "route_option_matrix_ref": "route_option_matrix.json",
        "priority_ranking_ref": "priority_ranking.json",
        "selected_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "rejected_or_deferred_routes": recommended_next_phase_decision["rejected_or_deferred_routes"],
        "decision_reason": recommended_next_phase_decision["decision_reason"],
        "boundary_freeze_ref": "boundary_freeze.json",
        "final_decision": summary["final_decision"],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "post_crossing_decision_roadmap_decision": post_crossing_decision_roadmap_decision,
        "current_crossing_decision_status_summary": current_crossing_decision_status_summary,
        "completed_capability_summary": completed_capability_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "deferred_gate_taxonomy_register": deferred_gate_taxonomy_register,
        "deferred_resilience_distributed_midplatform_register": deferred_resilience_distributed_midplatform_register,
        "deferred_worldmodel_memory_library_emotion_register": deferred_worldmodel_memory_library_emotion_register,
        "boundary_freeze": boundary_freeze,
        "governance_debt_roadmap_register": governance_debt_roadmap_register,
        "non_claims_register": non_claims_register,
        "next_phase_recommendation": {
            "recommended_next_phase": summary["recommended_next_phase"],
            "final_decision": summary["final_decision"],
            "priority_level": "P0",
            "route_name": "Controlled Frame Sample Planning",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        },
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }
