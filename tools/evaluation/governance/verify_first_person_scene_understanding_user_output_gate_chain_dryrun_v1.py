#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify First Person Scene Understanding User Output Gate Chain DryRun v1."""

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
    FINAL_DECISION_GO as OUTPUT_CAND_DR_FINAL_GO,
    NEXT_PHASE_GO as OUTPUT_CAND_DR_NEXT_PHASE,
)
from capabilities.governance.first_person_scene_understanding_user_output_gate_chain_dryrun_v1 import (
    ALLOWED_PATHS,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONSTITUTION_GATE_RESULT_FIELDS,
    CONSTITUTION_GATE_REVIEW_ITEMS,
    DISPLAY_GATE_RESULT_FIELDS,
    DISPLAY_GATE_REVIEW_ITEMS,
    ENFORCEMENT_RESULT_FIELDS,
    EXECUTION_HANDOFF_ITEMS,
    FINAL_DECISION_GO,
    GATE_CHAIN_MODEL_FIELDS,
    HEALTH_OVERSIGHT_REVIEW_ITEMS,
    MEMORY_WM_TASK_NAV_BLOCK_REVIEW_ITEMS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    NOTIFICATION_DEFERMENT_REVIEW_ITEMS,
    PHASE_ID,
    PRIVACY_IDENTITY_DEFERMENT_REVIEW_ITEMS,
    SAFETY_GATE_RESULT_FIELDS,
    SAFETY_GATE_REVIEW_ITEMS,
    SCOPE,
    SPEECH_GATE_RESULT_FIELDS,
    SPEECH_GATE_REVIEW_ITEMS,
    TRACEABILITY_REVIEW_ITEMS,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID

MIN_CHECKS = 323

REQUIRED = (
    "first_person_scene_understanding_user_output_gate_chain_dryrun_policy_v1.json",
    "output_candidate_input_review_v1.json",
    "gate_coverage_matrix_input_review_v1.json",
    "user_output_gate_chain_model_candidate_v1.json",
    "sample_user_output_constitution_gate_result_candidate_v1.json",
    "sample_safety_gate_result_candidate_v1.json",
    "sample_speech_gate_result_candidate_v1.json",
    "sample_display_gate_result_candidate_v1.json",
    "sample_enforcement_result_candidate_v1.json",
    "constitution_gate_chain_review_v1.json",
    "safety_gate_chain_review_v1.json",
    "speech_gate_chain_review_v1.json",
    "display_gate_chain_review_v1.json",
    "notification_gate_deferment_review_v1.json",
    "memory_worldmodel_task_navigation_gate_block_review_v1.json",
    "privacy_identity_gate_deferment_review_v1.json",
    "health_oversight_gate_chain_review_v1.json",
    "gate_result_traceability_review_v1.json",
    "gate_chain_to_execution_layer_handoff_plan_v1.json",
    "gate_chain_boundary_audit_v1.json",
    "gate_chain_blocked_path_result_v1.json",
    "gate_chain_closure_decision_v1.json",
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
            "first_person_scene_understanding_user_output_gate_chain_dryrun"
        ),
    )
    p.add_argument(
        "--output-candidate-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_output_candidate_dryrun"
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
    p.add_argument(
        "--layered-stack-standard-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "layered_capability_stack_standard_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    output_cand_vr = _load(Path(args.output_candidate_dryrun_root) / "verifier_report.json")
    output_cand_sm = _load(Path(args.output_candidate_dryrun_root) / "summary.json")
    uoc_vr = _load(Path(args.user_output_constitution_dryrun_root) / "verifier_report.json")
    safety_vr = _load(Path(args.safety_gate_dryrun_root) / "verifier_report.json")
    speech_vr = _load(Path(args.speech_gate_dryrun_root) / "verifier_report.json")
    display_vr = _load(Path(args.display_gate_dryrun_root) / "verifier_report.json")
    cb_vr = _load(Path(args.constitution_bus_dryrun_root) / "verifier_report.json")
    stack_vr = _load(Path(args.layered_stack_standard_dryrun_root) / "verifier_report.json")

    ok("upstream.output_cand_go", output_cand_vr.get("verifier") == "GO")
    ok("upstream.output_cand_final", output_cand_sm.get("final_decision") == OUTPUT_CAND_DR_FINAL_GO)
    ok("upstream.output_cand_next", output_cand_sm.get("recommended_next_phase") == OUTPUT_CAND_DR_NEXT_PHASE)
    ok("upstream.uoc_gen", output_cand_sm.get("user_output_candidate_generated_now") is True)
    ok("upstream.no_facing", output_cand_sm.get("user_facing_output_generated_now") is False)
    ok(
        "upstream.gate_matrix",
        (Path(args.output_candidate_dryrun_root) / "first_person_output_gate_chain_coverage_matrix_v1.json").is_file(),
    )
    ok("upstream.uoc_go", uoc_vr.get("verifier") == "GO")
    ok("upstream.safety_go", safety_vr.get("verifier") == "GO")
    ok("upstream.speech_go", speech_vr.get("verifier") == "GO")
    ok("upstream.display_go", display_vr.get("verifier") == "GO")
    ok("upstream.cb_go", cb_vr.get("verifier") == "GO")
    ok("upstream.stack_go", stack_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "first_person_scene_understanding_user_output_gate_chain_dryrun_policy_v1.json")
    output_input = _load(root / "output_candidate_input_review_v1.json")
    gate_input = _load(root / "gate_coverage_matrix_input_review_v1.json")
    model = _load(root / "user_output_gate_chain_model_candidate_v1.json")
    constitution_result = _load(root / "sample_user_output_constitution_gate_result_candidate_v1.json")
    safety_result = _load(root / "sample_safety_gate_result_candidate_v1.json")
    speech_result = _load(root / "sample_speech_gate_result_candidate_v1.json")
    display_result = _load(root / "sample_display_gate_result_candidate_v1.json")
    enforcement = _load(root / "sample_enforcement_result_candidate_v1.json")
    constitution_review = _load(root / "constitution_gate_chain_review_v1.json")
    safety_review = _load(root / "safety_gate_chain_review_v1.json")
    speech_review = _load(root / "speech_gate_chain_review_v1.json")
    display_review = _load(root / "display_gate_chain_review_v1.json")
    notification_review = _load(root / "notification_gate_deferment_review_v1.json")
    memory_block_review = _load(root / "memory_worldmodel_task_navigation_gate_block_review_v1.json")
    privacy_review = _load(root / "privacy_identity_gate_deferment_review_v1.json")
    health_review = _load(root / "health_oversight_gate_chain_review_v1.json")
    trace_review = _load(root / "gate_result_traceability_review_v1.json")
    handoff = _load(root / "gate_chain_to_execution_layer_handoff_plan_v1.json")
    boundary = _load(root / "gate_chain_boundary_audit_v1.json")
    blocked = _load(root / "gate_chain_blocked_path_result_v1.json")
    closure = _load(root / "gate_chain_closure_decision_v1.json")
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

    ok("policy.gate_chain_only", policy.get("gate_chain_dryrun_only_not_user_facing_not_execution") is True)
    ok("policy.gate_system", policy.get("gate_chain_system_ref") == GATE_CHAIN_SYSTEM_ID)

    ok("output_input.pass", output_input.get("review_pass") is True)
    ok("gate_input.pass", gate_input.get("review_pass") is True)
    ok("gate_input.count16", gate_input.get("gate_count") == 16)

    for field in GATE_CHAIN_MODEL_FIELDS:
        ok(f"model.{field[:18]}", field in model)
    ok("model.id", model.get("model_id") == "first_person_scene_understanding_user_output_gate_chain_v1")
    ok("model.no_vop", model.get("does_not_invoke_voice_output_plane") is True)
    ok("model.no_tts", model.get("does_not_invoke_tts") is True)

    for field in CONSTITUTION_GATE_RESULT_FIELDS:
        ok(f"constitution.{field[:18]}", field in constitution_result)
    ok("constitution.gate_id", constitution_result.get("gate_id") == "user_output_constitution_gate")
    ok("constitution.status", constitution_result.get("gate_status") == "pass_with_constraints")
    ok("constitution.safety_next", "safety_gate" in (constitution_result.get("allowed_next_gates") or []))
    ok("constitution.candidate", constitution_result.get("candidate_only") is True)

    for field in SAFETY_GATE_RESULT_FIELDS:
        ok(f"safety.{field[:18]}", field in safety_result)
    ok("safety.gate_id", safety_result.get("gate_id") == "safety_gate")
    ok("safety.status", safety_result.get("safety_status") == "hold_or_observe_more_allowed_candidate")
    ok("safety.survival", safety_result.get("survival_priority_applied") is True)
    ok(
        "safety.blocked_nav",
        "navigation_action_gate" in (safety_result.get("blocked_downstream_gates") or []),
    )

    for field in SPEECH_GATE_RESULT_FIELDS:
        ok(f"speech.{field[:18]}", field in speech_result)
    ok("speech.gate_id", speech_result.get("gate_id") == "speech_gate")
    ok("speech.no_request", speech_result.get("speech_request_candidate_allowed") is False)
    ok("speech.no_vop", speech_result.get("voice_output_plane_allowed") is False)
    ok("speech.no_tts", speech_result.get("tts_allowed") is False)
    ok(
        "speech.blocked_tts",
        "tts_invocation" in (speech_result.get("blocked_speech_actions") or []),
    )

    for field in DISPLAY_GATE_RESULT_FIELDS:
        ok(f"display.{field[:18]}", field in display_result)
    ok("display.gate_id", display_result.get("gate_id") == "display_gate")
    ok("display.no_output", display_result.get("display_output_allowed") is False)
    ok("display.no_notif", display_result.get("notification_allowed") is False)
    ok(
        "display.blocked_notif",
        "notification_now" in (display_result.get("blocked_display_actions") or []),
    )

    for field in ENFORCEMENT_RESULT_FIELDS:
        ok(f"enforcement.{field[:18]}", field in enforcement)
    ok("enforcement.complete", enforcement.get("output_gate_chain_complete_candidate") is True)
    ok("enforcement.no_facing", enforcement.get("user_facing_output_allowed") is False)
    ok("enforcement.no_vop", enforcement.get("voice_output_plane_allowed") is False)
    ok(
        "enforcement.blocked_nav",
        "direct_navigation_instruction" in (enforcement.get("blocked_channel_candidates") or []),
    )
    ok(
        "enforcement.refs4",
        len(enforcement.get("source_gate_result_refs") or []) == 4,
    )

    for item in CONSTITUTION_GATE_REVIEW_ITEMS:
        ok(f"constitution_review.{item[:18]}", constitution_review.get("dryrun_and_review_pass") is True)
    for item in SAFETY_GATE_REVIEW_ITEMS:
        ok(f"safety_review.{item[:18]}", safety_review.get("dryrun_and_review_pass") is True)
    for item in SPEECH_GATE_REVIEW_ITEMS:
        ok(f"speech_review.{item[:18]}", speech_review.get("dryrun_and_review_pass") is True)
    for item in DISPLAY_GATE_REVIEW_ITEMS:
        ok(f"display_review.{item[:18]}", display_review.get("dryrun_and_review_pass") is True)
    for item in NOTIFICATION_DEFERMENT_REVIEW_ITEMS:
        ok(f"notification_review.{item[:18]}", notification_review.get("dryrun_and_review_pass") is True)
    ok("notification.in_matrix", notification_review.get("notification_gate_in_matrix") is True)
    for item in MEMORY_WM_TASK_NAV_BLOCK_REVIEW_ITEMS:
        ok(f"memory_block_review.{item[:18]}", memory_block_review.get("dryrun_and_review_pass") is True)
    for item in PRIVACY_IDENTITY_DEFERMENT_REVIEW_ITEMS:
        ok(f"privacy_review.{item[:18]}", privacy_review.get("dryrun_and_review_pass") is True)
    for item in HEALTH_OVERSIGHT_REVIEW_ITEMS:
        ok(f"health_review.{item[:18]}", health_review.get("dryrun_and_review_pass") is True)
    ok("health.external", health_review.get("health_oversight_external") is True)

    for item in TRACEABILITY_REVIEW_ITEMS:
        ok(f"trace_review.{item[:18]}", trace_review.get("dryrun_and_review_pass") is True)
    ok(
        "trace.uoc_ref",
        trace_review.get("source_user_output_candidate_ref") == "user_output_scene_understanding_chain_001",
    )
    ok(
        "trace.task_resp",
        trace_review.get("source_task_response_candidate_ref") == "task_response_scene_understanding_chain_001",
    )

    for item in EXECUTION_HANDOFF_ITEMS:
        ok(f"handoff.{item[:18]}", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.no_vop", handoff.get("voice_output_plane_invoked_now") is False)
    ok("handoff.no_tts", handoff.get("tts_invoked_now") is False)
    ok("handoff.no_display", handoff.get("display_output_invoked_now") is False)

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count29", blocked.get("blocked_count") == 29)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )
    for path in ALLOWED_PATHS:
        ok(
            f"allowed.{path[:18]}",
            any(
                a.get("path_id") == path
                and a.get("status") == "allowed_candidate_only"
                and a.get("candidate_only") is True
                for a in (blocked.get("allowed_paths") or [])
            ),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_output_chain_closure_review") is True)
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
