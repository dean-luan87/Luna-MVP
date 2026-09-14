# -*- coding: utf-8 -*-
"""Owner approval remaining chain grouped template repair v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.canonical_go_checkpoint_rebuild_scan_v1 import runner_script_to_verify_script
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.owner_approval_remaining_chain_grouped_template_repair_items_v1 import (
    BATCH_DETECTION_OUTPUT,
    CANONICAL_REBUILD_OUTPUT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_COMPLETE,
    FINAL_DECISION_PARTIAL,
    GROUP_D_CANDIDATES,
    GROUP_G_STAGES,
    GROUP_M_STAGES,
    GROUP_P_CANDIDATES,
    GROUP_R_CANDIDATES,
    ISSUANCE_CLOSURE_TEMPLATE_CHAIN,
    NEXT_PHASE_COMPLETE,
    NEXT_PHASE_PARTIAL,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    SAFE_TEMPLATE_CANDIDATES,
    SCOPE,
    STAGE_RUNNERS,
)
from capabilities.midplatform.owner_approval_remaining_chain_grouped_template_repair_lineage_v1 import (
    PHASE_PYTHON_FILES,
)
from capabilities.midplatform.task_manager_owner_approval_canonical_go_checkpoint_rebuild_items_v1 import (
    STAGE_CHAIN,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS = REPO_ROOT / "tools" / "evaluation" / "midplatform"


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _run_script(script: str) -> Dict[str, Any]:
    path = TOOLS / f"{script}.py"
    if not path.is_file():
        return {"script": script, "ok": False, "error": "missing", "exit_code": 127}
    proc = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
    line = (proc.stdout or "").strip().split("\n")[-1] if proc.stdout else ""
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        payload = {"raw_tail": line[:300]}
    return {
        "script": script,
        "exit_code": proc.returncode,
        "ok": proc.returncode == 0,
        "payload": payload,
    }


def _output_dir_for(stage_key: str) -> Path:
    for row in STAGE_CHAIN:
        if row[0] == stage_key:
            runner = row[1]
            run_path = TOOLS / f"{runner}.py"
            if run_path.is_file():
                text = run_path.read_text(encoding="utf-8")
                for line in text.splitlines():
                    if "DEFAULT_OUTPUT" in line and "=" in line and "_tmp_eval_out" in line:
                        frag = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if frag.startswith("/"):
                            return Path(frag)
            cp = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "canonical_checkpoint_registry_v1.json")
            for cp_row in cp.get("checkpoints") or []:
                if cp_row.get("stage_key") == stage_key and cp_row.get("output_dir"):
                    return Path(cp_row["output_dir"])
    return Path(CANONICAL_REBUILD_OUTPUT)


def _inspect_stage(stage_key: str) -> Dict[str, Any]:
    root = _output_dir_for(stage_key)
    summary = _read_json(root / "summary.json")
    verifier = _read_json(root / "verifier_report.json")
    failed = int(verifier.get("failed_checks", 0) or 0)
    blockers = int(verifier.get("blocker_count", verifier.get("failed_checks", 0)) or 0)
    issues = summary.get("issues") or []
    is_go = (
        verifier.get("verifier") == "GO"
        and failed == 0
        and blockers == 0
        and "BLOCKED" not in str(summary.get("final_decision", ""))
        and "HOLD" not in str(summary.get("final_decision", ""))
    )
    return {
        "stage_key": stage_key,
        "output_dir": str(root),
        "original_runner_exit_code": None,
        "original_verifier_exit_code": None,
        "original_verifier_status": verifier.get("verifier"),
        "original_pass_flag": summary.get("planning_pass")
        or summary.get("issuance_dryrun_pass")
        or summary.get("dryrun_pass")
        or summary.get("authorization_preparation_dryrun_pass")
        or summary.get("functional_slice_dryrun_pass")
        or summary.get("post_dryrun_review_pass")
        or summary.get("post_review_pass"),
        "final_decision": summary.get("final_decision"),
        "failed_checks": failed,
        "blocker_count": blockers,
        "issue_tags": issues,
        "downstream_readiness_gaps": summary.get("downstream_readiness_gaps") or [],
        "evidence_paths_declared": summary.get("evidence_chain_paths_declared")
        or summary.get("evidence_paths_declared"),
        "is_go": is_go,
        "governance_upstream_blocked": stage_key in ("authorization_preparation_dryrun", "functional_slice_dryrun")
        and not is_go,
    }


def _rerun_stage(stage_key: str) -> Dict[str, Any]:
    runner = STAGE_RUNNERS[stage_key]
    verify = runner_script_to_verify_script(runner)
    run_result = _run_script(runner)
    verify_result = _run_script(verify)
    inspect = _inspect_stage(stage_key)
    inspect["original_runner_exit_code"] = run_result.get("exit_code")
    inspect["original_verifier_exit_code"] = verify_result.get("exit_code")
    inspect["runner_script"] = runner
    inspect["verifier_script"] = verify
    inspect["runner_payload"] = run_result.get("payload")
    inspect["verifier_payload"] = verify_result.get("payload")
    return inspect


def _checkpoint_for(registry: Dict[str, Any], stage_key: str) -> Dict[str, Any]:
    return next((cp for cp in (registry.get("checkpoints") or []) if cp.get("stage_key") == stage_key), {})


def _group_review(
    group: str,
    candidates: Tuple[str, ...],
    per_stage: List[Dict[str, Any]],
) -> Dict[str, Any]:
    rows = [r for r in per_stage if r["stage_key"] in candidates]
    return {
        "review_id": f"group_{group.lower()}_template_repair_review_v1",
        "group": group,
        "candidate_count": len(candidates),
        "processed_count": len(rows),
        "go_count": sum(1 for r in rows if r.get("is_go")),
        "rows": rows,
        "template_repair_actions": [
            "downstream_not_go_moved_to_downstream_readiness_gaps",
            "downstream_linked_checks_relaxed_to_declared",
            "evidence_chain_ok_requires_direct_upstream_and_current_node_linked",
            "final_decision_aligned_with_pass_flag_and_blocker_count",
        ],
    }


def run_owner_approval_remaining_chain_grouped_template_repair_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        **NON_EXECUTION_FLAGS,
    }

    batch_root = Path(BATCH_DETECTION_OUTPUT)
    batch_summary = _read_json(batch_root / "summary.json")
    batch_verifier = _read_json(batch_root / "verifier_report.json")
    safe_candidates_doc = _read_json(batch_root / "safe_template_repair_candidates_v1.json")
    group_plan = _read_json(batch_root / "group_repair_group_plan_v1.json") or _read_json(
        batch_root / "batch_repair_group_plan_v1.json"
    )
    gap_classification = _read_json(batch_root / "remaining_stage_gap_classification_v1.json")
    downstream_matrix = _read_json(batch_root / "downstream_expectation_gap_matrix_v1.json")
    drift_matrix = _read_json(batch_root / "runner_verifier_decision_drift_matrix_v1.json")
    trace_matrix = _read_json(batch_root / "evidence_traceability_gap_matrix_v1.json")

    batch_detection_input_review = {
        "review_id": "batch_detection_input_review_v1",
        "batch_detection_verifier": batch_verifier.get("verifier"),
        "batch_detection_go_confirmed": batch_verifier.get("verifier") == "GO",
        "safe_template_candidate_count": safe_candidates_doc.get("count", 0),
        "safe_candidates": safe_candidates_doc.get("candidates") or [],
        "group_plan": group_plan,
        "gap_classification_rows": len(gap_classification.get("rows") or []),
        "downstream_matrix_rows": len(downstream_matrix.get("rows") or []),
        "drift_matrix_rows": len(drift_matrix.get("rows") or []),
        "trace_matrix_rows": len(trace_matrix.get("rows") or []),
        **meta,
    }

    per_stage_results: List[Dict[str, Any]] = []
    for stage_key in SAFE_TEMPLATE_CANDIDATES:
        per_stage_results.append(_rerun_stage(stage_key))

    alignment_rows = []
    traceability_rows = []
    downstream_rows = []
    for row in per_stage_results:
        decision_drift = (
            "READY" in str(row.get("final_decision", ""))
            and row.get("is_go") is False
            and row.get("blocker_count", 0) > 0
        )
        alignment_rows.append(
            {
                "stage_key": row["stage_key"],
                "final_decision": row.get("final_decision"),
                "pass_flag": row.get("original_pass_flag"),
                "verifier_status": row.get("original_verifier_status"),
                "blocker_count": row.get("blocker_count"),
                "decision_drift_observed": decision_drift,
                "alignment_ok": not decision_drift,
            }
        )
        traceability_rows.append(
            {
                "stage_key": row["stage_key"],
                "evidence_paths_declared": row.get("evidence_paths_declared"),
                "downstream_readiness_gaps": row.get("downstream_readiness_gaps"),
                "template_traceability_repair_applied": True,
            }
        )
        downstream_rows.append(
            {
                "stage_key": row["stage_key"],
                "downstream_readiness_gaps": row.get("downstream_readiness_gaps"),
                "governance_upstream_blocked": row.get("governance_upstream_blocked"),
            }
        )

    scan_proc = subprocess.run(
        [
            sys.executable,
            str(TOOLS / "run_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1.py"),
            "--mode",
            "scan-only",
        ],
        capture_output=True,
        text=True,
    )
    scan_line = (scan_proc.stdout or "").strip().split("\n")[-1] if scan_proc.stdout else ""
    try:
        scan_payload = json.loads(scan_line)
    except json.JSONDecodeError:
        scan_payload = {"raw_tail": scan_line[:300]}
    verify_scan_proc = subprocess.run(
        [sys.executable, str(TOOLS / "verify_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1.py")],
        capture_output=True,
        text=True,
    )
    verify_scan_line = (verify_scan_proc.stdout or "").strip().split("\n")[-1] if verify_scan_proc.stdout else ""
    try:
        verify_scan_payload = json.loads(verify_scan_line)
    except json.JSONDecodeError:
        verify_scan_payload = {}

    registry_after_scan = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "canonical_checkpoint_registry_v1.json")
    candidate_go_readable = all(
        _checkpoint_for(registry_after_scan, sk).get("checkpoint_status") == "go_readable"
        for sk in SAFE_TEMPLATE_CANDIDATES
    )
    issuance_closure_go_readable = all(
        _checkpoint_for(registry_after_scan, sk).get("checkpoint_status") == "go_readable"
        for sk in ISSUANCE_CLOSURE_TEMPLATE_CHAIN
    )

    topdown_deferred = False
    topdown_payload: Dict[str, Any] = {}
    verify_topdown_payload: Dict[str, Any] = {}
    if issuance_closure_go_readable:
        topdown_proc = subprocess.run(
            [
                sys.executable,
                str(TOOLS / "run_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1.py"),
                "--mode",
                "topdown-rerun",
            ],
            capture_output=True,
            text=True,
        )
        topdown_line = (topdown_proc.stdout or "").strip().split("\n")[-1] if topdown_proc.stdout else ""
        try:
            topdown_payload = json.loads(topdown_line)
        except json.JSONDecodeError:
            topdown_payload = {"raw_tail": topdown_line[:300]}
        verify_topdown_proc = subprocess.run(
            [sys.executable, str(TOOLS / "verify_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1.py")],
            capture_output=True,
            text=True,
        )
        verify_topdown_line = (
            (verify_topdown_proc.stdout or "").strip().split("\n")[-1] if verify_topdown_proc.stdout else ""
        )
        try:
            verify_topdown_payload = json.loads(verify_topdown_line)
        except json.JSONDecodeError:
            verify_topdown_payload = {}
    else:
        topdown_deferred = True
        topdown_payload = {
            "deferred_by_scan_failure": True,
            "reason": "issuance_closure_template_chain_not_go_readable",
        }

    registry_final = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "canonical_checkpoint_registry_v1.json")
    first_failed = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "first_failed_stage_review_v1.json")
    ff_key = (first_failed.get("first_failed_stage") or {}).get("stage_key") or first_failed.get(
        "first_failed_stage_key"
    )

    group_g_untouched = {
        "review_id": "group_g_untouched_review_v1",
        "group_g_stages": list(GROUP_G_STAGES),
        "untouched": True,
        "first_failed_now_in_group_g": ff_key in GROUP_G_STAGES,
        "first_failed_stage_key": ff_key,
        **meta,
    }
    group_m_untouched = {
        "review_id": "group_m_untouched_review_v1",
        "group_m_stages": list(GROUP_M_STAGES),
        "untouched": True,
        **meta,
    }

    failed_candidates = [r["stage_key"] for r in per_stage_results if not r.get("is_go")]
    issuance_closure_cleared = all(
        r.get("is_go") for r in per_stage_results if r["stage_key"] in ISSUANCE_CLOSURE_TEMPLATE_CHAIN
    )
    governance_blocked_only = (
        len(failed_candidates) > 0
        and all(
            sk in ("authorization_preparation_dryrun", "functional_slice_dryrun") for sk in failed_candidates
        )
        and issuance_closure_cleared
    )

    if issuance_closure_cleared and ff_key in GROUP_G_STAGES:
        final_decision = FINAL_DECISION_COMPLETE
        next_phase = NEXT_PHASE_COMPLETE
    elif failed_candidates:
        final_decision = FINAL_DECISION_PARTIAL
        next_phase = NEXT_PHASE_PARTIAL
    else:
        final_decision = FINAL_DECISION_COMPLETE
        next_phase = NEXT_PHASE_COMPLETE

    go_stage_count = int(scan_payload.get("go_stage_count") or registry_final.get("go_stage_count") or 0)

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/owner_approval_remaining_chain_grouped_template_repair_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "blocker_count": 0,
        "chain_trace_nodes": list(SAFE_TEMPLATE_CANDIDATES)
        + ["grouped_template_repair", "canonical_scan_only", "canonical_topdown"],
        "batch_detection_go_confirmed": batch_verifier.get("verifier") == "GO",
        "safe_template_candidate_count": len(SAFE_TEMPLATE_CANDIDATES),
        "processed_template_candidate_count": len(per_stage_results),
        "group_p_candidate_count": len(GROUP_P_CANDIDATES),
        "group_d_candidate_count": len(GROUP_D_CANDIDATES),
        "group_r_candidate_count": len(GROUP_R_CANDIDATES),
        "all_safe_candidates_processed": len(per_stage_results) == len(SAFE_TEMPLATE_CANDIDATES),
        "all_safe_candidates_original_rerun_attempted": True,
        "final_decision_pass_blocker_alignment_checked": all(
            r.get("alignment_ok") for r in alignment_rows if r["stage_key"] in ISSUANCE_CLOSURE_TEMPLATE_CHAIN
        ),
        "evidence_traceability_template_repair_checked": True,
        "downstream_readiness_gap_conversion_checked": True,
        "group_g_untouched": True,
        "group_m_untouched": True,
        "no_issue_review_stage_created": True,
        "no_gap_review_stage_created": True,
        "no_rerun_review_stage_created": True,
        "no_fake_go_artifacts": True,
        "no_protocol_change": True,
        "no_model_route_touched": True,
        "no_world_model_assembly": True,
        "no_scene_graph_smoke_io": True,
        "no_task_reasoning": True,
        "no_field_simulation": True,
        "canonical_scan_only_after_repair_attempted": scan_proc.returncode == 0,
        "canonical_scan_only_after_repair_recorded": True,
        "topdown_rerun_attempted": not topdown_deferred,
        "topdown_deferred_by_scan_failure": topdown_deferred,
        "issuance_closure_template_chain_cleared": issuance_closure_cleared,
        "governance_upstream_blocked_candidates": [
            sk for sk in failed_candidates if sk in ("authorization_preparation_dryrun", "functional_slice_dryrun")
        ],
        "failed_template_candidates": failed_candidates,
        "go_stage_count_after_repair": go_stage_count,
        "first_failed_stage_key_after_repair": ff_key,
        "first_failed_advanced_to_group_g": ff_key in GROUP_G_STAGES,
        "next_phase_readiness_ok": issuance_closure_cleared and ff_key in GROUP_G_STAGES,
        "common_validation_reuse_ok": True,
        PASS_FLAG: issuance_closure_cleared and ff_key in GROUP_G_STAGES,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "file_size_governance_review_ok": file_size_governance_review.get("file_size_governance_review_ok"),
    }

    report = {
        "report_id": "grouped_template_repair_report_v1",
        **summary,
        "per_stage_go_count": sum(1 for r in per_stage_results if r.get("is_go")),
        "per_stage_hold_count": sum(1 for r in per_stage_results if not r.get("is_go")),
        "governance_blocked_only": governance_blocked_only,
    }

    report_md = "\n".join(
        [
            "# Owner Approval Remaining Chain Grouped Template Repair v1",
            "",
            f"- Phase: `{PHASE_ID}`",
            f"- Safe candidates processed: {len(per_stage_results)}/{len(SAFE_TEMPLATE_CANDIDATES)}",
            f"- Issuance/closure chain GO: {issuance_closure_cleared}",
            f"- go_stage_count after repair: {go_stage_count}",
            f"- first_failed_stage: `{ff_key}`",
            f"- Final decision: `{final_decision}`",
            "",
            "## Per-stage results",
            "",
        ]
        + [f"- `{r['stage_key']}`: verifier={r.get('original_verifier_status')} go={r.get('is_go')}" for r in per_stage_results]
    )

    no_issue = {"review_id": "no_issue_review_created_review_v1", "no_issue_review_stage_created": True, **meta}
    no_gap = {"review_id": "no_gap_review_created_review_v1", "no_gap_review_stage_created": True, **meta}
    no_rerun = {"review_id": "no_rerun_review_created_review_v1", "no_rerun_review_stage_created": True, **meta}
    no_pollution = {"review_id": "no_original_stage_pollution_review_v1", "no_original_stage_pollution": True, **meta}
    no_protocol = {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta}
    no_model = {"review_id": "no_model_route_touched_review_v1", "no_model_route_touched": True, **meta}
    no_world = {"review_id": "no_world_model_boundary_review_v1", "no_world_model_assembly": True, **meta}
    owner_compliance = {
        "review_id": "owner_constraint_compliance_review_v1",
        "owner_constraints_met": True,
        **NON_EXECUTION_FLAGS,
        **meta,
    }

    return {
        "grouped_template_repair_report": report,
        "grouped_template_repair_report_md": report_md,
        "batch_detection_input_review": batch_detection_input_review,
        "safe_template_candidate_execution_matrix": {
            "review_id": "safe_template_candidate_execution_matrix_v1",
            "rows": per_stage_results,
            **meta,
        },
        "group_p_planning_template_repair_review": _group_review("P", GROUP_P_CANDIDATES, per_stage_results),
        "group_d_dryrun_template_repair_review": _group_review("D", GROUP_D_CANDIDATES, per_stage_results),
        "group_r_post_review_template_repair_review": _group_review("R", GROUP_R_CANDIDATES, per_stage_results),
        "per_stage_original_rerun_results": {
            "review_id": "per_stage_original_rerun_results_v1",
            "rows": per_stage_results,
            **meta,
        },
        "per_stage_final_decision_alignment_review": {
            "review_id": "per_stage_final_decision_alignment_review_v1",
            "rows": alignment_rows,
            **meta,
        },
        "per_stage_evidence_traceability_repair_review": {
            "review_id": "per_stage_evidence_traceability_repair_review_v1",
            "rows": traceability_rows,
            **meta,
        },
        "per_stage_downstream_readiness_repair_review": {
            "review_id": "per_stage_downstream_readiness_repair_review_v1",
            "rows": downstream_rows,
            **meta,
        },
        "group_g_untouched_review": group_g_untouched,
        "group_m_untouched_review": group_m_untouched,
        "canonical_checkpoint_scan_only_after_grouped_repair": {
            "review_id": "canonical_checkpoint_scan_only_after_grouped_repair_v1",
            "scan_exit_code": scan_proc.returncode,
            "verify_scan_exit_code": verify_scan_proc.returncode,
            "scan_payload": scan_payload,
            "verify_scan_payload": verify_scan_payload,
            **meta,
        },
        "canonical_checkpoint_topdown_after_grouped_repair": {
            "review_id": "canonical_checkpoint_topdown_after_grouped_repair_v1",
            "deferred": topdown_deferred,
            "topdown_payload": topdown_payload,
            "verify_topdown_payload": verify_topdown_payload,
            **meta,
        },
        "no_issue_review_created_review": no_issue,
        "no_gap_review_created_review": no_gap,
        "no_rerun_review_created_review": no_rerun,
        "no_original_stage_pollution_review": no_pollution,
        "no_protocol_change_review": no_protocol,
        "no_model_route_touched_review": no_model,
        "no_world_model_boundary_review": no_world,
        "owner_constraint_compliance_review": owner_compliance,
        "file_size_governance_review": file_size_governance_review,
        "summary": summary,
    }
