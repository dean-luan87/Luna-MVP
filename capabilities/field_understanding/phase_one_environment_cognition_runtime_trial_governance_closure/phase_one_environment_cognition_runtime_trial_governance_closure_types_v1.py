# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Runtime Trial Governance Closure — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
SCOPE = "phase_one_environment_cognition_runtime_trial_governance_closure_review_only"
SOURCE_CHAIN = "phase_one_environment_cognition_runtime_trial_governance_closure_v1"

GOVERNANCE_CLOSURE_PRINCIPLE_ZH = (
    "对 Luna 一期第一视角环境认知 controlled runtime trial governance 链路做压缩 closure，"
    "封存 Planning → Request → Issuance → Package Boundary → Closure Readiness → "
    "Issuance Package → Execution Planning 连续治理拆分；execution planning 为 planning-only 链终端。"
)

PHASE_ONE_CHAIN_REF = "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
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
PRE_RUNTIME_TRIAL_PACKAGE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Package-Closure-Readiness-Review-v1-001"
)
ISSUANCE_PACKAGE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Issuance-Package-v1-001"
)
EXECUTION_PLANNING_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Execution-Planning-v1-001"
)

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
PHASE_ONE_CHAIN_STATUS = "sealed"
PRE_RUNTIME_TRIAL_PACKAGE_STATUS = "sealed"
RUNTIME_TRIAL_MODE = "governance_closure_only"
CANDIDATE_ONLY_SOURCE_CHAIN_REQUIRED = True

FINAL_DECISION_GO = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_GO"
)
FINAL_DECISION_BLOCKED = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_CONTROLLED_RUNTIME_TRIAL_GOVERNANCE_CLOSURE_BLOCKED"
)

NEXT_PHASE_REF = "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-Planning-v1-001"

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "PhaseOneRuntimeTrialGovernanceClosure",
    "PhaseOneRuntimeTrialGovernanceStageRef",
    "PhaseOneRuntimeTrialGovernanceCoverage",
    "PhaseOneRuntimeTrialGovernanceReuseBinding",
    "PhaseOneRuntimeTrialGovernanceClosureDecision",
)

GOVERNANCE_STAGE_REFS: Tuple[str, ...] = (
    "phase_one_chain_closure",
    "controlled_runtime_trial_planning",
    "owner_approval_request",
    "owner_approval_issuance",
    "package_boundary_planning",
    "package_closure_readiness",
    "issuance_package",
    "execution_planning",
)

SCENARIO_COVERAGE_REFS: Tuple[str, ...] = (
    "mall_find_entrance",
    "subway_enter_station",
    "stadium_concert_ticket_gate",
    "plaza_market_crowd",
    "gps_slam_conflict",
    "home_return",
)

SCENARIO_COVERAGE_GO_KEYS: Tuple[str, ...] = (
    "mall_find_entrance_scope_preserved",
    "subway_enter_station_scope_preserved",
    "stadium_concert_observation_only_preserved",
    "plaza_market_observation_only_preserved",
    "gps_slam_conflict_blocked_preserved",
    "home_return_scope_preserved",
)

GOVERNANCE_STAGE_GO_KEYS: Tuple[str, ...] = (
    "phase_one_chain_closure_go_verified",
    "controlled_runtime_trial_planning_go_verified",
    "owner_approval_request_go_verified",
    "owner_approval_issuance_go_verified",
    "package_boundary_planning_go_verified",
    "package_closure_readiness_go_verified",
    "issuance_package_go_verified",
    "execution_planning_go_verified",
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

GOVERNANCE_CLOSURE_RULES: Tuple[str, ...] = (
    "governance_closure_is_not_runtime_activation",
    "execution_planning_is_terminal_planning_stage_for_this_governance_chain",
    "no_further_gate_package_issuance_split_for_same_planning_only_chain",
    "future_model_capability_runtime_trial_governance_must_reuse_template_by_default",
    "scenario_scope_must_remain_unchanged",
    "blocked_scenario_must_remain_blocked",
    "observation_only_scenarios_must_remain_observation_only",
    "constrained_scenario_must_remain_constrained",
    "low_risk_trial_candidates_remain_candidate_replay_only",
    "allowed_operations_remain_candidate_only",
    "runtime_activation_direct_action_speech_fact_write_real_navigation_live_sensor_remain_blocked",
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

_CANDIDATE_ONLY_ALLOWED_MARKERS: Tuple[str, ...] = (
    "candidate_",
    "_replay",
    "_check",
    "conflict_record_",
    "conflict_resolution_planning_",
    "ocr_sign_evidence_request_placeholder",
    "event_overlay_validation_replay",
    "crowd_flow_risk_observation_replay",
    "crowd_queue_risk_observation_replay",
    "temporary_layout_uncertainty_logging_replay",
    "wait_observe_candidate_replay",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "governance_closure_only": True,
    "runtime_activation_deferred": True,
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
class PhaseOneRuntimeTrialGovernanceClosure:
    closure_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    pre_runtime_trial_package_status: str
    phase_one_chain_status: str
    runtime_trial_mode: str
    governance_stage_refs: Tuple[str, ...]
    scenario_coverage_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only_source_chain_required: bool = True


@dataclass(frozen=True)
class PhaseOneRuntimeTrialGovernanceStageRef:
    stage_ref: str
    phase_ref: str
    template_stage_id: str
    expected_final_decision: str
    expected_status: str
    source_chain: str
    stage_verified: bool = True


@dataclass(frozen=True)
class PhaseOneRuntimeTrialGovernanceCoverage:
    scenario_ref: str
    expected_scope: str
    expected_execution_plan_status: str
    scope_preserved: bool
    source_chain: str


@dataclass(frozen=True)
class PhaseOneRuntimeTrialGovernanceReuseBinding:
    binding_ref: str
    governance_template_ref: str
    reuse_profile_id: str
    target_domain: str
    future_governance_reuse_template_required: bool
    execution_planning_marked_terminal_for_planning_only_chain: bool
    no_further_gate_package_issuance_split_required: bool
    template_supports_compressed_mode: bool
    source_chain: str


@dataclass(frozen=True)
class PhaseOneRuntimeTrialGovernanceClosureDecision:
    decision_ref: str
    closure_ref: str
    governance_closure_profile_count: int
    controlled_trial_governance_template_created: bool
    controlled_trial_governance_template_stage_count: int
    governance_stage_ref_count: int
    all_governance_stage_refs_verified: bool
    pre_runtime_package_sealed: bool
    scenario_scope_preserved_for_all: bool
    final_decision: str
    runtime_activation_allowed: bool = False
    trial_runtime_started: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
