"""Static registries for the single Personality Governance owner."""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping, Tuple

CANONICAL_OWNER = "Personality Governance"
MODULE_VERSION = "personality-governance-v1"
SCHEMA_VERSION = "personality-governance-schema-v1"
CONTRACT_VERSION = "personality-governance-contract-v1"

TRAIT_DIMENSIONS: Tuple[str, ...] = (
    "interaction_style",
    "expressiveness",
    "initiative_tendency",
    "social_openness",
    "caution_tendency",
    "exploration_tendency",
    "persistence_tendency",
    "adaptability",
    "empathy_expression_tendency",
    "humor_expression_tendency",
    "directness",
    "formality",
    "risk_tolerance_candidate",
    "uncertainty_tolerance_candidate",
    "attachment_expression_tendency",
    "conflict_style_candidate",
    "support_style_candidate",
    "reflection_tendency",
)

STABILITY_STATES: Tuple[str, ...] = (
    "EMERGING",
    "TENTATIVE",
    "SEMI_STABLE",
    "STABLE_CANDIDATE",
    "CONTESTED",
    "REVISING",
    "SUPERSEDED",
    "REVOKED",
    "EXPIRED",
)

ADMISSION_STATES: Tuple[str, ...] = (
    "PROPOSED",
    "EVIDENCE_ACCUMULATING",
    "ELIGIBLE",
    "INSUFFICIENT_EVIDENCE",
    "CONTESTED",
    "NEEDS_CONFIRMATION",
    "ADMITTED_CANDIDATE",
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

IDEMPOTENCY_GUARDS: Tuple[str, ...] = (
    "duplicate_personality_evidence_guard",
    "duplicate_trait_candidate_guard",
    "duplicate_profile_update_guard",
    "duplicate_revision_guard",
    "duplicate_revocation_guard",
    "duplicate_supersession_guard",
    "replayed_evidence_guard",
    "explicit_user_correction_precedence",
)

SEMANTIC_COMPRESSION_STATUS = "DEFERRED_TO_EMOTION_ENGINE"

NEGATIVE_GUARDS: Mapping[str, bool] = MappingProxyType({
    "personality_can_mutate_self": False,
    "personality_can_mutate_memory": False,
    "personality_can_execute_learning": False,
    "personality_can_mutate_intent": False,
    "personality_can_mutate_pcn": False,
    "personality_can_mutate_emotion": False,
    "personality_can_mutate_regulation_parameters": False,
    "personality_can_activate_parameter_genome": False,
    "personality_can_create_task": False,
    "personality_can_control_device": False,
    "personality_can_run_scheduler": False,
    "personality_can_call_model": False,
    "database_write": False,
    "vector_store_write": False,
    "embedding_execution": False,
    "runtime_execution": False,
    "source_owner_mutation": False,
    "cross_user_transfer": False,
    "semantic_compression_execution": False,
    "affective_memory_compression": False,
    "emotion_memory_summary_generation": False,
    "personality_memory_semantic_fusion": False,
    "real_side_effect": False,
    "trait_activation": False,
    "profile_action_control": False,
    "profile_intent_control": False,
    "fact_admission": False,
    "synthetic_only": True,
    "candidate_only": True,
})

FORBIDDEN_PARALLEL_OWNERS: Tuple[str, ...] = (
    "trait_governance",
    "profile_governance",
    "persona_governance",
    "temperament_governance",
    "emotion_personality_governance",
    "character_governance",
)
