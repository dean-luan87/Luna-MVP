# -*- coding: utf-8 -*-
"""Owner approval remaining chain batch pattern detection — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.owner_approval_remaining_chain_batch_pattern_detection_items_v1 import (
    FINAL_DECISION_COMPLETE,
)

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/owner_approval_remaining_chain_batch_pattern_detection_items_v1.py",
    "capabilities/midplatform/owner_approval_remaining_chain_batch_pattern_detection_lineage_v1.py",
    "capabilities/midplatform/owner_approval_remaining_chain_batch_pattern_detection_scan_v1.py",
    "capabilities/midplatform/owner_approval_remaining_chain_batch_pattern_detection_and_repair_plan_v1.py",
    "tools/evaluation/midplatform/run_owner_approval_remaining_chain_batch_pattern_detection_and_repair_plan_v1.py",
    "tools/evaluation/midplatform/verify_owner_approval_remaining_chain_batch_pattern_detection_and_repair_plan_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES
DOCS: Tuple[str, ...] = ()

ARTIFACTS: Tuple[str, ...] = (
    "batch_pattern_detection_report_v1.json",
    "remaining_stage_inventory_v1.json",
    "remaining_stage_family_classification_v1.json",
    "remaining_stage_gap_classification_v1.json",
    "downstream_expectation_gap_matrix_v1.json",
    "runner_verifier_decision_drift_matrix_v1.json",
    "evidence_traceability_gap_matrix_v1.json",
    "schema_output_gap_matrix_v1.json",
    "verifier_locator_gap_matrix_v1.json",
    "genuine_logic_hold_candidate_matrix_v1.json",
    "batch_repair_group_plan_v1.json",
    "safe_template_repair_candidates_v1.json",
    "stages_requiring_individual_repair_v1.json",
    "no_issue_review_created_review_v1.json",
    "no_original_stage_pollution_review_v1.json",
    "no_protocol_change_review_v1.json",
    "no_model_route_touched_review_v1.json",
    "no_world_model_boundary_review_v1.json",
    "owner_constraint_compliance_review_v1.json",
    "common_validation_reuse_report_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "canonical_rebuild_go_confirmed",
    "go_stage_count_at_least_7",
    "first_failed_stage_is_issuance_planning",
    "remaining_stage_count_detected_at_least_19",
    "remaining_stage_inventory_complete",
    "family_classification_complete",
    "gap_classification_complete",
    "batch_repair_group_plan_complete",
    "no_issue_review_stage_created",
    "no_gap_review_stage_created",
    "no_rerun_review_stage_created",
    "no_original_stage_pollution",
    "no_fake_go_artifacts",
    "no_protocol_change",
    "no_model_route_touched",
    "no_world_model_assembly",
    "no_scene_graph_smoke_io",
    "no_task_reasoning",
    "no_field_simulation",
    "common_validation_reuse_ok",
    "batch_pattern_detection_complete",
    "repair_group_plan_complete",
    "safe_template_repair_candidates_identified",
    "individual_repair_required_stages_identified",
    "next_phase_readiness_ok",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (FINAL_DECISION_COMPLETE,)
