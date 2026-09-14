# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Controlled Runtime Trial Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Planning-v1-001"
SCOPE = "phase_one_environment_cognition_runtime_trial_planning_review_only"
SOURCE_CHAIN = "phase_one_environment_cognition_runtime_trial_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "为已封存的 Luna 一期第一视角环境认知主链制定 controlled runtime trial planning；"
    "本阶段仅定义准入条件与治理边界，不启动真实 runtime。"
)

PHASE_ONE_CHAIN_REF = "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
RUNTIME_TRIAL_MODE = "controlled_planning_only"
CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED = True

FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
TASK_MANAGER_ENTRYPOINT = "task_manager_v1"
GUIDANCE_ENTRYPOINT = "navigation_guidance_candidate_v1"
SPEECH_GATE_ENTRYPOINT = "speech_gate_v1"
ACTION_SAFETY_ENTRYPOINT = "action_safety_candidate_v1"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"

FINAL_DECISION_GO = "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PLANNING_GO"
FINAL_DECISION_BLOCKED = "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_PLANNING_BLOCKED"

NEXT_PHASE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Owner-Approval-Request-v1-001"
)

RUNTIME_ADMISSION_LEVELS: Tuple[str, ...] = (
    "blocked",
    "observation_only",
    "cautious_candidate_trial",
    "low_risk_controlled_trial_candidate",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "ControlledRuntimeTrialPlanningProfile",
    "RuntimeTrialScenarioPolicy",
    "RuntimeTrialEvidenceRequirement",
    "RuntimeTrialSafetyGateRequirement",
    "RuntimeTrialOwnerApprovalRequirement",
    "RuntimeTrialRollbackRequirement",
    "RuntimeTrialObservationLogRequirement",
    "RuntimeTrialFailureHandlingPolicy",
    "RuntimeTrialAdmissionDecision",
)

SCENARIO_POLICY_REFS: Tuple[str, ...] = (
    "mall_find_entrance_low_risk_trial_candidate",
    "subway_enter_station_cautious_trial_candidate",
    "stadium_concert_ticket_gate_observation_trial_candidate",
    "plaza_market_crowd_blocked_or_observation_only",
    "gps_slam_conflict_runtime_blocker",
    "home_return_low_risk_trial_candidate",
)

SCENARIO_POLICY_GO_KEYS: Tuple[str, ...] = (
    "mall_find_entrance_low_risk_trial_candidate",
    "subway_enter_station_cautious_trial_candidate",
    "stadium_concert_observation_trial_candidate",
    "plaza_market_crowd_observation_only",
    "gps_slam_conflict_runtime_blocker",
    "home_return_low_risk_trial_candidate",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    PHASE_ONE_CHAIN_REF,
    "Phase-Task-To-Guidance-Safety-Gate-DryRun-v1-001",
    "Phase-Field-To-Task-Alignment-DryRun-v1-001",
    "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001",
    "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001",
    "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001",
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
    "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001",
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001",
)

PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "upstream_chain_must_be_sealed_before_runtime_trial_planning",
    "controlled_runtime_trial_planning_is_not_runtime_activation",
    "every_trial_candidate_must_declare_admission_level",
    "every_trial_candidate_must_preserve_source_chain_and_upstream_refs",
    "every_trial_candidate_must_define_rollback_policy",
    "every_trial_candidate_must_define_observation_log_policy",
    "owner_approval_required_before_future_runtime_trial_issuance",
    "action_safety_required_before_action_like_guidance",
    "speech_gate_required_before_future_speech_output",
    "conflict_candidate_blocks_action_like_guidance",
    "high_risk_crowd_traffic_indoor_uncertainty_downgrades_or_blocks",
    "no_fact_write_in_trial_planning",
    "no_commercial_runtime_approval_implied",
)

PROHIBITED_ITEMS: Tuple[str, ...] = (
    "no_real_navigation_runtime_start",
    "no_real_action",
    "no_real_speech_tts",
    "no_fact_write",
    "no_action_like_guidance_under_gps_slam_conflict",
    "no_movement_guidance_under_crowd_high_risk",
    "event_overlay_must_not_rewrite_map_place_ref",
    "field_interaction_label_must_not_be_fact",
    "no_bypass_action_safety_candidate",
    "no_bypass_owner_approval",
    "no_trial_without_rollback_plan",
    "no_trial_without_observation_log",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "controlled_planning_only": True,
    "no_runtime_activation": True,
    "no_real_navigation": True,
    "no_real_map_api": True,
    "no_real_gps_gnss": True,
    "no_live_sensor": True,
    "no_live_camera": True,
    "no_live_imu": True,
    "runtime_activation_allowed": False,
    "real_navigation_started": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "live_sensor_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
    "owner_approval_runtime_not_issued": True,
}


@dataclass(frozen=True)
class ControlledRuntimeTrialPlanningProfile:
    profile_ref: str
    phase_id: str
    phase_one_chain_ref: str
    runtime_trial_mode: str
    field_synthesis_entrypoint: str
    task_manager_entrypoint: str
    guidance_entrypoint: str
    speech_gate_entrypoint: str
    action_safety_entrypoint: str
    interface_layer_protocol_ref: str
    scenario_policy_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    prohibited_items: Tuple[str, ...]
    candidate_only_source_chain_required: bool = True


@dataclass(frozen=True)
class RuntimeTrialScenarioPolicy:
    policy_ref: str
    source_scenario_ref: str
    admission_level: str
    trial_conditions: Tuple[str, ...]
    rollback_policy_ref: str
    observation_log_policy_ref: str
    upstream_refs: Tuple[str, ...]
    source_chain: str
    policy_active: bool = True


@dataclass(frozen=True)
class RuntimeTrialEvidenceRequirement:
    requirement_ref: str
    local_spatial_evidence_required: bool
    gps_degraded_acknowledgement_required: bool
    conflict_candidate_blocks_trial: bool
    ocr_sign_evidence_optional_placeholder: bool
    coarse_map_route_allowed: bool
    local_spatial_check_required: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialSafetyGateRequirement:
    requirement_ref: str
    action_safety_candidate_required: bool
    speech_gate_candidate_required: bool
    crowd_risk_downgrade_required: bool
    conflict_blocks_action_like_guidance: bool
    no_direct_action: bool
    no_movement_command: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialOwnerApprovalRequirement:
    requirement_ref: str
    owner_approval_required: bool
    owner_approval_runtime_not_issued: bool
    owner_approval_phase_placeholder: str
    record_approval_chain_placeholder: str
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialRollbackRequirement:
    requirement_ref: str
    rollback_policy_required: bool
    fallback_observe_wait: bool
    candidate_only_rollback: bool
    no_fact_write_on_rollback: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialObservationLogRequirement:
    requirement_ref: str
    observation_log_policy_required: bool
    log_upstream_source_refs: bool
    log_admission_level: bool
    log_safety_gate_decisions: bool
    log_rollback_events: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialFailureHandlingPolicy:
    policy_ref: str
    failure_handling_policy_required: bool
    downgrade_on_high_risk: bool
    block_on_unresolved_conflict: bool
    evidence_request_on_insufficient_data: bool
    no_silent_runtime_escalation: bool
    source_chain: str


@dataclass(frozen=True)
class RuntimeTrialAdmissionDecision:
    decision_ref: str
    profile_ref: str
    planning_profile_count: int
    scenario_policy_count: int
    sealed_phase_one_chain_verified: bool
    admission_level_declared_for_all: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
