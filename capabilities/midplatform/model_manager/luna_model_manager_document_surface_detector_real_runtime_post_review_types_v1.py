# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — post-review types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Post-Review-v1-001"
SYSTEM_ID = "LunaModelManagerDocumentSurfaceDetectorRealRuntimeIntegrationPostReviewV1"
POST_REVIEW_ONLY = True
RUNTIME_ID = "document_surface_detector_v1"

POLICY_REF = "runtime/document_surface/post_review/document_surface_detector_post_review_policy_v1.json"
ADAPTER_REF = "runtime/document_surface/post_review/document_surface_detector_post_review_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_GO",
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

RISK_IDS = (
    "real_detector_model_selection_deferred",
    "document_vs_screen_ambiguity",
    "severe_occlusion_boundary_uncertainty",
    "layout_detector_conflict_resolution_deferred",
    "real_image_benchmark_not_started",
    "OCR_per_surface_not_started",
    "field_centric_role_dryrun_pending",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-DryRun-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

BOUNDARY_FLAGS = {
    "post_review_only": True,
    "no_real_model_execution": True,
    "no_ocr_execution": True,
    "no_vlm_execution": True,
    "no_new_layout_parser_behavior": True,
    "boundary_frozen": True,
    "candidate_only": True,
    "no_fact_write": True,
}
