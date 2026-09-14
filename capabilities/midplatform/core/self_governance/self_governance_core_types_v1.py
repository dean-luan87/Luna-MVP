"""Shared immutable value types for Self Governance candidates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SourceReferenceV1:
    owner: str
    ref_id: str
    ref_type: str = "REFERENCE"
    read_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class TemporalValidityV1:
    valid_from_ref: str
    valid_until_ref: str
    status: str = "TRANSIENT"


@dataclass(frozen=True)
class TraceLinkV1:
    root_cycle_trace_id: str
    self_trace_id: str
    source_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    schema_version: str
    contract_version: str
    reverse_locatable: bool = True
    provenance_grants_authority: bool = False
