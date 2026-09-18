"""Regression protection for GPT6-G03 Gateway admission deep immutability."""

from dataclasses import replace

from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_runtime_ingress.adapters_v1 import (
    build_gateway_request,
)
from capabilities.midplatform.core.observation_runtime_ingress.fixtures_v1 import (
    build_runtime_observation_cases_v1,
)


def test_live_admission_does_not_retain_caller_owned_nested_reference() -> None:
    case = build_runtime_observation_cases_v1()[0]
    caller_owned_refs = [
        ["evidence-information:caller-owned", ["information:before"]],
    ]
    request = replace(
        build_gateway_request(case),
        evidence_information_refs=caller_owned_refs,
    )

    gateway = ObservationGatewayEngineV1()
    result = gateway.run_case(request)
    admission = result.runtime_admission

    assert result.admission_state == "ADMITTED_OBSERVATION"
    assert admission is not None
    admission_ref = admission.gateway_admission_ref
    execution_ref = admission.execution_instance_ref
    canonical_before = admission.evidence_information_refs
    assert canonical_before == (
        ("evidence-information:caller-owned", ("information:before",)),
    )
    assert admission.evidence_information_refs is not caller_owned_refs
    assert admission.evidence_information_refs[0][1] is not caller_owned_refs[0][1]
    assert gateway.admission_query.lookup(execution_ref, admission_ref) is not None
    assert gateway.admission_query.matches_canonical_admission(
        execution_ref,
        admission_ref,
        admission,
    )

    caller_owned_refs[0][1].append("information:after")

    assert admission.evidence_information_refs == canonical_before
    assert admission.evidence_information_refs[0][1] == ("information:before",)
    assert gateway.admission_query.matches_canonical_admission(
        execution_ref,
        admission_ref,
        admission,
    )
