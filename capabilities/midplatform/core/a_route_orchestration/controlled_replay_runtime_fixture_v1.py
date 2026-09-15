"""One canonical controlled-replay input for A-Route runtime verification."""

from __future__ import annotations

from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    ControlledReplayInputV1,
)
from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import GoalContextV1
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_engine_v1 import (
    ARouteRequiredCognitiveConditionFormationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
    ARouteRequiredCognitiveConditionFormationRequestV1,
    CurrentCognitiveSituationV1,
    GovernedObjectiveConditionRuleV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_loop_types_v1 import (
    CognitiveInformationGapCandidateV1,
    CognitiveReobservationCandidateV1,
    CognitiveSufficiencyCandidateV1,
    requirement_establishment_from_condition_formation_status_v1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    ObservationIngressRequestV1,
)


def _canonical_establishment_proof(
    *,
    case_id: str,
    required_information_refs: tuple[str, ...],
    available_information_refs: tuple[str, ...],
):
    goal_ref = f"goal:controlled-replay:{case_id}"
    rules = (
        GovernedObjectiveConditionRuleV1(
            rule_ref=f"rule:controlled-replay:{case_id}:v1",
            condition_ref=f"condition:controlled-replay:{case_id}:v1",
            objective_refs=(goal_ref,),
            satisfaction_coverage_refs=required_information_refs,
            source_refs=(f"governance:controlled-replay:{case_id}:v1",),
            provenance_refs=(f"provenance:controlled-replay:{case_id}:v1",),
        ),
    ) if required_information_refs else ()
    return ARouteRequiredCognitiveConditionFormationEngineV1().form(
        ARouteRequiredCognitiveConditionFormationRequestV1(
            goal_context=GoalContextV1(
                goal_ref=goal_ref,
                primary_goal=goal_ref,
                secondary_goal_refs=(),
                success_condition_refs=(),
                stop_condition_refs=(),
                provenance={"source": "controlled-replay-fixture"},
                trace=f"trace:controlled-replay:{case_id}:v1",
            ),
            governed_condition_rules=rules,
            current_situation=CurrentCognitiveSituationV1(
                current_cognitive_coverage_refs=available_information_refs,
            ),
            formation_trace_ref=f"trace:controlled-replay:required-conditions:{case_id}:v1",
        )
    )


def build_controlled_replay_input_v1() -> ControlledReplayInputV1:
    proof = _canonical_establishment_proof(
        case_id="obvious-target",
        required_information_refs=(),
        available_information_refs=(),
    )
    return ControlledReplayInputV1(
        replay_input_ref="replay-input:controlled-fixture:level1:obvious-target:v1",
        replay_version="v1",
        origin_class="CONTROLLED_RECORDED_FIXTURE",
        source_ref="controlled-recorded-fixture:level1:obvious-target",
        evidence_refs=("evidence:controlled-replay:obvious-target:1",),
        provenance_refs=(
            "provenance:controlled-recorded-fixture:v1",
            "source-version:controlled-recorded-fixture:v1",
        ),
        ordering_refs=("order:controlled-replay:obvious-target:0001",),
        required_cognitive_condition_formation_result=proof,
    )


def build_controlled_replay_gateway_request_v1() -> ObservationIngressRequestV1:
    replay = build_controlled_replay_input_v1()
    return ObservationIngressRequestV1(
        scenario_id="S01",
        ingress_type="VISION",
        provider_ref="recorded-evidence-origin:controlled-fixture",
        source_ref=replay.source_ref,
        payload_ref=replay.replay_input_ref,
        temporal_ref="recorded-time:controlled-replay:0001",
        observed_at="recorded-time:controlled-replay:0001",
        valid_from_candidate="recorded-time:controlled-replay:0001",
        confidence_candidate=0.8,
        quality_candidate=0.8,
        sensitivity="NORMAL",
        source_model_ref=None,
        evidence_refs=replay.evidence_refs,
        routing_targets=("Context", "A Route Orchestration"),
        execution_mode=CONTROLLED_REPLAY_RUNTIME,
        replay_input=replay,
        synthetic_only=False,
        controlled_integration_only=True,
        candidate_only=True,
    )


def build_minimum_sufficient_loop_replay_input_v1(
    *,
    case_id: str,
    cycle_index: int,
    evidence_refs: tuple[str, ...],
    available_information_refs: tuple[str, ...],
    prior_current_world_ref: str | None = None,
    prior_hypothesis_refs: tuple[str, ...] = (),
    prior_information_gap_ref: str | None = None,
    prior_reobservation_ref: str | None = None,
    prior_next_cycle_ingress_ref: str | None = None,
    prior_sufficiency_candidate: CognitiveSufficiencyCandidateV1 | None = None,
    prior_information_gap_candidate: CognitiveInformationGapCandidateV1 | None = None,
    prior_reobservation_candidate: CognitiveReobservationCandidateV1 | None = None,
) -> ControlledReplayInputV1:
    proof = _canonical_establishment_proof(
        case_id=case_id,
        required_information_refs=("information:target-identity", "information:target-location"),
        available_information_refs=available_information_refs,
    )
    establishment_status, establishment_basis = requirement_establishment_from_condition_formation_status_v1(
        proof.status
    )
    return ControlledReplayInputV1(
        replay_input_ref=f"replay-input:controlled-fixture:{case_id}:cycle-{cycle_index}:v1",
        replay_version="v1",
        origin_class="CONTROLLED_RECORDED_FIXTURE",
        source_ref=f"controlled-recorded-fixture:minimum-sufficient-loop:{case_id}",
        evidence_refs=evidence_refs,
        provenance_refs=(
            "provenance:controlled-recorded-fixture:minimum-sufficient-loop:v1",
            f"source-version:controlled-recorded-fixture:{case_id}:v1",
        ),
        ordering_refs=tuple(f"order:{case_id}:cycle-{cycle_index}:{index:04d}" for index, _ in enumerate(evidence_refs, start=1)),
        cycle_index=cycle_index,
        required_information_refs=("information:target-identity", "information:target-location"),
        available_information_refs=available_information_refs,
        requirement_establishment_status=establishment_status,
        requirement_establishment_ref=proof.trace_ref,
        requirement_establishment_basis=establishment_basis,
        required_cognitive_condition_formation_result=proof,
        prior_current_world_ref=prior_current_world_ref,
        prior_hypothesis_refs=prior_hypothesis_refs,
        prior_information_gap_ref=prior_information_gap_ref,
        prior_reobservation_ref=prior_reobservation_ref,
        prior_next_cycle_ingress_ref=prior_next_cycle_ingress_ref,
        prior_sufficiency_candidate=prior_sufficiency_candidate,
        prior_information_gap_candidate=prior_information_gap_candidate,
        prior_reobservation_candidate=prior_reobservation_candidate,
    )


def build_minimum_sufficient_loop_gateway_request_v1(
    *,
    scenario_id: str,
    replay: ControlledReplayInputV1,
    execution_identity_ref: str | None = None,
) -> ObservationIngressRequestV1:
    return ObservationIngressRequestV1(
        scenario_id=scenario_id,
        ingress_type="VISION",
        provider_ref="recorded-evidence-origin:controlled-fixture",
        source_ref=replay.source_ref,
        payload_ref=replay.replay_input_ref,
        temporal_ref=f"recorded-time:minimum-sufficient-loop:{replay.cycle_index:04d}",
        observed_at=f"recorded-time:minimum-sufficient-loop:{replay.cycle_index:04d}",
        valid_from_candidate=f"recorded-time:minimum-sufficient-loop:{replay.cycle_index:04d}",
        confidence_candidate=0.8,
        quality_candidate=0.8,
        sensitivity="NORMAL",
        source_model_ref=None,
        evidence_refs=replay.evidence_refs,
        routing_targets=("Context", "A Route Orchestration"),
        execution_mode=CONTROLLED_REPLAY_RUNTIME,
        execution_identity_ref=execution_identity_ref,
        replay_input=replay,
        synthetic_only=False,
        controlled_integration_only=True,
        candidate_only=True,
    )
