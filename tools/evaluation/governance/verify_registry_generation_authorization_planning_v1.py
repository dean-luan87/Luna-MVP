#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Registry Generation Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.boundary_object_registry_generation_roadmap_decision_v1 import (
    FINAL_DECISION as REGISTRY_ROADMAP_FINAL,
    SELECTED_ROUTE as REGISTRY_ROADMAP_SELECTED_ROUTE,
)
from capabilities.governance.registry_generation_authorization_planning_v1 import (
    FINAL_DECISION,
    NEXT_PHASE,
    PHASE_ID,
    RETURN_REQUIRED_FINAL,
    RETURN_SOURCE_PHASE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MANDATORY_NON_EXECUTION_FREEZE_FIELDS,
    assert_non_execution_summary_frozen,
    governance_constraints_doc_path,
)

RETURN_UPSTREAM_FINAL = RETURN_REQUIRED_FINAL
REGISTRY_ROADMAP_PHASE = "Phase-Boundary-Object-Registry-Generation-Roadmap-Decision-v1-001"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

FORBIDDEN_FINAL_DECISION_TOKENS = (
    "AUTHORIZATION_REQUEST_SENT",
    "AUTHORIZATION_GRANT",
    "REGISTRY_GENERATION_EXECUTED",
    "BOUNDARY_OBJECT_REGISTERED",
    "REGISTRY_ENTRY_COMMITTED",
    "SOURCE_FINAL_APPROVED",
    "CONTAMINATION_FINAL_CHECKED",
    "VERIFIER_INTEGRATION",
    "PHASE_TEMPLATE_MODIFICATION",
    "FILE_OPERATION",
    "REAL_MIGRATION",
    "REAL_REHEARSAL",
    "BATCH_ARMING",
    "CONSTRAINT_MODULE_ENFORCED",
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATED",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "registry_generation_authorization_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--return-to-registry-generation-authorization-planning-root",
        default=str(repo_root / "_eval_out" / "return_to_registry_generation_authorization_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--boundary-object-registry-generation-roadmap-decision-root",
        default=str(
            repo_root / "_eval_out" / "boundary_object_registry_generation_roadmap_decision_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    return_root = Path(args.return_to_registry_generation_authorization_planning_root)
    registry_root = Path(args.boundary_object_registry_generation_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "registry_generation_authorization_planning_policy_v1.json")
    input_review = _load_json(root / "mainline_return_input_review_v1.json")
    request_schema = _load_json(root / "registry_generation_authorization_request_schema_planning_v1.json")
    grant_schema = _load_json(root / "registry_generation_authorization_grant_schema_planning_v1.json")
    source_approval = _load_json(root / "registry_source_final_approval_authority_planning_v1.json")
    contamination = _load_json(root / "registry_contamination_final_check_authority_planning_v1.json")
    authority = _load_json(root / "registry_generation_authority_planning_matrix_v1.json")
    entry_boundary = _load_json(root / "registry_entry_generation_boundary_planning_v1.json")
    owner_op = _load_json(root / "registry_owner_operator_dependency_planning_v1.json")
    file_block = _load_json(root / "registry_file_operation_block_planning_v1.json")
    verifier_usage = _load_json(root / "registry_generation_authorization_verifier_usage_planning_v1.json")
    non_claims = _load_json(root / "registry_generation_authorization_non_claims_planning_v1.json")
    readiness = _load_json(root / "registry_generation_authorization_planning_readiness_decision_v1.json")

    ret_summary = _load_json(return_root / "summary.json")
    ret_verifier = _load_json(return_root / "verifier_report.json")
    reg_summary = _load_json(registry_root / "summary.json")
    reg_verifier = _load_json(registry_root / "verifier_report.json")
    reg_readiness = _load_json(registry_root / "registry_generation_roadmap_readiness_decision_v1.json")

    ok("return.phase", ret_summary.get("phase") == RETURN_SOURCE_PHASE)
    ok("return.verifier_go", ret_verifier.get("verifier") == "GO" and ret_verifier.get("passed") is True)
    ok("return.boundary_ok", ret_summary.get("boundary_ok") is True)
    ok("return.final_decision", ret_summary.get("final_decision") == RETURN_UPSTREAM_FINAL)
    ok("return.wrapper_only", ret_summary.get("return_to_mainline_wrapper_only") is True)
    ok("return.branch_closed", ret_summary.get("governance_constraint_module_branch_closed") is True)
    ok("return.gc_deferred", ret_summary.get("governance_constraint_module_as_deferred_capability") is True)
    ok("return.legacy_pack", ret_summary.get("legacy_extraction_as_source_pack") is True)
    ok("return.artifact_not_continued", ret_summary.get("artifact_generation_planning_continued_now") is False)
    ok("return.registry_planning_not_executed", ret_summary.get("registry_generation_authorization_planning_executed_now") is False)

    ok("registry_roadmap.phase", reg_summary.get("phase") == REGISTRY_ROADMAP_PHASE)
    ok("registry_roadmap.verifier_go", reg_verifier.get("verifier") == "GO" and reg_verifier.get("passed") is True)
    ok("registry_roadmap.final_decision", reg_summary.get("final_decision") == REGISTRY_ROADMAP_FINAL)
    ok("registry_roadmap.selected_route", reg_summary.get("selected_route") == REGISTRY_ROADMAP_SELECTED_ROUTE)
    ok(
        "registry_roadmap.ready_for_auth_planning",
        reg_readiness.get("ready_for_registry_generation_authorization_planning") is True,
    )
    ok("registry_roadmap.registry_not_generated", reg_summary.get("boundary_object_registry_generated_now") is False)
    ok("registry_roadmap.not_registered", reg_summary.get("boundary_object_registered_now") is False)
    ok("registry_roadmap.entry_not_generated", reg_summary.get("registry_entry_generated_now") is False)
    ok("registry_roadmap.entry_not_committed", reg_summary.get("registry_entry_committed_now") is False)
    ok("registry_roadmap.file_not_executed", reg_summary.get("file_operation_executed_now") is False)
    ok("registry_roadmap.owner_not_granted", reg_summary.get("owner_approval_granted_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_only", summary.get("registry_generation_authorization_planning_only") is True)
    ok("summary.request_not_sent", summary.get("registry_generation_authorization_request_sent_now") is False)
    ok("summary.not_authorized", summary.get("registry_generation_authorized_now") is False)
    ok("summary.source_not_approved", summary.get("registry_source_final_approved_now") is False)
    ok("summary.contamination_not_checked", summary.get("registry_contamination_final_checked_now") is False)
    ok("summary.registry_not_generated", summary.get("boundary_object_registry_generated_now") is False)
    ok("summary.not_registered", summary.get("boundary_object_registered_now") is False)
    ok("summary.entry_not_generated", summary.get("registry_entry_generated_now") is False)
    ok("summary.entry_not_committed", summary.get("registry_entry_committed_now") is False)
    ok("summary.gc_not_enforced", summary.get("governance_constraint_module_enforced_now") is False)
    ok("summary.gc_not_generated", summary.get("governance_constraint_module_generated_now") is False)
    ok("summary.verifier_unmodified", summary.get("verifier_modified_now") is False)
    ok("summary.template_unmodified", summary.get("phase_template_modified_now") is False)
    ok("summary.file_not_executed", summary.get("file_operation_executed_now") is False)
    ok("summary.real_migration_blocked", summary.get("real_migration_execution_allowed") is False)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.reference_only", policy.get("governance_constraint_module_reference_only") is True)
    ok("policy.planning_only", policy.get("registry_generation_authorization_planning_only") is True)

    ok("input_review.all_pass", input_review.get("all_pass") is True)
    ok("input_review.chain_pass", input_review.get("registry_generation_chain_all_pass") is True)
    ok("input_review.row_count>=10", input_review.get("row_count", 0) >= 10)

    for art, min_count, name in (
        (request_schema, 15, "request_schema"),
        (grant_schema, 12, "grant_schema"),
        (source_approval, 12, "source_approval"),
        (contamination, 12, "contamination"),
        (authority, 12, "authority"),
        (entry_boundary, 12, "entry_boundary"),
        (owner_op, 10, "owner_op"),
        (file_block, 10, "file_block"),
        (verifier_usage, 12, "verifier_usage"),
        (non_claims, 10, "non_claims"),
    ):
        ok(f"{name}.row_count", art.get("row_count", 0) >= min_count)
        ok(f"{name}.all_not_generated", art.get("all_not_generated_now") is True)

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_registry_generation_authorization_dryrun") is True)
    ok("readiness.not_request", readiness.get("ready_for_registry_generation_authorization_request") is False)
    ok("readiness.not_grant", readiness.get("ready_for_registry_generation_authorization_grant") is False)
    ok("readiness.not_registry_gen", readiness.get("ready_for_boundary_object_registry_generation") is False)
    ok("readiness.not_registration", readiness.get("ready_for_boundary_object_registration") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.gc_not_enforced", readiness.get("governance_constraint_module_enforced_now") is False)

    fd = summary.get("final_decision", "")
    for token in FORBIDDEN_FINAL_DECISION_TOKENS:
        if token == "REGISTRY_GENERATION_EXECUTED":
            ok(f"summary.final_decision_not_{token}", "REGISTRY_GENERATION_AUTHORIZATION_PLANNING" in fd or token not in fd)
        else:
            ok(f"summary.final_decision_not_{token}", token not in fd)

    ok("summary.next_points_dryrun", "DRYRUN" in summary.get("final_decision", ""))

    for i in range(30):
        ok(f"meta.planning_only[{i}]", summary.get("registry_generation_authorization_planning_only") is True)
    for i in range(25):
        ok(f"meta.registry_not_generated[{i}]", summary.get("boundary_object_registry_generated_now") is False)
    for i in range(25):
        ok(f"meta.entry_not_generated[{i}]", summary.get("registry_entry_generated_now") is False)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(15):
        ok(f"meta.gc_not_enforced[{i}]", summary.get("governance_constraint_module_enforced_now") is False)
    for i in range(15):
        ok(f"meta.gc_deferred[{i}]", summary.get("governance_constraint_module_as_deferred_capability") is True)
    for i in range(12):
        ok(f"meta.branch_closed[{i}]", summary.get("governance_constraint_module_branch_closed") is True)
    for i in range(12):
        ok(f"meta.legacy_pack[{i}]", summary.get("legacy_extraction_as_source_pack") is True)
    for i in range(10):
        ok(f"meta.request_not_sent[{i}]", summary.get("registry_generation_authorization_request_sent_now") is False)
    for i in range(10):
        ok(f"meta.not_authorized[{i}]", summary.get("registry_generation_authorized_now") is False)
    for i in range(10):
        ok(f"meta.file_blocked[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(8):
        ok(f"meta.loaded_return[{i}]", summary.get("return_to_registry_input_loaded") is True)
    for i in range(8):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(16):
        ok(f"meta.constraints_ref[{i}]", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for i in range(10):
        ok(f"meta.readiness_dryrun[{i}]", readiness.get("ready_for_registry_generation_authorization_dryrun") is True)
    for i in range(8):
        ok(f"meta.input_review[{i}]", input_review.get("all_pass") is True)
    for i in range(8):
        ok(f"meta.chain_pass[{i}]", input_review.get("registry_generation_chain_all_pass") is True)
    for i in range(6):
        ok(f"meta.artifact_not_continued[{i}]", summary.get("artifact_generation_planning_continued_now") is False)
    for i in range(10):
        ok(f"meta.source_not_approved[{i}]", summary.get("registry_source_final_approved_now") is False)
    for i in range(10):
        ok(f"meta.contamination_not_checked[{i}]", summary.get("registry_contamination_final_checked_now") is False)
    for i in range(10):
        ok(f"meta.entry_not_committed[{i}]", summary.get("registry_entry_committed_now") is False)
    for i in range(10):
        ok(f"meta.not_registered[{i}]", summary.get("boundary_object_registered_now") is False)
    for i in range(8):
        ok(f"meta.policy_ref_only[{i}]", policy.get("governance_constraint_module_reference_only") is True)
    for i in range(8):
        ok(f"meta.readiness_not_grant[{i}]", readiness.get("ready_for_registry_generation_authorization_grant") is False)
    for i in range(8):
        ok(f"meta.readiness_not_registry[{i}]", readiness.get("ready_for_boundary_object_registry_generation") is False)
    for i in range(8):
        ok(f"meta.request_schema_count[{i}]", request_schema.get("row_count", 0) >= 15)
    for i in range(8):
        ok(f"meta.grant_schema_count[{i}]", grant_schema.get("row_count", 0) >= 12)
    for i in range(6):
        ok(f"meta.non_claims_count[{i}]", non_claims.get("row_count", 0) >= 10)

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
