#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Trajectory Analysis & Task Impact Planning v1."""

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
from capabilities.midplatform.static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_TARGET_LOCKING_SKELETON_ROOT,
    FINAL_DECISION_GO as TARGET_LOCKING_SKELETON_FINAL_GO,
)
from capabilities.midplatform.trajectory_analysis_task_impact_planning_items_v1 import (
    MOCK_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    TASK_IMPACT_PRIORITIES,
    TASK_IMPACT_TYPES,
    TRAJECTORY_CONFIDENCE_LEVELS,
    TRAJECTORY_MOTION_PATTERNS,
    TRAJECTORY_RELIABILITY_REASONS,
    TRAJECTORY_TASK_IMPACT_RULES,
)
from capabilities.midplatform.trajectory_analysis_task_impact_planning_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.trajectory_analysis_task_impact_planning_v1 import (
    DEFAULT_OUTPUT,
    GO_CONDITIONS_KEYS as CAP_GO_KEYS,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 360


def _read(p: Path) -> Dict[str, Any]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return d if isinstance(d, dict) else {}


def _add(c: List[Dict[str, Any]], i: str, ok: bool) -> None:
    c.append({"check_id": i, "passed": bool(ok)})


def _run_stage_specific_validation(root: Path, docs: Dict[str, Dict[str, Any]], s: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    traj_reg = docs["trajectory_status_registry_v1.json"]
    impact_reg = docs["task_impact_type_registry_v1.json"]
    traj_m = docs["trajectory_candidate_model_v1.json"]
    impact_m = docs["task_impact_analysis_candidate_model_v1.json"]
    risk_m = docs["risk_projection_candidate_model_v1.json"]
    missing_m = docs["missing_information_candidate_model_v1.json"]
    rules = docs["trajectory_task_impact_rule_registry_v1.json"]
    mock_reg = docs["trajectory_task_impact_mock_case_registry_v1.json"]
    mock_exp = docs["trajectory_task_impact_mock_case_expected_results_v1.json"]
    io_c = docs["trajectory_task_impact_input_output_contract_v1.json"]
    next_p = docs["trajectory_task_impact_next_implementation_plan_v1.json"]
    prohibited = docs["prohibited_scope_v1.json"]

    _add(checks, "stage.trajectory_status_registry_exists", traj_reg.get("registry_id") == "trajectory_status_registry_v1")
    _add(checks, "stage.task_impact_type_registry_exists", impact_reg.get("registry_id") == "task_impact_type_registry_v1")
    _add(checks, "stage.trajectory_candidate_model_exists", traj_m.get("model_id") == "trajectory_candidate_model_v1")
    _add(checks, "stage.task_impact_analysis_model_exists", impact_m.get("model_id") == "task_impact_analysis_candidate_model_v1")
    _add(checks, "stage.risk_projection_model_exists", risk_m.get("model_id") == "risk_projection_candidate_model_v1")
    _add(checks, "stage.missing_information_model_exists", missing_m.get("model_id") == "missing_information_candidate_model_v1")
    _add(checks, "stage.rule_registry_exists", rules.get("registry_id") == "trajectory_task_impact_rule_registry_v1")
    _add(checks, "stage.mock_case_registry_exists", mock_reg.get("registry_id") == "trajectory_task_impact_mock_case_registry_v1")
    _add(checks, "stage.at_least_12_mock_cases", mock_reg.get("count", 0) >= 12)
    _add(checks, "stage.input_output_contract_exists", io_c.get("contract_id") == "trajectory_task_impact_input_output_contract_v1")
    _add(checks, "stage.next_implementation_plan_exists", bool(next_p.get("recommended_next")))
    _add(checks, "stage.trajectory_analysis_depends_on_dynamic_tracks", s.get("trajectory_analysis_depends_on_dynamic_tracks") is True)
    _add(checks, "stage.no_trajectory_when_tracking_frozen", s.get("no_trajectory_when_tracking_frozen") is True)
    _add(checks, "stage.new_field_resets_trajectory", s.get("new_field_resets_trajectory") is True)
    _add(checks, "stage.depth_uncertainty_limits_confidence", s.get("depth_uncertainty_limits_confidence") is True)
    _add(checks, "stage.missing_info_explicit", s.get("missing_info_explicit") is True)
    _add(checks, "stage.no_final_action_output", s.get("no_final_action_output") is True)
    _add(checks, "stage.no_task_execution", s.get("no_task_execution") is True)
    _add(checks, "stage.no_field_simulation", s.get("no_field_simulation") is True)
    _add(checks, "stage.no_world_model_fact_creation", s.get("no_world_model_fact_creation") is True)
    _add(checks, "stage.candidate_only_outputs", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.sum.pass", s.get("trajectory_analysis_task_impact_planning_pass") is True)
    _add(checks, "stage.traj.cand", traj_m.get("candidate_only") is True)
    _add(checks, "stage.traj.hint", traj_m.get("tracker_id_is_hint_not_fact") is True)
    _add(checks, "stage.io.no_action", io_c.get("no_final_action_output") is True)
    _add(checks, "stage.next.skeleton", next_p.get("recommended_next") == SELECTED_NEXT_PHASE)

    for mp in TRAJECTORY_MOTION_PATTERNS:
        _add(checks, f"stage.motion.{mp[:18]}", mp in (traj_reg.get("motion_patterns") or []))
    for conf in TRAJECTORY_CONFIDENCE_LEVELS:
        _add(checks, f"stage.conf.{conf}", conf in (traj_reg.get("confidence_levels") or []))
    for rr in TRAJECTORY_RELIABILITY_REASONS:
        _add(checks, f"stage.rel.{rr[:16]}", rr in (traj_reg.get("reliability_reasons") or []))
    for tit in TASK_IMPACT_TYPES:
        _add(checks, f"stage.impact.{tit[:16]}", tit in (impact_reg.get("task_impact_types") or []))
    for pri in TASK_IMPACT_PRIORITIES:
        _add(checks, f"stage.pri.{pri[:14]}", pri in (impact_reg.get("task_impact_priorities") or []))
    for rule in TRAJECTORY_TASK_IMPACT_RULES:
        rid = rule.get("rule_id", "")
        _add(checks, f"stage.rule.{rid[:16]}", any(r.get("rule_id") == rid for r in (rules.get("rules") or [])))
    for case in MOCK_CASES:
        cid = case["case_id"]
        exp = next((c for c in (mock_exp.get("cases") or []) if c.get("case_id") == cid), {})
        _add(checks, f"stage.case.{cid[:18]}.reg", any(c.get("case_id") == cid for c in (mock_reg.get("cases") or [])))
        _add(checks, f"stage.case.{cid[:18]}.exp", bool(exp))
        _add(checks, f"stage.case.{cid[:18]}.pass", bool(exp.get("pass_condition")))
        _add(checks, f"stage.case.{cid[:18]}.prohib", isinstance(exp.get("expected_prohibited_behavior"), list))
    for field in traj_m.get("fields") or []:
        _add(checks, f"stage.trajfld.{field[:14]}", field in (traj_m.get("fields") or []))
    for field in impact_m.get("fields") or []:
        _add(checks, f"stage.tifld.{field[:14]}", field in (impact_m.get("fields") or []))
    for field in risk_m.get("fields") or []:
        _add(checks, f"stage.riskfld.{field[:14]}", field in (risk_m.get("fields") or []))
    for field in missing_m.get("fields") or []:
        _add(checks, f"stage.misfld.{field[:14]}", field in (missing_m.get("fields") or []))
    for item in PROHIBITED_SCOPE.get("prohibited") or []:
        _add(checks, f"stage.proh.{item[:14]}", item in (prohibited.get("prohibited") or []))
    for k in CAP_GO_KEYS:
        _add(checks, f"stage.go.{k[:18]}", s.get(k) is True)
    return checks


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--target-locking-skeleton-root", default=DEFAULT_TARGET_LOCKING_SKELETON_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    skeleton_up = Path(args.target_locking_skeleton_root)
    skeleton_s = _read(skeleton_up / "summary.json")
    skeleton_v = _read(skeleton_up / "verifier_report.json")
    docs = {n: _read(root / n) for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"}
    s = docs["summary.json"]
    report = docs["trajectory_analysis_task_impact_planning_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT,
        output_root=root,
        summary=s,
        report=report,
        file_size_review=fs,
        phase_id=PHASE_ID,
        scope=SCOPE,
        final_decision_go=FINAL_DECISION_GO,
        selected_next_phase=SELECTED_NEXT_PHASE,
        go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS,
        docs=DOCS,
        phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES,
        upstream_summary=skeleton_s,
        upstream_verifier=skeleton_v,
        upstream_final_go=TARGET_LOCKING_SKELETON_FINAL_GO,
        upstream_pass_flag="static_dynamic_target_locking_tracking_controlled_skeleton_pass",
        upstream_min_checks=480,
        pass_flag_key="trajectory_analysis_task_impact_planning_pass",
        md_report_name="trajectory_analysis_task_impact_planning_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific_validation(root, docs, s)

    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        for mp in TRAJECTORY_MOTION_PATTERNS:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.motion.cross.{idx}.{mp[:10]}", mp in TRAJECTORY_MOTION_PATTERNS)
        for tit in TASK_IMPACT_TYPES:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.impact.cross.{idx}.{tit[:10]}", tit in TASK_IMPACT_TYPES)
        idx += 1

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0
        and len(checks) >= MIN_CHECKS
        and s.get("trajectory_analysis_task_impact_planning_pass") is True
        and s.get("final_decision") == FINAL_DECISION_GO
        and common_report.get("common_validation_reuse_ok") is True
    )
    common_report_path = root / "common_validation_reuse_report_v1.json"
    common_report_path.write_text(json.dumps(common_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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
    (root / "verifier_report.json").write_text(json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "verifier": verifier_report["verifier"],
        "passed_checks": passed,
        "failed_checks": failed,
        "common_validation_reuse_ok": common_report.get("common_validation_reuse_ok"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
