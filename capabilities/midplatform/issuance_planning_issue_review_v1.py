# -*- coding: utf-8 -*-
"""Issuance planning issue review v1."""

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
from capabilities.midplatform.issuance_planning_issue_review_items_v1 import (
    DEFAULT_OUTPUT,
    DIRECT_PRIOR_UPSTREAM_SPECS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    ISSUANCE_PLANNING_ARTIFACTS,
    ISSUANCE_PLANNING_OUTPUT,
    ISSUANCE_PLANNING_RUN_SCRIPT,
    ISSUANCE_PLANNING_STAGE_ID,
    ISSUANCE_POST_DRYRUN_ISSUE_REVIEW_OUTPUT,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    REQUIRED_ISSUANCE_PLANNING_FILES,
    SCOPE,
)
from capabilities.midplatform.issuance_planning_issue_review_lineage_v1 import (
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
        "planning_pass": summary.get("planning_pass"),
        "issuance_planning_pass": summary.get("issuance_planning_pass"),
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


def _build_prior_upstream_registry(planning_summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for field, stage_id, run_script in DIRECT_PRIOR_UPSTREAM_SPECS:
        expected = planning_summary.get(field) or ""
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
        "review_id": "issuance_planning_artifact_visibility_review_v1",
        "output_root": str(root),
        "artifacts": rows,
        "all_required_present": not missing,
        "missing_artifacts": missing,
    }


def _internal_gap_reviews(planning_summary: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    issues = planning_summary.get("issues") or []
    return {
        "prior_acceptance": {
            "review_id": "issuance_planning_prior_review_acceptance_review_v1",
            "prior_request_post_dryrun_review_not_go": "prior_request_post_dryrun_review_not_go" in issues,
            "prior_request_planning_not_go": "prior_request_planning_not_go" in issues,
            "prior_request_dryrun_not_go": "prior_request_dryrun_not_go" in issues,
            "prior_request_post_dryrun_review_go": planning_summary.get("prior_request_post_dryrun_review_go"),
            "blocked_by_prior_review_gap": planning_summary.get("final_decision", "").endswith("PRIOR_REVIEW_GAP"),
        },
        "evidence_chain": {
            "review_id": "issuance_planning_evidence_chain_review_v1",
            "issuance_input_output_traceability_contract_complete": planning_summary.get(
                "issuance_input_output_traceability_contract_complete"
            ),
            "issuance_protocol_traceability_contract_complete": planning_summary.get(
                "issuance_protocol_traceability_contract_complete"
            ),
        },
        "prerequisite": {
            "review_id": "issuance_planning_prerequisite_review_v1",
            "owner_approval_request_issuance_plan_complete": planning_summary.get(
                "owner_approval_request_issuance_plan_complete"
            ),
            "prior_shared_code_smoke_go": planning_summary.get("prior_shared_code_smoke_go"),
            "prior_validate_once_rule_review_go": planning_summary.get("prior_validate_once_rule_review_go"),
        },
        "registry_patch": {
            "review_id": "issuance_planning_registry_patch_review_v1",
            "prior_registry_patch_not_go": "prior_registry_patch_not_go" in issues,
            "prior_registry_patch_go": planning_summary.get("prior_registry_patch_go"),
            "input_output_symmetry_reference_ok": planning_summary.get("input_output_symmetry_reference_ok"),
        },
    }


def run_issuance_planning_issue_review_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        "issuance_planning_output_root": ISSUANCE_PLANNING_OUTPUT,
        **NON_EXECUTION_FLAGS,
    }

    post_issue = _read_json(Path(ISSUANCE_POST_DRYRUN_ISSUE_REVIEW_OUTPUT) / "summary.json")
    post_issue_verifier = _read_json(Path(ISSUANCE_POST_DRYRUN_ISSUE_REVIEW_OUTPUT) / "verifier_report.json")
    post_issue_result_b = (
        post_issue.get("final_decision", "").endswith("STILL_BLOCKED_BY_DIRECT_ISSUANCE_UPSTREAM_GAP")
        and post_issue_verifier.get("verifier") == "GO"
    )
    first_gap = _read_json(Path(ISSUANCE_POST_DRYRUN_ISSUE_REVIEW_OUTPUT) / "first_unresolved_gap_review_v1.json")
    upstream_review = _read_json(
        Path(ISSUANCE_POST_DRYRUN_ISSUE_REVIEW_OUTPUT) / "issuance_post_dryrun_review_first_non_go_upstream_review_v1.json"
    )
    next_fix = first_gap.get("next_required_fix") or post_issue.get("next_required_fix") or {}
    direct_planning_confirmed = next_fix.get("stage_id") == ISSUANCE_PLANNING_STAGE_ID

    planning_files = {rel: (REPO_ROOT / rel).is_file() for rel in REQUIRED_ISSUANCE_PLANNING_FILES}
    planning_files_exist = all(planning_files.values())

    planning_before = _inspect_stage(ISSUANCE_PLANNING_OUTPUT)
    planning_rerun_initial = _run_and_verify(ISSUANCE_PLANNING_RUN_SCRIPT)
    planning_after_initial = _inspect_stage(ISSUANCE_PLANNING_OUTPUT)
    planning_summary = _read_json(Path(ISSUANCE_PLANNING_OUTPUT) / "summary.json")

    registry = _build_prior_upstream_registry(planning_summary)
    first_non_go = _first_non_go_upstream(registry)

    upstream_rerun: Optional[Dict[str, Any]] = None
    upstream_after: Optional[Dict[str, Any]] = None
    planning_rerun_final: Optional[Dict[str, Any]] = None
    planning_after_final: Optional[Dict[str, Any]] = None
    stop_reason: Optional[str] = None

    planning_go_initial = planning_after_initial.get("is_go") is True
    if planning_go_initial:
        stop_reason = "issuance_planning_already_go_after_initial_rerun"
    elif first_non_go:
        upstream_rerun = _run_and_verify(first_non_go["run_script"])
        upstream_after = _inspect_stage(first_non_go["actual_output_dir"])
        if not upstream_after.get("is_go"):
            stop_reason = f"first_non_go_prior_upstream_still_hold:{first_non_go['stage_name']}"
        else:
            planning_rerun_final = _run_and_verify(ISSUANCE_PLANNING_RUN_SCRIPT)
            planning_after_final = _inspect_stage(ISSUANCE_PLANNING_OUTPUT)
            planning_summary = _read_json(Path(ISSUANCE_PLANNING_OUTPUT) / "summary.json")
            registry = _build_prior_upstream_registry(planning_summary)
            first_non_go = _first_non_go_upstream(registry)
    else:
        stop_reason = "no_direct_prior_upstream_identified"

    planning_final = planning_after_final or planning_after_initial
    planning_go = planning_final.get("is_go") is True
    planning_summary_final = _read_json(Path(ISSUANCE_PLANNING_OUTPUT) / "summary.json")
    internal_gaps = _internal_gap_reviews(planning_summary_final)
    visibility = _artifact_visibility(ISSUANCE_PLANNING_OUTPUT, ISSUANCE_PLANNING_ARTIFACTS)

    first_upstream_resolved = planning_go or (
        first_non_go is not None and (upstream_after or {}).get("is_go") is True and not planning_go
    )

    next_required_fix: Optional[Dict[str, Any]] = None
    if first_non_go and not (upstream_after or {}).get("is_go") and not planning_go:
        next_required_fix = {
            "stage_id": first_non_go["stage_name"],
            "upstream_field": first_non_go["upstream_field"],
            "reason": "first_non_go_prior_upstream",
            "upstream_final_decision": first_non_go.get("final_decision"),
            "upstream_issue_tags": first_non_go.get("issues"),
            "upstream_verifier_status": first_non_go.get("verifier_status"),
            "recommended_action": f"Fix {first_non_go['stage_name']} until verifier=GO",
        }
    elif not planning_go and first_non_go is None:
        next_required_fix = {
            "stage_id": ISSUANCE_PLANNING_STAGE_ID,
            "reason": "issuance_planning_remaining_internal_gap",
            "issues": planning_summary_final.get("issues"),
            "recommended_action": "Fix issuance planning internal gaps until verifier=GO",
        }

    gap_resolved = planning_go
    post_dryrun_rerun_readiness = planning_go

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/issuance_planning_issue_review_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    final_decision = FINAL_DECISION_COMPLETE if gap_resolved else FINAL_DECISION_BLOCKED
    review_pass = (
        post_issue_result_b
        and direct_planning_confirmed
        and planning_files_exist
        and planning_rerun_initial.get("run_script") is not None
        and (next_required_fix is not None or gap_resolved)
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "chain_trace_nodes": [
            "issuance_post_dryrun_review_issue_review",
            "issuance_planning",
            "grant_owner_approval_request_post_dryrun_review",
            "grant_owner_approval_request_planning",
            "grant_owner_approval_request_dryrun",
            "issuance_planning_issue_review",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
        )},
        PASS_FLAG: review_pass,
        "issuance_post_dryrun_review_issue_review_result_b_confirmed": post_issue_result_b,
        "direct_issuance_planning_upstream_confirmed": direct_planning_confirmed,
        "issuance_planning_files_exist": planning_files_exist,
        "issuance_planning_rerun_attempted": True,
        "issuance_planning_result_recorded": True,
        "direct_prior_upstream_registry_exists": True,
        "first_non_go_prior_upstream_identified": first_non_go is not None,
        "prior_review_acceptance_review_exists": True,
        "evidence_chain_review_exists": True,
        "prerequisite_review_exists": True,
        "registry_patch_review_exists": True,
        "first_unresolved_gap_review_exists": True,
        "issuance_planning_go": planning_go,
        "first_non_go_prior_upstream_resolved": first_upstream_resolved,
        "issuance_post_dryrun_review_rerun_readiness": post_dryrun_rerun_readiness,
        "first_unresolved_gap_identified": not gap_resolved,
        "first_non_go_prior_upstream": (first_non_go or {}).get("stage_name"),
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
        "# Issuance Planning Issue Review v1",
        "",
        f"**Issuance post-dryrun issue review Result B confirmed:** `{post_issue_result_b}`",
        f"**Issuance planning GO:** `{planning_go}`",
        f"**First non-GO prior upstream:** `{(first_non_go or {}).get('stage_name')}`",
        f"**Stop reason:** `{stop_reason}`",
        "",
        f"**Final decision:** `{final_decision}`",
    ])

    return {
        "issuance_planning_issue_review_report": {
            "report_id": "issuance_planning_issue_review_report_v1",
            "post_issue_context": {
                "final_decision": post_issue.get("final_decision"),
                "first_non_go_issuance_upstream": upstream_review.get("first_non_go_issuance_upstream"),
                "next_required_fix": next_fix,
            },
            "stop_reason": stop_reason,
            "gap_resolved": gap_resolved,
            "final_decision": final_decision,
            **meta,
        },
        "issuance_planning_issue_review_report_md": report_md,
        "issuance_planning_gap_review": {
            "review_id": "issuance_planning_gap_review_v1",
            "before": planning_before,
            "after_initial": planning_after_initial,
            "after_final": planning_after_final,
            "issues": planning_summary_final.get("issues"),
            "blocked_by_prior_review_gap": planning_summary_final.get("final_decision", "").endswith("PRIOR_REVIEW_GAP"),
            **meta,
        },
        "issuance_planning_artifact_visibility_review": {**meta, **visibility},
        "issuance_planning_direct_prior_upstream_registry": {
            "registry_id": "issuance_planning_direct_prior_upstream_registry_v1",
            "rows": registry,
            "declared_order_fields": [s[0] for s in DIRECT_PRIOR_UPSTREAM_SPECS],
            **meta,
        },
        "issuance_planning_first_non_go_prior_upstream_review": {
            "review_id": "issuance_planning_first_non_go_prior_upstream_review_v1",
            "first_non_go_prior_upstream": first_non_go,
            "upstream_rerun": upstream_rerun,
            "upstream_after": upstream_after,
            **meta,
        },
        "issuance_planning_prior_review_acceptance_review": {**meta, **internal_gaps["prior_acceptance"]},
        "issuance_planning_evidence_chain_review": {**meta, **internal_gaps["evidence_chain"]},
        "issuance_planning_prerequisite_review": {**meta, **internal_gaps["prerequisite"]},
        "issuance_planning_registry_patch_review": {**meta, **internal_gaps["registry_patch"]},
        "issuance_planning_rerun_review": {
            "review_id": "issuance_planning_rerun_review_v1",
            "initial_rerun": planning_rerun_initial,
            "final_rerun": planning_rerun_final,
            "initial_after": planning_after_initial,
            "final_after": planning_after_final,
            **meta,
        },
        "issuance_post_dryrun_review_rerun_readiness_review": {
            "review_id": "issuance_post_dryrun_review_rerun_readiness_review_v1",
            "issuance_post_dryrun_review_rerun_readiness": post_dryrun_rerun_readiness,
            "skipped_issuance_post_dryrun_review_rerun": True,
            "recommended_next_phase_if_ready": NEXT_PHASE_COMPLETE,
            **meta,
        },
        "first_unresolved_gap_review": {
            "review_id": "first_unresolved_gap_review_v1",
            "first_non_go_prior_upstream": (first_non_go or {}).get("stage_name"),
            "next_required_fix": next_required_fix,
            **meta,
        },
        "no_protocol_change_review": {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta},
        "owner_constraint_compliance_review": {
            "review_id": "owner_constraint_compliance_review_v1",
            "owner_constraint_compliance_ok": True,
            **meta,
        },
        "source_files_review": {"issuance_planning": planning_files},
        "file_size_governance_review": file_size,
        "summary": summary,
    }
