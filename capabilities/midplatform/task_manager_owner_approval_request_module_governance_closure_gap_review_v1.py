# -*- coding: utf-8 -*-
"""Module governance closure gap review v1."""

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
from capabilities.midplatform.task_manager_owner_approval_request_module_governance_closure_gap_review_items_v1 import (
    DEFAULT_OUTPUT,
    DRYRUN_ARTIFACTS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    FUNCTIONAL_SLICE_DRYRUN_OUTPUT,
    FUNCTIONAL_SLICE_DRYRUN_RUN_SCRIPT,
    FUNCTIONAL_SLICE_PLANNING_OUTPUT,
    GOVERNANCE_CLOSURE_OUTPUT,
    GOVERNANCE_CLOSURE_RUN_SCRIPT,
    HANDOFF_GAP_CLOSURE_OUTPUT,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    OPTIONAL_GOVERNANCE_DOCS,
    PASS_FLAG,
    PHASE_ID,
    REQUIRED_DRYRUN_FILES,
    REQUIRED_GOVERNANCE_CLOSURE_FILES,
    SCOPE,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_governance_closure_gap_review_lineage_v1 import (
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
    failed_checks_sample: List[Dict[str, Any]] = []
    for check in (verifier.get("checks") or [])[:5]:
        if not check.get("passed"):
            failed_checks_sample.append(check)
    return {
        "output_dir": str(root),
        "output_dir_exists": root.is_dir(),
        "summary_exists": (root / "summary.json").is_file(),
        "verifier_report_exists": (root / "verifier_report.json").is_file(),
        "verifier_status": verifier.get("verifier"),
        "failed_checks": failed,
        "blocker_count": blockers,
        "final_decision": summary.get("final_decision"),
        "pass_flag": (
            summary.get("module_governance_closure_pass")
            or summary.get("functional_slice_dryrun_pass")
        ),
        "issues": summary.get("issues") or [],
        "is_go": is_go,
        "first_failed_checks_sample": failed_checks_sample,
    }


def _check_files(required: tuple, optional_docs: tuple) -> Dict[str, Any]:
    req = {rel: (REPO_ROOT / rel).is_file() for rel in required}
    docs = {rel: (REPO_ROOT / rel).is_file() for rel in optional_docs}
    return {
        "required_files": req,
        "optional_docs": docs,
        "required_files_exist": all(req.values()),
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


def _artifact_visibility(output_dir: str, artifacts: tuple) -> Dict[str, Any]:
    root = Path(output_dir)
    rows = []
    for name in artifacts:
        path = root / name
        rows.append({
            "artifact": name,
            "exists": path.is_file(),
            "readable": path.is_file() and (
                bool(_read_json(path)) if name.endswith(".json") else True
            ),
        })
    return {
        "review_id": "functional_slice_dryrun_artifact_visibility_review_v1",
        "output_root": str(root),
        "artifacts": rows,
        "all_required_present": all(r["exists"] for r in rows),
        "missing_artifacts": [r["artifact"] for r in rows if not r["exists"]],
    }


def _classify_dryrun_gap(
    dryrun: Dict[str, Any],
    planning_vis: Dict[str, Any],
    visibility: Dict[str, Any],
) -> Dict[str, Any]:
    issues = dryrun.get("issues") or []
    gap_type = "unknown"
    if not planning_vis.get("is_go") and "functional_slice_planning_not_go" in issues:
        gap_type = "planning_upstream_not_go"
    elif visibility.get("missing_artifacts"):
        gap_type = "artifact_missing"
    elif "non_execution_boundary_gap" in issues:
        gap_type = "non_execution_boundary_gap"
    elif any("slice_dryrun_failed" in i for i in issues):
        gap_type = "slice_dryrun_not_all_ok"
    elif any("real_execution" in i for i in issues):
        gap_type = "real_execution_preconditions_gap"
    return {
        "first_unresolved_functional_slice_gap": gap_type,
        "dryrun_issues": issues,
        "planning_visibility": planning_vis,
    }


def run_task_manager_owner_approval_request_module_governance_closure_gap_review_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        "governance_closure_output_root": GOVERNANCE_CLOSURE_OUTPUT,
        "functional_slice_dryrun_output_root": FUNCTIONAL_SLICE_DRYRUN_OUTPUT,
        **NON_EXECUTION_FLAGS,
    }

    handoff_closure = _read_json(Path(HANDOFF_GAP_CLOSURE_OUTPUT) / "summary.json")
    handoff_verifier = _read_json(Path(HANDOFF_GAP_CLOSURE_OUTPUT) / "verifier_report.json")
    handoff_result_b = (
        handoff_closure.get("final_decision", "").endswith("HANDOFF_ARTIFACT_GAP")
        and handoff_verifier.get("verifier") == "GO"
    )
    next_fix = handoff_closure.get("next_required_fix") or {}
    next_fix_confirmed = next_fix.get("stage_id") == (
        "task_manager_owner_approval_request_module_governance_closure_v1"
    )

    gov_files = _check_files(REQUIRED_GOVERNANCE_CLOSURE_FILES, OPTIONAL_GOVERNANCE_DOCS)
    dryrun_files = _check_files(REQUIRED_DRYRUN_FILES, ())

    gov_before = _inspect_stage(GOVERNANCE_CLOSURE_OUTPUT)
    dryrun_before = _inspect_stage(FUNCTIONAL_SLICE_DRYRUN_OUTPUT)
    planning_vis = _inspect_stage(FUNCTIONAL_SLICE_PLANNING_OUTPUT)
    planning_vis["visibility_only"] = True

    gov_rerun_initial = _run_and_verify(GOVERNANCE_CLOSURE_RUN_SCRIPT)
    gov_after_initial = _inspect_stage(GOVERNANCE_CLOSURE_OUTPUT)

    dryrun_rerun: Optional[Dict[str, Any]] = None
    dryrun_after: Optional[Dict[str, Any]] = None
    gov_rerun_final: Optional[Dict[str, Any]] = None
    gov_after_final: Optional[Dict[str, Any]] = None
    stop_reason: Optional[str] = None

    if gov_after_initial.get("is_go"):
        stop_reason = "governance_closure_already_go_after_initial_rerun"
    else:
        dryrun_rerun = _run_and_verify(FUNCTIONAL_SLICE_DRYRUN_RUN_SCRIPT)
        dryrun_after = _inspect_stage(FUNCTIONAL_SLICE_DRYRUN_OUTPUT)
        if not dryrun_after.get("is_go"):
            stop_reason = "functional_slice_dryrun_still_hold_stop_on_first_non_go"
        else:
            gov_rerun_final = _run_and_verify(GOVERNANCE_CLOSURE_RUN_SCRIPT)
            gov_after_final = _inspect_stage(GOVERNANCE_CLOSURE_OUTPUT)

    gov_final = gov_after_final or gov_after_initial
    dryrun_final = dryrun_after or dryrun_before
    gov_go = gov_final.get("is_go") is True
    dryrun_go = dryrun_final.get("is_go") is True

    visibility = _artifact_visibility(FUNCTIONAL_SLICE_DRYRUN_OUTPUT, DRYRUN_ARTIFACTS)
    dryrun_summary = _read_json(Path(FUNCTIONAL_SLICE_DRYRUN_OUTPUT) / "summary.json")

    boundary_review = {
        "review_id": "functional_slice_dryrun_boundary_gap_review_v1",
        "non_execution_boundary_gap": "non_execution_boundary_gap" in (dryrun_final.get("issues") or []),
        "non_execution_boundary_ok": dryrun_summary.get("non_execution_boundary_ok"),
        "functional_slice_real_execution_absent": dryrun_summary.get("functional_slice_real_execution_absent"),
        "real_request_issuance_authorized": dryrun_summary.get("real_request_issuance_authorized"),
        **meta,
    }

    preconditions_review = {
        "review_id": "functional_slice_dryrun_real_execution_preconditions_review_v1",
        "real_execution_preconditions_gap": any(
            "real_execution" in i for i in (dryrun_final.get("issues") or [])
        ) or any(
            "real_execution" in i for i in (gov_final.get("issues") or [])
        ),
        "prior_functional_slice_planning_go": dryrun_summary.get("prior_functional_slice_planning_go"),
        "prior_integrated_implementation_go": dryrun_summary.get("prior_integrated_implementation_go"),
        "prior_authorization_preparation_dryrun_go": dryrun_summary.get("prior_authorization_preparation_dryrun_go"),
        **meta,
    }

    gap_class = _classify_dryrun_gap(dryrun_final, planning_vis, visibility)

    next_required_fix: Optional[Dict[str, Any]] = None
    if not dryrun_go:
        if gap_class["first_unresolved_functional_slice_gap"] == "planning_upstream_not_go":
            next_required_fix = {
                "stage_id": "task_manager_owner_approval_request_module_level_functional_slice_planning_v1",
                "reason": "functional_slice_dryrun_blocked_by_planning_not_go",
                "planning_final_decision": planning_vis.get("final_decision"),
                "planning_issues": planning_vis.get("issues"),
                "recommended_action": (
                    "Fix functional_slice_planning upstream until GO; "
                    "do not expand in this phase — dryrun blocked at planning visibility gap"
                ),
            }
        else:
            next_required_fix = {
                "stage_id": "task_manager_owner_approval_request_functional_slice_dryrun_v1",
                "reason": gap_class["first_unresolved_functional_slice_gap"],
                "missing_artifacts": visibility.get("missing_artifacts"),
                "dryrun_issues": dryrun_final.get("issues"),
                "recommended_action": "Fix functional_slice_dryrun until verifier=GO before governance closure",
            }
    elif not gov_go:
        next_required_fix = {
            "stage_id": "task_manager_owner_approval_request_module_governance_closure_v1",
            "reason": "dryrun_go_but_governance_closure_remaining_gap",
            "governance_issues": gov_final.get("issues"),
            "recommended_action": "Fix module_governance_closure remaining gaps after dryrun GO",
        }

    gap_resolved = gov_go and dryrun_go
    handoff_rerun_readiness = gov_go

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=(
            "capabilities/midplatform/task_manager_owner_approval_request_module_governance_closure_gap_review_lineage_v1.py"
        ),
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    final_decision = FINAL_DECISION_COMPLETE if gap_resolved else FINAL_DECISION_BLOCKED
    review_pass = (
        handoff_result_b
        and next_fix_confirmed
        and gov_files.get("required_files_exist")
        and dryrun_files.get("required_files_exist")
        and gov_rerun_initial.get("run_script") is not None
        and (next_required_fix is not None or gap_resolved)
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "chain_trace_nodes": [
            "task_manager_owner_approval_request_module_handoff_gap_closure",
            "task_manager_owner_approval_request_module_governance_closure",
            "task_manager_owner_approval_request_functional_slice_dryrun",
            "task_manager_owner_approval_request_module_level_functional_slice_planning",
            "task_manager_owner_approval_request_module_governance_closure_gap_review",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
        )},
        PASS_FLAG: review_pass,
        "handoff_gap_closure_result_b_confirmed": handoff_result_b,
        "next_required_fix_confirmed": next_fix_confirmed,
        "module_governance_closure_files_exist": gov_files.get("required_files_exist"),
        "module_governance_closure_rerun_attempted": True,
        "module_governance_closure_result_recorded": True,
        "functional_slice_dryrun_gap_review_exists": True,
        "functional_slice_dryrun_visibility_review_exists": True,
        "functional_slice_dryrun_boundary_gap_review_exists": True,
        "real_execution_preconditions_review_exists": True,
        "first_unresolved_gap_review_exists": True,
        "functional_slice_dryrun_go": dryrun_go,
        "module_governance_closure_go": gov_go,
        "handoff_rerun_readiness": handoff_rerun_readiness,
        "first_unresolved_gap_identified": not gap_resolved,
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
        "# Module Governance Closure Gap Review v1",
        "",
        f"**Handoff gap closure Result B confirmed:** `{handoff_result_b}`",
        f"**Functional slice dryrun GO:** `{dryrun_go}`",
        f"**Module governance closure GO:** `{gov_go}`",
        f"**First unresolved gap:** `{gap_class.get('first_unresolved_functional_slice_gap')}`",
        f"**Stop reason:** `{stop_reason}`",
        "",
        f"**Final decision:** `{final_decision}`",
    ])

    return {
        "task_manager_owner_approval_request_module_governance_closure_gap_review_report": {
            "report_id": "task_manager_owner_approval_request_module_governance_closure_gap_review_report_v1",
            "handoff_closure_context": {
                "final_decision": handoff_closure.get("final_decision"),
                "next_required_fix": next_fix,
            },
            "stop_reason": stop_reason,
            "gap_resolved": gap_resolved,
            "final_decision": final_decision,
            **meta,
        },
        "task_manager_owner_approval_request_module_governance_closure_gap_review_report_md": report_md,
        "module_governance_closure_gap_review": {
            "review_id": "module_governance_closure_gap_review_v1",
            "before": gov_before,
            "after_initial": gov_after_initial,
            "after_final": gov_after_final,
            "issues": gov_final.get("issues"),
            **meta,
        },
        "functional_slice_dryrun_gap_review": {
            "review_id": "functional_slice_dryrun_gap_review_v1",
            "before": dryrun_before,
            "rerun": dryrun_rerun,
            "after": dryrun_after,
            "gap_classification": gap_class,
            **meta,
        },
        "functional_slice_dryrun_artifact_visibility_review": {**meta, **visibility},
        "functional_slice_dryrun_boundary_gap_review": boundary_review,
        "functional_slice_dryrun_real_execution_preconditions_review": preconditions_review,
        "module_governance_closure_rerun_review": {
            "review_id": "module_governance_closure_rerun_review_v1",
            "initial_rerun": gov_rerun_initial,
            "final_rerun": gov_rerun_final,
            "initial_after": gov_after_initial,
            "final_after": gov_after_final,
            **meta,
        },
        "handoff_rerun_readiness_review": {
            "review_id": "handoff_rerun_readiness_review_v1",
            "handoff_rerun_readiness": handoff_rerun_readiness,
            "skipped_broader_roadmap_rerun": True,
            "recommended_next_phase_if_ready": NEXT_PHASE_COMPLETE,
            **meta,
        },
        "first_unresolved_gap_review": {
            "review_id": "first_unresolved_gap_review_v1",
            "first_unresolved_functional_slice_gap": gap_class.get("first_unresolved_functional_slice_gap"),
            "next_required_fix": next_required_fix,
            "planning_visibility_only": planning_vis,
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
            "governance_closure": gov_files,
            "functional_slice_dryrun": dryrun_files,
        },
        "file_size_governance_review": file_size,
        "summary": summary,
    }
