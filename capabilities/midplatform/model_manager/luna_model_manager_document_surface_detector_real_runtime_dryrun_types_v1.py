# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — real runtime integration dryrun types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-DryRun-v1-001"
SYSTEM_ID = "LunaModelManagerDocumentSurfaceDetectorRealRuntimeIntegrationDryrunV1"
DRYRUN_ONLY = True
RUNTIME_ID = "document_surface_detector_v1"

POLICY_REF = "runtime/document_surface/dryrun/document_surface_detector_dryrun_policy_v1.json"
ADAPTER_REF = "runtime/document_surface/dryrun/document_surface_detector_dryrun_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_FIELD_CENTRIC_OBJECT_ROLE_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_GO",
)

SMOKE_CASE_IDS = (
    "case_a_stacked_papers_occlusion",
    "case_b_stacked_menus_no_ocr",
    "case_c_receipt_attached_to_package",
    "case_d_attention_blocked_skip",
    "case_e_uncertain_boundary",
    "case_f_runtime_unavailable",
    "case_g_layout_detector_conflict",
    "case_h_screen_document_confusion",
)

NEGATIVE_GUARD_IDS = (
    "no_ocr_text_output",
    "no_document_fact_output",
    "no_global_ocr",
    "no_full_scene_segmentation_by_default",
    "attention_gate_required",
    "candidate_only_not_fact",
    "runtime_does_not_override_ownership_graph",
    "surface_candidate_before_text_owner_assignment",
    "owner_required_for_text_assignment",
    "occlusion_not_absence",
    "no_silent_fallback_to_vlm",
    "no_silent_fallback_to_ocr",
    "no_merge_overlapped_documents",
    "screen_surface_not_document_surface_fact",
    "failure_returns_runtime_error_candidate",
    "attention_blocked_zero_runtime_call",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

BOUNDARY_FLAGS = {
    "dryrun_only": True,
    "no_real_model_execution": True,
    "no_ocr_execution": True,
    "no_vlm_execution": True,
    "attention_gate_required": True,
    "runtime_outputs_candidate_only": True,
    "first_real_lightweight_runtime_seam": True,
    "candidate_only": True,
    "no_fact_write": True,
}
