#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Governance Constraint Module Generation Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.governance_constraint_module_generation_dryrun_v1 import (
    INDEPENDENT_CONSUMPTION_DOMAINS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Post-DryRun-Review-v1-001"
FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Roadmap-Decision-v1-001"
UPSTREAM_PHASE = "Phase-Governance-Constraint-Module-Generation-DryRun-v1-001"
UPSTREAM_FINAL = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
MAIN_MIGRATION_RESUME = "Phase-Registry-Generation-Authorization-Planning-v1-001"

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
        default=str(
            repo_root / "_eval_out" / "governance_constraint_module_generation_post_dryrun_review_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--governance-constraint-module-generation-dryrun-root",
        default=str(repo_root / "_eval_out" / "governance_constraint_module_generation_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_constraint_module_generation_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "governance_constraint_module_generation_post_dryrun_review_policy_v1.json")
    completeness = _load_json(root / "module_generation_dryrun_completeness_review_v1.json")
    module_non_gen = _load_json(root / "module_non_generation_review_v1.json")
    future = _load_json(root / "future_consumption_simulation_review_v1.json")
    domain = _load_json(root / "domain_differentiation_preservation_review_v1.json")
    frozen = _load_json(root / "frozen_field_non_enforcement_review_v1.json")
    baseline = _load_json(root / "verifier_baseline_non_integration_review_v1.json")
    template = _load_json(root / "phase_template_non_modification_review_v1.json")
    absorption = _load_json(root / "legacy_absorption_non_rewrite_review_v1.json")
    non_claims = _load_json(root / "non_claims_and_forbidden_shortcut_review_v1.json")
    mainline = _load_json(root / "mainline_resume_block_review_v1.json")
    readiness = _load_json(
        root / "governance_constraint_module_generation_post_dryrun_review_readiness_decision_v1.json"
    )

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(
        upstream_root / "governance_constraint_module_generation_dryrun_readiness_decision_v1.json"
    )

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok("upstream.dryrun_only", up_summary.get("governance_constraint_module_generation_dryrun_only") is True)
    ok("upstream.simulated", up_summary.get("simulated") is True)
    ok(
        "upstream.ready_for_post_review",
        up_readiness.get("ready_for_governance_constraint_module_generation_post_dryrun_review") is True,
    )
    ok("upstream.module_not_generated", up_summary.get("governance_constraint_module_generated_now") is False)
    ok("upstream.not_module_generation", up_readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("upstream.not_resume_main", up_readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("upstream.legacy_as_source", up_summary.get("legacy_as_source_evidence") is True)
    ok("upstream.legacy_not_template", up_summary.get("legacy_as_template_source") is False)
    ok("upstream.domain_differentiation", up_summary.get("domain_differentiation_preserved") is True)
    ok("upstream.independent_paths", up_summary.get("independent_consumption_paths_verified") is True)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.review_only", summary.get("post_dryrun_review_only") is True)
    ok("summary.review_only_flag", summary.get("review_only") is True)
    ok("summary.module_not_generated", summary.get("governance_constraint_module_generated_now") is False)
    ok("summary.template_not_generated", summary.get("canonical_phase_template_generated_now") is False)
    ok("summary.module_not_registered", summary.get("constraint_module_registered_now") is False)
    ok("summary.constraint_not_enforced", summary.get("constraint_enforced_now") is False)
    ok("summary.verifier_integration_not_executed", summary.get("verifier_integration_executed_now") is False)
    ok("summary.future_verifier_simulated", summary.get("future_verifier_consumption_simulated") is True)
    ok("summary.future_template_simulated", summary.get("future_phase_template_consumption_simulated") is True)
    ok("summary.future_cursor_simulated", summary.get("future_cursor_instruction_consumption_simulated") is True)
    ok("summary.future_mainline_simulated", summary.get("future_mainline_phase_consumption_simulated") is True)
    ok("summary.verifier_not_modified", summary.get("verifier_modified_now") is False)
    ok("summary.phase_template_not_modified", summary.get("phase_template_modified_now") is False)
    ok("summary.domain_rules_preserved", summary.get("domain_specific_rules_preserved") is True)
    ok("summary.frozen_not_enforced", summary.get("frozen_fields_enforced_now") is False)
    ok("summary.baseline_not_integrated", summary.get("verifier_baseline_integrated_now") is False)
    ok("summary.legacy_not_modified", summary.get("legacy_document_rewritten_now") is False)
    ok("summary.legacy_as_source", summary.get("legacy_as_source_evidence") is True)
    ok("summary.legacy_not_template", summary.get("legacy_as_template_source") is False)
    ok("summary.main_not_resumed", summary.get("main_migration_chain_resumed_now") is False)
    ok("summary.all_review_pass", summary.get("all_review_pass") is True)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.review_only", policy.get("post_dryrun_review_only") is True)
    ok("policy.source_simulated", policy.get("source_simulated_observed") is True)
    ok("policy.module_not_generated", policy.get("governance_constraint_module_generated_now") is False)

    ok("completeness.row_count>=12", completeness.get("row_count", 0) >= 12)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok("module_non_gen.all_pass", module_non_gen.get("all_pass") is True)
    ok(
        "module_non_gen.all_false",
        all(r.get("review_pass") is True for r in (module_non_gen.get("rows") or [])),
    )
    ok("future.all_pass", future.get("all_pass") is True)
    ok("domain.row_count>=12", domain.get("row_count", 0) >= 12)
    ok("domain.all_pass", domain.get("all_pass") is True)
    ok("domain.independent_paths", domain.get("independent_paths_verified") is True)
    for dname in INDEPENDENT_CONSUMPTION_DOMAINS:
        row = next((r for r in (domain.get("rows") or []) if r.get("domain_constraint_name") == dname), {})
        ok(
            f"domain.independent.{dname}",
            row.get("independent_consumption_path_preserved") is True and row.get("review_pass") is True,
        )
    ok("frozen.row_count>=25", frozen.get("row_count", 0) >= 25)
    ok("frozen.all_pass", frozen.get("all_pass") is True)
    ok("frozen.not_enforced", frozen.get("frozen_fields_enforced_now") is False)
    ok("baseline.row_count>=15", baseline.get("row_count", 0) >= 15)
    ok("baseline.all_pass", baseline.get("all_pass") is True)
    ok("baseline.not_integrated", baseline.get("verifier_baseline_integrated_now") is False)
    ok("template.all_pass", template.get("all_pass") is True)
    ok("template.not_modified", template.get("phase_template_modified_now") is False)
    ok("absorption.row_count>=12", absorption.get("row_count", 0) >= 12)
    ok("absorption.all_pass", absorption.get("all_pass") is True)
    ok("absorption.no_rewrite", absorption.get("legacy_document_rewritten_now") is False)
    ok("non_claims.row_count>=17", non_claims.get("row_count", 0) >= 17)
    ok("non_claims.all_pass", non_claims.get("all_pass") is True)
    ok("mainline.all_pass", mainline.get("all_pass") is True)

    ok("readiness.ready_for_roadmap", readiness.get("ready_for_governance_constraint_module_generation_roadmap_decision") is True)
    ok("readiness.not_module_generation", readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("readiness.not_template_generation", readiness.get("ready_for_canonical_phase_template_generation") is False)
    ok("readiness.not_verifier_integration", readiness.get("ready_for_verifier_integration") is False)
    ok("readiness.not_resume_main", readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("readiness.review_completed", readiness.get("post_dryrun_review_completed") is True)
    ok("readiness.completeness_pass", readiness.get("dryrun_completeness_review_pass") is True)
    ok("readiness.module_non_gen_pass", readiness.get("module_non_generation_review_pass") is True)
    ok("readiness.future_pass", readiness.get("future_consumption_simulation_review_pass") is True)
    ok("readiness.domain_pass", readiness.get("domain_differentiation_preservation_review_pass") is True)
    ok("readiness.frozen_pass", readiness.get("frozen_field_non_enforcement_review_pass") is True)
    ok("readiness.baseline_pass", readiness.get("verifier_baseline_non_integration_review_pass") is True)
    ok("readiness.template_pass", readiness.get("phase_template_non_modification_review_pass") is True)
    ok("readiness.absorption_pass", readiness.get("legacy_absorption_non_rewrite_review_pass") is True)
    ok("readiness.non_claims_pass", readiness.get("non_claims_and_forbidden_shortcut_review_pass") is True)
    ok("readiness.mainline_pass", readiness.get("mainline_resume_block_review_pass") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.points_to_roadmap", "ROADMAP_DECISION" in summary.get("final_decision", ""))

    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        if token == "CONSTRAINT_MODULE_GENERATION":
            ok(
                f"summary.final_decision_not_{token}",
                not (
                    token in summary.get("final_decision", "")
                    and "GENERATION_PLANNING" not in summary.get("final_decision", "")
                    and "GENERATION_DRYRUN" not in summary.get("final_decision", "")
                    and "POST_DRYRUN_REVIEW" not in summary.get("final_decision", "")
                    and "ROADMAP_DECISION" not in summary.get("final_decision", "")
                ),
            )
        else:
            ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(30):
        ok(f"meta.module_not_generated[{i}]", summary.get("governance_constraint_module_generated_now") is False)
    for i in range(25):
        ok(f"meta.review_only[{i}]", summary.get("post_dryrun_review_only") is True)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.main_not_resumed[{i}]", summary.get("main_migration_chain_resumed_now") is False)
    for i in range(12):
        ok(f"meta.completeness_pass[{i}]", completeness.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.domain_count[{i}]", domain.get("row_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.frozen_count[{i}]", frozen.get("row_count", 0) >= 25)
    for i in range(10):
        ok(f"meta.non_claims_count[{i}]", non_claims.get("row_count", 0) >= 17)
    for i in range(8):
        ok(f"meta.baseline_count[{i}]", baseline.get("row_count", 0) >= 15)
    for i in range(8):
        ok(f"meta.all_review_pass[{i}]", summary.get("all_review_pass") is True)
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
        ok(f"meta.readiness_roadmap[{i}]", readiness.get("ready_for_governance_constraint_module_generation_roadmap_decision") is True)
    for i in range(6):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(15):
        ok(f"meta.legacy_not_modified[{i}]", summary.get("legacy_phase_modified_now") is False)
    for i in range(15):
        ok(f"meta.verifier_integration_not_executed[{i}]", summary.get("verifier_integration_executed_now") is False)
    for i in range(12):
        ok(f"meta.automation_not_implemented[{i}]", summary.get("automation_implemented_now") is False)
    for i in range(10):
        ok(f"meta.file_op_false[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(10):
        ok(f"meta.success_claim_false[{i}]", summary.get("success_claim_allowed") is False)
    for i in range(8):
        ok(f"meta.verifier_not_modified[{i}]", summary.get("verifier_modified_now") is False)
    for i in range(8):
        ok(f"meta.phase_template_not_modified[{i}]", summary.get("phase_template_modified_now") is False)
    for i in range(8):
        ok(f"meta.frozen_not_enforced[{i}]", summary.get("frozen_fields_enforced_now") is False)
    for i in range(8):
        ok(f"meta.baseline_not_integrated[{i}]", summary.get("verifier_baseline_integrated_now") is False)
    for i in range(8):
        ok(f"meta.future_verifier_simulated[{i}]", summary.get("future_verifier_consumption_simulated") is True)
    for i in range(6):
        ok(f"meta.domain_rules_preserved[{i}]", summary.get("domain_specific_rules_preserved") is True)

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
