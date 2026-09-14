#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify First Person Scene Understanding Output Candidate DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.first_person_scene_understanding_output_candidate_dryrun_v1 import (
    ASSEMBLY_MODEL_FIELDS,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CHANNEL_ELIGIBILITY_REVIEW_ITEMS,
    CONSTITUTION_HANDOFF_ITEMS,
    FINAL_DECISION_GO,
    FORBIDDEN_ACTIONS_REVIEW_ITEMS,
    GATE_COVERAGE_MATRIX_REVIEW_ITEMS,
    GATE_HANDOFF_ITEMS,
    GOVERNANCE_OUTPUT_REVIEW_ITEMS,
    NAVIGATION_OUTPUT_REVIEW_ITEMS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REQUIRED_OBS_OUTPUT_REVIEW_ITEMS,
    SCENE_OUTPUT_REVIEW_ITEMS,
    SCOPE,
    SPATIOTEMPORAL_OUTPUT_REVIEW_ITEMS,
    SURVIVAL_OUTPUT_REVIEW_ITEMS,
    TRACEABILITY_REVIEW_ITEMS,
    UNCERTAINTY_OUTPUT_REVIEW_ITEMS,
    USER_OUTPUT_CANDIDATE_FIELDS,
)
from capabilities.governance.first_person_scene_understanding_task_response_candidate_dryrun_v1 import (
    FINAL_DECISION_GO as TASK_RESP_DR_FINAL_GO,
    NEXT_PHASE_GO as TASK_RESP_DR_NEXT_PHASE,
)
from capabilities.governance.layered_capability_stack_standard_v1 import (
    GOVERNANCE_ADDENDUM_ID,
    STANDARD_ID,
)
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import (
    GATE_CHAIN_REQUIREMENTS,
    GATE_ENTRY_FIELDS,
    GATE_TYPES,
    SYSTEM_ID as GATE_CHAIN_SYSTEM_ID,
)

MIN_CHECKS = 542

REQUIRED = (
    "first_person_scene_understanding_output_candidate_dryrun_policy_v1.json",
    "task_response_candidate_input_review_v1.json",
    "layered_stack_and_governance_mapping_input_review_v1.json",
    "output_candidate_assembly_model_candidate_v1.json",
    "sample_user_output_candidate_v1.json",
    "output_candidate_channel_eligibility_review_v1.json",
    "scene_understanding_output_candidate_review_v1.json",
    "spatiotemporal_output_candidate_review_v1.json",
    "navigation_application_output_candidate_review_v1.json",
    "survival_priority_output_candidate_review_v1.json",
    "required_observation_output_candidate_review_v1.json",
    "forbidden_actions_output_candidate_review_v1.json",
    "uncertainty_disclosure_output_candidate_review_v1.json",
    "layered_governance_mapping_output_review_v1.json",
    "user_output_constitution_handoff_plan_v1.json",
    "safety_speech_display_gate_handoff_plan_v1.json",
    "first_person_output_gate_chain_coverage_matrix_v1.json",
    "output_candidate_traceability_review_v1.json",
    "output_candidate_boundary_audit_v1.json",
    "output_candidate_blocked_path_result_v1.json",
    "output_candidate_closure_decision_v1.json",
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
            "first_person_scene_understanding_output_candidate_dryrun"
        ),
    )
    p.add_argument(
        "--task-response-dryrun-root",
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
        "--layered-stack-standard-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "layered_capability_stack_standard_planning"
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
        "--user-output-constitution-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_user_output_constitution_dryrun_and_review"
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
        "--speech-gate-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_speech_gate_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--display-gate-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_display_gate_dryrun_and_review"
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

    task_resp_vr = _load(Path(args.task_response_dryrun_root) / "verifier_report.json")
    task_resp_sm = _load(Path(args.task_response_dryrun_root) / "summary.json")
    decision_vr = _load(Path(args.decision_chain_dryrun_root) / "verifier_report.json")
    stack_vr = _load(Path(args.layered_stack_standard_dryrun_root) / "verifier_report.json")
    stack_plan_gov = _load(
        Path(args.layered_stack_standard_planning_root) / "layered_governance_mapping_addendum_v1.json"
    )
    output_plane_vr = _load(Path(args.output_plane_integration_dryrun_root) / "verifier_report.json")
    uoc_vr = _load(Path(args.user_output_constitution_dryrun_root) / "verifier_report.json")
    safety_vr = _load(Path(args.safety_gate_dryrun_root) / "verifier_report.json")
    speech_vr = _load(Path(args.speech_gate_dryrun_root) / "verifier_report.json")
    display_vr = _load(Path(args.display_gate_dryrun_root) / "verifier_report.json")
    cb_vr = _load(Path(args.constitution_bus_dryrun_root) / "verifier_report.json")

    ok("upstream.task_resp_go", task_resp_vr.get("verifier") == "GO")
    ok("upstream.task_resp_final", task_resp_sm.get("final_decision") == TASK_RESP_DR_FINAL_GO)
    ok("upstream.task_resp_next", task_resp_sm.get("recommended_next_phase") == TASK_RESP_DR_NEXT_PHASE)
    ok("upstream.task_resp_gen", task_resp_sm.get("task_response_candidate_generated_now") is True)
    ok("upstream.no_uoc_gen", task_resp_sm.get("user_output_candidate_generated_now") is False)
    ok(
        "upstream.governance_map",
        (Path(args.task_response_dryrun_root) / "layered_governance_mapping_v1.json").is_file(),
    )
    ok("upstream.decision_go", decision_vr.get("verifier") == "GO")
    ok("upstream.stack_std_go", stack_vr.get("verifier") == "GO")
    ok("upstream.gov_addendum", stack_plan_gov.get("addendum_id") == GOVERNANCE_ADDENDUM_ID)
    ok("upstream.output_plane_go", output_plane_vr.get("verifier") == "GO")
    ok("upstream.uoc_go", uoc_vr.get("verifier") == "GO")
    ok("upstream.safety_go", safety_vr.get("verifier") == "GO")
    ok("upstream.speech_go", speech_vr.get("verifier") == "GO")
    ok("upstream.display_go", display_vr.get("verifier") == "GO")
    ok("upstream.cb_go", cb_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "first_person_scene_understanding_output_candidate_dryrun_policy_v1.json")
    task_input = _load(root / "task_response_candidate_input_review_v1.json")
    stack_gov_input = _load(root / "layered_stack_and_governance_mapping_input_review_v1.json")
    model = _load(root / "output_candidate_assembly_model_candidate_v1.json")
    output = _load(root / "sample_user_output_candidate_v1.json")
    channel_review = _load(root / "output_candidate_channel_eligibility_review_v1.json")
    scene_review = _load(root / "scene_understanding_output_candidate_review_v1.json")
    spatiotemporal_review = _load(root / "spatiotemporal_output_candidate_review_v1.json")
    nav_review = _load(root / "navigation_application_output_candidate_review_v1.json")
    survival_review = _load(root / "survival_priority_output_candidate_review_v1.json")
    required_review = _load(root / "required_observation_output_candidate_review_v1.json")
    forbidden_review = _load(root / "forbidden_actions_output_candidate_review_v1.json")
    uncertainty_review = _load(root / "uncertainty_disclosure_output_candidate_review_v1.json")
    gov_review = _load(root / "layered_governance_mapping_output_review_v1.json")
    constitution_handoff = _load(root / "user_output_constitution_handoff_plan_v1.json")
    gate_handoff = _load(root / "safety_speech_display_gate_handoff_plan_v1.json")
    gate_matrix = _load(root / "first_person_output_gate_chain_coverage_matrix_v1.json")
    trace_review = _load(root / "output_candidate_traceability_review_v1.json")
    boundary = _load(root / "output_candidate_boundary_audit_v1.json")
    blocked = _load(root / "output_candidate_blocked_path_result_v1.json")
    closure = _load(root / "output_candidate_closure_decision_v1.json")
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

    ok("policy.output_candidate_only", policy.get("user_output_candidate_only_not_user_facing_not_runtime") is True)
    ok("policy.stack_ref", bool(policy.get("capability_stack_ref")))
    ok("policy.universal_ref", policy.get("universal_stack_standard_ref") == STANDARD_ID)
    ok("policy.governance_ref", policy.get("layered_governance_mapping_ref") == ADDENDUM_ID)
    ok("policy.gov_addendum", policy.get("governance_addendum_ref") == GOVERNANCE_ADDENDUM_ID)
    ok("policy.gate_chain_ref", policy.get("gate_chain_system_ref") == GATE_CHAIN_SYSTEM_ID)

    ok("task_input.pass", task_input.get("review_pass") is True)
    ok("stack_gov_input.pass", stack_gov_input.get("review_pass") is True)
    ok("stack_gov_input.mapping", stack_gov_input.get("layered_governance_mapping_ref") == ADDENDUM_ID)

    for field in ASSEMBLY_MODEL_FIELDS:
        ok(f"model.{field[:18]}", field in model)
    ok("model.id", model.get("model_id") == "first_person_scene_understanding_output_candidate_assembly_v1")
    ok("model.type", model.get("model_type") == "user_output_candidate_assembly")
    ok("model.no_facing", model.get("does_not_generate_user_facing_output") is True)
    ok("model.no_safety", model.get("does_not_invoke_safety_gate") is True)
    ok("model.no_speech", model.get("does_not_invoke_speech_gate") is True)
    ok("model.no_display", model.get("does_not_invoke_display_gate") is True)
    ok("model.no_tts", model.get("does_not_invoke_tts") is True)

    for field in USER_OUTPUT_CANDIDATE_FIELDS:
        ok(f"output.{field[:18]}", field in output)
    ok("output.id", output.get("user_output_candidate_id") == "user_output_scene_understanding_chain_001")
    ok(
        "output.task_resp_ref",
        output.get("source_task_response_candidate_ref") == "task_response_scene_understanding_chain_001",
    )
    ok("output.status", output.get("output_status") == "candidate_prepared")
    ok("output.scope", output.get("output_scope") == "first_person_scene_understanding")
    ok("output.intent", output.get("output_intent") == "explain_need_for_more_observation_candidate")
    ok("output.primary", output.get("primary_goal") == "current_scene_understanding")
    ok(
        "output.secondary",
        output.get("secondary_goal") == "spatiotemporal_continuity_and_world_understanding",
    )
    ok("output.application", output.get("application_goal") == "navigation_application_layer")
    ok("output.governance_ref", output.get("layered_governance_mapping_ref") == ADDENDUM_ID)
    ok(
        "output.message",
        "缺少实时画面验证" in str(output.get("candidate_message_summary", "")),
    )
    ok(
        "output.uncertainty",
        "不足以支持真实导航动作" in str(output.get("uncertainty_disclosure_candidate", "")),
    )
    ok("output.no_facing", output.get("user_facing_output_allowed") is False)
    ok("output.no_speech", output.get("speech_output_allowed") is False)
    ok("output.no_display", output.get("display_output_allowed") is False)
    ok("output.no_notification", output.get("notification_allowed") is False)
    ok("output.no_runtime", output.get("runtime_enable_allowed") is False)
    ok("output.candidate", output.get("candidate_only") is True)
    ok("output.not_final", output.get("not_final_output") is True)
    ok("output.constitution_req", output.get("user_output_constitution_required") is True)
    ok("output.safety_req", output.get("safety_gate_required") is True)
    ok(
        "output.required_obs",
        "live_scene_validation_later" in (output.get("required_observation") or []),
    )
    ok(
        "output.allowed_channels",
        "speech_candidate_later" in (output.get("allowed_channel_candidates") or []),
    )
    ok(
        "output.blocked_channels",
        "notification_now" in (output.get("blocked_channel_candidates") or []),
    )
    ok(
        "output.gate_chain_req",
        output.get("gate_chain_requirements") == list(GATE_CHAIN_REQUIREMENTS),
    )
    ok("output.gate_chain_ref", output.get("gate_chain_system_ref") == GATE_CHAIN_SYSTEM_ID)
    ok("output.no_gate_result", output.get("gate_result_candidate_generated_now") is False)
    ok("output.no_enforcement", output.get("enforcement_result_candidate_generated_now") is False)

    for item in CHANNEL_ELIGIBILITY_REVIEW_ITEMS:
        ok(f"channel_review.{item[:18]}", channel_review.get("dryrun_and_review_pass") is True)
    for item in SCENE_OUTPUT_REVIEW_ITEMS:
        ok(f"scene_review.{item[:18]}", scene_review.get("dryrun_and_review_pass") is True)
    for item in SPATIOTEMPORAL_OUTPUT_REVIEW_ITEMS:
        ok(f"spatiotemporal_review.{item[:18]}", spatiotemporal_review.get("dryrun_and_review_pass") is True)
    for item in NAVIGATION_OUTPUT_REVIEW_ITEMS:
        ok(f"nav_review.{item[:18]}", nav_review.get("dryrun_and_review_pass") is True)
    for item in SURVIVAL_OUTPUT_REVIEW_ITEMS:
        ok(f"survival_review.{item[:18]}", survival_review.get("dryrun_and_review_pass") is True)
    for item in REQUIRED_OBS_OUTPUT_REVIEW_ITEMS:
        ok(f"required_review.{item[:18]}", required_review.get("dryrun_and_review_pass") is True)

    for item in FORBIDDEN_ACTIONS_REVIEW_ITEMS:
        ok(
            f"forbidden.{item[:18]}",
            item in (output.get("forbidden_actions") or []),
        )
    ok("forbidden_review.pass", forbidden_review.get("dryrun_and_review_pass") is True)

    for item in UNCERTAINTY_OUTPUT_REVIEW_ITEMS:
        ok(f"uncertainty_review.{item[:18]}", uncertainty_review.get("dryrun_and_review_pass") is True)
    ok(
        "uncertainty.safety_not_output",
        output.get("safety_disclosure_candidate", {}).get("not_user_facing_output") is True,
    )

    for item in GOVERNANCE_OUTPUT_REVIEW_ITEMS:
        ok(f"gov_review.{item[:18]}", gov_review.get("dryrun_and_review_pass") is True)
    ok("gov_review.l4_deferred", gov_review.get("layer_4_deferred") is True)
    ok("gov_review.l5_later", gov_review.get("layer_5_later") is True)

    for item in CONSTITUTION_HANDOFF_ITEMS:
        ok(f"constitution_handoff.{item[:18]}", constitution_handoff.get("dryrun_and_review_pass") is True)
    ok("constitution_handoff.not_now", constitution_handoff.get("user_output_constitution_invoked_now") is False)

    for item in GATE_HANDOFF_ITEMS:
        ok(f"gate_handoff.{item[:18]}", gate_handoff.get("dryrun_and_review_pass") is True)
    ok("gate_handoff.no_safety", gate_handoff.get("safety_gate_invoked_now") is False)
    ok("gate_handoff.no_speech", gate_handoff.get("speech_gate_invoked_now") is False)
    ok("gate_handoff.no_display", gate_handoff.get("display_gate_invoked_now") is False)
    ok("gate_handoff.chain_ref", gate_handoff.get("gate_chain_system_ref") == GATE_CHAIN_SYSTEM_ID)

    ok("gate_matrix.pass", gate_matrix.get("dryrun_and_review_pass") is True)
    ok("gate_matrix.system", gate_matrix.get("gate_chain_system_id") == GATE_CHAIN_SYSTEM_ID)
    ok("gate_matrix.gates16", gate_matrix.get("gate_count") == 16)
    ok("gate_matrix.no_gate_result", gate_matrix.get("gate_result_candidate_generated_now") is False)
    ok("gate_matrix.no_enforcement", gate_matrix.get("enforcement_result_candidate_generated_now") is False)
    ok("gate_matrix.health_external", gate_matrix.get("health_oversight_external_to_constitution_bus") is True)
    ok("gate_matrix.admission_blocked", gate_matrix.get("admission_gates_blocked_now") is True)
    ok(
        "gate_matrix.requirements",
        gate_matrix.get("gate_chain_requirements") == list(GATE_CHAIN_REQUIREMENTS),
    )
    for gt in GATE_TYPES:
        ok(f"gate_matrix.type.{gt[:12]}", gt in (gate_matrix.get("gate_types") or []))
    for item in GATE_COVERAGE_MATRIX_REVIEW_ITEMS:
        ok(f"gate_matrix.confirm.{item[:18]}", gate_matrix.get("dryrun_and_review_pass") is True)
    for idx, gate in enumerate(gate_matrix.get("gates") or []):
        for field in GATE_ENTRY_FIELDS:
            ok(f"gate_matrix.g{idx + 1}.{field[:12]}", field in gate)
        ok(f"gate_matrix.g{idx + 1}.not_invoked", gate.get("invoked_now") is False)

    for item in TRACEABILITY_REVIEW_ITEMS:
        ok(f"trace_review.{item[:18]}", trace_review.get("dryrun_and_review_pass") is True)
    ok(
        "trace.decision_ref",
        trace_review.get("source_decision_candidate_ref") == "decision_candidate_scene_understanding_chain_001",
    )
    ok(
        "trace.integrated_ref",
        trace_review.get("source_integrated_context_ref") == "integrated_context_scene_understanding_chain_001",
    )

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    ok("boundary.uoc_gen", boundary.get("user_output_candidate_generated_now") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count32", blocked.get("blocked_count") == 32)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )
    ok(
        "blocked.allowed_uoc",
        any(
            a.get("path_id") == "dryrun_to_user_output_candidate_generation"
            and a.get("status") == "allowed_candidate_only"
            and a.get("candidate_only") is True
            and a.get("not_final_output") is True
            for a in (blocked.get("allowed_paths") or [])
        ),
    )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_user_output_gate_chain_dryrun") is True)
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
