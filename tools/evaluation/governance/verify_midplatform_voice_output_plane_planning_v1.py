#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Voice Output Plane Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.midplatform_voice_output_plane_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL,
    NEXT_PHASE_GO as ROADMAP_NEXT,
    SELECTED_ROUTE,
)
from capabilities.governance.midplatform_voice_output_plane_planning_v1 import (
    AUDIO_OUTPUT_BOUNDARY_RULES,
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_FALSE,
    BOUNDARY_TRUE,
    CORE_CHAIN_BOUNDARY,
    EXECUTION_SCOPE_RULES,
    FAILURE_ROUTE_MAPPINGS,
    FINAL_DECISION_GO,
    FOUR_LAYER_ARCHITECTURE,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    NO_RAW_CONSTITUTION_RULES,
    PHASE_ID,
    SCOPE,
    SPEECH_CONTENT_RENDERING_RULES,
    SPEECH_GATE_NON_BYPASS_RULES,
    SPEECH_GATE_RESULT_INTAKE_FIELDS,
    SPEECH_REQUEST_CANDIDATE_FIELDS,
    SPEECH_TIMING_PRIORITY_RULES,
    TRACEABILITY_REQUIREMENTS,
    TTS_RUNTIME_BOUNDARY_RULES,
    UPSTREAM_ROADMAP_FINAL,
    UPSTREAM_ROADMAP_NEXT,
    VOICE_OUTPUT_PLANE_LAYER_POSITIONING,
    VOICE_QUEUE_INTERRUPTION_RULES,
)

MIN_CHECKS = 249

REQUIRED = (
    "voice_output_plane_planning_policy_v1.json",
    "voice_output_plane_roadmap_input_review_v1.json",
    "voice_output_plane_module_definition_v1.json",
    "speech_gate_result_intake_contract_v1.json",
    "speech_request_candidate_contract_v1.json",
    "voice_output_execution_scope_plan_v1.json",
    "tts_runtime_boundary_plan_v1.json",
    "audio_output_boundary_plan_v1.json",
    "voice_queue_and_interruption_boundary_plan_v1.json",
    "speech_timing_and_priority_plan_v1.json",
    "speech_content_rendering_boundary_plan_v1.json",
    "voice_output_failure_route_plan_v1.json",
    "voice_output_traceability_plan_v1.json",
    "voice_output_no_raw_constitution_policy_v1.json",
    "voice_output_speech_gate_non_bypass_policy_v1.json",
    "voice_output_plane_boundary_matrix_v1.json",
    "voice_output_plane_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "voice_output_plane_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_voice_output_plane_planning",
    )
    p.add_argument(
        "--roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_voice_output_plane_roadmap_decision"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    roadmap_vr = _load(roadmap_root / "verifier_report.json")
    roadmap_sm = _load(roadmap_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "voice_output_plane_planning_policy_v1.json")
    input_review = _load(root / "voice_output_plane_roadmap_input_review_v1.json")
    module_def = _load(root / "voice_output_plane_module_definition_v1.json")
    intake = _load(root / "speech_gate_result_intake_contract_v1.json")
    request_contract = _load(root / "speech_request_candidate_contract_v1.json")
    execution = _load(root / "voice_output_execution_scope_plan_v1.json")
    tts = _load(root / "tts_runtime_boundary_plan_v1.json")
    audio = _load(root / "audio_output_boundary_plan_v1.json")
    queue = _load(root / "voice_queue_and_interruption_boundary_plan_v1.json")
    timing = _load(root / "speech_timing_and_priority_plan_v1.json")
    rendering = _load(root / "speech_content_rendering_boundary_plan_v1.json")
    failure = _load(root / "voice_output_failure_route_plan_v1.json")
    trace = _load(root / "voice_output_traceability_plan_v1.json")
    no_raw = _load(root / "voice_output_no_raw_constitution_policy_v1.json")
    non_bypass = _load(root / "voice_output_speech_gate_non_bypass_policy_v1.json")
    boundary = _load(root / "voice_output_plane_boundary_matrix_v1.json")
    dryrun = _load(root / "voice_output_plane_dryrun_plan_v1.json")
    decision = _load(root / "voice_output_plane_planning_decision_v1.json")

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == ROADMAP_FINAL)
    ok("upstream.roadmap_next", roadmap_sm.get("recommended_next_phase") == ROADMAP_NEXT)
    ok("upstream.route_a", roadmap_sm.get("selected_route") == SELECTED_ROUTE)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("voice_output_plane_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.boundary", summary.get("core_chain_boundary") == CORE_CHAIN_BOUNDARY)
    ok("summary.display_defer", summary.get("display_gate_deferred_not_skipped") is True)
    ok("summary.tts_blocked", summary.get("direct_tts_runtime_route_blocked") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.execution", policy.get("voice_output_plane_is_execution_not_enforcement") is True)
    ok("policy.speech_result_only", policy.get("speech_gate_result_only_not_raw_clauses") is True)
    ok("policy.non_bypass", policy.get("speech_gate_non_bypass_required") is True)
    ok("policy.four_layer", policy.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)
    for pos in VOICE_OUTPUT_PLANE_LAYER_POSITIONING:
        ok(f"policy.pos.{pos[:18]}", pos in (policy.get("voice_output_plane_layer_positioning") or []))

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.route", input_review.get("selected_route") == SELECTED_ROUTE)
    ok("input.exec_layer", input_review.get("voice_output_plane_is_execution_layer") is True)
    ok("input.enforcement", input_review.get("speech_gate_is_enforcement_layer") is True)
    ok("input.tts_blocked", input_review.get("direct_tts_route_blocked") is True)

    identity = module_def.get("module_identity") or {}
    processing = module_def.get("processing_scope") or {}
    runtime = module_def.get("runtime_boundaries") or {}
    valid, issues = validate_module_definition(module_def)
    ok("module.valid", valid and len(issues) == 0)
    ok("module.id", identity.get("module_id") == "midplatform_voice_output_plane_v1")
    ok("module.type", identity.get("module_type") == "midplatform_voice_execution_plane_module")
    ok(
        "module.role",
        identity.get("role") == "speech_gate_result_to_speech_request_candidate_execution_planning",
    )
    ok("module.layer", identity.get("system_layer") == "Output")
    ok("module.arch_layer", identity.get("architectural_layer") == "Execution")
    ok("module.no_write", processing.get("write_allowed") is False)
    ok("module.runtime_off", runtime.get("runtime_enabled_now") is False)

    upstream_mods = (module_def.get("upstream_sources") or {}).get("upstream_modules") or []
    ok("module.up_speech_gate", "midplatform_speech_gate_v1" in upstream_mods)

    downstream_mods = (module_def.get("downstream_targets") or {}).get("downstream_modules") or []
    ok("module.down_tts", "tts_runtime_later" in downstream_mods)
    ok("module.down_audio", "audio_output_later" in downstream_mods)

    output_contract = module_def.get("output_contract") or {}
    ok("module.speech_req", output_contract.get("output_object_type") == "speech_request_candidate")

    for section in TEMPLATE_SECTIONS:
        ok(f"section.{section[:12]}", section in module_def)

    ok("intake.fields22", len(intake.get("required_fields") or []) == 22)
    ok("intake.speech_only", intake.get("consumes_speech_gate_result_only") is True)
    ok("intake.no_raw", intake.get("raw_constitution_clause_binding_forbidden") is True)
    ok("intake.no_bypass", intake.get("speech_gate_bypass_forbidden") is True)
    for field in SPEECH_GATE_RESULT_INTAKE_FIELDS:
        ok(f"intake.{field[:15]}", field in (intake.get("required_fields") or []))

    ok("request.fields17", len(request_contract.get("required_fields") or []) == 17)
    ok("request.not_tts", request_contract.get("not_tts_or_audio_output") is True)
    r_defaults = request_contract.get("defaults") or {}
    ok("request.no_tts", r_defaults.get("tts_runtime_allowed") is False)
    ok("request.no_audio", r_defaults.get("audio_output_allowed") is False)
    ok("request.no_facing", r_defaults.get("user_facing_output_allowed") is False)
    for field in SPEECH_REQUEST_CANDIDATE_FIELDS:
        ok(f"request.{field[:15]}", field in (request_contract.get("required_fields") or []))

    ok("exec.count7", execution.get("rule_count") == 7)
    for rule in EXECUTION_SCOPE_RULES:
        ok(f"exec.{rule[:18]}", rule in (execution.get("rules") or []))

    ok("tts.count6", tts.get("rule_count") == 6)
    for rule in TTS_RUNTIME_BOUNDARY_RULES:
        ok(f"tts.{rule[:18]}", rule in (tts.get("rules") or []))

    ok("audio.count5", audio.get("rule_count") == 5)
    for rule in AUDIO_OUTPUT_BOUNDARY_RULES:
        ok(f"audio.{rule[:18]}", rule in (audio.get("rules") or []))

    ok("queue.count7", queue.get("rule_count") == 7)
    for rule in VOICE_QUEUE_INTERRUPTION_RULES:
        ok(f"queue.{rule[:18]}", rule in (queue.get("rules") or []))

    ok("timing.count6", timing.get("rule_count") == 6)
    for rule in SPEECH_TIMING_PRIORITY_RULES:
        ok(f"timing.{rule[:18]}", rule in (timing.get("rules") or []))

    ok("render.count6", rendering.get("rule_count") == 6)
    for rule in SPEECH_CONTENT_RENDERING_RULES:
        ok(f"render.{rule[:18]}", rule in (rendering.get("rules") or []))

    ok("failure.count6", failure.get("route_count") == 6)
    for m in FAILURE_ROUTE_MAPPINGS:
        ok(
            f"failure.{m['condition'][:16]}",
            any(
                x.get("condition") == m["condition"] and x.get("route") == m["route"]
                for x in (failure.get("routes") or [])
            ),
        )

    ok("trace.count8", trace.get("requirement_count") == 8)
    for req in TRACEABILITY_REQUIREMENTS:
        ok(f"trace.{req[:18]}", req in (trace.get("requirements") or []))

    ok("no_raw.count5", no_raw.get("rule_count") == 5)
    ok("no_raw.speech_only", no_raw.get("consumes_speech_gate_result_only") is True)
    for rule in NO_RAW_CONSTITUTION_RULES:
        ok(f"noraw.{rule[:18]}", rule in (no_raw.get("rules") or []))

    ok("bypass.count6", non_bypass.get("rule_count") == 6)
    ok("bypass.forbidden", non_bypass.get("speech_gate_bypass_forbidden") is True)
    for rule in SPEECH_GATE_NON_BYPASS_RULES:
        ok(f"bypass.{rule[:18]}", rule in (non_bypass.get("rules") or []))

    ok("boundary.all_false", boundary.get("all_runtime_actions_false") is True)
    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:18]}", boundary.get("matrix", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.four_layer", decision.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)
    ok("decision.chain3", len(decision.get("main_chain_defined") or []) == 3)
    ok("decision.layer_pos", len(decision.get("voice_output_plane_layer_positioning") or []) >= 5)

    ok("template_id", summary.get("template_id") == TEMPLATE_ID)
    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("planning_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "planning_pass": pass_all,
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
