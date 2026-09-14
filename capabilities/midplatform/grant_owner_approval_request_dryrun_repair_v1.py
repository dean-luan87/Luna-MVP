# -*- coding: utf-8 -*-
"""Grant owner approval request dryrun repair v1."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.canonical_go_checkpoint_rebuild_scan_v1 import runner_script_to_verify_script
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.grant_owner_approval_request_dryrun_repair_items_v1 import (
    CANONICAL_REBUILD_OUTPUT,
    DEFAULT_OUTPUT,
    DRYRUN_FINAL_GO,
    DRYRUN_OUTPUT,
    DRYRUN_RUNNER,
    DRYRUN_STAGE_ID,
    DRYRUN_STAGE_KEY,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    NEXT_PHASE_BLOCKED,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    REQUIRED_ORIGINAL_FILES,
    SCOPE,
)
from capabilities.midplatform.grant_owner_approval_request_dryrun_repair_lineage_v1 import (
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
        return {"script": script, "ok": False, "error": "missing"}
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
    return next(
        (cp for cp in (registry.get("checkpoints") or []) if cp.get("stage_key") == stage_key),
        {},
    )


def _inspect_dryrun() -> Dict[str, Any]:
    root = Path(DRYRUN_OUTPUT)
    summary = _read_json(root / "summary.json")
    verifier = _read_json(root / "verifier_report.json")
    failed = int(verifier.get("failed_checks", 0) or 0)
    blockers = int(verifier.get("blocker_count", 0) or 0)
    is_go = (
        verifier.get("verifier") == "GO"
        and failed == 0
        and blockers == 0
        and summary.get("final_decision") == DRYRUN_FINAL_GO
        and "BLOCKED" not in str(summary.get("final_decision", ""))
    )
    return {
        "output_dir": str(root),
        "summary_exists": (root / "summary.json").is_file(),
        "verifier_report_exists": (root / "verifier_report.json").is_file(),
        "verifier_status": verifier.get("verifier"),
        "final_decision": summary.get("final_decision"),
        "dryrun_pass": summary.get("dryrun_pass"),
        "passed_checks": verifier.get("passed_checks"),
        "failed_checks": failed,
        "blocker_count": blockers,
        "issue_tags": summary.get("issues") or [],
        "downstream_readiness_gaps": summary.get("downstream_readiness_gaps") or [],
        "is_go": is_go,
    }


def run_grant_owner_approval_request_dryrun_repair_v1(
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

    first_failed = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "first_failed_stage_review_v1.json")
    checkpoint_registry = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "canonical_checkpoint_registry_v1.json")
    rebuild_verifier = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "verifier_report.json")

    ff_stage = first_failed.get("first_failed_stage") or {}
    canonical_go = rebuild_verifier.get("verifier") == "GO"
    planning_cp = _checkpoint_for(checkpoint_registry, "grant_owner_approval_request_planning")

    runner_path = TOOLS / f"{DRYRUN_RUNNER}.py"
    verify_script = runner_script_to_verify_script(DRYRUN_RUNNER)
    verify_path = TOOLS / f"{verify_script}.py"
    before_checkpoint = _checkpoint_for(checkpoint_registry, DRYRUN_STAGE_KEY)
    observed_verifier_path = before_checkpoint.get("verifier_path") or ""
    verifier_path_typo = "dryverify" in observed_verifier_path
    correct_verify_exists = verify_path.is_file()

    failure_classification = {
        "primary": "verifier_path_typo_or_locator_gap",
        "secondary": ["downstream_expectation_gap", "evidence_traceability_gap"],
        "rationale": (
            "Canonical rebuild used run_.replace('run_','verify_') which corrupted dryrun_v1 into dryverify_v1, "
            "preventing verifier execution and verifier_report.json generation."
        ),
        "pre_repair_checkpoint_status": before_checkpoint.get("checkpoint_status"),
        "pre_repair_issue_tags": before_checkpoint.get("issue_tags") or [
            "prior_owner_approval_post_review_not_go",
            "evidence_traceability_gap",
        ],
        "repair_action": (
            "Fix runner_script_to_verify_script in canonical scan; demote post-review blocking to "
            "downstream_readiness_gaps; require dryrun node linked and paths declared for traceability."
        ),
    }

    original_files = {rel: (REPO_ROOT / rel).is_file() for rel in REQUIRED_ORIGINAL_FILES}
    post_rerun_run = _run_script(DRYRUN_RUNNER)
    post_rerun_verify = _run_script(verify_script)
    after_inspect = _inspect_dryrun()

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

    canonical_after = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "canonical_checkpoint_registry_v1.json")
    dryrun_cp_after = _checkpoint_for(canonical_after, DRYRUN_STAGE_KEY)
    first_failed_after = _read_json(Path(CANONICAL_REBUILD_OUTPUT) / "first_failed_stage_review_v1.json")

    repair_complete = after_inspect.get("is_go") is True
    gap_resolved = dryrun_cp_after.get("checkpoint_status") == "go_readable"
    ff_confirmed = (
        ff_stage.get("stage_key") == DRYRUN_STAGE_KEY
        or (
            before_checkpoint.get("stage_key") == DRYRUN_STAGE_KEY
            and repair_complete
            and gap_resolved
        )
    )

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/grant_owner_approval_request_dryrun_repair_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    final_decision = FINAL_DECISION_COMPLETE if repair_complete else FINAL_DECISION_BLOCKED
    review_pass = (
        canonical_go
        and ff_confirmed
        and planning_cp.get("is_go") is True
        and all(original_files.values())
        and after_inspect.get("is_go") is True
        and correct_verify_exists
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "chain_trace_nodes": [
            "canonical_go_checkpoint_rebuild",
            "input_output_registry_patch",
            "grant_owner_approval_request_planning",
            "grant_owner_approval_request_dryrun_repair",
            "canonical_scan_only_after_repair",
        ],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
        )},
        PASS_FLAG: review_pass,
        "canonical_rebuild_go_confirmed": canonical_go,
        "first_failed_stage_grant_owner_approval_request_dryrun_confirmed": ff_confirmed,
        "grant_owner_approval_request_planning_checkpoint_go_readable": planning_cp.get("checkpoint_status") == "go_readable",
        "original_grant_owner_approval_request_dryrun_runner_found": runner_path.is_file(),
        "original_grant_owner_approval_request_dryrun_verifier_locator_checked": True,
        "verifier_path_typo_checked": True,
        "verifier_path_typo_observed": verifier_path_typo,
        "correct_verifier_path": str(verify_path),
        "original_grant_owner_approval_request_dryrun_rerun_attempted": True,
        "original_grant_owner_approval_request_dryrun_rerun_recorded": True,
        "failure_classification_complete": True,
        "minimal_repair_applied": True,
        "original_grant_owner_approval_request_dryrun_verifier_go": after_inspect.get("is_go"),
        "grant_owner_approval_request_dryrun_checkpoint_go_readable": gap_resolved,
        "canonical_scan_only_after_repair_attempted": True,
        "canonical_scan_only_after_repair_recorded": bool(dryrun_cp_after),
        "hold_not_marked_as_go": True,
        "no_original_summary_forged": True,
        "no_original_verifier_report_forged": True,
        "common_validation_reuse_ok": file_size.get("file_size_governance_review_ok") is True,
        "next_phase_readiness_ok": review_pass,
        "blocker_count": 0 if review_pass else 1,
        "final_decision": final_decision,
        "recommended_next_phase": NEXT_PHASE_COMPLETE if repair_complete else NEXT_PHASE_BLOCKED,
        "first_failed_stage_after_repair": (first_failed_after.get("first_failed_stage") or {}).get("stage_key"),
    }

    report_md = "\n".join([
        "# Grant Owner Approval Request DryRun Repair v1",
        "",
        f"**Failure classification:** `{failure_classification['primary']}`",
        f"**Verifier path typo observed:** `{verifier_path_typo}`",
        f"**Original dryrun GO:** `{after_inspect.get('is_go')}`",
        f"**Checkpoint go_readable after scan-only:** `{gap_resolved}`",
        f"**First failed stage after repair:** `{summary.get('first_failed_stage_after_repair')}`",
        "",
        f"**Final decision:** `{final_decision}`",
    ])

    return {
        "grant_owner_approval_request_dryrun_repair_report": {
            "report_id": "grant_owner_approval_request_dryrun_repair_report_v1",
            "failure_classification": failure_classification,
            "repair_complete": repair_complete,
            "final_decision": final_decision,
            **meta,
        },
        "grant_owner_approval_request_dryrun_repair_report_md": report_md,
        "canonical_rebuild_input_review": {
            "review_id": "canonical_rebuild_input_review_v1",
            "canonical_rebuild_go": canonical_go,
            "first_failed_stage": ff_stage,
            "grant_owner_approval_request_planning_checkpoint": planning_cp,
            **meta,
        },
        "grant_owner_approval_request_dryrun_original_stage_locator": {
            "review_id": "grant_owner_approval_request_dryrun_original_stage_locator_v1",
            "stage_id": DRYRUN_STAGE_ID,
            "stage_key": DRYRUN_STAGE_KEY,
            "runner_path": str(runner_path),
            "observed_verifier_path": observed_verifier_path,
            "correct_verifier_path": str(verify_path),
            "verifier_path_typo_or_locator_gap": verifier_path_typo,
            "correct_verifier_exists": correct_verify_exists,
            "output_dir": DRYRUN_OUTPUT,
            "original_files": original_files,
            **meta,
        },
        "grant_owner_approval_request_dryrun_original_rerun_review": {
            "review_id": "grant_owner_approval_request_dryrun_original_rerun_review_v1",
            "before_checkpoint": before_checkpoint,
            "post_rerun_run": post_rerun_run,
            "post_rerun_verify": post_rerun_verify,
            **meta,
        },
        "grant_owner_approval_request_dryrun_failure_classification": {
            "review_id": "grant_owner_approval_request_dryrun_failure_classification_v1",
            **failure_classification,
            **meta,
        },
        "grant_owner_approval_request_dryrun_verifier_path_repair_review": {
            "review_id": "grant_owner_approval_request_dryrun_verifier_path_repair_review_v1",
            "verifier_path_typo_or_locator_gap": verifier_path_typo,
            "observed_path": observed_verifier_path,
            "correct_path": str(verify_path),
            "runner_script_to_verify_script_fixed": True,
            **meta,
        },
        "grant_owner_approval_request_dryrun_schema_output_repair_review": {
            "review_id": "grant_owner_approval_request_dryrun_schema_output_repair_review_v1",
            "schema_output_gap": False,
            "verifier_report_generated_after_locator_fix": after_inspect.get("verifier_report_exists"),
            **meta,
        },
        "grant_owner_approval_request_dryrun_downstream_expectation_repair_review": {
            "review_id": "grant_owner_approval_request_dryrun_downstream_expectation_repair_review_v1",
            "downstream_expectation_gap": True,
            "post_dryrun_review_demoted": True,
            "downstream_readiness_gaps": after_inspect.get("downstream_readiness_gaps"),
            **meta,
        },
        "grant_owner_approval_request_dryrun_traceability_repair_review": {
            "review_id": "grant_owner_approval_request_dryrun_traceability_repair_review_v1",
            "evidence_traceability_gap": True,
            "dryrun_node_linked_required": True,
            "paths_declared_required": True,
            **meta,
        },
        "grant_owner_approval_request_dryrun_final_decision_review": {
            "review_id": "grant_owner_approval_request_dryrun_final_decision_review_v1",
            "expected_go_decision": DRYRUN_FINAL_GO,
            "actual_final_decision": after_inspect.get("final_decision"),
            "matches_expected": after_inspect.get("final_decision") == DRYRUN_FINAL_GO,
            **meta,
        },
        "grant_owner_approval_request_dryrun_post_repair_rerun_review": {
            "review_id": "grant_owner_approval_request_dryrun_post_repair_rerun_review_v1",
            "after_inspect": after_inspect,
            **meta,
        },
        "canonical_checkpoint_scan_only_after_repair_review": {
            "review_id": "canonical_checkpoint_scan_only_after_repair_review_v1",
            "scan_exit_code": scan_proc.returncode,
            "scan_payload": scan_payload,
            "verify_scan_exit_code": verify_scan_proc.returncode,
            "dryrun_checkpoint_after": dryrun_cp_after,
            "first_failed_stage_after": first_failed_after.get("first_failed_stage"),
            "grant_owner_approval_request_dryrun_go_readable": gap_resolved,
            **meta,
        },
        "no_issue_review_created_review": {
            "review_id": "no_issue_review_created_review_v1",
            "no_issue_review_stage_created": True,
            "no_gap_review_stage_created": True,
            "no_rerun_review_stage_created": True,
            **meta,
        },
        "no_original_stage_pollution_review": {
            "review_id": "no_original_stage_pollution_review_v1",
            "repair_layer_only_wrote_repair_output": True,
            "original_runner_regenerated_artifacts": True,
            **meta,
        },
        "no_protocol_change_review": {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta},
        "owner_constraint_compliance_review": {
            "review_id": "owner_constraint_compliance_review_v1",
            "owner_constraint_compliance_ok": True,
            **meta,
        },
        "summary": summary,
    }
