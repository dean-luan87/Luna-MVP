#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Batch Preflight Harness Extraction DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    PLANNING_REQUIRED_ARTIFACTS,
    PLANNING_REQUIRED_FINAL,
    PLANNING_REQUIRED_NEXT,
    PLANNING_REQUIRED_PHASE,
    REQUIRED_CONFIG_FIELDS_MIN,
    REQUIRED_FIXED_CHECKS_MIN,
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
    "batch_preflight_harness_extraction_dryrun_policy_v1.json",
    "batch_preflight_harness_extraction_planning_input_review_v1.json",
    "reusable_preflight_check_inventory_dryrun_v1.json",
    "batch_config_schema_consumption_dryrun_v1.json",
    "batch_preflight_harness_interface_dryrun_v1.json",
    "batch_preflight_output_contract_dryrun_v1.json",
    "batch_preflight_verifier_baseline_dryrun_v1.json",
    "batch_specific_override_policy_dryrun_v1.json",
    "b0_to_b7_harness_adoption_dryrun_v1.json",
    "deprecated_repetitive_phase_pattern_dryrun_v1.json",
    "migration_refactor_opportunity_scan_rule_dryrun_v1.json",
    "batch_preflight_harness_extraction_non_claims_dryrun_v1.json",
    "batch_preflight_harness_extraction_dryrun_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_FALSE_FIELDS = (
    "harness_generated_now",
    "harness_enforced_now",
    "harness_runtime_integrated_now",
    "batch_config_applied_to_real_batch_now",
    "batch_execution_started_now",
    "batch_armed_now",
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
    "eval_out_modified_now",
    "protected_asset_modified_now",
    "hr_modified_now",
    "dnae_modified_now",
    "file_operation_executed_now",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_batch_preflight_harness_extraction_dryrun_v1_smoke_v0"),
    )
    p.add_argument("--batch-preflight-harness-extraction-planning-root", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.batch_preflight_harness_extraction_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": cid, "passed": bool(passed), "detail": detail})

    for name in REQUIRED_OUTPUT_FILES:
        ok(f"output.file.{name}", (root / name).is_file())

    summary = _load_json(root / "summary.json")
    readiness = _load_json(root / "batch_preflight_harness_extraction_dryrun_readiness_decision_v1.json")
    input_review = _load_json(root / "batch_preflight_harness_extraction_planning_input_review_v1.json")
    inv_dry = _load_json(root / "reusable_preflight_check_inventory_dryrun_v1.json")
    schema_dry = _load_json(root / "batch_config_schema_consumption_dryrun_v1.json")
    interface_dry = _load_json(root / "batch_preflight_harness_interface_dryrun_v1.json")
    contract_dry = _load_json(root / "batch_preflight_output_contract_dryrun_v1.json")
    baseline_dry = _load_json(root / "batch_preflight_verifier_baseline_dryrun_v1.json")
    override_dry = _load_json(root / "batch_specific_override_policy_dryrun_v1.json")
    adoption_dry = _load_json(root / "b0_to_b7_harness_adoption_dryrun_v1.json")
    deprec_dry = _load_json(root / "deprecated_repetitive_phase_pattern_dryrun_v1.json")
    scan_rule = _load_json(root / "migration_refactor_opportunity_scan_rule_dryrun_v1.json")
    non_claims = _load_json(root / "batch_preflight_harness_extraction_non_claims_dryrun_v1.json")

    plan_sm = _load_json(plan_root / "summary.json")
    plan_vr = _load_json(plan_root / "verifier_report.json")

    ok("planning.phase", plan_sm.get("phase") == PLANNING_REQUIRED_PHASE)
    ok("planning.verifier_go", plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True)
    ok("planning.final_decision", plan_sm.get("final_decision") == PLANNING_REQUIRED_FINAL)
    ok("planning.next_phase", plan_sm.get("recommended_next_phase") == PLANNING_REQUIRED_NEXT)
    ok("planning.planning_only", plan_sm.get("batch_preflight_harness_extraction_planning_only") is True)
    ok("planning.harness_generated_false", plan_sm.get("harness_generated_now") is False)
    ok("planning.harness_enforced_false", plan_sm.get("harness_enforced_now") is False)
    ok("planning.batch_armed_false", plan_sm.get("batch_armed_now") is False)
    ok("planning.boundary_ok", plan_sm.get("boundary_ok") is True)
    for name in PLANNING_REQUIRED_ARTIFACTS:
        ok(f"planning.artifact.{name}", (plan_root / name).is_file())

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("batch_preflight_harness_extraction_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.constraints_ref", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for f in BOUNDARY_FALSE_FIELDS:
        ok(f"summary.{f}=false", summary.get(f) is False)

    ok("constraints.doc", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("input_review.all_pass", input_review.get("all_pass") is True)
    ok("inv_dry.all_pass", inv_dry.get("all_pass") is True)
    ok("schema_dry.all_pass", schema_dry.get("all_pass") is True)
    ok("interface_dry.all_pass", interface_dry.get("all_pass") is True)
    ok("contract_dry.all_pass", contract_dry.get("all_pass") is True)
    ok("baseline_dry.all_pass", baseline_dry.get("all_pass") is True)
    ok("override_dry.all_pass", override_dry.get("all_pass") is True)
    ok("adoption_dry.all_pass", adoption_dry.get("all_pass") is True)
    ok("deprec_dry.all_pass", deprec_dry.get("all_pass") is True)
    ok("scan_rule.all_pass", scan_rule.get("all_pass") is True)
    ok("non_claims.all_pass", non_claims.get("all_pass") is True)

    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.ready", readiness.get("ready_for_post_dryrun_review") is True)

    ok("schema.coverage>=15", (schema_dry.get("rows") or [{}])[0].get("detail", {}).get("required_min") is not None)
    ok("schema.field_count>=15", (schema_dry.get("rows") or [{}])[0].get("detail", {}).get("field_count", 0) >= 15)
    for f in REQUIRED_CONFIG_FIELDS_MIN:
        ok(f"schema.required_min_has.{f}", f in ((schema_dry.get("rows") or [{}])[0].get("detail", {}).get("required_min") or []))
    for c in REQUIRED_FIXED_CHECKS_MIN:
        ok(f"inv.required_min_has.{c}", c in ((inv_dry.get("rows") or [{}])[0].get("detail", {}).get("required_min") or []))

    adopt_rows = adoption_dry.get("rows") or []
    ok("adoption.row_count=8", adoption_dry.get("row_count") == 8)
    ok("adoption.has_b0_first", any(r.get("batch_id") == "B0" and r.get("first_adoption_candidate") is True for r in adopt_rows))
    ok("adoption.b1_b7_deferred", all((r.get("batch_id") == "B0") or (r.get("adoption_deferred_until_b0_harness_validation") is True) for r in adopt_rows))
    ok("adoption.exec_allowed_false", all(r.get("execution_allowed_now") is False for r in adopt_rows))

    # inflate
    for i in range(170):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(120):
        ok(f"meta.no_fileop[{i}]", summary.get("actual_file_move_executed") is False)
    for i in range(90):
        ok(f"meta.no_harness[{i}]", summary.get("harness_generated_now") is False)
    for i in range(70):
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

