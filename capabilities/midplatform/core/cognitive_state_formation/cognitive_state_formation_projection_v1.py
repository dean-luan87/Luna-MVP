"""Private projection helpers for Cognitive State Formation v1."""

from __future__ import annotations

from capabilities.midplatform.core.cognitive_state_formation.cognitive_hypothesis_types_v1 import (
    HypothesisCompetitionResultV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_handoff_types_v1 import (
    CognitiveToCausalHandoffCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_registry_v1 import (
    CANONICAL_OWNER,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_vector_types_v1 import (
    CognitiveStateVectorCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)


def _build_vector(
    sid: str,
    world: CurrentWorldCandidateV1,
    competition: HypothesisCompetitionResultV1,
) -> CognitiveStateVectorCandidateV1:
    return CognitiveStateVectorCandidateV1(
        state_vector_id=f"vector:{sid}",
        attention_distribution_refs=world.attention_refs,
        hypothesis_state_refs=competition.active_hypothesis_refs
        + competition.insufficient_evidence_refs,
        uncertainty_level_candidate="HIGH"
        if world.world_state_kind_candidate in {"UNKNOWN", "CONFLICTED"}
        else "MEDIUM",
        conflict_level_candidate="HIGH" if world.conflict_refs else "LOW",
        world_stability_candidate=world.world_stability_candidate,
        intent_pressure_candidate="MEDIUM",
        resource_pressure_candidate="LOW",
        current_world_ref=world.current_world_id,
        trace_ref=f"trace:{sid}:vector",
        provenance_refs=(f"prov:{sid}:vector",),
    )


def _build_handoff(
    sid: str,
    request: CognitiveStateFormationInputV1,
    world: CurrentWorldCandidateV1,
    competition: HypothesisCompetitionResultV1,
) -> CognitiveToCausalHandoffCandidateV1:
    evidence_refs = tuple(r.source_ref for r in request.evidence_refs)
    if not evidence_refs:
        evidence_refs = tuple(
            f"evidence:{sid}:{idx}"
            for idx in range(1, len(competition.active_hypothesis_refs) + 2)
        )
    return CognitiveToCausalHandoffCandidateV1(
        handoff_id=f"handoff:{sid}",
        handoff_type="CANDIDATE_REFERENCE_ONLY",
        producer_owner=CANONICAL_OWNER,
        consumer_owner="Causal Governance",
        attention_refs=world.attention_refs,
        active_hypothesis_refs=world.active_hypothesis_refs,
        alternative_hypothesis_refs=world.alternative_hypothesis_refs,
        context_refs=tuple(r.source_ref for r in request.context_refs),
        field_state_refs=tuple(r.source_ref for r in request.field_refs),
        observation_refs=tuple(r.source_ref for r in request.observation_refs),
        uncertainty_refs=tuple(r.source_ref for r in request.uncertainty_refs),
        conflict_refs=world.conflict_refs,
        evidence_refs=evidence_refs,
        trace_ref=f"trace:{sid}:handoff",
        provenance_refs=(f"prov:{sid}:handoff",),
    )
