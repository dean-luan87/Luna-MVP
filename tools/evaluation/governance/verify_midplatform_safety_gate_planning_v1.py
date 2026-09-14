#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Safety Gate Planning v1."""

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
from capabilities.governance.midplatform_safety_gate_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_FALSE,
    BOUNDARY_TRUE,
    CHANNEL_BOUNDARY_RULES,
    CONSTRAINT_BUNDLE_INTAKE_FIELDS,
    CORE_CHAIN_BOUNDARY,
    DOWNSTREAM_HANDOFF_MAPPINGS,
    ENFORCEMENT_LAYER_POSITIONING,
    FINAL_DECISION_GO,
    FOUR_LAYER_ARCHITECTURE,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    NO_RAW_CONSTITUTION_RULES,
    PHASE_ID,
    REFUSAL_HOLD_DEGRADE_MAPPINGS,
    RULE_APPLICATION_RULES,
    SAFETY_ACTION_TAXONOMY,
    SAFETY_GATE_RESULT_FIELDS,
    SCOPE,
    TRACEABILITY_REQUIREMENTS,
    UNCERTAINTY_RISK_RULES,
    UPSTREAM_UO_CONST_DR_FINAL,
    UPSTREAM_UO_CONST_DR_NEXT,
    USER_OUTPUT_INTAKE_FIELDS,
)

MIN_CHECKS = 272

REQUIRED = (
    "safety_gate_planning_policy_v1.json",
    "user_output_constitution_input_review_v1.json",
    "safety_gate_module_definition_v1.json",
    "safety_gate_constraint_bundle_intake_contract_v1.json",
    "safety_gate_user_output_candidate_intake_contract_v1.json",
    "safety_gate_result_candidate_contract_v1.json",
    "safety_gate_action_taxonomy_v1.json",
    "safety_gate_rule_application_plan_v1.json",
    "safety_gate_uncertainty_risk_policy_v1.json",
    "safety_gate_channel_boundary_plan_v1.json",
    "safety_gate_refusal_hold_degrade_plan_v1.json",
    "safety_gate_traceability_plan_v1.json",
    "safety_gate_downstream_handoff_plan_v1.json",
    "safety_gate_no_raw_constitution_binding_policy_v1.json",
    "safety_gate_boundary_matrix_v1.json",
    "safety_gate_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "safety_gate_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_planning",
    )
    p.add_argument(
        "--user-output-constitution-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_user_output_constitution_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    uo_dr_root = Path(args.user_output_constitution_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    uo_dr_vr = _load(uo_dr_root / "verifier_report.json")
    uo_dr_sm = _load(uo_dr_root / "summary.json")
    bundle = _load(uo_dr_root / "constitution_constraint_bundle_candidate_v1.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "safety_gate_planning_policy_v1.json")
    input_review = _load(root / "user_output_constitution_input_review_v1.json")
    module_def = _load(root / "safety_gate_module_definition_v1.json")
    bundle_intake = _load(root / "safety_gate_constraint_bundle_intake_contract_v1.json")
    user_intake = _load(root / "safety_gate_user_output_candidate_intake_contract_v1.json")
    result_contract = _load(root / "safety_gate_result_candidate_contract_v1.json")
    taxonomy = _load(root / "safety_gate_action_taxonomy_v1.json")
    rule_app = _load(root / "safety_gate_rule_application_plan_v1.json")
    uncertainty = _load(root / "safety_gate_uncertainty_risk_policy_v1.json")
    channel = _load(root / "safety_gate_channel_boundary_plan_v1.json")
    refusal = _load(root / "safety_gate_refusal_hold_degrade_plan_v1.json")
    trace = _load(root / "safety_gate_traceability_plan_v1.json")
    handoff = _load(root / "safety_gate_downstream_handoff_plan_v1.json")
    no_raw = _load(root / "safety_gate_no_raw_constitution_binding_policy_v1.json")
    boundary = _load(root / "safety_gate_boundary_matrix_v1.json")
    dryrun = _load(root / "safety_gate_dryrun_plan_v1.json")
    decision = _load(root / "safety_gate_planning_decision_v1.json")

    ok("upstream.uo_dr_go", uo_dr_vr.get("verifier") == "GO")
    ok("upstream.uo_dr_final", uo_dr_sm.get("final_decision") == UPSTREAM_UO_CONST_DR_FINAL)
    ok("upstream.uo_dr_next", uo_dr_sm.get("recommended_next_phase") == UPSTREAM_UO_CONST_DR_NEXT)
    ok("upstream.bundle", bundle.get("bundle_id") is not None)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("safety_gate_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.boundary", summary.get("core_chain_boundary") == CORE_CHAIN_BOUNDARY)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.bundle_only", policy.get("bundle_only_not_raw_clauses") is True)
    ok("policy.enforcement", policy.get("safety_gate_is_enforcement_not_execution") is True)
    ok("policy.exec_reads_enforcement", policy.get("execution_consumes_enforcement_result_not_constitution") is True)
    ok("policy.four_layer", policy.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)
    for pos in ENFORCEMENT_LAYER_POSITIONING:
        ok(f"policy.pos.{pos[:18]}", pos in (policy.get("enforcement_layer_positioning") or []))

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.bundle", input_review.get("constraint_bundle_present") is True)
    ok("input.resolver", input_review.get("resolver_binding_pass") is True)
    ok("input.impact", input_review.get("downstream_impact_pass") is True)
    ok("input.bundle_only", input_review.get("consumes_bundle_not_raw_clauses") is True)

    identity = module_def.get("module_identity") or {}
    processing = module_def.get("processing_scope") or {}
    valid, issues = validate_module_definition(module_def)
    ok("module.valid", valid and len(issues) == 0)
    ok("module.id", identity.get("module_id") == "midplatform_safety_gate_v1")
    ok("module.type", identity.get("module_type") == "midplatform_enforcement_gate_module")
    ok("module.role", identity.get("role") == "user_output_safety_enforcement")
    ok("module.layer", identity.get("system_layer") == "Validation")
    ok("module.arch_layer", identity.get("architectural_layer") == "Enforcement")
    ok("module.no_write", processing.get("write_allowed") is False)

    downstream = module_def.get("downstream_targets") or {}
    downstream_mods = downstream.get("downstream_modules") or []
    ok("module.down_enforcement", downstream.get("downstream_enforcement_only") is True)
    ok("module.no_voice_direct", "voice_output_plane_later" not in downstream_mods)
    ok("module.down_speech_gate", "speech_gate_later" in downstream_mods)
    ok("module.down_display_gate", "display_gate_later" in downstream_mods)

    output_contract = module_def.get("output_contract") or {}
    ok("module.enforcement_alias", output_contract.get("enforcement_result_alias") == "enforcement_result_candidate")
    ok("module.exec_reads", output_contract.get("execution_layer_consumes_enforcement_result") is True)

    principles = module_def.get("module_principles") or {}
    ok("module.four_layer", principles.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)

    upstream_mods = (module_def.get("upstream_sources") or {}).get("upstream_modules") or []
    ok("module.upstream_output", "midplatform_output_plane_integration_v1" in upstream_mods)
    ok("module.upstream_resolver", "constitution_resolver" in upstream_mods)
    ok("module.upstream_constitution", "midplatform_user_output_constitution_v1" in upstream_mods)

    for section in TEMPLATE_SECTIONS:
        ok(f"section.{section[:12]}", section in module_def)

    ok("bundle_intake.fields20", len(bundle_intake.get("required_fields") or []) == 20)
    ok("bundle_intake.only", bundle_intake.get("consumes_bundle_only") is True)
    ok("bundle_intake.no_raw", bundle_intake.get("raw_constitution_clause_binding_forbidden") is True)
    ok("bundle_intake.version", bundle_intake.get("bundle_version_required") is True)
    ok("bundle_intake.ttl", bundle_intake.get("bundle_ttl_required") is True)
    for field in CONSTRAINT_BUNDLE_INTAKE_FIELDS:
        ok(f"bundle.{field[:15]}", field in (bundle_intake.get("required_fields") or []))

    ok("user_intake.fields17", len(user_intake.get("required_fields") or []) == 17)
    u_defaults = user_intake.get("defaults") or {}
    ok("user_intake.no_facing", u_defaults.get("user_facing_output_allowed") is False)
    ok("user_intake.no_speech", u_defaults.get("speech_request_allowed") is False)
    ok("user_intake.no_display", u_defaults.get("display_output_allowed") is False)
    for field in USER_OUTPUT_INTAKE_FIELDS:
        ok(f"user.{field[:15]}", field in (user_intake.get("required_fields") or []))

    ok("result.fields21", len(result_contract.get("required_fields") or []) == 21)
    ok("result.enforcement_alias", result_contract.get("enforcement_result_alias") == "enforcement_result_candidate")
    ok("result.not_execution", result_contract.get("not_execution_output") is True)
    ok("result.forbidden_actions", "forbidden_actions" in (result_contract.get("required_fields") or []))
    r_defaults = result_contract.get("defaults") or {}
    ok("result.no_facing", r_defaults.get("user_facing_output_allowed") is False)
    ok("result.no_speech", r_defaults.get("speech_request_allowed") is False)
    ok("result.no_display", r_defaults.get("display_output_allowed") is False)
    for field in SAFETY_GATE_RESULT_FIELDS:
        ok(f"result.{field[:15]}", field in (result_contract.get("required_fields") or []))

    ok("taxonomy.count12", taxonomy.get("action_count") == 12)
    for action in SAFETY_ACTION_TAXONOMY:
        ok(f"action.{action[:18]}", action in (taxonomy.get("actions") or []))

    ok("rule_app.count8", rule_app.get("rule_count") == 8)
    for rule in RULE_APPLICATION_RULES:
        ok(f"rule.{rule[:18]}", rule in (rule_app.get("rules") or []))

    ok("uncertainty.count6", uncertainty.get("rule_count") == 6)
    for rule in UNCERTAINTY_RISK_RULES:
        ok(f"risk.{rule[:18]}", rule in (uncertainty.get("rules") or []))

    ok("channel.count7", channel.get("rule_count") == 7)
    for rule in CHANNEL_BOUNDARY_RULES:
        ok(f"channel.{rule[:18]}", rule in (channel.get("rules") or []))
    ok("channel.not_speech", channel.get("safety_pass_not_speech_or_display") is True)

    ok("refusal.count6", refusal.get("mapping_count") == 6)
    for m in REFUSAL_HOLD_DEGRADE_MAPPINGS:
        ok(
            f"refusal.{m['safety_action'][:18]}",
            any(
                x.get("safety_action") == m["safety_action"] and x.get("path") == m["path"]
                for x in (refusal.get("mappings") or [])
            ),
        )

    ok("trace.count8", trace.get("requirement_count") == 8)
    for req in TRACEABILITY_REQUIREMENTS:
        ok(f"trace.{req[:18]}", req in (trace.get("requirements") or []))

    ok("handoff.count7", handoff.get("handoff_count") == 7)
    ok("handoff.enforcement_chain", handoff.get("enforcement_to_enforcement_handoff") is True)
    ok("handoff.exec_reads", handoff.get("execution_layer_consumes_enforcement_result") is True)
    ok("handoff.speech_split", handoff.get("speech_gate_enforcement_voice_plane_execution") is True)
    ok("handoff.display_split", handoff.get("display_gate_enforcement_display_output_execution") is True)
    ok("handoff.no_runtime", handoff.get("no_downstream_runtime_invoked_now") is True)
    for m in DOWNSTREAM_HANDOFF_MAPPINGS:
        ok(
            f"handoff.{m['safety_action'][:18]}",
            any(
                x.get("safety_action") == m["safety_action"] and x.get("handoff") == m["handoff"]
                for x in (handoff.get("handoffs") or [])
            ),
        )

    ok("no_raw.count6", no_raw.get("rule_count") == 6)
    ok("no_raw.bundle_only", no_raw.get("consumes_constraint_bundle_only") is True)
    for rule in NO_RAW_CONSTITUTION_RULES:
        ok(f"noraw.{rule[:18]}", rule in (no_raw.get("rules") or []))

    ok("boundary.all_false", boundary.get("all_runtime_actions_false") is True)
    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:18]}", boundary.get("matrix", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.four_layer", decision.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)
    ok("decision.chain4", len(decision.get("main_chain_defined") or []) == 4)
    ok("decision.enforcement_exemplar", len(decision.get("enforcement_layer_exemplar") or []) >= 3)

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
