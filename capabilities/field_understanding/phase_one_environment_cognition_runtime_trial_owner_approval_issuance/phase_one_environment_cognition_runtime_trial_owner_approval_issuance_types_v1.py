# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Owner Approval Issuance — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Owner-Approval-Issuance-v1-001"
)
SCOPE = "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_review_only"
SOURCE_CHAIN = "phase_one_environment_cognition_runtime_trial_owner_approval_issuance_v1"

ISSUANCE_PRINCIPLE_ZH = (
    "基于已封口的 Owner Approval Request 生成 Owner Approval Issuance 记录；"
    "固化授权状态供下一阶段 trial package planning，不启动真实 runtime。"
)

PLANNING_REF = "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Planning-v1-001"
OWNER_APPROVAL_REQUEST_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Owner-Approval-Request-v1-001"
)
PHASE_ONE_CHAIN_REF = "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
PHASE_ONE_CHAIN_STATUS = "sealed"
RUNTIME_TRIAL_MODE = "owner_approval_issuance_only"
CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED = True

FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
TASK_MANAGER_ENTRYPOINT = "task_manager_v1"
GUIDANCE_ENTRYPOINT = "navigation_guidance_candidate_v1"
SPEECH_GATE_ENTRYPOINT = "speech_gate_v1"
ACTION_SAFETY_ENTRYPOINT = "action_safety_candidate_v1"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"

FINAL_DECISION_GO = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_ISSUANCE_GO"
)
FINAL_DECISION_BLOCKED = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_ISSUANCE_BLOCKED"
)

NEXT_PHASE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Package-Boundary-Planning-v1-001"
)

ISSUED_STATUSES: Tuple[str, ...] = (
    "issued_for_next_stage_planning",
    "issued_with_constraints_for_next_stage_planning",
    "issued_observation_only",
    "not_issued_blocked",
)

ISSUED_SCOPES: Tuple[str, ...] = (
    "low_risk_controlled_trial_candidate",
    "cautious_candidate_trial",
    "observation_only",
    "blocked",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "RuntimeTrialOwnerApprovalIssuanceProfile",
    "RuntimeTrialOwnerApprovalIssuanceItem",
    "RuntimeTrialIssuedScope",
    "RuntimeTrialIssuedControlBinding",
    "RuntimeTrialIssuedBlockerRecord",
    "RuntimeTrialIssuanceAuditRecord",
    "RuntimeTrialOwnerApprovalIssuanceDecision",
)

ISSUANCE_ITEM_REFS: Tuple[str, ...] = (
    "mall_find_entrance",
    "subway_enter_station",
    "stadium_concert_ticket_gate",
    "plaza_market_crowd",
    "gps_slam_conflict",
    "home_return",
)

REQUEST_ITEM_REF_MAP: Dict[str, str] = {
    "mall_find_entrance": "mall_find_entrance_low_risk_trial_candidate",
    "subway_enter_station": "subway_enter_station_cautious_trial_candidate",
    "stadium_concert_ticket_gate": "stadium_concert_ticket_gate_observation_trial_candidate",
    "plaza_market_crowd": "plaza_market_crowd_blocked_or_observation_only",
    "gps_slam_conflict": "gps_slam_conflict_runtime_blocker",
    "home_return": "home_return_low_risk_trial_candidate",
}

ISSUANCE_ITEM_GO_KEYS: Tuple[str, ...] = (
    "mall_find_entrance_issued_for_next_stage_planning",
    "subway_enter_station_issued_with_constraints",
    "stadium_concert_issued_observation_only",
    "plaza_market_issued_observation_only",
    "gps_slam_conflict_not_issued_blocked",
    "home_return_issued_for_next_stage_planning",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    PHASE_ONE_CHAIN_REF,
    PLANNING_REF,
    OWNER_APPROVAL_REQUEST_REF,
    "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001",
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001",
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
)

ISSUANCE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "owner_approval_issuance_is_not_runtime_activation",
    "issuance_must_preserve_request_scope_and_admission_level",
    "blocked_request_items_must_remain_not_issued",
    "observation_only_items_must_remain_observation_only",
    "constrained_items_must_remain_constrained",
    "issued_items_only_allow_next_stage_planning_not_runtime_start",
    "every_issued_item_must_bind_rollback_policy_ref",
    "every_issued_item_must_bind_observation_log_policy_ref",
    "every_issued_item_must_preserve_source_chain_and_upstream_refs",
    "gps_slam_conflict_must_remain_blocked",
    "crowd_high_risk_must_not_become_movement_guidance_trial",
    "speech_gate_candidate_remains_candidate_not_tts",
    "action_safety_candidate_remains_candidate_not_action",
    "no_fact_write_no_real_navigation_no_live_sensor_no_runtime_activation",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "owner_approval_issuance_only": True,
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
    "issuance_not_runtime_activation": True,
}


@dataclass(frozen=True)
class RuntimeTrialOwnerApprovalIssuanceProfile:
    profile_ref: str
    phase_id: str
    owner_approval_request_ref: str
    planning_ref: str
    phase_one_chain_ref: str
    phase_one_chain_status: str
    runtime_trial_mode: str
    field_synthesis_entrypoint: str
    task_manager_entrypoint: str
    guidance_entrypoint: str
    speech_gate_entrypoint: str
    action_safety_entrypoint: str
    interface_layer_protocol_ref: str
    issuance_item_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only_source_chain_required: bool = True


@dataclass(frozen=True)
class RuntimeTrialOwnerApprovalIssuanceItem:
    item_ref: str
    request_item_ref: str
    admission_level: str
    request_status: str
    request_scope: str
    issued_status: str
    issued_scope: str
    required_controls: Tuple[str, ...]
    rollback_policy_ref: str
    observation_log_policy_ref: str
    upstream_refs: Tuple[str, ...]
    source_chain: str
    issuance_active: bool = True


@dataclass(frozen=True)
class RuntimeTrialIssuedScope:
    scope_ref: str
    issued_scope: str
    admission_level: str
    request_scope: str
    movement_guidance_allowed: bool
    runtime_activation_allowed: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialIssuedControlBinding:
    binding_ref: str
    rollback_policy_ref: str
    observation_log_policy_ref: str
    rollback_policy_bound: bool
    observation_log_policy_bound: bool
    no_runtime_activation: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialIssuedBlockerRecord:
    record_ref: str
    blocked_scenario_not_issued: bool
    observation_only_not_upgraded: bool
    constrained_item_not_unconstrained: bool
    gps_slam_conflict_blocks_issuance: bool
    crowd_high_risk_blocks_movement_guidance_trial: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialIssuanceAuditRecord:
    audit_ref: str
    owner_approval_request_go_verified: bool
    planning_go_verified: bool
    sealed_phase_one_chain_verified: bool
    admission_level_preserved_for_all: bool
    request_scope_preserved_for_all: bool
    issuance_not_runtime_activation: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialOwnerApprovalIssuanceDecision:
    decision_ref: str
    profile_ref: str
    issuance_profile_count: int
    issuance_item_count: int
    owner_approval_request_go_verified: bool
    planning_go_verified: bool
    sealed_phase_one_chain_verified: bool
    admission_level_preserved_for_all: bool
    request_scope_preserved_for_all: bool
    issued_for_next_stage_planning_count: int
    issued_with_constraints_count: int
    issued_observation_only_count: int
    not_issued_blocked_count: int
    final_decision: str
    trial_runtime_started: bool = False
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
