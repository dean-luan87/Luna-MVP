"""Admission-to-Reducer adapter contract for Field Kernel v1.

The adapter validates and preserves an Admission result. It never invokes the
Reducer, chooses a state, writes a state, or revisits Temporal Validity.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple

from capabilities.midplatform.core.field_event_admission_types_v1 import (
    FieldEventAdmissionResultV1,
)


@dataclass(frozen=True)
class ReducerAdapterInputV1:
    """The only adapter input form accepted from Field Event Admission."""

    event_ref: str
    field_ref: str
    reducer_input_candidate: Mapping[str, Any]
    temporal_assessment: Mapping[str, Any]
    evidence_refs: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    trace_ref: str
    admission_status: str
    reducer_eligible: bool
    schema_version: str = "luna.field_kernel.v1"


class FieldKernelReducerAdapterV1:
    """Projection-only bridge from admitted event to existing Reducer input."""

    @staticmethod
    def adapt_admitted_event(
        admission_result: FieldEventAdmissionResultV1 | Mapping[str, Any],
    ) -> ReducerAdapterInputV1:
        """Return a validated adapter input without calling the Reducer."""

        if isinstance(admission_result, FieldEventAdmissionResultV1):
            data: Mapping[str, Any] = {
                "admission_status": admission_result.admission_status,
                "event_ref": admission_result.event_ref,
                "field_ref": admission_result.field_ref,
                "temporal_assessment": admission_result.temporal_assessment.__dict__,
                "evidence_refs": admission_result.evidence_refs,
                "source_chain": admission_result.source_chain,
                "trace_ref": admission_result.trace_ref,
                "reducer_eligible": admission_result.reducer_eligible,
                "reducer_input_candidate": admission_result.reducer_input_candidate,
            }
        elif isinstance(admission_result, Mapping):
            data = dict(admission_result)
        else:
            raise ValueError("admission_result must be a structured admission result")

        if data.get("admission_status") != "admitted_event":
            raise ValueError("Field Kernel accepts admitted_event only")
        if data.get("reducer_eligible") is not True:
            raise ValueError("Field Kernel accepts reducer-eligible events only")
        reducer_input = data.get("reducer_input_candidate")
        if not isinstance(reducer_input, Mapping):
            raise ValueError("admitted_event requires reducer_input_candidate")
        if reducer_input.get("admission_status") != "admitted_event":
            raise ValueError("reducer_input_candidate must preserve admission status")
        if reducer_input.get("reducer_eligible") is not True:
            raise ValueError("reducer_input_candidate must preserve eligibility")

        temporal_assessment = data.get("temporal_assessment")
        if not isinstance(temporal_assessment, Mapping):
            raise ValueError("admitted_event requires temporal_assessment")

        event_ref = str(data.get("event_ref") or reducer_input.get("event_id") or "")
        field_ref = str(data.get("field_ref") or reducer_input.get("field_ref") or "")
        trace_ref = str(data.get("trace_ref") or reducer_input.get("trace_ref") or "")
        if not event_ref or not field_ref or not trace_ref:
            raise ValueError("admitted_event requires event_ref, field_ref, and trace_ref")

        return ReducerAdapterInputV1(
            event_ref=event_ref,
            field_ref=field_ref,
            reducer_input_candidate=dict(reducer_input),
            temporal_assessment=dict(temporal_assessment),
            evidence_refs=tuple(data.get("evidence_refs") or ()),
            source_chain=tuple(data.get("source_chain") or ()),
            trace_ref=trace_ref,
            admission_status="admitted_event",
            reducer_eligible=True,
        )
