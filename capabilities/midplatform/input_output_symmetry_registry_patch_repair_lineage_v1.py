# -*- coding: utf-8 -*-
"""Input/output symmetry registry patch repair — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.input_output_symmetry_registry_patch_repair_items_v1 import (
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
)

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/input_output_symmetry_registry_patch_repair_items_v1.py",
    "capabilities/midplatform/input_output_symmetry_registry_patch_repair_lineage_v1.py",
    "capabilities/midplatform/input_output_symmetry_registry_patch_repair_v1.py",
    "tools/evaluation/midplatform/run_input_output_symmetry_registry_patch_repair_v1.py",
    "tools/evaluation/midplatform/verify_input_output_symmetry_registry_patch_repair_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES

DOCS: Tuple[str, ...] = ()

ARTIFACTS: Tuple[str, ...] = (
    "input_output_symmetry_registry_patch_repair_report_v1.json",
    "canonical_rebuild_input_review_v1.json",
    "registry_patch_original_stage_locator_v1.json",
    "registry_patch_original_rerun_review_v1.json",
    "registry_patch_failure_classification_v1.json",
    "registry_patch_schema_output_repair_review_v1.json",
    "registry_patch_mapping_repair_review_v1.json",
    "registry_patch_downstream_expectation_review_v1.json",
    "registry_patch_final_decision_review_v1.json",
    "registry_patch_post_repair_rerun_review_v1.json",
    "canonical_checkpoint_scan_only_after_repair_review_v1.json",
    "no_issue_review_created_review_v1.json",
    "no_original_stage_pollution_review_v1.json",
    "no_protocol_change_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "file_size_governance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "canonical_rebuild_go_confirmed",
    "first_failed_stage_registry_patch_confirmed",
    "repair_plan_option_d_confirmed",
    "original_registry_patch_runner_found",
    "original_registry_patch_verifier_found",
    "original_registry_patch_rerun_attempted",
    "failure_classification_complete",
    "minimal_repair_applied",
    "no_issue_review_stage_created",
    "no_gap_review_stage_created",
    "no_original_summary_forged",
    "no_original_verifier_report_forged",
    "hold_not_marked_as_go",
    "no_protocol_change",
    "no_model_route_touched",
    "no_world_model_assembly",
    "no_scene_graph_smoke_io",
    "no_task_reasoning",
    "no_field_simulation",
    "canonical_scan_only_after_repair_attempted",
    "common_validation_reuse_ok",
    "registry_patch_repair_complete",
    "original_registry_patch_rerun_recorded",
    "canonical_scan_only_after_repair_recorded",
    "next_phase_readiness_ok",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (FINAL_DECISION_COMPLETE, FINAL_DECISION_BLOCKED)
