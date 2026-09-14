# -*- coding: utf-8 -*-
"""Followup runner route constants — planning v1."""

from __future__ import annotations

FOLLOWUP_RUNNER_ROUTE_SYSTEM_ID = "LunaModelTestLensFollowupRunnerRouteV1"
PHASE_REF = "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-Planning-v1-001"
PLANNING_ONLY = True

PIPELINE_STAGES = (
    "segmentation_region",
    "observation_attention_record",
    "followup_model_route_candidate",
    "runner_task_candidate",
    "manual_trigger",
    "future_scheduler_trigger",
)

TARGET_MODEL_IDS = (
    "detection", "ocr", "tracking", "depth", "slam", "slam_reference",
    "motion_analysis", "walkable_area_review", "vio", "vlm",
    "human_review", "no_followup_required",
)

QUEUE_ADMISSION = ("auto_eligible", "manual_only", "rejected")
TRIGGER_MODES = ("manual_only", "scheduler_candidate")

PRIORITY_ADMISSION_DEFAULT = {
    "P0_immediate_attention": "auto_eligible",
    "P1_high_attention": "auto_eligible",
    "P2_medium_attention": "manual_only",
    "P3_low_attention": "manual_only",
    "ignore_for_now": "rejected",
}

FORBIDDEN_OPERATIONS = (
    "no_runner_execution",
    "no_model_call",
    "no_fact_write",
    "no_navigation_decision",
    "no_auto_runner_trigger",
    "no_human_correction_ground_truth",
    "no_prompt_label_fact_upgrade",
    "no_motion_confirmed_from_single_frame",
    "no_visual_expression_mutation",
    "execute_runner",
    "automatic_model_invocation",
    "auto_runner_trigger",
    "write_fact",
    "navigation_decision",
    "mutate_visual_expression_system",
    "upgrade_prompt_label_to_fact",
    "treat_human_correction_as_ground_truth",
    "output_confirmed_dynamic_single_frame",
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "runner_task_candidate_only": True,
    "not_runner_execution": True,
    "not_fact": True,
    "not_fact_write": True,
    "not_auto_runner_trigger": True,
    "not_navigation_instruction": True,
    "followup_model_route_candidate_only": True,
    "human_correction_priority_signal_only": True,
    "visual_expression_system_frozen": True,
}

RECOMMENDED_NEXT_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-And-Post-Review-v1-001"
)
