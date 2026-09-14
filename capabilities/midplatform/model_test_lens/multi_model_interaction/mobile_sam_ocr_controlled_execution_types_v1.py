# -*- coding: utf-8 -*-
"""MobileSAM → OCR controlled execution planning — types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-Planning-v1-001"
SYSTEM_ID = "LunaMidplatformMobileSamOcrControlledExecutionPlanningV1"
PLANNING_ONLY = True

UPSTREAM_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO",
    "P1_MIDPLATFORM_MODEL_TEST_LENS_SINGLE_MODEL_INTERACTION_VALIDATION_UI_EXECUTION_GO",
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_EXPLORATION_SMOKE_GO",
)

FROZEN_CHAIN_STAGES = (
    "image_input",
    "mobilesam_controlled_execution",
    "segmentation_result_envelope",
    "result_candidate",
    "midplatform_processing",
    "ocr_route_candidate",
    "ocr_task_candidate",
    "ocr_invocation_request",
    "ocr_admission",
    "ocr_controlled_execution_candidate",
    "ocr_runner_execution",
    "ocr_result_envelope",
    "midplatform_fusion",
    "fact_admission",
)

PLANNING_ENDPOINT = "ocr_controlled_execution_candidate"

OCR_ALLOWED_INPUTS = (
    "source_image_ref",
    "source_region_id",
    "region_crop_ref",
    "region_geometry_ref",
    "source_result_candidate_id",
    "source_analysis_record_id",
    "source_ocr_task_candidate_id",
    "ocr_target_reason",
    "trace_chain",
)

OCR_FORBIDDEN_INPUTS = (
    "confirmed_text",
    "fact_label",
    "sign_label",
    "billboard_label",
    "confirmed_dynamic",
    "human_correction_as_ground_truth",
    "mobilesam_prompt_label_as_fact",
    "navigation_decision_context",
)

OCR_EXECUTION_CANDIDATE_ALLOWED_STATUS = ("planned_only", "not_executed")

OCR_EXECUTION_CANDIDATE_FORBIDDEN_STATUS = (
    "running",
    "executed",
    "completed",
    "success",
    "failed_with_model_output",
)

HUMAN_CORRECTION_DUAL_MODEL_ATTRIBUTIONS = (
    "ocr_model_error",
    "mobilesam_region_selection_error",
    "ocr_route_strategy_error",
    "attention_priority_error",
    "user_preference",
)

FORBIDDEN_OPERATIONS = (
    "no_ocr_runner_call",
    "no_ocr_execution",
    "no_ocr_result_generation",
    "no_model_call",
    "no_fact_write",
    "no_navigation_decision",
    "no_mobile_sam_direct_to_ocr",
    "no_bypass_midplatform",
    "no_visual_expression_mutation",
    "no_boundary_clone",
    "no_ocr_box_on_canvas",
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "ocr_runner_forbidden": True,
    "ocr_result_forbidden": True,
    "fact_write_forbidden": True,
    "ocr_request_requires_ocr_task_candidate": True,
    "ocr_execution_candidate_requires_admitted_request": True,
    "ocr_result_requires_envelope": True,
    "ocr_result_requires_fact_admission": True,
    "fusion_candidate_not_fact": True,
    "candidate_only_not_executed_not_fact_preserved": True,
}

RECOMMENDED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Controlled-Execution-UI-Execution-v1-001"
)
