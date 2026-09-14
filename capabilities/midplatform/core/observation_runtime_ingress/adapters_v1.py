"""Small adapter from provider output envelopes to canonical Gateway/A-Route inputs."""

from __future__ import annotations

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteIngressRefsV1,
    ARouteOrchestrationRequestV1,
)
from capabilities.midplatform.core.execution_mode_v1 import LIVE_RUNTIME
from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    ObservationGatewayResultV1,
    ObservationIngressRequestV1,
)

from .types_v1 import RuntimeObservationIngressCaseV1


def build_gateway_request(case: RuntimeObservationIngressCaseV1) -> ObservationIngressRequestV1:
    observation = case.observation
    observed_at = observation.observed_at
    return ObservationIngressRequestV1(
        scenario_id=case.case_id,
        ingress_type=observation.modality,
        provider_ref=observation.provider_ref,
        source_ref=observation.source_ref,
        payload_ref=observation.raw_result_ref,
        temporal_ref=observation.temporal_ref,
        observed_at=observed_at,
        valid_from_candidate=observed_at,
        confidence_candidate=observation.confidence_candidate if observation.confidence_candidate is not None else 0.0,
        quality_candidate=observation.quality_candidate if observation.quality_candidate is not None else 0.0,
        source_model_ref=observation.source_model_ref,
        source_region_ref=observation.source_region_ref,
        evidence_refs=(f"evidence:{observation.execution_instance_ref}:1",),
        spatial_refs=observation.spatial_refs,
        routing_targets=("A Route Orchestration",),
        route_to_orchestration=case.route_to_orchestration,
        synthetic_only=case.synthetic_only,
        controlled_integration_only=case.controlled_integration_only,
        candidate_only=case.candidate_only,
        execution_mode=LIVE_RUNTIME,
        execution_identity_ref=observation.execution_instance_ref,
        runtime_observation=observation,
        required_information_refs=case.required_information_refs,
        available_information_refs=case.available_information_refs,
        evidence_information_refs=case.evidence_information_refs,
        inherited_information_refs=case.inherited_information_refs,
        cycle_index=case.cycle_index,
        prior_current_world_ref=case.prior_current_world_ref,
        prior_hypothesis_refs=case.prior_hypothesis_refs,
        prior_information_gap_ref=case.prior_information_gap_ref,
        prior_reobservation_ref=case.prior_reobservation_ref,
        prior_next_cycle_ingress_ref=case.prior_next_cycle_ingress_ref,
        prior_sufficiency_candidate=case.prior_sufficiency_candidate,
        prior_information_gap_candidate=case.prior_information_gap_candidate,
        prior_reobservation_candidate=case.prior_reobservation_candidate,
    )


def build_aroute_request(
    case: RuntimeObservationIngressCaseV1,
    gateway: ObservationGatewayResultV1,
) -> ARouteOrchestrationRequestV1:
    observation = gateway.observation
    admission = gateway.runtime_admission
    return ARouteOrchestrationRequestV1(
        scenario_id=case.case_id,
        ingress=ARouteIngressRefsV1(
            observation_refs=(observation.observation_id,) if observation else (),
            perception_refs=tuple(item.evidence_id for item in gateway.evidence),
            field_refs=case.field_refs,
            relation_refs=case.relation_refs,
        ),
        context_ref=case.context_ref,
        pcn_ref=case.pcn_ref,
        intent_ref=case.intent_ref,
        execution_mode=LIVE_RUNTIME,
        execution_identity_ref=case.observation.execution_instance_ref,
        runtime_admission=admission,
        role_refs=case.role_refs,
        task_refs=case.task_refs,
        goal_refs=case.goal_refs,
        concern_refs=case.concern_refs,
        information_need_refs=case.information_need_refs,
        synthetic_only=case.synthetic_only,
        candidate_only=case.candidate_only,
    )
