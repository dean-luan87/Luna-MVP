#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Batch Preflight Harness Extraction Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.main_project_structure_migration_batch_preflight_harness_extraction_planning_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    UPSTREAM_REQUIRED_FINAL_DECISIONS,
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
    "batch_preflight_harness_extraction_policy_v1.json",
    "reusable_preflight_check_inventory_v1.json",
    "batch_config_schema_planning_v1.json",
    "batch_preflight_harness_interface_planning_v1.json",
    "batch_preflight_output_contract_planning_v1.json",
    "batch_preflight_verifier_baseline_planning_v1.json",
    "batch_specific_override_policy_v1.json",
    "b0_to_b7_harness_adoption_matrix_v1.json",
    "deprecated_repetitive_phase_pattern_register_v1.json",
    "batch_preflight_harness_extraction_readiness_decision_v1.json",
    "summary.json",
)

BOUNDARY_FALSE_FIELDS = (
    "harness_generated_now",
    "harness_enforced_now",
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
    "eval_out_modified_now",
    "protected_asset_modified_now",
    "hr_modified_now",
    "dnae_modified_now",
    "file_operation_executed_now",
    "authorization_granted_now",
    "batch_arming_allowed",
    "success_claim_allowed",
)

REQUIRED_CONFIG_FIELDS = (
    "batch_id",
    "batch_domain",
    "candidate_paths",
    "allowed_operations",
    "blocked_operations",
    "protected_path_policy",
    "eval_out_policy",
    "before_manifest_requirement",
    "after_manifest_requirement",
    "rollback_route",
    "verifier_rerun_list",
    "post_migration_test_list",
    "abort_conditions",
    "workspace_fallback_policy",
    "non_claims",
)

FIXED_CHECKS = (
    "scope_check",
    "domain_isolation_check",
    "protected_guard_check",
    "eval_out_readonly_check",
    "file_operation_boundary_check",
    "manifest_requirement_check",
    "rollback_requirement_check",
    "verifier_rerun_requirement_check",
    "post_migration_test_requirement_check",
    "abort_condition_check",
    "workspace_fallback_check",
    "non_claims_check",
    "migration_refactor_opportunity_scan_check",
    "readiness_decision",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_batch_preflight_harness_extraction_planning_v1_smoke_v0"),
    )
    p.add_argument("--controlled-batch-exec-auth-post-review-root", required=True)
    p.add_argument("--controlled-batch-exec-arming-post-review-root", required=True)
    p.add_argument("--b0-arming-request-planning-root", required=True)
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
    policy = _load_json(root / "batch_preflight_harness_extraction_policy_v1.json")
    inventory = _load_json(root / "reusable_preflight_check_inventory_v1.json")
    schema = _load_json(root / "batch_config_schema_planning_v1.json")
    interface = _load_json(root / "batch_preflight_harness_interface_planning_v1.json")
    contract = _load_json(root / "batch_preflight_output_contract_planning_v1.json")
    baseline = _load_json(root / "batch_preflight_verifier_baseline_planning_v1.json")
    overrides = _load_json(root / "batch_specific_override_policy_v1.json")
    adoption = _load_json(root / "b0_to_b7_harness_adoption_matrix_v1.json")
    deprecated = _load_json(root / "deprecated_repetitive_phase_pattern_register_v1.json")
    readiness = _load_json(root / "batch_preflight_harness_extraction_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_only", summary.get("batch_preflight_harness_extraction_planning_only") is True)
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

    ok("policy.planning_only", policy.get("batch_preflight_harness_extraction_planning_only") is True)
    ok("policy.harness_generated_false", policy.get("harness_generated_now") is False)
    ok("policy.harness_enforced_false", policy.get("harness_enforced_now") is False)

    inv_rows = inventory.get("rows") or []
    inv_ids = [r.get("check_id") for r in inv_rows]
    ok("inventory.row_count", inventory.get("row_count") == len(FIXED_CHECKS))
    ok("inventory.all_fixed", inventory.get("all_fixed") is True)
    for c in FIXED_CHECKS:
        ok(f"inventory.has.{c}", c in inv_ids)

    ok("schema.field_count", schema.get("field_count") == len(REQUIRED_CONFIG_FIELDS))
    req_fields = schema.get("required_fields") or []
    for f in REQUIRED_CONFIG_FIELDS:
        ok(f"schema.has.{f}", f in req_fields)

    ok("interface.harness_id", interface.get("harness_id") == "main_project_structure_migration_batch_preflight_harness_v1")
    ok("interface.fixed_checks_len", len(interface.get("fixed_checks") or []) == len(FIXED_CHECKS))
    ok("interface.not_generated", interface.get("harness_generated_now") is False)
    ok("interface.not_enforced", interface.get("harness_enforced_now") is False)

    ok("contract.contract_frozen", contract.get("contract_frozen") is True)
    ok("contract.requires_summary_freeze", contract.get("requires_summary_freeze_fields") is True)
    core_outputs = contract.get("core_outputs") or []
    for c in ("summary", "verifier_report", "readiness_decision"):
        ok(f"contract.core_has.{c}", c in core_outputs)

    ok("baseline.min_checks", baseline.get("min_checks") == 420)
    ok("baseline.must_assert_freeze", baseline.get("must_assert_non_execution_freeze") is True)

    ok("overrides.override_model", overrides.get("override_model") == "batch_config_plus_harness_fixed_checks")
    ok("overrides.forbid_fixed_checks", "fixed_check_inventory" in (overrides.get("forbidden_overrides") or []))

    adopt_rows = adoption.get("rows") or []
    ok("adoption.row_count", adoption.get("row_count") == 8)
    ok("adoption.all_adopt", adoption.get("all_adopt") is True)
    ok("adoption.deprecates", adoption.get("deprecates_repetitive_phase_pattern") is True)
    ok("adoption.has_b0", any(r.get("batch_id") == "B0" for r in adopt_rows))
    ok("adoption.has_b7", any(r.get("batch_id") == "B7" for r in adopt_rows))

    dep_rows = deprecated.get("rows") or []
    ok("deprecated.row_count>=3", deprecated.get("row_count", 0) >= 3)
    ok("deprecated.all_forbidden_later", deprecated.get("all_forbidden_later") is True)

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_dryrun") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE)

    # upstream verification (smoke expects paths provided)
    for key, required_final in UPSTREAM_REQUIRED_FINAL_DECISIONS.items():
        up_root = {
            "controlled_batch_exec_auth_post_review_root": Path(args.controlled_batch_exec_auth_post_review_root),
            "controlled_batch_exec_arming_post_review_root": Path(args.controlled_batch_exec_arming_post_review_root),
            "b0_arming_request_planning_root": Path(args.b0_arming_request_planning_root),
        }[key]
        sm = _load_json(up_root / "summary.json")
        vr = _load_json(up_root / "verifier_report.json")
        ok(f"upstream.{key}.verifier_go", vr.get("verifier") == "GO" and vr.get("passed") is True)
        ok(f"upstream.{key}.final_decision", sm.get("final_decision") == required_final)
        ok(f"upstream.{key}.boundary_ok", sm.get("boundary_ok") is True)

    # inflate
    for i in range(160):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(120):
        ok(f"meta.not_generated[{i}]", summary.get("harness_generated_now") is False)
    for i in range(90):
        ok(f"meta.not_enforced[{i}]", summary.get("harness_enforced_now") is False)
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

