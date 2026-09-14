# -*- coding: utf-8 -*-
"""Information Processing Core classifiers v1 — controlled type classification only."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from capabilities.midplatform.information_processing_core_types_v1 import (
    InformationType,
    InformationTypeSignal,
    RawInformationInput,
)

CLASSIFIER_FUNCTIONS: Tuple[str, ...] = (
    "detect_information_signals",
    "classify_information_type",
    "classify_candidate_priority",
    "classify_processing_intent",
)

_TYPE_HINT_MAP: Dict[str, str] = {
    "task": InformationType.TASK_INPUT.value,
    "task_input": InformationType.TASK_INPUT.value,
    "user_instruction": InformationType.USER_INSTRUCTION.value,
    "instruction": InformationType.USER_INSTRUCTION.value,
    "system_signal": InformationType.SYSTEM_SIGNAL.value,
    "system": InformationType.SYSTEM_SIGNAL.value,
    "evidence": InformationType.EVIDENCE_INPUT.value,
    "evidence_input": InformationType.EVIDENCE_INPUT.value,
    "governance": InformationType.GOVERNANCE_SIGNAL.value,
    "governance_signal": InformationType.GOVERNANCE_SIGNAL.value,
    "approval": InformationType.APPROVAL_SIGNAL.value,
    "approval_signal": InformationType.APPROVAL_SIGNAL.value,
    "permission": InformationType.PERMISSION_SIGNAL.value,
    "permission_signal": InformationType.PERMISSION_SIGNAL.value,
    "memory": InformationType.MEMORY_SIGNAL.value,
    "memory_signal": InformationType.MEMORY_SIGNAL.value,
    "world_model": InformationType.WORLD_MODEL_SIGNAL.value,
    "world_model_signal": InformationType.WORLD_MODEL_SIGNAL.value,
    "health": InformationType.HEALTH_SIGNAL.value,
    "health_signal": InformationType.HEALTH_SIGNAL.value,
    "unknown": InformationType.UNKNOWN_INFORMATION.value,
    "unknown_information": InformationType.UNKNOWN_INFORMATION.value,
}

_GOVERNANCE_SENSITIVE_TYPES: Tuple[str, ...] = (
    InformationType.GOVERNANCE_SIGNAL.value,
    InformationType.APPROVAL_SIGNAL.value,
    InformationType.PERMISSION_SIGNAL.value,
)


def _normalize_hint(hint: Optional[str]) -> Optional[str]:
    if not hint:
        return None
    key = hint.strip().lower().replace("-", "_")
    return _TYPE_HINT_MAP.get(key)


def _infer_from_payload(raw: RawInformationInput) -> Optional[str]:
    kind = (raw.payload_kind or "").lower()
    summary = (raw.content_summary or "").lower()
    combined = f"{kind} {summary}"
    for token, info_type in _TYPE_HINT_MAP.items():
        if token in combined and token not in ("unknown", "instruction"):
            return info_type
    if "task" in combined:
        return InformationType.TASK_INPUT.value
    if "user" in combined or "instruction" in combined:
        return InformationType.USER_INSTRUCTION.value
    if "evidence" in combined:
        return InformationType.EVIDENCE_INPUT.value
    if "governance" in combined or "safety" in combined or "privacy" in combined or "authorization" in combined:
        return InformationType.GOVERNANCE_SIGNAL.value
    if "approval" in combined:
        return InformationType.APPROVAL_SIGNAL.value
    if "permission" in combined:
        return InformationType.PERMISSION_SIGNAL.value
    if "memory" in combined:
        return InformationType.MEMORY_SIGNAL.value
    if "world_model" in combined or "worldmodel" in combined:
        return InformationType.WORLD_MODEL_SIGNAL.value
    if "health" in combined:
        return InformationType.HEALTH_SIGNAL.value
    if "system" in combined:
        return InformationType.SYSTEM_SIGNAL.value
    return None


def detect_information_signals(raw: RawInformationInput) -> Tuple[str, ...]:
    signals = []
    hint = _normalize_hint(raw.type_hint)
    if hint:
        signals.append(f"type_hint:{hint}")
    inferred = _infer_from_payload(raw)
    if inferred:
        signals.append(f"payload:{inferred}")
    if raw.required_fields and set(raw.required_fields) - set(raw.present_fields or ()):
        signals.append("completeness:incomplete")
    if raw.idempotency_ref:
        signals.append(f"idempotency:{raw.idempotency_ref}")
    if not signals:
        signals.append("signal:unknown")
    return tuple(signals)


def classify_information_type(raw: RawInformationInput) -> InformationTypeSignal:
    hint = _normalize_hint(raw.type_hint)
    inferred = _infer_from_payload(raw)
    if hint and inferred and hint != inferred and hint != InformationType.UNKNOWN_INFORMATION.value:
        detected = hint
        confidence = "medium"
        reason = "type_hint_with_payload_conflict_using_hint"
    elif hint:
        detected = hint
        confidence = "high" if hint != InformationType.UNKNOWN_INFORMATION.value else "low"
        reason = "type_hint_classification"
    elif inferred:
        detected = inferred
        confidence = "medium"
        reason = "payload_inference_classification"
    else:
        detected = InformationType.UNKNOWN_INFORMATION.value
        confidence = "low"
        reason = "unknown_information_no_forced_misclassification"
    gov_sensitive = detected in _GOVERNANCE_SENSITIVE_TYPES or "safety" in (raw.content_summary or "").lower()
    refs = raw.traceability_refs or (f"trace:ipc:{raw.input_id}",)
    gov_refs = raw.governance_refs or (("governance:ipc_sensitive" if gov_sensitive else "governance:ipc_default"),)
    return InformationTypeSignal(
        signal_id=f"ipc_signal_{raw.input_id}",
        input_ref=raw.input_id,
        detected_type=detected,
        confidence=confidence,
        governance_sensitive=gov_sensitive,
        signal_reason=reason,
        traceability_refs=refs,
        governance_refs=gov_refs,
    )


def classify_candidate_priority(
    signal: InformationTypeSignal,
    *,
    high_risk: bool = False,
    incomplete: bool = False,
) -> str:
    if high_risk or signal.governance_sensitive:
        return "high"
    if incomplete or signal.detected_type == InformationType.UNKNOWN_INFORMATION.value:
        return "low"
    if signal.detected_type in (InformationType.HEALTH_SIGNAL.value, InformationType.GOVERNANCE_SIGNAL.value):
        return "high"
    return "normal"


def classify_processing_intent(
    signal: InformationTypeSignal,
    *,
    incomplete: bool = False,
    duplicate: bool = False,
    overload: bool = False,
) -> str:
    if overload:
        return "defer_overload"
    if duplicate:
        return "idempotent_reprocess"
    if incomplete:
        return "defer_incomplete"
    if signal.governance_sensitive:
        return "governance_review_candidate"
    if signal.detected_type == InformationType.UNKNOWN_INFORMATION.value:
        return "unknown_mark_and_defer"
    return "normalize_and_candidate_build"
