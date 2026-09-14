#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Navigation Decision Chain Candidate DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_decision_center_module_planning_v1 import (
    OUTPUT_CONTRACT_FIELDS,
)
from capabilities.governance.vision_navigation_decision_chain_candidate_dryrun_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONSTITUTION_BINDING_REVIEW_ITEMS,
    DECISION_BOUNDARY_REVIEW_ITEMS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    RATIONALE_TRACEABILITY_REVIEW_ITEMS,
    READINESS_CONSUMPTION_REVIEW_ITEMS,
    SCOPE,
    TASK_RESPONSE_HANDOFF_REVIEW_ITEMS,
)
from capabilities.governance.vision_navigation_information_integration_chain_dryrun_v1 import (
    FINAL_DECISION_GO as II_CHAIN_DR_FINAL_GO,
    NEXT_PHASE_GO as II_CHAIN_DR_NEXT_PHASE,
)

MIN_CHECKS = 200

REQUIRED = (
    "vision_navigation_decision_chain_candidate_dryrun_policy_v1.json",
    "integration_chain_input_review_v1.json",
    "decision_chain_model_candidate_v1.json",
    "sample_decision_request_candidate_v1.json",
    "sample_decision_candidate_v1.json",
    "readiness_conflict_gap_consumption_review_v1.json",
    "constitution_health_drive_binding_review_v1.json",
    "decision_rationale_traceability_review_v1.json",
    "decision_boundary_review_v1.json",
    "task_response_handoff_readiness_review_v1.json",
    "decision_boundary_audit_v1.json",
    "decision_blocked_path_result_v1.json",
    "decision_closure_decision_v1.json",
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
            "vision_navigation_decision_chain_candidate_dryrun"
        ),
    )
    p.add_argument(
        "--integration-chain-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_navigation_information_integration_chain_dryrun"
        ),
    )
    p.add_argument(
        "--decision-center-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_decision_center_module_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--constitution-bus-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--drive-signal-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "seed_core_drive_signal_contract_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--provider-abstraction-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "provider_abstraction_standard_alignment_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    ii_chain_vr = _load(Path(args.integration_chain_dryrun_root) / "verifier_report.json")
    ii_chain_sm = _load(Path(args.integration_chain_dryrun_root) / "summary.json")
    dc_dr_vr = _load(Path(args.decision_center_dryrun_root) / "verifier_report.json")
    cb_dr_vr = _load(Path(args.constitution_bus_dryrun_root) / "verifier_report.json")
    ds_dr_vr = _load(Path(args.drive_signal_dryrun_root) / "verifier_report.json")
    provider_dr_vr = _load(Path(args.provider_abstraction_dryrun_root) / "verifier_report.json")

    ok("upstream.ii_chain_go", ii_chain_vr.get("verifier") == "GO")
    ok("upstream.ii_chain_final", ii_chain_sm.get("final_decision") == II_CHAIN_DR_FINAL_GO)
    ok("upstream.ii_chain_next", ii_chain_sm.get("recommended_next_phase") == II_CHAIN_DR_NEXT_PHASE)
    ok("upstream.dc_dr_go", dc_dr_vr.get("verifier") == "GO")
    ok("upstream.cb_dr_go", cb_dr_vr.get("verifier") == "GO")
    ok("upstream.ds_dr_go", ds_dr_vr.get("verifier") == "GO")
    ok("upstream.provider_go", provider_dr_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "vision_navigation_decision_chain_candidate_dryrun_policy_v1.json")
    input_review = _load(root / "integration_chain_input_review_v1.json")
    chain_model = _load(root / "decision_chain_model_candidate_v1.json")
    decision_request = _load(root / "sample_decision_request_candidate_v1.json")
    decision = _load(root / "sample_decision_candidate_v1.json")
    readiness_review = _load(root / "readiness_conflict_gap_consumption_review_v1.json")
    constitution_review = _load(root / "constitution_health_drive_binding_review_v1.json")
    rationale_review = _load(root / "decision_rationale_traceability_review_v1.json")
    boundary_review = _load(root / "decision_boundary_review_v1.json")
    task_handoff = _load(root / "task_response_handoff_readiness_review_v1.json")
    boundary = _load(root / "decision_boundary_audit_v1.json")
    blocked = _load(root / "decision_blocked_path_result_v1.json")
    closure = _load(root / "decision_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.fixture_decision", summary.get("fixture_decision_candidate_generated") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.chain_dryrun", policy.get("chain_dryrun_candidate_only_not_execute_not_output") is True)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.fixture_only", input_review.get("fixture_metadata_only") is True)
    ok("input.ii_go", input_review.get("integration_chain_dryrun_verifier") == "GO")
    ok("input.dc_go", input_review.get("decision_center_dryrun_verifier") == "GO")

    ok("model.id", chain_model.get("model_id") == "vision_navigation_decision_chain_v1")
    ok("model.chain_type", chain_model.get("chain_type") == "fixture_based_decision_chain_candidate")
    ok("model.consumes_integrated", chain_model.get("consumes_integrated_context_candidate") is True)
    ok("model.consumes_readiness", chain_model.get("consumes_decision_readiness_candidate") is True)
    ok("model.emits_decision", chain_model.get("emits_decision_candidate") is True)
    ok("model.not_execute", chain_model.get("does_not_execute_decision") is True)
    ok("model.not_task_resp", chain_model.get("does_not_generate_task_response") is True)
    ok("model.not_output", chain_model.get("does_not_generate_user_output") is True)
    ok("model.candidate", chain_model.get("candidate_only") is True)

    ok(
        "request.integrated_ref",
        decision_request.get("integrated_context_ref") == "integrated_context_vision_nav_chain_001",
    )
    ok(
        "request.readiness_ref",
        decision_request.get("decision_readiness_ref") == "readiness_vision_nav_chain_001",
    )
    ok("request.fixture", decision_request.get("fixture_metadata_only") is True)
    ok("request.candidate", decision_request.get("candidate_only") is True)

    for field in OUTPUT_CONTRACT_FIELDS:
        ok(f"decision.{field[:18]}", field in decision)
    ok("decision.id", decision.get("decision_candidate_id") == "decision_candidate_vision_nav_chain_001")
    ok("decision.type", decision.get("decision_type") == "navigation_safety_hold_review")
    ok("decision.scope", decision.get("decision_scope") == "street_crossing_navigation_fixture")
    ok("decision.action", decision.get("selected_action") == "hold_candidate")
    ok("decision.hold_reason", bool(decision.get("hold_reason")))
    ok("decision.candidate", decision.get("candidate_only") is True)
    ok("decision.not_nav", decision.get("navigation_action_allowed") is False)
    ok("decision.no_output", decision.get("user_output_allowed") is False)
    ok("decision.no_task_resp", decision.get("task_response_generation_allowed") is False)
    ok("decision.no_memory", decision.get("memory_write_allowed") is False)
    ok("decision.no_worldmodel", decision.get("world_model_write_allowed") is False)
    ok("decision.not_executed", decision.get("not_executed") is True)

    for item in READINESS_CONSUMPTION_REVIEW_ITEMS:
        ok(f"readiness_review.{item[:18]}", readiness_review.get("dryrun_and_review_pass") is True)
    ok(
        "readiness_review.status",
        readiness_review.get("readiness_status") == "not_ready_for_real_navigation_decision",
    )
    ok("readiness_review.sufficient_false", readiness_review.get("sufficient_for_decision") is False)
    ok("readiness_review.conflict", readiness_review.get("conflict_type") == "map_vs_vision")
    ok(
        "readiness_review.gap",
        "missing_real_time_frame_validation" in str(readiness_review.get("gap_type", "")),
    )
    ok("readiness_review.hold_action", readiness_review.get("selected_action") == "hold_candidate")

    for item in CONSTITUTION_BINDING_REVIEW_ITEMS:
        ok(f"constitution_review.{item[:18]}", constitution_review.get("dryrun_and_review_pass") is True)
    ok("constitution_review.survival", constitution_review.get("survival_drive_elevated") is True)

    for item in RATIONALE_TRACEABILITY_REVIEW_ITEMS:
        ok(f"rationale_review.{item[:18]}", rationale_review.get("dryrun_and_review_pass") is True)
    ok("rationale_review.hold", rationale_review.get("hold_reason_present") is True)

    for item in DECISION_BOUNDARY_REVIEW_ITEMS:
        ok(f"boundary_review.{item[:18]}", boundary_review.get("dryrun_and_review_pass") is True)
    ok("boundary_review.generated", boundary_review.get("decision_candidate_generated") is True)
    ok("boundary_review.not_executed", boundary_review.get("decision_executed") is False)

    for item in TASK_RESPONSE_HANDOFF_REVIEW_ITEMS:
        ok(f"task_handoff.{item[:18]}", task_handoff.get("dryrun_and_review_pass") is True)
    ok(
        "task_handoff.no_task_resp",
        task_handoff.get("handoff_package", {}).get("task_response_candidate_generated") is False,
    )
    ok(
        "task_handoff.no_output",
        task_handoff.get("handoff_package", {}).get("user_output_generated") is False,
    )

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    ok("boundary.decision_gen", boundary.get("decision_candidate_generated_now") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count19", blocked.get("blocked_count") == 19)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )
    ok(
        "blocked.allowed_candidate",
        any(
            a.get("path_id") == "dryrun_to_decision_candidate_generation"
            and a.get("status") == "allowed_candidate_only"
            for a in (blocked.get("allowed_paths") or [])
        ),
    )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_task_response_candidate_dryrun") is True)
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
