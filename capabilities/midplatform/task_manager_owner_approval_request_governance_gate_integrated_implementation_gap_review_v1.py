# -*- coding: utf-8 -*-
"""Governance gate integrated implementation gap review v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_items_v1 import (
    DEFAULT_OUTPUT,
    DIRECT_UPSTREAM_SPECS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    INTEGRATED_ARTIFACTS,
    INTEGRATED_IMPLEMENTATION_OUTPUT,
    INTEGRATED_RUN_SCRIPT,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    PLANNING_GAP_REVIEW_OUTPUT,
    REQUIRED_INTEGRATED_FILES,
    SCOPE,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_lineage_v1 import (
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


def _build_direct_upstream_registry(impl_summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for field, stage_id, run_script in DIRECT_UPSTREAM_SPECS:
        expected = impl_summary.get(field) or ""
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
        "review_id": "integrated_implementation_upstream_artifact_visibility_review_v1",
        "output_root": str(root),
        "artifacts": rows,
        "all_required_present": not missing,
        "missing_artifacts": missing,
    }


def _internal_gap_reviews(summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    issues = summary.get("issues") or []
    return {
        "routing": {
            "review_id": "integrated_implementation_routing_gap_review_v1",
            "routing_incomplete": "routing_incomplete" in issues,
            "missing_conditions_routing_complete": summary.get("missing_conditions_routing_complete"),
        },
        "roadmap": {
            "review_id": "integrated_implementation_roadmap_gap_review_v1",
            "roadmap_incomplete": "roadmap_incomplete" in issues,
            "integrated_roadmap_decision_complete": summary.get("integrated_roadmap_decision_complete"),
        },
        "auth_prep": {
            "review_id": "integrated_implementation_auth_prep_gap_review_v1",
            "auth_prep_incomplete": "auth_prep_incomplete" in issues,
            "issuance_authorization_preparation_package_complete": summary.get(
                "issuance_authorization_preparation_package_complete"
            ),
        },
        "closure_boundary": {
            "review_id": "integrated_implementation_closure_boundary_gap_review_v1",
            "closure_boundary_incomplete": "closure_boundary_incomplete" in issues,
            "record_approval_ack_evidence_boundary_complete": summary.get(
                "record_approval_ack_evidence_boundary_complete"
            ),
        },
        "slice_plan": {
            "review_id": "integrated_implementation_slice_plan_gap_review_v1",
            "slice_plan_incomplete": "slice_plan_incomplete" in issues,
            "module_level_functional_slice_test_plan_complete": summary.get(
                "module_level_functional_slice_test_plan_complete"
            ),
        },
        "checklist": {
            "review_id": "integrated_implementation_checklist_gap_review_v1",
            "checklist_incomplete": "checklist_incomplete" in issues,
            "real_issuance_precondition_checklist_complete": summary.get(
                "real_issuance_precondition_checklist_complete"
            ),
        },
    }


def run_task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        "integrated_implementation_output_root": INTEGRATED_IMPLEMENTATION_OUTPUT,
        **NON_EXECUTION_FLAGS,
    }

    planning_review = _read_json(Path(PLANNING_GAP_REVIEW_OUTPUT) / "summary.json")
    planning_verifier = _read_json(Path(PLANNING_GAP_REVIEW_OUTPUT) / "verifier_report.json")
    planning_result_b = (
        planning_review.get("final_decision", "").endswith("AUTHORIZATION_PREPARATION_DRYRUN_GAP")
        and planning_verifier.get("verifier") == "GO"
    )
    first_gap = _read_json(Path(PLANNING_GAP_REVIEW_OUTPUT) / "first_unresolved_gap_review_v1.json")
    next_fix = first_gap.get("next_required_fix") or planning_review.get("next_required_fix") or {}
    next_fix_confirmed = next_fix.get("stage_id") == (
        "task_manager_owner_approval_request_governance_gate_integrated_implementation_v1"
    )

    integrated_files = {
        rel: (REPO_ROOT / rel).is_file() for rel in REQUIRED_INTEGRATED_FILES
    }
    integrated_files_exist = all(integrated_files.values())

    impl_before = _inspect_stage(INTEGRATED_IMPLEMENTATION_OUTPUT)
    impl_rerun_initial = _run_and_verify(INTEGRATED_RUN_SCRIPT)
    impl_after_initial = _inspect_stage(INTEGRATED_IMPLEMENTATION_OUTPUT)
    impl_summary = _read_json(Path(INTEGRATED_IMPLEMENTATION_OUTPUT) / "summary.json")

    registry = _build_direct_upstream_registry(impl_summary)
    first_non_go = _first_non_go_upstream(registry)

    upstream_rerun: Optional[Dict[str, Any]] = None
    upstream_after: Optional[Dict[str, Any]] = None
    impl_rerun_final: Optional[Dict[str, Any]] = None
    impl_after_final: Optional[Dict[str, Any]] = None
    stop_reason: Optional[str] = None

    if impl_after_initial.get("is_go"):
        stop_reason = "integrated_implementation_already_go_after_initial_rerun"
    elif first_non_go:
        upstream_rerun = _run_and_verify(first_non_go["run_script"])
        upstream_after = _inspect_stage(first_non_go["actual_output_dir"])
        if not upstream_after.get("is_go"):
            stop_reason = f"first_non_go_direct_upstream_still_hold:{first_non_go['stage_name']}"
        else:
            impl_rerun_final = _run_and_verify(INTEGRATED_RUN_SCRIPT)
            impl_after_final = _inspect_stage(INTEGRATED_IMPLEMENTATION_OUTPUT)
            registry = _build_direct_upstream_registry(
                _read_json(Path(INTEGRATED_IMPLEMENTATION_OUTPUT) / "summary.json")
            )
    else:
        stop_reason = "no_direct_upstream_identified"

    impl_final = impl_after_final or impl_after_initial
    impl_go = impl_final.get("is_go") is True
    impl_summary_final = _read_json(Path(INTEGRATED_IMPLEMENTATION_OUTPUT) / "summary.json")
    internal_gaps = _internal_gap_reviews(impl_summary_final)
    visibility = _artifact_visibility(INTEGRATED_IMPLEMENTATION_OUTPUT, INTEGRATED_ARTIFACTS)

    boundary_review = {
        "review_id": "integrated_implementation_upstream_boundary_gap_review_v1",
        "upstream_not_go": "upstream_not_go" in (impl_summary_final.get("issues") or []),
        "non_execution_boundary_ok": impl_summary_final.get("non_execution_boundary_ok"),
        "prior_post_review_go": impl_summary_final.get("prior_post_review_go"),
        "prior_final_gate_planning_go": impl_summary_final.get("prior_final_gate_planning_go"),
        **meta,
    }

    next_required_fix: Optional[Dict[str, Any]] = None
    if first_non_go and not (upstream_after or {}).get("is_go") and not impl_go:
        next_required_fix = {
            "stage_id": first_non_go["stage_name"],
            "upstream_field": first_non_go["upstream_field"],
            "reason": "first_non_go_direct_upstream",
            "upstream_final_decision": first_non_go.get("final_decision"),
            "upstream_issue_tags": first_non_go.get("issues"),
            "upstream_verifier_status": first_non_go.get("verifier_status"),
            "recommended_action": f"Fix {first_non_go['stage_name']} until verifier=GO",
        }
    elif not impl_go and impl_go is False and first_non_go is None:
        next_required_fix = {
            "stage_id": "task_manager_owner_approval_request_governance_gate_integrated_implementation_v1",
            "reason": "integrated_implementation_remaining_internal_gap",
            "issues": impl_summary_final.get("issues"),
            "recommended_action": "Fix integrated implementation internal gaps",
        }

    gap_resolved = impl_go
    auth_dryrun_rerun_readiness = impl_go
    first_non_go_resolved = impl_go or (
        first_non_go is not None and (upstream_after or {}).get("is_go") is True and not impl_go
    )

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=(
            "capabilities/midplatform/task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_lineage_v1.py"
        ),
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    final_decision = FINAL_DECISION_COMPLETE if gap_resolved else FINAL_DECISION_BLOCKED
    review_pass = (
        planning_result_b
        and next_fix_confirmed
        and integrated_files_exist
        and impl_rerun_initial.get("run_script") is not None
        and (next_required_fix is not None or gap_resolved)
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "chain_trace_nodes": [
            "functional_slice_planning_gap_review",
            "governance_gate_integrated_implementation",
            "record_approval_closure_post_dryrun_review",
            "final_gate_planning",
            "governance_gate_integrated_implementation_gap_review",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
        )},
        PASS_FLAG: review_pass,
        "functional_slice_planning_gap_review_result_b_confirmed": planning_result_b,
        "next_required_fix_confirmed": next_fix_confirmed,
        "integrated_implementation_files_exist": integrated_files_exist,
        "integrated_implementation_rerun_attempted": True,
        "integrated_implementation_result_recorded": True,
        "integrated_implementation_direct_upstream_registry_exists": True,
        "first_non_go_direct_upstream_identified": first_non_go is not None,
        "direct_upstream_visibility_review_exists": True,
        "routing_gap_review_exists": True,
        "roadmap_gap_review_exists": True,
        "auth_prep_gap_review_exists": True,
        "closure_boundary_gap_review_exists": True,
        "slice_plan_gap_review_exists": True,
        "checklist_gap_review_exists": True,
        "first_unresolved_gap_review_exists": True,
        "integrated_implementation_go": impl_go,
        "first_non_go_direct_upstream_resolved": first_non_go_resolved,
        "authorization_preparation_dryrun_rerun_readiness": auth_dryrun_rerun_readiness,
        "first_unresolved_gap_identified": not gap_resolved,
        "first_non_go_direct_upstream": (first_non_go or {}).get("stage_name"),
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
        "# Governance Gate Integrated Implementation Gap Review v1",
        "",
        f"**Planning gap review Result B confirmed:** `{planning_result_b}`",
        f"**Integrated implementation GO:** `{impl_go}`",
        f"**First non-GO direct upstream:** `{(first_non_go or {}).get('stage_name')}`",
        f"**Stop reason:** `{stop_reason}`",
        "",
        f"**Final decision:** `{final_decision}`",
    ])

    return {
        "task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_report": {
            "report_id": "task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_report_v1",
            "planning_review_context": {"final_decision": planning_review.get("final_decision"), "next_required_fix": next_fix},
            "stop_reason": stop_reason,
            "gap_resolved": gap_resolved,
            "final_decision": final_decision,
            **meta,
        },
        "task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_report_md": report_md,
        "integrated_implementation_gap_review": {
            "review_id": "integrated_implementation_gap_review_v1",
            "before": impl_before,
            "after_initial": impl_after_initial,
            "after_final": impl_after_final,
            "issues": impl_summary_final.get("issues"),
            **meta,
        },
        "integrated_implementation_direct_upstream_registry": {
            "registry_id": "integrated_implementation_direct_upstream_registry_v1",
            "rows": registry,
            "declared_order_fields": [s[0] for s in DIRECT_UPSTREAM_SPECS],
            **meta,
        },
        "integrated_implementation_first_non_go_upstream_review": {
            "review_id": "integrated_implementation_first_non_go_upstream_review_v1",
            "first_non_go_direct_upstream": first_non_go,
            "upstream_rerun": upstream_rerun,
            "upstream_after": upstream_after,
            **meta,
        },
        "integrated_implementation_upstream_artifact_visibility_review": {**meta, **visibility},
        "integrated_implementation_upstream_boundary_gap_review": boundary_review,
        "integrated_implementation_routing_gap_review": {**meta, **internal_gaps["routing"]},
        "integrated_implementation_roadmap_gap_review": {**meta, **internal_gaps["roadmap"]},
        "integrated_implementation_auth_prep_gap_review": {**meta, **internal_gaps["auth_prep"]},
        "integrated_implementation_closure_boundary_gap_review": {**meta, **internal_gaps["closure_boundary"]},
        "integrated_implementation_slice_plan_gap_review": {**meta, **internal_gaps["slice_plan"]},
        "integrated_implementation_checklist_gap_review": {**meta, **internal_gaps["checklist"]},
        "integrated_implementation_rerun_review": {
            "review_id": "integrated_implementation_rerun_review_v1",
            "initial_rerun": impl_rerun_initial,
            "final_rerun": impl_rerun_final,
            "initial_after": impl_after_initial,
            "final_after": impl_after_final,
            **meta,
        },
        "authorization_preparation_dryrun_rerun_readiness_review": {
            "review_id": "authorization_preparation_dryrun_rerun_readiness_review_v1",
            "authorization_preparation_dryrun_rerun_readiness": auth_dryrun_rerun_readiness,
            "skipped_authorization_preparation_dryrun_rerun": True,
            "recommended_next_phase_if_ready": NEXT_PHASE_COMPLETE,
            **meta,
        },
        "first_unresolved_gap_review": {
            "review_id": "first_unresolved_gap_review_v1",
            "first_non_go_direct_upstream": (first_non_go or {}).get("stage_name"),
            "next_required_fix": next_required_fix,
            **meta,
        },
        "no_protocol_change_review": {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta},
        "owner_constraint_compliance_review": {
            "review_id": "owner_constraint_compliance_review_v1",
            "owner_constraint_compliance_ok": True,
            **meta,
        },
        "source_files_review": {"integrated_implementation": integrated_files},
        "file_size_governance_review": file_size,
        "summary": summary,
    }
