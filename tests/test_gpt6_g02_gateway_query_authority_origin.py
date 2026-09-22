"""Positive regression for the GPT6-G02 Gateway query-origin boundary."""

from dataclasses import asdict

from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.brain_cognitive_loop_closure_assimilation_engine_v1 import (
    run_brain_cognitive_case_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_result_to_decision_governance_controlled_handoff.engine_v1 import (
    build_cognitive_decision_handoff_candidate_v1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    GatewayAdmissionStateRecordV1,
    ObservationGatewayAdmissionQueryV1,
)


class CallerControlledGatewayQuery(ObservationGatewayAdmissionQueryV1):
    """A caller-owned query that fabricates the expected read results."""

    __slots__ = ("_record",)

    def __init__(self, record: GatewayAdmissionStateRecordV1) -> None:
        super().__init__()
        self._record = record

    def lookup(
        self,
        execution_identity_ref: str,
        gateway_admission_ref: str,
    ) -> GatewayAdmissionStateRecordV1:
        return self._record

    def matches_canonical_admission(
        self,
        execution_identity_ref: str,
        gateway_admission_ref: str,
        admission: object,
    ) -> bool:
        return True


def test_decision_handoff_rejects_caller_controlled_query_origin() -> None:
    typed_case = run_brain_cognitive_case_v1(
        "CASE_A_SUFFICIENT_STOP", "gpt6-g02"
    )
    proof = typed_case.cognitive_proofs[-1]
    case = asdict(typed_case)
    case["gateway_results"] = typed_case.gateway_results
    case["gateway_execution_identity_ref"] = proof.gateway_execution_identity_ref
    case["gateway_admission_queries"] = (
        CallerControlledGatewayQuery(
            GatewayAdmissionStateRecordV1(
                execution_identity_ref=proof.gateway_execution_identity_ref,
                gateway_admission_ref=proof.gateway_admission_ref,
                evidence_refs=tuple(proof.admitted_evidence_refs),
            )
        ),
    )

    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, proof)

    assert handoff is None
    assert errors == ("decision_handoff_requires_gateway_admission_query",)

    case["gateway_admission_queries"] = typed_case.gateway_admission_queries
    owner_handoff, owner_errors = build_cognitive_decision_handoff_candidate_v1(
        case, proof
    )
    assert owner_errors == ()
    assert owner_handoff is not None
