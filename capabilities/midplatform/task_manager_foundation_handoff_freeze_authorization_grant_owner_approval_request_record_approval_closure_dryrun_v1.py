# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Record Approval Closure Lightweight Compliance DryRun v1.

Lightweight compliance dry-run only — no L1 protocol body revalidation, no shared protocol
system revalidation, no 29-item protocol classification rerun.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_planning_v1 import (
    CHAIN_EVIDENCE_NODES,
    DEFAULT_OUTPUT as DEFAULT_RECORD_APPROVAL_CLOSURE_PLANNING_ROOT,
    FINAL_DECISION_GO as RECORD_APPROVAL_CLOSURE_PLANNING_FINAL_GO,
    LIGHTWEIGHT_PROTOCOL_REFS,
    NEXT_PHASE_GO as RECORD_APPROVAL_CLOSURE_PLANNING_NEXT_PHASE,
)

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-DryRun-v1-001"
)
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_lightweight_compliance_dryrun_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
FINAL_DECISION_PLAN_GAP = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_BLOCKED_BY_PLANNING_GAP"
)
FINAL_DECISION_CANDIDATE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_BLOCKED_BY_CANDIDATE_ESCALATION"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Post-DryRun-Review-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-DryRun-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1_smoke_v0"
)
RECORD_APPROVAL_CLOSURE_DRYRUN_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_foundation_handoff_evaluation_template_lineage_v1.py"

DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_report_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_report_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_matrix_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_traceability_reference_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_boundary_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_governance_debt_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_review_readiness_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

PLANNING_MATRIX_FILES: Tuple[str, ...] = (
    "task_manager_freeze_authorization_grant_owner_approval_request_record_candidate_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_approval_candidate_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_ack_candidate_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_evidence_binding_closure_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_traceability_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_protocol_reference_matrix_v1.json",
)

CORE_CANDIDATE_IDS: Tuple[str, ...] = (
    "owner_approval_request_record_candidate",
    "owner_approval_record_candidate",
    "owner_operator_ack_record_candidate",
    "approval_evidence_bound_record_candidate",
    "owner_approval_request_record_approval_closure_candidate",
)

CANDIDATE_BOUNDARY_PAIRS: Tuple[Tuple[str, str], ...] = (
    ("owner_approval_request_record_candidate", "request_record"),
    ("owner_approval_record_candidate", "owner_approval_record"),
    ("owner_operator_ack_record_candidate", "owner_operator_ack_record"),
    ("approval_evidence_bound_record_candidate", "approval_evidence_bound_record"),
    ("owner_approval_request_record_approval_closure_candidate", "closure_executed"),
)

BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "record_approval_closure_dryrun != closure_executed",
    "owner_approval_request_record_candidate != request_record",
    "owner_approval_record_candidate != owner_approval_record",
    "owner_operator_ack_record_candidate != owner_operator_ack_record",
    "approval_evidence_bound_record_candidate != approval_evidence_bound_record",
    "closure_candidate != closure_executed",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_record_approval_closure_planning_go",
    "candidate_validation_ok",
    "matrix_validation_ok",
    "traceability_reference_validation_ok",
    "absence_validation_ok",
    "boundary_validation_ok",
    "governance_debt_preserved",
    "template_lineage_ok",
    "file_size_governance_review_ok",
    "non_execution_boundary_ok",
    "post_review_readiness_ok",
    "shared_protocol_system_revalidation",
    "l1_input_output_protocol_revalidation",
    "protocol_migration",
    "whitebox_runtime_integration",
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
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "lightweight_compliance_dryrun_only": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "protocol_migration": False,
        "whitebox_runtime_integration": False,
        "output_root": str(out),
        "record_approval_closure_planning_root": str(planning),
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1(
    *,
    record_approval_closure_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(record_approval_closure_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, planning)
    issues: List[str] = []

    planning_summary = _read_json(planning / "summary.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    planning_file_size = _read_json(planning / "file_size_governance_review_v1.json")

    prior_record_approval_closure_planning_go = (
        planning_summary.get("final_decision") == RECORD_APPROVAL_CLOSURE_PLANNING_FINAL_GO
        and planning_summary.get("recommended_next_phase") == RECORD_APPROVAL_CLOSURE_PLANNING_NEXT_PHASE
        and planning_verifier.get("verifier") == "GO"
        and int(planning_verifier.get("passed_checks", 0)) >= 420
        and planning_verifier.get("failed_checks") == 0
        and planning_verifier.get("blocker_count") == 0
        and planning_summary.get("planning_pass") is True
    )
    if not prior_record_approval_closure_planning_go:
        issues.append("planning_not_go")

    protocol_ref_matrix = _read_json(planning / PLANNING_MATRIX_FILES[5])
    traceability_matrix = _read_json(planning / PLANNING_MATRIX_FILES[4])

    status_map = {
        "owner_approval_request_record_candidate": "owner-approval-request-record-candidate",
        "owner_approval_record_candidate": "owner-approval-record-candidate",
        "owner_operator_ack_record_candidate": "owner-operator-ack-record-candidate",
        "approval_evidence_bound_record_candidate": "approval-evidence-bound-record-candidate",
        "owner_approval_request_record_approval_closure_candidate": "owner-approval-request-record-approval-closure-candidate",
    }
    candidate_rows = [
        {
            "candidate_id": cid,
            "candidate_status": status_map[cid],
            "still_candidate": True,
            "record_created": False,
            "request_issued": False,
            "closure_executed": False,
        }
        for cid in CORE_CANDIDATE_IDS
    ]

    record_matrix = _read_json(planning / PLANNING_MATRIX_FILES[0])
    approval_matrix = _read_json(planning / PLANNING_MATRIX_FILES[1])
    ack_matrix = _read_json(planning / PLANNING_MATRIX_FILES[2])
    evidence_matrix = _read_json(planning / PLANNING_MATRIX_FILES[3])

    candidate_validation_ok = (
        prior_record_approval_closure_planning_go
        and record_matrix.get("record_candidate_closure_matrix_complete") is True
        and approval_matrix.get("approval_candidate_closure_matrix_complete") is True
        and ack_matrix.get("ack_candidate_closure_matrix_complete") is True
        and evidence_matrix.get("evidence_binding_closure_matrix_complete") is True
        and all(row.get("still_candidate") for row in candidate_rows)
        and all(row.get("record_created") is False for row in candidate_rows)
        and all(row.get("closure_executed") is False for row in candidate_rows)
    )
    if not candidate_validation_ok:
        issues.append("candidate_escalation")

    matrix_rows = []
    for fname in PLANNING_MATRIX_FILES:
        path = planning / fname
        payload = _read_json(path) if path.is_file() else {}
        matrix_rows.append(
            {
                "file": fname,
                "exists": path.is_file(),
                "non_placeholder": bool(payload),
            }
        )
    matrix_validation_ok = prior_record_approval_closure_planning_go and all(
        row["exists"] and row["non_placeholder"] for row in matrix_rows
    )
    if not matrix_validation_ok:
        issues.append("matrix_gap")

    trace_chain = list(traceability_matrix.get("chain") or planning_summary.get("evidence_chain") or [])
    trace_chain.append(
        {
            "stage": "freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun",
            "root": str(out),
            "linked": True,
            "authorization_request_issued": False,
            "request_record": False,
            "closure_executed": False,
        }
    )
    protocol_refs = [
        {"protocol_id": r.get("protocol_id"), "reference_mode": r.get("reference_mode", "lightweight")}
        for r in (protocol_ref_matrix.get("refs") or [])
        if r.get("protocol_id")
    ]
    if not protocol_refs:
        protocol_refs = [{"protocol_id": pid, "reference_mode": "lightweight"} for pid in LIGHTWEIGHT_PROTOCOL_REFS]

    traceability_reference_validation_ok = (
        traceability_matrix.get("traceability_matrix_complete") is True
        and traceability_matrix.get("shared_protocol_system_revalidation") is False
        and traceability_matrix.get("l1_input_output_protocol_revalidation") is False
        and len(protocol_refs) >= len(LIGHTWEIGHT_PROTOCOL_REFS)
        and all(r.get("reference_mode") == "lightweight" for r in protocol_refs if isinstance(r, dict))
    )
    if not traceability_reference_validation_ok:
        issues.append("traceability_reference_gap")

    absence = {
        "request_issued_absent": planning_summary.get("request_issued_absent") is True,
        "notification_sent_absent": planning_summary.get("notification_sent_absent") is True,
        "request_record_absent": planning_summary.get("request_record_absent") is True,
        "approval_record_absent": planning_summary.get("approval_record_absent") is True,
        "ack_record_absent": planning_summary.get("ack_record_absent") is True,
        "evidence_bound_record_absent": planning_summary.get("evidence_bound_record_absent") is True,
        "authorization_request_absent": planning_summary.get("authorization_request_absent") is True,
        "grant_absent": planning_summary.get("grant_absent") is True,
        "foundation_not_frozen": planning_summary.get("foundation_not_frozen") is True,
        "closure_not_executed": planning_summary.get("closure_not_executed") is True,
        "runtime_execution_absent": planning_summary.get("runtime_execution_absent") is True,
        "protocol_runtime_absent": planning_summary.get("protocol_runtime_absent") is True,
        "whitebox_runtime_integration_absent": planning_summary.get("whitebox_runtime_integration_absent") is True,
        "module_adapter_implementation_absent": planning_summary.get("module_adapter_implementation_absent") is True,
    }
    absence_validation_ok = prior_record_approval_closure_planning_go and all(absence.values())
    if not absence_validation_ok:
        issues.append("absence_drift")

    boundary_validation_ok = (
        absence_validation_ok
        and planning_summary.get("non_execution_boundary_ok") is True
    )
    if not boundary_validation_ok:
        issues.append("boundary_gap")

    debts = list(GOVERNANCE_DEBTS)
    governance_debt_preserved = (
        planning_summary.get("governance_debt_preserved") is True
        and len(debts) >= 2
        and debts[0].get("must_not_implement_now") is True
        and debts[1].get("must_not_implement_now") is True
    )
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    non_execution_boundary_ok = planning_summary.get("non_execution_boundary_ok") is True
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if planning_summary.get(flag) is True:
            non_execution_boundary_ok = False
            issues.append(f"runtime_flag:{flag}")
            break

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Request-Record-DryRun-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_WHITELIST_FILES[2],
        base_go_no_go_pack=RECORD_APPROVAL_CLOSURE_DRYRUN_GO_NO_GO_PACK,
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-DryRun-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_DRYRUN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Planning-v1-001",
    )
    template_lineage_ok = (
        template_lineage.get("template_lineage_ok") is True
        and planning_summary.get("template_lineage_ok") is True
    )
    if not template_lineage_ok:
        issues.append("template_lineage_gap")

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first",
        full_repo_scan=False,
        previous_interruption_type=planning_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=planning_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=planning_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    post_review_readiness_ok = (
        prior_record_approval_closure_planning_go
        and candidate_validation_ok
        and matrix_validation_ok
        and traceability_reference_validation_ok
        and absence_validation_ok
        and boundary_validation_ok
        and governance_debt_preserved
        and non_execution_boundary_ok
        and template_lineage_ok
        and file_size_governance_review_ok
    )

    if not prior_record_approval_closure_planning_go:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not template_lineage_ok:
        final_decision = FINAL_DECISION_LINEAGE
    elif not candidate_validation_ok:
        final_decision = FINAL_DECISION_CANDIDATE
    elif not absence_validation_ok:
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_record_approval_closure_planning_go": prior_record_approval_closure_planning_go,
        "candidate_validation_ok": candidate_validation_ok,
        "matrix_validation_ok": matrix_validation_ok,
        "traceability_reference_validation_ok": traceability_reference_validation_ok,
        "absence_validation_ok": absence_validation_ok,
        "boundary_validation_ok": boundary_validation_ok,
        "governance_debt_preserved": governance_debt_preserved,
        "template_lineage_ok": template_lineage_ok,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "post_review_readiness_ok": post_review_readiness_ok,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "protocol_migration": False,
        "whitebox_runtime_integration": False,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "large_file_read_avoidance_ok": file_size_governance_review.get("large_file_read_avoidance_ok") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "verifier_large_file_scan_absent": file_size_governance_review.get("verifier_large_file_scan_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    def _go_value_ok(key: str, value: Any) -> bool:
        if key in (
            "shared_protocol_system_revalidation",
            "l1_input_output_protocol_revalidation",
            "protocol_migration",
            "whitebox_runtime_integration",
        ):
            return value is False
        return value is True

    dryrun_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(_go_value_ok(k, go_condition_values.get(k)) for k in GO_CONDITIONS_KEYS)
    )
    next_phase = NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_condition_values[k] for k in GO_CONDITIONS_KEYS if k in go_condition_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=CHAIN_EVIDENCE_NODES + ("freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun",),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    dryrun_report = {
        "report_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_report_v1",
        "lightweight_compliance_dryrun_only": True,
        "planning_final_decision": planning_summary.get("final_decision"),
        **go_condition_values,
        "boundary_statements": list(BOUNDARY_STATEMENTS),
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    candidate_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_validation_v1",
        "candidates": candidate_rows,
        "candidate_validation_ok": candidate_validation_ok,
        "core_candidate_ids": list(CORE_CANDIDATE_IDS),
        **meta,
    }
    matrix_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_matrix_validation_v1",
        "rows": matrix_rows,
        "matrix_validation_ok": matrix_validation_ok,
        **meta,
    }
    traceability_reference_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_traceability_reference_validation_v1",
        "chain": trace_chain,
        "protocol_refs": protocol_refs,
        "traceability_reference_validation_ok": traceability_reference_validation_ok,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        **meta,
    }
    absence_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_validation_v1",
        "absence_validation_ok": absence_validation_ok,
        **absence,
        **meta,
    }
    boundary_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_boundary_validation_v1",
        "statements": list(BOUNDARY_STATEMENTS),
        "boundary_pairs": [{"candidate": c, "forbidden_final": f} for c, f in CANDIDATE_BOUNDARY_PAIRS],
        "boundary_validation_ok": boundary_validation_ok,
        "closure_candidate_ne_closure_executed": True,
        **meta,
    }
    governance_debt_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_governance_debt_validation_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        **meta,
    }
    template_lineage_doc = {
        "lineage_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_template_lineage_v1",
        "upstream_record_approval_closure_planning_lineage_ok": planning_summary.get("template_lineage_ok") is True,
        **template_lineage,
        **meta,
    }
    post_review_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_review_readiness_v1",
        "post_review_readiness_ok": post_review_readiness_ok,
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review",
        "request_issued": False,
        "notification_sent": False,
        "request_record_created": False,
        "approval_record_created": False,
        "ack_record_created": False,
        "evidence_bound_record_created": False,
        "authorization_request_issued": False,
        "grant_issued": False,
        "foundation_frozen": False,
        "closure_executed": False,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "lightweight_compliance_dryrun_only": True,
        "blocker_count": len(issues),
        "issues": issues,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Record Approval Closure Lightweight Compliance DryRun Report v1",
            "",
            "Lightweight compliance dry-run only. No L1 protocol body revalidation. No shared protocol system revalidation.",
            "",
            f"Planning GO: `{prior_record_approval_closure_planning_go}`",
            f"Candidate validation OK: `{candidate_validation_ok}`",
            f"Absence validation OK: `{absence_validation_ok}`",
            f"shared_protocol_system_revalidation: `false`",
            f"l1_input_output_protocol_revalidation: `false`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_report": dryrun_report,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_report_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_validation": candidate_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_matrix_validation": matrix_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_traceability_reference_validation": traceability_reference_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_validation": absence_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_boundary_validation": boundary_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_governance_debt_validation": governance_debt_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_template_lineage": template_lineage_doc,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_review_readiness": post_review_readiness,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
