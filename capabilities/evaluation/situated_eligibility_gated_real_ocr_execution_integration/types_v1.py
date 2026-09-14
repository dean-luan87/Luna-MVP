"""Candidate bridge contract from Situated Eligibility to Provider Runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class SituatedCapabilityExecutionAdmissionV1:
    """A narrow handoff; it does not replace Provider Runtime admission."""

    admission_ref: str
    capability_requirement_ref: str
    eligibility_ref: str
    eligible_now: bool
    provider_execution_admitted: bool
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class GatedOCRExecutionRecordV1:
    case_id: str
    state_id: str
    execution_mode: str
    source_ref: str
    situated_precondition_result: object
    execution_admission: SituatedCapabilityExecutionAdmissionV1
    execution_events: Tuple[str, ...]
    runtime_result: object | None
    provider_real_execution_attempted: bool
    provider_real_execution_verified: bool
    provider_invoked: bool
    model_invoked: bool
    recorded_provider_result_used: bool
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
