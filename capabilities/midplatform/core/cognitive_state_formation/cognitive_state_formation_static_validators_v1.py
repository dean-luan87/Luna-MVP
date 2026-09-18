"""Static validators for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from typing import Any, Iterable, Sequence, Tuple

from capabilities.midplatform.core.cognitive_state_formation.attention_types_v1 import (
    AttentionCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_hypothesis_types_v1 import (
    CognitiveHypothesisCandidateV1,
    HypothesisCompetitionResultV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    CognitiveReferenceSemanticV1,
    NegativeGuardStatusV1,
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_handoff_types_v1 import (
    CognitiveToCausalHandoffCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
    CognitiveStateFormationOutputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_conditioning_types_v1 import (
    CognitiveRelationInterpretationCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_ownership_guard_v1 import (
    validate_field_ref_read_only,
    validate_no_owner_transfer,
    validate_ref_read_only,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_loop_types_v1 import (
    validate_cognitive_loop_candidates_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_registry_v1 import (
    HYPOTHESIS_STATES,
    NEGATIVE_GUARDS,
    WORLD_STATE_KINDS,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    LIVE_RUNTIME,
    SYNTHETIC_CONTROLLED,
)


def _valid_typed_refs(value: Any) -> bool:
    return isinstance(value, (list, tuple)) and all(isinstance(item, SourceRefV1) for item in value)


def _valid_string_refs(value: Any) -> bool:
    return isinstance(value, (list, tuple)) and all(isinstance(item, str) and bool(item.strip()) for item in value)


def validate_input_contract(request: CognitiveStateFormationInputV1) -> Tuple[str, ...]:
    """Reject invalid structure before semantic or epistemic processing."""
    if not isinstance(request, CognitiveStateFormationInputV1):
        return ("request_type_invalid",)
    errors = []
    if not isinstance(request.scenario_id, str) or not request.scenario_id.strip():
        errors.append("scenario_id_invalid_field_type")
    for name in (
        "context_refs", "pcn_refs", "intent_refs", "field_refs", "observation_refs",
        "risk_refs", "uncertainty_refs", "task_refs", "role_refs", "memory_refs",
        "evidence_refs", "goal_refs", "concern_refs", "information_need_refs", "relation_refs",
    ):
        if not _valid_typed_refs(getattr(request, name)):
            errors.append(f"{name}_must_contain_typed_source_refs")
    for name in ("required_information_refs", "available_information_refs", "inherited_information_refs", "prior_hypothesis_refs"):
        if not _valid_string_refs(getattr(request, name)):
            errors.append(f"{name}_must_contain_strings")
    for name in ("current_world_ref", "prior_current_world_ref"):
        value = getattr(request, name)
        if value is not None and not isinstance(value, SourceRefV1):
            errors.append(f"{name}_invalid_shape")
    if not isinstance(request.evidence_information_refs, (list, tuple)):
        errors.append("evidence_information_refs_invalid_shape")
    else:
        for index, item in enumerate(request.evidence_information_refs):
            if (not isinstance(item, (list, tuple)) or len(item) != 2
                    or not isinstance(item[0], str) or not item[0].strip()
                    or not _valid_string_refs(item[1])):
                errors.append(f"evidence_information_refs[{index}]_invalid_shape")
    if not isinstance(request.semantic_reference_values, (list, tuple)) or any(
        not isinstance(item, CognitiveReferenceSemanticV1) for item in request.semantic_reference_values
    ):
        errors.append("semantic_reference_values_invalid_shape")
    if not isinstance(request.relation_interpretation_candidates, (list, tuple)) or any(
        not isinstance(item, CognitiveRelationInterpretationCandidateV1)
        for item in request.relation_interpretation_candidates
    ):
        errors.append("relation_interpretation_candidates_invalid_shape")
    for name in ("requirement_establishment_status", "execution_mode"):
        if not isinstance(getattr(request, name), str) or not getattr(request, name).strip():
            errors.append(f"{name}_invalid_field_type")
    for name in ("synthetic_only", "candidate_only"):
        if not isinstance(getattr(request, name), bool):
            errors.append(f"{name}_invalid_field_type")
    return tuple(dict.fromkeys(errors))


def validate_no_field_mutation(world: CurrentWorldCandidateV1) -> bool:
    return (
        world.field_mutation is False
        and world.field_entity_creation is False
        and world.field_confidence_mutation is False
        and world.field_transition is False
        and world.event_admission is False
        and world.reducer_invocation_as_mutation_authority is False
        and world.field_truth_declaration is False
    )


def validate_current_world_candidate_only(world: CurrentWorldCandidateV1) -> bool:
    return (
        world.candidate_only is True
        and world.world_state_kind_candidate in WORLD_STATE_KINDS
    )


def validate_immutable_snapshot_mappings(world: CurrentWorldCandidateV1) -> bool:
    return (
        isinstance(world.source_versions, tuple)
        and all(
            isinstance(item, tuple)
            and len(item) == 2
            and isinstance(item[0], str)
            and bool(item[0].strip())
            and isinstance(item[1], str)
            and bool(item[1].strip())
            for item in world.source_versions
        )
        and len({item[0] for item in world.source_versions}) == len(world.source_versions)
    )


def validate_immutable_reverse_lookup(value: object) -> bool:
    return (
        isinstance(value, tuple)
        and all(
            isinstance(item, tuple)
            and len(item) == 2
            and isinstance(item[0], str)
            and bool(item[0].strip())
            and isinstance(item[1], tuple)
            and all(isinstance(ref, str) and bool(ref.strip()) for ref in item[1])
            for item in value
        )
        and len({item[0] for item in value}) == len(value)
    )


def validate_field_ref_read_only_boundary(field_refs: Iterable[SourceRefV1]) -> bool:
    return validate_field_ref_read_only(field_refs)


def validate_attention_boundary(items: Sequence[AttentionCandidateV1]) -> bool:
    return all(
        item.candidate_only is True
        and item.decision_priority is False
        and item.action_priority is False
        and item.score_semantics == "candidate_heuristic"
        for item in items
    )


def validate_hypothesis_boundary(
    items: Sequence[CognitiveHypothesisCandidateV1],
) -> bool:
    return all(
        item.candidate_only is True
        and item.causal_truth is False
        and item.decision_output is False
        and item.action_output is False
        and item.state in HYPOTHESIS_STATES
        for item in items
    )


def validate_hypothesis_competition_boundary(
    result: HypothesisCompetitionResultV1,
) -> bool:
    return result.candidate_only is True and result.single_truth_collapsed is False


def validate_causal_handoff_boundary(
    handoff: CognitiveToCausalHandoffCandidateV1,
) -> bool:
    return (
        handoff.candidate_only is True
        and handoff.handoff_type == "CANDIDATE_REFERENCE_ONLY"
        and handoff.causal_truth is False
        and handoff.causal_accepted_state is False
        and handoff.decision_output is False
        and handoff.action_output is False
        and handoff.task_output is False
        and handoff.runtime_command is False
    )


def validate_negative_guard_status(guard: NegativeGuardStatusV1) -> bool:
    return (
        guard.candidate_only is True
        and guard.context_mutation is NEGATIVE_GUARDS["context_mutation"]
        and guard.pcn_mutation is NEGATIVE_GUARDS["pcn_mutation"]
        and guard.intent_mutation is NEGATIVE_GUARDS["intent_mutation"]
        and guard.field_mutation is NEGATIVE_GUARDS["field_mutation"]
        and guard.causal_mutation is NEGATIVE_GUARDS["causal_mutation"]
        and guard.decision_output is NEGATIVE_GUARDS["decision_output"]
        and guard.action_output is NEGATIVE_GUARDS["action_output"]
        and guard.task_output is NEGATIVE_GUARDS["task_output"]
        and guard.database_write is NEGATIVE_GUARDS["database_write"]
        and guard.device_control is NEGATIVE_GUARDS["device_control"]
        and guard.scheduler_execution is NEGATIVE_GUARDS["scheduler_execution"]
        and guard.runtime_side_effect is NEGATIVE_GUARDS["runtime_side_effect"]
        and guard.model_call is NEGATIVE_GUARDS["model_call"]
        and guard.learning_update is NEGATIVE_GUARDS["learning_update"]
        and guard.self_regulation_update is NEGATIVE_GUARDS["self_regulation_update"]
        and guard.dynamic_parameter_mutation
        is NEGATIVE_GUARDS["dynamic_parameter_mutation"]
        and guard.single_truth_collapse is NEGATIVE_GUARDS["single_truth_collapse"]
    )


def validate_output_contract(
    output: CognitiveStateFormationOutputV1,
    all_refs: Iterable[SourceRefV1],
) -> bool:
    return (
        output.candidate_only is True
        and output.source_mutation_executed is False
        and output.semantic_owner_ref == "A_REASONING_ROLE"
        and output.semantic_projection_only is True
        and output.semantic_authority is False
        and output.formation_role == "SNAPSHOT_FORMATION"
        and validate_ref_read_only(all_refs)
        and validate_no_owner_transfer(all_refs)
        and validate_attention_boundary(output.attention_candidates)
        and validate_hypothesis_boundary(output.cognitive_hypotheses)
        and validate_hypothesis_competition_boundary(
            output.hypothesis_competition_result
        )
        and validate_current_world_candidate_only(output.current_world_candidate)
        and validate_immutable_snapshot_mappings(output.current_world_candidate)
        and validate_immutable_reverse_lookup(output.provenance.reverse_lookup)
        and validate_no_field_mutation(output.current_world_candidate)
        and validate_causal_handoff_boundary(output.causal_handoff_candidate)
        and validate_negative_guard_status(output.negative_guard_status)
        and output.execution_mode in {SYNTHETIC_CONTROLLED, CONTROLLED_REPLAY_RUNTIME, LIVE_RUNTIME}
        and (
            (
                output.execution_mode == SYNTHETIC_CONTROLLED
                and output.runtime_executed is False
                and not output.cognitive_transition_refs
            )
            or (
                output.execution_mode == CONTROLLED_REPLAY_RUNTIME
                and output.runtime_executed is True
                and bool(output.execution_ref)
                and bool(output.cognitive_transition_refs)
                and output.execution_owner_ref == "Cognitive State Formation Governance"
            )
            or (
                output.execution_mode == LIVE_RUNTIME
                and output.runtime_executed is True
                and bool(output.execution_ref)
                and bool(output.cognitive_transition_refs)
                and output.execution_owner_ref == "Cognitive State Formation Governance"
            )
        )
        and (
            (
                output.execution_mode == SYNTHETIC_CONTROLLED
                and not validate_cognitive_loop_candidates_v1(
                    sufficiency=output.sufficiency_candidate,
                    information_gap=output.information_gap_candidate,
                    reobservation=output.reobservation_candidate,
                    hypothesis_revision=output.hypothesis_revision_candidate,
                    stop=output.stop_candidate,
                )
            )
            or (
                output.execution_mode in {CONTROLLED_REPLAY_RUNTIME, LIVE_RUNTIME}
                and output.sufficiency_candidate is None
                and output.information_gap_candidate is None
                and output.reobservation_candidate is None
                and output.hypothesis_revision_candidate is None
                and output.stop_candidate is None
                and output.next_cycle_ingress_ref is None
            )
        )
    )
