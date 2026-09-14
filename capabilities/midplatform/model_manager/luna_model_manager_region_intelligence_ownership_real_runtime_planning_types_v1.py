# -*- coding: utf-8 -*-
"""Luna Ownership Real Runtime Integration — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerRegionIntelligenceOwnershipRealRuntimeIntegrationPlanningV1"
PLANNING_ONLY = True
LAYER_ID = "Region_Intelligence_Ownership_Real_Runtime"

POLICY_REF = "runtime/mixed_region/ownership_real_runtime/planning/ownership_real_runtime_policy_v1.json"
PLAN_REF = "runtime/mixed_region/ownership_real_runtime/planning/ownership_real_runtime_plan_v1.md"
ADAPTER_REF = "runtime/mixed_region/ownership_real_runtime/planning/ownership_real_runtime_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_GO",
)

SMOKE_CASE_IDS = (
    "case_a_stacked_papers_per_owner_ocr",
    "case_b_shelf_distinct_owners",
    "case_c_glass_reflection_separation",
    "case_d_attention_blocked_no_ownership",
    "case_e_occluded_title_not_absent",
    "case_f_runtime_unavailable_no_fallback",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "attention_gated_input": True,
    "slot_ownership_discovery": True,
    "slot_occlusion_reasoning": True,
    "slot_text_owner_assignment": True,
    "carrier_before_ocr": True,
    "text_owner_binding_required": True,
    "no_silent_fallback": True,
    "deterministic_fixture_only": True,
    "candidate_only": True,
    "no_fact_write": True,
}
