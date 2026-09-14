"""Immutable derived Current Cognitive Context v1 object."""

from __future__ import annotations

from dataclasses import dataclass
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
from .context_types_v1 import (
    CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1,
    ContextInvalidationReasonV1,
    ContextLifecycleStatusV1,
)
from .information_gap_v1 import InformationGapV1


@dataclass(frozen=True)
class CurrentCognitiveContextV1:
    """A derived analysis input; never a Field State, Fact, or Snapshot."""

    context_id: str
    context_version: str
    previous_context_ref: str | None
    superseded_by_ref: str | None
    lifecycle_status: str
    field_ref: str
    snapshot_ref: str
    subject_context: SubjectContextV1
    task_context: TaskContextV1
    goal_context: GoalContextV1
    temporal_context: TemporalContextV1
    attention_context: AttentionContextV1
    schema_refs: Tuple[str, ...]
    selected_field_unit_refs: Tuple[str, ...]
    selected_relation_refs: Tuple[str, ...]
    selected_state_refs: Tuple[str, ...]
    selected_history_refs: Tuple[str, ...]
    selected_evidence_refs: Tuple[str, ...]
    inclusion_records: Tuple[ContextInclusionRecordV1, ...]
    exclusion_records: Tuple[ContextExclusionRecordV1, ...]
    information_gaps: Tuple[InformationGapV1, ...]
    sufficiency_result: ContextSufficiencyResultV1
    context_boundary: Mapping[str, Any]
    invalidation_reasons: Tuple[str, ...]
    refresh_required: bool
    provenance: Mapping[str, Any]
    trace: str
    created_from_refs: Tuple[str, ...]
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1
    derived_only: bool = True
    read_only: bool = True
    field_state_mutation_executed: bool = False

    def __post_init__(self) -> None:
        lifecycle_values = {status.value for status in ContextLifecycleStatusV1}
        invalidation_values = {reason.value for reason in ContextInvalidationReasonV1}
        if self.lifecycle_status not in lifecycle_values:
            raise ValueError("unsupported Current Cognitive Context lifecycle_status")
        if any(reason not in invalidation_values for reason in self.invalidation_reasons):
            raise ValueError("unsupported Current Cognitive Context invalidation reason")
        if not self.context_id or not self.context_version or not self.field_ref or not self.snapshot_ref:
            raise ValueError("Current Cognitive Context requires stable context, Field, and Snapshot references")
