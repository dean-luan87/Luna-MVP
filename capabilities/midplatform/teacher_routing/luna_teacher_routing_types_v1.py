# -*- coding: utf-8 -*-
"""Teacher Routing Layer — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Teacher-Routing-Layer-Planning-v1-001"
SYSTEM_ID = "LunaTeacherRoutingLayerPlanningV1"
POLICY_REF = "teacher_routing_policy_v1"
REGISTRY_REF = "teacher_capability_registry_v1"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_TEACHER_PERFORMANCE_EVALUATION_GO",
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO",
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_DRYRUN_GO",
)

ROUTE_TYPES = (
    "tool_os",
    "teacher_single",
    "teacher_multi_candidate",
    "noop",
)

TEACHER_ROLES = (
    "perception_teacher",
    "planning_teacher",
    "learning_teacher",
    "domain_teacher",
)

KNOWN_TEACHERS = (
    "qwen_vl",
    "gpt_vision",
    "gemini",
    "internvl",
    "medical_teacher",
    "legal_teacher",
    "embodied_teacher",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_ocr_not_qwen",
    "case_b_unknown_scene_qwen_vl",
    "case_c_complex_multi_teacher_candidate",
    "case_d_precise_ocr_tool_route",
)

FINAL_GO = "P1_MIDPLATFORM_TEACHER_ROUTING_LAYER_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_TEACHER_ROUTING_LAYER_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Provider-Integration-v1-001"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "deterministic_routing_only": True,
    "no_teacher_execution": True,
    "no_tool_execution": True,
    "no_fact_write": True,
    "no_multi_teacher_voting": True,
    "router_does_not_override_plan": True,
    "router_does_not_override_scene": True,
    "future_multi_teacher_ready": True,
}
