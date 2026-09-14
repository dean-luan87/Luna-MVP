from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Mapping, Optional, Tuple


ERROR_NAMESPACE_V1 = "LUNA-PROTO-L2-FIELD-EVENT-ADMISSION-TEMPORAL-VALIDITY-V1::*"


class AdmissionStatusV1(str, Enum):
    ADMITTED_EVENT = "admitted_event"
    REJECTED_EVENT = "rejected_event"
    DEFERRED_EVENT = "deferred_event"
    DUPLICATE_EVENT = "duplicate_event"
    EXPIRED_EVENT = "expired_event"
    OUT_OF_ORDER_EVENT = "out_of_order_event"


class AdmissionReasonCodeV1(str, Enum):
    ADMITTED = "ADMISSION_ADMITTED"
    MISSING_REQUIRED_FIELD = "ADMISSION_MISSING_REQUIRED_FIELD"
    INVALID_FIELD_TYPE = "ADMISSION_INVALID_FIELD_TYPE"
    INVALID_TIMESTAMP = "TEMPORAL_INVALID_TIMESTAMP"
    TIME_INFORMATION_INSUFFICIENT = "TEMPORAL_INFORMATION_INSUFFICIENT"
    EVENT_TIME_IN_FUTURE = "TEMPORAL_EVENT_TIME_IN_FUTURE"
    DUPLICATE_EVENT_ID = "ADMISSION_DUPLICATE_EVENT_ID"
    EVENT_EXPIRED = "TEMPORAL_EVENT_EXPIRED"
    TEMPORAL_SEQUENCE_OUT_OF_ORDER = "TEMPORAL_SEQUENCE_OUT_OF_ORDER"
    FIELD_SEQUENCE_OUT_OF_ORDER = "TEMPORAL_FIELD_SEQUENCE_OUT_OF_ORDER"


ADMISSION_STATUS_REGISTRY_V1: Tuple[str, ...] = tuple(
    status.value for status in AdmissionStatusV1
)
ADMISSION_REASON_CODE_REGISTRY_V1: Tuple[str, ...] = tuple(
    reason.value for reason in AdmissionReasonCodeV1
)


@dataclass(frozen=True)
class FieldEventCandidateV1:
    event_id: str
    event_type: str
    field_ref: str
    occurred_at: Optional[str]
    observed_at: Optional[str]
    received_at: Optional[str]
    source_chain: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    payload: Mapping[str, Any]
    trace_ref: str


@dataclass(frozen=True)
class AdmissionPolicyV1:
    evaluated_at: str
    max_event_age_seconds: int = 86400
    max_out_of_order_seconds: int = 0
    future_tolerance_seconds: int = 0


@dataclass(frozen=True)
class AdmissionContextV1:
    known_event_ids: Tuple[str, ...] = field(default_factory=tuple)
    latest_occurred_at_by_field: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class TemporalAssessmentV1:
    status: str
    occurred_at_utc: Optional[str]
    observed_at_utc: Optional[str]
    received_at_utc: Optional[str]
    evaluated_at_utc: Optional[str]
    event_age_seconds: Optional[int]
    latest_field_occurred_at_utc: Optional[str]
    timezone_aware: bool
    chronology_valid: Optional[bool]


@dataclass(frozen=True)
class AdmissionDecisionStepV1:
    step_id: str
    step_name: str
    outcome: str


@dataclass(frozen=True)
class FieldEventAdmissionResultV1:
    admission_status: str
    reason_code: str
    event_ref: str
    field_ref: str
    temporal_assessment: TemporalAssessmentV1
    evidence_refs: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    trace_ref: str
    evaluated_at: str
    reducer_eligible: bool
    reducer_input_candidate: Optional[Dict[str, Any]]
    decision_steps: Tuple[AdmissionDecisionStepV1, ...]
    candidate_only: bool = True
    fact_admitted: bool = False
    field_state_modified: bool = False
    reducer_executed: bool = False
    external_io_executed: bool = False

