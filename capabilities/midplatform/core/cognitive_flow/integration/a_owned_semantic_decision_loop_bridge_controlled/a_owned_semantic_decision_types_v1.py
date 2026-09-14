"""Candidate-only A-owned semantic decision envelopes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass(frozen=True)
class ASemanticDecisionContextV1:
    work_ref: str
    concern_ref: str
    a_grant_ref: str
    source_state_version_ref: str
    goal_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    role_refs: Tuple[str, ...]
    perspective_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    task_behavior_refs: Tuple[str, ...]
    emotion_modulation_refs: Tuple[str, ...]
    experience_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    resource_envelope_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    prior_need_refs: Tuple[str, ...]
    prior_hypothesis_refs: Tuple[str, ...]
    prior_requirement_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class ACurrentNeedDecisionCandidateV1:
    decision_ref: str
    work_ref: str
    concern_ref: str
    source_state_version_ref: str
    selected_need_ref: Optional[str]
    alternative_need_refs: Tuple[str, ...]
    selection_reason_refs: Tuple[str, ...]
    evidence_basis_refs: Tuple[str, ...]
    hypothesis_basis_refs: Tuple[str, ...]
    grant_ref: str
    decision_owner_ref: str = "A_REASONING_ROLE"
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class ALocalSufficiencyDecisionCandidateV1:
    decision_ref: str
    work_ref: str
    concern_ref: str
    source_state_version_ref: str
    sufficiency_status: str
    sufficiency_reason_refs: Tuple[str, ...]
    evidence_basis_refs: Tuple[str, ...]
    current_need_ref: Optional[str]
    grant_ref: str
    decision_owner_ref: str = "A_REASONING_ROLE"
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class AReconsiderationDecisionCandidateV1:
    decision_ref: str
    work_ref: str
    concern_ref: str
    source_state_version_ref: str
    reconsideration_required: bool
    reconsideration_reason_refs: Tuple[str, ...]
    invalidated_hypothesis_refs: Tuple[str, ...]
    stale_requirement_refs: Tuple[str, ...]
    replacement_need_ref: Optional[str]
    grant_ref: str
    decision_owner_ref: str = "A_REASONING_ROLE"
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class ANextStepDecisionCandidateV1:
    decision_ref: str
    source_need_decision_ref: str
    source_sufficiency_decision_ref: str
    source_reconsideration_decision_ref: str
    next_step_disposition: str
    selected_next_need_ref: Optional[str]
    reason_refs: Tuple[str, ...]
    grant_ref: str
    decision_owner_ref: str = "A_REASONING_ROLE"
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class ASemanticDecisionValidationCandidateV1:
    validation_ref: str
    decision_kind: str
    grant_ref: str
    required_authority_ref: str
    concern_ref: str
    work_ref: str
    source_state_version_ref: str
    accepted: bool
    failure_class: Optional[str]
    grant_active: bool
    scope_ok: bool
    state_version_ok: bool
    authority_ok: bool
    decision_owner_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class ASemanticDecisionBundleV1:
    context: ASemanticDecisionContextV1
    need_decision: Optional[ACurrentNeedDecisionCandidateV1]
    sufficiency_decision: Optional[ALocalSufficiencyDecisionCandidateV1]
    reconsideration_decision: Optional[AReconsiderationDecisionCandidateV1]
    next_step_decision: Optional[ANextStepDecisionCandidateV1]
    validations: Tuple[ASemanticDecisionValidationCandidateV1, ...]
    compatibility_source_owner_ref: str
    compatibility_wrapper_only: bool
    candidate_only: bool = True
    synthetic_only: bool = True


__all__ = [
    "ASemanticDecisionContextV1",
    "ACurrentNeedDecisionCandidateV1",
    "ALocalSufficiencyDecisionCandidateV1",
    "AReconsiderationDecisionCandidateV1",
    "ANextStepDecisionCandidateV1",
    "ASemanticDecisionBundleV1",
    "ASemanticDecisionValidationCandidateV1",
]
