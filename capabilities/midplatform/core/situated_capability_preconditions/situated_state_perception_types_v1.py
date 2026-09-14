"""Candidate contracts for deriving situated conditions from state inputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from capabilities.midplatform.field_perception_orchestrator.integration.active_observation_precondition_types_v1 import (
    RelativeObservationStateV1,
    SelfPerceptualViewpointStateV1,
)
from .situated_capability_precondition_types_v1 import (
    SituatedCapabilityStateV1,
    SituatedConditionStateCandidateV1,
)


OWNER = "Capability Admission / Capability Governance"
CONDITION_STATUSES = ("SATISFIED", "UNSATISFIED", "UNKNOWN")
SITUATED_CONDITION_REFS = (
    "condition:target-visible:v1",
    "condition:target-complete:v1",
    "condition:target-scale-adequate:v1",
    "condition:stable-relation:v1",
)


@dataclass(frozen=True)
class SituatedStatePerceptionRequestV1:
    """Raw Self/Field/Target/Relation candidates for one situated assessment."""

    case_id: str
    state_id: str
    cycle_index: int
    temporal_ref: str
    capability_requirement_ref: str
    situated_state_ref: str
    self_state: SelfPerceptualViewpointStateV1
    relative_state: RelativeObservationStateV1
    field_state_refs: Tuple[str, ...]
    target_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SituatedStatePerceptionResultV1:
    """Derived condition candidates and a state consumable by generic feasibility."""

    case_id: str
    state_id: str
    cycle_index: int
    request: SituatedStatePerceptionRequestV1
    condition_candidates: Tuple[SituatedConditionStateCandidateV1, ...]
    situated_state: SituatedCapabilityStateV1
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    behavior: Dict[str, bool] = field(default_factory=dict)
    validation_errors: Tuple[str, ...] = tuple()
    candidate_only: bool = True


__all__ = [
    "CONDITION_STATUSES",
    "OWNER",
    "SITUATED_CONDITION_REFS",
    "SituatedStatePerceptionRequestV1",
    "SituatedStatePerceptionResultV1",
]
