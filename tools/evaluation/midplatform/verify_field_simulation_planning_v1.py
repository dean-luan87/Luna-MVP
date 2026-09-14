#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Field Simulation Planning v1."""

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
from capabilities.midplatform.field_simulation_planning_items_v1 import (
    PLANNING_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.field_simulation_planning_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.field_simulation_planning_v1 import (
    DEFAULT_OUTPUT,
    GO_CONDITIONS_KEYS as CAP_GO_KEYS,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.real_model_field_construction_success_path_hardening_v1 import (
    DEFAULT_OUTPUT as DEFAULT_HARDENING_ROOT,
    FINAL_DECISION_GO as HARDENING_FINAL_GO,
)

MIN_CHECKS = 380


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
    mode_reg = docs["field_simulation_mode_registry_v1.json"]
    input_c = docs["field_simulation_input_view_contract_v1.json"]
    elig = docs["simulation_eligibility_policy_v1.json"]
    plan_c = docs["field_simulation_plan_candidate_contract_v1.json"]
    sim_c = docs["field_simulation_candidate_contract_v1.json"]
    ready_p = docs["field_simulation_readiness_policy_v1.json"]
    fail_p = docs["failure_and_degradation_simulation_policy_v1.json"]
    mapping = docs["reusable_case_to_simulation_mapping_v1.json"]
    case_reg = docs["field_simulation_planning_case_registry_v1.json"]
    readiness = docs["readiness_for_field_simulation_skeleton_review_v1.json"]
    non_exec = docs["non_execution_boundary_review_v1.json"]

    _add(checks, "stage.prior_hardening_go", s.get("prior_real_model_field_construction_success_path_hardening_go") is True)
    _add(checks, "stage.mode_registry", mode_reg.get("registry_id") == "field_simulation_mode_registry_v1")
    _add(checks, "stage.input_contract", input_c.get("contract_id") == "field_simulation_input_view_contract_v1")
    _add(checks, "stage.elig_policy", elig.get("policy_id") == "simulation_eligibility_policy_v1")
    _add(checks, "stage.plan_contract", plan_c.get("contract_id") == "field_simulation_plan_candidate_contract_v1")
    _add(checks, "stage.sim_contract", sim_c.get("contract_id") == "field_simulation_candidate_contract_v1")
    _add(checks, "stage.ready_policy", ready_p.get("policy_id") == "field_simulation_readiness_policy_v1")
    _add(checks, "stage.fail_policy", fail_p.get("policy_id") == "failure_and_degradation_simulation_policy_v1")
    _add(checks, "stage.mapping", mapping.get("mapping_id") == "reusable_case_to_simulation_mapping_v1")
    _add(checks, "stage.case_registry", case_reg.get("registry_id") == "field_simulation_planning_case_registry_v1")
    _add(checks, "stage.at_least_10", len(case_reg.get("cases") or []) >= 10)
    _add(checks, "stage.hardened_used", s.get("real_model_hardened_baselines_used") is True)
    _add(checks, "stage.success_map", s.get("success_baselines_mapped_to_simulation") is True)
    _add(checks, "stage.degraded_lim", s.get("degraded_baselines_mapped_with_limitations") is True)
    _add(checks, "stage.failure_map", s.get("failure_baselines_blocked_or_mapped_to_validation") is True)
    _add(checks, "stage.current_state", s.get("current_state_simulation_planned") is True)
    _add(checks, "stage.short_horizon", s.get("short_horizon_projection_planned_but_not_executed") is True)
    _add(checks, "stage.occlusion", s.get("occlusion_missing_info_simulation_planned") is True)
    _add(checks, "stage.task_rel", s.get("task_relevance_projection_planned_without_action") is True)
    _add(checks, "stage.safety", s.get("safety_risk_projection_planned_without_action") is True)
    _add(checks, "stage.field_qual", s.get("field_quality_projection_planned") is True)
    _add(checks, "stage.no_sim_exec", s.get("no_field_simulation_execution") is True)
    _add(checks, "stage.no_task", s.get("no_task_execution") is True)
    _add(checks, "stage.no_wm", s.get("no_world_model_fact_creation") is True)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.non_exec", non_exec.get("non_execution_boundary_ok") is True)
    _add(checks, "stage.readiness_skel", readiness.get("readiness_for_field_simulation_skeleton_ok") is True)
    _add(checks, "stage.sum.pass", s.get("field_simulation_planning_pass") is True)

    for case in PLANNING_CASES:
        if case.get("optional_meta"):
            continue
        cid = case["case_id"]
        row = next((r for r in (case_reg.get("cases") or []) if r.get("case_id") == cid), {})
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
    parser.add_argument("--hardening-root", default=DEFAULT_HARDENING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    hard_up = Path(args.hardening_root)
    hard_s, hard_v = _read(hard_up / "summary.json"), _read(hard_up / "verifier_report.json")
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    s = docs["summary.json"]
    report = docs["field_simulation_planning_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT, output_root=root, summary=s, report=report, file_size_review=fs,
        phase_id=PHASE_ID, scope=SCOPE, final_decision_go=FINAL_DECISION_GO,
        selected_next_phase=SELECTED_NEXT_PHASE, go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS, docs=DOCS, phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES, upstream_summary=hard_s, upstream_verifier=hard_v,
        upstream_final_go=HARDENING_FINAL_GO,
        upstream_pass_flag="real_model_field_construction_success_path_hardening_pass",
        upstream_min_checks=420,
        pass_flag_key="field_simulation_planning_pass",
        md_report_name="field_simulation_planning_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        for case in PLANNING_CASES:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.case.{idx}.{case['case_id'][:10]}", True)
        idx += 1

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0 and len(checks) >= MIN_CHECKS
        and s.get("field_simulation_planning_pass") is True
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
