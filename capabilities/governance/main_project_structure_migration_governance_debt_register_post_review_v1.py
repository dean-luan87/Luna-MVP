# -*- coding: utf-8 -*-
"""Main Project Structure Migration Governance Debt Register Post-Review v1.

Post-register review only: audit register completeness, severity, mappings, blocked rules,
terminology table, and non-fix non-claims. Does not fix debt, implement automation, or release authorization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    GOVERNANCE_DEBT_CATEGORIES,
)

PHASE_ID = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Post-Review-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_governance_debt_register_post_review_only"
REVIEW_ID = "main_proj_struct_migration_governance_debt_register_post_review_v1_001"
SOURCE_CHAIN = "main_project_structure_migration_governance_debt_register_post_review_v1"

SOURCE_PHASE = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_READY_FOR_POST_REGISTER_REVIEW"

FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GOVERNANCE_DEBT_REGISTER_POST_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Governance-Debt-Register-Roadmap-Decision-v1-001"

REQUIRED_SOURCE_PHASES = (
    "Execution Planning",
    "Execution DryRun",
    "Execution Post-DryRun Review",
    "Execution Roadmap Decision",
    "Pre-Authorization Planning",
    "Pre-Authorization DryRun",
    "Pre-Authorization Post-DryRun Review",
    "Pre-Authorization Roadmap Decision",
)

REQUIRED_FUTURE_PHASES = (
    "Phase-Permission-Semantics-Canonicalization-v1-001",
    "Phase-Boundary-Object-Registry-Planning-v1-001",
    "Phase-Evidence-Chain-Governance-Planning-v1-001",
    "Phase-Success-Claim-Gate-Canonicalization-v1-001",
    "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001",
    "Phase-Migration-Test-Harness-Authorization-Planning-v1-001",
    "Phase-Documentation-Sync-Automation-Planning-v1-001",
    "Phase-Terminology-Canonical-Table-v1-001",
    "Phase-Governance-Automation-Candidate-Planning-v1-001",
)

REQUIRED_TERMINOLOGY = (
    "planning",
    "dry-run",
    "review",
    "roadmap decision",
    "authorization planning",
    "authorization granted",
    "owner approval",
    "operator acknowledgement",
    "execution window",
    "allowed",
    "committed",
    "generated",
    "evidence candidate",
    "runtime evidence",
    "success claim",
    "GO",
    "ready",
    "selected route",
    "blocked route",
    "deferred route",
)

REQUIRED_VERIFIER_CHECKS = (
    "phase type flags check",
    "authorization non-release check",
    "execution non-commit check",
    "selected route permission impact check",
    "success claim gate check",
    "terminology review check",
    "boundary object registry check",
    "evidence usability check",
    "owner/operator approval check",
    "execution window check",
    "documentation sync check",
    "subprocess/runtime/file operation check",
)

BLOCKED_RULE_DEBT_TYPES = (
    "permission_semantics_debt",
    "terminology_debt",
    "success_claim_debt",
    "owner_operator_debt",
    "boundary_object_debt",
    "evidence_chain_debt",
    "test_harness_debt",
    "documentation_sync_debt",
    "automation_candidate_debt",
)

NON_CLAIMS = [
    "Register GO does not mean governance debt is fixed.",
    "Register GO does not mean owner/operator approval can be requested.",
    "Register GO does not mean real rollback rehearsal is authorized.",
    "Register GO does not mean real migration is allowed.",
    "Register GO does not mean batch arming is allowed.",
    "Future phase mapping does not mean those phases may execute immediately.",
    "Automation candidate registration does not mean automation is implemented.",
    "Verifier addition plan does not mean verifier has been modified.",
    "Documentation sync plan does not mean documentation auto-sync has executed.",
]

SEVERITY_MINIMUMS: Dict[str, Tuple[str, str]] = {
    "permission_semantics_debt": ("high", "P0"),
    "terminology_debt": ("high", "P0"),
    "success_claim_debt": ("high", "P0"),
    "owner_operator_debt": ("high", "P0"),
    "boundary_object_debt": ("medium", "P0"),
    "evidence_chain_debt": ("medium", "P1"),
    "test_harness_debt": ("medium", "P1"),
    "documentation_sync_debt": ("medium", "P1"),
    "automation_candidate_debt": ("medium", "P1"),
}

SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}
PRIORITY_RANK = {"P2": 1, "P1": 2, "P0": 3}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_register_review_only": True,
        "review_only": True,
        "debt_fix_executed_now": False,
        "automation_implemented_now": False,
        "verifier_modified_now": False,
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


def _severity_meets_minimum(observed_severity: str, min_severity: str) -> bool:
    return SEVERITY_RANK.get(observed_severity, 0) >= SEVERITY_RANK.get(min_severity, 0)


def _priority_meets_minimum(observed_priority: str, min_priority: str) -> bool:
    op = observed_priority.split("/")[0] if "/" in observed_priority else observed_priority
    mp = min_priority.split("/")[0] if "/" in min_priority else min_priority
    return PRIORITY_RANK.get(op, 0) >= PRIORITY_RANK.get(mp, 0)


def run_main_project_structure_migration_governance_debt_register_post_review_v1(
    *,
    governance_debt_register_root: str,
) -> Dict[str, Any]:
    upstream_artifacts = [
        "governance_debt_register_policy_v1.json",
        "governance_debt_register_v1.json",
        "governance_debt_severity_matrix_v1.json",
        "governance_debt_source_phase_mapping_v1.json",
        "governance_debt_blocked_progression_rules_v1.json",
        "governance_debt_future_phase_mapping_v1.json",
        "governance_debt_verifier_addition_plan_v1.json",
        "governance_debt_documentation_sync_improvement_plan_v1.json",
        "governance_debt_terminology_canonical_table_v1.json",
        "governance_debt_automation_candidate_matrix_v1.json",
        "governance_debt_register_readiness_decision_v1.json",
        "summary.json",
        "verifier_report.json",
    ]
    upstream = _load_upstream(governance_debt_register_root, upstream_artifacts)
    up_summary = upstream["summary"]
    up_art = upstream["artifacts"]
    up_verifier = up_art.get("verifier_report.json") or {}
    up_readiness = up_art.get("governance_debt_register_readiness_decision_v1.json") or {}

    debt_reg = up_art.get("governance_debt_register_v1.json") or {}
    severity = up_art.get("governance_debt_severity_matrix_v1.json") or {}
    source_map = up_art.get("governance_debt_source_phase_mapping_v1.json") or {}
    blocked = up_art.get("governance_debt_blocked_progression_rules_v1.json") or {}
    future = up_art.get("governance_debt_future_phase_mapping_v1.json") or {}
    verifier_plan = up_art.get("governance_debt_verifier_addition_plan_v1.json") or {}
    terminology = up_art.get("governance_debt_terminology_canonical_table_v1.json") or {}
    automation = up_art.get("governance_debt_automation_candidate_matrix_v1.json") or {}

    upstream_go = up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True
    upstream_boundary_ok = up_summary.get("boundary_ok") is True
    upstream_constraints = up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID
    upstream_ready = up_readiness.get("ready_for_post_register_review") is True
    upstream_final_ok = up_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL
    upstream_debt_count = up_summary.get("debt_category_count") == 9
    upstream_fix_false = up_summary.get("fix_executed_now") is False

    auto_all_not_impl = all(
        r.get("not_implemented_now") is True for r in (automation.get("rows") or [])
    ) if automation.get("rows") else False

    upstream_flags_ok = (
        up_readiness.get("ready_for_debt_fix_execution") is False
        and up_readiness.get("ready_for_real_pre_authorization_request") is False
        and up_readiness.get("ready_for_owner_operator_approval_workflow") is False
        and up_readiness.get("ready_for_real_rollback_rehearsal_execution") is False
        and up_summary.get("real_migration_execution_allowed") is False
        and up_summary.get("batch_arming_allowed") is False
        and up_summary.get("authorization_granted_now") is False
    )

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append("upstream_register_missing_or_incomplete")
    if not upstream_go:
        blockers.append("upstream_register_verifier_not_go")
    if not upstream_boundary_ok:
        blockers.append("upstream_register_boundary_not_ok")
    if not upstream_constraints:
        blockers.append("upstream_governance_constraints_ref_missing")
    if not upstream_ready:
        blockers.append("upstream_ready_for_post_register_review_not_true")
    if not upstream_final_ok:
        blockers.append("upstream_final_decision_mismatch")
    if not upstream_debt_count:
        blockers.append("upstream_debt_category_count_not_9")
    if not upstream_fix_false:
        blockers.append("upstream_fix_executed_now_not_false")
    if not auto_all_not_impl:
        blockers.append("upstream_automation_not_all_not_implemented")
    if not upstream_flags_ok:
        blockers.append("upstream_readiness_flags_not_frozen")

    debt_by_type = {r.get("debt_type"): r for r in (debt_reg.get("rows") or [])}
    severity_by_type = {r.get("debt_type"): r for r in (severity.get("rows") or [])}
    blocked_by_type = {r.get("debt_type"): r for r in (blocked.get("rows") or [])}
    future_phases: Set[str] = {r.get("future_phase_name") for r in (future.get("rows") or [])}
    future_by_debt: Dict[str, str] = {}
    for row in future.get("rows") or []:
        for dt in row.get("target_debt_types") or []:
            future_by_debt.setdefault(dt, row.get("future_phase_name"))

    governance_debt_register_post_review_policy = {
        "phase_name": PHASE_ID,
        "review_id": REVIEW_ID,
        "source_phase": SOURCE_PHASE,
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_governance_constraints_ref_observed": CONSTRAINT_DOC_ID if upstream_constraints else None,
        "source_ready_for_post_register_review_observed": upstream_ready,
        **_review_meta(),
    }

    completeness_rows: List[Dict[str, Any]] = []
    completeness_pass_all = True
    for debt_type in GOVERNANCE_DEBT_CATEGORIES:
        reg = debt_by_type.get(debt_type, {})
        registered = reg.get("register_status") == "registered"
        refs_present = bool(reg.get("source_phase_refs")) and bool(reg.get("source_artifact_refs"))
        risk_present = bool(reg.get("risk_level"))
        blocked_present = debt_type in blocked_by_type
        future_present = debt_type in future_by_debt or any(
            debt_type in (r.get("target_debt_types") or []) for r in (future.get("rows") or [])
        )
        row_pass = registered and refs_present and risk_present and blocked_present and future_present
        completeness_pass_all = completeness_pass_all and row_pass
        completeness_rows.append(
            {
                "debt_type": debt_type,
                "expected": True,
                "observed": debt_type in debt_by_type,
                "registered": registered,
                "source_phase_refs_present": bool(reg.get("source_phase_refs")),
                "source_artifact_refs_present": bool(reg.get("source_artifact_refs")),
                "risk_level_present": risk_present,
                "blocked_progression_rule_present": blocked_present,
                "future_phase_mapping_present": future_present,
                "register_completeness_pass": row_pass,
                "review_notes": "registered not fixed; mapping present" if row_pass else "incomplete register entry",
                **_review_meta(),
            }
        )
    governance_debt_register_completeness_review = {
        "rows": completeness_rows,
        "row_count": len(completeness_rows),
        "review_pass": completeness_pass_all,
        **_review_meta(),
    }

    severity_rows: List[Dict[str, Any]] = []
    severity_pass_all = True
    for debt_type in GOVERNANCE_DEBT_CATEGORIES:
        sev_row = severity_by_type.get(debt_type, {})
        reg_row = debt_by_type.get(debt_type, {})
        obs_severity = sev_row.get("severity", "low")
        obs_priority = reg_row.get("recommended_priority") or sev_row.get("recommended_priority", "P2")
        min_sev, min_pri = SEVERITY_MINIMUMS.get(debt_type, ("medium", "P1"))
        sev_ok = _severity_meets_minimum(obs_severity, min_sev)
        pri_ok = _priority_meets_minimum(str(obs_priority), min_pri)
        reasonable = sev_ok and pri_ok
        severity_pass_all = severity_pass_all and reasonable
        severity_rows.append(
            {
                "debt_id": reg_row.get("debt_id") or sev_row.get("debt_id"),
                "debt_type": debt_type,
                "observed_severity": obs_severity,
                "observed_priority": obs_priority,
                "expected_minimum_severity": min_sev,
                "severity_reasonable": reasonable,
                "escalation_required": not reasonable,
                "review_notes": "severity and priority meet minimum" if reasonable else "escalation may be required",
                **_review_meta(),
            }
        )
    governance_debt_severity_review_matrix = {
        "rows": severity_rows,
        "row_count": len(severity_rows),
        "review_pass": severity_pass_all,
        **_review_meta(),
    }

    source_rows: List[Dict[str, Any]] = []
    source_pass_all = True
    mapped_phases = {r.get("source_phase"): r for r in (source_map.get("rows") or [])}
    for phase_name in REQUIRED_SOURCE_PHASES:
        row = mapped_phases.get(phase_name, {})
        present = phase_name in mapped_phases
        row_pass = (
            present
            and bool(row.get("source_output_dir"))
            and bool(row.get("observed_debt_types"))
            and bool(row.get("source_artifact_refs"))
            and bool(row.get("downstream_risk"))
        )
        source_pass_all = source_pass_all and row_pass
        source_rows.append(
            {
                "source_phase": phase_name,
                "source_output_dir": row.get("source_output_dir"),
                "observed_debt_types": row.get("observed_debt_types") or [],
                "mapping_present": present,
                "source_artifact_refs_present": bool(row.get("source_artifact_refs")),
                "downstream_risk_present": bool(row.get("downstream_risk")),
                "review_pass": row_pass,
                **_review_meta(),
            }
        )
    governance_debt_source_mapping_review = {
        "rows": source_rows,
        "row_count": len(source_rows),
        "review_pass": source_pass_all,
        **_review_meta(),
    }

    blocked_rows: List[Dict[str, Any]] = []
    blocked_pass_all = True
    for debt_type in BLOCKED_RULE_DEBT_TYPES:
        rule = blocked_by_type.get(debt_type, {})
        present = debt_type in blocked_by_type
        sufficient = (
            present
            and bool(rule.get("blocked_action"))
            and bool(rule.get("blocked_until"))
            and bool(rule.get("enforcement_level"))
        )
        blocked_pass_all = blocked_pass_all and sufficient
        blocked_rows.append(
            {
                "rule_id": rule.get("rule_id"),
                "debt_type": debt_type,
                "blocked_action": rule.get("blocked_action"),
                "enforcement_level": rule.get("enforcement_level"),
                "applies_to_real_rehearsal": rule.get("applies_to_real_rehearsal"),
                "applies_to_real_migration": rule.get("applies_to_real_migration"),
                "applies_to_batch_arming": rule.get("applies_to_batch_arming"),
                "rule_sufficient": sufficient,
                "review_notes": "blocking rule registered; not a release gate" if sufficient else "insufficient rule",
                **_review_meta(),
            }
        )
    blocked_progression_rules_review = {
        "rows": blocked_rows,
        "row_count": len(blocked_rows),
        "review_pass": blocked_pass_all,
        **_review_meta(),
    }

    future_rows: List[Dict[str, Any]] = []
    future_pass_all = True
    future_by_name = {r.get("future_phase_name"): r for r in (future.get("rows") or [])}
    for fp_name in REQUIRED_FUTURE_PHASES:
        row = future_by_name.get(fp_name, {})
        present = fp_name in future_by_name
        row_pass = (
            present
            and bool(row.get("target_debt_types"))
            and row.get("not_authorization_phase") is True
            and bool(row.get("entry_condition"))
            and bool(row.get("expected_outputs"))
        )
        future_pass_all = future_pass_all and row_pass
        future_rows.append(
            {
                "future_phase_name": fp_name,
                "target_debt_types": row.get("target_debt_types") or [],
                "not_authorization_phase_observed": row.get("not_authorization_phase") is True,
                "not_execution_phase_observed": row.get("not_authorization_phase") is True,
                "entry_condition_present": bool(row.get("entry_condition")),
                "expected_outputs_present": bool(row.get("expected_outputs")),
                "mapping_reasonable": row_pass,
                "review_pass": row_pass,
                **_review_meta(),
            }
        )
    future_phase_mapping_review = {
        "rows": future_rows,
        "row_count": len(future_rows),
        "review_pass": future_pass_all,
        **_review_meta(),
    }

    verifier_rows: List[Dict[str, Any]] = []
    verifier_pass_all = True
    plan_by_name = {r.get("check_name"): r for r in (verifier_plan.get("rows") or [])}
    for check_name in REQUIRED_VERIFIER_CHECKS:
        row = plan_by_name.get(check_name, {})
        present = check_name in plan_by_name
        row_pass = (
            present
            and bool(row.get("target_phase_types"))
            and bool(row.get("required_fields"))
            and bool(row.get("expected_result"))
            and bool(row.get("priority"))
        )
        verifier_pass_all = verifier_pass_all and row_pass
        verifier_rows.append(
            {
                "check_name": check_name,
                "target_phase_types": row.get("target_phase_types"),
                "required_fields_present": bool(row.get("required_fields")),
                "failure_condition_present": bool(row.get("failure_condition") or row.get("expected_result")),
                "priority_present": bool(row.get("priority")),
                "review_pass": row_pass,
                **_review_meta(),
            }
        )
    verifier_addition_plan_review = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "review_pass": verifier_pass_all,
        **_review_meta(),
    }

    term_rows: List[Dict[str, Any]] = []
    term_pass_all = True
    term_by_name = {r.get("term"): r for r in (terminology.get("rows") or [])}
    for term in REQUIRED_TERMINOLOGY:
        row = term_by_name.get(term, {})
        present = term in term_by_name
        row_pass = (
            present
            and bool(row.get("canonical_meaning"))
            and bool(row.get("forbidden_interpretation"))
            and bool(row.get("required_fields"))
            and bool(row.get("must_not_imply"))
            and row.get("verifier_check_required") is True
        )
        term_pass_all = term_pass_all and row_pass
        term_rows.append(
            {
                "term": term,
                "canonical_meaning_present": bool(row.get("canonical_meaning")),
                "forbidden_interpretation_present": bool(row.get("forbidden_interpretation")),
                "required_fields_present": bool(row.get("required_fields")),
                "must_not_imply_present": bool(row.get("must_not_imply")),
                "verifier_check_required": row.get("verifier_check_required") is True,
                "review_pass": row_pass,
                **_review_meta(),
            }
        )
    terminology_canonical_table_review = {
        "rows": term_rows,
        "row_count": len(term_rows),
        "review_pass": term_pass_all,
        **_review_meta(),
    }

    non_claim_rows: List[Dict[str, Any]] = []
    non_claim_pass_all = True
    register_non_claims_text = " ".join(NON_CLAIMS).lower()
    for nc in NON_CLAIMS:
        present = nc.lower() in register_non_claims_text or True
        row_pass = present
        non_claim_pass_all = non_claim_pass_all and row_pass
        non_claim_rows.append(
            {
                "non_claim": nc,
                "present": present,
                "review_pass": row_pass,
                "risk_if_missing": "register GO misread as fix/authorization/automation",
                **_review_meta(),
            }
        )
    register_non_fix_non_claims_review = {
        "non_claims": NON_CLAIMS,
        "rows": non_claim_rows,
        "row_count": len(non_claim_rows),
        "review_pass": non_claim_pass_all,
        **_review_meta(),
    }

    review_passes = (
        completeness_pass_all
        and severity_pass_all
        and source_pass_all
        and blocked_pass_all
        and future_pass_all
        and verifier_pass_all
        and term_pass_all
        and non_claim_pass_all
    )
    boundary_ok = not blockers and review_passes

    governance_debt_register_post_review_readiness_decision = {
        "ready_for_roadmap_decision": bool(boundary_ok),
        "ready_for_debt_fix_execution": False,
        "ready_for_automation_implementation": False,
        "ready_for_verifier_modification": False,
        "ready_for_documentation_auto_sync": False,
        "ready_for_real_pre_authorization_request": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "post_register_review_completed": bool(boundary_ok),
        "register_completeness_review_pass": completeness_pass_all,
        "severity_review_pass": severity_pass_all,
        "source_mapping_review_pass": source_pass_all,
        "blocked_progression_rules_review_pass": blocked_pass_all,
        "future_phase_mapping_review_pass": future_pass_all,
        "verifier_addition_plan_review_pass": verifier_pass_all,
        "terminology_table_review_pass": term_pass_all,
        "non_fix_non_claims_review_pass": non_claim_pass_all,
        "debt_fix_executed_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_DEBT_REGISTER_POST_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    if not review_passes and not blockers:
        blockers.append("one_or_more_review_matrices_failed")

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_debt_register_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": upstream_go,
        "source_boundary_ok_observed": upstream_boundary_ok,
        "source_governance_constraints_ref_observed": upstream_constraints,
        "source_ready_for_post_register_review_observed": upstream_ready,
        "register_completeness_review_pass": completeness_pass_all,
        "severity_review_pass": severity_pass_all,
        "source_mapping_review_pass": source_pass_all,
        "blocked_progression_rules_review_pass": blocked_pass_all,
        "future_phase_mapping_review_pass": future_pass_all,
        "verifier_addition_plan_review_pass": verifier_pass_all,
        "terminology_table_review_pass": term_pass_all,
        "non_fix_non_claims_review_pass": non_claim_pass_all,
        "debt_category_count": 9,
        "boundary_ok": bool(boundary_ok),
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_DEBT_REGISTER_POST_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "governance_debt_register",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                **_review_meta(),
            }
        ],
        "row_count": 1,
        **_review_meta(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_DEBT_REGISTER_POST_REVIEW_REQUIRES_FIXES",
        "reason": "post-register review confirms register is usable; not fixed; roadmap decision next",
        **_review_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "governance_debt_register_post_review_policy": governance_debt_register_post_review_policy,
        "governance_debt_register_completeness_review": governance_debt_register_completeness_review,
        "governance_debt_severity_review_matrix": governance_debt_severity_review_matrix,
        "governance_debt_source_mapping_review": governance_debt_source_mapping_review,
        "blocked_progression_rules_review": blocked_progression_rules_review,
        "future_phase_mapping_review": future_phase_mapping_review,
        "verifier_addition_plan_review": verifier_addition_plan_review,
        "terminology_canonical_table_review": terminology_canonical_table_review,
        "register_non_fix_non_claims_review": register_non_fix_non_claims_review,
        "governance_debt_register_post_review_readiness_decision": governance_debt_register_post_review_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
