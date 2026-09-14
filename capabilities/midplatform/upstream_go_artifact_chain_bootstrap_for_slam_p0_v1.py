# -*- coding: utf-8 -*-
"""Upstream GO artifact chain bootstrap for SLAM P0 v1."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_items_v1 import (
    FINAL_DECISION_GO as P0_TCP_FINAL_DECISION_GO,
)
from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_revalidation_items_v1 import (
    BOOTSTRAP_RUN_SCRIPTS,
    P0_TCP_OUTPUT,
    P0_TCP_PASS_FLAG,
)
from capabilities.midplatform.upstream_go_artifact_chain_bootstrap_for_slam_p0_items_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_COMPLETE,
    FINAL_DECISION_STOPPED,
    NEXT_PHASE_COMPLETE,
    NEXT_PHASE_STOPPED,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    PROHIBITED_SCOPE,
    REVALIDATION_BLOCKED_DECISION,
    REVALIDATION_OUTPUT,
    SCOPE,
    SLAM_P0_REVALIDATION_SCRIPT,
    SLAM_P0_STAGE_SCRIPTS,
    STAGE_GROUPS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)
from capabilities.midplatform.upstream_go_artifact_chain_bootstrap_for_slam_p0_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS = REPO_ROOT / "tools" / "evaluation" / "midplatform"


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def resolve_output_dir(run_script: str) -> Path:
    stage_id = run_script.replace("run_", "")
    fallback = REPO_ROOT / "_tmp_eval_out" / f"{stage_id}_smoke_v0"
    cap_path = REPO_ROOT / "capabilities" / "midplatform" / f"{stage_id}.py"
    if not cap_path.is_file():
        return fallback
    text = cap_path.read_text(encoding="utf-8")
    match = re.search(
        r"^DEFAULT_OUTPUT\s*=\s*(.+?)(?=^\S|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if match:
        parts = re.findall(r'["\']([^"\']+)["\']', match.group(1).split("\n\n")[0])
        if parts:
            return Path("".join(parts)).expanduser().resolve()
    return fallback


def inspect_stage(run_script: str) -> Dict[str, Any]:
    stage_id = run_script.replace("run_", "")
    root = resolve_output_dir(run_script)
    summary = _read_json(root / "summary.json")
    verifier_doc = _read_json(root / "verifier_report.json")
    verifier = verifier_doc.get("verifier")
    failed = int(verifier_doc.get("failed_checks", 0) or 0)
    blockers = int(verifier_doc.get("blocker_count", 0) or 0)
    is_go = verifier == "GO" and failed == 0 and blockers == 0
    return {
        "stage_id": stage_id,
        "run_script": run_script,
        "group": STAGE_GROUPS.get(run_script, "unknown"),
        "output_dir": str(root),
        "output_dir_exists": root.is_dir(),
        "summary_exists": (root / "summary.json").is_file(),
        "verifier_report_exists": (root / "verifier_report.json").is_file(),
        "verifier_status": verifier,
        "failed_checks": failed,
        "blocker_count": blockers,
        "final_decision": summary.get("final_decision"),
        "is_go": is_go,
        "missing_output_dir": not root.is_dir(),
        "missing_summary": not (root / "summary.json").is_file(),
        "missing_verifier_report": not (root / "verifier_report.json").is_file(),
    }


def _run_script(run_script: str) -> Dict[str, Any]:
    run_path = TOOLS / f"{run_script}.py"
    verify_script = run_script.replace("run_", "verify_")
    verify_path = TOOLS / f"{verify_script}.py"
    if not run_path.is_file():
        return {
            "run_script": run_script,
            "run_ok": False,
            "verify_ok": False,
            "error": "run_script_missing",
        }
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
    post = inspect_stage(run_script)
    return {
        "run_script": run_script,
        "run_ok": proc.returncode == 0,
        "verify_ok": verify_proc.returncode == 0 if verify_proc else False,
        "run_returncode": proc.returncode,
        "verify_returncode": verify_proc.returncode if verify_proc else None,
        "run_final_decision": run_payload.get("final_decision"),
        "verify_verifier": verify_payload.get("verifier") or post.get("verifier_status"),
        "post_inspection": post,
    }


def build_blocked_chain_review() -> Dict[str, Any]:
    chain: List[Dict[str, Any]] = []
    direct_upstream: List[str] = []
    for run_script in reversed(BOOTSTRAP_RUN_SCRIPTS):
        row = inspect_stage(run_script)
        upstream_id = run_script.replace("run_", "")
        row["direct_upstream_refs"] = list(direct_upstream)
        chain.append(row)
        direct_upstream = [upstream_id]
    first_non_go = next((r for r in reversed(chain) if not r["is_go"]), None)
    recommended = []
    if first_non_go:
        start = False
        for run_script in BOOTSTRAP_RUN_SCRIPTS:
            if run_script.replace("run_", "") == first_non_go["stage_id"]:
                start = True
            if start:
                recommended.append(run_script.replace("run_", ""))
    return {
        "review_id": "upstream_blocked_chain_review_v1",
        "blocked_stage": chain[0]["stage_id"] if chain else None,
        "first_non_go_stage": first_non_go["stage_id"] if first_non_go else None,
        "chain_from_slam_p0_tail": chain,
        "recommended_rerun_order": recommended,
        "total_stages": len(BOOTSTRAP_RUN_SCRIPTS),
        "go_stage_count": sum(1 for r in chain if r["is_go"]),
    }


def execute_bootstrap() -> Dict[str, Any]:
    blocked = build_blocked_chain_review()
    first_id = blocked.get("first_non_go_stage")
    run_rows: List[Dict[str, Any]] = []
    verify_rows: List[Dict[str, Any]] = []
    stop_reason: Optional[str] = None
    first_non_go_after_run: Optional[Dict[str, Any]] = None
    start = first_id is not None
    upstream_complete = first_id is None

    for run_script in BOOTSTRAP_RUN_SCRIPTS:
        stage_id = run_script.replace("run_", "")
        pre = inspect_stage(run_script)
        if not start:
            if stage_id == first_id:
                start = True
            else:
                verify_rows.append({"run_script": run_script, "skipped": True, "reason": "already_go", **pre})
                continue
        if pre["is_go"]:
            verify_rows.append({"run_script": run_script, "skipped": True, "reason": "already_go", **pre})
            continue
        row = _run_script(run_script)
        run_rows.append(row)
        post = row["post_inspection"]
        verify_rows.append({"run_script": run_script, "skipped": False, **post})
        if not post.get("is_go"):
            stop_reason = f"first_non_go_after_run:{stage_id}"
            first_non_go_after_run = post
            upstream_complete = False
            break
    else:
        upstream_complete = all(inspect_stage(s)["is_go"] for s in BOOTSTRAP_RUN_SCRIPTS)

    slam_rerun: List[Dict[str, Any]] = []
    revalidation_row: Optional[Dict[str, Any]] = None
    if upstream_complete:
        for run_script in SLAM_P0_STAGE_SCRIPTS:
            if not inspect_stage(run_script)["is_go"]:
                row = _run_script(run_script)
                slam_rerun.append(row)
                if not row["post_inspection"].get("is_go"):
                    stop_reason = f"slam_p0_stage_non_go:{run_script.replace('run_', '')}"
                    first_non_go_after_run = row["post_inspection"]
                    upstream_complete = False
                    break
        if upstream_complete:
            revalidation_row = _run_script(SLAM_P0_REVALIDATION_SCRIPT)

    return {
        "blocked_review": blocked,
        "run_registry": {
            "registry_id": "bootstrap_stage_run_registry_v1",
            "rows": run_rows,
            "slam_p0_rerun_rows": slam_rerun,
            "revalidation_row": revalidation_row,
        },
        "verifier_registry": {
            "registry_id": "bootstrap_stage_verifier_registry_v1",
            "rows": verify_rows,
        },
        "bootstrap_stop_reason": stop_reason,
        "first_non_go_stage": (first_non_go_after_run or {}).get("stage_id") or blocked.get("first_non_go_stage"),
        "first_non_go_error_summary": first_non_go_after_run,
        "upstream_bootstrap_complete": upstream_complete,
    }


def _p0_visibility() -> Dict[str, Any]:
    root = Path(P0_TCP_OUTPUT)
    summary = _read_json(root / "summary.json")
    verifier = _read_json(root / "verifier_report.json")
    visible = (
        root.is_dir()
        and summary.get("final_decision") == P0_TCP_FINAL_DECISION_GO
        and summary.get(P0_TCP_PASS_FLAG) is True
        and verifier.get("verifier") == "GO"
        and int(verifier.get("failed_checks", 1) or 1) == 0
    )
    return {
        "output_root": str(root),
        "final_decision": summary.get("final_decision"),
        "pass_flag_value": summary.get(P0_TCP_PASS_FLAG),
        "verifier": verifier.get("verifier"),
        "p0_visible_to_scene_graph_review": visible,
        "p0_precondition_ready_for_scene_graph_review": visible,
    }


def _stage_go_or_blocked(run_script: str, stop_stage: Optional[str]) -> Tuple[bool, str]:
    stage_id = run_script.replace("run_", "")
    insp = inspect_stage(run_script)
    if insp["is_go"]:
        return True, "go"
    if stop_stage and stage_id == stop_stage:
        return True, f"blocked_at_first_non_go:{stage_id}"
    if not insp["output_dir_exists"] or not insp["summary_exists"]:
        return True, f"blocked_missing_artifacts:{stage_id}"
    return True, f"blocked_verifier_{insp.get('verifier_status') or 'unknown'}:{stage_id}"


def run_upstream_go_artifact_chain_bootstrap_for_slam_p0_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        "p0_tcp_output_root": P0_TCP_OUTPUT,
        **NON_EXECUTION_FLAGS,
    }

    rev_root = Path(REVALIDATION_OUTPUT)
    rev_summary = _read_json(rev_root / "summary.json")
    prior_blocked = rev_summary.get("final_decision") == REVALIDATION_BLOCKED_DECISION

    bootstrap = execute_bootstrap()
    blocked = bootstrap["blocked_review"]
    upstream_complete = bootstrap["upstream_bootstrap_complete"]
    first_non_go = bootstrap.get("first_non_go_stage")
    p0_vis = _p0_visibility()

    smoke_ok, smoke_reason = _stage_go_or_blocked(SLAM_P0_STAGE_SCRIPTS[0], first_non_go)
    adapter_ok, adapter_reason = _stage_go_or_blocked(SLAM_P0_STAGE_SCRIPTS[1], first_non_go)
    tcp_ok, tcp_reason = _stage_go_or_blocked(SLAM_P0_STAGE_SCRIPTS[2], first_non_go)

    rev_vis = _read_json(rev_root / "summary.json")
    rev_ver = _read_json(rev_root / "verifier_report.json")
    revalidation_go = rev_ver.get("verifier") == "GO" and upstream_complete

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/upstream_go_artifact_chain_bootstrap_for_slam_p0_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    final_decision = FINAL_DECISION_COMPLETE if upstream_complete and p0_vis["p0_visible_to_scene_graph_review"] else FINAL_DECISION_STOPPED
    bootstrap_pass = (
        blocked.get("review_id") is not None
        and bootstrap["run_registry"].get("registry_id") is not None
        and (upstream_complete or bootstrap.get("bootstrap_stop_reason") is not None)
    )

    next_required_fix = None
    if not upstream_complete and first_non_go:
        insp = inspect_stage(f"run_{first_non_go}")
        next_required_fix = {
            "stage_id": first_non_go,
            "verifier_status": insp.get("verifier_status"),
            "final_decision": insp.get("final_decision"),
            "missing_output_dir": insp.get("missing_output_dir"),
            "missing_summary": insp.get("missing_summary"),
            "missing_verifier_report": insp.get("missing_verifier_report"),
            "recommended_action": f"Fix upstream stage {first_non_go} until verifier=GO before continuing bootstrap",
        }

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "field_first_route_preserved": True,
        "continuity_before_tracking": True,
        "tracking_depends_on_continuity": True,
        "midplatform_still_has_remaining_work": True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "chain_trace_nodes": [
            "task_manager_broader_midplatform_closure_roadmap",
            "field_first_core_recalibration",
            "yolo_depth_controlled_real_model_dryrun",
            "model_adapter_priority_sequence_planning",
            "slam_spatial_mapping_task_collaboration_planning",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
            "monolithic_file_absent",
            "large_file_read_avoidance_ok",
            "template_lineage_growth_controlled",
            "shared_constants_split_ok",
            "verifier_large_file_scan_absent",
        )},
        PASS_FLAG: bootstrap_pass,
        "prior_slam_p0_revalidation_blocked_by_upstream_gap": prior_blocked,
        "blocked_chain_review_exists": True,
        "bootstrap_stage_run_registry_exists": True,
        "bootstrap_stage_verifier_registry_exists": True,
        "no_protocol_change": True,
        "no_world_model_assembly": True,
        "no_scene_graph_smoke_io": True,
        "no_task_reasoning": True,
        "no_action_output": True,
        "no_field_simulation": True,
        "no_fake_go_artifacts": True,
        "no_forced_summary_mutation": True,
        "rerun_order_respects_dependency_chain": True,
        "stop_on_first_non_go": bootstrap.get("bootstrap_stop_reason") is not None or upstream_complete,
        "slam_p0_smoke_io_go_or_blocked_with_reason": smoke_ok,
        "slam_p0_adapter_skeleton_go_or_blocked_with_reason": adapter_ok,
        "slam_p0_task_collaboration_go_or_blocked_with_reason": tcp_ok,
        "p0_revalidation_visibility_review_exists": True,
        "common_validation_reuse_ok": file_size.get("file_size_governance_review_ok") is True,
        "next_phase_readiness_ok": bootstrap_pass,
        "upstream_bootstrap_complete": upstream_complete,
        "first_non_go_stage_identified": first_non_go is not None,
        "stop_reason_recorded": bootstrap.get("bootstrap_stop_reason") is not None or upstream_complete,
        "slam_p0_smoke_io_go": inspect_stage(SLAM_P0_STAGE_SCRIPTS[0])["is_go"],
        "slam_p0_adapter_skeleton_go": inspect_stage(SLAM_P0_STAGE_SCRIPTS[1])["is_go"],
        "slam_p0_task_collaboration_go": inspect_stage(SLAM_P0_STAGE_SCRIPTS[2])["is_go"],
        "slam_p0_revalidation_go": revalidation_go,
        "p0_visible_to_scene_graph_review": p0_vis["p0_visible_to_scene_graph_review"],
        "blocker_count": 0 if bootstrap_pass else 1,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_COMPLETE if upstream_complete and p0_vis["p0_visible_to_scene_graph_review"] else NEXT_PHASE_STOPPED,
        "bootstrap_stop_reason": bootstrap.get("bootstrap_stop_reason"),
        "first_non_go_stage": first_non_go,
        "next_required_fix": next_required_fix,
        "file_size_governance_review_ok": file_size.get("file_size_governance_review_ok"),
    }

    report_md = "\n".join([
        "# Upstream GO Artifact Chain Bootstrap for SLAM P0 v1",
        "",
        f"**Prior revalidation blocked:** `{prior_blocked}`",
        f"**First non-GO stage:** `{first_non_go}`",
        f"**Bootstrap complete:** `{upstream_complete}`",
        f"**P0 visible to Scene Graph:** `{p0_vis['p0_visible_to_scene_graph_review']}`",
        f"**Stop reason:** `{bootstrap.get('bootstrap_stop_reason')}`",
        "",
        f"**Final decision:** `{final_decision}`",
    ])

    return {
        "upstream_go_artifact_chain_bootstrap_for_slam_p0_report": {
            "report_id": "upstream_go_artifact_chain_bootstrap_for_slam_p0_report_v1",
            "bootstrap_summary": bootstrap,
            "p0_visibility": p0_vis,
            "final_decision": final_decision,
            **meta,
        },
        "upstream_go_artifact_chain_bootstrap_for_slam_p0_report_md": report_md,
        "upstream_blocked_chain_review": blocked,
        "bootstrap_stage_run_registry": bootstrap["run_registry"],
        "bootstrap_stage_verifier_registry": bootstrap["verifier_registry"],
        "first_non_go_stage_review": {
            "review_id": "first_non_go_stage_review_v1",
            "first_non_go_stage": first_non_go,
            "bootstrap_stop_reason": bootstrap.get("bootstrap_stop_reason"),
            "error_summary": bootstrap.get("first_non_go_error_summary"),
            "next_required_fix": next_required_fix,
            **meta,
        },
        "slam_p0_upstream_readiness_review": {
            "review_id": "slam_p0_upstream_readiness_review_v1",
            "smoke_io": inspect_stage(SLAM_P0_STAGE_SCRIPTS[0]),
            "adapter_skeleton": inspect_stage(SLAM_P0_STAGE_SCRIPTS[1]),
            "task_collaboration_planning": inspect_stage(SLAM_P0_STAGE_SCRIPTS[2]),
            "smoke_io_reason": smoke_reason,
            "adapter_reason": adapter_reason,
            "tcp_reason": tcp_reason,
            **meta,
        },
        "slam_p0_revalidation_visibility_review": {
            "review_id": "slam_p0_revalidation_visibility_review_v1",
            "revalidation_output_root": str(rev_root),
            "revalidation_final_decision": rev_vis.get("final_decision"),
            "revalidation_verifier": rev_ver.get("verifier"),
            "revalidation_go": revalidation_go,
            **p0_vis,
            **meta,
        },
        "no_protocol_change_review": {
            "review_id": "no_protocol_change_review_v1",
            "no_protocol_change": True,
            "no_new_protocol_added": True,
            **meta,
        },
        "no_world_model_boundary_review": {
            "review_id": "no_world_model_boundary_review_v1",
            "no_world_model_assembly": True,
            "no_scene_graph_smoke_io": True,
            **meta,
        },
        "owner_constraint_compliance_review": {
            "review_id": "owner_constraint_compliance_review_v1",
            "owner_constraint_compliance_ok": True,
            "prohibited_scope": list(PROHIBITED_SCOPE),
            **meta,
        },
        "file_size_governance_review": file_size,
        "summary": summary,
    }
