# -*- coding: utf-8 -*-
"""Input/output symmetry registry patch repair — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = "Phase-Midplatform-Input-Output-Symmetry-Registry-Patch-Repair-v1-001"
SCOPE = "input_output_symmetry_registry_patch_repair_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "input_output_symmetry_registry_patch_repair_v1_smoke_v0"
)

CANONICAL_REBUILD_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1_smoke_v0"
)

REGISTRY_PATCH_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_protocol_input_output_symmetry_registry_patch_v1_smoke_v0"
)

REGISTRY_PATCH_STAGE_ID = "midplatform_protocol_input_output_symmetry_registry_patch_v1"
REGISTRY_PATCH_RUNNER = "run_midplatform_protocol_input_output_symmetry_registry_patch_v1"
REGISTRY_PATCH_FINAL_GO = (
    "MIDPLATFORM_PROTOCOL_INPUT_OUTPUT_SYMMETRY_REGISTRY_PATCH_READY_FOR_OWNER_APPROVAL_REQUEST_PLANNING"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_INPUT_OUTPUT_SYMMETRY_REGISTRY_PATCH_REPAIR_READY_FOR_CANONICAL_CHECKPOINT_REBUILD_TOPDOWN_RERUN"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_INPUT_OUTPUT_SYMMETRY_REGISTRY_PATCH_REPAIR_STILL_BLOCKED_BY_REGISTRY_PATCH_LOGIC_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Canonical-GO-Checkpoint-Rebuild-v1-001"
)
NEXT_PHASE_BLOCKED = PHASE_ID

PASS_FLAG = "registry_patch_repair_complete"

REQUIRED_ORIGINAL_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/protocol_input_output_symmetry_registry_patch_v1.py",
    "tools/evaluation/midplatform/run_midplatform_protocol_input_output_symmetry_registry_patch_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_protocol_input_output_symmetry_registry_patch_v1.py",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "registry_patch_repair_only": True,
    "candidate_only": True,
    "no_protocol_change": True,
    "no_model_route_touched": True,
    "no_world_model_assembly": True,
    "no_scene_graph_smoke_io": True,
    "no_task_reasoning": True,
    "no_field_simulation": True,
    "no_action_output": True,
    "no_fake_go_artifacts": True,
    "no_issue_review_stage_created": True,
    "no_gap_review_stage_created": True,
    "repair_plan_option_d": True,
}

FAILURE_CLASSES: Tuple[str, ...] = (
    "schema_output_gap",
    "registry_mapping_gap",
    "downstream_expectation_gap",
    "genuine_logic_hold",
)
