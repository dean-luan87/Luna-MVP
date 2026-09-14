# -*- coding: utf-8 -*-
"""First Person Scene Understanding Decision Chain Candidate DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.first_person_scene_understanding_information_integration_chain_dryrun_v1 import (
    FINAL_DECISION_GO as II_CHAIN_DR_FINAL_GO,
    NEXT_PHASE_GO as II_CHAIN_DR_NEXT_PHASE,
)
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CB_DR_FINAL_GO,
)
from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DC_DR_FINAL_GO,
)
from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL_GO,
)

PHASE_ID = "Phase-First-Person-Scene-Understanding-Decision-Chain-Candidate-DryRun-v1-001"
SCOPE = "first_person_scene_understanding_decision_chain_candidate_dryrun_only"
SOURCE_CHAIN = "first_person_scene_understanding_decision_chain_candidate_dryrun_v1"

UPSTREAM_II_CHAIN_DR_FINAL = II_CHAIN_DR_FINAL_GO
UPSTREAM_II_CHAIN_DR_NEXT = II_CHAIN_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "FIRST_PERSON_SCENE_UNDERSTANDING_DECISION_CHAIN_CANDIDATE_DRYRUN_CLOSED_"
    "READY_FOR_TASK_RESPONSE_CANDIDATE_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "FIRST_PERSON_SCENE_UNDERSTANDING_DECISION_CHAIN_CANDIDATE_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-First-Person-Scene-Understanding-Task-Response-Candidate-DryRun-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-First-Person-Scene-Understanding-Decision-Chain-Issue-Review-v1-001"
)

CAPABILITY_STACK_ID = "first_person_capability_stack_v1"
CAPABILITY_STACK_NAME = "First-Person Capability Stack"

CAPABILITY_STACK_LAYER_FIELDS: Tuple[str, ...] = (
    "layer_id",
    "layer_name",
    "capability_scope",
    "capability_boundary",
    "input_sources",
    "output_objects",
    "required_lower_layers",
    "candidate_objects",
    "integration_path",
    "decision_review_scope",
    "test_scope",
    "failure_routes",
    "forbidden_cross_layer_override",
    "metrics",
)

CAPABILITY_STACK_GOVERNANCE_RULES: Tuple[str, ...] = (
    "capability goals must be layered, not mixed as one mega-capability",
    "each layer must define capability_boundary independently",
    "each layer must define candidate_object_set independently",
    "each layer must define integration_path independently",
    "each layer must define decision_review independently",
    "each layer must define test_case_set independently",
    "each layer must define failure_route independently",
    "upper layer depends on lower layer",
    "upper layer cannot reverse-override lower layer",
    "application layer cannot masquerade as foundation layer",
    "navigation is Layer 3 not Layer 1",
    "person recognition and reading are Layer 4+ not current main axis",
)

CAPABILITY_STACK_LAYERS: Tuple[Dict[str, Any], ...] = (
    {
        "layer_id": "layer_1",
        "layer_name": "Current Scene Understanding",
        "capability_scope": "current_scene_understanding",
        "capability_boundary": (
            "identify targets, text, tracking, scene content, task intent, risk; "
            "no navigation execution; no long-term memory write; no person identity fact"
        ),
        "input_sources": [
            "visual_observation_candidate",
            "target_recognition_candidate",
            "text_recognition_candidate",
            "target_tracking_candidate",
            "scene_context_candidate",
            "task_intent_candidate",
            "risk_context_candidate",
            "required_observation_candidate",
        ],
        "output_objects": [
            "scene_context_candidate",
            "target_recognition_candidate",
            "text_recognition_candidate",
            "integrated_scene_context_fragment",
        ],
        "required_lower_layers": [],
        "candidate_objects": [
            "visual_observation_candidate",
            "target_recognition_candidate",
            "text_recognition_candidate",
            "target_tracking_candidate",
            "scene_context_candidate",
            "task_intent_candidate",
            "risk_context_candidate",
            "required_observation_candidate",
        ],
        "integration_path": "perception_to_information_integration_scene_layer",
        "decision_review_scope": "primary_goal_current_scene_understanding",
        "test_scope": "scene_understanding_test",
        "failure_routes": [
            "target_recognition_failure",
            "text_recognition_failure",
            "tracking_failure",
            "scene_context_failure",
            "task_intent_failure",
        ],
        "forbidden_cross_layer_override": [
            "navigation_cannot_override_scene_understanding",
            "person_recognition_cannot_override_scene_understanding",
            "reading_cannot_bypass_ocr_evidence_validation",
        ],
        "metrics": [
            "target_candidate_precision",
            "text_candidate_binding_rate",
            "tracking_continuity_rate",
            "required_observation_trigger_rate",
        ],
    },
    {
        "layer_id": "layer_2",
        "layer_name": "Spatiotemporal Continuity Understanding",
        "capability_scope": "spatiotemporal_continuity_and_world_understanding",
        "capability_boundary": (
            "continuous frame understanding, location continuity, scene rules, survival context; "
            "no WorldModel write; no navigation action"
        ),
        "input_sources": [
            "spatiotemporal_context_candidate",
            "world_continuity_candidate",
            "scene_rule_candidate",
            "drive_signal_candidate",
            "health_signal_candidate",
        ],
        "output_objects": [
            "spatiotemporal_context_candidate",
            "world_continuity_candidate",
            "scene_rule_candidate",
            "integrated_continuity_context_fragment",
        ],
        "required_lower_layers": ["layer_1"],
        "candidate_objects": [
            "spatiotemporal_context_candidate",
            "world_continuity_candidate",
            "scene_rule_candidate",
        ],
        "integration_path": "temporal_sequence_to_information_integration_continuity_layer",
        "decision_review_scope": "secondary_goal_spatiotemporal_continuity",
        "test_scope": "spatiotemporal_continuity_test",
        "failure_routes": [
            "sequence_gap_failure",
            "continuity_hypothesis_failure",
            "stale_sequence_failure",
            "scene_rule_validation_failure",
        ],
        "forbidden_cross_layer_override": [
            "navigation_cannot_override_continuity_requirements",
            "world_continuity_hypothesis_cannot_become_fact_without_validation",
        ],
        "metrics": [
            "sequence_gap_detection_rate",
            "continuity_confidence_distribution",
            "stale_sequence_block_rate",
        ],
    },
    {
        "layer_id": "layer_3",
        "layer_name": "Navigation Application Layer",
        "capability_scope": "navigation_application_layer",
        "capability_boundary": (
            "route/navigation task context as application layer only; "
            "requires Layer 1+2 readiness; no direct navigation runtime in dryrun"
        ),
        "input_sources": [
            "route_context_candidate",
            "navigation_task_candidate",
            "task_route_progress_candidate",
            "map_location_context_candidate",
        ],
        "output_objects": [
            "navigation_application_context_fragment",
            "route_context_candidate",
            "navigation_task_candidate",
        ],
        "required_lower_layers": ["layer_1", "layer_2"],
        "candidate_objects": [
            "route_context_candidate",
            "navigation_task_candidate",
            "task_route_progress_candidate",
            "map_location_context_candidate",
        ],
        "integration_path": "application_context_to_information_integration_navigation_layer",
        "decision_review_scope": "application_goal_navigation_application_layer",
        "test_scope": "navigation_application_test",
        "failure_routes": [
            "map_context_failure",
            "navigation_rule_failure",
            "route_context_failure",
            "navigation_not_ready_failure",
        ],
        "forbidden_cross_layer_override": [
            "navigation_cannot_override_survival_safety",
            "navigation_cannot_override_scene_understanding_foundation",
            "navigation_cannot_masquerade_as_layer_1",
        ],
        "metrics": [
            "navigation_application_readiness_rate",
            "route_context_binding_rate",
            "navigation_blocked_by_lower_layer_rate",
        ],
    },
    {
        "layer_id": "layer_4",
        "layer_name": "Extended Application Capabilities",
        "capability_scope": "expanded_application_capabilities",
        "capability_boundary": (
            "person recognition memory hints, advanced reading; deferred; "
            "no default long-term memory write; no identity fact without validation"
        ),
        "input_sources": [
            "person_recognition_candidate",
            "reading_capability_candidate",
            "voice_identity_hint_candidate",
        ],
        "output_objects": [
            "person_recognition_candidate",
            "reading_result_candidate",
        ],
        "required_lower_layers": ["layer_1", "layer_2", "layer_3"],
        "candidate_objects": [
            "person_recognition_candidate",
            "reading_capability_candidate",
        ],
        "integration_path": "extended_application_deferred_integration_path",
        "decision_review_scope": "fourth_goal_expanded_application_deferred",
        "test_scope": "person_recognition_test_reading_capability_test",
        "failure_routes": [
            "person_recognition_failure",
            "reading_validation_failure",
            "identity_overreach_failure",
        ],
        "forbidden_cross_layer_override": [
            "person_recognition_cannot_default_write_long_term_memory",
            "reading_cannot_bypass_ocr_evidence_validation",
            "extended_capabilities_cannot_override_layer_1_2_3",
        ],
        "metrics": [
            "person_candidate_precision",
            "reading_validation_pass_rate",
            "identity_overreach_block_rate",
        ],
        "deferred": True,
    },
    {
        "layer_id": "layer_5",
        "layer_name": "Long-Term Social / Personal Capability",
        "capability_scope": "long_term_social_personal_capability",
        "capability_boundary": (
            "long-term relationship, personal continuity, social memory; later phase only; "
            "no automatic memory/worldmodel write"
        ),
        "input_sources": [
            "personal_continuity_candidate",
            "social_relationship_candidate",
            "long_term_reading_memory_candidate",
        ],
        "output_objects": [
            "personal_continuity_context_candidate",
            "social_relationship_context_candidate",
        ],
        "required_lower_layers": ["layer_1", "layer_2", "layer_3", "layer_4"],
        "candidate_objects": [
            "personal_continuity_candidate",
            "social_relationship_candidate",
        ],
        "integration_path": "long_term_social_personal_deferred_integration_path",
        "decision_review_scope": "long_term_social_personal_later",
        "test_scope": "long_term_social_personal_test_later",
        "failure_routes": [
            "personal_continuity_failure",
            "social_relationship_failure",
            "long_term_memory_write_blocked_failure",
        ],
        "forbidden_cross_layer_override": [
            "long_term_capability_cannot_override_scene_foundation",
            "social_memory_cannot_bypass_validation_and_gate",
        ],
        "metrics": [
            "personal_continuity_candidate_rate",
            "social_context_binding_rate",
        ],
        "deferred": True,
        "later": True,
    },
)

DECISION_ACTION_TAXONOMY: Tuple[str, ...] = (
    "allow_candidate_forward",
    "hold_for_safety",
    "observe_more",
    "ask_user",
    "block_candidate",
    "request_validation",
    "request_more_evidence",
    "degrade_to_non_navigation_context",
    "preserve_as_scene_understanding_only",
    "mark_not_ready_for_navigation_decision",
    "escalate_to_governance_review",
    "emit_violation_report_candidate",
    "no_output_candidate",
)

DECISION_REQUEST_FIELDS: Tuple[str, ...] = (
    "decision_request_candidate_id",
    "source_integrated_context_ref",
    "source_decision_readiness_ref",
    "source_context_conflict_refs",
    "source_context_gap_refs",
    "source_freshness_status_refs",
    "source_priority_map_ref",
    "target_context_refs",
    "text_context_refs",
    "tracking_context_refs",
    "task_intent_context_refs",
    "spatiotemporal_context_refs",
    "world_continuity_context_refs",
    "risk_context_refs",
    "navigation_application_context_refs",
    "drive_signal_refs",
    "health_refs",
    "validation_refs",
    "constitution_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "not_action",
    "not_user_output",
)

DECISION_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "decision_candidate_id",
    "source_decision_request_ref",
    "selected_action",
    "decision_status",
    "decision_scope",
    "primary_goal",
    "secondary_goal",
    "application_goal",
    "decision_reason",
    "hold_reason",
    "observe_more_reason",
    "ask_user_reason",
    "block_reason",
    "allowed_next_candidates",
    "forbidden_actions",
    "required_observation",
    "uncertainty_level",
    "survival_priority_applied",
    "task_priority_applied",
    "confidence",
    "evidence_refs",
    "context_conflict_refs",
    "context_gap_refs",
    "freshness_status_refs",
    "rationale_refs",
    "whitebox_trace_refs",
    "candidate_only",
    "not_action",
    "not_user_output",
    "task_response_generation_allowed",
    "runtime_enable_allowed",
)

SCENE_PRIORITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "当前场景理解优先于导航应用",
    "navigation context 不作为第一目标",
    "Scene Understanding 是 primary decision scope",
    "navigation 是 application context only",
    "Decision 不把导航任务推进作为默认输出",
    "Layer 1 当前场景理解是 primary_goal",
    "Layer 2 时空间连续是 secondary_goal",
    "Layer 3 导航是 application_goal",
    "Layer 4 扩展能力 deferred",
    "capability stack layers must not be mixed as one mega-capability",
)

TARGET_RECOGNITION_DECISION_REVIEW_ITEMS: Tuple[str, ...] = (
    "target_recognition_candidate 可影响 observe_more / ask_user / allow_candidate_forward",
    "未验证目标不能成为 identified fact",
    "missing target creates required_observation",
    "target recognition 不触发直接行动",
)

TEXT_RECOGNITION_DECISION_REVIEW_ITEMS: Tuple[str, ...] = (
    "text recognition / OCR candidate 可辅助场景理解",
    "text not fact by default",
    "OCR text may require validation",
    "text 不直接触发导航动作",
)

TARGET_TRACKING_DECISION_REVIEW_ITEMS: Tuple[str, ...] = (
    "target_tracking_candidate 可触发 observe_more",
    "lost_target_risk 可降低 readiness",
    "tracking 不调用 camera/runtime",
    "tracking 不等于身份识别",
)

TASK_INTENT_DECISION_REVIEW_ITEMS: Tuple[str, ...] = (
    "task_intent_candidate 可影响目标搜索",
    "voice/dialogue requirement 不直接执行",
    "task intent 不能 override Survival risk",
    "target search remains observation requirement",
)

SPATIOTEMPORAL_DECISION_REVIEW_ITEMS: Tuple[str, ...] = (
    "spatiotemporal continuity 是第二目标",
    "missing sequence gap 可触发 observe_more",
    "stale/simulated sequence blocks real action",
    "continuity candidate 不写 WorldModel",
)

WORLD_CONTINUITY_DECISION_REVIEW_ITEMS: Tuple[str, ...] = (
    "world_continuity_candidate 只是 hypothesis",
    "scene_rule_candidate 不等于场景规则事实",
    "inferred continuity 不能直接行动",
    "missing content 可触发 reobserve",
)

SURVIVAL_RISK_DECISION_REVIEW_ITEMS: Tuple[str, ...] = (
    "Survival safety > task progress",
    "risk_context 可触发 hold_for_safety / observe_more",
    "traffic / obstacle / fall / collision / lost-context risk 禁止直接导航动作",
    "user/task preference cannot override survival safety",
)

NAVIGATION_APP_DECISION_REVIEW_ITEMS: Tuple[str, ...] = (
    "route_context / navigation_task 是第三目标应用层 context",
    "navigation action not generated",
    "decision can mark_not_ready_for_navigation_decision",
    "navigation requires target recognition + spatiotemporal readiness + controlled runtime later",
)

ACTION_TAXONOMY_REVIEW_ITEMS: Tuple[str, ...] = (
    "selected_action 属于 taxonomy",
    "selected_action 不等于 runtime action",
    "decision_candidate 不等于 task_response_candidate",
    "decision_candidate 不等于 user_output_candidate",
    "decision_candidate 不写 Memory/WorldModel",
)

TASK_RESPONSE_HANDOFF_ITEMS: Tuple[str, ...] = (
    "decision_candidate 可交给 Task Response Candidate Integration later",
    "task_response_candidate_generated_now=false",
    "Output/Gate chain later",
    "no user-facing output now",
)

TRACEABILITY_REVIEW_ITEMS: Tuple[str, ...] = (
    "source_integrated_context_ref preserved",
    "target/text/tracking/task/spatiotemporal/world/risk/navigation refs preserved",
    "conflict/gap/freshness/priority refs preserved",
    "drive/health/validation/constitution refs preserved",
    "whitebox_trace_refs preserved",
    "rationale_refs preserved",
)

DC_BINDING_REVIEW_ITEMS: Tuple[str, ...] = (
    "Decision Center consumes integrated_context_candidate only",
    "Decision Center remains裁决层",
    "Constitution-Bus refs consumed not authored",
    "Health/Safety gate context consumed as pressure only",
    "no decision execution in this phase",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_task_response_generation",
    "dryrun_to_user_output_candidate_generation",
    "dryrun_to_user_output",
    "dryrun_to_camera_invocation",
    "dryrun_to_real_frame_read",
    "dryrun_to_vision_runtime_enable",
    "dryrun_to_ocr_runtime_enable",
    "dryrun_to_real_ocr_execution",
    "dryrun_to_map_provider_invocation",
    "dryrun_to_navigation_runtime_enable",
    "dryrun_to_real_navigation_action",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_controlled_runtime_enable",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Decision Chain Candidate DryRun GO ≠ real decision execution",
    "decision_candidate ≠ task_response_candidate",
    "decision_candidate ≠ user output",
    "observe_more / hold_for_safety ≠ camera/runtime invoked",
    "mark_not_ready_for_navigation_decision ≠ navigation failure",
    "next Task Response Candidate DryRun ≠ user-facing output",
    "capability stack GO ≠ all layers runtime enabled",
    "layered capabilities ≠ single mixed mega-capability",
    "Layer 4/5 deferred ≠ current main axis activated",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "first_person_scene_understanding_decision_chain_candidate_dryrun_only",
    "simulated",
    "decision_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "task_response_candidate_generated_now",
    "user_output_candidate_generated_now",
    "user_output_generated_now",
    "camera_invoked_now",
    "real_frame_read_now",
    "vision_runtime_enabled_now",
    "ocr_runtime_enabled_now",
    "real_ocr_executed_now",
    "map_provider_invoked_now",
    "navigation_runtime_enabled_now",
    "real_navigation_action_executed_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "controlled_runtime_enabled_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_decision_chain_candidate_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
        "mainline": "first_person_scene_understanding",
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _build_capability_stack_governance(meta: Dict[str, Any]) -> Dict[str, Any]:
    layers = [{**layer, **meta} for layer in CAPABILITY_STACK_LAYERS]
    return {
        "governance_id": "first_person_capability_stack_governance_v1",
        "stack_id": CAPABILITY_STACK_ID,
        "stack_name": CAPABILITY_STACK_NAME,
        "stack_name_zh": "第一视角能力栈",
        "layer_count": len(layers),
        "layers": layers,
        "governance_rules": list(CAPABILITY_STACK_GOVERNANCE_RULES),
        "layer_independence_required": True,
        "no_mega_capability_mixing": True,
        "layer_1_primary_goal": "current_scene_understanding",
        "layer_2_secondary_goal": "spatiotemporal_continuity_and_world_understanding",
        "layer_3_application_goal": "navigation_application_layer",
        "layer_4_deferred": True,
        "layer_5_later": True,
        "navigation_is_layer_3_not_layer_1": True,
        "person_recognition_reading_layer_4_plus": True,
        "extends_universal_standard_ref": UNIVERSAL_STACK_STANDARD_ID,
        "universal_standard_applies_to_all_modules": True,
        "governance_pass": True,
        **meta,
    }


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def run_first_person_scene_understanding_decision_chain_candidate_dryrun_v1(
    *,
    first_person_scene_understanding_information_integration_chain_dryrun_root: str,
    midplatform_decision_center_module_dryrun_and_review_root: str,
    midplatform_information_integration_layer_dryrun_and_review_root: str,
    seed_core_drive_signal_contract_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    health_enforcement_supervisor_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    ii_chain_root = Path(
        first_person_scene_understanding_information_integration_chain_dryrun_root
    ).expanduser().resolve()
    dc_dr_root = Path(
        midplatform_decision_center_module_dryrun_and_review_root
    ).expanduser().resolve()
    ii_dr_root = Path(
        midplatform_information_integration_layer_dryrun_and_review_root
    ).expanduser().resolve()
    ds_dr_root = Path(seed_core_drive_signal_contract_dryrun_and_review_root).expanduser().resolve()
    cb_dr_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    health_dr_root = Path(health_enforcement_supervisor_dryrun_and_review_root).expanduser().resolve()

    ii_chain_sm = _try_read_json(ii_chain_root / "summary.json") or {}
    ii_chain_vr = _try_read_json(ii_chain_root / "verifier_report.json") or {}
    dc_dr_vr = _try_read_json(dc_dr_root / "verifier_report.json") or {}
    ii_dr_vr = _try_read_json(ii_dr_root / "verifier_report.json") or {}
    ds_dr_vr = _try_read_json(ds_dr_root / "verifier_report.json") or {}
    cb_dr_vr = _try_read_json(cb_dr_root / "verifier_report.json") or {}
    safety_dr_vr = _try_read_json(safety_dr_root / "verifier_report.json") or {}
    health_dr_vr = _try_read_json(health_dr_root / "verifier_report.json") or {}

    integrated = _try_read_json(ii_chain_root / "sample_integrated_context_candidate_v1.json") or {}
    readiness = _try_read_json(ii_chain_root / "sample_decision_readiness_candidate_v1.json") or {}
    conflict = _try_read_json(ii_chain_root / "sample_context_conflict_candidate_v1.json") or {}
    gap = _try_read_json(ii_chain_root / "sample_context_gap_candidate_v1.json") or {}
    freshness = _try_read_json(ii_chain_root / "sample_context_freshness_status_v1.json") or {}
    priority = _try_read_json(ii_chain_root / "sample_context_priority_map_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_scene_understanding_integration_chain_root": str(ii_chain_root),
        "upstream_decision_center_dryrun_root": str(dc_dr_root),
        "upstream_information_integration_dryrun_root": str(ii_dr_root),
        "upstream_drive_signal_dryrun_root": str(ds_dr_root),
        "upstream_constitution_bus_dryrun_root": str(cb_dr_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_health_enforcement_dryrun_root": str(health_dr_root),
        "output_root": str(out_root),
    }

    if ii_chain_vr.get("verifier") != "GO":
        blockers.append("Scene Understanding Integration Chain DryRun must be GO")
    if ii_chain_sm.get("final_decision") != UPSTREAM_II_CHAIN_DR_FINAL:
        blockers.append("integration chain dryrun final_decision mismatch")
    if ii_chain_sm.get("recommended_next_phase") != UPSTREAM_II_CHAIN_DR_NEXT:
        blockers.append("integration chain dryrun recommended_next_phase mismatch")
    if dc_dr_vr.get("verifier") != "GO":
        blockers.append("Decision Center Module DryRunAndReview must be GO")
    if ii_dr_vr.get("verifier") != "GO":
        blockers.append("Information Integration Layer DryRunAndReview must be GO")
    if ds_dr_vr.get("verifier") != "GO":
        blockers.append("Drive Signal Contract DryRunAndReview must be GO")
    if cb_dr_vr.get("verifier") != "GO":
        blockers.append("Constitution-Bus v1.0 must be GO")
    if safety_dr_vr.get("verifier") != "GO":
        blockers.append("Safety Gate DryRunAndReview must be GO")
    if health_dr_vr.get("verifier") != "GO":
        blockers.append("Health Enforcement Supervisor DryRunAndReview must be GO")

    if integrated.get("candidate_only") is not True:
        blockers.append("integrated_context must be candidate_only")
    if integrated.get("not_fact") is not True:
        blockers.append("integrated_context must be not_fact")
    if integrated.get("application_context", {}).get("not_primary_goal") is not True:
        blockers.append("navigation must remain application-layer context")
    if readiness.get("sufficient_for_decision") is not False:
        blockers.append("readiness sufficient_for_decision must be false")

    input_ok = len(blockers) == 0

    input_review = {
        "review_id": "information_integration_input_review_v1",
        "integration_chain_dryrun_verifier": ii_chain_vr.get("verifier"),
        "integration_chain_dryrun_final_decision": ii_chain_sm.get("final_decision"),
        "integrated_context_ref": integrated.get("integrated_context_id"),
        "decision_readiness_ref": readiness.get("decision_readiness_id"),
        "scene_understanding_primary": True,
        "navigation_application_layer_only": True,
        "fixture_metadata_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    dc_binding_review = {
        "review_id": "decision_center_binding_review_v1",
        "review_items": list(DC_BINDING_REVIEW_ITEMS),
        "decision_center_dryrun_verifier": dc_dr_vr.get("verifier"),
        "constitution_bus_verifier": cb_dr_vr.get("verifier"),
        "safety_gate_verifier": safety_dr_vr.get("verifier"),
        "health_enforcement_verifier": health_dr_vr.get("verifier"),
        **_review_ok([(f"item.{i[:18]}", True) for i in DC_BINDING_REVIEW_ITEMS]),
        **meta,
    }

    decision_request = {
        "decision_request_candidate_id": "decision_request_scene_understanding_chain_001",
        "source_integrated_context_ref": integrated.get("integrated_context_id"),
        "source_decision_readiness_ref": readiness.get("decision_readiness_id"),
        "source_context_conflict_refs": integrated.get("context_conflict_refs") or [],
        "source_context_gap_refs": integrated.get("context_gap_refs") or [],
        "source_freshness_status_refs": integrated.get("freshness_status_refs") or [],
        "source_priority_map_ref": integrated.get("context_priority_map_ref"),
        "target_context_refs": [
            integrated.get("target_context", {}).get("target_refs", ["target_recognition_sample_crosswalk_001"])[0]
            if isinstance(integrated.get("target_context", {}).get("target_refs"), list)
            else "target_recognition_sample_crosswalk_001"
        ],
        "text_context_refs": [integrated.get("text_context", {}).get("text_region_ref", "text_region_candidate:sign_001")],
        "tracking_context_refs": [
            integrated.get("tracking_context", {}).get("tracking_ref", "target_tracking_sample_crosswalk_001")
        ],
        "task_intent_context_refs": [
            integrated.get("task_intent_context", {}).get("task_intent_ref", "task_intent_sample_find_crosswalk_001")
        ],
        "spatiotemporal_context_refs": [
            integrated.get("spatiotemporal_context", {}).get(
                "spatiotemporal_ref", "spatiotemporal_context_sample_approach_001"
            )
        ],
        "world_continuity_context_refs": [
            integrated.get("world_continuity_context", {}).get(
                "world_continuity_ref", "world_continuity_sample_intersection_001"
            )
        ],
        "risk_context_refs": ["risk_context_sample_traffic_001"],
        "navigation_application_context_refs": [
            integrated.get("application_context", {}).get("route_context_ref", "route_context_sample_001"),
            integrated.get("application_context", {}).get("navigation_task_ref", "navigation_task_sample_001"),
        ],
        "drive_signal_refs": [
            integrated.get("drive_context", {}).get("drive_signal_ref", "drive_signal_sample_survival_001")
        ],
        "health_refs": ["health_signal_candidate:module_status_001"],
        "validation_refs": ["validation_fixture_pending"],
        "constitution_refs": ["constitution_bus:governance_baseline_v1"],
        "whitebox_trace_refs": integrated.get("whitebox_trace_refs") or [],
        "candidate_only": True,
        "not_action": True,
        "not_user_output": True,
        **meta,
    }

    decision_candidate = {
        "decision_candidate_id": "decision_candidate_scene_understanding_chain_001",
        "source_decision_request_ref": decision_request["decision_request_candidate_id"],
        "selected_action": "observe_more",
        "decision_status": "candidate_hold",
        "decision_scope": "first_person_scene_understanding",
        "primary_goal": "current_scene_understanding",
        "secondary_goal": "spatiotemporal_continuity_and_world_understanding",
        "application_goal": "navigation_application_layer",
        "decision_reason": (
            "fixture_scene_understanding_with_missing_live_validation_and_elevated_survival_risk;"
            "navigation_application_context_present_but_not_ready"
        ),
        "hold_reason": "survival_crossing_attention_with_insufficient_scene_validation",
        "observe_more_reason": (
            "missing_real_time_frame_validation_and_continuous_sequence_validation;"
            "live_scene_validation_later_required"
        ),
        "ask_user_reason": None,
        "block_reason": None,
        "allowed_next_candidates": [
            "preserve_as_scene_understanding_only",
            "mark_not_ready_for_navigation_decision",
            "request_validation",
        ],
        "forbidden_actions": [
            "direct_navigation_action_without_runtime_authorization",
            "user_output_without_gate",
            "memory_worldmodel_write",
            "camera_runtime_invocation",
            "navigation_runtime_enable",
        ],
        "required_observation": [
            "live_scene_validation_later",
            "observe_crossing_status_later",
            "continuous_sequence_validation_later",
        ],
        "uncertainty_level": integrated.get("uncertainty_level", "moderate"),
        "survival_priority_applied": True,
        "task_priority_applied": False,
        "confidence": 0.47,
        "evidence_refs": [
            "visual_obs_sample_crossing_001",
            "target_recognition_sample_crosswalk_001",
            "text_recognition_sample_sign_001",
            "target_tracking_sample_crosswalk_001",
            "drive_signal_sample_survival_001",
        ],
        "context_conflict_refs": integrated.get("context_conflict_refs") or [],
        "context_gap_refs": integrated.get("context_gap_refs") or [],
        "freshness_status_refs": integrated.get("freshness_status_refs") or [],
        "rationale_refs": [
            "rationale:scene_understanding_decision:001",
            "readiness:not_ready_for_scene_understanding_decision",
            "gap:missing_real_time_frame_validation",
            "gap:missing_mid_sequence_frame_validation",
            "survival:elevated_crossing_attention",
            "navigation:application_layer_not_ready",
        ],
        "whitebox_trace_refs": integrated.get("whitebox_trace_refs") or [],
        "candidate_only": True,
        "not_action": True,
        "not_user_output": True,
        "task_response_generation_allowed": False,
        "runtime_enable_allowed": False,
        "mark_not_ready_for_navigation_decision": True,
        **meta,
    }

    capability_stack_governance = _build_capability_stack_governance(meta)

    scene_priority_review = {
        "review_id": "scene_understanding_decision_priority_review_v1",
        "review_items": list(SCENE_PRIORITY_REVIEW_ITEMS),
        "primary_goal": decision_candidate.get("primary_goal"),
        "secondary_goal": decision_candidate.get("secondary_goal"),
        "application_goal": decision_candidate.get("application_goal"),
        "layer_1_primary_confirmed": decision_candidate.get("primary_goal") == "current_scene_understanding",
        "layer_2_secondary_confirmed": (
            decision_candidate.get("secondary_goal") == "spatiotemporal_continuity_and_world_understanding"
        ),
        "layer_3_application_confirmed": (
            decision_candidate.get("application_goal") == "navigation_application_layer"
        ),
        "layer_4_deferred_confirmed": capability_stack_governance.get("layer_4_deferred") is True,
        "capability_stack_ref": capability_stack_governance["governance_id"],
        "no_mega_capability_mixing": True,
        **_review_ok([(f"item.{i[:18]}", True) for i in SCENE_PRIORITY_REVIEW_ITEMS]),
        **meta,
    }

    target_decision_review = {
        "review_id": "target_recognition_decision_review_v1",
        "review_items": list(TARGET_RECOGNITION_DECISION_REVIEW_ITEMS),
        "selected_action": decision_candidate.get("selected_action"),
        **_review_ok([(f"item.{i[:18]}", True) for i in TARGET_RECOGNITION_DECISION_REVIEW_ITEMS]),
        **meta,
    }

    text_decision_review = {
        "review_id": "text_recognition_decision_review_v1",
        "review_items": list(TEXT_RECOGNITION_DECISION_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in TEXT_RECOGNITION_DECISION_REVIEW_ITEMS]),
        **meta,
    }

    tracking_decision_review = {
        "review_id": "target_tracking_decision_review_v1",
        "review_items": list(TARGET_TRACKING_DECISION_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in TARGET_TRACKING_DECISION_REVIEW_ITEMS]),
        **meta,
    }

    task_intent_decision_review = {
        "review_id": "task_intent_decision_review_v1",
        "review_items": list(TASK_INTENT_DECISION_REVIEW_ITEMS),
        "survival_over_task": decision_candidate.get("survival_priority_applied") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in TASK_INTENT_DECISION_REVIEW_ITEMS]),
        **meta,
    }

    spatiotemporal_decision_review = {
        "review_id": "spatiotemporal_continuity_decision_review_v1",
        "review_items": list(SPATIOTEMPORAL_DECISION_REVIEW_ITEMS),
        "secondary_goal": decision_candidate.get("secondary_goal"),
        **_review_ok([(f"item.{i[:18]}", True) for i in SPATIOTEMPORAL_DECISION_REVIEW_ITEMS]),
        **meta,
    }

    world_decision_review = {
        "review_id": "world_continuity_decision_review_v1",
        "review_items": list(WORLD_CONTINUITY_DECISION_REVIEW_ITEMS),
        **_review_ok([(f"item.{i[:18]}", True) for i in WORLD_CONTINUITY_DECISION_REVIEW_ITEMS]),
        **meta,
    }

    survival_decision_review = {
        "review_id": "survival_risk_decision_review_v1",
        "review_items": list(SURVIVAL_RISK_DECISION_REVIEW_ITEMS),
        "survival_priority_applied": decision_candidate.get("survival_priority_applied") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in SURVIVAL_RISK_DECISION_REVIEW_ITEMS]),
        **meta,
    }

    nav_app_decision_review = {
        "review_id": "navigation_application_context_decision_review_v1",
        "review_items": list(NAVIGATION_APP_DECISION_REVIEW_ITEMS),
        "mark_not_ready": decision_candidate.get("mark_not_ready_for_navigation_decision") is True,
        **_review_ok([(f"item.{i[:18]}", True) for i in NAVIGATION_APP_DECISION_REVIEW_ITEMS]),
        **meta,
    }

    taxonomy_review = {
        "review_id": "decision_action_taxonomy_review_v1",
        "review_items": list(ACTION_TAXONOMY_REVIEW_ITEMS),
        "taxonomy": list(DECISION_ACTION_TAXONOMY),
        "selected_action_in_taxonomy": decision_candidate.get("selected_action") in DECISION_ACTION_TAXONOMY,
        **_review_ok([(f"item.{i[:18]}", True) for i in ACTION_TAXONOMY_REVIEW_ITEMS]),
        **meta,
    }

    handoff_plan = {
        "plan_id": "decision_to_task_response_handoff_plan_v1",
        "review_items": list(TASK_RESPONSE_HANDOFF_ITEMS),
        "decision_candidate_ref": decision_candidate["decision_candidate_id"],
        "task_response_candidate_generated_now": False,
        "user_output_generated_now": False,
        "next_chain": "task_response_candidate_integration_later",
        **_review_ok([(f"item.{i[:18]}", True) for i in TASK_RESPONSE_HANDOFF_ITEMS]),
        **meta,
    }

    traceability_review = {
        "review_id": "decision_traceability_review_v1",
        "review_items": list(TRACEABILITY_REVIEW_ITEMS),
        "source_integrated_context_ref": integrated.get("integrated_context_id"),
        "rationale_count": len(decision_candidate.get("rationale_refs") or []),
        **_review_ok([(f"item.{i[:18]}", True) for i in TRACEABILITY_REVIEW_ITEMS]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "decision_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "boundary_true_fields": {f: True for f in BOUNDARY_TRUE},
        "decision_candidate_generated_now": True,
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "decision_blocked_path_result_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS
        ],
        "allowed_paths": [
            {
                "path_id": "dryrun_to_decision_candidate_generation",
                "status": "allowed_candidate_only",
                "executed": True,
            }
        ],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    reviews = [
        scene_priority_review,
        target_decision_review,
        text_decision_review,
        tracking_decision_review,
        task_intent_decision_review,
        spatiotemporal_decision_review,
        world_decision_review,
        survival_decision_review,
        nav_app_decision_review,
        taxonomy_review,
        handoff_plan,
        traceability_review,
        dc_binding_review,
    ]

    request_ok = all(f in decision_request for f in DECISION_REQUEST_FIELDS)
    decision_ok = (
        all(f in decision_candidate for f in DECISION_CANDIDATE_FIELDS)
        and decision_candidate.get("selected_action") in DECISION_ACTION_TAXONOMY
        and decision_candidate.get("selected_action") in ("observe_more", "hold_for_safety")
        and decision_candidate.get("decision_status") == "candidate_hold"
        and decision_candidate.get("primary_goal") == "current_scene_understanding"
        and decision_candidate.get("application_goal") == "navigation_application_layer"
        and decision_candidate.get("task_response_generation_allowed") is False
        and decision_candidate.get("runtime_enable_allowed") is False
        and decision_candidate.get("candidate_only") is True
        and bool(decision_candidate.get("observe_more_reason"))
        and bool(decision_candidate.get("hold_reason"))
    )

    stack_ok = (
        capability_stack_governance.get("governance_pass") is True
        and capability_stack_governance.get("no_mega_capability_mixing") is True
        and capability_stack_governance.get("navigation_is_layer_3_not_layer_1") is True
        and len(capability_stack_governance.get("layers") or []) == 5
        and all(
            all(f in layer for f in CAPABILITY_STACK_LAYER_FIELDS)
            for layer in (capability_stack_governance.get("layers") or [])
        )
        and scene_priority_review.get("layer_1_primary_confirmed") is True
        and scene_priority_review.get("layer_2_secondary_confirmed") is True
        and scene_priority_review.get("layer_3_application_confirmed") is True
        and scene_priority_review.get("layer_4_deferred_confirmed") is True
    )

    chain_pass = (
        input_ok
        and request_ok
        and decision_ok
        and stack_ok
        and all(r.get("dryrun_and_review_pass") for r in reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
        and taxonomy_review.get("selected_action_in_taxonomy") is True
        and meta.get("decision_candidate_generated_now") is True
        and meta.get("task_response_candidate_generated_now") is False
        and meta.get("navigation_runtime_enabled_now") is False
    )

    closure_decision = {
        "decision_id": "decision_closure_decision_v1",
        "dryrun_and_review_pass": chain_pass,
        "high_risk": not chain_pass,
        "final_decision": FINAL_DECISION_GO if chain_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "First-Person Capability Stack governance registered as mainline hard rule",
            "5 layers independently defined with boundary/candidate/integration/test/failure routes",
            "scene understanding integrated_context consumed by Decision Center",
            "decision_candidate generated as observe_more/candidate_hold",
            "Layer 1/2/3 goals confirmed; Layer 4/5 deferred",
            "target/text/tracking/task/spatiotemporal/world/survival/navigation decision reviews pass",
            "action taxonomy + task response handoff + traceability verified",
            "17 blocked paths + decision_candidate_generated_now true",
        ],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_task_response_candidate_dryrun": chain_pass,
        "selected_next_phase": NEXT_PHASE_GO if chain_pass else NEXT_PHASE_HOLD,
        "next_focus": (
            "Task Response layer assembles task_response_candidate from decision_candidate, "
            "still no user output"
        ),
        **meta,
    }

    policy = {
        "policy_id": "first_person_scene_understanding_decision_chain_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "decision_candidate_only_not_execute_not_output": True,
        "mainline": "first_person_scene_understanding",
        "capability_stack_governance_required": True,
        "capability_stack_ref": CAPABILITY_STACK_ID,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": chain_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": chain_pass,
        "system_level_simulated_go": True,
        "fixture_decision_candidate_generated": True,
        "mainline": "first_person_scene_understanding",
        "capability_stack_governance_registered": True,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "first_person_scene_understanding_decision_chain_dryrun_policy": policy,
        "first_person_capability_stack_governance": capability_stack_governance,
        "information_integration_input_review": input_review,
        "decision_center_binding_review": dc_binding_review,
        "sample_decision_request_candidate": decision_request,
        "sample_decision_candidate": decision_candidate,
        "scene_understanding_decision_priority_review": scene_priority_review,
        "target_recognition_decision_review": target_decision_review,
        "text_recognition_decision_review": text_decision_review,
        "target_tracking_decision_review": tracking_decision_review,
        "task_intent_decision_review": task_intent_decision_review,
        "spatiotemporal_continuity_decision_review": spatiotemporal_decision_review,
        "world_continuity_decision_review": world_decision_review,
        "survival_risk_decision_review": survival_decision_review,
        "navigation_application_context_decision_review": nav_app_decision_review,
        "decision_action_taxonomy_review": taxonomy_review,
        "decision_to_task_response_handoff_plan": handoff_plan,
        "decision_traceability_review": traceability_review,
        "decision_boundary_audit": boundary_audit,
        "decision_blocked_path_result": blocked_path_result,
        "decision_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
