#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify First Person Scene Understanding Decision Chain Candidate DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.first_person_scene_understanding_decision_chain_candidate_dryrun_v1 import (
    ACTION_TAXONOMY_REVIEW_ITEMS,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CAPABILITY_STACK_GOVERNANCE_RULES,
    CAPABILITY_STACK_LAYER_FIELDS,
    CAPABILITY_STACK_LAYERS,
    DC_BINDING_REVIEW_ITEMS,
    DECISION_ACTION_TAXONOMY,
    DECISION_CANDIDATE_FIELDS,
    DECISION_REQUEST_FIELDS,
    FINAL_DECISION_GO,
    NAVIGATION_APP_DECISION_REVIEW_ITEMS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCENE_PRIORITY_REVIEW_ITEMS,
    SCOPE,
    SPATIOTEMPORAL_DECISION_REVIEW_ITEMS,
    SURVIVAL_RISK_DECISION_REVIEW_ITEMS,
    TARGET_RECOGNITION_DECISION_REVIEW_ITEMS,
    TARGET_TRACKING_DECISION_REVIEW_ITEMS,
    TASK_INTENT_DECISION_REVIEW_ITEMS,
    TASK_RESPONSE_HANDOFF_ITEMS,
    TEXT_RECOGNITION_DECISION_REVIEW_ITEMS,
    TRACEABILITY_REVIEW_ITEMS,
    WORLD_CONTINUITY_DECISION_REVIEW_ITEMS,
)
from capabilities.governance.first_person_scene_understanding_information_integration_chain_dryrun_v1 import (
    FINAL_DECISION_GO as II_CHAIN_DR_FINAL_GO,
    NEXT_PHASE_GO as II_CHAIN_DR_NEXT_PHASE,
)

MIN_CHECKS = 378

REQUIRED = (
    "first_person_scene_understanding_decision_chain_dryrun_policy_v1.json",
    "first_person_capability_stack_governance_v1.json",
    "information_integration_input_review_v1.json",
    "decision_center_binding_review_v1.json",
    "sample_decision_request_candidate_v1.json",
    "sample_decision_candidate_v1.json",
    "scene_understanding_decision_priority_review_v1.json",
    "target_recognition_decision_review_v1.json",
    "text_recognition_decision_review_v1.json",
    "target_tracking_decision_review_v1.json",
    "task_intent_decision_review_v1.json",
    "spatiotemporal_continuity_decision_review_v1.json",
    "world_continuity_decision_review_v1.json",
    "survival_risk_decision_review_v1.json",
    "navigation_application_context_decision_review_v1.json",
    "decision_action_taxonomy_review_v1.json",
    "decision_to_task_response_handoff_plan_v1.json",
    "decision_traceability_review_v1.json",
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
            "first_person_scene_understanding_decision_chain_candidate_dryrun"
        ),
    )
    p.add_argument(
        "--integration-chain-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_information_integration_chain_dryrun"
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
        "--information-integration-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_information_integration_layer_dryrun_and_review"
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
        "--constitution-bus-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--safety-gate-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_safety_gate_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--health-enforcement-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "health_enforcement_supervisor_dryrun_and_review"
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
    ii_dr_vr = _load(Path(args.information_integration_dryrun_root) / "verifier_report.json")
    ds_dr_vr = _load(Path(args.drive_signal_dryrun_root) / "verifier_report.json")
    cb_dr_vr = _load(Path(args.constitution_bus_dryrun_root) / "verifier_report.json")
    safety_dr_vr = _load(Path(args.safety_gate_dryrun_root) / "verifier_report.json")
    health_dr_vr = _load(Path(args.health_enforcement_dryrun_root) / "verifier_report.json")

    ok("upstream.ii_chain_go", ii_chain_vr.get("verifier") == "GO")
    ok("upstream.ii_chain_final", ii_chain_sm.get("final_decision") == II_CHAIN_DR_FINAL_GO)
    ok("upstream.ii_chain_next", ii_chain_sm.get("recommended_next_phase") == II_CHAIN_DR_NEXT_PHASE)
    ok("upstream.dc_dr_go", dc_dr_vr.get("verifier") == "GO")
    ok("upstream.ii_dr_go", ii_dr_vr.get("verifier") == "GO")
    ok("upstream.ds_dr_go", ds_dr_vr.get("verifier") == "GO")
    ok("upstream.cb_dr_go", cb_dr_vr.get("verifier") == "GO")
    ok("upstream.safety_go", safety_dr_vr.get("verifier") == "GO")
    ok("upstream.health_go", health_dr_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "first_person_scene_understanding_decision_chain_dryrun_policy_v1.json")
    stack_gov = _load(root / "first_person_capability_stack_governance_v1.json")
    input_review = _load(root / "information_integration_input_review_v1.json")
    dc_binding = _load(root / "decision_center_binding_review_v1.json")
    request = _load(root / "sample_decision_request_candidate_v1.json")
    decision = _load(root / "sample_decision_candidate_v1.json")
    scene_review = _load(root / "scene_understanding_decision_priority_review_v1.json")
    target_review = _load(root / "target_recognition_decision_review_v1.json")
    text_review = _load(root / "text_recognition_decision_review_v1.json")
    tracking_review = _load(root / "target_tracking_decision_review_v1.json")
    task_review = _load(root / "task_intent_decision_review_v1.json")
    spatiotemporal_review = _load(root / "spatiotemporal_continuity_decision_review_v1.json")
    world_review = _load(root / "world_continuity_decision_review_v1.json")
    survival_review = _load(root / "survival_risk_decision_review_v1.json")
    nav_review = _load(root / "navigation_application_context_decision_review_v1.json")
    taxonomy_review = _load(root / "decision_action_taxonomy_review_v1.json")
    handoff = _load(root / "decision_to_task_response_handoff_plan_v1.json")
    trace_review = _load(root / "decision_traceability_review_v1.json")
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
    ok("summary.stack_registered", summary.get("capability_stack_governance_registered") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.decision_only", policy.get("decision_candidate_only_not_execute_not_output") is True)
    ok("policy.stack_required", policy.get("capability_stack_governance_required") is True)

    ok("stack.governance_id", stack_gov.get("governance_id") == "first_person_capability_stack_governance_v1")
    ok("stack.layer_count5", stack_gov.get("layer_count") == 5)
    ok("stack.no_mega_mix", stack_gov.get("no_mega_capability_mixing") is True)
    ok("stack.nav_layer3", stack_gov.get("navigation_is_layer_3_not_layer_1") is True)
    ok("stack.layer4_deferred", stack_gov.get("layer_4_deferred") is True)
    ok("stack.layer5_later", stack_gov.get("layer_5_later") is True)
    ok("stack.governance_pass", stack_gov.get("governance_pass") is True)
    ok("stack.layer1_goal", stack_gov.get("layer_1_primary_goal") == "current_scene_understanding")
    ok(
        "stack.layer2_goal",
        stack_gov.get("layer_2_secondary_goal") == "spatiotemporal_continuity_and_world_understanding",
    )
    ok("stack.layer3_goal", stack_gov.get("layer_3_application_goal") == "navigation_application_layer")
    for rule in CAPABILITY_STACK_GOVERNANCE_RULES:
        ok(f"stack.rule.{rule[:18]}", rule in (stack_gov.get("governance_rules") or []))
    layers = stack_gov.get("layers") or []
    for layer_def in CAPABILITY_STACK_LAYERS:
        layer = next((l for l in layers if l.get("layer_id") == layer_def["layer_id"]), {})
        ok(f"stack.layer.{layer_def['layer_id']}", bool(layer))
        for field in CAPABILITY_STACK_LAYER_FIELDS:
            ok(f"stack.{layer_def['layer_id']}.{field[:12]}", field in layer)
        ok(
            f"stack.{layer_def['layer_id']}.scope",
            layer.get("capability_scope") == layer_def["capability_scope"],
        )

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.scene_primary", input_review.get("scene_understanding_primary") is True)
    ok("input.nav_app", input_review.get("navigation_application_layer_only") is True)
    ok("input.ii_go", input_review.get("integration_chain_dryrun_verifier") == "GO")

    for item in DC_BINDING_REVIEW_ITEMS:
        ok(f"dc_binding.{item[:18]}", dc_binding.get("dryrun_and_review_pass") is True)

    for field in DECISION_REQUEST_FIELDS:
        ok(f"request.{field[:18]}", field in request)
    ok(
        "request.integrated_ref",
        request.get("source_integrated_context_ref") == "integrated_context_scene_understanding_chain_001",
    )
    ok("request.candidate", request.get("candidate_only") is True)
    ok("request.not_action", request.get("not_action") is True)

    for field in DECISION_CANDIDATE_FIELDS:
        ok(f"decision.{field[:18]}", field in decision)
    ok("decision.id", decision.get("decision_candidate_id") == "decision_candidate_scene_understanding_chain_001")
    ok("decision.action", decision.get("selected_action") in ("observe_more", "hold_for_safety"))
    ok("decision.action_taxonomy", decision.get("selected_action") in DECISION_ACTION_TAXONOMY)
    ok("decision.status", decision.get("decision_status") == "candidate_hold")
    ok("decision.scope", decision.get("decision_scope") == "first_person_scene_understanding")
    ok("decision.primary", decision.get("primary_goal") == "current_scene_understanding")
    ok(
        "decision.secondary",
        decision.get("secondary_goal") == "spatiotemporal_continuity_and_world_understanding",
    )
    ok("decision.application", decision.get("application_goal") == "navigation_application_layer")
    ok("decision.observe_reason", bool(decision.get("observe_more_reason")))
    ok("decision.hold_reason", bool(decision.get("hold_reason")))
    ok("decision.no_task_resp", decision.get("task_response_generation_allowed") is False)
    ok("decision.no_runtime", decision.get("runtime_enable_allowed") is False)
    ok("decision.candidate", decision.get("candidate_only") is True)
    ok(
        "decision.forbidden_nav",
        "direct_navigation_action_without_runtime_authorization" in (decision.get("forbidden_actions") or []),
    )
    ok(
        "decision.required_obs",
        "live_scene_validation_later" in (decision.get("required_observation") or []),
    )
    ok("decision.survival", decision.get("survival_priority_applied") is True)

    for item in SCENE_PRIORITY_REVIEW_ITEMS:
        ok(f"scene_review.{item[:18]}", scene_review.get("dryrun_and_review_pass") is True)
    ok("scene_review.layer1", scene_review.get("layer_1_primary_confirmed") is True)
    ok("scene_review.layer2", scene_review.get("layer_2_secondary_confirmed") is True)
    ok("scene_review.layer3", scene_review.get("layer_3_application_confirmed") is True)
    ok("scene_review.layer4_deferred", scene_review.get("layer_4_deferred_confirmed") is True)
    ok("scene_review.no_mega", scene_review.get("no_mega_capability_mixing") is True)
    for item in TARGET_RECOGNITION_DECISION_REVIEW_ITEMS:
        ok(f"target_review.{item[:18]}", target_review.get("dryrun_and_review_pass") is True)
    for item in TEXT_RECOGNITION_DECISION_REVIEW_ITEMS:
        ok(f"text_review.{item[:18]}", text_review.get("dryrun_and_review_pass") is True)
    for item in TARGET_TRACKING_DECISION_REVIEW_ITEMS:
        ok(f"tracking_review.{item[:18]}", tracking_review.get("dryrun_and_review_pass") is True)
    for item in TASK_INTENT_DECISION_REVIEW_ITEMS:
        ok(f"task_review.{item[:18]}", task_review.get("dryrun_and_review_pass") is True)
    for item in SPATIOTEMPORAL_DECISION_REVIEW_ITEMS:
        ok(f"spatiotemporal_review.{item[:18]}", spatiotemporal_review.get("dryrun_and_review_pass") is True)
    for item in WORLD_CONTINUITY_DECISION_REVIEW_ITEMS:
        ok(f"world_review.{item[:18]}", world_review.get("dryrun_and_review_pass") is True)
    for item in SURVIVAL_RISK_DECISION_REVIEW_ITEMS:
        ok(f"survival_review.{item[:18]}", survival_review.get("dryrun_and_review_pass") is True)
    for item in NAVIGATION_APP_DECISION_REVIEW_ITEMS:
        ok(f"nav_review.{item[:18]}", nav_review.get("dryrun_and_review_pass") is True)
    ok("nav_review.mark_not_ready", nav_review.get("mark_not_ready") is True)

    for item in ACTION_TAXONOMY_REVIEW_ITEMS:
        ok(f"taxonomy_review.{item[:18]}", taxonomy_review.get("dryrun_and_review_pass") is True)
    ok("taxonomy.in_taxonomy", taxonomy_review.get("selected_action_in_taxonomy") is True)
    for action in DECISION_ACTION_TAXONOMY:
        ok(f"taxonomy.{action[:18]}", action in (taxonomy_review.get("taxonomy") or []))

    for item in TASK_RESPONSE_HANDOFF_ITEMS:
        ok(f"handoff.{item[:18]}", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.no_task_resp", handoff.get("task_response_candidate_generated_now") is False)

    for item in TRACEABILITY_REVIEW_ITEMS:
        ok(f"trace_review.{item[:18]}", trace_review.get("dryrun_and_review_pass") is True)
    ok(
        "trace_review.source",
        trace_review.get("source_integrated_context_ref") == "integrated_context_scene_understanding_chain_001",
    )

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    ok("boundary.decision_gen", boundary.get("decision_candidate_generated_now") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count17", blocked.get("blocked_count") == 17)
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
