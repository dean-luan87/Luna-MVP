# -*- coding: utf-8 -*-
"""Luna Model Manager Mixed Region Understanding — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Mixed-Region-Understanding-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerMixedRegionUnderstandingPlanningV1"
PLANNING_ONLY = True

LAYER_ID = "Region_Intelligence_Layer"
POLICY_REF = "runtime/mixed_region/mixed_region_understanding_policy_v1.json"
PLAN_REF = "runtime/mixed_region/region_intelligence_plan_v1.md"
ADAPTER_REF = "runtime/mixed_region/mixed_region_understanding_adapter_v1.py"

REGION_CAPABILITIES = (
    "understand_region_text",
    "understand_region_visual",
    "understand_region_layout",
    "understand_region_context",
    "understand_region_ownership",
)

INFORMATION_SLOTS = (
    "text",
    "visual_symbol",
    "style",
    "layout",
    "layout_relation",
    "direction_symbol",
    "logo",
    "context",
    "ownership",
    "price_number",
    "qr_code",
)

EVIDENCE_CHANNELS = (
    "text_channel",
    "visual_channel",
    "spatial_channel",
    "context_channel",
    "ownership_channel",
)

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_OCR_RECOGNITION_RUNTIME_INTEGRATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_DRYRUN_GO",
)

FROZEN_PREREQUISITES = (
    "Model_OS_Foundation_Frozen",
    "Region_Intelligence_Layer",
    "Information_Channel_Activation",
    "Ownership_Understanding",
    "Evidence_Completeness",
    "Not_OCR_Extension",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_information_slots",
    "case_b_metro_multi_channel",
    "case_f_occlusion_visual_supplement",
    "case_g_text_visual_conflict",
    "case_h_artistic_text_visual_gap",
    "case_i_logo_only_no_text_fact",
    "case_j_ocr_wrong_visual_support",
    "case_k_multi_object_multi_slots",
    "case_l_stacked_documents_ownership",
    "case_m_glass_reflection_ownership",
    "case_n_shelf_entity_separation",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MIXED_REGION_UNDERSTANDING_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MIXED_REGION_UNDERSTANDING_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"
DRYRUN_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-DryRun-v1-001"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "region_intelligence_layer": True,
    "information_channel_activation": True,
    "five_channel_with_ownership": True,
    "ownership_before_ocr": True,
    "evidence_completeness": True,
    "not_ocr_extension": True,
    "not_fixed_ocr_plus_vlm": True,
    "not_full_image_text_merge": True,
    "fusion_not_answer_merge": True,
    "analyzer_not_recognizer": True,
    "candidate_only": True,
    "no_fact_write": True,
}
