#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Factory Standard Historical Redundancy Cleanup DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1 import (
    ABSORBED_RULE_SAMPLES,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CLEANUP_SCOPES,
    DEPRECATED_PATTERNS,
    FINAL_DECISION_GO,
    METADATA_SCHEMA_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SUPERSEDED_COVERAGE,
)
from capabilities.governance.factory_standard_historical_redundancy_cleanup_planning_v1 import (
    FINAL_DECISION_GO as CLEANUP_PLANNING_FINAL,
    NEXT_PHASE_GO as CLEANUP_PLANNING_NEXT,
)

MIN_CHECKS = 95


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _marker_ok(item: Dict[str, Any]) -> bool:
    for field in METADATA_SCHEMA_FIELDS:
        if field not in item:
            return False
    return (
        item.get("keep_for_audit") is True
        and item.get("physical_delete_allowed") is False
        and item.get("migration_required") is False
    )


REQUIRED = (
    "factory_standard_historical_cleanup_dryrun_and_review_policy_v1.json",
    "cleanup_planning_input_review_v1.json",
    "historical_redundancy_cleanup_candidate_v1.json",
    "superseded_phase_marker_samples_v1.json",
    "absorbed_rule_marker_samples_v1.json",
    "deprecated_for_new_phase_marker_samples_v1.json",
    "read_only_evidence_source_marker_samples_v1.json",
    "cleanup_metadata_schema_validation_result_v1.json",
    "historical_chain_preservation_review_v1.json",
    "no_physical_delete_audit_v1.json",
    "future_phase_reference_policy_dryrun_result_v1.json",
    "cleanup_boundary_blocked_path_result_v1.json",
    "cleanup_compression_alignment_review_v1.json",
    "cleanup_dryrun_and_review_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--factory-standard-historical-redundancy-cleanup-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "factory_standard_historical_redundancy_cleanup_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.factory_standard_historical_redundancy_cleanup_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    planning_review = _load(root / "cleanup_planning_input_review_v1.json")
    candidate = _load(root / "historical_redundancy_cleanup_candidate_v1.json")
    superseded = _load(root / "superseded_phase_marker_samples_v1.json")
    absorbed = _load(root / "absorbed_rule_marker_samples_v1.json")
    deprecated = _load(root / "deprecated_for_new_phase_marker_samples_v1.json")
    read_only = _load(root / "read_only_evidence_source_marker_samples_v1.json")
    schema_val = _load(root / "cleanup_metadata_schema_validation_result_v1.json")
    preservation = _load(root / "historical_chain_preservation_review_v1.json")
    no_delete = _load(root / "no_physical_delete_audit_v1.json")
    future_ref = _load(root / "future_phase_reference_policy_dryrun_result_v1.json")
    blocked = _load(root / "cleanup_boundary_blocked_path_result_v1.json")
    compression = _load(root / "cleanup_compression_alignment_review_v1.json")
    closure = _load(root / "cleanup_dryrun_and_review_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("factory_standard_historical_redundancy_cleanup_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.marking_only", summary.get("marking_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == CLEANUP_PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == CLEANUP_PLANNING_NEXT)
    ok("planning_review.pass", planning_review.get("review_pass") is True)

    ok("candidate.scopes6", candidate.get("scope_count") == len(CLEANUP_SCOPES))
    ok("candidate.marking", candidate.get("marking_only") is True)

    for field in BOUNDARY_TRUE:
        ok(f"boundary_true.{field}", summary.get(field) is True)

    ok("superseded.schema", superseded.get("all_schema_valid") is True)
    ok("superseded.verdict", superseded.get("all_verdict_preserved") is True)
    ok("superseded.read_only", superseded.get("all_read_only") is True)
    superseded_phases = {s.get("source_phase") for s in (superseded.get("samples") or [])}
    for phase in SUPERSEDED_COVERAGE:
        ok(f"superseded.cover.{phase}", phase in superseded_phases)

    ok("absorbed.schema", absorbed.get("all_schema_valid") is True)
    ok("absorbed.ref_std", absorbed.get("all_reference_standard") is True)
    for rule_id, _, _ in ABSORBED_RULE_SAMPLES:
        ok(f"absorbed.rule.{rule_id}", any(s.get("rule_pattern") == rule_id for s in (absorbed.get("samples") or [])))

    ok("deprecated.schema", deprecated.get("all_schema_valid") is True)
    ok("deprecated.all_flag", deprecated.get("all_deprecated") is True)
    for pattern in DEPRECATED_PATTERNS:
        ok(f"deprecated.pattern.{pattern}", any(s.get("pattern_id") == pattern for s in (deprecated.get("samples") or [])))

    ok("readonly.count7", read_only.get("sample_count") == 7)
    ok("readonly.schema", read_only.get("all_schema_valid") is True)
    ok("readonly.paths", read_only.get("all_paths_exist") is True)
    ok("readonly.verifier", read_only.get("all_verifier_preserved") is True)
    ok("readonly.chain", all(s.get("evidence_chain_preserved") is True for s in (read_only.get("samples") or [])))

    ok("schema.pass", schema_val.get("all_samples_valid") is True)

    ok("preservation.pass", preservation.get("dryrun_and_review_pass") is True)
    ok("no_delete.pass", no_delete.get("dryrun_and_review_pass") is True)
    ok("future.pass", future_ref.get("dryrun_and_review_pass") is True)
    ok("future.no_triple", future_ref.get("do_not_replicate_triple_chain") is True)

    ok("blocked.count", blocked.get("path_count") == len(BLOCKED_PATHS))
    ok("blocked.all", blocked.get("all_blocked") is True)
    for bp in BLOCKED_PATHS:
        row = next((r for r in (blocked.get("blocked_paths") or []) if r.get("path_id") == bp), None)
        ok(f"blocked.{bp}", row is not None and row.get("status") == "blocked")

    ok("compression.pass", compression.get("dryrun_and_review_pass") is True)
    ok("compression.triple_blocked", compression.get("triple_chain_blocked_for_new_phase") is True)

    ok("closure.pass", closure.get("closure_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_ocr_authorization_next_route_decision") is True)
    ok("next_route.no_real_dep", next_route.get("real_dependency_check_allowed_now") is False)

    for field in BOUNDARY_FALSE:
        ok(f"boundary_false.{field}", summary.get(field) is False)

    all_samples = (
        (superseded.get("samples") or [])
        + (absorbed.get("samples") or [])
        + (deprecated.get("samples") or [])
        + (read_only.get("samples") or [])
    )
    ok("markers.all_schema", all(_marker_ok(s) for s in all_samples))
    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
