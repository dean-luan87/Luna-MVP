"""Static registry for Cognitive State Formation controlled implementation v1."""

from __future__ import annotations

from typing import Dict, Tuple

CANONICAL_OWNER = "Cognitive State Formation Governance"

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
