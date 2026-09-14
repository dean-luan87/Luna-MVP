"""Static registries for Decision Governance controlled implementation v1."""

from __future__ import annotations

from typing import Dict, Tuple


DECISION_OWNER = "Decision Governance"
LEGACY_ALIASES: Tuple[str, ...] = (
    "Decision Arbitration",
    "Brain Decision",
    "Decision Commitment",
)
ACTION_CONSUMER_OWNER = "Action Boundary"
TASK_CONSUMER_OWNER = "Task Manager"

STATE_SET = {
    "PROPOSED",
    "ELIGIBLE",
    "CONSTRAINED",
    "CONTESTED",
    "DEFERRED",
    "ABSTAINED",
    "NEEDS_MORE_EVIDENCE",
    "NEEDS_CONFIRMATION",
    "SELECTED_CANDIDATE",
    "REJECTED",
    "SUSPENDED",
    "REVISED",
    "REVOKED",
}

NEGATIVE_GUARD_FLAGS: Dict[str, bool] = {
    "intent_not_decision": True,
    "causal_not_decision": True,
    "correlation_not_decision_authority": True,
    "model_suggestion_not_decision_authority": True,
    "memory_preference_not_decision_authority": True,
    "emotion_not_decision_authority": True,
    "utility_not_permission": True,
    "risk_not_safety_authority": True,
    "preferred_candidate_not_executable_action": True,
    "selected_candidate_not_task": True,
    "decision_layer_not_action_executor": True,
    "decision_layer_not_task_creator": True,
    "no_permission_bypass": True,
    "no_safety_bypass": True,
    "no_fabricated_confirmation": True,
    "no_runtime_side_effect": True,
    "no_database_write": True,
    "no_source_mutation": True,
}
