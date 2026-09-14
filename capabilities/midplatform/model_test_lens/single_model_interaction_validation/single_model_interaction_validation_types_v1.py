# -*- coding: utf-8 -*-
"""Single model interaction validation — types v1."""

from __future__ import annotations

SINGLE_MODEL_INTERACTION_VALIDATION_SYSTEM_ID = "LunaMidplatformSingleModelInteractionValidationV1"
PHASE_REF = "Phase-P1-Midplatform-Single-Model-Interaction-Validation-v1-001"
PLANNING_ONLY = True

UPSTREAM_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO"

INTERACTION_LOOP_STAGES = (
    "image_input",
    "segmentation_region",
    "execution_candidate",
    "runner_execution",
    "segmentation_result_envelope",
    "result_candidate",
    "midplatform_processing",
    "observation_update_candidate",
    "followup_model_route_candidate",
    "new_task_candidate",
)

CASE_1_ID = "Case-1-MobileSAM-to-OCR-Route-Candidate"
CASE_2_ID = "Case-2-MobileSAM-Correction-Midplatform-Routing"

VALIDATION_CAPABILITIES = (
    "result_envelope_to_midplatform_input",
    "result_candidate_does_not_pollute_observation",
    "midplatform_secondary_scheduling",
    "human_correction_closed_loop",
    "trace_closure",
)

FORBIDDEN_OPERATIONS = (
    "no_ocr_runner_execution",
    "no_detection_runner_execution",
    "no_pipeline_bypass_mobilesam_to_ocr",
    "no_direct_training_from_raw_correction",
    "midplatform_correction_entry_required",
    "mobilesam_output_not_direct_ui_routing",
    "mobilesam_does_not_assert_fact_label",
    "result_does_not_overwrite_attention_record",
    "result_candidate_not_observation_owner",
    "human_correction_must_not_modify_mask",
    "human_correction_priority_signal_only",
    "no_fact_write",
    "no_auto_fact_admission",
    "no_visual_expression_mutation",
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "ocr_runner_forbidden": True,
    "detection_runner_forbidden": True,
    "midplatform_schedules_not_pipeline": True,
    "midplatform_correction_entry_required": True,
    "no_direct_training_from_raw_correction": True,
    "result_as_evidence_only": True,
    "observation_attention_frozen_as_candidate": True,
    "new_task_candidate_only": True,
    "trace_closure_required": True,
}

RECOMMENDED_NEXT_EXECUTION = (
    "Phase-P1-Midplatform-Single-Model-Interaction-Validation-UI-Execution-v1-001"
)
