# -*- coding: utf-8 -*-
"""Field-Oriented Egocentric Action Understanding — registry v1."""

from __future__ import annotations

from typing import Dict, FrozenSet, Tuple

REGISTRY_ID = "field_understanding_registry_v1"

FIELD_TYPES: Tuple[str, ...] = (
    "home",
    "street",
    "mall",
    "metro_station",
    "hospital",
    "office",
    "school",
    "restaurant",
    "shop",
    "elevator_lobby",
    "corridor",
    "crosswalk",
    "unknown",
)

STATIC_OBJECT_CLASSES: Tuple[str, ...] = (
    "door",
    "wall",
    "elevator",
    "elevator_door",
    "stairs",
    "handrail",
    "counter",
    "shelf",
    "fixed_sign",
    "crosswalk",
    "metro_exit",
    "fixed_pillar",
    "unknown_static",
)

DYNAMIC_TYPES: Tuple[str, ...] = (
    "moving_person",
    "vehicle",
    "temporary_obstacle",
    "crowd",
    "door_state_change",
    "temporary_blocked_passage",
    "ground_temporary_object",
    "sudden_obstacle",
    "unknown_dynamic",
)

DYNAMIC_CURRENT_STATES: Tuple[str, ...] = (
    "present",
    "approaching",
    "receding",
    "stationary",
    "temporary_obstacle",
    "blocked",
    "opening",
    "closing",
    "unknown",
)

MOVEMENT_TRENDS: Tuple[str, ...] = (
    "approaching",
    "receding",
    "lateral",
    "stationary",
    "uncertain",
    "unknown",
)

RISK_LEVELS: Tuple[str, ...] = (
    "none",
    "low",
    "medium",
    "high",
    "critical",
    "unknown",
)

POSITION_BANDS: Tuple[str, ...] = (
    "immediate_front",
    "near_front",
    "mid_field",
    "far_field",
    "peripheral",
    "unknown",
)

SEMANTIC_ROLES: Tuple[str, ...] = (
    "obstacle",
    "path_anchor",
    "destination_anchor",
    "warning_signal",
    "navigation_signal",
    "memory_anchor",
    "support_object",
    "social_object",
    "unknown_relevant_object",
)

RISK_TAGS: Tuple[str, ...] = (
    "collision_risk",
    "trip_risk",
    "head_level_risk",
    "low_obstacle_risk",
    "moving_object_risk",
    "glass_risk",
    "crowd_risk",
    "vehicle_risk",
    "uncertain_risk",
)

ATTENTION_TAGS: Tuple[str, ...] = (
    "high_attention",
    "must_confirm",
    "task_relevant",
    "user_requested",
    "rare_signal",
    "environment_change",
)

DESTINATION_TAGS: Tuple[str, ...] = (
    "target_place",
    "possible_target",
    "route_checkpoint",
    "exit_candidate",
    "entrance_candidate",
    "elevator_candidate",
    "room_candidate",
    "shop_candidate",
)

MEMORY_TAGS: Tuple[str, ...] = (
    "seen_before",
    "user_named",
    "frequent_anchor",
    "previously_dangerous",
    "previously_successful_path",
    "user_preference_related",
)

INFLUENCE_TYPES: Tuple[str, ...] = (
    "movement_constraint",
    "attention_shift",
    "risk_increase",
    "risk_decrease",
    "semantic_confirmation_needed",
    "memory_activation",
    "route_uncertainty",
    "visibility_degradation",
    "social_density_increase",
    "task_progress_support",
    "task_progress_block",
)

AFFECTED_TARGETS: Tuple[str, ...] = (
    "user",
    "luna",
    "action_plan",
    "navigation_plan",
    "attention_budget",
    "risk_profile",
    "memory_context",
    "task_progress",
)

DISTANCE_BANDS: Tuple[str, ...] = (
    "immediate_risk",
    "near_action_zone",
    "mid_anchor_zone",
    "far_semantic_zone",
    "unknown_but_risky",
    "clear_enough",
    "unknown",
)

DISTANCE_METHODS: Tuple[str, ...] = (
    "object_size_prior",
    "ground_plane_constraint",
    "temporal_approach",
    "depth_sensor",
    "map_prior",
    "human_like_estimation",
    "action_point_field",
)

MAP_SOURCES: Tuple[str, ...] = (
    "external_poi_api",
    "offline_map_pack",
    "user_provided",
    "midplatform_route_hint",
    "unknown",
)

MAP_TYPES: Tuple[str, ...] = (
    "poi",
    "area",
    "route",
    "floor_plan_hint",
    "exit_hint",
    "unknown",
)

MAP_FRESHNESS: Tuple[str, ...] = (
    "fresh",
    "stale",
    "unknown",
    "not_applicable",
)

ALIGNMENT_STATUSES: Tuple[str, ...] = (
    "aligned",
    "partially_aligned",
    "conflicted",
    "not_observed",
    "unknown",
)

ACTION_READINESS: Tuple[str, ...] = (
    "ready_for_action_decision",
    "needs_more_observation",
    "conflicted",
    "low_confidence",
    "blocked_by_safety",
    "unknown",
)

ACTION_RELEVANCE: Tuple[str, ...] = (
    "high",
    "medium",
    "low",
    "none",
    "unknown",
)

RELEVANCE_QUALIFIERS: Tuple[str, ...] = (
    "high",
    "medium",
    "low",
    "none",
    "unknown",
)

FACT_INFLUENCE_LEVELS: Tuple[str, ...] = (
    "none",
    "weak",
    "moderate",
    "strong",
    "critical",
)

FIELD_REVISION_POLICIES: Tuple[str, ...] = (
    "no_revision",
    "influence_only",
    "request_recheck",
    "temporary_field_adjustment",
    "escalate_to_user_confirmation",
)

PROHIBITED_FIELD_REVISION_POLICIES: Tuple[str, ...] = (
    "override_field",
    "replace_field",
    "direct_fact_to_action",
)

INFLUENCE_SCOPES: Tuple[str, ...] = (
    "field_synthesis",
    "attention_weighting",
    "risk_escalation",
    "user_confirmation",
)

FIELD_DIMENSIONS: Tuple[str, ...] = (
    "field_purpose",
    "field_structure",
    "field_state",
    "field_risk",
    "field_task_relevance",
    "field_action_logic",
    "field_memory",
    "field_attention",
)

FIELD_PURPOSES: Tuple[str, ...] = (
    "take_metro",
    "transfer",
    "exit_station",
    "find_platform",
    "check_direction",
    "wait_train",
    "avoid_crowd",
    "navigate_mall",
    "find_clinic",
    "passage_safety",
    "home_navigation",
    "unknown",
)

FIELD_STATE_VALUES: Tuple[str, ...] = (
    "train_arriving",
    "train_suspended",
    "exit_blocked",
    "crowd_dense",
    "uncertain_exit",
    "passage_blocked",
    "low_visibility",
    "crosswalk_waiting",
    "unknown",
)

PROHIBITED_FIELD_TYPES_FROM_ISOLATED_FACT: Tuple[str, ...] = (
    "display_screen",
    "train_display",
    "ocr_panel",
    "sign_only",
)

FACT_DERIVED_FIELD_IDENTITY_KEYS: Tuple[str, ...] = (
    "field_type_override",
    "revised_field_type",
    "fact_derived_field_type",
    "identity_from_fact",
    "field_identity_from_fact",
)

FIELD_SYNTHESIS_CHAIN: Tuple[str, ...] = (
    "fact_candidates",
    "field_synthesis",
    "field_information",
    "fact_influence_governance",
    "spatial_action_fusion",
    "decision_candidate",
)

SPEECH_DISTANCE_OUTPUT_FORBIDDEN_PATTERNS: Tuple[str, ...] = (
    r"\d+\.?\d*\s*m\b",
    r"\d+\.?\d*\s*米",
    r"exactly\s+\d",
    r"precise\s+distance",
)

HIGH_RISK_DISTANCE_BANDS: FrozenSet[str] = frozenset({"immediate_risk", "near_action_zone"})

ALIGNMENT_CONFLICT_STATUSES: FrozenSet[str] = frozenset({"conflicted", "not_observed"})

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "field_types": FIELD_TYPES,
    "static_object_classes": STATIC_OBJECT_CLASSES,
    "dynamic_types": DYNAMIC_TYPES,
    "dynamic_current_states": DYNAMIC_CURRENT_STATES,
    "movement_trends": MOVEMENT_TRENDS,
    "risk_levels": RISK_LEVELS,
    "position_bands": POSITION_BANDS,
    "semantic_roles": SEMANTIC_ROLES,
    "risk_tags": RISK_TAGS,
    "attention_tags": ATTENTION_TAGS,
    "destination_tags": DESTINATION_TAGS,
    "memory_tags": MEMORY_TAGS,
    "influence_types": INFLUENCE_TYPES,
    "affected_targets": AFFECTED_TARGETS,
    "distance_bands": DISTANCE_BANDS,
    "distance_methods": DISTANCE_METHODS,
    "map_sources": MAP_SOURCES,
    "map_types": MAP_TYPES,
    "map_freshness": MAP_FRESHNESS,
    "alignment_statuses": ALIGNMENT_STATUSES,
    "action_readiness": ACTION_READINESS,
    "action_relevance": ACTION_RELEVANCE,
    "relevance_qualifiers": RELEVANCE_QUALIFIERS,
    "fact_influence_levels": FACT_INFLUENCE_LEVELS,
    "field_revision_policies": FIELD_REVISION_POLICIES,
    "influence_scopes": INFLUENCE_SCOPES,
    "field_dimensions": FIELD_DIMENSIONS,
    "field_purposes": FIELD_PURPOSES,
    "field_state_values": FIELD_STATE_VALUES,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry_value(domain: str, value: str) -> bool:
    return is_registered(domain, value)
