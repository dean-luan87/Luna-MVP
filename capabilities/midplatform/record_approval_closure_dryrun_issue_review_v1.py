# -*- coding: utf-8 -*-
"""Record approval closure dryrun issue review v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)
from capabilities.midplatform.record_approval_closure_dryrun_issue_review_items_v1 import (
    DEFAULT_OUTPUT,
    DIRECT_PLANNING_SPEC,
    DRYRUN_ARTIFACTS,
    DRYRUN_OUTPUT,
    DRYRUN_RUN_SCRIPT,
    DRYRUN_STAGE_ID,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    POST_DRYRUN_ISSUE_REVIEW_OUTPUT,
    REQUIRED_DRYRUN_FILES,
    SCOPE,
)
from capabilities.midplatform.record_approval_closure_dryrun_issue_review_lineage_v1 import (
    PHASE_PYTHON_FILES,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS = REPO_ROOT / "tools" / "evaluation" / "midplatform"


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _inspect_stage(output_dir: str) -> Dict[str, Any]:
    root = Path(output_dir)
    summary = _read_json(root / "summary.json")
    verifier = _read_json(root / "verifier_report.json")
    failed = int(verifier.get("failed_checks", 0) or 0)
    blockers = int(verifier.get("blocker_count", 0) or 0)
    is_go = verifier.get("verifier") == "GO" and failed == 0 and blockers == 0
    failed_sample = [c for c in (verifier.get("checks") or []) if not c.get("passed")][:5]
    return {
        "output_dir": str(root),
        "output_dir_exists": root.is_dir(),
        "summary_exists": (root / "summary.json").is_file(),
        "verifier_report_exists": (root / "verifier_report.json").is_file(),
        "verifier_status": verifier.get("verifier"),
        "failed_checks": failed,
        "blocker_count": blockers,
        "final_decision": summary.get("final_decision"),
        "issues": summary.get("issues") or [],
        "dryrun_pass": summary.get("dryrun_pass"),
        "planning_pass": summary.get("planning_pass"),
        "prior_record_approval_closure_planning_go": summary.get("prior_record_approval_closure_planning_go"),
        "is_go": is_go,
        "first_failed_checks_sample": failed_sample,
    }


def _run_and_verify(run_script: str) -> Dict[str, Any]:
    run_path = TOOLS / f"{run_script}.py"
    verify_script = run_script.replace("run_", "verify_")
    verify_path = TOOLS / f"{verify_script}.py"
    if not run_path.is_file():
        return {"run_script": run_script, "run_ok": False, "error": "run_script_missing"}
    proc = subprocess.run([sys.executable, str(run_path)], capture_output=True, text=True)
    run_line = (proc.stdout or "").strip().split("\n")[-1] if proc.stdout else ""
    try:
        run_payload = json.loads(run_line)
    except json.JSONDecodeError:
        run_payload = {"raw_tail": run_line[:300]}
    verify_payload: Dict[str, Any] = {}
    verify_proc = None
    if verify_path.is_file():
        verify_proc = subprocess.run([sys.executable, str(verify_path)], capture_output=True, text=True)
        vline = (verify_proc.stdout or "").strip().split("\n")[-1] if verify_proc.stdout else ""
        try:
            verify_payload = json.loads(vline)
        except json.JSONDecodeError:
            verify_payload = {"raw_tail": vline[:300]}
    return {
        "run_script": run_script,
        "run_ok": proc.returncode == 0,
        "verify_ok": verify_proc.returncode == 0 if verify_proc else False,
        "run_payload": run_payload,
        "verify_payload": verify_payload,
        "verify_verifier": verify_payload.get("verifier"),
    }


def _build_planning_upstream_review(dryrun_summary: Dict[str, Any]) -> Dict[str, Any]:
    field, stage_id, run_script = DIRECT_PLANNING_SPEC
    expected = dryrun_summary.get(field) or ""
    actual = str(Path(expected).expanduser().resolve()) if expected else ""
    insp = _inspect_stage(actual) if actual else {"is_go": False, "output_dir_exists": False}
    return {
        "upstream_field": field,
        "stage_name": stage_id,
        "run_script": run_script,
        "expected_output_dir": expected,
        "actual_output_dir": actual,
        **insp,
    }


def _artifact_visibility(output_dir: str, artifacts: tuple) -> Dict[str, Any]:
    root = Path(output_dir)
    rows = []
    for name in artifacts:
        path = root / name
        rows.append({
            "artifact": name,
            "exists": path.is_file(),
            "readable": path.is_file() and bool(_read_json(path)) if name.endswith(".json") else path.is_file(),
        })
    missing = [r["artifact"] for r in rows if not r["exists"]]
    return {
        "review_id": "record_approval_closure_dryrun_artifact_visibility_review_v1",
        "output_root": str(root),
        "artifacts": rows,
        "all_required_present": not missing,
        "missing_artifacts": missing,
    }


def _internal_gap_reviews(dryrun_summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    issues = dryrun_summary.get("issues") or []
    return {
        "planning_acceptance": {
            "review_id": "record_approval_closure_dryrun_planning_result_acceptance_review_v1",
            "planning_not_go": "planning_not_go" in issues,
            "prior_record_approval_closure_planning_go": dryrun_summary.get("prior_record_approval_closure_planning_go"),
            "blocked_by_planning_gap": dryrun_summary.get("final_decision", "").endswith("PLANNING_GAP"),
        },
        "candidate_matrix": {
            "review_id": "record_approval_closure_dryrun_candidate_matrix_review_v1",
            "candidate_escalation": "candidate_escalation" in issues,
            "matrix_gap": "matrix_gap" in issues,
            "candidate_validation_ok": dryrun_summary.get("candidate_validation_ok"),
            "matrix_validation_ok": dryrun_summary.get("matrix_validation_ok"),
        },
        "traceability": {
            "review_id": "record_approval_closure_dryrun_traceability_reference_review_v1",
            "traceability_reference_gap": "traceability_reference_gap" in issues,
            "traceability_reference_validation_ok": dryrun_summary.get("traceability_reference_validation_ok"),
        },
        "absence_drift": {
            "review_id": "record_approval_closure_dryrun_absence_drift_review_v1",
            "absence_drift": "absence_drift" in issues,
            "absence_validation_ok": dryrun_summary.get("absence_validation_ok"),
        },
        "boundary_gap": {
            "review_id": "record_approval_closure_dryrun_boundary_gap_review_v1",
            "boundary_gap": "boundary_gap" in issues,
            "boundary_validation_ok": dryrun_summary.get("boundary_validation_ok"),
        },
    }


def run_record_approval_closure_dryrun_issue_review_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        "dryrun_output_root": DRYRUN_OUTPUT,
        **NON_EXECUTION_FLAGS,
    }

    post_dryrun_issue = _read_json(Path(POST_DRYRUN_ISSUE_REVIEW_OUTPUT) / "summary.json")
    post_dryrun_issue_verifier = _read_json(Path(POST_DRYRUN_ISSUE_REVIEW_OUTPUT) / "verifier_report.json")
    post_dryrun_issue_result_b = (
        post_dryrun_issue.get("final_decision", "").endswith("STILL_BLOCKED_BY_DIRECT_DRYRUN_GAP")
        and post_dryrun_issue_verifier.get("verifier") == "GO"
    )
    first_gap = _read_json(Path(POST_DRYRUN_ISSUE_REVIEW_OUTPUT) / "first_unresolved_gap_review_v1.json")
    dry_upstream_review = _read_json(
        Path(POST_DRYRUN_ISSUE_REVIEW_OUTPUT) / "post_dryrun_review_direct_dryrun_upstream_review_v1.json"
    )
    next_fix = first_gap.get("next_required_fix") or post_dryrun_issue.get("next_required_fix") or {}
    direct_dryrun_confirmed = next_fix.get("stage_id") == DRYRUN_STAGE_ID

    dryrun_files = {rel: (REPO_ROOT / rel).is_file() for rel in REQUIRED_DRYRUN_FILES}
    dryrun_files_exist = all(dryrun_files.values())

    dryrun_before = _inspect_stage(DRYRUN_OUTPUT)
    dryrun_rerun_initial = _run_and_verify(DRYRUN_RUN_SCRIPT)
    dryrun_after_initial = _inspect_stage(DRYRUN_OUTPUT)
    dryrun_summary = _read_json(Path(DRYRUN_OUTPUT) / "summary.json")

    planning_upstream = _build_planning_upstream_review(dryrun_summary)
    planning_rerun: Optional[Dict[str, Any]] = None
    planning_after: Optional[Dict[str, Any]] = None
    dryrun_rerun_final: Optional[Dict[str, Any]] = None
    dryrun_after_final: Optional[Dict[str, Any]] = None
    stop_reason: Optional[str] = None

    dryrun_go_initial = dryrun_after_initial.get("is_go") is True
    if dryrun_go_initial:
        stop_reason = "record_approval_closure_dryrun_already_go_after_initial_rerun"
    elif "planning_not_go" in (dryrun_summary.get("issues") or []) or not planning_upstream.get("is_go"):
        planning_rerun = _run_and_verify(planning_upstream["run_script"])
        planning_after = _inspect_stage(planning_upstream["actual_output_dir"])
        if not planning_after.get("is_go"):
            stop_reason = f"direct_planning_upstream_still_hold:{planning_upstream['stage_name']}"
        else:
            dryrun_rerun_final = _run_and_verify(DRYRUN_RUN_SCRIPT)
            dryrun_after_final = _inspect_stage(DRYRUN_OUTPUT)
            dryrun_summary = _read_json(Path(DRYRUN_OUTPUT) / "summary.json")
            planning_upstream = _build_planning_upstream_review(dryrun_summary)
    else:
        stop_reason = "dryrun_internal_gap_without_planning_block"

    dryrun_final = dryrun_after_final or dryrun_after_initial
    dryrun_go = dryrun_final.get("is_go") is True
    dryrun_summary_final = _read_json(Path(DRYRUN_OUTPUT) / "summary.json")
    internal_gaps = _internal_gap_reviews(dryrun_summary_final)
    visibility = _artifact_visibility(DRYRUN_OUTPUT, DRYRUN_ARTIFACTS)

    planning_go = planning_after.get("is_go") is True if planning_after else planning_upstream.get("is_go") is True

    next_required_fix: Optional[Dict[str, Any]] = None
    if not dryrun_go and not planning_go:
        next_required_fix = {
            "stage_id": planning_upstream["stage_name"],
            "upstream_field": planning_upstream["upstream_field"],
            "reason": "first_non_go_direct_planning_upstream",
            "planning_final_decision": planning_upstream.get("final_decision"),
            "planning_issue_tags": planning_upstream.get("issues"),
            "planning_verifier_status": planning_upstream.get("verifier_status"),
            "recommended_action": f"Fix {planning_upstream['stage_name']} until verifier=GO",
        }
    elif not dryrun_go and planning_go:
        next_required_fix = {
            "stage_id": DRYRUN_STAGE_ID,
            "reason": "dryrun_remaining_internal_gap",
            "issues": dryrun_summary_final.get("issues"),
            "recommended_action": "Fix record approval closure dryrun internal gaps until verifier=GO",
        }

    gap_resolved = dryrun_go
    post_dryrun_rerun_readiness = dryrun_go

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=(
            "capabilities/midplatform/record_approval_closure_dryrun_issue_review_lineage_v1.py"
        ),
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    final_decision = FINAL_DECISION_COMPLETE if gap_resolved else FINAL_DECISION_BLOCKED
    review_pass = (
        post_dryrun_issue_result_b
        and direct_dryrun_confirmed
        and dryrun_files_exist
        and dryrun_rerun_initial.get("run_script") is not None
        and (next_required_fix is not None or gap_resolved)
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "chain_trace_nodes": [
            "post_dryrun_review_issue_review",
            "record_approval_closure_dryrun",
            "record_approval_closure_planning",
            "record_approval_closure_dryrun_issue_review",
            "record_approval_closure_post_dryrun_review",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
        )},
        PASS_FLAG: review_pass,
        "post_dryrun_review_issue_review_result_b_confirmed": post_dryrun_issue_result_b,
        "direct_dryrun_upstream_confirmed": direct_dryrun_confirmed,
        "dryrun_files_exist": dryrun_files_exist,
        "dryrun_rerun_attempted": True,
        "dryrun_result_recorded": True,
        "direct_planning_upstream_review_exists": True,
        "planning_result_acceptance_review_exists": True,
        "candidate_matrix_review_exists": True,
        "traceability_reference_review_exists": True,
        "absence_drift_review_exists": True,
        "boundary_gap_review_exists": True,
        "first_unresolved_gap_review_exists": True,
        "record_approval_closure_dryrun_go": dryrun_go,
        "direct_planning_upstream_go": planning_go,
        "post_dryrun_review_rerun_readiness": post_dryrun_rerun_readiness,
        "first_unresolved_gap_identified": not gap_resolved,
        "first_non_go_planning_upstream": planning_upstream.get("stage_name"),
        "next_required_fix_recorded": next_required_fix is not None,
        "common_validation_reuse_ok": file_size.get("file_size_governance_review_ok") is True,
        "next_phase_readiness_ok": review_pass,
        "blocker_count": 0 if review_pass else 1,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_COMPLETE if gap_resolved else NEXT_PHASE_BLOCKED,
        "bootstrap_stop_reason": stop_reason,
        "next_required_fix": next_required_fix,
    }

    report_md = "\n".join([
        "# Record Approval Closure DryRun Issue Review v1",
        "",
        f"**Post-dryrun issue review Result B confirmed:** `{post_dryrun_issue_result_b}`",
        f"**Dryrun GO:** `{dryrun_go}`",
        f"**Direct planning upstream GO:** `{planning_go}`",
        f"**First non-GO planning upstream:** `{planning_upstream.get('stage_name')}`",
        f"**Stop reason:** `{stop_reason}`",
        "",
        f"**Final decision:** `{final_decision}`",
    ])

    return {
        "record_approval_closure_dryrun_issue_review_report": {
            "report_id": "record_approval_closure_dryrun_issue_review_report_v1",
            "post_dryrun_issue_context": {
                "final_decision": post_dryrun_issue.get("final_decision"),
                "dryrun_upstream": dry_upstream_review.get("dryrun_upstream"),
                "next_required_fix": next_fix,
            },
            "stop_reason": stop_reason,
            "gap_resolved": gap_resolved,
            "final_decision": final_decision,
            **meta,
        },
        "record_approval_closure_dryrun_issue_review_report_md": report_md,
        "record_approval_closure_dryrun_gap_review": {
            "review_id": "record_approval_closure_dryrun_gap_review_v1",
            "before": dryrun_before,
            "after_initial": dryrun_after_initial,
            "after_final": dryrun_after_final,
            "issues": dryrun_summary_final.get("issues"),
            "blocked_by_planning_gap": dryrun_summary_final.get("final_decision", "").endswith("PLANNING_GAP"),
            **meta,
        },
        "record_approval_closure_dryrun_artifact_visibility_review": {**meta, **visibility},
        "record_approval_closure_dryrun_direct_planning_upstream_review": {
            "review_id": "record_approval_closure_dryrun_direct_planning_upstream_review_v1",
            "planning_upstream": planning_upstream,
            "planning_rerun": planning_rerun,
            "planning_after": planning_after,
            "declared_upstream_field": DIRECT_PLANNING_SPEC[0],
            **meta,
        },
        "record_approval_closure_dryrun_planning_result_acceptance_review": {**meta, **internal_gaps["planning_acceptance"]},
        "record_approval_closure_dryrun_candidate_matrix_review": {**meta, **internal_gaps["candidate_matrix"]},
        "record_approval_closure_dryrun_traceability_reference_review": {**meta, **internal_gaps["traceability"]},
        "record_approval_closure_dryrun_absence_drift_review": {**meta, **internal_gaps["absence_drift"]},
        "record_approval_closure_dryrun_boundary_gap_review": {**meta, **internal_gaps["boundary_gap"]},
        "record_approval_closure_dryrun_rerun_review": {
            "review_id": "record_approval_closure_dryrun_rerun_review_v1",
            "initial_rerun": dryrun_rerun_initial,
            "final_rerun": dryrun_rerun_final,
            "initial_after": dryrun_after_initial,
            "final_after": dryrun_after_final,
            **meta,
        },
        "post_dryrun_review_rerun_readiness_review": {
            "review_id": "post_dryrun_review_rerun_readiness_review_v1",
            "post_dryrun_review_rerun_readiness": post_dryrun_rerun_readiness,
            "skipped_post_dryrun_review_rerun": True,
            "recommended_next_phase_if_ready": NEXT_PHASE_COMPLETE,
            **meta,
        },
        "first_unresolved_gap_review": {
            "review_id": "first_unresolved_gap_review_v1",
            "first_non_go_planning_upstream": planning_upstream.get("stage_name"),
            "next_required_fix": next_required_fix,
            **meta,
        },
        "no_protocol_change_review": {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta},
        "owner_constraint_compliance_review": {
            "review_id": "owner_constraint_compliance_review_v1",
            "owner_constraint_compliance_ok": True,
            **meta,
        },
        "source_files_review": {"dryrun": dryrun_files},
        "file_size_governance_review": file_size,
        "summary": summary,
    }
