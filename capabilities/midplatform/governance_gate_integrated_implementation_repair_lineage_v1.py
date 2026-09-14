# -*- coding: utf-8 -*-
"""Governance gate integrated implementation repair — lineage v1."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.governance_gate_integrated_implementation_repair_items_v1 import (
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
)

WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "capabilities/midplatform/governance_gate_integrated_implementation_repair_items_v1.py",
    "capabilities/midplatform/governance_gate_integrated_implementation_repair_lineage_v1.py",
    "capabilities/midplatform/governance_gate_integrated_implementation_repair_v1.py",
    "tools/evaluation/midplatform/run_governance_gate_integrated_implementation_repair_v1.py",
    "tools/evaluation/midplatform/verify_governance_gate_integrated_implementation_repair_v1.py",
)

PHASE_PYTHON_FILES: Tuple[str, ...] = WHITELIST_FILES
DOCS: Tuple[str, ...] = ()

ARTIFACTS: Tuple[str, ...] = (
    "governance_gate_integrated_implementation_repair_report_v1.json",
    "canonical_rebuild_input_review_v1.json",
    "governance_gate_integrated_implementation_original_stage_locator_v1.json",
    "governance_gate_integrated_implementation_original_rerun_review_v1.json",
    "governance_gate_integrated_implementation_failure_classification_v1.json",
    "governance_gate_integrated_implementation_decision_drift_repair_review_v1.json",
    "governance_gate_integrated_implementation_schema_output_repair_review_v1.json",
    "governance_gate_integrated_implementation_downstream_expectation_repair_review_v1.json",
    "governance_gate_integrated_implementation_traceability_repair_review_v1.json",
    "governance_gate_integrated_implementation_final_decision_review_v1.json",
    "governance_gate_integrated_implementation_post_repair_rerun_review_v1.json",
    "canonical_checkpoint_scan_only_after_repair_review_v1.json",
    "canonical_checkpoint_topdown_after_repair_review_v1.json",
    "group_g_scope_review_v1.json",
    "group_m_untouched_review_v1.json",
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
    "grouped_template_repair_go_confirmed",
    "first_failed_stage_governance_gate_confirmed",
    "record_closure_post_review_checkpoint_go_readable",
    "original_governance_gate_runner_found",
    "original_governance_gate_verifier_found",
    "original_governance_gate_rerun_attempted",
    "failure_classification_complete",
    "runner_verifier_decision_drift_checked",
    "evidence_traceability_gap_checked",
    "downstream_expectation_gap_checked",
    "minimal_repair_applied",
    "group_m_untouched",
    "no_issue_review_stage_created",
    "no_gap_review_stage_created",
    "no_rerun_review_stage_created",
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
    "canonical_scan_only_after_repair_recorded",
    "next_phase_readiness_ok",
    "governance_gate_integrated_implementation_repair_complete",
    "original_governance_gate_integrated_implementation_rerun_recorded",
)

VALID_FINAL_DECISIONS: Tuple[str, ...] = (FINAL_DECISION_COMPLETE, FINAL_DECISION_BLOCKED)
