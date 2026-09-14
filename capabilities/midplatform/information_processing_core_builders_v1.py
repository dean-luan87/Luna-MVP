# -*- coding: utf-8 -*-
"""Information Processing Core builders v1 — candidate builders only."""

from __future__ import annotations

from typing import Optional, Tuple

from capabilities.midplatform.information_processing_core_types_v1 import (
    DownstreamReadiness,
    InformationCandidate,
    InformationClassificationCandidate,
    InformationNormalizationCandidate,
    InformationProcessingResultCandidate,
    InformationTypeSignal,
    ProcessingStatus,
    RawInformationInput,
)


def _refs(*items: str) -> Tuple[str, ...]:
    return tuple(x for x in items if x)


def build_information_type_signal(
    raw: RawInformationInput,
    *,
    detected_type: str,
    confidence: str,
    governance_sensitive: bool,
    signal_reason: str,
) -> InformationTypeSignal:
    refs = raw.traceability_refs or (f"trace:ipc:{raw.input_id}",)
    gov = raw.governance_refs or (("governance:ipc_sensitive" if governance_sensitive else "governance:ipc_default"),)
    return InformationTypeSignal(
        signal_id=f"ipc_signal_{raw.input_id}",
        input_ref=raw.input_id,
        detected_type=detected_type,
        confidence=confidence,
        governance_sensitive=governance_sensitive,
        signal_reason=signal_reason,
        traceability_refs=refs,
        governance_refs=gov,
    )


def build_information_classification_candidate(
    raw: RawInformationInput,
    signal: InformationTypeSignal,
    *,
    priority: str,
    processing_intent: str,
    candidate_id: Optional[str] = None,
) -> InformationClassificationCandidate:
    cid = candidate_id or f"ipc_class_{raw.input_id}"
    return InformationClassificationCandidate(
        candidate_id=cid,
        input_ref=raw.input_id,
        signal_ref=signal.signal_id,
        information_type=signal.detected_type,
        priority=priority,
        processing_intent=processing_intent,
        governance_sensitive=signal.governance_sensitive,
        traceability_refs=signal.traceability_refs,
        governance_refs=signal.governance_refs,
    )


def build_information_normalization_candidate(
    classification: InformationClassificationCandidate,
    *,
    normalized_payload_ref: str,
    normalized_kind: str,
    completeness_ok: bool,
    missing_fields: Tuple[str, ...] = (),
    candidate_id: Optional[str] = None,
) -> InformationNormalizationCandidate:
    cid = candidate_id or f"ipc_norm_{classification.candidate_id}"
    return InformationNormalizationCandidate(
        candidate_id=cid,
        classification_ref=classification.candidate_id,
        normalized_payload_ref=normalized_payload_ref,
        normalized_kind=normalized_kind,
        completeness_ok=completeness_ok,
        missing_fields=missing_fields,
        traceability_refs=classification.traceability_refs,
        governance_refs=classification.governance_refs,
    )


def build_information_candidate(
    raw: RawInformationInput,
    classification: InformationClassificationCandidate,
    normalization: InformationNormalizationCandidate,
    *,
    processing_status: str,
    downstream_readiness: str,
    candidate_id: Optional[str] = None,
) -> InformationCandidate:
    cid = candidate_id or f"ipc_info_{raw.input_id}"
    return InformationCandidate(
        candidate_id=cid,
        input_ref=raw.input_id,
        classification_ref=classification.candidate_id,
        normalization_ref=normalization.candidate_id,
        information_type=classification.information_type,
        processing_status=processing_status,
        downstream_readiness=downstream_readiness,
        traceability_refs=normalization.traceability_refs,
        governance_refs=normalization.governance_refs,
    )


def build_information_processing_result_candidate(
    raw: RawInformationInput,
    classification: InformationClassificationCandidate,
    normalization: InformationNormalizationCandidate,
    information: InformationCandidate,
    *,
    validation_pass: bool,
    workload_control_pass: bool,
    non_execution_guard_pass: bool,
    candidate_id: Optional[str] = None,
) -> InformationProcessingResultCandidate:
    cid = candidate_id or f"ipc_result_{raw.input_id}"
    return InformationProcessingResultCandidate(
        candidate_id=cid,
        input_ref=raw.input_id,
        information_candidate_ref=information.candidate_id,
        classification_candidate_ref=classification.candidate_id,
        normalization_candidate_ref=normalization.candidate_id,
        detected_information_type=classification.information_type,
        processing_status=information.processing_status,
        downstream_readiness=information.downstream_readiness,
        validation_pass=validation_pass,
        workload_control_pass=workload_control_pass,
        non_execution_guard_pass=non_execution_guard_pass,
        traceability_refs=information.traceability_refs,
        governance_refs=information.governance_refs,
    )


BUILDER_FUNCTIONS: Tuple[str, ...] = (
    "build_information_type_signal",
    "build_information_classification_candidate",
    "build_information_normalization_candidate",
    "build_information_candidate",
    "build_information_processing_result_candidate",
)
