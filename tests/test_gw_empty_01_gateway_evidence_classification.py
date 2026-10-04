"""GW-EMPTY-01: empty result state must not erase modality semantics."""

from dataclasses import replace
from types import SimpleNamespace

from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_runtime_ingress.adapters_v1 import (
    build_gateway_request,
)
from capabilities.midplatform.core.observation_runtime_ingress.fixtures_v1 import (
    build_runtime_observation_cases_v1,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.provider_result_adapter_v1 import (
    provider_result_to_runtime_observation,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.real_provider_execution_engine_v1 import (
    _provider_result,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.types_v1 import (
    ProviderRuntimeRequestV1,
)


def _gateway_evidence(modality: str, *, empty: bool):
    cases = build_runtime_observation_cases_v1()
    case = next(item for item in cases if item.observation.modality == modality)
    observation = replace(
        case.observation,
        empty_result=empty,
        output_candidate=None if empty else {"candidate_ref": "provider-local:candidate"},
    )
    result = ObservationGatewayEngineV1().run_case(
        build_gateway_request(replace(case, observation=observation))
    )
    assert result.admission_state == "ADMITTED_OBSERVATION"
    assert len(result.evidence) == 1
    return result.evidence[0]


def test_ocr_empty_retains_historical_evidence_type() -> None:
    evidence = _gateway_evidence("OCR", empty=True)
    assert evidence.evidence_type == "ocr_empty_success"
    assert evidence.empty_result is True
    assert evidence.candidate_payload is None


def test_vision_empty_retains_vision_type_and_separate_result_state() -> None:
    evidence = _gateway_evidence("VISION", empty=True)
    assert evidence.evidence_type == "visual_detection_evidence"
    assert evidence.evidence_type != "ocr_empty_success"
    assert evidence.empty_result is True
    assert evidence.candidate_payload is None


def test_vision_nonempty_classification_is_unchanged() -> None:
    evidence = _gateway_evidence("VISION", empty=False)
    assert evidence.evidence_type == "visual_detection_evidence"
    assert evidence.empty_result is False


def test_ocr_nonempty_classification_is_unchanged() -> None:
    evidence = _gateway_evidence("OCR", empty=False)
    assert evidence.evidence_type == "ocr_text_evidence"
    assert evidence.empty_result is False


def test_yolo_zero_detections_follow_existing_provider_result_adapter() -> None:
    request = ProviderRuntimeRequestV1(
        provider_request_ref="request:yolo:empty",
        observation_demand_ref="demand:yolo:empty",
        observation_request_ref="observation-request:yolo:empty",
        capability_requirement_ref="requirement:vision-detection",
        capability_ref="capability:vision-object-detection",
        provider_ref="provider:yolo:local:v1",
        model_ref="model:yolo11n",
        execution_instance_ref="execution:yolo:empty",
        input_source_ref="image:yolo:empty",
        modality="VISION",
        temporal_ref="2026-08-31T00:00:00Z",
        spatial_refs=(),
        trace_refs=("trace:yolo:request",),
        provenance_refs=("provenance:yolo:request",),
    )
    native = SimpleNamespace(
        accepted=True,
        detections=(),
        trace_ref="trace:yolo:provider",
        error_code=None,
        provenance_refs=("provenance:yolo:provider",),
        invocation_performed=False,
    )
    result = _provider_result(request, native)
    assert result.status == "EMPTY_SUCCESS"
    assert result.empty_result is True
    observation, errors = provider_result_to_runtime_observation(request, result)
    assert errors == ()
    assert observation is not None

    vision_case = next(
        item for item in build_runtime_observation_cases_v1()
        if item.observation.modality == "VISION"
    )
    gateway_result = ObservationGatewayEngineV1().run_case(
        build_gateway_request(replace(vision_case, observation=observation))
    )
    assert gateway_result.admission_state == "ADMITTED_OBSERVATION"
    assert len(gateway_result.evidence) == 1
    evidence = gateway_result.evidence[0]
    assert evidence.evidence_type == "visual_detection_evidence"
    assert evidence.empty_result is True
    assert evidence.evidence_type != "ocr_empty_success"
