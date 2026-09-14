"""Static registries for Causal Governance controlled implementation v1."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.core.causal_governance.causal_state_types_v1 import (
    STATE_CANDIDATES_V1,
)


CAUSAL_OWNER = "Causal Governance"
LEGACY_CAUSAL_ALIAS = "Causal Reasoning Governance"
DECISION_CONSUMER_OWNER = "Decision Arbitration"

ALLOWED_SOURCE_OWNERS: Tuple[str, ...] = (
    "Observation Governance",
    "Context Governance",
    "Memory Governance",
    "Intent Governance",
    "Cognitive Field",
    "Field Governance",
    "Causal Governance",
)

FORBIDDEN_AUTHORITY_TOKENS: Tuple[str, ...] = (
    "Decision",
    "Action",
    "Task",
    "Runtime",
    "Database",
)

NEGATIVE_GUARD_FLAGS: Dict[str, bool] = {
    "temporal_precedence_not_causality": True,
    "correlation_not_causality": True,
    "model_output_not_causal_fact": True,
    "memory_prior_not_causal_fact": True,
    "intent_preference_not_causal_conclusion": True,
    "emotion_not_causal_authority": True,
    "field_context_not_causal_authority": True,
    "causal_hypothesis_not_decision": True,
    "causal_result_not_action": True,
    "causal_layer_not_task_creator": True,
}

DEFAULT_STATE = "PROPOSED"
STATE_SET = set(STATE_CANDIDATES_V1)
