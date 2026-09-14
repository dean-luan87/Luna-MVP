"""Controlled provider-output-shaped fixtures; no provider is invoked."""

from __future__ import annotations

from dataclasses import replace
from typing import Tuple

from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    RuntimeObservationEnvelopeV1,
)

from .types_v1 import RuntimeObservationIngressCaseV1


def _observation(
    execution_ref: str,
    modality: str,
    provider_ref: str,
    capability_ref: str,
    raw_result_ref: str,
    *,
    spatial_refs: Tuple[str, ...] = (),
) -> RuntimeObservationEnvelopeV1:
    return RuntimeObservationEnvelopeV1(
        observation_id=f"runtime-observation:{execution_ref}",
        execution_instance_ref=execution_ref,
        provider_ref=provider_ref,
        capability_ref=capability_ref,
        modality=modality,
        source_ref=f"runtime-source:{execution_ref}",
        raw_result_ref=raw_result_ref,
        temporal_ref=f"temporal:{execution_ref}",
        observed_at="2026-08-31T00:00:00Z",
        provenance_refs=(f"provider-provenance:{execution_ref}",),
        trace_refs=(f"provider-trace:{execution_ref}",),
        confidence_candidate=0.86,
        quality_candidate=0.82,
        spatial_refs=spatial_refs,
    )


def build_runtime_observation_cases_v1() -> Tuple[RuntimeObservationIngressCaseV1, ...]:
    return (
        RuntimeObservationIngressCaseV1(
            case_id="REAL_RUNTIME_VISION_OBJECT",
            title="vision object provider result enters Gateway",
            observation=_observation(
                "runtime-vision-object",
                "VISION",
                "provider:vision:runtime-result",
                "capability:vision-object-detection",
                "provider-output:vision:object-candidate",
            ),
            context_ref="context:runtime:office",
            pcn_ref="pcn:runtime:office",
            intent_ref="intent:runtime:locate-document",
            role_refs=("role:workspace-owner",),
            task_refs=("task:find-document",),
            goal_refs=("goal:locate-document",),
            concern_refs=("concern:document-location",),
            information_need_refs=("need:document-location",),
            field_refs=("field:office:physical-v1",),
            relation_refs=("relation:desk-document-private",),
            required_information_refs=("need:document-location",),
            available_information_refs=("need:document-location",),
        ),
        RuntimeObservationIngressCaseV1(
            case_id="REAL_RUNTIME_OCR_TEXT",
            title="OCR text provider result enters Gateway",
            observation=_observation(
                "runtime-ocr-text",
                "OCR",
                "provider:ocr:runtime-result",
                "capability:ocr-text-recognition",
                "provider-output:ocr:document-text",
            ),
            context_ref="context:runtime:office",
            pcn_ref="pcn:runtime:office",
            intent_ref="intent:runtime:read-document",
            role_refs=("role:workspace-owner",),
            task_refs=("task:find-document",),
            goal_refs=("goal:locate-document",),
            concern_refs=("concern:document-location",),
            information_need_refs=("need:document-location",),
            field_refs=("field:office:physical-v1",),
            relation_refs=("relation:desk-document-private",),
            required_information_refs=("need:document-location",),
            available_information_refs=("need:document-location",),
        ),
        RuntimeObservationIngressCaseV1(
            case_id="REAL_RUNTIME_SLAM_REFERENCE",
            title="SLAM spatial reference enters Gateway",
            observation=_observation(
                "runtime-slam-reference",
                "SLAM_SPATIAL",
                "provider:slam:runtime-result",
                "capability:slam-spatial-mapping",
                "provider-output:slam:exit-geometry",
                spatial_refs=("spatial-reference:exit-geometry",),
            ),
            context_ref="context:runtime:office",
            pcn_ref="pcn:runtime:office",
            intent_ref="intent:runtime:locate-exit",
            role_refs=("role:visitor",),
            task_refs=("task:identify-exit",),
            goal_refs=("goal:locate-exit",),
            concern_refs=("concern:exit-location",),
            information_need_refs=("need:exit-location",),
            field_refs=("field:office:physical-v1",),
            relation_refs=("relation:door-shared-exit",),
            required_information_refs=("need:exit-location",),
            available_information_refs=("need:exit-location",),
        ),
    )


def malformed_runtime_observation_case_v1() -> RuntimeObservationIngressCaseV1:
    case = build_runtime_observation_cases_v1()[0]
    return replace(case, case_id="MALFORMED_RUNTIME_OBSERVATION", observation=replace(case.observation, capability_ref=""))


def unavailable_provider_case_v1() -> RuntimeObservationIngressCaseV1:
    case = build_runtime_observation_cases_v1()[0]
    return replace(case, case_id="PROVIDER_UNAVAILABLE", observation=replace(case.observation, provider_available=False, result_status="UNAVAILABLE"))


def missing_information_case_v1() -> RuntimeObservationIngressCaseV1:
    case = build_runtime_observation_cases_v1()[0]
    return replace(
        case,
        case_id="MISSING_REQUIRED_INFORMATION",
        information_need_refs=("need:document-location", "need:document-operational-state"),
        required_information_refs=("need:document-location", "need:document-operational-state"),
        available_information_refs=("need:document-location",),
    )
