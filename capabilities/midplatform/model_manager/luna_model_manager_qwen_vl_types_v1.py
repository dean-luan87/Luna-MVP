# -*- coding: utf-8 -*-
"""Luna Model Manager Qwen-VL Integration — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-QwenVL-Real-Provider-Integration-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerQwenVLIntegrationPlanningV1"
MODEL_ID = "qwen_vl"
MODEL_ID_V2 = "qwen_vl_v2"
PROVIDER_TYPE = "external_teacher"
MODEL_TYPE = "vision_language_model"

POLICY_REF = "qwen_vl_model_manager_provider_policy_v1"
REGISTRY_REF = "model_registry_v1"
CAPABILITY_REF = "capability_registry_v1"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LIFECYCLE_SANDBOX_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_DRYRUN_GO",
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO",
)

FROZEN_PREREQUISITES = (
    "Teacher_Adapter_Qwen_VL",
    "Model_Manager_Foundation",
    "Model_Manager_Lifecycle",
)

SMOKE_CASE_IDS = (
    "case_a_unknown_scene_qwen_evidence",
    "case_b_shopfront_ocr_qwen_noop",
    "case_c_qwen_provider_timeout_fallback",
    "case_d_qwen_unsupported_claim_reject",
    "case_e_qwen_lifecycle_version_switch",
)

ALLOWED_OUTPUT_TYPES = (
    "teacher_evidence_candidate",
    "scene_hypothesis_candidate",
    "visual_reasoning_candidate",
    "visual_attention_candidate",
    "task_clue_candidate",
    "provider_error_candidate",
)

FORBIDDEN_OUTPUT_TYPES = (
    "scene_fact",
    "selected_plan",
    "tool_execution",
    "fact_write",
    "teacher_decision",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-QwenVL-Real-Provider-Integration-DryRun-v1-001"

DRYRUN_PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-QwenVL-Real-Provider-Integration-DryRun-v1-001"
DRYRUN_FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_DRYRUN_GO"
DRYRUN_FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_DRYRUN_BLOCKED"
DRYRUN_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-Planning-v1-001"

DRYRUN_CASE_IDS = (
    "case_a_qwen_normal_closed_loop",
    "case_b_capability_mismatch_ocr_selected",
    "case_c_qwen_version_switch",
    "case_d_provider_timeout_no_silent_switch",
    "case_e_unsupported_claim_governance",
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "qwen_not_special_teacher": True,
    "model_registry_owned": True,
    "capability_first_routing": True,
    "lifecycle_gated": True,
    "no_fact_write": True,
    "no_plan_override": True,
    "no_tool_execution": True,
    "frozen_teacher_adapter_prerequisite": True,
}
