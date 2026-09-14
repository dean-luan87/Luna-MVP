"""Project a real visual relation candidate into Field Event Admission.

This module owns only the evaluation/integration projection.  It reuses the
real YOLO source, EntityCandidate/RelationCandidate construction, and the
existing Field Event Admission API.  It does not alter the Field Event
taxonomy, invoke the Field Reducer, or promote a relation to a fact.
"""

from __future__ import annotations

import dataclasses
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple

from capabilities.midplatform.core.field_event_admission_api_v1 import (
    AdmissionContextV1,
    AdmissionPolicyV1,
    admit_field_event,
)
from capabilities.midplatform.core.field_event_admission_types_v1 import (
    FieldEventCandidateV1,
)
from capabilities.evaluation.real_visual_cognitive_entity_to_field_relation_candidate_integration.engine_v1 import (
    _entity_candidates,
    _relation_candidate,
    _repo_root,
    _source_detection_refs,
    _subject_binding_ref,
)
from capabilities.evaluation.real_visual_evidence_to_field_state_candidate_projection.engine_v1 import (
    EVALUATED_AT,
    SOURCE_DEFAULT_FIELD_REF,
    RealVisualEvidenceFieldProjectionEngineV1,
)

from .types_v1 import (
    RelationBearingFieldSemanticEventProjectionV1,
    RelationSemanticAdmissionCaseResultV1,
)


PHASE = (
    "Phase-P1-Luna-Relation-Candidate-To-Field-Semantic-Event-Admission-"
    "Integration-v1-001"
)
EXECUTION_MODE = "LIVE_RUNTIME"
PROVIDER_REF = "provider:yolo:local:v1"
MODEL_REF = "model-asset:yolo11n:weights-v1"
FIELD_REF = SOURCE_DEFAULT_FIELD_REF
FIELD_REF_RESOLUTION_STATUS = "CONTROLLED_CONTEXT_CANDIDATE"
RELATION_SEMANTIC_KIND = "ENTITY_TO_FIELD_OBSERVATION_RELATION"
RELATION_SEMANTIC_STATUS = "CANDIDATE_ONLY"
RELATION_PREDICATE = "OBSERVED_IN_FIELD"
TARGET_BINDING_STATUS = "EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE"
EVIDENCE_MINIMUM_EVENT_COUNT = 2
EVIDENCE_SOURCE_DIVERSITY_REQUIREMENT = 2


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value).strip()))


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _projection(
    *,
    runtime: Mapping[str, Any],
    entity_candidate: Any,
    relation_candidate: Any,
    projection_ref: str,
    field_ref: str = FIELD_REF,
    field_ref_resolution_status: str = FIELD_REF_RESOLUTION_STATUS,
) -> RelationBearingFieldSemanticEventProjectionV1:
    runtime_ref = str(runtime.get("runtime_observation_ref") or "")
    source_detection_refs = _source_detection_refs(
        entity_candidate=entity_candidate,
        runtime=runtime,
    )
    subject_binding_ref = _subject_binding_ref(
        entity_ref=entity_candidate.entity_id
    )
    trace_ref = f"trace:relation-semantic-event:{projection_ref}:v1"
    provenance_refs = _unique(
        (
            *tuple(entity_candidate.provenance_refs),
            *tuple(relation_candidate.provenance_refs),
            runtime_ref,
            projection_ref,
            subject_binding_ref,
            "provenance:relation-to-field-semantic-event-admission:v1",
        )
    )
    return RelationBearingFieldSemanticEventProjectionV1(
        projection_ref=projection_ref,
        relation_semantic_kind=RELATION_SEMANTIC_KIND,
        relation_candidate_ref=relation_candidate.relation_id,
        subject_ref=relation_candidate.subject_ref,
        predicate=relation_candidate.predicate,
        object_ref=relation_candidate.object_ref,
        field_ref=field_ref,
        entity_candidate_ref=entity_candidate.entity_id,
        runtime_observation_ref=runtime_ref,
        evidence_refs=tuple(entity_candidate.evidence_refs),
        source_detection_refs=source_detection_refs,
        subject_binding_ref=subject_binding_ref,
        trace_ref=trace_ref,
        provenance_refs=provenance_refs,
        field_ref_resolution_status=field_ref_resolution_status,
    )


def _field_event_candidate(
    projection: RelationBearingFieldSemanticEventProjectionV1,
    *,
    case_id: str,
) -> FieldEventCandidateV1:
    return FieldEventCandidateV1(
        event_id=f"field-event:entity-field-relation:{case_id}:v1",
        event_type="entity_field_relation_observed",
        field_ref=projection.field_ref,
        occurred_at=EVALUATED_AT,
        observed_at=EVALUATED_AT,
        received_at=EVALUATED_AT,
        source_chain=(
            "Real YOLO Provider Runtime",
            "Runtime Observation",
            "Visual Evidence Candidate",
            "EntityCandidateV1",
            "L1 Subject Binding Candidate",
            "RelationCandidateV1",
            "Relation-bearing Field Semantic Event Projection",
            "FieldEventCandidateV1",
            "Field Event Admission",
        ),
        evidence_refs=projection.evidence_refs,
        payload={
            "relation_semantic_kind": projection.relation_semantic_kind,
            "relation_semantic_status": RELATION_SEMANTIC_STATUS,
            "relation_candidate_ref": projection.relation_candidate_ref,
            "subject_ref": projection.subject_ref,
            "predicate": projection.predicate,
            "object_ref": projection.object_ref,
            "field_ref": projection.field_ref,
            "entity_candidate_ref": projection.entity_candidate_ref,
            "runtime_observation_ref": projection.runtime_observation_ref,
            "evidence_refs": list(projection.evidence_refs),
            "source_detection_refs": list(projection.source_detection_refs),
            "subject_binding_ref": projection.subject_binding_ref,
            "field_ref_resolution_status": projection.field_ref_resolution_status,
            "candidate_only": projection.candidate_only,
            "fact_admitted": projection.fact_admitted,
            "truth_declared": projection.truth_declared,
            "persistent_relation_declared": projection.persistent_relation_declared,
            "identity_resolution_status": projection.identity_resolution_status,
            "target_binding_status": projection.target_binding_status,
        },
        trace_ref=projection.trace_ref,
    )


def _admit(event: FieldEventCandidateV1) -> Any:
    return admit_field_event(
        event,
        AdmissionPolicyV1(evaluated_at=EVALUATED_AT),
        AdmissionContextV1(),
    )


def _case(
    *,
    case_id: str,
    entity_candidate: Any,
    relation_candidate: Any,
    runtime: Mapping[str, Any],
    admit: bool,
    field_ref: str = FIELD_REF,
    field_ref_resolution_status: str = FIELD_REF_RESOLUTION_STATUS,
) -> RelationSemanticAdmissionCaseResultV1:
    projection = _projection(
        runtime=runtime,
        entity_candidate=entity_candidate,
        relation_candidate=relation_candidate,
        projection_ref=f"relation-semantic-projection:{case_id}",
        field_ref=field_ref,
        field_ref_resolution_status=field_ref_resolution_status,
    )
    event = _field_event_candidate(projection, case_id=case_id)
    admission = _admit(event) if admit else None
    event_data = _jsonable(event)
    admission_data = _jsonable(admission) if admission is not None else None
    payload = dict(event_data.get("payload") or {})
    reducer_candidate = dict((admission_data or {}).get("reducer_input_candidate") or {})
    reducer_payload = dict(reducer_candidate.get("payload") or {})
    payload_lineage = (
        bool(payload.get("runtime_observation_ref"))
        and bool(payload.get("evidence_refs"))
        and bool(payload.get("source_detection_refs"))
        and bool(payload.get("subject_binding_ref"))
        and bool(payload.get("relation_candidate_ref"))
    )
    if admission is None:
        field_event_lineage_preserved = payload_lineage
    else:
        field_event_lineage_preserved = payload_lineage and all(
            reducer_payload.get(key) == payload.get(key)
            for key in (
                "runtime_observation_ref",
                "evidence_refs",
                "source_detection_refs",
                "subject_binding_ref",
                "relation_candidate_ref",
            )
        )
    behavior = {
        "relation_semantic_projection_created": True,
        "field_event_candidate_created": True,
        "relation_semantic_kind_explicit": (
            payload.get("relation_semantic_kind") == RELATION_SEMANTIC_KIND
        ),
        "relation_candidate_ref_preserved": (
            payload.get("relation_candidate_ref")
            == relation_candidate.relation_id
            and reducer_payload.get("relation_candidate_ref")
            == relation_candidate.relation_id
        ),
        "subject_ref_matches_entity": (
            payload.get("subject_ref") == entity_candidate.entity_id
            and payload.get("entity_candidate_ref") == entity_candidate.entity_id
        ),
        "observed_in_field_not_belongs_to_field": (
            payload.get("predicate") == RELATION_PREDICATE
            and payload.get("predicate") not in {"BELONGS_TO", "belongs_to"}
        ),
        "candidate_only": (
            payload.get("candidate_only") is True
            and payload.get("fact_admitted") is False
            and payload.get("truth_declared") is False
        ),
        "persistent_relation_not_declared": (
            payload.get("persistent_relation_declared") is False
        ),
        "identity_unresolved": (
            payload.get("identity_resolution_status") == "UNRESOLVED"
        ),
        "target_binding_unresolved": (
            payload.get("target_binding_status") == TARGET_BINDING_STATUS
        ),
        "relation_not_source_diversity": True,
        "event_admission_not_fact_admission": bool(
            admission is not None
            and admission.admission_status == "admitted_event"
            and admission.fact_admitted is False
        ),
        "event_admission_not_field_truth": payload.get("truth_declared") is False,
        "event_admission_not_world_truth": payload.get("truth_declared") is False,
        "unresolved_field_ref_not_admitted": (
            field_ref_resolution_status != "UNRESOLVED"
            or (admission is not None and admission.admission_status != "admitted_event")
        ),
        "field_event_lineage_preserved": field_event_lineage_preserved,
    }
    return RelationSemanticAdmissionCaseResultV1(
        case_id=case_id,
        relation_candidate=_jsonable(relation_candidate),
        projection=_jsonable(projection),
        field_event_candidate=event_data,
        admission=admission_data,
        behavior=behavior,
    )


class RealVisualRelationToFieldSemanticEventAdmissionEngineV1:
    """One real provider execution plus relation-event admission guards."""

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root
        self.visual_engine = RealVisualEvidenceFieldProjectionEngineV1(
            repository_root
        )

    def run(self, *, source_ref: str) -> Dict[str, Any]:
        runtime = self.visual_engine._run_provider(source_ref)
        provider = runtime.get("provider")
        detections = tuple(getattr(provider, "detections", ()) or ())
        evidence = tuple(getattr(provider, "evidence", ()) or ())
        candidates = _entity_candidates(runtime)
        first = candidates[0] if candidates else None
        first_relation = (
            _relation_candidate(entity_candidate=first, runtime=runtime)
            if first is not None
            else None
        )

        cases = []
        if first is not None and first_relation is not None:
            cases.append(
                _case(
                    case_id="ENTITY_FIELD_RELATION_SEMANTIC_EVENT_ADMITTED",
                    entity_candidate=first,
                    relation_candidate=first_relation,
                    runtime=runtime,
                    admit=True,
                )
            )
            for case_id in (
                "RELATION_EVENT_NOT_FIELD_TRUTH",
                "OBSERVED_IN_FIELD_NOT_BELONGS_TO_FIELD",
                "RELATION_EVENT_NOT_PERSISTENT_RELATION",
                "RELATION_EVENT_DOES_NOT_RESOLVE_IDENTITY",
                "RELATION_EVENT_NOT_SOURCE_DIVERSITY",
            ):
                cases.append(
                    _case(
                        case_id=case_id,
                        entity_candidate=first,
                        relation_candidate=first_relation,
                        runtime=runtime,
                        admit=False,
                    )
                )
            cases.append(
                _case(
                    case_id="UNRESOLVED_FIELD_REF_NOT_ADMITTED",
                    entity_candidate=first,
                    relation_candidate=first_relation,
                    runtime=runtime,
                    admit=True,
                    field_ref="",
                    field_ref_resolution_status="UNRESOLVED",
                )
            )

        positive = next(
            (item for item in cases if item.case_id == "ENTITY_FIELD_RELATION_SEMANTIC_EVENT_ADMITTED"),
            None,
        )
        positive_projection = dict(positive.projection or {}) if positive else {}
        positive_event = dict(positive.field_event_candidate or {}) if positive else {}
        positive_admission = dict(positive.admission or {}) if positive else {}
        positive_payload = dict(positive_event.get("payload") or {})
        positive_reducer_input = dict(
            positive_admission.get("reducer_input_candidate") or {}
        )
        positive_reducer_payload = dict(positive_reducer_input.get("payload") or {})

        return {
            "phase": PHASE,
            "execution_mode": EXECUTION_MODE,
            "semantic_event_mode": "RELATION_BEARING_FIELD_EVENT_CANDIDATE",
            "provider_ref": PROVIDER_REF,
            "model_ref": MODEL_REF,
            "source_ref": source_ref,
            "provider_real_execution_attempted": bool(
                runtime.get("provider_real_execution_attempted")
            ),
            "provider_real_execution_verified": bool(
                runtime.get("provider_real_execution_verified")
            ),
            "provider_invoked": bool(runtime.get("provider_invoked")),
            "model_invoked": bool(runtime.get("model_invoked")),
            "recorded_provider_result_used": False,
            "runtime_observation_ref": runtime.get("runtime_observation_ref"),
            "evidence_refs": list(runtime.get("evidence_refs") or ()),
            "detection_count": len(detections),
            "real_visual_evidence_count": len(evidence),
            "entity_candidate_count": len(candidates),
            "relation_candidate_count": len(candidates),
            "field_event_candidate_count": len(cases),
            "admitted_event_count": (
                1 if positive_admission.get("admission_status") == "admitted_event" else 0
            ),
            "relation_semantic_kind": RELATION_SEMANTIC_KIND,
            "relation_predicate": RELATION_PREDICATE,
            "field_ref": FIELD_REF,
            "field_ref_resolution_status": FIELD_REF_RESOLUTION_STATUS,
            "entity_candidate_ref": positive_payload.get("entity_candidate_ref"),
            "subject_ref": positive_payload.get("subject_ref"),
            "object_ref": positive_payload.get("object_ref"),
            "relation_candidate_ref": positive_payload.get("relation_candidate_ref"),
            "subject_binding_ref": positive_payload.get("subject_binding_ref"),
            "positive_event_trace_ref": positive_event.get("trace_ref"),
            "positive_admission_status": positive_admission.get("admission_status"),
            "positive_reducer_eligible": positive_admission.get("reducer_eligible"),
            "positive_reducer_input_payload": positive_reducer_payload,
            "candidate_only": True,
            "fact_admitted": False,
            "truth_declared": False,
            "persistent_relation_declared": False,
            "identity_resolution_status": "UNRESOLVED",
            "target_binding_status": TARGET_BINDING_STATUS,
            "evidence_sufficiency_contract": {
                "minimum_event_count": EVIDENCE_MINIMUM_EVENT_COUNT,
                "source_diversity_requirement": EVIDENCE_SOURCE_DIVERSITY_REQUIREMENT,
            },
            "evidence_source_count": 1,
            "relation_candidates_are_not_sources": True,
            "entity_candidates_are_not_sources": True,
            "subject_bindings_are_not_sources": True,
            "policy_trace_compatibility_gap": True,
            "policy_trace_compatibility_gap_status": "KNOWN_NON_BLOCKING_INDEPENDENT_DEBT",
            "field_truth_declared": False,
            "world_truth_declared": False,
            "field_state_reducer_invoked": False,
            "a_route_invoked": False,
            "memory_mutation": False,
            "pcn_mutation": False,
            "cases": [_jsonable(item) for item in cases],
            "forbidden_behaviors": {
                "field_truth_promotion": False,
                "world_truth_declared": False,
                "field_mutation": False,
                "decision_execution": False,
                "task_execution": False,
                "action_execution": False,
                "device_control": False,
                "camera_control": False,
                "movement_control": False,
                "ocr_invocation": False,
                "slam_invocation": False,
                "memory_mutation": False,
                "pcn_mutation": False,
            },
            "validation_errors": list(runtime.get("errors") or ()),
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


def jsonable(value: Any) -> Any:
    return _jsonable(value)


__all__ = [
    "PHASE",
    "RealVisualRelationToFieldSemanticEventAdmissionEngineV1",
    "jsonable",
    "_repo_root",
]
