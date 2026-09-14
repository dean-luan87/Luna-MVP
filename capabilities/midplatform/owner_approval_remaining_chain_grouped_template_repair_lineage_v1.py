# -*- coding: utf-8 -*-
"""Owner approval remaining chain grouped template repair — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.owner_approval_remaining_chain_grouped_template_repair_items_v1 import (
    FINAL_DECISION_COMPLETE,
    FINAL_DECISION_PARTIAL,
)

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/owner_approval_remaining_chain_grouped_template_repair_items_v1.py",
    "capabilities/midplatform/owner_approval_remaining_chain_grouped_template_repair_lineage_v1.py",
    "capabilities/midplatform/owner_approval_remaining_chain_grouped_template_repair_v1.py",
    "tools/evaluation/midplatform/run_owner_approval_remaining_chain_grouped_template_repair_v1.py",
    "tools/evaluation/midplatform/verify_owner_approval_remaining_chain_grouped_template_repair_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES
DOCS: Tuple[str, ...] = ()

ARTIFACTS: Tuple[str, ...] = (
    "grouped_template_repair_report_v1.json",
    "batch_detection_input_review_v1.json",
    "safe_template_candidate_execution_matrix_v1.json",
    "group_p_planning_template_repair_review_v1.json",
    "group_d_dryrun_template_repair_review_v1.json",
    "group_r_post_review_template_repair_review_v1.json",
    "per_stage_original_rerun_results_v1.json",
    "per_stage_final_decision_alignment_review_v1.json",
    "per_stage_evidence_traceability_repair_review_v1.json",
    "per_stage_downstream_readiness_repair_review_v1.json",
    "group_g_untouched_review_v1.json",
    "group_m_untouched_review_v1.json",
    "canonical_checkpoint_scan_only_after_grouped_repair_v1.json",
    "canonical_checkpoint_topdown_after_grouped_repair_v1.json",
    "no_issue_review_created_review_v1.json",
    "no_gap_review_created_review_v1.json",
    "no_rerun_review_created_review_v1.json",
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
    "batch_detection_go_confirmed",
    "all_safe_candidates_processed",
    "all_safe_candidates_original_rerun_attempted",
    "final_decision_pass_blocker_alignment_checked",
    "evidence_traceability_template_repair_checked",
    "downstream_readiness_gap_conversion_checked",
    "group_g_untouched",
    "group_m_untouched",
    "no_issue_review_stage_created",
    "no_gap_review_stage_created",
    "no_rerun_review_stage_created",
    "no_fake_go_artifacts",
    "no_protocol_change",
    "no_model_route_touched",
    "no_world_model_assembly",
    "no_scene_graph_smoke_io",
    "no_task_reasoning",
    "no_field_simulation",
    "canonical_scan_only_after_repair_attempted",
    "canonical_scan_only_after_repair_recorded",
    "issuance_closure_template_chain_cleared",
    "first_failed_advanced_to_group_g",
    "next_phase_readiness_ok",
    "grouped_template_repair_complete",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (
    FINAL_DECISION_COMPLETE,
    FINAL_DECISION_PARTIAL,
)
