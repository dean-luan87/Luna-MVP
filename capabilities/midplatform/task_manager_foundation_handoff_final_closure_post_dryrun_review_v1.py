# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Final Closure Post-DryRun Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_closure_dryrun_v1 import CLOSURE_CHANNEL_BOUNDARIES
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_dryrun_v1 import (
    CHAIN_TRACE_STAGES,
    DEFAULT_OUTPUT as DEFAULT_FINAL_CLOSURE_DRYRUN_ROOT,
    DRYRUN_BOUNDARY_STATEMENTS,
    FINAL_DECISION_GO as FINAL_CLOSURE_DRYRUN_FINAL_GO,
    GOVERNANCE_DEBTS,
    NEXT_PHASE_GO as FINAL_CLOSURE_DRYRUN_NEXT_PHASE,
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-Post-DryRun-Review-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_final_closure_post_dryrun_review_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_final_closure_post_dryrun_review_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_POST_DRYRUN_REVIEW_READY_FOR_FREEZE_AUTHORIZATION_PLANNING"
FINAL_DECISION_EVIDENCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_DRYRUN_EVIDENCE_GAP"
FINAL_DECISION_BOUNDARY = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_BOUNDARY_DRIFT"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_FREEZE_SCOPE_LEAKAGE"
FINAL_DECISION_STATE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_CLOSURE_STATE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-Post-DryRun-Review-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_final_closure_post_dryrun_review_v1_smoke_v0"
)

FINAL_CLOSURE_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_final_closure_dryrun_report_v1.json",
    "task_manager_foundation_handoff_final_closure_dryrun_report_v1.md",
    "task_manager_final_closure_plan_integrity_matrix_v1.json",
    "task_manager_final_closure_chain_traceability_matrix_v1.json",
    "task_manager_final_freeze_candidate_validation_v1.json",
    "task_manager_final_closure_boundary_validation_v1.json",
    "task_manager_final_downstream_reference_validation_v1.json",
    "task_manager_final_governance_debt_validation_v1.json",
    "task_manager_final_non_execution_validation_v1.json",
    "task_manager_final_closure_post_review_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)
DRYRUN_TRUE_KEYS: Tuple[str, ...] = (
    "final_closure_plan_integrity_ok",
    "final_chain_traceability_ok",
    "freeze_candidate_preserved",
    "closure_candidate_preserved",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_reference_scope_ok",
    "governance_debt_preserved",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
    "final_closure_dryrun_only",
    "post_review_readiness_ok",
)
CHAIN_EVIDENCE_NODES: Tuple[str, ...] = CHAIN_TRACE_STAGES + ("final_closure_dryrun",)
ALLOWED_DOWNSTREAM_READINESS: Tuple[str, ...] = (
    "reference-ready",
    "planning-reference-ready",
    "post-review-reference-ready",
    "authorization-planning-reference-ready",
)
FORBIDDEN_DOWNSTREAM: Tuple[str, ...] = (
    "implementation-ready",
    "runtime-ready",
    "production-ready",
    "module-adapter-ready",
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
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "final_closure_dryrun_root": str(dryrun),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_final_closure_post_dryrun_review_v1(
    *,
    final_closure_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(final_closure_dryrun_root).expanduser().resolve()
    meta = _meta(out, dryrun)
    issues: List[str] = []

    dryrun_summary = _read_json(dryrun / "summary.json")
    dryrun_verifier = _read_json(dryrun / "verifier_report.json")
    trace_matrix = _read_json(dryrun / "task_manager_final_closure_chain_traceability_matrix_v1.json")
    freeze_val = _read_json(dryrun / "task_manager_final_freeze_candidate_validation_v1.json")
    boundary_val = _read_json(dryrun / "task_manager_final_closure_boundary_validation_v1.json")
    downstream_val = _read_json(dryrun / "task_manager_final_downstream_reference_validation_v1.json")
    debt_val = _read_json(dryrun / "task_manager_final_governance_debt_validation_v1.json")
    non_exec = _read_json(dryrun / "task_manager_final_non_execution_validation_v1.json")

    review_rows = []
    for fname in FINAL_CLOSURE_DRYRUN_ARTIFACTS:
        path = dryrun / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        review_rows.append({"artifact": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_dryrun_artifact:{fname}")

    final_closure_dryrun_result_accepted = (
        dryrun_summary.get("final_decision") == FINAL_CLOSURE_DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == FINAL_CLOSURE_DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 420
        and dryrun_verifier.get("failed_checks") == 0
        and dryrun_verifier.get("blocker_count") == 0
        and all(dryrun_summary.get(k) is True for k in DRYRUN_TRUE_KEYS)
    )
    if not final_closure_dryrun_result_accepted:
        issues.append("final_closure_dryrun_not_accepted")

    boundary_drift_rows = []
    for fname in FINAL_CLOSURE_DRYRUN_ARTIFACTS:
        if not fname.endswith(".json"):
            continue
        doc = _read_json(dryrun / fname)
        runtime_leak = any(doc.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
        boundary_drift_rows.append(
            {"artifact": fname, "runtime_scope_leak_absent": not runtime_leak, "post_review_added_runtime": False}
        )
        if runtime_leak:
            issues.append(f"runtime_scope_leakage:{fname}")

    trace_rows = list(trace_matrix.get("rows") or [])
    chain_evidence = []
    for stage in CHAIN_EVIDENCE_NODES:
        if stage == "final_closure_dryrun":
            chain_evidence.append({"stage": stage, "linked": final_closure_dryrun_result_accepted})
        else:
            row = next((r for r in trace_rows if r.get("stage") == stage), {})
            chain_evidence.append({"stage": stage, "linked": row.get("linked") is True})
    final_chain_evidence_accepted = (
        final_closure_dryrun_result_accepted
        and all(node.get("linked") is True for node in chain_evidence)
    )
    if not final_chain_evidence_accepted:
        issues.append("chain_evidence_gap")

    freeze_status = freeze_val.get("freeze_status")
    freeze_candidate_preserved = (
        freeze_status == "freeze-candidate"
        and freeze_val.get("freeze_candidate_preserved") is True
        and freeze_val.get("foundation_frozen") is False
    )
    if freeze_status in ("frozen", "foundation-frozen", "production-ready"):
        freeze_candidate_preserved = False
    if not freeze_candidate_preserved:
        issues.append("freeze_candidate_drift")

    closure_readiness = "authorization-planning-ready"
    closure_candidate_preserved = (
        closure_readiness in ("final-closure-post-review-ready", "authorization-planning-ready")
        and freeze_val.get("closure_candidate_preserved") is True
        and freeze_val.get("closure_applied") is False
        and "closure_candidate != closed" in (boundary_val.get("statements") or [])
        and "final_closure_dryrun != closure_execution" in (boundary_val.get("statements") or [])
    )
    if closure_readiness in ("closed", "foundation-finalized"):
        closure_candidate_preserved = False
    if not closure_candidate_preserved:
        issues.append("closure_state_escalation")

    candidate_semantics_preserved = boundary_val.get("candidate_semantics_preserved") is True
    if not candidate_semantics_preserved:
        issues.append("candidate_semantics_drift")

    review_downstream = []
    downstream_reference_scope_ok = True
    for row in downstream_val.get("consumers") or []:
        readiness = row.get("readiness")
        if row.get("consumer") == "freeze_authorization_planning":
            readiness = "authorization-planning-reference-ready"
        review_downstream.append({**row, "readiness": readiness})
        if readiness not in ALLOWED_DOWNSTREAM_READINESS or readiness in FORBIDDEN_DOWNSTREAM:
            downstream_reference_scope_ok = False
    if not downstream_reference_scope_ok:
        issues.append("downstream_reference_escalation")

    debts = debt_val.get("debts") or []
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

    l1_protocols_not_implemented = debt_val.get("l1_protocols_not_implemented") is True
    system_protocols_integration_not_implemented = debt_val.get("system_protocols_integration_not_implemented") is True
    if not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        issues.append("l1_protocol_scope_leakage")

    non_execution_boundary_ok = non_exec.get("non_execution_boundary_ok") is True
    if not non_execution_boundary_ok:
        issues.append("runtime_scope_leakage")

    boundary_drift_absent = all(r["runtime_scope_leak_absent"] for r in boundary_drift_rows)
    authorization_planning_ready = (
        final_closure_dryrun_result_accepted
        and boundary_drift_absent
        and final_chain_evidence_accepted
        and governance_debt_preserved
        and l1_protocols_not_implemented
        and system_protocols_integration_not_implemented
        and freeze_candidate_preserved
        and closure_candidate_preserved
        and candidate_semantics_preserved
        and non_execution_boundary_ok
        and downstream_reference_scope_ok
    )

    if not final_closure_dryrun_result_accepted:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not boundary_drift_absent:
        final_decision = FINAL_DECISION_BOUNDARY
    elif not freeze_candidate_preserved:
        final_decision = FINAL_DECISION_FREEZE
    elif not closure_candidate_preserved:
        final_decision = FINAL_DECISION_STATE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    review_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO
    review_report = {
        "review_id": "task_manager_foundation_handoff_final_closure_post_dryrun_review_v1",
        "final_closure_dryrun_result_accepted": final_closure_dryrun_result_accepted,
        "boundary_drift_absent": boundary_drift_absent,
        "final_chain_evidence_accepted": final_chain_evidence_accepted,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "closure_candidate_preserved": closure_candidate_preserved,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_reference_scope_ok": downstream_reference_scope_ok,
        "post_review_only": True,
        "authorization_planning_ready": authorization_planning_ready,
        "closure_readiness": closure_readiness,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    dryrun_review_matrix = {
        "matrix_id": "task_manager_final_closure_dryrun_review_matrix_v1",
        "rows": review_rows,
        "final_closure_dryrun_result_accepted": final_closure_dryrun_result_accepted,
        **meta,
    }
    boundary_drift_review = {
        "review_id": "task_manager_final_closure_boundary_drift_review_v1",
        "rows": boundary_drift_rows,
        "boundary_drift_absent": boundary_drift_absent,
        "boundary_statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        **meta,
    }
    chain_evidence_review = {
        "review_id": "task_manager_final_closure_chain_evidence_review_v1",
        "chain": chain_evidence,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        "final_chain_evidence_accepted": final_chain_evidence_accepted,
        **meta,
    }
    freeze_candidate_review = {
        "review_id": "task_manager_final_freeze_candidate_review_v1",
        "freeze_status": freeze_status,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "foundation_frozen": False,
        **meta,
    }
    downstream_reference_review = {
        "review_id": "task_manager_final_downstream_reference_review_v1",
        "consumers": review_downstream,
        "allowed_readiness": list(ALLOWED_DOWNSTREAM_READINESS),
        "downstream_reference_scope_ok": downstream_reference_scope_ok,
        **meta,
    }
    governance_debt_review = {
        "review_id": "task_manager_final_governance_debt_review_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    authorization_planning_readiness = {
        "readiness_id": "task_manager_final_authorization_planning_readiness_v1",
        "authorization_planning_ready": authorization_planning_ready,
        "candidates": [
            {
                "phase": "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Planning-v1-001",
                "readiness": "freeze-authorization-planning-ready",
                "module_adapter_implementation": False,
                "foundation_frozen": False,
                "closed": False,
            },
            {
                "phase": "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-Authorization-Planning-v1-001",
                "readiness": "final-closure-authorization-planning-ready",
                "module_adapter_implementation": False,
                "foundation_frozen": False,
                "closed": False,
            },
        ],
        "module_adapter_implementation_ready": False,
        "foundation_frozen": False,
        "closed": False,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    review_non_execution = {
        "constraints_id": "task_manager_final_review_non_execution_constraints_v1",
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
        "no_system_protocols_integration_implementation": True,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "post_dryrun_review_pass": review_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "final_closure_dryrun_result_accepted": final_closure_dryrun_result_accepted,
        "boundary_drift_absent": boundary_drift_absent,
        "final_chain_evidence_accepted": final_chain_evidence_accepted,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "closure_candidate_preserved": closure_candidate_preserved,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_reference_scope_ok": downstream_reference_scope_ok,
        "post_review_only": True,
        "authorization_planning_ready": authorization_planning_ready,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Final Closure Post-DryRun Review v1",
            "",
            "This phase reviews final closure dry-run results only. It does not execute closure, freeze the foundation, or implement L1 protocol layers.",
            "",
            "本阶段仅审查 final closure dry-run 结果，不执行 closure，不冻结 foundation，不实现 L1 协议层。",
            "",
            f"Final closure dry-run accepted: `{final_closure_dryrun_result_accepted}`",
            f"Chain evidence accepted: `{final_chain_evidence_accepted}`",
            f"Governance debt preserved: `{governance_debt_preserved}`",
            f"Authorization planning ready: `{authorization_planning_ready}`",
            f"Freeze status preserved: `freeze-candidate` (not frozen)",
            f"Closure readiness: `authorization-planning-ready` (not closed)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Red Line Boundaries",
            *[f"- {stmt}" for stmt in DRYRUN_BOUNDARY_STATEMENTS[:4]],
            "",
            "## Closure Channel Boundaries",
            *[f"- {item['boundary']}" for item in CLOSURE_CHANNEL_BOUNDARIES[:5]],
            "",
            "## Governance Debts (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_final_closure_post_dryrun_review": review_report,
        "task_manager_foundation_handoff_final_closure_post_dryrun_review_md": markdown,
        "task_manager_final_closure_dryrun_review_matrix": dryrun_review_matrix,
        "task_manager_final_closure_boundary_drift_review": boundary_drift_review,
        "task_manager_final_closure_chain_evidence_review": chain_evidence_review,
        "task_manager_final_freeze_candidate_review": freeze_candidate_review,
        "task_manager_final_downstream_reference_review": downstream_reference_review,
        "task_manager_final_governance_debt_review": governance_debt_review,
        "task_manager_final_authorization_planning_readiness": authorization_planning_readiness,
        "task_manager_final_review_non_execution_constraints": review_non_execution,
        "summary": summary,
    }
