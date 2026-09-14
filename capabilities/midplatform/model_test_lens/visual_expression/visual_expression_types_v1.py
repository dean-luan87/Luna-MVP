# -*- coding: utf-8 -*-
"""Visual expression layer constants — planning v1."""

from __future__ import annotations

VISUAL_EXPRESSION_SYSTEM_ID = "LunaModelTestLensVisualExpressionSystemV1"
PHASE_REF = "Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-Planning-v1-001"

CANVAS_ROLES = ("spatial_localization",)
PANEL_ROLES = ("observation_judgment",)
SUMMARY_ROLES = ("frame_scheduling_summary",)
INTERACTION_ROLES = ("region_record_mapping",)

FORBIDDEN_VISUAL_OPERATIONS = (
    "draw_secondary_boundary_from_attention",
    "clone_segmentation_box_for_priority",
    "hide_segmentation_boundary_on_select",
    "replace_boundary_with_priority_box",
    "stack_multiple_model_boundary_systems",
    "icon_only_default_canvas_expression",
    "execute_runner_from_canvas_click",
    "not_runner_execution",
    "write_fact_from_visual_expression",
    "write_fact",
    "navigation_decision_from_visual_expression",
    "upgrade_prompt_label_to_fact_on_canvas",
    "treat_correction_as_ground_truth_on_canvas",
    "output_confirmed_dynamic_on_canvas_single_frame",
)

BOUNDARY_FLAGS = {
    "segmentation_is_sole_boundary_owner": True,
    "attention_annotation_layer_only": True,
    "planning_only": True,
    "candidate_only": True,
    "not_fact": True,
    "not_fact_write": True,
    "not_navigation_instruction": True,
    "not_runner_execution": True,
}
