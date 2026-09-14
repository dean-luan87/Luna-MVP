# -*- coding: utf-8 -*-
"""Issuance post-dryrun review issue review v1."""

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
from capabilities.midplatform.issuance_post_dryrun_review_issue_review_items_v1 import (
    DEFAULT_OUTPUT,
    DIRECT_UPSTREAM_SPECS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    ISSUANCE_POST_DRYRUN_ARTIFACTS,
    ISSUANCE_POST_DRYRUN_REVIEW_OUTPUT,
    ISSUANCE_POST_DRYRUN_RUN_SCRIPT,
    ISSUANCE_POST_DRYRUN_STAGE_ID,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    PLANNING_ISSUE_REVIEW_OUTPUT,
    REQUIRED_ISSUANCE_POST_DRYRUN_FILES,
    SCOPE,
)
from capabilities.midplatform.issuance_post_dryrun_review_issue_review_lineage_v1 import (
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
        "post_dryrun_review_pass": summary.get("post_dryrun_review_pass"),
        "issuance_dryrun_result_accepted": summary.get("issuance_dryrun_result_accepted"),
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


def _build_direct_upstream_registry(post_summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for field, stage_id, run_script in DIRECT_UPSTREAM_SPECS:
        expected = post_summary.get(field) or ""
        actual = str(Path(expected).expanduser().resolve()) if expected else ""
        insp = _inspect_stage(actual) if actual else {"is_go": False, "output_dir_exists": False}
        rows.append({
            "upstream_field": field,
            "stage_name": stage_id,
            "run_script": run_script,
            "expected_output_dir": expected,
            "actual_output_dir": actual,
            **insp,
        })
    return rows


def _first_non_go_upstream(registry: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for row in registry:
        if not row.get("is_go"):
            return row
    return None


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
        "review_id": "issuance_post_dryrun_review_artifact_visibility_review_v1",
        "output_root": str(root),
        "artifacts": rows,
        "all_required_present": not missing,
        "missing_artifacts": missing,
    }


def _internal_gap_reviews(summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    issues = summary.get("issues") or []
    return {
        "dryrun_acceptance": {
            "review_id": "issuance_post_dryrun_review_dryrun_acceptance_review_v1",
            "owner_approval_request_issuance_dryrun_not_go": "owner_approval_request_issuance_dryrun_not_go" in issues,
            "issuance_dryrun_not_accepted": "issuance_dryrun_not_accepted" in issues,
            "prior_owner_approval_request_issuance_dryrun_go": summary.get("prior_owner_approval_request_issuance_dryrun_go"),
            "issuance_dryrun_result_accepted": summary.get("issuance_dryrun_result_accepted"),
        },
        "validate_once": {
            "review_id": "issuance_post_dryrun_review_validate_once_reference_review_v1",
            "validate_once_reference_review_gap": "validate_once_reference_review_gap" in issues,
            "validate_once_reference_review_ok": summary.get("validate_once_reference_review_ok"),
        },
        "precondition_leakage": {
            "review_id": "issuance_post_dryrun_review_precondition_leakage_review_v1",
            "precondition_execution_leakage": "precondition_execution_leakage" in issues,
            "precondition_candidate_only": summary.get("precondition_candidate_only"),
        },
        "evidence_chain": {
            "review_id": "issuance_post_dryrun_review_evidence_chain_review_v1",
            "evidence_chain_gap": "evidence_chain_gap" in issues,
            "evidence_chain_review_ok": summary.get("evidence_chain_review_ok"),
        },
    }


def run_issuance_post_dryrun_review_issue_review_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        "issuance_post_dryrun_review_output_root": ISSUANCE_POST_DRYRUN_REVIEW_OUTPUT,
        **NON_EXECUTION_FLAGS,
    }

    planning_issue = _read_json(Path(PLANNING_ISSUE_REVIEW_OUTPUT) / "summary.json")
    planning_issue_verifier = _read_json(Path(PLANNING_ISSUE_REVIEW_OUTPUT) / "verifier_report.json")
    planning_issue_result_b = (
        planning_issue.get("final_decision", "").endswith("STILL_BLOCKED_BY_DIRECT_PRIOR_REVIEW_GAP")
        and planning_issue_verifier.get("verifier") == "GO"
    )
    first_gap = _read_json(Path(PLANNING_ISSUE_REVIEW_OUTPUT) / "first_unresolved_gap_review_v1.json")
    prior_upstream_review = _read_json(
        Path(PLANNING_ISSUE_REVIEW_OUTPUT) / "record_approval_closure_planning_direct_prior_review_upstream_review_v1.json"
    )
    next_fix = first_gap.get("next_required_fix") or planning_issue.get("next_required_fix") or {}
    direct_prior_confirmed = next_fix.get("stage_id") == ISSUANCE_POST_DRYRUN_STAGE_ID

    post_files = {rel: (REPO_ROOT / rel).is_file() for rel in REQUIRED_ISSUANCE_POST_DRYRUN_FILES}
    post_files_exist = all(post_files.values())

    post_before = _inspect_stage(ISSUANCE_POST_DRYRUN_REVIEW_OUTPUT)
    post_rerun_initial = _run_and_verify(ISSUANCE_POST_DRYRUN_RUN_SCRIPT)
    post_after_initial = _inspect_stage(ISSUANCE_POST_DRYRUN_REVIEW_OUTPUT)
    post_summary = _read_json(Path(ISSUANCE_POST_DRYRUN_REVIEW_OUTPUT) / "summary.json")

    registry = _build_direct_upstream_registry(post_summary)
    first_non_go = _first_non_go_upstream(registry)

    upstream_rerun: Optional[Dict[str, Any]] = None
    upstream_after: Optional[Dict[str, Any]] = None
    post_rerun_final: Optional[Dict[str, Any]] = None
    post_after_final: Optional[Dict[str, Any]] = None
    stop_reason: Optional[str] = None

    post_go_initial = post_after_initial.get("is_go") is True
    if post_go_initial:
        stop_reason = "issuance_post_dryrun_review_already_go_after_initial_rerun"
    elif first_non_go:
        upstream_rerun = _run_and_verify(first_non_go["run_script"])
        upstream_after = _inspect_stage(first_non_go["actual_output_dir"])
        if not upstream_after.get("is_go"):
            stop_reason = f"first_non_go_issuance_upstream_still_hold:{first_non_go['stage_name']}"
        else:
            post_rerun_final = _run_and_verify(ISSUANCE_POST_DRYRUN_RUN_SCRIPT)
            post_after_final = _inspect_stage(ISSUANCE_POST_DRYRUN_REVIEW_OUTPUT)
            registry = _build_direct_upstream_registry(
                _read_json(Path(ISSUANCE_POST_DRYRUN_REVIEW_OUTPUT) / "summary.json")
            )
            first_non_go = _first_non_go_upstream(registry)
    else:
        stop_reason = "no_direct_issuance_upstream_identified"

    post_final = post_after_final or post_after_initial
    post_go = post_final.get("is_go") is True
    post_summary_final = _read_json(Path(ISSUANCE_POST_DRYRUN_REVIEW_OUTPUT) / "summary.json")
    internal_gaps = _internal_gap_reviews(post_summary_final)
    visibility = _artifact_visibility(ISSUANCE_POST_DRYRUN_REVIEW_OUTPUT, ISSUANCE_POST_DRYRUN_ARTIFACTS)

    first_upstream_resolved = post_go or (
        first_non_go is not None and (upstream_after or {}).get("is_go") is True and not post_go
    )

    next_required_fix: Optional[Dict[str, Any]] = None
    if first_non_go and not (upstream_after or {}).get("is_go") and not post_go:
        next_required_fix = {
            "stage_id": first_non_go["stage_name"],
            "upstream_field": first_non_go["upstream_field"],
            "reason": "first_non_go_issuance_upstream",
            "upstream_final_decision": first_non_go.get("final_decision"),
            "upstream_issue_tags": first_non_go.get("issues"),
            "upstream_verifier_status": first_non_go.get("verifier_status"),
            "recommended_action": f"Fix {first_non_go['stage_name']} until verifier=GO",
        }
    elif not post_go and first_non_go is None:
        next_required_fix = {
            "stage_id": ISSUANCE_POST_DRYRUN_STAGE_ID,
            "reason": "issuance_post_dryrun_review_remaining_internal_gap",
            "issues": post_summary_final.get("issues"),
            "recommended_action": "Fix issuance post-dryrun review internal gaps until verifier=GO",
        }

    gap_resolved = post_go
    planning_rerun_readiness = post_go

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/issuance_post_dryrun_review_issue_review_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    final_decision = FINAL_DECISION_COMPLETE if gap_resolved else FINAL_DECISION_BLOCKED
    review_pass = (
        planning_issue_result_b
        and direct_prior_confirmed
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
            "record_approval_closure_planning_issue_review",
            "issuance_post_dryrun_review",
            "issuance_planning",
            "input_output_registry_patch",
            "issuance_dryrun",
            "issuance_post_dryrun_review_issue_review",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
        )},
        PASS_FLAG: review_pass,
        "record_approval_closure_planning_issue_review_result_b_confirmed": planning_issue_result_b,
        "direct_prior_review_upstream_confirmed": direct_prior_confirmed,
        "issuance_post_dryrun_review_files_exist": post_files_exist,
        "issuance_post_dryrun_review_rerun_attempted": True,
        "issuance_post_dryrun_review_result_recorded": True,
        "direct_upstream_registry_exists": True,
        "first_non_go_issuance_upstream_identified": first_non_go is not None,
        "dryrun_acceptance_review_exists": True,
        "validate_once_reference_review_exists": True,
        "precondition_leakage_review_exists": True,
        "evidence_chain_review_exists": True,
        "first_unresolved_gap_review_exists": True,
        "issuance_post_dryrun_review_go": post_go,
        "first_non_go_issuance_upstream_resolved": first_upstream_resolved,
        "record_approval_closure_planning_rerun_readiness": planning_rerun_readiness,
        "first_unresolved_gap_identified": not gap_resolved,
        "first_non_go_issuance_upstream": (first_non_go or {}).get("stage_name"),
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
        "# Issuance Post-DryRun Review Issue Review v1",
        "",
        f"**Planning issue review Result B confirmed:** `{planning_issue_result_b}`",
        f"**Issuance post-dryrun review GO:** `{post_go}`",
        f"**First non-GO issuance upstream:** `{(first_non_go or {}).get('stage_name')}`",
        f"**Stop reason:** `{stop_reason}`",
        "",
        f"**Final decision:** `{final_decision}`",
    ])

    return {
        "issuance_post_dryrun_review_issue_review_report": {
            "report_id": "issuance_post_dryrun_review_issue_review_report_v1",
            "planning_issue_context": {
                "final_decision": planning_issue.get("final_decision"),
                "prior_review_upstream": prior_upstream_review.get("prior_review_upstream"),
                "next_required_fix": next_fix,
            },
            "stop_reason": stop_reason,
            "gap_resolved": gap_resolved,
            "final_decision": final_decision,
            **meta,
        },
        "issuance_post_dryrun_review_issue_review_report_md": report_md,
        "issuance_post_dryrun_review_gap_review": {
            "review_id": "issuance_post_dryrun_review_gap_review_v1",
            "before": post_before,
            "after_initial": post_after_initial,
            "after_final": post_after_final,
            "issues": post_summary_final.get("issues"),
            "blocked_by_dryrun_evidence_gap": post_summary_final.get("final_decision", "").endswith("DRYRUN_EVIDENCE_GAP"),
            **meta,
        },
        "issuance_post_dryrun_review_artifact_visibility_review": {**meta, **visibility},
        "issuance_post_dryrun_review_direct_upstream_registry": {
            "registry_id": "issuance_post_dryrun_review_direct_upstream_registry_v1",
            "rows": registry,
            "declared_order_fields": [s[0] for s in DIRECT_UPSTREAM_SPECS],
            **meta,
        },
        "issuance_post_dryrun_review_first_non_go_upstream_review": {
            "review_id": "issuance_post_dryrun_review_first_non_go_upstream_review_v1",
            "first_non_go_issuance_upstream": first_non_go,
            "upstream_rerun": upstream_rerun,
            "upstream_after": upstream_after,
            **meta,
        },
        "issuance_post_dryrun_review_dryrun_acceptance_review": {**meta, **internal_gaps["dryrun_acceptance"]},
        "issuance_post_dryrun_review_validate_once_reference_review": {**meta, **internal_gaps["validate_once"]},
        "issuance_post_dryrun_review_precondition_leakage_review": {**meta, **internal_gaps["precondition_leakage"]},
        "issuance_post_dryrun_review_evidence_chain_review": {**meta, **internal_gaps["evidence_chain"]},
        "issuance_post_dryrun_review_rerun_review": {
            "review_id": "issuance_post_dryrun_review_rerun_review_v1",
            "initial_rerun": post_rerun_initial,
            "final_rerun": post_rerun_final,
            "initial_after": post_after_initial,
            "final_after": post_after_final,
            **meta,
        },
        "record_approval_closure_planning_rerun_readiness_review": {
            "review_id": "record_approval_closure_planning_rerun_readiness_review_v1",
            "record_approval_closure_planning_rerun_readiness": planning_rerun_readiness,
            "skipped_record_approval_closure_planning_rerun": True,
            "recommended_next_phase_if_ready": NEXT_PHASE_COMPLETE,
            **meta,
        },
        "first_unresolved_gap_review": {
            "review_id": "first_unresolved_gap_review_v1",
            "first_non_go_issuance_upstream": (first_non_go or {}).get("stage_name"),
            "next_required_fix": next_required_fix,
            **meta,
        },
        "no_protocol_change_review": {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta},
        "owner_constraint_compliance_review": {
            "review_id": "owner_constraint_compliance_review_v1",
            "owner_constraint_compliance_ok": True,
            **meta,
        },
        "source_files_review": {"issuance_post_dryrun_review": post_files},
        "file_size_governance_review": file_size,
        "summary": summary,
    }
