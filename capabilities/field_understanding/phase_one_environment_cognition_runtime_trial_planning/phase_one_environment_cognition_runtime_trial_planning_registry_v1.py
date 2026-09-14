# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_planning.phase_one_environment_cognition_runtime_trial_planning_types_v1 import (
    ACTION_SAFETY_ENTRYPOINT,
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    ControlledRuntimeTrialPlanningProfile,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_GO,
    GUIDANCE_ENTRYPOINT,
    INTERFACE_LAYER_PROTOCOL_REF,
    NEXT_PHASE_REF,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PLANNING_GOVERNANCE_RULES,
    PLANNING_OBJECT_TYPES,
    PROHIBITED_ITEMS,
    RUNTIME_TRIAL_MODE,
    SCENARIO_POLICY_GO_KEYS,
    SCENARIO_POLICY_REFS,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    SPEECH_GATE_ENTRYPOINT,
    TASK_MANAGER_ENTRYPOINT,
    RuntimeTrialAdmissionDecision,
    RuntimeTrialEvidenceRequirement,
    RuntimeTrialFailureHandlingPolicy,
    RuntimeTrialObservationLogRequirement,
    RuntimeTrialOwnerApprovalRequirement,
    RuntimeTrialRollbackRequirement,
    RuntimeTrialSafetyGateRequirement,
    RuntimeTrialScenarioPolicy,
    candidate_to_dict,
)

REGISTRY_ID = "phase_one_environment_cognition_runtime_trial_planning_registry_v1"
PROFILE_REF = "phase_one_environment_cognition_runtime_trial_planning_profile_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "planning_object_types": PLANNING_OBJECT_TYPES,
    "scenario_policy_refs": SCENARIO_POLICY_REFS,
    "scenario_policy_go_keys": SCENARIO_POLICY_GO_KEYS,
    "planning_governance_rules": PLANNING_GOVERNANCE_RULES,
    "prohibited_items": PROHIBITED_ITEMS,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
}

_POLICY_GO_KEY_MAP: Dict[str, str] = {
    "mall_find_entrance_low_risk_trial_candidate": "mall_find_entrance_low_risk_trial_candidate",
    "subway_enter_station_cautious_trial_candidate": "subway_enter_station_cautious_trial_candidate",
    "stadium_concert_ticket_gate_observation_trial_candidate": "stadium_concert_observation_trial_candidate",
    "plaza_market_crowd_blocked_or_observation_only": "plaza_market_crowd_observation_only",
    "gps_slam_conflict_runtime_blocker": "gps_slam_conflict_runtime_blocker",
    "home_return_low_risk_trial_candidate": "home_return_low_risk_trial_candidate",
}

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": PHASE_ONE_CHAIN_REF,
        "artifact_rel": (
            "_tmp_eval_out/field_task_guidance_safety_chain_closure_v1_smoke_v0/"
            "field_task_guidance_safety_chain_closure_review_v1.json"
        ),
        "expected_go": "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/field_task_guidance_safety_chain_closure/"
            "field_task_guidance_safety_chain_closure_types_v1.py"
        ),
        "require_go": True,
        "require_sealed": True,
    },
    {
        "phase_ref": "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/slam_spatial_evidence_chain_closure_v1_smoke_v0/"
            "slam_spatial_evidence_chain_closure_review_v1.json"
        ),
        "expected_go": "SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/slam_spatial_evidence_chain_closure/"
            "slam_spatial_evidence_chain_closure_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/field_synthesis_map_place_event_overlay_dryrun_v1_smoke_v0/"
            "field_synthesis_map_place_event_overlay_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "FIELD_SYNTHESIS_MAP_PLACE_REALTIME_EVENT_OVERLAY_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/field_synthesis_map_place_event_overlay_dryrun/"
            "field_synthesis_map_place_event_overlay_dryrun_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": "Phase-Field-To-Task-Alignment-DryRun-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/field_to_task_alignment_dryrun_v1_smoke_v0/"
            "field_to_task_alignment_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "FIELD_TO_TASK_ALIGNMENT_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/field_to_task_alignment_dryrun/"
            "field_to_task_alignment_dryrun_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": "Phase-Task-To-Guidance-Safety-Gate-DryRun-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/task_to_guidance_safety_gate_dryrun_v1_smoke_v0/"
            "task_to_guidance_safety_gate_dryrun_run_and_review_v1.json"
        ),
        "expected_go": "TASK_TO_GUIDANCE_SAFETY_GATE_DRYRUN_GO",
        "module_rel": (
            "capabilities/field_understanding/task_to_guidance_safety_gate_dryrun/"
            "task_to_guidance_safety_gate_dryrun_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/midplatform_task_manager_controlled_skeleton_implementation_dryrun/"
            "summary.json"
        ),
        "expected_go": None,
        "module_rel": (
            "capabilities/midplatform/midplatform_task_manager_controlled_skeleton_implementation_dryrun_v1.py"
        ),
        "require_go": False,
        "skeleton_module_rel": "capabilities/midplatform/core/task_manager_skeleton_v1.py",
    },
    {
        "phase_ref": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "module_rel": (
            "capabilities/midplatform/interface_layer_governance/"
            "interface_layer_governance_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/provider_manager_runtime_skeleton_dryrun_v1_smoke_v0/"
            "provider_manager_runtime_skeleton_verification_and_review_v1.json"
        ),
        "expected_go": "PROVIDER_MANAGER_RUNTIME_SKELETON_POST_DRYRUN_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/provider_manager_runtime_skeleton/"
            "provider_manager_runtime_skeleton_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/task_manager_owner_approval_request_module_handoff_v1_smoke_v0/"
            "owner_approval_request_module_handoff_report_v1.json"
        ),
        "expected_go": (
            "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_"
            "READY_FOR_BROADER_MIDPLATFORM_TASK_MANAGER_CLOSURE_ROADMAP"
        ),
        "module_rel": (
            "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_v1.py"
        ),
        "require_go": True,
        "placeholder_only": False,
    },
)


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(PLANNING_OBJECT_TYPES) != 9:
        issues.append("planning_object_types_count_not_9")
    if len(SCENARIO_POLICY_REFS) != 6:
        issues.append("scenario_policy_refs_count_not_6")
    if len(SCENARIO_POLICY_GO_KEYS) != 6:
        issues.append("scenario_policy_go_keys_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 10:
        issues.append("sealed_upstream_phase_refs_count_not_10")
    if len(PLANNING_GOVERNANCE_RULES) != 13:
        issues.append("planning_governance_rules_count_not_13")
    if len(PROHIBITED_ITEMS) != 12:
        issues.append("prohibited_items_count_not_12")
    return len(issues) == 0, issues


def build_scenario_policies_v1() -> Tuple[RuntimeTrialScenarioPolicy, ...]:
    return (
        RuntimeTrialScenarioPolicy(
            policy_ref="mall_find_entrance_low_risk_trial_candidate",
            source_scenario_ref="mall_find_entrance_chain_closed",
            admission_level="low_risk_controlled_trial_candidate",
            trial_conditions=(
                "indoor_static_route_hint_only",
                "no_road_crossing",
                "no_crowd_high_risk",
                "action_safety_candidate_required",
                "speech_output_requires_speech_gate_approval",
                "fallback_to_observe_wait",
            ),
            rollback_policy_ref="runtime_trial_rollback_v1",
            observation_log_policy_ref="runtime_trial_observation_log_v1",
            upstream_refs=(
                PHASE_ONE_CHAIN_REF,
                "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001",
                "Phase-Field-To-Task-Alignment-DryRun-v1-001",
                "Phase-Task-To-Guidance-Safety-Gate-DryRun-v1-001",
            ),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialScenarioPolicy(
            policy_ref="subway_enter_station_cautious_trial_candidate",
            source_scenario_ref="subway_enter_station_chain_closed",
            admission_level="cautious_candidate_trial",
            trial_conditions=(
                "gps_degraded_must_be_acknowledged",
                "local_spatial_evidence_required",
                "crowd_risk_must_downgrade_guidance",
                "no_direct_action",
                "requires_more_evidence_before_action_like_guidance",
            ),
            rollback_policy_ref="runtime_trial_rollback_v1",
            observation_log_policy_ref="runtime_trial_observation_log_v1",
            upstream_refs=(
                PHASE_ONE_CHAIN_REF,
                "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001",
                "Phase-Field-To-Task-Alignment-DryRun-v1-001",
            ),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialScenarioPolicy(
            policy_ref="stadium_concert_ticket_gate_observation_trial_candidate",
            source_scenario_ref="stadium_concert_ticket_gate_chain_closed",
            admission_level="observation_only",
            trial_conditions=(
                "crowd_flow_risk_required",
                "ocr_sign_evidence_optional_placeholder",
                "no_movement_command",
                "event_overlay_must_not_rewrite_map_place_ref",
            ),
            rollback_policy_ref="runtime_trial_rollback_v1",
            observation_log_policy_ref="runtime_trial_observation_log_v1",
            upstream_refs=(
                PHASE_ONE_CHAIN_REF,
                "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001",
            ),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialScenarioPolicy(
            policy_ref="plaza_market_crowd_blocked_or_observation_only",
            source_scenario_ref="plaza_market_crowd_chain_closed",
            admission_level="observation_only",
            trial_conditions=(
                "crowd_density_risk_blocks_action_like_guidance",
                "only_evidence_request_wait_observe_allowed",
                "no_movement_guidance_runtime_trial",
            ),
            rollback_policy_ref="runtime_trial_rollback_v1",
            observation_log_policy_ref="runtime_trial_observation_log_v1",
            upstream_refs=(
                PHASE_ONE_CHAIN_REF,
                "Phase-Task-To-Guidance-Safety-Gate-DryRun-v1-001",
            ),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialScenarioPolicy(
            policy_ref="gps_slam_conflict_runtime_blocker",
            source_scenario_ref="gps_slam_conflict_chain_closed",
            admission_level="blocked",
            trial_conditions=(
                "conflict_candidate_unresolved",
                "no_route_hint_activation",
                "no_action_like_guidance",
                "requires_conflict_resolution_planning",
            ),
            rollback_policy_ref="runtime_trial_rollback_v1",
            observation_log_policy_ref="runtime_trial_observation_log_v1",
            upstream_refs=(
                PHASE_ONE_CHAIN_REF,
                "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001",
            ),
            source_chain=SOURCE_CHAIN,
        ),
        RuntimeTrialScenarioPolicy(
            policy_ref="home_return_low_risk_trial_candidate",
            source_scenario_ref="home_return_chain_closed",
            admission_level="low_risk_controlled_trial_candidate",
            trial_conditions=(
                "coarse_map_route_plus_local_spatial_check",
                "action_safety_pending_required",
                "no_fact_write",
                "rollback_path_required",
            ),
            rollback_policy_ref="runtime_trial_rollback_v1",
            observation_log_policy_ref="runtime_trial_observation_log_v1",
            upstream_refs=(
                PHASE_ONE_CHAIN_REF,
                "Phase-Field-To-Task-Alignment-DryRun-v1-001",
                "Phase-Task-To-Guidance-Safety-Gate-DryRun-v1-001",
            ),
            source_chain=SOURCE_CHAIN,
        ),
    )


def build_shared_requirements_v1() -> Dict[str, Any]:
    return {
        "evidence_requirement": candidate_to_dict(
            RuntimeTrialEvidenceRequirement(
                requirement_ref="runtime_trial_evidence_requirement_v1",
                local_spatial_evidence_required=True,
                gps_degraded_acknowledgement_required=True,
                conflict_candidate_blocks_trial=True,
                ocr_sign_evidence_optional_placeholder=True,
                coarse_map_route_allowed=True,
                local_spatial_check_required=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "safety_gate_requirement": candidate_to_dict(
            RuntimeTrialSafetyGateRequirement(
                requirement_ref="runtime_trial_safety_gate_requirement_v1",
                action_safety_candidate_required=True,
                speech_gate_candidate_required=True,
                crowd_risk_downgrade_required=True,
                conflict_blocks_action_like_guidance=True,
                no_direct_action=True,
                no_movement_command=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "owner_approval_requirement": candidate_to_dict(
            RuntimeTrialOwnerApprovalRequirement(
                requirement_ref="runtime_trial_owner_approval_requirement_v1",
                owner_approval_required=True,
                owner_approval_runtime_not_issued=True,
                owner_approval_phase_placeholder=NEXT_PHASE_REF,
                record_approval_chain_placeholder=(
                    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-"
                    "Authorization-Grant-Owner-Approval-Request-Record-Approval-"
                    "Closure-Planning-v1-001"
                ),
                source_chain=SOURCE_CHAIN,
            )
        ),
        "rollback_requirement": candidate_to_dict(
            RuntimeTrialRollbackRequirement(
                requirement_ref="runtime_trial_rollback_requirement_v1",
                rollback_policy_required=True,
                fallback_observe_wait=True,
                candidate_only_rollback=True,
                no_fact_write_on_rollback=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "observation_log_requirement": candidate_to_dict(
            RuntimeTrialObservationLogRequirement(
                requirement_ref="runtime_trial_observation_log_requirement_v1",
                observation_log_policy_required=True,
                log_upstream_source_refs=True,
                log_admission_level=True,
                log_safety_gate_decisions=True,
                log_rollback_events=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "failure_handling_policy": candidate_to_dict(
            RuntimeTrialFailureHandlingPolicy(
                policy_ref="runtime_trial_failure_handling_policy_v1",
                failure_handling_policy_required=True,
                downgrade_on_high_risk=True,
                block_on_unresolved_conflict=True,
                evidence_request_on_insufficient_data=True,
                no_silent_runtime_escalation=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_planning_profile_v1() -> ControlledRuntimeTrialPlanningProfile:
    return ControlledRuntimeTrialPlanningProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        phase_one_chain_ref=PHASE_ONE_CHAIN_REF,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        task_manager_entrypoint=TASK_MANAGER_ENTRYPOINT,
        guidance_entrypoint=GUIDANCE_ENTRYPOINT,
        speech_gate_entrypoint=SPEECH_GATE_ENTRYPOINT,
        action_safety_entrypoint=ACTION_SAFETY_ENTRYPOINT,
        interface_layer_protocol_ref=INTERFACE_LAYER_PROTOCOL_REF,
        scenario_policy_refs=SCENARIO_POLICY_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=PLANNING_GOVERNANCE_RULES,
        prohibited_items=PROHIBITED_ITEMS,
        candidate_only_source_chain_required=CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    )


def build_admission_decision_v1(
    *,
    sealed_phase_one_chain_verified: bool,
    admission_level_declared_for_all: bool,
) -> RuntimeTrialAdmissionDecision:
    return RuntimeTrialAdmissionDecision(
        decision_ref="runtime_trial_admission_decision_v1",
        profile_ref=PROFILE_REF,
        planning_profile_count=1,
        scenario_policy_count=len(SCENARIO_POLICY_REFS),
        sealed_phase_one_chain_verified=sealed_phase_one_chain_verified,
        admission_level_declared_for_all=admission_level_declared_for_all,
        final_decision=FINAL_DECISION_GO,
    )


def build_scenario_policy_go_map(
    policies: Tuple[RuntimeTrialScenarioPolicy, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for policy in policies:
        go_key = _POLICY_GO_KEY_MAP.get(policy.policy_ref, policy.policy_ref)
        result[go_key] = policy.policy_active is True and bool(policy.admission_level)
    return result


def build_phase_one_environment_cognition_runtime_trial_planning_matrix_v1() -> Dict[str, Any]:
    profile = build_planning_profile_v1()
    policies = build_scenario_policies_v1()
    shared = build_shared_requirements_v1()
    admission = build_admission_decision_v1(
        sealed_phase_one_chain_verified=True,
        admission_level_declared_for_all=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "controlled_runtime_trial_planning_profile": candidate_to_dict(profile),
        "scenario_policies": [candidate_to_dict(p) for p in policies],
        "shared_requirements": shared,
        "admission_decision": candidate_to_dict(admission),
        "scenario_policy_go_map": build_scenario_policy_go_map(policies),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "planning_governance_rules": list(PLANNING_GOVERNANCE_RULES),
        "prohibited_items": list(PROHIBITED_ITEMS),
        "runtime_admission_levels": list(
            ("blocked", "observation_only", "cautious_candidate_trial", "low_risk_controlled_trial_candidate")
        ),
    }
