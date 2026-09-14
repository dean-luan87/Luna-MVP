# -*- coding: utf-8
"""Perception Tool Layer — freeze and handoff types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Perception-Tool-Layer-Freeze-And-Handoff-v1-001"
SYSTEM_ID = "LunaMidplatformPerceptionToolLayerFreezeV1"
FREEZE_ONLY = True

ARCHITECTURE_STATUS = "frozen"
EXECUTION_STATUS = "available_in_test_only"
OPTIMIZATION_STATUS = "paused"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_GO",
    "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_GO",
    "P1_MIDPLATFORM_TEXT_FIRST_TARGET_PROPOSAL_VALIDATION_PLANNING_GO",
    "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_GO",
    "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_GO",
    "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO",
)

FROZEN_CHAIN = (
    "input_image",
    "observation_attention",
    "task_candidate",
    "runner_admission",
    "controlled_execution",
    "result_envelope",
    "midplatform_processing",
    "model_collaboration_candidate",
)

VERIFIED_MODELS = (
    "mobile_sam",
    "ocr_route_candidate",
    "dual_route_stub",
    "scene_task_model_activation_stub",
)

FINAL_GO = "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_BLOCKED"
SMOKE_GO = "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_SMOKE_GO"
SMOKE_BLOCKED = "P1_MIDPLATFORM_PERCEPTION_TOOL_LAYER_FREEZE_SMOKE_BLOCKED"

RECOMMENDED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Luna-Perception-Controller-Planning-v1-001"
)

DOCS_REL = "docs/perception_tool_layer_freeze_report_v1.md"
ISSUE_REGISTRY_REL = "schemas/perception_controller/perception_tool_layer_issue_registry_v1.json"

FREEZE_FORBIDDEN = (
    "optimize_mobilesam_prompt",
    "add_sam_scene_prompt",
    "add_ocr_scene_exception",
    "integrate_new_vision_model",
    "modify_runner_governance",
    "modify_observation_attention_schema",
)
