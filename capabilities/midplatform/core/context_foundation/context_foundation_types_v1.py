# -*- coding: utf-8 -*-
"""Context Foundation controlled skeleton types v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from capabilities.midplatform.core.context_foundation.context_carryover_types_v1 import (
    MentalFieldContinuityReferenceV1,
)
from capabilities.midplatform.core.context_foundation.context_projection_types_v1 import (
    ProjectionReferenceV1,
)


@dataclass(frozen=True)
class TemporalScopeReferenceV1:
    scope_id: str
    valid_from_reference: str
    valid_until_reference: str
    expiry_condition_reference: str
    reset_condition_reference: str
    reference_only: bool = True


@dataclass(frozen=True)
class ContextAssemblyInputV1:
    context_id: str
    version: str
    temporal_scope: TemporalScopeReferenceV1
    field_projection_reference: Optional[ProjectionReferenceV1] = None
    observation_projection_reference: Optional[ProjectionReferenceV1] = None
    memory_projection_reference: Optional[ProjectionReferenceV1] = None
    self_projection_reference: Optional[ProjectionReferenceV1] = None
    role_projection_reference: Optional[ProjectionReferenceV1] = None
    relationship_projection_reference: Optional[ProjectionReferenceV1] = None
    emotion_projection_reference: Optional[ProjectionReferenceV1] = None
    mental_field_continuity_reference: Optional[
        MentalFieldContinuityReferenceV1
    ] = None
    provenance: Tuple[str, ...] = field(default_factory=tuple)
    trace_timestamp: str = ""
    direct_mutation_requested: bool = False
    skeleton_only: bool = True


@dataclass(frozen=True)
class ContextEnvelopeCandidateV1:
    context_id: str
    version: str
    temporal_scope: TemporalScopeReferenceV1
    field_projection_reference: Optional[ProjectionReferenceV1]
    observation_projection_reference: Optional[ProjectionReferenceV1]
    memory_projection_reference: Optional[ProjectionReferenceV1]
    self_projection_reference: Optional[ProjectionReferenceV1]
    role_projection_reference: Optional[ProjectionReferenceV1]
    relationship_projection_reference: Optional[ProjectionReferenceV1]
    emotion_projection_reference: Optional[ProjectionReferenceV1]
    mental_field_continuity_reference: Optional[
        MentalFieldContinuityReferenceV1
    ]
    provenance: Tuple[str, ...]
    trace_reference: str
    status: str = "CONTEXT_ENVELOPE_CANDIDATE"
    candidate_only: bool = True
    reference_only: bool = True
    skeleton_only: bool = True
    real_context_generation: bool = False
    runtime_executed: bool = False
    state_mutation: bool = False
    fact_write_executed: bool = False
    intent_output_created: bool = False
    causal_output_created: bool = False
    decision_output_created: bool = False


@dataclass(frozen=True)
class ContextValidationResultV1:
    valid: bool
    issues: Tuple[str, ...] = field(default_factory=tuple)
    unknown_preserved: bool = True
    reference_only: bool = True

