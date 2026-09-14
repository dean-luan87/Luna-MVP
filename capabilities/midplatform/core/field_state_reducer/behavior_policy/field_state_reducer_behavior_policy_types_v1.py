from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Tuple


class BehaviorPolicyIdV1(str, Enum):
    LATEST_VALID_EVENT = "latest_valid_event"
    HIGHEST_CONFIDENCE_VALID_EVENT = "highest_confidence_valid_event"
    MULTI_EVENT_CONSENSUS = "multi_event_consensus"
    NEGATIVE_EVENT_OVERRIDE = "negative_event_override"
    REVOCATION_OVERRIDE = "revocation_override"
    EXPIRATION_DEGRADE = "expiration_degrade"
    TEMPORARY_OVERLAY_SEPARATION = "temporary_overlay_separation"
    CONFLICT_PRESERVATION = "conflict_preservation"
    INSUFFICIENT_EVIDENCE_UNRESOLVED = "insufficient_evidence_unresolved"
    EXPLICIT_OWNER_OVERRIDE_CANDIDATE = "explicit_owner_override_candidate"
    NO_STATE_CHANGE = "no_state_change"


class BehaviorPolicyOutcomeV1(str, Enum):
    SKELETON_POLICY_DECISION = "skeleton_policy_decision"
    NO_STATE_CHANGE = "no_state_change"


class BehaviorPolicyPrecedenceClassV1(str, Enum):
    OVERRIDE_TOP = "override_top"
    OVERRIDE_HIGH = "override_high"
    OVERLAY_HIGH = "overlay_high"
    SAFETY_TOP = "safety_top"
    SAFETY_HIGH = "safety_high"
    SELECTION_HIGH = "selection_high"
    SELECTION_MID = "selection_mid"
    SELECTION_LOW = "selection_low"
    GOVERNED_MID = "governed_mid"
    FALLBACK = "fallback"


class BehaviorPolicyEligibilityStatusV1(str, Enum):
    PLACEHOLDER_ELIGIBLE = "placeholder_eligible"
    PLACEHOLDER_REJECTED = "placeholder_rejected"


class BehaviorPolicyCompositionModeV1(str, Enum):
    SEQUENTIAL = "sequential"
    GUARDED = "guarded"
    FALLBACK = "fallback"
    PARALLEL = "parallel"


@dataclass(frozen=True)
class BehaviorPolicyRegistryEntryV1:
    policy_id: str
    policy_version: str
    eligible_state_types: Tuple[str, ...]
    precedence_class: str
    composable_with: Tuple[str, ...] = field(default_factory=tuple)
    mutually_exclusive_with: Tuple[str, ...] = field(default_factory=tuple)
    deterministic_required: bool = True
    implemented: bool = False
    runtime_callable: bool = False
    real_execution: bool = False
    fact_promotion_allowed: bool = False
    state_write_allowed: bool = False
    action_trigger_allowed: bool = False


@dataclass(frozen=True)
class BehaviorPolicyEligibilityInputV1:
    state_type: str
    admitted_field_events: Tuple[Dict[str, Any], ...]
    temporal_snapshot: Dict[str, Any]
    no_provider_recall: bool = True
    no_external_lookup: bool = True
    no_action_trigger: bool = True


@dataclass(frozen=True)
class BehaviorPolicyEligibilityResultV1:
    policy_id: str
    status: str
    reasons: Tuple[str, ...] = field(default_factory=tuple)
    eligibility_executed: bool = False
    placeholder_only: bool = True


@dataclass(frozen=True)
class BehaviorPolicySelectionInputV1:
    field_id: str
    state_type: str
    candidate_policy_ids: Tuple[str, ...]
    temporal_inputs: Dict[str, Any]
    confidence_inputs: Dict[str, Any]
    conflict_inputs: Dict[str, Any]
    owner_correction_inputs: Dict[str, Any]
    overlay_inputs: Dict[str, Any]


@dataclass(frozen=True)
class BehaviorPolicySelectionResultV1:
    selected_policy_ids: Tuple[str, ...] = field(default_factory=tuple)
    rejected_policy_ids: Tuple[str, ...] = field(default_factory=tuple)
    decision_outcome: str = BehaviorPolicyOutcomeV1.SKELETON_POLICY_DECISION.value
    selection_executed: bool = False
    placeholder_only: bool = True


@dataclass(frozen=True)
class BehaviorPolicyReplaySnapshotV1:
    policy_registry_version: str
    eligibility_matrix_version: str
    precedence_matrix_version: str
    composition_contract_version: str
    state_type_mapping_version: str
    temporal_policy_version: str
    confidence_policy_version: str
    conflict_policy_version: str


@dataclass(frozen=True)
class BehaviorPolicyDecisionV1:
    decision_id: str
    reducer_run_id: str
    field_id: str
    state_type: str
    candidate_policy_ids: Tuple[str, ...]
    eligible_policy_ids: Tuple[str, ...]
    rejected_policy_ids: Tuple[str, ...]
    selected_policy_ids: Tuple[str, ...]
    precedence_steps: Tuple[Dict[str, Any], ...]
    composition_sequence: Tuple[str, ...]
    temporal_inputs: Dict[str, Any]
    confidence_inputs: Dict[str, Any]
    conflict_inputs: Dict[str, Any]
    owner_correction_inputs: Dict[str, Any]
    overlay_inputs: Dict[str, Any]
    decision_outcome: str
    resulting_state_candidate: Any = None
    resulting_state_status_candidate: str = "candidate"
    unresolved_conditions: Tuple[str, ...] = field(default_factory=tuple)
    policy_replay_snapshot: BehaviorPolicyReplaySnapshotV1 = field(
        default_factory=lambda: BehaviorPolicyReplaySnapshotV1(
            policy_registry_version="v1",
            eligibility_matrix_version="v1",
            precedence_matrix_version="v1",
            composition_contract_version="v1",
            state_type_mapping_version="v1",
            temporal_policy_version="v1",
            confidence_policy_version="v1",
            conflict_policy_version="v1",
        )
    )
    deterministic_replay_key: str = ""
    skeleton_only: bool = True
    candidate_only: bool = True
    policy_execution_executed: bool = False
    state_mutation_executed: bool = False
    fact_promotion_executed: bool = False
    action_trigger_executed: bool = False
    runtime_execution: bool = False
