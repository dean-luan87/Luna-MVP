"""Thin, read-only adapter from governed Field relation state to A-Route input."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

from capabilities.midplatform.core.cognitive_state_formation.cognitive_conditioning_types_v1 import (
    CognitiveRelationInterpretationCandidateV1,
)

from .types_v1 import RelationStateAssimilationResultV1


ENTITY_FIELD_OBSERVATION_RELATION_STATE = "entity_field_observation_relation_state"
ENTITY_TO_FIELD_OBSERVATION_RELATION = "ENTITY_TO_FIELD_OBSERVATION_RELATION"
OBSERVED_IN_FIELD = "OBSERVED_IN_FIELD"


def _mapping(value: Any) -> Mapping[str, Any]:
    if is_dataclass(value):
        return asdict(value)
    return value if isinstance(value, Mapping) else {}


class RelationStateAssimilationAdapterV1:
    """Project only a reducer-governed typed relation state into A-Route."""

    def project(self, field_state_candidate: Any) -> RelationStateAssimilationResultV1:
        candidate = _mapping(field_state_candidate)
        if candidate.get("state_type") != ENTITY_FIELD_OBSERVATION_RELATION_STATE:
            return RelationStateAssimilationResultV1(False, "unsupported_state_type")

        value = _mapping(candidate.get("candidate_value"))
        if not value:
            return RelationStateAssimilationResultV1(False, "empty_candidate_value")

        required = (
            "subject_ref",
            "predicate",
            "object_ref",
            "relation_candidate_ref",
            "relation_semantic_kind",
        )
        missing = tuple(name for name in required if not value.get(name))
        if missing:
            return RelationStateAssimilationResultV1(
                False, f"missing_relation_fields:{','.join(missing)}"
            )
        if value.get("predicate") != OBSERVED_IN_FIELD:
            return RelationStateAssimilationResultV1(False, "unsupported_relation_predicate")
        if value.get("relation_semantic_kind") != ENTITY_TO_FIELD_OBSERVATION_RELATION:
            return RelationStateAssimilationResultV1(False, "unsupported_relation_semantic_kind")
        if value.get("candidate_only") is not True:
            return RelationStateAssimilationResultV1(False, "candidate_only_required")
        if value.get("fact_admitted") is not False:
            return RelationStateAssimilationResultV1(False, "fact_admission_forbidden")
        if value.get("truth_declared") is not False:
            return RelationStateAssimilationResultV1(False, "truth_declaration_forbidden")
        if value.get("persistent_relation_declared") is not False:
            return RelationStateAssimilationResultV1(False, "persistent_relation_forbidden")
        if value.get("identity_resolution_status") != "UNRESOLVED":
            return RelationStateAssimilationResultV1(False, "identity_resolution_forbidden")

        state_ref = str(candidate.get("state_candidate_id") or "")
        interpretation_ref = f"relation-interpretation:{state_ref or value['relation_candidate_ref']}"
        projection = CognitiveRelationInterpretationCandidateV1(
            relation_interpretation_ref=interpretation_ref,
            relation_ref=str(value["relation_candidate_ref"]),
            role_refs=(),
            task_refs=(),
            goal_refs=(),
            information_need_refs=(),
            interpretation_candidate=(
                f"candidate observation: {value['subject_ref']} "
                f"{value['predicate']} {value['object_ref']}"
            ),
            relevance_state="CANDIDATE_ONLY",
            candidate_only=True,
            field_state_candidate_ref=state_ref or None,
            subject_ref=str(value["subject_ref"]),
            predicate=str(value["predicate"]),
            object_ref=str(value["object_ref"]),
            relation_candidate_ref=str(value["relation_candidate_ref"]),
            relation_semantic_kind=str(value["relation_semantic_kind"]),
            evidence_refs=tuple(str(item) for item in value.get("evidence_refs", ())),
            source_refs=tuple(str(item) for item in value.get("source_refs", ())),
            provenance_refs=tuple(str(item) for item in value.get("provenance_refs", ())),
            identity_resolution_status="UNRESOLVED",
            fact_admitted=False,
            truth_declared=False,
            persistent_relation_declared=False,
        )
        return RelationStateAssimilationResultV1(
            accepted=True,
            reason="relation_state_candidate_projected",
            field_state_candidate_ref=state_ref or None,
            relation_interpretation_candidate=projection,
        )


__all__ = [
    "ENTITY_FIELD_OBSERVATION_RELATION_STATE",
    "ENTITY_TO_FIELD_OBSERVATION_RELATION",
    "OBSERVED_IN_FIELD",
    "RelationStateAssimilationAdapterV1",
]
