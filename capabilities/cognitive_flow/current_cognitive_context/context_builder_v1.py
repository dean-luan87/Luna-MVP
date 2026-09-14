"""Controlled caller-assembly builder for Current Cognitive Context v1."""

from __future__ import annotations

from typing import Any, Mapping, Tuple

from .context_inputs_v1 import (
    AttentionContextV1,
    GoalContextV1,
    SubjectContextV1,
    TaskContextV1,
    TemporalContextV1,
)
from .context_records_v1 import ContextExclusionRecordV1, ContextInclusionRecordV1
from .context_sufficiency_v1 import ContextSufficiencyResultV1
from .current_cognitive_context_v1 import CurrentCognitiveContextV1
from .information_gap_v1 import InformationGapV1


class CurrentCognitiveContextBuildErrorV1(ValueError):
    """Stable boundary error for incomplete or inconsistent caller input."""


def _require_ref(value: str | None, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CurrentCognitiveContextBuildErrorV1(f"CONTEXT_BUILD_MISSING_{name.upper()}")
    return value.strip()


def _normalize_refs(value: Tuple[str, ...], name: str) -> Tuple[str, ...]:
    refs = tuple(_require_ref(item, name) for item in value)
    if len(set(refs)) != len(refs):
        raise CurrentCognitiveContextBuildErrorV1(f"CONTEXT_BUILD_DUPLICATE_{name.upper()}")
    return refs


def build_current_cognitive_context_v1(
    *,
    context_id: str,
    context_version: str,
    previous_context_ref: str | None,
    superseded_by_ref: str | None,
    lifecycle_status: str,
    field_ref: str,
    snapshot_ref: str,
    subject_context: SubjectContextV1,
    task_context: TaskContextV1,
    goal_context: GoalContextV1,
    temporal_context: TemporalContextV1,
    attention_context: AttentionContextV1,
    schema_refs: Tuple[str, ...],
    selected_field_unit_refs: Tuple[str, ...],
    selected_relation_refs: Tuple[str, ...],
    selected_state_refs: Tuple[str, ...],
    selected_history_refs: Tuple[str, ...],
    selected_evidence_refs: Tuple[str, ...],
    inclusion_records: Tuple[ContextInclusionRecordV1, ...],
    exclusion_records: Tuple[ContextExclusionRecordV1, ...],
    information_gaps: Tuple[InformationGapV1, ...],
    sufficiency_result: ContextSufficiencyResultV1,
    context_boundary: Mapping[str, Any],
    invalidation_reasons: Tuple[str, ...],
    refresh_required: bool,
    provenance: Mapping[str, Any],
    trace: str,
    created_from_refs: Tuple[str, ...],
) -> CurrentCognitiveContextV1:
    """Assemble a Context from explicit caller choices only.

    This builder performs no relevance scoring, object selection, Snapshot read,
    Field State read, gap generation, sufficiency alteration, model invocation,
    or missing-information completion.
    """

    normalized_context_id = _require_ref(context_id, "context_id")
    normalized_version = _require_ref(context_version, "context_version")
    normalized_field = _require_ref(field_ref, "field_ref")
    normalized_snapshot = _require_ref(snapshot_ref, "snapshot_ref")
    normalized_trace = _require_ref(trace, "trace")
    if not isinstance(context_boundary, Mapping):
        raise CurrentCognitiveContextBuildErrorV1("CONTEXT_BUILD_INVALID_CONTEXT_BOUNDARY")

    normalized_schema_refs = _normalize_refs(schema_refs, "schema_ref")
    units = _normalize_refs(selected_field_unit_refs, "selected_field_unit_ref")
    relations = _normalize_refs(selected_relation_refs, "selected_relation_ref")
    states = _normalize_refs(selected_state_refs, "selected_state_ref")
    history = _normalize_refs(selected_history_refs, "selected_history_ref")
    evidence = _normalize_refs(selected_evidence_refs, "selected_evidence_ref")
    source_refs = _normalize_refs(created_from_refs, "created_from_ref")
    if normalized_snapshot not in source_refs:
        raise CurrentCognitiveContextBuildErrorV1("CONTEXT_BUILD_SNAPSHOT_SOURCE_REQUIRED")

    selected_refs = set(units + relations + states + history + evidence)
    for record in inclusion_records:
        if record.selected_object_ref not in selected_refs:
            raise CurrentCognitiveContextBuildErrorV1("CONTEXT_BUILD_INCLUSION_SELECTION_MISMATCH")
        _require_ref(record.source_ref, "inclusion_source_ref")
    for record in exclusion_records:
        if not record.excluded_for_current_context_only or not record.recoverable:
            raise CurrentCognitiveContextBuildErrorV1("CONTEXT_BUILD_EXCLUSION_RECOVERABILITY_REQUIRED")
        if record.source_snapshot_ref != normalized_snapshot:
            raise CurrentCognitiveContextBuildErrorV1("CONTEXT_BUILD_EXCLUSION_SNAPSHOT_MISMATCH")
        _require_ref(record.source_ref, "exclusion_source_ref")

    return CurrentCognitiveContextV1(
        context_id=normalized_context_id,
        context_version=normalized_version,
        previous_context_ref=previous_context_ref,
        superseded_by_ref=superseded_by_ref,
        lifecycle_status=lifecycle_status,
        field_ref=normalized_field,
        snapshot_ref=normalized_snapshot,
        subject_context=subject_context,
        task_context=task_context,
        goal_context=goal_context,
        temporal_context=temporal_context,
        attention_context=attention_context,
        schema_refs=normalized_schema_refs,
        selected_field_unit_refs=units,
        selected_relation_refs=relations,
        selected_state_refs=states,
        selected_history_refs=history,
        selected_evidence_refs=evidence,
        inclusion_records=tuple(inclusion_records),
        exclusion_records=tuple(exclusion_records),
        information_gaps=tuple(information_gaps),
        sufficiency_result=sufficiency_result,
        context_boundary=dict(context_boundary),
        invalidation_reasons=tuple(invalidation_reasons),
        refresh_required=bool(refresh_required),
        provenance=dict(provenance),
        trace=normalized_trace,
        created_from_refs=source_refs,
    )
