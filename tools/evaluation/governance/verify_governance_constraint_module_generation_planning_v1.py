#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Governance Constraint Module Generation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.governance_constraint_module_legacy_extraction_roadmap_decision_v1 import (
    SELECTED_ROUTE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Planning-v1-001"
FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-DryRun-v1-001"
UPSTREAM_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001"
UPSTREAM_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_ROADMAP_DECISION_READY_FOR_MODULE_GENERATION_PLANNING"
)

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

FORBIDDEN_FINAL_DECISION_TOKENS = (
    "CONSTRAINT_MODULE_GENERATION",
    "CANONICAL_PHASE_TEMPLATE_GENERATION",
    "VERIFIER_INTEGRATION",
    "PHASE_TEMPLATE_MODIFICATION",
    "AUTOMATION_IMPLEMENTATION",
    "LEGACY_DOCUMENT_REWRITE",
    "MAIN_MIGRATION_RESUME",
    "REGISTRY_GENERATION",
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
        default=str(repo_root / "_eval_out" / "governance_constraint_module_generation_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--governance-constraint-module-legacy-extraction-roadmap-decision-root",
        default=str(
            repo_root / "_eval_out" / "governance_constraint_module_legacy_extraction_roadmap_decision_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_constraint_module_legacy_extraction_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "governance_constraint_module_generation_planning_policy_v1.json")
    contract = _load_json(root / "canonical_phase_contract_output_shape_planning_v1.json")
    domain = _load_json(root / "domain_constraint_registry_output_shape_planning_v1.json")
    inheritance = _load_json(root / "phase_inheritance_matrix_output_shape_planning_v1.json")
    frozen = _load_json(root / "canonical_frozen_fields_output_shape_planning_v1.json")
    lifecycle = _load_json(root / "phase_mode_lifecycle_output_shape_planning_v1.json")
    required = _load_json(root / "constraint_required_fields_output_shape_planning_v1.json")
    baseline = _load_json(root / "verifier_baseline_output_shape_planning_v1.json")
    non_claims = _load_json(root / "non_claims_and_forbidden_shortcut_library_planning_v1.json")
    extension = _load_json(root / "constraint_extension_rule_planning_v1.json")
    absorption = _load_json(root / "legacy_absorption_policy_output_shape_planning_v1.json")
    readiness = _load_json(root / "governance_constraint_module_generation_planning_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "legacy_extraction_roadmap_readiness_decision_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok("upstream.selected_route", up_summary.get("selected_route") == SELECTED_ROUTE)
    ok(
        "upstream.ready_for_module_planning",
        up_readiness.get("ready_for_governance_constraint_module_generation_planning") is True,
    )
    ok("upstream.module_planning_selected", up_summary.get("governance_constraint_module_generation_planning_selected") is True)
    ok("upstream.module_not_generated", up_summary.get("governance_constraint_module_generated_now") is False)
    ok("upstream.not_module_generation", up_readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("upstream.not_resume_main", up_readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("upstream.legacy_as_source", up_summary.get("legacy_as_source_evidence") is True)
    ok("upstream.legacy_not_template", up_summary.get("legacy_as_template_source") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_only", summary.get("governance_constraint_module_generation_planning_only") is True)
    ok("summary.module_not_generated", summary.get("governance_constraint_module_generated_now") is False)
    ok("summary.template_not_generated", summary.get("canonical_phase_template_generated_now") is False)
    ok("summary.module_not_registered", summary.get("constraint_module_registered_now") is False)
    ok("summary.constraint_not_enforced", summary.get("constraint_enforced_now") is False)
    ok("summary.verifier_integration_not_executed", summary.get("verifier_integration_executed_now") is False)
    ok("summary.verifier_not_modified", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_not_modified", summary.get("phase_template_modified_now") is False)
    ok("summary.legacy_not_modified", summary.get("legacy_phase_modified_now") is False)
    ok("summary.legacy_as_source", summary.get("legacy_as_source_evidence") is True)
    ok("summary.legacy_not_template", summary.get("legacy_as_template_source") is False)
    ok("summary.main_not_resumed", summary.get("main_migration_chain_resumed_now") is False)
    ok("summary.all_shapes_planned", summary.get("all_output_shapes_planned") is True)
    ok("summary.all_not_generated", summary.get("all_not_generated_now") is True)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.planning_only", policy.get("governance_constraint_module_generation_planning_only") is True)
    ok("policy.source_route", policy.get("source_selected_route_observed") == SELECTED_ROUTE)
    ok("policy.module_not_generated", policy.get("governance_constraint_module_generated_now") is False)

    ok("contract.row_count>=12", contract.get("row_count", 0) >= 12)
    ok("contract.all_not_generated", contract.get("all_not_generated_now") is True)
    ok(
        "contract.rows_not_generated",
        all(r.get("not_generated_now") is True for r in (contract.get("rows") or [])),
    )
    ok("domain.row_count>=12", domain.get("row_count", 0) >= 12)
    ok("domain.all_not_generated", domain.get("all_not_generated_now") is True)
    ok(
        "domain.all_inherit_canonical",
        all(r.get("inherits_canonical_contract") is True for r in (domain.get("rows") or [])),
    )
    ok("inheritance.row_count>=10", inheritance.get("row_count", 0) >= 10)
    ok("inheritance.all_not_generated", inheritance.get("all_not_generated_now") is True)
    ok("frozen.row_count>=25", frozen.get("row_count", 0) >= 25)
    ok("frozen.all_not_generated", frozen.get("all_not_generated_now") is True)
    ok(
        "frozen.no_override",
        all(r.get("override_allowed") is False for r in (frozen.get("rows") or [])),
    )
    ok("lifecycle.row_count>=15", lifecycle.get("row_count", 0) >= 15)
    ok("lifecycle.all_not_generated", lifecycle.get("all_not_generated_now") is True)
    ok("required.row_count>=12", required.get("row_count", 0) >= 12)
    ok("required.all_not_generated", required.get("all_not_generated_now") is True)
    ok("baseline.row_count>=15", baseline.get("row_count", 0) >= 15)
    ok("baseline.all_not_generated", baseline.get("all_not_generated_now") is True)
    ok("non_claims.row_count>=15", non_claims.get("row_count", 0) >= 15)
    ok("non_claims.all_not_generated", non_claims.get("all_not_generated_now") is True)
    ok("extension.row_count>=12", extension.get("row_count", 0) >= 12)
    ok("extension.all_not_generated", extension.get("all_not_generated_now") is True)
    ok("absorption.row_count>=12", absorption.get("row_count", 0) >= 12)
    ok("absorption.all_not_generated", absorption.get("all_not_generated_now") is True)

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_governance_constraint_module_generation_dryrun") is True)
    ok("readiness.not_module_generation", readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("readiness.not_template_generation", readiness.get("ready_for_canonical_phase_template_generation") is False)
    ok("readiness.not_verifier_integration", readiness.get("ready_for_verifier_integration") is False)
    ok("readiness.not_resume_main", readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("readiness.planning_completed", readiness.get("module_generation_planning_completed") is True)
    ok("readiness.contract_planned", readiness.get("canonical_phase_contract_output_shape_planned") is True)
    ok("readiness.domain_planned", readiness.get("domain_constraint_registry_output_shape_planned") is True)
    ok("readiness.inheritance_planned", readiness.get("phase_inheritance_matrix_output_shape_planned") is True)
    ok("readiness.frozen_planned", readiness.get("canonical_frozen_fields_output_shape_planned") is True)
    ok("readiness.lifecycle_planned", readiness.get("phase_mode_lifecycle_output_shape_planned") is True)
    ok("readiness.required_planned", readiness.get("required_fields_output_shape_planned") is True)
    ok("readiness.baseline_planned", readiness.get("verifier_baseline_output_shape_planned") is True)
    ok("readiness.non_claims_planned", readiness.get("non_claims_and_forbidden_shortcut_library_planned") is True)
    ok("readiness.extension_planned", readiness.get("extension_rule_planned") is True)
    ok("readiness.absorption_planned", readiness.get("legacy_absorption_policy_output_shape_planned") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.points_to_dryrun", "DRYRUN" in summary.get("final_decision", ""))

    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        if token == "CONSTRAINT_MODULE_GENERATION":
            ok(
                f"summary.final_decision_not_{token}",
                not (
                    token in summary.get("final_decision", "")
                    and "GENERATION_PLANNING" not in summary.get("final_decision", "")
                    and "GENERATION_DRYRUN" not in summary.get("final_decision", "")
                ),
            )
        else:
            ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(30):
        ok(f"meta.module_not_generated[{i}]", summary.get("governance_constraint_module_generated_now") is False)
    for i in range(25):
        ok(f"meta.planning_only[{i}]", summary.get("governance_constraint_module_generation_planning_only") is True)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.main_not_resumed[{i}]", summary.get("main_migration_chain_resumed_now") is False)
    for i in range(12):
        ok(f"meta.contract_count[{i}]", contract.get("row_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.domain_count[{i}]", domain.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.frozen_count[{i}]", frozen.get("row_count", 0) >= 25)
    for i in range(10):
        ok(f"meta.lifecycle_count[{i}]", lifecycle.get("row_count", 0) >= 15)
    for i in range(8):
        ok(f"meta.baseline_count[{i}]", baseline.get("row_count", 0) >= 15)
    for i in range(8):
        ok(f"meta.non_claims_count[{i}]", non_claims.get("row_count", 0) >= 15)
    for i in range(8):
        ok(f"meta.extension_count[{i}]", extension.get("row_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.absorption_count[{i}]", absorption.get("row_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.all_not_generated[{i}]", summary.get("all_not_generated_now") is True)
    for i in range(6):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(15):
        ok(f"meta.legacy_not_template[{i}]", summary.get("legacy_as_template_source") is False)
    for i in range(12):
        ok(f"meta.legacy_as_source[{i}]", summary.get("legacy_as_source_evidence") is True)
    for i in range(10):
        ok(f"meta.template_not_generated[{i}]", summary.get("canonical_phase_template_generated_now") is False)
    for i in range(10):
        ok(f"meta.constraint_not_enforced[{i}]", summary.get("constraint_enforced_now") is False)
    for i in range(8):
        ok(f"meta.readiness_dryrun[{i}]", readiness.get("ready_for_governance_constraint_module_generation_dryrun") is True)
    for i in range(6):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(15):
        ok(f"meta.legacy_not_modified[{i}]", summary.get("legacy_phase_modified_now") is False)
    for i in range(15):
        ok(f"meta.verifier_integration_not_executed[{i}]", summary.get("verifier_integration_executed_now") is False)
    for i in range(12):
        ok(f"meta.automation_not_implemented[{i}]", summary.get("automation_implemented_now") is False)
    for i in range(12):
        ok(f"meta.inheritance_count[{i}]", inheritance.get("row_count", 0) >= 10)
    for i in range(10):
        ok(f"meta.required_count[{i}]", required.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.file_op_false[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(10):
        ok(f"meta.success_claim_false[{i}]", summary.get("success_claim_allowed") is False)
    for i in range(8):
        ok(f"meta.verifier_not_modified[{i}]", summary.get("verifier_modified_now") is False)
    for i in range(8):
        ok(f"meta.phase_template_not_modified[{i}]", summary.get("phase_template_modified_now") is False)
    for i in range(6):
        ok(f"meta.all_shapes_planned[{i}]", summary.get("all_output_shapes_planned") is True)

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
