# -*- coding: utf-8 -*-
"""Layered Governance Mapping v1 — addendum to Layered Capability Stack Standard #11."""

from __future__ import annotations

from typing import Any, Dict, Tuple

ADDENDUM_ID = "layered_governance_mapping_v1"
ADDENDUM_NAME = "Layered Governance Mapping Addendum"
ADDENDUM_NAME_ZH = "分层治理映射附录"

PRINCIPLE_EN = "Governance principles are consistent; governance enforcement is layered."
PRINCIPLE_ZH = "治理原则一致，治理落点分层。"
SLOGAN_ZH = "宪法精神统一，执法方式分层。"

EXTENDS_STANDARD_ID = "layered_capability_stack_standard_v1"

GOVERNANCE_MAPPING_LAYER_FIELDS: Tuple[str, ...] = (
    "capability_layer",
    "constitution_scope",
    "validation_scope",
    "health_scope",
    "whitebox_scope",
    "controlled_runtime_scope",
    "memory_worldmodel_scope",
    "privacy_scope",
    "failure_route_scope",
    "metrics_scope",
)

HARD_RULES: Tuple[str, ...] = (
    "same governance principles consistent across layers",
    "governance execution granularity adapts per layer",
    "lower layers focus on candidate/evidence/source",
    "middle layers focus on continuity/conflict/gap",
    "application layer focuses on adjudication/safety/forbidden actions",
    "long-term layer focuses on memory/identity/relationship/worldmodel",
    "upper-layer risk must not pollute lower layers",
    "lower layers must not bear upper-layer application responsibility",
    "must not apply all governance rules indiscriminately to every layer",
    "must not weaken core constitution principles due to layering",
)

MODULE_SUBMISSION_REQUIREMENTS: Tuple[str, ...] = (
    "capability_stack_definition",
    "layered_governance_mapping",
)

FIRST_PERSON_GOVERNANCE_LAYERS: Tuple[Dict[str, Any], ...] = (
    {
        "capability_layer": "layer_1_current_scene_understanding",
        "layer_name": "Current Scene Understanding",
        "governance_focus": "candidate authenticity, source, confidence, not_fact",
        "constitution_scope": "candidate_only_not_fact_baseline",
        "validation_scope": "source_chain_confidence_ttl_validation",
        "health_scope": "light_pressure_hint_only",
        "whitebox_scope": "source_chain_trace_refs",
        "controlled_runtime_scope": "not_applicable_foundation_layer",
        "memory_worldmodel_scope": "no_write",
        "privacy_scope": "minimal_scene_context_only",
        "failure_route_scope": "target_recognition_failure,text_recognition_failure,tracking_failure",
        "metrics_scope": "candidate_precision,confidence_distribution,ttl_compliance",
    },
    {
        "capability_layer": "layer_2_spatiotemporal_continuity",
        "layer_name": "Spatiotemporal Continuity Understanding",
        "governance_focus": "continuity, stale info, conflict/gap, world continuity not fact",
        "constitution_scope": "continuity_hypothesis_not_fact",
        "validation_scope": "freshness_conflict_gap_temporal_spatial_consistency",
        "health_scope": "continuity_pressure_degradation_hint",
        "whitebox_scope": "evidence_chain_sequence_trace",
        "controlled_runtime_scope": "not_applicable_continuity_layer",
        "memory_worldmodel_scope": "no_write_hypothesis_only",
        "privacy_scope": "scene_continuity_no_identity",
        "failure_route_scope": "sequence_gap_failure,continuity_hypothesis_failure,stale_sequence_failure",
        "metrics_scope": "freshness_state,gap_detection_rate,conflict_rate",
    },
    {
        "capability_layer": "layer_3_navigation_application",
        "layer_name": "Navigation Application Layer",
        "governance_focus": "safety priority, task boundary, forbid direct action, runtime later",
        "constitution_scope": "decision_center_safety_forbidden_actions_task_boundary",
        "validation_scope": "readiness_validation_before_application",
        "health_scope": "survival_pressure_elevated_monitoring",
        "whitebox_scope": "decision_rationale_application_context_trace",
        "controlled_runtime_scope": "admission_precondition_later_not_now",
        "memory_worldmodel_scope": "no_direct_write",
        "privacy_scope": "route_context_only",
        "failure_route_scope": "navigation_not_ready_failure,map_context_failure,route_context_failure",
        "metrics_scope": "application_readiness,safety_hold_rate,forbidden_action_block_rate",
    },
    {
        "capability_layer": "layer_4_extended_application",
        "layer_name": "Extended Application Capabilities",
        "governance_focus": "privacy, identity, sensitive info, memory/worldmodel admission",
        "constitution_scope": "privacy_identity_sensitive_info_baseline",
        "validation_scope": "higher_risk_validation_identity_reading",
        "health_scope": "identity_overreach_pressure",
        "whitebox_scope": "identity_reading_trace_with_privacy_mask",
        "controlled_runtime_scope": "deferred_high_risk_admission",
        "memory_worldmodel_scope": "admission_proposal_only_no_default_write",
        "privacy_scope": "strict_privacy_identity_masking",
        "failure_route_scope": "person_recognition_failure,reading_validation_failure,identity_overreach_failure",
        "metrics_scope": "privacy_mask_rate,identity_overreach_block_rate",
        "deferred": True,
    },
    {
        "capability_layer": "layer_5_long_term_personal",
        "layer_name": "Long-Term Social / Personal Capability",
        "governance_focus": "personal continuity, relationship, emotion state, long-term memory pollution",
        "constitution_scope": "personal_continuity_relationship_long_term_impact",
        "validation_scope": "memory_worldmodel_write_admission_validation",
        "health_scope": "long_term_drift_and_relationship_pressure",
        "whitebox_scope": "long_term_impact_audit_trace",
        "controlled_runtime_scope": "not_applicable_long_term_layer",
        "memory_worldmodel_scope": "write_admission_only_with_review",
        "privacy_scope": "maximum_personal_data_protection",
        "failure_route_scope": "personal_continuity_failure,relationship_failure,long_term_memory_pollution_failure",
        "metrics_scope": "write_admission_rate,relationship_model_drift,anti_copy_anti_miswrite_rate",
        "deferred": True,
        "later": True,
    },
)
