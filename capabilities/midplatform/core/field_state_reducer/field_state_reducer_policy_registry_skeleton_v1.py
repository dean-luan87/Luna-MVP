# -*- coding: utf-8 -*-
"""Field State Reducer policy registry skeleton v1."""

from __future__ import annotations

from typing import Dict, Tuple


POLICY_REGISTRY_SKELETON_V1: Tuple[Dict[str, object], ...] = (
    {
        "policy": "latest_valid_event",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
    {
        "policy": "highest_confidence_valid_event",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
    {
        "policy": "multi_event_consensus",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
    {
        "policy": "negative_event_override",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
    {
        "policy": "revocation_override",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
    {
        "policy": "expiration_degrade",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
    {
        "policy": "temporary_overlay_separation",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
    {
        "policy": "conflict_preservation",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
    {
        "policy": "insufficient_evidence_unresolved",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
    {
        "policy": "explicit_owner_override_candidate",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
    {
        "policy": "no_state_change",
        "registered": True,
        "implemented": False,
        "runtime_callable": False,
        "planning_reference": "field_state_reduction_policy_registry_v1.json",
        "fact_promotion_allowed": False,
    },
)
