#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Output Plane Integration Planning v1."""

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
from capabilities.governance.midplatform_output_plane_integration_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_FALSE,
    BOUNDARY_TRUE,
    CORE_CHAIN_BOUNDARY,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_ASSEMBLY_MAPPINGS,
    OUTPUT_CHANNEL_TAXONOMY,
    PHASE_ID,
    SCOPE,
    TASK_RESPONSE_INTAKE_FIELDS,
    UPSTREAM_TASK_RESP_DR_FINAL,
    UPSTREAM_TASK_RESP_DR_NEXT,
    USER_OUTPUT_CANDIDATE_FIELDS,
)

MIN_CHECKS = 209

REQUIRED = (
    "output_plane_integration_planning_policy_v1.json",
    "upstream_task_response_input_review_v1.json",
    "output_plane_module_definition_v1.json",
    "task_response_candidate_intake_contract_v1.json",
    "user_output_candidate_contract_v1.json",
    "output_channel_taxonomy_v1.json",
    "user_output_constitution_binding_plan_v1.json",
    "safety_gate_binding_plan_v1.json",
    "speech_gate_binding_plan_v1.json",
    "voice_output_plane_boundary_plan_v1.json",
    "display_output_boundary_plan_v1.json",
    "output_assembly_rule_plan_v1.json",
    "output_uncertainty_and_evidence_preservation_plan_v1.json",
    "output_personalization_boundary_plan_v1.json",
    "memory_worldmodel_task_state_boundary_plan_v1.json",
    "output_plane_boundary_matrix_v1.json",
    "output_plane_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "output_plane_integration_planning_decision_v1.json",
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
            "midplatform_output_plane_integration_planning"
        ),
    )
    p.add_argument(
        "--task-response-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_task_response_candidate_integration_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    task_dr_root = Path(args.task_response_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    task_dr_vr = _load(task_dr_root / "verifier_report.json")
    task_dr_sm = _load(task_dr_root / "summary.json")
    sample_task = _load(task_dr_root / "sample_task_response_candidate_v1.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "output_plane_integration_planning_policy_v1.json")
    upstream = _load(root / "upstream_task_response_input_review_v1.json")
    module_def = _load(root / "output_plane_module_definition_v1.json")
    intake = _load(root / "task_response_candidate_intake_contract_v1.json")
    user_output = _load(root / "user_output_candidate_contract_v1.json")
    channels = _load(root / "output_channel_taxonomy_v1.json")
    constitution = _load(root / "user_output_constitution_binding_plan_v1.json")
    safety = _load(root / "safety_gate_binding_plan_v1.json")
    speech = _load(root / "speech_gate_binding_plan_v1.json")
    voice = _load(root / "voice_output_plane_boundary_plan_v1.json")
    display = _load(root / "display_output_boundary_plan_v1.json")
    assembly = _load(root / "output_assembly_rule_plan_v1.json")
    preservation = _load(root / "output_uncertainty_and_evidence_preservation_plan_v1.json")
    personalization = _load(root / "output_personalization_boundary_plan_v1.json")
    memory_task = _load(root / "memory_worldmodel_task_state_boundary_plan_v1.json")
    boundary = _load(root / "output_plane_boundary_matrix_v1.json")
    dryrun = _load(root / "output_plane_dryrun_plan_v1.json")
    decision = _load(root / "output_plane_integration_planning_decision_v1.json")

    ok("upstream.task_dr_go", task_dr_vr.get("verifier") == "GO")
    ok("upstream.task_dr_final", task_dr_sm.get("final_decision") == UPSTREAM_TASK_RESP_DR_FINAL)
    ok("upstream.task_dr_next", task_dr_sm.get("recommended_next_phase") == UPSTREAM_TASK_RESP_DR_NEXT)
    ok("upstream.sample_no_user", sample_task.get("user_output_allowed") is False)
    ok("upstream.sample_no_speech", sample_task.get("speech_output_allowed") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("output_plane_integration_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.boundary", summary.get("core_chain_boundary") == CORE_CHAIN_BOUNDARY)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_user", policy.get("output_plane_not_user_facing_output") is True)
    ok("policy.not_speech", policy.get("output_plane_not_speech_not_tts") is True)
    ok("policy.planning", policy.get("planning_not_runtime") is True)

    ok("upstream.pass", upstream.get("review_pass") is True)
    ok("upstream.not_user", upstream.get("task_response_not_user_output") is True)
    ok("upstream.not_facing", upstream.get("user_output_candidate_not_user_facing") is True)
    ok("upstream.not_speech", upstream.get("output_plane_not_speech_not_tts") is True)
    ok("upstream.sample", upstream.get("sample_task_response_present") is True)

    identity = module_def.get("module_identity") or {}
    processing = module_def.get("processing_scope") or {}
    runtime = module_def.get("runtime_boundaries") or {}
    valid, issues = validate_module_definition(module_def)
    ok("module.valid", valid and len(issues) == 0)
    ok("module.id", identity.get("module_id") == "midplatform_output_plane_integration_v1")
    ok("module.type", identity.get("module_type") == "midplatform_output_candidate_assembly_module")
    ok("module.role", identity.get("role") == "task_response_candidate_to_user_output_candidate_assembly")
    ok("module.layer", identity.get("system_layer") == "Output")
    ok("module.no_arbitrate", processing.get("arbitration_allowed") is False)
    ok("module.no_write", processing.get("write_allowed") is False)
    ok("module.runtime_off", runtime.get("runtime_enabled_now") is False)

    for section in TEMPLATE_SECTIONS:
        ok(f"section.{section[:12]}", section in module_def)

    upstream_mods = (module_def.get("upstream_sources") or {}).get("upstream_modules") or []
    ok("module.upstream_task", "midplatform_task_response_candidate_integration_v1" in upstream_mods)

    downstream_mods = (module_def.get("downstream_targets") or {}).get("downstream_modules") or []
    for dm in ("speech_gate_later", "voice_output_plane_later", "display_output_later", "user_output_constitution_later"):
        ok(f"module.down.{dm[:12]}", dm in downstream_mods)

    ok("intake.fields20", len(intake.get("required_fields") or []) == 20)
    intake_defaults = intake.get("defaults") or {}
    ok("intake.no_user", intake_defaults.get("user_output_allowed") is False)
    ok("intake.no_speech", intake_defaults.get("speech_output_allowed") is False)
    ok("intake.not_fact", intake_defaults.get("fact_status") == "not_fact")
    for field in TASK_RESPONSE_INTAKE_FIELDS:
        ok(f"intake.{field[:15]}", field in (intake.get("required_fields") or []))

    ok("user_out.fields17", len(user_output.get("required_fields") or []) == 17)
    uo_defaults = user_output.get("defaults") or {}
    ok("user_out.no_facing", uo_defaults.get("user_facing_output_allowed") is False)
    ok("user_out.no_speech", uo_defaults.get("speech_request_allowed") is False)
    ok("user_out.no_display", uo_defaults.get("display_output_allowed") is False)
    ok("user_out.not_fact", uo_defaults.get("fact_status") == "not_fact")
    ok("user_out.candidate", uo_defaults.get("candidate_only") is True)
    for field in USER_OUTPUT_CANDIDATE_FIELDS:
        ok(f"user_out.{field[:15]}", field in (user_output.get("required_fields") or []))

    ok("channels.count6", channels.get("channel_count") == 6)
    ok("channels.not_exec", channels.get("channel_candidate_not_execution") is True)
    ok("channels.speech_not_tts", channels.get("speech_output_candidate_not_tts") is True)
    ok("channels.display_not_ui", channels.get("display_output_candidate_not_actual_display") is True)
    ok("channels.no_output_valid", channels.get("no_output_candidate_valid_for_blocked_hold_safety") is True)
    for ch in OUTPUT_CHANNEL_TAXONOMY:
        ok(
            f"channel.{ch['channel_id'][:18]}",
            any(c.get("channel_id") == ch["channel_id"] for c in (channels.get("channels") or [])),
        )

    ok("constitution.later", constitution.get("user_output_candidate_requires_constitution_later") is True)
    ok("constitution.bind", constitution.get("safety_privacy_fact_constraints_must_bind") is True)
    ok("constitution.no_pref", constitution.get("personalized_preference_cannot_override_constitution") is True)
    ok("constitution.unsafe", constitution.get("unsafe_or_unvalidated_cannot_become_user_facing") is True)

    ok("safety.required", safety.get("safety_gate_required_before_user_facing_output") is True)
    ok("safety.block", safety.get("safety_block_overrides_output_preference") is True)
    ok("safety.no_output", safety.get("safety_hold_can_produce_no_output_candidate") is True)
    ok("safety.not_now", safety.get("safety_gate_not_invoked_now") is True)

    ok("speech.gate_later", speech.get("speech_output_requires_speech_gate_later") is True)
    ok("speech.voice_later", speech.get("speech_output_requires_voice_output_plane_later") is True)
    ok("speech.no_request", speech.get("speech_request_generated_now") is False)
    ok("speech.no_gate", speech.get("speech_gate_invoked_now") is False)
    ok("speech.no_tts", speech.get("tts_invoked_now") is False)

    ok("voice.not_invoked", voice.get("voice_output_plane_invoked_now") is False)
    ok("voice.no_tts", voice.get("no_tts") is True)
    ok("voice.no_audio", voice.get("no_audio_output") is True)
    ok("voice.later", voice.get("voice_output_remains_later_only") is True)

    ok("display.not_invoked", display.get("display_output_invoked_now") is False)
    ok("display.no_ui", display.get("no_ui_rendering") is True)
    ok("display.no_notif", display.get("no_notification") is True)
    ok("display.later", display.get("display_output_remains_later_only") is True)

    ok("assembly.count11", assembly.get("mapping_count") == 11)
    ok("assembly.no_exec", assembly.get("assembly_does_not_execute_output") is True)
    ok("assembly.notice_later", assembly.get("notice_candidate_not_user_facing_now") is True)
    ok("assembly.no_camera", assembly.get("reobserve_candidate_does_not_activate_camera") is True)
    ok("assembly.no_hive", assembly.get("escalation_notice_does_not_notify_hive_owner_now") is True)
    for m in OUTPUT_ASSEMBLY_MAPPINGS:
        ok(
            f"assembly.{m['task_response_type'][:18]}",
            any(
                x.get("task_response_type") == m["task_response_type"]
                and x.get("output_assembly") == m["output_assembly"]
                for x in (assembly.get("mappings") or [])
            ),
        )

    ok("preserve.uncertainty", preservation.get("uncertainty_level_preserved") is True)
    ok("preserve.chain", preservation.get("source_chain_preserved") is True)
    ok("preserve.no_mutate", preservation.get("no_evidence_mutation") is True)

    ok("personal.shape", personalization.get("personalization_can_shape_tone_channel_later") is True)
    ok("personal.no_override", personalization.get("personalization_cannot_override_safety_constitution_validation") is True)
    ok("personal.no_mem", personalization.get("no_personal_memory_write") is True)
    ok("personal.no_profile", personalization.get("no_user_profile_update") is True)

    ok("mem.no_write", memory_task.get("no_memory_write") is True)
    ok("mem.no_wm", memory_task.get("no_world_model_write") is True)
    ok("mem.no_fact", memory_task.get("no_fact_admission") is True)
    ok("mem.no_commit", memory_task.get("no_task_state_commit") is True)

    ok("boundary.all_false", boundary.get("all_runtime_actions_false") is True)
    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:18]}", boundary.get("matrix", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.chain5", len(decision.get("main_chain_defined") or []) == 5)

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
