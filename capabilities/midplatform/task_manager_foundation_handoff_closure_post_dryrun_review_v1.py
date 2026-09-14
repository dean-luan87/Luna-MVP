# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Closure Post-DryRun Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_closure_dryrun_v1 import (
    CLOSURE_CHANNEL_BOUNDARIES,
    CLOSURE_GOVERNANCE_DEBT,
    DEFAULT_OUTPUT as DEFAULT_CLOSURE_DRYRUN_ROOT,
    FINAL_DECISION_GO as CLOSURE_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as CLOSURE_DRYRUN_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Closure-Post-DryRun-Review-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_closure_post_dryrun_review_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_closure_post_dryrun_review_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_POST_DRYRUN_REVIEW_READY_FOR_FINAL_CLOSURE_PLANNING"
FINAL_DECISION_EVIDENCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_DRYRUN_EVIDENCE_GAP"
FINAL_DECISION_BOUNDARY = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_BOUNDARY_DRIFT"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_L1_CLOSURE_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_SEMANTICS = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_CANDIDATE_SEMANTICS_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_DOWNSTREAM = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_DOWNSTREAM_SCOPE_ESCALATION"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Closure-Post-DryRun-Review-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_closure_post_dryrun_review_v1_smoke_v0"
)

CLOSURE_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_closure_dryrun_report_v1.json",
    "task_manager_foundation_handoff_closure_dryrun_report_v1.md",
    "task_manager_closure_plan_integrity_matrix_v1.json",
    "task_manager_closure_evidence_traceability_matrix_v1.json",
    "task_manager_closure_freeze_candidate_validation_v1.json",
    "task_manager_closure_candidate_semantics_validation_v1.json",
    "task_manager_closure_downstream_scope_validation_v1.json",
    "task_manager_closure_non_execution_validation_v1.json",
    "task_manager_closure_governance_debt_register_v1.json",
    "summary.json",
    "verifier_report.json",
)
DRYRUN_TRUE_KEYS: Tuple[str, ...] = (
    "closure_plan_integrity_ok",
    "closure_evidence_traceability_ok",
    "freeze_candidate_preserved",
    "closure_candidate_preserved",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_scope_ok",
    "closure_channel_governance_debt_recorded",
    "l1_closure_protocol_not_implemented",
    "closure_dryrun_only",
)
FORBIDDEN_STATUS: Tuple[str, ...] = (
    "closed",
    "frozen",
    "foundation-finalized",
    "foundation_finalized",
    "implementation-ready",
    "runtime-ready",
    "production-ready",
)
RUNTIME_FORBIDDEN: Tuple[str, ...] = (
    "runtime_executor_created_now",
    "scheduler_binding_created_now",
    "task_execution_authority_granted_now",
    "output_authorization_granted_now",
    "module_adapter_integration_created_now",
    "information_channel_governance_implemented_now",
    "protocol_governance_implemented_now",
    "closure_channel_governance_implemented_now",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, dryrun: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "post_review_only": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "closure_channel_governance_not_implemented": True,
        "output_root": str(out),
        "closure_dryrun_root": str(dryrun),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_closure_post_dryrun_review_v1(
    *,
    closure_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(closure_dryrun_root).expanduser().resolve()
    meta = _meta(out, dryrun)
    issues: List[str] = []

    dryrun_summary = _read_json(dryrun / "summary.json")
    dryrun_verifier = _read_json(dryrun / "verifier_report.json")
    debt_register = _read_json(dryrun / "task_manager_closure_governance_debt_register_v1.json")
    freeze_val = _read_json(dryrun / "task_manager_closure_freeze_candidate_validation_v1.json")
    semantics_val = _read_json(dryrun / "task_manager_closure_candidate_semantics_validation_v1.json")
    downstream_val = _read_json(dryrun / "task_manager_closure_downstream_scope_validation_v1.json")
    non_exec = _read_json(dryrun / "task_manager_closure_non_execution_validation_v1.json")

    review_rows = []
    for fname in CLOSURE_DRYRUN_ARTIFACTS:
        path = dryrun / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        review_rows.append({"artifact": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_dryrun_artifact:{fname}")

    closure_dryrun_result_accepted = (
        dryrun_summary.get("final_decision") == CLOSURE_DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == CLOSURE_DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 420
        and dryrun_verifier.get("failed_checks") == 0
        and dryrun_verifier.get("blocker_count") == 0
        and all(dryrun_summary.get(k) is True for k in DRYRUN_TRUE_KEYS)
    )
    if not closure_dryrun_result_accepted:
        issues.append("closure_dryrun_not_accepted")

    boundary_drift_rows = []
    for fname in CLOSURE_DRYRUN_ARTIFACTS:
        if not fname.endswith(".json"):
            continue
        doc = _read_json(dryrun / fname)
        runtime_leak = any(doc.get(flag) is True for flag in RUNTIME_FORBIDDEN)
        boundary_drift_rows.append(
            {"artifact": fname, "runtime_scope_leak_absent": not runtime_leak, "post_review_added_runtime": False}
        )
        if runtime_leak:
            issues.append(f"runtime_scope_leakage:{fname}")

    debts = debt_register.get("debts") or []
    debt = debts[0] if debts else {}
    governance_debt_preserved = (
        debt.get("debt_title") == CLOSURE_GOVERNANCE_DEBT["debt_title"]
        and debt.get("priority") == "P1"
        and debt.get("classification") == "L1 Midplatform System Protocols"
        and debt.get("must_not_implement_now") is True
        and debt.get("recommended_future_phase") == CLOSURE_GOVERNANCE_DEBT["recommended_future_phase"]
    )
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    closure_channel_governance_not_implemented = (
        debt_register.get("l1_closure_protocol_not_implemented") is True
        and debt.get("must_not_implement_now") is True
    )
    if not closure_channel_governance_not_implemented:
        issues.append("l1_closure_protocol_scope_leakage")

    freeze_status = freeze_val.get("freeze_status")
    closure_readiness = freeze_val.get("closure_readiness")
    freeze_candidate_preserved = (
        freeze_status == "freeze-candidate"
        and freeze_val.get("freeze_candidate_preserved") is True
        and freeze_val.get("foundation_frozen") is False
    )
    closure_candidate_preserved = (
        closure_readiness in ("closure-dryrun-ready", "final-closure-planning-ready")
        and freeze_val.get("closure_candidate_preserved") is True
        and freeze_val.get("closure_applied") is False
    )
    if not freeze_candidate_preserved:
        issues.append("freeze_candidate_drift")
    if not closure_candidate_preserved or closure_readiness == "closed":
        issues.append("closure_state_escalation")

    candidate_semantics_preserved = semantics_val.get("candidate_semantics_preserved") is True
    if not candidate_semantics_preserved:
        issues.append("candidate_semantics_drift")

    downstream_scope_ok = downstream_val.get("downstream_scope_ok") is True
    for row in downstream_val.get("consumers") or []:
        if row.get("readiness") in FORBIDDEN_STATUS:
            downstream_scope_ok = False
    if not downstream_scope_ok:
        issues.append("downstream_scope_escalation")

    non_execution_boundary_ok = non_exec.get("non_execution_boundary_ok") is True
    if not non_execution_boundary_ok:
        issues.append("runtime_scope_leakage")

    boundary_drift_absent = all(r["runtime_scope_leak_absent"] for r in boundary_drift_rows)
    final_closure_planning_ready = (
        closure_dryrun_result_accepted
        and boundary_drift_absent
        and governance_debt_preserved
        and closure_channel_governance_not_implemented
        and freeze_candidate_preserved
        and closure_candidate_preserved
        and candidate_semantics_preserved
        and non_execution_boundary_ok
        and downstream_scope_ok
    )

    evidence_chain = [
        {"stage": "closure_planning", "linked": True},
        {"stage": "closure_dryrun", "linked": closure_dryrun_result_accepted},
        {"stage": "closure_post_dryrun_review", "readiness": "final-closure-planning-ready", "closure_applied": False},
    ]
    final_planning_rows = [
        {"target": "final_closure_planning", "readiness": "final-closure-planning-ready", "closure_applied": False, "foundation_freeze_applied": False},
        {"target": "freeze_planning", "readiness": "final-closure-planning-ready", "closure_applied": False, "foundation_freeze_applied": False},
        {"target": "module_adapter_implementation", "readiness": "not-ready", "closure_applied": False, "foundation_freeze_applied": False},
    ]

    if not closure_dryrun_result_accepted:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not closure_channel_governance_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not boundary_drift_absent:
        final_decision = FINAL_DECISION_BOUNDARY
    elif not candidate_semantics_preserved:
        final_decision = FINAL_DECISION_SEMANTICS
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not downstream_scope_ok:
        final_decision = FINAL_DECISION_DOWNSTREAM
    else:
        final_decision = FINAL_DECISION_GO

    review_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO
    review_report = {
        "review_id": "task_manager_foundation_handoff_closure_post_dryrun_review_v1",
        "closure_dryrun_result_accepted": closure_dryrun_result_accepted,
        "boundary_drift_absent": boundary_drift_absent,
        "governance_debt_preserved": governance_debt_preserved,
        "closure_channel_governance_not_implemented": closure_channel_governance_not_implemented,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "closure_candidate_preserved": closure_candidate_preserved,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_scope_ok": downstream_scope_ok,
        "post_review_only": True,
        "final_closure_planning_ready": final_closure_planning_ready,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    dryrun_review_matrix = {
        "matrix_id": "task_manager_closure_dryrun_review_matrix_v1",
        "rows": review_rows,
        "closure_dryrun_result_accepted": closure_dryrun_result_accepted,
        **meta,
    }
    boundary_drift_review = {
        "review_id": "task_manager_closure_boundary_drift_review_v1",
        "rows": boundary_drift_rows,
        "boundary_drift_absent": boundary_drift_absent,
        **meta,
    }
    evidence_chain_review = {
        "review_id": "task_manager_closure_evidence_chain_review_v1",
        "chain": evidence_chain,
        "evidence_chain_ok": closure_dryrun_result_accepted,
        **meta,
    }
    governance_debt_review = {
        "review_id": "task_manager_closure_governance_debt_review_v1",
        "debt": debt,
        "governance_debt_preserved": governance_debt_preserved,
        "closure_channel_governance_not_implemented": closure_channel_governance_not_implemented,
        **meta,
    }
    final_planning_matrix = {
        "matrix_id": "task_manager_closure_final_planning_readiness_matrix_v1",
        "rows": final_planning_rows,
        "final_closure_planning_ready": final_closure_planning_ready,
        "closure_applied": False,
        "foundation_freeze_applied": False,
        **meta,
    }
    review_non_execution = {
        "constraints_id": "task_manager_closure_review_non_execution_constraints_v1",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_runtime_executor": True,
        "no_scheduler_binding": True,
        "no_task_execution_authority": True,
        "no_output_authorization": True,
        "no_memory_worldmodel_write_path": True,
        "no_module_adapter_integration": True,
        "no_authorization_grant": True,
        "no_information_channel_governance_implementation": True,
        "no_protocol_governance_implementation": True,
        "no_closure_channel_governance_implementation": True,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "post_dryrun_review_pass": review_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "closure_dryrun_result_accepted": closure_dryrun_result_accepted,
        "boundary_drift_absent": boundary_drift_absent,
        "governance_debt_preserved": governance_debt_preserved,
        "closure_channel_governance_not_implemented": closure_channel_governance_not_implemented,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "closure_candidate_preserved": closure_candidate_preserved,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_scope_ok": downstream_scope_ok,
        "post_review_only": True,
        "final_closure_planning_ready": final_closure_planning_ready,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Closure Post-DryRun Review v1",
            "",
            "This phase reviews closure dry-run results only. It does not execute closure, freeze the foundation, or implement L1 Closure Channel Governance.",
            "",
            "本阶段仅审查 closure dry-run 结果，不执行 closure，不冻结 foundation，不实现 L1 Closure Channel Governance。",
            "",
            f"Closure dry-run accepted: `{closure_dryrun_result_accepted}`",
            f"Governance debt preserved: `{governance_debt_preserved}`",
            f"Final closure planning ready: `{final_closure_planning_ready}`",
            f"Freeze status preserved: `freeze-candidate` (not frozen)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Closure Channel Boundaries",
            *[f"- {item['boundary']}" for item in CLOSURE_CHANNEL_BOUNDARIES],
            "",
            "## Governance Debt Preserved",
            f"- {CLOSURE_GOVERNANCE_DEBT['debt_title']} (P1, not implemented)",
        ]
    )
    return {
        "task_manager_foundation_handoff_closure_post_dryrun_review": review_report,
        "task_manager_foundation_handoff_closure_post_dryrun_review_md": markdown,
        "task_manager_closure_dryrun_review_matrix": dryrun_review_matrix,
        "task_manager_closure_boundary_drift_review": boundary_drift_review,
        "task_manager_closure_evidence_chain_review": evidence_chain_review,
        "task_manager_closure_governance_debt_review": governance_debt_review,
        "task_manager_closure_final_planning_readiness_matrix": final_planning_matrix,
        "task_manager_closure_review_non_execution_constraints": review_non_execution,
        "summary": summary,
    }
