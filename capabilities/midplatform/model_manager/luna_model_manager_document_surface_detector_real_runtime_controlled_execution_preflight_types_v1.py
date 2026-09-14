# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — controlled execution preflight types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Preflight-v1-001"
SYSTEM_ID = "LunaModelManagerDocumentSurfaceDetectorRealRuntimeControlledExecutionPreflightV1"
CONTROLLED_EXECUTION_PREFLIGHT_ONLY = True
RUNTIME_ID = "document_surface_detector_v1"
REAL_EXECUTION_ENABLED = False
DETECTOR_EXECUTION_ENABLED = False

ADAPTER_REF = "runtime/document_surface/controlled_execution_preflight/document_surface_preflight_adapter_v1.py"

SMOKE_CASE_IDS = (
    "case_a_cv2_dependency_preflight",
    "case_b_controlled_input_registry",
    "case_c_blocked_invalid_input_path",
    "case_d_output_boundary",
    "case_e_trace_schema",
    "case_f_abort_policy",
    "case_g_protocol_compliance_retained",
    "case_h_real_execution_remains_disabled",
)

NEGATIVE_GUARD_IDS = (
    "no_detector_execution_in_preflight",
    "no_cv2_processing_in_preflight",
    "no_cv2_imread",
    "no_real_image_content_read",
    "no_ocr_execution",
    "no_vlm_call",
    "no_layout_parser_execution",
    "no_silent_dependency_install",
    "no_network_image_download",
    "no_arbitrary_input_directory",
    "no_production_write",
    "no_runtime_registry_activation",
    "no_candidate_to_fact_promotion",
    "no_fallback_to_ocr_vlm_layout",
    "attention_gate_required",
    "protocol_compliance_required",
    "existing_protocol_chain_required",
    "protocol_patch_not_new_branch",
    "real_execution_disabled_in_preflight",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_GO"
FINAL_GO_WITH_DEPENDENCY_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_GO_WITH_DEPENDENCY_BLOCKED"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_BLOCKED"
NEXT_PHASE_DRYRUN = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-DryRun-v1-001"
NEXT_PHASE_CV2_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-CV2-Dependency-Admission-Review-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
