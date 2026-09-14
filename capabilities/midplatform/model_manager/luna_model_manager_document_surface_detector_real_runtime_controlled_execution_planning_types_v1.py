# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — controlled execution planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerDocumentSurfaceDetectorRealRuntimeControlledExecutionPlanningV1"
CONTROLLED_EXECUTION_PLANNING_ONLY = True
RUNTIME_ID = "document_surface_detector_v1"
REAL_EXECUTION_ENABLED = False

ADAPTER_REF = "runtime/document_surface/controlled_execution_planning/document_surface_controlled_execution_planning_adapter_v1.py"

SMOKE_CASE_IDS = (
    "case_a_cv2_dependency_admission_planning",
    "case_b_input_output_boundary_planning",
    "case_c_abort_condition_planning",
    "case_d_trace_schema_planning",
    "case_e_controlled_smoke_plan",
    "case_f_protocol_compliance_retained",
    "case_g_next_phase_gate",
)

NEGATIVE_GUARD_IDS = (
    "no_cv2_import_in_planning",
    "no_real_image_read_in_planning",
    "no_detector_execution_in_planning",
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
    "no_direct_real_execution_next_phase",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PLANNING_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Preflight-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
