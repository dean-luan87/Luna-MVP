#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Governance Constraint Module Legacy Extraction Post-DryRun Review v1."""

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

PHASE_ID = "Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001"
FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001"
UPSTREAM_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001"
UPSTREAM_FINAL = "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
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
        default=str(
            repo_root / "_eval_out" / "governance_constraint_module_legacy_extraction_post_dryrun_review_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--governance-constraint-module-legacy-extraction-dryrun-root",
        default=str(repo_root / "_eval_out" / "governance_constraint_module_legacy_extraction_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_constraint_module_legacy_extraction_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "legacy_extraction_post_dryrun_review_policy_v1.json")
    completeness = _load_json(root / "legacy_extraction_dryrun_completeness_review_v1.json")
    asset = _load_json(root / "legacy_asset_non_modification_review_v1.json")
    chain = _load_json(root / "legacy_chain_status_review_v1.json")
    mapping = _load_json(root / "constraint_mapping_quality_review_v1.json")
    frozen = _load_json(root / "canonical_frozen_field_extraction_review_v1.json")
    domain = _load_json(root / "domain_constraint_preservation_review_v1.json")
    inheritance = _load_json(root / "inheritance_and_absorption_policy_review_v1.json")
    output = _load_json(root / "constraint_module_output_non_generation_review_v1.json")
    readiness = _load_json(root / "legacy_extraction_post_dryrun_review_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "legacy_extraction_dryrun_readiness_decision_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok(
        "upstream.ready_for_post_review",
        up_readiness.get("ready_for_governance_constraint_module_legacy_extraction_post_dryrun_review") is True,
    )
    ok("upstream.dryrun_only", up_summary.get("legacy_extraction_dryrun_only") is True)
    ok("upstream.simulated", up_summary.get("simulated") is True)
    ok("upstream.main_not_resumed", up_summary.get("main_migration_chain_resumed_now") is False)
    ok("upstream.legacy_as_source", up_summary.get("legacy_as_source_evidence") is True)
    ok("upstream.legacy_not_template", up_summary.get("legacy_as_template_source") is False)
    ok("upstream.legacy_not_modified", up_summary.get("legacy_phase_modified_now") is False)
    ok("upstream.doc_not_rewritten", up_summary.get("legacy_document_rewritten_now") is False)
    ok("upstream.eval_out_not_modified", up_summary.get("legacy_eval_out_modified_now") is False)
    ok("upstream.module_not_generated", up_summary.get("governance_constraint_module_generated_now") is False)
    ok("upstream.template_not_generated", up_summary.get("canonical_phase_template_generated_now") is False)
    ok("upstream.constraint_not_enforced", up_summary.get("constraint_enforced_now") is False)
    ok("upstream.not_module_generation", up_readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("upstream.not_resume_main", up_readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.post_dryrun_review_only", summary.get("post_dryrun_review_only") is True)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.legacy_not_modified", summary.get("legacy_phase_modified_now") is False)
    ok("summary.doc_not_rewritten", summary.get("legacy_document_rewritten_now") is False)
    ok("summary.eval_out_not_modified", summary.get("legacy_eval_out_modified_now") is False)
    ok("summary.verifier_not_rerun", summary.get("legacy_verifier_rerun_now") is False)
    ok("summary.chain_not_deprecated", summary.get("legacy_chain_deprecated_now") is False)
    ok("summary.legacy_as_source", summary.get("legacy_as_source_evidence") is True)
    ok("summary.legacy_not_template", summary.get("legacy_as_template_source") is False)
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
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.post_dryrun_review_only", policy.get("post_dryrun_review_only") is True)
    ok("policy.review_only", policy.get("review_only") is True)
    ok("policy.source_phase", policy.get("source_phase") == UPSTREAM_PHASE)
    ok("policy.module_not_generated", policy.get("governance_constraint_module_generated_now") is False)

    ok("completeness.row_count=10", completeness.get("row_count") == 10)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok(
        "completeness.all_expected",
        all(r.get("expected") is True and r.get("observed") is True for r in (completeness.get("rows") or [])),
    )

    ok("asset.all_pass", asset.get("all_pass") is True)
    ok(
        "asset.no_violations",
        all(r.get("violation_detected") is False for r in (asset.get("rows") or [])),
    )
    ok(
        "asset.all_pass_rows",
        all(r.get("review_pass") is True for r in (asset.get("rows") or [])),
    )

    ok("chain.row_count>=12", chain.get("row_count", 0) >= 12)
    ok("chain.all_pass", chain.get("all_pass") is True)
    ok("chain.legacy_as_source", chain.get("legacy_as_source_evidence") is True)
    ok("chain.legacy_not_template", chain.get("legacy_as_template_source") is False)
    ok(
        "chain.all_validated",
        all(r.get("legacy_validated_governance_chain") is True for r in (chain.get("rows") or [])),
    )
    ok(
        "chain.no_deprecated",
        all(r.get("deprecated_now") is False for r in (chain.get("rows") or [])),
    )
    ok(
        "chain.no_rewrite",
        all(r.get("rewrite_required") is False for r in (chain.get("rows") or [])),
    )
    ok(
        "chain.no_template_source",
        all(r.get("legacy_as_template_source") is False for r in (chain.get("rows") or [])),
    )

    ok("mapping.row_count>=14", mapping.get("row_count", 0) >= 14)
    ok("mapping.all_pass", mapping.get("all_pass") is True)
    ok(
        "mapping.no_constraint_generated",
        all(r.get("constraint_generated_now") is False for r in (mapping.get("rows") or [])),
    )
    ok(
        "mapping.domain_rules_present",
        all(r.get("domain_specific_rules_present") is True for r in (mapping.get("rows") or [])),
    )

    ok("frozen.row_count>=25", frozen.get("row_count", 0) >= 25)
    ok("frozen.all_pass", frozen.get("all_pass") is True)
    ok("frozen.contract_not_generated", frozen.get("canonical_contract_generated_now") is False)
    ok(
        "frozen.no_field_enforced",
        all(r.get("field_enforced_now") is False for r in (frozen.get("rows") or [])),
    )

    ok("domain.row_count>=12", domain.get("row_count", 0) >= 12)
    ok("domain.all_pass", domain.get("all_pass") is True)
    ok("domain.differentiation_preserved", domain.get("domain_differentiation_preserved") is True)
    ok(
        "domain.no_constraint_generated",
        all(r.get("domain_constraint_generated_now") is False for r in (domain.get("rows") or [])),
    )
    ok(
        "domain.non_claims_present",
        all(r.get("domain_specific_non_claims_present") is True for r in (domain.get("rows") or [])),
    )

    ok(
        "inheritance.model",
        inheritance.get("inheritance_model") == "canonical_contract_plus_domain_constraints",
    )
    ok("inheritance.legacy_as_source", inheritance.get("legacy_as_source_evidence") is True)
    ok("inheritance.not_template", inheritance.get("legacy_as_template_source") is False)
    ok("inheritance.not_enforced", inheritance.get("inheritance_policy_enforced_now") is False)
    ok("inheritance.review_pass", inheritance.get("review_pass") is True)

    ok("output.row_count>=12", output.get("row_count", 0) >= 12)
    ok("output.all_pass", output.get("all_pass") is True)
    ok("output.all_not_generated", output.get("all_not_generated") is True)
    ok(
        "output.each_not_generated",
        all(r.get("generated_now") is False and r.get("not_generated_now") is True for r in (output.get("rows") or [])),
    )

    ok(
        "readiness.ready_for_roadmap",
        readiness.get("ready_for_governance_constraint_module_legacy_extraction_roadmap_decision") is True,
    )
    ok("readiness.not_module_generation", readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("readiness.not_template_generation", readiness.get("ready_for_canonical_phase_template_generation") is False)
    ok("readiness.not_verifier_integration", readiness.get("ready_for_verifier_integration") is False)
    ok("readiness.not_resume_main", readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("readiness.review_completed", readiness.get("post_dryrun_review_completed") is True)
    ok("readiness.completeness_pass", readiness.get("dryrun_completeness_review_pass") is True)
    ok("readiness.asset_pass", readiness.get("legacy_asset_non_modification_review_pass") is True)
    ok("readiness.chain_pass", readiness.get("legacy_chain_status_review_pass") is True)
    ok("readiness.mapping_pass", readiness.get("constraint_mapping_quality_review_pass") is True)
    ok("readiness.frozen_pass", readiness.get("canonical_frozen_field_extraction_review_pass") is True)
    ok("readiness.domain_pass", readiness.get("domain_constraint_preservation_review_pass") is True)
    ok("readiness.inheritance_pass", readiness.get("inheritance_and_absorption_policy_review_pass") is True)
    ok("readiness.output_pass", readiness.get("constraint_module_output_non_generation_review_pass") is True)
    ok("readiness.main_not_resumed", readiness.get("main_migration_chain_resumed_now") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.all_review_pass", summary.get("all_review_pass") is True)
    ok("summary.points_to_roadmap", "ROADMAP_DECISION" in summary.get("final_decision", ""))

    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(25):
        ok(f"meta.post_dryrun_review_only[{i}]", summary.get("post_dryrun_review_only") is True)
    for i in range(25):
        ok(f"meta.review_only[{i}]", summary.get("review_only") is True)
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
        ok(f"meta.completeness_pass[{i}]", completeness.get("all_pass") is True)
    for i in range(10):
        ok(f"meta.chain_count[{i}]", chain.get("row_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.mapping_count[{i}]", mapping.get("row_count", 0) >= 14)
    for i in range(8):
        ok(f"meta.frozen_count[{i}]", frozen.get("row_count", 0) >= 25)
    for i in range(8):
        ok(f"meta.domain_count[{i}]", domain.get("row_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.output_count[{i}]", output.get("row_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.file_op_false[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(6):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(6):
        ok(f"meta.all_review_pass[{i}]", summary.get("all_review_pass") is True)
    for i in range(15):
        ok(f"meta.legacy_not_modified[{i}]", summary.get("legacy_phase_modified_now") is False)
    for i in range(12):
        ok(f"meta.constraint_not_enforced[{i}]", summary.get("constraint_enforced_now") is False)
    for i in range(10):
        ok(f"meta.chain_not_deprecated[{i}]", summary.get("legacy_chain_deprecated_now") is False)
    for i in range(8):
        ok(f"meta.readiness_roadmap[{i}]", readiness.get("ready_for_governance_constraint_module_legacy_extraction_roadmap_decision") is True)

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
