"""Regulation candidate, influence, revision, and revocation types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_types_v1 import (
    ParameterConflictCandidateV1,
    ParameterModulationCandidateV1,
)


@dataclass(frozen=True)
class InfluenceCandidateV1:
    influence_id: str
    influence_kind: str
    target_owner: str
    source_regulation_ref: str
    parameter_modulation_ref: Optional[str]
    reason_codes: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    owner_transfer: bool = False
    target_mutation: bool = False
    decision_override: bool = False
    action_override: bool = False


@dataclass(frozen=True)
class DynamicRegulationCandidateV1:
    regulation_id: str
    owner: str
    state_vector_ref: str
    context_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    emotion_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    learning_refs: Tuple[str, ...]
    policy_refs: Tuple[str, ...]
    parameter_bound_refs: Tuple[str, ...]
    modulation_candidates: Tuple[ParameterModulationCandidateV1, ...]
    conflict_candidates: Tuple[ParameterConflictCandidateV1, ...]
    influence_candidates: Tuple[InfluenceCandidateV1, ...]
    state_candidate: str
    evaluation_status: str
    reason_codes: Tuple[str, ...]
    unknowns: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    revision_parent_ref: Optional[str] = None
    revocation_parent_ref: Optional[str] = None
    candidate_only: bool = True
    runtime_side_effect: bool = False
    source_mutation: bool = False


@dataclass(frozen=True)
class RegulationRevisionCandidateV1:
    revision_id: str
    prior_regulation_ref: str
    revised_regulation_ref: str
    reason_codes: Tuple[str, ...]
    source_version_lineage: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True


@dataclass(frozen=True)
class RegulationRevocationCandidateV1:
    revocation_id: str
    revoked_regulation_ref: str
    reason_codes: Tuple[str, ...]
    source_version_lineage: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    source_deleted: bool = False
