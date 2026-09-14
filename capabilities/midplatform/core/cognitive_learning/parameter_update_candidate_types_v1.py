"""Parameter update proposal types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ParameterUpdateCandidateV1:
    parameter_update_candidate_id: str
    learning_candidate_refs: Tuple[str, ...]
    target_regulation_parameter_refs: Tuple[str, ...]
    parameter_class_refs: Tuple[str, ...]
    proposed_direction: str
    proposed_delta_candidate: str
    proposed_bounds_ref: str
    expected_effect_candidate: str
    risk_candidate: str
    reversibility_candidate: str
    approval_requirement_candidate: str
    activation_allowed: bool = False
    persistence_allowed: bool = False
    genome_activation_allowed: bool = False
    source_owner_mutation: bool = False
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = ()
