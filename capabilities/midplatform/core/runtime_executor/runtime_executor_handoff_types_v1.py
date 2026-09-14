"""Downstream result handoff candidate types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResultHandoffCandidateV1:
    handoff_id: str
    producer_owner: str
    consumer_owner: str
    handoff_kind: str
    execution_result_candidate_ref: str
    failure_candidate_ref_optional: str | None
    partial_result_candidate_ref_optional: str | None
    trace_ref: str
    provenance_ref: str
    reference_only: bool = True
    owner_mutation: bool = False
