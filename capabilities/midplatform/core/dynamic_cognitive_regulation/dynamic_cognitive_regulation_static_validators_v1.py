"""Pure validation helpers used by the user-terminal controlled runner."""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_bounds_types_v1 import (
    CognitiveParameterBoundsV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.cognitive_parameter_types_v1 import (
    ParameterModulationCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_core_types_v1 import (
    NegativeGuardStatusV1,
    SourceRefV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_io_types_v1 import (
    CognitiveStateVectorInputCandidateV1,
    DynamicCognitiveRegulationOutputV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_ownership_guard_v1 import (
    validate_genome_boundary,
    validate_source_refs_read_only,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_cognitive_regulation_registry_v1 import (
    CANONICAL_OWNER,
    LIFECYCLE_STATES,
    NEGATIVE_GUARDS,
    PARAMETER_CLASSES,
    REQUIRED_PARAMETER_KINDS,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_handoff_types_v1 import (
    DynamicRegulationHandoffCandidateV1,
)
from capabilities.midplatform.core.dynamic_cognitive_regulation.dynamic_regulation_trace_types_v1 import (
    DynamicRegulationProvenanceV1,
    DynamicRegulationTraceV1,
)


def validate_state_vector_boundary(vector: CognitiveStateVectorInputCandidateV1) -> bool:
    return (
        vector.candidate_only is True
        and vector.parameter_store is False
        and vector.model_weight is False
        and vector.long_term_memory is False
        and vector.learning_result is False
        and bool(vector.state_vector_id)
        and bool(vector.trace_ref)
        and bool(vector.provenance_refs)
    )


def validate_parameter_class_coverage() -> bool:
    return set(PARAMETER_CLASSES) == {"A", "B", "C", "D", "E"}


def validate_parameter_kind_coverage(items: Iterable[str]) -> bool:
    return set(REQUIRED_PARAMETER_KINDS).issubset(set(items))


def validate_bounds_contract(bounds: Iterable[CognitiveParameterBoundsV1]) -> bool:
    return all(
        item.lower_bound <= item.upper_bound
        and item.step_bound >= 0.0
        and item.frozen is True
        and item.bypass_allowed is False
        and item.parameter_class in PARAMETER_CLASSES
        and bool(item.policy_ref)
        and bool(item.trace_ref)
        for item in bounds
    )


def validate_modulation_candidates(
    items: Iterable[ParameterModulationCandidateV1],
    bounds_by_parameter: dict[str, CognitiveParameterBoundsV1],
) -> bool:
    for item in items:
        bounds = bounds_by_parameter.get(item.parameter_id)
        if bounds is None or item.silent_coercion is not False:
            return False
        if item.effective_value is not None and not (
            bounds.lower_bound <= item.effective_value <= bounds.upper_bound
        ):
            return False
        if item.candidate_only is not True or item.auto_applied or item.persisted:
            return False
    return True


def validate_handoff_boundary(handoff: DynamicRegulationHandoffCandidateV1) -> bool:
    return (
        handoff.producer_owner == CANONICAL_OWNER
        and handoff.candidate_only is True
        and handoff.attention_mutation is False
        and handoff.intent_mutation is False
        and handoff.hypothesis_mutation is False
        and handoff.causal_mutation is False
        and handoff.emotion_mutation is False
        and handoff.learning_direct_activation is False
        and handoff.scheduler_execution is False
        and handoff.task_mutation is False
        and handoff.runtime_command is False
        and handoff.device_control is False
    )


def validate_trace_reverse_locatable(
    trace: DynamicRegulationTraceV1,
    provenance: DynamicRegulationProvenanceV1,
) -> bool:
    chain = trace.reverse_lookup.get(trace.resulting_regulation_candidate_ref, ())
    return (
        bool(trace.root_trace_id)
        and bool(trace.cognitive_state_vector_ref)
        and bool(trace.state_vector_trace_ref)
        and bool(trace.source_influence_refs)
        and bool(trace.parameter_refs)
        and bool(trace.parameter_bounds_refs)
        and bool(trace.policy_refs)
        and bool(trace.regulation_function_id)
        and bool(trace.regulation_function_version)
        and bool(trace.influence_handoff_trace_ref)
        and trace.cognitive_state_vector_ref in chain
        and all(ref in chain for ref in trace.source_influence_refs)
        and all(ref in chain for ref in trace.parameter_bounds_refs)
        and all(ref in chain for ref in trace.policy_refs)
        and provenance.reverse_locatable is True
        and provenance.source_mutation_authority is False
        and provenance.resulting_candidate_ref
        == trace.resulting_regulation_candidate_ref
    )


def validate_negative_guard_status(guard: NegativeGuardStatusV1) -> bool:
    return asdict(guard) == NEGATIVE_GUARDS


def validate_output_contract(
    output: DynamicCognitiveRegulationOutputV1,
    source_refs: Iterable[SourceRefV1],
    bounds_by_parameter: dict[str, CognitiveParameterBoundsV1],
) -> bool:
    candidate = output.regulation_candidate
    return (
        output.candidate_only is True
        and output.synthetic_only is True
        and output.runtime_executed is False
        and output.source_mutation_executed is False
        and candidate.owner == CANONICAL_OWNER
        and candidate.candidate_only is True
        and candidate.runtime_side_effect is False
        and candidate.source_mutation is False
        and output.state_candidate.current_state in LIFECYCLE_STATES
        and output.state_candidate.runtime_activation is False
        and validate_source_refs_read_only(source_refs)
        and validate_modulation_candidates(
            candidate.modulation_candidates, bounds_by_parameter
        )
        and validate_handoff_boundary(output.handoff_candidate)
        and validate_trace_reverse_locatable(output.trace, output.provenance)
        and validate_negative_guard_status(output.negative_guard_status)
        and validate_genome_boundary(output.genome_candidate)
    )
