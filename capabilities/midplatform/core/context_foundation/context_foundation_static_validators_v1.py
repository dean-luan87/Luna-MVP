# -*- coding: utf-8 -*-
"""Static boundary validators for Context Foundation skeleton v1."""

from __future__ import annotations

from dataclasses import fields
from typing import Iterable, List, Tuple

from capabilities.midplatform.core.context_foundation.context_carryover_types_v1 import (
    ContinuityTypeV1,
    MentalFieldContinuityReferenceV1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_types_v1 import (
    ContextAssemblyInputV1,
    ContextEnvelopeCandidateV1,
    ContextValidationResultV1,
)
from capabilities.midplatform.core.context_foundation.context_projection_types_v1 import (
    ProjectionKindV1,
    ProjectionReferenceV1,
    UnknownStateV1,
)


OWNER_BY_KIND = {
    ProjectionKindV1.FIELD.value: "Field State System",
    ProjectionKindV1.OBSERVATION.value: "Observation Manager",
    ProjectionKindV1.MEMORY.value: "Memory System",
    ProjectionKindV1.SELF.value: "Self System",
    ProjectionKindV1.ROLE.value: "Role System / Social Self",
    ProjectionKindV1.RELATIONSHIP.value: "Relationship System / Social Self",
    ProjectionKindV1.EMOTION.value: "Emotion Context Boundary / Integration Layer",
}


def projection_references(
    request: ContextAssemblyInputV1,
) -> Tuple[ProjectionReferenceV1, ...]:
    candidates = (
        request.field_projection_reference,
        request.observation_projection_reference,
        request.memory_projection_reference,
        request.self_projection_reference,
        request.role_projection_reference,
        request.relationship_projection_reference,
        request.emotion_projection_reference,
    )
    return tuple(item for item in candidates if item is not None)


def _result(issues: Iterable[str]) -> ContextValidationResultV1:
    issue_tuple = tuple(issues)
    return ContextValidationResultV1(valid=not issue_tuple, issues=issue_tuple)


def validate_projection_owner_exists(
    projection: ProjectionReferenceV1,
) -> ContextValidationResultV1:
    issues: List[str] = []
    if not projection.source_owner:
        issues.append("projection_owner_missing")
    expected_owner = OWNER_BY_KIND.get(projection.projection_kind)
    if expected_owner is None:
        issues.append("projection_kind_unknown")
    elif projection.source_owner != expected_owner:
        issues.append("projection_owner_mismatch")
    return _result(issues)


def validate_projection_reference_complete(
    projection: ProjectionReferenceV1,
) -> ContextValidationResultV1:
    issues: List[str] = []
    required_values = {
        "projection_id": projection.projection_id,
        "projection_version": projection.projection_version,
        "timestamp": projection.timestamp,
        "validity": projection.validity,
        "unknown_state": projection.unknown_state,
        "trace_reference": projection.trace_reference,
    }
    for name, value in required_values.items():
        if not value:
            issues.append(f"missing_{name}")
    if not projection.provenance:
        issues.append("missing_provenance")
    if projection.confidence is not None and not 0.0 <= projection.confidence <= 1.0:
        issues.append("confidence_out_of_range")
    if projection.read_only is not True:
        issues.append("projection_must_be_read_only")
    if projection.reference_only is not True:
        issues.append("projection_must_be_reference_only")
    if projection.source_mutation_allowed is not False:
        issues.append("source_mutation_forbidden")
    return _result(issues)


def validate_unknown_preserved(
    projection: ProjectionReferenceV1,
) -> ContextValidationResultV1:
    allowed = {item.value for item in UnknownStateV1}
    return _result(
        ()
        if projection.unknown_state in allowed
        else ("unknown_state_not_preserved",)
    )


def validate_context_input(
    request: ContextAssemblyInputV1,
) -> ContextValidationResultV1:
    issues: List[str] = []
    if not request.context_id:
        issues.append("context_id_missing")
    if not request.version:
        issues.append("context_version_missing")
    if not request.temporal_scope.scope_id:
        issues.append("temporal_scope_missing")
    if request.temporal_scope.reference_only is not True:
        issues.append("temporal_scope_must_be_reference_only")
    if request.direct_mutation_requested:
        issues.append("direct_mutation_forbidden")
    if request.skeleton_only is not True:
        issues.append("skeleton_only_required")
    projections = projection_references(request)
    if not projections:
        issues.append("at_least_one_projection_required")
    projection_ids = [item.projection_id for item in projections]
    if len(projection_ids) != len(set(projection_ids)):
        issues.append("duplicate_projection_id")
    for projection in projections:
        for result in (
            validate_projection_owner_exists(projection),
            validate_projection_reference_complete(projection),
            validate_unknown_preserved(projection),
        ):
            issues.extend(result.issues)
    if request.mental_field_continuity_reference is not None:
        issues.extend(
            validate_carryover_reference_only(
                request.mental_field_continuity_reference
            ).issues
        )
    return _result(issues)


def validate_context_no_fact_write(
    context: ContextEnvelopeCandidateV1,
) -> ContextValidationResultV1:
    issues = []
    if context.fact_write_executed:
        issues.append("fact_write_forbidden")
    if hasattr(context, "fact") or hasattr(context, "reality_override"):
        issues.append("fact_field_forbidden")
    return _result(issues)


def validate_context_no_intent_output(
    context: ContextEnvelopeCandidateV1,
) -> ContextValidationResultV1:
    issues = []
    if context.intent_output_created:
        issues.append("intent_output_forbidden")
    if hasattr(context, "intent") or hasattr(context, "intent_candidate"):
        issues.append("intent_field_forbidden")
    return _result(issues)


def validate_context_no_causal_output(
    context: ContextEnvelopeCandidateV1,
) -> ContextValidationResultV1:
    issues = []
    if context.causal_output_created:
        issues.append("causal_output_forbidden")
    if hasattr(context, "causal_explanation") or hasattr(context, "cause"):
        issues.append("causal_field_forbidden")
    return _result(issues)


def validate_context_no_mutation_authority(
    context: ContextEnvelopeCandidateV1,
) -> ContextValidationResultV1:
    issues = []
    if context.state_mutation:
        issues.append("state_mutation_forbidden")
    if context.runtime_executed:
        issues.append("runtime_execution_forbidden")
    if context.real_context_generation:
        issues.append("real_context_generation_forbidden")
    return _result(issues)


def validate_carryover_reference_only(
    carryover: MentalFieldContinuityReferenceV1,
) -> ContextValidationResultV1:
    issues: List[str] = []
    required = {
        "continuity_id": carryover.continuity_id,
        "previous_field_reference": carryover.previous_field_reference,
        "current_field_reference": carryover.current_field_reference,
        "duration_scope": carryover.duration_scope,
        "intensity_reference": carryover.intensity_reference,
        "activation_state": carryover.activation_state,
    }
    for name, value in required.items():
        if not value:
            issues.append(f"missing_{name}")
    if carryover.continuity_type not in {item.value for item in ContinuityTypeV1}:
        issues.append("continuity_type_invalid")
    if carryover.reference_only is not True:
        issues.append("carryover_reference_only_required")
    forbidden_flags = (
        carryover.memory_record_created,
        carryover.emotion_calculation_executed,
        carryover.emotion_mutation_executed,
        carryover.causal_explanation_created,
        carryover.source_mutation_executed,
    )
    if any(forbidden_flags):
        issues.append("carryover_boundary_violation")
    if not carryover.provenance or not carryover.source_owner_references:
        issues.append("carryover_provenance_or_owner_missing")
    return _result(issues)


def validate_context_envelope_boundary(
    context: ContextEnvelopeCandidateV1,
) -> ContextValidationResultV1:
    issues: List[str] = []
    for result in (
        validate_context_no_fact_write(context),
        validate_context_no_intent_output(context),
        validate_context_no_causal_output(context),
        validate_context_no_mutation_authority(context),
    ):
        issues.extend(result.issues)
    if context.candidate_only is not True:
        issues.append("context_candidate_only_required")
    if context.reference_only is not True:
        issues.append("context_reference_only_required")
    if context.skeleton_only is not True:
        issues.append("context_skeleton_only_required")
    if not context.trace_reference:
        issues.append("context_trace_reference_missing")
    if not context.provenance:
        issues.append("context_provenance_missing")
    forbidden_field_names = {
        "intent",
        "goal",
        "causal_explanation",
        "decision",
        "action",
        "memory_mutation",
        "field_mutation",
    }
    actual_field_names = {item.name for item in fields(context)}
    if actual_field_names & forbidden_field_names:
        issues.append("forbidden_context_field_present")
    return _result(issues)

