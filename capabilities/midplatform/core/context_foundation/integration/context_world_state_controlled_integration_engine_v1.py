"""Deterministic Context / Field / Current World controlled handoff engine."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

from capabilities.midplatform.core.context_foundation.context_foundation_skeleton_v1 import (
    ContextFoundationSkeletonV1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_types_v1 import (
    ContextAssemblyInputV1,
    TemporalScopeReferenceV1,
)
from capabilities.midplatform.core.context_foundation.context_projection_types_v1 import (
    ProjectionReferenceV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)
from capabilities.midplatform.core.field_event_admission_api_v1 import (
    AdmissionContextV1,
    AdmissionPolicyV1,
    admit_field_event,
)

from .context_world_state_controlled_integration_error_types_v1 import make_error
from .context_world_state_controlled_integration_types_v1 import (
    ContextWorldAssemblyCandidateV1,
    ContextWorldStateControlResultV1,
    ContextWorldTraceV1,
    FieldEventHandoffCandidateV1,
    ObservationContextHandoffCandidateV1,
)


EVALUATED_AT = "2026-08-13T00:00:00Z"
CONTEXT_OWNER = "Context Foundation"
FIELD_EVENT_OWNER = "Field Event Admission"
FIELD_REDUCER_OWNER = "Field State Reducer"
CURRENT_WORLD_OWNER = "Cognitive State Formation"


def _tuple(value: Any) -> Tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value else ()
    return tuple(str(item) for item in value if item)


def _ref(prefix: str, case_id: str) -> str:
    return f"{prefix}:{case_id}"


def _temporal_status(payload: Mapping[str, Any]) -> str:
    if payload.get("source_revoked") or payload.get("revoked"):
        return "REVOKED"
    if payload.get("expired"):
        return "EXPIRED"
    if payload.get("superseded"):
        return "SUPERSEDED"
    if payload.get("stale"):
        return "STALE"
    if payload.get("refresh"):
        return "REFRESHED"
    return "ACTIVE"


def _observation_usable(payload: Mapping[str, Any], temporal_status: str) -> bool:
    return bool(payload.get("observation_admitted", True)) and temporal_status not in {
        "REVOKED",
        "EXPIRED",
    }


def _projection(
    owner: str,
    projection_id: str,
    kind: str,
    case_id: str,
    validity: str,
    unknown_state: str = "known",
) -> ProjectionReferenceV1:
    return ProjectionReferenceV1(
        source_owner=owner,
        projection_id=projection_id,
        projection_version="v1",
        timestamp=EVALUATED_AT,
        validity=validity,
        confidence=0.7,
        unknown_state=unknown_state,
        provenance=(_ref("provenance", case_id), projection_id),
        projection_kind=kind,
        trace_reference=_ref("trace:projection", case_id),
        read_only=True,
        reference_only=True,
        source_mutation_allowed=False,
    )


def _build_observation_context_handoff(
    payload: Mapping[str, Any], temporal_status: str
) -> ObservationContextHandoffCandidateV1 | None:
    if not _observation_usable(payload, temporal_status) or payload.get("duplicate_observation_handoff"):
        return None
    case_id = str(payload.get("case_id") or "unknown")
    observation_ref = str(payload.get("observation_ref") or _ref("observation", case_id))
    evidence_refs = _tuple(payload.get("evidence_refs") or (_ref("evidence", case_id),))
    return ObservationContextHandoffCandidateV1(
        handoff_id=_ref("observation-context-handoff", case_id),
        observation_refs=(observation_ref,),
        admitted_observation_refs=(observation_ref,),
        evidence_refs=evidence_refs,
        temporal_refs=(_ref("temporal", case_id), str(payload.get("observed_at") or EVALUATED_AT), temporal_status),
        uncertainty_refs=_tuple(payload.get("uncertainty_refs")),
        contradiction_refs=_tuple(payload.get("contradiction_refs")),
        correction_refs=_tuple(payload.get("correction_refs")),
        task_refs=_tuple(payload.get("task_refs") or payload.get("task_ref")),
        field_refs=_tuple(payload.get("field_refs") or payload.get("field_ref")),
        pcn_refs=_tuple(payload.get("pcn_refs") or payload.get("pcn_ref")),
        intent_refs=_tuple(payload.get("intent_refs") or payload.get("intent_ref")),
        provenance_refs=tuple(dict.fromkeys((_ref("provenance", case_id), *evidence_refs))),
        trace_ref=_ref("trace:observation-context", case_id),
        context_mutation=False,
    )


def _build_field_event(
    payload: Mapping[str, Any],
    temporal_status: str,
) -> FieldEventHandoffCandidateV1 | None:
    if not payload.get("field_relevant") or not payload.get("observation_admitted", True):
        return None
    if payload.get("duplicate_field_event"):
        return None
    case_id = str(payload.get("case_id") or "unknown")
    observation_ref = str(payload.get("observation_ref") or _ref("observation", case_id))
    evidence_refs = _tuple(payload.get("evidence_refs") or (_ref("evidence", case_id),))
    field_ref = str(payload.get("field_ref") or _ref("field", case_id))
    event = {
        "event_id": _ref("field-event", case_id),
        "event_type": str(payload.get("event_type") or "observation_field_event_candidate"),
        "field_ref": field_ref,
        "occurred_at": str(payload.get("occurred_at") or EVALUATED_AT),
        "observed_at": str(payload.get("observed_at") or EVALUATED_AT),
        "received_at": str(payload.get("received_at") or EVALUATED_AT),
        "source_chain": ["Observation Gateway", "Context Foundation integration", FIELD_EVENT_OWNER],
        "evidence_refs": list(evidence_refs),
        "payload": {"observation_ref": observation_ref, "candidate_only": True},
        "trace_ref": _ref("trace:field-event", case_id),
    }
    admission_required = not bool(payload.get("field_event_admission", False))
    admission_status = "REQUIRES_ADMISSION"
    reducer_eligible = False
    reducer_input: Dict[str, Any] = {}
    if not admission_required:
        if temporal_status == "EXPIRED":
            admission_status = "EXPIRED_EVENT"
        elif temporal_status == "REVOKED":
            admission_status = "REVOKED_EVENT"
        elif temporal_status == "SUPERSEDED":
            admission_status = "SUPERSEDED_EVENT"
        elif temporal_status == "STALE":
            admission_status = "STALE_EVENT"
        else:
            admission_result = admit_field_event(
                event,
                AdmissionPolicyV1(evaluated_at=EVALUATED_AT),
                AdmissionContextV1(),
            )
            admission_status = admission_result.admission_status.upper()
            reducer_eligible = bool(admission_result.reducer_eligible)
            reducer_input = dict(admission_result.reducer_input_candidate or {})
            if reducer_eligible:
                reducer_input["admitted"] = True
                reducer_input["raw_observation"] = False
    return FieldEventHandoffCandidateV1(
        event_id=event["event_id"],
        event_type=event["event_type"],
        field_ref=field_ref,
        observation_refs=(observation_ref,),
        evidence_refs=evidence_refs,
        source_chain=tuple(event["source_chain"]),
        occurred_at=event["occurred_at"],
        observed_at=event["observed_at"],
        received_at=event["received_at"],
        temporal_status=temporal_status,
        admission_status=admission_status,
        admission_required=admission_required,
        reducer_eligible=reducer_eligible,
        reducer_input_candidate=reducer_input,
        contradiction_refs=_tuple(payload.get("contradiction_refs")),
        correction_refs=_tuple(payload.get("correction_refs")),
        supersedes_ref=str(payload.get("supersedes_ref") or ""),
        revocation_refs=_tuple(payload.get("revocation_refs")),
        expiration_ref=str(payload.get("expiration_ref") or ""),
        trace_ref=event["trace_ref"],
        provenance_refs=tuple(dict.fromkeys((_ref("provenance", case_id), *evidence_refs))),
        field_state_mutation=False,
    )


def _build_context(
    payload: Mapping[str, Any],
    handoff: ObservationContextHandoffCandidateV1 | None,
    field_event: FieldEventHandoffCandidateV1 | None,
    temporal_status: str,
) -> ContextWorldAssemblyCandidateV1 | None:
    if handoff is None or payload.get("duplicate_context_update"):
        return None
    case_id = str(payload.get("case_id") or "unknown")
    field_refs = handoff.field_refs or ((field_event.field_ref,) if field_event else ())
    observation_projection = _projection(
        "Observation Manager",
        handoff.observation_refs[0],
        "observation",
        case_id,
        temporal_status.lower(),
        "multiple_candidates" if handoff.contradiction_refs else "known",
    )
    field_projection = (
        _projection(
            "Field State System",
            field_refs[0],
            "field",
            case_id,
            temporal_status.lower(),
            "multiple_candidates" if handoff.contradiction_refs else "known",
        )
        if field_refs
        else None
    )
    foundation_request = ContextAssemblyInputV1(
        context_id=_ref("context", case_id),
        version="context-world-integration-v1",
        temporal_scope=TemporalScopeReferenceV1(
            scope_id=_ref("temporal-scope", case_id),
            valid_from_reference=str(payload.get("valid_from") or EVALUATED_AT),
            valid_until_reference=str(payload.get("valid_until") or ""),
            expiry_condition_reference="source_revoked_or_temporal_invalidated",
            reset_condition_reference="next_cognitive_cycle",
            reference_only=True,
        ),
        field_projection_reference=field_projection,
        observation_projection_reference=observation_projection,
        provenance=handoff.provenance_refs,
        trace_timestamp=EVALUATED_AT,
        direct_mutation_requested=False,
        skeleton_only=True,
    )
    foundation_context = ContextFoundationSkeletonV1().assemble_context(foundation_request)
    context_status = "CONTESTED" if handoff.contradiction_refs else "ASSEMBLED"
    if temporal_status == "STALE":
        context_status = "DEGRADED_STALE"
    return ContextWorldAssemblyCandidateV1(
        context_id=foundation_context.context_id,
        context_ref=foundation_context.context_id,
        task_refs=handoff.task_refs,
        observation_refs=handoff.admitted_observation_refs,
        field_refs=field_refs,
        pcn_refs=handoff.pcn_refs,
        intent_refs=handoff.intent_refs,
        uncertainty_refs=handoff.uncertainty_refs,
        contradiction_refs=handoff.contradiction_refs,
        temporal_refs=handoff.temporal_refs,
        source_context_foundation_trace_ref=foundation_context.trace_reference,
        trace_ref=_ref("trace:context", case_id),
        provenance_refs=tuple(dict.fromkeys((*handoff.provenance_refs, foundation_context.trace_reference))),
        context_status=context_status,
    )


def _build_current_world(
    payload: Mapping[str, Any],
    context: ContextWorldAssemblyCandidateV1 | None,
    handoff: ObservationContextHandoffCandidateV1 | None,
    temporal_status: str,
) -> CurrentWorldCandidateV1 | None:
    if context is None or payload.get("duplicate_current_world"):
        return None
    case_id = str(payload.get("case_id") or "unknown")
    conflicts = tuple(dict.fromkeys((*context.contradiction_refs, *_tuple(payload.get("field_conflict_refs")))))
    status = "CONTESTED" if conflicts else "PARTIAL_CANDIDATE"
    if temporal_status in {"STALE", "EXPIRED", "REVOKED", "SUPERSEDED"}:
        status = temporal_status
    refs = tuple(dict.fromkeys((*context.provenance_refs, handoff.trace_ref if handoff else "")))
    return CurrentWorldCandidateV1(
        current_world_id=_ref("current-world", case_id),
        attention_refs=_tuple(payload.get("attention_refs")),
        active_hypothesis_refs=_tuple(payload.get("hypothesis_refs")),
        alternative_hypothesis_refs=_tuple(payload.get("alternative_hypothesis_refs")),
        context_refs=(context.context_ref,),
        field_state_refs=context.field_refs,
        pcn_refs=context.pcn_refs,
        intent_refs=context.intent_refs,
        observation_refs=context.observation_refs,
        uncertainty_refs=context.uncertainty_refs,
        conflict_refs=conflicts,
        temporal_refs=context.temporal_refs,
        source_versions={"context": "context-world-integration-v1", "field": "field-state-reference-v1"},
        world_state_kind_candidate="conflicted_world" if conflicts else "partial_world",
        world_stability_candidate=status,
        trace_ref=_ref("trace:current-world", case_id),
        provenance_refs=refs,
        candidate_only=True,
        field_mutation=False,
        field_entity_creation=False,
        field_confidence_mutation=False,
        field_transition=False,
        event_admission=False,
        reducer_invocation_as_mutation_authority=False,
        field_truth_declaration=False,
    )


def _build_trace(
    payload: Mapping[str, Any],
    handoff: ObservationContextHandoffCandidateV1 | None,
    field_event: FieldEventHandoffCandidateV1 | None,
    context: ContextWorldAssemblyCandidateV1 | None,
    current_world: CurrentWorldCandidateV1 | None,
) -> ContextWorldTraceV1:
    case_id = str(payload.get("case_id") or "unknown")
    observation_trace = _ref("trace:observation", case_id)
    evidence_traces = tuple(_ref("trace:evidence", ref) for ref in (handoff.evidence_refs if handoff else (_ref("evidence", case_id),)))
    field_traces = (field_event.trace_ref,) if field_event else ()
    context_trace = context.trace_ref if context else ""
    world_trace = current_world.trace_ref if current_world else ""
    root = str(payload.get("root_trace_id") or _ref("root-trace", case_id))
    source_refs = tuple(dict.fromkeys((*_tuple(payload.get("source_refs")), *(handoff.observation_refs if handoff else ()))))
    provenance = tuple(dict.fromkeys((*source_refs, *(handoff.provenance_refs if handoff else ()), *(context.provenance_refs if context else ()))))
    correction = _tuple(payload.get("correction_refs"))
    contradiction = _tuple(payload.get("contradiction_refs")) + _tuple(payload.get("field_conflict_refs"))
    temporal = (_ref("temporal", case_id), str(payload.get("observed_at") or EVALUATED_AT), _temporal_status(payload))
    path = tuple(item for item in (root, world_trace, context_trace, *field_traces, observation_trace, *evidence_traces, *source_refs) if item)
    return ContextWorldTraceV1(
        root_trace_id=root,
        current_world_trace_ref=world_trace,
        context_trace_ref=context_trace,
        field_event_trace_refs=field_traces,
        observation_trace_refs=(observation_trace,),
        evidence_trace_refs=evidence_traces,
        source_refs=source_refs,
        provenance_refs=provenance,
        correction_lineage=correction,
        contradiction_lineage=tuple(dict.fromkeys(contradiction)),
        temporal_lineage=temporal,
        reverse_lookup_path=path,
        authority_granted=False,
    )


class ContextWorldStateControlledIntegrationEngineV1:
    """Pure candidate adapter; Context/Field/World owners retain authority."""

    runtime_execution = False
    provider_invocation = False
    model_call = False
    mutation_authority = False
    field_state_reducer_is_single_mutation_authority = True

    def run_case(self, payload: Mapping[str, Any]) -> ContextWorldStateControlResultV1:
        case_id = str(payload.get("case_id") or "unknown")
        temporal_status = _temporal_status(payload)
        handoff = _build_observation_context_handoff(payload, temporal_status)
        field_event = _build_field_event(payload, temporal_status)
        context = _build_context(payload, handoff, field_event, temporal_status)
        current_world = _build_current_world(payload, context, handoff, temporal_status)
        errors = []
        if payload.get("duplicate_observation_handoff"):
            errors.append(make_error("DUPLICATE_OBSERVATION_HANDOFF", "observation handoff replayed", (), _ref("trace:error", case_id)))
        if payload.get("duplicate_field_event"):
            errors.append(make_error("DUPLICATE_FIELD_EVENT", "field event replayed", (), _ref("trace:error", case_id)))
        if payload.get("duplicate_context_update"):
            errors.append(make_error("DUPLICATE_CONTEXT_UPDATE", "context update replayed", (), _ref("trace:error", case_id)))
        if payload.get("duplicate_current_world"):
            errors.append(make_error("DUPLICATE_CURRENT_WORLD", "current world candidate replayed", (), _ref("trace:error", case_id)))
        if field_event and field_event.admission_required:
            errors.append(make_error("FIELD_EVENT_ADMISSION_REQUIRED", "field event is not reducer eligible before admission", (field_event.event_id,), field_event.trace_ref))
        if temporal_status in {"STALE", "EXPIRED", "REVOKED", "SUPERSEDED"}:
            errors.append(make_error("TEMPORAL_INVALIDATION", "temporal or source lineage limits downstream use", (), _ref("trace:temporal", case_id)))

        behavior = {
            "observation_present": True,
            "observation_admitted": bool(payload.get("observation_admitted", True)),
            "observation_context_handoff_present": handoff is not None,
            "context_candidate_present": context is not None,
            "context_status": context.context_status if context else "NOT_ASSEMBLED",
            "context_mutation": False,
            "context_field_refs_read_only": bool(context and context.field_refs),
            "task_context_present": bool(context and context.task_refs),
            "intent_reference_read_only": bool(context and context.intent_refs),
            "pcn_reference_read_only": bool(context and context.pcn_refs),
            "field_event_candidate_present": field_event is not None,
            "field_event_admission_required": bool(field_event and field_event.admission_required),
            "field_event_admitted": bool(field_event and field_event.admission_status == "ADMITTED_EVENT"),
            "field_event_admission_status": field_event.admission_status if field_event else "NOT_APPLICABLE",
            "reducer_eligible": bool(field_event and field_event.reducer_eligible),
            "reducer_invoked": False,
            "reducer_is_single_mutation_authority": True,
            "field_state_mutation": False,
            "observation_can_mutate_field": False,
            "current_world_candidate_present": current_world is not None,
            "current_world_refs_context": bool(current_world and current_world.context_refs),
            "current_world_refs_field_state": bool(current_world and current_world.field_state_refs),
            "current_world_is_field_truth": False,
            "current_world_field_mutation": False,
            "current_world_event_admission": False,
            "contradiction_preserved": bool(_tuple(payload.get("contradiction_refs")) or _tuple(payload.get("field_conflict_refs"))),
            "correction_lineage_preserved": bool(_tuple(payload.get("correction_refs"))),
            "temporal_status": temporal_status,
            "temporal_lineage_preserved": True,
            "duplicate_observation_guard": not bool(payload.get("duplicate_observation_handoff")),
            "duplicate_field_event_guard": not bool(payload.get("duplicate_field_event")),
            "duplicate_context_guard": not bool(payload.get("duplicate_context_update")),
            "duplicate_current_world_guard": not bool(payload.get("duplicate_current_world")),
            "provenance_reverse_lookup_complete": bool(current_world and current_world.trace_ref and context and context.trace_ref),
            "a_route_handoff_candidate_present": bool(current_world or context),
            "runtime_handoff_ready": False,
            "mutation_authority": False,
            "provider_invocation": False,
            "model_call": False,
            "source_truth_declared": False,
            "ocr_evidence_is_world_fact": False,
            "visual_detection_is_object_truth": False,
            "slam_geometry_is_semantic_truth": False,
            "emotion_engine_execution": False,
            "b_route_execution": False,
            "semantic_compression_execution": False,
        }
        guards = {
            "provider_can_mutate_context": False,
            "provider_can_mutate_field": False,
            "observation_can_mutate_field": False,
            "context_can_mutate_field": False,
            "current_world_can_mutate_field": False,
            "observation_declares_truth": False,
            "context_declares_truth": False,
            "current_world_is_field_truth": False,
            "second_field_writer": False,
            "runtime_execution": False,
            "provider_invocation": False,
            "model_call": False,
            "database_write": False,
            "vector_store_write": False,
            "scheduler_execution": False,
            "device_control": False,
            "emotion_engine_execution": False,
            "b_route_execution": False,
            "semantic_compression_execution": False,
            "real_side_effect": False,
            "candidate_only": True,
            "synthetic_only": True,
            "controlled_integration_only": True,
        }
        trace = _build_trace(payload, handoff, field_event, context, current_world)
        next_ref = _ref("a-route-next-cognitive-stage", case_id) if (context or current_world) else ""
        return ContextWorldStateControlResultV1(
            case_id=case_id,
            observation_context_handoff=handoff,
            field_event_handoff=field_event,
            context=context,
            current_world=current_world,
            trace=trace,
            behavior=behavior,
            errors=tuple(error.__dict__ for error in errors),
            negative_guards=guards,
            next_route_handoff_ref=next_ref,
        )
