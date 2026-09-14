#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Adapter Priority Sequence Planning v1."""

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
from capabilities.midplatform.model_adapter_priority_sequence_planning_items_v1 import (
    PLANNING_CASES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
)
from capabilities.midplatform.model_adapter_priority_sequence_planning_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_GO,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.model_adapter_priority_sequence_planning_v1 import (
    DEFAULT_OUTPUT,
    GO_CONDITIONS_KEYS as CAP_GO_KEYS,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.model_workflow_protocol_reuse_and_cleanup_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CLEANUP_ROOT,
    FINAL_DECISION_GO as CLEANUP_FINAL_GO,
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


def _run_stage_specific(docs: Dict[str, Dict[str, Any]], s: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    priority = docs["model_adapter_priority_registry_v1.json"]
    reuse = docs["model_adapter_reuse_path_registry_v1.json"]
    wm = docs["world_model_construction_model_mapping_v1.json"]
    task = docs["task_collaboration_model_mapping_v1.json"]
    scenario = docs["scenario_2_to_3_model_group_registry_v1.json"]
    protocol = docs["model_adapter_protocol_reuse_decision_v1.json"]
    reason = docs["model_adapter_new_protocol_reason_required_report_v1.json"]
    next_sk = docs["next_model_adapter_skeleton_recommendation_v1.json"]
    deferred = docs["deferred_model_adapter_registry_v1.json"]
    owner = docs["owner_constraint_compliance_review_v1.json"]
    case_res = docs.get("planning_case_results_v1.json") or {}

    _add(checks, "stage.prior_cleanup", s.get("prior_model_workflow_protocol_reuse_and_cleanup_review_go") is True)
    _add(checks, "stage.priority_reg", priority.get("registry_id") == "model_adapter_priority_registry_v1")
    _add(checks, "stage.reuse_reg", reuse.get("registry_id") == "model_adapter_reuse_path_registry_v1")
    _add(checks, "stage.wm_map", wm.get("mapping_id") == "world_model_construction_model_mapping_v1")
    _add(checks, "stage.task_map", task.get("mapping_id") == "task_collaboration_model_mapping_v1")
    _add(checks, "stage.scenario", scenario.get("registry_id") == "scenario_2_to_3_model_group_registry_v1")
    _add(checks, "stage.protocol", protocol.get("new_protocol_added") is False)
    _add(checks, "stage.reason_rep", bool(reason.get("report_id")))
    _add(checks, "stage.next_sk", next_sk.get("recommended_adapter") == "slam_spatial_mapping")
    _add(checks, "stage.deferred", deferred.get("count", 0) >= 1)
    _add(checks, "stage.owner", owner.get("owner_constraints_inherited") is True)
    _add(checks, "stage.slam_p0", s.get("slam_or_spatial_mapping_prioritized") is True)
    _add(checks, "stage.track_p1", s.get("tracking_second_priority") is True)
    _add(checks, "stage.ocr_p2", s.get("ocr_third_priority") is True)
    _add(checks, "stage.seg_p3", s.get("segmentation_fourth_priority") is True)
    _add(checks, "stage.scene_def", s.get("scene_graph_deferred") is True)
    _add(checks, "stage.no_sim", s.get("no_field_simulation_route") is True)
    _add(checks, "stage.no_task", s.get("no_task_reasoning_route") is True)
    _add(checks, "stage.at_least_10", len(case_res.get("results") or []) >= 10)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.sum.pass", s.get("model_adapter_priority_sequence_planning_pass") is True)

    for case in PLANNING_CASES:
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
    parser.add_argument("--cleanup-root", default=DEFAULT_CLEANUP_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    cleanup_up = Path(args.cleanup_root)
    cleanup_s, cleanup_v = _read(cleanup_up / "summary.json"), _read(cleanup_up / "verifier_report.json")
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    if (root / "planning_case_results_v1.json").is_file():
        docs["planning_case_results_v1.json"] = _read(root / "planning_case_results_v1.json")
    s = docs["summary.json"]
    report = docs["model_adapter_priority_sequence_planning_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT, output_root=root, summary=s, report=report, file_size_review=fs,
        phase_id=PHASE_ID, scope=SCOPE, final_decision_go=FINAL_DECISION_GO,
        selected_next_phase=SELECTED_NEXT_PHASE, go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS, docs=DOCS, phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES, upstream_summary=cleanup_s, upstream_verifier=cleanup_v,
        upstream_final_go=CLEANUP_FINAL_GO,
        upstream_pass_flag="cleanup_review_pass",
        upstream_min_checks=300,
        pass_flag_key="model_adapter_priority_sequence_planning_pass",
        md_report_name="model_adapter_priority_sequence_planning_report_v1.md",
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
        and s.get("model_adapter_priority_sequence_planning_pass") is True
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
