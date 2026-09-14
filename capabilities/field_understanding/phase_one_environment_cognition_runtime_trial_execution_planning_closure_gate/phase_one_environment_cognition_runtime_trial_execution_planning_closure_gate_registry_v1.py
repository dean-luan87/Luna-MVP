# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Runtime Trial Execution Planning Closure Gate — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate.phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_types_v1 import (
    CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    CLOSURE_GATE_GOVERNANCE_RULES,
    CLOSURE_GATE_PRINCIPLE_ZH,
    EXECUTION_PLANNING_REF,
    EXECUTION_PLAN_REF_MAP,
    ExecutionPlanningClosureGateDecision,
    ExecutionPlanningClosureGateProfile,
    ExecutionPlanningClosureStageRef,
    FINAL_DECISION_GO,
    ISSUANCE_PACKAGE_REF,
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
    READINESS_GATE_GO_KEYS,
    READINESS_GATE_ITEM_REFS,
    RUNTIME_TRIAL_MODE,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    UNIVERSAL_BLOCKED_OPERATIONS,
    TrialReadinessBlockedRecord,
    TrialReadinessGateItem,
    TrialReadinessGatePolicy,
    TrialReadinessHumanAckRequirement,
    TrialReadinessObservationReadiness,
    TrialReadinessRollbackReadiness,
    candidate_to_dict,
)

REGISTRY_ID = "phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_registry_v1"
PROFILE_REF = "execution_planning_closure_gate_profile_v1"
ROLLBACK_TRIGGER_POLICY_REF = "runtime_trial_execution_rollback_trigger_v1"
OBSERVATION_LOG_PLAN_REF = "runtime_trial_execution_observation_log_plan_v1"
FAILURE_HANDLING_PLAN_REF = "runtime_trial_execution_failure_handling_plan_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "readiness_gate_item_refs": READINESS_GATE_ITEM_REFS,
    "readiness_gate_go_keys": READINESS_GATE_GO_KEYS,
    "closure_gate_governance_rules": CLOSURE_GATE_GOVERNANCE_RULES,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
    "universal_blocked_operations": UNIVERSAL_BLOCKED_OPERATIONS,
    "execution_plan_ref_map": tuple(EXECUTION_PLAN_REF_MAP.items()),
}

_GATE_GO_KEY_MAP: Dict[str, Tuple[str, str, str, bool]] = {
    "mall_find_entrance_readiness_gate": (
        "mall_find_entrance_ready_for_controlled_replay_trial_planning",
        "planned_candidate_replay_only",
        "ready_for_controlled_replay_trial_planning",
        True,
    ),
    "subway_enter_station_readiness_gate": (
        "subway_enter_station_ready_with_constraints",
        "planned_constrained_candidate_replay_only",
        "ready_with_constraints_for_controlled_replay_trial_planning",
        True,
    ),
    "stadium_concert_ticket_gate_readiness_gate": (
        "stadium_concert_observation_ready_for_replay_planning",
        "planned_observation_replay_only",
        "observation_only_ready_for_replay_planning",
        True,
    ),
    "plaza_market_crowd_readiness_gate": (
        "plaza_market_observation_ready_for_replay_planning",
        "planned_observation_replay_only",
        "observation_only_ready_for_replay_planning",
        True,
    ),
    "gps_slam_conflict_readiness_gate": (
        "gps_slam_conflict_blocked_preserved",
        "blocked_no_execution_plan",
        "blocked_preserved",
        False,
    ),
    "home_return_readiness_gate": (
        "home_return_ready_for_controlled_replay_trial_planning",
        "planned_candidate_replay_only",
        "ready_for_controlled_replay_trial_planning",
        True,
    ),
}

_EXECUTION_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/phase_one_environment_cognition_runtime_trial_execution_planning_v1_smoke_v0/"
    "phase_one_environment_cognition_runtime_trial_execution_planning_review_v1.json"
)

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
        "phase_ref": EXECUTION_PLANNING_REF,
        "artifact_rel": _EXECUTION_PLANNING_ARTIFACT_REL,
        "expected_go": "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_EXECUTION_PLANNING_GO",
        "module_rel": (
            "capabilities/field_understanding/phase_one_environment_cognition_runtime_trial_execution_planning/"
            "phase_one_environment_cognition_runtime_trial_execution_planning_types_v1.py"
        ),
        "require_go": True,
        "require_execution_planning_go": True,
    },
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
    if len(READINESS_GATE_ITEM_REFS) != 6:
        issues.append("readiness_gate_item_refs_count_not_6")
    if len(READINESS_GATE_GO_KEYS) != 6:
        issues.append("readiness_gate_go_keys_count_not_6")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 12:
        issues.append("sealed_upstream_phase_refs_count_not_12")
    if len(CLOSURE_GATE_GOVERNANCE_RULES) != 14:
        issues.append("closure_gate_governance_rules_count_not_14")
    if len(EXECUTION_PLAN_REF_MAP) != 6:
        issues.append("execution_plan_ref_map_count_not_6")
    return len(issues) == 0, issues


def _merge_blocked(*ops: str) -> Tuple[str, ...]:
    merged = list(UNIVERSAL_BLOCKED_OPERATIONS)
    for op in ops:
        if op not in merged:
            merged.append(op)
    return tuple(merged)


def build_closure_gate_stage_ref_v1() -> ExecutionPlanningClosureStageRef:
    return ExecutionPlanningClosureStageRef(
        stage_ref="execution_planning_closure_trial_readiness_gate_stage_v1",
        phase_ref=PHASE_ID,
        stage_zh=CLOSURE_GATE_PRINCIPLE_ZH,
        stage_closed=True,
        source_chain=SOURCE_CHAIN,
    )


def build_readiness_gate_items_v1() -> Tuple[TrialReadinessGateItem, ...]:
    common_upstream = (EXECUTION_PLANNING_REF, ISSUANCE_PACKAGE_REF, PRE_RUNTIME_TRIAL_PACKAGE_REF)
    return (
        TrialReadinessGateItem(
            gate_ref="mall_find_entrance_readiness_gate",
            execution_plan_ref="mall_find_entrance_execution_plan",
            source_execution_plan_status="planned_candidate_replay_only",
            readiness_gate_status="ready_for_controlled_replay_trial_planning",
            gate_scope="low_risk_controlled_trial_candidate",
            gate_requirements=(
                "owner_review_required",
                "human_ack_before_replay_batch",
                "action_safety_candidate_required",
                "rollback_trigger_policy_bound",
                "observation_log_plan_bound",
            ),
            gate_constraints=(),
            blocked_operations=_merge_blocked(),
            allowed_next_step="controlled_replay_trial_planning_only",
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=common_upstream,
            source_chain=SOURCE_CHAIN,
            gate_passed=True,
            replay_capable=True,
        ),
        TrialReadinessGateItem(
            gate_ref="subway_enter_station_readiness_gate",
            execution_plan_ref="subway_enter_station_execution_plan",
            source_execution_plan_status="planned_constrained_candidate_replay_only",
            readiness_gate_status="ready_with_constraints_for_controlled_replay_trial_planning",
            gate_scope="cautious_candidate_trial",
            gate_requirements=(
                "gps_degraded_acknowledged",
                "local_spatial_evidence_required",
                "indoor_uncertainty_downgrade_required",
                "more_evidence_required_before_action_like_guidance",
                "human_ack_before_replay_batch",
            ),
            gate_constraints=(
                "gps_degraded_acknowledged",
                "local_spatial_evidence_required",
                "indoor_uncertainty_downgrade_required",
                "more_evidence_required_before_action_like_guidance",
            ),
            blocked_operations=_merge_blocked(
                "action_like_guidance_without_action_safety_candidate",
            ),
            allowed_next_step="constrained_controlled_replay_trial_planning_only",
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=common_upstream,
            source_chain=SOURCE_CHAIN,
            gate_passed=True,
            replay_capable=True,
        ),
        TrialReadinessGateItem(
            gate_ref="stadium_concert_ticket_gate_readiness_gate",
            execution_plan_ref="stadium_concert_ticket_gate_execution_plan",
            source_execution_plan_status="planned_observation_replay_only",
            readiness_gate_status="observation_only_ready_for_replay_planning",
            gate_scope="observation_only",
            gate_requirements=(
                "crowd_flow_risk_observation",
                "event_overlay_label_validation",
                "no_movement_command",
                "human_ack_before_replay_batch",
            ),
            gate_constraints=("no_movement_command",),
            blocked_operations=_merge_blocked(
                "route_activation",
                "movement_command",
            ),
            allowed_next_step="observation_controlled_replay_trial_planning_only",
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=common_upstream,
            source_chain=SOURCE_CHAIN,
            gate_passed=True,
            replay_capable=True,
        ),
        TrialReadinessGateItem(
            gate_ref="plaza_market_crowd_readiness_gate",
            execution_plan_ref="plaza_market_crowd_execution_plan",
            source_execution_plan_status="planned_observation_replay_only",
            readiness_gate_status="observation_only_ready_for_replay_planning",
            gate_scope="observation_only",
            gate_requirements=(
                "crowd_queue_risk_observation",
                "temporary_layout_uncertainty_logging",
                "wait_observe_candidate_only",
                "human_ack_before_replay_batch",
            ),
            gate_constraints=("wait_observe_candidate_only",),
            blocked_operations=_merge_blocked(
                "movement_guidance_trial",
                "route_activation",
            ),
            allowed_next_step="observation_controlled_replay_trial_planning_only",
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=common_upstream,
            source_chain=SOURCE_CHAIN,
            gate_passed=True,
            replay_capable=True,
        ),
        TrialReadinessGateItem(
            gate_ref="gps_slam_conflict_readiness_gate",
            execution_plan_ref="gps_slam_conflict_execution_plan",
            source_execution_plan_status="blocked_no_execution_plan",
            readiness_gate_status="blocked_preserved",
            gate_scope="blocked",
            gate_requirements=(
                "conflict_resolution_planning_required",
                "no_execution_plan",
            ),
            gate_constraints=(),
            blocked_operations=_merge_blocked(
                "controlled_replay_trial_planning",
                "runtime_trial_execution",
                "route_activation",
                "action_like_guidance",
                "speech_guidance",
            ),
            allowed_next_step="conflict_resolution_planning_only",
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=common_upstream,
            source_chain=SOURCE_CHAIN,
            gate_passed=False,
            replay_capable=False,
        ),
        TrialReadinessGateItem(
            gate_ref="home_return_readiness_gate",
            execution_plan_ref="home_return_execution_plan",
            source_execution_plan_status="planned_candidate_replay_only",
            readiness_gate_status="ready_for_controlled_replay_trial_planning",
            gate_scope="low_risk_controlled_trial_candidate",
            gate_requirements=(
                "owner_review_required",
                "human_ack_before_replay_batch",
                "action_safety_candidate_required",
                "rollback_trigger_policy_bound",
                "observation_log_plan_bound",
            ),
            gate_constraints=(),
            blocked_operations=_merge_blocked(),
            allowed_next_step="controlled_replay_trial_planning_only",
            rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
            observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
            failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
            upstream_refs=common_upstream,
            source_chain=SOURCE_CHAIN,
            gate_passed=True,
            replay_capable=True,
        ),
    )


def build_shared_gate_policies_v1() -> Dict[str, Any]:
    return {
        "gate_policy": candidate_to_dict(
            TrialReadinessGatePolicy(
                policy_ref="trial_readiness_gate_policy_v1",
                readiness_gate_not_runtime_execution=True,
                allowed_next_step_planning_only=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "blocked_record": candidate_to_dict(
            TrialReadinessBlockedRecord(
                record_ref="trial_readiness_blocked_record_v1",
                blocked_scenario_remains_blocked=True,
                blocked_scenario_cannot_pass_readiness_gate=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "human_ack_requirement": candidate_to_dict(
            TrialReadinessHumanAckRequirement(
                requirement_ref="trial_readiness_human_ack_requirement_v1",
                human_ack_declared_for_replay_capable_scenarios=True,
                owner_review_required=True,
                human_ack_before_replay_batch=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "rollback_readiness": candidate_to_dict(
            TrialReadinessRollbackReadiness(
                readiness_ref="trial_readiness_rollback_readiness_v1",
                rollback_trigger_policy_ref=ROLLBACK_TRIGGER_POLICY_REF,
                rollback_readiness_bound_for_replay_capable_scenarios=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
        "observation_readiness": candidate_to_dict(
            TrialReadinessObservationReadiness(
                readiness_ref="trial_readiness_observation_readiness_v1",
                observation_log_plan_ref=OBSERVATION_LOG_PLAN_REF,
                failure_handling_plan_ref=FAILURE_HANDLING_PLAN_REF,
                observation_log_readiness_bound_for_replay_capable_scenarios=True,
                failure_handling_readiness_bound_for_replay_capable_scenarios=True,
                source_chain=SOURCE_CHAIN,
            )
        ),
    }


def build_closure_gate_profile_v1() -> ExecutionPlanningClosureGateProfile:
    return ExecutionPlanningClosureGateProfile(
        profile_ref=PROFILE_REF,
        phase_id=PHASE_ID,
        execution_planning_ref=EXECUTION_PLANNING_REF,
        issuance_package_ref=ISSUANCE_PACKAGE_REF,
        pre_runtime_trial_package_status=PRE_RUNTIME_TRIAL_PACKAGE_STATUS,
        phase_one_chain_ref=PHASE_ONE_CHAIN_REF,
        phase_one_chain_status=PHASE_ONE_CHAIN_STATUS,
        runtime_trial_mode=RUNTIME_TRIAL_MODE,
        readiness_gate_item_refs=READINESS_GATE_ITEM_REFS,
        sealed_upstream_phase_refs=SEALED_UPSTREAM_PHASE_REFS,
        governance_rules=CLOSURE_GATE_GOVERNANCE_RULES,
        candidate_only_source_chain_required=CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED,
    )


def build_readiness_gate_go_map(
    items: Tuple[TrialReadinessGateItem, ...],
) -> Dict[str, bool]:
    result: Dict[str, bool] = {}
    for item in items:
        go_key, expected_status, expected_gate_status, expected_passed = _GATE_GO_KEY_MAP[item.gate_ref]
        if go_key == "gps_slam_conflict_blocked_preserved":
            result[go_key] = (
                item.source_execution_plan_status == expected_status
                and item.readiness_gate_status == expected_gate_status
                and item.gate_passed is False
            )
        else:
            result[go_key] = (
                item.source_execution_plan_status == expected_status
                and item.readiness_gate_status == expected_gate_status
                and item.gate_passed is expected_passed
            )
    return result


def build_closure_gate_decision_v1(
    *,
    execution_planning_go_verified: bool,
    issuance_package_go_verified: bool,
    pre_runtime_trial_package_status_sealed: bool,
    sealed_phase_one_chain_verified: bool,
    scenario_scope_preserved_for_all: bool,
) -> ExecutionPlanningClosureGateDecision:
    return ExecutionPlanningClosureGateDecision(
        decision_ref="execution_planning_closure_gate_decision_v1",
        profile_ref=PROFILE_REF,
        closure_gate_profile_count=1,
        readiness_gate_item_count=len(READINESS_GATE_ITEM_REFS),
        execution_planning_go_verified=execution_planning_go_verified,
        issuance_package_go_verified=issuance_package_go_verified,
        pre_runtime_trial_package_status_sealed=pre_runtime_trial_package_status_sealed,
        sealed_phase_one_chain_verified=sealed_phase_one_chain_verified,
        scenario_scope_preserved_for_all=scenario_scope_preserved_for_all,
        final_decision=FINAL_DECISION_GO,
    )


def build_phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_matrix_v1() -> Dict[str, Any]:
    profile = build_closure_gate_profile_v1()
    stage_ref = build_closure_gate_stage_ref_v1()
    items = build_readiness_gate_items_v1()
    shared = build_shared_gate_policies_v1()
    decision = build_closure_gate_decision_v1(
        execution_planning_go_verified=True,
        issuance_package_go_verified=True,
        pre_runtime_trial_package_status_sealed=True,
        sealed_phase_one_chain_verified=True,
        scenario_scope_preserved_for_all=True,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "closure_gate_principle_zh": CLOSURE_GATE_PRINCIPLE_ZH,
        "execution_planning_closure_gate_profile": candidate_to_dict(profile),
        "execution_planning_closure_stage_ref": candidate_to_dict(stage_ref),
        "readiness_gate_items": [candidate_to_dict(i) for i in items],
        "shared_gate_policies": shared,
        "closure_gate_decision": candidate_to_dict(decision),
        "readiness_gate_go_map": build_readiness_gate_go_map(items),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
        "execution_planning_artifact_rel": _EXECUTION_PLANNING_ARTIFACT_REL,
        "closure_gate_governance_rules": list(CLOSURE_GATE_GOVERNANCE_RULES),
        "universal_blocked_operations": list(UNIVERSAL_BLOCKED_OPERATIONS),
        "next_phase_ref": NEXT_PHASE_REF,
    }
