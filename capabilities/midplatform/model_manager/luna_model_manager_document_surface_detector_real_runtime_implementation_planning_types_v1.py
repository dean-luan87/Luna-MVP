# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — implementation planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerDocumentSurfaceDetectorRealRuntimeImplementationPlanningV1"
IMPLEMENTATION_PLANNING_ONLY = True
RUNTIME_ID = "document_surface_detector_v1"
FIRST_REAL_IMPLEMENTATION_CANDIDATE = "option_a_classical_cv_boundary"

POLICY_REF = "runtime/document_surface/implementation_planning/document_surface_real_runtime_admission_policy_v1.json"
PLAN_REF = "runtime/document_surface/implementation_planning/document_surface_real_runtime_implementation_plan_v1.md"
ADAPTER_REF = "runtime/document_surface/implementation_planning/document_surface_real_runtime_implementation_planning_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO",
)

SMOKE_CASE_IDS = (
    "case_a_implementation_path_selection",
    "case_b_contract_alignment",
    "case_c_failure_modes_coverage",
    "case_d_test_image_registry",
    "case_e_benchmark_metrics",
    "case_f_attention_gate_constraint",
    "case_g_vlm_teacher_restriction",
    "case_h_real_execution_block",
)

NEGATIVE_GUARD_IDS = (
    "no_real_model_execution",
    "no_image_segmentation_execution",
    "no_ocr_execution",
    "no_vlm_call",
    "no_layout_parser_execution",
    "no_document_fact_output",
    "no_implementation_without_attention_gate",
    "no_global_ocr",
    "no_full_scene_segmentation_by_default",
    "no_candidate_to_fact_promotion",
    "no_silent_fallback",
    "no_accuracy_only_benchmark",
    "no_test_image_requirement_in_planning",
    "no_direct_real_execution_next_phase",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_PLANNING_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Post-Review-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

BOUNDARY_FLAGS = {
    "implementation_planning_only": True,
    "no_real_model_execution": True,
    "no_image_segmentation_execution": True,
    "no_ocr_execution": True,
    "no_vlm_execution": True,
    "real_execution_enabled": False,
    "candidate_only": True,
    "no_fact_write": True,
}
