"""Minimal Evidence -> Field Event candidate bridge.

The bridge belongs to the existing Field Event / Field Kernel boundary.  It
only validates the source shape, preserves lineage, and performs the explicit
field-reference mapping supplied by its caller.  It does not interpret an
opaque provider payload, admit an event, invoke the Reducer, or mutate Field
State.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Mapping, Optional, Tuple

from capabilities.midplatform.core.field_event_admission_types_v1 import (
    FieldEventCandidateV1,
)


FORMATION_STATUS = "FIELD_EVENT_CANDIDATE_FORMED"
BLOCKED_STATUS = "FIELD_EVENT_CANDIDATE_BLOCKED"
INVALID_STATUS = "INVALID_INPUT"


@dataclass(frozen=True)
class PerceptionEvidenceFieldEventFormationResultV1:
    formation_status: str
    event_candidate: Optional[FieldEventCandidateV1]
    source_evidence_ref: str = ""
    context_ref: str = ""
    field_ref: str = ""
    validation_errors: Tuple[str, ...] = ()
    adapter_semantic_authority: bool = False
    field_state_mutation: bool = False
    truth_declared: bool = False


def _mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if is_dataclass(value):
        return asdict(value)
    return {}


def _strict_refs(value: Any, field_name: str, *, allow_empty: bool = True) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    if not isinstance(value, (list, tuple)):
        return (), (f"invalid_field_type:{field_name}",)
    refs = tuple(value)
    if not allow_empty and not refs:
        return (), (f"missing:{field_name}",)
    if any(not isinstance(item, str) or not item.strip() for item in refs):
        return (), (f"invalid_member_type:{field_name}",)
    return refs, ()


def form_field_event_candidate_from_evidence(
    evidence: Any,
    *,
    field_ref: str,
    context_ref: str,
    occurred_at: str,
    observed_at: str,
    received_at: str,
    event_type: str = "perception_evidence_field_event_candidate",
    correction_refs: Tuple[str, ...] = (),
    supersedes_ref: str = "",
) -> PerceptionEvidenceFieldEventFormationResultV1:
    """Map one admitted Evidence shape to a candidate-only Field Event.

    ``field_ref`` and the temporal values are explicit governed inputs.  The
    bridge never derives them from provider names, capability names, or the
    opaque payload.
    """

    source = _mapping(evidence)
    evidence_ref = str(source.get("evidence_id") or "")
    errors = []
    required = (
        "evidence_id",
        "source_provider",
        "source_capability",
        "raw_output_ref",
        "source_temporal_ref",
        "trace_ref",
        "provenance_refs",
    )
    provenance_refs, provenance_errors = _strict_refs(
        source.get("provenance_refs"), "provenance_refs", allow_empty=False
    )
    errors.extend(provenance_errors)
    for name in required:
        value = source.get(name)
        if name == "provenance_refs":
            continue
        elif not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")
    if source.get("candidate_only") is not True:
        errors.append("evidence_not_candidate_only")
    if source.get("fact_declared") is True:
        errors.append("evidence_fact_declared")
    if not isinstance(field_ref, str) or not field_ref.strip():
        errors.append("field_ref_missing")
    if not isinstance(context_ref, str) or not context_ref.strip():
        errors.append("context_ref_missing")
    for name, value in (
        ("occurred_at", occurred_at),
        ("observed_at", observed_at),
        ("received_at", received_at),
    ):
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing:{name}")
    if errors:
        status = INVALID_STATUS if any(item.startswith("missing:") for item in errors) else BLOCKED_STATUS
        return PerceptionEvidenceFieldEventFormationResultV1(
            formation_status=status,
            event_candidate=None,
            source_evidence_ref=evidence_ref,
            context_ref=str(context_ref or ""),
            field_ref=str(field_ref or ""),
            validation_errors=tuple(dict.fromkeys(errors)),
        )

    event_id = f"field-event:{evidence_ref}:{field_ref}"
    source_chain = tuple(
        dict.fromkeys(
            (
                "Perception Evidence",
                *provenance_refs,
                "Evidence-to-Field Event Adapter",
                "Field Event Candidate",
                event_id,
            )
        )
    )
    candidate_payload = source.get("candidate_payload")
    opaque_payload_ref = str(source.get("raw_output_ref") or "")
    if isinstance(candidate_payload, Mapping):
        opaque_payload_ref = str(
            candidate_payload.get("opaque_payload_ref") or opaque_payload_ref
        )
    event = FieldEventCandidateV1(
        event_id=event_id,
        event_type=event_type,
        field_ref=field_ref,
        occurred_at=occurred_at,
        observed_at=observed_at,
        received_at=received_at,
        source_chain=source_chain,
        evidence_refs=(evidence_ref,),
        payload={
            "source_provider": source["source_provider"],
            "source_capability": source["source_capability"],
            "source_model_ref": source.get("source_model_ref"),
            "context_ref": context_ref,
            "source_temporal_ref": source["source_temporal_ref"],
            "opaque_payload_ref": opaque_payload_ref,
            "correction_refs": list(correction_refs),
            "supersedes_ref": supersedes_ref,
            "candidate_only": True,
            "truth_declared": False,
            "field_mutation": False,
        },
        trace_ref=f"trace:evidence-to-field-event:{evidence_ref}:{field_ref}",
    )
    return PerceptionEvidenceFieldEventFormationResultV1(
        formation_status=FORMATION_STATUS,
        event_candidate=event,
        source_evidence_ref=evidence_ref,
        context_ref=context_ref,
        field_ref=field_ref,
    )


__all__ = [
    "FORMATION_STATUS",
    "BLOCKED_STATUS",
    "INVALID_STATUS",
    "PerceptionEvidenceFieldEventFormationResultV1",
    "form_field_event_candidate_from_evidence",
]
