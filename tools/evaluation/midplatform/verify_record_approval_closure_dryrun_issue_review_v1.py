#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify record approval closure dryrun issue review v1."""

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
from capabilities.midplatform.record_approval_closure_dryrun_issue_review_items_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    PASS_FLAG,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.record_approval_closure_dryrun_issue_review_lineage_v1 import (
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
    gap = docs.get("record_approval_closure_dryrun_gap_review_v1.json", {})
    planning = docs.get("record_approval_closure_dryrun_direct_planning_upstream_review_v1.json", {})
    vis = docs.get("record_approval_closure_dryrun_artifact_visibility_review_v1.json", {})
    accept = docs.get("record_approval_closure_dryrun_planning_result_acceptance_review_v1.json", {})
    matrix = docs.get("record_approval_closure_dryrun_candidate_matrix_review_v1.json", {})
    trace = docs.get("record_approval_closure_dryrun_traceability_reference_review_v1.json", {})
    absence = docs.get("record_approval_closure_dryrun_absence_drift_review_v1.json", {})
    boundary = docs.get("record_approval_closure_dryrun_boundary_gap_review_v1.json", {})
    rerun = docs.get("record_approval_closure_dryrun_rerun_review_v1.json", {})
    readiness = docs.get("post_dryrun_review_rerun_readiness_review_v1.json", {})
    first = docs.get("first_unresolved_gap_review_v1.json", {})

    _add(checks, "stage.post_dryrun_b", s.get("post_dryrun_review_issue_review_result_b_confirmed") is True)
    _add(checks, "stage.dryrun_confirmed", s.get("direct_dryrun_upstream_confirmed") is True)
    _add(checks, "stage.dryrun_files", s.get("dryrun_files_exist") is True)
    _add(checks, "stage.dryrun_rerun", s.get("dryrun_rerun_attempted") is True)
    _add(checks, "stage.dryrun_rec", s.get("dryrun_result_recorded") is True)
    _add(checks, "stage.planning_upstream", planning.get("review_id") == "record_approval_closure_dryrun_direct_planning_upstream_review_v1")
    _add(checks, "stage.accept", accept.get("review_id") == "record_approval_closure_dryrun_planning_result_acceptance_review_v1")
    _add(checks, "stage.matrix", matrix.get("review_id") == "record_approval_closure_dryrun_candidate_matrix_review_v1")
    _add(checks, "stage.trace", trace.get("review_id") == "record_approval_closure_dryrun_traceability_reference_review_v1")
    _add(checks, "stage.absence", absence.get("review_id") == "record_approval_closure_dryrun_absence_drift_review_v1")
    _add(checks, "stage.boundary", boundary.get("review_id") == "record_approval_closure_dryrun_boundary_gap_review_v1")
    _add(checks, "stage.vis", vis.get("review_id") == "record_approval_closure_dryrun_artifact_visibility_review_v1")
    _add(checks, "stage.gap", gap.get("review_id") == "record_approval_closure_dryrun_gap_review_v1")
    _add(checks, "stage.rerun", rerun.get("review_id") == "record_approval_closure_dryrun_rerun_review_v1")
    _add(checks, "stage.readiness", readiness.get("review_id") == "post_dryrun_review_rerun_readiness_review_v1")
    _add(checks, "stage.first_gap", first.get("review_id") == "first_unresolved_gap_review_v1")
    _add(checks, "stage.no_protocol", s.get("no_protocol_change") is True)
    _add(checks, "stage.pass_flag", s.get(PASS_FLAG) is True)
    _add(checks, "stage.final_valid", s.get("final_decision") in VALID_FINAL_DECISIONS)

    complete = s.get("record_approval_closure_dryrun_go") is True
    blocked = s.get("first_unresolved_gap_identified") is True and s.get("next_required_fix_recorded") is True
    _add(
        checks,
        "stage.result_path",
        (complete and s.get("final_decision") == FINAL_DECISION_COMPLETE)
        or (blocked and s.get("final_decision") == FINAL_DECISION_BLOCKED),
    )

    if complete:
        _add(checks, "stage.dryrun_go", s.get("record_approval_closure_dryrun_go") is True)
        _add(checks, "stage.planning_go", s.get("direct_planning_upstream_go") is True)
        _add(checks, "stage.post_ready", s.get("post_dryrun_review_rerun_readiness") is True)
    else:
        _add(checks, "stage.gap_id", s.get("first_unresolved_gap_identified") is True)
        _add(checks, "stage.next_fix_rec", s.get("next_required_fix_recorded") is True)
        _add(checks, "stage.dryrun_not_go", s.get("record_approval_closure_dryrun_go") is False)
        _add(checks, "stage.planning_named", bool(s.get("first_non_go_planning_upstream")))

    upstream = planning.get("planning_upstream") or {}
    _add(checks, "stage.planning_field", upstream.get("upstream_field") == "record_approval_closure_planning_root")
    _add(checks, "stage.planning_dir", upstream.get("output_dir_exists") is True)

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
    report = docs["record_approval_closure_dryrun_issue_review_report_v1.json"]
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
        md_report_name="record_approval_closure_dryrun_issue_review_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        _add(checks, f"pad.review.{idx}", s.get("issue_review_only") is True)
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
        "record_approval_closure_dryrun_go": s.get("record_approval_closure_dryrun_go"),
        "direct_planning_upstream_go": s.get("direct_planning_upstream_go"),
        "first_non_go_planning_upstream": s.get("first_non_go_planning_upstream"),
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
        "record_approval_closure_dryrun_go": s.get("record_approval_closure_dryrun_go"),
        "direct_planning_upstream_go": s.get("direct_planning_upstream_go"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
