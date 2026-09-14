# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — controlled execution dryrun types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-DryRun-v1-001"
SYSTEM_ID = "LunaModelManagerDocumentSurfaceDetectorRealRuntimeControlledExecutionDryrunV1"
CONTROLLED_EXECUTION_DRYRUN_ONLY = True
RUNTIME_ID = "document_surface_detector_v1"
REAL_EXECUTION_ENABLED = False
RUNTIME_ACTIVATION = False
DETECTOR_EXECUTION_ENABLED = True

ADAPTER_REF = "runtime/document_surface/controlled_execution_dryrun/document_surface_controlled_execution_dryrun_adapter_v1.py"

SMOKE_CASE_IDS = (
    "case_a_single_flat_paper_controlled",
    "case_b_two_overlapping_papers_controlled",
    "case_c_low_contrast_paper_controlled",
    "case_d_receipt_attached_to_package_controlled",
    "case_e_document_on_screen_controlled",
    "case_f_attention_blocked_controlled",
    "case_g_unsupported_format_controlled",
    "case_h_image_read_failed_controlled",
)

NEGATIVE_GUARD_IDS = (
    "no_ocr_execution",
    "no_vlm_call",
    "no_layout_parser_execution",
    "no_full_scene_segmentation",
    "no_arbitrary_input_directory",
    "no_registry_external_read",
    "no_network_image_download",
    "no_silent_dependency_install",
    "no_production_write",
    "no_runtime_registry_activation",
    "no_candidate_to_fact_promotion",
    "no_fallback_to_ocr_vlm_layout",
    "attention_gate_required",
    "attention_blocked_zero_runtime_call",
    "candidate_only_not_fact",
    "output_boundary_required",
    "runtime_trace_required",
    "protocol_compliance_required",
    "existing_protocol_chain_required",
    "protocol_patch_not_new_branch",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_GO"
FINAL_BLOCKED_BY_MISSING_FIXTURES = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_BLOCKED_BY_MISSING_FIXTURES"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_DRYRUN_BLOCKED"
NEXT_PHASE_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Post-Review-v1-001"
NEXT_PHASE_FIXTURE_PLANNING = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Fixture-Preparation-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
