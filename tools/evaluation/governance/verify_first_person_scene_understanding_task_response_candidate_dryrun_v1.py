#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify First Person Scene Understanding Task Response Candidate DryRun v1."""

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
    FINAL_DECISION_GO as DECISION_DR_FINAL_GO,
    NEXT_PHASE_GO as DECISION_DR_NEXT_PHASE,
)
from capabilities.governance.first_person_scene_understanding_task_response_candidate_dryrun_v1 import (
    ASSEMBLY_MODEL_FIELDS,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CAPABILITY_STACK_PRESERVATION_REVIEW_ITEMS,
    FINAL_DECISION_GO,
    FORBIDDEN_ACTIONS_REVIEW_ITEMS,
    GOVERNANCE_MAPPING_REVIEW_ITEMS,
    NAVIGATION_APP_TASK_RESPONSE_REVIEW_ITEMS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_HANDOFF_ITEMS,
    PHASE_ID,
    REQUIRED_OBS_TASK_RESPONSE_REVIEW_ITEMS,
    SCENE_TASK_RESPONSE_REVIEW_ITEMS,
    SCOPE,
    SPATIOTEMPORAL_TASK_RESPONSE_REVIEW_ITEMS,
    SURVIVAL_TASK_RESPONSE_REVIEW_ITEMS,
    TASK_RESPONSE_CANDIDATE_FIELDS,
    TRACEABILITY_REVIEW_ITEMS,
    UNCERTAINTY_DISCLOSURE_REVIEW_ITEMS,
)
from capabilities.governance.layered_capability_stack_standard_v1 import (
    GOVERNANCE_ADDENDUM_ID,
    MODULE_SUBMISSION_ARTIFACTS,
    STANDARD_ID,
)
from capabilities.governance.layered_governance_mapping_v1 import (
    ADDENDUM_ID,
    EXTENDS_STANDARD_ID,
    GOVERNANCE_MAPPING_LAYER_FIELDS,
    HARD_RULES,
)

MIN_CHECKS = 331

REQUIRED = (
    "first_person_scene_understanding_task_response_dryrun_policy_v1.json",
    "decision_candidate_input_review_v1.json",
    "layered_capability_stack_input_review_v1.json",
    "layered_governance_mapping_v1.json",
    "layered_governance_mapping_review_v1.json",
    "first_person_task_response_assembly_model_candidate_v1.json",
    "sample_task_response_candidate_v1.json",
    "capability_stack_preservation_review_v1.json",
    "scene_understanding_task_response_review_v1.json",
    "spatiotemporal_task_response_review_v1.json",
    "navigation_application_task_response_review_v1.json",
    "survival_priority_task_response_review_v1.json",
    "required_observation_task_response_review_v1.json",
    "forbidden_actions_preservation_review_v1.json",
    "uncertainty_disclosure_candidate_review_v1.json",
    "task_response_to_output_plane_handoff_plan_v1.json",
    "task_response_traceability_review_v1.json",
    "task_response_boundary_audit_v1.json",
    "task_response_blocked_path_result_v1.json",
    "task_response_closure_decision_v1.json",
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
            "first_person_scene_understanding_task_response_candidate_dryrun"
        ),
    )
    p.add_argument(
        "--decision-chain-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_decision_chain_candidate_dryrun"
        ),
    )
    p.add_argument(
        "--layered-stack-standard-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "layered_capability_stack_standard_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--task-response-integration-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_task_response_candidate_integration_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--output-plane-integration-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_output_plane_integration_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--constitution-bus-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    decision_vr = _load(Path(args.decision_chain_dryrun_root) / "verifier_report.json")
    decision_sm = _load(Path(args.decision_chain_dryrun_root) / "summary.json")
    stack_vr = _load(Path(args.layered_stack_standard_dryrun_root) / "verifier_report.json")
    task_resp_vr = _load(Path(args.task_response_integration_dryrun_root) / "verifier_report.json")
    output_plane_vr = _load(Path(args.output_plane_integration_dryrun_root) / "verifier_report.json")
    cb_vr = _load(Path(args.constitution_bus_dryrun_root) / "verifier_report.json")

    ok("upstream.decision_go", decision_vr.get("verifier") == "GO")
    ok("upstream.decision_final", decision_sm.get("final_decision") == DECISION_DR_FINAL_GO)
    ok("upstream.decision_next", decision_sm.get("recommended_next_phase") == DECISION_DR_NEXT_PHASE)
    ok(
        "upstream.fp_stack",
        (Path(args.decision_chain_dryrun_root) / "first_person_capability_stack_governance_v1.json").is_file(),
    )
    ok("upstream.stack_std_go", stack_vr.get("verifier") == "GO")
    ok("upstream.task_resp_go", task_resp_vr.get("verifier") == "GO")
    ok("upstream.output_plane_go", output_plane_vr.get("verifier") == "GO")
    ok("upstream.cb_go", cb_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "first_person_scene_understanding_task_response_dryrun_policy_v1.json")
    decision_input = _load(root / "decision_candidate_input_review_v1.json")
    stack_input = _load(root / "layered_capability_stack_input_review_v1.json")
    governance_mapping = _load(root / "layered_governance_mapping_v1.json")
    governance_mapping_review = _load(root / "layered_governance_mapping_review_v1.json")
    model = _load(root / "first_person_task_response_assembly_model_candidate_v1.json")
    response = _load(root / "sample_task_response_candidate_v1.json")
    stack_review = _load(root / "capability_stack_preservation_review_v1.json")
    scene_review = _load(root / "scene_understanding_task_response_review_v1.json")
    spatiotemporal_review = _load(root / "spatiotemporal_task_response_review_v1.json")
    nav_review = _load(root / "navigation_application_task_response_review_v1.json")
    survival_review = _load(root / "survival_priority_task_response_review_v1.json")
    required_review = _load(root / "required_observation_task_response_review_v1.json")
    forbidden_review = _load(root / "forbidden_actions_preservation_review_v1.json")
    uncertainty_review = _load(root / "uncertainty_disclosure_candidate_review_v1.json")
    handoff = _load(root / "task_response_to_output_plane_handoff_plan_v1.json")
    trace_review = _load(root / "task_response_traceability_review_v1.json")
    boundary = _load(root / "task_response_boundary_audit_v1.json")
    blocked = _load(root / "task_response_blocked_path_result_v1.json")
    closure = _load(root / "task_response_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.task_resp_only", policy.get("task_response_candidate_only_not_output_not_runtime") is True)
    ok("policy.stack_ref", bool(policy.get("capability_stack_ref")))
    ok("policy.universal_ref", policy.get("universal_stack_standard_ref") == STANDARD_ID)
    ok("policy.governance_ref", policy.get("layered_governance_mapping_ref") == ADDENDUM_ID)
    ok("policy.governance_addendum", policy.get("governance_addendum_ref") == GOVERNANCE_ADDENDUM_ID)

    ok("decision_input.pass", decision_input.get("review_pass") is True)
    ok("stack_input.pass", stack_input.get("review_pass") is True)
    ok("stack_input.universal", stack_input.get("universal_standard_ref") == STANDARD_ID)

    ok("mapping.id", governance_mapping.get("mapping_id") == ADDENDUM_ID)
    ok("mapping.extends", governance_mapping.get("extends_universal_standard_ref") == EXTENDS_STANDARD_ID)
    ok("mapping.stack_ref", bool(governance_mapping.get("capability_stack_ref")))
    ok("mapping.mainline", governance_mapping.get("mainline") == "first_person_scene_understanding")
    ok("mapping.layers5", len(governance_mapping.get("layers") or []) == 5)
    ok("mapping.hard_rules10", len(governance_mapping.get("hard_rules") or []) == len(HARD_RULES))
    ok("mapping.active3", len(governance_mapping.get("active_layers_now") or []) == 3)
    ok("mapping.deferred2", len(governance_mapping.get("deferred_layers") or []) == 2)
    ok(
        "mapping.submission_dual",
        set(governance_mapping.get("module_submission_requirements") or [])
        == set(MODULE_SUBMISSION_ARTIFACTS),
    )
    for idx, layer in enumerate(governance_mapping.get("layers") or []):
        for field in GOVERNANCE_MAPPING_LAYER_FIELDS:
            ok(f"mapping.layer{idx + 1}.{field[:12]}", field in layer and bool(layer.get(field)))

    ok("mapping_review.pass", governance_mapping_review.get("dryrun_and_review_pass") is True)
    ok("mapping_review.ref", governance_mapping_review.get("layered_governance_mapping_ref") == ADDENDUM_ID)
    ok("mapping_review.l4_deferred", governance_mapping_review.get("layer_4_deferred") is True)
    ok("mapping_review.l5_later", governance_mapping_review.get("layer_5_later") is True)
    for item in GOVERNANCE_MAPPING_REVIEW_ITEMS:
        ok(f"mapping_review.{item[:18]}", governance_mapping_review.get("dryrun_and_review_pass") is True)

    for field in ASSEMBLY_MODEL_FIELDS:
        ok(f"model.{field[:18]}", field in model)
    ok("model.id", model.get("model_id") == "first_person_scene_understanding_task_response_assembly_v1")
    ok("model.type", model.get("model_type") == "task_response_candidate_assembly")
    ok("model.no_output", model.get("does_not_generate_user_output") is True)
    ok("model.no_gate", model.get("does_not_invoke_output_gate") is True)

    for field in TASK_RESPONSE_CANDIDATE_FIELDS:
        ok(f"response.{field[:18]}", field in response)
    ok("response.id", response.get("task_response_candidate_id") == "task_response_scene_understanding_chain_001")
    ok(
        "response.decision_ref",
        response.get("source_decision_candidate_ref") == "decision_candidate_scene_understanding_chain_001",
    )
    ok("response.status", response.get("response_status") == "observe_more_candidate")
    ok("response.scope", response.get("response_scope") == "first_person_scene_understanding")
    ok("response.primary", response.get("primary_goal") == "current_scene_understanding")
    ok(
        "response.secondary",
        response.get("secondary_goal") == "spatiotemporal_continuity_and_world_understanding",
    )
    ok("response.application", response.get("application_goal") == "navigation_application_layer")
    ok("response.intent", response.get("response_intent") == "explain_need_for_more_observation_later")
    ok("response.scene_summary", "缺少实时画面验证" in str(response.get("scene_understanding_summary_candidate", "")))
    ok("response.nav_summary", "Layer 3" in str(response.get("navigation_application_context_summary_candidate", "")))
    ok("response.no_output", response.get("user_output_allowed") is False)
    ok("response.no_speech", response.get("speech_output_allowed") is False)
    ok("response.no_display", response.get("display_output_allowed") is False)
    ok("response.no_runtime", response.get("runtime_enable_allowed") is False)
    ok("response.candidate", response.get("candidate_only") is True)
    ok("response.governance_ref", response.get("layered_governance_mapping_ref") == ADDENDUM_ID)
    ok(
        "response.required_obs",
        "live_scene_validation_later" in (response.get("required_observation") or []),
    )

    for item in CAPABILITY_STACK_PRESERVATION_REVIEW_ITEMS:
        ok(f"stack_review.{item[:18]}", stack_review.get("dryrun_and_review_pass") is True)
    ok("stack_review.universal", stack_review.get("universal_standard_ref") == STANDARD_ID)
    ok("stack_review.governance_ref", stack_review.get("layered_governance_mapping_ref") == ADDENDUM_ID)

    for item in SCENE_TASK_RESPONSE_REVIEW_ITEMS:
        ok(f"scene_review.{item[:18]}", scene_review.get("dryrun_and_review_pass") is True)
    for item in SPATIOTEMPORAL_TASK_RESPONSE_REVIEW_ITEMS:
        ok(f"spatiotemporal_review.{item[:18]}", spatiotemporal_review.get("dryrun_and_review_pass") is True)
    for item in NAVIGATION_APP_TASK_RESPONSE_REVIEW_ITEMS:
        ok(f"nav_review.{item[:18]}", nav_review.get("dryrun_and_review_pass") is True)
    ok("nav_review.mark_not_ready", nav_review.get("mark_not_ready") is True)

    for item in SURVIVAL_TASK_RESPONSE_REVIEW_ITEMS:
        ok(f"survival_review.{item[:18]}", survival_review.get("dryrun_and_review_pass") is True)
    for item in REQUIRED_OBS_TASK_RESPONSE_REVIEW_ITEMS:
        ok(f"required_review.{item[:18]}", required_review.get("dryrun_and_review_pass") is True)

    for item in FORBIDDEN_ACTIONS_REVIEW_ITEMS:
        ok(
            f"forbidden.{item[:18]}",
            item in (response.get("forbidden_actions") or []),
        )
    ok("forbidden_review.pass", forbidden_review.get("dryrun_and_review_pass") is True)

    for item in UNCERTAINTY_DISCLOSURE_REVIEW_ITEMS:
        ok(f"uncertainty_review.{item[:18]}", uncertainty_review.get("dryrun_and_review_pass") is True)
    ok("uncertainty.disclosure", response.get("disclosure_candidate", {}).get("not_user_output") is True)

    for item in OUTPUT_HANDOFF_ITEMS:
        ok(f"handoff.{item[:18]}", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.no_user_output", handoff.get("user_output_candidate_generated_now") is False)

    for item in TRACEABILITY_REVIEW_ITEMS:
        ok(f"trace_review.{item[:18]}", trace_review.get("dryrun_and_review_pass") is True)
    ok(
        "trace.integrated_ref",
        trace_review.get("source_integrated_context_ref") == "integrated_context_scene_understanding_chain_001",
    )

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    ok("boundary.task_resp_gen", boundary.get("task_response_candidate_generated_now") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count20", blocked.get("blocked_count") == 20)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )
    ok(
        "blocked.allowed_task_resp",
        any(
            a.get("path_id") == "dryrun_to_task_response_candidate_generation"
            and a.get("status") == "allowed_candidate_only"
            for a in (blocked.get("allowed_paths") or [])
        ),
    )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_output_candidate_dryrun") is True)
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
