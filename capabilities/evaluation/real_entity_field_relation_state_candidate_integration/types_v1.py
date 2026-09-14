"""Evaluation result contracts for Entity↔Field relation state reduction."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class EntityFieldRelationStateCandidateCaseResultV1:
    case_id: str
    source_mode: str
    admitted_events: Tuple[Dict[str, Any], ...]
    reducer_result: Dict[str, Any]
    typed_relation_state_candidate: Dict[str, Any] | None
    behavior: Dict[str, Any]
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


__all__ = ["EntityFieldRelationStateCandidateCaseResultV1"]
