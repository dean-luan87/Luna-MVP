"""Provenance trace types for Action Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ActionTraceCandidateV1:
    trace_id: str
    owner: str
    action_candidate_ref: str
    decision_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    causal_refs: Tuple[str, ...]
    target_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    precondition_refs: Tuple[str, ...]
    dependency_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    confirmation_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    rollback_refs: Tuple[str, ...]
    failure_refs: Tuple[str, ...]
    revision_refs: Tuple[str, ...]
    provenance: Tuple[str, ...]
    candidate_only: bool = True
