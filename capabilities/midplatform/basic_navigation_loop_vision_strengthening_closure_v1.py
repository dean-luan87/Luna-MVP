# -*- coding: utf-8 -*-
"""Basic Navigation Loop Vision Strengthening Closure v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Phase-Basic-Navigation-Loop-Vision-Strengthening-Closure-v1-001"
CLOSURE_SCOPE = "basic_navigation_loop_vision_strengthening_closure_only"
SOURCE_CHAIN = "basic_navigation_loop_vision_strengthening_closure_v1"
CLOSURE_ID = "bnlvsc_v1_001"
FINAL_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Vision-Strengthening-Roadmap-Decision-v1-001"

POST_REVIEW_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
DRYRUN_DECISION = "BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FEEDBACK_DRYRUN_DECISION = "VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN_READY_FOR_BASIC_NAVIGATION_LOOP_VISION_STRENGTHENING"
TRACKING_DECISION = "SELECTIVE_TRACKING_ADAPTER_POLICY_READY_FOR_VISUAL_OCR_MAP_TASK_FEEDBACK_DRYRUN"
WORLDOBS_DECISION = "WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY_READY_FOR_SELECTIVE_TRACKING_ADAPTER_POLICY"
VISUAL_FOCUS_DECISION = "TASK_AWARE_VISUAL_FOCUS_POLICY_READY_FOR_WORLD_OBSERVATION_AND_ENTITY_FEATURE_POLICY"
MIDPLATFORM_DECISION = "MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY_READY_FOR_TASK_AWARE_VISUAL_FOCUS_POLICY"
PLANNING_DECISION = "RETURN_TO_VISION_MAINLINE_PLANNING_READY_FOR_MIDPLATFORM_PERCEPTION_ORCHESTRATION_POLICY"
PREPLAN_FINAL_DECISION = "PREPLAN_READY_FOR_FORMAL_PHASE_DECISION"
MRI_DECISION = "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE"
OCR_DECISION = "OCR_MAINLINE_FINAL_CLOSURE_RETURN_TO_VISION_MAINLINE"

ROOT_SPECS = [
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
]

COMPLETED_PHASES = [
    ("Return-To-Vision Mainline Preplan v1", "return_to_vision_preplan", "_eval_out/return_to_vision_mainline_preplan_v1/", "COMPLETE", "vision planning precondition"),
    ("Return-To-Vision Mainline Planning v1", "return_to_vision_planning", "_eval_out/return_to_vision_mainline_planning_v1_smoke_v0/", "GO", "formal planning baseline"),
    ("MidPlatform Perception Orchestration Policy v1", "midplatform_perception_orchestration", "_eval_out/midplatform_perception_orchestration_policy_v1_smoke_v0/", "GO", "perception orchestration baseline"),
    ("Task-Aware Visual Focus Policy v1", "task_aware_visual_focus", "_eval_out/task_aware_visual_focus_policy_v1_smoke_v0/", "GO", "visual focus baseline"),
    ("World Observation and Entity Feature Policy v1", "world_observation_entity_feature", "_eval_out/world_observation_and_entity_feature_policy_v1_smoke_v0/", "GO", "world observation baseline"),
    ("Selective Tracking Adapter Policy v1", "selective_tracking", "_eval_out/selective_tracking_adapter_policy_v1_smoke_v0/", "GO", "tracking candidate baseline"),
    ("Visual-OCR-Map-Task Feedback DryRun v1", "visual_ocr_map_task_feedback", "_eval_out/visual_ocr_map_task_feedback_dryrun_v1_smoke_v0/", "GO", "feedback chain baseline"),
    ("Basic Navigation Loop Vision Strengthening DryRun v1", "dryrun", "_eval_out/basic_navigation_loop_vision_strengthening_dryrun_v1_smoke_v0/", "GO", "navigation dryrun baseline"),
    ("Basic Navigation Loop Vision Strengthening Post-DryRun Review v1", "post_dryrun_review", "_eval_out/basic_navigation_loop_vision_strengthening_post_dryrun_review_v1_smoke_v0/", "GO", "closure readiness audit"),
]

VALIDATED_CAPABILITIES = [
    "MidPlatform perception orchestration policy",
    "task-aware visual focus policy",
    "scene sketch candidate schema",
    "visual focus plan schema",
    "visual focus slot schema",
    "view quality candidate",
    "active view adjustment candidate",
    "world observation candidate policy",
    "world entity feature candidate policy",
    "selective tracking adapter policy",
    "OCR activation candidate policy",
    "tracking request candidate policy",
    "map/memory context feedback candidate",
    "visual/OCR/map/task feedback dry-run",
    "basic navigation loop vision strengthening dry-run",
    "post-dryrun review",
]

DISABLED_RUNTIMES = [
    "camera runtime",
    "visual model runtime",
    "OCR provider runtime",
    "OCRRequest submission",
    "map API / 高德 API",
    "tracking runtime",
    "optical flow runtime",
    "Supervision / ByteTrack / OC-SORT",
    "Speech Gate runtime",
    "VOP runtime",
    "TTS runtime",
    "Safety-Task Arbitration runtime",
    "NavigationAction runtime",
    "WorldModel write runtime",
    "Memory write runtime",
    "Library write runtime",
    "SceneDelta runtime",
]

NON_CLAIMS = [
    "closure 不等于 live navigation",
    "dry-run 闭环不等于真实导航能力",
    "guidance candidate 不等于导航动作",
    "text-only dry output 不等于用户听见",
    "OCR activation candidate 不等于 OCRRequest 提交",
    "tracking request candidate 不等于 tracking runtime",
    "map/memory hint 不等于现实事实",
    "WorldObservationCandidate 不等于 WorldModel fact",
    "WorldEntityFeatureCandidate 不等于实体事实",
    "ObjectIdentityCandidate 不等于身份事实",
    "TemporaryFacilityCandidate 不等于固定 POI",
    "CrowdFlowFeedback 不等于跟随人流指令",
    "CrossingUncertainFeedback 不等于允许过马路",
    "SafetyArbitrationBridgeCandidate 不等于真实 arbitration runtime",
    "closure 不等于 production readiness",
]

DEFERRED_CAPABILITIES = [
    "real camera runtime",
    "visual model integration",
    "OCR provider re-enable",
    "OCRRequest gated submission for live flow",
    "map API / 高德 API integration",
    "GPS / route context runtime",
    "tracking runtime",
    "Supervision / ByteTrack / OC-SORT experiment branch",
    "optical flow runtime",
    "real Speech Gate / VOP / TTS output",
    "Safety-Task Arbitration runtime integration",
    "NavigationAction guarded runtime",
    "WorldModel Candidate Layer",
    "Memory Governance",
    "Library Experience Governance",
    "Entity Resolution",
    "Fact Admission",
    "Crossing Decision Safety Governance",
    "MidPlatform Function Governance / Consolidation",
]

DEBT_CARRYOVER_TOPICS = [
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


def _bool_summary(flag: bool) -> bool:
    return bool(flag)


def _verifier_verdict(root: Optional[Path]) -> str:
    if not root:
        return "MISSING"
    report = _read_json(root / "verifier_report.json")
    if isinstance(report, dict) and report.get("verdict"):
        return str(report["verdict"])
    return "COMPLETE"


def _boundary_payload() -> Dict[str, Any]:
    return {
        "closure_only": True,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "camera_invoked": False,
        "visual_model_invoked": False,
        "map_api_invoked": False,
        "ocr_provider_invoked": False,
        "ocrrequest_submitted": False,
        "tracking_runtime_invoked": False,
        "optical_flow_runtime_invoked": False,
        "supervision_imported": False,
        "supervision_invoked": False,
        "bytetrack_imported": False,
        "bytetrack_invoked": False,
        "ocsort_imported": False,
        "ocsort_invoked": False,
        "safety_task_arbitration_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "user_heard_assumed": False,
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
        "full_frame_ocr_allowed": False,
        "full_scene_tracking_allowed": False,
        "crowd_flow_follow_action_allowed": False,
        "crossing_action_instruction_allowed": False,
        "fixed_poi_commit_allowed": False,
        "identity_fact_allowed": False,
        "emotional_attachment_fact_allowed": False,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_basic_navigation_loop_vision_strengthening_closure_v1(
    *,
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
) -> Dict[str, Any]:
    args = locals().copy()
    roots = {
        spec["id"]: _load_root(args[spec["arg"]], spec["summary"], spec["artifacts"])
        for spec in ROOT_SPECS
    }

    input_root_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        input_root_rows.append(
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

    summary = {key: roots[key]["summary"] for key in roots}
    preplan_gate = _read_json(roots["return_to_vision_preplan"]["root"] / "preplan_readiness_gate.json") if roots["return_to_vision_preplan"]["root"] else {}

    post_dryrun_review_input_loaded = roots["post_dryrun_review"]["loaded"] and summary["post_dryrun_review"].get("final_decision") == POST_REVIEW_DECISION
    dryrun_input_loaded = roots["dryrun"]["loaded"] and summary["dryrun"].get("final_decision") == DRYRUN_DECISION
    visual_ocr_map_task_feedback_input_loaded = roots["visual_ocr_map_task_feedback"]["loaded"] and summary["visual_ocr_map_task_feedback"].get("final_decision") == FEEDBACK_DRYRUN_DECISION
    selective_tracking_input_loaded = roots["selective_tracking"]["loaded"] and summary["selective_tracking"].get("final_decision") == TRACKING_DECISION
    world_observation_entity_feature_input_loaded = roots["world_observation_entity_feature"]["loaded"] and summary["world_observation_entity_feature"].get("final_decision") == WORLDOBS_DECISION
    task_aware_visual_focus_input_loaded = roots["task_aware_visual_focus"]["loaded"] and summary["task_aware_visual_focus"].get("final_decision") == VISUAL_FOCUS_DECISION
    midplatform_perception_orchestration_input_loaded = roots["midplatform_perception_orchestration"]["loaded"] and summary["midplatform_perception_orchestration"].get("final_decision") == MIDPLATFORM_DECISION
    return_to_vision_planning_input_loaded = roots["return_to_vision_planning"]["loaded"] and summary["return_to_vision_planning"].get("final_decision") == PLANNING_DECISION
    return_to_vision_preplan_input_loaded = roots["return_to_vision_preplan"]["loaded"] and summary["return_to_vision_preplan"].get("preplan_ready_for_formal_phase_decision") is True and (preplan_gate or {}).get("final_assessment", {}).get("preplan_ready_for_formal_phase_decision") is True
    minimal_runtime_integration_closure_loaded = roots["minimal_runtime_integration_closure"]["loaded"] and summary["minimal_runtime_integration_closure"].get("final_decision") == MRI_DECISION
    ocr_final_closure_loaded = roots["ocr_final_closure"]["loaded"] and summary["ocr_final_closure"].get("final_decision") == OCR_DECISION

    completed_phase_rows = []
    for phase_id, intake_id, output_dir, status, role in COMPLETED_PHASES:
        final_decision = summary[intake_id].get("final_decision")
        if intake_id == "return_to_vision_preplan":
            final_decision = PREPLAN_FINAL_DECISION
        completed_phase_rows.append(
            {
                "phase_id": phase_id,
                "status": status,
                "output_dir": output_dir,
                "verifier_verdict": _verifier_verdict(roots[intake_id]["root"]),
                "final_decision": final_decision,
                "role_in_closure": role,
                "runtime_enabled": False,
                "write_enabled": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    validated_capability_summary = {
        "validated_capabilities": [
            {
                "capability_name": item,
                "validation_level": "policy_or_dryrun",
                "runtime_enablement": False,
                "note": "policy / schema / candidate / dry-run validation; not runtime enablement",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for item in VALIDATED_CAPABILITIES
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    disabled_runtime_summary = {
        "disabled_runtime_capabilities": [
            {
                "runtime_name": item,
                "enabled": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for item in DISABLED_RUNTIMES
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    closure_boundary_freeze = {
        "no_runtime": True,
        "no_write": True,
        "no_action": True,
        "no_speech": True,
        "no_fact": True,
        "candidate_only": True,
        "handoff_only_for_worldmodel_memory_library": True,
        "no_entity_resolution": True,
        "no_fact_admission": True,
        "no_memory_consolidation": True,
        "no_library_experience_commit": True,
        "no_full_frame_ocr": True,
        "no_full_scene_tracking": True,
        "no_crowd_flow_follow_action": True,
        "no_crossing_action_instruction": True,
        "no_fixed_poi_commit_for_temporary_facility": True,
        "no_identity_fact": True,
        "no_emotional_attachment_fact": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    vision_strengthening_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "production_readiness_claimed": False,
        "live_navigation_claimed": False,
        "runtime_enablement_claimed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    deferred_capability_pool = {
        "deferred_capabilities": [
            {
                "capability_name": item,
                "deferred": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for item in DEFERRED_CAPABILITIES
        ],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_carryover = {
        "carryover_items": [
            {
                "topic": topic,
                "carried_over": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
            for topic in DEBT_CARRYOVER_TOPICS
        ],
        "future_midplatform_function_governance_required": True,
        "no_duplicate_governance_module_allowed": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    policy_chain_closed = all(
        [
            return_to_vision_planning_input_loaded,
            midplatform_perception_orchestration_input_loaded,
            task_aware_visual_focus_input_loaded,
            world_observation_entity_feature_input_loaded,
            selective_tracking_input_loaded,
        ]
    )
    feedback_chain_closed = visual_ocr_map_task_feedback_input_loaded
    dryrun_chain_closed = dryrun_input_loaded and post_dryrun_review_input_loaded
    navigation_loop_vision_strengthening_closed = policy_chain_closed and feedback_chain_closed and dryrun_chain_closed

    blockers = []
    if not all(
        [
            post_dryrun_review_input_loaded,
            dryrun_input_loaded,
            visual_ocr_map_task_feedback_input_loaded,
            selective_tracking_input_loaded,
            world_observation_entity_feature_input_loaded,
            task_aware_visual_focus_input_loaded,
            midplatform_perception_orchestration_input_loaded,
            return_to_vision_planning_input_loaded,
            minimal_runtime_integration_closure_loaded,
            ocr_final_closure_loaded,
        ]
    ):
        blockers.append("required_root_missing")
    if not navigation_loop_vision_strengthening_closed:
        blockers.append("vision_strengthening_chain_not_closed")

    closure_readiness_gate = {
        "go_conditions": [
            "post_dryrun_review_loaded",
            "dryrun_loaded",
            "feedback_dryrun_loaded",
            "selective_tracking_policy_loaded",
            "world_observation_policy_loaded",
            "visual_focus_policy_loaded",
            "midplatform_orchestration_policy_loaded",
            "all_required_phase_statuses_go_or_complete",
            "no_runtime_boundary_pass",
            "no_write_boundary_pass",
            "no_action_boundary_pass",
            "no_speech_boundary_pass",
            "non_claims_generated",
            "deferred_capability_pool_generated",
            "governance_debt_carryover_generated",
            "next_phase_fixed",
        ],
        "no_go_conditions": [
            "any_required_root_missing",
            "any_runtime_enabled",
            "any_write_enabled",
            "any_navigation_action_triggered",
            "any_speech_output_invoked",
            "any_fact_written",
            "entity_resolution_enabled",
            "fact_admission_enabled",
            "tracking_runtime_enabled",
            "ocr_provider_enabled",
            "map_api_enabled",
            "closure_claims_production_readiness",
            "next_phase_unclear",
        ],
        "ready_for_closure": not blockers,
        "verdict": "GO" if not blockers else "NO_GO",
        "blockers": blockers,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    vision_strengthening_closure_summary = {
        "closure_id": CLOSURE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "source_phase_chain": [row["phase_id"] for row in completed_phase_rows],
        "completed_phase_count": len(completed_phase_rows),
        "completed_phase_matrix_ref": "completed_phase_matrix.json",
        "validated_capability_summary_ref": "validated_capability_summary.json",
        "disabled_runtime_summary_ref": "disabled_runtime_summary.json",
        "boundary_freeze_ref": "closure_boundary_freeze.json",
        "non_claims_register_ref": "vision_strengthening_non_claims_register.json",
        "deferred_capability_pool_ref": "deferred_capability_pool.json",
        "governance_debt_carryover_ref": "governance_debt_carryover.json",
        "next_phase_recommendation": NEXT_PHASE,
        "final_decision": FINAL_DECISION,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    result_summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
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
        "completed_phase_matrix_generated": True,
        "completed_phase_count": len(completed_phase_rows),
        "validated_capability_summary_generated": True,
        "disabled_runtime_summary_generated": True,
        "closure_boundary_freeze_generated": True,
        "non_claims_register_generated": True,
        "deferred_capability_pool_generated": True,
        "governance_debt_carryover_generated": True,
        "closure_readiness_gate_generated": True,
        "policy_chain_closed": policy_chain_closed,
        "dryrun_chain_closed": dryrun_chain_closed,
        "feedback_chain_closed": feedback_chain_closed,
        "navigation_loop_vision_strengthening_closed": navigation_loop_vision_strengthening_closed,
        "production_readiness_claimed": False,
        "live_navigation_claimed": False,
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
        "supervision_imported": False,
        "supervision_invoked": False,
        "bytetrack_imported": False,
        "bytetrack_invoked": False,
        "ocsort_imported": False,
        "ocsort_invoked": False,
        "safety_task_arbitration_runtime_invoked": False,
        "speech_gate_invoked": False,
        "vop_invoked": False,
        "tts_invoked": False,
        "user_heard_assumed": False,
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
        "full_frame_ocr_allowed": False,
        "full_scene_tracking_allowed": False,
        "crowd_flow_follow_action_allowed": False,
        "crossing_action_instruction_allowed": False,
        "fixed_poi_commit_allowed": False,
        "identity_fact_allowed": False,
        "emotional_attachment_fact_allowed": False,
        "handoff_candidate_not_fact": True,
        "placeholder_not_runtime": True,
        "boundary_ok": True,
        "violations": [],
        "final_decision": FINAL_DECISION,
        "recommended_next_phase": NEXT_PHASE,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": result_summary,
        "input_root_matrix": {"rows": input_root_rows, "row_count": len(input_root_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "vision_strengthening_closure_summary": vision_strengthening_closure_summary,
        "completed_phase_matrix": {"phases": completed_phase_rows, "completed_phase_count": len(completed_phase_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "validated_capability_summary": validated_capability_summary,
        "disabled_runtime_summary": disabled_runtime_summary,
        "closure_boundary_freeze": closure_boundary_freeze,
        "vision_strengthening_non_claims_register": vision_strengthening_non_claims_register,
        "deferred_capability_pool": deferred_capability_pool,
        "governance_debt_carryover": governance_debt_carryover,
        "closure_readiness_gate": closure_readiness_gate,
        "next_phase_recommendation": next_phase_recommendation,
        "no_runtime_boundary_report": _boundary_payload(),
        "no_write_boundary_report": _boundary_payload(),
    }
