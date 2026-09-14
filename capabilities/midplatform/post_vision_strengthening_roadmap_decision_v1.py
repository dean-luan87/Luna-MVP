# -*- coding: utf-8 -*-
"""Post Vision Strengthening Roadmap Decision v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Post-Vision-Strengthening-Roadmap-Decision-v1-001"
DECISION_SCOPE = "post_vision_strengthening_roadmap_decision_only"
SOURCE_CHAIN = "post_vision_strengthening_roadmap_decision_v1"
DECISION_ID = "pvsrd_v1_001"
FINAL_DECISION = "POST_VISION_STRENGTHENING_ROADMAP_DECISION_READY_FOR_MAP_LOCATION_READONLY_CONTEXT_POLICY"
NEXT_PHASE = "Phase-Map-Location-ReadOnly-Context-Policy-v1-001"

VISION_STRENGTHENING_CLOSURE_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
POST_REVIEW_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FEEDBACK_DRYRUN_DECISION = "VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_READY_FOR_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING"
TRACKING_DECISION = "SELECTIVE_TRACKING_ADAPTER_POLICY_READY_FOR_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN"
WORLDOBS_DECISION = "WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY"
VISUAL_FOCUS_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
PLANNING_DECISION = "RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY"
PREPLAN_DECISION = "PREPLAN_READY_FOR_FORMAL_PHASE_DECISION"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
    {
        "id": "vision_strengthening_closure",
        "arg": "vision_strengthening_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "vision_strengthening_closure_summary.json", "completed_phase_matrix.json"],
    },
    {
        "id": "post_dryrun_review",
        "arg": "post_dryrun_review_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "closure_readiness_decision.json", "verifier_report.json"],
    },
    {
        "id": "dryrun",
        "arg": "dryrun_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "navigation_loop_vision_strengthening_dryrun_results.json", "verifier_report.json"],
    },
    {
        "id": "visual_ocr_map_task_feedback",
        "arg": "visual_ocr_map_task_feedback_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "governance_debt_register.json"],
    },
    {
        "id": "selective_tracking",
        "arg": "selective_tracking_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "governance_debt_register.json"],
    },
    {
        "id": "world_observation_entity_feature",
        "arg": "world_observation_entity_feature_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "governance_debt_register.json"],
    },
    {
        "id": "task_aware_visual_focus",
        "arg": "task_aware_visual_focus_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "governance_debt_register.json"],
    },
    {
        "id": "midplatform_perception_orchestration",
        "arg": "midplatform_perception_orchestration_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "governance_debt_register.json"],
    },
    {
        "id": "return_to_vision_planning",
        "arg": "return_to_vision_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "return_to_vision_preplan",
        "arg": "return_to_vision_preplan_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "preplan_readiness_gate.json"],
    },
    {
        "id": "minimal_runtime_integration_closure",
        "arg": "minimal_runtime_integration_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "completed_phase_matrix.json"],
    },
    {
        "id": "ocr_final_closure",
        "arg": "ocr_final_closure_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "ocr_completed_phase_matrix.json"],
    },
    {
        "id": "basic_navigation_loop_stabilization",
        "arg": "basic_navigation_loop_stabilization_root",
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
        "id": "navigation_guidance_speech_adapter",
        "arg": "navigation_guidance_speech_adapter_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "voice_interruption_governance_dryrun",
        "arg": "voice_interruption_governance_dryrun_root",
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
        "id": "map_location_readonly_context_policy",
        "arg": "map_location_readonly_context_policy_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "map_route_location_context_integration",
        "arg": "map_route_location_context_integration_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
    {
        "id": "gps_route_context_dryrun",
        "arg": "gps_route_context_dryrun_root",
        "required": False,
        "summary": "summary.json",
        "artifacts": ["summary.json"],
    },
]

COMPLETED_CAPABILITIES = [
    "Return-To-Vision Mainline Planning",
    "MidPlatform Perception Orchestration Policy",
    "Task-Aware Visual Focus Policy",
    "World Observation and Entity Feature Policy",
    "Selective Tracking Adapter Policy",
    "Visual-OCR-Map-Task Feedback DryRun",
    "Basic Navigation Loop Vision Strengthening DryRun",
    "Post-DryRun Review",
    "Closure",
]

ROUTE_OPTIONS = [
    {
        "route_id": "A",
        "route_name": "Map / Location Read-Only Context Policy",
        "route_type": "policy",
        "readiness_level": "high",
        "dependency": [
            "vision strengthening closure",
            "feedback dryrun map/memory context hint chain",
            "task-driven perception baseline",
        ],
        "risk_level": "low",
        "expected_value": "high",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "reduces downstream ambiguity around map/location hint contracts",
        "recommended_priority": "P0",
        "selected_now": True,
        "defer_reason": "",
        "recommended_phase_name": NEXT_PHASE,
    },
    {
        "route_id": "B",
        "route_name": "Controlled Frame Input Planning / Policy",
        "route_type": "planning_policy",
        "readiness_level": "medium",
        "dependency": [
            "map/location read-only context boundary",
            "privacy filtering boundary",
            "view quality governance",
        ],
        "risk_level": "medium",
        "expected_value": "high",
        "runtime_risk": "medium",
        "write_risk": "low",
        "governance_debt_impact": "clarifies future frame governance without enabling camera",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "map/location hint contract should land first because it unlocks task-context gains at lower risk",
        "recommended_phase_name": "Phase-Controlled-Frame-Input-Planning-v1-001",
    },
    {
        "route_id": "C",
        "route_name": "Crossing Decision Safety Governance Policy",
        "route_type": "safety_governance_policy",
        "readiness_level": "medium",
        "dependency": [
            "navigation safety semantics",
            "crossing uncertainty boundary",
            "traffic and crowd candidate policy",
        ],
        "risk_level": "high",
        "expected_value": "high",
        "runtime_risk": "high",
        "write_risk": "low",
        "governance_debt_impact": "isolates a high-risk decision area before any runtime crossing language",
        "recommended_priority": "P0",
        "selected_now": False,
        "defer_reason": "important but should follow the read-only context contract because route-stage and location hints improve the governance surface first",
        "recommended_phase_name": "Phase-Crossing-Decision-Safety-Governance-Policy-v1-001",
    },
    {
        "route_id": "D",
        "route_name": "MidPlatform Function Governance / Consolidation",
        "route_type": "governance_consolidation",
        "readiness_level": "medium",
        "dependency": [
            "more route surfaces become explicit",
            "governance debt carryover",
        ],
        "risk_level": "medium",
        "expected_value": "medium",
        "runtime_risk": "low",
        "write_risk": "low",
        "governance_debt_impact": "directly reduces schema sprawl and duplicated governance modules",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "should remain queued, but a single new read-only context policy can land before broader consolidation",
        "recommended_phase_name": "Phase-MidPlatform-Function-Governance-Consolidation-v1-001",
    },
    {
        "route_id": "E",
        "route_name": "Minimal Controlled Runtime Trial Planning",
        "route_type": "trial_planning",
        "readiness_level": "low",
        "dependency": [
            "map/location context policy",
            "controlled frame input planning",
            "crossing safety governance",
        ],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "medium",
        "governance_debt_impact": "premature runtime planning would amplify unresolved boundaries",
        "recommended_priority": "P1",
        "selected_now": False,
        "defer_reason": "runtime trial planning stays later because current mainline is still explicitly non-runtime",
        "recommended_phase_name": "Phase-Minimal-Controlled-Runtime-Trial-Planning-v1-001",
    },
    {
        "route_id": "F",
        "route_name": "Exploration Drive Policy",
        "route_type": "future_policy_candidate",
        "readiness_level": "low",
        "dependency": [
            "task-driven perception strengthening first",
            "map/location context formalization",
            "WML governance readiness",
        ],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "high",
        "write_risk": "high",
        "governance_debt_impact": "would explode scope if introduced before task-first and safety-first boundaries are stronger",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "future roadmap only; must not bypass MidPlatform and Safety arbitration",
        "recommended_phase_name": "Phase-Exploration-Drive-Policy-v1-001",
    },
    {
        "route_id": "G",
        "route_name": "WorldModel Candidate Layer",
        "route_type": "future_candidate_layer",
        "readiness_level": "low",
        "dependency": [
            "world observation candidate maturity",
            "entity governance",
            "fact admission governance",
        ],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "needs strong admission controls before any candidate aggregation grows",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "deferred until entity resolution and fact admission remain explicitly outside the mainline",
        "recommended_phase_name": "Phase-WorldModel-Candidate-Layer-v1-001",
    },
    {
        "route_id": "H",
        "route_name": "Memory / Library Governance",
        "route_type": "future_governance",
        "readiness_level": "low",
        "dependency": [
            "WML boundary governance",
            "memory consolidation policy",
            "library experience governance",
        ],
        "risk_level": "high",
        "expected_value": "medium",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "must stay deferred to preserve no-write guarantees",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "memory and library remain explicitly deferred while task-driven perception is still being strengthened",
        "recommended_phase_name": "Phase-Memory-Library-Governance-v1-001",
    },
    {
        "route_id": "I",
        "route_name": "Emotion Map / Affective Engine",
        "route_type": "future_affective_candidate",
        "readiness_level": "very_low",
        "dependency": [
            "real world event chain",
            "relationship grounding",
            "memory governance",
            "worldmodel governance",
        ],
        "risk_level": "high",
        "expected_value": "long_term",
        "runtime_risk": "medium",
        "write_risk": "high",
        "governance_debt_impact": "must remain late because affective interpretation without grounded memory would be structurally unsound",
        "recommended_priority": "P2",
        "selected_now": False,
        "defer_reason": "wait until real-world information, event chain, relationship, and memory governance are mature",
        "recommended_phase_name": "Phase-Emotion-Map-Affective-Engine-v1-001",
    },
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
    "midplatform capability expansion debt",
    "resource budget complexity",
    "privacy filtering complexity",
    "conflict correction complexity",
    "temporary facility governance complexity",
    "world observation handoff complexity",
    "duplicated schema risk",
    "visual focus policy complexity",
    "selective tracking policy complexity",
    "feedback candidate proliferation",
    "map/location context contract gap",
    "crossing safety governance gap",
    "controlled frame input governance gap",
]

NON_CLAIMS = [
    "roadmap decision 不等于 runtime enablement",
    "roadmap decision 不等于 live navigation",
    "roadmap priority 不等于 production readiness",
    "selected next phase 不等于 camera 接入",
    "selected next phase 不等于 map API 接入",
    "selected next phase 不等于 OCR provider 接入",
    "selected next phase 不等于 tracking runtime 接入",
    "Map / Location Read-Only Context Policy 不等于真实地图调用",
    "Controlled Frame Input Planning 不等于 live camera",
    "Crossing Decision Safety Governance 不等于允许过街动作",
    "MidPlatform Function Governance 不等于新增 runtime module",
    "Exploration Drive Policy 当前不进入 runtime",
    "WorldModel Candidate Layer 当前不进入 fact admission",
    "Memory / Library Governance 当前不进入 write path",
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
        "roadmap_decision_only": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
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


def run_post_vision_strengthening_roadmap_decision_v1(
    *,
    vision_strengthening_closure_root: str,
    post_dryrun_review_root: str,
    dryrun_root: str,
    visual_ocr_map_task_feedback_root: str,
    selective_tracking_root: str,
    world_observation_entity_feature_root: str,
    task_aware_visual_focus_root: str,
    midplatform_perception_orchestration_root: str,
    return_to_vision_planning_root: str,
    return_to_vision_preplan_root: str,
    minimal_runtime_integration_closure_root: str,
    ocr_final_closure_root: str,
    basic_navigation_loop_stabilization_root: Optional[str] = None,
    safety_task_arbitration_policy_root: Optional[str] = None,
    navigation_guidance_speech_adapter_root: Optional[str] = None,
    voice_interruption_governance_dryrun_root: Optional[str] = None,
    voice_command_ownership_gate_policy_root: Optional[str] = None,
    map_location_readonly_context_policy_root: Optional[str] = None,
    map_route_location_context_integration_root: Optional[str] = None,
    gps_route_context_dryrun_root: Optional[str] = None,
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {
        spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"])
        for spec in ROOT_SPECS
    }

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
    preplan_gate = _read_json(roots["return_to_vision_preplan"]["root"] / "preplan_readiness_gate.json") if roots["return_to_vision_preplan"]["root"] else {}
    closure_summary_payload = _read_json(roots["vision_strengthening_closure"]["root"] / "vision_strengthening_closure_summary.json") if roots["vision_strengthening_closure"]["root"] else {}

    vision_strengthening_closure_input_loaded = roots["vision_strengthening_closure"]["loaded"] and summaries["vision_strengthening_closure"].get("final_decision") == VISION_STRENGTHENING_CLOSURE_DECISION
    post_dryrun_review_input_loaded = roots["post_dryrun_review"]["loaded"] and summaries["post_dryrun_review"].get("final_decision") == POST_REVIEW_DECISION
    dryrun_input_loaded = roots["dryrun"]["loaded"] and summaries["dryrun"].get("final_decision") == DRYRUN_DECISION
    visual_ocr_map_task_feedback_input_loaded = roots["visual_ocr_map_task_feedback"]["loaded"] and summaries["visual_ocr_map_task_feedback"].get("final_decision") == FEEDBACK_DRYRUN_DECISION
    selective_tracking_input_loaded = roots["selective_tracking"]["loaded"] and summaries["selective_tracking"].get("final_decision") == TRACKING_DECISION
    world_observation_entity_feature_input_loaded = roots["world_observation_entity_feature"]["loaded"] and summaries["world_observation_entity_feature"].get("final_decision") == WORLDOBS_DECISION
    task_aware_visual_focus_input_loaded = roots["task_aware_visual_focus"]["loaded"] and summaries["task_aware_visual_focus"].get("final_decision") == VISUAL_FOCUS_DECISION
    midplatform_perception_orchestration_input_loaded = roots["midplatform_perception_orchestration"]["loaded"] and summaries["midplatform_perception_orchestration"].get("final_decision") == MIDPLATFORM_DECISION
    return_to_vision_planning_input_loaded = roots["return_to_vision_planning"]["loaded"] and summaries["return_to_vision_planning"].get("final_decision") == PLANNING_DECISION
    return_to_vision_preplan_input_loaded = roots["return_to_vision_preplan"]["loaded"] and summaries["return_to_vision_preplan"].get("preplan_ready_for_formal_phase_decision") is True and (preplan_gate or {}).get("final_assessment", {}).get("preplan_ready_for_formal_phase_decision") is True
    minimal_runtime_integration_closure_loaded = roots["minimal_runtime_integration_closure"]["loaded"] and summaries["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    ocr_final_closure_loaded = roots["ocr_final_closure"]["loaded"] and summaries["ocr_final_closure"].get("final_decision") == OCR_DECISION

    current_mainline_status_summary = {
        "current_mainline_status": "vision_strengthening_closed_waiting_for_next_policy_line",
        "basic_navigation_loop_vision_strengthening_closed": True,
        "policy_chain_closed": bool(summaries["vision_strengthening_closure"].get("policy_chain_closed")),
        "dryrun_chain_closed": bool(summaries["vision_strengthening_closure"].get("dryrun_chain_closed")),
        "feedback_chain_closed": bool(summaries["vision_strengthening_closure"].get("feedback_chain_closed")),
        "navigation_loop_vision_strengthening_closed": bool(summaries["vision_strengthening_closure"].get("navigation_loop_vision_strengthening_closed")),
        "runtime_enabled": False,
        "live_navigation_claimed": False,
        "production_readiness_claimed": False,
        "source_closure_ref": "_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0/vision_strengthening_closure_summary.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    completed_capability_summary = {
        "capabilities": [
            {
                "capability_name": item,
                "completion_level": "policy_or_dryrun_or_closure",
                "runtime_enabled": False,
                "production_ready": False,
                "live_navigation_ready": False,
                "note": "completed at policy / dry-run / closure level only",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for item in COMPLETED_CAPABILITIES
        ],
        "completed_capability_count": len(COMPLETED_CAPABILITIES),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    route_option_matrix = {
        "routes": [
            {**route, "source_chain": SOURCE_CHAIN, **_not_fact()}
            for route in ROUTE_OPTIONS
        ],
        "route_option_count": len(ROUTE_OPTIONS),
        "selected_route_id": "A",
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
        "task_driven_perception_priority_first": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    recommended_next_phase_decision = {
        "decision_id": DECISION_ID,
        "decision_scope": DECISION_SCOPE,
        "source_closure_ref": "_eval_out/basic_navigation_loop_vision_strengthening_closure_v1_smoke_v0/vision_strengthening_closure_summary.json",
        "current_mainline_status": current_mainline_status_summary["current_mainline_status"],
        "completed_capability_summary_ref": "completed_capability_summary.json",
        "deferred_capability_summary_ref": "deferred_worldmodel_memory_library_emotion_register.json",
        "route_option_matrix_ref": "route_option_matrix.json",
        "priority_ranking_ref": "priority_ranking.json",
        "selected_next_phase": NEXT_PHASE,
        "rejected_or_deferred_routes": [
            route["route_name"] for route in ROUTE_OPTIONS if not route["selected_now"]
        ],
        "decision_reason": [
            "visual/OCR/map/memory feedback chain is already dry-run linked and benefits directly from formal read-only context contracts",
            "map/location read-only context strengthens task-driven navigation without opening action permissions",
            "risk is lower than controlled frame input or any runtime planning",
            "the route preserves no-runtime, no-write, and no-live-navigation boundaries",
            "it provides route-stage, side-of-path, proximity, and location hint contracts for future task-first perception",
        ],
        "boundary_freeze_ref": "boundary_freeze.json",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_exploration_drive_register = {
        "capability_name": "Survival-Oriented Exploration Drive / Adaptive Exploration Layer",
        "current_status": "deferred_future_candidate",
        "priority": "P2",
        "runtime_allowed_now": False,
        "direct_action_allowed": False,
        "worldmodel_write_allowed": False,
        "memory_write_allowed": False,
        "fact_write_allowed": False,
        "exploration_directions": DEFERRED_EXPLORATION_DIRECTIONS,
        "defer_reason": [
            "task-driven perception should be strengthened first",
            "world observation candidate layer exists but runtime not enabled",
            "map/location context not yet formalized",
            "memory/worldmodel/library governance deferred",
            "exploration must not bypass MidPlatform/Safety arbitration",
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
                "defer_reason": "entity fusion and fact admission remain deferred",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "capability_name": "Memory / Library Governance",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "defer_reason": "memory consolidation and library experience commit remain deferred",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            },
            {
                "capability_name": "Emotion Map / Affective Engine",
                "current_status": "deferred_future_candidate",
                "priority": "P2",
                "runtime_allowed_now": False,
                "write_allowed_now": False,
                "defer_reason": "requires grounded world information, event chains, relationship context, and memory governance first",
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
        "no_live_navigation": True,
        "no_production_readiness": True,
        "no_camera": True,
        "no_map_api": True,
        "no_ocr_provider": True,
        "no_tracking_runtime": True,
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
            {
                "topic": topic,
                "impact_on_roadmap": "must remain visible during next-phase prioritization",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for topic in GOVERNANCE_DEBT_TOPICS
        ],
        "midplatform_function_governance_retained_in_p1": True,
        "map_location_contract_gap_selected_for_p0": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    non_claims_register = {
        "non_claims": NON_CLAIMS,
        "live_navigation_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "priority_level": "P0",
        "route_name": "Map / Location Read-Only Context Policy",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    blockers = []
    required_flags = [
        vision_strengthening_closure_input_loaded,
        post_dryrun_review_input_loaded,
        dryrun_input_loaded,
        visual_ocr_map_task_feedback_input_loaded,
        selective_tracking_input_loaded,
        world_observation_entity_feature_input_loaded,
        task_aware_visual_focus_input_loaded,
        midplatform_perception_orchestration_input_loaded,
        return_to_vision_planning_input_loaded,
        return_to_vision_preplan_input_loaded,
        minimal_runtime_integration_closure_loaded,
        ocr_final_closure_loaded,
    ]
    if not all(required_flags):
        blockers.append("required_root_missing_or_invalid")

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "vision_strengthening_closure_input_loaded": vision_strengthening_closure_input_loaded,
        "post_dryrun_review_input_loaded": post_dryrun_review_input_loaded,
        "dryrun_input_loaded": dryrun_input_loaded,
        "visual_ocr_map_task_feedback_input_loaded": visual_ocr_map_task_feedback_input_loaded,
        "selective_tracking_input_loaded": selective_tracking_input_loaded,
        "world_observation_entity_feature_input_loaded": world_observation_entity_feature_input_loaded,
        "task_aware_visual_focus_input_loaded": task_aware_visual_focus_input_loaded,
        "midplatform_perception_orchestration_input_loaded": midplatform_perception_orchestration_input_loaded,
        "return_to_vision_planning_input_loaded": return_to_vision_planning_input_loaded,
        "return_to_vision_preplan_input_loaded": return_to_vision_preplan_input_loaded,
        "minimal_runtime_integration_closure_loaded": minimal_runtime_integration_closure_loaded,
        "ocr_final_closure_loaded": ocr_final_closure_loaded,
        "current_mainline_status_summary_generated": True,
        "completed_capability_summary_generated": True,
        "route_option_matrix_generated": True,
        "priority_ranking_generated": True,
        "recommended_next_phase_decision_generated": True,
        "deferred_exploration_drive_register_generated": True,
        "deferred_worldmodel_memory_library_emotion_register_generated": True,
        "boundary_freeze_generated": True,
        "governance_debt_roadmap_register_generated": True,
        "non_claims_register_generated": True,
        "route_option_count": len(ROUTE_OPTIONS),
        "p0_route_count": len(p0_routes),
        "p1_route_count": len(p1_routes),
        "p2_route_count": len(p2_routes),
        "exploration_drive_deferred": True,
        "task_driven_perception_priority_first": True,
        "worldmodel_candidate_layer_deferred": True,
        "memory_library_governance_deferred": True,
        "emotion_engine_deferred": True,
        "live_navigation_claimed": False,
        "production_readiness_claimed": False,
        "runtime_enablement_claimed": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_invoked": False,
        "bytetrack_invoked": False,
        "ocsort_invoked": False,
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
        "final_decision": FINAL_DECISION if not blockers else "POST_VISION_STRENGTHENING_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if not blockers else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "current_mainline_status_summary": current_mainline_status_summary,
        "completed_capability_summary": completed_capability_summary,
        "route_option_matrix": route_option_matrix,
        "priority_ranking": priority_ranking,
        "recommended_next_phase_decision": recommended_next_phase_decision,
        "deferred_exploration_drive_register": deferred_exploration_drive_register,
        "deferred_worldmodel_memory_library_emotion_register": deferred_worldmodel_memory_library_emotion_register,
        "boundary_freeze": boundary_freeze,
        "governance_debt_roadmap_register": governance_debt_roadmap_register,
        "non_claims_register": non_claims_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }
