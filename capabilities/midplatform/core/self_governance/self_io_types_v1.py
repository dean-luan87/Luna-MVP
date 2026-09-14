"""Input/output contracts for deterministic Self Governance evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from .self_attribution_types_v1 import SelfAttributionCandidateV1
from .self_continuity_types_v1 import SelfContinuityCandidateV1
from .self_reference_types_v1 import SelfReferenceCandidateV1
from .self_revision_types_v1 import (
    SelfExpirationCandidateV1,
    SelfRevisionCandidateV1,
    SelfRevocationCandidateV1,
    SelfSupersessionCandidateV1,
)
from .self_trace_types_v1 import SelfProvenanceV1, SelfTraceV1
from .self_influence_types_v1 import SelfEvidenceInfluenceCandidateV1


@dataclass(frozen=True)
class SelfGovernanceInputV1:
    scenario_id: str
    statement: str
    source_owner: str
    source_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    root_cycle_trace_id: str
    temporal_validity: str = "TRANSIENT"
    uncertainty: str = "MEDIUM"
    sensitivity: str = "NORMAL"
    boundary_class: str | None = None
    requested_domain: str = "IDENTITY"
    user_correction: bool = False
    replayed_evidence: bool = False
    duplicate_request: bool = False
    duplicate_continuity_update: bool = False
    duplicate_revision: bool = False
    duplicate_revocation: bool = False
    duplicate_supersession: bool = False
    prior_self_candidate_ref: str | None = None
    current_self_candidate_ref: str | None = None
    source_intent_refs: Tuple[str, ...] = ()
    source_memory_refs: Tuple[str, ...] = ()
    source_learning_refs: Tuple[str, ...] = ()
    source_pcn_refs: Tuple[str, ...] = ()
    source_regulation_refs: Tuple[str, ...] = ()
    source_context_refs: Tuple[str, ...] = ()
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class SelfGovernanceOutputV1:
    scenario_id: str
    self_reference: SelfReferenceCandidateV1
    self_attribution: SelfAttributionCandidateV1 | None
    self_continuity: SelfContinuityCandidateV1 | None
    revision: SelfRevisionCandidateV1 | None
    revocation: SelfRevocationCandidateV1 | None
    supersession: SelfSupersessionCandidateV1 | None
    expiration: SelfExpirationCandidateV1 | None
    influences: Tuple[SelfEvidenceInfluenceCandidateV1, ...]
    trace: SelfTraceV1
    provenance: SelfProvenanceV1
    boundary_class: str
    duplicate_guard_triggered: bool
    replay_guard_triggered: bool
    user_correction_precedence: bool
    idempotency_guards: Dict[str, bool] = field(default_factory=dict)
    negative_guards: Dict[str, bool] = field(default_factory=dict)
    synthetic_only: bool = True
    candidate_only: bool = True
    runtime_execution: bool = False
    database_write: bool = False
    vector_store_write: bool = False
    embedding_execution: bool = False
    model_call: bool = False
    scheduler_execution: bool = False
    task_mutation: bool = False
    source_owner_mutation: bool = False
    personality_mutation: bool = False
    emotion_mutation: bool = False
    semantic_compression_execution: bool = False
    cross_user_transfer: bool = False
