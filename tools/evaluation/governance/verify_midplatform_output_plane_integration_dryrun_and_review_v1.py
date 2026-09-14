#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Output Plane Integration DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_output_plane_integration_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_ASSEMBLY_DRYRUN,
    PHASE_ID,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.midplatform_output_plane_integration_planning_v1 import (
    OUTPUT_CHANNEL_TAXONOMY,
    TASK_RESPONSE_INTAKE_FIELDS,
    USER_OUTPUT_CANDIDATE_FIELDS,
)

MIN_CHECKS = 208

REQUIRED = (
    "output_plane_integration_dryrun_review_policy_v1.json",
    "output_plane_planning_input_review_v1.json",
    "output_plane_model_candidate_v1.json",
    "sample_task_response_candidate_intake_v1.json",
    "sample_user_output_candidate_v1.json",
    "output_channel_taxonomy_dryrun_review_v1.json",
    "user_output_constitution_binding_review_v1.json",
    "safety_gate_binding_review_v1.json",
    "speech_gate_binding_review_v1.json",
    "voice_output_plane_boundary_review_v1.json",
    "display_output_boundary_review_v1.json",
    "output_assembly_rule_dryrun_review_v1.json",
    "output_uncertainty_evidence_preservation_review_v1.json",
    "output_personalization_boundary_review_v1.json",
    "memory_worldmodel_task_state_boundary_review_v1.json",
    "output_plane_boundary_audit_v1.json",
    "output_plane_blocked_path_result_v1.json",
    "output_plane_closure_decision_v1.json",
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
            "midplatform_output_plane_integration_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_output_plane_integration_planning"
        ),
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
    model = _load(root / "output_plane_model_candidate_v1.json")
    sample_intake = _load(root / "sample_task_response_candidate_intake_v1.json")
    sample_user = _load(root / "sample_user_output_candidate_v1.json")
    channels = _load(root / "output_channel_taxonomy_dryrun_review_v1.json")
    constitution = _load(root / "user_output_constitution_binding_review_v1.json")
    safety = _load(root / "safety_gate_binding_review_v1.json")
    speech = _load(root / "speech_gate_binding_review_v1.json")
    voice = _load(root / "voice_output_plane_boundary_review_v1.json")
    display = _load(root / "display_output_boundary_review_v1.json")
    assembly = _load(root / "output_assembly_rule_dryrun_review_v1.json")
    preservation = _load(root / "output_uncertainty_evidence_preservation_review_v1.json")
    personalization = _load(root / "output_personalization_boundary_review_v1.json")
    memory = _load(root / "memory_worldmodel_task_state_boundary_review_v1.json")
    boundary = _load(root / "output_plane_boundary_audit_v1.json")
    blocked = _load(root / "output_plane_blocked_path_result_v1.json")
    closure = _load(root / "output_plane_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("output_plane_integration_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("model.module_id", model.get("module_id") == "midplatform_output_plane_integration_v1")
    ok("model.type", model.get("module_type") == "midplatform_output_candidate_assembly_module")
    ok("model.role", model.get("role") == "task_response_candidate_to_user_output_candidate_assembly")
    ok("model.layer", model.get("system_layer") == "Output")
    ok("model.runtime_off", model.get("runtime_enabled_now") is False)
    ok("model.consumes_task", model.get("consumes_task_response_candidate") is True)
    ok("model.emits_user", model.get("emits_user_output_candidate") is True)
    ok("model.no_facing", model.get("emits_user_facing_output") is False)
    ok("model.no_speech_gate", model.get("speech_gate_invocation_allowed") is False)
    ok("model.no_tts", model.get("tts_invocation_allowed") is False)
    ok("model.no_voice", model.get("voice_output_plane_invocation_allowed") is False)
    ok("model.no_display", model.get("display_output_invocation_allowed") is False)
    ok("model.no_memory", model.get("memory_write_allowed") is False)
    ok("model.no_wm", model.get("world_model_write_allowed") is False)
    ok("model.no_task_state", model.get("task_state_commit_allowed") is False)
    ok("model.no_provider", model.get("provider_invocation_allowed") is False)

    for field in TASK_RESPONSE_INTAKE_FIELDS:
        ok(f"intake.{field[:15]}", field in sample_intake)
    ok("intake.candidate", sample_intake.get("candidate_only") is True)
    ok("intake.no_user", sample_intake.get("user_output_allowed") is False)
    ok("intake.no_speech", sample_intake.get("speech_output_allowed") is False)
    ok("intake.not_fact", sample_intake.get("fact_status") == "not_fact")

    for field in USER_OUTPUT_CANDIDATE_FIELDS:
        ok(f"user.{field[:15]}", field in sample_user)
    ok("user.candidate", sample_user.get("candidate_only") is True)
    ok("user.no_facing", sample_user.get("user_facing_output_allowed") is False)
    ok("user.no_speech", sample_user.get("speech_request_allowed") is False)
    ok("user.no_display", sample_user.get("display_output_allowed") is False)
    ok("user.not_fact", sample_user.get("fact_status") == "not_fact")
    ok(
        "user.source_ref",
        sample_user.get("source_task_response_candidate_ref")
        == sample_intake.get("task_response_candidate_id"),
    )

    ok("channels.pass", channels.get("dryrun_and_review_pass") is True)
    ok("channels.count6", channels.get("channel_count") == 6)
    ok("channels.all6", channels.get("all_six_channels_covered") is True)
    ok("channels.not_exec", channels.get("channel_candidate_not_execution") is True)
    ok("channels.speech_not_tts", channels.get("speech_output_candidate_not_tts") is True)
    ok("channels.display_not_ui", channels.get("display_output_candidate_not_actual_display") is True)
    ok("channels.notif_not_push", channels.get("app_notification_candidate_not_app_push") is True)
    for ch in OUTPUT_CHANNEL_TAXONOMY:
        ok(
            f"channel.{ch['channel_id'][:18]}",
            any(c.get("channel_id") == ch["channel_id"] for c in (channels.get("channels") or [])),
        )

    ok("constitution.pass", constitution.get("dryrun_and_review_pass") is True)
    ok("constitution.later", constitution.get("user_output_candidate_requires_constitution_later") is True)
    ok("constitution.not_now", constitution.get("constitution_gate_not_executed_now") is True)

    ok("safety.pass", safety.get("dryrun_and_review_pass") is True)
    ok("safety.required", safety.get("safety_gate_required_before_user_facing_output") is True)
    ok("safety.not_now", safety.get("safety_gate_not_invoked_now") is True)

    ok("speech.pass", speech.get("dryrun_and_review_pass") is True)
    ok("speech.gate_later", speech.get("speech_output_requires_speech_gate_later") is True)
    ok("speech.voice_later", speech.get("speech_output_requires_voice_output_plane_later") is True)

    ok("voice.pass", voice.get("dryrun_and_review_pass") is True)
    ok("voice.later", voice.get("voice_output_remains_later_only") is True)

    ok("display.pass", display.get("dryrun_and_review_pass") is True)
    ok("display.later", display.get("display_output_remains_later_only") is True)

    ok("assembly.pass", assembly.get("dryrun_and_review_pass") is True)
    ok("assembly.count11", assembly.get("mapping_count") == 11)
    ok("assembly.all11", assembly.get("all_eleven_types_covered") is True)
    ok("assembly.no_exec", assembly.get("assembly_does_not_execute_output") is True)
    for m in OUTPUT_ASSEMBLY_DRYRUN:
        ok(
            f"asm.{m['task_response_type'][:18]}",
            any(
                x.get("task_response_type") == m["task_response_type"]
                and x.get("output_assembly") == m["output_assembly"]
                for x in (assembly.get("mappings") or [])
            ),
        )
    for m in assembly.get("mappings") or []:
        ok(f"asm.sim.{m.get('task_response_type','')[:12]}", m.get("executes_output") is False)

    ok("preserve.pass", preservation.get("dryrun_and_review_pass") is True)
    ok("preserve.refs", preservation.get("sample_refs_preserved") is True)
    ok("preserve.uncertainty", sample_user.get("uncertainty_level") == sample_intake.get("uncertainty_level"))
    ok("preserve.evidence", sample_user.get("evidence_refs") == sample_intake.get("evidence_refs"))
    ok("preserve.rationale", sample_user.get("rationale_refs") == sample_intake.get("rationale_refs"))

    ok("personal.pass", personalization.get("dryrun_and_review_pass") is True)
    ok("personal.optional", personalization.get("personalization_refs_optional_context_only") is True)

    ok("memory.pass", memory.get("dryrun_and_review_pass") is True)
    ok("memory.no_admission", memory.get("no_fact_admission_here") is True)

    ok("audit.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("audit.forbidden", boundary.get("forbidden_actions_absent") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count15", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(
            f"blocked.{bp[:22]}",
            any(
                x.get("blocked_path") == bp and x.get("blocked") is True
                for x in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("closure.chain5", len(closure.get("main_chain_closed") or []) == 5)

    ok("next.ready", next_route.get("ready_for_user_output_constitution_planning") is True)
    ok("next.no_runtime", next_route.get("output_plane_runtime_enabled") is False)
    ok("next.no_facing", next_route.get("user_facing_output_still_forbidden") is True)
    ok("next.phase", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)

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
    print(
        json.dumps(
            {"verifier": report["verifier"], "checks_passed": passed, "checks_total": total},
            ensure_ascii=False,
        )
    )
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
