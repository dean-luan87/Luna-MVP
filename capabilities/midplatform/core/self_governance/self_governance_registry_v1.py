"""Static registries for the narrow Self Governance owner."""

from __future__ import annotations

from typing import Dict, Tuple

CANONICAL_OWNER = "Self Governance"
MODULE_VERSION = "self-governance-v1"
SCHEMA_VERSION = "self-governance-schema-v1"
CONTRACT_VERSION = "self-governance-contract-v1"

BOUNDARY_CLASSES: Tuple[str, ...] = (
    "SELF", "OTHER", "SHARED", "ENVIRONMENT", "SYSTEM", "UNKNOWN", "CONTESTED"
)
REFERENCE_KINDS: Tuple[str, ...] = (
    "SELF_REFERENCE", "IDENTITY_REFERENCE", "ROLE_REFERENCE",
    "CAPABILITY_REFERENCE", "LIMITATION_REFERENCE", "RELATIONSHIP_REFERENCE",
    "EXPERIENCE_REFERENCE", "MEMORY_REFERENCE", "LEARNING_REFERENCE",
    "REGULATION_REFERENCE", "EMOTIONAL_EVIDENCE_REFERENCE",
    "PERSONALITY_EVIDENCE_REFERENCE", "UNKNOWN_REFERENCE",
)
ATTRIBUTION_DOMAINS: Tuple[str, ...] = (
    "IDENTITY", "ROLE", "RELATIONSHIP_POSITION", "CAPABILITY", "LIMITATION",
    "PREFERENCE", "HABITUAL_TENDENCY", "AGENCY", "RESPONSIBILITY",
    "RESOURCE_CONDITION", "INTERACTION_STYLE", "AUTOBIOGRAPHICAL",
    "OWN_INTENT", "OWN_PREFERENCE_CANDIDATE", "OWN_EXPERIENCE", "OWN_MEMORY",
    "OWN_CAPABILITY", "OWN_LIMITATION", "OWN_ROLE", "OWN_RELATIONSHIP_POSITION",
    "OWN_REGULATION_TENDENCY", "OWN_LEARNING_PATTERN", "OWN_EMOTIONAL_EVIDENCE",
    "OWN_PERSONALITY_EVIDENCE", "OWN_ACTION_RESULT_HISTORY", "UNCERTAIN_SELF",
)
ATTRIBUTION_STATES: Tuple[str, ...] = (
    "PROPOSED", "ELIGIBLE", "INSUFFICIENT_EVIDENCE", "CONTESTED",
    "NEEDS_CONFIRMATION", "TEMPORARY", "ADMITTED_CANDIDATE", "REJECTED",
    "SUPERSEDED", "REVISED", "REVOKED", "EXPIRED",
)
STABILITY_PARTITIONS: Tuple[str, ...] = (
    "STRUCTURAL_SELF", "SEMI_STABLE_SELF", "TRANSIENT_SELF",
    "FUTURE_PERSONALITY_DERIVED_SELF",
)
SENSITIVITY_LEVELS: Tuple[str, ...] = (
    "NORMAL", "SENSITIVE", "HIGH_SENSITIVITY", "USER_CONFIRMATION_REQUIRED",
    "DO_NOT_GENERALIZE", "DO_NOT_TRANSFER", "DO_NOT_PERSIST_CANDIDATE",
)
REVISION_TRIGGERS: Tuple[str, ...] = (
    "mistaken_attribution", "stale_preference", "changed_role",
    "relationship_change", "capability_change", "limitation_change",
    "user_correction", "learning_counterexample", "identity_ambiguity",
    "source_revocation", "temporal_expiration",
)
IDEMPOTENCY_GUARDS: Tuple[str, ...] = (
    "duplicate_self_reference_guard",
    "duplicate_attribution_guard",
    "duplicate_continuity_update_guard",
    "duplicate_revision_guard",
    "duplicate_revocation_guard",
    "duplicate_supersession_guard",
    "replayed_source_evidence_guard",
    "explicit_user_correction_precedence",
)

NEGATIVE_GUARDS: Dict[str, bool] = {
    "self_can_mutate_pcn": False,
    "self_can_mutate_memory": False,
    "self_can_execute_learning": False,
    "self_can_mutate_intent": False,
    "self_can_mutate_attention": False,
    "self_can_mutate_hypothesis": False,
    "self_can_mutate_current_world": False,
    "self_can_mutate_state_vector": False,
    "self_can_mutate_regulation_parameter": False,
    "self_can_activate_parameter_genome": False,
    "self_can_mutate_personality": False,
    "self_can_mutate_emotion": False,
    "self_can_create_task": False,
    "self_can_control_device": False,
    "self_can_run_scheduler": False,
    "self_can_call_model": False,
    "database_write": False,
    "vector_store_write": False,
    "embedding_execution": False,
    "runtime_execution": False,
    "source_owner_mutation": False,
    "cross_user_transfer": False,
    "semantic_compression_execution": False,
    "real_side_effect": False,
    "synthetic_only": True,
    "candidate_only": True,
}

FORBIDDEN_PARALLEL_OWNERS: Tuple[str, ...] = (
    "identity_governance", "self_attribution_governance",
    "self_continuity_governance", "personality_governance",
    "emotion_governance",
)
