# -*- coding: utf-8 -*-
"""Module handoff gap closure — items v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-Gap-Closure-v1-001"
SCOPE = "task_manager_owner_approval_request_module_handoff_gap_closure_only"

DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_handoff_gap_closure_v1_smoke_v0"
)

BOOTSTRAP_GAP_CLOSURE_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "upstream_go_artifact_chain_bootstrap_for_slam_p0_v1_smoke_v0"
)

MODULE_HANDOFF_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_handoff_v1_smoke_v0"
)

MODULE_GOVERNANCE_CLOSURE_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_governance_closure_v1_smoke_v0"
)

BROADER_ROADMAP_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_broader_midplatform_closure_roadmap_v1_smoke_v0"
)

FINAL_DECISION_COMPLETE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_GAP_CLOSURE_READY_FOR_UPSTREAM_GO_ARTIFACT_CHAIN_BOOTSTRAP_FOR_SLAM_P0_RERUN"
)
FINAL_DECISION_BLOCKED = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_GAP_CLOSURE_STILL_BLOCKED_BY_HANDOFF_ARTIFACT_GAP"
)

NEXT_PHASE_COMPLETE = "Phase-Midplatform-Upstream-GO-Artifact-Chain-Bootstrap-For-SLAM-P0-v1-001"
NEXT_PHASE_BLOCKED = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-Gap-Closure-v1-001"
)

PASS_FLAG = "task_manager_owner_approval_request_module_handoff_gap_closure_pass"

HANDOFF_RUN_SCRIPT = "run_task_manager_owner_approval_request_module_handoff_v1"
BROADER_ROADMAP_RUN_SCRIPT = "run_task_manager_broader_midplatform_closure_roadmap_v1"

REQUIRED_HANDOFF_SOURCE_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_handoff_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_handoff_v1.py",
)

OPTIONAL_HANDOFF_SOURCE_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_items_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_lineage_v1.py",
)

OPTIONAL_HANDOFF_DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_V1_GO_NO_GO_PACK_V0.md",
)

HANDOFF_ARTIFACTS: Tuple[str, ...] = (
    "owner_approval_request_module_handoff_report_v1.json",
    "owner_approval_request_module_status_summary_v1.json",
    "owner_approval_request_midplatform_integration_position_v1.json",
    "owner_approval_request_handoff_boundary_v1.json",
    "midplatform_mainline_return_plan_v1.json",
    "future_test_strategy_v1.json",
    "governance_debt_and_future_runtime_handoff_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "gap_closure_only": True,
    "no_protocol_change": True,
    "no_model_route_touched": True,
    "no_world_model_assembly": True,
    "no_scene_graph_smoke_io": True,
    "no_task_reasoning": True,
    "no_field_simulation": True,
    "no_action_output": True,
    "no_fake_go_artifacts": True,
}
