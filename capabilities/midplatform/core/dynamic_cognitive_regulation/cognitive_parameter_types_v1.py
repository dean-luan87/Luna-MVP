"""Candidate-only cognitive parameter representations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple, Union


NumericInput = Union[int, float]


@dataclass(frozen=True)
class CognitiveParameterCandidateV1:
    parameter_id: str
    parameter_kind: str
    parameter_class: str
    current_value: NumericInput
    requested_value: object
    field_scope: str
    evidence_refs: Tuple[str, ...]
    policy_ref: str
    trace_ref: str
    parameter_version: str
    owner_approved: bool = False
    human_confirmed: bool = False
    expiry_ref: Optional[str] = None
    expired: bool = False
    learning_update_candidate: bool = False
    candidate_only: bool = True
    auto_apply: bool = False


@dataclass(frozen=True)
class ParameterModulationCandidateV1:
    modulation_id: str
    parameter_id: str
    parameter_kind: str
    parameter_class: str
    requested_value: object
    effective_value: Optional[float]
    prior_value: float
    evaluation_status: str
    boundary_action: str
    reason_codes: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    policy_ref: str
    bounds_ref: str
    parameter_version: str
    trace_ref: str
    candidate_only: bool = True
    auto_applied: bool = False
    persisted: bool = False
    silent_coercion: bool = False


@dataclass(frozen=True)
class ParameterConflictCandidateV1:
    conflict_id: str
    parameter_id: str
    modulation_refs: Tuple[str, ...]
    requested_values: Tuple[object, ...]
    resolution_status: str = "PRESERVED_UNRESOLVED"
    winner_selected: bool = False
    candidate_only: bool = True
