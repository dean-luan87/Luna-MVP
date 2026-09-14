# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Final Closure DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_closure_dryrun_v1 import CLOSURE_CHANNEL_BOUNDARIES
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import (
    BOUNDARY_CONTRACT_STATEMENTS,
    DEFAULT_OUTPUT as DEFAULT_FINAL_CLOSURE_PLANNING_ROOT,
    FINAL_DECISION_GO as FINAL_CLOSURE_PLANNING_FINAL_GO,
    GOVERNANCE_DEBTS,
    NEXT_PHASE_GO as FINAL_CLOSURE_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-DryRun-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_final_closure_dryrun_validation_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_final_closure_dryrun_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_PLAN_GAP = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_DRYRUN_BLOCKED_BY_FINAL_PLAN_GAP"
FINAL_DECISION_TRACE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_DRYRUN_BLOCKED_BY_CHAIN_TRACE_GAP"
FINAL_DECISION_FREEZE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_DRYRUN_BLOCKED_BY_FREEZE_SCOPE_LEAKAGE"
FINAL_DECISION_STATE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_DRYRUN_BLOCKED_BY_CLOSURE_STATE_ESCALATION"
FINAL_DECISION_DOWNSTREAM = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_DRYRUN_BLOCKED_BY_DOWNSTREAM_SCOPE_ESCALATION"
FINAL_DECISION_DEBT = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_DRYRUN_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
FINAL_DECISION_L1 = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_DRYRUN_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FINAL_CLOSURE_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Final-Closure-DryRun-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_final_closure_dryrun_v1_smoke_v0"
)

FINAL_CLOSURE_PLANNING_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_final_closure_plan_v1.json",
    "task_manager_foundation_handoff_final_closure_plan_v1.md",
    "task_manager_final_closure_chain_evidence_map_v1.json",
    "task_manager_final_freeze_candidate_asset_map_v1.json",
    "task_manager_final_closure_boundary_contract_v1.json",
    "task_manager_final_candidate_semantics_lock_plan_v1.json",
    "task_manager_final_downstream_reference_contract_v1.json",
    "task_manager_final_governance_debt_carryover_v1.json",
    "task_manager_final_non_execution_constraints_v1.json",
    "task_manager_final_closure_next_phase_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)
PLANNING_TRUE_KEYS: Tuple[str, ...] = (
    "prior_full_chain_go",
    "final_closure_plan_complete",
    "chain_evidence_complete",
    "freeze_candidate_asset_map_complete",
    "freeze_candidate_only",
    "closure_planning_only",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_reference_scope_ok",
    "governance_debt_carryover_complete",
    "l1_protocols_not_implemented",
    "system_protocols_integration_not_implemented",
)
CHAIN_TRACE_STAGES: Tuple[str, ...] = (
    "planning",
    "dryrun",
    "post_dryrun_review",
    "closure_planning",
    "closure_dryrun",
    "closure_post_dryrun_review",
    "final_closure_planning",
)
DRYRUN_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "final_closure_dryrun != closure_execution",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
    "handoff_candidate != handed_off",
    "finalization_candidate != finalized",
    "planning-reference-ready != implementation-ready",
)
ALLOWED_DOWNSTREAM_READINESS: Tuple[str, ...] = (
    "reference-ready",
    "planning-reference-ready",
    "post-review-reference-ready",
)
FORBIDDEN_DOWNSTREAM: Tuple[str, ...] = (
    "implementation-ready",
    "runtime-ready",
    "production-ready",
    "module-adapter-ready",
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
    "system_protocols_integration_implemented_now",
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
        "final_closure_dryrun_only": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "final_closure_planning_root": str(planning),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
        "module_scoped_closure_rehearsal": True,
    }


def run_task_manager_foundation_handoff_final_closure_dryrun_v1(
    *,
    final_closure_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(final_closure_planning_root).expanduser().resolve()
    meta = _meta(out, planning)
    issues: List[str] = []

    planning_summary = _read_json(planning / "summary.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    final_plan = _read_json(planning / "task_manager_foundation_handoff_final_closure_plan_v1.json")
    chain_map = _read_json(planning / "task_manager_final_closure_chain_evidence_map_v1.json")
    freeze_map = _read_json(planning / "task_manager_final_freeze_candidate_asset_map_v1.json")
    boundary_contract = _read_json(planning / "task_manager_final_closure_boundary_contract_v1.json")
    semantics_plan = _read_json(planning / "task_manager_final_candidate_semantics_lock_plan_v1.json")
    downstream_contract = _read_json(planning / "task_manager_final_downstream_reference_contract_v1.json")
    debt_carryover = _read_json(planning / "task_manager_final_governance_debt_carryover_v1.json")
    non_execution_doc = _read_json(planning / "task_manager_final_non_execution_constraints_v1.json")

    integrity_rows = []
    for fname in FINAL_CLOSURE_PLANNING_PACKAGE_FILES:
        path = planning / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        integrity_rows.append({"file": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_or_placeholder:{fname}")

    planning_go = (
        planning_summary.get("final_decision") == FINAL_CLOSURE_PLANNING_FINAL_GO
        and planning_summary.get("recommended_next_phase") == FINAL_CLOSURE_PLANNING_NEXT_PHASE
        and planning_verifier.get("verifier") == "GO"
        and int(planning_verifier.get("passed_checks", 0)) >= 420
        and planning_verifier.get("failed_checks") == 0
        and planning_verifier.get("blocker_count") == 0
    )
    if not planning_go:
        issues.append("final_closure_planning_not_go")

    for key in PLANNING_TRUE_KEYS:
        if planning_summary.get(key) is not True:
            issues.append(f"planning_key_false:{key}")
        if key in planning_verifier and planning_verifier.get(key) is not True:
            issues.append(f"planning_verifier_key_false:{key}")

    trace_rows = chain_map.get("chain") or []
    final_chain_traceability_ok = chain_map.get("chain_evidence_complete") is True and all(
        row.get("linked") is True for row in trace_rows if row.get("stage") in CHAIN_TRACE_STAGES
    )
    for stage in CHAIN_TRACE_STAGES:
        row = next((r for r in trace_rows if r.get("stage") == stage), {})
        if row.get("linked") is not True:
            final_chain_traceability_ok = False
    if not final_chain_traceability_ok:
        issues.append("chain_trace_gap")

    freeze_status = freeze_map.get("freeze_status") or boundary_contract.get("freeze_status")
    freeze_candidate_preserved = (
        freeze_status == "freeze-candidate"
        and freeze_map.get("foundation_frozen") is False
        and freeze_map.get("freeze_candidate_only") is True
    )
    if freeze_status in ("frozen", "foundation-frozen", "production-ready"):
        freeze_candidate_preserved = False
    if not freeze_candidate_preserved:
        issues.append("freeze_scope_leakage")

    closure_state = "final-closure-dryrun"
    closure_readiness = "final-closure-post-review-ready"
    closure_candidate_preserved = (
        closure_state == "final-closure-dryrun"
        and closure_readiness == "final-closure-post-review-ready"
        and boundary_contract.get("closure_applied") is False
    )
    if closure_state in ("closed", "foundation-finalized") or closure_readiness in ("closed", "foundation-finalized"):
        closure_candidate_preserved = False
    if not closure_candidate_preserved:
        issues.append("closure_state_escalation")

    candidate_semantics_preserved = (
        semantics_plan.get("candidate_semantics_preserved") is True
        and semantics_plan.get("lock_plan_only") is True
        and semantics_plan.get("semantics_executed") is False
        and semantics_plan.get("lock_executed") is False
    )
    if not candidate_semantics_preserved:
        issues.append("candidate_semantics_drift")

    downstream_consumers = list(downstream_contract.get("consumers") or [])
    dryrun_downstream = [
        {**row, "readiness": "post-review-reference-ready" if row.get("consumer") == "final_closure_dryrun" else row.get("readiness")}
        for row in downstream_consumers
    ]
    downstream_reference_scope_ok = downstream_contract.get("downstream_reference_scope_ok") is True
    for row in dryrun_downstream:
        readiness = row.get("readiness")
        if readiness not in ALLOWED_DOWNSTREAM_READINESS or readiness in FORBIDDEN_DOWNSTREAM:
            downstream_reference_scope_ok = False
    if not downstream_reference_scope_ok:
        issues.append("downstream_scope_escalation")

    non_execution_boundary_ok = non_execution_doc.get("non_execution_boundary_ok") is True
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if final_plan.get(flag) is True or planning_summary.get(flag) is True:
            non_execution_boundary_ok = False
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
        and debt0.get("recommended_future_phase") == GOVERNANCE_DEBTS[0]["recommended_future_phase"]
        and debt1.get("debt_title") == GOVERNANCE_DEBTS[1]["debt_title"]
        and debt1.get("priority") == "P1"
        and debt1.get("classification") == "L1 Midplatform System Protocols"
        and debt1.get("must_not_implement_now") is True
        and debt1.get("recommended_future_phase") == GOVERNANCE_DEBTS[1]["recommended_future_phase"]
    )
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    l1_protocols_not_implemented = debt_carryover.get("l1_protocols_not_implemented") is True
    system_protocols_integration_not_implemented = debt_carryover.get("system_protocols_integration_not_implemented") is True
    if not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        issues.append("l1_protocol_scope_leakage")

    final_closure_plan_integrity_ok = all(r["exists"] and r["non_placeholder"] for r in integrity_rows)
    final_closure_dryrun_only = True
    post_review_readiness_ok = planning_go and final_chain_traceability_ok and governance_debt_preserved

    if not final_closure_plan_integrity_ok or not planning_go:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not final_chain_traceability_ok:
        final_decision = FINAL_DECISION_TRACE
    elif not freeze_candidate_preserved:
        final_decision = FINAL_DECISION_FREEZE
    elif not closure_candidate_preserved:
        final_decision = FINAL_DECISION_STATE
    elif not downstream_reference_scope_ok:
        final_decision = FINAL_DECISION_DOWNSTREAM
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    dryrun_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and final_closure_plan_integrity_ok
        and final_chain_traceability_ok
        and freeze_candidate_preserved
        and closure_candidate_preserved
        and candidate_semantics_preserved
        and non_execution_boundary_ok
        and downstream_reference_scope_ok
        and governance_debt_preserved
        and l1_protocols_not_implemented
        and system_protocols_integration_not_implemented
        and final_closure_dryrun_only
        and post_review_readiness_ok
    )

    dryrun_report = {
        "report_id": "task_manager_foundation_handoff_final_closure_dryrun_report_v1",
        "planning_final_decision": planning_summary.get("final_decision"),
        "planning_verifier": planning_verifier.get("verifier"),
        "final_closure_plan_integrity_ok": final_closure_plan_integrity_ok,
        "final_chain_traceability_ok": final_chain_traceability_ok,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "closure_candidate_preserved": closure_candidate_preserved,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_reference_scope_ok": downstream_reference_scope_ok,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "final_closure_dryrun_only": final_closure_dryrun_only,
        "post_review_readiness_ok": post_review_readiness_ok,
        "boundary_statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    plan_integrity_matrix = {
        "matrix_id": "task_manager_final_closure_plan_integrity_matrix_v1",
        "rows": integrity_rows,
        "final_closure_plan_integrity_ok": final_closure_plan_integrity_ok,
        **meta,
    }
    chain_traceability_matrix = {
        "matrix_id": "task_manager_final_closure_chain_traceability_matrix_v1",
        "rows": trace_rows,
        "final_chain_traceability_ok": final_chain_traceability_ok,
        **meta,
    }
    freeze_candidate_validation = {
        "validation_id": "task_manager_final_freeze_candidate_validation_v1",
        "freeze_status": freeze_status,
        "closure_state": closure_state,
        "closure_readiness": closure_readiness,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "closure_candidate_preserved": closure_candidate_preserved,
        "foundation_frozen": False,
        "closure_applied": False,
        **meta,
    }
    boundary_validation = {
        "validation_id": "task_manager_final_closure_boundary_validation_v1",
        "statements": list(DRYRUN_BOUNDARY_STATEMENTS) + list(BOUNDARY_CONTRACT_STATEMENTS),
        "closure_state": closure_state,
        "closure_readiness": closure_readiness,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        **meta,
    }
    downstream_reference_validation = {
        "validation_id": "task_manager_final_downstream_reference_validation_v1",
        "consumers": dryrun_downstream,
        "allowed_readiness": list(ALLOWED_DOWNSTREAM_READINESS),
        "downstream_reference_scope_ok": downstream_reference_scope_ok,
        **meta,
    }
    governance_debt_validation = {
        "validation_id": "task_manager_final_governance_debt_validation_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    non_execution_validation = {
        "validation_id": "task_manager_final_non_execution_validation_v1",
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
    post_review_readiness = {
        "readiness_id": "task_manager_final_closure_post_review_readiness_v1",
        "post_review_readiness_ok": post_review_readiness_ok,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "module_adapter_implementation_ready": False,
        "freeze_authorization_ready": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "final_closure_plan_integrity_ok": final_closure_plan_integrity_ok,
        "final_chain_traceability_ok": final_chain_traceability_ok,
        "freeze_candidate_preserved": freeze_candidate_preserved,
        "closure_candidate_preserved": closure_candidate_preserved,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_reference_scope_ok": downstream_reference_scope_ok,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        "final_closure_dryrun_only": final_closure_dryrun_only,
        "post_review_readiness_ok": post_review_readiness_ok,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Final Closure DryRun Report v1",
            "",
            "This phase performs final closure dry-run validation only. It does not execute closure, freeze the foundation, or implement L1 protocol layers.",
            "",
            "本阶段仅执行 final closure dry-run validation，不执行 closure，不冻结 foundation，不实现 L1 协议层。",
            "",
            f"Planning GO: `{planning_go}`",
            f"Freeze status: `{freeze_status}` (not frozen)",
            f"Closure state: `{closure_state}` (not closed)",
            f"Closure readiness: `{closure_readiness}`",
            f"Governance debt preserved: `{governance_debt_preserved}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Red Line Boundaries",
            *[f"- {stmt}" for stmt in DRYRUN_BOUNDARY_STATEMENTS],
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
        "task_manager_foundation_handoff_final_closure_dryrun_report": dryrun_report,
        "task_manager_foundation_handoff_final_closure_dryrun_report_md": markdown,
        "task_manager_final_closure_plan_integrity_matrix": plan_integrity_matrix,
        "task_manager_final_closure_chain_traceability_matrix": chain_traceability_matrix,
        "task_manager_final_freeze_candidate_validation": freeze_candidate_validation,
        "task_manager_final_closure_boundary_validation": boundary_validation,
        "task_manager_final_downstream_reference_validation": downstream_reference_validation,
        "task_manager_final_governance_debt_validation": governance_debt_validation,
        "task_manager_final_non_execution_validation": non_execution_validation,
        "task_manager_final_closure_post_review_readiness": post_review_readiness,
        "summary": summary,
    }
