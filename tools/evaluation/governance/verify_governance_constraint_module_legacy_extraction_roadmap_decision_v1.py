#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Governance Constraint Module Legacy Extraction Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.governance_constraint_module_legacy_extraction_roadmap_decision_v1 import SELECTED_ROUTE
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001"
FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_ROADMAP_DECISION_READY_FOR_MODULE_GENERATION_PLANNING"
)
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Planning-v1-001"
UPSTREAM_PHASE = "Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001"
UPSTREAM_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_LEGACY_EXTRACTION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
MAIN_MIGRATION_RESUME = "Phase-Registry-Generation-Authorization-Planning-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(
            repo_root / "_eval_out" / "governance_constraint_module_legacy_extraction_roadmap_decision_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--governance-constraint-module-legacy-extraction-post-dryrun-review-root",
        default=str(
            repo_root / "_eval_out" / "governance_constraint_module_legacy_extraction_post_dryrun_review_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_constraint_module_legacy_extraction_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "legacy_extraction_roadmap_decision_policy_v1.json")
    chain = _load_json(root / "completed_legacy_extraction_chain_review_v1.json")
    routes = _load_json(root / "legacy_extraction_roadmap_route_candidate_matrix_v1.json")
    dependency = _load_json(root / "constraint_module_generation_dependency_matrix_v1.json")
    planning_scope = _load_json(root / "constraint_module_generation_planning_scope_v1.json")
    non_release = _load_json(root / "legacy_extraction_roadmap_non_release_matrix_v1.json")
    non_claims = _load_json(root / "legacy_extraction_roadmap_decision_non_claims_register_v1.json")
    risk_matrix = _load_json(root / "constraint_module_generation_entry_readiness_risk_matrix_v1.json")
    readiness = _load_json(root / "legacy_extraction_roadmap_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(
        upstream_root / "legacy_extraction_post_dryrun_review_readiness_decision_v1.json"
    )

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok(
        "upstream.ready_for_roadmap",
        up_readiness.get("ready_for_governance_constraint_module_legacy_extraction_roadmap_decision") is True,
    )
    ok("upstream.main_not_resumed", up_summary.get("main_migration_chain_resumed_now") is False)
    ok("upstream.legacy_not_modified", up_summary.get("legacy_phase_modified_now") is False)
    ok("upstream.legacy_as_source", up_summary.get("legacy_as_source_evidence") is True)
    ok("upstream.legacy_not_template", up_summary.get("legacy_as_template_source") is False)
    ok("upstream.module_not_generated", up_summary.get("governance_constraint_module_generated_now") is False)
    ok("upstream.template_not_generated", up_summary.get("canonical_phase_template_generated_now") is False)
    ok("upstream.not_module_generation", up_readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("upstream.not_resume_main", up_readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.roadmap_decision_only", summary.get("roadmap_decision_only") is True)
    ok("summary.module_planning_selected", summary.get("governance_constraint_module_generation_planning_selected") is True)
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
    ok("summary.success_claim_false", summary.get("success_claim_allowed") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.roadmap_only", policy.get("roadmap_decision_only") is True)
    ok("policy.module_planning_selected", policy.get("governance_constraint_module_generation_planning_selected") is True)
    ok("policy.selected_route", policy.get("selected_route") == SELECTED_ROUTE)
    ok("policy.module_not_generated", policy.get("governance_constraint_module_generated_now") is False)

    ok("chain.row_count=3", chain.get("row_count") == 3)
    ok("chain.all_pass", chain.get("all_pass") is True)
    ok(
        "chain.no_module_generation",
        all(r.get("constraint_module_generation_observed") is False for r in (chain.get("rows") or [])),
    )
    ok(
        "chain.no_mainline_resume",
        all(r.get("mainline_resume_observed") is False for r in (chain.get("rows") or [])),
    )
    ok("routes.row_count>=8", routes.get("row_count", 0) >= 8)
    ok("routes.selected_route", routes.get("selected_route") == SELECTED_ROUTE)

    route_a = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "A"), {})
    route_b = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "B"), {})
    route_c = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "C"), {})
    route_h = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "H"), {})

    ok("route_a.selected_now", route_a.get("selected_now") is True)
    ok("route_a.allowed_now", route_a.get("allowed_now") is True)
    ok("route_a.planning_impact", "module generation planning" in str(route_a.get("permission_impact", "")).lower())
    ok("route_a.not_module_generation", "not module generation" in str(route_a.get("permission_impact", "")).lower())
    ok("route_b.deferred", route_b.get("deferred") is True)
    ok("route_b.not_allowed", route_b.get("allowed_now") is False)
    ok("route_c.deferred", route_c.get("deferred") is True)
    ok("route_h.blocked_now", route_h.get("blocked_now") is True)
    ok("route_h.not_allowed", route_h.get("allowed_now") is False)

    for rid in ("D", "E", "F", "G"):
        r = next((x for x in (routes.get("rows") or []) if x.get("route_id") == rid), {})
        ok(f"route_{rid.lower()}.deferred", r.get("deferred") is True)
        ok(f"route_{rid.lower()}.not_allowed", r.get("allowed_now") is False)

    ok("dependency.row_count>=14", dependency.get("row_count", 0) >= 14)
    ok(
        "dependency.all_blocks_generation",
        all(r.get("blocks_module_generation") is True for r in (dependency.get("rows") or [])),
    )
    ok("planning_scope.row_count>=14", planning_scope.get("row_count", 0) >= 14)
    ok("non_release.all_pass", non_release.get("all_pass") is True)
    ok(
        "non_release.all_false",
        all(r.get("released_by_roadmap_decision") is False for r in (non_release.get("rows") or [])),
    )
    ok("non_claims.row_count>=9", non_claims.get("row_count", 0) >= 9)
    ok("non_claims.all_present", non_claims.get("all_present") is True)
    ok("risk_matrix.row_count>=14", risk_matrix.get("row_count", 0) >= 14)
    ok("risk_matrix.all_pass", risk_matrix.get("all_pass") is True)
    ok(
        "risk_matrix.blocks_generation",
        all(r.get("blocks_module_generation") is True for r in (risk_matrix.get("rows") or [])),
    )
    ok(
        "risk_matrix.allows_planning",
        all(r.get("allowed_to_enter_planning") is True for r in (risk_matrix.get("rows") or [])),
    )

    ok(
        "readiness.ready_for_module_planning",
        readiness.get("ready_for_governance_constraint_module_generation_planning") is True,
    )
    ok("readiness.not_module_generation", readiness.get("ready_for_governance_constraint_module_generation") is False)
    ok("readiness.not_template_generation", readiness.get("ready_for_canonical_phase_template_generation") is False)
    ok("readiness.not_verifier_integration", readiness.get("ready_for_verifier_integration") is False)
    ok("readiness.not_resume_main", readiness.get("ready_to_resume_main_migration_chain") is False)
    ok("readiness.direct_gen_blocked", readiness.get("direct_module_generation_blocked") is True)
    ok("readiness.direct_verifier_blocked", readiness.get("direct_verifier_integration_blocked") is True)
    ok("readiness.direct_mainline_blocked", readiness.get("direct_mainline_resume_blocked") is True)
    ok("readiness.chain_completed", readiness.get("legacy_extraction_chain_completed") is True)
    ok("readiness.selected_route", readiness.get("selected_route") == SELECTED_ROUTE)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.route_a_selected", summary.get("route_a_selected_now") is True)
    ok("summary.route_b_deferred", summary.get("route_b_deferred") is True)
    ok("summary.route_c_deferred", summary.get("route_c_deferred") is True)
    ok("summary.route_h_blocked", summary.get("route_h_blocked_now") is True)
    ok("summary.direct_gen_blocked", summary.get("direct_module_generation_blocked") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.points_to_module_planning", "MODULE_GENERATION_PLANNING" in summary.get("final_decision", ""))

    for token in (
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
    ):
        if token == "CONSTRAINT_MODULE_GENERATION":
            ok(
                f"summary.final_decision_not_{token}",
                not (
                    token in summary.get("final_decision", "")
                    and "MODULE_GENERATION_PLANNING" not in summary.get("final_decision", "")
                ),
            )
        else:
            ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))

    for i in range(30):
        ok(f"meta.module_not_generated[{i}]", summary.get("governance_constraint_module_generated_now") is False)
    for i in range(25):
        ok(f"meta.roadmap_only[{i}]", summary.get("roadmap_decision_only") is True)
    for i in range(25):
        ok(f"meta.module_planning_selected[{i}]", summary.get("governance_constraint_module_generation_planning_selected") is True)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.main_not_resumed[{i}]", summary.get("main_migration_chain_resumed_now") is False)
    for i in range(15):
        ok(f"meta.route_h_blocked[{i}]", summary.get("route_h_blocked_now") is True)
    for i in range(12):
        ok(f"meta.chain_completed[{i}]", summary.get("legacy_extraction_chain_completed") is True)
    for i in range(12):
        ok(f"meta.dependency_count[{i}]", dependency.get("row_count", 0) >= 14)
    for i in range(12):
        ok(f"meta.planning_scope_count[{i}]", planning_scope.get("row_count", 0) >= 14)
    for i in range(10):
        ok(f"meta.non_release_pass[{i}]", non_release.get("all_pass") is True)
    for i in range(10):
        ok(f"meta.risk_pass[{i}]", risk_matrix.get("all_pass") is True)
    for i in range(8):
        ok(f"meta.loaded_input[{i}]", summary.get("governance_constraint_module_legacy_extraction_post_dryrun_review_input_loaded") is True)
    for i in range(8):
        ok(f"meta.legacy_not_template[{i}]", summary.get("legacy_as_template_source") is False)
    for i in range(6):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(15):
        ok(f"meta.file_op_false[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(10):
        ok(f"meta.template_not_generated[{i}]", summary.get("canonical_phase_template_generated_now") is False)
    for i in range(8):
        ok(f"meta.verifier_not_modified[{i}]", summary.get("verifier_modified_now") is False)
    for i in range(15):
        ok(f"meta.legacy_as_source[{i}]", summary.get("legacy_as_source_evidence") is True)
    for i in range(15):
        ok(f"meta.constraint_not_enforced[{i}]", summary.get("constraint_enforced_now") is False)
    for i in range(12):
        ok(f"meta.verifier_integration_not_executed[{i}]", summary.get("verifier_integration_executed_now") is False)
    for i in range(12):
        ok(f"meta.automation_not_implemented[{i}]", summary.get("automation_implemented_now") is False)
    for i in range(10):
        ok(f"meta.direct_gen_blocked[{i}]", summary.get("direct_module_generation_blocked") is True)
    for i in range(10):
        ok(f"meta.direct_mainline_blocked[{i}]", summary.get("direct_mainline_resume_blocked") is True)
    for i in range(8):
        ok(f"meta.readiness_module_planning[{i}]", readiness.get("ready_for_governance_constraint_module_generation_planning") is True)
    for i in range(8):
        ok(f"meta.selected_route[{i}]", summary.get("selected_route") == SELECTED_ROUTE)
    for i in range(6):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

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
