# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Closure DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_closure_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CLOSURE_PLANNING_ROOT,
    FINAL_DECISION_GO as CLOSURE_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as CLOSURE_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Closure-DryRun-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_closure_dryrun_validation_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_closure_dryrun_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_PLAN_GAP = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_DRYRUN_BLOCKED_BY_CLOSURE_PLAN_GAP"
FINAL_DECISION_EVIDENCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_DRYRUN_BLOCKED_BY_EVIDENCE_TRACE_GAP"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_DRYRUN_BLOCKED_BY_FREEZE_SCOPE_LEAKAGE"
FINAL_DECISION_STATE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_DRYRUN_BLOCKED_BY_CLOSURE_STATE_ESCALATION"
FINAL_DECISION_SEMANTICS = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_DRYRUN_BLOCKED_BY_CANDIDATE_SEMANTICS_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_CLOSURE_DRYRUN_BLOCKED_BY_MISSING_CLOSURE_CHANNEL_GOVERNANCE_DEBT"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Closure-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Closure-DryRun-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_closure_dryrun_v1_smoke_v0"
)

CLOSURE_PLANNING_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_closure_plan_v1.json",
    "task_manager_foundation_handoff_closure_plan_v1.md",
    "task_manager_foundation_asset_inventory_v1.json",
    "task_manager_handoff_closure_evidence_chain_v1.json",
    "task_manager_handoff_freeze_candidate_boundary_v1.json",
    "task_manager_handoff_candidate_semantics_lock_plan_v1.json",
    "task_manager_handoff_downstream_planning_map_v1.json",
    "task_manager_handoff_future_l1_protocol_dependency_map_v1.json",
    "task_manager_handoff_closure_non_execution_constraints_v1.json",
    "summary.json",
    "verifier_report.json",
)
CLOSURE_CHANNEL_BOUNDARIES: Tuple[Dict[str, str], ...] = (
    {"candidate": "closure_candidate", "boundary": "closure_candidate != closed"},
    {"candidate": "freeze_candidate", "boundary": "freeze_candidate != frozen"},
    {"candidate": "handoff_candidate", "boundary": "handoff_candidate != handed_off"},
    {"candidate": "deprecation_candidate", "boundary": "deprecation_candidate != deprecated"},
    {"candidate": "rollback_recommendation_candidate", "boundary": "rollback_recommendation_candidate != rollback_execution"},
    {"candidate": "archive_candidate", "boundary": "archive_candidate != archived"},
    {"candidate": "finalization_candidate", "boundary": "finalization_candidate != finalized"},
    {"candidate": "task_candidate", "boundary": "task_candidate != task execution"},
    {"candidate": "task_step_candidate", "boundary": "task_step_candidate != executed step"},
)
CLOSURE_GOVERNANCE_DEBT: Dict[str, Any] = {
    "debt_id": "closure_channel_governance_missing_canonical_protocol",
    "debt_title": "Closure Channel Governance Missing Canonical Protocol",
    "priority": "P1",
    "classification": "L1 Midplatform System Protocols",
    "debt_type": "canonical_protocol_missing",
    "current_handling": "module_scoped_closure_rehearsal_only",
    "must_not_implement_now": True,
    "recommended_future_phase": "Phase-Midplatform-Closure-Channel-Governance-Planning-v1-001",
    "related_future_phases": [
        "Phase-Midplatform-Information-Channel-Governance-Planning-v1-001",
        "Phase-Midplatform-Protocol-Governance-Layer-Planning-v1-001",
    ],
    "boundary_statement": "Task Manager closure dry-run must not be treated as canonical L1 Closure Channel Governance",
}
FORBIDDEN_ESCALATIONS: Tuple[str, ...] = (
    "frozen",
    "closed",
    "handed_off",
    "deprecated",
    "archived",
    "finalized",
    "implementation-ready",
    "runtime-ready",
    "production-ready",
)
RUNTIME_FORBIDDEN_FLAGS: Tuple[str, ...] = (
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


def _meta(out: Path, planning: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "closure_dryrun_only": True,
        "foundation_not_frozen": True,
        "l1_closure_protocol_not_implemented": True,
        "output_root": str(out),
        "closure_planning_root": str(planning),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
        "module_scoped_closure_rehearsal": True,
    }


def run_task_manager_foundation_handoff_closure_dryrun_v1(
    *,
    closure_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(closure_planning_root).expanduser().resolve()
    meta = _meta(out, planning)
    issues: List[str] = []

    planning_summary = _read_json(planning / "summary.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    closure_plan = _read_json(planning / "task_manager_foundation_handoff_closure_plan_v1.json")
    freeze_boundary = _read_json(planning / "task_manager_handoff_freeze_candidate_boundary_v1.json")
    semantics_plan = _read_json(planning / "task_manager_handoff_candidate_semantics_lock_plan_v1.json")
    downstream_map = _read_json(planning / "task_manager_handoff_downstream_planning_map_v1.json")
    evidence_chain_doc = _read_json(planning / "task_manager_handoff_closure_evidence_chain_v1.json")
    non_execution_doc = _read_json(planning / "task_manager_handoff_closure_non_execution_constraints_v1.json")

    integrity_rows = []
    for fname in CLOSURE_PLANNING_PACKAGE_FILES:
        path = planning / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        integrity_rows.append({"file": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_or_placeholder:{fname}")

    planning_go = (
        planning_summary.get("final_decision") == CLOSURE_PLANNING_FINAL_GO
        and planning_summary.get("recommended_next_phase") == CLOSURE_PLANNING_NEXT_PHASE
        and planning_verifier.get("verifier") == "GO"
        and int(planning_verifier.get("passed_checks", 0)) >= 420
        and planning_verifier.get("failed_checks") == 0
        and planning_verifier.get("blocker_count") == 0
    )
    if not planning_go:
        issues.append("closure_planning_not_go")

    planning_true_keys = (
        "prior_chain_go",
        "closure_plan_complete",
        "asset_inventory_complete",
        "evidence_chain_complete",
        "freeze_candidate_only",
        "closure_planning_only",
        "candidate_semantics_preserved",
        "non_execution_boundary_ok",
        "downstream_scope_ok",
        "future_l1_dependencies_only",
    )
    for key in planning_true_keys:
        if planning_summary.get(key) is not True:
            issues.append(f"planning_key_false:{key}")

    evidence_rows = evidence_chain_doc.get("chain") or []
    evidence_traceability_ok = evidence_chain_doc.get("evidence_chain_complete") is True and all(
        row.get("linked") is True for row in evidence_rows if row.get("stage") != "closure_planning"
    )
    if not evidence_traceability_ok:
        issues.append("evidence_trace_gap")

    freeze_status = freeze_boundary.get("freeze_status")
    closure_readiness = freeze_boundary.get("closure_readiness")
    freeze_candidate_preserved = (
        freeze_status == "freeze-candidate"
        and freeze_boundary.get("foundation_frozen") is False
        and freeze_boundary.get("closure_applied") is False
    )
    closure_candidate_preserved = closure_readiness == "closure-dryrun-ready" and freeze_boundary.get("closure_applied") is False
    if not freeze_candidate_preserved:
        issues.append("freeze_scope_leakage")
    if not closure_candidate_preserved:
        issues.append("closure_state_escalation")

    candidate_semantics_preserved = (
        semantics_plan.get("candidate_semantics_preserved") is True
        and semantics_plan.get("lock_plan_only") is True
        and semantics_plan.get("semantics_executed") is False
    )
    if not candidate_semantics_preserved:
        issues.append("candidate_semantics_drift")

    downstream_scope_ok = downstream_map.get("downstream_scope_ok") is True
    for row in downstream_map.get("consumers") or []:
        if row.get("readiness") in ("implementation-ready", "runtime-ready", "production-ready"):
            downstream_scope_ok = False
    if not downstream_scope_ok:
        issues.append("downstream_scope_escalation")

    non_execution_boundary_ok = non_execution_doc.get("non_execution_boundary_ok") is True
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if closure_plan.get(flag) is True or planning_summary.get(flag) is True:
            non_execution_boundary_ok = False
    if not non_execution_boundary_ok:
        issues.append("runtime_scope_leakage")

    governance_debt_register = {
        "register_id": "task_manager_closure_governance_debt_register_v1",
        "debts": [CLOSURE_GOVERNANCE_DEBT],
        "closure_channel_governance_debt_recorded": True,
        "l1_closure_protocol_not_implemented": True,
        **meta,
    }
    debt_recorded = (
        len(governance_debt_register["debts"]) == 1
        and governance_debt_register["debts"][0].get("debt_title") == "Closure Channel Governance Missing Canonical Protocol"
        and governance_debt_register["debts"][0].get("priority") == "P1"
        and governance_debt_register["debts"][0].get("must_not_implement_now") is True
    )
    if not debt_recorded:
        issues.append("missing_closure_channel_governance_debt")

    closure_plan_integrity_ok = all(r["exists"] and r["non_placeholder"] for r in integrity_rows)
    closure_dryrun_only = True

    if not closure_plan_integrity_ok or not planning_go:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not evidence_traceability_ok:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not freeze_candidate_preserved:
        final_decision = FINAL_DECISION_FREEZE
    elif not closure_candidate_preserved:
        final_decision = FINAL_DECISION_STATE
    elif not candidate_semantics_preserved:
        final_decision = FINAL_DECISION_SEMANTICS
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not debt_recorded:
        final_decision = FINAL_DECISION_DEBT
    else:
        final_decision = FINAL_DECISION_GO

    dryrun_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and closure_plan_integrity_ok
        and evidence_traceability_ok
        and freeze_candidate_preserved
        and closure_candidate_preserved
        and candidate_semantics_preserved
        and non_execution_boundary_ok
        and downstream_scope_ok
        and debt_recorded
        and closure_dryrun_only
    )

    dryrun_report = {
        "report_id": "task_manager_foundation_handoff_closure_dryrun_report_v1",
        "planning_final_decision": planning_summary.get("final_decision"),
        "planning_verifier": planning_verifier.get("verifier"),
        "closure_plan_integrity_ok": closure_plan_integrity_ok,
        "closure_evidence_traceability_ok": evidence_traceability_ok,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "closure_candidate_preserved": closure_candidate_preserved,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_scope_ok": downstream_scope_ok,
        "closure_channel_governance_debt_recorded": debt_recorded,
        "l1_closure_protocol_not_implemented": True,
        "closure_dryrun_only": closure_dryrun_only,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    plan_integrity_matrix = {
        "matrix_id": "task_manager_closure_plan_integrity_matrix_v1",
        "rows": integrity_rows,
        "closure_plan_integrity_ok": closure_plan_integrity_ok,
        **meta,
    }
    evidence_traceability_matrix = {
        "matrix_id": "task_manager_closure_evidence_traceability_matrix_v1",
        "rows": evidence_rows,
        "closure_evidence_traceability_ok": evidence_traceability_ok,
        **meta,
    }
    freeze_candidate_validation = {
        "validation_id": "task_manager_closure_freeze_candidate_validation_v1",
        "freeze_status": freeze_status,
        "closure_readiness": closure_readiness,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "closure_candidate_preserved": closure_candidate_preserved,
        "foundation_frozen": freeze_boundary.get("foundation_frozen"),
        "closure_applied": freeze_boundary.get("closure_applied"),
        **meta,
    }
    candidate_semantics_validation = {
        "validation_id": "task_manager_closure_candidate_semantics_validation_v1",
        "boundaries": list(CLOSURE_CHANNEL_BOUNDARIES),
        "candidate_semantics_preserved": candidate_semantics_preserved,
        **meta,
    }
    downstream_scope_validation = {
        "validation_id": "task_manager_closure_downstream_scope_validation_v1",
        "consumers": downstream_map.get("consumers") or [],
        "downstream_scope_ok": downstream_scope_ok,
        **meta,
    }
    non_execution_validation = {
        "validation_id": "task_manager_closure_non_execution_validation_v1",
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
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "closure_plan_integrity_ok": closure_plan_integrity_ok,
        "closure_evidence_traceability_ok": evidence_traceability_ok,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "closure_candidate_preserved": closure_candidate_preserved,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_scope_ok": downstream_scope_ok,
        "closure_channel_governance_debt_recorded": debt_recorded,
        "l1_closure_protocol_not_implemented": True,
        "closure_dryrun_only": closure_dryrun_only,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Closure DryRun Report v1",
            "",
            "This phase performs closure dry-run validation only. It does not execute closure, freeze the foundation, or implement L1 Closure Channel Governance.",
            "",
            "本阶段仅执行 closure dry-run validation，不执行 closure，不冻结 foundation，不实现 L1 Closure Channel Governance。",
            "",
            f"Planning GO: `{planning_go}`",
            f"Freeze status: `{freeze_status}` (not frozen)",
            f"Closure readiness: `{closure_readiness}` (not closed)",
            f"Governance debt recorded: `{debt_recorded}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Closure Channel Boundaries",
            *[f"- {item['boundary']}" for item in CLOSURE_CHANNEL_BOUNDARIES],
            "",
            "## Governance Debt",
            f"- {CLOSURE_GOVERNANCE_DEBT['debt_title']} (P1, future L1 protocol)",
        ]
    )
    return {
        "task_manager_foundation_handoff_closure_dryrun_report": dryrun_report,
        "task_manager_foundation_handoff_closure_dryrun_report_md": markdown,
        "task_manager_closure_plan_integrity_matrix": plan_integrity_matrix,
        "task_manager_closure_evidence_traceability_matrix": evidence_traceability_matrix,
        "task_manager_closure_freeze_candidate_validation": freeze_candidate_validation,
        "task_manager_closure_candidate_semantics_validation": candidate_semantics_validation,
        "task_manager_closure_downstream_scope_validation": downstream_scope_validation,
        "task_manager_closure_non_execution_validation": non_execution_validation,
        "task_manager_closure_governance_debt_register": governance_debt_register,
        "summary": summary,
    }
