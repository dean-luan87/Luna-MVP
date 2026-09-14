#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify First Person Scene Understanding Information Integration Chain DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.first_person_vision_navigation_candidate_flow_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CF_DR_FINAL_GO,
)
from capabilities.governance.first_person_scene_understanding_information_integration_chain_dryrun_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DC_HANDOFF_REVIEW_ITEMS,
    EVIDENCE_TRACEABILITY_REVIEW_ITEMS,
    FINAL_DECISION_GO,
    INTAKE_SAMPLE_IDS,
    NAVIGATION_APPLICATION_REVIEW_ITEMS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCENE_RULE_FIELDS,
    SCENE_UNDERSTANDING_GOALS,
    SPATIOTEMPORAL_CONTEXT_FIELDS,
    SPATIOTEMPORAL_CONTINUITY_REVIEW_ITEMS,
    SURVIVAL_CONTEXT_REVIEW_ITEMS,
    TARGET_RECOGNITION_FIELDS,
    TARGET_RECOGNITION_REVIEW_ITEMS,
    TARGET_TRACKING_FIELDS,
    TARGET_TRACKING_REVIEW_ITEMS,
    TASK_INTENT_FIELDS,
    TASK_INTENT_TARGET_SEARCH_REVIEW_ITEMS,
    TEXT_RECOGNITION_REVIEW_ITEMS,
    WORLD_CONTINUITY_FIELDS,
    WORLD_CONTINUITY_REVIEW_ITEMS,
    SCOPE,
)
from capabilities.governance.midplatform_information_integration_layer_planning_v1 import (
    DECISION_READINESS_FIELDS,
    FRESHNESS_STATUS_FIELDS,
    INTEGRATED_CONTEXT_CANDIDATE_FIELDS,
    PRIORITY_MAP_FIELDS,
)

MIN_CHECKS = 331

REQUIRED = (
    "first_person_scene_understanding_chain_dryrun_policy_v1.json",
    "previous_candidate_flow_input_review_v1.json",
    "scene_understanding_priority_reframe_v1.json",
    "sample_scene_understanding_candidate_intake_set_v1.json",
    "information_integration_chain_model_candidate_v1.json",
    "sample_integrated_context_candidate_v1.json",
    "sample_context_conflict_candidate_v1.json",
    "sample_context_gap_candidate_v1.json",
    "sample_context_freshness_status_v1.json",
    "sample_context_priority_map_v1.json",
    "sample_decision_readiness_candidate_v1.json",
    "target_recognition_integration_review_v1.json",
    "text_recognition_integration_review_v1.json",
    "target_tracking_integration_review_v1.json",
    "task_intent_target_search_integration_review_v1.json",
    "spatiotemporal_continuity_integration_review_v1.json",
    "world_continuity_understanding_review_v1.json",
    "survival_context_integration_review_v1.json",
    "navigation_as_application_context_review_v1.json",
    "evidence_traceability_integration_review_v1.json",
    "decision_center_handoff_readiness_review_v1.json",
    "chain_boundary_audit_v1.json",
    "chain_blocked_path_result_v1.json",
    "chain_closure_decision_v1.json",
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
            "first_person_scene_understanding_information_integration_chain_dryrun"
        ),
    )
    p.add_argument(
        "--candidate-flow-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_vision_navigation_candidate_flow_dryrun_and_review"
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

    cf_dr_vr = _load(Path(args.candidate_flow_dryrun_root) / "verifier_report.json")
    cf_dr_sm = _load(Path(args.candidate_flow_dryrun_root) / "summary.json")
    ii_dr_vr = _load(Path(args.information_integration_dryrun_root) / "verifier_report.json")
    ds_dr_vr = _load(Path(args.drive_signal_dryrun_root) / "verifier_report.json")
    cb_dr_vr = _load(Path(args.constitution_bus_dryrun_root) / "verifier_report.json")
    provider_dr_vr = _load(Path(args.provider_abstraction_dryrun_root) / "verifier_report.json")

    ok("upstream.cf_dr_go", cf_dr_vr.get("verifier") == "GO")
    ok("upstream.cf_dr_final", cf_dr_sm.get("final_decision") == CF_DR_FINAL_GO)
    ok("upstream.ii_dr_go", ii_dr_vr.get("verifier") == "GO")
    ok("upstream.ds_dr_go", ds_dr_vr.get("verifier") == "GO")
    ok("upstream.cb_dr_go", cb_dr_vr.get("verifier") == "GO")
    ok("upstream.provider_go", provider_dr_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "first_person_scene_understanding_chain_dryrun_policy_v1.json")
    input_review = _load(root / "previous_candidate_flow_input_review_v1.json")
    reframe = _load(root / "scene_understanding_priority_reframe_v1.json")
    intake = _load(root / "sample_scene_understanding_candidate_intake_set_v1.json")
    chain_model = _load(root / "information_integration_chain_model_candidate_v1.json")
    integrated = _load(root / "sample_integrated_context_candidate_v1.json")
    conflict = _load(root / "sample_context_conflict_candidate_v1.json")
    gap = _load(root / "sample_context_gap_candidate_v1.json")
    freshness = _load(root / "sample_context_freshness_status_v1.json")
    priority = _load(root / "sample_context_priority_map_v1.json")
    readiness = _load(root / "sample_decision_readiness_candidate_v1.json")
    target_review = _load(root / "target_recognition_integration_review_v1.json")
    text_review = _load(root / "text_recognition_integration_review_v1.json")
    tracking_review = _load(root / "target_tracking_integration_review_v1.json")
    task_review = _load(root / "task_intent_target_search_integration_review_v1.json")
    spatiotemporal_review = _load(root / "spatiotemporal_continuity_integration_review_v1.json")
    world_review = _load(root / "world_continuity_understanding_review_v1.json")
    survival_review = _load(root / "survival_context_integration_review_v1.json")
    nav_review = _load(root / "navigation_as_application_context_review_v1.json")
    trace_review = _load(root / "evidence_traceability_integration_review_v1.json")
    dc_handoff = _load(root / "decision_center_handoff_readiness_review_v1.json")
    boundary = _load(root / "chain_boundary_audit_v1.json")
    blocked = _load(root / "chain_blocked_path_result_v1.json")
    closure = _load(root / "chain_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.reframe", summary.get("mainline_reframe_applied") is True)
    ok("summary.fixture", summary.get("fixture_scene_understanding_integrated") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.chain_dryrun", policy.get("chain_dryrun_not_runtime_not_decide") is True)
    ok("policy.mainline", policy.get("mainline") == "first_person_scene_understanding")

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.historical_preserved", input_review.get("historical_phase_name_preserved") is True)
    ok("input.reframe", input_review.get("mainline_reframe_applied") is True)
    ok("input.cf_go", input_review.get("candidate_flow_dryrun_verifier") == "GO")

    ok("reframe.first_goal", reframe.get("first_goal") == "current_scene_understanding")
    ok(
        "reframe.second_goal",
        reframe.get("second_goal") == "spatiotemporal_continuity_and_world_understanding",
    )
    ok("reframe.third_goal", reframe.get("third_goal") == "navigation_application_layer")
    ok(
        "reframe.fourth_goal",
        reframe.get("fourth_goal")
        == "expanded_application_capabilities_person_recognition_reading_etc",
    )
    ok("reframe.nav_not_first", reframe.get("navigation_is_core_application_not_first_goal") is True)
    ok("reframe.historical", reframe.get("historical_vision_navigation_flow_preserved") is True)
    ok("reframe.pass", reframe.get("reframe_pass") is True)
    for goal in SCENE_UNDERSTANDING_GOALS:
        ok(f"reframe.goal.{goal['goal_id']}", goal in (reframe.get("goals") or []))

    for sid in INTAKE_SAMPLE_IDS:
        ok(f"intake.{sid[:18]}", sid in (intake.get("sample_ids") or []))
    ok("intake.scene_primary", intake.get("scene_understanding_primary") is True)
    ok("intake.nav_app", intake.get("navigation_application_layer_only") is True)
    ok("intake.fixture", intake.get("fixture_metadata_only") is True)

    samples = intake.get("samples") or {}
    target = samples.get("target_recognition_candidate") or {}
    tracking = samples.get("target_tracking_candidate") or {}
    task_intent = samples.get("task_intent_candidate") or {}
    spatiotemporal = samples.get("spatiotemporal_context_candidate") or {}
    world = samples.get("world_continuity_candidate") or {}
    scene_rule = samples.get("scene_rule_candidate") or {}

    for field in TARGET_RECOGNITION_FIELDS:
        ok(f"target_field.{field[:18]}", field in target)
    for field in TARGET_TRACKING_FIELDS:
        ok(f"tracking_field.{field[:18]}", field in tracking)
    for field in TASK_INTENT_FIELDS:
        ok(f"task_intent_field.{field[:18]}", field in task_intent)
    for field in SPATIOTEMPORAL_CONTEXT_FIELDS:
        ok(f"spatiotemporal_field.{field[:18]}", field in spatiotemporal)
    for field in WORLD_CONTINUITY_FIELDS:
        ok(f"world_field.{field[:18]}", field in world)
    for field in SCENE_RULE_FIELDS:
        ok(f"scene_rule_field.{field[:18]}", field in scene_rule)

    ok("samples.route_app", samples.get("route_context_candidate", {}).get("application_layer") is True)
    ok("samples.nav_app", samples.get("navigation_task_candidate", {}).get("application_layer") is True)
    ok("samples.tracking_runtime", tracking.get("runtime_source") is False)

    ok(
        "model.id",
        chain_model.get("model_id") == "first_person_scene_understanding_information_integration_chain_v1",
    )
    ok("model.primary", chain_model.get("primary_goal") == "current_scene_understanding")
    ok("model.secondary", chain_model.get("secondary_goal") == "spatiotemporal_continuity_and_world_understanding")
    ok("model.tertiary", chain_model.get("tertiary_goal") == "navigation_application_layer")
    ok("model.emits_integrated", chain_model.get("emits_integrated_context_candidate") is True)
    ok("model.not_decide", chain_model.get("does_not_decide") is True)

    for field in INTEGRATED_CONTEXT_CANDIDATE_FIELDS:
        ok(f"integrated.{field[:18]}", field in integrated)
    ok("integrated.target_ctx", integrated.get("target_context") is not None)
    ok("integrated.text_ctx", integrated.get("text_context") is not None)
    ok("integrated.tracking_ctx", integrated.get("tracking_context") is not None)
    ok("integrated.task_intent_ctx", integrated.get("task_intent_context") is not None)
    ok("integrated.spatiotemporal_ctx", integrated.get("spatiotemporal_context") is not None)
    ok("integrated.world_ctx", integrated.get("world_continuity_context") is not None)
    ok("integrated.app_ctx", integrated.get("application_context") is not None)
    ok(
        "integrated.app_not_primary",
        integrated.get("application_context", {}).get("not_primary_goal") is True,
    )
    ok(
        "integrated.scene_priority",
        integrated.get("current_scene_context", {}).get("scene_understanding_priority") == "first_goal",
    )
    ok("integrated.candidate", integrated.get("candidate_only") is True)
    ok("integrated.not_decision", integrated.get("not_decision") is True)
    ok("integrated.no_runtime", integrated.get("runtime_enable_allowed") is False)
    ok(
        "integrated.gap_refs",
        "gap_missing_mid_sequence_validation_001" in (integrated.get("context_gap_refs") or []),
    )

    ok("conflict.candidate", conflict.get("candidate_only") is True)
    ok("conflict.decision_req", conflict.get("decision_required") is True)
    ok(
        "gap.missing_seq",
        "missing_mid_sequence_frame_validation" in str(gap.get("missing_source_type", "")),
    )
    ok("gap.candidate", gap.get("candidate_only") is True)

    items = freshness.get("freshness_items") or []
    ok("freshness.count5", len(items) >= 5)
    ok("freshness.all_false", freshness.get("all_can_drive_decision_false") is True)
    for field in FRESHNESS_STATUS_FIELDS:
        ok(f"freshness_field.{field[:18]}", all(field in i for i in items))

    ok("priority.scene_high", priority.get("scene_understanding_priority_weight", 0) >= 0.9)
    ok("priority.nav_low", priority.get("navigation_application_weight", 1) <= 0.6)

    for field in DECISION_READINESS_FIELDS:
        ok(f"readiness.{field[:18]}", field in readiness)
    ok(
        "readiness.status",
        readiness.get("readiness_status") == "not_ready_for_scene_understanding_decision",
    )
    ok("readiness.sufficient_false", readiness.get("sufficient_for_decision") is False)
    ok("readiness.handoff_false", readiness.get("decision_center_handoff_allowed") is False)

    for item in TARGET_RECOGNITION_REVIEW_ITEMS:
        ok(f"target_review.{item[:18]}", target_review.get("dryrun_and_review_pass") is True)
    for item in TEXT_RECOGNITION_REVIEW_ITEMS:
        ok(f"text_review.{item[:18]}", text_review.get("dryrun_and_review_pass") is True)
    for item in TARGET_TRACKING_REVIEW_ITEMS:
        ok(f"tracking_review.{item[:18]}", tracking_review.get("dryrun_and_review_pass") is True)
    for item in TASK_INTENT_TARGET_SEARCH_REVIEW_ITEMS:
        ok(f"task_review.{item[:18]}", task_review.get("dryrun_and_review_pass") is True)
    for item in SPATIOTEMPORAL_CONTINUITY_REVIEW_ITEMS:
        ok(f"spatiotemporal_review.{item[:18]}", spatiotemporal_review.get("dryrun_and_review_pass") is True)
    for item in WORLD_CONTINUITY_REVIEW_ITEMS:
        ok(f"world_review.{item[:18]}", world_review.get("dryrun_and_review_pass") is True)
    for item in SURVIVAL_CONTEXT_REVIEW_ITEMS:
        ok(f"survival_review.{item[:18]}", survival_review.get("dryrun_and_review_pass") is True)
    for item in NAVIGATION_APPLICATION_REVIEW_ITEMS:
        ok(f"nav_review.{item[:18]}", nav_review.get("dryrun_and_review_pass") is True)
    ok("nav_review.app_layer", nav_review.get("application_layer") is True)

    for item in EVIDENCE_TRACEABILITY_REVIEW_ITEMS:
        ok(f"trace_review.{item[:18]}", trace_review.get("dryrun_and_review_pass") is True)
    ok("trace_review.matrix", trace_review.get("source_chain_matrix_present") is True)

    for item in DC_HANDOFF_REVIEW_ITEMS:
        ok(f"dc_handoff.{item[:18]}", dc_handoff.get("dryrun_and_review_pass") is True)
    ok(
        "dc_handoff.no_decision",
        dc_handoff.get("handoff_package", {}).get("decision_candidate_generated") is False,
    )

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count18", blocked.get("blocked_count") == 18)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_decision_chain_candidate_dryrun") is True)
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
        "mainline_reframe_applied": summary.get("mainline_reframe_applied"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
