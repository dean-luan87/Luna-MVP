from __future__ import annotations

from dataclasses import replace

from capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.fixtures_v1 import (
    build_replay_inputs_v1,
    get_contrast_specs_v1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteCognitiveExecutionEvidenceV1,
    ARouteIngressRefsV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)


def test_aroute_private_proof_builder_preserves_canonical_boundary(monkeypatch) -> None:
    spec = next(item for item in get_contrast_specs_v1() if item.contrast_id == "role-owner")
    gateway_request, route_request = build_replay_inputs_v1(spec)
    gateway = ObservationGatewayEngineV1().run_case(gateway_request)
    route_request = replace(
        route_request,
        ingress=ARouteIngressRefsV1(
            observation_refs=(gateway.observation.observation_id,),
            perception_refs=tuple(item.evidence_id for item in gateway.evidence),
            field_refs=route_request.ingress.field_refs,
            relation_refs=route_request.ingress.relation_refs,
        ),
        replay_admission=gateway.replay_admission,
    )

    original_builder = ARouteOrchestrationEngineV1._build_cognitive_execution_evidence
    captured = {}
    input_reprs_before = {}

    def capture_builder(**kwargs):
        captured.update(kwargs)
        if not input_reprs_before:
            input_reprs_before.update(
                {
                    name: repr(kwargs[name])
                    for name in (
                        "admission",
                        "normalized_information",
                        "state_request",
                        "state_output",
                        "a_judgment",
                    )
                }
            )
        return original_builder(**kwargs)

    monkeypatch.setattr(
        ARouteOrchestrationEngineV1,
        "_build_cognitive_execution_evidence",
        staticmethod(capture_builder),
    )

    route = ARouteOrchestrationEngineV1().run_case(route_request)
    proof = route.cognitive_execution

    assert not route.errors
    assert isinstance(proof, ARouteCognitiveExecutionEvidenceV1)
    assert proof.execution_ref == captured["execution_ref"]
    assert proof.execution_mode == captured["execution_mode"]
    assert proof.ingress_refs == captured["ingress_refs"]

    admission = captured["admission"]
    state_output = captured["state_output"]
    a_judgment = captured["a_judgment"]

    assert proof.canonical_gateway_admission_result is admission
    assert proof.evidence_binding is admission.evidence_binding
    assert proof.cognitive_semantic_judgment is a_judgment
    assert proof.relation_interpretation_semantic_candidates is state_output.relation_interpretation_candidates

    assert proof.sufficiency_ref == a_judgment.sufficiency_ref
    assert proof.information_gap_ref == a_judgment.information_gap_ref
    assert proof.reobservation_ref == a_judgment.reobservation_ref
    assert proof.hypothesis_revision_ref == a_judgment.reconsideration_ref
    assert proof.stop_ref == a_judgment.local_disposition_ref
    assert proof.semantic_owner_ref == "A_REASONING_ROLE"
    assert proof.semantic_judgment_ref == a_judgment.judgment_ref
    assert proof.semantic_provenance_refs == a_judgment.provenance_refs

    assert proof.candidate_only is True
    assert proof.field_mutation is False
    assert proof.world_truth_declared is False
    assert proof.model_invocation is False
    assert proof.provider_invocation is False
    assert proof.live_observation_execution is False
    assert proof.action_execution is False

    repeated = original_builder(**captured)
    assert repeated == proof
    assert captured["admission"] is admission
    assert captured["state_output"] is state_output
    assert captured["a_judgment"] is a_judgment
    assert {
        name: repr(captured[name])
        for name in input_reprs_before
    } == input_reprs_before
