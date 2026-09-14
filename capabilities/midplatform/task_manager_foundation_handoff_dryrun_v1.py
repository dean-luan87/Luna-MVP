# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    FOUNDATION_ID,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Handoff-DryRun-v1-001"
SCOPE = "midplatform_task_manager_foundation_handoff_dryrun_validation_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_dryrun_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_MISSING_PACKAGE = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_DRYRUN_BLOCKED_BY_MISSING_PACKAGE"
FINAL_DECISION_EVIDENCE_GAP = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_DRYRUN_BLOCKED_BY_EVIDENCE_TRACE_GAP"
FINAL_DECISION_SEMANTICS = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_DRYRUN_BLOCKED_BY_CANDIDATE_SEMANTICS_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_DOWNSTREAM = "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_DRYRUN_BLOCKED_BY_DOWNSTREAM_SCOPE_ESCALATION"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Handoff-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Foundation-Handoff-DryRun-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_dryrun_v1_smoke_v0"
)

PLANNING_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_plan_v1.json",
    "task_manager_foundation_handoff_plan_v1.md",
    "task_manager_foundation_boundary_matrix_v1.json",
    "task_manager_candidate_lifecycle_matrix_v1.json",
    "task_manager_downstream_readiness_matrix_v1.json",
    "task_manager_non_execution_constraints_v1.json",
    "summary.json",
    "verifier_report.json",
)
JSON_PACKAGE_FILES: Tuple[str, ...] = tuple(name for name in PLANNING_PACKAGE_FILES if name.endswith(".json"))
FORBIDDEN_DOWNSTREAM_READINESS: Tuple[str, ...] = ("implementation-ready", "runtime-ready", "production-ready")
FORBIDDEN_STATUS_VALUES: Tuple[str, ...] = (
    "foundation_frozen",
    "foundation_finalized",
    "production_ready",
    "frozen",
    "finalized",
    "production-ready",
)
FORBIDDEN_BOUNDARY_TRUE_FLAGS: Tuple[str, ...] = (
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


def _meta(out: Path, planning: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "dryrun_only": True,
        "foundation_not_frozen": True,
        "output_root": str(out),
        "planning_root": str(planning),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def _has_forbidden_status(value: Any) -> bool:
    if isinstance(value, str):
        return value in FORBIDDEN_STATUS_VALUES
    if isinstance(value, dict):
        return any(_has_forbidden_status(v) for v in value.values())
    if isinstance(value, list):
        return any(_has_forbidden_status(v) for v in value)
    return False


def run_task_manager_foundation_handoff_dryrun_v1(
    *,
    planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(planning_root).expanduser().resolve()
    meta = _meta(out, planning)
    issues: List[str] = []

    docs = {name: _read_json(planning / name) for name in JSON_PACKAGE_FILES}
    markdown_path = planning / "task_manager_foundation_handoff_plan_v1.md"
    markdown = markdown_path.read_text(encoding="utf-8") if markdown_path.is_file() else ""

    package_integrity_rows = []
    for name in PLANNING_PACKAGE_FILES:
        path = planning / name
        if name.endswith(".json"):
            non_placeholder = bool(docs.get(name))
        else:
            non_placeholder = len(markdown.strip()) > 200
        row = {"file": name, "exists": path.is_file(), "non_placeholder": non_placeholder, "readable": path.is_file()}
        package_integrity_rows.append(row)
        if not row["exists"] or not row["non_placeholder"]:
            issues.append(f"missing_or_placeholder_package:{name}")

    planning_summary = docs.get("summary.json") or {}
    planning_verifier = docs.get("verifier_report.json") or {}
    if planning_summary.get("final_decision") != PLANNING_FINAL_GO:
        issues.append("planning_summary_not_go")
    if planning_verifier.get("verifier") != "GO":
        issues.append("planning_verifier_not_go")

    plan = docs.get("task_manager_foundation_handoff_plan_v1.json") or {}
    boundary = docs.get("task_manager_foundation_boundary_matrix_v1.json") or {}
    lifecycle = docs.get("task_manager_candidate_lifecycle_matrix_v1.json") or {}
    downstream = docs.get("task_manager_downstream_readiness_matrix_v1.json") or {}
    constraints = docs.get("task_manager_non_execution_constraints_v1.json") or {}
    evidence_map = plan.get("handoff_evidence_map") or {}

    evidence_rows = []
    for key in ("dryrun_summary", "dryrun_verifier", "post_dryrun_summary", "post_dryrun_verifier"):
        item = evidence_map.get(key) or {}
        row = {"evidence_key": key, "referenced": item.get("referenced") is True, "path": item.get("path", "")}
        evidence_rows.append(row)
        if not row["referenced"]:
            issues.append(f"evidence_trace_gap:{key}")
    for item in evidence_map.get("core_skeleton_files") or []:
        row = {
            "evidence_key": item.get("path"),
            "referenced": item.get("exists") is True,
            "role": item.get("role"),
        }
        evidence_rows.append(row)
        if not row["referenced"]:
            issues.append(f"evidence_trace_gap:{item.get('path')}")

    lifecycle_rows = lifecycle.get("candidate_semantics") or []
    task_candidate_ok = any(
        row.get("payload_type") == "task_candidate"
        and row.get("task_execution") is False
        and row.get("action_allowed") is False
        for row in lifecycle_rows
    )
    task_step_ok = any(
        row.get("payload_type") == "task_step_candidate"
        and row.get("executed_step") is False
        and row.get("action_allowed") is False
        for row in lifecycle_rows
    )
    handoff_ok = any(
        row.get("payload_type") == "task_handoff_candidate"
        and row.get("direct_mount") is False
        and row.get("direct_mount_allowed") is False
        for row in lifecycle_rows
    )
    candidate_semantics_preserved = task_candidate_ok and task_step_ok and handoff_ok and lifecycle.get("candidate_semantics_preserved") is True
    if not candidate_semantics_preserved:
        issues.append("candidate_semantics_drift")

    global_boundaries = boundary.get("global_boundaries") or {}
    non_execution_boundary_ok = all(global_boundaries.get(flag) is False for flag in FORBIDDEN_BOUNDARY_TRUE_FLAGS)
    if not non_execution_boundary_ok:
        issues.append("runtime_scope_leakage")

    downstream_rows = downstream.get("downstream") or []
    downstream_scope_ok = all(
        row.get("implementation_ready") == "false"
        and row.get("readiness") not in FORBIDDEN_DOWNSTREAM_READINESS
        for row in downstream_rows
    )
    future_protocol_dependency_ok = any(
        row.get("consumer") == "information_channel_governance"
        and row.get("readiness") == "future_l1_protocol_input"
        for row in downstream_rows
    ) and any(
        row.get("consumer") == "protocol_governance"
        and row.get("readiness") == "future_l1_protocol_dependency"
        for row in downstream_rows
    )
    if not downstream_scope_ok or not future_protocol_dependency_ok:
        issues.append("downstream_scope_escalation")

    constraints_ok = (
        constraints.get("no_runtime_executor") is True
        and constraints.get("no_scheduler_binding") is True
        and constraints.get("no_output_authorization") is True
        and constraints.get("no_memory_worldmodel_write_path") is True
        and constraints.get("no_module_adapter_integration") is True
        and constraints.get("no_authorization_claim") is True
    )
    if not constraints_ok:
        issues.append("non_execution_constraints_gap")

    foundation_not_frozen = not any(_has_forbidden_status(doc) for doc in docs.values())
    if not foundation_not_frozen:
        issues.append("foundation_status_escalation")

    handoff_package_integrity_ok = all(row["exists"] and row["non_placeholder"] for row in package_integrity_rows)
    evidence_traceability_ok = all(row["referenced"] for row in evidence_rows)
    dryrun_only = True

    if not handoff_package_integrity_ok:
        final_decision = FINAL_DECISION_MISSING_PACKAGE
    elif not evidence_traceability_ok:
        final_decision = FINAL_DECISION_EVIDENCE_GAP
    elif not candidate_semantics_preserved:
        final_decision = FINAL_DECISION_SEMANTICS
    elif not non_execution_boundary_ok or not constraints_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not downstream_scope_ok:
        final_decision = FINAL_DECISION_DOWNSTREAM
    else:
        final_decision = FINAL_DECISION_GO

    dryrun_pass = (
        final_decision == FINAL_DECISION_GO
        and len(issues) == 0
        and handoff_package_integrity_ok
        and evidence_traceability_ok
        and candidate_semantics_preserved
        and non_execution_boundary_ok
        and downstream_scope_ok
        and foundation_not_frozen
        and dryrun_only
    )
    handoff_package_integrity_matrix = {
        "matrix_id": "task_manager_handoff_package_integrity_matrix_v1",
        "rows": package_integrity_rows,
        "handoff_package_integrity_ok": handoff_package_integrity_ok,
        **meta,
    }
    evidence_traceability_matrix = {
        "matrix_id": "task_manager_handoff_evidence_traceability_matrix_v1",
        "rows": evidence_rows,
        "evidence_traceability_ok": evidence_traceability_ok,
        **meta,
    }
    downstream_consumption_dryrun_matrix = {
        "matrix_id": "task_manager_handoff_downstream_consumption_dryrun_matrix_v1",
        "rows": downstream_rows,
        "downstream_scope_ok": downstream_scope_ok,
        "future_protocol_dependency_ok": future_protocol_dependency_ok,
        "no_implementation_ready": True,
        "no_runtime_ready": True,
        "no_production_readiness": True,
        **meta,
    }
    non_execution_verification = {
        "verification_id": "task_manager_handoff_non_execution_verification_v1",
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "task_candidate_is_not_task_execution": task_candidate_ok,
        "task_step_candidate_is_not_executed_step": task_step_ok,
        "task_handoff_candidate_is_not_direct_mount": handoff_ok,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "constraints_ok": constraints_ok,
        "foundation_not_frozen": foundation_not_frozen,
        "dryrun_only": dryrun_only,
        "no_runtime_executor": True,
        "no_scheduler_binding": True,
        "no_task_execution_authority": True,
        "no_output_authorization": True,
        "no_memory_worldmodel_write_path": True,
        "no_module_adapter_integration": True,
        "no_authorization_grant": True,
        **meta,
    }
    dryrun_report = {
        "report_id": "task_manager_foundation_handoff_dryrun_report_v1",
        "planning_final_decision": planning_summary.get("final_decision"),
        "planning_verifier": planning_verifier.get("verifier"),
        "handoff_package_integrity_ok": handoff_package_integrity_ok,
        "evidence_traceability_ok": evidence_traceability_ok,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_scope_ok": downstream_scope_ok,
        "foundation_not_frozen": foundation_not_frozen,
        "dryrun_only": dryrun_only,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "handoff_package_integrity_ok": handoff_package_integrity_ok,
        "evidence_traceability_ok": evidence_traceability_ok,
        "candidate_semantics_preserved": candidate_semantics_preserved,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "downstream_scope_ok": downstream_scope_ok,
        "foundation_not_frozen": foundation_not_frozen,
        "dryrun_only": dryrun_only,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff DryRun Report v1",
            "",
            BOUNDARY_STATEMENT_EN,
            "",
            BOUNDARY_STATEMENT_ZH,
            "",
            f"Planning decision: `{planning_summary.get('final_decision')}`",
            f"Dry-run decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## DryRun Results",
            f"- handoff_package_integrity_ok: `{handoff_package_integrity_ok}`",
            f"- evidence_traceability_ok: `{evidence_traceability_ok}`",
            f"- candidate_semantics_preserved: `{candidate_semantics_preserved}`",
            f"- non_execution_boundary_ok: `{non_execution_boundary_ok}`",
            f"- downstream_scope_ok: `{downstream_scope_ok}`",
            f"- foundation_not_frozen: `{foundation_not_frozen}`",
            f"- dryrun_only: `{dryrun_only}`",
        ]
    )
    return {
        "task_manager_foundation_handoff_dryrun_report": dryrun_report,
        "task_manager_foundation_handoff_dryrun_report_md": markdown,
        "task_manager_handoff_package_integrity_matrix": handoff_package_integrity_matrix,
        "task_manager_handoff_evidence_traceability_matrix": evidence_traceability_matrix,
        "task_manager_handoff_downstream_consumption_dryrun_matrix": downstream_consumption_dryrun_matrix,
        "task_manager_handoff_non_execution_verification": non_execution_verification,
        "summary": summary,
    }
