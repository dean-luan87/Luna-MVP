"""Counterfactual candidate types for Causal Governance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CounterfactualCandidateV1:
    counterfactual_id: str
    base_hypothesis_ref: str
    intervention_candidate: str
    expected_difference_candidate: str
    required_assumptions: Tuple[str, ...]
    uncertainty: Tuple[str, ...]
    provenance: Tuple[str, ...]
    trace_ref: str
    counterfactual_is_fact: bool = False
    counterfactual_is_decision: bool = False
    counterfactual_outputs_action: bool = False
