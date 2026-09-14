# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Runtime Trial Execution Planning Closure Gate — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Execution-Planning-Closure-Trial-Readiness-Gate-v1-001"
)
SCOPE = "phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_review_only"
SOURCE_CHAIN = "phase_one_environment_cognition_runtime_trial_execution_planning_closure_gate_v1"

CLOSURE_GATE_PRINCIPLE_ZH = (
    "对 controlled runtime trial execution planning 做 closure review，"
    "形成 Trial Readiness Gate；仅允许未来 controlled replay trial planning，不执行真实 runtime。"
)

EXECUTION_PLANNING_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Execution-Planning-v1-001"
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
RUNTIME_TRIAL_MODE = "execution_planning_closure_gate_only"
CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED = True

FINAL_DECISION_GO = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_EXECUTION_PLANNING_CLOSURE_GATE_GO"
)
FINAL_DECISION_BLOCKED = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_EXECUTION_PLANNING_CLOSURE_GATE_BLOCKED"
)

NEXT_PHASE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Controlled-Replay-Trial-Planning-v1-001"
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "ExecutionPlanningClosureGateProfile",
    "ExecutionPlanningClosureStageRef",
    "TrialReadinessGateItem",
    "TrialReadinessGatePolicy",
    "TrialReadinessBlockedRecord",
    "TrialReadinessHumanAckRequirement",
    "TrialReadinessRollbackReadiness",
    "TrialReadinessObservationReadiness",
    "ExecutionPlanningClosureGateDecision",
)

READINESS_GATE_ITEM_REFS: Tuple[str, ...] = (
    "mall_find_entrance_readiness_gate",
    "subway_enter_station_readiness_gate",
    "stadium_concert_ticket_gate_readiness_gate",
    "plaza_market_crowd_readiness_gate",
    "gps_slam_conflict_readiness_gate",
    "home_return_readiness_gate",
)

EXECUTION_PLAN_REF_MAP: Dict[str, str] = {
    "mall_find_entrance_readiness_gate": "mall_find_entrance_execution_plan",
    "subway_enter_station_readiness_gate": "subway_enter_station_execution_plan",
    "stadium_concert_ticket_gate_readiness_gate": "stadium_concert_ticket_gate_execution_plan",
    "plaza_market_crowd_readiness_gate": "plaza_market_crowd_execution_plan",
    "gps_slam_conflict_readiness_gate": "gps_slam_conflict_execution_plan",
    "home_return_readiness_gate": "home_return_execution_plan",
}

READINESS_GATE_GO_KEYS: Tuple[str, ...] = (
    "mall_find_entrance_ready_for_controlled_replay_trial_planning",
    "subway_enter_station_ready_with_constraints",
    "stadium_concert_observation_ready_for_replay_planning",
    "plaza_market_observation_ready_for_replay_planning",
    "gps_slam_conflict_blocked_preserved",
    "home_return_ready_for_controlled_replay_trial_planning",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    PHASE_ONE_CHAIN_REF,
    PLANNING_REF,
    OWNER_APPROVAL_REQUEST_REF,
    OWNER_APPROVAL_ISSUANCE_REF,
    PACKAGE_BOUNDARY_REF,
    PRE_RUNTIME_TRIAL_PACKAGE_REF,
    ISSUANCE_PACKAGE_REF,
    EXECUTION_PLANNING_REF,
    "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001",
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001",
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
)

CLOSURE_GATE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "execution_planning_closure_gate_is_not_runtime_execution",
    "readiness_gate_only_allows_future_controlled_replay_trial_planning",
    "scenario_scope_must_remain_unchanged_from_execution_planning",
    "blocked_scenario_must_remain_blocked_and_cannot_pass_readiness_gate",
    "observation_only_scenarios_must_remain_observation_only_replay_planning",
    "constrained_scenario_must_preserve_all_constraints",
    "low_risk_scenarios_do_not_start_runtime",
    "human_ack_requirements_must_be_declared_for_replay_capable_scenarios",
    "rollback_readiness_must_be_bound_for_replay_capable_scenarios",
    "observation_log_readiness_must_be_bound_for_replay_capable_scenarios",
    "allowed_next_step_must_remain_planning_only",
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

PLANNING_ONLY_NEXT_STEPS: Tuple[str, ...] = (
    "controlled_replay_trial_planning_only",
    "constrained_controlled_replay_trial_planning_only",
    "observation_controlled_replay_trial_planning_only",
    "conflict_resolution_planning_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "execution_planning_closure_gate_only": True,
    "readiness_gate_not_runtime_execution": True,
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
class ExecutionPlanningClosureGateProfile:
    profile_ref: str
    phase_id: str
    execution_planning_ref: str
    issuance_package_ref: str
    pre_runtime_trial_package_status: str
    phase_one_chain_ref: str
    phase_one_chain_status: str
    runtime_trial_mode: str
    readiness_gate_item_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only_source_chain_required: bool = True


@dataclass(frozen=True)
class ExecutionPlanningClosureStageRef:
    stage_ref: str
    phase_ref: str
    stage_zh: str
    stage_closed: bool
    source_chain: str


@dataclass(frozen=True)
class TrialReadinessGateItem:
    gate_ref: str
    execution_plan_ref: str
    source_execution_plan_status: str
    readiness_gate_status: str
    gate_scope: str
    gate_requirements: Tuple[str, ...]
    gate_constraints: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    allowed_next_step: str
    rollback_trigger_policy_ref: str
    observation_log_plan_ref: str
    failure_handling_plan_ref: str
    upstream_refs: Tuple[str, ...]
    source_chain: str
    gate_passed: bool = True
    replay_capable: bool = True


@dataclass(frozen=True)
class TrialReadinessGatePolicy:
    policy_ref: str
    readiness_gate_not_runtime_execution: bool
    allowed_next_step_planning_only: bool
    source_chain: str


@dataclass(frozen=True)
class TrialReadinessBlockedRecord:
    record_ref: str
    blocked_scenario_remains_blocked: bool
    blocked_scenario_cannot_pass_readiness_gate: bool
    source_chain: str


@dataclass(frozen=True)
class TrialReadinessHumanAckRequirement:
    requirement_ref: str
    human_ack_declared_for_replay_capable_scenarios: bool
    owner_review_required: bool
    human_ack_before_replay_batch: bool
    source_chain: str


@dataclass(frozen=True)
class TrialReadinessRollbackReadiness:
    readiness_ref: str
    rollback_trigger_policy_ref: str
    rollback_readiness_bound_for_replay_capable_scenarios: bool
    source_chain: str


@dataclass(frozen=True)
class TrialReadinessObservationReadiness:
    readiness_ref: str
    observation_log_plan_ref: str
    failure_handling_plan_ref: str
    observation_log_readiness_bound_for_replay_capable_scenarios: bool
    failure_handling_readiness_bound_for_replay_capable_scenarios: bool
    source_chain: str


@dataclass(frozen=True)
class ExecutionPlanningClosureGateDecision:
    decision_ref: str
    profile_ref: str
    closure_gate_profile_count: int
    readiness_gate_item_count: int
    execution_planning_go_verified: bool
    issuance_package_go_verified: bool
    pre_runtime_trial_package_status_sealed: bool
    sealed_phase_one_chain_verified: bool
    scenario_scope_preserved_for_all: bool
    final_decision: str
    runtime_activation_allowed: bool = False
    trial_runtime_started: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
