"""Core shared datatypes for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class SourceRefV1:
    owner: str
    source_ref: str
    schema_version: str
    trace_ref: str
    provenance_ref: str
    read_only: bool = True
    reference_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class NegativeGuardStatusV1:
    candidate_only: bool
    context_mutation: bool
    pcn_mutation: bool
    intent_mutation: bool
    field_mutation: bool
    causal_mutation: bool
    decision_output: bool
    action_output: bool
    task_output: bool
    database_write: bool
    device_control: bool
    scheduler_execution: bool
    runtime_side_effect: bool
    model_call: bool
    learning_update: bool
    self_regulation_update: bool
    dynamic_parameter_mutation: bool
    single_truth_collapse: bool


@dataclass(frozen=True)
class TraceEnvelopeV1:
    root_trace_id: str
    attention_trace_ref: str
    hypothesis_trace_ref: str
    current_world_trace_ref: str
    downstream_handoff_trace_ref: str
    revision_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    revocation_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    source_version_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    alternative_hypothesis_lineage_refs: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ProvenanceEnvelopeV1:
    source_refs: Tuple[str, ...]
    owner_refs: Tuple[str, ...]
    version_refs: Tuple[str, ...]
    reverse_lookup: Dict[str, Tuple[str, ...]]
