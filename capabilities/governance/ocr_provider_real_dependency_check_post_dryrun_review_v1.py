# -*- coding: utf-8 -*-
"""OCR Provider Real Dependency Check Post-DryRun Review v1 — review-only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_real_dependency_check_dryrun_v1 import (
    BLOCKED_PATHS,
    EVIDENCE_CANDIDATE_SLOTS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    SCOPE as DRYRUN_SCOPE,
)
from capabilities.governance.ocr_provider_real_dependency_check_planning_v1 import (
    CHECK_SEQUENCE,
    FAILURE_HANDLING,
    ROLLBACK_RULES,
)

PHASE_ID = "Phase-OCR-Provider-Real-Dependency-Check-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "ocr_provider_real_dependency_check_post_dryrun_review_only"
SOURCE_CHAIN = "ocr_provider_real_dependency_check_post_dryrun_review_v1"

UPSTREAM_REQUIRED_FINAL = DRYRUN_FINAL_GO
UPSTREAM_NEXT_PHASE = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_PROVIDER_REAL_DEPENDENCY_CHECK_POST_DRYRUN_REVIEW_CLOSED_DRYRUN_TRUSTED_READY_FOR_READINESS_HARNESS"
)
FINAL_DECISION_HOLD = "OCR_PROVIDER_REAL_DEPENDENCY_CHECK_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Controlled-Provider-Readiness-Harness-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Real-Dependency-Check-Issue-Review-v1-001"

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "new_evidence_package_candidate_generated_now",
    "new_failure_route_candidate_generated_now",
    "real_dependency_check_executed_now",
    "python_package_check_executed_now",
    "provider_import_check_executed_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_smoke_check_executed_now",
    "sample_ocr_executed_now",
    "provider_selection_finalized_now",
    "provider_authorization_started_now",
    "paddleocr_imported_now",
    "rapidocr_imported_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ real dependency check executed",
    "dryrun flow trusted ≠ import/install allowed",
    "evidence candidate trusted ≠ evidence committed",
    "harness extraction next ≠ provider invocation",
    "readiness harness ≠ PaddleOCR enabled",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_real_dependency_check_post_dryrun_review_only": True,
        "review_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE_REVIEW:
        meta[field] = False
    meta["new_evidence_package_candidate_generated_now"] = False
    meta["new_failure_route_candidate_generated_now"] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _simple_review(issues: List[Dict[str, Any]], review_id: str, meta: Dict[str, Any], **extra: Any) -> Dict[str, Any]:
    return {
        "review_id": review_id,
        "issues": issues,
        "review_pass": len(issues) == 0,
        **extra,
        **meta,
    }


def run_ocr_provider_real_dependency_check_post_dryrun_review_v1(
    *,
    ocr_provider_real_dependency_check_dryrun_root: str,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(ocr_provider_real_dependency_check_dryrun_root).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}

    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    )
    meta = {**_review_meta(), "upstream_dryrun_root": str(dryrun_root), "review_output_root": str(out_root)}

    sequence = _try_read_json(dryrun_root / "dependency_check_sequence_dryrun_result_v1.json") or {}
    paddle = _try_read_json(dryrun_root / "paddleocr_dependency_check_dryrun_result_v1.json") or {}
    rapid = _try_read_json(dryrun_root / "rapidocr_dependency_check_dryrun_result_v1.json") or {}
    external = _try_read_json(dryrun_root / "external_ocr_dependency_check_dryrun_result_v1.json") or {}
    evidence = _try_read_json(dryrun_root / "evidence_package_candidate_v1.json") or {}
    failure = _try_read_json(dryrun_root / "failure_route_candidate_matrix_v1.json") or {}
    rollback = _try_read_json(dryrun_root / "rollback_plan_candidate_result_v1.json") or {}
    isolation = _try_read_json(dryrun_root / "environment_isolation_boundary_dryrun_result_v1.json") or {}
    gate = _try_read_json(dryrun_root / "future_execution_gate_dryrun_result_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "real_dependency_check_blocked_path_result_v1.json") or {}
    audit = _try_read_json(dryrun_root / "real_dependency_check_no_execution_audit_v1.json") or {}

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_NEXT_PHASE:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("simulated") is not True:
        blockers.append("dryrun must be simulated")

    input_review = {
        "review_id": "real_dependency_check_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_phase": DRYRUN_PHASE,
        "upstream_scope": DRYRUN_SCOPE,
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "sequence_step_count": sequence.get("step_count"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    seq_issues: List[Dict[str, Any]] = []
    if sequence.get("step_count") != len(CHECK_SEQUENCE):
        seq_issues.append({"issue_id": "count", "detail": "expected 9 steps"})
    for step in sequence.get("steps") or []:
        if step.get("current_executed_now") is not False:
            seq_issues.append({"issue_id": step.get("step_id"), "detail": "must not execute"})
        if step.get("evidence_candidate_generated") is not True:
            seq_issues.append({"issue_id": step.get("step_id"), "detail": "evidence candidate required"})

    sequence_review = _simple_review(seq_issues, "dependency_check_sequence_review_v1", meta)

    def _provider_issues(plan: Dict[str, Any], fam: str) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        if not plan.get("provider_candidate_ref"):
            issues.append({"issue_id": "ref", "detail": "missing ref"})
        if plan.get("current_import_executed_now") is not False:
            issues.append({"issue_id": "import", "detail": "must be false"})
        if plan.get("current_provider_invoked_now") is not False:
            issues.append({"issue_id": "invoke", "detail": "must be false"})
        return issues

    paddle_review = _simple_review(
        _provider_issues(paddle, "paddleocr_later"),
        "paddleocr_dependency_check_review_v1",
        meta,
        provider_family="paddleocr_later",
    )
    rapid_review = _simple_review(
        _provider_issues(rapid, "rapidocr_later"),
        "rapidocr_dependency_check_review_v1",
        meta,
        provider_family="rapidocr_later",
    )
    external_review = _simple_review(
        _provider_issues(external, "external_ocr_later"),
        "external_ocr_dependency_check_review_v1",
        meta,
        provider_family="external_ocr_later",
    )

    ev_issues: List[Dict[str, Any]] = []
    if evidence.get("slot_count") != len(EVIDENCE_CANDIDATE_SLOTS):
        ev_issues.append({"issue_id": "slots", "detail": f"expected {len(EVIDENCE_CANDIDATE_SLOTS)}"})
    if evidence.get("evidence_collected_now") is not False:
        ev_issues.append({"issue_id": "collected", "detail": "must be false"})

    evidence_review = _simple_review(ev_issues, "evidence_package_candidate_review_v1", meta)

    fail_issues: List[Dict[str, Any]] = []
    if failure.get("route_count") != len(FAILURE_HANDLING):
        fail_issues.append({"issue_id": "routes", "detail": "route count mismatch"})

    failure_review = _simple_review(fail_issues, "failure_route_candidate_review_v1", meta)

    rb_issues: List[Dict[str, Any]] = []
    if rollback.get("rollback_executed_now") is not False:
        rb_issues.append({"issue_id": "rollback", "detail": "must not execute"})
    for rule in ROLLBACK_RULES:
        if rollback.get("rules", {}).get(rule) is not True:
            rb_issues.append({"issue_id": rule, "detail": "rule required"})

    rollback_review = _simple_review(rb_issues, "rollback_plan_candidate_review_v1", meta)

    iso_issues: List[Dict[str, Any]] = []
    if isolation.get("boundary_pass") is not True:
        iso_issues.append({"issue_id": "boundary", "detail": "must pass"})

    isolation_review = _simple_review(iso_issues, "environment_isolation_boundary_review_v1", meta)

    gate_issues: List[Dict[str, Any]] = []
    if gate.get("gate_open_now") is not False:
        gate_issues.append({"issue_id": "gate_open", "detail": "must be false"})
    if gate.get("execution_allowed_now") is not False:
        gate_issues.append({"issue_id": "exec", "detail": "must be false"})

    gate_review = _simple_review(gate_issues, "future_execution_gate_review_v1", meta)

    blocked_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in blocked.get("paths") or []}
    if blocked.get("all_blocked") is not True or len(paths) != len(BLOCKED_PATHS):
        blocked_issues.append({"issue_id": "count", "detail": f"expected {len(BLOCKED_PATHS)}"})
    for pid in BLOCKED_PATHS:
        if not paths.get(pid) or paths[pid].get("blocked") is not True:
            blocked_issues.append({"issue_id": pid, "detail": "must be blocked"})

    blocked_review = _simple_review(
        blocked_issues,
        "real_dependency_check_blocked_path_review_v1",
        meta,
        paths_total=len(BLOCKED_PATHS),
    )

    audit_issues: List[Dict[str, Any]] = []
    if audit.get("audit_pass") is not True:
        audit_issues.append({"issue_id": "audit", "detail": "must pass"})
    for flag in ("no_import", "no_install", "no_download", "no_smoke", "no_sample_ocr"):
        if audit.get(flag) is not True:
            audit_issues.append({"issue_id": flag, "detail": "must be true"})

    audit_review = _simple_review(audit_issues, "real_dependency_check_no_execution_review_v1", meta)

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and all(
            r.get("review_pass")
            for r in (
                sequence_review,
                paddle_review,
                rapid_review,
                external_review,
                evidence_review,
                failure_review,
                rollback_review,
                isolation_review,
                gate_review,
                blocked_review,
                audit_review,
            )
        )
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "real_dependency_check_closure_decision_v1",
        "ocr_provider_real_dependency_check_dryrun_closed": boundary_ok,
        "real_dependency_check_flow_trusted": boundary_ok,
        "evidence_package_candidate_trusted": boundary_ok,
        "failure_route_candidate_trusted": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_readiness = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_controlled_provider_readiness_harness": boundary_ok,
        "do_not_execute_real_dependency_check_now": True,
        "do_not_import_provider_now": True,
        "do_not_install_dependency_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "ocr_provider_real_dependency_check_dryrun_closed": boundary_ok,
        "real_dependency_check_flow_trusted": boundary_ok,
        **meta,
    }

    return {
        "real_dependency_check_dryrun_input_review": input_review,
        "dependency_check_sequence_review": sequence_review,
        "paddleocr_dependency_check_review": paddle_review,
        "rapidocr_dependency_check_review": rapid_review,
        "external_ocr_dependency_check_review": external_review,
        "evidence_package_candidate_review": evidence_review,
        "failure_route_candidate_review": failure_review,
        "rollback_plan_candidate_review": rollback_review,
        "environment_isolation_boundary_review": isolation_review,
        "future_execution_gate_review": gate_review,
        "real_dependency_check_blocked_path_review": blocked_review,
        "real_dependency_check_no_execution_review": audit_review,
        "real_dependency_check_closure_decision": closure,
        "next_route_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
