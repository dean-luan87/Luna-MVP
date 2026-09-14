# -*- coding: utf-8 -*-
"""Luna Model Manager — foundation planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Foundation-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerFoundationPlanningV1"
POLICY_REF = "model_admission_policy_v1"
LIFECYCLE_REF = "model_lifecycle_policy_v1"

MODEL_TYPES = (
    "teacher",
    "tool",
    "perception",
    "speech",
    "memory",
    "personalization",
)

MODEL_OWNERS = (
    "external_teacher",
    "tool_os",
    "luna_internal",
    "third_party_provider",
)

LIFECYCLE_STATES = (
    "candidate",
    "sandbox",
    "admitted",
    "active",
    "deprecated",
    "blocked",
)

ROUTE_TARGET_TYPES = (
    "tool",
    "model",
    "noop",
    "multi_candidate",
)

UPSTREAM_GO = (
    "P1_MIDPLATFORM_TEACHER_ROUTING_LAYER_PLANNING_GO",
    "P1_MIDPLATFORM_TEACHER_PERFORMANCE_EVALUATION_GO",
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO",
)

FROZEN_PREREQUISITES = (
    "Teacher_Adapter",
    "Teacher_Routing",
    "Teacher_Performance_Evaluation",
    "Qwen_VL_Real_Provider",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_ocr_routing",
    "case_b_unknown_scene_qwen_routing",
    "case_c_capability_first_lookup",
    "case_d_model_admission_candidate",
    "case_e_unified_evaluation_profile",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-DryRun-v1-001"
LOCAL_MODEL_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-DryRun-v1-001"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "unified_manager_not_fragmented": True,
    "capability_first_routing": True,
    "no_auto_execution": True,
    "no_auto_admission": True,
    "no_fact_write": True,
    "teacher_system_subsumed": True,
    "future_multi_model_ready": True,
}
