# -*- coding: utf-8 -*-
"""Luna Lightweight Vision Runtime — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Lightweight-Vision-Runtime-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerRegionIntelligenceOwnershipLightweightVisionRuntimePlanningV1"
PLANNING_ONLY = True
LAYER_ID = "Region_Intelligence_Lightweight_Vision_Runtime"

POLICY_REF = "runtime/mixed_region/lightweight_vision/planning/lightweight_vision_runtime_policy_v1.json"
PLAN_REF = "runtime/mixed_region/lightweight_vision/planning/lightweight_vision_runtime_plan_v1.md"
ADAPTER_REF = "runtime/mixed_region/lightweight_vision/planning/lightweight_vision_planning_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_PLANNING_GO",
)

SMOKE_CASE_IDS = (
    "case_a_stacked_documents_occlusion",
    "case_b_shelf_price_tag_separation",
    "case_c_screen_surface_split",
    "case_d_reflection_not_real_sign",
    "case_e_attention_blocked_no_runtime",
    "case_f_runtime_unavailable_replan",
    "case_g_layout_multi_block",
    "case_h_runtime_conflict_validation",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-DryRun-v1-001"
FIRST_REAL_RUNTIME = "document_surface_detector_v1"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "attention_gate_required": True,
    "runtime_outputs_candidate_only": True,
    "runtime_does_not_assign_fact": True,
    "runtime_does_not_override_ownership_graph": True,
    "no_global_ocr": True,
    "no_full_scene_segmentation_by_default": True,
    "no_all_model_activation": True,
    "failure_returns_runtime_error_candidate": True,
    "deterministic_fixture_only": True,
    "candidate_only": True,
    "no_fact_write": True,
}
