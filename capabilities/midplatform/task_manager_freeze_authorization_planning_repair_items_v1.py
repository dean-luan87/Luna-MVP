# -*- coding: utf-8 -*-
"""Task Manager freeze authorization planning repair — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Planning-Repair-v1-001"
SCOPE = "task_manager_freeze_authorization_planning_repair_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_freeze_authorization_planning_repair_v1_smoke_v0"
)

CANONICAL_REBUILD_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1_smoke_v0"
)

PLANNING_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_planning_v1_smoke_v0"
)

PLANNING_STAGE_ID = "midplatform_task_manager_foundation_handoff_freeze_authorization_planning_v1"
PLANNING_STAGE_KEY = "task_manager_freeze_authorization_planning"
PLANNING_RUNNER = "run_midplatform_task_manager_foundation_handoff_freeze_authorization_planning_v1"
PLANNING_FINAL_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_TASK_MANAGER_FREEZE_AUTHORIZATION_PLANNING_REPAIR_READY_FOR_CANONICAL_CHECKPOINT_REBUILD_TOPDOWN_RERUN"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_TASK_MANAGER_FREEZE_AUTHORIZATION_PLANNING_REPAIR_STILL_BLOCKED_BY_PLANNING_LOGIC_GAP"
)

NEXT_PHASE_COMPLETE = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Canonical-GO-Checkpoint-Rebuild-v1-001"
)
NEXT_PHASE_BLOCKED = PHASE_ID

PASS_FLAG = "freeze_authorization_planning_repair_complete"

REQUIRED_ORIGINAL_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_planning_v1.py",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "freeze_authorization_planning_repair_only": True,
    "candidate_only": True,
    "no_protocol_change": True,
    "no_model_route_touched": True,
    "no_world_model_assembly": True,
    "no_scene_graph_smoke_io": True,
    "no_task_reasoning": True,
    "no_field_simulation": True,
    "no_fake_go_artifacts": True,
    "no_issue_review_stage_created": True,
    "no_gap_review_stage_created": True,
    "no_rerun_review_stage_created": True,
}

FAILURE_CLASSES: Tuple[str, ...] = (
    "downstream_expectation_gap",
    "schema_output_gap",
    "evidence_mapping_gap",
    "genuine_logic_hold",
)
