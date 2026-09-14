"""Frozen parameter bounds and explicit evaluation result types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class CognitiveParameterBoundsV1:
    bounds_id: str
    parameter_id: str
    parameter_class: str
    lower_bound: float
    upper_bound: float
    step_bound: float
    policy_ref: str
    trace_ref: str
    frozen: bool = True
    bypass_allowed: bool = False


@dataclass(frozen=True)
class ParameterBoundsEvaluationV1:
    parameter_id: str
    requested_value: object
    effective_value: Optional[float]
    within_absolute_bounds: bool
    within_step_bound: bool
    boundary_action: str
    reason_codes: Tuple[str, ...]
    rejected: bool
    constrained: bool
    silent_coercion: bool = False
