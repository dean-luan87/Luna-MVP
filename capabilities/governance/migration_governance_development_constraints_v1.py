# -*- coding: utf-8 -*-
"""Canonical migration governance development constraints v1 — for verifier and capability reference.

Human-readable source of truth:
  docs/architecture/governance/LUNA_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_AND_ANTI_INCIDENT_RULES_V1.md

Machine-readable manifest:
  docs/architecture/governance/migration_governance_development_constraints_v1_manifest.json
"""

from __future__ import annotations

from pathlib import Path

CONSTRAINT_DOC_ID = "migration_governance_development_constraints_v1"
CONSTRAINT_DOC_REL_PATH = (
    "docs/architecture/governance/LUNA_MIGRATION_GOVERNANCE_DEVELOPMENT_CONSTRAINTS_AND_ANTI_INCIDENT_RULES_V1.md"
)
MANIFEST_REL_PATH = "docs/architecture/governance/migration_governance_development_constraints_v1_manifest.json"

REPO_ROOT = Path(__file__).resolve().parents[2]

MANDATORY_NON_EXECUTION_FREEZE_FIELDS = (
    "runtime_invoked",
    "execution_committed",
    "write_allowed",
    "authorization_granted_now",
    "owner_approval_granted_now",
    "operator_acknowledgement_granted_now",
    "execution_window_opened_now",
    "real_rehearsal_execution_allowed",
    "real_migration_execution_allowed",
    "batch_arming_allowed",
)

PHASE_TYPE_FLAGS = (
    "planning_only",
    "dryrun_only",
    "review_only",
    "roadmap_decision_only",
)

GOVERNANCE_DEBT_CATEGORIES = (
    "permission_semantics_debt",
    "boundary_object_debt",
    "evidence_chain_debt",
    "success_claim_debt",
    "owner_operator_debt",
    "test_harness_debt",
    "documentation_sync_debt",
    "terminology_debt",
    "automation_candidate_debt",
)

PHASE_GOVERNANCE_STANDARD_REUSE_RULE = (
    "New phase must reuse existing governance standard unless it proves a new governance need."
)
PHASE_GOVERNANCE_STANDARD_REUSE_RULE_ZH = (
    "新阶段必须复用已有治理标准，除非证明存在新的治理需求。"
)
FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF = "File Size & Module Split Governance Rule"
FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_DOC = (
    "docs/architecture/governance/LUNA_FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_V1.md"
)
FILE_SIZE_GOVERNANCE_INVENTORY_DOC = "docs/architecture/governance/LUNA_FILE_SIZE_GOVERNANCE_INVENTORY_V0.md"
REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF = "Reuse-First Protocol Engineering Rule"
MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF = "Module-First Development & Verification Cadence Rule"
MODULE_FIRST_CADENCE_RULE_DOC = "docs/architecture/governance/LUNA_MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_V1.md"
TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_REF = "Top-Level Objective Priority Rule"
TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_DOC = "docs/architecture/governance/LUNA_TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_V1.md"
RESULT_FIRST_MODULE_ENGINEERING_RULE_REF = "Result-First Module Engineering Rule"
RESULT_FIRST_MODULE_ENGINEERING_RULE_DOC = "docs/architecture/governance/LUNA_RESULT_FIRST_MODULE_ENGINEERING_RULE_V1.md"

PRE_PHASE_GATE_QUESTION_IDS = (
    "phase_kind_identified",
    "real_authorization_release_explicit",
    "real_execution_action_explicit",
    "file_operation_explicit",
    "subprocess_explicit",
    "runtime_explicit",
    "protected_hr_dnae_modification_explicit",
    "worldmodel_memory_fact_library_write_explicit",
    "evidence_generation_explicit",
    "evidence_supports_success_claim_explicit",
    "verifier_go_misread_risk_assessed",
    "final_decision_escalation_checked",
    "selected_route_permission_release_checked",
    "ready_semantics_disambiguated",
    "owner_operator_approval_required_checked",
    "execution_window_required_checked",
    "abort_authority_required_checked",
    "non_claims_required_checked",
    "terminology_review_required_checked",
    "governance_debt_registration_required_checked",
    "existing_governance_standard_reuse_checked",
    "new_governance_need_proven_if_deviating",
)

CANONICAL_NON_CLAIM_SNIPPET = (
    "GO only means this phase passed its scoped checks. "
    "It does not mean real execution is authorized, completed, or successful."
)

VERIFIER_RULE_IDS = (
    "phase_semantics_must_match_final_decision_or_no_go",
    "non_execution_phase_must_freeze_mandatory_summary_fields",
    "roadmap_selected_route_must_not_release_execution_permissions",
    "success_claim_must_remain_blocked_until_explicit_gate",
    "boundary_matrix_required_for_migration_phases_or_no_go",
    "terminology_review_fail_means_no_go",
    "verifier_go_must_not_imply_execution_or_success_claim",
    "new_phase_must_reuse_existing_governance_standard_unless_new_need_proven",
)


def governance_constraints_doc_path() -> Path:
    return REPO_ROOT / CONSTRAINT_DOC_REL_PATH


def governance_constraints_manifest_path() -> Path:
    return REPO_ROOT / MANIFEST_REL_PATH


def assert_non_execution_summary_frozen(summary: dict) -> list[str]:
    """Return violation messages if mandatory freeze fields are not false."""
    violations: list[str] = []
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        if summary.get(field) is not False:
            violations.append(f"{field} must be false for non-execution phase")
    return violations
