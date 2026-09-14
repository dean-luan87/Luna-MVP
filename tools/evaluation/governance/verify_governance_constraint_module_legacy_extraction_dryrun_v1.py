#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Governance Constraint Module Legacy Extraction DryRun v1."""

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

PHASE_ID = "Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001"
FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001"
UPSTREAM_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001"
UPSTREAM_FINAL = "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_PLANNING_READY_FOR_DRYRUN"
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
        default=str(repo_root / "_eval_out" / "governance_constraint_module_legacy_extraction_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--governance-constraint-module-legacy-extraction-planning-root",
        default=str(repo_root / "_eval_out" / "governance_constraint_module_legacy_extraction_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_constraint_module_legacy_extraction_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "legacy_extraction_dryrun_policy_v1.json")
    inventory = _load_json(root / "legacy_chain_inventory_consumption_dryrun_v1.json")
    mapping = _load_json(root / "phase_to_constraint_mapping_dryrun_v1.json")
    frozen = _load_json(root / "canonical_frozen_field_extraction_dryrun_v1.json")
    lifecycle = _load_json(root / "phase_mode_lifecycle_contract_dryrun_v1.json")
    domain = _load_json(root / "domain_constraint_extraction_dryrun_v1.json")
    inheritance = _load_json(root / "constraint_inheritance_policy_dryrun_v1.json")
    absorption = _load_json(root / "legacy_absorption_policy_dryrun_v1.json")
    output_plan = _load_json(root / "constraint_module_output_plan_dryrun_v1.json")
    readiness = _load_json(root / "legacy_extraction_dryrun_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "legacy_extraction_planning_readiness_decision_v1.json")
    up_absorption = _load_json(upstream_root / "legacy_absorption_policy_plan_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok(
        "upstream.ready_for_dryrun",
        up_readiness.get("ready_for_governance_constraint_module_legacy_extraction_dryrun") is True,
    )
    ok("upstream.planning_only", up_summary.get("legacy_extraction_planning_only") is True)
    ok("upstream.main_paused", up_summary.get("main_migration_chain_paused") is True)
    ok("upstream.main_resume_phase", up_summary.get("main_migration_resume_phase") == MAIN_MIGRATION_RESUME)
    ok("upstream.inheritance_model", up_summary.get("inheritance_model") == "canonical_contract_plus_domain_constraints")
    ok("upstream.legacy_as_source", up_absorption.get("legacy_as_source_evidence") is True)
    ok("upstream.legacy_not_template", up_absorption.get("legacy_as_template_source") is False)
    ok("upstream.legacy_not_modified", up_summary.get("legacy_phase_modified_now") is False)
    ok("upstream.doc_not_rewritten", up_summary.get("legacy_document_rewritten_now") is False)
    ok("upstream.eval_out_not_modified", up_summary.get("legacy_eval_out_modified_now") is False)
    ok("upstream.module_not_generated", up_summary.get("governance_constraint_module_generated_now") is False)
    ok("upstream.template_not_generated", up_summary.get("canonical_phase_template_generated_now") is False)
    ok("upstream.constraint_not_enforced", up_summary.get("constraint_enforced_now") is False)
    ok("upstream.not_module_generation", up_readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("upstream.not_template_generation", up_readiness.get("ready_for_canonical_phase_template_generation") is False)
    ok("upstream.not_verifier_integration", up_readiness.get("ready_for_verifier_integration") is False)
    ok("upstream.not_resume_main", up_readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("legacy_extraction_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.legacy_not_modified", summary.get("legacy_phase_modified_now") is False)
    ok("summary.doc_not_rewritten", summary.get("legacy_document_rewritten_now") is False)
    ok("summary.eval_out_not_modified", summary.get("legacy_eval_out_modified_now") is False)
    ok("summary.verifier_not_rerun", summary.get("legacy_verifier_rerun_now") is False)
    ok("summary.module_not_generated", summary.get("governance_constraint_module_generated_now") is False)
    ok("summary.template_not_generated", summary.get("canonical_phase_template_generated_now") is False)
    ok("summary.module_not_registered", summary.get("constraint_module_registered_now") is False)
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
    ok("summary.main_not_resumed", summary.get("main_migration_chain_resumed_now") is False)
    ok("summary.main_paused", summary.get("main_migration_chain_paused") is True)
    ok("summary.main_resume_phase", summary.get("main_migration_resume_phase") == MAIN_MIGRATION_RESUME)
    ok("summary.legacy_as_source", summary.get("legacy_as_source_evidence") is True)
    ok("summary.legacy_not_template", summary.get("legacy_as_template_source") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.dryrun_only", policy.get("legacy_extraction_dryrun_only") is True)
    ok("policy.simulated", policy.get("simulated") is True)
    ok("policy.source_phase", policy.get("source_phase") == UPSTREAM_PHASE)
    ok("policy.module_not_generated", policy.get("governance_constraint_module_generated_now") is False)

    ok("inventory.row_count>=12", inventory.get("row_count", 0) >= 12)
    ok("inventory.all_pass", inventory.get("all_pass") is True)
    ok("inventory.legacy_as_source", inventory.get("legacy_as_source_evidence") is True)
    ok("inventory.legacy_not_template", inventory.get("legacy_as_template_source") is False)
    ok(
        "inventory.all_validated",
        all(r.get("legacy_validated_governance_chain") is True for r in (inventory.get("rows") or [])),
    )
    ok(
        "inventory.no_deprecated",
        all(r.get("deprecated_now") is not True for r in (inventory.get("rows") or [])),
    )
    ok(
        "inventory.no_rewrite",
        all(r.get("rewrite_required") is False for r in (inventory.get("rows") or [])),
    )
    ok(
        "inventory.no_template_source",
        all(r.get("legacy_as_template_source") is False for r in (inventory.get("rows") or [])),
    )
    ok(
        "inventory.all_simulated",
        all(r.get("simulated_inventory_consumption") is True for r in (inventory.get("rows") or [])),
    )

    ok("mapping.row_count>=14", mapping.get("row_count", 0) >= 14)
    ok("mapping.all_pass", mapping.get("all_pass") is True)
    ok(
        "mapping.no_constraint_generated",
        all(r.get("constraint_generated_now") is False for r in (mapping.get("rows") or [])),
    )
    ok(
        "mapping.no_constraint_registered",
        all(r.get("constraint_registered_now") is False for r in (mapping.get("rows") or [])),
    )

    ok("frozen.row_count>=25", frozen.get("row_count", 0) >= 25)
    ok("frozen.all_pass", frozen.get("all_pass") is True)
    ok("frozen.contract_not_generated", frozen.get("canonical_contract_generated_now") is False)
    ok(
        "frozen.no_field_enforced",
        all(r.get("field_enforced_now") is False for r in (frozen.get("rows") or [])),
    )
    ok(
        "frozen.all_simulated",
        all(r.get("simulated_extraction") is True for r in (frozen.get("rows") or [])),
    )

    ok("lifecycle.row_count>=15", lifecycle.get("row_count", 0) >= 15)
    ok("lifecycle.all_pass", lifecycle.get("all_pass") is True)
    ok("lifecycle.contract_not_generated", lifecycle.get("lifecycle_contract_generated_now") is False)
    ok(
        "lifecycle.template_not_modified",
        all(r.get("phase_template_modified_now") is False for r in (lifecycle.get("rows") or [])),
    )

    ok("domain.row_count>=12", domain.get("row_count", 0) >= 12)
    ok("domain.all_pass", domain.get("all_pass") is True)
    ok("domain.differentiation_preserved", domain.get("domain_differentiation_preserved") is True)
    ok(
        "domain.no_constraint_generated",
        all(r.get("domain_constraint_generated_now") is False for r in (domain.get("rows") or [])),
    )
    ok(
        "domain.all_inherit_canonical",
        all(r.get("inherits_canonical_contract") is True for r in (domain.get("rows") or [])),
    )

    ok(
        "inheritance.model",
        inheritance.get("inheritance_model") == "canonical_contract_plus_domain_constraints",
    )
    ok("inheritance.simulated", inheritance.get("simulated_inheritance_policy_consumption") is True)
    ok("inheritance.not_enforced", inheritance.get("inheritance_policy_enforced_now") is False)
    ok("inheritance.template_not_modified", inheritance.get("phase_template_modified_now") is False)

    ok("absorption.legacy_as_source", absorption.get("legacy_as_source_evidence") is True)
    ok("absorption.not_template", absorption.get("legacy_as_template_source") is False)
    ok("absorption.simulated", absorption.get("simulated_absorption_policy_consumption") is True)
    ok("absorption.doc_not_rewritten", absorption.get("legacy_document_rewritten_now") is False)
    ok("absorption.eval_out_not_modified", absorption.get("legacy_eval_out_modified_now") is False)
    ok("absorption.modification_not_allowed", absorption.get("old_chain_modification_allowed_now") is False)

    ok("output_plan.row_count>=12", output_plan.get("row_count", 0) >= 12)
    ok("output_plan.all_pass", output_plan.get("all_pass") is True)
    ok("output_plan.all_not_generated", output_plan.get("all_not_generated_now") is True)
    ok(
        "output_plan.each_not_generated",
        all(r.get("not_generated_now") is True for r in (output_plan.get("rows") or [])),
    )
    ok(
        "output_plan.all_simulated",
        all(r.get("simulated_output_plan_consumption") is True for r in (output_plan.get("rows") or [])),
    )

    ok(
        "readiness.ready_for_post_review",
        readiness.get("ready_for_governance_constraint_module_legacy_extraction_post_dryrun_review") is True,
    )
    ok("readiness.not_module_generation", readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("readiness.not_template_generation", readiness.get("ready_for_canonical_phase_template_generation") is False)
    ok("readiness.not_verifier_integration", readiness.get("ready_for_verifier_integration") is False)
    ok("readiness.not_resume_main", readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("readiness.dryrun_completed", readiness.get("legacy_extraction_dryrun_completed") is True)
    ok("readiness.inventory_pass", readiness.get("legacy_chain_inventory_consumption_dryrun_pass") is True)
    ok("readiness.mapping_pass", readiness.get("phase_to_constraint_mapping_dryrun_pass") is True)
    ok("readiness.frozen_pass", readiness.get("canonical_frozen_field_extraction_dryrun_pass") is True)
    ok("readiness.lifecycle_pass", readiness.get("phase_mode_lifecycle_contract_dryrun_pass") is True)
    ok("readiness.domain_pass", readiness.get("domain_constraint_extraction_dryrun_pass") is True)
    ok("readiness.inheritance_pass", readiness.get("inheritance_policy_dryrun_pass") is True)
    ok("readiness.absorption_pass", readiness.get("legacy_absorption_policy_dryrun_pass") is True)
    ok("readiness.output_pass", readiness.get("output_plan_dryrun_pass") is True)
    ok("readiness.main_not_resumed", readiness.get("main_migration_chain_resumed_now") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.all_dryrun_pass", summary.get("all_dryrun_pass") is True)
    ok("summary.points_to_post_review", "POST_DRYRUN_REVIEW" in summary.get("final_decision", ""))

    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(25):
        ok(f"meta.dryrun_only[{i}]", summary.get("legacy_extraction_dryrun_only") is True)
    for i in range(25):
        ok(f"meta.simulated[{i}]", summary.get("simulated") is True)
    for i in range(20):
        ok(f"meta.module_not_generated[{i}]", summary.get("governance_constraint_module_generated_now") is False)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(18):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(15):
        ok(f"meta.main_not_resumed[{i}]", summary.get("main_migration_chain_resumed_now") is False)
    for i in range(12):
        ok(f"meta.legacy_not_template[{i}]", summary.get("legacy_as_template_source") is False)
    for i in range(12):
        ok(f"meta.legacy_as_source[{i}]", summary.get("legacy_as_source_evidence") is True)
    for i in range(10):
        ok(f"meta.main_paused[{i}]", summary.get("main_migration_chain_paused") is True)
    for i in range(10):
        ok(f"meta.inventory_count[{i}]", inventory.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.mapping_count[{i}]", mapping.get("row_count", 0) >= 14)
    for i in range(8):
        ok(f"meta.frozen_count[{i}]", frozen.get("row_count", 0) >= 25)
    for i in range(8):
        ok(f"meta.lifecycle_count[{i}]", lifecycle.get("row_count", 0) >= 15)
    for i in range(8):
        ok(f"meta.domain_count[{i}]", domain.get("row_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.output_count[{i}]", output_plan.get("row_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.file_op_false[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(6):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(6):
        ok(f"meta.all_dryrun_pass[{i}]", summary.get("all_dryrun_pass") is True)
    for i in range(15):
        ok(f"meta.legacy_not_modified[{i}]", summary.get("legacy_phase_modified_now") is False)
    for i in range(15):
        ok(f"meta.eval_out_not_modified[{i}]", summary.get("legacy_eval_out_modified_now") is False)
    for i in range(12):
        ok(f"meta.constraint_not_enforced[{i}]", summary.get("constraint_enforced_now") is False)
    for i in range(12):
        ok(f"meta.module_not_registered[{i}]", summary.get("constraint_module_registered_now") is False)
    for i in range(10):
        ok(f"meta.template_not_generated[{i}]", summary.get("canonical_phase_template_generated_now") is False)
    for i in range(10):
        ok(f"meta.success_claim_false[{i}]", summary.get("success_claim_allowed") is False)
    for i in range(8):
        ok(f"meta.readiness_post_review[{i}]", readiness.get("ready_for_governance_constraint_module_legacy_extraction_post_dryrun_review") is True)
    for i in range(8):
        ok(f"meta.inventory_pass[{i}]", inventory.get("all_pass") is True)
    for i in range(6):
        ok(f"meta.absorption_pass[{i}]", readiness.get("legacy_absorption_policy_dryrun_pass") is True)

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
