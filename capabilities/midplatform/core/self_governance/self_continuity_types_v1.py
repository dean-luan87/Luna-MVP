"""Continuity candidates preserve change and unresolved attribution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SelfContinuityCandidateV1:
    continuity_id: str
    prior_self_candidate_ref: str | None
    current_self_candidate_ref: str
    continuity_kind: str
    stable_refs: Tuple[str, ...]
    changed_refs: Tuple[str, ...]
    unresolved_refs: Tuple[str, ...]
    revision_refs: Tuple[str, ...]
    revocation_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    root_cycle_trace_id: str
    self_id_ref: str
    previous_self_state_ref: str | None
    current_self_state_candidate_ref: str
    persistent_self_attribute_candidate_refs: Tuple[str, ...]
    transient_self_attribute_candidate_refs: Tuple[str, ...]
    unresolved_attribution_refs: Tuple[str, ...]
    revision_lineage_refs: Tuple[str, ...]
    revocation_lineage_refs: Tuple[str, ...]
    schema_version: str
    contract_version: str
    candidate_only: bool = True
    immutable_identity_claim: bool = False
