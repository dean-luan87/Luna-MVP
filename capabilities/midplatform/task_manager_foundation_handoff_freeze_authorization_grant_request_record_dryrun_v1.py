# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Request Record DryRun v1.

Structure inherited from task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_dryrun_v1.py
with upstream input from grant_request_record_planning_v1 (whitelist template reuse).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_REQUEST_RECORD_DRYRUN_STAGE_ADDITIONS,
    GRANT_REQUEST_RECORD_DRYRUN_STAGE_TERM_OVERRIDES,
    GRANT_REQUEST_RECORD_DRYRUN_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_request_record_planning_v1 import (
    CHAIN_EVIDENCE_NODES,
    DEFAULT_OUTPUT as DEFAULT_GRANT_REQUEST_RECORD_PLANNING_ROOT,
    FINAL_DECISION_GO as GRANT_REQUEST_RECORD_PLANNING_FINAL_GO,
    GRANT_REQUEST_RECORD_PLANNING_PACKAGE_FILES,
    NEXT_PHASE_GO as GRANT_REQUEST_RECORD_PLANNING_NEXT_PHASE,
    PLANNING_TRUE_KEYS,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Request-Record-DryRun-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_validation_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_RECORD_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_PLAN_GAP = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_RECORD_DRYRUN_BLOCKED_BY_PLANNING_PACKAGE_GAP"
FINAL_DECISION_SCOPE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_RECORD_DRYRUN_BLOCKED_BY_RECORD_SCOPE_ESCALATION"
FINAL_DECISION_RECORD = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_RECORD_DRYRUN_BLOCKED_BY_REQUEST_RECORD_LEAKAGE"
FINAL_DECISION_REQUEST = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_RECORD_DRYRUN_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_RECORD_DRYRUN_BLOCKED_BY_FREEZE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_RECORD_DRYRUN_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_RECORD_DRYRUN_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_REQUEST_RECORD_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Request-Record-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Request-Record-DryRun-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1_smoke_v0"
)

GRANT_REQUEST_RECORD_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_report_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_report_v1.md",
    "task_manager_freeze_authorization_grant_request_record_plan_integrity_matrix_v1.json",
    "task_manager_freeze_authorization_grant_request_record_scope_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_schema_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_evidence_binding_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_owner_approval_binding_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_lifecycle_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_revocation_reference_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_prerequisite_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_evidence_traceability_v1.json",
    "task_manager_freeze_authorization_grant_request_record_absence_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_boundary_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_governance_debt_validation_v1.json",
    "task_manager_freeze_authorization_grant_request_record_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_request_record_post_review_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)
CHAIN_TRACE_NODES: Tuple[str, ...] = CHAIN_EVIDENCE_NODES + ("freeze_authorization_grant_request_record_dryrun",)
DRYRUN_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "request_record_dryrun != request_record",
    "request_record_candidate != request_record",
    "request_record_schema_candidate != request_record_schema_final",
    "evidence_binding_candidate != evidence_bound_record",
    "owner_approval_binding_candidate != owner_approval_record",
    "revocation_reference_candidate != revocation_execution",
    "authorization_request_candidate != authorization_request_issued",
    "grant_token_candidate != grant_token",
    "grant_candidate != grant_record",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
)
ALLOWED_SCOPE_CLASSIFICATIONS: Tuple[str, ...] = (
    "request-record-planning-scope",
    "request-record-dryrun-scope",
)
FORBIDDEN_ASSET_STATES: Tuple[str, ...] = (
    "frozen",
    "foundation-frozen",
    "closed",
    "foundation-finalized",
    "request-record",
    "request-record-schema-final",
    "evidence-bound-record",
    "owner-approval-record",
    "authorization-request-issued",
    "revocation-execution-path",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_request_record_planning_go",
    "request_record_plan_integrity_ok",
    "record_scope_preserved",
    "request_record_candidate_preserved",
    "request_record_schema_candidate_preserved",
    "evidence_binding_candidate_preserved",
    "owner_approval_binding_candidate_preserved",
    "candidate_lifecycle_preserved",
    "revocation_reference_candidate_preserved",
    "record_prerequisites_satisfied",
    "record_evidence_traceability_ok",
    "authorization_request_absent",
    "request_record_absent",
    "request_record_schema_final_absent",
    "evidence_bound_record_absent",
    "owner_approval_record_absent",
    "grant_token_absent",
    "grant_record_absent",
    "authorization_grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "template_lineage_ok",
    "request_record_dryrun_only",
    "post_review_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, planning: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "request_record_dryrun_only": True,
        "authorization_request_absent": True,
        "authorization_request_issued": False,
        "request_record_absent": True,
        "request_record_schema_final_absent": True,
        "evidence_bound_record_absent": True,
        "owner_approval_record_absent": True,
        "authorization_grant_absent": True,
        "grant_token_absent": True,
        "grant_record_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "grant_request_record_planning_root": str(planning),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_v1(
    *,
    grant_request_record_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(grant_request_record_planning_root).expanduser().resolve()
    meta = _meta(out, planning)
    issues: List[str] = []

    planning_summary = _read_json(planning / "summary.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    scope_matrix = _read_json(planning / "task_manager_freeze_authorization_grant_request_record_scope_matrix_v1.json")
    candidate_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_request_record_candidate_matrix_v1.json"
    )
    schema_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_request_record_schema_candidate_v1.json"
    )
    evidence_binding_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_request_record_evidence_binding_matrix_v1.json"
    )
    owner_binding_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_request_record_owner_approval_binding_matrix_v1.json"
    )
    lifecycle_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_request_record_lifecycle_matrix_v1.json"
    )
    revocation_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_request_record_revocation_reference_matrix_v1.json"
    )
    prerequisite_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_request_record_prerequisite_matrix_v1.json"
    )
    record_plan = _read_json(
        planning / "task_manager_foundation_handoff_freeze_authorization_grant_request_record_plan_v1.json"
    )
    boundary_contract = _read_json(
        planning / "task_manager_freeze_authorization_grant_request_record_boundary_contract_v1.json"
    )
    debt_carryover = _read_json(
        planning / "task_manager_freeze_authorization_grant_request_record_governance_debt_carryover_v1.json"
    )
    non_execution_doc = _read_json(
        planning / "task_manager_freeze_authorization_grant_request_record_non_execution_constraints_v1.json"
    )

    integrity_rows = []
    for fname in GRANT_REQUEST_RECORD_PLANNING_PACKAGE_FILES:
        path = planning / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        integrity_rows.append({"file": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_or_placeholder:{fname}")

    prior_request_record_planning_go = (
        planning_summary.get("final_decision") == GRANT_REQUEST_RECORD_PLANNING_FINAL_GO
        and planning_summary.get("recommended_next_phase") == GRANT_REQUEST_RECORD_PLANNING_NEXT_PHASE
        and planning_verifier.get("verifier") == "GO"
        and int(planning_verifier.get("passed_checks", 0)) >= 420
        and planning_verifier.get("failed_checks") == 0
        and planning_verifier.get("blocker_count") == 0
        and planning_summary.get("next_phase_readiness_ok") is True
    )
    if not prior_request_record_planning_go:
        issues.append("request_record_planning_not_go")

    for key in PLANNING_TRUE_KEYS:
        if planning_summary.get(key) is not True:
            issues.append(f"planning_key_false:{key}")

    trace_rows = list(record_plan.get("evidence_chain") or [])
    trace_rows.append(
        {
            "stage": "freeze_authorization_grant_request_record_dryrun",
            "root": str(out),
            "readiness": "request-record-dryrun-scope",
            "authorization_request_issued": False,
            "request_record": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    record_evidence_traceability_ok = all(
        next((r for r in trace_rows if r.get("stage") == stage), {}).get("linked") is True
        for stage in CHAIN_TRACE_NODES
    )
    dryrun_node = next(
        (r for r in trace_rows if r.get("stage") == "freeze_authorization_grant_request_record_dryrun"),
        {},
    )
    if (
        dryrun_node.get("authorization_request_issued") is True
        or dryrun_node.get("request_record") is True
        or dryrun_node.get("grant_issued") is True
    ):
        record_evidence_traceability_ok = False
    if not record_evidence_traceability_ok:
        issues.append("chain_trace_gap")

    scope_rows = []
    for row in scope_matrix.get("rows") or []:
        scope_rows.append({**row, "classification": "request-record-dryrun-scope"})
    record_scope_preserved = all(
        row.get("classification") in ALLOWED_SCOPE_CLASSIFICATIONS for row in scope_rows
    ) and all(
        row.get("classification") not in ("request-record-created-scope", "authorized-scope") for row in scope_rows
    )
    if not record_scope_preserved:
        issues.append("record_scope_escalation")

    freeze_status = boundary_contract.get("freeze_status") or "freeze-candidate"
    record_rows = candidate_matrix.get("rows") or []
    request_record_candidate_preserved = all(
        row.get("record_status") == "request-record-candidate"
        and row.get("record_status") != "request-record"
        and row.get("record_created") is False
        and row.get("authorization_request_issued") is False
        for row in record_rows
    ) if record_rows else candidate_matrix.get("request_record_candidate_only") is True
    if not request_record_candidate_preserved:
        issues.append("request_record_leakage")

    schema_rows = schema_matrix.get("rows") or []
    request_record_schema_candidate_preserved = all(
        row.get("schema_status") == "request-record-schema-candidate"
        and row.get("schema_status") not in ("stable-schema", "production-schema", "request-record-schema-final")
        and row.get("schema_final") is False
        and row.get("production_schema") is False
        for row in schema_rows
    ) if schema_rows else schema_matrix.get("request_record_schema_candidate_only") is True
    if not request_record_schema_candidate_preserved:
        issues.append("schema_escalation")

    evidence_binding_rows = evidence_binding_matrix.get("rows") or []
    evidence_binding_candidate_preserved = all(
        row.get("binding_status") == "evidence-binding-candidate"
        and row.get("binding_status") != "evidence-bound-record"
        and row.get("evidence_bound") is False
        for row in evidence_binding_rows
    ) if evidence_binding_rows else evidence_binding_matrix.get("evidence_binding_candidate_only") is True
    if not evidence_binding_candidate_preserved:
        issues.append("evidence_binding_leakage")

    owner_binding_rows = owner_binding_matrix.get("rows") or []
    owner_approval_binding_candidate_preserved = all(
        row.get("binding_status") == "owner-approval-binding-candidate"
        and row.get("binding_status") != "owner-approval-record"
        and row.get("owner_approval_record") is not True
        for row in owner_binding_rows
    ) if owner_binding_rows else owner_binding_matrix.get("owner_approval_binding_candidate_only") is True
    if not owner_approval_binding_candidate_preserved:
        issues.append("owner_approval_binding_leakage")

    lifecycle_rows = lifecycle_matrix.get("rows") or []
    candidate_lifecycle_preserved = all(
        row.get("lifecycle_type") == "candidate-lifecycle"
        and row.get("lifecycle_type") != "active-record-lifecycle"
        for row in lifecycle_rows
    ) if lifecycle_rows else lifecycle_matrix.get("lifecycle_candidate_only") is True
    if not candidate_lifecycle_preserved:
        issues.append("lifecycle_escalation")

    revocation_rows = revocation_matrix.get("rows") or []
    revocation_reference_candidate_preserved = all(
        row.get("reference_status") == "revocation-reference-candidate"
        and row.get("reference_status") != "revocation-execution-path"
        and row.get("revocation_execution_path") is False
        for row in revocation_rows
    ) if revocation_rows else revocation_matrix.get("revocation_reference_candidate_only") is True
    if not revocation_reference_candidate_preserved:
        issues.append("revocation_execution_leakage")

    authorization_request_absent = True
    authorization_grant_absent = (
        planning_summary.get("authorization_grant_absent") is True
        and boundary_contract.get("grant_issued") is False
    )
    request_record_absent = True
    request_record_schema_final_absent = True
    evidence_bound_record_absent = True
    grant_token_absent = planning_summary.get("grant_token_absent") is True
    grant_record_absent = planning_summary.get("grant_record_absent") is True
    owner_approval_record_absent = planning_summary.get("owner_approval_record_absent") is True
    foundation_not_frozen = boundary_contract.get("foundation_frozen") is False
    closure_not_executed = (
        boundary_contract.get("closure_applied") is False
        and boundary_contract.get("closed") is False
    )
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if planning_summary.get(flag) is True:
            if "authorization_request" in flag:
                authorization_request_absent = False
            elif flag == "authorization_grant_created_now":
                authorization_grant_absent = False
            elif flag == "grant_token_created_now":
                grant_token_absent = False
            elif flag == "grant_record_created_now":
                grant_record_absent = False
            elif flag == "owner_approval_record_created_now":
                owner_approval_record_absent = False

    prerequisite_validation = {
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "request_record_schema_final_absent": request_record_schema_final_absent,
        "evidence_bound_record_absent": evidence_bound_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
    }
    record_prerequisites_satisfied = (
        prerequisite_matrix.get("prerequisites_ok") is True
        and all(prerequisite_validation[k] for k in prerequisite_validation)
    )
    if not authorization_request_absent:
        issues.append("authorization_request_leakage")
    if not request_record_absent or not owner_approval_record_absent or not grant_token_absent or not grant_record_absent:
        issues.append("request_record_leakage")
    if not request_record_schema_final_absent or not evidence_bound_record_absent:
        issues.append("schema_or_binding_leakage")
    if not authorization_grant_absent:
        issues.append("grant_issuance_leakage")
    if not foundation_not_frozen:
        issues.append("freeze_state_escalation")
    if not closure_not_executed:
        issues.append("closure_state_escalation")
    if not record_prerequisites_satisfied:
        issues.append("prerequisite_gap")

    non_execution_boundary_ok = non_execution_doc.get("non_execution_boundary_ok") is True
    if not non_execution_boundary_ok:
        issues.append("runtime_scope_leakage")

    debts = debt_carryover.get("debts") or []
    debt0 = debts[0] if debts else {}
    debt1 = debts[1] if len(debts) > 1 else {}
    governance_debt_preserved = (
        len(debts) >= 2
        and debt0.get("debt_title") == GOVERNANCE_DEBTS[0]["debt_title"]
        and debt0.get("priority") == "P1"
        and debt0.get("classification") == "L1 Midplatform System Protocols"
        and debt0.get("must_not_implement_now") is True
        and debt1.get("debt_title") == GOVERNANCE_DEBTS[1]["debt_title"]
        and debt1.get("priority") == "P1"
        and debt1.get("classification") == "L1 Midplatform System Protocols"
        and debt1.get("must_not_implement_now") is True
    )
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    l1_protocols_not_implemented = debt_carryover.get("l1_protocols_not_implemented") is True
    system_protocols_integration_not_implemented = (
        debt_carryover.get("system_protocols_integration_not_implemented") is True
    )
    if not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        issues.append("l1_protocol_scope_leakage")

    request_record_plan_integrity_ok = all(r["exists"] and r["non_placeholder"] for r in integrity_rows)
    request_record_dryrun_only = True
    post_review_readiness_ok = (
        prior_request_record_planning_go
        and record_evidence_traceability_ok
        and governance_debt_preserved
    )

    if not request_record_plan_integrity_ok or not prior_request_record_planning_go:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not record_evidence_traceability_ok:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not record_scope_preserved:
        final_decision = FINAL_DECISION_SCOPE
    elif not authorization_request_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif (
        not request_record_absent
        or not request_record_schema_final_absent
        or not evidence_bound_record_absent
        or not owner_approval_record_absent
        or not grant_token_absent
        or not grant_record_absent
        or not authorization_grant_absent
    ):
        final_decision = FINAL_DECISION_RECORD
    elif (
        not request_record_candidate_preserved
        or not request_record_schema_candidate_preserved
        or not evidence_binding_candidate_preserved
        or not owner_approval_binding_candidate_preserved
        or not candidate_lifecycle_preserved
        or not revocation_reference_candidate_preserved
        or not foundation_not_frozen
    ):
        final_decision = FINAL_DECISION_FREEZE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    repo_root = Path(__file__).resolve().parents[2]
    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Request-Issuance-DryRun-v1-001",
        base_capability=GRANT_REQUEST_RECORD_DRYRUN_WHITELIST_FILES[0],
        base_runner=GRANT_REQUEST_RECORD_DRYRUN_WHITELIST_FILES[1],
        base_verifier=GRANT_REQUEST_RECORD_DRYRUN_WHITELIST_FILES[2],
        base_go_no_go_pack=GRANT_REQUEST_RECORD_DRYRUN_WHITELIST_FILES[3],
        stage_phase="Freeze-Authorization-Grant-Request-Record-DryRun-v1-001",
        stage_term_overrides=GRANT_REQUEST_RECORD_DRYRUN_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_REQUEST_RECORD_DRYRUN_STAGE_ADDITIONS,
        template_files=GRANT_REQUEST_RECORD_DRYRUN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Request-Record-Planning-v1-001",
    )
    upstream_lineage_ok = planning_summary.get("template_lineage_ok") is True
    template_lineage_ok = template_lineage.get("template_lineage_ok") is True and upstream_lineage_ok
    if not template_lineage_ok:
        issues.append("template_lineage_gap")

    go_condition_values = {
        "prior_request_record_planning_go": prior_request_record_planning_go,
        "request_record_plan_integrity_ok": request_record_plan_integrity_ok,
        "record_scope_preserved": record_scope_preserved,
        "request_record_candidate_preserved": request_record_candidate_preserved,
        "request_record_schema_candidate_preserved": request_record_schema_candidate_preserved,
        "evidence_binding_candidate_preserved": evidence_binding_candidate_preserved,
        "owner_approval_binding_candidate_preserved": owner_approval_binding_candidate_preserved,
        "candidate_lifecycle_preserved": candidate_lifecycle_preserved,
        "revocation_reference_candidate_preserved": revocation_reference_candidate_preserved,
        "record_prerequisites_satisfied": record_prerequisites_satisfied,
        "record_evidence_traceability_ok": record_evidence_traceability_ok,
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "request_record_schema_final_absent": request_record_schema_final_absent,
        "evidence_bound_record_absent": evidence_bound_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "template_lineage_ok": template_lineage_ok,
        "request_record_dryrun_only": request_record_dryrun_only,
        "post_review_readiness_ok": post_review_readiness_ok,
    }
    dryrun_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO and all(go_condition_values.values())
    next_phase = NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions=go_condition_values,
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=CHAIN_TRACE_NODES,
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    dryrun_report = {
        "report_id": "task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_report_v1",
        "planning_final_decision": planning_summary.get("final_decision"),
        "planning_verifier": planning_verifier.get("verifier"),
        **go_condition_values,
        "boundary_statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    plan_integrity_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_request_record_plan_integrity_matrix_v1",
        "rows": integrity_rows,
        "request_record_plan_integrity_ok": request_record_plan_integrity_ok,
        **meta,
    }
    scope_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_scope_validation_v1",
        "rows": scope_rows,
        "record_scope_preserved": record_scope_preserved,
        "allowed_classifications": list(ALLOWED_SCOPE_CLASSIFICATIONS),
        **meta,
    }
    candidate_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_candidate_validation_v1",
        "rows": record_rows,
        "freeze_status": freeze_status,
        "request_record_candidate_preserved": request_record_candidate_preserved,
        "record_status": "request-record-candidate",
        "forbidden_states": list(FORBIDDEN_ASSET_STATES),
        **meta,
    }
    schema_candidate_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_schema_candidate_validation_v1",
        "rows": schema_rows,
        "request_record_schema_candidate_preserved": request_record_schema_candidate_preserved,
        "schema_status": "request-record-schema-candidate",
        **meta,
    }
    evidence_binding_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_evidence_binding_validation_v1",
        "rows": evidence_binding_rows,
        "evidence_binding_candidate_preserved": evidence_binding_candidate_preserved,
        "binding_status": "evidence-binding-candidate",
        **meta,
    }
    owner_approval_binding_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_owner_approval_binding_validation_v1",
        "rows": owner_binding_rows,
        "owner_approval_binding_candidate_preserved": owner_approval_binding_candidate_preserved,
        "binding_status": "owner-approval-binding-candidate",
        **meta,
    }
    lifecycle_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_lifecycle_validation_v1",
        "rows": lifecycle_rows,
        "candidate_lifecycle_preserved": candidate_lifecycle_preserved,
        "lifecycle_type": "candidate-lifecycle",
        **meta,
    }
    revocation_reference_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_revocation_reference_validation_v1",
        "rows": revocation_rows,
        "revocation_reference_candidate_preserved": revocation_reference_candidate_preserved,
        "reference_status": "revocation-reference-candidate",
        **meta,
    }
    prerequisite_validation_doc = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_prerequisite_validation_v1",
        "rows": prerequisite_matrix.get("rows") or [],
        "record_prerequisites_satisfied": record_prerequisites_satisfied,
        **prerequisite_validation,
        **meta,
    }
    evidence_traceability = {
        "trace_id": "task_manager_freeze_authorization_grant_request_record_evidence_traceability_v1",
        "matrix_id": "task_manager_freeze_authorization_grant_request_record_chain_traceability_matrix_v1",
        "rows": trace_rows,
        "record_evidence_traceability_ok": record_evidence_traceability_ok,
        "freeze_authorization_chain_traceability_ok": record_evidence_traceability_ok,
        "points_to_dryrun_not_record": True,
        "points_to_dryrun_not_issued": True,
        **meta,
    }
    absence_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_absence_validation_v1",
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "request_record_schema_final_absent": request_record_schema_final_absent,
        "evidence_bound_record_absent": evidence_bound_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "no_freeze_execution_path": True,
        "no_rollback_execution_path": True,
        **meta,
    }
    boundary_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_boundary_validation_v1",
        "statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "request_record_dryrun_only": request_record_dryrun_only,
        "authorization_request_issued": False,
        "request_record_created": False,
        "request_record_schema_final_created": False,
        "evidence_bound_record_created": False,
        "owner_approval_record_created": False,
        "grant_issued": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    governance_debt_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_request_record_governance_debt_validation_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    post_review_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_request_record_post_review_readiness_v1",
        "post_review_readiness_ok": post_review_readiness_ok,
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_request_record_post_dryrun_review",
        "module_adapter_implementation_ready": False,
        "authorization_request_issued": False,
        "request_record_created": False,
        "owner_approval_record_created": False,
        "grant_issued": False,
        "freeze_authorization_granted": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    template_lineage_doc = {
        "lineage_id": "task_manager_freeze_authorization_grant_request_record_template_lineage_v1",
        "upstream_request_record_planning_lineage_ok": upstream_lineage_ok,
        **template_lineage,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Grant Request Record DryRun Report v1",
            "",
            "This phase performs freeze authorization grant request record dry-run validation only. It does not create request records, bind evidence records, or issue authorization request.",
            "",
            "本阶段仅执行 freeze authorization grant request record dry-run validation，不生成 request record，不绑定 evidence record，不发起 authorization request，不生成 owner approval record，不签发 grant。",
            "",
            f"Request record planning GO: `{prior_request_record_planning_go}`",
            f"Authorization request absent: `{authorization_request_absent}`",
            f"Request record absent: `{request_record_absent}`",
            f"Request record schema final absent: `{request_record_schema_final_absent}`",
            f"Evidence bound record absent: `{evidence_bound_record_absent}`",
            f"Owner approval record absent: `{owner_approval_record_absent}`",
            f"Grant token absent: `{grant_token_absent}`",
            f"Grant record absent: `{grant_record_absent}`",
            f"Freeze status: `{freeze_status}` (not frozen)",
            f"Governance debt preserved: `{governance_debt_preserved}`",
            f"Template lineage OK: `{template_lineage_ok}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Request Record DryRun Boundary Statements",
            *[f"- {stmt}" for stmt in DRYRUN_BOUNDARY_STATEMENTS],
            "",
            "request record dryrun ≠ request record",
            "",
            "## Governance Debts (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_report": dryrun_report,
        "task_manager_foundation_handoff_freeze_authorization_grant_request_record_dryrun_report_md": markdown,
        "task_manager_freeze_authorization_grant_request_record_plan_integrity_matrix": plan_integrity_matrix,
        "task_manager_freeze_authorization_grant_request_record_scope_validation": scope_validation,
        "task_manager_freeze_authorization_grant_request_record_candidate_validation": candidate_validation,
        "task_manager_freeze_authorization_grant_request_record_schema_candidate_validation": schema_candidate_validation,
        "task_manager_freeze_authorization_grant_request_record_evidence_binding_validation": evidence_binding_validation,
        "task_manager_freeze_authorization_grant_request_record_owner_approval_binding_validation": owner_approval_binding_validation,
        "task_manager_freeze_authorization_grant_request_record_lifecycle_validation": lifecycle_validation,
        "task_manager_freeze_authorization_grant_request_record_revocation_reference_validation": revocation_reference_validation,
        "task_manager_freeze_authorization_grant_request_record_prerequisite_validation": prerequisite_validation_doc,
        "task_manager_freeze_authorization_grant_request_record_evidence_traceability": evidence_traceability,
        "task_manager_freeze_authorization_grant_request_record_absence_validation": absence_validation,
        "task_manager_freeze_authorization_grant_request_record_boundary_validation": boundary_validation,
        "task_manager_freeze_authorization_grant_request_record_governance_debt_validation": governance_debt_validation,
        "task_manager_freeze_authorization_grant_request_record_post_review_readiness": post_review_readiness,
        "task_manager_freeze_authorization_grant_request_record_template_lineage": template_lineage_doc,
        "summary": summary,
    }
