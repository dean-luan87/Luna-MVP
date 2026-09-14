# -*- coding: utf-8 -*-
"""Luna Midplatform Record Approval Closure Lightweight Compliance Post-DryRun Review v1.

Lightweight post-dryrun review only — accepts DryRun GO, confirms candidate/absence/boundary
drift absent; no L1 protocol body revalidation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1 import (
    CANDIDATE_BOUNDARY_PAIRS,
    CORE_CANDIDATE_IDS,
    DEFAULT_OUTPUT as DEFAULT_RECORD_APPROVAL_CLOSURE_DRYRUN_ROOT,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
)

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Post-DryRun-Review-v1-001"
)
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_lightweight_post_dryrun_review_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_DRYRUN_REVIEW_READY_FOR_FINAL_GATE_PLANNING"
)
FINAL_DECISION_DRYRUN = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_DRYRUN_GAP"
)
FINAL_DECISION_CANDIDATE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_CANDIDATE_ESCALATION"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_DRYRUN_REVIEW_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Planning-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Post-DryRun-Review-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1_smoke_v0"
)
POST_REVIEW_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_DRYRUN_REVIEW_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_foundation_handoff_evaluation_template_lineage_v1.py"

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_report_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_report_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_result_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_boundary_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_traceability_reference_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_governance_debt_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_next_phase_readiness_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

DRYRUN_INDEX_FILES: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "file_size_governance_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_boundary_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_traceability_reference_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_governance_debt_validation_v1.json",
)

ABSENCE_KEYS: Tuple[str, ...] = (
    "request_issued_absent",
    "notification_sent_absent",
    "request_record_absent",
    "approval_record_absent",
    "ack_record_absent",
    "evidence_bound_record_absent",
    "authorization_request_absent",
    "grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "runtime_execution_absent",
    "protocol_runtime_absent",
    "whitebox_runtime_integration_absent",
    "module_adapter_implementation_absent",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_record_approval_closure_dryrun_go",
    "dryrun_result_accepted",
    "candidate_review_ok",
    "absence_review_ok",
    "boundary_review_ok",
    "traceability_reference_review_ok",
    "governance_debt_preserved",
    "file_size_governance_review_ok",
    "post_review_only",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
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
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "post_review_only": True,
        "lightweight_compliance_post_review_only": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "record_approval_closure_dryrun_root": str(dryrun),
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1(
    *,
    record_approval_closure_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(record_approval_closure_dryrun_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, dryrun)
    issues: List[str] = []

    dryrun_summary = _read_json(dryrun / "summary.json")
    dryrun_verifier = _read_json(dryrun / "verifier_report.json")
    dryrun_file_size = _read_json(dryrun / "file_size_governance_review_v1.json")
    candidate_val = _read_json(dryrun / DRYRUN_INDEX_FILES[3])
    absence_val = _read_json(dryrun / DRYRUN_INDEX_FILES[4])
    boundary_val = _read_json(dryrun / DRYRUN_INDEX_FILES[5])
    trace_val = _read_json(dryrun / DRYRUN_INDEX_FILES[6])
    debt_val = _read_json(dryrun / DRYRUN_INDEX_FILES[7])

    prior_record_approval_closure_dryrun_go = (
        dryrun_summary.get("final_decision") == DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 420
        and dryrun_verifier.get("failed_checks") == 0
        and dryrun_verifier.get("blocker_count") == 0
        and dryrun_summary.get("dryrun_pass") is True
        and dryrun_summary.get("lightweight_compliance_dryrun_only") is True
        and dryrun_verifier.get("lightweight_compliance_verifier_only") is True
        and dryrun_summary.get("file_size_governance_review_ok") is True
    )
    if not prior_record_approval_closure_dryrun_go:
        issues.append("dryrun_not_go")

    dryrun_result_accepted = (
        prior_record_approval_closure_dryrun_go
        and dryrun_summary.get("candidate_validation_ok") is True
        and dryrun_summary.get("absence_validation_ok") is True
        and dryrun_summary.get("boundary_validation_ok") is True
        and dryrun_summary.get("traceability_reference_validation_ok") is True
    )
    if not dryrun_result_accepted:
        issues.append("dryrun_result_not_accepted")

    candidate_rows = list(candidate_val.get("candidates") or [])
    candidate_review_ok = (
        dryrun_result_accepted
        and candidate_val.get("candidate_validation_ok") is True
        and len(candidate_rows) >= 5
        and all(row.get("still_candidate") for row in candidate_rows)
        and all(row.get("record_created") is False for row in candidate_rows)
        and all(row.get("closure_executed") is False for row in candidate_rows)
    )
    for cid in CORE_CANDIDATE_IDS:
        row = next((r for r in candidate_rows if r.get("candidate_id") == cid), {})
        if not row or row.get("still_candidate") is not True:
            candidate_review_ok = False
    if not candidate_review_ok:
        issues.append("candidate_escalation")

    absence = {key: dryrun_summary.get(key) is True for key in ABSENCE_KEYS}
    if absence_val:
        absence = {key: absence.get(key) and absence_val.get(key) is True for key in ABSENCE_KEYS}
    absence_review_ok = dryrun_result_accepted and all(absence.values())
    if not absence_review_ok:
        issues.append("absence_drift")

    boundary_review_ok = (
        absence_review_ok
        and boundary_val.get("boundary_validation_ok") is True
        and dryrun_summary.get("non_execution_boundary_ok") is True
    )
    if not boundary_review_ok:
        issues.append("boundary_drift")

    traceability_reference_review_ok = (
        dryrun_result_accepted
        and trace_val.get("traceability_reference_validation_ok") is True
        and trace_val.get("shared_protocol_system_revalidation") is False
        and trace_val.get("l1_input_output_protocol_revalidation") is False
    )
    if not traceability_reference_review_ok:
        issues.append("traceability_drift")

    governance_debt_preserved = (
        dryrun_summary.get("governance_debt_preserved") is True
        and debt_val.get("governance_debt_preserved") is True
        and len(GOVERNANCE_DEBTS) >= 2
        and GOVERNANCE_DEBTS[0].get("must_not_implement_now") is True
    )
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    non_execution_boundary_ok = dryrun_summary.get("non_execution_boundary_ok") is True
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if dryrun_summary.get(flag) is True:
            non_execution_boundary_ok = False
            issues.append(f"runtime_flag:{flag}")
            break

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-DryRun-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_WHITELIST_FILES[2],
        base_go_no_go_pack=POST_REVIEW_GO_NO_GO_PACK,
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Post-DryRun-Review-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_REQUEST_RECORD_APPROVAL_CLOSURE_POST_REVIEW_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-DryRun-v1-001",
    )
    template_lineage_ok = (
        template_lineage.get("template_lineage_ok") is True
        and dryrun_summary.get("template_lineage_ok") is True
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
        previous_interruption_type=dryrun_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=dryrun_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=dryrun_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    post_review_only = True
    next_phase_readiness_ok = (
        dryrun_result_accepted
        and candidate_review_ok
        and absence_review_ok
        and boundary_review_ok
        and traceability_reference_review_ok
        and governance_debt_preserved
        and non_execution_boundary_ok
        and template_lineage_ok
        and file_size_governance_review_ok
    )

    if not prior_record_approval_closure_dryrun_go or not dryrun_result_accepted:
        final_decision = FINAL_DECISION_DRYRUN
    elif not template_lineage_ok:
        final_decision = FINAL_DECISION_LINEAGE
    elif not candidate_review_ok:
        final_decision = FINAL_DECISION_CANDIDATE
    elif not absence_review_ok:
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_record_approval_closure_dryrun_go": prior_record_approval_closure_dryrun_go,
        "dryrun_result_accepted": dryrun_result_accepted,
        "candidate_review_ok": candidate_review_ok,
        "absence_review_ok": absence_review_ok,
        "boundary_review_ok": boundary_review_ok,
        "traceability_reference_review_ok": traceability_reference_review_ok,
        "governance_debt_preserved": governance_debt_preserved,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "post_review_only": post_review_only,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "template_lineage_ok": template_lineage_ok,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "large_file_read_avoidance_ok": file_size_governance_review.get("large_file_read_avoidance_ok") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "verifier_large_file_scan_absent": file_size_governance_review.get("verifier_large_file_scan_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    post_review_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(go_condition_values[k] for k in GO_CONDITIONS_KEYS)
    )
    next_phase = NEXT_PHASE_GO if post_review_pass else NEXT_PHASE_HOLD
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_condition_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(dryrun_summary.get("chain_trace_nodes") or [])
            + ["freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    dryrun_result_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_result_review_v1",
        "dryrun_final_decision": dryrun_summary.get("final_decision"),
        "dryrun_verifier": dryrun_verifier.get("verifier"),
        "dryrun_passed_checks": dryrun_verifier.get("passed_checks"),
        "lightweight_compliance_verifier_only": dryrun_verifier.get("lightweight_compliance_verifier_only"),
        "dryrun_result_accepted": dryrun_result_accepted,
        **meta,
    }
    candidate_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_review_v1",
        "candidates": candidate_rows,
        "boundary_pairs": [{"candidate": c, "forbidden_final": f} for c, f in CANDIDATE_BOUNDARY_PAIRS],
        "candidate_review_ok": candidate_review_ok,
        "core_candidate_ids": list(CORE_CANDIDATE_IDS),
        **meta,
    }
    absence_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_review_v1",
        "absence_review_ok": absence_review_ok,
        **absence,
        **meta,
    }
    boundary_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_boundary_review_v1",
        "boundary_review_ok": boundary_review_ok,
        "closure_candidate_ne_closure_executed": True,
        **meta,
    }
    traceability_reference_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_traceability_reference_review_v1",
        "traceability_reference_review_ok": traceability_reference_review_ok,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "protocol_refs": trace_val.get("protocol_refs") or [],
        **meta,
    }
    governance_debt_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_governance_debt_review_v1",
        "debts": list(GOVERNANCE_DEBTS),
        "governance_debt_preserved": governance_debt_preserved,
        **meta,
    }
    next_phase_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_next_phase_readiness_v1",
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_request_final_gate_planning",
        "final_gate_planning_readiness": next_phase_readiness_ok,
        "request_issued": False,
        "notification_sent": False,
        "request_record_created": False,
        "approval_record_created": False,
        "grant_issued": False,
        "foundation_frozen": False,
        "closure_executed": False,
        **meta,
    }
    post_review_report = {
        "report_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_report_v1",
        **go_condition_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "post_review_pass": post_review_pass,
        "post_review_only": True,
        "lightweight_compliance_post_review_only": True,
        "blocker_count": len(issues),
        "issues": issues,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Record Approval Closure Lightweight Post-DryRun Review Report v1",
            "",
            "Lightweight compliance post-dryrun review only. No L1 protocol body revalidation.",
            "",
            f"DryRun GO accepted: `{dryrun_result_accepted}`",
            f"Candidate review OK: `{candidate_review_ok}`",
            f"Absence review OK: `{absence_review_ok}`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_report": post_review_report,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_report_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_result_review": dryrun_result_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_review": candidate_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_review": absence_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_boundary_review": boundary_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_traceability_reference_review": traceability_reference_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_governance_debt_review": governance_debt_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_next_phase_readiness": next_phase_readiness,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
