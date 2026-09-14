"""Static registry for Cognitive Learning controlled implementation v1."""

from __future__ import annotations

from typing import Dict, Tuple

CANONICAL_OWNER = "Cognitive Learning Governance"
MODULE_VERSION = "cognitive-learning-v1"
SCHEMA_VERSION = "cognitive-learning-schema-v1"
CONTRACT_VERSION = "cognitive-learning-contract-v1"

LEARNING_KINDS: Tuple[str, ...] = (
    "SUCCESS_PATTERN",
    "FAILURE_PATTERN",
    "PREFERENCE_PATTERN",
    "CONTEXT_DEPENDENT_PATTERN",
    "INTERACTION_PATTERN",
    "RESOURCE_PATTERN",
    "ATTENTION_PATTERN",
    "HYPOTHESIS_RESOLUTION_PATTERN",
    "REGULATION_EFFECT_PATTERN",
    "TASK_EXPERIENCE_PATTERN",
    "SOCIAL_PATTERN",
    "TEMPORAL_PATTERN",
    "CONTRADICTION_PATTERN",
    "USER_FEEDBACK_PATTERN",
    "UNCERTAINTY_PATTERN",
    "NEGATIVE_EVIDENCE_PATTERN",
    "UNRESOLVED_PATTERN",
)

GENERALIZATION_LEVELS: Tuple[str, ...] = (
    "INSTANCE_ONLY",
    "LOCAL_CONTEXT",
    "TEMPORAL_PATTERN",
    "ROLE_CONTEXT",
    "RELATIONSHIP_CONTEXT",
    "DOMAIN_PATTERN",
    "CROSS_CONTEXT_CANDIDATE",
)

ADMISSION_STATES: Tuple[str, ...] = (
    "PROPOSED",
    "EVIDENCE_ACCUMULATING",
    "ELIGIBLE",
    "CONTESTED",
    "INSUFFICIENT_EVIDENCE",
    "NEEDS_CONFIRMATION",
    "LEARNING_CANDIDATE_READY",
    "PARAMETER_UPDATE_CANDIDATE_READY",
    "REVISED",
    "SUPERSEDED",
    "REVOKED",
    "EXPIRED",
    "REJECTED",
)

SENSITIVITY_LEVELS: Tuple[str, ...] = (
    "NORMAL",
    "SENSITIVE",
    "HIGH_SENSITIVITY",
    "USER_CONFIRMATION_REQUIRED",
    "DO_NOT_GENERALIZE",
    "DO_NOT_TRANSFER",
    "DO_NOT_PERSIST_CANDIDATE",
)

NEGATIVE_GUARDS: Dict[str, bool] = {
    "learning_can_create_fact": False,
    "learning_can_mutate_memory": False,
    "learning_can_mutate_context": False,
    "learning_can_mutate_pcn": False,
    "learning_can_mutate_intent": False,
    "learning_can_mutate_attention": False,
    "learning_can_declare_hypothesis_truth": False,
    "learning_can_mutate_current_world": False,
    "learning_can_mutate_state_vector": False,
    "learning_can_mutate_causal": False,
    "learning_can_mutate_regulation_parameter": False,
    "learning_can_bypass_parameter_bounds": False,
    "learning_can_activate_parameter": False,
    "learning_can_activate_genome": False,
    "learning_can_mutate_self": False,
    "learning_can_mutate_personality": False,
    "learning_can_mutate_emotion": False,
    "learning_can_create_task": False,
    "learning_can_control_device": False,
    "learning_can_run_scheduler": False,
    "learning_can_call_model": False,
    "database_write": False,
    "vector_store_write": False,
    "embedding_execution": False,
    "runtime_training": False,
    "model_weight_update": False,
    "source_owner_mutation": False,
    "cross_user_transfer": False,
    "semantic_compression_execution": False,
    "real_side_effect": False,
    "planning_only": True,
}
