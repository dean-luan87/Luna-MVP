# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Execution Planning — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_execution_planning.phase_one_environment_cognition_runtime_trial_execution_planning_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    ControlledRuntimeTrialExecutionPlanItem,
    ControlledRuntimeTrialExecutionPlanningDecision,
    ControlledRuntimeTrialExecutionPlanningProfile,
    EXECUTION_PLAN_GO_KEYS,
    EXECUTION_PLAN_ITEM_REFS,
    EXECUTION_PLANNING_GOVERNANCE_RULES,
    EXECUTION_PLANNING_PRINCIPLE_ZH,
    ExecutionBlockedOperationPolicy,
    ExecutionFailureHandlingPlan,
    ExecutionObservationLogPlan,
    ExecutionPlanningAuditRecord,
    ExecutionPreconditionPolicy,
    ExecutionRollbackTriggerPolicy,
    FINAL_DECISION_GO,
    ISSUANCE_PACKAGE_REF,
    ISSUANCE_PACKAGE_REF_MAP,
    MANUAL_CONFIRMATION_POINTS,
    NEXT_PHASE_REF,
    OWNER_APPROVAL_ISSUANCE_REF,
    OWNER_APPROVAL_REQUEST_REF,
    PACKAGE_BOUNDARY_REF,
    PHASE_ID,
    PHASE_ONE_CHAIN_REF,
    PHASE_ONE_CHAIN_STATUS,
    PLANNING_REF,
    PRE_RUNTIME_TRIAL_PACKAGE_REF,
    PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
    RUNTIME_TRIAL_MODE,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    UNIVERSAL_BLOCKED_OPERATIONS,
    candidate_to_dict,
)

REGISTRY_ID = "phase_one_environment_cognition_runtime_trial_execution_planning_registry_v1"
PROFILE_REF = "controlled_runtime_trial_execution_planning_profile_v1"
ROLLBACK_TRIGGER_POLICY_REF = "runtime_trial_execution_rollback_trigger_v1"
OBSERVATION_LOG_PLAN_REF = "runtime_trial_execution_observation_log_plan_v1"
FAILURE_HANDLING_PLAN_REF = "runtime_trial_execution_failure_handling_plan_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "execution_plan_item_refs": EXECUTION_PLAN_ITEM_REFS,
    "execution_plan_go_keys": EXECUTION_PLAN_GO_KEYS,
    "execution_planning_governance_rules": EXECUTION_PLANNING_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "universal_blocked_operations": UNIVERSAL_BLOCKED_OPERATIONS,
    "manual_confirmation_points": MANUAL_CONFIRMATION_POINTS,
}

_PLAN_GO_KEY_MAP: Dict[str, Tuple[str, str, bool]] = {
    "mall_find_entrance_execution_plan": (
        "mall_find_entrance_execution_plan_ready",
        "planned_candidate_replay_only",
        True,
    ),
    "subway_enter_station_execution_plan": (
        "subway_enter_station_constrained_execution_plan_ready",
        "planned_constrained_candidate_replay_only",
        True,
    ),
    "stadium_concert_ticket_gate_execution_plan": (
        "stadium_concert_observation_execution_plan_ready",
        "planned_observation_replay_only",
        True,
    ),
    "plaza_market_crowd_execution_plan": (
        "plaza_market_observation_execution_plan_ready",
        "planned_observation_replay_only",
        True,
    ),
    "gps_slam_conflict_execution_plan": (
        "gps_slam_conflict_execution_plan_blocked",
        "blocked_no_execution_plan",
        False,
    ),
    "home_return_execution_plan": (
        "home_return_execution_plan_ready",
        "planned_candidate_replay_only",
        True,
    ),
}

_ISSUANCE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_issuance_package_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_issuance_package_review_v1.json"
)

_CLOSURE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1.json"
)

_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_planning_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_planning_review_v1.json"
)

_REQUEST_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_owner_approval_request_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_request_review_v1.json"
)

_OWNER_ISSUANCE_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_owner_approval_issuance_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_review_v1.json"
)

_PACKAGE_BOUNDARY_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_package_boundary_planning_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_package_boundary_planning_review_v1.json"
)

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_ref": ISSUANCE_PACKAGE_REF,
        "artifact_rel": _ISSUANCE_ARTIFACT_REL,
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_ISSUANCE_PACKAGE_GO",
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_issuance_package/"
            "phase_one_environment_cognition_runtime_trial_issuance_package_types_v1.py"
        ),
        "require_go": True,
        "require_issuance_package_go": True,
    },
    {
        "phase_ref": PRE_RUNTIME_TRIAL_PACKAGE_REF,
        "artifact_rel": _CLOSURE_ARTIFACT_REL,
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_CLOSURE_READINESS_REVIEW_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_closure_readiness_review/"
            "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_types_v1.py"
        ),
        "require_go": True,
        "require_pre_package_sealed": True,
    },
    {
        "phase_ref": PACKAGE_BOUNDARY_REF,
        "artifact_rel": _PACKAGE_BOUNDARY_ARTIFACT_REL,
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_BOUNDARY_PLANNING_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_package_boundary_planning/"
            "phase_one_environment_cognition_runtime_trial_package_boundary_planning_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": OWNER_APPROVAL_ISSUANCE_REF,
        "artifact_rel": _OWNER_ISSUANCE_ARTIFACT_REL,
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_ISSUANCE_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_issuance/"
            "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": OWNER_APPROVAL_REQUEST_REF,
        "artifact_rel": _REQUEST_ARTIFACT_REL,
        "expected_go": (
            "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_REQUEST_GO"
        ),
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_owner_approval_request/"
            "phase_one_environment_cognition_runtime_trial_owner_approval_request_types_v1.py"
        ),
        "require_go": True,
    },
    {
        "phase_ref": PLANNING_REF,
        "artifact_rel": _PLANNING_ARTIFACT_REL,
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_planning/"
            "phase_one_environment_cognition_runtime_trial_planning_types_v1.py"
        ),
        "require_go": True,
    },
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
)


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(EXECUTION_PLAN_ITEM_REFS) != 6:
        issues.append("execution_plan_item_refs_count_not_6")
    if len(EXECUTION_PLAN_GO_KEYS) != 6:
        issues.append("execution_plan_go_keys_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 11:
        issues.append("sealed_upstream_phase_refs_count_not_11")
    if len(EXECUTION_PLANNING_GOVERNANCE_RULES) != 14:
        issues.append("execution_planning_governance_rules_count_not_14")
    if len(ISSUANCE_PACKAGE_REF_MAP) != 6:
        issues.append("issuance_package_ref_map_count_not_6")
    return len(issues) == 0, issues


def _merge_blocked(*ops: str) -> Tuple[str, ...]:
    merged = list(UNIVERSAL_BLOCKED_OPERATIONS)
    for op in ops:
        if op not in merged:
            merged.append(op)
    return tuple(merged)


def build_execution_plan_items_v1() -> Tuple[ControlledRuntimeTrialExecutionPlanItem, ...]:
    common_preconditions = (
        "source_chain_intact",
        "rollback_policy_bound",
        "observation_log_bound",
        "no_live_sensor",
    )
    return (
        ControlledRuntimeTrialExecutionPlanItem(
            plan_ref="mall_find_entrance_execution_plan",
            issuance_package_ref="mall_find_entrance_issuance_package",
            source_package_status="packaged_for_trial_execution_planning",
            execution_plan_status="planned_candidate_replay_only",
            execution_scope="low_risk_controlled_trial_candidate",
            allowed_plan_operations=(
                "candidate_field_task_guidance_replay",
                "evidence_request_candidate_replay",
                "action_safety_candidate_check",
            ),
            execution_preconditions=common_preconditions,
            execution_constraints=(),
            blocked_operations=_merge_blocked(),
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=(ISSUANCE_PACKAGE_REF, PRE_RUNTIME_TRIAL_PACKAGE_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialExecutionPlanItem(
            plan_ref="subway_enter_station_execution_plan",
            issuance_package_ref="subway_enter_station_issuance_package",
            source_package_status="packaged_with_constraints_for_trial_execution_planning",
            execution_plan_status="planned_constrained_candidate_replay_only",
            execution_scope="cautious_candidate_trial",
            allowed_plan_operations=(
                "candidate_field_task_guidance_replay",
                "evidence_request_candidate_replay",
            ),
            execution_preconditions=common_preconditions,
            execution_constraints=(
                "gps_degraded_acknowledged",
                "local_spatial_evidence_required",
                "indoor_uncertainty_downgrade_required",
                "more_evidence_required_before_action_like_guidance",
            ),
            blocked_operations=_merge_blocked(
                "action_like_guidance_without_action_safety_candidate",
            ),
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=(ISSUANCE_PACKAGE_REF, PRE_RUNTIME_TRIAL_PACKAGE_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialExecutionPlanItem(
            plan_ref="stadium_concert_ticket_gate_execution_plan",
            issuance_package_ref="stadium_concert_ticket_gate_issuance_package",
            source_package_status="packaged_observation_only",
            execution_plan_status="planned_observation_replay_only",
            execution_scope="observation_only",
            allowed_plan_operations=(
                "event_overlay_validation_replay",
                "crowd_flow_risk_observation_replay",
                "ocr_sign_evidence_request_placeholder",
            ),
            execution_preconditions=common_preconditions,
            execution_constraints=(),
            blocked_operations=_merge_blocked(
                "movement_command",
                "route_activation",
            ),
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=(ISSUANCE_PACKAGE_REF, PRE_RUNTIME_TRIAL_PACKAGE_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialExecutionPlanItem(
            plan_ref="plaza_market_crowd_execution_plan",
            issuance_package_ref="plaza_market_crowd_issuance_package",
            source_package_status="packaged_observation_only",
            execution_plan_status="planned_observation_replay_only",
            execution_scope="observation_only",
            allowed_plan_operations=(
                "crowd_queue_risk_observation_replay",
                "temporary_layout_uncertainty_logging_replay",
                "wait_observe_candidate_replay",
            ),
            execution_preconditions=common_preconditions,
            execution_constraints=(),
            blocked_operations=_merge_blocked(
                "movement_guidance_trial",
                "route_activation",
            ),
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=(ISSUANCE_PACKAGE_REF, PRE_RUNTIME_TRIAL_PACKAGE_REF),
            source_chain=SOURCE_CHAIN,
        ),
        ControlledRuntimeTrialExecutionPlanItem(
            plan_ref="gps_slam_conflict_execution_plan",
            issuance_package_ref="gps_slam_conflict_issuance_package",
            source_package_status="packaged_as_blocked_record",
            execution_plan_status="blocked_no_execution_plan",
            execution_scope="blocked",
            allowed_plan_operations=(
                "conflict_record_review",
                "conflict_resolution_planning_placeholder",
            ),
            execution_preconditions=common_preconditions,
            execution_constraints=(),
            blocked_operations=_merge_blocked(
                "runtime_trial_execution",
                "route_activation",
                "action_like_guidance",
                "speech_guidance",
            ),
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=(ISSUANCE_PACKAGE_REF, PRE_RUNTIME_TRIAL_PACKAGE_REF),
            source_chain=SOURCE_CHAIN,
            plan_ready=False,
        ),
        ControlledRuntimeTrialExecutionPlanItem(
            plan_ref="home_return_execution_plan",
            issuance_package_ref="home_return_issuance_package",
            source_package_status="packaged_for_trial_execution_planning",
            execution_plan_status="planned_candidate_replay_only",
            execution_scope="low_risk_controlled_trial_candidate",
            allowed_plan_operations=(
                "candidate_field_task_guidance_replay",
                "coarse_map_route_candidate_replay",
                "local_spatial_check_candidate_replay",
                "action_safety_candidate_check",
            ),
            execution_preconditions=common_preconditions,
            execution_constraints=(),
            blocked_operations=_merge_blocked(),
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=(ISSUANCE_PACKAGE_REF, PRE_RUNTIME_TRIAL_PACKAGE_REF),
            source_chain=SOURCE_CHAIN,
        ),
    )


def build_shared_policies_v1() -> Dict[str, Any]:
    return {
        "precondition_policy": candidate_to_dict(
            ExecutionPreconditionPolicy(
                policy_ref="execution_precondition_policy_v1",
                source_chain_intact_required=True,
                rollback_policy_bound_required=True,
                observation_log_bound_required=True,
                no_live_sensor_required=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "blocked_operation_policy": candidate_to_dict(
            ExecutionBlockedOperationPolicy(
                policy_ref="execution_blocked_operation_policy_v1",
                blocked_operations=UNIVERSAL_BLOCKED_OPERATIONS,
                runtime_activation_blocked=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "rollback_trigger_policy": candidate_to_dict(
            ExecutionRollbackTriggerPolicy(
                policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
                rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
                fallback_observe_wait=True,
                candidate_only_rollback=True,
                human_ack_required=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "observation_log_plan": candidate_to_dict(
            ExecutionObservationLogPlan(
                plan_ref=OBSERVATION_LOG_PLAN_REF,
                observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
                log_execution_plan_status=True,
                log_preconditions=True,
                log_blocked_operations=True,
                log_manual_confirmation_points=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "failure_handling_plan": candidate_to_dict(
            ExecutionFailureHandlingPlan(
                plan_ref=FAILURE_HANDLING_PLAN_REF,
                failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
                downgrade_on_high_risk=True,
                block_on_unresolved_conflict=True,
                no_silent_runtime_escalation=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "audit_record": candidate_to_dict(
            ExecutionPlanningAuditRecord(
                audit_ref="execution_planning_audit_record_v1",
                issuance_package_go_verified=True,
                pre_runtime_trial_package_status_sealed=True,
                sealed_phase_one_chain_verified=True,
                execution_planning_not_runtime_execution=True,
                dry_run_replay_boundary_candidate_only=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_execution_planning_profile_v1() -> ControlledRuntimeTrialExecutionPlanningProfile:
    return ControlledRuntimeTrialExecutionPlanningProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        issuance_package_ref=ISSUANCE_PACKAGE_REF,
        pre_runtime_trial_package_status=PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        phase_one_chain_ref=PHASE_ONE_CHAIN_REF,
        phase_one_chain_status=PHASE_ONE_CHAIN_STATUS,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        execution_plan_item_refs=EXECUTION_PLAN_ITEM_REFS,
        manual_confirmation_points=MANUAL_CONFIRMATION_POINTS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=EXECUTION_PLANNING_GOVERNANCE_RULES,
        candidate_only_source_chain_required=CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    )


def build_execution_plan_go_map(
    items: Tuple[ControlledRuntimeTrialExecutionPlanItem, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for item in items:
        go_key, expected_status, expected_ready = _PLAN_GO_KEY_MAP[item.plan_ref]
        if go_key == "gps_slam_conflict_execution_plan_blocked":
            result[go_key] = (
                item.execution_plan_status == expected_status and item.plan_ready is False
            )
        else:
            result[go_key] = (
                item.execution_plan_status == expected_status and item.plan_ready is expected_ready
            )
    return result


def build_execution_planning_decision_v1(
    *,
    issuance_package_go_verified: bool,
    pre_runtime_trial_package_status_sealed: bool,
    sealed_phase_one_chain_verified: bool,
    scenario_scope_preserved_for_all: bool,
) -> ControlledRuntimeTrialExecutionPlanningDecision:
    return ControlledRuntimeTrialExecutionPlanningDecision(
        decision_ref="controlled_runtime_trial_execution_planning_decision_v1",
        profile_ref=PROFILE_REF,
        execution_planning_profile_count=1,
        execution_plan_item_count=len(EXECUTION_PLAN_ITEM_REFS),
        issuance_package_go_verified=issuance_package_go_verified,
        pre_runtime_trial_package_status_sealed=pre_runtime_trial_package_status_sealed,
        sealed_phase_one_chain_verified=sealed_phase_one_chain_verified,
        scenario_scope_preserved_for_all=scenario_scope_preserved_for_all,
        final_decision=FINAL_DECISION_GO,
    )


def build_phase_one_environment_cognition_runtime_trial_execution_planning_matrix_v1() -> Dict[str, Any]:
    profile = build_execution_planning_profile_v1()
    items = build_execution_plan_items_v1()
    shared = build_shared_policies_v1()
    decision = build_execution_planning_decision_v1(
        issuance_package_go_verified=True,
        pre_runtime_trial_package_status_sealed=True,
        sealed_phase_one_chain_verified=True,
        scenario_scope_preserved_for_all=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "execution_planning_principle_zh": EXECUTION_PLANNING_PRINCIPLE_ZH,
        "controlled_runtime_trial_execution_planning_profile": candidate_to_dict(profile),
        "execution_plan_items": [candidate_to_dict(i) for i in items],
        "shared_policies": shared,
        "execution_planning_decision": candidate_to_dict(decision),
        "execution_plan_go_map": build_execution_plan_go_map(items),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "issuance_package_artifact_rel": _ISSUANCE_ARTIFACT_REL,
        "execution_planning_governance_rules": list(EXECUTION_PLANNING_GOVERNANCE_RULES),
        "universal_blocked_operations": list(UNIVERSAL_BLOCKED_OPERATIONS),
        "manual_confirmation_points": list(MANUAL_CONFIRMATION_POINTS),
        "next_phase_ref": NEXT_PHASE_REF,
    }
