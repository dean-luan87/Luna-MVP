"""Cognitive to Causal handoff types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CognitiveToCausalHandoffCandidateV1:
    handoff_id: str
    handoff_type: str
    producer_owner: str
    consumer_owner: str
    attention_refs: Tuple[str, ...]
    active_hypothesis_refs: Tuple[str, ...]
    alternative_hypothesis_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    field_state_refs: Tuple[str, ...]
    observation_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    causal_truth: bool = False
    causal_accepted_state: bool = False
    decision_output: bool = False
    action_output: bool = False
    task_output: bool = False
    runtime_command: bool = False
