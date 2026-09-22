"""Static registry for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from typing import Dict, Tuple

CANONICAL_OWNER = "Cognitive State Formation Governance"
COGNITIVE_STATE_VERSION_OWNER = CANONICAL_OWNER

COGNITIVE_STATE_VERSION_VALID = "VALID"
COGNITIVE_STATE_VERSION_INVALIDATED = "INVALIDATED"

COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL = (
    "cognitive-state-profile:production-canonical"
)
COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1 = (
    "cognitive-state-profile:controlled-evaluation-v1"
)

COGNITIVE_STATE_VERSION_PROFILES: Tuple[str, ...] = (
    COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL,
    COGNITIVE_STATE_PROFILE_CONTROLLED_EVALUATION_V1,
)


def resolve_cognitive_state_version_profile_v1(
    profile_ref: str | None,
) -> str | None:
    """Resolve an owner-defined profile; omitted means production canonical."""
    if profile_ref is None:
        return COGNITIVE_STATE_PROFILE_PRODUCTION_CANONICAL
    if not isinstance(profile_ref, str) or not profile_ref.strip():
        return None
    if profile_ref not in COGNITIVE_STATE_VERSION_PROFILES:
        return None
    return profile_ref

UPSTREAM_OWNERS: Tuple[str, ...] = (
    "Context Foundation",
    "Personal Cognitive Network Governance",
    "Intent Governance",
    "Field State Reducer",
)

DOWNSTREAM_OWNERS: Tuple[str, ...] = (
    "Causal Governance",
    "Decision Governance",
)

FORBIDDEN_AUTHORITY_TOKENS: Tuple[str, ...] = (
    "Field Mutation",
    "Intent Mutation",
    "Causal Mutation",
    "Decision",
    "Action",
    "Task",
    "Runtime",
    "Database",
    "Device",
    "Scheduler",
)

OUTPUT_FORBIDDEN_FIELDS: Tuple[str, ...] = (
    "decision_output",
    "action_output",
    "task_output",
    "runtime_execution_request",
    "database_write",
)

NEGATIVE_GUARDS: Dict[str, bool] = {
    "integration_module_not_field_owner": True,
    "current_world_not_field_state": True,
    "cognitive_hypothesis_not_causal_hypothesis": True,
    "attention_not_decision_priority": True,
    "attention_not_action_priority": True,
    "context_mutation": False,
    "pcn_mutation": False,
    "intent_mutation": False,
    "field_mutation": False,
    "causal_mutation": False,
    "decision_output": False,
    "action_output": False,
    "task_output": False,
    "database_write": False,
    "device_control": False,
    "scheduler_execution": False,
    "runtime_side_effect": False,
    "model_call": False,
    "learning_update": False,
    "self_regulation_update": False,
    "dynamic_parameter_mutation": False,
    "single_truth_collapse": False,
}

WORLD_STATE_KINDS: Tuple[str, ...] = (
    "PARTIAL",
    "UNKNOWN",
    "CONFLICTED",
    "MULTI_HYPOTHESIS",
    "STABLE_CANDIDATE",
)

HYPOTHESIS_STATES: Tuple[str, ...] = (
    "PROPOSED",
    "SUPPORTED",
    "CONTESTED",
    "INSUFFICIENT_EVIDENCE",
    "SUSPENDED",
    "REVISED",
    "REJECTED",
    "REVOKED",
)
