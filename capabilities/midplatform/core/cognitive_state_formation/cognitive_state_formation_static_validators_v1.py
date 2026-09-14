"""Static validators for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from typing import Iterable, Sequence

from capabilities.midplatform.core.cognitive_state_formation.attention_types_v1 import (
    AttentionCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_hypothesis_types_v1 import (
    CognitiveHypothesisCandidateV1,
    HypothesisCompetitionResultV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    NegativeGuardStatusV1,
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_handoff_types_v1 import (
    CognitiveToCausalHandoffCandidateV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationOutputV1,
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
        and validate_ref_read_only(all_refs)
        and validate_no_owner_transfer(all_refs)
        and validate_attention_boundary(output.attention_candidates)
        and validate_hypothesis_boundary(output.cognitive_hypotheses)
        and validate_hypothesis_competition_boundary(
            output.hypothesis_competition_result
        )
        and validate_current_world_candidate_only(output.current_world_candidate)
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
            output.execution_mode == SYNTHETIC_CONTROLLED
            or not validate_cognitive_loop_candidates_v1(
                sufficiency=output.sufficiency_candidate,
                information_gap=output.information_gap_candidate,
                reobservation=output.reobservation_candidate,
                hypothesis_revision=output.hypothesis_revision_candidate,
                stop=output.stop_candidate,
            )
        )
    )
