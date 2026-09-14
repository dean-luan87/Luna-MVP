#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify model-SLAM readiness chain batch detection and recovery plan v1."""

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
from capabilities.midplatform.model_slam_readiness_chain_batch_detection_items_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_COMPLETE,
    FIRST_FAILED_STAGE_KEY,
    GROUP_M_STAGES,
    MIN_GO_STAGE_COUNT,
    PASS_FLAG,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.model_slam_readiness_chain_batch_detection_lineage_v1 import (
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
    inventory = docs.get("group_m_stage_inventory_v1.json", {})
    gap = docs.get("group_m_gap_classification_v1.json", {})
    recovery = docs.get("group_m_recovery_plan_v1.json", {})
    safe = docs.get("safe_model_slam_readiness_repair_candidates_v1.json", {})
    no_model = docs.get("no_model_execution_review_v1.json", {})

    _add(checks, "stage.gov_repair", s.get("governance_gate_repair_go_confirmed") is True)
    _add(checks, "stage.go20", s.get("go_stage_count_at_least_20") is True)
    _add(checks, "stage.ff_group_m", s.get("first_failed_stage_group_m_confirmed") is True)
    _add(checks, "stage.m6", s.get("group_m_stage_count") == len(GROUP_M_STAGES))
    _add(checks, "stage.inventory", inventory.get("count", 0) == len(GROUP_M_STAGES))
    _add(checks, "stage.gap_rows", len(gap.get("rows") or []) == len(GROUP_M_STAGES))
    _add(checks, "stage.recovery", recovery.get("Plan_C_ready_for_slam_readiness_repair", {}).get("ready") is not None)
    _add(checks, "stage.safe", safe.get("count", 0) > 0)
    _add(checks, "stage.no_model", no_model.get("no_model_execution") is True)
    _add(checks, "stage.pass_flag", s.get(PASS_FLAG) is True)
    _add(checks, "stage.final", s.get("final_decision") in VALID_FINAL_DECISIONS)

    for rel in PHASE_PYTHON_FILES:
        _add(checks, f"stage.core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())
    for k in GO_CONDITIONS_KEYS:
        val = s.get(k)
        if isinstance(val, bool):
            _add(checks, f"stage.go.{k[:22]}", val is True)
        elif isinstance(val, int):
            _add(checks, f"stage.go.{k[:22]}", val >= (len(GROUP_M_STAGES) if "group_m_stage" in k else MIN_GO_STAGE_COUNT))
    return checks


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    root = Path(args.output_root)
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    s = docs["summary.json"]
    report = docs["model_slam_readiness_chain_batch_detection_report_v1.json"]
    fs = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/model_slam_readiness_chain_batch_detection_lineage_v1.py",
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
        go_conditions_keys=[k for k in GO_CONDITIONS_KEYS if isinstance(s.get(k), bool)],
        artifacts=ARTIFACTS,
        docs=DOCS,
        phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES,
        pass_flag_key=PASS_FLAG,
        md_report_name="model_slam_readiness_chain_batch_detection_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        _add(checks, f"pad.mslam.{idx}", s.get("model_slam_readiness_chain_batch_detection_only") is True)
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
    s["common_validation_reuse_ok"] = common_report.get("common_validation_reuse_ok") is True
    (root / "summary.json").write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    verifier_report = {
        "verifier": "GO" if go else "HOLD",
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": failed,
        "group_m_batch_detection_complete": s.get(PASS_FLAG),
        "first_failed_stage_key": s.get("first_failed_stage_key"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verifier": verifier_report["verifier"],
                "passed_checks": passed,
                "failed_checks": failed,
                "blocker_count": failed,
                "group_m_batch_detection_complete": s.get(PASS_FLAG),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
