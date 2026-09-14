"""Canonical registry for Outcome Evaluation Governance v1."""

CANONICAL_OWNER = "Outcome Evaluation Governance"
MODULE_VERSION = "1.0.0"
SCHEMA_VERSION = "outcome-evaluation-v1"
CONTRACT_VERSION = "outcome-evaluation-contract-v1"

COMPARABILITY_STATES = (
    "COMPARABLE",
    "PARTIALLY_COMPARABLE",
    "NOT_COMPARABLE",
    "INSUFFICIENT_EVIDENCE",
    "STALE_ACTUAL",
    "STALE_EXPECTATION",
    "CONTESTED",
    "NEEDS_CONFIRMATION",
)

DEVIATION_STATUSES = ("MATCH", "PARTIAL_MATCH", "MISMATCH", "UNKNOWN", "CONTESTED")

RECOMMENDATIONS = (
    "NO_ACTION",
    "REOBSERVE",
    "RECONSIDER_HYPOTHESIS",
    "RECONSIDER_DECISION",
    "REPLAN_TASK",
    "RETRY_EXECUTION",
    "REQUEST_USER_CONFIRMATION",
    "DEFER",
    "FAIL_CYCLE",
    "START_NEXT_CYCLE",
)

ATTRIBUTION_KINDS = (
    "OBSERVATION_ERROR_CANDIDATE",
    "WORLD_MODEL_ERROR_CANDIDATE",
    "PREDICTION_ERROR_CANDIDATE",
    "DECISION_ERROR_CANDIDATE",
    "TASK_PLANNING_ERROR_CANDIDATE",
    "EXECUTION_ERROR_CANDIDATE",
    "CAPABILITY_ERROR_CANDIDATE",
    "TEMPORAL_VALIDITY_ERROR_CANDIDATE",
    "STALE_INFORMATION_CANDIDATE",
    "EXTERNAL_WORLD_CHANGE_CANDIDATE",
    "USER_CORRECTION_CANDIDATE",
    "INSUFFICIENT_EVIDENCE",
    "UNRESOLVED_ATTRIBUTION",
)

NEGATIVE_GUARDS = {
    "runtime_execution": False,
    "provider_invocation": False,
    "model_call": False,
    "database_write": False,
    "vector_store_write": False,
    "embedding_execution": False,
    "scheduler_execution": False,
    "device_control": False,
    "field_state_mutation": False,
    "context_mutation": False,
    "intent_mutation": False,
    "decision_mutation": False,
    "task_mutation": False,
    "action_execution": False,
    "memory_mutation": False,
    "learning_execution": False,
    "self_mutation": False,
    "personality_mutation": False,
    "dynamic_regulation_mutation": False,
    "emotion_engine_execution": False,
    "b_route_execution": False,
    "semantic_compression_execution": False,
    "cross_user_transfer": False,
    "real_side_effect": False,
}
