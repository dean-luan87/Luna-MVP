"""Private versioning/provenance helpers for Cognitive State Formation v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.core.cognitive_state_formation.cognitive_hypothesis_types_v1 import (
    HypothesisCompetitionResultV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    ProvenanceEnvelopeV1,
    TraceEnvelopeV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_handoff_types_v1 import (
    CognitiveToCausalHandoffCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)


def _build_trace_and_provenance(
    request: CognitiveStateFormationInputV1,
    sid: str,
    world: CurrentWorldCandidateV1,
    competition: HypothesisCompetitionResultV1,
    handoff: CognitiveToCausalHandoffCandidateV1,
) -> Tuple[TraceEnvelopeV1, ProvenanceEnvelopeV1]:
    trace = TraceEnvelopeV1(
        root_trace_id=f"trace:{sid}:root",
        attention_trace_ref=f"trace:{sid}:attention",
        hypothesis_trace_ref=f"trace:{sid}:hypothesis",
        current_world_trace_ref=world.trace_ref,
        downstream_handoff_trace_ref=handoff.trace_ref,
        revision_lineage_refs=(f"lineage:{sid}:revision",)
        if sid in {"S10"}
        else (),
        revocation_lineage_refs=(f"lineage:{sid}:revocation",)
        if sid in {"S11", "S20"}
        else (),
        source_version_lineage_refs=(
            "context:v1",
            "pcn:v1",
            "intent:v1",
            "field:v1",
            "observation:v1",
            "current-world-candidate-v1"
            if request.current_world_ref is not None
            else "",
        ),
        alternative_hypothesis_lineage_refs=competition.alternative_explanation_refs,
    )
    provenance = ProvenanceEnvelopeV1(
        source_refs=tuple(
            item
            for item in (
                *((request.current_world_ref.source_ref,)
                  if request.current_world_ref is not None
                  else ()),
                "context",
                "pcn",
                "intent",
                "field",
                "observation",
                "risk",
                "uncertainty",
                "task",
                "role",
                "memory",
            )
            if item
        ),
        owner_refs=(
            "Context Foundation",
            "Personal Cognitive Network Governance",
            "Intent Governance",
            "Field State Reducer",
            "Cognitive State Formation Governance",
            "Causal Governance",
        ),
        version_refs=("v1",),
        reverse_lookup=(
            (world.current_world_id, (
                *((request.current_world_ref.source_ref,)
                  if request.current_world_ref is not None
                  else ()),
                *world.active_hypothesis_refs,
                *world.attention_refs,
                *world.context_refs,
                *world.field_state_refs,
                *world.observation_refs,
            )),
            (handoff.handoff_id, (
                *handoff.active_hypothesis_refs,
                *handoff.evidence_refs,
                *handoff.context_refs,
                *handoff.field_state_refs,
            )),
        ),
    )
    return trace, provenance
