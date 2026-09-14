"""Reversible trace and provenance types for Self candidates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .self_governance_registry_v1 import CONTRACT_VERSION, SCHEMA_VERSION


@dataclass(frozen=True)
class SelfTraceV1:
    root_cycle_trace_id: str
    self_trace_id: str
    self_ref_id: str
    self_attribution_id: str | None
    continuity_id: str | None
    source_intent_refs: Tuple[str, ...]
    source_memory_refs: Tuple[str, ...]
    source_learning_refs: Tuple[str, ...]
    source_pcn_refs: Tuple[str, ...]
    source_regulation_refs: Tuple[str, ...]
    source_context_refs: Tuple[str, ...]
    revision_refs: Tuple[str, ...]
    revocation_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION
    reverse_locatable: bool = True
    provenance_grants_authority: bool = False
    source_owner_mutation: bool = False


@dataclass(frozen=True)
class SelfProvenanceV1:
    provenance_id: str
    source_owner_trace: Tuple[str, ...]
    original_source_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    upstream_trace_refs: Tuple[str, ...]
    self_trace_id: str
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION
    reverse_locatable: bool = True
    immutable: bool = True
