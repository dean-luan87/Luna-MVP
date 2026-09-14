# -*- coding: utf-8 -*-
"""Owner Approval Request Governance Gate template lineage — split from main lineage file."""

from __future__ import annotations

from typing import Dict, Tuple

GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review",
        "stage_term": "freeze_authorization_grant_owner_approval_request_final_gate_planning",
    },
    {
        "base_term": "post_review_only",
        "stage_term": "final_gate_planning_only",
    },
    {
        "base_term": "prior_record_approval_closure_dryrun_go",
        "stage_term": "prior_record_approval_closure_post_review_go",
    },
    {
        "base_term": "dryrun_result_accepted",
        "stage_term": "final_gate_plan_complete",
    },
    {
        "base_term": "candidate_review_ok",
        "stage_term": "final_gate_readiness_matrix_complete",
    },
    {
        "base_term": "final_gate_planning_readiness",
        "stage_term": "roadmap_decision_readiness",
    },
    {
        "base_term": "record-approval-closure-post-review-scope",
        "stage_term": "final-gate-planning-scope",
    },
)

GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_record_approval_closure_post_review_go",
    "final_gate_plan_complete",
    "final_gate_readiness_matrix_complete",
    "missing_conditions_matrix_complete",
    "blocker_matrix_complete",
    "module_first_cadence_rule_ref_ok",
    "reuse_first_rule_ref_ok",
    "validate_once_rule_ref_ok",
    "final_gate_planning_only",
    "roadmap_decision_readiness",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1.py",
)

GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "freeze_authorization_grant_owner_approval_request_final_gate_planning",
        "stage_term": "freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision",
    },
    {
        "base_term": "final_gate_planning_only",
        "stage_term": "roadmap_decision_only",
    },
    {
        "base_term": "prior_record_approval_closure_post_review_go",
        "stage_term": "prior_final_gate_planning_go",
    },
    {
        "base_term": "final_gate_plan_complete",
        "stage_term": "roadmap_decision_complete",
    },
    {
        "base_term": "roadmap_decision_readiness",
        "stage_term": "issuance_authorization_planning_readiness",
    },
    {
        "base_term": "final-gate-planning-scope",
        "stage_term": "final-gate-roadmap-decision-scope",
    },
)

GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_final_gate_planning_go",
    "roadmap_decision_complete",
    "route_matrix_complete",
    "missing_conditions_route_mapping_complete",
    "selected_route_rationale_complete",
    "selected_route_is_authorization_planning",
    "real_request_issuance_not_executed",
    "roadmap_decision_only",
    "issuance_authorization_planning_readiness",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1.py",
)

OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "freeze_authorization_grant_owner_approval_request_final_gate_planning",
        "stage_term": "owner_approval_request_governance_gate_integrated_planning",
    },
    {
        "base_term": "final_gate_planning_only",
        "stage_term": "integrated_planning_only",
    },
    {
        "base_term": "prior_record_approval_closure_post_review_go",
        "stage_term": "prior_final_gate_planning_go",
    },
    {
        "base_term": "final_gate_plan_complete",
        "stage_term": "integrated_planning_complete",
    },
    {
        "base_term": "roadmap_decision_readiness",
        "stage_term": "roadmap_decision_integrated",
    },
    {
        "base_term": "final-gate-planning-scope",
        "stage_term": "governance-gate-integrated-planning-scope",
    },
)

OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_final_gate_planning_go",
    "integrated_planning_complete",
    "roadmap_decision_integrated",
    "missing_conditions_route_mapping_complete",
    "issuance_authorization_plan_complete",
    "record_approval_ack_evidence_boundary_complete",
    "module_level_slice_test_plan_complete",
    "route_matrix_complete",
    "integrated_planning_only",
    "real_request_issuance_not_executed",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_governance_gate_integrated_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_owner_approval_request_governance_gate_integrated_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_owner_approval_request_governance_gate_integrated_planning_v1.py",
)

OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "owner_approval_request_governance_gate_integrated_planning",
        "stage_term": "owner_approval_request_governance_gate_integrated_implementation",
    },
    {
        "base_term": "integrated_planning_only",
        "stage_term": "integrated_implementation_only",
    },
    {
        "base_term": "integrated_planning_complete",
        "stage_term": "integrated_plan_complete",
    },
    {
        "base_term": "roadmap_decision_integrated",
        "stage_term": "integrated_roadmap_decision_complete",
    },
    {
        "base_term": "governance-gate-integrated-planning-scope",
        "stage_term": "governance-gate-integrated-implementation-scope",
    },
)

OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_IMPLEMENTATION_STAGE_ADDITIONS: Tuple[str, ...] = (
    "integrated_plan_complete",
    "integrated_roadmap_decision_complete",
    "issuance_authorization_preparation_package_complete",
    "missing_conditions_routing_complete",
    "real_issuance_precondition_checklist_complete",
    "module_level_functional_slice_test_plan_complete",
    "top_level_objective_priority_rule_ref_ok",
    "integrated_implementation_only",
    "no_fragmentary_phase_expansion",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_governance_gate_integrated_implementation_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_governance_gate_integrated_implementation_v1.py",
)

OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "owner_approval_request_governance_gate_integrated_implementation",
        "stage_term": "owner_approval_request_authorization_preparation_dryrun",
    },
    {
        "base_term": "integrated_implementation_only",
        "stage_term": "authorization_preparation_dryrun_only",
    },
    {
        "base_term": "integrated_plan_complete",
        "stage_term": "authorization_preparation_package_validation_ok",
    },
    {
        "base_term": "issuance_authorization_preparation_package_complete",
        "stage_term": "authorization_preparation_dryrun_pass",
    },
    {
        "base_term": "governance-gate-integrated-implementation-scope",
        "stage_term": "authorization-preparation-dryrun-scope",
    },
)

OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_integrated_implementation_go",
    "authorization_preparation_package_validation_ok",
    "authorization_precondition_validation_ok",
    "missing_conditions_routing_validation_ok",
    "real_issuance_safety_boundary_ok",
    "authorization_preparation_dryrun_only",
    "authorization_preparation_dryrun_pass",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_authorization_preparation_dryrun_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_authorization_preparation_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_authorization_preparation_dryrun_v1.py",
)

OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "owner_approval_request_authorization_preparation_dryrun",
        "stage_term": "owner_approval_request_module_level_functional_slice_planning",
    },
    {
        "base_term": "authorization_preparation_dryrun_only",
        "stage_term": "functional_slice_planning_only",
    },
    {
        "base_term": "authorization_preparation_dryrun_pass",
        "stage_term": "functional_slice_plan_complete",
    },
    {
        "base_term": "authorization-preparation-dryrun-scope",
        "stage_term": "module-level-functional-slice-planning-scope",
    },
)

OWNER_APPROVAL_REQUEST_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_authorization_preparation_dryrun_go",
    "functional_slice_plan_complete",
    "functional_slice_registry_complete",
    "result_first_rule_ref_ok",
    "module_first_cadence_rule_ref_ok",
    "functional_slice_planning_only",
    "functional_slice_tests_not_executed",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_module_level_functional_slice_planning_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_level_functional_slice_planning_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_level_functional_slice_planning_v1.py",
)

OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "owner_approval_request_module_level_functional_slice_planning",
        "stage_term": "owner_approval_request_functional_slice_dryrun",
    },
    {
        "base_term": "functional_slice_planning_only",
        "stage_term": "functional_slice_dryrun_only",
    },
    {
        "base_term": "functional_slice_plan_complete",
        "stage_term": "functional_slice_dryrun_pass",
    },
    {
        "base_term": "module-level-functional-slice-planning-scope",
        "stage_term": "functional-slice-dryrun-scope",
    },
)

OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_functional_slice_planning_go",
    "functional_slice_dryrun_registry_complete",
    "all_slice_primary_results_reached",
    "forbidden_state_transitions_absent",
    "functional_slice_real_execution_absent",
    "functional_slice_dryrun_only",
    "single_phase_all_slices",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_functional_slice_dryrun_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_functional_slice_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_functional_slice_dryrun_v1.py",
)

OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "owner_approval_request_functional_slice_dryrun",
        "stage_term": "owner_approval_request_module_governance_closure",
    },
    {
        "base_term": "functional_slice_dryrun_only",
        "stage_term": "module_governance_closure_only",
    },
    {
        "base_term": "functional_slice_dryrun_pass",
        "stage_term": "module_governance_closure_pass",
    },
    {
        "base_term": "functional-slice-dryrun-scope",
        "stage_term": "module-governance-closure-scope",
    },
)

OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_functional_slice_dryrun_go",
    "module_result_closure_complete",
    "governance_rule_closure_complete",
    "non_execution_closure_complete",
    "module_closure_decision_complete",
    "current_module_state_governance_candidate_chain_closed",
    "real_execution_not_authorized",
    "module_governance_closure_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)

OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_module_governance_closure_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_governance_closure_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_governance_closure_v1.py",
)

OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {
        "base_term": "owner_approval_request_module_governance_closure",
        "stage_term": "owner_approval_request_module_handoff",
    },
    {
        "base_term": "module_governance_closure_only",
        "stage_term": "module_handoff_only",
    },
    {
        "base_term": "module_governance_closure_pass",
        "stage_term": "module_handoff_pass",
    },
    {
        "base_term": "module-governance-closure-scope",
        "stage_term": "module-handoff-scope",
    },
)

OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_module_governance_closure_go",
    "module_handoff_report_complete",
    "owner_approval_request_chain_not_extended",
    "real_execution_not_authorized",
    "module_handoff_only",
    "return_to_midplatform_mainline",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
