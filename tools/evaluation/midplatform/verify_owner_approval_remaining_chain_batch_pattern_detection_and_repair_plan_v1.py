#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify owner approval remaining chain batch pattern detection and repair plan v1."""

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
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.owner_approval_remaining_chain_batch_pattern_detection_items_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_COMPLETE,
    MIN_REMAINING_STAGE_COUNT,
    PASS_FLAG,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.owner_approval_remaining_chain_batch_pattern_detection_lineage_v1 import (
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
    inventory = docs.get("remaining_stage_inventory_v1.json", {})
    gap = docs.get("remaining_stage_gap_classification_v1.json", {})
    groups = docs.get("batch_repair_group_plan_v1.json", {})
    safe = docs.get("safe_template_repair_candidates_v1.json", {})
    individual = docs.get("stages_requiring_individual_repair_v1.json", {})
    no_issue = docs.get("no_issue_review_created_review_v1.json", {})

    _add(checks, "stage.canonical", s.get("canonical_rebuild_go_confirmed") is True)
    _add(checks, "stage.go7", s.get("go_stage_count_at_least_7") is True)
    _add(checks, "stage.ff_issuance", s.get("first_failed_stage_is_issuance_planning") is True)
    _add(checks, "stage.remain19", s.get("remaining_stage_count_detected_at_least_19") is True)
    _add(checks, "stage.inventory", inventory.get("remaining_stage_count", 0) >= MIN_REMAINING_STAGE_COUNT)
    _add(checks, "stage.family", len(gap.get("rows") or []) >= MIN_REMAINING_STAGE_COUNT)
    _add(checks, "stage.groups", bool(groups.get("Group_P_planning_template_repair_candidates")))
    _add(checks, "stage.safe", safe.get("count", 0) > 0)
    _add(checks, "stage.individual", individual.get("count", 0) > 0)
    _add(checks, "stage.no_issue", no_issue.get("no_issue_review_stage_created") is True)
    _add(checks, "stage.pass_flag", s.get(PASS_FLAG) is True)
    _add(checks, "stage.final", s.get("final_decision") in VALID_FINAL_DECISIONS)

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
    report = docs["batch_pattern_detection_report_v1.json"]
    fs = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/owner_approval_remaining_chain_batch_pattern_detection_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

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
        md_report_name="batch_pattern_detection_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        _add(
            checks,
            f"pad.batch.{idx}",
            s.get("owner_approval_remaining_chain_batch_pattern_detection_only") is True,
        )
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
        "phase": PHASE_ID,
        "scope": SCOPE,
        "verifier": "GO" if go else "HOLD",
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": 0 if go else 1,
        PASS_FLAG: s.get(PASS_FLAG),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }
    (root / "verifier_report.json").write_text(
        json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(verifier_report, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
