#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform User Output Constitution Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_user_output_constitution_planning_v1 import (
    ADMISSION_RULES,
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_FALSE,
    BOUNDARY_TRUE,
    CHANNEL_RULES,
    CONFLICT_PRIORITY,
    CONFLICT_RULES,
    CORE_CHAIN_BOUNDARY,
    EXPLAINABILITY_REQUIREMENTS,
    FACT_UNCERTAINTY_RULES,
    FINAL_DECISION_GO,
    JURISDICTION_GOVERNED,
    JURISDICTION_NOT_GOVERNED,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PRIVACY_RULES,
    REFUSAL_HOLD_DEGRADE_RULES,
    SAFETY_RULES,
    SCOPE,
    UPSTREAM_OUTPUT_DR_FINAL,
    UPSTREAM_OUTPUT_DR_NEXT,
    USER_OUTPUT_CANDIDATE_FIELDS,
)

MIN_CHECKS = 207

REQUIRED = (
    "user_output_constitution_planning_policy_v1.json",
    "output_plane_dryrun_input_review_v1.json",
    "user_output_constitution_definition_v1.json",
    "user_output_scope_and_jurisdiction_v1.json",
    "user_output_admission_rule_plan_v1.json",
    "user_output_safety_rule_plan_v1.json",
    "user_output_fact_and_uncertainty_rule_plan_v1.json",
    "user_output_privacy_rule_plan_v1.json",
    "user_output_channel_rule_plan_v1.json",
    "user_output_tone_personalization_boundary_plan_v1.json",
    "user_output_refusal_hold_degrade_rule_plan_v1.json",
    "user_output_explainability_traceability_plan_v1.json",
    "user_output_speech_display_boundary_plan_v1.json",
    "user_output_memory_worldmodel_taskstate_boundary_plan_v1.json",
    "user_output_constitution_conflict_policy_v1.json",
    "user_output_constitution_boundary_matrix_v1.json",
    "user_output_constitution_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "user_output_constitution_planning_decision_v1.json",
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
            "midplatform_user_output_constitution_planning"
        ),
    )
    p.add_argument(
        "--output-plane-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_output_plane_integration_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    output_dr_root = Path(args.output_plane_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    output_dr_vr = _load(output_dr_root / "verifier_report.json")
    output_dr_sm = _load(output_dr_root / "summary.json")
    sample_user = _load(output_dr_root / "sample_user_output_candidate_v1.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "user_output_constitution_planning_policy_v1.json")
    input_review = _load(root / "output_plane_dryrun_input_review_v1.json")
    constitution = _load(root / "user_output_constitution_definition_v1.json")
    scope = _load(root / "user_output_scope_and_jurisdiction_v1.json")
    admission = _load(root / "user_output_admission_rule_plan_v1.json")
    safety = _load(root / "user_output_safety_rule_plan_v1.json")
    fact_unc = _load(root / "user_output_fact_and_uncertainty_rule_plan_v1.json")
    privacy = _load(root / "user_output_privacy_rule_plan_v1.json")
    channel = _load(root / "user_output_channel_rule_plan_v1.json")
    tone = _load(root / "user_output_tone_personalization_boundary_plan_v1.json")
    refusal = _load(root / "user_output_refusal_hold_degrade_rule_plan_v1.json")
    explain = _load(root / "user_output_explainability_traceability_plan_v1.json")
    speech_display = _load(root / "user_output_speech_display_boundary_plan_v1.json")
    memory = _load(root / "user_output_memory_worldmodel_taskstate_boundary_plan_v1.json")
    conflict = _load(root / "user_output_constitution_conflict_policy_v1.json")
    boundary = _load(root / "user_output_constitution_boundary_matrix_v1.json")
    dryrun = _load(root / "user_output_constitution_dryrun_plan_v1.json")
    decision = _load(root / "user_output_constitution_planning_decision_v1.json")

    ok("upstream.output_dr_go", output_dr_vr.get("verifier") == "GO")
    ok("upstream.output_dr_final", output_dr_sm.get("final_decision") == UPSTREAM_OUTPUT_DR_FINAL)
    ok("upstream.output_dr_next", output_dr_sm.get("recommended_next_phase") == UPSTREAM_OUTPUT_DR_NEXT)
    ok("upstream.sample_no_facing", sample_user.get("user_facing_output_allowed") is False)
    ok("upstream.sample_no_speech", sample_user.get("speech_request_allowed") is False)
    ok("upstream.sample_no_display", sample_user.get("display_output_allowed") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("user_output_constitution_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.boundary", summary.get("core_chain_boundary") == CORE_CHAIN_BOUNDARY)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_facing", policy.get("constitution_not_user_facing_output") is True)
    ok("policy.not_speech", policy.get("constitution_not_speech_not_display") is True)
    ok("policy.planning", policy.get("planning_not_runtime") is True)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.not_facing", input_review.get("user_output_not_user_facing") is True)
    ok("input.sample", input_review.get("sample_user_output_present") is True)

    ok("constitution.id", constitution.get("constitution_id") == "midplatform_user_output_constitution_v1")
    ok("constitution.type", constitution.get("constitution_type") == "user_output_governance_constitution")
    ok("constitution.jurisdiction", constitution.get("jurisdiction") == "user_output_candidate_to_user_facing_output")
    ok("constitution.layer", constitution.get("system_layer") == "Output")
    ok("constitution.runtime_off", constitution.get("runtime_enabled_now") is False)
    ok("constitution.governs_user", constitution.get("governs_user_output_candidate") is True)
    ok("constitution.governs_speech", constitution.get("governs_speech_output_candidate") is True)
    ok("constitution.governs_display", constitution.get("governs_display_output_candidate") is True)
    ok("constitution.governs_notif", constitution.get("governs_notification_candidate") is True)
    ok("constitution.no_provider", constitution.get("does_not_govern_provider_runtime") is True)
    ok("constitution.no_memory", constitution.get("does_not_write_memory") is True)
    ok("constitution.no_wm", constitution.get("does_not_write_worldmodel") is True)

    ok("scope.governed6", scope.get("governed_count") == 6)
    ok("scope.not_governed7", scope.get("not_governed_count") == 7)
    for obj in JURISDICTION_GOVERNED:
        ok(f"gov.{obj[:18]}", obj in (scope.get("governed_objects") or []))
    for obj in JURISDICTION_NOT_GOVERNED:
        ok(f"notgov.{obj[:18]}", obj in (scope.get("not_governed_objects") or []))

    ok("admission.count10", admission.get("rule_count") == 10)
    for rule in ADMISSION_RULES:
        ok(f"adm.{rule[:18]}", rule in (admission.get("rules") or []))
    ok("admission.no_output", admission.get("admission_does_not_generate_output") is True)

    ok("safety.count6", safety.get("rule_count") == 6)
    for rule in SAFETY_RULES:
        ok(f"safety.{rule[:18]}", rule in (safety.get("rules") or []))
    ok("safety.gate", safety.get("safety_gate_required_before_final_output") is True)

    ok("fact.count7", fact_unc.get("rule_count") == 7)
    for rule in FACT_UNCERTAINTY_RULES:
        ok(f"fact.{rule[:18]}", rule in (fact_unc.get("rules") or []))
    ok("fact.no_fabricate", fact_unc.get("no_fabricated_certainty") is True)

    ok("privacy.count5", privacy.get("rule_count") == 5)
    for rule in PRIVACY_RULES:
        ok(f"privacy.{rule[:18]}", rule in (privacy.get("rules") or []))

    ok("channel.count6", channel.get("rule_count") == 6)
    for rule in CHANNEL_RULES:
        ok(f"channel.{rule[:18]}", rule in (channel.get("rules") or []))
    ok("channel.not_exec", channel.get("channel_candidate_not_execution") is True)

    ok("tone.shape", tone.get("personalization_may_shape_tone_later") is True)
    ok("tone.no_override", tone.get("personalization_cannot_override_safety_constitution_validation_privacy") is True)
    ok("tone.no_distort", tone.get("emotional_tone_must_not_distort_factual_uncertainty") is True)
    ok("tone.no_mem", tone.get("no_personal_memory_write") is True)
    ok("tone.no_profile", tone.get("no_user_profile_update") is True)

    ok("refusal.count7", refusal.get("rule_count") == 7)
    for route in REFUSAL_HOLD_DEGRADE_RULES:
        ok(
            f"refusal.{route['trigger'][:14]}",
            any(
                r.get("trigger") == route["trigger"] and r.get("response") == route["response"]
                for r in (refusal.get("rules") or [])
            ),
        )
    ok("refusal.silent", refusal.get("silent_mode_valid") is True)

    ok("explain.count9", explain.get("requirement_count") == 9)
    for req in EXPLAINABILITY_REQUIREMENTS:
        ok(f"explain.{req[:18]}", req in (explain.get("requirements") or []))

    ok("speech.not_request", speech_display.get("constitution_pass_not_speech_request") is True)
    ok("speech.gate_sep", speech_display.get("speech_gate_required_separately") is True)
    ok("speech.tts_sep", speech_display.get("tts_required_separately") is True)
    ok("speech.voice_sep", speech_display.get("voice_output_plane_required_separately") is True)
    ok("speech.display_sep", speech_display.get("display_output_required_separately") is True)
    ok("speech.no_gate", speech_display.get("speech_gate_invoked_now") is False)
    ok("speech.no_tts", speech_display.get("tts_invoked_now") is False)
    ok("speech.no_display", speech_display.get("display_output_invoked_now") is False)

    ok("memory.no_write", memory.get("no_memory_write") is True)
    ok("memory.no_wm", memory.get("no_world_model_write") is True)
    ok("memory.no_fact", memory.get("no_fact_admission") is True)
    ok("memory.no_commit", memory.get("no_task_state_commit") is True)

    ok("conflict.priority9", conflict.get("priority_count") == 9)
    for i, layer in enumerate(CONFLICT_PRIORITY):
        ok(f"prio.{i+1}", layer in (conflict.get("priority_layers") or []))
    ok("conflict.rules6", conflict.get("conflict_rule_count") == 6)
    for rule in CONFLICT_RULES:
        ok(f"conflict.{rule[:18]}", rule in (conflict.get("conflict_rules") or []))

    ok("boundary.all_false", boundary.get("all_runtime_actions_false") is True)
    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:18]}", boundary.get("matrix", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.chain6", len(decision.get("main_chain_defined") or []) == 6)

    ok("user_out.fields17", len(USER_OUTPUT_CANDIDATE_FIELDS) == 17)

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
