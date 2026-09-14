# -*- coding: utf-8 -*-
"""Luna Model Manager Local Model — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Local-Model-Integration-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerLocalModelIntegrationPlanningV1"

EXECUTION_MODES = ("external_api", "local_runtime")
LOCAL_MODEL_ID = "internvl2_5"
LOCAL_MODEL_ID_V2 = "internvl2_5_v2"
EXTERNAL_MODEL_ID = "qwen_vl"

POLICY_REF = "local_model_admission_policy_v1"
RUNTIME_POLICY_REF = "runtime_policy_v1"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LIFECYCLE_SANDBOX_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_DRYRUN_GO",
)

FROZEN_PREREQUISITES = (
    "Qwen_VL_Model_Manager_Integration",
    "Model_Manager_Lifecycle",
    "External_API_Provider_Pattern",
)

SMOKE_CASE_IDS = (
    "case_a_local_model_normal_admission",
    "case_b_gpu_insufficient_fallback",
    "case_c_local_vs_external_routing",
    "case_d_local_version_upgrade",
)

DRYRUN_PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Local-Model-Integration-DryRun-v1-001"
DRYRUN_CASE_IDS = (
    "case_a_local_runtime_normal",
    "case_b_runtime_unavailable_fallback",
    "case_c_local_vs_external_competition",
    "case_d_local_output_pollution",
    "case_e_runtime_lifecycle_upgrade",
)
DRYRUN_FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_DRYRUN_GO"
DRYRUN_FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_DRYRUN_BLOCKED"
DRYRUN_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-Planning-v1-001"

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-Planning-v1-001"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "unified_model_abstraction": True,
    "no_separate_api_local_logic": True,
    "resource_aware_routing": True,
    "provider_fallback_explicit": True,
    "no_training_no_finetuning": True,
    "model_manager_location_agnostic": True,
}
