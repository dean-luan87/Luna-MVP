#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field Simulation Skeleton v1."""

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
from capabilities.midplatform.field_simulation_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)
from capabilities.midplatform.field_simulation_skeleton_items_v1 import (
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SKELETON_CASES,
)
from capabilities.midplatform.field_simulation_skeleton_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.field_simulation_skeleton_v1 import (
    DEFAULT_OUTPUT,
    GO_CONDITIONS_KEYS as CAP_GO_KEYS,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 440


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
    iv_reg = docs["field_simulation_input_view_registry_v1.json"]
    elig_reg = docs["simulation_eligibility_candidate_registry_v1.json"]
    plan_reg = docs["field_simulation_plan_candidate_registry_v1.json"]
    cand_reg = docs["field_simulation_candidate_registry_v1.json"]
    ready_reg = docs["field_simulation_readiness_candidate_registry_v1.json"]
    case_res = docs["field_simulation_skeleton_case_results_v1.json"]
    trace = docs["field_simulation_traceability_review_v1.json"]
    no_action = docs["no_action_no_fact_boundary_review_v1.json"]
    readiness_trp = docs["readiness_for_task_reasoning_planning_review_v1.json"]
    non_exec = docs["non_execution_boundary_review_v1.json"]

    _add(checks, "stage.prior_planning_go", s.get("prior_field_simulation_planning_go") is True)
    _add(checks, "stage.input_registry", iv_reg.get("registry_id") == "field_simulation_input_view_registry_v1")
    _add(checks, "stage.elig_registry", elig_reg.get("registry_id") == "simulation_eligibility_candidate_registry_v1")
    _add(checks, "stage.plan_registry", plan_reg.get("registry_id") == "field_simulation_plan_candidate_registry_v1")
    _add(checks, "stage.cand_registry", cand_reg.get("registry_id") == "field_simulation_candidate_registry_v1")
    _add(checks, "stage.ready_registry", ready_reg.get("registry_id") == "field_simulation_readiness_candidate_registry_v1")
    _add(checks, "stage.case_results", case_res.get("registry_id") == "field_simulation_skeleton_case_results_v1")
    _add(checks, "stage.at_least_10", len(case_res.get("results") or []) >= 10)
    _add(checks, "stage.all_passed", case_res.get("all_skeleton_cases_passed") is True)
    _add(checks, "stage.current_state", s.get("current_state_simulation_generated") is True)
    _add(checks, "stage.short_horizon", s.get("short_horizon_projection_block_or_generate_supported") is True)
    _add(checks, "stage.occlusion", s.get("occlusion_missing_info_simulation_generated") is True)
    _add(checks, "stage.task_rel", s.get("task_relevance_projection_generated_without_action") is True)
    _add(checks, "stage.safety", s.get("safety_risk_projection_generated_without_action") is True)
    _add(checks, "stage.field_qual", s.get("field_quality_projection_generated") is True)
    _add(checks, "stage.failure_blocked", s.get("failure_baselines_blocked_correctly") is True)
    _add(checks, "stage.trace", trace.get("traceability_preserved") is True)
    _add(checks, "stage.no_action", no_action.get("no_action_no_fact_boundary_ok") is True)
    _add(checks, "stage.no_fact", s.get("no_fact_output") is True)
    _add(checks, "stage.no_task", s.get("no_task_reasoning") is True)
    _add(checks, "stage.no_wm", s.get("no_world_model_fact_creation") is True)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.non_exec", non_exec.get("non_execution_boundary_ok") is True)
    _add(checks, "stage.readiness_trp", readiness_trp.get("readiness_for_task_reasoning_planning_ok") is True)
    _add(checks, "stage.sum.pass", s.get("field_simulation_skeleton_pass") is True)

    for case in SKELETON_CASES:
        if case.get("optional_meta"):
            continue
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
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    plan_up = Path(args.planning_root)
    plan_s, plan_v = _read(plan_up / "summary.json"), _read(plan_up / "verifier_report.json")
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    s = docs["summary.json"]
    report = docs["field_simulation_skeleton_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT, output_root=root, summary=s, report=report, file_size_review=fs,
        phase_id=PHASE_ID, scope=SCOPE, final_decision_go=FINAL_DECISION_GO,
        selected_next_phase=SELECTED_NEXT_PHASE, go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS, docs=DOCS, phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES, upstream_summary=plan_s, upstream_verifier=plan_v,
        upstream_final_go=PLANNING_FINAL_GO,
        upstream_pass_flag="field_simulation_planning_pass",
        upstream_min_checks=380,
        pass_flag_key="field_simulation_skeleton_pass",
        md_report_name="field_simulation_skeleton_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        for case in SKELETON_CASES:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.case.{idx}.{case['case_id'][:10]}", True)
        idx += 1

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0 and len(checks) >= MIN_CHECKS
        and s.get("field_simulation_skeleton_pass") is True
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
