#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Voice Output Plane DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_voice_output_plane_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FAILURE_ROUTE_RULES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SPEECH_GATE_NON_BYPASS_DRYRUN_RULES,
    SPEECH_GATE_RESULT_CONSUMPTION_RULES,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.midplatform_voice_output_plane_planning_v1 import (
    AUDIO_OUTPUT_BOUNDARY_RULES,
    NO_RAW_CONSTITUTION_RULES,
    SPEECH_CONTENT_RENDERING_RULES,
    SPEECH_GATE_RESULT_INTAKE_FIELDS,
    SPEECH_REQUEST_CANDIDATE_FIELDS,
    SPEECH_TIMING_PRIORITY_RULES,
    TRACEABILITY_REQUIREMENTS,
    TTS_RUNTIME_BOUNDARY_RULES,
    VOICE_OUTPUT_PLANE_LAYER_POSITIONING,
    VOICE_QUEUE_INTERRUPTION_RULES,
)

MIN_CHECKS = 241

REQUIRED = (
    "voice_output_plane_dryrun_review_policy_v1.json",
    "voice_output_plane_planning_input_review_v1.json",
    "voice_output_plane_model_candidate_v1.json",
    "sample_speech_gate_result_intake_v1.json",
    "sample_speech_request_candidate_v1.json",
    "execution_layer_identity_review_v1.json",
    "speech_gate_result_consumption_review_v1.json",
    "no_raw_constitution_binding_review_v1.json",
    "speech_gate_non_bypass_review_v1.json",
    "tts_runtime_boundary_review_v1.json",
    "audio_output_boundary_review_v1.json",
    "voice_queue_interruption_boundary_review_v1.json",
    "speech_timing_priority_review_v1.json",
    "speech_content_rendering_boundary_review_v1.json",
    "voice_output_failure_route_review_v1.json",
    "voice_output_traceability_review_v1.json",
    "voice_output_plane_boundary_audit_v1.json",
    "voice_output_plane_blocked_path_result_v1.json",
    "voice_output_plane_closure_decision_v1.json",
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
            "midplatform_voice_output_plane_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_voice_output_plane_planning",
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
    model = _load(root / "voice_output_plane_model_candidate_v1.json")
    sample_gate = _load(root / "sample_speech_gate_result_intake_v1.json")
    sample_request = _load(root / "sample_speech_request_candidate_v1.json")
    identity = _load(root / "execution_layer_identity_review_v1.json")
    consumption = _load(root / "speech_gate_result_consumption_review_v1.json")
    no_raw = _load(root / "no_raw_constitution_binding_review_v1.json")
    non_bypass = _load(root / "speech_gate_non_bypass_review_v1.json")
    tts = _load(root / "tts_runtime_boundary_review_v1.json")
    audio = _load(root / "audio_output_boundary_review_v1.json")
    queue = _load(root / "voice_queue_interruption_boundary_review_v1.json")
    timing = _load(root / "speech_timing_priority_review_v1.json")
    rendering = _load(root / "speech_content_rendering_boundary_review_v1.json")
    failure = _load(root / "voice_output_failure_route_review_v1.json")
    trace = _load(root / "voice_output_traceability_review_v1.json")
    blocked = _load(root / "voice_output_plane_blocked_path_result_v1.json")
    closure = _load(root / "voice_output_plane_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok(
        "upstream.execution",
        _load(plan_root / "voice_output_plane_planning_policy_v1.json").get(
            "voice_output_plane_is_execution_not_enforcement"
        )
        is True,
    )

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("voice_output_plane_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.display_defer", summary.get("display_gate_deferred_not_skipped") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("model.id", model.get("module_id") == "midplatform_voice_output_plane_v1")
    ok("model.type", model.get("module_type") == "midplatform_voice_execution_plane_module")
    ok("model.role", model.get("role") == "speech_gate_result_to_speech_request_candidate_execution_planning")
    ok("model.arch", model.get("architectural_layer") == "Execution")
    ok("model.layer", model.get("system_layer") == "Output")
    ok("model.runtime_off", model.get("runtime_enabled_now") is False)
    ok("model.consumes_gate", model.get("consumes_speech_gate_result_candidate") is True)
    ok("model.emits_request", model.get("emits_speech_request_candidate") is True)
    ok("model.no_raw", model.get("reads_raw_constitution_clauses") is False)
    ok("model.no_bypass", model.get("bypasses_speech_gate") is False)
    ok("model.no_tts", model.get("invokes_tts") is False)
    ok("model.no_audio", model.get("generates_audio_output") is False)
    ok("model.no_mic", model.get("microphone_runtime_allowed") is False)
    ok("model.no_asr", model.get("asr_runtime_allowed") is False)

    for field in SPEECH_GATE_RESULT_INTAKE_FIELDS:
        ok(f"gate.{field[:15]}", field in sample_gate)
    ok("gate.candidate", sample_gate.get("candidate_only") is True)
    ok("gate.no_speech_req", sample_gate.get("speech_request_allowed") is False)

    for field in SPEECH_REQUEST_CANDIDATE_FIELDS:
        ok(f"request.{field[:15]}", field in sample_request)
    ok("request.no_tts", sample_request.get("tts_runtime_allowed") is False)
    ok("request.no_audio", sample_request.get("audio_output_allowed") is False)
    ok("request.candidate", sample_request.get("candidate_only") is True)
    ok("request.no_facing", sample_request.get("user_facing_output_allowed") is False)

    ok("identity.pass", identity.get("dryrun_and_review_pass") is True)
    for pos in VOICE_OUTPUT_PLANE_LAYER_POSITIONING:
        ok(f"id_pos.{pos[:18]}", pos in (identity.get("voice_output_plane_layer_positioning") or []))

    ok("consumption.pass", consumption.get("dryrun_and_review_pass") is True)
    for rule in SPEECH_GATE_RESULT_CONSUMPTION_RULES:
        ok(f"consume.{rule[:18]}", rule in (consumption.get("rules") or []))

    ok("no_raw.pass", no_raw.get("dryrun_and_review_pass") is True)
    for rule in NO_RAW_CONSTITUTION_RULES:
        ok(f"noraw.{rule[:18]}", rule in (no_raw.get("rules") or []))

    ok("bypass.pass", non_bypass.get("dryrun_and_review_pass") is True)
    for rule in SPEECH_GATE_NON_BYPASS_DRYRUN_RULES:
        ok(f"bypass.{rule[:18]}", rule in (non_bypass.get("rules") or []))

    ok("tts.pass", tts.get("dryrun_and_review_pass") is True)
    ok("tts.not_tts", tts.get("speech_request_not_tts") is True)
    for rule in TTS_RUNTIME_BOUNDARY_RULES:
        ok(f"tts.{rule[:18]}", rule in (tts.get("rules") or []))

    ok("audio.pass", audio.get("dryrun_and_review_pass") is True)
    for rule in AUDIO_OUTPUT_BOUNDARY_RULES:
        ok(f"audio.{rule[:18]}", rule in (audio.get("rules") or []))

    ok("queue.pass", queue.get("dryrun_and_review_pass") is True)
    for rule in VOICE_QUEUE_INTERRUPTION_RULES:
        ok(f"queue.{rule[:18]}", rule in (queue.get("rules") or []))

    ok("timing.pass", timing.get("dryrun_and_review_pass") is True)
    for rule in SPEECH_TIMING_PRIORITY_RULES:
        ok(f"timing.{rule[:18]}", rule in (timing.get("rules") or []))

    ok("render.pass", rendering.get("dryrun_and_review_pass") is True)
    for rule in SPEECH_CONTENT_RENDERING_RULES:
        ok(f"render.{rule[:18]}", rule in (rendering.get("rules") or []))

    ok("failure.pass", failure.get("dryrun_and_review_pass") is True)
    ok("failure.count7", failure.get("route_count") == 7)
    for m in FAILURE_ROUTE_RULES:
        ok(
            f"failure.{m['condition'][:16]}",
            any(
                x.get("condition") == m["condition"] and x.get("route") == m["route"]
                for x in (failure.get("routes") or [])
            ),
        )

    ok("trace.pass", trace.get("dryrun_and_review_pass") is True)
    for req in TRACEABILITY_REQUIREMENTS:
        ok(f"trace.{req[:18]}", req in (trace.get("requirements") or []))

    ok("audit.pass", _load(root / "voice_output_plane_boundary_audit_v1.json").get("dryrun_and_review_pass") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count20", blocked.get("blocked_count") == 20)
    for bp in BLOCKED_PATHS:
        ok(
            f"blocked.{bp[:18]}",
            any(x.get("blocked_path") == bp and x.get("blocked") is True for x in (blocked.get("blocked_paths") or [])),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.execution", closure.get("execution_layer_validated") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next.ready", next_route.get("ready_for_tts_runtime_roadmap_decision") is True)
    ok("next.no_runtime", next_route.get("voice_output_plane_runtime_enabled") is False)
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
