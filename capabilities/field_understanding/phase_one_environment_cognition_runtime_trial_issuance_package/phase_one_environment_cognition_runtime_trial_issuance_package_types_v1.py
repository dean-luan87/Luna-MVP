# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Issuance Package — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Issuance-Package-v1-001"
SCOPE = "phase_one_environment_cognition_runtime_trial_issuance_package_review_only"
SOURCE_CHAIN = "phase_one_environment_cognition_runtime_trial_issuance_package_v1"

ISSUANCE_PACKAGE_PRINCIPLE_ZH = (
    "基于已封存的 runtime trial 前置包生成 controlled runtime trial issuance package；"
    "仅授权下一阶段 trial execution planning，不启动真实 runtime。"
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
RUNTIME_TRIAL_MODE = "issuance_package_only"
CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED = True

FINAL_DECISION_GO = "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_ISSUANCE_PACKAGE_GO"
FINAL_DECISION_BLOCKED = "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_ISSUANCE_PACKAGE_BLOCKED"

NEXT_PHASE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Execution-Planning-v1-001"
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "ControlledRuntimeTrialIssuancePackageProfile",
    "ControlledRuntimeTrialIssuancePackageItem",
    "IssuedTrialPackageScope",
    "IssuedTrialPackageBoundary",
    "IssuedTrialPackageControlBinding",
    "IssuedTrialPackageBlockerRecord",
    "IssuedTrialPackageAuditRecord",
    "ControlledRuntimeTrialIssuancePackageDecision",
)

ISSUANCE_PACKAGE_ITEM_REFS: Tuple[str, ...] = (
    "mall_find_entrance_issuance_package",
    "subway_enter_station_issuance_package",
    "stadium_concert_ticket_gate_issuance_package",
    "plaza_market_crowd_issuance_package",
    "gps_slam_conflict_issuance_package",
    "home_return_issuance_package",
)

CLOSURE_SCENARIO_REF_MAP: Dict[str, str] = {
    "mall_find_entrance_issuance_package": "mall_find_entrance_package",
    "subway_enter_station_issuance_package": "subway_enter_station_package",
    "stadium_concert_ticket_gate_issuance_package": "stadium_concert_ticket_gate_package",
    "plaza_market_crowd_issuance_package": "plaza_market_crowd_package",
    "gps_slam_conflict_issuance_package": "gps_slam_conflict_package",
    "home_return_issuance_package": "home_return_package",
}

ISSUANCE_PACKAGE_GO_KEYS: Tuple[str, ...] = (
    "mall_find_entrance_packaged_for_trial_execution_planning",
    "subway_enter_station_packaged_with_constraints",
    "stadium_concert_packaged_observation_only",
    "plaza_market_packaged_observation_only",
    "gps_slam_conflict_packaged_as_blocked_record",
    "home_return_packaged_for_trial_execution_planning",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    PHASE_ONE_CHAIN_REF,
    PLANNING_REF,
    OWNER_APPROVAL_REQUEST_REF,
    OWNER_APPROVAL_ISSUANCE_REF,
    PACKAGE_BOUNDARY_REF,
    PRE_RUNTIME_TRIAL_PACKAGE_REF,
    "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001",
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001",
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
)

ISSUANCE_PACKAGE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "issuance_package_is_not_runtime_activation",
    "issuance_package_only_authorizes_next_stage_trial_execution_planning",
    "scenario_scope_must_remain_unchanged_from_closure_readiness",
    "blocked_scenario_must_remain_blocked",
    "observation_only_scenarios_must_remain_observation_only",
    "constrained_scenario_must_remain_constrained",
    "low_risk_trial_candidates_still_do_not_start_runtime",
    "every_packaged_scenario_must_bind_rollback_policy_ref",
    "every_packaged_scenario_must_bind_observation_log_policy_ref",
    "every_packaged_scenario_must_bind_failure_handling_policy_ref",
    "allowed_next_step_must_be_planning_only",
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
    "trial_execution_planning_only",
    "constrained_trial_execution_planning_only",
    "observation_trial_execution_planning_only",
    "conflict_resolution_planning_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "issuance_package_only": True,
    "issuance_package_not_runtime_activation": True,
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
class ControlledRuntimeTrialIssuancePackageProfile:
    profile_ref: str
    phase_id: str
    pre_runtime_trial_package_ref: str
    pre_runtime_trial_package_status: str
    phase_one_chain_ref: str
    phase_one_chain_status: str
    runtime_trial_mode: str
    issuance_package_item_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only_source_chain_required: bool = True


@dataclass(frozen=True)
class ControlledRuntimeTrialIssuancePackageItem:
    package_ref: str
    closure_scenario_ref: str
    source_readiness: str
    package_scope: str
    issuance_package_status: str
    allowed_next_step: str
    package_boundaries: Tuple[str, ...]
    package_constraints: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    rollback_policy_ref: str
    observation_log_policy_ref: str
    failure_handling_policy_ref: str
    upstream_refs: Tuple[str, ...]
    source_chain: str
    package_active: bool = True


@dataclass(frozen=True)
class IssuedTrialPackageScope:
    scope_ref: str
    package_scope: str
    source_readiness: str
    issuance_package_status: str
    runtime_activation_allowed: bool
    source_chain: str


@dataclass(frozen=True)
class IssuedTrialPackageBoundary:
    boundary_ref: str
    package_boundaries: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class IssuedTrialPackageControlBinding:
    binding_ref: str
    rollback_policy_ref: str
    observation_log_policy_ref: str
    failure_handling_policy_ref: str
    rollback_policy_bound: bool
    observation_log_policy_bound: bool
    failure_handling_policy_bound: bool
    source_chain: str


@dataclass(frozen=True)
class IssuedTrialPackageBlockerRecord:
    record_ref: str
    blocked_scenario_remains_blocked: bool
    observation_only_not_upgraded: bool
    constrained_item_constraints_preserved: bool
    live_sensor_trigger_blocked_for_all: bool
    source_chain: str


@dataclass(frozen=True)
class IssuedTrialPackageAuditRecord:
    audit_ref: str
    pre_runtime_trial_package_go_verified: bool
    pre_runtime_trial_package_status_sealed: bool
    sealed_phase_one_chain_verified: bool
    allowed_next_step_planning_only: bool
    issuance_package_not_runtime_activation: bool
    source_chain: str


@dataclass(frozen=True)
class ControlledRuntimeTrialIssuancePackageDecision:
    decision_ref: str
    profile_ref: str
    issuance_package_profile_count: int
    issuance_package_item_count: int
    pre_runtime_trial_package_go_verified: bool
    pre_runtime_trial_package_status_sealed: bool
    sealed_phase_one_chain_verified: bool
    scenario_scope_preserved_for_all: bool
    final_decision: str
    runtime_activation_allowed: bool = False
    trial_runtime_started: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
