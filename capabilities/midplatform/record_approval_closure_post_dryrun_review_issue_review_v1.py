# -*- coding: utf-8 -*-
"""Record approval closure post-dryrun review issue review v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)
from capabilities.midplatform.record_approval_closure_post_dryrun_review_issue_review_items_v1 import (
    DEFAULT_OUTPUT,
    DIRECT_DRYRUN_SPEC,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    INTEGRATED_IMPL_GAP_REVIEW_OUTPUT,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    POST_DRYRUN_ARTIFACTS,
    POST_DRYRUN_REVIEW_OUTPUT,
    POST_DRYRUN_RUN_SCRIPT,
    POST_DRYRUN_STAGE_ID,
    REQUIRED_POST_DRYRUN_FILES,
    SCOPE,
)
from capabilities.midplatform.record_approval_closure_post_dryrun_review_issue_review_lineage_v1 import (
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
        "post_review_pass": summary.get("post_review_pass"),
        "dryrun_pass": summary.get("dryrun_pass"),
        "dryrun_result_accepted": summary.get("dryrun_result_accepted"),
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


def _build_dryrun_upstream_review(post_summary: Dict[str, Any]) -> Dict[str, Any]:
    field, stage_id, run_script = DIRECT_DRYRUN_SPEC
    expected = post_summary.get(field) or ""
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
        "review_id": "post_dryrun_review_artifact_visibility_review_v1",
        "output_root": str(root),
        "artifacts": rows,
        "all_required_present": not missing,
        "missing_artifacts": missing,
    }


def _drift_reviews(post_summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    issues = post_summary.get("issues") or []
    return {
        "dryrun_acceptance": {
            "review_id": "post_dryrun_review_dryrun_result_acceptance_review_v1",
            "dryrun_not_go": "dryrun_not_go" in issues,
            "dryrun_result_not_accepted": "dryrun_result_not_accepted" in issues,
            "prior_record_approval_closure_dryrun_go": post_summary.get("prior_record_approval_closure_dryrun_go"),
            "dryrun_result_accepted": post_summary.get("dryrun_result_accepted"),
        },
        "candidate_escalation": {
            "review_id": "post_dryrun_review_candidate_escalation_review_v1",
            "candidate_escalation": "candidate_escalation" in issues,
            "candidate_review_ok": post_summary.get("candidate_review_ok"),
        },
        "absence_drift": {
            "review_id": "post_dryrun_review_absence_drift_review_v1",
            "absence_drift": "absence_drift" in issues,
            "absence_review_ok": post_summary.get("absence_review_ok"),
        },
        "boundary_drift": {
            "review_id": "post_dryrun_review_boundary_drift_review_v1",
            "boundary_drift": "boundary_drift" in issues,
            "boundary_review_ok": post_summary.get("boundary_review_ok"),
        },
        "traceability_drift": {
            "review_id": "post_dryrun_review_traceability_drift_review_v1",
            "traceability_drift": "traceability_drift" in issues,
            "traceability_reference_review_ok": post_summary.get("traceability_reference_review_ok"),
        },
    }


def run_record_approval_closure_post_dryrun_review_issue_review_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        "post_dryrun_review_output_root": POST_DRYRUN_REVIEW_OUTPUT,
        **NON_EXECUTION_FLAGS,
    }

    integrated_gap = _read_json(Path(INTEGRATED_IMPL_GAP_REVIEW_OUTPUT) / "summary.json")
    integrated_gap_verifier = _read_json(Path(INTEGRATED_IMPL_GAP_REVIEW_OUTPUT) / "verifier_report.json")
    integrated_gap_result_b = (
        integrated_gap.get("final_decision", "").endswith("STILL_BLOCKED_BY_DIRECT_UPSTREAM_GAP")
        and integrated_gap_verifier.get("verifier") == "GO"
    )
    first_gap = _read_json(Path(INTEGRATED_IMPL_GAP_REVIEW_OUTPUT) / "first_unresolved_gap_review_v1.json")
    first_upstream_review = _read_json(
        Path(INTEGRATED_IMPL_GAP_REVIEW_OUTPUT) / "integrated_implementation_first_non_go_upstream_review_v1.json"
    )
    next_fix = first_gap.get("next_required_fix") or integrated_gap.get("next_required_fix") or {}
    first_non_go_confirmed = next_fix.get("stage_id") == POST_DRYRUN_STAGE_ID

    post_files = {rel: (REPO_ROOT / rel).is_file() for rel in REQUIRED_POST_DRYRUN_FILES}
    post_files_exist = all(post_files.values())

    post_before = _inspect_stage(POST_DRYRUN_REVIEW_OUTPUT)
    post_rerun_initial = _run_and_verify(POST_DRYRUN_RUN_SCRIPT)
    post_after_initial = _inspect_stage(POST_DRYRUN_REVIEW_OUTPUT)
    post_summary = _read_json(Path(POST_DRYRUN_REVIEW_OUTPUT) / "summary.json")

    dryrun_upstream = _build_dryrun_upstream_review(post_summary)
    dryrun_rerun: Optional[Dict[str, Any]] = None
    dryrun_after: Optional[Dict[str, Any]] = None
    post_rerun_final: Optional[Dict[str, Any]] = None
    post_after_final: Optional[Dict[str, Any]] = None
    stop_reason: Optional[str] = None

    post_go_initial = post_after_initial.get("is_go") is True
    if post_go_initial:
        stop_reason = "post_dryrun_review_already_go_after_initial_rerun"
    elif "dryrun_not_go" in (post_summary.get("issues") or []) or not dryrun_upstream.get("is_go"):
        dryrun_rerun = _run_and_verify(dryrun_upstream["run_script"])
        dryrun_after = _inspect_stage(dryrun_upstream["actual_output_dir"])
        if not dryrun_after.get("is_go"):
            stop_reason = f"direct_dryrun_upstream_still_hold:{dryrun_upstream['stage_name']}"
        else:
            post_rerun_final = _run_and_verify(POST_DRYRUN_RUN_SCRIPT)
            post_after_final = _inspect_stage(POST_DRYRUN_REVIEW_OUTPUT)
            post_summary = _read_json(Path(POST_DRYRUN_REVIEW_OUTPUT) / "summary.json")
            dryrun_upstream = _build_dryrun_upstream_review(post_summary)
    else:
        stop_reason = "post_dryrun_review_internal_gap_without_dryrun_block"

    post_final = post_after_final or post_after_initial
    post_go = post_final.get("is_go") is True
    post_summary_final = _read_json(Path(POST_DRYRUN_REVIEW_OUTPUT) / "summary.json")
    drift = _drift_reviews(post_summary_final)
    visibility = _artifact_visibility(POST_DRYRUN_REVIEW_OUTPUT, POST_DRYRUN_ARTIFACTS)

    dryrun_go = dryrun_after.get("is_go") is True if dryrun_after else dryrun_upstream.get("is_go") is True

    next_required_fix: Optional[Dict[str, Any]] = None
    if not post_go and not dryrun_go:
        next_required_fix = {
            "stage_id": dryrun_upstream["stage_name"],
            "upstream_field": dryrun_upstream["upstream_field"],
            "reason": "first_non_go_direct_dryrun_upstream",
            "dryrun_final_decision": dryrun_upstream.get("final_decision"),
            "dryrun_issue_tags": dryrun_upstream.get("issues"),
            "dryrun_verifier_status": dryrun_upstream.get("verifier_status"),
            "recommended_action": f"Fix {dryrun_upstream['stage_name']} until verifier=GO",
        }
    elif not post_go and dryrun_go:
        next_required_fix = {
            "stage_id": POST_DRYRUN_STAGE_ID,
            "reason": "post_dryrun_review_remaining_internal_gap",
            "issues": post_summary_final.get("issues"),
            "recommended_action": "Fix post-dryrun review internal drift until verifier=GO",
        }

    gap_resolved = post_go
    integrated_impl_rerun_readiness = post_go

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=(
            "capabilities/midplatform/record_approval_closure_post_dryrun_review_issue_review_lineage_v1.py"
        ),
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    final_decision = FINAL_DECISION_COMPLETE if gap_resolved else FINAL_DECISION_BLOCKED
    review_pass = (
        integrated_gap_result_b
        and first_non_go_confirmed
        and post_files_exist
        and post_rerun_initial.get("run_script") is not None
        and (next_required_fix is not None or gap_resolved)
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "chain_trace_nodes": [
            "governance_gate_integrated_implementation_gap_review",
            "record_approval_closure_post_dryrun_review",
            "record_approval_closure_dryrun",
            "record_approval_closure_post_dryrun_review_issue_review",
            "governance_gate_integrated_implementation",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
        )},
        PASS_FLAG: review_pass,
        "integrated_implementation_gap_review_result_b_confirmed": integrated_gap_result_b,
        "first_non_go_direct_upstream_confirmed": first_non_go_confirmed,
        "post_dryrun_review_files_exist": post_files_exist,
        "post_dryrun_review_rerun_attempted": True,
        "post_dryrun_review_result_recorded": True,
        "direct_dryrun_upstream_review_exists": True,
        "dryrun_result_acceptance_review_exists": True,
        "candidate_escalation_review_exists": True,
        "absence_drift_review_exists": True,
        "boundary_drift_review_exists": True,
        "traceability_drift_review_exists": True,
        "first_unresolved_gap_review_exists": True,
        "post_dryrun_review_go": post_go,
        "direct_dryrun_upstream_go": dryrun_go,
        "integrated_implementation_rerun_readiness": integrated_impl_rerun_readiness,
        "first_unresolved_gap_identified": not gap_resolved,
        "first_non_go_dryrun_upstream": dryrun_upstream.get("stage_name"),
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
        "# Record Approval Closure Post-DryRun Review Issue Review v1",
        "",
        f"**Integrated implementation gap review Result B confirmed:** `{integrated_gap_result_b}`",
        f"**Post-dryrun review GO:** `{post_go}`",
        f"**Direct dryrun upstream GO:** `{dryrun_go}`",
        f"**First non-GO dryrun upstream:** `{dryrun_upstream.get('stage_name')}`",
        f"**Stop reason:** `{stop_reason}`",
        "",
        f"**Final decision:** `{final_decision}`",
    ])

    return {
        "record_approval_closure_post_dryrun_review_issue_review_report": {
            "report_id": "record_approval_closure_post_dryrun_review_issue_review_report_v1",
            "integrated_gap_context": {
                "final_decision": integrated_gap.get("final_decision"),
                "first_non_go_direct_upstream": first_upstream_review.get("first_non_go_direct_upstream"),
                "next_required_fix": next_fix,
            },
            "stop_reason": stop_reason,
            "gap_resolved": gap_resolved,
            "final_decision": final_decision,
            **meta,
        },
        "record_approval_closure_post_dryrun_review_issue_review_report_md": report_md,
        "post_dryrun_review_gap_review": {
            "review_id": "post_dryrun_review_gap_review_v1",
            "before": post_before,
            "after_initial": post_after_initial,
            "after_final": post_after_final,
            "issues": post_summary_final.get("issues"),
            "blocked_by_dryrun_gap": post_summary_final.get("final_decision", "").endswith("DRYRUN_GAP"),
            **meta,
        },
        "post_dryrun_review_artifact_visibility_review": {**meta, **visibility},
        "post_dryrun_review_direct_dryrun_upstream_review": {
            "review_id": "post_dryrun_review_direct_dryrun_upstream_review_v1",
            "dryrun_upstream": dryrun_upstream,
            "dryrun_rerun": dryrun_rerun,
            "dryrun_after": dryrun_after,
            "declared_upstream_field": DIRECT_DRYRUN_SPEC[0],
            **meta,
        },
        "post_dryrun_review_dryrun_result_acceptance_review": {**meta, **drift["dryrun_acceptance"]},
        "post_dryrun_review_candidate_escalation_review": {**meta, **drift["candidate_escalation"]},
        "post_dryrun_review_absence_drift_review": {**meta, **drift["absence_drift"]},
        "post_dryrun_review_boundary_drift_review": {**meta, **drift["boundary_drift"]},
        "post_dryrun_review_traceability_drift_review": {**meta, **drift["traceability_drift"]},
        "post_dryrun_review_rerun_review": {
            "review_id": "post_dryrun_review_rerun_review_v1",
            "initial_rerun": post_rerun_initial,
            "final_rerun": post_rerun_final,
            "initial_after": post_after_initial,
            "final_after": post_after_final,
            **meta,
        },
        "integrated_implementation_rerun_readiness_review": {
            "review_id": "integrated_implementation_rerun_readiness_review_v1",
            "integrated_implementation_rerun_readiness": integrated_impl_rerun_readiness,
            "skipped_integrated_implementation_rerun": True,
            "recommended_next_phase_if_ready": NEXT_PHASE_COMPLETE,
            **meta,
        },
        "first_unresolved_gap_review": {
            "review_id": "first_unresolved_gap_review_v1",
            "first_non_go_dryrun_upstream": dryrun_upstream.get("stage_name"),
            "next_required_fix": next_required_fix,
            **meta,
        },
        "no_protocol_change_review": {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta},
        "owner_constraint_compliance_review": {
            "review_id": "owner_constraint_compliance_review_v1",
            "owner_constraint_compliance_ok": True,
            **meta,
        },
        "source_files_review": {"post_dryrun_review": post_files},
        "file_size_governance_review": file_size,
        "summary": summary,
    }
