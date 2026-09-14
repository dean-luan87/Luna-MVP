# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Owner Approval Request — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Owner-Approval-Request-v1-001"
)
SCOPE = "phase_one_environment_cognition_runtime_trial_owner_approval_request_review_only"
SOURCE_CHAIN = "phase_one_environment_cognition_runtime_trial_owner_approval_request_v1"

REQUEST_PRINCIPLE_ZH = (
    "将已 GO 的 controlled runtime trial planning 转为正式 Owner Approval Request；"
    "本阶段仅 request planning + matrix review，不签发 runtime trial，不启动真实 runtime。"
)

PLANNING_REF = "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Planning-v1-001"
PHASE_ONE_CHAIN_REF = "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
PHASE_ONE_CHAIN_STATUS = "sealed"
RUNTIME_TRIAL_MODE = "owner_approval_request_only"
CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED = True

FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
TASK_MANAGER_ENTRYPOINT = "task_manager_v1"
GUIDANCE_ENTRYPOINT = "navigation_guidance_candidate_v1"
SPEECH_GATE_ENTRYPOINT = "speech_gate_v1"
ACTION_SAFETY_ENTRYPOINT = "action_safety_candidate_v1"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"

FINAL_DECISION_GO = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_REQUEST_GO"
)
FINAL_DECISION_BLOCKED = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_OWNER_APPROVAL_REQUEST_BLOCKED"
)

NEXT_PHASE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Owner-Approval-Issuance-v1-001"
)

APPROVAL_REQUEST_STATUSES: Tuple[str, ...] = (
    "requestable",
    "requestable_with_constraints",
    "observation_only_requestable",
    "not_requestable",
)

REQUEST_SCOPES: Tuple[str, ...] = (
    "controlled_trial_candidate",
    "cautious_trial_candidate",
    "observation_only",
    "blocked",
)

RUNTIME_ADMISSION_LEVELS: Tuple[str, ...] = (
    "blocked",
    "observation_only",
    "cautious_candidate_trial",
    "low_risk_controlled_trial_candidate",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "RuntimeTrialOwnerApprovalRequestProfile",
    "RuntimeTrialOwnerApprovalRequestItem",
    "RuntimeTrialApprovalScopeCandidate",
    "RuntimeTrialApprovalRiskSummary",
    "RuntimeTrialApprovalRollbackBinding",
    "RuntimeTrialApprovalObservationLogBinding",
    "RuntimeTrialApprovalBlockerPolicy",
    "RuntimeTrialOwnerApprovalRequestDecision",
)

REQUEST_ITEM_REFS: Tuple[str, ...] = (
    "mall_find_entrance_low_risk_trial_candidate",
    "subway_enter_station_cautious_trial_candidate",
    "stadium_concert_ticket_gate_observation_trial_candidate",
    "plaza_market_crowd_blocked_or_observation_only",
    "gps_slam_conflict_runtime_blocker",
    "home_return_low_risk_trial_candidate",
)

REQUEST_ITEM_GO_KEYS: Tuple[str, ...] = (
    "mall_find_entrance_requestable",
    "subway_enter_station_requestable_with_constraints",
    "stadium_concert_observation_only_requestable",
    "plaza_market_observation_only_requestable",
    "gps_slam_conflict_not_requestable",
    "home_return_requestable",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    PHASE_ONE_CHAIN_REF,
    PLANNING_REF,
    "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001",
    "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001",
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001",
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
)

REQUEST_GOVERNANCE_RULES: Tuple[str, ...] = (
    "owner_approval_request_is_not_owner_approval_issuance",
    "owner_approval_request_does_not_activate_runtime",
    "owner_approval_request_must_preserve_admission_level_from_planning",
    "blocked_scenarios_must_not_become_requestable",
    "observation_only_scenarios_must_not_become_movement_guidance_trials",
    "low_risk_trial_candidates_still_require_owner_approval_before_issuance",
    "every_requestable_item_must_bind_rollback_policy_ref",
    "every_requestable_item_must_bind_observation_log_policy_ref",
    "every_requestable_item_must_preserve_source_chain_and_upstream_refs",
    "gps_slam_conflict_must_remain_blocked",
    "crowd_high_risk_must_remain_observation_only_or_blocked",
    "speech_gate_candidate_remains_candidate_not_tts",
    "action_safety_candidate_remains_candidate_not_action",
    "no_fact_write_no_real_navigation_no_live_sensor",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "owner_approval_request_only": True,
    "owner_approval_required": True,
    "owner_approval_issued": False,
    "trial_issuance_allowed": False,
    "runtime_activation_allowed": False,
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
class RuntimeTrialOwnerApprovalRequestProfile:
    profile_ref: str
    phase_id: str
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
    request_item_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    owner_approval_required: bool = True
    owner_approval_issued: bool = False
    trial_issuance_allowed: bool = False
    candidate_only_source_chain_required: bool = True


@dataclass(frozen=True)
class RuntimeTrialOwnerApprovalRequestItem:
    item_ref: str
    planning_policy_ref: str
    admission_level: str
    approval_request_status: str
    request_scope: str
    required_controls: Tuple[str, ...]
    rollback_policy_ref: str
    observation_log_policy_ref: str
    upstream_refs: Tuple[str, ...]
    source_chain: str
    request_active: bool = True


@dataclass(frozen=True)
class RuntimeTrialApprovalScopeCandidate:
    scope_ref: str
    request_scope: str
    admission_levels: Tuple[str, ...]
    approval_request_statuses: Tuple[str, ...]
    movement_guidance_allowed: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialApprovalRiskSummary:
    summary_ref: str
    gps_slam_conflict_blocks_runtime_trial: bool
    crowd_high_risk_blocks_movement_guidance_trial: bool
    event_overlay_does_not_rewrite_map_place: bool
    field_interaction_label_not_fact: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_not_action: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialApprovalRollbackBinding:
    binding_ref: str
    rollback_policy_ref: str
    rollback_policy_required: bool
    fallback_observe_wait: bool
    candidate_only_rollback: bool
    no_fact_write_on_rollback: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialApprovalObservationLogBinding:
    binding_ref: str
    observation_log_policy_ref: str
    observation_log_policy_required: bool
    log_upstream_source_refs: bool
    log_admission_level: bool
    log_approval_request_status: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialApprovalBlockerPolicy:
    policy_ref: str
    blocked_scenario_not_requestable: bool
    observation_only_not_movement_trial: bool
    conflict_blocks_route_hint_activation: bool
    crowd_density_blocks_movement_guidance: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialOwnerApprovalRequestDecision:
    decision_ref: str
    profile_ref: str
    approval_request_profile_count: int
    approval_request_item_count: int
    planning_go_verified: bool
    sealed_phase_one_chain_verified: bool
    admission_level_preserved_for_all: bool
    requestable_item_count: int
    requestable_with_constraints_item_count: int
    observation_only_requestable_item_count: int
    not_requestable_item_count: int
    final_decision: str
    owner_approval_issued: bool = False
    trial_issuance_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
