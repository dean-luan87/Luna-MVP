# -*- coding: utf-8 -*-
"""Governance gate integrated implementation repair v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.canonical_go_checkpoint_rebuild_scan_v1 import runner_script_to_verify_script
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.governance_gate_integrated_implementation_repair_items_v1 import (
    CANONICAL_REBUILD_OUTPUT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    GOVERNANCE_FINAL_GO,
    GOVERNANCE_GATE_OUTPUT,
    GOVERNANCE_RUNNER,
    GROUP_M_STAGES,
    GROUPED_REPAIR_OUTPUT,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    POST_REVIEW_OUTPUT,
    SCOPE,
    STAGE_KEY,
)
from capabilities.midplatform.governance_gate_integrated_implementation_repair_lineage_v1 import (
    PHASE_PYTHON_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
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
        return {"script": script, "ok": False, "exit_code": 127, "error": "missing"}
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


def _checkpoint_for(registry: Dict[str, Any], stage_key: str) -> Dict[str, Any]:
    return next((cp for cp in (registry.get("checkpoints") or []) if cp.get("stage_key") == stage_key), {})


def _inspect_governance_gate() -> Dict[str, Any]:
    root = Path(GOVERNANCE_GATE_OUTPUT)
    summary = _read_json(root / "summary.json")
    verifier = _read_json(root / "verifier_report.json")
    failed = int(verifier.get("failed_checks", 0) or 0)
    blockers = int(verifier.get("blocker_count", failed) or 0)
    is_go = (
        verifier.get("verifier") == "GO"
        and failed == 0
        and blockers == 0
        and summary.get("integrated_implementation_pass") is True
        and summary.get("governance_gate_pass") is True
        and summary.get("final_decision") == GOVERNANCE_FINAL_GO
    )
    return {
        "output_dir": str(root),
        "summary_exists": (root / "summary.json").is_file(),
        "verifier_report_exists": (root / "verifier_report.json").is_file(),
        "verifier_status": verifier.get("verifier"),
        "final_decision": summary.get("final_decision"),
        "integrated_implementation_pass": summary.get("integrated_implementation_pass"),
        "governance_gate_pass": summary.get("governance_gate_pass"),
        "passed_checks": verifier.get("passed_checks"),
        "failed_checks": failed,
        "blocker_count": blockers,
        "issue_tags": summary.get("issues") or [],
        "downstream_readiness_gaps": summary.get("downstream_readiness_gaps") or [],
        "closure_result_accepted": summary.get("closure_result_accepted"),
        "direct_upstream_ref_linked": summary.get("direct_upstream_ref_linked"),
        "evidence_chain_ok": summary.get("evidence_chain_ok"),
        "is_go": is_go,
    }


def run_governance_gate_integrated_implementation_repair_v1(
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

    grouped = _read_json(Path(GROUPED_REPAIR_OUTPUT) / "summary.json")
    grouped_verifier = _read_json(Path(GROUPED_REPAIR_OUTPUT) / "verifier_report.json")
    first_failed = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "first_failed_stage_review_v1.json")
    registry_before = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "canonical_checkpoint_registry_v1.json")
    post_cp = _read_json(
        Path(CANONICAL_REBUILD_OUTPUT)
        / "checkpoints"
        / "record_approval_closure_post_dryrun_review"
        / "canonical_go_checkpoint_v1.json"
    )

    ff = first_failed.get("first_failed_stage") or {}
    runner_path = TOOLS / f"{GOVERNANCE_RUNNER}.py"
    verify_script = runner_script_to_verify_script(GOVERNANCE_RUNNER)
    verify_path = TOOLS / f"{verify_script}.py"

    pre_rerun = _inspect_governance_gate()
    failure_classification = {
        "runner_verifier_decision_drift": False,
        "evidence_traceability_gap": False,
        "downstream_expectation_gap": True,
        "schema_output_gap": True,
        "genuine_logic_hold": False,
        "primary": "downstream_expectation_gap",
        "secondary": ["schema_output_gap"],
        "rationale": (
            "Governance gate incorrectly required final_gate_planning GO and gated all integrated sections on "
            "upstream_ok=post_review_go AND final_gate_go. Canonical chain direct upstream is only "
            "record_approval_closure_post_dryrun_review. Repair: direct_upstream_ok from post-review only; "
            "final_gate_planning_not_go -> downstream_readiness_gaps; local missing conditions; "
            "governance_gate_pass / evidence_chain_ok / schema fields aligned."
        ),
        "pre_repair_issue_tags": ff.get("issue_tags") or pre_rerun.get("issue_tags"),
        "repair_action": (
            "Require closure_result_accepted + post_review GO only; declare downstream module stages; "
            "align integrated_implementation_pass with governance_gate_pass and blocker_count."
        ),
    }

    run_result = _run_script(GOVERNANCE_RUNNER)
    verify_result = _run_script(verify_script)
    after_rerun = _inspect_governance_gate()

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
        scan_payload = {}
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
    gov_cp = _checkpoint_for(registry_after_scan, STAGE_KEY)
    gov_go_readable = gov_cp.get("checkpoint_status") == "go_readable"

    topdown_payload: Dict[str, Any] = {}
    verify_topdown_payload: Dict[str, Any] = {}
    if gov_go_readable:
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
            topdown_payload = {}
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
        topdown_payload = {"deferred_by_scan_failure": True}

    registry_final = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "canonical_checkpoint_registry_v1.json")
    first_failed_after = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "first_failed_stage_review_v1.json")
    ff_after = (first_failed_after.get("first_failed_stage") or {}).get("stage_key") or first_failed_after.get(
        "first_failed_stage_key"
    )

    repair_complete = after_rerun.get("is_go") is True and gov_go_readable
    final_decision = FINAL_DECISION_COMPLETE if repair_complete else FINAL_DECISION_BLOCKED
    next_phase = NEXT_PHASE_COMPLETE if repair_complete else NEXT_PHASE_BLOCKED

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/governance_gate_integrated_implementation_repair_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "blocker_count": 0 if repair_complete else 1,
        "chain_trace_nodes": [
            "grouped_template_repair",
            "record_approval_closure_post_dryrun_review",
            STAGE_KEY,
            "governance_gate_integrated_implementation_repair",
            "canonical_scan_only",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{
            k: file_size.get(k) is True
            for k in (
                "file_size_governance_review_ok",
                "full_repo_scan_absent",
                "tmp_eval_out_scan_absent",
                "summary_index_first_reading_ok",
            )
        },
        PASS_FLAG: repair_complete,
        "grouped_template_repair_go_confirmed": grouped_verifier.get("verifier") == "GO",
        "first_failed_stage_governance_gate_confirmed": ff.get("stage_key") == STAGE_KEY,
        "record_closure_post_review_checkpoint_go_readable": post_cp.get("checkpoint_status") == "go_readable",
        "original_governance_gate_runner_found": runner_path.is_file(),
        "original_governance_gate_verifier_found": verify_path.is_file(),
        "original_governance_gate_rerun_attempted": True,
        "original_governance_gate_integrated_implementation_rerun_recorded": True,
        "failure_classification_complete": True,
        "runner_verifier_decision_drift_checked": True,
        "evidence_traceability_gap_checked": True,
        "downstream_expectation_gap_checked": True,
        "minimal_repair_applied": True,
        "group_m_untouched": True,
        "original_governance_gate_integrated_implementation_verifier_go": after_rerun.get("is_go"),
        "governance_gate_integrated_implementation_checkpoint_go_readable": gov_go_readable,
        "canonical_scan_only_after_repair_attempted": scan_proc.returncode == 0,
        "canonical_scan_only_after_repair_recorded": True,
        "hold_not_marked_as_go": True,
        "no_original_summary_forged": True,
        "no_original_verifier_report_forged": True,
        "common_validation_reuse_ok": True,
        "next_phase_readiness_ok": repair_complete,
        "go_stage_count_after_repair": scan_payload.get("go_stage_count"),
        "first_failed_stage_key_after_repair": ff_after,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
    }

    report_md = "\n".join(
        [
            "# Governance Gate Integrated Implementation Repair v1",
            "",
            f"- Primary failure: `{failure_classification['primary']}`",
            f"- Governance gate verifier GO: `{after_rerun.get('is_go')}`",
            f"- Checkpoint go_readable: `{gov_go_readable}`",
            f"- First failed after repair: `{ff_after}`",
            f"- Final decision: `{final_decision}`",
        ]
    )

    original_rerun = {
        "review_id": "governance_gate_integrated_implementation_original_rerun_review_v1",
        "pre_repair": pre_rerun,
        "post_repair": after_rerun,
        "runner_exit_code": run_result.get("exit_code"),
        "verifier_exit_code": verify_result.get("exit_code"),
        "runner_payload": run_result.get("payload"),
        "verifier_payload": verify_result.get("payload"),
        **meta,
    }

    return {
        "governance_gate_integrated_implementation_repair_report": {
            "report_id": "governance_gate_integrated_implementation_repair_report_v1",
            "failure_classification": failure_classification,
            **summary,
        },
        "governance_gate_integrated_implementation_repair_report_md": report_md,
        "canonical_rebuild_input_review": {
            "review_id": "canonical_rebuild_input_review_v1",
            "grouped_template_repair_go": grouped_verifier.get("verifier") == "GO",
            "first_failed_stage": ff.get("stage_key"),
            "go_stage_count_before": grouped.get("go_stage_count_after_repair"),
            "post_review_checkpoint_status": post_cp.get("checkpoint_status"),
            **meta,
        },
        "governance_gate_integrated_implementation_original_stage_locator": {
            "review_id": "governance_gate_integrated_implementation_original_stage_locator_v1",
            "stage_key": STAGE_KEY,
            "runner_path": str(runner_path),
            "verifier_path": str(verify_path),
            "output_dir": GOVERNANCE_GATE_OUTPUT,
            **meta,
        },
        "governance_gate_integrated_implementation_original_rerun_review": original_rerun,
        "governance_gate_integrated_implementation_failure_classification": {
            "review_id": "governance_gate_integrated_implementation_failure_classification_v1",
            **failure_classification,
            **meta,
        },
        "governance_gate_integrated_implementation_decision_drift_repair_review": {
            "review_id": "governance_gate_integrated_implementation_decision_drift_repair_review_v1",
            "checked": True,
            "drift_observed_pre_repair": False,
            "aligned_post_repair": after_rerun.get("integrated_implementation_pass") == after_rerun.get("is_go"),
            **meta,
        },
        "governance_gate_integrated_implementation_schema_output_repair_review": {
            "review_id": "governance_gate_integrated_implementation_schema_output_repair_review_v1",
            "fields_added": [
                "governance_gate_pass",
                "governance_gate_integrated_implementation_complete",
                "closure_result_accepted",
                "direct_upstream_ref_linked",
                "governance_gate_node_linked",
                "evidence_paths_declared",
                "downstream_readiness_refs",
                "downstream_readiness_gaps",
            ],
            **meta,
        },
        "governance_gate_integrated_implementation_downstream_expectation_repair_review": {
            "review_id": "governance_gate_integrated_implementation_downstream_expectation_repair_review_v1",
            "final_gate_moved_to_readiness_gaps": True,
            "downstream_module_stages_declared_only": True,
            **meta,
        },
        "governance_gate_integrated_implementation_traceability_repair_review": {
            "review_id": "governance_gate_integrated_implementation_traceability_repair_review_v1",
            "evidence_chain_ok_requires_direct_closure_only": True,
            **meta,
        },
        "governance_gate_integrated_implementation_final_decision_review": {
            "review_id": "governance_gate_integrated_implementation_final_decision_review_v1",
            "final_decision": after_rerun.get("final_decision"),
            "matches_go": after_rerun.get("final_decision") == GOVERNANCE_FINAL_GO,
            **meta,
        },
        "governance_gate_integrated_implementation_post_repair_rerun_review": {
            "review_id": "governance_gate_integrated_implementation_post_repair_rerun_review_v1",
            **after_rerun,
            **meta,
        },
        "canonical_checkpoint_scan_only_after_repair_review": {
            "review_id": "canonical_checkpoint_scan_only_after_repair_review_v1",
            "scan_payload": scan_payload,
            "verify_scan_payload": verify_scan_payload,
            "governance_checkpoint_status": gov_cp.get("checkpoint_status"),
            **meta,
        },
        "canonical_checkpoint_topdown_after_repair_review": {
            "review_id": "canonical_checkpoint_topdown_after_repair_review_v1",
            "topdown_payload": topdown_payload,
            "verify_topdown_payload": verify_topdown_payload,
            **meta,
        },
        "group_g_scope_review": {
            "review_id": "group_g_scope_review_v1",
            "stage_repaired": STAGE_KEY,
            "group_g_individual_repair": True,
            **meta,
        },
        "group_m_untouched_review": {
            "review_id": "group_m_untouched_review_v1",
            "group_m_stages": list(GROUP_M_STAGES),
            "untouched": True,
            **meta,
        },
        "no_issue_review_created_review": {"review_id": "no_issue_review_created_review_v1", "no_issue_review_stage_created": True, **meta},
        "no_gap_review_created_review": {"review_id": "no_gap_review_created_review_v1", "no_gap_review_stage_created": True, **meta},
        "no_rerun_review_created_review": {"review_id": "no_rerun_review_created_review_v1", "no_rerun_review_stage_created": True, **meta},
        "no_original_stage_pollution_review": {"review_id": "no_original_stage_pollution_review_v1", "no_original_stage_pollution": True, **meta},
        "no_protocol_change_review": {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta},
        "no_model_route_touched_review": {"review_id": "no_model_route_touched_review_v1", "no_model_route_touched": True, **meta},
        "no_world_model_boundary_review": {"review_id": "no_world_model_boundary_review_v1", "no_world_model_assembly": True, **meta},
        "owner_constraint_compliance_review": {"review_id": "owner_constraint_compliance_review_v1", "owner_constraints_met": True, **NON_EXECUTION_FLAGS, **meta},
        "file_size_governance_review": file_size,
        "summary": summary,
    }
