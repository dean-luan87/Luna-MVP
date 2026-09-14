# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — controlled execution iteration dryrun types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-DryRun-v1-001"
SYSTEM_ID = "LunaModelManagerDocumentSurfaceDetectorControlledExecutionIterationDryrunV1"
ITERATION_DRYRUN_ONLY = True
RUNTIME_ID = "document_surface_detector_v1"
REAL_EXECUTION_ENABLED = False
RUNTIME_ACTIVATION = False
ITERATION_STRATEGY_LAYER = True

ADAPTER_REF = "runtime/document_surface/controlled_execution_iteration_dryrun/document_surface_iteration_dryrun_adapter_v1.py"

SMOKE_CASE_IDS = (
    "case_a_two_overlapping_papers_clear_edges",
    "case_b_two_overlapping_papers_low_overlap",
    "case_c_two_overlapping_papers_high_overlap",
    "case_d_low_contrast_single_paper",
    "case_e_low_contrast_texture_false_positive",
    "case_f_receipt_attached_clear",
    "case_g_receipt_attached_uncertain",
    "case_h_document_on_screen_control",
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
    "no_fake_relation",
    "no_forced_multi_surface_output",
    "no_relation_without_evidence",
    "attention_gate_required",
    "candidate_only_not_fact",
    "output_boundary_required",
    "runtime_trace_required",
    "protocol_compliance_required",
    "existing_protocol_chain_required",
    "protocol_patch_not_new_branch",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_DRYRUN_GO"
FINAL_BLOCKED_BY_MISSING_FIXTURES = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_DRYRUN_BLOCKED_BY_MISSING_ITERATION_FIXTURES"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_DRYRUN_BLOCKED"
NEXT_PHASE_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Post-Review-v1-001"
NEXT_PHASE_FIXTURE_PLANNING = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Iteration-Fixture-Preparation-Planning-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
