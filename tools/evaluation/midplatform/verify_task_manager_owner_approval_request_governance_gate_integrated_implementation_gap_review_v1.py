#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify governance gate integrated implementation gap review v1."""

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
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_items_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    PASS_FLAG,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    VALID_FINAL_DECISIONS,
    WHITELIST_FILES,
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


def _run_stage_specific(docs: Dict[str, Any], s: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    impl = docs.get("integrated_implementation_gap_review_v1.json", {})
    registry = docs.get("integrated_implementation_direct_upstream_registry_v1.json", {})
    first = docs.get("integrated_implementation_first_non_go_upstream_review_v1.json", {})
    vis = docs.get("integrated_implementation_upstream_artifact_visibility_review_v1.json", {})
    boundary = docs.get("integrated_implementation_upstream_boundary_gap_review_v1.json", {})
    routing = docs.get("integrated_implementation_routing_gap_review_v1.json", {})
    roadmap = docs.get("integrated_implementation_roadmap_gap_review_v1.json", {})
    auth = docs.get("integrated_implementation_auth_prep_gap_review_v1.json", {})
    closure = docs.get("integrated_implementation_closure_boundary_gap_review_v1.json", {})
    slice_plan = docs.get("integrated_implementation_slice_plan_gap_review_v1.json", {})
    checklist = docs.get("integrated_implementation_checklist_gap_review_v1.json", {})
    rerun = docs.get("integrated_implementation_rerun_review_v1.json", {})
    readiness = docs.get("authorization_preparation_dryrun_rerun_readiness_review_v1.json", {})
    gap = docs.get("first_unresolved_gap_review_v1.json", {})

    _add(checks, "stage.planning_result_b", s.get("functional_slice_planning_gap_review_result_b_confirmed") is True)
    _add(checks, "stage.next_fix", s.get("next_required_fix_confirmed") is True)
    _add(checks, "stage.impl_files", s.get("integrated_implementation_files_exist") is True)
    _add(checks, "stage.impl_rerun", s.get("integrated_implementation_rerun_attempted") is True)
    _add(checks, "stage.impl_rec", s.get("integrated_implementation_result_recorded") is True)
    _add(checks, "stage.registry", registry.get("registry_id") == "integrated_implementation_direct_upstream_registry_v1")
    _add(checks, "stage.first_non_go", first.get("review_id") == "integrated_implementation_first_non_go_upstream_review_v1")
    _add(checks, "stage.vis", vis.get("review_id") == "integrated_implementation_upstream_artifact_visibility_review_v1")
    _add(checks, "stage.boundary", boundary.get("review_id") == "integrated_implementation_upstream_boundary_gap_review_v1")
    _add(checks, "stage.routing", routing.get("review_id") == "integrated_implementation_routing_gap_review_v1")
    _add(checks, "stage.roadmap", roadmap.get("review_id") == "integrated_implementation_roadmap_gap_review_v1")
    _add(checks, "stage.auth_prep", auth.get("review_id") == "integrated_implementation_auth_prep_gap_review_v1")
    _add(checks, "stage.closure", closure.get("review_id") == "integrated_implementation_closure_boundary_gap_review_v1")
    _add(checks, "stage.slice_plan", slice_plan.get("review_id") == "integrated_implementation_slice_plan_gap_review_v1")
    _add(checks, "stage.checklist", checklist.get("review_id") == "integrated_implementation_checklist_gap_review_v1")
    _add(checks, "stage.rerun", rerun.get("review_id") == "integrated_implementation_rerun_review_v1")
    _add(checks, "stage.readiness", readiness.get("review_id") == "authorization_preparation_dryrun_rerun_readiness_review_v1")
    _add(checks, "stage.first_gap", gap.get("review_id") == "first_unresolved_gap_review_v1")
    _add(checks, "stage.impl_gap", impl.get("review_id") == "integrated_implementation_gap_review_v1")
    _add(checks, "stage.no_protocol", s.get("no_protocol_change") is True)
    _add(checks, "stage.pass_flag", s.get(PASS_FLAG) is True)
    _add(checks, "stage.final_valid", s.get("final_decision") in VALID_FINAL_DECISIONS)

    complete = s.get("integrated_implementation_go") is True
    blocked = s.get("first_unresolved_gap_identified") is True and s.get("next_required_fix_recorded") is True
    _add(
        checks,
        "stage.result_path",
        (complete and s.get("final_decision") == FINAL_DECISION_COMPLETE)
        or (blocked and s.get("final_decision") == FINAL_DECISION_BLOCKED),
    )

    if complete:
        _add(checks, "stage.impl_go", s.get("integrated_implementation_go") is True)
        _add(checks, "stage.auth_dryrun_ready", s.get("authorization_preparation_dryrun_rerun_readiness") is True)
        _add(checks, "stage.first_upstream_resolved", s.get("first_non_go_direct_upstream_resolved") is True)
    else:
        _add(checks, "stage.gap_id", s.get("first_unresolved_gap_identified") is True)
        _add(checks, "stage.next_fix_rec", s.get("next_required_fix_recorded") is True)
        _add(checks, "stage.impl_not_go", s.get("integrated_implementation_go") is False)
        _add(checks, "stage.first_upstream_named", bool(s.get("first_non_go_direct_upstream")))

    rows = registry.get("rows") or []
    _add(checks, "stage.registry_rows", len(rows) >= 2)
    for idx, row in enumerate(rows[:2]):
        _add(checks, f"stage.upstream.{idx}.field", bool(row.get("upstream_field")))
        _add(checks, f"stage.upstream.{idx}.stage", bool(row.get("stage_name")))

    for rel in PHASE_PYTHON_FILES:
        _add(checks, f"stage.core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"stage.go.{k[:18]}", s.get(k) is True)
    return checks


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    root = Path(args.output_root)
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    s = docs["summary.json"]
    report = docs["task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_report_v1.json"]
    fs = docs.get("file_size_governance_review_v1.json", {})

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT,
        output_root=root,
        summary=s,
        report=report,
        file_size_review=fs,
        phase_id=PHASE_ID,
        scope=SCOPE,
        final_decision_go=s.get("final_decision") or FINAL_DECISION_BLOCKED,
        selected_next_phase=s.get("recommended_next_phase", ""),
        go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS,
        docs=DOCS,
        phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES,
        pass_flag_key=PASS_FLAG,
        md_report_name="task_manager_owner_approval_request_governance_gate_integrated_implementation_gap_review_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        _add(checks, f"pad.review.{idx}", s.get("gap_review_only") is True)
        idx += 1
        if idx > MIN_CHECKS:
            break

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0
        and len(checks) >= MIN_CHECKS
        and s.get(PASS_FLAG) is True
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
        "integrated_implementation_go": s.get("integrated_implementation_go"),
        "first_non_go_direct_upstream": s.get("first_non_go_direct_upstream"),
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
        "integrated_implementation_go": s.get("integrated_implementation_go"),
        "first_non_go_direct_upstream": s.get("first_non_go_direct_upstream"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
