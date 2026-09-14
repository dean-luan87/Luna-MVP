# -*- coding: utf-8 -*-
"""Task Manager / Owner Approval canonical GO checkpoint rebuild — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.task_manager_owner_approval_canonical_go_checkpoint_rebuild_items_v1 import (
    FINAL_DECISION_COMPLETE,
    STAGE_CHAIN,
)

FINAL_DECISION_GO = FINAL_DECISION_COMPLETE

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/canonical_go_checkpoint_rebuild_scan_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_canonical_go_checkpoint_rebuild_items_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_canonical_go_checkpoint_rebuild_lineage_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES

DOCS: Tuple[str, ...] = (
    "docs/architecture/midplatform/LUNA_MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_CANONICAL_GO_CHECKPOINT_REBUILD_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_CANONICAL_GO_CHECKPOINT_REBUILD_V1.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_CANONICAL_GO_CHECKPOINT_REBUILD_V1_GO_NO_GO_PACK_V0.md",
)

ARTIFACTS: Tuple[str, ...] = (
    "task_manager_owner_approval_canonical_go_checkpoint_rebuild_report_v1.json",
    "canonical_checkpoint_registry_v1.json",
    "downstream_readable_checkpoint_index_v1.json",
    "final_decision_mapping_registry_v1.json",
    "upstream_downstream_reference_map_v1.json",
    "first_failed_stage_review_v1.json",
    "failed_stage_registry_v1.json",
    "downstream_blockage_projection_v1.json",
    "canonical_checkpoint_gap_classification_v1.json",
    "checkpoint_rebuild_repair_plan_v1.json",
    "checkpoint_rebuild_execution_mode_review_v1.json",
    "no_original_stage_pollution_review_v1.json",
    "no_protocol_change_review_v1.json",
    "no_world_model_boundary_review_v1.json",
    "no_model_route_touched_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "checkpoint_rebuild_scope_respected",
    "no_original_stage_pollution",
    "no_original_summary_overwritten",
    "no_original_verifier_report_overwritten",
    "no_fake_go_artifacts",
    "no_protocol_change",
    "no_model_route_touched",
    "no_world_model_assembly",
    "no_scene_graph_smoke_io",
    "no_task_reasoning",
    "no_field_simulation",
    "scan_order_topdown",
    "canonical_checkpoint_registry_exists",
    "downstream_readable_checkpoint_index_exists",
    "final_decision_mapping_registry_exists",
    "upstream_downstream_reference_map_exists",
    "first_failed_stage_review_exists",
    "failed_stage_registry_exists",
    "gap_classification_exists",
    "repair_plan_exists",
    "per_stage_checkpoints_generated",
    "hold_not_marked_as_go",
    "missing_verifier_report_not_marked_as_go",
    "common_validation_reuse_ok",
    "checkpoint_rebuild_complete",
    "canonical_checkpoint_registry_complete",
    "downstream_readable_checkpoint_index_complete",
    "first_failed_stage_identified",
    "failed_stage_registry_complete",
    "gap_classification_complete",
    "repair_plan_complete",
    "next_phase_readiness_ok",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (FINAL_DECISION_COMPLETE,)

EXPECTED_STAGE_COUNT: int = len(STAGE_CHAIN)
