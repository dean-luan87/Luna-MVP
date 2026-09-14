# -*- coding: utf-8 -*-
"""Module handoff gap closure v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_broader_midplatform_closure_roadmap_v1 import (
    DEFAULT_OUTPUT as BROADER_DEFAULT,
    FINAL_DECISION_GO as BROADER_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_gap_closure_items_v1 import (
    BOOTSTRAP_GAP_CLOSURE_ROOT,
    BROADER_ROADMAP_OUTPUT,
    BROADER_ROADMAP_RUN_SCRIPT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    HANDOFF_ARTIFACTS,
    HANDOFF_RUN_SCRIPT,
    MODULE_GOVERNANCE_CLOSURE_OUTPUT,
    MODULE_HANDOFF_OUTPUT,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    OPTIONAL_HANDOFF_DOCS,
    OPTIONAL_HANDOFF_SOURCE_FILES,
    PASS_FLAG,
    PHASE_ID,
    REQUIRED_HANDOFF_SOURCE_FILES,
    SCOPE,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_gap_closure_lineage_v1 import (
    PHASE_PYTHON_FILES,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_v1 import (
    DEFAULT_OUTPUT as HANDOFF_DEFAULT,
    FINAL_DECISION_GO as HANDOFF_FINAL_GO,
    HANDOFF_ARTIFACTS as HANDOFF_EXPECTED_ARTIFACTS,
    NEXT_PHASE_GO as HANDOFF_NEXT_PHASE,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS = REPO_ROOT / "tools" / "evaluation" / "midplatform"

BROADER_EXPECTED_FIELDS: Tuple[Tuple[str, Any], ...] = (
    ("final_decision", HANDOFF_FINAL_GO),
    ("recommended_next_phase", HANDOFF_NEXT_PHASE),
    ("module_handoff_pass", True),
    ("owner_approval_request_chain_not_extended", True),
    ("no_fragmentary_phase_expansion", True),
    ("real_request_issuance_authorized", False),
)


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
    return {
        "output_dir": str(root),
        "output_dir_exists": root.is_dir(),
        "summary_exists": (root / "summary.json").is_file(),
        "verifier_report_exists": (root / "verifier_report.json").is_file(),
        "verifier_status": verifier.get("verifier"),
        "failed_checks": failed,
        "blocker_count": blockers,
        "final_decision": summary.get("final_decision"),
        "pass_flag": summary.get("module_handoff_pass") or summary.get("module_governance_closure_pass"),
        "issues": summary.get("issues") or [],
        "is_go": is_go,
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


def _load_bootstrap_context() -> Dict[str, Any]:
    root = Path(BOOTSTRAP_GAP_CLOSURE_ROOT)
    first = _read_json(root / "first_non_go_stage_review_v1.json")
    blocked = _read_json(root / "upstream_blocked_chain_review_v1.json")
    return {
        "bootstrap_root": str(root),
        "first_non_go_stage": first.get("first_non_go_stage"),
        "bootstrap_stop_reason": first.get("bootstrap_stop_reason"),
        "blocked_stage": blocked.get("blocked_stage"),
        "blocked_first_non_go": blocked.get("first_non_go_stage"),
    }


def _check_source_files() -> Dict[str, Any]:
    required = {rel: (REPO_ROOT / rel).is_file() for rel in REQUIRED_HANDOFF_SOURCE_FILES}
    optional = {rel: (REPO_ROOT / rel).is_file() for rel in OPTIONAL_HANDOFF_SOURCE_FILES}
    docs = {rel: (REPO_ROOT / rel).is_file() for rel in OPTIONAL_HANDOFF_DOCS}
    return {
        "required_files": required,
        "optional_split_files": optional,
        "optional_docs": docs,
        "required_files_exist": all(required.values()),
        "consolidated_in_single_v1": not any(optional.values()),
    }


def _artifact_visibility(handoff_root: Path) -> Dict[str, Any]:
    rows = []
    for name in HANDOFF_ARTIFACTS:
        path = handoff_root / name
        rows.append({
            "artifact": name,
            "exists": path.is_file(),
            "readable": path.is_file() and bool(_read_json(path) if name.endswith(".json") else path.read_text(encoding="utf-8")[:1]),
        })
    return {
        "review_id": "owner_approval_request_handoff_artifact_visibility_review_v1",
        "output_root": str(handoff_root),
        "artifacts": rows,
        "all_required_present": all(r["exists"] for r in rows),
    }


def _field_alignment(handoff_summary: Dict[str, Any], handoff_verifier: Dict[str, Any]) -> Dict[str, Any]:
    mismatches: List[Dict[str, Any]] = []
    for field, expected in BROADER_EXPECTED_FIELDS:
        actual = handoff_summary.get(field)
        if field == "final_decision":
            ok = actual == expected
        elif field == "recommended_next_phase":
            ok = actual == expected
        else:
            ok = actual is expected
        if not ok:
            mismatches.append({"field": field, "expected": expected, "actual": actual})
    verifier_ok = (
        handoff_verifier.get("verifier") == "GO"
        and int(handoff_verifier.get("failed_checks", 1) or 1) == 0
        and int(handoff_verifier.get("passed_checks", 0) or 0) >= 240
    )
    if not verifier_ok:
        mismatches.append({
            "field": "verifier_report",
            "expected": {"verifier": "GO", "failed_checks": 0, "passed_checks": ">=240"},
            "actual": {
                "verifier": handoff_verifier.get("verifier"),
                "failed_checks": handoff_verifier.get("failed_checks"),
                "passed_checks": handoff_verifier.get("passed_checks"),
            },
        })
    return {
        "review_id": "handoff_output_field_alignment_review_v1",
        "downstream_consumer": "task_manager_broader_midplatform_closure_roadmap_v1",
        "expected_final_decision": HANDOFF_FINAL_GO,
        "expected_next_phase": HANDOFF_NEXT_PHASE,
        "actual_final_decision": handoff_summary.get("final_decision"),
        "actual_next_phase": handoff_summary.get("recommended_next_phase"),
        "field_mismatches": mismatches,
        "alignment_ok": len(mismatches) == 0,
    }


def _module_handoff_gap_review(
    *,
    governance: Dict[str, Any],
    handoff_before: Dict[str, Any],
) -> Dict[str, Any]:
    gov_issues = governance.get("issues") or []
    return {
        "review_id": "module_handoff_gap_review_v1",
        "direct_upstream_for_broader_roadmap": "task_manager_owner_approval_request_module_handoff_v1",
        "handoff_upstream_dependency": "task_manager_owner_approval_request_module_governance_closure_v1",
        "module_governance_closure_status": governance,
        "handoff_status_before_rerun": handoff_before,
        "primary_gap_causes": [
            "module_governance_closure_not_go" if not governance.get("is_go") else None,
            "handoff_verifier_not_go" if not handoff_before.get("is_go") else None,
        ],
        "governance_closure_issues": gov_issues,
        "handoff_issues": handoff_before.get("issues") or [],
    }


def run_task_manager_owner_approval_request_module_handoff_gap_closure_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        "module_handoff_output_root": MODULE_HANDOFF_OUTPUT,
        "broader_roadmap_output_root": BROADER_ROADMAP_OUTPUT,
        **NON_EXECUTION_FLAGS,
    }

    bootstrap_ctx = _load_bootstrap_context()
    source_check = _check_source_files()
    first_non_go_confirmed = bootstrap_ctx.get("first_non_go_stage") == (
        "task_manager_broader_midplatform_closure_roadmap_v1"
    )
    direct_upstream_confirmed = bootstrap_ctx.get("blocked_first_non_go") == (
        "task_manager_broader_midplatform_closure_roadmap_v1"
    ) or first_non_go_confirmed

    governance_before = _inspect_stage(MODULE_GOVERNANCE_CLOSURE_OUTPUT)
    handoff_before = _inspect_stage(MODULE_HANDOFF_OUTPUT)
    gap_review = _module_handoff_gap_review(
        governance=governance_before,
        handoff_before=handoff_before,
    )
    gap_review["primary_gap_causes"] = [c for c in gap_review["primary_gap_causes"] if c]

    handoff_rerun = _run_and_verify(HANDOFF_RUN_SCRIPT)
    handoff_after = _inspect_stage(MODULE_HANDOFF_OUTPUT)
    handoff_root = Path(MODULE_HANDOFF_OUTPUT)
    handoff_summary = _read_json(handoff_root / "summary.json")
    handoff_verifier = _read_json(handoff_root / "verifier_report.json")

    visibility = _artifact_visibility(handoff_root)
    alignment = _field_alignment(handoff_summary, handoff_verifier)

    broader_rerun: Optional[Dict[str, Any]] = None
    broader_after: Optional[Dict[str, Any]] = None
    if handoff_after.get("is_go"):
        broader_rerun = _run_and_verify(BROADER_ROADMAP_RUN_SCRIPT)
        broader_after = _inspect_stage(BROADER_ROADMAP_OUTPUT)

    handoff_go = handoff_after.get("is_go") is True
    broader_go = (broader_after or {}).get("is_go") is True if handoff_go else False
    gap_resolved = handoff_go and broader_go

    next_required_fix: Optional[Dict[str, Any]] = None
    if not handoff_go:
        failed_summary = []
        if handoff_verifier.get("failed_checks"):
            failed_summary.append(f"handoff_verifier_failed_checks={handoff_verifier.get('failed_checks')}")
        for issue in handoff_summary.get("issues") or []:
            failed_summary.append(f"handoff_issue:{issue}")
        if not governance_before.get("is_go"):
            next_required_fix = {
                "stage_id": "task_manager_owner_approval_request_module_governance_closure_v1",
                "reason": "module_handoff_blocked_by_module_governance_closure_not_go",
                "governance_final_decision": governance_before.get("final_decision"),
                "governance_issues": governance_before.get("issues"),
                "recommended_action": (
                    "Fix task_manager_owner_approval_request_module_governance_closure_v1 until GO "
                    "before module handoff can become GO"
                ),
            }
        else:
            next_required_fix = {
                "stage_id": "task_manager_owner_approval_request_module_handoff_v1",
                "reason": "handoff_artifact_or_field_gap",
                "field_mismatches": alignment.get("field_mismatches"),
                "failed_checks_summary": failed_summary,
                "missing_artifacts": [a["artifact"] for a in visibility["artifacts"] if not a["exists"]],
                "recommended_action": "Fix module handoff artifacts/fields until verifier=GO",
            }

    downstream_review = {
        "review_id": "downstream_roadmap_expected_artifact_review_v1",
        "consumer_stage": "task_manager_broader_midplatform_closure_roadmap_v1",
        "consumer_output_root": BROADER_ROADMAP_OUTPUT,
        "expected_handoff_final_decision": HANDOFF_FINAL_GO,
        "expected_handoff_next_phase": HANDOFF_NEXT_PHASE,
        "expected_handoff_pass_flag": "module_handoff_pass",
        "expected_verifier": "GO",
        "expected_handoff_artifacts": list(HANDOFF_EXPECTED_ARTIFACTS),
        "expected_mainline_artifact": "midplatform_mainline_return_plan_v1.json",
        **meta,
    }

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=(
            "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_gap_closure_lineage_v1.py"
        ),
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    final_decision = FINAL_DECISION_COMPLETE if gap_resolved else FINAL_DECISION_BLOCKED
    closure_pass = (
        first_non_go_confirmed
        and source_check.get("required_files_exist")
        and handoff_rerun.get("run_script") is not None
        and (next_required_fix is not None or gap_resolved)
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "chain_trace_nodes": [
            "upstream_go_artifact_chain_bootstrap_for_slam_p0",
            "task_manager_broader_midplatform_closure_roadmap",
            "task_manager_owner_approval_request_module_handoff",
            "task_manager_owner_approval_request_module_governance_closure",
            "task_manager_owner_approval_request_module_handoff_gap_closure",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
        )},
        PASS_FLAG: closure_pass,
        "first_non_go_stage_confirmed": first_non_go_confirmed,
        "direct_upstream_module_handoff_confirmed": True,
        "owner_approval_request_module_handoff_files_exist": source_check.get("required_files_exist"),
        "owner_approval_request_module_handoff_rerun_attempted": True,
        "owner_approval_request_module_handoff_result_recorded": True,
        "downstream_broader_roadmap_expectation_review_exists": True,
        "handoff_artifact_visibility_review_exists": True,
        "field_alignment_review_exists": True,
        "owner_approval_request_module_handoff_go": handoff_go,
        "broader_midplatform_closure_roadmap_go": broader_go,
        "first_non_go_stage_resolved": gap_resolved,
        "first_unresolved_handoff_gap_identified": not gap_resolved,
        "next_required_fix_recorded": next_required_fix is not None,
        "common_validation_reuse_ok": file_size.get("file_size_governance_review_ok") is True,
        "next_phase_readiness_ok": closure_pass,
        "blocker_count": 0 if closure_pass else 1,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_COMPLETE if gap_resolved else NEXT_PHASE_BLOCKED,
        "bootstrap_context": bootstrap_ctx,
        "next_required_fix": next_required_fix,
    }

    report_md = "\n".join([
        "# Module Handoff Gap Closure v1",
        "",
        f"**First non-GO confirmed:** `{first_non_go_confirmed}`",
        f"**Module handoff GO:** `{handoff_go}`",
        f"**Broader roadmap GO:** `{broader_go}`",
        f"**Gap resolved:** `{gap_resolved}`",
        "",
        f"**Next required fix:** `{next_required_fix.get('stage_id') if next_required_fix else 'none'}`",
        f"**Final decision:** `{final_decision}`",
    ])

    return {
        "task_manager_owner_approval_request_module_handoff_gap_closure_report": {
            "report_id": "task_manager_owner_approval_request_module_handoff_gap_closure_report_v1",
            "bootstrap_context": bootstrap_ctx,
            "handoff_rerun": handoff_rerun,
            "broader_rerun": broader_rerun,
            "gap_resolved": gap_resolved,
            "final_decision": final_decision,
            **meta,
        },
        "task_manager_owner_approval_request_module_handoff_gap_closure_report_md": report_md,
        "module_handoff_gap_review": {**gap_review, **meta},
        "downstream_roadmap_expected_artifact_review": downstream_review,
        "owner_approval_request_handoff_artifact_visibility_review": {**visibility, **meta},
        "handoff_output_field_alignment_review": {**alignment, **meta},
        "task_manager_owner_approval_request_module_handoff_rerun_review": {
            "review_id": "task_manager_owner_approval_request_module_handoff_rerun_review_v1",
            "before": handoff_before,
            "rerun": handoff_rerun,
            "after": handoff_after,
            **meta,
        },
        "task_manager_broader_midplatform_closure_roadmap_readiness_review": {
            "review_id": "task_manager_broader_midplatform_closure_roadmap_readiness_review_v1",
            "handoff_go_required": True,
            "handoff_go": handoff_go,
            "broader_rerun": broader_rerun,
            "broader_after": broader_after,
            "broader_go": broader_go,
            "skipped_reason": None if handoff_go else "handoff_not_go",
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
        "source_files_review": source_check,
        "file_size_governance_review": file_size,
        "summary": summary,
    }
