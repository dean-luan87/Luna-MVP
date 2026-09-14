"""Candidate-only types for the A working-context bridge."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class AWorkingEnvelopeCandidateV1:
    work_ref: str
    concern_ref: str
    goal_refs: Tuple[str, ...]
    authority_grant_ref: str
    role_refs: Tuple[str, ...]
    perspective_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    behavior_refs: Tuple[str, ...]
    emotion_modulation_refs: Tuple[str, ...]
    experience_prior_refs: Tuple[str, ...]
    attention_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    resource_envelope_refs: Tuple[str, ...]
    source_cognitive_state_version_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True
    authoritative_state_duplicated: bool = False
    source_owner_preserved: bool = True


@dataclass(frozen=True)
class WorkingEnvelopeVersionCandidateV1:
    envelope_ref: str
    version_ref: str
    parent_version_ref: Optional[str]
    source_state_version_ref: str
    changed_source_refs: Tuple[str, ...]
    unchanged_source_refs: Tuple[str, ...]
    change_reason_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class AEnvironmentImpactAssessmentCandidateV1:
    assessment_ref: str
    work_ref: str
    concern_ref: str
    source_envelope_ref: str
    source_envelope_version_ref: str
    source_state_version_ref: str
    changed_source_refs: Tuple[str, ...]
    impact_disposition: str
    reason_refs: Tuple[str, ...]
    grant_ref: str
    decision_owner_ref: str = "A_REASONING_ROLE"
    accepted: bool = True
    failure_class: Optional[str] = None
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class ACognitiveRequirementCandidateV1:
    requirement_ref: str
    work_ref: str
    concern_ref: str
    source_need_decision_ref: str
    source_need_ref: str
    source_state_version_ref: str
    information_gap_ref: str
    requested_information_type: str
    requested_operation: str
    required_evidence_characteristics_refs: Tuple[str, ...]
    priority_ref: str
    resource_constraint_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    issuing_owner_ref: str = "A_REASONING_ROLE"
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class AEvidenceReturnCandidateV1:
    return_ref: str
    work_ref: str
    concern_ref: str
    source_requirement_ref: str
    capability_requirement_ref: str
    scope_ref: str
    resolution_ref: str
    observation_candidate_ref: str
    observation_admission_ref: str
    evidence_refs: Tuple[str, ...]
    source_state_version_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    target_owner_ref: str = "A_REASONING_ROLE"
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class WorkingEnvelopeInvalidationCandidateV1:
    invalidation_ref: str
    source_change_refs: Tuple[str, ...]
    affected_envelope_ref: str
    affected_state_version_ref: str
    affected_grant_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


__all__ = [
    "AWorkingEnvelopeCandidateV1",
    "WorkingEnvelopeVersionCandidateV1",
    "AEnvironmentImpactAssessmentCandidateV1",
    "ACognitiveRequirementCandidateV1",
    "AEvidenceReturnCandidateV1",
    "WorkingEnvelopeInvalidationCandidateV1",
]
