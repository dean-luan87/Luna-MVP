"""Core immutable references and guard status for controlled regulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Tuple


@dataclass(frozen=True)
class SourceRefV1:
    owner: str
    ref_id: str
    ref_type: str
    trace_ref: str
    provenance_ref: str
    read_only: bool = True
    reference_only: bool = True
    candidate_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class RegulationPolicyRefV1:
    policy_id: str
    version: str
    owner: str
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class RegulationFunctionIdentityV1:
    function_id: str
    version: str
    deterministic: bool = True
    inspectable: bool = True
    traceable: bool = True
    bounded_output_required: bool = True


@dataclass(frozen=True)
class NegativeGuardStatusV1:
    integration_has_no_parallel_owner: bool = True
    source_mutation: bool = False
    intent_mutation: bool = False
    attention_mutation: bool = False
    hypothesis_mutation: bool = False
    causal_mutation: bool = False
    emotion_mutation: bool = False
    learning_direct_activation: bool = False
    database_write: bool = False
    device_control: bool = False
    scheduler_execution: bool = False
    task_mutation: bool = False
    runtime_side_effect: bool = False
    model_call: bool = False
    parameter_bounds_bypass: bool = False
    parameter_genome_auto_activation: bool = False
    cross_user_genome_propagation: bool = False
    silent_parameter_coercion: bool = False


@dataclass(frozen=True)
class ReverseLookupIndexV1:
    by_output_ref: Mapping[str, Tuple[str, ...]] = field(default_factory=dict)
