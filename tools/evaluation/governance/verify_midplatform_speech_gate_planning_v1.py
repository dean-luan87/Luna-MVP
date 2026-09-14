#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Speech Gate Planning v1."""

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
from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SAFETY_DR_FINAL,
)
from capabilities.governance.midplatform_speech_display_gate_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL,
    NEXT_PHASE_GO as ROADMAP_NEXT,
    SELECTED_ROUTE,
)
from capabilities.governance.midplatform_speech_gate_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_FALSE,
    BOUNDARY_TRUE,
    CHANNEL_ADMISSION_RULES,
    CONTENT_CONSTRAINT_RULES,
    CORE_CHAIN_BOUNDARY,
    DOWNSTREAM_HANDOFF_MAPPINGS,
    ENFORCEMENT_RESULT_INTAKE_FIELDS,
    EXECUTION_LAYER_BOUNDARY_RULES,
    FINAL_DECISION_GO,
    FOUR_LAYER_ARCHITECTURE,
    INTERRUPTION_TIMING_RULES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    NO_RAW_CONSTITUTION_RULES,
    PHASE_ID,
    REFUSAL_HOLD_DEGRADE_MAPPINGS,
    SCOPE,
    SPEECH_ACTION_TAXONOMY,
    SPEECH_GATE_LAYER_POSITIONING,
    SPEECH_GATE_RESULT_FIELDS,
    TONE_PERSONALIZATION_RULES,
    TRACEABILITY_REQUIREMENTS,
    UNCERTAINTY_DISCLOSURE_RULES,
    UPSTREAM_ROADMAP_FINAL,
    UPSTREAM_ROADMAP_NEXT,
    USER_OUTPUT_INTAKE_FIELDS,
)

MIN_CHECKS = 290

REQUIRED = (
    "speech_gate_planning_policy_v1.json",
    "speech_display_roadmap_input_review_v1.json",
    "speech_gate_module_definition_v1.json",
    "speech_gate_enforcement_result_intake_contract_v1.json",
    "speech_gate_user_output_candidate_intake_contract_v1.json",
    "speech_gate_result_candidate_contract_v1.json",
    "speech_gate_action_taxonomy_v1.json",
    "speech_channel_admission_rule_plan_v1.json",
    "speech_content_constraint_rule_plan_v1.json",
    "speech_uncertainty_disclosure_rule_plan_v1.json",
    "speech_tone_personalization_boundary_plan_v1.json",
    "speech_interruption_and_timing_boundary_plan_v1.json",
    "speech_safety_refusal_hold_degrade_plan_v1.json",
    "speech_gate_downstream_handoff_plan_v1.json",
    "speech_gate_no_raw_constitution_binding_policy_v1.json",
    "speech_gate_execution_layer_boundary_plan_v1.json",
    "speech_gate_traceability_plan_v1.json",
    "speech_gate_boundary_matrix_v1.json",
    "speech_gate_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "speech_gate_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_planning",
    )
    p.add_argument(
        "--roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_speech_display_gate_roadmap_decision"
        ),
    )
    p.add_argument(
        "--safety-gate-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_safety_gate_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.roadmap_decision_root)
    safety_dr_root = Path(args.safety_gate_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    roadmap_vr = _load(roadmap_root / "verifier_report.json")
    roadmap_sm = _load(roadmap_root / "summary.json")
    safety_dr_vr = _load(safety_dr_root / "verifier_report.json")
    safety_model = _load(safety_dr_root / "safety_gate_model_candidate_v1.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "speech_gate_planning_policy_v1.json")
    input_review = _load(root / "speech_display_roadmap_input_review_v1.json")
    module_def = _load(root / "speech_gate_module_definition_v1.json")
    enforcement_intake = _load(root / "speech_gate_enforcement_result_intake_contract_v1.json")
    user_intake = _load(root / "speech_gate_user_output_candidate_intake_contract_v1.json")
    result_contract = _load(root / "speech_gate_result_candidate_contract_v1.json")
    taxonomy = _load(root / "speech_gate_action_taxonomy_v1.json")
    channel = _load(root / "speech_channel_admission_rule_plan_v1.json")
    content = _load(root / "speech_content_constraint_rule_plan_v1.json")
    uncertainty = _load(root / "speech_uncertainty_disclosure_rule_plan_v1.json")
    tone = _load(root / "speech_tone_personalization_boundary_plan_v1.json")
    interruption = _load(root / "speech_interruption_and_timing_boundary_plan_v1.json")
    refusal = _load(root / "speech_safety_refusal_hold_degrade_plan_v1.json")
    handoff = _load(root / "speech_gate_downstream_handoff_plan_v1.json")
    no_raw = _load(root / "speech_gate_no_raw_constitution_binding_policy_v1.json")
    exec_boundary = _load(root / "speech_gate_execution_layer_boundary_plan_v1.json")
    trace = _load(root / "speech_gate_traceability_plan_v1.json")
    boundary = _load(root / "speech_gate_boundary_matrix_v1.json")
    dryrun = _load(root / "speech_gate_dryrun_plan_v1.json")
    decision = _load(root / "speech_gate_planning_decision_v1.json")

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == ROADMAP_FINAL)
    ok("upstream.roadmap_next", roadmap_sm.get("recommended_next_phase") == ROADMAP_NEXT)
    ok("upstream.route_a", roadmap_sm.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.safety_dr_go", safety_dr_vr.get("verifier") == "GO")
    ok("upstream.safety_dr_final", _load(safety_dr_root / "summary.json").get("final_decision") == SAFETY_DR_FINAL)
    ok("upstream.emits_enforcement", safety_model.get("emits_enforcement_result_candidate") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("speech_gate_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.boundary", summary.get("core_chain_boundary") == CORE_CHAIN_BOUNDARY)
    ok("summary.display_defer", summary.get("display_gate_deferred_not_skipped") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.enforcement_only", policy.get("enforcement_result_only_not_raw_clauses") is True)
    ok("policy.speech_enforcement", policy.get("speech_gate_is_enforcement_not_execution") is True)
    ok("policy.exec_later", policy.get("execution_consumes_speech_gate_result_later") is True)
    ok("policy.four_layer", policy.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)
    for pos in SPEECH_GATE_LAYER_POSITIONING:
        ok(f"policy.pos.{pos[:18]}", pos in (policy.get("speech_gate_layer_positioning") or []))

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.route", input_review.get("selected_route") == SELECTED_ROUTE)
    ok("input.enforcement_layer", input_review.get("speech_gate_is_enforcement_layer") is True)
    ok("input.exec_layer", input_review.get("voice_output_plane_is_execution_layer") is True)
    ok("input.emits", input_review.get("safety_gate_emits_enforcement_result") is True)

    identity = module_def.get("module_identity") or {}
    processing = module_def.get("processing_scope") or {}
    runtime = module_def.get("runtime_boundaries") or {}
    valid, issues = validate_module_definition(module_def)
    ok("module.valid", valid and len(issues) == 0)
    ok("module.id", identity.get("module_id") == "midplatform_speech_gate_v1")
    ok("module.type", identity.get("module_type") == "midplatform_user_output_gate_module")
    ok("module.role", identity.get("role") == "speech_output_enforcement_gate")
    ok("module.layer", identity.get("system_layer") == "Validation")
    ok("module.arch_layer", identity.get("architectural_layer") == "Enforcement")
    ok("module.no_write", processing.get("write_allowed") is False)
    ok("module.runtime_off", runtime.get("runtime_enabled_now") is False)

    downstream = module_def.get("downstream_targets") or {}
    downstream_mods = downstream.get("downstream_modules") or []
    ok("module.down_voice", "voice_output_plane_later" in downstream_mods)
    ok("module.down_no_output", "no_output_handler_later" in downstream_mods)
    ok("module.down_display_defer", "display_gate_later" in downstream_mods)

    output_contract = module_def.get("output_contract") or {}
    ok("module.speech_result", output_contract.get("output_object_type") == "speech_gate_result_candidate")
    ok("module.exec_reads_speech", output_contract.get("execution_layer_consumes_speech_gate_result") is True)

    upstream_mods = (module_def.get("upstream_sources") or {}).get("upstream_modules") or []
    ok("module.upstream_safety", "safety_gate" in upstream_mods)
    ok("module.upstream_output", "output_plane_integration" in upstream_mods)
    ok("module.upstream_resolver", "constitution_resolver" in upstream_mods)

    for section in TEMPLATE_SECTIONS:
        ok(f"section.{section[:12]}", section in module_def)

    ok("enforcement_intake.fields18", len(enforcement_intake.get("required_fields") or []) == 18)
    ok("enforcement_intake.only", enforcement_intake.get("consumes_enforcement_result_only") is True)
    ok("enforcement_intake.no_raw", enforcement_intake.get("raw_constitution_clause_binding_forbidden") is True)
    ok("enforcement_intake.version", enforcement_intake.get("enforcement_result_version_required") is True)
    ok("enforcement_intake.ttl", enforcement_intake.get("enforcement_result_ttl_required") is True)
    ok("enforcement_intake.trace_refs", enforcement_intake.get("applicable_rule_refs_are_trace_refs") is True)
    for field in ENFORCEMENT_RESULT_INTAKE_FIELDS:
        ok(f"enforcement.{field[:15]}", field in (enforcement_intake.get("required_fields") or []))

    ok("user_intake.fields17", len(user_intake.get("required_fields") or []) == 17)
    u_defaults = user_intake.get("defaults") or {}
    ok("user_intake.no_facing", u_defaults.get("user_facing_output_allowed") is False)
    ok("user_intake.no_speech", u_defaults.get("speech_request_allowed") is False)
    ok("user_intake.not_fact", u_defaults.get("fact_status") == "not_fact")
    for field in USER_OUTPUT_INTAKE_FIELDS:
        ok(f"user.{field[:15]}", field in (user_intake.get("required_fields") or []))

    ok("result.fields22", len(result_contract.get("required_fields") or []) == 22)
    ok("result.not_execution", result_contract.get("not_execution_output") is True)
    r_defaults = result_contract.get("defaults") or {}
    ok("result.no_speech_req", r_defaults.get("speech_request_allowed") is False)
    for field in SPEECH_GATE_RESULT_FIELDS:
        ok(f"result.{field[:15]}", field in (result_contract.get("required_fields") or []))

    ok("taxonomy.count13", taxonomy.get("action_count") == 13)
    for action in SPEECH_ACTION_TAXONOMY:
        ok(f"action.{action[:18]}", action in (taxonomy.get("actions") or []))

    ok("channel.count6", channel.get("rule_count") == 6)
    for rule in CHANNEL_ADMISSION_RULES:
        ok(f"channel.{rule[:18]}", rule in (channel.get("rules") or []))

    ok("content.count7", content.get("rule_count") == 7)
    for rule in CONTENT_CONSTRAINT_RULES:
        ok(f"content.{rule[:18]}", rule in (content.get("rules") or []))

    ok("uncertainty.count6", uncertainty.get("rule_count") == 6)
    for rule in UNCERTAINTY_DISCLOSURE_RULES:
        ok(f"uncertainty.{rule[:18]}", rule in (uncertainty.get("rules") or []))

    ok("tone.count6", tone.get("rule_count") == 6)
    for rule in TONE_PERSONALIZATION_RULES:
        ok(f"tone.{rule[:18]}", rule in (tone.get("rules") or []))

    ok("interrupt.count6", interruption.get("rule_count") == 6)
    for rule in INTERRUPTION_TIMING_RULES:
        ok(f"interrupt.{rule[:18]}", rule in (interruption.get("rules") or []))

    ok("refusal.count6", refusal.get("mapping_count") == 6)
    for m in REFUSAL_HOLD_DEGRADE_MAPPINGS:
        ok(
            f"refusal.{m['safety_signal'][:18]}",
            any(
                x.get("safety_signal") == m["safety_signal"] and x.get("speech_path") == m["speech_path"]
                for x in (refusal.get("mappings") or [])
            ),
        )

    ok("handoff.count6", handoff.get("handoff_count") == 6)
    ok("handoff.speech_voice_split", handoff.get("speech_gate_enforcement_voice_plane_execution") is True)
    ok("handoff.display_defer", handoff.get("display_gate_deferred_not_skipped") is True)
    ok("handoff.no_runtime", handoff.get("no_downstream_runtime_invoked_now") is True)
    for m in DOWNSTREAM_HANDOFF_MAPPINGS:
        ok(
            f"handoff.{m['speech_action'][:18]}",
            any(
                x.get("speech_action") == m["speech_action"] and x.get("handoff") == m["handoff"]
                for x in (handoff.get("handoffs") or [])
            ),
        )

    ok("no_raw.count6", no_raw.get("rule_count") == 6)
    ok("no_raw.enforcement_only", no_raw.get("consumes_enforcement_result_only") is True)
    for rule in NO_RAW_CONSTITUTION_RULES:
        ok(f"noraw.{rule[:18]}", rule in (no_raw.get("rules") or []))

    ok("exec_boundary.count7", exec_boundary.get("rule_count") == 7)
    ok("exec_boundary.not_tts", exec_boundary.get("speech_pass_not_speech_request_or_tts") is True)
    for rule in EXECUTION_LAYER_BOUNDARY_RULES:
        ok(f"exec.{rule[:18]}", rule in (exec_boundary.get("rules") or []))

    ok("trace.count9", trace.get("requirement_count") == 9)
    for req in TRACEABILITY_REQUIREMENTS:
        ok(f"trace.{req[:18]}", req in (trace.get("requirements") or []))

    ok("boundary.all_false", boundary.get("all_runtime_actions_false") is True)
    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:18]}", boundary.get("matrix", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.four_layer", decision.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)
    ok("decision.chain4", len(decision.get("main_chain_defined") or []) == 4)
    ok("decision.layer_pos", len(decision.get("speech_gate_layer_positioning") or []) >= 4)

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
