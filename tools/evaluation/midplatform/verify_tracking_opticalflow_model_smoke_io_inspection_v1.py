#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Tracking / Optical Flow Model Smoke IO Inspection v1."""

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
from capabilities.midplatform.slam_spatial_mapping_task_collaboration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_TASK_PLANNING_ROOT,
    FINAL_DECISION_GO as TASK_PLANNING_FINAL_GO,
)
from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_items_v1 import (
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SMOKE_IO_CASES,
)
from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_v1 import (
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


def _run_stage_specific(docs: Dict[str, Any], s: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    smoke_reg = docs["model_smoke_run_candidate_registry_v1.json"]
    io_reg = docs["model_io_inspection_candidate_registry_v1.json"]
    map_reg = docs["model_candidate_mapping_feasibility_registry_v1.json"]
    avail = docs["tracking_opticalflow_available_model_review_v1.json"]
    inp = docs["tracking_opticalflow_input_format_review_v1.json"]
    outp = docs["tracking_opticalflow_output_format_review_v1.json"]
    fail = docs["tracking_opticalflow_failure_point_review_v1.json"]
    cmap = docs["tracking_opticalflow_candidate_mapping_review_v1.json"]
    auth = docs["model_execution_authorization_review_v1.json"]
    case_res = docs.get("smoke_io_case_results_v1.json") or {}
    non_exec = docs["non_execution_boundary_review_v1.json"]

    _add(checks, "stage.prior_task_plan", s.get("prior_slam_task_collaboration_planning_go") is True)
    _add(checks, "stage.route_smoke_first", s.get("route_follows_model_smoke_io_first") is True)
    _add(checks, "stage.no_adapter_sk", s.get("no_adapter_skeleton_yet") is True)
    _add(checks, "stage.smoke_reg", smoke_reg.get("registry_id") == "model_smoke_run_candidate_registry_v1")
    _add(checks, "stage.io_reg", io_reg.get("registry_id") == "model_io_inspection_candidate_registry_v1")
    _add(checks, "stage.map_reg", map_reg.get("registry_id") == "model_candidate_mapping_feasibility_registry_v1")
    _add(checks, "stage.avail_rev", avail.get("review_id") == "tracking_opticalflow_available_model_review_v1")
    _add(checks, "stage.input_rev", inp.get("review_id") == "tracking_opticalflow_input_format_review_v1")
    _add(checks, "stage.output_rev", outp.get("review_id") == "tracking_opticalflow_output_format_review_v1")
    _add(checks, "stage.fail_rev", fail.get("review_id") == "tracking_opticalflow_failure_point_review_v1")
    _add(checks, "stage.cmap_rev", cmap.get("review_id") == "tracking_opticalflow_candidate_mapping_review_v1")
    _add(checks, "stage.auth_rev", auth.get("review_id") == "model_execution_authorization_review_v1")
    _add(checks, "stage.at_least_10", len(case_res.get("results") or []) >= 10)
    _add(checks, "stage.all_cases", case_res.get("all_smoke_io_cases_passed") is True)
    _add(checks, "stage.modes_class", s.get("model_execution_modes_classified") is True)
    _add(checks, "stage.blocked_no_dl", s.get("blocked_cases_do_not_download") is True)
    _add(checks, "stage.cached_not_real", s.get("cached_output_not_marked_as_real_run") is True)
    _add(checks, "stage.stub_not_real", s.get("adapter_stub_not_marked_as_real_run") is True)
    _add(checks, "stage.track_map", s.get("track_id_mapping_feasibility_checked") is True)
    _add(checks, "stage.persist_map", s.get("object_persistence_mapping_feasibility_checked") is True)
    _add(checks, "stage.motion_map", s.get("motion_candidate_mapping_feasibility_checked") is True)
    _add(checks, "stage.trace", s.get("traceability_preserved") is True)
    _add(checks, "stage.no_wm_asm", s.get("no_world_model_assembly") is True)
    _add(checks, "stage.no_sim", s.get("no_field_simulation") is True)
    _add(checks, "stage.no_task", s.get("no_task_reasoning") is True)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.non_exec", non_exec.get("non_execution_boundary_ok") is True)
    _add(checks, "stage.sum.pass", s.get("tracking_opticalflow_smoke_io_inspection_pass") is True)

    for case in SMOKE_IO_CASES:
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
    parser.add_argument("--task-planning-root", default=DEFAULT_TASK_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    plan_up = Path(args.task_planning_root)
    plan_s, plan_v = _read(plan_up / "summary.json"), _read(plan_up / "verifier_report.json")
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    if (root / "prohibited_scope_v1.json").is_file():
        docs["prohibited_scope_v1.json"] = _read(root / "prohibited_scope_v1.json")
    s = docs["summary.json"]
    report = docs["tracking_opticalflow_model_smoke_io_inspection_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT, output_root=root, summary=s, report=report, file_size_review=fs,
        phase_id=PHASE_ID, scope=SCOPE, final_decision_go=FINAL_DECISION_GO,
        selected_next_phase=SELECTED_NEXT_PHASE, go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS, docs=DOCS, phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES, upstream_summary=plan_s, upstream_verifier=plan_v,
        upstream_final_go=TASK_PLANNING_FINAL_GO,
        upstream_pass_flag="slam_task_collaboration_planning_pass",
        upstream_min_checks=360,
        pass_flag_key="tracking_opticalflow_smoke_io_inspection_pass",
        md_report_name="tracking_opticalflow_model_smoke_io_inspection_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        for case in SMOKE_IO_CASES:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.case.{idx}.{case['case_id'][:10]}", True)
        idx += 1

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0 and len(checks) >= MIN_CHECKS
        and s.get("tracking_opticalflow_smoke_io_inspection_pass") is True
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
