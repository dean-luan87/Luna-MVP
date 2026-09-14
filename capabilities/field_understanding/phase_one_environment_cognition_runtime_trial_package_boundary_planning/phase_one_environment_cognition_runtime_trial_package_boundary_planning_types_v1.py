# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Package Boundary Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Package-Boundary-Planning-v1-001"
)
SCOPE = "phase_one_environment_cognition_runtime_trial_package_boundary_planning_review_only"
SOURCE_CHAIN = "phase_one_environment_cognition_runtime_trial_package_boundary_planning_v1"

PACKAGE_PRINCIPLE_ZH = (
    "基于已封口的 Owner Approval Issuance 封装 controlled runtime trial package；"
    "明确边界、允许/禁止行为、回滚、日志与失败处理，不启动真实 runtime。"
)

PLANNING_REF = "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Planning-v1-001"
OWNER_APPROVAL_REQUEST_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Owner-Approval-Request-v1-001"
)
OWNER_APPROVAL_ISSUANCE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Owner-Approval-Issuance-v1-001"
)
PHASE_ONE_CHAIN_REF = "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
PHASE_ONE_CHAIN_STATUS = "sealed"
RUNTIME_TRIAL_MODE = "trial_package_boundary_planning_only"
CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED = True

FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
TASK_MANAGER_ENTRYPOINT = "task_manager_v1"
GUIDANCE_ENTRYPOINT = "navigation_guidance_candidate_v1"
SPEECH_GATE_ENTRYPOINT = "speech_gate_v1"
ACTION_SAFETY_ENTRYPOINT = "action_safety_candidate_v1"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"

FINAL_DECISION_GO = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_BOUNDARY_PLANNING_GO"
)
FINAL_DECISION_BLOCKED = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PACKAGE_BOUNDARY_PLANNING_BLOCKED"
)

NEXT_PHASE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Package-Closure-Readiness-Review-v1-001"
)

PACKAGE_SCOPES: Tuple[str, ...] = (
    "low_risk_controlled_trial_candidate",
    "cautious_candidate_trial",
    "observation_only",
    "blocked",
)

ISSUED_STATUSES: Tuple[str, ...] = (
    "issued_for_next_stage_planning",
    "issued_with_constraints_for_next_stage_planning",
    "issued_observation_only",
    "not_issued_blocked",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "ControlledRuntimeTrialPackageProfile",
    "ControlledRuntimeTrialPackageItem",
    "TrialPackageBoundaryPolicy",
    "TrialPackageAllowedOperation",
    "TrialPackageBlockedOperation",
    "TrialPackageRollbackBinding",
    "TrialPackageObservationLogBinding",
    "TrialPackageFailureHandlingBinding",
    "TrialPackageBoundaryPlanningDecision",
)

PACKAGE_ITEM_REFS: Tuple[str, ...] = (
    "mall_find_entrance_package",
    "subway_enter_station_package",
    "stadium_concert_ticket_gate_package",
    "plaza_market_crowd_package",
    "gps_slam_conflict_package",
    "home_return_package",
)

ISSUANCE_ITEM_REF_MAP: Dict[str, str] = {
    "mall_find_entrance_package": "mall_find_entrance",
    "subway_enter_station_package": "subway_enter_station",
    "stadium_concert_ticket_gate_package": "stadium_concert_ticket_gate",
    "plaza_market_crowd_package": "plaza_market_crowd",
    "gps_slam_conflict_package": "gps_slam_conflict",
    "home_return_package": "home_return",
}

PACKAGE_ITEM_GO_KEYS: Tuple[str, ...] = (
    "mall_find_entrance_package_ready",
    "subway_enter_station_package_constraints_ready",
    "stadium_concert_observation_package_ready",
    "plaza_market_observation_package_ready",
    "gps_slam_conflict_package_blocked",
    "home_return_package_ready",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    PHASE_ONE_CHAIN_REF,
    PLANNING_REF,
    OWNER_APPROVAL_REQUEST_REF,
    OWNER_APPROVAL_ISSUANCE_REF,
    "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001",
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001",
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
)

PACKAGE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "trial_package_planning_is_not_runtime_activation",
    "package_scope_must_preserve_issued_scope",
    "blocked_scenarios_must_remain_blocked",
    "observation_only_scenarios_must_not_upgrade_to_movement_guidance",
    "constrained_scenarios_must_preserve_constraints",
    "every_package_item_must_bind_rollback_policy_ref",
    "every_package_item_must_bind_observation_log_policy_ref",
    "every_package_item_must_bind_failure_handling_policy_ref",
    "every_package_item_must_preserve_source_chain_and_upstream_refs",
    "allowed_operations_must_be_candidate_only",
    "blocked_operations_must_include_direct_action_speech_fact_write_real_navigation",
    "gps_slam_conflict_package_must_block_route_activation_and_action_like_guidance",
    "crowd_high_risk_package_must_block_movement_guidance_trial",
    "no_live_sensor_no_real_gps_no_real_map_api_no_runtime_activation",
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
    "trial_package_boundary_planning_only": True,
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
class ControlledRuntimeTrialPackageProfile:
    profile_ref: str
    phase_id: str
    owner_approval_issuance_ref: str
    planning_ref: str
    owner_approval_request_ref: str
    phase_one_chain_ref: str
    phase_one_chain_status: str
    runtime_trial_mode: str
    field_synthesis_entrypoint: str
    task_manager_entrypoint: str
    guidance_entrypoint: str
    speech_gate_entrypoint: str
    action_safety_entrypoint: str
    interface_layer_protocol_ref: str
    package_item_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only_source_chain_required: bool = True


@dataclass(frozen=True)
class ControlledRuntimeTrialPackageItem:
    package_ref: str
    issuance_item_ref: str
    issued_status: str
    package_scope: str
    allowed_operations: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    package_constraints: Tuple[str, ...]
    rollback_policy_ref: str
    observation_log_policy_ref: str
    failure_handling_policy_ref: str
    upstream_refs: Tuple[str, ...]
    source_chain: str
    package_ready: bool = True


@dataclass(frozen=True)
class TrialPackageBoundaryPolicy:
    policy_ref: str
    package_scope: str
    issued_status: str
    candidate_only_allowed: bool
    movement_guidance_allowed: bool
    runtime_activation_allowed: bool
    source_chain: str


@dataclass(frozen=True)
class TrialPackageAllowedOperation:
    operation_ref: str
    operation_kind: str
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class TrialPackageBlockedOperation:
    operation_ref: str
    operation_kind: str
    universally_blocked: bool
    source_chain: str


@dataclass(frozen=True)
class TrialPackageRollbackBinding:
    binding_ref: str
    rollback_policy_ref: str
    rollback_policy_bound: bool
    candidate_only_rollback: bool
    source_chain: str


@dataclass(frozen=True)
class TrialPackageObservationLogBinding:
    binding_ref: str
    observation_log_policy_ref: str
    observation_log_policy_bound: bool
    log_package_boundary: bool
    source_chain: str


@dataclass(frozen=True)
class TrialPackageFailureHandlingBinding:
    binding_ref: str
    failure_handling_policy_ref: str
    failure_handling_policy_bound: bool
    downgrade_on_high_risk: bool
    block_on_unresolved_conflict: bool
    source_chain: str


@dataclass(frozen=True)
class TrialPackageBoundaryPlanningDecision:
    decision_ref: str
    profile_ref: str
    trial_package_profile_count: int
    trial_package_item_count: int
    owner_approval_issuance_go_verified: bool
    owner_approval_request_go_verified: bool
    planning_go_verified: bool
    sealed_phase_one_chain_verified: bool
    package_scope_preserved_for_all: bool
    issued_status_preserved_for_all: bool
    final_decision: str
    runtime_activation_allowed: bool = False
    trial_runtime_started: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
