"""Static validators for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_core_types_v1 import (
    NegativeGuardStatusV1,
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_inheritance_types_v1 import (
    CognitiveMemoryObservationCandidateV1,
    CycleInheritanceCandidateV1,
    FutureLearningHandoffCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_cycle_transition_types_v1 import (
    CognitiveCycleTransitionCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_io_types_v1 import (
    CognitiveFlowOutputV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_ownership_guard_v1 import (
    validate_no_owner_transfer,
    validate_source_refs_read_only,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_flow_registry_v1 import (
    CYCLE_STATES,
    NEGATIVE_GUARDS,
    RELATIONSHIP_KINDS,
)


def validate_transition_set(
    transitions: Iterable[CognitiveCycleTransitionCandidateV1],
) -> bool:
    return all(
        item.source_state in CYCLE_STATES + ("ANY_ACTIVE",)
        and item.target_state in CYCLE_STATES
        and item.relationship_kind in RELATIONSHIP_KINDS
        and item.transition_candidate_only is True
        and item.runtime_transition_executed is False
        and item.owner_mutation is False
        and bool(item.trace_ref)
        for item in transitions
    )


def validate_inheritance(candidate: CycleInheritanceCandidateV1 | None) -> bool:
    if candidate is None:
        return True
    return (
        candidate.candidate_only is True
        and candidate.mutable_runtime_state_inherited is False
        and bool(candidate.trace_ref)
    )


def validate_memory_boundary(
    candidate: CognitiveMemoryObservationCandidateV1 | None,
) -> bool:
    if candidate is None:
        return True
    return (
        candidate.candidate_only is True
        and candidate.memory_write is False
        and candidate.memory_fact_creation is False
        and candidate.memory_owner_transfer is False
    )


def validate_learning_boundary(
    candidate: FutureLearningHandoffCandidateV1 | None,
) -> bool:
    if candidate is None:
        return True
    return (
        candidate.candidate_only is True
        and candidate.learning_execution is False
        and candidate.parameter_mutation is False
        and candidate.genome_activation is False
        and candidate.intent_mutation is False
        and candidate.state_mutation is False
    )


def validate_negative_guard_status(guard: NegativeGuardStatusV1 | None) -> bool:
    if guard is None:
        return False
    return asdict(guard) == NEGATIVE_GUARDS


def validate_output_contract(
    output: CognitiveFlowOutputV1, refs: Iterable[SourceRefV1]
) -> bool:
    return (
        output.candidate_only is True
        and output.synthetic_only is True
        and output.runtime_executed is False
        and output.source_owner_mutation is False
        and output.final_state.current_state in CYCLE_STATES
        and output.final_state.candidate_only is True
        and output.final_state.runtime_transition_executed is False
        and output.final_state.owner_mutation is False
        and validate_source_refs_read_only(refs)
        and validate_no_owner_transfer(refs)
        and validate_transition_set(output.transition_candidates)
        and validate_inheritance(output.inheritance_candidate)
        and validate_memory_boundary(output.memory_observation_candidate)
        and validate_learning_boundary(output.learning_handoff_candidate)
        and validate_negative_guard_status(output.negative_guard_status)
        and output.trace is not None
        and output.provenance is not None
    )
