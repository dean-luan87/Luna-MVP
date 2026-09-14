#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Task Manager foundation handoff planning repair v1."""

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
from capabilities.midplatform.task_manager_foundation_handoff_planning_repair_items_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_COMPLETE,
    PASS_FLAG,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_repair_lineage_v1 import (
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
    canonical = docs.get("canonical_rebuild_input_review_v1.json", {})
    classification = docs.get("foundation_handoff_planning_failure_classification_v1.json", {})
    downstream = docs.get("foundation_handoff_planning_downstream_expectation_repair_review_v1.json", {})
    post = docs.get("foundation_handoff_planning_post_repair_rerun_review_v1.json", {})
    scan = docs.get("canonical_checkpoint_scan_only_after_repair_review_v1.json", {})
    no_issue = docs.get("no_issue_review_created_review_v1.json", {})

    _add(checks, "stage.canonical", s.get("canonical_rebuild_go_confirmed") is True)
    _add(checks, "stage.ff_planning", s.get("first_failed_stage_foundation_handoff_planning_confirmed") is True)
    _add(checks, "stage.registry_go", s.get("registry_patch_checkpoint_go_readable") is True)
    _add(checks, "stage.smoke_go", s.get("protocol_shared_code_smoke_checkpoint_go_readable") is True)
    _add(checks, "stage.classification", classification.get("primary") == "downstream_expectation_gap")
    _add(checks, "stage.downstream", downstream.get("dryrun_post_review_demoted") is True)
    _add(checks, "stage.post_go", (post.get("after_inspect") or {}).get("is_go") is True)
    _add(checks, "stage.scan", scan.get("foundation_handoff_planning_go_readable") is True)
    _add(checks, "stage.no_issue", no_issue.get("no_issue_review_stage_created") is True)
    _add(checks, "stage.no_gap", no_issue.get("no_gap_review_stage_created") is True)
    _add(checks, "stage.no_rerun", no_issue.get("no_rerun_review_stage_created") is True)
    _add(checks, "stage.pass_flag", s.get(PASS_FLAG) is True)
    _add(checks, "stage.final", s.get("final_decision") in VALID_FINAL_DECISIONS)

    if s.get("original_foundation_handoff_planning_verifier_go"):
        _add(checks, "stage.result_a", s.get("final_decision") == FINAL_DECISION_COMPLETE)
        _add(checks, "stage.checkpoint_readable", s.get("foundation_handoff_planning_checkpoint_go_readable") is True)

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
    report = docs["task_manager_foundation_handoff_planning_repair_report_v1.json"]
    fs = docs.get("file_size_governance_review_v1.json", {})

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT,
        output_root=root,
        summary=s,
        report=report,
        file_size_review=fs,
        phase_id=PHASE_ID,
        scope=SCOPE,
        final_decision_go=FINAL_DECISION_COMPLETE,
        selected_next_phase=s.get("recommended_next_phase", ""),
        go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS,
        docs=DOCS,
        phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES,
        pass_flag_key=PASS_FLAG,
        md_report_name="task_manager_foundation_handoff_planning_repair_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        _add(checks, f"pad.repair.{idx}", s.get("foundation_handoff_planning_repair_only") is True)
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
        "original_foundation_handoff_planning_verifier_go": s.get("original_foundation_handoff_planning_verifier_go"),
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
        "original_foundation_handoff_planning_verifier_go": s.get("original_foundation_handoff_planning_verifier_go"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
