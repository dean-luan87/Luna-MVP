# -*- coding: utf-8 -*-
"""MobileSAM single model execution integration — types v1."""

from __future__ import annotations

MOBILE_SAM_SINGLE_MODEL_EXECUTION_INTEGRATION_SYSTEM_ID = (
    "LunaModelTestLensMobileSAMSingleModelExecutionIntegrationV1"
)
PHASE_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-001"
)

# First phase where runner_execution is allowed — MobileSAM only.
RUNNER_EXECUTION_ALLOWED = True
RUNNER_EXECUTION_MODEL_ALLOWLIST = ("mobile_sam",)
RUNNER_EXECUTION_ENVIRONMENT_ALLOWLIST = ("test_environment", "localhost_8787")

PIPELINE_STAGES = (
    "segmentation_region",
    "observation_attention_record",
    "followup_model_route_candidate",
    "runner_task_candidate",
    "runner_invocation_request",
    "runner_invocation_admission",
    "controlled_runner_execution_candidate",
    "runner_execution",
    "segmentation_result_envelope",
    "result_candidate",
    "fact_admission",
)

TASK_TYPE = "segmentation"
MODEL_ID = "mobile_sam"
MODEL_CATEGORY = "segmentation"

EXECUTION_CANDIDATE_REQUIRED_STATUSES = (
    "planned_only",
    "ready_for_execution_review",
)
FORBIDDEN_EXECUTION_CANDIDATE_STATUSES = (
    "cancelled",
    "blocked",
)

RUNNER_EXECUTION_FORBIDDEN_STATUSES = (
    "cancelled",
    "blocked",
    "failed_model_output",
)

ERROR_TYPES = (
    "timeout",
    "runner_unavailable",
    "invalid_crop",
    "empty_mask_output",
    "empty_mask_output",
    "schema_validation_failed",
    "model_output_invalid",
    "execution_cancelled",
    "trace_chain_incomplete",
    "sandbox_policy_violation",
)

ADAPTER_INPUT_REQUIRED_FIELDS = (
    "image_ref",
    "region_ref",
    "task_type",
    "model_id",
    "constraints",
    "trace_chain",
    "source_execution_candidate_id",
)

SEGMENTATION_ENVELOPE_REQUIRED_FIELDS = (
    "envelope_type",
    "source_model",
    "source_runner_execution_id",
    "source_execution_candidate_id",
    "region_id",
    "mask_ref",
    "confidence",
    "candidate_only",
    "not_fact",
    "needs_fact_admission",
)

FORBIDDEN_OPERATIONS = (
    "ui_direct_model_call",
    "bypass_admission",
    "bypass_execution_candidate",
    "non_mobile_sam_runner",
    "non_test_environment_execution",
    "runner_output_direct_to_fact",
    "runner_output_overwrite_attention",
    "runner_output_overwrite_segmentation_boundary",
    "human_correction_modify_model_result",
    "human_correction_as_ground_truth",
    "no_trace_chain_execution",
    "orphan_runner_execution",
)

BOUNDARY_FLAGS = {
    "runner_execution_allowed": True,
    "mobile_sam_only": True,
    "test_environment_only": True,
    "execution_candidate_required": True,
    "trace_chain_required": True,
    "adapter_input_normalized": True,
    "runner_output_requires_envelope": True,
    "runner_output_not_fact": True,
    "fact_admission_required_before_fact_write": True,
    "human_correction_priority_signal_only": True,
    "no_prompt_label_fact_upgrade": True,
    "visual_expression_system_frozen": True,
    "no_auto_fact_admission": True,
    "browser_runtime_guard_inherited": True,
}

RECOMMENDED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Single-Model-Interaction-Validation-v1-001"
)
