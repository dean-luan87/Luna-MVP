"""Trace helper types for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ProvenanceReverseLookupV1:
    current_world_ref: str
    active_hypothesis_refs: Tuple[str, ...]
    attention_refs: Tuple[str, ...]
    source_context_or_field_or_observation_refs: Tuple[str, ...]


@dataclass(frozen=True)
class HandoffTraceV1:
    handoff_id: str
    hypothesis_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
