"""Static registry for the single Dynamic Cognitive Regulation module."""

from __future__ import annotations

from typing import Dict, Tuple


CANONICAL_OWNER = "Dynamic Cognitive Regulation Governance"
MODULE_VERSION = "dynamic-cognitive-regulation-v1"
REGULATION_FUNCTION_ID = "deterministic-bounded-regulation-v1"

INTERNAL_SUBSYSTEMS: Tuple[str, ...] = (
    "Dynamic Function",
    "Self-Regulation",
    "Parameter Governance",
    "Parameter Bounds",
    "Parameter Genome Candidate",
    "Trace and Revision",
)

FORBIDDEN_PARALLEL_OWNERS: Tuple[str, ...] = (
    "Dynamic Function Governance",
    "Self Regulation Governance",
    "Parameter Governance",
    "Parameter Genome Governance",
)

PARAMETER_CLASSES: Dict[str, Dict[str, bool]] = {
    "A": {
        "auto_modify_allowed": False,
        "bounded_modulation_allowed": False,
        "owner_approval_required": True,
        "human_confirmation_required": True,
        "expiry_required": False,
        "candidate_only": True,
    },
    "B": {
        "auto_modify_allowed": False,
        "bounded_modulation_allowed": True,
        "owner_approval_required": True,
        "human_confirmation_required": True,
        "expiry_required": False,
        "candidate_only": True,
    },
    "C": {
        "auto_modify_allowed": False,
        "bounded_modulation_allowed": True,
        "owner_approval_required": True,
        "human_confirmation_required": False,
        "expiry_required": False,
        "candidate_only": True,
    },
    "D": {
        "auto_modify_allowed": True,
        "bounded_modulation_allowed": True,
        "owner_approval_required": False,
        "human_confirmation_required": False,
        "expiry_required": True,
        "candidate_only": True,
    },
    "E": {
        "auto_modify_allowed": False,
        "bounded_modulation_allowed": False,
        "owner_approval_required": True,
        "human_confirmation_required": True,
        "expiry_required": False,
        "candidate_only": True,
    },
}

REQUIRED_PARAMETER_KINDS: Tuple[str, ...] = (
    "attention_modulation",
    "salience_modulation",
    "explore_exploit_tendency",
    "confidence_threshold",
    "persistence_decay",
    "resource_allocation",
    "interaction_intensity",
    "reconsideration_sensitivity",
)

LIFECYCLE_STATES: Tuple[str, ...] = (
    "OBSERVED",
    "ASSESSED",
    "CANDIDATE",
    "UNDER_REVIEW",
    "DEFERRED",
    "REVISED",
    "REVOKED",
)

EVALUATION_STATUSES: Tuple[str, ...] = (
    "NO_CHANGE",
    "BOUNDED_ELIGIBLE",
    "CONSTRAINED",
    "DEFERRED",
    "REJECTED",
    "REVISED",
    "REVOKED",
    "CONFLICTS_PRESERVED",
    "CANDIDATE_ONLY_NO_AUTO_APPLY",
    "EXPIRED_NOT_REUSED",
)

NEGATIVE_GUARDS: Dict[str, bool] = {
    "integration_has_no_parallel_owner": True,
    "source_mutation": False,
    "intent_mutation": False,
    "attention_mutation": False,
    "hypothesis_mutation": False,
    "causal_mutation": False,
    "emotion_mutation": False,
    "learning_direct_activation": False,
    "database_write": False,
    "device_control": False,
    "scheduler_execution": False,
    "task_mutation": False,
    "runtime_side_effect": False,
    "model_call": False,
    "parameter_bounds_bypass": False,
    "parameter_genome_auto_activation": False,
    "cross_user_genome_propagation": False,
    "silent_parameter_coercion": False,
}

DOWNSTREAM_INFLUENCE_KINDS: Tuple[str, ...] = (
    "attention_modulation_candidate",
    "salience_modulation_candidate",
    "exploration_exploitation_bias_candidate",
    "confidence_threshold_candidate",
    "persistence_decay_candidate",
    "resource_allocation_candidate",
    "interaction_intensity_candidate",
    "reconsideration_sensitivity_candidate",
    "emotion_aware_modulation_candidate",
    "intent_pressure_influence_candidate",
)
