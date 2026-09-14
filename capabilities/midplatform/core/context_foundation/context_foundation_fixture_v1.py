# -*- coding: utf-8 -*-
"""Synthetic, immutable Context Foundation fixture set v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.context_foundation.context_carryover_types_v1 import (
    ContinuityTypeV1,
    MentalFieldContinuityReferenceV1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_types_v1 import (
    ContextAssemblyInputV1,
    TemporalScopeReferenceV1,
)
from capabilities.midplatform.core.context_foundation.context_projection_types_v1 import (
    ProjectionKindV1,
    ProjectionReferenceV1,
    UnknownStateV1,
)


@dataclass(frozen=True)
class ContextFoundationFixtureCaseV1:
    case_id: str
    description: str
    assembly_input: ContextAssemblyInputV1
    forbidden_outputs: Tuple[str, ...]
    synthetic_only: bool = True


def _projection(
    kind: ProjectionKindV1,
    owner: str,
    projection_id: str,
    unknown_state: UnknownStateV1 = UnknownStateV1.KNOWN,
    confidence: float | None = 0.9,
) -> ProjectionReferenceV1:
    return ProjectionReferenceV1(
        source_owner=owner,
        projection_id=projection_id,
        projection_version="projection-v1",
        timestamp="2026-08-10T09:00:00Z",
        validity="fixture-valid",
        confidence=confidence,
        unknown_state=unknown_state.value,
        provenance=(f"synthetic:{projection_id}",),
        projection_kind=kind.value,
        trace_reference=f"trace:{projection_id}",
        read_only=True,
        reference_only=True,
        source_mutation_allowed=False,
    )


def _scope(case_id: str) -> TemporalScopeReferenceV1:
    return TemporalScopeReferenceV1(
        scope_id=f"scope:{case_id}",
        valid_from_reference="fixture-time:start",
        valid_until_reference="fixture-time:end",
        expiry_condition_reference="fixture-condition:expiry",
        reset_condition_reference="fixture-condition:reset",
        reference_only=True,
    )


def get_context_foundation_fixture_cases_v1(
) -> Tuple[ContextFoundationFixtureCaseV1, ...]:
    work_to_home = ContextFoundationFixtureCaseV1(
        case_id="CF-01-WORK-TO-HOME",
        description="Physical Field changes to Home while work pressure remains a reference.",
        assembly_input=ContextAssemblyInputV1(
            context_id="context:work-to-home",
            version="context-v1",
            temporal_scope=_scope("work-to-home"),
            field_projection_reference=_projection(
                ProjectionKindV1.FIELD,
                "Field State System",
                "field:home",
            ),
            memory_projection_reference=_projection(
                ProjectionKindV1.MEMORY,
                "Memory System",
                "memory:recent-project-pressure",
                UnknownStateV1.UNCERTAIN,
                0.7,
            ),
            role_projection_reference=_projection(
                ProjectionKindV1.ROLE,
                "Role System / Social Self",
                "role:employee-residual",
            ),
            emotion_projection_reference=_projection(
                ProjectionKindV1.EMOTION,
                "Emotion Context Boundary / Integration Layer",
                "emotion:residual-stress-reference",
                UnknownStateV1.UNCERTAIN,
                0.6,
            ),
            mental_field_continuity_reference=MentalFieldContinuityReferenceV1(
                continuity_id="continuity:office-to-home",
                previous_field_reference="field:office",
                current_field_reference="field:home",
                continuity_type=ContinuityTypeV1.EMOTIONAL_PRESSURE.value,
                duration_scope="scope:work-to-home",
                intensity_reference="emotion:residual-stress-reference",
                activation_state="candidate",
                release_condition_reference=("condition:work-closure",),
                unknown_state=UnknownStateV1.UNCERTAIN.value,
                provenance=("synthetic:office-to-home",),
                source_owner_references=(
                    "Field State System",
                    "Emotion Context Boundary / Integration Layer",
                ),
            ),
            provenance=("fixture:CF-01-WORK-TO-HOME",),
            trace_timestamp="2026-08-10T09:00:00Z",
        ),
        forbidden_outputs=("Intent", "Causal Explanation", "Decision", "Mutation"),
    )

    weather = ContextFoundationFixtureCaseV1(
        case_id="CF-02-WEATHER-MINIMAL",
        description="Minimal Field, Observation, and temporal references for weather.",
        assembly_input=ContextAssemblyInputV1(
            context_id="context:weather-minimal",
            version="context-v1",
            temporal_scope=_scope("weather-minimal"),
            field_projection_reference=_projection(
                ProjectionKindV1.FIELD,
                "Field State System",
                "field:current-location",
            ),
            observation_projection_reference=_projection(
                ProjectionKindV1.OBSERVATION,
                "Observation Manager",
                "observation:weather-evidence",
            ),
            provenance=("fixture:CF-02-WEATHER-MINIMAL",),
            trace_timestamp="2026-08-10T09:01:00Z",
        ),
        forbidden_outputs=("Deep PCN Activation", "Intent", "Causal", "Decision"),
    )

    tired_expression = ContextFoundationFixtureCaseV1(
        case_id="CF-03-TIRED-EXPRESSION",
        description="Tiredness expression keeps cause unknown and exposes references only.",
        assembly_input=ContextAssemblyInputV1(
            context_id="context:tired-expression",
            version="context-v1",
            temporal_scope=_scope("tired-expression"),
            observation_projection_reference=_projection(
                ProjectionKindV1.OBSERVATION,
                "Observation Manager",
                "observation:tired-expression",
                UnknownStateV1.UNCERTAIN,
                0.8,
            ),
            memory_projection_reference=_projection(
                ProjectionKindV1.MEMORY,
                "Memory System",
                "memory:recent-history-candidate",
                UnknownStateV1.MULTIPLE_CANDIDATES,
                0.5,
            ),
            emotion_projection_reference=_projection(
                ProjectionKindV1.EMOTION,
                "Emotion Context Boundary / Integration Layer",
                "emotion:tiredness-context-reference",
                UnknownStateV1.UNCERTAIN,
                0.5,
            ),
            provenance=("fixture:CF-03-TIRED-EXPRESSION",),
            trace_timestamp="2026-08-10T09:02:00Z",
        ),
        forbidden_outputs=("Cause", "Intent", "Causal Explanation", "Decision"),
    )

    change_job = ContextFoundationFixtureCaseV1(
        case_id="CF-04-CHANGE-JOB",
        description="Job-change question exposes broad references without producing Intent.",
        assembly_input=ContextAssemblyInputV1(
            context_id="context:change-job",
            version="context-v1",
            temporal_scope=_scope("change-job"),
            field_projection_reference=_projection(
                ProjectionKindV1.FIELD,
                "Field State System",
                "field:work-context",
            ),
            self_projection_reference=_projection(
                ProjectionKindV1.SELF,
                "Self System",
                "self:resource-boundary-reference",
            ),
            role_projection_reference=_projection(
                ProjectionKindV1.ROLE,
                "Role System / Social Self",
                "role:employee",
            ),
            relationship_projection_reference=_projection(
                ProjectionKindV1.RELATIONSHIP,
                "Relationship System / Social Self",
                "relationship:work-stakeholder-reference",
                UnknownStateV1.MULTIPLE_CANDIDATES,
                0.6,
            ),
            memory_projection_reference=_projection(
                ProjectionKindV1.MEMORY,
                "Memory System",
                "memory:work-history-reference",
            ),
            emotion_projection_reference=_projection(
                ProjectionKindV1.EMOTION,
                "Emotion Context Boundary / Integration Layer",
                "emotion:work-state-reference",
                UnknownStateV1.UNCERTAIN,
                0.6,
            ),
            provenance=("fixture:CF-04-CHANGE-JOB",),
            trace_timestamp="2026-08-10T09:03:00Z",
        ),
        forbidden_outputs=("Recommend Quit", "Recommend Stay", "Intent", "Decision"),
    )

    return work_to_home, weather, tired_expression, change_job

