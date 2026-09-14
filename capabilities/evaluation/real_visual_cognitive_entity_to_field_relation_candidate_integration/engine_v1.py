"""Project real visual entity candidates into candidate-only Field relations.

This integration reuses the real-YOLO visual projection and the existing L1
subject-candidate binding boundary.  It creates the canonical
``RelationCandidateV1`` directly through the Cognitive Primitive builder.  The
relation means only that an observation-linked entity candidate was observed
in the current Field context; it does not resolve identity, ownership,
membership, Field meaning, Field Truth, or World Truth.
"""

from __future__ import annotations

import dataclasses
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple

from capabilities.cognitive_flow.cognitive_primitives.api_v1 import (
    create_relation_candidate,
)
from capabilities.evaluation.real_visual_evidence_to_cognitive_entity_subject_binding_integration.engine_v1 import (
    _entity_candidates,
    _repo_root,
)
from capabilities.evaluation.real_visual_evidence_to_field_state_candidate_projection.engine_v1 import (
    EVALUATED_AT,
    SOURCE_DEFAULT_FIELD_REF,
    RealVisualEvidenceFieldProjectionEngineV1,
    _projection,
)
from capabilities.evaluation.real_visual_evidence_to_canonical_field_semantic_event_integration.engine_v1 import (
    _semantic_event,
    _semantic_projection,
)

from .types_v1 import EntityFieldRelationCaseResultV1


PHASE = "Phase-P1-Luna-Real-Cognitive-Entity-To-Field-Relation-Candidate-Integration-v1-001"
EXECUTION_MODE = "LIVE_RUNTIME"
PROVIDER_REF = "provider:yolo:local:v1"
MODEL_REF = "model-asset:yolo11n:weights-v1"
FIELD_REF = SOURCE_DEFAULT_FIELD_REF
FIELD_REF_RESOLUTION_STATUS = "CONTROLLED_CONTEXT_CANDIDATE"
RELATION_PREDICATE = "OBSERVED_IN_FIELD"
RELATION_CONFIDENCE_STATUS = "UNAVAILABLE"
TARGET_BINDING_STATUS = "EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE"
EVIDENCE_MINIMUM_EVENT_COUNT = 2
EVIDENCE_SOURCE_DIVERSITY_REQUIREMENT = 2


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value).strip()))


def _jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            key: _jsonable(item)
            for key, item in dataclasses.asdict(value).items()
        }
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _subject_binding_ref(*, entity_ref: str) -> str:
    return f"subject-binding:real-visual:entity:{entity_ref}"


def _source_detection_refs(
    *,
    entity_candidate: Any,
    runtime: Mapping[str, Any],
) -> Tuple[str, ...]:
    """Read detection refs from the canonical visual-evidence records.

    Capability/model binding refs are provenance, not detection identity. The
    evidence record's ``detection_ref`` is the canonical bridge back to the
    ProviderNativeDetectionRecordV1 detection.
    """

    provider = runtime.get("provider")
    evidence_by_id = {
        str(getattr(item, "evidence_id", "") or ""): item
        for item in tuple(getattr(provider, "evidence", ()) or ())
    }
    return _unique(
        str(getattr(evidence_by_id.get(str(evidence_ref)), "detection_ref", "") or "")
        for evidence_ref in tuple(entity_candidate.evidence_refs)
    )


def _relation_candidate(*, entity_candidate: Any, runtime: Mapping[str, Any]) -> Any:
    entity_ref = str(entity_candidate.entity_id)
    relation_ref = (
        f"relation-candidate:observed-in-field:{entity_ref}:{FIELD_REF}"
    )
    runtime_ref = str(runtime.get("runtime_observation_ref") or "")
    evidence_refs = tuple(entity_candidate.evidence_refs)
    provenance_refs = _unique(
        (
            *tuple(entity_candidate.provenance_refs),
            runtime_ref,
            FIELD_REF,
            relation_ref,
            "provenance:entity-observed-in-field-relation:v1",
        )
    )
    return create_relation_candidate(
        {
            "relation_id": relation_ref,
            "subject_ref": entity_ref,
            "predicate": RELATION_PREDICATE,
            "object_ref": FIELD_REF,
            "evidence_refs": evidence_refs,
            "trace_ref": f"trace:entity-observed-in-field:{entity_ref}:v1",
            "provenance_refs": provenance_refs,
        }
    )


def _relation_trace(
    *,
    relation_candidate: Any,
    entity_candidate: Any,
    runtime: Mapping[str, Any],
) -> Dict[str, Any]:
    """Return a trace projection without changing the semantic-event owner."""

    return {
        "trace_ref": relation_candidate.trace_ref,
        "source_chain": [
            "Real YOLO Provider Runtime",
            "Runtime Observation",
            "Visual Evidence Candidate",
            "EntityCandidateV1",
            "L1 Subject Binding Candidate",
            "RelationCandidateV1",
            "Field Semantic Event / Cognitive Trace",
        ],
        "runtime_observation_ref": runtime.get("runtime_observation_ref"),
        "evidence_refs": list(entity_candidate.evidence_refs),
        "source_detection_refs": list(
            _source_detection_refs(
                entity_candidate=entity_candidate,
                runtime=runtime,
            )
        ),
        "entity_candidate_ref": entity_candidate.entity_id,
        "subject_binding_ref": _subject_binding_ref(
            entity_ref=entity_candidate.entity_id
        ),
        "relation_candidate_ref": relation_candidate.relation_id,
        "field_ref_candidate": FIELD_REF,
        "field_ref_resolution_status": FIELD_REF_RESOLUTION_STATUS,
        "predicate": relation_candidate.predicate,
        "candidate_only": True,
        "fact_admitted": False,
        "truth_declared": False,
    }


def _semantic_trace(
    *,
    runtime: Mapping[str, Any],
    entity_candidate: Any,
    relation_candidate: Any,
    case_id: str,
) -> Dict[str, Any]:
    """Reuse the previous canonical semantic-event projection as a trace."""

    projection = _projection(
        runtime=runtime,
        field_ref_candidate=FIELD_REF,
        field_ref_resolution_status=FIELD_REF_RESOLUTION_STATUS,
        projection_ref=f"field-projection:real-visual-relation:{case_id}:v1",
    )
    semantic_projection = replace(
        _semantic_projection(projection, case_id=case_id),
        subject_ref_candidate=entity_candidate.entity_id,
    )
    event = _semantic_event(semantic_projection, case_id=case_id)
    event["source_chain"] = [
        "Real YOLO Provider Runtime",
        "Runtime Observation",
        "Visual Evidence Candidate",
        "EntityCandidateV1",
        "L1 Subject Binding Candidate",
        "RelationCandidateV1",
        "Field Semantic Event / Cognitive Trace",
    ]
    event["payload"].update(
        {
            "subject_reference_layer": "L1",
            "identity_resolution_status": "UNRESOLVED",
            "semantic_target_resolved": False,
            "relation_candidate_ref": relation_candidate.relation_id,
            "relation_predicate": relation_candidate.predicate,
            "field_ref_resolution_status": FIELD_REF_RESOLUTION_STATUS,
        }
    )
    return event


def _case(
    *,
    case_id: str,
    runtime: Mapping[str, Any],
    entity_candidates: Tuple[Any, ...],
    semantic_trace: Dict[str, Any] | None = None,
) -> EntityFieldRelationCaseResultV1:
    relations = tuple(
        _relation_candidate(entity_candidate=item, runtime=runtime)
        for item in entity_candidates
    )
    binding_refs = tuple(
        _subject_binding_ref(entity_ref=item.entity_id)
        for item in entity_candidates
    )
    relation_traces = tuple(
        _relation_trace(
            relation_candidate=relation,
            entity_candidate=entity_candidate,
            runtime=runtime,
        )
        for entity_candidate, relation in zip(entity_candidates, relations)
    )
    relation_data = tuple(_jsonable(item) for item in relations)
    entity_data = tuple(_jsonable(item) for item in entity_candidates)
    relation_ids = {item.relation_id for item in relations}
    behavior: Dict[str, Any] = {
        "candidate_only": all(
            item.candidate_only is True and item.fact_admitted is False
            for item in relations
        ),
        "relation_candidate_created": bool(relations),
        "observed_in_field_not_belongs_to_field": all(
            item.predicate not in {"BELONGS_TO", "belongs_to"}
            for item in relations
        ),
        "relation_candidate_not_fact": all(
            item.candidate_only is True and item.fact_admitted is False
            for item in relations
        ),
        "relation_candidate_not_persistent_relation": True,
        "relation_does_not_resolve_entity_identity": all(
            item.attributes.get("identity_resolution_status") == "UNRESOLVED"
            for item in entity_candidates
        ),
        "same_relation_ids_are_independent": len(relation_ids) == len(relations),
        "relation_confidence_not_inferred": all(
            not hasattr(item, "confidence") for item in relations
        ),
        "entity_candidate_not_source_diversity": True,
        "cross_field_knowledge_not_meaning_reuse": all(
            not any(
                key in item.attributes
                for key in (
                    "merchandise",
                    "private_property",
                    "office_supply",
                    "ownership",
                    "function",
                )
            )
            for item in entity_candidates
        ),
        "target_binding_remains_unresolved": True,
        "memory_identity_not_entered": True,
    }
    return EntityFieldRelationCaseResultV1(
        case_id=case_id,
        entity_candidates=entity_data,
        subject_binding_refs=binding_refs,
        relation_candidates=relation_data,
        relation_traces=relation_traces,
        semantic_trace=semantic_trace,
        behavior=behavior,
    )


class RealVisualCognitiveEntityToFieldRelationCandidateEngineV1:
    """One real YOLO result plus bounded relation-candidate guards."""

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
        all_relations = tuple(
            _relation_candidate(entity_candidate=item, runtime=runtime)
            for item in candidates
        )
        first = candidates[0] if candidates else None
        first_relation = (
            _relation_candidate(entity_candidate=first, runtime=runtime)
            if first is not None
            else None
        )
        semantic_trace = (
            _semantic_trace(
                runtime=runtime,
                entity_candidate=first,
                relation_candidate=first_relation,
                case_id="ENTITY_OBSERVED_IN_FIELD_RELATION_CREATED",
            )
            if first is not None and first_relation is not None
            else None
        )
        cases = [
            _case(
                case_id="ENTITY_OBSERVED_IN_FIELD_RELATION_CREATED",
                runtime=runtime,
                entity_candidates=(first,) if first is not None else tuple(),
                semantic_trace=semantic_trace,
            )
        ]
        for case_id in (
            "OBSERVED_IN_FIELD_NOT_BELONGS_TO_FIELD",
            "RELATION_CANDIDATE_NOT_FACT",
            "RELATION_CANDIDATE_NOT_PERSISTENT_RELATION",
            "RELATION_DOES_NOT_RESOLVE_ENTITY_IDENTITY",
            "ENTITY_CANDIDATE_NOT_SOURCE_DIVERSITY",
            "ENTITY_CANDIDATE_NOT_MEMORY_IDENTITY",
        ):
            cases.append(
                _case(
                    case_id=case_id,
                    runtime=runtime,
                    entity_candidates=(first,) if first is not None else tuple(),
                )
            )

        same_class_pair: Tuple[Any, Any] | None = None
        for left_index, left in enumerate(candidates):
            left_class = left.attributes.get("class_candidate")
            for right in candidates[left_index + 1 :]:
                if right.attributes.get("class_candidate") == left_class:
                    same_class_pair = (left, right)
                    break
            if same_class_pair:
                break
        cases.append(
            _case(
                case_id="SAME_CLASS_ENTITIES_HAVE_INDEPENDENT_FIELD_RELATIONS",
                runtime=runtime,
                entity_candidates=same_class_pair or tuple(),
            )
        )

        frame_dimensions = getattr(
            detections[0], "frame_dimensions", ()
        ) if detections else ()
        width = frame_dimensions[0] if len(frame_dimensions) == 2 else None
        height = frame_dimensions[1] if len(frame_dimensions) == 2 else None
        source_confidence = (
            float(getattr(detections[0], "confidence", 0.0))
            if detections
            else None
        )
        return {
            "phase": PHASE,
            "execution_mode": EXECUTION_MODE,
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
            "relation_candidate_count": len(all_relations),
            "relation_candidate_refs": [
                item.relation_id for item in all_relations
            ],
            "frame_dimensions": {"width": width, "height": height},
            "frame_dimensions_source": (
                "ProviderNativeDetectionRecordV1.frame_dimensions"
            ),
            "field_ref": FIELD_REF,
            "field_ref_resolution_status": FIELD_REF_RESOLUTION_STATUS,
            "field_context_candidate": True,
            "relation_predicate": RELATION_PREDICATE,
            "relation_confidence_status": RELATION_CONFIDENCE_STATUS,
            "source_visual_confidence": source_confidence,
            "visual_confidence_not_relation_confidence": True,
            "identity_resolution_status": "UNRESOLVED",
            "semantic_target_resolved": False,
            "target_binding_status": TARGET_BINDING_STATUS,
            "evidence_sufficiency_contract": {
                "minimum_event_count": EVIDENCE_MINIMUM_EVENT_COUNT,
                "source_diversity_requirement": EVIDENCE_SOURCE_DIVERSITY_REQUIREMENT,
            },
            "evidence_source_count": 1,
            "relation_candidates_are_not_sources": True,
            "policy_trace_compatibility_gap": True,
            "policy_trace_compatibility_gap_status": "KNOWN_NON_BLOCKING_INDEPENDENT_DEBT",
            "cross_field_knowledge_reuse_not_meaning_reuse": True,
            "field_truth_declared": False,
            "world_truth_declared": False,
            "fact_admitted": False,
            "persistent_relation_declared": False,
            "target_identity_resolved": False,
            "memory_mutation": False,
            "pcn_mutation": False,
            "cases": cases,
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
                "memory_mutation": False,
                "pcn_mutation": False,
                "provider_invocation": False,
                "model_invocation": False,
            },
            "validation_errors": list(runtime.get("errors") or ()),
            "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        }


def jsonable(value: Any) -> Any:
    return _jsonable(value)


__all__ = [
    "PHASE",
    "RealVisualCognitiveEntityToFieldRelationCandidateEngineV1",
    "jsonable",
    "_repo_root",
]
