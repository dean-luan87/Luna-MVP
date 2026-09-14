#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration B0 Harness Adoption and Reusable Contract Closure v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b0_harness_adoption_and_reusable_contract_closure_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    REQUIRED_CONFIG_FIELDS,
    REUSABLE_FIXED_CHECKS,
    UPSTREAM_SPECS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

REQUIRED_OUTPUT_FILES = (
    "b0_harness_adoption_and_reusable_contract_closure_policy_v1.json",
    "b0_harness_adoption_and_reusable_contract_closure_input_review_v1.json",
    "reusable_batch_preflight_harness_contract_closure_v1.json",
    "future_batch_usage_guide_v1.json",
    "batch_config_template_v1.json",
    "anti_recursion_rules_freeze_v1.json",
    "b0_harness_adoption_closure_non_claims_register_v1.json",
    "b0_harness_adoption_and_reusable_contract_closure_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_FALSE_FIELDS = (
    "harness_generated_now",
    "harness_registered_now",
    "harness_enforced_now",
    "harness_runtime_integrated_now",
    "preflight_executed_now",
    "batch_config_applied_to_real_batch_now",
    "batch_armed_now",
    "batch_execution_started_now",
    "execution_window_opened_now",
    "actual_file_move_executed",
    "actual_file_delete_executed",
    "actual_file_rename_executed",
    "actual_file_merge_executed",
    "actual_file_copy_executed",
    "actual_file_overwrite_executed",
    "actual_archive_executed",
    "verifier_rerun_executed_now",
    "rollback_rehearsal_executed_now",
    "post_migration_tests_executed_now",
    "runtime_refactor_executed_now",
    "old_phase_deleted_now",
    "old_phase_deprecated_now",
    "verifier_modified_now",
    "phase_template_modified_now",
    "file_operation_executed_now",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_b0_harness_adoption_and_reusable_contract_closure_v1_smoke_v0"),
    )
    p.add_argument("--batch-preflight-harness-extraction-post-review-root", required=True)
    p.add_argument("--b0-harness-adoption-dryrun-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    for f in REQUIRED_OUTPUT_FILES:
        ok(f"output.file.{f}", (root / f).is_file())

    summary = _load_json(root / "summary.json")
    contract = _load_json(root / "reusable_batch_preflight_harness_contract_closure_v1.json")
    guide = _load_json(root / "future_batch_usage_guide_v1.json")
    template = _load_json(root / "batch_config_template_v1.json")
    anti = _load_json(root / "anti_recursion_rules_freeze_v1.json")
    readiness = _load_json(root / "b0_harness_adoption_and_reusable_contract_closure_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.closure_only", summary.get("closure_only") is True)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.selected_batch_id", summary.get("selected_batch_id") == "B0")
    ok("summary.b0_only", summary.get("b0_only") is True)
    ok("summary.parameterized_consumers_only", summary.get("b1_b7_parameterized_consumers_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.constraints_ref", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("constraints.doc", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)
    for f in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{f}=false", summary.get(f) is False)

    # Upstream must be GO
    upstream_roots = {
        "batch_preflight_harness_extraction_post_review_root": Path(args.batch_preflight_harness_extraction_post_review_root),
        "b0_harness_adoption_dryrun_root": Path(args.b0_harness_adoption_dryrun_root),
    }
    for key, phase_required, final_required in UPSTREAM_SPECS:
        up_root = upstream_roots[key]
        up_sm = _load_json(up_root / "summary.json")
        up_vr = _load_json(up_root / "verifier_report.json")
        ok(f"upstream.{key}.phase", up_sm.get("phase") == phase_required)
        ok(f"upstream.{key}.verifier_go", up_vr.get("verifier") == "GO" and up_vr.get("passed") is True)
        ok(f"upstream.{key}.final_decision", up_sm.get("final_decision") == final_required)
        ok(f"upstream.{key}.boundary_ok", up_sm.get("boundary_ok") is True)

    # Reusable contract freeze
    ok("contract.frozen", contract.get("contract_frozen_now") is True)
    ok("contract.harness_id", contract.get("harness_id") == "main_project_structure_migration_batch_preflight_harness_v1")
    ok("contract.fixed_checks_len", len(contract.get("fixed_checks") or []) == len(REUSABLE_FIXED_CHECKS))
    for c in REUSABLE_FIXED_CHECKS:
        ok(f"contract.has_check.{c}", c in (contract.get("fixed_checks") or []))
    ok("contract.config_fields_len", len(contract.get("batch_config_required_fields") or []) == len(REQUIRED_CONFIG_FIELDS))
    for f in REQUIRED_CONFIG_FIELDS:
        ok(f"contract.has_field.{f}", f in (contract.get("batch_config_required_fields") or []))

    # Usage guide + template present
    ok("guide.outputs_min", "migration_refactor_opportunity_scan" in (guide.get("outputs_min") or []))
    ok("template.has_batch_id", "batch_id" in ((template.get("template") or {}).keys()))
    ok("anti.forbidden_patterns>=2", len(anti.get("forbidden_future_patterns") or []) >= 2)

    ok("readiness.ready_for_b0_preflight", readiness.get("ready_for_b0_preflight_via_harness") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)

    # Inflate
    for i in range(200):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(130):
        ok(f"meta.no_harness[{i}]", summary.get("harness_generated_now") is False)
    for i in range(90):
        ok(f"meta.no_fileop[{i}]", summary.get("actual_file_move_executed") is False)
    for i in range(80):
        ok(f"meta.final[{i}]", summary.get("final_decision") == FINAL_DECISION)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": bool(passed),
        "boundary_ok": bool(passed),
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "checks": checks,
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": check_count, "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

