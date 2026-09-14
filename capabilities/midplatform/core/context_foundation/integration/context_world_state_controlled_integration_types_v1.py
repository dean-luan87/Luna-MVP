"""Candidate-only Context / Field / Current World integration types v1.

This package is an adapter layer inside the existing Context Foundation owner.
It does not create a World owner and it does not grant mutation authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)


@dataclass(frozen=True)
class ObservationContextHandoffCandidateV1:
    handoff_id: str
    observation_refs: Tuple[str, ...]
    admitted_observation_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    correction_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    context_mutation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class FieldEventHandoffCandidateV1:
    event_id: str
    event_type: str
    field_ref: str
    observation_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    occurred_at: str
    observed_at: str
    received_at: str
    temporal_status: str
    admission_status: str
    admission_required: bool
    reducer_eligible: bool
    reducer_input_candidate: Dict[str, Any]
    contradiction_refs: Tuple[str, ...]
    correction_refs: Tuple[str, ...]
    supersedes_ref: str
    revocation_refs: Tuple[str, ...]
    expiration_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    field_state_mutation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class ContextWorldAssemblyCandidateV1:
    context_id: str
    context_ref: str
    task_refs: Tuple[str, ...]
    observation_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    source_context_foundation_trace_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    context_status: str
    reference_only: bool = True
    context_mutation: bool = False
    truth_declared: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class ContextWorldTraceV1:
    root_trace_id: str
    current_world_trace_ref: str
    context_trace_ref: str
    field_event_trace_refs: Tuple[str, ...]
    observation_trace_refs: Tuple[str, ...]
    evidence_trace_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    correction_lineage: Tuple[str, ...]
    contradiction_lineage: Tuple[str, ...]
    temporal_lineage: Tuple[str, ...]
    reverse_lookup_path: Tuple[str, ...]
    authority_granted: bool = False


@dataclass(frozen=True)
class ContextWorldStateControlResultV1:
    case_id: str
    observation_context_handoff: ObservationContextHandoffCandidateV1 | None
    field_event_handoff: FieldEventHandoffCandidateV1 | None
    context: ContextWorldAssemblyCandidateV1 | None
    current_world: CurrentWorldCandidateV1 | None
    trace: ContextWorldTraceV1
    behavior: Dict[str, Any]
    errors: Tuple[Dict[str, Any], ...] = field(default_factory=tuple)
    negative_guards: Dict[str, bool] = field(default_factory=dict)
    next_route_handoff_ref: str = ""
    candidate_only: bool = True
    synthetic_only: bool = True
