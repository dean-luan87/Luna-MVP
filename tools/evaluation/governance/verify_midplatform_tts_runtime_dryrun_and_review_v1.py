#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform TTS Runtime DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_tts_runtime_dryrun_and_review_v1 import (
    AUDIO_SYNTHESIS_DRYRUN_RULES,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
    FAILURE_ROUTE_MAPPINGS,
    FINAL_DECISION_GO,
    FUTURE_PROVIDER_CANDIDATES,
    HARNESS_ID,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PROVIDER_ABSTRACTION_DRYRUN_RULES,
    PROVIDER_READINESS_RULES,
    PROVIDER_SWITCH_BOUNDARY_RULES,
    SCOPE,
    SPEECH_GATE_NON_BYPASS_RULES,
    TRACEABILITY_DRYRUN_REQUIREMENTS,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    AUDIO_ARTIFACT_CANDIDATE_FIELDS,
    AUDIO_PLAYBACK_BOUNDARY_RULES,
    AUTHORIZATION_REQUIREMENTS,
    CACHE_ARTIFACT_BOUNDARY_RULES,
    NO_RAW_CONSTITUTION_RULES,
    SPEECH_REQUEST_INTAKE_FIELDS,
    TTS_RUNTIME_LAYER_POSITIONING,
    VOICE_MODEL_BOUNDARY_RULES,
    VOICE_PROFILE_BOUNDARY_RULES,
)

MIN_CHECKS = 324

REQUIRED = (
    "tts_runtime_dryrun_review_policy_v1.json",
    "tts_runtime_planning_input_review_v1.json",
    "tts_runtime_model_candidate_v1.json",
    "sample_speech_request_candidate_intake_v1.json",
    "sample_audio_artifact_candidate_v1.json",
    "tts_provider_abstraction_dryrun_review_v1.json",
    "current_tts_provider_candidate_review_v1.json",
    "provider_switch_boundary_dryrun_review_v1.json",
    "provider_readiness_requirement_review_v1.json",
    "voice_model_boundary_review_v1.json",
    "voice_profile_personalization_boundary_review_v1.json",
    "audio_synthesis_boundary_review_v1.json",
    "audio_output_playback_boundary_review_v1.json",
    "cache_artifact_boundary_review_v1.json",
    "authorization_requirement_review_v1.json",
    "tts_failure_route_review_v1.json",
    "tts_traceability_audit_review_v1.json",
    "tts_no_raw_constitution_review_v1.json",
    "tts_speech_gate_non_bypass_review_v1.json",
    "tts_runtime_boundary_audit_v1.json",
    "tts_runtime_blocked_path_result_v1.json",
    "tts_runtime_closure_decision_v1.json",
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
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_dryrun_and_review",
    )
    p.add_argument(
        "--planning-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_planning",
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
    policy = _load(root / "tts_runtime_dryrun_review_policy_v1.json")
    input_review = _load(root / "tts_runtime_planning_input_review_v1.json")
    model = _load(root / "tts_runtime_model_candidate_v1.json")
    sample_intake = _load(root / "sample_speech_request_candidate_intake_v1.json")
    sample_audio = _load(root / "sample_audio_artifact_candidate_v1.json")
    pabs = _load(root / "tts_provider_abstraction_dryrun_review_v1.json")
    qianwen = _load(root / "current_tts_provider_candidate_review_v1.json")
    pswitch = _load(root / "provider_switch_boundary_dryrun_review_v1.json")
    readiness = _load(root / "provider_readiness_requirement_review_v1.json")
    vmodel = _load(root / "voice_model_boundary_review_v1.json")
    vprofile = _load(root / "voice_profile_personalization_boundary_review_v1.json")
    synthesis = _load(root / "audio_synthesis_boundary_review_v1.json")
    playback = _load(root / "audio_output_playback_boundary_review_v1.json")
    cache = _load(root / "cache_artifact_boundary_review_v1.json")
    auth = _load(root / "authorization_requirement_review_v1.json")
    failure = _load(root / "tts_failure_route_review_v1.json")
    trace = _load(root / "tts_traceability_audit_review_v1.json")
    no_raw = _load(root / "tts_no_raw_constitution_review_v1.json")
    non_bypass = _load(root / "tts_speech_gate_non_bypass_review_v1.json")
    audit = _load(root / "tts_runtime_boundary_audit_v1.json")
    blocked = _load(root / "tts_runtime_blocked_path_result_v1.json")
    closure = _load(root / "tts_runtime_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok("upstream.runtime_abstraction", plan_sm.get("tts_runtime_planning_only") is True)
    ok(
        "upstream.provider_abstraction",
        plan_sm.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE,
    )
    ok("upstream.no_qianwen_invoke", plan_sm.get("qianwen_tts_invoked_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("tts_runtime_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.harness", summary.get("controlled_provider_readiness_harness_ref") == HARNESS_ID)
    ok("summary.display_defer", summary.get("display_gate_deferred_not_skipped") is True)
    ok("summary.e2e_defer", summary.get("end_to_end_simulation_deferred_not_cancelled") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.runtime_abstraction", policy.get("runtime_abstraction") is True)
    ok("policy.provider_abstraction", policy.get("provider_abstraction_required") is True)
    ok("policy.qianwen_candidate", policy.get("qianwen_is_provider_candidate_not_runtime") is True)
    ok("policy.not_tts", policy.get("speech_request_candidate_not_tts_or_audio") is True)
    ok("policy.not_audio", policy.get("audio_artifact_candidate_not_audio_output") is True)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.runtime_abstraction", input_review.get("runtime_abstraction") is True)
    ok("input.provider_abstraction", input_review.get("provider_abstraction_required") is True)
    ok("input.no_provider_logic_core", input_review.get("provider_specific_logic_forbidden_in_runtime_core") is True)
    ok("input.current_pref", input_review.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE)
    ok("input.no_provider_selected", input_review.get("provider_selected_for_execution_now") is False)
    ok("input.request_exists", input_review.get("speech_request_candidate_exists") is True)
    ok("input.not_tts", input_review.get("speech_request_not_tts") is True)

    ok("model.id", model.get("module_id") == "midplatform_tts_runtime_v1")
    ok("model.type", model.get("module_type") == "midplatform_voice_synthesis_runtime_module")
    ok(
        "model.role",
        model.get("role") == "speech_request_candidate_to_audio_artifact_runtime_planning",
    )
    ok("model.layer", model.get("system_layer") == "Output")
    ok("model.arch", model.get("architectural_layer") == "ExecutionRuntime")
    ok("model.runtime_off", model.get("runtime_enabled_now") is False)
    ok("model.runtime_abstraction", model.get("runtime_abstraction") is True)
    ok("model.provider_abstraction", model.get("provider_abstraction_required") is True)
    ok("model.no_provider_logic_core", model.get("provider_specific_logic_forbidden_in_runtime_core") is True)
    ok("model.current_pref", model.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE)
    ok("model.no_provider_selected", model.get("provider_selected_for_execution_now") is False)
    ok("model.consumes_request", model.get("consumes_speech_request_candidate") is True)
    ok("model.emits_audio_artifact", model.get("emits_audio_artifact_candidate") is True)
    ok("model.no_tts", model.get("invokes_tts") is False)
    ok("model.no_audio", model.get("generates_audio_output") is False)
    ok("model.no_raw", model.get("reads_raw_constitution_clauses") is False)
    ok("model.no_bypass", model.get("bypasses_speech_gate") is False)
    ok("model.no_provider_invoke", model.get("provider_invocation_allowed") is False)
    ok("model.no_memory", model.get("memory_write_allowed") is False)
    ok("model.no_world", model.get("world_model_write_allowed") is False)

    for field in SPEECH_REQUEST_INTAKE_FIELDS:
        ok(f"intake.{field[:15]}", field in sample_intake)
    ok("intake.no_tts", sample_intake.get("tts_runtime_allowed") is False)
    ok("intake.no_audio", sample_intake.get("audio_output_allowed") is False)
    ok("intake.candidate", sample_intake.get("candidate_only") is True)
    ok("intake.no_facing", sample_intake.get("user_facing_output_allowed") is False)

    for field in AUDIO_ARTIFACT_CANDIDATE_FIELDS:
        ok(f"audio.{field[:15]}", field in sample_audio)
    ok("audio.provider_ref", sample_audio.get("tts_provider_ref") == CURRENT_PREFERRED_PROVIDER_CANDIDATE)
    ok("audio.no_voice_model", sample_audio.get("voice_model_ref") is None)
    ok("audio.no_voice_profile", sample_audio.get("voice_profile_ref") is None)
    ok("audio.disclosures", sample_audio.get("required_disclosures_preserved") is True)
    ok("audio.uncertainty", sample_audio.get("uncertainty_surface_preserved") is True)
    ok("audio.candidate", sample_audio.get("candidate_only") is True)
    ok("audio.no_output", sample_audio.get("audio_output_allowed") is False)
    ok("audio.no_play", sample_audio.get("playback_allowed") is False)
    ok("audio.no_facing", sample_audio.get("user_facing_output_allowed") is False)

    ok("pabs.pass", pabs.get("dryrun_and_review_pass") is True)
    ok("pabs.not_qianwen", pabs.get("runtime_not_qianwen") is True)
    for rule in PROVIDER_ABSTRACTION_DRYRUN_RULES:
        ok(f"pabs.{rule[:18]}", rule in (pabs.get("rules") or []))

    ok("qianwen.pass", qianwen.get("dryrun_and_review_pass") is True)
    ok("qianwen.current_pref", qianwen.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE)
    ok("qianwen.registered_not_selected", qianwen.get("qianwen_candidate_registered_not_selected") is True)
    for fc in FUTURE_PROVIDER_CANDIDATES:
        ok(f"qianwen.future.{fc[:18]}", fc in (qianwen.get("future_provider_candidates") or []))

    ok("pswitch.pass", pswitch.get("dryrun_and_review_pass") is True)
    for rule in PROVIDER_SWITCH_BOUNDARY_RULES:
        ok(f"pswitch.{rule[:18]}", rule in (pswitch.get("rules") or []))

    ok("ready.pass", readiness.get("dryrun_and_review_pass") is True)
    ok("ready.harness", readiness.get("controlled_provider_readiness_harness_ref") == HARNESS_ID)
    for rule in PROVIDER_READINESS_RULES:
        ok(f"ready.{rule[:18]}", rule in (readiness.get("rules") or []))

    ok("vmodel.pass", vmodel.get("dryrun_and_review_pass") is True)
    for rule in VOICE_MODEL_BOUNDARY_RULES:
        ok(f"vmodel.{rule[:18]}", rule in (vmodel.get("rules") or []))

    ok("vprofile.pass", vprofile.get("dryrun_and_review_pass") is True)
    for rule in VOICE_PROFILE_BOUNDARY_RULES:
        ok(f"vprofile.{rule[:18]}", rule in (vprofile.get("rules") or []))

    ok("synth.pass", synthesis.get("dryrun_and_review_pass") is True)
    for rule in AUDIO_SYNTHESIS_DRYRUN_RULES:
        ok(f"synth.{rule[:18]}", rule in (synthesis.get("rules") or []))

    ok("playback.pass", playback.get("dryrun_and_review_pass") is True)
    for rule in AUDIO_PLAYBACK_BOUNDARY_RULES:
        ok(f"playback.{rule[:18]}", rule in (playback.get("rules") or []))

    ok("cache.pass", cache.get("dryrun_and_review_pass") is True)
    for rule in CACHE_ARTIFACT_BOUNDARY_RULES:
        ok(f"cache.{rule[:18]}", rule in (cache.get("rules") or []))

    ok("auth.pass", auth.get("dryrun_and_review_pass") is True)
    for req in AUTHORIZATION_REQUIREMENTS:
        ok(f"auth.{req[:18]}", req in (auth.get("requirements") or []))

    ok("failure.pass", failure.get("dryrun_and_review_pass") is True)
    ok("failure.count8", failure.get("route_count") == 8)
    for m in FAILURE_ROUTE_MAPPINGS:
        ok(
            f"failure.{m['condition'][:16]}",
            any(
                x.get("condition") == m["condition"] and x.get("route") == m["route"]
                for x in (failure.get("routes") or [])
            ),
        )

    ok("trace.pass", trace.get("dryrun_and_review_pass") is True)
    for req in TRACEABILITY_DRYRUN_REQUIREMENTS:
        ok(f"trace.{req[:18]}", req in (trace.get("requirements") or []))

    ok("no_raw.pass", no_raw.get("dryrun_and_review_pass") is True)
    for rule in NO_RAW_CONSTITUTION_RULES:
        ok(f"noraw.{rule[:18]}", rule in (no_raw.get("rules") or []))

    ok("bypass.pass", non_bypass.get("dryrun_and_review_pass") is True)
    for rule in SPEECH_GATE_NON_BYPASS_RULES:
        ok(f"bypass.{rule[:18]}", rule in (non_bypass.get("rules") or []))

    ok("audit.pass", audit.get("dryrun_and_review_pass") is True)
    ok("audit.forbidden_absent", audit.get("forbidden_actions_absent") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count22", blocked.get("blocked_count") == 22)
    for bp in BLOCKED_PATHS:
        ok(
            f"blocked.{bp[:18]}",
            any(
                x.get("blocked_path") == bp and x.get("blocked") is True
                for x in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.execution", closure.get("execution_runtime_validated") is True)
    ok("closure.provider_abstraction", closure.get("provider_abstraction_validated") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("closure.chain4", len(closure.get("main_chain_closed") or []) == 4)
    for pos in TTS_RUNTIME_LAYER_POSITIONING:
        ok(f"closure.pos.{pos[:18]}", pos in (closure.get("tts_runtime_layer_positioning") or []))

    ok("next.ready", next_route.get("ready_for_end_to_end_output_chain_simulation_planning") is True)
    ok("next.no_runtime", next_route.get("tts_runtime_runtime_enabled") is False)
    ok("next.no_provider_selected", next_route.get("provider_selected_for_execution") is False)
    ok("next.display_defer", next_route.get("display_gate_deferred_not_skipped") is True)
    ok("next.e2e_defer", next_route.get("end_to_end_simulation_deferred_not_cancelled") is True)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    pass_all = summary.get("dryrun_and_review_pass") is True
    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
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
