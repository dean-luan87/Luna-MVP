# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — implementation dryrun types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-DryRun-v1-001"
SYSTEM_ID = "LunaModelManagerDocumentSurfaceDetectorRealRuntimeImplementationDryrunV1"
IMPLEMENTATION_DRYRUN_ONLY = True
RUNTIME_ID = "document_surface_detector_v1"
IMPLEMENTATION_MODE = "classical_cv_boundary_v1"
FIRST_REAL_IMPLEMENTATION_CANDIDATE = "option_a_classical_cv_boundary"

POLICY_REF = "runtime/document_surface/implementation_dryrun/document_surface_option_a_dryrun_policy_v1.json"
ADAPTER_REF = "runtime/document_surface/implementation_dryrun/document_surface_option_a_dryrun_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_PLANNING_GO",
)

SMOKE_CASE_IDS = (
    "case_a_single_flat_paper",
    "case_b_two_overlapping_papers",
    "case_c_folded_or_curved_paper",
    "case_d_receipt_attached_to_package",
    "case_e_document_on_screen",
    "case_f_low_contrast_paper_on_desk",
    "case_g_attention_blocked",
    "case_h_runtime_error",
)

NEGATIVE_GUARD_IDS = (
    "no_real_model_execution",
    "no_cv2_import",
    "no_real_image_read",
    "no_image_segmentation_execution",
    "no_ocr_execution",
    "no_vlm_call",
    "no_layout_parser_execution",
    "no_document_fact_output",
    "no_global_ocr",
    "no_full_scene_segmentation_by_default",
    "no_candidate_to_fact_promotion",
    "no_silent_fallback",
    "no_accuracy_only_benchmark",
    "attention_gate_required",
    "attention_blocked_zero_runtime_call",
    "candidate_only_not_fact",
    "surface_candidate_before_text_owner_assignment",
    "no_merge_overlapped_documents",
    "screen_surface_not_document_surface_fact",
    "protocol_compliance_required",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_DRYRUN_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

BOUNDARY_FLAGS = {
    "implementation_dryrun_only": True,
    "no_cv2_import": True,
    "no_real_image_read": True,
    "no_real_model_execution": True,
    "no_ocr_execution": True,
    "no_vlm_execution": True,
    "candidate_only": True,
    "no_fact_write": True,
}
