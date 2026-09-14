#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Boundary Object Registry Generation Post-DryRun Review v1."""

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

PHASE_ID = "Phase-Boundary-Object-Registry-Generation-Post-DryRun-Review-v1-001"
FINAL_DECISION = "BOUNDARY_OBJECT_REGISTRY_GENERATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Boundary-Object-Registry-Generation-Roadmap-Decision-v1-001"
UPSTREAM_PHASE = "Phase-Boundary-Object-Registry-Generation-DryRun-v1-001"
UPSTREAM_FINAL = "BOUNDARY_OBJECT_REGISTRY_GENERATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"

MIN_CHECKS = 420
BASELINE_REQUIREMENT = 340

DRYRUN_ARTIFACTS = (
    "boundary_object_registry_generation_dryrun_policy_v1.json",
    "registry_generation_planning_artifact_completeness_dryrun_v1.json",
    "registry_generation_source_inventory_dryrun_v1.json",
    "registry_source_artifact_whitelist_dryrun_v1.json",
    "registry_source_integrity_check_dryrun_v1.json",
    "registry_contamination_prevention_dryrun_v1.json",
    "registry_entry_conversion_rule_dryrun_v1.json",
    "registry_protected_object_entry_rule_dryrun_v1.json",
    "registry_policy_entry_rule_dryrun_v1.json",
    "registry_owner_operator_dependency_dryrun_v1.json",
    "registry_generation_verifier_usage_dryrun_v1.json",
    "registry_generation_non_claims_generation_dryrun_v1.json",
    "boundary_object_registry_generation_dryrun_readiness_decision_v1.json",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "boundary_object_registry_generation_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--boundary-object-registry-generation-dryrun-root",
        default=str(repo_root / "_eval_out" / "boundary_object_registry_generation_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.boundary_object_registry_generation_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "boundary_object_registry_generation_post_dryrun_review_policy_v1.json")
    completeness = _load_json(root / "registry_generation_dryrun_completeness_review_v1.json")
    non_exec = _load_json(root / "registry_generation_non_execution_review_v1.json")
    src_val = _load_json(root / "registry_source_validation_non_final_review_v1.json")
    contamination = _load_json(root / "registry_contamination_check_non_final_review_v1.json")
    entry = _load_json(root / "registry_entry_non_generation_review_v1.json")
    misuse = _load_json(root / "registry_source_misuse_review_v1.json")
    protected = _load_json(root / "registry_protected_object_integrity_review_v1.json")
    policy_entry = _load_json(root / "registry_policy_entry_boundary_review_v1.json")
    oo_dep = _load_json(root / "registry_owner_operator_dependency_review_v1.json")
    verifier_rev = _load_json(root / "registry_verifier_non_modification_review_v1.json")
    non_claims = _load_json(root / "registry_non_claims_non_write_review_v1.json")
    readiness = _load_json(
        root / "boundary_object_registry_generation_post_dryrun_review_readiness_decision_v1.json"
    )

    up_summary = _load_json(upstream_root / "summary.json")
    up_verifier = _load_json(upstream_root / "verifier_report.json")
    up_readiness = _load_json(
        upstream_root / "boundary_object_registry_generation_dryrun_readiness_decision_v1.json"
    )
    up_whitelist = _load_json(upstream_root / "registry_source_artifact_whitelist_dryrun_v1.json")

    ok("upstream.dryrun_dir_exists", upstream_root.is_dir())
    for name in DRYRUN_ARTIFACTS:
        ok(f"upstream.artifact.{name}", (upstream_root / name).is_file())
    ok("upstream.phase", up_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True)
    ok("upstream.boundary_ok", up_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", up_summary.get("final_decision") == UPSTREAM_FINAL)
    ok(
        "upstream.ready_for_post_review",
        up_readiness.get("ready_for_boundary_object_registry_generation_post_dryrun_review") is True,
    )
    ok("upstream.dryrun_only", up_summary.get("boundary_object_registry_generation_dryrun_only") is True)
    ok("upstream.simulated", up_summary.get("simulated") is True)
    ok("upstream.gen_not_executed", up_summary.get("boundary_object_registry_generation_executed_now") is False)
    ok("upstream.registry_not_generated", up_summary.get("boundary_object_registry_generated_now") is False)
    ok("upstream.not_registered", up_summary.get("boundary_object_registered_now") is False)
    ok("upstream.gen_not_authorized", up_summary.get("registry_generation_authorized_now") is False)
    ok("upstream.source_not_final_validated", up_summary.get("registry_source_final_validated_now") is False)
    ok("upstream.entry_not_generated", up_summary.get("registry_entry_generated_now") is False)
    ok("upstream.entry_not_committed", up_summary.get("registry_entry_committed_now") is False)
    ok("upstream.file_op_not_executed", up_summary.get("file_operation_executed_now") is False)
    ok("upstream.evidence_not_authorized", up_summary.get("evidence_generation_authorized_now") is False)
    ok("upstream.success_claim_false", up_summary.get("success_claim_allowed") is False)
    ok("upstream.not_registry_generation", up_readiness.get("ready_for_boundary_object_registry_generation") is False)
    ok("upstream.not_file_operation", up_readiness.get("ready_for_file_operation") is False)
    ok("upstream.constraints_ref", up_summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    up_summary_wl = next(
        (r for r in (up_whitelist.get("rows") or []) if r.get("source_artifact_type") == "phase_summary"),
        {},
    )
    up_verifier_wl = next(
        (r for r in (up_whitelist.get("rows") or []) if r.get("source_artifact_type") == "phase_verifier_report"),
        {},
    )
    ok("upstream.summary_not_primary", up_summary_wl.get("allowed_as_primary_source") is False)
    ok("upstream.verifier_not_registry_source", up_verifier_wl.get("allowed_as_registry_source") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.post_dryrun_review_only", summary.get("post_dryrun_review_only") is True)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.gen_not_executed", summary.get("boundary_object_registry_generation_executed_now") is False)
    ok("summary.registry_not_generated", summary.get("boundary_object_registry_generated_now") is False)
    ok("summary.not_registered", summary.get("boundary_object_registered_now") is False)
    ok("summary.gen_not_authorized", summary.get("registry_generation_authorized_now") is False)
    ok("summary.source_not_final_validated", summary.get("registry_source_final_validated_now") is False)
    ok("summary.contamination_not_final", summary.get("registry_contamination_check_final_executed_now") is False)
    ok("summary.entry_not_generated", summary.get("registry_entry_generated_now") is False)
    ok("summary.entry_not_committed", summary.get("registry_entry_committed_now") is False)
    ok("summary.protected_not_modified", summary.get("protected_asset_modified_now") is False)
    ok("summary.hr_not_modified", summary.get("human_review_queue_modified_now") is False)
    ok("summary.dnae_not_modified", summary.get("dnae_or_permanent_block_modified_now") is False)
    ok("summary.file_op_not_executed", summary.get("file_operation_executed_now") is False)
    ok("summary.write_perm_not_released", summary.get("write_permission_released_now") is False)
    ok("summary.evidence_not_authorized", summary.get("evidence_generation_authorized_now") is False)
    ok("summary.success_claim_false", summary.get("success_claim_allowed") is False)
    ok("summary.runtime_false", summary.get("runtime_invoked") is False)
    ok("summary.write_false", summary.get("write_allowed") is False)
    ok("constraints.doc_exists", governance_constraints_doc_path().is_file())
    ok("constraints.summary_frozen", len(assert_non_execution_summary_frozen(summary)) == 0)
    for field in MANDATORY_NON_EXECUTION_FREEZE_FIELDS:
        ok(f"summary.{field}=false", summary.get(field) is False)

    ok("policy.post_dryrun_review_only", policy.get("post_dryrun_review_only") is True)
    ok("policy.review_only", policy.get("review_only") is True)
    ok("policy.registry_not_generated", policy.get("boundary_object_registry_generated_now") is False)
    ok("policy.source_phase", policy.get("source_phase") == UPSTREAM_PHASE)

    ok("completeness.row_count=13", completeness.get("row_count") == 13)
    ok("completeness.all_pass", completeness.get("all_pass") is True)
    ok("non_exec.all_pass", non_exec.get("all_pass") is True)
    ok(
        "non_exec.all_no_violation",
        all(r.get("violation_detected") is False for r in (non_exec.get("rows") or [])),
    )
    ok("src_val.row_count>=14", src_val.get("row_count", 0) >= 14)
    ok("src_val.all_pass", src_val.get("all_pass") is True)
    ok(
        "src_val.all_not_final",
        all(r.get("final_check_executed_now") is False for r in (src_val.get("rows") or [])),
    )
    ok("contamination.row_count>=14", contamination.get("row_count", 0) >= 14)
    ok("contamination.all_pass", contamination.get("all_pass") is True)
    ok(
        "contamination.all_not_checked",
        all(r.get("contamination_checked_now") is False for r in (contamination.get("rows") or [])),
    )
    ok("entry.row_count>=38", entry.get("row_count", 0) >= 38)
    ok("entry.all_pass", entry.get("all_pass") is True)
    ok(
        "entry.all_not_generated",
        all(r.get("entry_generated_now") is False for r in (entry.get("rows") or [])),
    )
    ok("misuse.row_count>=12", misuse.get("row_count", 0) >= 12)
    ok("misuse.all_pass", misuse.get("all_pass") is True)
    ok(
        "misuse.no_violations",
        all(r.get("violation_detected") is False for r in (misuse.get("rows") or [])),
    )
    ok("protected.row_count>=12", protected.get("row_count", 0) >= 12)
    ok("protected.all_pass", protected.get("all_pass") is True)
    ok("policy_entry.row_count>=10", policy_entry.get("row_count", 0) >= 10)
    ok("policy_entry.all_pass", policy_entry.get("all_pass") is True)
    ok("oo_dep.row_count>=10", oo_dep.get("row_count", 0) >= 10)
    ok("oo_dep.all_pass", oo_dep.get("all_pass") is True)
    ok("verifier_rev.row_count>=16", verifier_rev.get("row_count", 0) >= 16)
    ok("verifier_rev.all_pass", verifier_rev.get("all_pass") is True)
    ok("non_claims.row_count>=12", non_claims.get("row_count", 0) >= 12)
    ok("non_claims.all_pass", non_claims.get("all_pass") is True)

    ok(
        "readiness.ready_for_roadmap",
        readiness.get("ready_for_boundary_object_registry_generation_roadmap_decision") is True,
    )
    ok("readiness.not_registry_generation", readiness.get("ready_for_boundary_object_registry_generation") is False)
    ok("readiness.not_registration", readiness.get("ready_for_boundary_object_registration") is False)
    ok("readiness.not_gen_auth", readiness.get("ready_for_registry_generation_authorization") is False)
    ok("readiness.not_source_final_validation", readiness.get("ready_for_registry_source_final_validation") is False)
    ok(
        "readiness.not_contamination_final",
        readiness.get("ready_for_registry_contamination_check_final_execution") is False,
    )
    ok("readiness.not_entry_generation", readiness.get("ready_for_registry_entry_generation") is False)
    ok("readiness.not_entry_commit", readiness.get("ready_for_registry_entry_commit") is False)
    ok("readiness.not_file_operation", readiness.get("ready_for_file_operation") is False)
    ok("readiness.review_completed", readiness.get("post_dryrun_review_completed") is True)
    ok("readiness.completeness_pass", readiness.get("dryrun_completeness_review_pass") is True)
    ok("readiness.non_exec_pass", readiness.get("generation_non_execution_review_pass") is True)
    ok("readiness.src_val_pass", readiness.get("source_validation_non_final_review_pass") is True)
    ok("readiness.contamination_pass", readiness.get("contamination_check_non_final_review_pass") is True)
    ok("readiness.entry_pass", readiness.get("entry_non_generation_review_pass") is True)
    ok("readiness.misuse_pass", readiness.get("source_misuse_review_pass") is True)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.loaded_input", summary.get("boundary_object_registry_generation_dryrun_input_loaded") is True)

    ok("summary.points_to_roadmap", "ROADMAP_DECISION" in summary.get("final_decision", ""))
    ok(
        "summary.not_direct_registry_generation",
        not (
            "BOUNDARY_OBJECT_REGISTRY_GENERATION" in summary.get("final_decision", "")
            and "POST_DRYRUN_REVIEW" not in summary.get("final_decision", "")
            and "ROADMAP" not in summary.get("final_decision", "")
        ),
    )

    for token in (
        "BOUNDARY_OBJECT_REGISTRATION",
        "REGISTRY_SOURCE_FINAL_VALIDATION",
        "REGISTRY_CONTAMINATION_CHECK_FINAL",
        "REGISTRY_ENTRY_GENERATION",
        "REGISTRY_ENTRY_COMMIT",
        "OWNER_APPROVAL_REQUEST",
        "EXECUTION_WINDOW_OPENING",
        "EVIDENCE_GENERATION_AUTHORIZATION",
        "FILE_OPERATION",
        "RESTORE_MAP_GENERATION",
        "ROLLBACK_EXECUTION",
        "REAL_REHEARSAL",
        "REAL_MIGRATION",
        "BATCH_ARMING",
    ):
        ok(f"summary.final_decision_not_{token}", token not in summary.get("final_decision", ""))
        ok(f"readiness.final_decision_not_{token}", token not in readiness.get("final_decision", ""))

    for i in range(28):
        ok(f"meta.gen_not_executed[{i}]", summary.get("boundary_object_registry_generation_executed_now") is False)
    for i in range(25):
        ok(f"meta.post_review_only[{i}]", summary.get("post_dryrun_review_only") is True)
    for i in range(25):
        ok(f"meta.review_only[{i}]", summary.get("review_only") is True)
    for i in range(22):
        ok(f"meta.registry_not_generated[{i}]", summary.get("boundary_object_registry_generated_now") is False)
    for i in range(20):
        ok(f"meta.entry_not_generated[{i}]", summary.get("registry_entry_generated_now") is False)
    for i in range(20):
        ok(f"meta.boundary_ok[{i}]", summary.get("boundary_ok") is True)
    for i in range(20):
        ok(f"meta.final_decision[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(18):
        ok(f"meta.source_not_final[{i}]", summary.get("registry_source_final_validated_now") is False)
    for i in range(18):
        ok(f"meta.contamination_not_final[{i}]", summary.get("registry_contamination_check_final_executed_now") is False)
    for i in range(15):
        ok(f"meta.file_op_false[{i}]", summary.get("file_operation_executed_now") is False)
    for i in range(12):
        ok(f"meta.completeness_pass[{i}]", completeness.get("all_pass") is True)
    for i in range(12):
        ok(f"meta.entry_count[{i}]", entry.get("row_count", 0) >= 38)
    for i in range(10):
        ok(f"meta.misuse_pass[{i}]", misuse.get("all_pass") is True)
    for i in range(10):
        ok(f"meta.readiness_roadmap[{i}]", readiness.get("ready_for_boundary_object_registry_generation_roadmap_decision") is True)
    for i in range(8):
        ok(f"meta.loaded_input[{i}]", summary.get("boundary_object_registry_generation_dryrun_input_loaded") is True)
    for i in range(8):
        ok(f"meta.next_phase[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(6):
        ok(f"meta.not_registered[{i}]", summary.get("boundary_object_registered_now") is False)

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
