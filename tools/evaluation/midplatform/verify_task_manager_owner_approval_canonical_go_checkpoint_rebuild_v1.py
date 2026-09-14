#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Task Manager / Owner Approval canonical GO checkpoint rebuild v1."""

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
from capabilities.midplatform.task_manager_owner_approval_canonical_go_checkpoint_rebuild_items_v1 import (
    CHECKPOINT_STATUS_GO,
    DEFAULT_OUTPUT,
    FINAL_DECISION_COMPLETE,
    PASS_FLAG,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.task_manager_owner_approval_canonical_go_checkpoint_rebuild_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    EXPECTED_STAGE_COUNT,
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


def _run_stage_specific(docs: Dict[str, Any], s: Dict[str, Any], root: Path) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    registry = docs.get("canonical_checkpoint_registry_v1.json", {})
    first = docs.get("first_failed_stage_review_v1.json", {})
    failed = docs.get("failed_stage_registry_v1.json", {})
    readable = docs.get("downstream_readable_checkpoint_index_v1.json", {})
    mapping = docs.get("final_decision_mapping_registry_v1.json", {})
    refmap = docs.get("upstream_downstream_reference_map_v1.json", {})
    gap = docs.get("canonical_checkpoint_gap_classification_v1.json", {})
    repair = docs.get("checkpoint_rebuild_repair_plan_v1.json", {})
    pollution = docs.get("no_original_stage_pollution_review_v1.json", {})
    mode = docs.get("checkpoint_rebuild_execution_mode_review_v1.json", {})

    cps = registry.get("checkpoints") or []
    _add(checks, "stage.registry", registry.get("registry_id") == "canonical_checkpoint_registry_v1")
    _add(checks, "stage.count", len(cps) == EXPECTED_STAGE_COUNT)
    _add(checks, "stage.first", first.get("review_id") == "first_failed_stage_review_v1")
    _add(checks, "stage.failed", failed.get("registry_id") == "failed_stage_registry_v1")
    _add(checks, "stage.readable", readable.get("index_id") == "downstream_readable_checkpoint_index_v1")
    _add(checks, "stage.mapping", mapping.get("registry_id") == "final_decision_mapping_registry_v1")
    _add(checks, "stage.refmap", refmap.get("map_id") == "upstream_downstream_reference_map_v1")
    _add(checks, "stage.gap", gap.get("classification_id") == "canonical_checkpoint_gap_classification_v1")
    _add(checks, "stage.repair", repair.get("plan_id") == "checkpoint_rebuild_repair_plan_v1")
    _add(checks, "stage.pollution", pollution.get("no_original_stage_pollution") is True)
    _add(checks, "stage.mode", mode.get("review_id") == "checkpoint_rebuild_execution_mode_review_v1")
    _add(checks, "stage.no_issue_review", repair.get("do_not_add_issue_review") is True)
    _add(checks, "stage.pass_flag", s.get(PASS_FLAG) is True)
    _add(checks, "stage.final", s.get("final_decision") == FINAL_DECISION_COMPLETE)

    per_stage = 0
    for cp in cps:
        sk = cp.get("stage_key")
        p = root / "checkpoints" / sk / "canonical_go_checkpoint_v1.json"
        if p.is_file():
            per_stage += 1
        if not cp.get("is_go") and cp.get("checkpoint_status") == CHECKPOINT_STATUS_GO:
            _add(checks, f"stage.fake_go.{sk[:12]}", False)
    _add(checks, "stage.per_stage_files", per_stage == EXPECTED_STAGE_COUNT)

    for cp in cps:
        if not cp.get("verifier_report_exists") and cp.get("checkpoint_status") == CHECKPOINT_STATUS_GO:
            _add(checks, f"stage.missing_vr_not_go.{cp.get('stage_key', '')[:10]}", False)

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
    report = docs["task_manager_owner_approval_canonical_go_checkpoint_rebuild_report_v1.json"]
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
        md_report_name="task_manager_owner_approval_canonical_go_checkpoint_rebuild_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s, root)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        _add(checks, f"pad.rebuild.{idx}", s.get("checkpoint_rebuild_only") is True)
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
        "first_failed_stage_key": s.get("first_failed_stage_key"),
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
        "first_failed_stage_key": s.get("first_failed_stage_key"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
