# -*- coding: utf-8 -*-
"""Runner manual trigger constants — planning v1 (Detection/OCR scope)."""

from __future__ import annotations

RUNNER_MANUAL_TRIGGER_SYSTEM_ID = "LunaModelTestLensRunnerManualTriggerV1"
PHASE_REF = "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-Planning-v1-001"
PLANNING_ONLY = True

PIPELINE_STAGES = (
    "segmentation_region",
    "observation_attention_record",
    "followup_model_route_candidate",
    "runner_task_candidate",
    "pinned_runner_task_candidate",
    "runner_invocation_request",
    "runner_execution",
)

THREE_LAYER_MODEL = {
    "runner_task_candidate": "what_could_be_considered",
    "runner_invocation_request": "prepared_application_to_execute",
    "runner_execution": "actual_model_run",
}

REQUESTED_RUNNER_TYPES_V1 = ("Detection", "OCR")
TARGET_MODEL_IDS_SOURCE = ("detection", "ocr")

REQUESTED_BY = ("manual_user_trigger", "developer_test_trigger")
TRIGGER_MODE = "manual_only"

ADMISSION_STATUS = ("pending_admission", "admitted", "rejected", "cancelled")
FORBIDDEN_ADMISSION_STATUS = ("running", "executed", "completed")

EXECUTION_STATUS_ALLOWED = ("not_executed",)
FORBIDDEN_EXECUTION_STATUS = (
    "running",
    "executed",
    "completed",
    "failed_with_model_output",
    "fact_written",
    "navigation_decided",
)

PINNED_QUEUE_STATES_FOR_REQUEST = ("pinned",)
FORBIDDEN_QUEUE_STATES_FOR_REQUEST = (
    "excluded",
    "blocked_by_policy",
    "stale_candidate",
)
CANDIDATE_REQUIRES_PIN = ("candidate", "manual_only")

TRACE_CHAIN_STAGES = (
    "segmentation_region",
    "observation_attention_record",
    "followup_model_route_candidate",
    "runner_task_candidate",
    "runner_invocation_request",
)

FORBIDDEN_OPERATIONS = (
    "no_runner_execution",
    "no_model_call",
    "no_fact_write",
    "no_navigation_decision",
    "no_auto_runner_trigger",
    "no_running_state_allowed",
    "no_executed_state_allowed",
    "no_completed_state_allowed",
    "invocation_request_not_execution",
    "invocation_request_requires_pinned_task_candidate",
    "excluded_task_cannot_generate_request",
    "stale_task_requires_reconfirmation",
    "blocked_task_cannot_generate_request",
    "no_orphan_invocation_request",
    "no_bypass_runner_task_candidate",
    "detection_request_requires_detection_route",
    "ocr_request_requires_ocr_route",
    "no_prompt_label_fact_upgrade",
    "no_human_correction_ground_truth",
    "no_motion_confirmed_from_single_frame",
    "no_visual_expression_mutation",
    "browser_runtime_guard_inherited",
    "execute_runner",
    "automatic_model_invocation",
    "auto_runner_trigger",
    "write_fact",
    "navigation_decision",
    "orphan_invocation_request",
    "bypass_task_candidate_to_request",
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "invocation_request_only": True,
    "not_runner_execution": True,
    "not_fact": True,
    "not_fact_write": True,
    "not_executed": True,
    "not_auto_runner_trigger": True,
    "no_navigation_decision": True,
    "candidate_only": True,
    "execution_status_not_executed_only": True,
    "requires_pinned_runner_task_candidate": True,
    "human_correction_priority_signal_only": True,
    "visual_expression_system_frozen": True,
    "browser_runtime_guard_inherited": True,
}

RECOMMENDED_NEXT_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-UI-Execution-v1-001"
)
