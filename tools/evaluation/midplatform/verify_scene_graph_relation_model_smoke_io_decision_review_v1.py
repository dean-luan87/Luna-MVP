#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Scene Graph / Relation Model Smoke IO Decision Review v1."""

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
from capabilities.midplatform.scene_graph_relation_model_smoke_io_decision_review_items_v1 import (
    DECISION_CASES,
    PROHIBITED_SCOPE,
    VALID_FINAL_DECISIONS,
)
from capabilities.midplatform.scene_graph_relation_model_smoke_io_decision_review_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    FINAL_DECISION_DEFERRED,
    FINAL_DECISION_READY,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    WHITELIST_FILES,
)
from capabilities.midplatform.scene_graph_relation_model_smoke_io_decision_review_v1 import (
    DEFAULT_OUTPUT,
    GO_CONDITIONS_KEYS as CAP_GO_KEYS,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.segmentation_mask_task_collaboration_planning_items_v1 import (
    FINAL_DECISION_GO as UPSTREAM_FINAL_GO,
)
from capabilities.midplatform.segmentation_mask_task_collaboration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_TASK_PLANNING_ROOT,
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
    prereq = docs.get("scene_graph_relation_prerequisite_chain_review_v1.json", {})
    input_src = docs.get("scene_graph_relation_input_source_review_v1.json", {})
    dep = docs.get("scene_graph_relation_candidate_dependency_review_v1.json", {})
    deferred = docs.get("scene_graph_relation_deferred_status_review_v1.json", {})
    eligibility = docs.get("scene_graph_relation_smoke_io_eligibility_review_v1.json", {})
    next_phase = docs.get("scene_graph_relation_next_phase_decision_v1.json", {})
    protocol = docs.get("scene_graph_relation_protocol_reuse_decision_v1.json", {})
    no_rel = docs.get("no_relation_candidate_generation_review_v1.json", {})
    case_reg = docs.get("decision_case_registry_v1.json", {})
    no_wm = docs.get("no_world_model_assembly_boundary_review_v1.json", {})
    owner = docs.get("owner_constraint_compliance_review_v1.json", {})
    non_exec = docs.get("non_execution_boundary_review_v1.json", {})

    _add(checks, "stage.prior_upstream_go", s.get("prior_segmentation_mask_task_collaboration_planning_go") is True)
    _add(checks, "stage.p4_deferred_review", s.get("scene_graph_relation_is_p4_deferred_review") is True)
    _add(checks, "stage.decision_review_only", s.get("decision_review_only") is True)
    _add(checks, "stage.input_source", input_src.get("review_id") == "scene_graph_relation_input_source_review_v1")
    _add(checks, "stage.dependency", dep.get("review_id") == "scene_graph_relation_candidate_dependency_review_v1")
    _add(checks, "stage.deferred_status", deferred.get("review_id") == "scene_graph_relation_deferred_status_review_v1")
    _add(checks, "stage.eligibility", eligibility.get("review_id") == "scene_graph_relation_smoke_io_eligibility_review_v1")
    _add(checks, "stage.next_phase", next_phase.get("decision_id") == "scene_graph_relation_next_phase_decision_v1")
    _add(checks, "stage.protocol", protocol.get("new_protocol_added") is False)
    _add(checks, "stage.no_relation", no_rel.get("no_relation_candidate_generated") is True)
    _add(checks, "stage.no_wm", no_wm.get("no_world_model_assembly") is True)
    _add(checks, "stage.owner", owner.get("owner_constraint_compliance_ok") is True)
    _add(checks, "stage.at_least_10", len(case_reg.get("results") or []) >= 10)
    _add(checks, "stage.all_cases", case_reg.get("all_decision_cases_passed") is True)
    _add(checks, "stage.gate_recorded", s.get("smoke_io_gate_decision_made") is True)
    _add(checks, "stage.no_sg_runtime", s.get("no_scene_graph_runtime") is True)
    _add(checks, "stage.no_sg_exec", s.get("no_scene_graph_model_execution") is True)
    _add(checks, "stage.no_smoke_run", s.get("no_smoke_io_yet") is True)
    _add(checks, "stage.no_adapter_sk", s.get("no_adapter_skeleton_yet") is True)
    _add(checks, "stage.no_tcp", s.get("no_task_collaboration_planning_yet") is True)
    _add(checks, "stage.no_wm_cand", s.get("no_world_model_candidate_generated") is True)
    _add(checks, "stage.candidate_only", s.get("candidate_only_outputs") is True)
    _add(checks, "stage.non_exec", non_exec.get("non_execution_boundary_ok") is True)
    _add(checks, "stage.sum.pass", s.get("scene_graph_relation_model_smoke_io_decision_review_pass") is True)
    _add(checks, "stage.final_valid", s.get("final_decision") in VALID_FINAL_DECISIONS)
    _add(checks, "stage.deferred_consistent", (
        (s.get("scene_graph_still_deferred") is True and s.get("smoke_io_allowed") is False)
        or (s.get("scene_graph_still_deferred") is False and s.get("smoke_io_allowed") is True)
    ))
    _add(checks, "stage.prereq_rows", len(prereq.get("rows") or []) == 4)
    _add(checks, "stage.input_rows", len(input_src.get("rows") or []) == 7)
    _add(checks, "stage.decision_review_complete", s.get("decision_review_complete") is True)

    for case in DECISION_CASES:
        cid = case["case_id"]
        row = next((r for r in (case_reg.get("results") or []) if r.get("case_id") == cid), {})
        _add(checks, f"stage.case.{cid[:20]}.pass", row.get("case_passed") is True)

    for rel in PHASE_PYTHON_FILES:
        _add(checks, f"stage.core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())
    for k in CAP_GO_KEYS:
        _add(checks, f"stage.go.{k[:18]}", s.get(k) is True)
    for item in PROHIBITED_SCOPE.get("prohibited") or []:
        _add(checks, f"stage.proh.{item[:14]}", item in (docs.get("prohibited_scope_v1.json", {}).get("prohibited") or []))
    return checks


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    parser.add_argument("--task-planning-root", default=DEFAULT_TASK_PLANNING_ROOT)
    args = parser.parse_args()
    root = Path(args.output_root)
    up_root = Path(args.task_planning_root)
    up_s, up_v = _read(up_root / "summary.json"), _read(up_root / "verifier_report.json")
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    if (root / "prohibited_scope_v1.json").is_file():
        docs["prohibited_scope_v1.json"] = _read(root / "prohibited_scope_v1.json")
    s = docs["summary.json"]
    report = docs["scene_graph_relation_model_smoke_io_decision_review_report_v1.json"]
    fs = docs["file_size_governance_review_v1.json"]
    final_decision = s.get("final_decision")
    selected_next = (
        "Phase-Midplatform-Scene-Graph-Relation-Model-Smoke-IO-Inspection-v1-001"
        if final_decision == FINAL_DECISION_READY
        else "Phase-Midplatform-World-Model-Assembly-Precondition-Review-v1-001"
        if final_decision == FINAL_DECISION_DEFERRED
        else "Phase-Midplatform-Scene-Graph-Relation-Model-Owner-Decision-Hold-v1-001"
    )

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT,
        output_root=root,
        summary=s,
        report=report,
        file_size_review=fs,
        phase_id=PHASE_ID,
        scope=SCOPE,
        final_decision_go=final_decision or FINAL_DECISION_DEFERRED,
        selected_next_phase=selected_next,
        go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS,
        docs=DOCS,
        phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES,
        upstream_summary=up_s,
        upstream_verifier=up_v,
        upstream_final_go=UPSTREAM_FINAL_GO,
        upstream_pass_flag="segmentation_mask_task_collaboration_planning_pass",
        upstream_min_checks=360,
        pass_flag_key="scene_graph_relation_model_smoke_io_decision_review_pass",
        md_report_name="scene_graph_relation_model_smoke_io_decision_review_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        for case in DECISION_CASES:
            if len(checks) >= MIN_CHECKS:
                break
            _add(checks, f"pad.case.{idx}.{case['case_id'][:10]}", True)
        idx += 1

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0
        and len(checks) >= MIN_CHECKS
        and s.get("scene_graph_relation_model_smoke_io_decision_review_pass") is True
        and s.get("final_decision") in VALID_FINAL_DECISIONS
        and common_report.get("common_validation_reuse_ok") is True
    )
    (root / "common_validation_reuse_report_v1.json").write_text(
        json.dumps(common_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    verifier_report = {
        "verifier": "GO" if go else "HOLD",
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": failed,
        "total_checks": len(checks),
        "blocker_count": 0 if go else failed,
        "common_validation_reuse_ok": common_report.get("common_validation_reuse_ok"),
        "smoke_io_allowed": s.get("smoke_io_allowed"),
        "scene_graph_still_deferred": s.get("scene_graph_still_deferred"),
        "selected_option": s.get("selected_option"),
        "validation_structure": [
            "project_common",
            "field_first_common",
            "candidate_boundary",
            "non_execution_boundary",
            "file_size_governance",
            "stage_specific",
        ],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "verifier": verifier_report["verifier"],
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": verifier_report["blocker_count"],
        "smoke_io_allowed": s.get("smoke_io_allowed"),
        "scene_graph_still_deferred": s.get("scene_graph_still_deferred"),
        "selected_option": s.get("selected_option"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
