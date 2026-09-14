"""Handoff sequencing types for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ModuleHandoffEnvelopeV1:
    handoff_id: str
    source_owner: str
    target_owner: str
    source_candidate_ref: str
    required_refs: Tuple[str, ...]
    relationship_kind: str
    trace_ref: str
    provenance_ref: str
    schema_version: str
    contract_version: str
    candidate_only: bool = True
    source_owner_mutation: bool = False
