"""Core types for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class SourceRefV1:
    owner: str
    ref_id: str
    ref_type: str
    version: str
    trace_ref: str
    provenance_ref: str
    read_only: bool = True
    candidate_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class NegativeGuardStatusV1:
    flow_owns_context: bool
    flow_owns_pcn: bool
    flow_owns_intent: bool
    flow_owns_attention: bool
    flow_owns_hypothesis: bool
    flow_owns_current_world: bool
    flow_owns_dynamic_regulation: bool
    flow_owns_field: bool
    flow_owns_causal: bool
    flow_owns_memory: bool
    flow_owns_learning: bool
    flow_can_rewrite_owner_output: bool
    flow_can_create_fact: bool
    flow_can_mutate_intent: bool
    flow_can_mutate_field: bool
    flow_can_activate_parameter_genome: bool
    flow_can_execute_task: bool
    flow_can_control_device: bool
    flow_can_write_database: bool
    flow_can_call_model: bool
    flow_can_run_scheduler: bool
    runtime_execution: bool
    database_write: bool
    device_control: bool
    scheduler_execution: bool
    task_mutation: bool
    model_call: bool
    source_owner_mutation: bool
    real_side_effect: bool
    synthetic_only: bool


@dataclass(frozen=True)
class CycleSnapshotV1:
    cycle_id: str
    previous_cycle_id: str | None
    context_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    state_formation_refs: Tuple[str, ...]
    attention_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    current_world_ref: str | None
    cognitive_state_vector_ref: str | None
    regulation_candidate_ref: str | None
    field_refs: Tuple[str, ...]
    causal_refs: Tuple[str, ...]
    snapshot_id: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]


@dataclass(frozen=True)
class CycleMetadataV1:
    relationship_kinds: Dict[str, str]
    transition_trace: Tuple[str, ...] = field(default_factory=tuple)
    interrupt_trace: Tuple[str, ...] = field(default_factory=tuple)
    reconsideration_trace: Tuple[str, ...] = field(default_factory=tuple)
    inheritance_trace: Tuple[str, ...] = field(default_factory=tuple)
