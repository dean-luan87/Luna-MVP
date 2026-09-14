"""Evaluation-only result type for EntityCandidate to Field relations.

The relation itself is the canonical ``RelationCandidateV1``.  This module
only packages bounded evaluation output and deliberately does not introduce a
second relation schema or a new relation owner.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class EntityFieldRelationCaseResultV1:
    case_id: str
    entity_candidates: Tuple[Dict[str, Any], ...]
    subject_binding_refs: Tuple[str, ...]
    relation_candidates: Tuple[Dict[str, Any], ...]
    relation_traces: Tuple[Dict[str, Any], ...]
    semantic_trace: Dict[str, Any] | None
    behavior: Dict[str, Any]
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


__all__ = ["EntityFieldRelationCaseResultV1"]
