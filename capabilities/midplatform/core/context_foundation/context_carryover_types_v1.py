# -*- coding: utf-8 -*-
"""Reference-only Context carryover types v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple


class ContinuityTypeV1(str, Enum):
    UNFINISHED_TASK = "unfinished_task"
    EMOTIONAL_PRESSURE = "emotional_pressure"
    ROLE_ACTIVATION = "role_activation"
    RELATIONSHIP_RESIDUAL = "relationship_residual"


@dataclass(frozen=True)
class MentalFieldContinuityReferenceV1:
    """Cross-Field continuity reference, not Memory, Emotion State, or Causal."""

    continuity_id: str
    previous_field_reference: str
    current_field_reference: str
    continuity_type: str
    duration_scope: str
    intensity_reference: str
    activation_state: str
    release_condition_reference: Tuple[str, ...] = field(default_factory=tuple)
    unknown_state: str = "unknown"
    provenance: Tuple[str, ...] = field(default_factory=tuple)
    source_owner_references: Tuple[str, ...] = field(default_factory=tuple)
    status: str = "REFERENCE_CANDIDATE"
    reference_only: bool = True
    memory_record_created: bool = False
    emotion_calculation_executed: bool = False
    emotion_mutation_executed: bool = False
    causal_explanation_created: bool = False
    source_mutation_executed: bool = False


@dataclass(frozen=True)
class ContextCarryoverCandidateV1:
    carryover_id: str
    mental_field_continuity_reference: MentalFieldContinuityReferenceV1
    temporal_scope_reference: str
    trace_reference: str
    provenance: Tuple[str, ...] = field(default_factory=tuple)
    status: str = "CONTEXT_CARRYOVER_CANDIDATE"
    reference_only: bool = True
    unknown_preserved: bool = True
    source_owner_precedence: bool = True
    state_mutation_executed: bool = False

