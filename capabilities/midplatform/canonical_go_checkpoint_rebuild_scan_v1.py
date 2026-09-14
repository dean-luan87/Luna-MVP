# -*- coding: utf-8 -*-
"""Canonical GO checkpoint rebuild scan helpers v1."""

from __future__ import annotations

import ast
import importlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.task_manager_owner_approval_canonical_go_checkpoint_rebuild_items_v1 import (
    CHECKPOINT_STATUS_BLOCKED,
    CHECKPOINT_STATUS_GO,
    CHECKPOINT_STATUS_HOLD,
    REPO_ROOT_STR,
)

REPO_ROOT = Path(REPO_ROOT_STR)
TOOLS = REPO_ROOT / "tools" / "evaluation" / "midplatform"


def runner_script_to_verify_script(runner_script: str) -> str:
    """Map run_* script name to verify_* without corrupting *_dryrun_* segments."""
    prefix = "run_"
    if runner_script.startswith(prefix):
        return "verify_" + runner_script[len(prefix):]
    return runner_script.replace("run_", "verify_", 1)


def read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def snapshot_artifact_mtimes(paths: List[Path]) -> Dict[str, int]:
    snap: Dict[str, int] = {}
    for p in paths:
        if p.is_file():
            snap[str(p.resolve())] = p.stat().st_mtime_ns
    return snap


def resolve_capability_module(runner_script: str) -> Optional[str]:
    run_path = TOOLS / f"{runner_script}.py"
    if not run_path.is_file():
        return None
    stage_id = runner_script[4:] if runner_script.startswith("run_") else runner_script
    tree = ast.parse(run_path.read_text(encoding="utf-8"))
    candidates: List[tuple] = []
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        if not node.module.startswith("capabilities.midplatform."):
            continue
        names = {a.name: a.asname or a.name for a in node.names}
        has_run = any(n.startswith("run_") for n in names)
        default_unaliased = "DEFAULT_OUTPUT" in names and names["DEFAULT_OUTPUT"] == "DEFAULT_OUTPUT"
        mod_suffix = node.module.rsplit(".", 1)[-1]
        candidates.append((node.module, has_run, default_unaliased, mod_suffix))

    for mod, has_run, default_unaliased, mod_suffix in candidates:
        if mod_suffix in stage_id and has_run and default_unaliased:
            return mod
    for mod, has_run, default_unaliased, mod_suffix in candidates:
        if mod_suffix in stage_id and default_unaliased:
            return mod
    for mod, has_run, default_unaliased, _ in candidates:
        if has_run and default_unaliased:
            return mod
    for mod, _, default_unaliased, _ in candidates:
        if default_unaliased:
            return mod
    return candidates[0][0] if candidates else None


def resolve_output_dir(runner_script: str) -> Optional[str]:
    mod_name = resolve_capability_module(runner_script)
    if not mod_name:
        return None
    try:
        mod = importlib.import_module(mod_name)
    except Exception:
        return None
    out = getattr(mod, "DEFAULT_OUTPUT", None)
    if out is None:
        return None
    if isinstance(out, (tuple, list)):
        return "".join(str(x) for x in out)
    return str(out)


def is_go(summary: Dict[str, Any], verifier: Dict[str, Any]) -> bool:
    failed = int(verifier.get("failed_checks", 0) or 0)
    blockers = int(verifier.get("blocker_count", 0) or 0)
    fd = str(summary.get("final_decision") or "")
    if not fd or "BLOCKED" in fd:
        return False
    return verifier.get("verifier") == "GO" and failed == 0 and blockers == 0


def run_and_verify(runner_script: str) -> Dict[str, Any]:
    run_path = TOOLS / f"{runner_script}.py"
    verify_script = runner_script_to_verify_script(runner_script)
    verify_path = TOOLS / f"{verify_script}.py"
    if not run_path.is_file():
        return {"run_script": runner_script, "run_ok": False, "error": "run_script_missing"}
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
        "run_script": runner_script,
        "run_ok": proc.returncode == 0,
        "verify_ok": verify_proc.returncode == 0 if verify_proc else False,
        "run_payload": run_payload,
        "verify_payload": verify_payload,
        "verify_verifier": verify_payload.get("verifier"),
    }


def extract_upstream_refs(summary: Dict[str, Any]) -> Dict[str, str]:
    refs: Dict[str, str] = {}
    for key, val in summary.items():
        if not isinstance(val, str):
            continue
        if key.endswith("_root") or key.endswith("_ref") or key.endswith("_output_root"):
            if val.startswith("/") or val.startswith(str(REPO_ROOT)):
                refs[key] = val
    return refs


def infer_expected_downstream_decision(summary: Dict[str, Any]) -> Optional[str]:
    for key in (
        "expected_final_decision",
        "downstream_expected_final_decision",
        "final_decision_go",
    ):
        val = summary.get(key)
        if isinstance(val, str) and val:
            return val
    fd = summary.get("final_decision")
    if isinstance(fd, str) and ("READY" in fd):
        return fd
    return None


def classify_gap(checkpoint: Dict[str, Any]) -> List[str]:
    gaps: List[str] = []
    status = checkpoint.get("checkpoint_status")
    if status == "runner_missing":
        gaps.append("runner_missing")
    if status == "verifier_missing":
        gaps.append("verifier_missing")
    if status == "missing_output_dir":
        gaps.append("artifact_missing")
    if status == "missing_summary":
        gaps.append("summary_missing")
    if status == "missing_verifier_report":
        gaps.append("verifier_report_missing")
    if status == "final_decision_drift":
        gaps.append("final_decision_drift")
    if status == "downstream_expectation_drift":
        gaps.append("downstream_expectation_drift")
    if status in (CHECKPOINT_STATUS_HOLD, CHECKPOINT_STATUS_BLOCKED):
        issues = checkpoint.get("issue_tags") or []
        if any("registry_patch" in str(i) for i in issues):
            gaps.append("registry_patch_not_go")
        elif status == "skipped_due_prior_failure":
            gaps.append("prior_stage_not_go")
        else:
            gaps.append("genuine_logic_hold")
    if checkpoint.get("upstream_ref_drift"):
        gaps.append("upstream_ref_drift")
    return gaps or (["artifact_missing"] if status == "unreadable" else [])


def recommended_fix(checkpoint: Dict[str, Any]) -> str:
    status = checkpoint.get("checkpoint_status")
    mapping: Dict[str, str] = {
        "missing_verifier_report": "regenerate_missing_verifier_report",
        "missing_summary": "regenerate_summary",
        "runner_missing": "owner_decision_required",
        "verifier_missing": "fix_verifier_output_schema",
        "final_decision_drift": "align_final_decision_mapping",
        "downstream_expectation_drift": "align_final_decision_mapping",
        CHECKPOINT_STATUS_GO: "no_fix_needed",
        "skipped_due_prior_failure": "upstream_stage_not_go",
        CHECKPOINT_STATUS_HOLD: "rerun_original_stage",
        CHECKPOINT_STATUS_BLOCKED: "upstream_stage_not_go",
    }
    if checkpoint.get("upstream_ref_drift"):
        return "align_upstream_refs"
    return mapping.get(status, "rerun_original_stage")


def build_checkpoint(
    spec: Dict[str, Any],
    *,
    output_dir: Optional[str],
    mode: str,
    skipped: bool,
    rerun_result: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    runner_script = spec["runner_script"]
    runner_path = TOOLS / f"{runner_script}.py"
    verify_script = runner_script_to_verify_script(runner_script)
    verifier_path = TOOLS / f"{verify_script}.py"
    runner_exists = runner_path.is_file()
    verifier_exists = verifier_path.is_file()

    base = {
        "stage_key": spec["stage_key"],
        "stage_id": spec["stage_id"],
        "stage_name": spec["stage_name"],
        "stage_family": spec["stage_family"],
        "stage_role": spec["stage_role"],
        "runner_path": str(runner_path),
        "verifier_path": str(verifier_path),
        "upstream_refs": spec["upstream_refs"],
        "downstream_refs": spec["downstream_refs"],
        "downstream_readiness_refs": spec["downstream_refs"] if spec["readiness_only"] else [],
        "candidate_only": True,
        "no_protocol_change": True,
        "no_world_model_assembly": True,
        "no_task_reasoning": True,
        "no_field_simulation": True,
        "no_fake_go": True,
        "created_by_checkpoint_rebuild": True,
        "scan_mode": mode,
        "readiness_only": spec["readiness_only"],
    }

    if not runner_exists:
        return {
            **base,
            "output_dir": output_dir,
            "runner_missing": True,
            "verifier_missing": not verifier_exists,
            "checkpoint_status": "runner_missing",
            "checkpoint_reason": "runner_script_not_found",
            "accepted_by_downstream": False,
        }

    if skipped and not spec["readiness_only"]:
        return {
            **base,
            "output_dir": output_dir,
            "summary_exists": False,
            "verifier_report_exists": False,
            "checkpoint_status": "skipped_due_prior_failure",
            "checkpoint_reason": "prior_non_go_in_topdown_chain",
            "accepted_by_downstream": False,
            "rerun_attempted": False,
        }

    root = Path(output_dir).expanduser().resolve() if output_dir else None
    summary_path = root / "summary.json" if root else None
    verifier_path_json = root / "verifier_report.json" if root else None
    summary = read_json(summary_path) if summary_path else {}
    verifier = read_json(verifier_path_json) if verifier_path_json else {}

    upstream_field_refs = extract_upstream_refs(summary)
    expected_downstream = infer_expected_downstream_decision(summary)
    actual_fd = summary.get("final_decision")
    fd_match = expected_downstream is None or actual_fd is None or actual_fd == expected_downstream

    failed = int(verifier.get("failed_checks", 0) or 0)
    blockers = int(verifier.get("blocker_count", 0) or 0)
    verifier_status = verifier.get("verifier")
    go = is_go(summary, verifier)

    if root is None or not root.is_dir():
        status, reason = "missing_output_dir", "output_dir_not_found"
    elif not summary_path or not summary_path.is_file():
        status, reason = "missing_summary", "summary_json_missing"
    elif not verifier_path_json or not verifier_path_json.is_file():
        status, reason = "missing_verifier_report", "verifier_report_json_missing"
    elif not verifier_exists:
        status, reason = "verifier_missing", "verifier_script_missing"
    elif not fd_match:
        status, reason = "downstream_expectation_drift", "final_decision_mismatch"
    elif go:
        status, reason = CHECKPOINT_STATUS_GO, "verifier_go_and_final_decision_readable"
    elif verifier_status == "HOLD" or failed > 0 or blockers > 0:
        status = CHECKPOINT_STATUS_BLOCKED if blockers > 0 else CHECKPOINT_STATUS_HOLD
        reason = "original_stage_hold"
    else:
        status, reason = "unreadable", "could_not_classify_stage_state"

    return {
        **base,
        "output_dir": str(root) if root else output_dir,
        "source_summary_path": str(summary_path) if summary_path else None,
        "source_verifier_report_path": str(verifier_path_json) if verifier_path_json else None,
        "summary_exists": summary_path.is_file() if summary_path else False,
        "verifier_report_exists": verifier_path_json.is_file() if verifier_path_json else False,
        "verifier_status": verifier_status,
        "final_decision": actual_fd,
        "expected_downstream_decision": expected_downstream,
        "final_decision_matches_downstream_expectation": fd_match,
        "failed_checks": failed,
        "blocker_count": blockers,
        "issue_tags": summary.get("issues") or [],
        "upstream_field_refs": upstream_field_refs,
        "upstream_ref_drift": False,
        "accepted_by_downstream": go and fd_match,
        "checkpoint_status": status,
        "checkpoint_reason": reason,
        "is_go": go,
        "rerun_attempted": rerun_result is not None,
        "rerun_result": rerun_result,
    }
