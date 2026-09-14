"""Static registry for Cognitive Memory & Experience controlled implementation v1."""

from __future__ import annotations

from typing import Dict, Tuple

CANONICAL_OWNER = "Cognitive Memory & Experience Governance"
MODULE_VERSION = "cognitive-memory-experience-v1"
SCHEMA_VERSION = "cognitive-memory-experience-schema-v1"
CONTRACT_VERSION = "cognitive-memory-experience-contract-v1"

MEMORY_TYPES: Tuple[str, ...] = (
    "EPISODIC",
    "SEMANTIC",
    "RELATIONAL",
    "SELF_RELATED",
    "PREFERENCE",
    "PROCEDURAL_REFERENCE",
    "ENVIRONMENTAL_CONTEXT",
    "TASK_EXPERIENCE",
    "SOCIAL_EXPERIENCE",
    "EMOTIONAL_EXPERIENCE",
    "UNRESOLVED_EXPERIENCE",
)

ADMISSION_STATES: Tuple[str, ...] = (
    "PROPOSED",
    "ELIGIBLE",
    "INSUFFICIENT_EVIDENCE",
    "CONTESTED",
    "NEEDS_CONFIRMATION",
    "TEMPORARY",
    "ADMITTED_CANDIDATE",
    "REJECTED",
    "SUPERSEDED",
    "REVISED",
    "REVOKED",
    "EXPIRED",
)

SENSITIVITY_LEVELS: Tuple[str, ...] = (
    "NORMAL",
    "SENSITIVE",
    "HIGH_SENSITIVITY",
)

NEGATIVE_GUARDS: Dict[str, bool] = {
    "memory_can_create_fact_directly": False,
    "memory_can_mutate_field": False,
    "memory_can_mutate_context": False,
    "memory_can_mutate_pcn": False,
    "memory_can_mutate_intent": False,
    "memory_can_mutate_attention": False,
    "memory_can_mutate_hypothesis": False,
    "memory_can_mutate_current_world": False,
    "memory_can_mutate_state_vector": False,
    "memory_can_mutate_regulation_parameter": False,
    "memory_can_activate_parameter_genome": False,
    "memory_can_execute_learning": False,
    "memory_can_mutate_personality": False,
    "memory_can_create_task": False,
    "memory_can_control_device": False,
    "memory_can_run_scheduler": False,
    "memory_can_call_model": False,
    "database_write": False,
    "vector_store_write": False,
    "embedding_execution": False,
    "runtime_execution": False,
    "model_call": False,
    "source_owner_mutation": False,
    "real_side_effect": False,
    "synthetic_only": True,
    "candidate_only": True,
    "learning_execution": False,
    "personality_mutation": False,
}
