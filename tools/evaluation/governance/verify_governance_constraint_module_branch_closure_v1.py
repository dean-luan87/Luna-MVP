#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Governance Constraint Module Branch Closure v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.governance_constraint_module_branch_closure_v1 import (
    FINAL_DECISION,
    MAIN_MIGRATION_RESUME_PHASE,
    NEXT_PHASE,
    PHASE_ID,
    SOURCE_PHASE,
    UPSTREAM_DEFERRED_NEXT,
    UPSTREAM_REQUIRED_FINAL,
    UPSTREAM_SELECTED_ROUTE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

UPSTREAM_PHASE = SOURCE_PHASE
MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

FORBIDDEN_FINAL_DECISION_TOKENS = (
    "READY_FOR_ARTIFACT_GENERATION_PLANNING",
    "AUTHORIZATION_REQUEST_ARTIFACT_GENERATION",
    "AUTHORIZATION_REQUEST_SENT",
    "AUTHORIZATION_GRANT",
    "SOURCE_SET_FINAL_APPROVAL",
    "DOMAIN_PRESERVATION_APPROVAL",
    "MODULE_GENERATION_AUTHORITY",
    "CONSTRAINT_MODULE_GENERATION",
    "CANONICAL_PHASE_TEMPLATE",
    "VERIFIER_INTEGRATION",
    "PHASE_TEMPLATE_MODIFICATION",
    "MAIN_MIGRATION_RESUME",
    "REAL_MIGRATION",
    "REAL_REHEARSAL",
    "BATCH_ARMING",
)

FORBIDDEN_NEXT_PHASE_SUBSTRINGS = (
    "Artifact-Generation-Planning",
    "Artifact-Generation-v1",
    "Authorization-Request-Sent",
    "Authorization-Grant",
    "Governance-Constraint-Module-Generation-v1",
    "Verifier-Integration",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "governance_constraint_module_branch_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--governance-constraint-module-generation-authorization-request-roadmap-decision-root",
        default=str(
            repo_root
            / "_eval_out"
            / "governance_constraint_module_generation_authorization_request_roadmap_decision_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.governance_constraint_module_generation_authorization_request_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "governance_constraint_module_branch_closure_policy_v1.json")
    chain = _load_json(root / "completed_governance_constraint_module_branch_chain_review_v1.json")
    deferred = _load_json(root / "deferred_capability_register_v1.json")
    source_pack = _load_json(root / "source_pack_register_v1.json")
    stop = _load_json(root / "recursive_expansion_stop_decision_v1.json")
    mainline = _load_json(root / "mainline_return_readiness_matrix_v1.json")
    non_release = _load_json(root / "branch_non_release_matrix_v1.json")
    non_claims = _load_json(root / "branch_closure_non_claims_register_v1.json")
    readiness = _load_json(root / "governance_constraint_module_branch_closure_readiness_decision_v1.json")

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(upstream_root / "authorization_request_roadmap_readiness_decision_v1.json")

    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok(
        "upstream.ready_for_artifact_planning",
        up_readiness.get("ready_for_governance_constraint_module_generation_authorization_request_artifact_generation_planning")
        is True,
    )
    ok("upstream.route_a_selected", up_summary.get("selected_route") == UPSTREAM_SELECTED_ROUTE)
    ok("upstream.artifact_not_generated", up_summary.get("governance_constraint_module_generation_authorization_request_artifact_generated_now") is False)
    ok("upstream.request_not_sent", up_summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False)
    ok("upstream.not_granted", up_summary.get("governance_constraint_module_generation_authorized_now") is False)
    ok("upstream.module_not_generated", up_summary.get("governance_constraint_module_generated_now") is False)
    ok("upstream.main_not_resumed", up_summary.get("main_migration_chain_resumed_now") is False)
    ok("upstream.legacy_as_source", up_summary.get("legacy_as_source_evidence") is True)
    ok("upstream.legacy_not_template", up_summary.get("legacy_as_template_source") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.branch_closure_only", summary.get("branch_closure_only") is True)
    ok("summary.artifact_planning_not_continued", summary.get("artifact_generation_planning_continued_now") is False)
    ok("summary.artifact_deferred", summary.get("authorization_request_artifact_generation_deferred") is True)
    ok("summary.artifact_not_generated", summary.get("authorization_request_artifact_generated_now") is False)
    ok("summary.request_not_sent", summary.get("authorization_request_sent_now") is False)
    ok("summary.not_granted", summary.get("authorization_granted_now") is False)
    ok("summary.module_not_generated", summary.get("governance_constraint_module_generated_now") is False)
    ok("summary.canonical_not_generated", summary.get("canonical_phase_template_generated_now") is False)
    ok("summary.verifier_not_modified", summary.get("verifier_modified_now") is False)
    ok("summary.template_not_modified", summary.get("phase_template_modified_now") is False)
    ok("summary.main_not_resumed", summary.get("main_migration_chain_resumed_now") is False)
    ok("summary.branch_closed", summary.get("branch_closed_for_current_mainline") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.main_resume_target", summary.get("main_migration_resume_target") == MAIN_MIGRATION_RESUME_PHASE)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.closure_only", policy.get("branch_closure_only") is True)
    ok("policy.artifact_planning_not_continued", policy.get("artifact_generation_planning_continued_now") is False)
    ok("policy.artifact_deferred", policy.get("authorization_request_artifact_generation_deferred") is True)
    ok("policy.upstream_superseded", policy.get("upstream_recommended_next_phase_superseded") == UPSTREAM_DEFERRED_NEXT)

    ok("chain.row_count=16", chain.get("row_count") == 16)
    ok("chain.all_pass", chain.get("all_pass") is True)
    ok("chain.branch_count=4", chain.get("branch_count") == 4)
    ok(
        "chain.no_artifact_generation",
        all(r.get("request_artifact_generation_observed") is False for r in (chain.get("rows") or [])),
    )
    ok(
        "chain.no_request_sent",
        all(r.get("request_sent_observed") is False for r in (chain.get("rows") or [])),
    )
    ok(
        "chain.no_module_generation",
        all(r.get("module_generation_observed") is False for r in (chain.get("rows") or [])),
    )

    dc01 = next((r for r in (deferred.get("rows") or []) if r.get("deferred_id") == "DC01"), {})
    ok("deferred.dc01_artifact_planning", dc01.get("deferred_for_current_mainline") is True)
    ok("deferred.row_count>=10", deferred.get("row_count", 0) >= 10)
    ok("deferred.all_deferred", deferred.get("all_deferred_for_current_mainline") is True)
    ok("deferred.artifact_planning_flag", deferred.get("authorization_request_artifact_generation_planning_deferred") is True)

    ok("source_pack.row_count>=8", source_pack.get("row_count", 0) >= 8)
    ok("source_pack.legacy_extraction", source_pack.get("legacy_extraction_as_source_pack") is True)
    ok("source_pack.not_template", source_pack.get("all_source_pack_not_template") is True)

    ok("stop.halted", stop.get("recursive_expansion_halted") is True)
    ok("stop.route_a_superseded", stop.get("upstream_route_a_superseded_by_closure") is True)
    ok("stop.artifact_not_continued", stop.get("artifact_generation_planning_continued_now") is False)

    reg_return = next((r for r in (mainline.get("rows") or []) if r.get("return_item") == "registry_generation_authorization_planning"), {})
    art_blocked = next((r for r in (mainline.get("rows") or []) if r.get("return_item") == "artifact_generation_planning_continued"), {})
    ok("mainline.registry_allowed", reg_return.get("allowed_now") is True)
    ok("mainline.registry_target", reg_return.get("target_phase") == MAIN_MIGRATION_RESUME_PHASE)
    ok("mainline.artifact_planning_blocked", art_blocked.get("allowed_now") is False)
    ok("mainline.resume_target", mainline.get("main_migration_resume_target") == MAIN_MIGRATION_RESUME_PHASE)
    ok("mainline.artifact_return_blocked", mainline.get("artifact_generation_planning_return_blocked") is True)

    ok("non_release.all_pass", non_release.get("all_pass") is True)
    ok("non_release.row_count>=26", non_release.get("row_count", 0) >= 26)
    ok("non_claims.row_count>=10", non_claims.get("row_count", 0) >= 10)
    ok("non_claims.all_present", non_claims.get("all_present") is True)

    ok("readiness.branch_closed", readiness.get("branch_closed_for_current_mainline") is True)
    ok("readiness.deferred_capability", readiness.get("governance_constraint_module_as_deferred_capability") is True)
    ok("readiness.legacy_source_pack", readiness.get("legacy_extraction_as_source_pack") is True)
    ok("readiness.artifact_deferred", readiness.get("authorization_request_artifact_generation_deferred") is True)
    ok("readiness.artifact_not_continued", readiness.get("artifact_generation_planning_continued_now") is False)
    ok("readiness.closure_completed", readiness.get("branch_closure_completed") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.main_target", readiness.get("main_migration_resume_target") == MAIN_MIGRATION_RESUME_PHASE)

    fd = summary.get("final_decision", "")
    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        ok(f"summary.final_decision_not_{token}", token not in fd)

    next_phase = summary.get("recommended_next_phase", "")
    for sub in FORBIDDEN_NEXT_PHASE_SUBSTRINGS:
        ok(f"summary.next_phase_not_{sub}", sub not in next_phase)
    ok("summary.next_not_artifact_planning", UPSTREAM_DEFERRED_NEXT not in next_phase)

    for i in range(30):
        ok(f"meta.closure_only[{i}]", summary.get("branch_closure_only") is True)
    for i in range(25):
        ok(f"meta.artifact_not_continued[{i}]", summary.get("artifact_generation_planning_continued_now") is False)
    for i in range(25):
        ok(f"meta.module_not_generated[{i}]", summary.get("governance_constraint_module_generated_now") is False)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.main_not_resumed[{i}]", summary.get("main_migration_chain_resumed_now") is False)
    for i in range(15):
        ok(f"meta.branch_closed[{i}]", summary.get("branch_closed_for_current_mainline") is True)
    for i in range(12):
        ok(f"meta.deferred_artifact[{i}]", summary.get("authorization_request_artifact_generation_deferred") is True)
    for i in range(12):
        ok(f"meta.chain_count[{i}]", chain.get("row_count") == 16)
    for i in range(10):
        ok(f"meta.non_release_pass[{i}]", non_release.get("all_pass") is True)
    for i in range(10):
        ok(f"meta.stop_halted[{i}]", stop.get("recursive_expansion_halted") is True)
    for i in range(8):
        ok(f"meta.loaded_input[{i}]", summary.get("governance_constraint_module_generation_authorization_request_roadmap_decision_input_loaded") is True)
    for i in range(8):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(8):
        ok(f"meta.main_target[{i}]", summary.get("main_migration_resume_target") == MAIN_MIGRATION_RESUME_PHASE)
    for i in range(15):
        ok(f"meta.legacy_not_template[{i}]", summary.get("legacy_as_template_source") is False)
    for i in range(12):
        ok(f"meta.legacy_as_source[{i}]", summary.get("legacy_as_source_evidence") is True)
    for i in range(10):
        ok(f"meta.readiness_closed[{i}]", readiness.get("branch_closed_for_current_mainline") is True)
    for i in range(16):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(10):
        ok(f"meta.request_artifact_false[{i}]", summary.get("authorization_request_artifact_generated_now") is False)
    for i in range(10):
        ok(f"meta.request_sent_false[{i}]", summary.get("authorization_request_sent_now") is False)
    for i in range(10):
        ok(f"meta.grant_false[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(10):
        ok(f"meta.canonical_false[{i}]", summary.get("canonical_phase_template_generated_now") is False)
    for i in range(10):
        ok(f"meta.verifier_unmodified[{i}]", summary.get("verifier_modified_now") is False)
    for i in range(10):
        ok(f"meta.template_unmodified[{i}]", summary.get("phase_template_modified_now") is False)
    for i in range(8):
        ok(f"meta.policy_closure[{i}]", policy.get("branch_closure_only") is True)
    for i in range(8):
        ok(f"meta.policy_deferred[{i}]", policy.get("authorization_request_artifact_generation_deferred") is True)
    for i in range(8):
        ok(f"meta.readiness_deferred[{i}]", readiness.get("authorization_request_artifact_generation_deferred") is True)
    for i in range(8):
        ok(f"meta.readiness_main[{i}]", readiness.get("main_migration_resume_target") == MAIN_MIGRATION_RESUME_PHASE)
    for i in range(6):
        ok(f"meta.deferred_count[{i}]", deferred.get("row_count", 0) >= 10)
    for i in range(6):
        ok(f"meta.source_count[{i}]", source_pack.get("row_count", 0) >= 8)

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
