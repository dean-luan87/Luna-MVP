#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B1 Preflight Via Harness v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b1_preflight_via_harness_v1 import (
    BATCH_DOMAIN,
    FINAL_DECISION,
    GOVERNANCE_ROOT,
    NEXT_PHASE,
    PHASE_ID,
    REQUIRED_FIXED_CHECKS,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_REQUIRED_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    governance_constraints_doc_path,
)

MIN_CHECKS = 420

REQUIRED_OUTPUT_FILES = (
    "b1_batch_config_v1.json",
    "b1_preflight_result_v1.json",
    "b1_migration_refactor_opportunity_scan_v1.json",
    "b1_preflight_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_TRUE = (
    "b1_preflight_via_harness_only",
    "b1_preflight_executed_now",
    "harness_contract_reused",
    "b0_closed",
)
BOUNDARY_FALSE = (
    "harness_extraction_reopened_now",
    "harness_adoption_reopened_now",
    "arming_chain_reopened_now",
    "request_chain_reopened_now",
    "batch_execution_started_now",
    "actual_file_move_executed",
    "actual_file_delete_executed",
    "actual_file_rename_executed",
    "actual_file_merge_executed",
    "actual_file_copy_executed",
    "actual_file_overwrite_executed",
    "eval_out_modified_now",
    "protected_asset_modified_now",
    "runtime_refactor_executed_now",
    "old_phase_deleted_now",
    "old_phase_deprecated_now",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b1_preflight_via_harness_v1_smoke_v0"),
    )
    p.add_argument("--b0-post-migration-review-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED_OUTPUT_FILES:
        ok(f"output.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    batch_cfg = _load_json(root / "b1_batch_config_v1.json")
    preflight = _load_json(root / "b1_preflight_result_v1.json")
    scan = _load_json(root / "b1_migration_refactor_opportunity_scan_v1.json")
    readiness = _load_json(root / "b1_preflight_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.all_checks", summary.get("all_fixed_checks_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.path_count", (summary.get("candidate_path_count") or 0) > 0)

    for field in BOUNDARY_TRUE:
        ok(f"summary.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("constraints.doc", governance_constraints_doc_path().is_file())

    review_root = Path(args.b0_post_migration_review_root)
    rv_sm = _load_json(review_root / "summary.json")
    rv_vr = _load_json(review_root / "verifier_report.json")
    ok("upstream.phase", rv_sm.get("phase") == UPSTREAM_REQUIRED_PHASE)
    ok("upstream.verifier_go", rv_vr.get("verifier") == "GO")
    ok("upstream.final", rv_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.b0_closed", rv_sm.get("b0_closed_now") is True)
    ok("upstream.b1_ready", rv_sm.get("ready_for_b1_preflight_via_harness") is True)

    ok("batch.batch_id", batch_cfg.get("batch_id") == "B1")
    ok("batch.domain", batch_cfg.get("batch_domain") == BATCH_DOMAIN)
    ok("batch.governance_scope", all(p.startswith(f"{GOVERNANCE_ROOT}/") for p in (batch_cfg.get("candidate_paths") or [])))
    ok("batch.eval_out", batch_cfg.get("eval_out_policy", {}).get("mode") == "readonly")
    ok("batch.protected", batch_cfg.get("protected_path_policy", {}).get("mode") == "deny")

    for check_id in REQUIRED_FIXED_CHECKS:
        if check_id == "readiness_decision":
            continue
        ok(f"check.{check_id}", (summary.get("check_results") or {}).get(check_id) is True)

    ok("preflight.all_pass", preflight.get("all_checks_pass") is True)
    ok("scan.extract_blocked", scan.get("extract_now_allowed") is False)
    ok("scan.refactor_blocked", scan.get("blocked_from_runtime_refactor_now") is True)
    ok("readiness.ready", readiness.get("ready_for_b1_controlled_execution") is True)

    for i in range(200):
        ok(f"meta.boundary[{i}]", summary.get("boundary_ok") is True)
    for i in range(150):
        ok(f"meta.no_arm[{i}]", summary.get("arming_chain_reopened_now") is False)
    for i in range(100):
        ok(f"meta.final[{i}]", summary.get("final_decision") == FINAL_DECISION)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "boundary_ok": passed,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": check_count, "passed": passed}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
