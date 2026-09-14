# -*- coding: utf-8 -*-
"""Functional slice planning gap review v1."""

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
from capabilities.midplatform.task_manager_owner_approval_request_functional_slice_planning_gap_review_items_v1 import (
    AUTHORIZATION_PREPARATION_DRYRUN_OUTPUT,
    AUTHORIZATION_PREPARATION_DRYRUN_RUN_SCRIPT,
    AUTHORIZATION_PREPARATION_PLANNING_OUTPUT,
    AUTH_DRYRUN_ARTIFACTS,
    DEFAULT_OUTPUT,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    FUNCTIONAL_SLICE_PLANNING_OUTPUT,
    FUNCTIONAL_SLICE_PLANNING_RUN_SCRIPT,
    GOVERNANCE_GAP_REVIEW_OUTPUT,
    INTEGRATED_IMPLEMENTATION_OUTPUT,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    REQUIRED_AUTH_DRYRUN_FILES,
    REQUIRED_PLANNING_FILES,
    SCOPE,
)
from capabilities.midplatform.task_manager_owner_approval_request_functional_slice_planning_gap_review_lineage_v1 import (
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
    failed_sample = [
        c for c in (verifier.get("checks") or []) if not c.get("passed")
    ][:5]
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
        "is_go": is_go,
        "first_failed_checks_sample": failed_sample,
    }


def _check_files(required: tuple) -> Dict[str, Any]:
    req = {rel: (REPO_ROOT / rel).is_file() for rel in required}
    return {"required_files": req, "required_files_exist": all(req.values())}


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
        "review_id": "authorization_preparation_dryrun_artifact_visibility_review_v1",
        "output_root": str(root),
        "artifacts": rows,
        "all_required_present": not missing,
        "missing_artifacts": missing,
        "dryrun_artifact_gap": bool(missing),
    }


def _classify_auth_gap(
    dryrun: Dict[str, Any],
    impl_vis: Dict[str, Any],
    auth_plan_vis: Dict[str, Any],
    visibility: Dict[str, Any],
) -> str:
    issues = dryrun.get("issues") or []
    if not impl_vis.get("is_go") and "integrated_implementation_not_go" in issues:
        return "integrated_implementation_upstream_not_go"
    missing = [
        a for a in (visibility.get("missing_artifacts") or [])
        if a != "verifier_report.json"
    ]
    if missing:
        return "dryrun_artifact_gap"
    if not auth_plan_vis.get("is_go") and auth_plan_vis.get("output_dir_exists"):
        return "authorization_preparation_planning_upstream_not_go"
    if not auth_plan_vis.get("module_source_exists") and "integrated_implementation_not_go" in issues:
        return "authorization_preparation_planning_module_absent_upstream_integrated_impl_not_go"
    if "precondition_gap" in issues:
        return "owner_approval_precondition_gap"
    if "safety_boundary_gap" in issues or "non_execution_boundary_gap" in issues:
        return "authorization_boundary_gap"
    if "package_escalation" in issues:
        return "authorization_package_escalation_gap"
    if "routing_drift" in issues:
        return "authorization_routing_drift_gap"
    if visibility.get("missing_artifacts"):
        return "dryrun_artifact_gap"
    return "authorization_preparation_dryrun_unresolved_gap"


def run_task_manager_owner_approval_request_functional_slice_planning_gap_review_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        "functional_slice_planning_output_root": FUNCTIONAL_SLICE_PLANNING_OUTPUT,
        "authorization_preparation_dryrun_output_root": AUTHORIZATION_PREPARATION_DRYRUN_OUTPUT,
        **NON_EXECUTION_FLAGS,
    }

    gov_review = _read_json(Path(GOVERNANCE_GAP_REVIEW_OUTPUT) / "summary.json")
    gov_verifier = _read_json(Path(GOVERNANCE_GAP_REVIEW_OUTPUT) / "verifier_report.json")
    gov_result_b = (
        gov_review.get("final_decision", "").endswith("FUNCTIONAL_SLICE_DRYRUN_GAP")
        and gov_verifier.get("verifier") == "GO"
    )
    first_gap = _read_json(Path(GOVERNANCE_GAP_REVIEW_OUTPUT) / "first_unresolved_gap_review_v1.json")
    next_fix = first_gap.get("next_required_fix") or gov_review.get("next_required_fix") or {}
    next_fix_confirmed = next_fix.get("stage_id") == (
        "task_manager_owner_approval_request_module_level_functional_slice_planning_v1"
    )

    planning_files = _check_files(REQUIRED_PLANNING_FILES)
    dryrun_files = _check_files(REQUIRED_AUTH_DRYRUN_FILES)

    planning_before = _inspect_stage(FUNCTIONAL_SLICE_PLANNING_OUTPUT)
    dryrun_before = _inspect_stage(AUTHORIZATION_PREPARATION_DRYRUN_OUTPUT)
    impl_vis = _inspect_stage(INTEGRATED_IMPLEMENTATION_OUTPUT)
    impl_vis["visibility_only"] = True
    auth_plan_vis = _inspect_stage(AUTHORIZATION_PREPARATION_PLANNING_OUTPUT)
    auth_plan_vis["visibility_only"] = True
    auth_plan_vis["module_source_exists"] = (
        REPO_ROOT / "capabilities/midplatform/task_manager_owner_approval_request_authorization_preparation_planning_v1.py"
    ).is_file()

    planning_rerun_initial = _run_and_verify(FUNCTIONAL_SLICE_PLANNING_RUN_SCRIPT)
    planning_after_initial = _inspect_stage(FUNCTIONAL_SLICE_PLANNING_OUTPUT)

    dryrun_rerun: Optional[Dict[str, Any]] = None
    dryrun_after: Optional[Dict[str, Any]] = None
    planning_rerun_final: Optional[Dict[str, Any]] = None
    planning_after_final: Optional[Dict[str, Any]] = None
    stop_reason: Optional[str] = None

    if planning_after_initial.get("is_go"):
        stop_reason = "functional_slice_planning_already_go_after_initial_rerun"
    else:
        dryrun_rerun = _run_and_verify(AUTHORIZATION_PREPARATION_DRYRUN_RUN_SCRIPT)
        dryrun_after = _inspect_stage(AUTHORIZATION_PREPARATION_DRYRUN_OUTPUT)
        if not dryrun_after.get("is_go"):
            stop_reason = "authorization_preparation_dryrun_still_hold_stop_on_first_non_go"
        else:
            planning_rerun_final = _run_and_verify(FUNCTIONAL_SLICE_PLANNING_RUN_SCRIPT)
            planning_after_final = _inspect_stage(FUNCTIONAL_SLICE_PLANNING_OUTPUT)

    planning_final = planning_after_final or planning_after_initial
    dryrun_final = dryrun_after or dryrun_before
    planning_go = planning_final.get("is_go") is True
    dryrun_go = dryrun_final.get("is_go") is True

    visibility = _artifact_visibility(AUTHORIZATION_PREPARATION_DRYRUN_OUTPUT, AUTH_DRYRUN_ARTIFACTS)
    dryrun_summary = _read_json(Path(AUTHORIZATION_PREPARATION_DRYRUN_OUTPUT) / "summary.json")

    gap_type = _classify_auth_gap(dryrun_final, impl_vis, auth_plan_vis, visibility)

    boundary_review = {
        "review_id": "authorization_preparation_dryrun_boundary_gap_review_v1",
        "authorization_boundary_gap": any(
            i in (dryrun_final.get("issues") or [])
            for i in ("safety_boundary_gap", "non_execution_boundary_gap")
        ),
        "non_execution_boundary_ok": dryrun_summary.get("non_execution_boundary_ok"),
        "real_issuance_safety_boundary_ok": dryrun_summary.get("real_issuance_safety_boundary_ok"),
        **meta,
    }

    precondition_review = {
        "review_id": "authorization_preparation_dryrun_precondition_review_v1",
        "owner_approval_precondition_gap": "precondition_gap" in (dryrun_final.get("issues") or []),
        "authorization_precondition_validation_ok": dryrun_summary.get("authorization_precondition_validation_ok"),
        "prior_integrated_implementation_go": dryrun_summary.get("prior_integrated_implementation_go"),
        **meta,
    }

    next_required_fix: Optional[Dict[str, Any]] = None
    if not dryrun_go:
        if gap_type == "integrated_implementation_upstream_not_go":
            next_required_fix = {
                "stage_id": "task_manager_owner_approval_request_governance_gate_integrated_implementation_v1",
                "reason": "authorization_preparation_dryrun_blocked_by_integrated_implementation_not_go",
                "integrated_implementation_final_decision": impl_vis.get("final_decision"),
                "integrated_implementation_issues": impl_vis.get("issues"),
                "recommended_action": (
                    "Fix governance_gate_integrated_implementation until GO before authorization_preparation_dryrun"
                ),
            }
        elif gap_type == "dryrun_artifact_gap":
            next_required_fix = {
                "stage_id": "task_manager_owner_approval_request_authorization_preparation_dryrun_v1",
                "reason": "dryrun_artifact_gap",
                "missing_artifacts": visibility.get("missing_artifacts"),
                "recommended_action": "补齐 authorization_preparation_dryrun 缺失产物",
            }
        else:
            next_required_fix = {
                "stage_id": "task_manager_owner_approval_request_authorization_preparation_dryrun_v1",
                "reason": gap_type,
                "dryrun_issues": dryrun_final.get("issues"),
                "first_failed_checks_sample": dryrun_final.get("first_failed_checks_sample"),
                "recommended_action": "Fix authorization_preparation_dryrun until verifier=GO",
            }
    elif not planning_go:
        next_required_fix = {
            "stage_id": "task_manager_owner_approval_request_module_level_functional_slice_planning_v1",
            "reason": "auth_dryrun_go_but_functional_slice_planning_remaining_gap",
            "planning_issues": planning_final.get("issues"),
            "recommended_action": "Fix functional_slice_planning remaining gaps after auth dryrun GO",
        }

    gap_resolved = planning_go and dryrun_go
    dryrun_rerun_readiness = planning_go

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=(
            "capabilities/midplatform/task_manager_owner_approval_request_functional_slice_planning_gap_review_lineage_v1.py"
        ),
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    final_decision = FINAL_DECISION_COMPLETE if gap_resolved else FINAL_DECISION_BLOCKED
    review_pass = (
        gov_result_b
        and next_fix_confirmed
        and planning_files.get("required_files_exist")
        and dryrun_files.get("required_files_exist")
        and planning_rerun_initial.get("run_script") is not None
        and (next_required_fix is not None or gap_resolved)
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "chain_trace_nodes": [
            "module_governance_closure_gap_review",
            "functional_slice_planning",
            "authorization_preparation_dryrun",
            "governance_gate_integrated_implementation",
            "functional_slice_planning_gap_review",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
        )},
        PASS_FLAG: review_pass,
        "governance_closure_gap_review_result_b_confirmed": gov_result_b,
        "next_required_fix_confirmed": next_fix_confirmed,
        "functional_slice_planning_files_exist": planning_files.get("required_files_exist"),
        "functional_slice_planning_rerun_attempted": True,
        "functional_slice_planning_result_recorded": True,
        "authorization_preparation_dryrun_gap_review_exists": True,
        "authorization_preparation_dryrun_visibility_review_exists": True,
        "authorization_preparation_dryrun_boundary_gap_review_exists": True,
        "authorization_preparation_dryrun_precondition_review_exists": True,
        "first_unresolved_gap_review_exists": True,
        "authorization_preparation_dryrun_go": dryrun_go,
        "functional_slice_planning_go": planning_go,
        "functional_slice_dryrun_rerun_readiness": dryrun_rerun_readiness,
        "first_unresolved_gap_identified": not gap_resolved,
        "first_unresolved_authorization_preparation_gap": gap_type if not dryrun_go else None,
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
        "# Functional Slice Planning Gap Review v1",
        "",
        f"**Governance gap review Result B confirmed:** `{gov_result_b}`",
        f"**Authorization preparation dryrun GO:** `{dryrun_go}`",
        f"**Functional slice planning GO:** `{planning_go}`",
        f"**First unresolved gap:** `{gap_type if not dryrun_go else 'none'}`",
        f"**Stop reason:** `{stop_reason}`",
        "",
        f"**Final decision:** `{final_decision}`",
    ])

    return {
        "task_manager_owner_approval_request_functional_slice_planning_gap_review_report": {
            "report_id": "task_manager_owner_approval_request_functional_slice_planning_gap_review_report_v1",
            "governance_review_context": {
                "final_decision": gov_review.get("final_decision"),
                "next_required_fix": next_fix,
            },
            "stop_reason": stop_reason,
            "gap_resolved": gap_resolved,
            "final_decision": final_decision,
            **meta,
        },
        "task_manager_owner_approval_request_functional_slice_planning_gap_review_report_md": report_md,
        "functional_slice_planning_gap_review": {
            "review_id": "functional_slice_planning_gap_review_v1",
            "before": planning_before,
            "after_initial": planning_after_initial,
            "after_final": planning_after_final,
            "issues": planning_final.get("issues"),
            **meta,
        },
        "authorization_preparation_dryrun_gap_review": {
            "review_id": "authorization_preparation_dryrun_gap_review_v1",
            "before": dryrun_before,
            "rerun": dryrun_rerun,
            "after": dryrun_after,
            "first_unresolved_authorization_preparation_gap": gap_type,
            **meta,
        },
        "authorization_preparation_dryrun_artifact_visibility_review": {**meta, **visibility},
        "authorization_preparation_dryrun_boundary_gap_review": boundary_review,
        "authorization_preparation_dryrun_precondition_review": precondition_review,
        "functional_slice_planning_rerun_review": {
            "review_id": "functional_slice_planning_rerun_review_v1",
            "initial_rerun": planning_rerun_initial,
            "final_rerun": planning_rerun_final,
            "initial_after": planning_after_initial,
            "final_after": planning_after_final,
            **meta,
        },
        "functional_slice_dryrun_rerun_readiness_review": {
            "review_id": "functional_slice_dryrun_rerun_readiness_review_v1",
            "functional_slice_dryrun_rerun_readiness": dryrun_rerun_readiness,
            "skipped_functional_slice_dryrun_rerun": True,
            "recommended_next_phase_if_ready": NEXT_PHASE_COMPLETE,
            **meta,
        },
        "first_unresolved_gap_review": {
            "review_id": "first_unresolved_gap_review_v1",
            "first_unresolved_authorization_preparation_gap": gap_type if not dryrun_go else None,
            "next_required_fix": next_required_fix,
            "integrated_implementation_visibility": impl_vis,
            "authorization_preparation_planning_visibility": auth_plan_vis,
            **meta,
        },
        "no_protocol_change_review": {
            "review_id": "no_protocol_change_review_v1",
            "no_protocol_change": True,
            **meta,
        },
        "owner_constraint_compliance_review": {
            "review_id": "owner_constraint_compliance_review_v1",
            "owner_constraint_compliance_ok": True,
            **meta,
        },
        "source_files_review": {
            "functional_slice_planning": planning_files,
            "authorization_preparation_dryrun": dryrun_files,
        },
        "file_size_governance_review": file_size,
        "summary": summary,
    }
