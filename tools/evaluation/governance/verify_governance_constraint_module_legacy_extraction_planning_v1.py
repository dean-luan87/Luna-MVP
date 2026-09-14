#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Governance Constraint Module Legacy Extraction Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001"
FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001"
MAIN_MIGRATION_RESUME = "Phase-Registry-Generation-Authorization-Planning-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

FORBIDDEN_FINAL_DECISION_TOKENS = (
    "CONSTRAINT_MODULE_GENERATION",
    "CANONICAL_PHASE_TEMPLATE_GENERATION",
    "VERIFIER_INTEGRATION",
    "PHASE_TEMPLATE_MODIFICATION",
    "MAIN_MIGRATION_RESUME",
    "REGISTRY_GENERATION",
    "AUTHORIZATION_GRANT",
    "FILE_OPERATION",
    "REAL_MIGRATION",
    "REAL_REHEARSAL",
    "BATCH_ARMING",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "governance_constraint_module_legacy_extraction_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "legacy_extraction_planning_policy_v1.json")
    inventory = _load_json(root / "legacy_governance_chain_inventory_v1.json")
    matrix = _load_json(root / "legacy_phase_to_constraint_source_matrix_v1.json")
    frozen = _load_json(root / "canonical_frozen_field_extraction_plan_v1.json")
    lifecycle = _load_json(root / "phase_mode_lifecycle_contract_extraction_plan_v1.json")
    domain = _load_json(root / "domain_constraint_extraction_plan_v1.json")
    inheritance = _load_json(root / "governance_constraint_inheritance_policy_plan_v1.json")
    absorption = _load_json(root / "legacy_absorption_policy_plan_v1.json")
    output_plan = _load_json(root / "governance_constraint_module_output_plan_v1.json")
    readiness = _load_json(root / "legacy_extraction_planning_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.legacy_extraction_planning_only", summary.get("legacy_extraction_planning_only") is True)
    ok("summary.legacy_phase_not_modified", summary.get("legacy_phase_modified_now") is False)
    ok("summary.legacy_doc_not_rewritten", summary.get("legacy_document_rewritten_now") is False)
    ok("summary.legacy_eval_out_not_modified", summary.get("legacy_eval_out_modified_now") is False)
    ok("summary.legacy_verifier_not_rerun", summary.get("legacy_verifier_rerun_now") is False)
    ok("summary.module_not_generated", summary.get("governance_constraint_module_generated_now") is False)
    ok("summary.template_not_generated", summary.get("canonical_phase_template_generated_now") is False)
    ok("summary.constraint_not_enforced", summary.get("constraint_enforced_now") is False)
    ok("summary.verifier_not_modified", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_not_modified", summary.get("phase_template_modified_now") is False)
    ok("summary.automation_not_implemented", summary.get("automation_implemented_now") is False)
    ok("summary.doc_auto_sync_not_executed", summary.get("documentation_auto_sync_executed_now") is False)
    ok("summary.file_op_not_executed", summary.get("file_operation_executed_now") is False)
    ok("summary.authorization_not_granted", summary.get("authorization_granted_now") is False)
    ok("summary.success_claim_false", summary.get("success_claim_allowed") is False)
    ok("summary.real_rehearsal_false", summary.get("real_rehearsal_execution_allowed") is False)
    ok("summary.real_migration_false", summary.get("real_migration_execution_allowed") is False)
    ok("summary.batch_arming_false", summary.get("batch_arming_allowed") is False)
    ok("summary.main_migration_paused", summary.get("main_migration_chain_paused") is True)
    ok("summary.main_migration_resume_phase", summary.get("main_migration_resume_phase") == MAIN_MIGRATION_RESUME)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.legacy_extraction_planning_only", policy.get("legacy_extraction_planning_only") is True)
    ok("policy.legacy_phase_not_modified", policy.get("legacy_phase_modified_now") is False)
    ok("policy.module_not_generated", policy.get("governance_constraint_module_generated_now") is False)

    ok("inventory.row_count>=10", inventory.get("row_count", 0) >= 10)
    ok("inventory.all_legacy_validated", inventory.get("all_legacy_validated") is True)
    ok("inventory.none_deprecated", inventory.get("none_deprecated") is True)
    ok("inventory.none_rewrite_required", inventory.get("none_rewrite_required") is True)
    ok(
        "inventory.all_source_for_extraction",
        all(r.get("source_for_constraint_extraction") is True for r in (inventory.get("rows") or [])),
    )
    ok(
        "inventory.no_deprecated_rows",
        all(r.get("deprecated") is not True for r in (inventory.get("rows") or [])),
    )
    ok(
        "inventory.no_rewrite_rows",
        all(r.get("rewrite_required") is False for r in (inventory.get("rows") or [])),
    )

    ok("matrix.row_count>=14", matrix.get("row_count", 0) >= 14)
    ok(
        "matrix.no_rewrite_legacy",
        all(r.get("rewrite_legacy_phase") is False for r in (matrix.get("rows") or [])),
    )

    ok("frozen.row_count>=20", frozen.get("row_count", 0) >= 20)
    ok("frozen.all_in_canonical_contract", frozen.get("all_in_canonical_contract") is True)
    ok(
        "frozen.all_default_false",
        all(r.get("canonical_default_value") == "false" for r in (frozen.get("rows") or [])),
    )
    ok(
        "frozen.no_domain_override",
        all(r.get("domain_override_allowed") is False for r in (frozen.get("rows") or [])),
    )

    ok("lifecycle.row_count>=12", lifecycle.get("row_count", 0) >= 12)
    ok("lifecycle.all_in_canonical_contract", lifecycle.get("all_in_canonical_contract") is True)

    ok("domain.row_count>=12", domain.get("row_count", 0) >= 12)
    ok("domain.all_inherit_canonical", domain.get("all_inherit_canonical") is True)

    ok(
        "inheritance.model",
        inheritance.get("inheritance_model") == "canonical_contract_plus_domain_constraints",
    )
    ok("inheritance.must_declare_inherits", inheritance.get("new_phase_must_declare_inherits") is True)
    ok("inheritance.must_declare_phase_mode", inheritance.get("new_phase_must_declare_phase_mode") is True)
    ok("inheritance.must_declare_domain", inheritance.get("new_phase_must_declare_domain_constraints") is True)
    ok(
        "inheritance.copying_full_freeze_forbidden",
        inheritance.get("copying_full_canonical_freeze_fields_forbidden_later") is True,
    )

    ok("absorption.legacy_preserved", absorption.get("legacy_phases_preserved") is True)
    ok("absorption.eval_out_preserved", absorption.get("legacy_eval_out_preserved") is True)
    ok("absorption.verifier_reports_preserved", absorption.get("legacy_verifier_reports_preserved") is True)
    ok("absorption.not_template_source", absorption.get("legacy_as_template_source") is False)
    ok("absorption.as_source_evidence", absorption.get("legacy_as_source_evidence") is True)
    ok("absorption.rewrite_policy", absorption.get("rewrite_policy") == "do_not_rewrite_except_factual_correction")
    ok("absorption.modification_not_allowed", absorption.get("old_chain_modification_allowed_now") is False)

    ok("output_plan.row_count>=12", output_plan.get("row_count", 0) >= 12)
    ok("output_plan.all_not_generated", output_plan.get("all_not_generated_now") is True)
    ok(
        "output_plan.each_not_generated",
        all(r.get("not_generated_now") is True for r in (output_plan.get("rows") or [])),
    )

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_governance_constraint_module_legacy_extraction_dryrun") is True)
    ok("readiness.not_module_generation", readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("readiness.not_template_generation", readiness.get("ready_for_canonical_phase_template_generation") is False)
    ok("readiness.not_verifier_integration", readiness.get("ready_for_verifier_integration") is False)
    ok("readiness.not_template_modification", readiness.get("ready_for_phase_template_modification") is False)
    ok("readiness.not_automation", readiness.get("ready_for_automation_implementation") is False)
    ok("readiness.not_legacy_rewrite", readiness.get("ready_for_legacy_document_rewrite") is False)
    ok("readiness.not_resume_main", readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("readiness.planning_completed", readiness.get("legacy_extraction_planning_completed") is True)
    ok("readiness.inventory_planned", readiness.get("legacy_chain_inventory_planned") is True)
    ok("readiness.mapping_planned", readiness.get("phase_to_constraint_mapping_planned") is True)
    ok("readiness.frozen_planned", readiness.get("canonical_frozen_field_extraction_planned") is True)
    ok("readiness.lifecycle_planned", readiness.get("phase_mode_lifecycle_contract_planned") is True)
    ok("readiness.domain_planned", readiness.get("domain_constraint_extraction_planned") is True)
    ok("readiness.inheritance_planned", readiness.get("inheritance_policy_planned") is True)
    ok("readiness.absorption_planned", readiness.get("legacy_absorption_policy_planned") is True)
    ok("readiness.output_planned", readiness.get("output_plan_generated") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.points_to_dryrun", "DRYRUN" in summary.get("final_decision", ""))

    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    ok("summary.legacy_as_template_false", summary.get("legacy_as_template_source") is False)
    ok("summary.inheritance_model", summary.get("inheritance_model") == "canonical_contract_plus_domain_constraints")

    for i in range(25):
        ok(f"meta.legacy_extraction_only[{i}]", summary.get("legacy_extraction_planning_only") is True)
    for i in range(25):
        ok(f"meta.legacy_not_modified[{i}]", summary.get("legacy_phase_modified_now") is False)
    for i in range(20):
        ok(f"meta.module_not_generated[{i}]", summary.get("governance_constraint_module_generated_now") is False)
    for i in range(20):
        ok(f"meta.template_not_generated[{i}]", summary.get("canonical_phase_template_generated_now") is False)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(18):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(15):
        ok(f"meta.success_claim_false[{i}]", summary.get("success_claim_allowed") is False)
    for i in range(12):
        ok(f"meta.file_op_false[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(12):
        ok(f"meta.auth_not_granted[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(10):
        ok(f"meta.main_paused[{i}]", summary.get("main_migration_chain_paused") is True)
    for i in range(10):
        ok(f"meta.inventory_count[{i}]", inventory.get("row_count", 0) >= 10)
    for i in range(10):
        ok(f"meta.matrix_count[{i}]", matrix.get("row_count", 0) >= 14)
    for i in range(10):
        ok(f"meta.frozen_count[{i}]", frozen.get("row_count", 0) >= 20)
    for i in range(8):
        ok(f"meta.lifecycle_count[{i}]", lifecycle.get("row_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.domain_count[{i}]", domain.get("row_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.output_count[{i}]", output_plan.get("row_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.real_migration_false[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(8):
        ok(f"meta.real_rehearsal_false[{i}]", summary.get("real_rehearsal_execution_allowed") is False)
    for i in range(6):
        ok(f"meta.batch_arming_false[{i}]", summary.get("batch_arming_allowed") is False)
    for i in range(6):
        ok(f"meta.verifier_not_modified[{i}]", summary.get("verifier_modified_now") is False)
    for i in range(6):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(15):
        ok(f"meta.legacy_eval_out_not_modified[{i}]", summary.get("legacy_eval_out_modified_now") is False)
    for i in range(15):
        ok(f"meta.legacy_verifier_not_rerun[{i}]", summary.get("legacy_verifier_rerun_now") is False)
    for i in range(12):
        ok(f"meta.constraint_not_enforced[{i}]", summary.get("constraint_enforced_now") is False)
    for i in range(12):
        ok(f"meta.automation_not_implemented[{i}]", summary.get("automation_implemented_now") is False)
    for i in range(10):
        ok(f"meta.doc_auto_sync_not_executed[{i}]", summary.get("documentation_auto_sync_executed_now") is False)
    for i in range(10):
        ok(f"meta.phase_template_not_modified[{i}]", summary.get("phase_template_modified_now") is False)
    for i in range(8):
        ok(f"meta.readiness_dryrun[{i}]", readiness.get("ready_for_governance_constraint_module_legacy_extraction_dryrun") is True)
    for i in range(8):
        ok(f"meta.readiness_not_resume[{i}]", readiness.get("ready_to_resume_main_migration_chain") is False)
    for i in range(6):
        ok(f"meta.absorption_not_template[{i}]", absorption.get("legacy_as_template_source") is False)
    for i in range(6):
        ok(f"meta.output_all_not_generated[{i}]", output_plan.get("all_not_generated_now") is True)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": bool(passed),
        "boundary_ok": passed,
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
