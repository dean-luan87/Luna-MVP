"""Memory candidate and future persistence types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class MemoryCandidateV1:
    memory_candidate_id: str
    memory_type: str
    source_experience_candidate_refs: Tuple[str, ...]
    cycle_refs: Tuple[str, ...]
    salience_candidate: str
    retention_candidate: str
    decay_candidate: str
    refresh_candidate: str
    revision_parent_ref: str | None
    superseded_ref: str | None
    revocation_ref: str | None
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    privacy_sensitivity_level: str
    requires_user_confirmation: bool
    do_not_persist_candidate: bool
    future_retrieval_eligibility: str
    provenance_refs: Tuple[str, ...]
    schema_version: str
    contract_version: str
    candidate_only: bool = True
    persisted: bool = False
    fact_admitted: bool = False
    automatic_consolidation: bool = False


@dataclass(frozen=True)
class FuturePersistenceHandoffCandidateV1:
    handoff_id: str
    memory_candidate_ref: str
    persistence_target_kind: str
    persistence_executed: bool = False
    database_write: bool = False
    vector_store_write: bool = False
    candidate_only: bool = True
    trace_ref: str = ""
