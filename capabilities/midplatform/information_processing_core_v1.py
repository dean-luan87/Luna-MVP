# -*- coding: utf-8 -*-
"""Information Processing Core v1 — controlled candidate-level information processing only."""

from __future__ import annotations

from typing import Any, Dict, Optional, Set, Tuple

from capabilities.midplatform.core.micro_os_common_types_v1 import ValidationResult
from capabilities.midplatform.information_processing_core_builders_v1 import (
    build_information_candidate,
    build_information_classification_candidate,
    build_information_normalization_candidate,
    build_information_processing_result_candidate,
)
from capabilities.midplatform.information_processing_core_classifiers_v1 import (
    classify_candidate_priority,
    classify_information_type,
    classify_processing_intent,
    detect_information_signals,
)
from capabilities.midplatform.information_processing_core_contracts_v1 import check_io_input_contract
from capabilities.midplatform.information_processing_core_static_validators_v1 import (
    validate_classification_candidate,
    validate_core_not_constrained_by_peripheral_contract,
    validate_forbidden_side_effects_absent,
    validate_information_candidate,
    validate_information_type_signal,
    validate_non_execution_boundary,
    validate_processing_result_candidate,
    validate_raw_information_input,
    validate_traceability_refs,
    validate_unknown_classification_allowed,
    validate_workload_control,
)
from capabilities.midplatform.information_processing_core_types_v1 import (
    DownstreamReadiness,
    InformationCandidate,
    InformationClassificationCandidate,
    InformationNormalizationCandidate,
    InformationProcessingContext,
    InformationProcessingResultCandidate,
    InformationType,
    InformationTypeSignal,
    ProcessingStatus,
    RawInformationInput,
)

CORE_FUNCTIONS: Tuple[str, ...] = (
    "receive_raw_information",
    "check_information_source",
    "detect_type_signal_for_information",
    "identify_information_type",
    "normalize_information_input",
    "check_information_completeness",
    "attach_traceability_to_information_candidate",
    "attach_governance_to_information_candidate",
    "build_information_candidate_from_raw_input",
    "mark_downstream_readiness",
    "assemble_information_processing_result",
    "run_controlled_information_processing_core",
)

_SEEN_IDEMPOTENCY: Set[str] = set()


def receive_raw_information(raw: RawInformationInput) -> RawInformationInput:
    ok, _ = check_io_input_contract(raw)
    if ok and raw.traceability_refs:
        return raw
    refs = raw.traceability_refs or (f"trace:ipc:{raw.input_id}", f"source:{raw.source_ref}")
    gov = raw.governance_refs or ("governance:ipc_default",)
    return RawInformationInput(
        input_id=raw.input_id,
        source_ref=raw.source_ref,
        payload_ref=raw.payload_ref,
        payload_kind=raw.payload_kind,
        content_summary=raw.content_summary,
        type_hint=raw.type_hint,
        required_fields=raw.required_fields,
        present_fields=raw.present_fields,
        idempotency_ref=raw.idempotency_ref,
        traceability_refs=refs,
        governance_refs=gov,
    )


def check_information_source(raw: RawInformationInput) -> ValidationResult:
    issues = []
    if not raw.source_ref:
        issues.append("source_ref_missing")
    if raw.source_ref and raw.source_ref.startswith("untrusted:"):
        issues.append("untrusted_source")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def detect_type_signal_for_information(raw: RawInformationInput) -> InformationTypeSignal:
    signals = detect_information_signals(raw)
    signal = classify_information_type(raw)
    reason = f"{signal.signal_reason};signals={','.join(signals)}"
    return InformationTypeSignal(
        signal_id=signal.signal_id,
        input_ref=signal.input_ref,
        detected_type=signal.detected_type,
        confidence=signal.confidence,
        governance_sensitive=signal.governance_sensitive,
        signal_reason=reason,
        traceability_refs=signal.traceability_refs,
        governance_refs=signal.governance_refs,
    )


def identify_information_type(raw: RawInformationInput) -> Tuple[InformationTypeSignal, InformationClassificationCandidate]:
    signal = detect_type_signal_for_information(raw)
    incomplete = bool(raw.required_fields and set(raw.required_fields) - set(raw.present_fields or ()))
    high_risk = signal.governance_sensitive or "high_risk" in (raw.content_summary or "").lower()
    priority = classify_candidate_priority(signal, high_risk=high_risk, incomplete=incomplete)
    intent = classify_processing_intent(signal, incomplete=incomplete)
    classification = build_information_classification_candidate(raw, signal, priority=priority, processing_intent=intent)
    return signal, classification


def normalize_information_input(
    raw: RawInformationInput,
    classification: InformationClassificationCandidate,
) -> InformationNormalizationCandidate:
    normalized_ref = f"norm:{raw.payload_ref}"
    normalized_kind = f"{classification.information_type}_normalized"
    missing = tuple(set(raw.required_fields) - set(raw.present_fields or ()))
    completeness_ok = len(missing) == 0
    return build_information_normalization_candidate(
        classification,
        normalized_payload_ref=normalized_ref,
        normalized_kind=normalized_kind,
        completeness_ok=completeness_ok,
        missing_fields=missing,
    )


def check_information_completeness(normalization: InformationNormalizationCandidate) -> ValidationResult:
    if normalization.completeness_ok:
        return ValidationResult(valid=True, issues=(), blocked=False)
    return ValidationResult(
        valid=False,
        issues=tuple(f"missing_{f}" for f in normalization.missing_fields) or ("incomplete",),
        blocked=False,
    )


def attach_traceability_to_information_candidate(
    information: InformationCandidate,
    *,
    extra_refs: Tuple[str, ...] = (),
) -> InformationCandidate:
    refs = tuple(dict.fromkeys((*information.traceability_refs, *extra_refs)))
    trace_result = validate_traceability_refs(information)
    trace_ok = trace_result.valid
    if trace_ok and refs == information.traceability_refs:
        return information
    return InformationCandidate(
        candidate_id=information.candidate_id,
        input_ref=information.input_ref,
        classification_ref=information.classification_ref,
        normalization_ref=information.normalization_ref,
        information_type=information.information_type,
        processing_status=information.processing_status,
        downstream_readiness=information.downstream_readiness,
        traceability_refs=refs or (f"trace:ipc:{information.input_ref}",),
        governance_refs=information.governance_refs,
    )


def attach_governance_to_information_candidate(
    information: InformationCandidate,
    *,
    extra_gov_refs: Tuple[str, ...] = (),
) -> InformationCandidate:
    gov = tuple(dict.fromkeys((*information.governance_refs, *extra_gov_refs)))
    return InformationCandidate(
        candidate_id=information.candidate_id,
        input_ref=information.input_ref,
        classification_ref=information.classification_ref,
        normalization_ref=information.normalization_ref,
        information_type=information.information_type,
        processing_status=information.processing_status,
        downstream_readiness=information.downstream_readiness,
        traceability_refs=information.traceability_refs,
        governance_refs=gov or ("governance:ipc_default",),
    )


def mark_downstream_readiness(
    information: InformationCandidate,
    *,
    classification: InformationClassificationCandidate,
    completeness: ValidationResult,
    source_check: ValidationResult,
    duplicate: bool = False,
    overload: bool = False,
) -> InformationCandidate:
    if source_check.blocked:
        status, readiness = ProcessingStatus.REJECT.value, DownstreamReadiness.REJECTED.value
    elif overload:
        status, readiness = ProcessingStatus.DEFER.value, DownstreamReadiness.DEFERRED.value
    elif duplicate:
        status, readiness = ProcessingStatus.READY.value, DownstreamReadiness.NONE.value
    elif not completeness.valid:
        status, readiness = ProcessingStatus.DEFER.value, DownstreamReadiness.DEFERRED.value
    elif classification.governance_sensitive or classification.processing_intent == "governance_review_candidate":
        status, readiness = ProcessingStatus.GOVERNANCE_REVIEW.value, DownstreamReadiness.ORCHESTRATION.value
    elif classification.information_type == InformationType.UNKNOWN_INFORMATION.value:
        status, readiness = ProcessingStatus.UNKNOWN.value, DownstreamReadiness.DEFERRED.value
    elif classification.information_type in (
        InformationType.TASK_INPUT.value,
        InformationType.USER_INSTRUCTION.value,
        InformationType.EVIDENCE_INPUT.value,
    ):
        status, readiness = ProcessingStatus.READY.value, DownstreamReadiness.ORCHESTRATION.value
    elif classification.information_type in (
        InformationType.MEMORY_SIGNAL.value,
        InformationType.WORLD_MODEL_SIGNAL.value,
        InformationType.HEALTH_SIGNAL.value,
    ):
        status, readiness = ProcessingStatus.READY.value, DownstreamReadiness.LIFECYCLE.value
    else:
        status, readiness = ProcessingStatus.READY.value, DownstreamReadiness.ORCHESTRATION.value
    return InformationCandidate(
        candidate_id=information.candidate_id,
        input_ref=information.input_ref,
        classification_ref=information.classification_ref,
        normalization_ref=information.normalization_ref,
        information_type=information.information_type,
        processing_status=status,
        downstream_readiness=readiness,
        traceability_refs=information.traceability_refs,
        governance_refs=information.governance_refs,
    )


def build_information_candidate_from_raw_input(
    raw: RawInformationInput,
    classification: InformationClassificationCandidate,
    normalization: InformationNormalizationCandidate,
    *,
    processing_status: str,
    downstream_readiness: str,
) -> InformationCandidate:
    info = build_information_candidate(
        raw, classification, normalization,
        processing_status=processing_status,
        downstream_readiness=downstream_readiness,
    )
    info = attach_traceability_to_information_candidate(info, extra_refs=(f"chain:ipc:{raw.input_id}",))
    return attach_governance_to_information_candidate(info)


def assemble_information_processing_result(
    raw: RawInformationInput,
    classification: InformationClassificationCandidate,
    normalization: InformationNormalizationCandidate,
    information: InformationCandidate,
    *,
    validation_results: Tuple[ValidationResult, ...],
    workload_flags: Dict[str, bool],
) -> InformationProcessingResultCandidate:
    validation_pass = all(r.valid for r in validation_results)
    workload_result = validate_workload_control(workload_flags)
    non_exec = validate_non_execution_boundary(information)
    return build_information_processing_result_candidate(
        raw, classification, normalization, information,
        validation_pass=validation_pass and non_exec.valid,
        workload_control_pass=workload_result.valid,
        non_execution_guard_pass=non_exec.valid,
    )


def run_controlled_information_processing_core(
    raw: RawInformationInput,
    *,
    overload: bool = False,
    reset_idempotency: bool = False,
) -> Dict[str, Any]:
    global _SEEN_IDEMPOTENCY
    if reset_idempotency:
        _SEEN_IDEMPOTENCY = set()
    received = receive_raw_information(raw)
    source_check = check_information_source(received)
    signal, classification = identify_information_type(received)
    normalization = normalize_information_input(received, classification)
    completeness = check_information_completeness(normalization)
    duplicate = bool(received.idempotency_ref and received.idempotency_ref in _SEEN_IDEMPOTENCY)
    if received.idempotency_ref and not duplicate:
        _SEEN_IDEMPOTENCY.add(received.idempotency_ref)
    info = build_information_candidate_from_raw_input(
        received, classification, normalization,
        processing_status=ProcessingStatus.READY.value,
        downstream_readiness=DownstreamReadiness.NONE.value,
    )
    info = mark_downstream_readiness(
        info, classification=classification, completeness=completeness,
        source_check=source_check, duplicate=duplicate, overload=overload,
    )
    workload_flags = {
        "single_envelope_processing": True,
        "unknown_not_silently_dropped": info.processing_status != ProcessingStatus.CLOSE.value or info.information_type == InformationType.UNKNOWN_INFORMATION.value,
        "incomplete_can_defer": True,
        "high_risk_governance_review_candidate": True,
        "duplicate_idempotency_supported": True,
        "overload_can_defer": True,
        "downstream_work_not_swallowed": True,
        "classification_scope_not_unbounded": True,
    }
    validations = (
        validate_raw_information_input(received),
        validate_information_type_signal(signal),
        validate_classification_candidate(classification),
        validate_information_candidate(info),
        validate_unknown_classification_allowed(classification),
        validate_non_execution_boundary(info),
        validate_forbidden_side_effects_absent(info),
        validate_core_not_constrained_by_peripheral_contract(info),
    )
    result = assemble_information_processing_result(
        received, classification, normalization, info,
        validation_results=validations,
        workload_flags=workload_flags,
    )
    result_validation = validate_processing_result_candidate(result)
    processing_pass = result.validation_pass and result.non_execution_guard_pass and result_validation.valid
    return {
        "processing_pass": processing_pass,
        "input_ref": received.input_id,
        "detected_information_type": signal.detected_type,
        "classification_candidate_id": classification.candidate_id,
        "normalization_candidate_id": normalization.candidate_id,
        "information_candidate_id": info.candidate_id,
        "processing_result_candidate_id": result.candidate_id,
        "downstream_readiness": info.downstream_readiness,
        "processing_status": info.processing_status,
        "validation_result": {"valid": result.validation_pass, "issues": ()},
        "workload_control_result": {"valid": result.workload_control_pass},
        "non_execution_guard_result": {"valid": result.non_execution_guard_pass},
        "candidate_only": result.candidate_only,
        "side_effect_allowed": result.side_effect_allowed,
        "real_execution": result.real_execution,
        "runtime_required_now": result.runtime_required_now,
        "signal": signal,
        "classification": classification,
        "normalization": normalization,
        "information_candidate": info,
        "result_candidate": result,
    }
