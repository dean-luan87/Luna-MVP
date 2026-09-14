# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Execution Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Execution-Planning-v1-001"
SCOPE = "phase_one_environment_cognition_runtime_trial_execution_planning_review_only"
SOURCE_CHAIN = "phase_one_environment_cognition_runtime_trial_execution_planning_v1"

EXECUTION_PLANNING_PRINCIPLE_ZH = (
    "基于已封口的 controlled runtime trial issuance package 生成 execution planning；"
    "明确执行前计划、blocker、dry-run replay 边界、人工确认点与回滚触发条件，不执行真实 runtime。"
)

ISSUANCE_PACKAGE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Issuance-Package-v1-001"
)
PRE_RUNTIME_TRIAL_PACKAGE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Package-Closure-Readiness-Review-v1-001"
)
PLANNING_REF = "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Planning-v1-001"
OWNER_APPROVAL_REQUEST_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Owner-Approval-Request-v1-001"
)
OWNER_APPROVAL_ISSUANCE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Owner-Approval-Issuance-v1-001"
)
PACKAGE_BOUNDARY_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Package-Boundary-Planning-v1-001"
)
PHASE_ONE_CHAIN_REF = "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
PHASE_ONE_CHAIN_STATUS = "sealed"
PRE_RUNTIME_TRIAL_PACKAGE_STATUS = "sealed"
RUNTIME_TRIAL_MODE = "execution_planning_only"
CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED = True

FINAL_DECISION_GO = "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_EXECUTION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_EXECUTION_PLANNING_BLOCKED"

NEXT_PHASE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Execution-Planning-Closure-Trial-Readiness-Gate-v1-001"
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "ControlledRuntimeTrialExecutionPlanningProfile",
    "ControlledRuntimeTrialExecutionPlanItem",
    "ExecutionPreconditionPolicy",
    "ExecutionBlockedOperationPolicy",
    "ExecutionRollbackTriggerPolicy",
    "ExecutionObservationLogPlan",
    "ExecutionFailureHandlingPlan",
    "ExecutionPlanningAuditRecord",
    "ControlledRuntimeTrialExecutionPlanningDecision",
)

EXECUTION_PLAN_ITEM_REFS: Tuple[str, ...] = (
    "mall_find_entrance_execution_plan",
    "subway_enter_station_execution_plan",
    "stadium_concert_ticket_gate_execution_plan",
    "plaza_market_crowd_execution_plan",
    "gps_slam_conflict_execution_plan",
    "home_return_execution_plan",
)

ISSUANCE_PACKAGE_REF_MAP: Dict[str, str] = {
    "mall_find_entrance_execution_plan": "mall_find_entrance_issuance_package",
    "subway_enter_station_execution_plan": "subway_enter_station_issuance_package",
    "stadium_concert_ticket_gate_execution_plan": "stadium_concert_ticket_gate_issuance_package",
    "plaza_market_crowd_execution_plan": "plaza_market_crowd_issuance_package",
    "gps_slam_conflict_execution_plan": "gps_slam_conflict_issuance_package",
    "home_return_execution_plan": "home_return_issuance_package",
}

EXECUTION_PLAN_GO_KEYS: Tuple[str, ...] = (
    "mall_find_entrance_execution_plan_ready",
    "subway_enter_station_constrained_execution_plan_ready",
    "stadium_concert_observation_execution_plan_ready",
    "plaza_market_observation_execution_plan_ready",
    "gps_slam_conflict_execution_plan_blocked",
    "home_return_execution_plan_ready",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    PHASE_ONE_CHAIN_REF,
    PLANNING_REF,
    OWNER_APPROVAL_REQUEST_REF,
    OWNER_APPROVAL_ISSUANCE_REF,
    PACKAGE_BOUNDARY_REF,
    PRE_RUNTIME_TRIAL_PACKAGE_REF,
    ISSUANCE_PACKAGE_REF,
    "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001",
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001",
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
)

EXECUTION_PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "execution_planning_is_not_runtime_execution",
    "execution_plan_only_authorizes_future_planning_review_not_runtime_start",
    "scenario_scope_must_remain_unchanged_from_issuance_package",
    "blocked_scenario_must_remain_blocked_and_must_not_receive_execution_plan",
    "observation_only_scenarios_must_remain_observation_replay_only",
    "constrained_scenario_must_preserve_all_constraints",
    "low_risk_trial_candidates_remain_candidate_replay_only_in_this_phase",
    "every_execution_plan_must_bind_rollback_trigger_policy",
    "every_execution_plan_must_bind_observation_log_plan",
    "every_execution_plan_must_bind_failure_handling_plan",
    "allowed_execution_plan_operations_must_remain_candidate_only",
    "blocked_operations_must_include_runtime_activation_direct_action_speech_fact_write_real_navigation_live_sensor",
    "all_source_chain_and_upstream_refs_must_be_preserved",
    "commercial_runtime_approval_not_implied",
)

UNIVERSAL_BLOCKED_OPERATIONS: Tuple[str, ...] = (
    "runtime_activation",
    "direct_action",
    "direct_speech_tts",
    "direct_fact_write",
    "real_navigation",
    "live_sensor_trigger",
)

MANUAL_CONFIRMATION_POINTS: Tuple[str, ...] = (
    "owner_review_before_any_future_runtime_trial",
    "human_ack_before_candidate_replay_batch",
    "human_ack_before_rollback_trigger_evaluation",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "execution_planning_only": True,
    "execution_planning_not_runtime_execution": True,
    "runtime_activation_allowed": False,
    "trial_runtime_started": False,
    "no_real_navigation": True,
    "no_real_map_api": True,
    "no_real_gps_gnss": True,
    "no_live_sensor": True,
    "real_navigation_started": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "live_sensor_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
    "runtime_activation_deferred": True,
}


@dataclass(frozen=True)
class ControlledRuntimeTrialExecutionPlanningProfile:
    profile_ref: str
    phase_id: str
    issuance_package_ref: str
    pre_runtime_trial_package_status: str
    phase_one_chain_ref: str
    phase_one_chain_status: str
    runtime_trial_mode: str
    execution_plan_item_refs: Tuple[str, ...]
    manual_confirmation_points: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only_source_chain_required: bool = True


@dataclass(frozen=True)
class ControlledRuntimeTrialExecutionPlanItem:
    plan_ref: str
    issuance_package_ref: str
    source_package_status: str
    execution_plan_status: str
    execution_scope: str
    allowed_plan_operations: Tuple[str, ...]
    execution_preconditions: Tuple[str, ...]
    execution_constraints: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    rollback_trigger_policy_ref: str
    observation_log_plan_ref: str
    failure_handling_plan_ref: str
    upstream_refs: Tuple[str, ...]
    source_chain: str
    plan_ready: bool = True


@dataclass(frozen=True)
class ExecutionPreconditionPolicy:
    policy_ref: str
    source_chain_intact_required: bool
    rollback_policy_bound_required: bool
    observation_log_bound_required: bool
    no_live_sensor_required: bool
    source_chain: str


@dataclass(frozen=True)
class ExecutionBlockedOperationPolicy:
    policy_ref: str
    blocked_operations: Tuple[str, ...]
    runtime_activation_blocked: bool
    source_chain: str


@dataclass(frozen=True)
class ExecutionRollbackTriggerPolicy:
    policy_ref: str
    rollback_trigger_policy_ref: str
    fallback_observe_wait: bool
    candidate_only_rollback: bool
    human_ack_required: bool
    source_chain: str


@dataclass(frozen=True)
class ExecutionObservationLogPlan:
    plan_ref: str
    observation_log_plan_ref: str
    log_execution_plan_status: bool
    log_preconditions: bool
    log_blocked_operations: bool
    log_manual_confirmation_points: bool
    source_chain: str


@dataclass(frozen=True)
class ExecutionFailureHandlingPlan:
    plan_ref: str
    failure_handling_plan_ref: str
    downgrade_on_high_risk: bool
    block_on_unresolved_conflict: bool
    no_silent_runtime_escalation: bool
    source_chain: str


@dataclass(frozen=True)
class ExecutionPlanningAuditRecord:
    audit_ref: str
    issuance_package_go_verified: bool
    pre_runtime_trial_package_status_sealed: bool
    sealed_phase_one_chain_verified: bool
    execution_planning_not_runtime_execution: bool
    dry_run_replay_boundary_candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class ControlledRuntimeTrialExecutionPlanningDecision:
    decision_ref: str
    profile_ref: str
    execution_planning_profile_count: int
    execution_plan_item_count: int
    issuance_package_go_verified: bool
    pre_runtime_trial_package_status_sealed: bool
    sealed_phase_one_chain_verified: bool
    scenario_scope_preserved_for_all: bool
    final_decision: str
    runtime_activation_allowed: bool = False
    trial_runtime_started: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
