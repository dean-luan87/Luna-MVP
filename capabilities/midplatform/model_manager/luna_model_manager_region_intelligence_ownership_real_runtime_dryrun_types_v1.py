# -*- coding: utf-8 -*-
"""Luna Ownership Real Runtime Integration — dryrun types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-DryRun-v1-001"
SYSTEM_ID = "LunaModelManagerRegionIntelligenceOwnershipRealRuntimeIntegrationDryrunV1"
DRYRUN_ONLY = True
LAYER_ID = "Region_Intelligence_Ownership_Runtime"

POLICY_REF = "runtime/mixed_region/ownership_runtime/dryrun/ownership_runtime_dryrun_policy_v1.json"
ADAPTER_REF = "runtime/mixed_region/ownership_runtime/dryrun/ownership_runtime_dryrun_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO",
)

DRYRUN_CASE_IDS = (
    "case_a_stacked_papers",
    "case_b_shelf_price_tags",
    "case_c_glass_reflection",
    "case_d_attention_blocked",
    "case_e_occluded_missing",
    "case_f_runtime_failure",
)

NEGATIVE_GUARD_IDS = (
    "no_global_ocr",
    "no_all_model_activation",
    "attention_gate_required",
    "owner_required_for_text",
    "occlusion_not_absence",
    "reflection_not_real_sign",
    "runtime_error_no_silent_fallback",
    "candidate_only_not_fact",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"

BOUNDARY_FLAGS = {
    "dryrun_only": True,
    "attention_gate_required": True,
    "three_slot_sequence": True,
    "owner_required_for_text": True,
    "occlusion_not_absence": True,
    "reflection_not_real_sign": True,
    "no_silent_fallback": True,
    "deterministic_fixture_only": True,
    "candidate_only": True,
    "no_fact_write": True,
}
