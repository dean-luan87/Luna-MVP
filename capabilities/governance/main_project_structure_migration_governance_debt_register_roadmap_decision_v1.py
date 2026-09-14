# -*- coding: utf-8 -*-
"""Main Project Structure Migration Governance Debt Register Roadmap Decision v1.

Roadmap decision only: select Permission Semantics Canonicalization Planning (Route A)
with Route B/C as required dependencies. Does not fix debt, execute canonicalization,
or release real authorization/execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    GOVERNANCE_DEBT_CATEGORIES,
)

PHASE_ID = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001"
DECISION_SCOPE = "main_project_structure_migration_governance_debt_register_roadmap_decision_only"
DECISION_ID = "main_proj_struct_migration_governance_debt_register_roadmap_decision_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_governance_debt_register_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Post-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_POST_REVIEW_READY_FOR_ROADMAP_DECISION"
)

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_ROADMAP_DECISION_READY_FOR_PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING"
)
NEXT_PHASE = "Phase-Permission-Semantics-Canonicalization-Planning-v1-001"

SELECTED_ROUTE_ID = "A"
SELECTED_ROUTE_NAME = "Permission Semantics Canonicalization Planning"
BOUND_DEP_B = "Route B — Terminology Canonical Table Planning"
BOUND_DEP_C = "Route C — Success Claim Gate Canonicalization Planning"

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": SELECTED_ROUTE_NAME,
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "permission_semantics_canonicalization_planning",
        "target_debt_types": ["permission_semantics_debt", "terminology_debt", "success_claim_debt"],
        "entry_reason": "root cause: permission/terminology/success-claim misread; plan canonical semantics + future dev norms",
        "required_dependencies": [BOUND_DEP_B, BOUND_DEP_C],
        "missing_preconditions": [],
        "permission_impact": "planning allowed only; not fix/canonicalization execution",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": ["planning allowed ≠ canonicalization executed", "≠ verifier modified"],
    },
    {
        "route_id": "B",
        "route_name": "Terminology Canonical Table Planning",
        "priority": "P0",
        "selected_now": False,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "terminology_canonical_table_planning",
        "target_debt_types": ["terminology_debt"],
        "entry_reason": "required dependency of Route A",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "dependency planning only",
        "next_phase_candidate": "Phase-Terminology-Canonical-Table-Planning-v1-001",
        "non_claims": ["dependency ≠ terminology debt fixed"],
    },
    {
        "route_id": "C",
        "route_name": "Success Claim Gate Canonicalization Planning",
        "priority": "P0",
        "selected_now": False,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "success_claim_gate_canonicalization_planning",
        "target_debt_types": ["success_claim_debt"],
        "entry_reason": "required dependency of Route A",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "dependency planning only",
        "next_phase_candidate": "Phase-Success-Claim-Gate-Canonicalization-Planning-v1-001",
        "non_claims": ["dependency ≠ success claim gate implemented"],
    },
    {
        "route_id": "D",
        "route_name": "Owner/Operator Approval Protocol Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "owner_operator_approval_protocol_planning",
        "target_debt_types": ["owner_operator_debt"],
        "entry_reason": "deferred until permission semantics canonicalized",
        "required_dependencies": [SELECTED_ROUTE_NAME],
        "missing_preconditions": ["permission semantics not canonicalized"],
        "permission_impact": "deferred",
        "next_phase_candidate": "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001",
        "non_claims": ["deferred ≠ approval granted"],
    },
    {
        "route_id": "E",
        "route_name": "Boundary Object Registry Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "boundary_object_registry_planning",
        "target_debt_types": ["boundary_object_debt"],
        "entry_reason": "deferred",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "deferred",
        "next_phase_candidate": "Phase-Boundary-Object-Registry-Planning-v1-001",
        "non_claims": ["planning deferred"],
    },
    {
        "route_id": "F",
        "route_name": "Evidence Chain Governance Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "evidence_chain_governance_planning",
        "target_debt_types": ["evidence_chain_debt"],
        "entry_reason": "deferred",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "deferred",
        "next_phase_candidate": "Phase-Evidence-Chain-Governance-Planning-v1-001",
        "non_claims": ["planning deferred"],
    },
    {
        "route_id": "G",
        "route_name": "Documentation Sync / Automation Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "documentation_sync_automation_planning",
        "target_debt_types": ["documentation_sync_debt", "automation_candidate_debt"],
        "entry_reason": "deferred",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "deferred",
        "next_phase_candidate": "Phase-Documentation-Sync-Automation-Planning-v1-001",
        "non_claims": ["≠ automation implemented"],
    },
    {
        "route_id": "H",
        "route_name": "Test Harness Authorization Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "test_harness_authorization_planning",
        "target_debt_types": ["test_harness_debt"],
        "entry_reason": "deferred",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "deferred",
        "next_phase_candidate": "Phase-Migration-Test-Harness-Authorization-Planning-v1-001",
        "non_claims": ["≠ test execution authorized"],
    },
    {
        "route_id": "I",
        "route_name": "Direct Debt Fix Execution",
        "priority": "blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_debt_fix_execution",
        "target_debt_types": list(GOVERNANCE_DEBT_CATEGORIES),
        "entry_reason": "forbidden: canonicalization and norms not planned/authorized",
        "required_dependencies": [],
        "missing_preconditions": ["all preconditions unmet"],
        "permission_impact": "not allowed",
        "next_phase_candidate": "Phase-Direct-Debt-Fix-Execution-v1-001",
        "non_claims": ["must not be selected"],
    },
]

DEBT_PRIORITY_SPECS: List[Dict[str, Any]] = [
    {
        "debt_type": "permission_semantics_debt",
        "severity": "critical",
        "priority": "P0",
        "selected_for_next_planning": True,
        "marked_as_required_dependency": False,
        "reason": "root cause of authorization/execution misread",
        "dependency_relation": "primary Route A target",
    },
    {
        "debt_type": "terminology_debt",
        "severity": "critical",
        "priority": "P0",
        "selected_for_next_planning": False,
        "marked_as_required_dependency": True,
        "reason": "Route B bound to Route A",
        "dependency_relation": "required dependency Route B",
    },
    {
        "debt_type": "success_claim_debt",
        "severity": "critical",
        "priority": "P0",
        "selected_for_next_planning": False,
        "marked_as_required_dependency": True,
        "reason": "Route C bound to Route A",
        "dependency_relation": "required dependency Route C",
    },
    {
        "debt_type": "owner_operator_debt",
        "severity": "critical",
        "priority": "P0",
        "selected_for_next_planning": False,
        "marked_as_required_dependency": False,
        "reason": "deferred until semantics canonicalized",
        "dependency_relation": "Route D deferred",
    },
    {
        "debt_type": "boundary_object_debt",
        "severity": "high",
        "priority": "P0",
        "selected_for_next_planning": False,
        "marked_as_required_dependency": False,
        "reason": "Route E deferred",
        "dependency_relation": "deferred",
    },
    {
        "debt_type": "evidence_chain_debt",
        "severity": "high",
        "priority": "P1",
        "selected_for_next_planning": False,
        "marked_as_required_dependency": False,
        "reason": "Route F deferred",
        "dependency_relation": "deferred",
    },
    {
        "debt_type": "test_harness_debt",
        "severity": "medium",
        "priority": "P1",
        "selected_for_next_planning": False,
        "marked_as_required_dependency": False,
        "reason": "Route H deferred",
        "dependency_relation": "deferred",
    },
    {
        "debt_type": "documentation_sync_debt",
        "severity": "medium",
        "priority": "P1",
        "selected_for_next_planning": False,
        "marked_as_required_dependency": False,
        "reason": "Route G deferred",
        "dependency_relation": "deferred",
    },
    {
        "debt_type": "automation_candidate_debt",
        "severity": "medium",
        "priority": "P1",
        "selected_for_next_planning": False,
        "marked_as_required_dependency": False,
        "reason": "Route G deferred",
        "dependency_relation": "deferred",
    },
]

SEMANTIC_GROUPS: List[Dict[str, Any]] = [
    {
        "semantic_group": "phase_type_semantics",
        "terms": ["planning", "dry-run", "review", "roadmap decision", "register", "authorization", "execution"],
        "current_risk": "phase GO misread as execution authorization",
        "required_output_next_phase": "phase_type_semantics_table_v1.json",
    },
    {
        "semantic_group": "permission_state_semantics",
        "terms": ["allowed", "granted", "authorized", "committed", "released", "blocked", "deferred"],
        "current_risk": "allowed misread as granted",
        "required_output_next_phase": "permission_state_semantics_table_v1.json",
    },
    {
        "semantic_group": "artifact_state_semantics",
        "terms": ["generated", "candidate", "executable", "runtime evidence", "audit evidence", "success evidence"],
        "current_risk": "candidate misread as generated",
        "required_output_next_phase": "artifact_state_semantics_table_v1.json",
    },
    {
        "semantic_group": "readiness_state_semantics",
        "terms": [
            "ready",
            "ready_for_planning",
            "ready_for_dryrun",
            "ready_for_review",
            "ready_for_roadmap",
            "ready_for_execution",
        ],
        "current_risk": "ready_for_roadmap misread as ready_for_execution",
        "required_output_next_phase": "readiness_state_semantics_table_v1.json",
    },
    {
        "semantic_group": "result_state_semantics",
        "terms": ["GO", "NO-GO", "pass", "fail", "reviewed", "completed", "succeeded"],
        "current_risk": "GO misread as success claim",
        "required_output_next_phase": "result_state_semantics_table_v1.json",
    },
    {
        "semantic_group": "route_state_semantics",
        "terms": ["selected route", "blocked route", "deferred route", "dependency route", "excluded route"],
        "current_risk": "selected route misread as permission release",
        "required_output_next_phase": "route_state_semantics_table_v1.json",
    },
]

DEVELOPMENT_NORMS: List[Dict[str, Any]] = [
    {"norm_id": "N01", "norm_name": "phase type declaration norm", "why_needed": "disambiguate planning/dry-run/review/roadmap/register", "target_phase_types": "all governance phases", "required_fields": "planning_only|dryrun_only|review_only|roadmap_decision_only|register_only", "forbidden_patterns": "missing phase type flag", "expected_next_phase_output": "phase_type_semantics_table_v1.json"},
    {"norm_id": "N02", "norm_name": "permission field naming norm", "why_needed": "consistent *_allowed vs *_granted_now", "target_phase_types": "all non-execution phases", "required_fields": "real_*_allowed, authorization_granted_now", "forbidden_patterns": "allowed used for granted", "expected_next_phase_output": "permission_state_semantics_table_v1.json"},
    {"norm_id": "N03", "norm_name": "authorization field naming norm", "why_needed": "owner/operator/window separation", "target_phase_types": "authorization chain phases", "required_fields": "owner_approval_granted_now, operator_acknowledgement_granted_now, execution_window_opened_now", "forbidden_patterns": "single auth boolean", "expected_next_phase_output": "authorization_state_semantics_table_v1.json"},
    {"norm_id": "N04", "norm_name": "execution field naming norm", "why_needed": "committed vs invoked vs allowed", "target_phase_types": "execution-adjacent phases", "required_fields": "execution_committed, runtime_invoked", "forbidden_patterns": "allowed implies committed", "expected_next_phase_output": "execution_state_semantics_table_v1.json"},
    {"norm_id": "N05", "norm_name": "artifact state field naming norm", "why_needed": "candidate vs generated", "target_phase_types": "dry-run, review, execution", "required_fields": "evidence_generated_now, evidence_candidate_only", "forbidden_patterns": "candidate without _only suffix", "expected_next_phase_output": "artifact_state_semantics_table_v1.json"},
    {"norm_id": "N06", "norm_name": "readiness decision norm", "why_needed": "ready_for_* must name next phase type", "target_phase_types": "all phases with readiness decision", "required_fields": "ready_for_* disambiguated fields", "forbidden_patterns": "ready_for_execution without authorization", "expected_next_phase_output": "readiness_state_semantics_table_v1.json"},
    {"norm_id": "N07", "norm_name": "final decision naming norm", "why_needed": "final_decision must encode phase outcome not execution", "target_phase_types": "all phases", "required_fields": "final_decision, recommended_next_phase", "forbidden_patterns": "SUCCESS or EXECUTED in final_decision", "expected_next_phase_output": "result_state_semantics_table_v1.json"},
    {"norm_id": "N08", "norm_name": "non-claims generation norm", "why_needed": "every phase must declare what GO does not mean", "target_phase_types": "all governance phases", "required_fields": "non_claims register", "forbidden_patterns": "missing non-claims", "expected_next_phase_output": "non_claims_generation_rules_v1.json"},
    {"norm_id": "N09", "norm_name": "forbidden state combination norm", "why_needed": "verifier must reject illegal flag pairs", "target_phase_types": "all phases", "required_fields": "forbidden_state_combination_matrix", "forbidden_patterns": "conflicting flags both true", "expected_next_phase_output": "forbidden_state_combination_matrix_v1.json"},
    {"norm_id": "N10", "norm_name": "verifier mandatory check norm", "why_needed": "canonical checks referenced by governance_constraints_ref", "target_phase_types": "all verify_* scripts", "required_fields": "governance_constraints_ref", "forbidden_patterns": "verifier without constraints ref", "expected_next_phase_output": "verifier_semantics_checklist_v1.json"},
    {"norm_id": "N11", "norm_name": "documentation sync reference norm", "why_needed": "doc sync declared not auto-executed", "target_phase_types": "phases with handoff", "required_fields": "documentation_auto_sync_executed_now=false", "forbidden_patterns": "silent doc mutation", "expected_next_phase_output": "development_norms_matrix_v1.json"},
    {"norm_id": "N12", "norm_name": "governance constraints ref norm", "why_needed": "all phases link to migration_governance_development_constraints_v1", "target_phase_types": "all migration governance phases", "required_fields": "governance_constraints_ref", "forbidden_patterns": "missing constraints ref", "expected_next_phase_output": "permission_semantics_canonical_policy_v1.json"},
]

FORBIDDEN_COMBINATIONS: List[Dict[str, Any]] = [
    {"forbidden_combination_id": "FC01", "state_a": "planning_only=true", "state_b": "execution_committed=true", "forbidden_reason": "planning must not commit execution", "failure_condition": "both true", "required_verifier_check": "phase_type_vs_execution_committed", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC02", "state_a": "dryrun_only=true", "state_b": "runtime_invoked=true", "forbidden_reason": "dry-run must not invoke runtime", "failure_condition": "both true", "required_verifier_check": "dryrun_vs_runtime", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC03", "state_a": "review_only=true", "state_b": "write_allowed=true", "forbidden_reason": "review must not write", "failure_condition": "both true", "required_verifier_check": "review_vs_write", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC04", "state_a": "roadmap_decision_only=true", "state_b": "authorization_granted_now=true", "forbidden_reason": "roadmap must not grant authorization", "failure_condition": "both true", "required_verifier_check": "roadmap_vs_authorization", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC05", "state_a": "register_only=true", "state_b": "fix_executed_now=true", "forbidden_reason": "register must not fix", "failure_condition": "both true", "required_verifier_check": "register_vs_fix", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC06", "state_a": "authorization_granted_now=false", "state_b": "real_rehearsal_execution_allowed=true", "forbidden_reason": "rehearsal requires authorization", "failure_condition": "both true", "required_verifier_check": "auth_vs_rehearsal", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC07", "state_a": "owner_approval_granted_now=false", "state_b": "execution_window_opened_now=true", "forbidden_reason": "window requires owner approval unless override policy", "failure_condition": "both true without override", "required_verifier_check": "owner_vs_window", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC08", "state_a": "success_claim_allowed=true", "state_b": "real_execution_observed=false", "forbidden_reason": "success claim requires real execution", "failure_condition": "both true", "required_verifier_check": "success_vs_execution", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC09", "state_a": "evidence_generated_now=false", "state_b": "success_claim_allowed=true", "forbidden_reason": "success claim requires evidence", "failure_condition": "both true", "required_verifier_check": "evidence_vs_success", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC10", "state_a": "selected_route set", "state_b": "real_*_execution_allowed=true without permission_release", "forbidden_reason": "route selection ≠ execution release", "failure_condition": "execution allowed without release flag false", "required_verifier_check": "route_vs_execution", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC11", "state_a": "verifier=GO", "state_b": "success_claim_allowed=true", "forbidden_reason": "phase GO ≠ success claim", "failure_condition": "both true in non-success phase", "required_verifier_check": "go_vs_success_claim", "expected_error_level": "NO_GO"},
    {"forbidden_combination_id": "FC12", "state_a": "ready_for_roadmap_decision=true", "state_b": "ready_for_execution=true", "forbidden_reason": "roadmap ready ≠ execution ready", "failure_condition": "both true", "required_verifier_check": "roadmap_ready_vs_exec_ready", "expected_error_level": "NO_GO"},
]

PLANNED_ARTIFACTS: List[str] = [
    "permission_semantics_canonical_policy_v1.json",
    "phase_type_semantics_table_v1.json",
    "permission_state_semantics_table_v1.json",
    "authorization_state_semantics_table_v1.json",
    "execution_state_semantics_table_v1.json",
    "artifact_state_semantics_table_v1.json",
    "readiness_state_semantics_table_v1.json",
    "result_state_semantics_table_v1.json",
    "route_state_semantics_table_v1.json",
    "forbidden_state_combination_matrix_v1.json",
    "development_norms_matrix_v1.json",
    "verifier_semantics_checklist_v1.json",
    "non_claims_generation_rules_v1.json",
    "canonical_semantics_readiness_decision_v1.json",
]

NON_CLAIMS = [
    "Roadmap Decision GO does not mean permission semantics are canonicalized.",
    "Roadmap Decision GO does not mean governance debt is fixed.",
    "Selected Route A does not mean canonicalization has been executed.",
    "Selected Route A does not mean verifier has been modified.",
    "Selected Route A does not mean future phase templates have been updated.",
    "Route B/C dependency does not mean terminology or success claim debt has been fixed.",
    "Roadmap Decision GO does not mean owner/operator approval can be requested.",
    "Roadmap Decision GO does not mean real rollback rehearsal is authorized.",
    "Roadmap Decision GO does not mean real migration or batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "debt_fix_executed_now": False,
        "canonicalization_executed_now": False,
        "verifier_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(path_str: Optional[str], artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in artifacts:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
    loaded = summary is not None and not missing
    return {"root": root, "loaded": loaded, "summary": summary or {}, "artifacts": art, "missing": missing}


def run_main_project_structure_migration_governance_debt_register_roadmap_decision_v1(
    *,
    governance_debt_register_post_review_root: str,
) -> Dict[str, Any]:
    upstream_artifacts = [
        "governance_debt_register_post_review_policy_v1.json",
        "governance_debt_register_completeness_review_v1.json",
        "governance_debt_severity_review_matrix_v1.json",
        "governance_debt_source_mapping_review_v1.json",
        "blocked_progression_rules_review_v1.json",
        "future_phase_mapping_review_v1.json",
        "verifier_addition_plan_review_v1.json",
        "terminology_canonical_table_review_v1.json",
        "register_non_fix_non_claims_review_v1.json",
        "governance_debt_register_post_review_readiness_decision_v1.json",
        "summary.json",
        "verifier_report.json",
    ]
    upstream = _load_upstream(governance_debt_register_post_review_root, upstream_artifacts)
    up_summary = upstream["summary"]
    up_art = upstream["artifacts"]
    up_verifier = up_art.get("verifier_report.json") or {}
    up_readiness = up_art.get("governance_debt_register_post_review_readiness_decision_v1.json") or {}
    completeness = up_art.get("governance_debt_register_completeness_review_v1.json") or {}

    upstream_go = up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True
    upstream_boundary_ok = up_summary.get("boundary_ok") is True
    upstream_constraints = up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID
    upstream_ready = up_readiness.get("ready_for_roadmap_decision") is True
    upstream_final_ok = up_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL
    completeness_pass = completeness.get("review_pass") is True and up_summary.get("register_completeness_review_pass") is True

    upstream_flags_ok = (
        up_summary.get("debt_fix_executed_now") is False
        and up_summary.get("automation_implemented_now") is False
        and up_summary.get("verifier_modified_now") is False
        and up_readiness.get("ready_for_debt_fix_execution") is False
        and up_readiness.get("ready_for_real_rollback_rehearsal_execution") is False
        and up_summary.get("real_migration_execution_allowed") is False
        and up_summary.get("batch_arming_allowed") is False
        and up_summary.get("authorization_granted_now") is False
    )

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append("upstream_post_review_missing_or_incomplete")
    if not upstream_go:
        blockers.append("upstream_post_review_verifier_not_go")
    if not upstream_boundary_ok:
        blockers.append("upstream_post_review_boundary_not_ok")
    if not upstream_constraints:
        blockers.append("upstream_governance_constraints_ref_missing")
    if not upstream_ready:
        blockers.append("upstream_ready_for_roadmap_decision_not_true")
    if not upstream_final_ok:
        blockers.append("upstream_final_decision_mismatch")
    if not completeness_pass:
        blockers.append("upstream_register_completeness_not_pass")
    if not upstream_flags_ok:
        blockers.append("upstream_flags_not_frozen")

    boundary_ok = not blockers

    governance_debt_register_roadmap_decision_policy = {
        "phase_name": PHASE_ID,
        "decision_id": DECISION_ID,
        "source_phase": SOURCE_PHASE,
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_governance_constraints_ref_observed": CONSTRAINT_DOC_ID if upstream_constraints else None,
        "source_ready_for_roadmap_decision_observed": upstream_ready,
        **_decision_meta(),
    }

    governance_debt_roadmap_route_candidate_matrix = {
        "routes": ROUTE_OPTIONS,
        "route_count": len(ROUTE_OPTIONS),
        "selected_route_id": SELECTED_ROUTE_ID,
        "selected_route_name": SELECTED_ROUTE_NAME,
        "bound_dependencies": [BOUND_DEP_B, BOUND_DEP_C],
        **_decision_meta(),
    }

    priority_rows: List[Dict[str, Any]] = []
    for spec in DEBT_PRIORITY_SPECS:
        comp_row = next(
            (r for r in (completeness.get("rows") or []) if r.get("debt_type") == spec["debt_type"]),
            {},
        )
        priority_rows.append(
            {
                "debt_type": spec["debt_type"],
                "registered": comp_row.get("registered") is True or comp_row.get("register_completeness_pass") is True,
                "review_passed": comp_row.get("register_completeness_pass") is True,
                "severity": spec["severity"],
                "priority": spec["priority"],
                "selected_for_next_planning": spec["selected_for_next_planning"],
                "marked_as_required_dependency": spec["marked_as_required_dependency"],
                "reason": spec["reason"],
                "dependency_relation": spec["dependency_relation"],
                "blocked_actions_until_planned": "real execution, owner approval, batch arming"
                if spec["debt_type"] in ("permission_semantics_debt", "terminology_debt", "success_claim_debt")
                else "deferred planning routes",
                **_decision_meta(),
            }
        )
    governance_debt_priority_decision_matrix = {
        "rows": priority_rows,
        "row_count": len(priority_rows),
        **_decision_meta(),
    }

    selected_governance_debt_roadmap_route_decision = {
        "selected_route_id": f"Route {SELECTED_ROUTE_ID}",
        "selected_route_name": SELECTED_ROUTE_NAME,
        "selected_now": True,
        "selection_reason": [
            "Root governance risk: permission semantics, terminology, success claim misread",
            "Route A plans canonical semantics + future development norms, not field glossary only",
            "Route B/C bound as required dependencies",
        ],
        "permission_release": False,
        "debt_fix_execution_allowed": False,
        "canonicalization_execution_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "required_bound_dependencies": [BOUND_DEP_B, BOUND_DEP_C],
        "excluded_routes": [
            "Direct Debt Fix Execution",
            "Owner/Operator Real Approval Request",
            "Real Rollback Rehearsal Execution",
            "Real Migration Execution",
            "Batch Arming",
        ],
        **_decision_meta(),
    }

    semantic_rows: List[Dict[str, Any]] = []
    for grp in SEMANTIC_GROUPS:
        semantic_rows.append(
            {
                "semantic_group": grp["semantic_group"],
                "terms": grp["terms"],
                "current_risk": grp["current_risk"],
                "canonicalization_needed": True,
                "required_output_next_phase": grp["required_output_next_phase"],
                "verifier_usage_expected": True,
                **_decision_meta(),
            }
        )
    permission_semantics_planning_scope = {
        "semantic_groups": semantic_rows,
        "group_count": len(semantic_rows),
        "scope_note": "semantics + norms foundation for all future governance phases",
        **_decision_meta(),
    }

    norm_rows: List[Dict[str, Any]] = []
    for norm in DEVELOPMENT_NORMS:
        norm_rows.append({**norm, "verifier_check_required": True, "not_implemented_now": True, **_decision_meta()})
    future_development_norms_planning_scope = {
        "rows": norm_rows,
        "row_count": len(norm_rows),
        "scope_note": "field naming, state flow, verifier checks, forbidden combos, non-claims, constraints ref",
        **_decision_meta(),
    }

    forbidden_rows: List[Dict[str, Any]] = []
    for fc in FORBIDDEN_COMBINATIONS:
        forbidden_rows.append({**fc, **_decision_meta()})
    forbidden_state_combination_planning = {
        "rows": forbidden_rows,
        "row_count": len(forbidden_rows),
        **_decision_meta(),
    }

    artifact_rows: List[Dict[str, Any]] = []
    for art in PLANNED_ARTIFACTS:
        artifact_rows.append(
            {
                "planned_artifact": art,
                "purpose": f"canonical semantics output for {NEXT_PHASE}",
                "required": True,
                "used_by_future_verifier": True,
                "used_by_future_phase_template": True,
                "not_generated_now": True,
                **_decision_meta(),
            }
        )
    canonical_semantics_output_plan = {
        "rows": artifact_rows,
        "row_count": len(artifact_rows),
        **_decision_meta(),
    }

    governance_roadmap_decision_non_claims_register = {
        "non_claims": NON_CLAIMS,
        "non_claim_count": len(NON_CLAIMS),
        **_decision_meta(),
    }

    ready = boundary_ok
    governance_debt_register_roadmap_readiness_decision = {
        "ready_for_permission_semantics_canonicalization_planning": bool(ready),
        "ready_for_debt_fix_execution": False,
        "ready_for_canonicalization_execution": False,
        "ready_for_verifier_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_documentation_auto_sync": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "selected_route": f"Route {SELECTED_ROUTE_ID} — {SELECTED_ROUTE_NAME}",
        "bound_dependencies": [BOUND_DEP_B, BOUND_DEP_C],
        "future_development_norms_required": True,
        "forbidden_state_combination_planning_generated": True,
        "final_decision": FINAL_DECISION if ready else "GOVERNANCE_DEBT_REGISTER_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_debt_register_post_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_governance_constraints_ref_observed": upstream_constraints,
        "source_ready_for_roadmap_decision_observed": upstream_ready,
        "route_candidate_count": len(ROUTE_OPTIONS),
        "selected_route": f"Route {SELECTED_ROUTE_ID} — {SELECTED_ROUTE_NAME}",
        "bound_dependencies": [BOUND_DEP_B, BOUND_DEP_C],
        "route_a_selected_now": True,
        "route_i_blocked_now": True,
        "semantic_group_count": len(semantic_rows),
        "development_norm_count": len(norm_rows),
        "forbidden_combination_count": len(forbidden_rows),
        "planned_artifact_count": len(artifact_rows),
        "boundary_ok": bool(boundary_ok),
        "violations": blockers,
        "final_decision": FINAL_DECISION if ready else "GOVERNANCE_DEBT_REGISTER_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if ready else PHASE_ID,
        **_decision_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "governance_debt_register_post_review",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                **_decision_meta(),
            }
        ],
        "row_count": 1,
        **_decision_meta(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if ready else PHASE_ID,
        "final_decision": FINAL_DECISION if ready else "GOVERNANCE_DEBT_REGISTER_ROADMAP_DECISION_REQUIRES_FIXES",
        "selected_route": f"Route {SELECTED_ROUTE_ID} — {SELECTED_ROUTE_NAME}",
        "bound_dependencies": [BOUND_DEP_B, BOUND_DEP_C],
        "reason": "roadmap decision only; plan canonical semantics + dev norms; Route B/C bound",
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "governance_debt_register_roadmap_decision_policy": governance_debt_register_roadmap_decision_policy,
        "governance_debt_roadmap_route_candidate_matrix": governance_debt_roadmap_route_candidate_matrix,
        "governance_debt_priority_decision_matrix": governance_debt_priority_decision_matrix,
        "selected_governance_debt_roadmap_route_decision": selected_governance_debt_roadmap_route_decision,
        "permission_semantics_planning_scope": permission_semantics_planning_scope,
        "future_development_norms_planning_scope": future_development_norms_planning_scope,
        "forbidden_state_combination_planning": forbidden_state_combination_planning,
        "canonical_semantics_output_plan": canonical_semantics_output_plan,
        "governance_roadmap_decision_non_claims_register": governance_roadmap_decision_non_claims_register,
        "governance_debt_register_roadmap_readiness_decision": governance_debt_register_roadmap_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
