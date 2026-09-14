# -*- coding: utf-8 -*-
"""Luna Model Manager Text Detection Runtime — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Text-Detection-Runtime-Integration-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerRealTextDetectionRuntimeIntegrationPlanningV1"
PLANNING_ONLY = True

POLICY_REF = "runtime/text_detection/text_detection_runtime_policy_v1.json"
RUNTIME_ADAPTER_REF = "runtime/text_detection/text_detection_runtime_adapter_v1.py"
SLOT_ID = "slot_1"
SLOT_CAPABILITY = "text_detection"
DEFAULT_PROVIDER = "paddleocr_detector_v1"
FALLBACK_PROVIDER = "detection_v1"

OUTPUT_TYPES = (
    "text_region_candidate",
    "direction_text_region_candidate",
    "no_text_candidate",
    "low_confidence_text_candidate",
)

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_DRYRUN_GO",
)

FROZEN_PREREQUISITES = (
    "Model_OS_Foundation_Frozen",
    "Collaboration_Slot_Abstraction",
    "Real_Chain_DryRun_GO",
    "Execution_Trace_Graph",
)

RUNTIME_ROADMAP = (
    "phase_1_text_detection",
    "phase_2_ocr_recognition",
    "phase_3_qwen_context",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_text_region",
    "case_b_metro_direction_region",
    "case_c_no_text_image",
    "case_d_low_confidence_detection",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Real-OCR-Recognition-Runtime-Integration-Planning-v1-001"

DRYRUN_PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Text-Detection-Runtime-Integration-DryRun-v1-001"
DRYRUN_POLICY_REF = "runtime/text_detection/dryrun/text_detection_dryrun_policy_v1.json"
DRYRUN_CASE_IDS = (
    "case_a_shopfront_text_region_dryrun",
    "case_b_subway_direction_dryrun",
    "case_c_no_text_environment_dryrun",
    "case_d_false_detection_dryrun",
    "case_e_runtime_failure_dryrun",
)
DRYRUN_FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_DRYRUN_GO"
DRYRUN_FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_DRYRUN_BLOCKED"
DRYRUN_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"

UPSTREAM_GO_DRYRUN = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_TEXT_DETECTION_RUNTIME_INTEGRATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_GO",
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "single_runtime_only": True,
    "text_detection_first_not_ocr": True,
    "detector_not_task_aware": True,
    "detector_not_auto_ocr": True,
    "l2_plan_unchanged": True,
    "grounding_dino_deferred": True,
    "sam_not_target_discovery": True,
    "candidate_only": True,
    "no_fact_write": True,
}
