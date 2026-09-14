"""Static registry for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from typing import Dict, Tuple

CANONICAL_OWNER = "Cognitive Flow Governance"
MODULE_VERSION = "cognitive-flow-v1"
SCHEMA_VERSION = "cognitive-flow-schema-v1"
CONTRACT_VERSION = "cognitive-flow-contract-v1"

CYCLE_STATES: Tuple[str, ...] = (
    "IDLE",
    "INITIALIZING",
    "CONTEXT_READY",
    "INTENT_READY",
    "STATE_FORMING",
    "STATE_READY",
    "REGULATING",
    "REGULATION_READY",
    "RECONSIDERING",
    "SUSPENDED",
    "COMPLETED",
    "ABORTED",
)

RELATIONSHIP_KINDS: Tuple[str, ...] = (
    "STRICT_SEQUENCE",
    "READ_ONLY_PARALLEL",
    "OPTIONAL_REFERENCE",
    "RECONSIDERATION_FEEDBACK",
    "CYCLE_INHERITANCE",
    "DEFERRED_ASYNC_REFERENCE",
)

FORBIDDEN_OWNER_CLAIMS: Tuple[str, ...] = (
    "Context Foundation",
    "Personal Cognitive Network Governance",
    "Intent Governance",
    "Cognitive State Formation Governance",
    "Dynamic Cognitive Regulation Governance",
    "Field State Reducer",
    "Causal Governance",
    "Memory Governance",
    "Learning Governance",
)

NEGATIVE_GUARDS: Dict[str, bool] = {
    "flow_owns_context": False,
    "flow_owns_pcn": False,
    "flow_owns_intent": False,
    "flow_owns_attention": False,
    "flow_owns_hypothesis": False,
    "flow_owns_current_world": False,
    "flow_owns_dynamic_regulation": False,
    "flow_owns_field": False,
    "flow_owns_causal": False,
    "flow_owns_memory": False,
    "flow_owns_learning": False,
    "flow_can_rewrite_owner_output": False,
    "flow_can_create_fact": False,
    "flow_can_mutate_intent": False,
    "flow_can_mutate_field": False,
    "flow_can_activate_parameter_genome": False,
    "flow_can_execute_task": False,
    "flow_can_control_device": False,
    "flow_can_write_database": False,
    "flow_can_call_model": False,
    "flow_can_run_scheduler": False,
    "runtime_execution": False,
    "database_write": False,
    "device_control": False,
    "scheduler_execution": False,
    "task_mutation": False,
    "model_call": False,
    "source_owner_mutation": False,
    "real_side_effect": False,
    "synthetic_only": True,
}
