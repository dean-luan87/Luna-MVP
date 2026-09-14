"""Candidate-only downstream influence handoff types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DynamicRegulationHandoffCandidateV1:
    handoff_id: str
    producer_owner: str
    regulation_candidate_ref: str
    influence_candidate_refs: Tuple[str, ...]
    consumer_owner_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    attention_mutation: bool = False
    intent_mutation: bool = False
    hypothesis_mutation: bool = False
    causal_mutation: bool = False
    emotion_mutation: bool = False
    learning_direct_activation: bool = False
    scheduler_execution: bool = False
    task_mutation: bool = False
    runtime_command: bool = False
    device_control: bool = False
