#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Information Integration Layer DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONTEXT_CONFLICT_TYPES,
    CONTEXT_GAP_TYPES,
    DECISION_READINESS_FIELDS,
    DRIVE_SIGNAL_INTEGRATION_CONFIRMATIONS,
    FINAL_DECISION_GO,
    HANDOFF_PLAN_ITEMS,
    HEALTH_VALIDATION_WHITEBOX_CONFIRMATIONS,
    INTEGRATED_CONTEXT_CANDIDATE_FIELDS,
    INTEGRATION_INPUT_CONFIRMATIONS,
    INTEGRATION_INPUT_SOURCES,
    MEMORY_WM_INTEGRATION_CONFIRMATIONS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    NO_UNIVERSAL_BRAIN_BOUNDARIES,
    PERCEPTION_INTEGRATION_CONFIRMATIONS,
    PHASE_ID,
    PROVIDER_STATUS_CONFIRMATIONS,
    SCORING_CONFIRMATIONS,
    SCORING_POLICY_ITEMS,
    SCOPE,
    TASK_ROUTE_MAP_CONFIRMATIONS,
    TRACEABILITY_FIELDS,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.midplatform_information_integration_layer_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
)
from capabilities.governance.seed_core_drive_signal_contract_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DS_DR_FINAL,
)

MIN_CHECKS = 311

REQUIRED = (
    "information_integration_dryrun_review_policy_v1.json",
    "information_integration_planning_input_review_v1.json",
    "information_integration_model_candidate_v1.json",
    "sample_integrated_context_candidate_v1.json",
    "sample_context_conflict_candidate_v1.json",
    "sample_context_gap_candidate_v1.json",
    "sample_context_freshness_status_v1.json",
    "sample_context_priority_map_v1.json",
    "sample_decision_readiness_candidate_v1.json",
    "integration_input_source_taxonomy_review_v1.json",
    "drive_signal_integration_review_v1.json",
    "perception_context_integration_review_v1.json",
    "memory_worldmodel_context_integration_review_v1.json",
    "task_route_map_context_integration_review_v1.json",
    "health_validation_whitebox_integration_review_v1.json",
    "provider_status_integration_review_v1.json",
    "conflict_gap_freshness_scoring_review_v1.json",
    "decision_center_handoff_review_v1.json",
    "no_universal_brain_boundary_review_v1.json",
    "information_integration_traceability_review_v1.json",
    "information_integration_boundary_audit_v1.json",
    "information_integration_blocked_path_result_v1.json",
    "information_integration_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_information_integration_layer_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_information_integration_layer_planning"
        ),
    )
    p.add_argument(
        "--drive-signal-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "seed_core_drive_signal_contract_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    ds_dr_root = Path(args.drive_signal_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")
    ds_dr_vr = _load(ds_dr_root / "verifier_report.json")
    ds_dr_sm = _load(ds_dr_root / "summary.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.plan_final_expected", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok("upstream.plan_next_expected", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("upstream.ds_dr_go", ds_dr_vr.get("verifier") == "GO")
    ok("upstream.ds_dr_final", ds_dr_sm.get("final_decision") == DS_DR_FINAL)

    summary = _load(root / "summary.json")
    policy = _load(root / "information_integration_dryrun_review_policy_v1.json")
    input_review = _load(root / "information_integration_planning_input_review_v1.json")
    model = _load(root / "information_integration_model_candidate_v1.json")
    integrated = _load(root / "sample_integrated_context_candidate_v1.json")
    conflict = _load(root / "sample_context_conflict_candidate_v1.json")
    gap = _load(root / "sample_context_gap_candidate_v1.json")
    freshness = _load(root / "sample_context_freshness_status_v1.json")
    priority = _load(root / "sample_context_priority_map_v1.json")
    readiness = _load(root / "sample_decision_readiness_candidate_v1.json")
    taxonomy = _load(root / "integration_input_source_taxonomy_review_v1.json")
    drive_review = _load(root / "drive_signal_integration_review_v1.json")
    perception_review = _load(root / "perception_context_integration_review_v1.json")
    memory_review = _load(root / "memory_worldmodel_context_integration_review_v1.json")
    task_review = _load(root / "task_route_map_context_integration_review_v1.json")
    health_review = _load(root / "health_validation_whitebox_integration_review_v1.json")
    provider_review = _load(root / "provider_status_integration_review_v1.json")
    scoring_review = _load(root / "conflict_gap_freshness_scoring_review_v1.json")
    handoff = _load(root / "decision_center_handoff_review_v1.json")
    no_brain = _load(root / "no_universal_brain_boundary_review_v1.json")
    traceability = _load(root / "information_integration_traceability_review_v1.json")
    boundary = _load(root / "information_integration_boundary_audit_v1.json")
    blocked = _load(root / "information_integration_blocked_path_result_v1.json")
    closure = _load(root / "information_integration_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.sim_go", summary.get("system_level_simulated_go") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_runtime", policy.get("dryrun_not_runtime_not_decide") is True)
    ok("policy.model_id", policy.get("model_id") == "information_integration_model_candidate_v1")

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.plan_go", input_review.get("planning_verifier") == "GO")
    ok("input.ds_go", input_review.get("drive_signal_dryrun_verifier") == "GO")
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("model.id", model.get("model_id") == "information_integration_model_candidate_v1")
    ok("model.not_dc", model.get("not_decision_center") is True)
    ok("model.not_brain", model.get("not_universal_brain") is True)
    ok("model.not_decide", model.get("does_not_decide") is True)
    ok("model.not_provider", model.get("does_not_invoke_provider") is True)
    ok("model.not_mem", model.get("does_not_write_memory") is True)
    ok("model.input18", model.get("input_source_count") == 18)

    for field in INTEGRATED_CONTEXT_CANDIDATE_FIELDS:
        ok(f"integrated.field.{field[:18]}", field in integrated)
    ok("integrated.candidate", integrated.get("candidate_only") is True)
    ok("integrated.not_decision", integrated.get("not_decision") is True)
    ok("integrated.runtime_false", integrated.get("runtime_enable_allowed") is False)

    ok("conflict.type", conflict.get("conflict_type") in CONTEXT_CONFLICT_TYPES)
    ok("conflict.decision_req", conflict.get("decision_required") is True)
    ok("conflict.candidate", conflict.get("candidate_only") is True)

    ok("gap.type", gap.get("gap_type") in CONTEXT_GAP_TYPES)
    ok("gap.candidate", gap.get("candidate_only") is True)

    ok("fresh.can_drive_false", freshness.get("can_drive_decision") is False)
    ok("fresh.candidate", freshness.get("candidate_only") is True)

    ok("priority.candidate", priority.get("candidate_only") is True)

    for field in DECISION_READINESS_FIELDS:
        ok(f"ready.field.{field[:18]}", field in readiness)
    ok("ready.sufficient_false", readiness.get("sufficient_for_decision") is False)
    ok("ready.handoff_false", readiness.get("decision_center_handoff_allowed") is False)

    ok("tax.review_pass", taxonomy.get("dryrun_and_review_pass") is True)
    ok("tax.count18", taxonomy.get("source_count") == 18)
    for src in INTEGRATION_INPUT_SOURCES:
        ok(f"tax.{src[:18]}", src in (taxonomy.get("input_sources") or []))
    for conf in INTEGRATION_INPUT_CONFIRMATIONS:
        ok(f"tax.conf.{conf[:18]}", conf in (taxonomy.get("confirmations") or []))

    for conf in DRIVE_SIGNAL_INTEGRATION_CONFIRMATIONS:
        ok(f"drive.{conf[:18]}", conf in (drive_review.get("confirmations") or []))
    ok("drive.review_pass", drive_review.get("dryrun_and_review_pass") is True)

    for conf in PERCEPTION_INTEGRATION_CONFIRMATIONS:
        ok(f"perception.{conf[:18]}", conf in (perception_review.get("confirmations") or []))
    ok("perception.review_pass", perception_review.get("dryrun_and_review_pass") is True)

    for conf in MEMORY_WM_INTEGRATION_CONFIRMATIONS:
        ok(f"memory.{conf[:18]}", conf in (memory_review.get("confirmations") or []))
    ok("memory.review_pass", memory_review.get("dryrun_and_review_pass") is True)

    for conf in TASK_ROUTE_MAP_CONFIRMATIONS:
        ok(f"task.{conf[:18]}", conf in (task_review.get("confirmations") or []))
    ok("task.review_pass", task_review.get("dryrun_and_review_pass") is True)

    for conf in HEALTH_VALIDATION_WHITEBOX_CONFIRMATIONS:
        ok(f"health.{conf[:18]}", conf in (health_review.get("confirmations") or []))
    ok("health.review_pass", health_review.get("dryrun_and_review_pass") is True)

    for conf in PROVIDER_STATUS_CONFIRMATIONS:
        ok(f"provider.{conf[:18]}", conf in (provider_review.get("confirmations") or []))
    ok("provider.review_pass", provider_review.get("dryrun_and_review_pass") is True)

    ok("scoring.review_pass", scoring_review.get("dryrun_and_review_pass") is True)
    for item in SCORING_POLICY_ITEMS:
        ok(f"scoring.item.{item[:18]}", item in (scoring_review.get("scoring_items") or []))
    for conf in SCORING_CONFIRMATIONS:
        ok(f"scoring.conf.{conf[:18]}", conf in (scoring_review.get("confirmations") or []))
    for ct in CONTEXT_CONFLICT_TYPES:
        ok(f"scoring.ctype.{ct[:18]}", ct in (scoring_review.get("conflict_types_covered") or []))
    for gt in CONTEXT_GAP_TYPES:
        ok(f"scoring.gtype.{gt[:18]}", gt in (scoring_review.get("gap_types_covered") or []))

    ok("handoff.review_pass", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.dc_final", handoff.get("decision_center_final") is True)
    for item in HANDOFF_PLAN_ITEMS:
        ok(f"handoff.{item[:18]}", item in (handoff.get("handoff_items") or []))
    ok("handoff.chain_preserved", handoff.get("sample_handoff_package", {}).get("source_chain_preserved") is True)

    ok("no_brain.review_pass", no_brain.get("dryrun_and_review_pass") is True)
    for b in NO_UNIVERSAL_BRAIN_BOUNDARIES:
        ok(f"no_brain.{b[:18]}", b in (no_brain.get("boundaries") or []))

    ok("trace.review_pass", traceability.get("dryrun_and_review_pass") is True)
    ok("trace.preserve", traceability.get("all_transformations_must_preserve") is True)
    for field in TRACEABILITY_FIELDS:
        ok(f"trace.{field[:18]}", field in (traceability.get("required_fields") or []))

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count16", blocked.get("blocked_count") == 16)
    for path in BLOCKED_PATHS:
        ok(f"blocked.{path[:18]}", any(
            b.get("path_id") == path and b.get("status") == "blocked"
            for b in (blocked.get("blocked_paths") or [])
        ))

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_vision_navigation_mainline_resume") is True)
    ok("next_route.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    min_checks = MIN_CHECKS if MIN_CHECKS else total
    verifier = "GO" if passed == total and passed >= min_checks else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": min_checks,
        "dryrun_and_review_pass": summary.get("dryrun_and_review_pass"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
