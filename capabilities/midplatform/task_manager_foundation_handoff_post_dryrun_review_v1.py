# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Post-DryRun Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Post-DryRun-Review-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_post_dryrun_review_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_post_dryrun_review_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE_PLANNING"
FINAL_DECISION_EVIDENCE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_POST_DRYRUN_REVIEW_BLOCKED_BY_DRYRUN_EVIDENCE_GAP"
FINAL_DECISION_BOUNDARY = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_POST_DRYRUN_REVIEW_BLOCKED_BY_BOUNDARY_DRIFT"
FINAL_DECISION_SEMANTICS = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_POST_DRYRUN_REVIEW_BLOCKED_BY_CANDIDATE_SEMANTICS_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_POST_DRYRUN_REVIEW_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_DOWNSTREAM = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_POST_DRYRUN_REVIEW_BLOCKED_BY_DOWNSTREAM_SCOPE_ESCALATION"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Closure-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Post-DryRun-Review-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_post_dryrun_review_v1_smoke_v0"
)

DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_dryrun_report_v1.json",
    "task_manager_foundation_handoff_dryrun_report_v1.md",
    "task_manager_handoff_package_integrity_matrix_v1.json",
    "task_manager_handoff_evidence_traceability_matrix_v1.json",
    "task_manager_handoff_downstream_consumption_dryrun_matrix_v1.json",
    "task_manager_handoff_non_execution_verification_v1.json",
    "summary.json",
    "verifier_report.json",
)
JSON_DRYRUN_ARTIFACTS: Tuple[str, ...] = tuple(name for name in DRYRUN_ARTIFACTS if name.endswith(".json"))
REQUIRED_TRUE_KEYS: Tuple[str, ...] = (
    "handoff_package_integrity_ok",
    "evidence_traceability_ok",
    "candidate_semantics_preserved",
    "non_execution_boundary_ok",
    "downstream_scope_ok",
    "foundation_not_frozen",
    "dryrun_only",
)
FORBIDDEN_STATUS_VALUES: Tuple[str, ...] = (
    "implementation-ready",
    "runtime-ready",
    "production-ready",
    "foundation_frozen",
    "foundation_finalized",
    "production_ready",
    "closed",
    "foundation-frozen",
)
FORBIDDEN_RUNTIME_FLAGS: Tuple[str, ...] = (
    "runtime_executor_created_now",
    "scheduler_binding_created_now",
    "task_execution_authority_granted_now",
    "output_authorization_granted_now",
    "module_adapter_integration_created_now",
    "information_channel_governance_implemented_now",
    "protocol_governance_implemented_now",
    "task_execution_now",
    "tool_call_now",
    "runtime_enabled_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "output_gate_mounted_now",
    "module_adapter_mounted_now",
    "real_scheduler_enabled_now",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _has_forbidden_status(value: Any) -> bool:
    if isinstance(value, str):
        return value in FORBIDDEN_STATUS_VALUES
    if isinstance(value, dict):
        return any(_has_forbidden_status(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_forbidden_status(v) for v in value)
    return False


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
        "output_root": str(out),
        "dryrun_root": str(dryrun),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_post_dryrun_review_v1(
    *,
    dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(dryrun_root).expanduser().resolve()
    meta = _meta(out, dryrun)
    issues: List[str] = []
    docs = {name: _read_json(dryrun / name) for name in JSON_DRYRUN_ARTIFACTS}
    md_path = dryrun / "task_manager_foundation_handoff_dryrun_report_v1.md"
    md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    dryrun_review_rows = []
    for name in DRYRUN_ARTIFACTS:
        path = dryrun / name
        non_placeholder = bool(docs.get(name)) if name.endswith(".json") else len(md.strip()) > 200
        row = {"artifact": name, "exists": path.is_file(), "non_placeholder": non_placeholder}
        dryrun_review_rows.append(row)
        if not row["exists"] or not row["non_placeholder"]:
            issues.append(f"missing_or_placeholder_dryrun_artifact:{name}")

    dryrun_summary = docs.get("summary.json") or {}
    dryrun_verifier = docs.get("verifier_report.json") or {}
    dryrun_result_accepted = (
        dryrun_summary.get("final_decision") == DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 420
        and dryrun_verifier.get("failed_checks") == 0
        and dryrun_verifier.get("blocker_count") == 0
        and all(dryrun_summary.get(key) is True for key in REQUIRED_TRUE_KEYS)
    )
    if not dryrun_result_accepted:
        issues.append("dryrun_result_not_accepted")

    boundary_drift_rows = []
    for name, doc in docs.items():
        forbidden_status = _has_forbidden_status(doc)
        runtime_leak = any(doc.get(flag) is True for flag in FORBIDDEN_RUNTIME_FLAGS)
        row = {
            "artifact": name,
            "forbidden_status_absent": not forbidden_status,
            "runtime_scope_leak_absent": not runtime_leak,
            "post_review_added_runtime": False,
        }
        boundary_drift_rows.append(row)
        if forbidden_status:
            issues.append(f"forbidden_status_detected:{name}")
        if runtime_leak:
            issues.append(f"runtime_scope_leakage:{name}")

    non_execution = docs.get("task_manager_handoff_non_execution_verification_v1.json") or {}
    candidate_semantics_preserved = (
        non_execution.get("candidate_semantics_preserved") is True
        and non_execution.get("task_candidate_is_not_task_execution") is True
        and non_execution.get("task_step_candidate_is_not_executed_step") is True
        and non_execution.get("task_handoff_candidate_is_not_direct_mount") is True
    )
    if not candidate_semantics_preserved:
        issues.append("candidate_semantics_drift")

    downstream_matrix = docs.get("task_manager_handoff_downstream_consumption_dryrun_matrix_v1.json") or {}
    downstream_scope_ok = downstream_matrix.get("downstream_scope_ok") is True and not _has_forbidden_status(
        downstream_matrix.get("rows") or []
    )
    if not downstream_scope_ok:
        issues.append("downstream_scope_escalation")

    non_execution_boundary_ok = (
        non_execution.get("non_execution_boundary_ok") is True
        and non_execution.get("no_runtime_executor") is True
        and non_execution.get("no_scheduler_binding") is True
        and non_execution.get("no_task_execution_authority") is True
        and non_execution.get("no_output_authorization") is True
        and non_execution.get("no_memory_worldmodel_write_path") is True
        and non_execution.get("no_module_adapter_integration") is True
        and non_execution.get("no_authorization_grant") is True
    )
    if not non_execution_boundary_ok:
        issues.append("runtime_scope_leakage")

    foundation_not_frozen = dryrun_summary.get("foundation_not_frozen") is True and not _has_forbidden_status(docs)
    if not foundation_not_frozen:
        issues.append("foundation_freeze_or_closure_escalation")

    evidence_doc = docs.get("task_manager_handoff_evidence_traceability_matrix_v1.json") or {}
    evidence_chain_rows = evidence_doc.get("rows") or []
    evidence_chain_ok = evidence_doc.get("evidence_traceability_ok") is True and all(row.get("referenced") is True for row in evidence_chain_rows)
    if not evidence_chain_ok:
        issues.append("dryrun_evidence_gap")

    boundary_drift_absent = all(row["forbidden_status_absent"] and row["runtime_scope_leak_absent"] for row in boundary_drift_rows)
    closure_planning_ready = (
        dryrun_result_accepted
        and boundary_drift_absent
        and candidate_semantics_preserved
        and non_execution_boundary_ok
        and downstream_scope_ok
        and foundation_not_frozen
    )

    closure_readiness_rows = [
        {"target": "foundation_handoff_closure_planning", "readiness": "closure-planning-ready", "closed": False, "foundation_freeze_applied": False},
        {"target": "freeze_planning", "readiness": "closure-planning-ready", "closed": False, "foundation_freeze_applied": False},
        {"target": "module_adapter_implementation", "readiness": "not-ready", "closed": False, "foundation_freeze_applied": False},
    ]

    if "dryrun_result_not_accepted" in issues or "dryrun_evidence_gap" in issues:
        final_decision = FINAL_DECISION_EVIDENCE
    elif any(issue.startswith("forbidden_status") for issue in issues) or "foundation_freeze_or_closure_escalation" in issues:
        final_decision = FINAL_DECISION_BOUNDARY
    elif "candidate_semantics_drift" in issues:
        final_decision = FINAL_DECISION_SEMANTICS
    elif "runtime_scope_leakage" in issues:
        final_decision = FINAL_DECISION_RUNTIME
    elif "downstream_scope_escalation" in issues:
        final_decision = FINAL_DECISION_DOWNSTREAM
    else:
        final_decision = FINAL_DECISION_GO

    review_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO
    review_report = {
        "review_id": "task_manager_foundation_handoff_post_dryrun_review_v1",
        "dryrun_result_accepted": dryrun_result_accepted,
        "boundary_drift_absent": boundary_drift_absent,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_scope_ok": downstream_scope_ok,
        "foundation_not_frozen": foundation_not_frozen,
        "post_review_only": True,
        "closure_planning_ready": closure_planning_ready,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    dryrun_review_matrix = {
        "matrix_id": "task_manager_handoff_dryrun_review_matrix_v1",
        "rows": dryrun_review_rows,
        "dryrun_result_accepted": dryrun_result_accepted,
        **meta,
    }
    boundary_drift_review = {
        "review_id": "task_manager_handoff_boundary_drift_review_v1",
        "rows": boundary_drift_rows,
        "boundary_drift_absent": boundary_drift_absent,
        "foundation_not_frozen": foundation_not_frozen,
        **meta,
    }
    evidence_chain_review = {
        "review_id": "task_manager_handoff_evidence_chain_review_v1",
        "rows": evidence_chain_rows,
        "evidence_chain_ok": evidence_chain_ok,
        **meta,
    }
    closure_readiness_matrix = {
        "matrix_id": "task_manager_handoff_closure_readiness_matrix_v1",
        "rows": closure_readiness_rows,
        "closure_planning_ready": closure_planning_ready,
        "closed": False,
        "foundation_freeze_applied": False,
        **meta,
    }
    review_non_execution_constraints = {
        "constraints_id": "task_manager_handoff_review_non_execution_constraints_v1",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "no_runtime_executor": True,
        "no_scheduler_binding": True,
        "no_task_execution_authority": True,
        "no_output_authorization": True,
        "no_memory_worldmodel_write_path": True,
        "no_module_adapter_integration": True,
        "no_information_channel_governance_implementation": True,
        "no_protocol_governance_implementation": True,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "post_dryrun_review_pass": review_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "dryrun_result_accepted": dryrun_result_accepted,
        "boundary_drift_absent": boundary_drift_absent,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_scope_ok": downstream_scope_ok,
        "foundation_not_frozen": foundation_not_frozen,
        "post_review_only": True,
        "closure_planning_ready": closure_planning_ready,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if review_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Post-DryRun Review v1",
            "",
            BOUNDARY_STATEMENT_EN,
            "",
            BOUNDARY_STATEMENT_ZH,
            "",
            f"Dry-run accepted: `{dryrun_result_accepted}`",
            f"Boundary drift absent: `{boundary_drift_absent}`",
            f"Closure planning ready: `{closure_planning_ready}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "This review does not close, freeze, or execute the handoff.",
        ]
    )
    return {
        "task_manager_foundation_handoff_post_dryrun_review": review_report,
        "task_manager_foundation_handoff_post_dryrun_review_md": markdown,
        "task_manager_handoff_dryrun_review_matrix": dryrun_review_matrix,
        "task_manager_handoff_boundary_drift_review": boundary_drift_review,
        "task_manager_handoff_evidence_chain_review": evidence_chain_review,
        "task_manager_handoff_closure_readiness_matrix": closure_readiness_matrix,
        "task_manager_handoff_review_non_execution_constraints": review_non_execution_constraints,
        "summary": summary,
    }
