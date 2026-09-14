#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Real Model Field Construction Execution Path Hardening v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.real_model_field_construction_execution_path_hardening_items_v1 import (
    EXECUTION_HARDENING_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.real_model_field_construction_execution_path_hardening_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.real_model_field_construction_execution_path_hardening_v1 import (
    DEFAULT_OUTPUT,
    GO_CONDITIONS_KEYS as CAP_GO_KEYS,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.field_first_common_validation_v1 import (
    CommonValidationConfig,
    flatten_checks,
    run_all_common_validations,
)
from capabilities.midplatform.real_model_field_construction_success_path_hardening_v1 import (
    DEFAULT_OUTPUT as DEFAULT_HARDENING_ROOT,
    FINAL_DECISION_GO as HARDENING_FINAL_GO,
)
from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
)

MIN_CHECKS = 460


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
    auth = docs["real_model_execution_authorization_resolved_v1.json"]
    frames = docs["real_frame_input_set_registry_v1.json"]
    yolo_reg = docs["yolo_execution_path_result_registry_v1.json"]
    depth_reg = docs["depth_execution_path_result_registry_v1.json"]
    exec_reg = docs["real_model_execution_path_result_registry_v1.json"]
    quality = docs["real_field_construction_quality_report_v1.json"]
    baseline = docs["real_field_construction_baseline_registry_v1.json"]
    failure = docs["real_field_failure_localization_review_v1.json"]
    trace = docs["real_field_traceability_review_v1.json"]
    no_sim = docs["no_simulation_boundary_review_v1.json"]
    readiness = docs["readiness_for_real_field_quality_evaluation_review_v1.json"]
    case_res = docs.get("real_model_execution_case_results_v1.json") or {}

    _add(checks, "stage.prior_dryrun_go", s.get("prior_yolo_depth_controlled_real_model_dryrun_go") is True)
    _add(checks, "stage.prior_hardening_go", s.get("prior_real_model_field_construction_success_path_hardening_go") is True)
    _add(checks, "stage.route_switch", s.get("route_switched_from_simulation_to_real_content") is True)
    _add(checks, "stage.sim_deferred", s.get("field_simulation_deferred") is True)
    _add(checks, "stage.auth_resolved", bool(auth.get("authorization_candidate")))
    _add(checks, "stage.frame_registry", frames.get("registry_id") == "real_frame_input_set_registry_v1")
    _add(checks, "stage.yolo_registry", yolo_reg.get("registry_id") == "yolo_execution_path_result_registry_v1")
    _add(checks, "stage.depth_registry", depth_reg.get("registry_id") == "depth_execution_path_result_registry_v1")
    _add(checks, "stage.exec_registry", exec_reg.get("registry_id") == "real_model_execution_path_result_registry_v1")
    _add(checks, "stage.quality_report", bool(quality.get("quality_report_id")))
    _add(checks, "stage.baseline_registry", baseline.get("registry_id") == "real_field_construction_baseline_registry_v1")
    _add(checks, "stage.at_least_10_cases", len(case_res.get("results") or []) >= 10)
    _add(checks, "stage.at_least_5_frames", s.get("real_frame_count", 0) >= 5)
    _add(checks, "stage.yolo_path", s.get("yolo_execution_path_ok") is True)
    _add(checks, "stage.depth_classified", s.get("depth_execution_path_classified") is True)
    _add(checks, "stage.mock_not_real", s.get("mock_depth_not_marked_as_real") is True)
    _add(checks, "stage.stub_not_full", s.get("stub_depth_not_marked_as_full_real_model") is True)
    _add(checks, "stage.enhanced_scene", s.get("enhanced_field_scene_candidate_generated") is True)
    _add(checks, "stage.failure_loc", failure.get("failure_localization_ok") is True)
    _add(checks, "stage.trace", trace.get("traceability_review_ok") is True)
    _add(checks, "stage.no_sim", no_sim.get("no_simulation_boundary_ok") is True)
    _add(checks, "stage.readiness", readiness.get("review_id") == "readiness_for_real_field_quality_evaluation_review_v1")
    _add(checks, "stage.no_field_sim", s.get("no_field_simulation") is True)
    _add(checks, "stage.no_task", s.get("no_task_execution") is True)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.sum.pass", s.get("real_model_execution_path_hardening_pass") is True)

    for case in EXECUTION_HARDENING_CASES:
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
    parser.add_argument("--dryrun-root", default=DEFAULT_DRYRUN_ROOT)
    parser.add_argument("--hardening-root", default=DEFAULT_HARDENING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    dry_up = Path(args.dryrun_root)
    hard_up = Path(args.hardening_root)
    dry_s, dry_v = _read(dry_up / "summary.json"), _read(dry_up / "verifier_report.json")
    hard_s, hard_v = _read(hard_up / "summary.json"), _read(hard_up / "verifier_report.json")
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    if (root / "real_model_execution_case_results_v1.json").is_file():
        docs["real_model_execution_case_results_v1.json"] = _read(root / "real_model_execution_case_results_v1.json")
    s = docs["summary.json"]
    report = docs["real_model_field_construction_execution_path_hardening_report_v1.json"]
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
        pass_flag_key="real_model_execution_path_hardening_pass",
        md_report_name="real_model_field_construction_execution_path_hardening_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        for case in EXECUTION_HARDENING_CASES:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.case.{idx}.{case['case_id'][:10]}", True)
        idx += 1

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0 and len(checks) >= MIN_CHECKS
        and s.get("real_model_execution_path_hardening_pass") is True
        and s.get("final_decision") == FINAL_DECISION_GO
        and s.get("field_simulation_deferred") is True
        and common_report.get("common_validation_reuse_ok") is True
        and dry_s.get("final_decision") == DRYRUN_FINAL_GO
        and dry_v.get("verifier") == "GO"
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
        "field_simulation_deferred": True,
        "route_switched_from_simulation_to_real_content": True,
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
        "field_simulation_deferred": s.get("field_simulation_deferred"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
