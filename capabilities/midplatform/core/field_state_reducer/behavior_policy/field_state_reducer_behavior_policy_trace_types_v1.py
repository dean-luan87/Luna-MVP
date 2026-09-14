from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class BehaviorPolicyEligibilityTraceStepV1:
    step_id: str
    policy_id: str
    status: str
    notes: str = ""


@dataclass(frozen=True)
class BehaviorPolicyPrecedenceTraceStepV1:
    step_id: str
    higher_policy: str
    lower_policy: str
    applied: bool
    reason: str = ""


@dataclass(frozen=True)
class BehaviorPolicyCompositionTraceStepV1:
    step_id: str
    mode: str
    sequence: Tuple[str, ...] = field(default_factory=tuple)
    notes: str = ""


@dataclass(frozen=True)
class BehaviorPolicyRejectionRefV1:
    policy_id: str
    reason: str


@dataclass(frozen=True)
class BehaviorPolicyReplayKeyV1:
    policy_registry_version: str
    eligibility_matrix_version: str
    precedence_matrix_version: str
    composition_contract_version: str
    stable_fingerprint: str


@dataclass(frozen=True)
class BehaviorPolicyTraceV1:
    trace_id: str
    reducer_run_id: str
    field_id: str
    state_type: str
    candidate_policy_ids: Tuple[str, ...]
    eligible_policy_ids: Tuple[str, ...]
    rejected_policy_ids: Tuple[str, ...]
    selected_policy_ids: Tuple[str, ...]
    precedence_steps: Tuple[BehaviorPolicyPrecedenceTraceStepV1, ...] = field(
        default_factory=tuple
    )
    composition_sequence: Tuple[str, ...] = field(default_factory=tuple)
    temporal_inputs: Dict[str, Any] = field(default_factory=dict)
    confidence_inputs: Dict[str, Any] = field(default_factory=dict)
    conflict_inputs: Dict[str, Any] = field(default_factory=dict)
    owner_correction_inputs: Dict[str, Any] = field(default_factory=dict)
    overlay_inputs: Dict[str, Any] = field(default_factory=dict)
    policy_versions: Dict[str, str] = field(default_factory=dict)
    replay_key: str = ""
    eligibility_steps: Tuple[BehaviorPolicyEligibilityTraceStepV1, ...] = field(
        default_factory=tuple
    )
    composition_steps: Tuple[BehaviorPolicyCompositionTraceStepV1, ...] = field(
        default_factory=tuple
    )
    rejection_refs: Tuple[BehaviorPolicyRejectionRefV1, ...] = field(
        default_factory=tuple
    )
    skeleton_only: bool = True
    candidate_only: bool = True
    policy_execution_executed: bool = False
    runtime_execution: bool = False
