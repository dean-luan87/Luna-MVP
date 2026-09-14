# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Package Closure Readiness Review — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Package-Closure-Readiness-Review-v1-001"
)
SCOPE = "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_only"
SOURCE_CHAIN = "phase_one_environment_cognition_runtime_trial_package_closure_readiness_review_v1"

CLOSURE_PRINCIPLE_ZH = (
    "将 Planning → Request → Issuance → Package Boundary 四段合并封存为 "
    "runtime trial 前置包；本阶段仅 closure / readiness review，不启动真实 runtime。"
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
RUNTIME_TRIAL_MODE = "pre_runtime_trial_package_closure_only"
CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED = True

FINAL_DECISION_GO = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_CLOSURE_READINESS_REVIEW_GO"
)
FINAL_DECISION_BLOCKED = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_CLOSURE_READINESS_REVIEW_BLOCKED"
)

PRE_RUNTIME_TRIAL_CHAIN_REFS: Tuple[str, ...] = (
    PLANNING_REF,
    OWNER_APPROVAL_REQUEST_REF,
    OWNER_APPROVAL_ISSUANCE_REF,
    PACKAGE_BOUNDARY_REF,
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "RuntimeTrialPackageClosureReadinessProfile",
    "RuntimeTrialPackageClosureStageRef",
    "RuntimeTrialPackageScenarioReadiness",
    "RuntimeTrialPackageGovernanceReadiness",
    "RuntimeTrialPackageBoundaryReadiness",
    "RuntimeTrialPackageClosureReadinessDecision",
)

CLOSURE_STAGE_REFS: Tuple[str, ...] = (
    "planning_stage_closed",
    "owner_approval_request_stage_closed",
    "owner_approval_issuance_stage_closed",
    "package_boundary_stage_closed",
)

SCENARIO_READINESS_REFS: Tuple[str, ...] = (
    "mall_find_entrance_package",
    "subway_enter_station_package",
    "stadium_concert_ticket_gate_package",
    "plaza_market_crowd_package",
    "gps_slam_conflict_package",
    "home_return_package",
)

SCENARIO_READINESS_GO_KEYS: Tuple[str, ...] = (
    "mall_find_entrance_ready_for_pre_runtime_trial_review",
    "subway_enter_station_ready_with_constraints",
    "stadium_concert_observation_only_ready",
    "plaza_market_observation_only_ready",
    "gps_slam_conflict_blocked_preserved",
    "home_return_ready_for_pre_runtime_trial_review",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    PHASE_ONE_CHAIN_REF,
    *PRE_RUNTIME_TRIAL_CHAIN_REFS,
    "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001",
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001",
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
)

CLOSURE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "package_closure_readiness_is_not_runtime_activation",
    "readiness_review_must_verify_planning_request_issuance_package_boundary_chain",
    "scenario_scope_must_remain_unchanged_from_issuance_package_boundary",
    "blocked_scenario_must_remain_blocked",
    "observation_only_scenarios_must_remain_observation_only",
    "constrained_scenario_must_remain_constrained",
    "low_risk_trial_candidates_still_do_not_start_runtime",
    "every_ready_scenario_must_bind_rollback_observation_failure_policies",
    "allowed_operations_must_remain_candidate_only",
    "blocked_operations_must_include_direct_action_speech_fact_write_real_navigation_live_sensor",
    "runtime_activation_not_allowed_in_this_phase",
    "commercial_runtime_approval_not_implied",
    "all_source_chain_and_upstream_refs_must_be_preserved",
)

UNIVERSAL_BLOCKED_OPERATIONS: Tuple[str, ...] = (
    "direct_action",
    "direct_speech_tts",
    "direct_fact_write",
    "real_navigation",
    "live_sensor_trigger",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "pre_runtime_trial_package_closure_only": True,
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
}


@dataclass(frozen=True)
class RuntimeTrialPackageClosureReadinessProfile:
    profile_ref: str
    phase_id: str
    pre_runtime_trial_chain_refs: Tuple[str, ...]
    phase_one_chain_ref: str
    phase_one_chain_status: str
    runtime_trial_mode: str
    closure_stage_refs: Tuple[str, ...]
    scenario_readiness_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only_source_chain_required: bool = True


@dataclass(frozen=True)
class RuntimeTrialPackageClosureStageRef:
    stage_ref: str
    phase_ref: str
    stage_zh: str
    required_checks: Tuple[str, ...]
    stage_closed: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialPackageScenarioReadiness:
    scenario_ref: str
    package_ref: str
    readiness_status: str
    package_scope: str
    readiness_constraints: Tuple[str, ...]
    rollback_policy_ref: str
    observation_log_policy_ref: str
    failure_handling_policy_ref: str
    upstream_refs: Tuple[str, ...]
    source_chain: str
    readiness_ok: bool = True


@dataclass(frozen=True)
class RuntimeTrialPackageGovernanceReadiness:
    readiness_ref: str
    scenario_scope_preserved_for_all: bool
    blocked_scenario_remains_blocked: bool
    observation_only_not_upgraded: bool
    constrained_item_constraints_preserved: bool
    low_risk_candidates_do_not_start_runtime: bool
    allowed_operations_candidate_only: bool
    source_chain_required: bool
    upstream_refs_required: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialPackageBoundaryReadiness:
    readiness_ref: str
    blocked_operations_declared_for_all: bool
    direct_action_blocked_for_all: bool
    direct_speech_blocked_for_all: bool
    direct_fact_write_blocked_for_all: bool
    real_navigation_blocked_for_all: bool
    live_sensor_trigger_blocked_for_all: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialPackageClosureReadinessDecision:
    decision_ref: str
    profile_ref: str
    closure_readiness_profile_count: int
    closure_stage_count: int
    scenario_readiness_count: int
    planning_go_verified: bool
    owner_approval_request_go_verified: bool
    owner_approval_issuance_go_verified: bool
    package_boundary_go_verified: bool
    sealed_phase_one_chain_verified: bool
    final_decision: str
    runtime_activation_allowed: bool = False
    trial_runtime_started: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
