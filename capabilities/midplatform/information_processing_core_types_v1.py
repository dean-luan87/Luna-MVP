# -*- coding: utf-8 -*-
"""Information Processing Core types v1 — candidate/planning dataclasses only."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, Tuple


class InformationType(str, Enum):
    TASK_INPUT = "task_input"
    USER_INSTRUCTION = "user_instruction"
    SYSTEM_SIGNAL = "system_signal"
    EVIDENCE_INPUT = "evidence_input"
    GOVERNANCE_SIGNAL = "governance_signal"
    APPROVAL_SIGNAL = "approval_signal"
    PERMISSION_SIGNAL = "permission_signal"
    MEMORY_SIGNAL = "memory_signal"
    WORLD_MODEL_SIGNAL = "world_model_signal"
    HEALTH_SIGNAL = "health_signal"
    UNKNOWN_INFORMATION = "unknown_information"


class ProcessingStatus(str, Enum):
    READY = "ready"
    DEFER = "defer"
    REJECT = "reject"
    UNKNOWN = "unknown"
    CLOSE = "close"
    GOVERNANCE_REVIEW = "governance_review"


class DownstreamReadiness(str, Enum):
    LIFECYCLE = "lifecycle"
    ORCHESTRATION = "orchestration"
    NONE = "none"
    DEFERRED = "deferred"
    REJECTED = "rejected"


INFORMATION_TYPE_REGISTRY: Tuple[str, ...] = tuple(t.value for t in InformationType)

IPC_CANDIDATE_TYPES: Tuple[str, ...] = (
    "RawInformationInput",
    "InformationTypeSignal",
    "InformationClassificationCandidate",
    "InformationNormalizationCandidate",
    "InformationCandidate",
    "InformationProcessingContext",
    "InformationProcessingResultCandidate",
)

NON_EXECUTION_FLAG_DEFAULTS: Tuple[str, ...] = (
    "candidate_only",
    "side_effect_allowed",
    "real_execution",
    "runtime_required_now",
)


@dataclass(frozen=True)
class NonExecutionFlags:
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False
    no_record_creation: bool = True
    no_grant_creation: bool = True
    no_authorization_request_creation: bool = True
    no_runtime_execution: bool = True
    no_route_execution: bool = True
    no_real_handoff_execution: bool = True
    no_candidate_promotion_execution: bool = True
    no_whitebox_runtime_call: bool = True
    no_persistent_write: bool = True


@dataclass(frozen=True)
class RawInformationInput:
    input_id: str
    source_ref: str
    payload_ref: str
    payload_kind: str
    content_summary: str
    type_hint: Optional[str] = None
    required_fields: Tuple[str, ...] = ()
    present_fields: Tuple[str, ...] = ()
    idempotency_ref: Optional[str] = None
    traceability_refs: Tuple[str, ...] = ()
    governance_refs: Tuple[str, ...] = ()
    non_execution_flags: NonExecutionFlags = field(default_factory=NonExecutionFlags)
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class InformationTypeSignal:
    signal_id: str
    input_ref: str
    detected_type: str
    confidence: str
    governance_sensitive: bool
    signal_reason: str
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class InformationClassificationCandidate:
    candidate_id: str
    input_ref: str
    signal_ref: str
    information_type: str
    priority: str
    processing_intent: str
    governance_sensitive: bool
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class InformationNormalizationCandidate:
    candidate_id: str
    classification_ref: str
    normalized_payload_ref: str
    normalized_kind: str
    completeness_ok: bool
    missing_fields: Tuple[str, ...] = ()
    traceability_refs: Tuple[str, ...] = ()
    governance_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class InformationCandidate:
    candidate_id: str
    input_ref: str
    classification_ref: str
    normalization_ref: str
    information_type: str
    processing_status: str
    downstream_readiness: str
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class InformationProcessingContext:
    context_id: str
    input_ref: str
    source_trust_tier: str
    workload_scope: str
    duplicate_detected: bool
    overload_marker: bool
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False


@dataclass(frozen=True)
class InformationProcessingResultCandidate:
    candidate_id: str
    input_ref: str
    information_candidate_ref: str
    classification_candidate_ref: str
    normalization_candidate_ref: str
    detected_information_type: str
    processing_status: str
    downstream_readiness: str
    validation_pass: bool
    workload_control_pass: bool
    non_execution_guard_pass: bool
    traceability_refs: Tuple[str, ...]
    governance_refs: Tuple[str, ...]
    candidate_only: bool = True
    side_effect_allowed: bool = False
    real_execution: bool = False
    runtime_required_now: bool = False
