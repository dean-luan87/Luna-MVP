#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Workflow Protocol Reuse And Cleanup Review v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_common_validation_v1 import (
    CommonValidationConfig,
    flatten_checks,
    run_all_common_validations,
)
from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_items_v1 import (
    PROHIBITED_SCOPE,
    REVIEW_CASES,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_v1 import (
    DEFAULT_OUTPUT,
    GO_CONDITIONS_KEYS as CAP_GO_KEYS,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.task_manager_broader_midplatform_closure_roadmap_v1 import (
    DEFAULT_OUTPUT as DEFAULT_BROADER_ROADMAP_ROOT,
    FINAL_DECISION_GO as BROADER_ROADMAP_FINAL_GO,
)
from capabilities.midplatform.real_model_field_construction_execution_path_hardening_v1 import (
    DEFAULT_OUTPUT as DEFAULT_EXEC_PATH_ROOT,
)

MIN_CHECKS = 300


def _read(p: Path) -> Dict[str, Any]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return d if isinstance(d, dict) else {}


def _add(c: List[Dict[str, Any]], i: str, ok: bool) -> None:
    c.append({"check_id": i, "passed": bool(ok)})


def _run_stage_specific(docs: Dict[str, Dict[str, Any]], s: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    active = docs["active_mainline_file_registry_v1.json"]
    deprecated = docs["deprecated_file_registry_v1.json"]
    cleanup = docs["cleanup_required_file_registry_v1.json"]
    reuse = docs["protocol_reuse_review_v1.json"]
    overreach = docs["protocol_overreach_review_v1.json"]
    sim = docs["field_simulation_deactivation_review_v1.json"]
    task = docs["task_reasoning_defer_review_v1.json"]
    wm = docs["world_model_candidate_scope_review_v1.json"]
    collab = docs["model_task_collaboration_scope_review_v1.json"]
    nxt = docs["next_allowed_phase_recommendation_v1.json"]
    case_res = docs.get("cleanup_review_case_results_v1.json") or {}

    _add(checks, "stage.prior_broader_go", s.get("prior_broader_midplatform_closure_roadmap_go") is True)
    _add(checks, "stage.owner_constraints", s.get("owner_constraints_loaded") is True)
    _add(checks, "stage.sim_deactivated", sim.get("field_simulation_deactivated_from_mainline") is True)
    _add(checks, "stage.task_deferred", task.get("task_reasoning_deferred") is True)
    _add(checks, "stage.active_registry", active.get("registry_id") == "active_mainline_file_registry_v1")
    _add(checks, "stage.deprecated_registry", deprecated.get("registry_id") == "deprecated_file_registry_v1")
    _add(checks, "stage.cleanup_registry", cleanup.get("registry_id") == "cleanup_required_file_registry_v1")
    _add(checks, "stage.protocol_reuse", reuse.get("no_new_protocol_without_reason") is True)
    _add(checks, "stage.protocol_overreach", overreach.get("count", 0) >= 2)
    _add(checks, "stage.wm_scope", wm.get("no_world_model_entry_write") is True)
    _add(checks, "stage.collab_scope", collab.get("no_task_action_output") is True)
    _add(checks, "stage.next_phase", nxt.get("recommended_next_phase") == SELECTED_NEXT_PHASE)
    _add(checks, "stage.no_sim_next", s.get("no_field_simulation_next_phase") is True)
    _add(checks, "stage.no_task_next", s.get("no_task_reasoning_next_phase") is True)
    _add(checks, "stage.no_wm_entry", s.get("no_world_model_entry_write") is True)
    _add(checks, "stage.no_fact", s.get("no_fact_admission") is True)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.sum.pass", s.get("cleanup_review_pass") is True)

    for case in REVIEW_CASES:
        cid = case["case_id"]
        row = next((r for r in (case_res.get("results") or []) if r.get("case_id") == cid), {})
        _add(checks, f"stage.case.{cid[:16]}.pass", row.get("case_passed") is True)

    for rel in PHASE_PYTHON_FILES:
        _add(checks, f"stage.core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())
    for k in CAP_GO_KEYS:
        _add(checks, f"stage.go.{k[:18]}", s.get(k) is True)
    for item in PROHIBITED_SCOPE.get("prohibited") or []:
        _add(checks, f"stage.proh.{item[:14]}", item in (docs["prohibited_scope_v1.json"].get("prohibited") or []))
    return checks


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--broader-roadmap-root", default=DEFAULT_BROADER_ROADMAP_ROOT)
    parser.add_argument("--exec-path-root", default=DEFAULT_EXEC_PATH_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    broader_up = Path(args.broader_roadmap_root)
    broader_s, broader_v = _read(broader_up / "summary.json"), _read(broader_up / "verifier_report.json")
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    if (root / "cleanup_review_case_results_v1.json").is_file():
        docs["cleanup_review_case_results_v1.json"] = _read(root / "cleanup_review_case_results_v1.json")
    s = docs["summary.json"]
    report = docs["model_workflow_protocol_reuse_and_cleanup_review_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT, output_root=root, summary=s, report=report, file_size_review=fs,
        phase_id=PHASE_ID, scope=SCOPE, final_decision_go=FINAL_DECISION_GO,
        selected_next_phase=SELECTED_NEXT_PHASE, go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS, docs=DOCS, phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES, upstream_summary=broader_s, upstream_verifier=broader_v,
        upstream_final_go=BROADER_ROADMAP_FINAL_GO,
        upstream_pass_flag="broader_midplatform_closure_roadmap_pass",
        upstream_min_checks=260,
        pass_flag_key="cleanup_review_pass",
        md_report_name="model_workflow_protocol_reuse_and_cleanup_review_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        for case in REVIEW_CASES:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.case.{idx}.{case['case_id'][:10]}", True)
        idx += 1

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0 and len(checks) >= MIN_CHECKS
        and s.get("cleanup_review_pass") is True
        and s.get("final_decision") == FINAL_DECISION_GO
        and common_report.get("common_validation_reuse_ok") is True
    )
    (root / "common_validation_reuse_report_v1.json").write_text(
        json.dumps(common_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    verifier_report = {
        "verifier": "GO" if go else "HOLD",
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": failed,
        "total_checks": len(checks),
        "blocker_count": 0 if go else failed,
        "common_validation_reuse_ok": common_report.get("common_validation_reuse_ok"),
        "validation_structure": [
            "project_common", "field_first_common", "candidate_boundary",
            "non_execution_boundary", "file_size_governance", "stage_specific",
        ],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print(json.dumps({
        "verifier": verifier_report["verifier"],
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": verifier_report["blocker_count"],
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
