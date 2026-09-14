"""Core candidate types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class SourceRefV1:
    owner: str
    ref_id: str
    ref_type: str = "REFERENCE"
    read_only: bool = True
    reference_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class ActionCandidateV1:
    action_candidate_id: str
    owner: str
    candidate_kind: str
    source_decision_refs: Tuple[SourceRefV1, ...]
    intent_refs: Tuple[SourceRefV1, ...]
    causal_refs: Tuple[SourceRefV1, ...]
    target_refs: Tuple[SourceRefV1, ...]
    context_refs: Tuple[SourceRefV1, ...]
    field_refs: Tuple[SourceRefV1, ...]
    permission_refs: Tuple[SourceRefV1, ...]
    safety_refs: Tuple[SourceRefV1, ...]
    confirmation_refs: Tuple[SourceRefV1, ...]
    precondition_refs: Tuple[SourceRefV1, ...]
    dependency_refs: Tuple[SourceRefV1, ...]
    resource_refs: Tuple[SourceRefV1, ...]
    reversibility: str
    action_state: str
    execution_readiness: str
    cancellation_policy: str
    rollback_policy: str
    provenance: Tuple[SourceRefV1, ...]
    revision_lineage: Tuple[str, ...] = field(default_factory=tuple)
    action_authority: bool = True
    runtime_authority: bool = False
    task_authority: bool = False
