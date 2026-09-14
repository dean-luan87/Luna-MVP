"""Recorded provider-result fixtures for the provider-to-ingress bridge."""

from __future__ import annotations

from dataclasses import replace
from typing import Tuple

from .types_v1 import ProviderObservationIngressCaseV1, ProviderRuntimeResultV1


def build_provider_observation_cases_v1() -> Tuple[ProviderObservationIngressCaseV1, ...]:
    return (
        ProviderObservationIngressCaseV1(
            case_id="VISION_PROVIDER_RESULT_TO_COGNITION",
            title="recorded vision result enters the canonical cognition path",
            capability_kind="VISION_DETECTION",
            capability_ref="object_detection",
            modality="VISION",
            input_source_ref="source:runtime:image-frame-001",
            execution_instance_ref="provider-runtime:vision-001",
            information_need_ref="need:document-location",
            required_information_refs=("need:document-location",),
            available_information_refs=("need:document-location",),
            context_ref="context:runtime:office",
            intent_ref="intent:runtime:locate-document",
            task_ref="task:find-document",
            goal_ref="goal:locate-document",
            concern_ref="concern:document-location",
            role_refs=("role:workspace-owner",),
            field_refs=("field:office:physical-v1",),
            relation_refs=("relation:desk-document-private",),
            source_ref="source:runtime:image-frame-001",
            raw_result_ref="provider-output:detection_v1:vision-001",
            expected_evidence_kinds=("object_candidate",),
            temporal_ref="time:runtime:vision-001",
        ),
        ProviderObservationIngressCaseV1(
            case_id="OCR_PROVIDER_RESULT_TO_COGNITION",
            title="recorded OCR result enters the canonical cognition path",
            capability_kind="OCR_TEXT_EVIDENCE",
            capability_ref="text_recognition",
            modality="OCR",
            input_source_ref="source:runtime:image-frame-002",
            execution_instance_ref="provider-runtime:ocr-001",
            information_need_ref="need:document-location",
            required_information_refs=("need:document-location",),
            available_information_refs=("need:document-location",),
            context_ref="context:runtime:office",
            intent_ref="intent:runtime:read-document",
            task_ref="task:find-document",
            goal_ref="goal:locate-document",
            concern_ref="concern:document-location",
            role_refs=("role:workspace-owner",),
            field_refs=("field:office:physical-v1",),
            relation_refs=("relation:desk-document-private",),
            source_ref="source:runtime:image-frame-002",
            raw_result_ref="provider-output:ocr_v1:ocr-001",
            expected_evidence_kinds=("text_candidate",),
            temporal_ref="time:runtime:ocr-001",
        ),
        ProviderObservationIngressCaseV1(
            case_id="SLAM_PROVIDER_RESULT_TO_COGNITION",
            title="recorded spatial result enters the canonical cognition path",
            capability_kind="SLAM_SPATIAL_EVIDENCE",
            capability_ref="spatial_mapping",
            modality="SLAM_SPATIAL",
            input_source_ref="source:runtime:pose-stream-001",
            execution_instance_ref="provider-runtime:slam-001",
            information_need_ref="need:exit-location",
            required_information_refs=("need:exit-location",),
            available_information_refs=("need:exit-location",),
            context_ref="context:runtime:office",
            intent_ref="intent:runtime:locate-exit",
            task_ref="task:identify-exit",
            goal_ref="goal:locate-exit",
            concern_ref="concern:exit-location",
            role_refs=("role:visitor",),
            field_refs=("field:office:physical-v1",),
            relation_refs=("relation:door-shared-exit",),
            source_ref="source:runtime:pose-stream-001",
            raw_result_ref="provider-output:slam_v1:slam-001",
            spatial_refs=("spatial-reference:exit-geometry",),
            expected_evidence_kinds=("spatial_map_candidate",),
            temporal_ref="time:runtime:slam-001",
        ),
    )


def reobservation_case_v1() -> ProviderObservationIngressCaseV1:
    return replace(
        build_provider_observation_cases_v1()[0],
        case_id="REOBSERVATION_TO_PROVIDER_REQUEST",
        execution_instance_ref="provider-runtime:reobserve-001",
        raw_result_ref="provider-output:detection_v1:reobserve-001",
        next_cycle_requested=True,
    )


def provider_unavailable_case_v1() -> ProviderObservationIngressCaseV1:
    return replace(
        build_provider_observation_cases_v1()[0],
        case_id="PROVIDER_UNAVAILABLE_NO_FAKE_EVIDENCE",
        provider_result_status="UNAVAILABLE",
    )


def malformed_provider_result_case_v1() -> ProviderObservationIngressCaseV1:
    return replace(
        build_provider_observation_cases_v1()[0],
        case_id="MALFORMED_PROVIDER_RESULT_REJECTED",
        raw_result_ref="",
    )


def unresolved_capability_case_v1() -> ProviderObservationIngressCaseV1:
    return replace(
        build_provider_observation_cases_v1()[0],
        case_id="CAPABILITY_UNRESOLVED_NO_PROVIDER_CALL",
        capability_kind="UNRESOLVED_CAPABILITY",
        capability_ref="capability:unresolved",
    )
