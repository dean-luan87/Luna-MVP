# -*- coding: utf-8 -*-
"""Model adapter priority sequence planning — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_field_simulation": True,
    "no_simulation_test_route": True,
    "no_task_reasoning_execution": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_task_action_output": True,
    "no_model_runtime": True,
    "no_unauthorized_download": True,
    "no_new_protocol_without_reason": True,
    "priority_sequence_planning_only": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_MODEL_ADAPTER_PRIORITY_SEQUENCE_PLANNING_READY_FOR_SLAM_SPATIAL_MAPPING_ADAPTER_SKELETON"
)
