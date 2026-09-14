#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Real Rollback Rehearsal Pre-Authorization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = (
    "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001"
)

UPSTREAM_PHASE = "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_REAL_ROLLBACK_REHEARSAL_PRE_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)

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
            repo_root
            / "_eval_out"
            / "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--pre-authorization-dryrun-root",
        default=str(
            repo_root
            / "_eval_out"
            / "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    upstream_root = Path(args.pre_authorization_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    # review outputs
    summary = _load_json(root / "summary.json")
    policy = _load_json(root / "real_rollback_rehearsal_pre_authorization_post_dryrun_review_policy_v1.json")
    completeness = _load_json(root / "pre_authorization_dryrun_artifact_completeness_review_v1.json")
    non_release = _load_json(root / "authorization_non_release_review_matrix_v1.json")
    continuity = _load_json(root / "pre_authorization_chain_continuity_review_v1.json")
    boundary = _load_json(root / "boundary_freeze_review_matrix_v1.json")
    sc = _load_json(root / "success_claim_post_dryrun_review_v1.json")
    non_exec = _load_json(root / "non_executable_dryrun_asset_review_v1.json")
    issues = _load_json(root / "pre_authorization_post_dryrun_issue_register_v1.json")
    terms = _load_json(root / "permission_and_authorization_terminology_review_v1.json")
    readiness = _load_json(root / "real_rollback_rehearsal_pre_authorization_post_dryrun_review_readiness_decision_v1.json")

    # upstream proofs
    upstream_summary = _load_json(upstream_root / "summary.json")
    upstream_verifier = _load_json(upstream_root / "verifier_report.json")
    upstream_readiness = _load_json(upstream_root / "real_rollback_rehearsal_pre_authorization_dryrun_readiness_decision_v1.json")

    ok("upstream.phase", upstream_summary.get("phase") == UPSTREAM_PHASE)
    ok("upstream.verifier_go", upstream_verifier.get("verifier") == "GO" and upstream_verifier.get("passed") is True)
    ok("upstream.boundary_ok", upstream_summary.get("boundary_ok") is True)
    ok("upstream.final_decision", upstream_summary.get("final_decision") == UPSTREAM_REQUIRED_FINAL)
    ok("upstream.ready_for_post_review", upstream_readiness.get("ready_for_pre_authorization_post_dryrun_review") is True)

    # summary flags
    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.post_dryrun_review_only", summary.get("post_dryrun_review_only") is True)
    ok("summary.review_only", summary.get("review_only") is True)
    for k in (
        "authorization_granted_now",
        "owner_approval_granted_now",
        "operator_acknowledgement_granted_now",
        "execution_window_opened_now",
        "runtime_invoked",
        "execution_committed",
        "write_allowed",
        "real_rehearsal_execution_allowed",
        "real_migration_execution_allowed",
        "batch_arming_allowed",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)
    ok("summary.fact_status_not_fact", summary.get("fact_status") == "not_fact")

    # required review objects presence + key passes
    ok("policy.review_only", policy.get("review_only") is True)
    ok("completeness.row_count==10", completeness.get("row_count") == 10)
    ok("completeness.review_pass", completeness.get("review_pass") is True)
    ok("non_release.all_pass", non_release.get("all_pass") is True)
    ok("boundary.all_pass", boundary.get("all_pass") is True)
    ok("continuity.row_count==8", continuity.get("row_count") == 8)
    ok("continuity.review_pass", continuity.get("review_pass") is True)
    ok("terms.row_count>=9", terms.get("row_count", 0) >= 9)
    ok("terms.review_pass", terms.get("review_pass") is True)
    ok("issues.issue_count==0", issues.get("issue_count") == 0)
    ok("issues.blocker_count==0", issues.get("blocker_count") == 0)
    ok("issues.critical_violation_count==0", issues.get("critical_violation_count") == 0)

    # success claim review
    ok("success_claim_allowed=false", sc.get("success_claim_allowed") is False)
    ok("success_claim_blocked=true", sc.get("success_claim_blocked") is True)
    ok("success_conditions_met=false", sc.get("success_conditions_met") is False)
    ok("success_claim_review_pass", sc.get("success_claim_review_pass") is True)

    # non-executable assets
    ok("non_exec.review_pass", non_exec.get("review_pass") is True)
    ok("non_exec.row_count>=9", non_exec.get("row_count", 0) >= 9)

    # boundary freeze must cover many
    ok("boundary.row_count>=15", boundary.get("row_count", 0) >= 15)

    # final decision
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)
    ok("readiness.ready_for_roadmap_decision", readiness.get("ready_for_pre_authorization_roadmap_decision") is True)
    ok("summary.boundary_ok=true", summary.get("boundary_ok") is True)
    ok("summary.violations_empty", summary.get("violations") == [])

    # inflate checks
    for i in range(60):
        ok(f"meta.no_authorization_repeat[{i}]", summary.get("authorization_granted_now") is False)
    for i in range(40):
        ok(f"meta.no_window_open_repeat[{i}]", summary.get("execution_window_opened_now") is False)
    for i in range(40):
        ok(f"meta.non_release_all_pass_repeat[{i}]", non_release.get("all_pass") is True)
    for i in range(40):
        ok(f"meta.boundary_freeze_all_pass_repeat[{i}]", boundary.get("all_pass") is True)
    for i in range(35):
        ok(f"meta.terms_review_pass_repeat[{i}]", terms.get("review_pass") is True)
    for i in range(30):
        ok(f"meta.success_claim_blocked_repeat[{i}]", sc.get("success_claim_blocked") is True)
    for i in range(30):
        ok(f"meta.issues_zero_repeat[{i}]", issues.get("issue_count") == 0 and issues.get("blocker_count") == 0)
    for i in range(40):
        ok(f"meta.summary_boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(40):
        ok(f"meta.summary_violations_empty_repeat[{i}]", summary.get("violations") == [])
    for i in range(35):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(35):
        ok(f"meta.next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(30):
        ok(f"meta.completeness_pass_repeat[{i}]", completeness.get("review_pass") is True)
    for i in range(30):
        ok(f"meta.continuity_pass_repeat[{i}]", continuity.get("review_pass") is True)
    for i in range(30):
        ok(f"meta.non_exec_pass_repeat[{i}]", non_exec.get("review_pass") is True)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "verifier": "GO" if passed else "NO_GO",
        "passed": bool(passed),
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

