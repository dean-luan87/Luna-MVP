#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Speech Gate DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.midplatform_speech_gate_planning_v1 import (
    CHANNEL_ADMISSION_RULES,
    CONTENT_CONSTRAINT_RULES,
    DOWNSTREAM_HANDOFF_MAPPINGS,
    ENFORCEMENT_RESULT_INTAKE_FIELDS,
    EXECUTION_LAYER_BOUNDARY_RULES,
    INTERRUPTION_TIMING_RULES,
    NO_RAW_CONSTITUTION_RULES,
    REFUSAL_HOLD_DEGRADE_MAPPINGS,
    SPEECH_ACTION_TAXONOMY,
    SPEECH_GATE_LAYER_POSITIONING,
    SPEECH_GATE_RESULT_FIELDS,
    TONE_PERSONALIZATION_RULES,
    TRACEABILITY_REQUIREMENTS,
    UNCERTAINTY_DISCLOSURE_RULES,
    USER_OUTPUT_INTAKE_FIELDS,
)

MIN_CHECKS = 272

REQUIRED = (
    "speech_gate_dryrun_review_policy_v1.json",
    "speech_gate_planning_input_review_v1.json",
    "speech_gate_model_candidate_v1.json",
    "sample_enforcement_result_intake_v1.json",
    "sample_user_output_candidate_intake_v1.json",
    "sample_speech_gate_result_candidate_v1.json",
    "speech_enforcement_layer_role_review_v1.json",
    "speech_no_raw_constitution_binding_review_v1.json",
    "speech_action_taxonomy_dryrun_review_v1.json",
    "speech_channel_admission_dryrun_review_v1.json",
    "speech_content_constraint_dryrun_review_v1.json",
    "speech_uncertainty_disclosure_dryrun_review_v1.json",
    "speech_tone_personalization_boundary_review_v1.json",
    "speech_interruption_timing_boundary_review_v1.json",
    "speech_refusal_hold_degrade_dryrun_review_v1.json",
    "speech_downstream_handoff_review_v1.json",
    "speech_execution_layer_boundary_review_v1.json",
    "speech_gate_traceability_review_v1.json",
    "speech_gate_boundary_audit_v1.json",
    "speech_gate_blocked_path_result_v1.json",
    "speech_gate_closure_decision_v1.json",
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
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review",
    )
    p.add_argument(
        "--planning-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_planning",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    summary = _load(root / "summary.json")
    model = _load(root / "speech_gate_model_candidate_v1.json")
    sample_enforcement = _load(root / "sample_enforcement_result_intake_v1.json")
    sample_user = _load(root / "sample_user_output_candidate_intake_v1.json")
    sample_result = _load(root / "sample_speech_gate_result_candidate_v1.json")
    enforcement = _load(root / "speech_enforcement_layer_role_review_v1.json")
    no_raw = _load(root / "speech_no_raw_constitution_binding_review_v1.json")
    actions = _load(root / "speech_action_taxonomy_dryrun_review_v1.json")
    channel = _load(root / "speech_channel_admission_dryrun_review_v1.json")
    content = _load(root / "speech_content_constraint_dryrun_review_v1.json")
    uncertainty = _load(root / "speech_uncertainty_disclosure_dryrun_review_v1.json")
    tone = _load(root / "speech_tone_personalization_boundary_review_v1.json")
    timing = _load(root / "speech_interruption_timing_boundary_review_v1.json")
    refusal = _load(root / "speech_refusal_hold_degrade_dryrun_review_v1.json")
    handoff = _load(root / "speech_downstream_handoff_review_v1.json")
    exec_boundary = _load(root / "speech_execution_layer_boundary_review_v1.json")
    trace = _load(root / "speech_gate_traceability_review_v1.json")
    blocked = _load(root / "speech_gate_blocked_path_result_v1.json")
    closure = _load(root / "speech_gate_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok(
        "upstream.enforcement",
        _load(plan_root / "speech_gate_planning_policy_v1.json").get(
            "speech_gate_is_enforcement_not_execution"
        )
        is True,
    )

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("speech_gate_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.display_defer", summary.get("display_gate_deferred_not_skipped") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("model.id", model.get("module_id") == "midplatform_speech_gate_v1")
    ok("model.type", model.get("module_type") == "midplatform_user_output_gate_module")
    ok("model.role", model.get("role") == "speech_output_enforcement_gate")
    ok("model.arch", model.get("architectural_layer") == "Enforcement")
    ok("model.layer", model.get("system_layer") == "Validation")
    ok("model.runtime_off", model.get("runtime_enabled_now") is False)
    ok("model.consumes_enforcement", model.get("consumes_enforcement_result_candidate") is True)
    ok("model.consumes_user", model.get("consumes_user_output_candidate") is True)
    ok("model.emits_speech", model.get("emits_speech_gate_result_candidate") is True)
    ok("model.no_raw", model.get("reads_raw_constitution_clauses") is False)
    ok("model.no_speech_req", model.get("generates_speech_request") is False)
    ok("model.no_tts", model.get("invokes_tts") is False)
    ok("model.no_voice", model.get("invokes_voice_output_plane") is False)
    ok("model.no_audio", model.get("generates_audio_output") is False)
    ok("model.no_provider", model.get("provider_invocation_allowed") is False)

    upstream_mods = model.get("upstream_modules") or []
    ok("model.up_safety", "safety_gate" in upstream_mods)
    ok("model.up_output", "output_plane_integration" in upstream_mods)
    ok("model.up_resolver", "constitution_resolver" in upstream_mods)

    downstream_mods = model.get("downstream_modules") or []
    ok("model.down_voice", "voice_output_plane_later" in downstream_mods)
    ok("model.down_display", "display_gate_later" in downstream_mods)

    for field in ENFORCEMENT_RESULT_INTAKE_FIELDS:
        ok(f"enforcement.{field[:15]}", field in sample_enforcement)
    ok("enforcement.candidate", sample_enforcement.get("candidate_only") is True)

    for field in USER_OUTPUT_INTAKE_FIELDS:
        ok(f"user.{field[:15]}", field in sample_user)
    ok("user.no_facing", sample_user.get("user_facing_output_allowed") is False)
    ok("user.no_speech_req", sample_user.get("speech_request_allowed") is False)
    ok("user.not_fact", sample_user.get("fact_status") == "not_fact")

    for field in SPEECH_GATE_RESULT_FIELDS:
        ok(f"result.{field[:15]}", field in sample_result)
    ok("result.no_speech_req", sample_result.get("speech_request_allowed") is False)
    ok("result.candidate", sample_result.get("candidate_only") is True)

    ok("enforcement_review.pass", enforcement.get("dryrun_and_review_pass") is True)
    for pos in SPEECH_GATE_LAYER_POSITIONING:
        ok(f"enf_pos.{pos[:18]}", pos in (enforcement.get("speech_gate_layer_positioning") or []))

    ok("no_raw.pass", no_raw.get("dryrun_and_review_pass") is True)
    for rule in NO_RAW_CONSTITUTION_RULES:
        ok(f"noraw.{rule[:18]}", rule in (no_raw.get("rules") or []))

    ok("actions.pass", actions.get("dryrun_and_review_pass") is True)
    ok("actions.count13", actions.get("action_count") == 13)
    ok("actions.all13", actions.get("all_thirteen_actions_covered") is True)
    for action in SPEECH_ACTION_TAXONOMY:
        ok(f"action.{action[:18]}", action in [a.get("speech_gate_action") for a in (actions.get("actions") or [])])

    ok("channel.pass", channel.get("dryrun_and_review_pass") is True)
    for rule in CHANNEL_ADMISSION_RULES:
        ok(f"channel.{rule[:18]}", rule in (channel.get("rules") or []))

    ok("content.pass", content.get("dryrun_and_review_pass") is True)
    for rule in CONTENT_CONSTRAINT_RULES:
        ok(f"content.{rule[:18]}", rule in (content.get("rules") or []))

    ok("uncertainty.pass", uncertainty.get("dryrun_and_review_pass") is True)
    for rule in UNCERTAINTY_DISCLOSURE_RULES:
        ok(f"uncertainty.{rule[:18]}", rule in (uncertainty.get("rules") or []))

    ok("tone.pass", tone.get("dryrun_and_review_pass") is True)
    for rule in TONE_PERSONALIZATION_RULES:
        ok(f"tone.{rule[:18]}", rule in (tone.get("rules") or []))

    ok("timing.pass", timing.get("dryrun_and_review_pass") is True)
    for rule in INTERRUPTION_TIMING_RULES:
        ok(f"timing.{rule[:18]}", rule in (timing.get("rules") or []))

    ok("refusal.pass", refusal.get("dryrun_and_review_pass") is True)
    for m in REFUSAL_HOLD_DEGRADE_MAPPINGS:
        ok(
            f"refusal.{m['safety_signal'][:16]}",
            any(
                x.get("safety_signal") == m["safety_signal"] and x.get("speech_path") == m["speech_path"]
                for x in (refusal.get("mappings") or [])
            ),
        )

    ok("handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.no_runtime", handoff.get("no_downstream_runtime_invoked_now") is True)
    for m in DOWNSTREAM_HANDOFF_MAPPINGS:
        ok(
            f"handoff.{m['speech_action'][:16]}",
            any(
                x.get("speech_action") == m["speech_action"] and x.get("handoff") == m["handoff"]
                for x in (handoff.get("handoffs") or [])
            ),
        )

    ok("exec.pass", exec_boundary.get("dryrun_and_review_pass") is True)
    ok("exec.not_tts", exec_boundary.get("speech_pass_not_speech_request_or_tts") is True)
    for rule in EXECUTION_LAYER_BOUNDARY_RULES:
        ok(f"exec.{rule[:18]}", rule in (exec_boundary.get("rules") or []))

    ok("trace.pass", trace.get("dryrun_and_review_pass") is True)
    for req in TRACEABILITY_REQUIREMENTS:
        ok(f"trace.{req[:18]}", req in (trace.get("requirements") or []))

    ok("audit.pass", _load(root / "speech_gate_boundary_audit_v1.json").get("dryrun_and_review_pass") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count16", blocked.get("blocked_count") == 16)
    for bp in BLOCKED_PATHS:
        ok(
            f"blocked.{bp[:18]}",
            any(x.get("blocked_path") == bp and x.get("blocked") is True for x in (blocked.get("blocked_paths") or [])),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.enforcement", closure.get("speech_enforcement_layer_validated") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next.ready", next_route.get("ready_for_voice_output_plane_roadmap_decision") is True)
    ok("next.no_runtime", next_route.get("speech_gate_runtime_enabled") is False)
    ok("next.display_defer", next_route.get("display_gate_deferred_not_skipped") is True)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("dryrun_and_review_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "dryrun_and_review_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
