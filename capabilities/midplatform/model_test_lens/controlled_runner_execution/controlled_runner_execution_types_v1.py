# -*- coding: utf-8 -*-
"""Controlled runner execution constants — planning v1 (Detection/OCR scope)."""

from __future__ import annotations

CONTROLLED_RUNNER_EXECUTION_SYSTEM_ID = "LunaModelTestLensControlledRunnerExecutionV1"
PHASE_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-Planning-v1-001"
)
PLANNING_ONLY = True

FIVE_LAYER_MODEL = {
    "runner_task_candidate": "what_could_be_considered",
    "runner_invocation_request": "prepared_application_to_execute",
    "runner_invocation_admission": "allowed_into_execution_preparation",
    "controlled_runner_execution_candidate": "how_to_execute_in_controlled_sandbox",
    "runner_execution": "actual_model_run_forbidden_in_this_phase",
}

PIPELINE_STAGES = (
    "segmentation_region",
    "observation_attention_record",
    "followup_model_route_candidate",
    "runner_task_candidate",
    "runner_invocation_request",
    "runner_invocation_admission",
    "controlled_runner_execution_candidate",
    "runner_execution",
    "runner_output_envelope",
    "fact_admission",
)

REQUESTED_RUNNER_TYPES = ("Detection", "OCR")
EXECUTION_MODE = "manual_controlled"
EXECUTION_STATUS_ALLOWED = ("planned_only", "not_executed")
FORBIDDEN_EXECUTION_STATUS = (
    "running", "executed", "completed", "failed_with_model_output",
    "fact_written", "navigation_decided",
)

ADMISSION_REQUIRED = "admitted"
FORBIDDEN_REQUEST_STATES_FOR_EXEC_CANDIDATE = (
    "pending", "rejected", "cancelled", "orphan", "stale",
)

TRACE_CHAIN_STAGES = (
    "segmentation_region",
    "observation_attention_record",
    "followup_model_route_candidate",
    "runner_task_candidate",
    "runner_invocation_request",
    "runner_invocation_admission",
    "controlled_runner_execution_candidate",
)

ERROR_TYPES = (
    "timeout",
    "runner_unavailable",
    "invalid_crop",
    "route_mismatch",
    "schema_validation_failed",
    "model_output_invalid",
    "confidence_too_low",
    "execution_cancelled",
)

FORBIDDEN_OPERATIONS = (
    "no_runner_execution",
    "no_model_call",
    "no_fact_write",
    "no_navigation_decision",
    "no_auto_runner_trigger",
    "admitted_does_not_execute_runner",
    "execution_candidate_not_runner_execution",
    "execution_candidate_requires_admitted_request",
    "rejected_request_cannot_generate_execution_candidate",
    "pending_request_cannot_generate_execution_candidate",
    "cancelled_request_cannot_generate_execution_candidate",
    "no_orphan_execution_candidate",
    "detection_input_does_not_contain_fact_label",
    "ocr_input_does_not_contain_fact_text",
    "no_prompt_label_fact_upgrade",
    "no_human_correction_ground_truth",
    "no_motion_confirmed_from_single_frame",
    "runner_output_requires_envelope",
    "runner_output_requires_fact_admission_before_fact_write",
    "runner_error_does_not_write_fact",
    "no_visual_expression_mutation",
    "no_execution_box_on_canvas",
    "execute_runner",
    "automatic_model_invocation",
    "write_fact",
    "navigation_decision",
    "runner_output_direct_to_fact",
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "execution_candidate_only": True,
    "not_runner_execution": True,
    "not_fact": True,
    "not_executed": True,
    "no_navigation_decision": True,
    "candidate_only": True,
    "admitted_request_required": True,
    "runner_output_requires_fact_admission": True,
    "visual_expression_system_frozen": True,
    "browser_runtime_guard_inherited": True,
}

RECOMMENDED_NEXT_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-UI-Execution-v1-001"
)
