# -*- coding: utf-8 -*-
"""Upstream GO artifact chain bootstrap for SLAM P0 — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_revalidation_items_v1 import (
    BOOTSTRAP_RUN_SCRIPTS,
    P0_TCP_OUTPUT,
)

PHASE_ID = "Phase-Midplatform-Upstream-GO-Artifact-Chain-Bootstrap-For-SLAM-P0-v1-001"
SCOPE = "upstream_go_artifact_chain_bootstrap_for_slam_p0_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "upstream_go_artifact_chain_bootstrap_for_slam_p0_v1_smoke_v0"
)

REVALIDATION_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "slam_spatial_mapping_task_collaboration_planning_revalidation_v1_smoke_v0"
)

REVALIDATION_BLOCKED_DECISION = (
    "MIDPLATFORM_SLAM_SPATIAL_MAPPING_TASK_COLLABORATION_PLANNING_REVALIDATION_BLOCKED_BY_UPSTREAM_GAP"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_UPSTREAM_GO_ARTIFACT_CHAIN_BOOTSTRAP_FOR_SLAM_P0_READY_FOR_TRACKING_OPTICALFLOW_TASK_COLLABORATION_REVALIDATION"
)
FINAL_DECISION_STOPPED = (
    "MIDPLATFORM_UPSTREAM_GO_ARTIFACT_CHAIN_BOOTSTRAP_FOR_SLAM_P0_STOPPED_BY_FIRST_NON_GO_UPSTREAM"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Tracking-OpticalFlow-Task-Collaboration-Planning-Revalidation-v1-001"
)
NEXT_PHASE_STOPPED = (
    "Phase-Midplatform-Upstream-GO-Artifact-Chain-Bootstrap-For-SLAM-P0-v1-001"
)

PASS_FLAG = "upstream_go_artifact_chain_bootstrap_for_slam_p0_pass"

SLAM_P0_REVALIDATION_SCRIPT = (
    "run_slam_spatial_mapping_task_collaboration_planning_revalidation_v1"
)

SLAM_P0_STAGE_SCRIPTS: Tuple[str, ...] = (
    "run_slam_spatial_mapping_model_smoke_io_inspection_v1",
    "run_slam_spatial_mapping_adapter_skeleton_v1",
    "run_slam_spatial_mapping_task_collaboration_planning_v1",
)

STAGE_GROUPS: Dict[str, str] = {}
for _s in BOOTSTRAP_RUN_SCRIPTS[:11]:
    STAGE_GROUPS[_s] = "A_foundation_task_manager"
for _s in BOOTSTRAP_RUN_SCRIPTS[11:44]:
    STAGE_GROUPS[_s] = "B_field_first_real_model"
for _s in BOOTSTRAP_RUN_SCRIPTS[44:46]:
    STAGE_GROUPS[_s] = "C_model_workflow_priority"
for _s in BOOTSTRAP_RUN_SCRIPTS[46:]:
    STAGE_GROUPS[_s] = "D_slam_p0_upstream"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "bootstrap_only": True,
    "bootstrap_only": True,
    "no_scene_graph_smoke_io": True,
    "no_world_model_assembly": True,
    "no_task_reasoning": True,
    "no_action_output": True,
    "no_new_protocol_added": True,
    "no_field_simulation": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_real_inference_execution": True,
    "no_fake_go_artifacts": True,
    "no_forced_summary_mutation": True,
}

PROHIBITED_SCOPE: Tuple[str, ...] = (
    "world_model_assembly",
    "scene_graph_smoke_io",
    "task_reasoning",
    "action_output",
    "field_simulation",
    "new_protocol",
    "new_model_adapter",
    "fake_go_artifacts",
    "forced_summary_mutation",
)
