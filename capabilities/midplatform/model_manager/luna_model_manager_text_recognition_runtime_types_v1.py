# -*- coding: utf-8 -*-
"""Luna Model Manager OCR Recognition Runtime — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Real-OCR-Recognition-Runtime-Integration-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerRealOCRRecognitionRuntimeIntegrationPlanningV1"
PLANNING_ONLY = True

POLICY_REF = "runtime/text_recognition/text_recognition_runtime_policy_v1.json"
MIXED_REGION_POLICY_REF = "runtime/mixed_region/mixed_region_understanding_policy_v1.json"
RUNTIME_ADAPTER_REF = "runtime/text_recognition/text_recognition_runtime_adapter_v1.py"
MIXED_REGION_ADAPTER_REF = "runtime/mixed_region/mixed_region_understanding_adapter_v1.py"

SLOT_ID = "slot_2a"
SLOT_CAPABILITY = "text_recognition"
VISUAL_SLOT_ID = "slot_2b"
VISUAL_SLOT_CAPABILITY = "visual_understanding"
FUSION_SLOT_ID = "slot_3"
FUSION_SLOT_CAPABILITY = "evidence_fusion"

UPSTREAM_SLOT_ID = "slot_1"
UPSTREAM_CAPABILITY = "text_detection"
DEFAULT_PROVIDER = "paddleocr_recognizer_v1"
FALLBACK_PROVIDER = "ocr_v1"

INPUT_TYPES = ("text_region_candidate", "direction_text_region_candidate", "mixed_visual_semantic_region")
OUTPUT_TYPES = (
    "text_candidate",
    "visual_candidate",
    "mixed_evidence_candidate",
    "ocr_text_candidate",
    "ocr_low_confidence_candidate",
    "unsupported_ocr_claim",
    "ocr_runtime_error_candidate",
)

EVIDENCE_LAYERS = (
    "layer_1_text_evidence",
    "layer_2_visual_evidence",
    "layer_3_semantic_fusion",
)

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_GO",
)

FROZEN_PREREQUISITES = (
    "Model_OS_Foundation_Frozen",
    "Text_Detection_Runtime_DryRun_GO",
    "Collaboration_Slot_Abstraction",
    "Mixed_Region_Understanding_Core",
    "OCR_Is_Text_Branch_Only",
)

RUNTIME_ROADMAP = (
    "phase_1_text_detection",
    "phase_2_mixed_region_understanding",
    "phase_3_qwen_context",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_ocr_text_candidate",
    "case_b_metro_direction_ocr",
    "case_c_blurry_low_confidence",
    "case_d_unsupported_ocr_claim",
    "case_e_ocr_runtime_failure",
    "case_f_occlusion_visual_supplement",
    "case_g_text_visual_conflict",
    "case_h_artistic_text_visual_gap",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_OCR_RECOGNITION_RUNTIME_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_OCR_RECOGNITION_RUNTIME_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "mixed_region_understanding_core": True,
    "text_visual_dual_processing": True,
    "ocr_is_text_branch_only": True,
    "three_layer_evidence": True,
    "recognition_only_not_detection": True,
    "region_interpreter_not_answerer": True,
    "ocr_not_location_fact": True,
    "low_confidence_no_qwen": True,
    "visual_supplements_not_replaces": True,
    "conflict_to_validation": True,
    "runtime_error_replan": True,
    "candidate_only": True,
    "no_fact_write": True,
}
