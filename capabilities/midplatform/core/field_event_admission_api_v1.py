from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional, Tuple

from capabilities.midplatform.core.field_event_admission_types_v1 import (
    AdmissionContextV1,
    AdmissionDecisionStepV1,
    AdmissionPolicyV1,
    AdmissionReasonCodeV1,
    AdmissionStatusV1,
    FieldEventAdmissionResultV1,
    FieldEventCandidateV1,
    TemporalAssessmentV1,
)


REQUIRED_STRUCTURAL_FIELDS: Tuple[str, ...] = (
    "event_id", "event_type", "field_ref", "source_chain",
    "evidence_refs", "payload", "trace_ref",
)
REQUIRED_TEMPORAL_FIELDS: Tuple[str, ...] = (
    "occurred_at", "observed_at", "received_at",
)


def _parse_aware_timestamp(value: Any) -> Optional[datetime]:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(timezone.utc)


def _utc_text(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _strict_tuple(value: Any) -> Tuple[str, ...] | None:
    if not isinstance(value, (list, tuple)):
        return None
    if any(not isinstance(item, str) or not item.strip() for item in value):
        return None
    return tuple(value)


def _assessment(
    status: str,
    occurred: Optional[datetime],
    observed: Optional[datetime],
    received: Optional[datetime],
    evaluated: Optional[datetime],
    latest: Optional[datetime],
    chronology_valid: Optional[bool],
) -> TemporalAssessmentV1:
    age = None
    if occurred is not None and evaluated is not None:
        age = int((evaluated - occurred).total_seconds())
    return TemporalAssessmentV1(
        status=status,
        occurred_at_utc=_utc_text(occurred),
        observed_at_utc=_utc_text(observed),
        received_at_utc=_utc_text(received),
        evaluated_at_utc=_utc_text(evaluated),
        event_age_seconds=age,
        latest_field_occurred_at_utc=_utc_text(latest),
        timezone_aware=all(
            value is not None for value in (occurred, observed, received, evaluated)
        ),
        chronology_valid=chronology_valid,
    )


def _step(step_id: str, name: str, outcome: str) -> AdmissionDecisionStepV1:
    return AdmissionDecisionStepV1(step_id=step_id, step_name=name, outcome=outcome)


def _result(
    event: Mapping[str, Any],
    policy: AdmissionPolicyV1,
    status: AdmissionStatusV1,
    reason: AdmissionReasonCodeV1,
    temporal: TemporalAssessmentV1,
    steps: Tuple[AdmissionDecisionStepV1, ...],
) -> FieldEventAdmissionResultV1:
    reducer_eligible = status is AdmissionStatusV1.ADMITTED_EVENT
    evidence_refs = _strict_tuple(event.get("evidence_refs")) or ()
    source_chain = _strict_tuple(event.get("source_chain")) or ()
    reducer_candidate: Optional[Dict[str, Any]] = None
    if reducer_eligible:
        reducer_candidate = {
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "field_ref": event["field_ref"],
            "occurred_at": temporal.occurred_at_utc,
            "observed_at": temporal.observed_at_utc,
            "received_at": temporal.received_at_utc,
            "source_chain": list(source_chain),
            "evidence_refs": list(evidence_refs),
            "payload": dict(event["payload"]),
            "trace_ref": event["trace_ref"],
            "admission_status": status.value,
            "reason_code": reason.value,
            "reducer_eligible": True,
            "candidate_only": True,
            "not_fact": True,
        }
        source_id = str(event.get("source_id") or "")
        if not source_id and isinstance(event.get("payload"), Mapping):
            source_id = str(event["payload"].get("source_id") or "")
        if source_id:
            reducer_candidate["source_id"] = source_id
    return FieldEventAdmissionResultV1(
        admission_status=status.value,
        reason_code=reason.value,
        event_ref=str(event.get("event_id") or ""),
        field_ref=str(event.get("field_ref") or ""),
        temporal_assessment=temporal,
        evidence_refs=evidence_refs,
        source_chain=source_chain,
        trace_ref=str(event.get("trace_ref") or ""),
        evaluated_at=policy.evaluated_at,
        reducer_eligible=reducer_eligible,
        reducer_input_candidate=reducer_candidate,
        decision_steps=steps,
    )


def admit_field_event(
    event_candidate: Mapping[str, Any] | FieldEventCandidateV1,
    policy: AdmissionPolicyV1,
    context: AdmissionContextV1 = AdmissionContextV1(),
) -> FieldEventAdmissionResultV1:
    event: Dict[str, Any] = (
        asdict(event_candidate)
        if isinstance(event_candidate, FieldEventCandidateV1)
        else dict(event_candidate)
        if isinstance(event_candidate, Mapping)
        else {}
    )
    evaluated = _parse_aware_timestamp(policy.evaluated_at)
    empty_temporal = _assessment(
        "not_evaluated", None, None, None, evaluated, None, None
    )

    missing = [name for name in REQUIRED_STRUCTURAL_FIELDS if not event.get(name)]
    if missing:
        return _result(
            event, policy, AdmissionStatusV1.REJECTED_EVENT,
            AdmissionReasonCodeV1.MISSING_REQUIRED_FIELD, empty_temporal,
            (_step("01", "structural_validation", "rejected"),),
        )
    scalar_fields = ("event_id", "event_type", "field_ref", "trace_ref")
    if any(not isinstance(event.get(name), str) or not event[name].strip() for name in scalar_fields):
        return _result(
            event, policy, AdmissionStatusV1.REJECTED_EVENT,
            AdmissionReasonCodeV1.INVALID_FIELD_TYPE, empty_temporal,
            (_step("01", "structural_validation", "invalid"),),
        )
    if (
        not isinstance(event.get("payload"), Mapping)
        or _strict_tuple(event.get("source_chain")) is None
        or _strict_tuple(event.get("evidence_refs")) is None
        or not _strict_tuple(event.get("source_chain"))
        or not _strict_tuple(event.get("evidence_refs"))
        or evaluated is None
        or policy.max_event_age_seconds < 0
        or policy.max_out_of_order_seconds < 0
        or policy.future_tolerance_seconds < 0
    ):
        return _result(
            event, policy, AdmissionStatusV1.REJECTED_EVENT,
            AdmissionReasonCodeV1.INVALID_FIELD_TYPE, empty_temporal,
            (_step("01", "structural_validation", "invalid"),),
        )

    structural = _step("01", "structural_validation", "passed")
    if event["event_id"] in set(context.known_event_ids):
        return _result(
            event, policy, AdmissionStatusV1.DUPLICATE_EVENT,
            AdmissionReasonCodeV1.DUPLICATE_EVENT_ID, empty_temporal,
            (structural, _step("02", "duplicate_detection", "duplicate")),
        )

    if any(not event.get(name) for name in REQUIRED_TEMPORAL_FIELDS):
        return _result(
            event, policy, AdmissionStatusV1.DEFERRED_EVENT,
            AdmissionReasonCodeV1.TIME_INFORMATION_INSUFFICIENT, empty_temporal,
            (structural, _step("02", "duplicate_detection", "unique"),
             _step("03", "temporal_validation", "insufficient")),
        )

    occurred = _parse_aware_timestamp(event.get("occurred_at"))
    observed = _parse_aware_timestamp(event.get("observed_at"))
    received = _parse_aware_timestamp(event.get("received_at"))
    latest_raw = context.latest_occurred_at_by_field.get(str(event["field_ref"]))
    latest = _parse_aware_timestamp(latest_raw) if latest_raw is not None else None
    if any(value is None for value in (occurred, observed, received)) or (
        latest_raw is not None and latest is None
    ):
        temporal = _assessment(
            "invalid_timestamp", occurred, observed, received, evaluated, latest, None
        )
        return _result(
            event, policy, AdmissionStatusV1.REJECTED_EVENT,
            AdmissionReasonCodeV1.INVALID_TIMESTAMP, temporal,
            (structural, _step("02", "duplicate_detection", "unique"),
             _step("03", "temporal_validation", "invalid_timestamp")),
        )

    assert occurred is not None and observed is not None and received is not None
    assert evaluated is not None
    chronology_valid = occurred <= observed <= received
    temporal = _assessment(
        "assessed", occurred, observed, received, evaluated, latest, chronology_valid
    )
    steps = (structural, _step("02", "duplicate_detection", "unique"))
    if int((occurred - evaluated).total_seconds()) > policy.future_tolerance_seconds:
        return _result(
            event, policy, AdmissionStatusV1.DEFERRED_EVENT,
            AdmissionReasonCodeV1.EVENT_TIME_IN_FUTURE, temporal,
            steps + (_step("03", "temporal_validation", "future"),),
        )
    if int((evaluated - occurred).total_seconds()) > policy.max_event_age_seconds:
        return _result(
            event, policy, AdmissionStatusV1.EXPIRED_EVENT,
            AdmissionReasonCodeV1.EVENT_EXPIRED, temporal,
            steps + (_step("03", "temporal_validation", "expired"),),
        )
    if not chronology_valid:
        return _result(
            event, policy, AdmissionStatusV1.OUT_OF_ORDER_EVENT,
            AdmissionReasonCodeV1.TEMPORAL_SEQUENCE_OUT_OF_ORDER, temporal,
            steps + (_step("03", "temporal_validation", "sequence_out_of_order"),),
        )
    if latest is not None and int((latest - occurred).total_seconds()) > policy.max_out_of_order_seconds:
        return _result(
            event, policy, AdmissionStatusV1.OUT_OF_ORDER_EVENT,
            AdmissionReasonCodeV1.FIELD_SEQUENCE_OUT_OF_ORDER, temporal,
            steps + (_step("03", "temporal_validation", "field_out_of_order"),),
        )
    return _result(
        event, policy, AdmissionStatusV1.ADMITTED_EVENT,
        AdmissionReasonCodeV1.ADMITTED, temporal,
        steps + (_step("03", "temporal_validation", "valid"),
                 _step("04", "reducer_eligibility", "eligible_candidate")),
    )
