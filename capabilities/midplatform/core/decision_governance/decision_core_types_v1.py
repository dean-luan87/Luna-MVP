"""Core candidate types for Decision Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass(frozen=True)
class SourceRefV1:
    owner: str
    ref_id: str
    ref_type: str = "REFERENCE"
    read_only: bool = True
    reference_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class RiskCandidateV1:
    risk_ref_id: str
    severity: int
    likelihood: int
    unknowns: Tuple[str, ...] = field(default_factory=tuple)
    provenance: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class UtilityCandidateV1:
    utility_ref_id: str
    expected_benefit: int
    tradeoff_notes: Tuple[str, ...] = field(default_factory=tuple)
    uncertainty: Tuple[str, ...] = field(default_factory=tuple)
    provenance: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DecisionOptionCandidateV1:
    option_id: str
    option_statement: str
    utility: UtilityCandidateV1
    risk: RiskCandidateV1
    cost: int
    hard_constraints_ok: bool
    permission_allowed: bool
    safety_allowed: bool
    role_allowed: bool
    reversibility: str
    intent_alignment: int
    evidence_ready: bool = True


@dataclass(frozen=True)
class DecisionCandidateV1:
    decision_candidate_id: str
    owner: str
    candidate_kind: str
    option_id: str
    decision_state: str
    utility_score_candidate: int
    risk_score_candidate: int
    constraint_refs: Tuple[SourceRefV1, ...]
    permission_refs: Tuple[SourceRefV1, ...]
    safety_refs: Tuple[SourceRefV1, ...]
    resource_refs: Tuple[SourceRefV1, ...]
    uncertainty_unknowns: Tuple[str, ...]
    reversibility: str
    confirmation_requirement: str
    eligibility_candidate: bool
    veto_reasons: Tuple[str, ...]
    provenance: Tuple[SourceRefV1, ...]
    trace_ref: str
    revision_lineage: Tuple[str, ...] = field(default_factory=tuple)
    decision_authority: bool = True
    action_authority: bool = False
    task_authority: bool = False


@dataclass(frozen=True)
class DecisionSelectionCandidateV1:
    selected_candidate_ref: Optional[str]
    preferred_candidate_ref: Optional[str]
    rejected_candidate_refs: Tuple[str, ...]
    defer_reason: Optional[str]
    abstain_reason: Optional[str]
    request_more_evidence_reason: Optional[str]
    contested: bool
    confirmation_requirement: str
    execution_eligibility_candidate: bool
