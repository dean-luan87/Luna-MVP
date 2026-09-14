#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Display Gate Planning v1."""

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
from capabilities.governance.midplatform_display_gate_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_FALSE,
    BOUNDARY_TRUE,
    CHANNEL_ADMISSION_RULES,
    CONTENT_CONSTRAINT_RULES,
    CORE_CHAIN_BOUNDARY,
    DISPLAY_ACTION_TAXONOMY,
    DISPLAY_GATE_LAYER_POSITIONING,
    DISPLAY_GATE_RESULT_FIELDS,
    DOWNSTREAM_HANDOFF_MAPPINGS,
    ENFORCEMENT_RESULT_INTAKE_FIELDS,
    EXECUTION_LAYER_BOUNDARY_RULES,
    FINAL_DECISION_GO,
    FOUR_LAYER_ARCHITECTURE,
    LAYOUT_BOUNDARY_RULES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    NOTIFICATION_BOUNDARY_RULES,
    NO_RAW_CONSTITUTION_RULES,
    PHASE_ID,
    PRIVACY_MASKING_RULES,
    REFUSAL_HOLD_DEGRADE_MAPPINGS,
    SCOPE,
    TRACEABILITY_REQUIREMENTS,
    UNCERTAINTY_DISCLOSURE_RULES,
    USER_OUTPUT_INTAKE_FIELDS,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL,
    NEXT_PHASE_GO as PROVIDER_ABS_DR_NEXT,
)

MIN_CHECKS = 299

REQUIRED = (
    "display_gate_planning_policy_v1.json",
    "provider_abstraction_alignment_input_review_v1.json",
    "display_gate_module_definition_v1.json",
    "display_gate_enforcement_result_intake_contract_v1.json",
    "display_gate_user_output_candidate_intake_contract_v1.json",
    "display_gate_result_candidate_contract_v1.json",
    "display_gate_action_taxonomy_v1.json",
    "display_channel_admission_rule_plan_v1.json",
    "display_content_constraint_rule_plan_v1.json",
    "display_uncertainty_disclosure_rule_plan_v1.json",
    "display_privacy_masking_rule_plan_v1.json",
    "display_layout_boundary_plan_v1.json",
    "display_notification_boundary_plan_v1.json",
    "display_refusal_hold_degrade_plan_v1.json",
    "display_gate_downstream_handoff_plan_v1.json",
    "display_gate_no_raw_constitution_binding_policy_v1.json",
    "display_gate_execution_layer_boundary_plan_v1.json",
    "display_gate_traceability_plan_v1.json",
    "display_gate_boundary_matrix_v1.json",
    "display_gate_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "display_gate_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_planning",
    )
    p.add_argument(
        "--provider-abstraction-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "provider_abstraction_standard_alignment_dryrun_and_review"
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
    provider_dr_root = Path(args.provider_abstraction_dryrun_root)
    safety_dr_root = Path(args.safety_gate_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    provider_dr_vr = _load(provider_dr_root / "verifier_report.json")
    provider_dr_sm = _load(provider_dr_root / "summary.json")
    safety_dr_vr = _load(safety_dr_root / "verifier_report.json")
    safety_model = _load(safety_dr_root / "safety_gate_model_candidate_v1.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "display_gate_planning_policy_v1.json")
    input_review = _load(root / "provider_abstraction_alignment_input_review_v1.json")
    module_def = _load(root / "display_gate_module_definition_v1.json")
    enforcement_intake = _load(root / "display_gate_enforcement_result_intake_contract_v1.json")
    user_intake = _load(root / "display_gate_user_output_candidate_intake_contract_v1.json")
    result_contract = _load(root / "display_gate_result_candidate_contract_v1.json")
    taxonomy = _load(root / "display_gate_action_taxonomy_v1.json")
    channel = _load(root / "display_channel_admission_rule_plan_v1.json")
    content = _load(root / "display_content_constraint_rule_plan_v1.json")
    uncertainty = _load(root / "display_uncertainty_disclosure_rule_plan_v1.json")
    privacy = _load(root / "display_privacy_masking_rule_plan_v1.json")
    layout = _load(root / "display_layout_boundary_plan_v1.json")
    notification = _load(root / "display_notification_boundary_plan_v1.json")
    refusal = _load(root / "display_refusal_hold_degrade_plan_v1.json")
    handoff = _load(root / "display_gate_downstream_handoff_plan_v1.json")
    no_raw = _load(root / "display_gate_no_raw_constitution_binding_policy_v1.json")
    exec_boundary = _load(root / "display_gate_execution_layer_boundary_plan_v1.json")
    trace = _load(root / "display_gate_traceability_plan_v1.json")
    boundary = _load(root / "display_gate_boundary_matrix_v1.json")
    dryrun = _load(root / "display_gate_dryrun_plan_v1.json")
    decision = _load(root / "display_gate_planning_decision_v1.json")

    ok("upstream.provider_go", provider_dr_vr.get("verifier") == "GO")
    ok("upstream.provider_final", provider_dr_sm.get("final_decision") == PROVIDER_ABS_DR_FINAL)
    ok("upstream.provider_next", provider_dr_sm.get("recommended_next_phase") == PROVIDER_ABS_DR_NEXT)
    ok("upstream.safety_dr_go", safety_dr_vr.get("verifier") == "GO")
    ok("upstream.safety_dr_final", _load(safety_dr_root / "summary.json").get("final_decision") == SAFETY_DR_FINAL)
    ok("upstream.emits_enforcement", safety_model.get("emits_enforcement_result_candidate") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("display_gate_planning_only") is True)
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
    ok("policy.display_enforcement", policy.get("display_gate_is_enforcement_not_execution") is True)
    ok("policy.exec_later", policy.get("execution_consumes_display_gate_result_later") is True)
    ok("policy.four_layer", policy.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)
    for pos in DISPLAY_GATE_LAYER_POSITIONING:
        ok(f"policy.pos.{pos[:18]}", pos in (policy.get("display_gate_layer_positioning") or []))

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.display_defer", input_review.get("display_gate_deferred_not_skipped") is True)
    ok("input.enforcement_layer", input_review.get("display_gate_is_enforcement_layer") is True)
    ok("input.exec_layer", input_review.get("display_output_is_execution_layer") is True)
    ok("input.emits", input_review.get("safety_gate_emits_enforcement_result") is True)
    ok("input.no_raw", input_review.get("display_gate_no_raw_constitution") is True)

    identity = module_def.get("module_identity") or {}
    processing = module_def.get("processing_scope") or {}
    runtime = module_def.get("runtime_boundaries") or {}
    valid, issues = validate_module_definition(module_def)
    ok("module.valid", valid and len(issues) == 0)
    ok("module.id", identity.get("module_id") == "midplatform_display_gate_v1")
    ok("module.type", identity.get("module_type") == "midplatform_user_output_gate_module")
    ok("module.role", identity.get("role") == "display_output_enforcement_gate")
    ok("module.layer", identity.get("system_layer") == "Validation")
    ok("module.arch_layer", identity.get("architectural_layer") == "Enforcement")
    ok("module.runtime_off", identity.get("runtime_enabled_now") is False)
    ok("module.no_write", processing.get("write_allowed") is False)
    ok("module.runtime_bound_off", runtime.get("runtime_enabled_now") is False)

    downstream = module_def.get("downstream_targets") or {}
    downstream_mods = downstream.get("downstream_modules") or []
    ok("module.down_display", "display_output_later" in downstream_mods)
    ok("module.down_notification", "notification_gate_later" in downstream_mods)
    ok("module.down_no_output", "no_output_handler_later" in downstream_mods)

    output_contract = module_def.get("output_contract") or {}
    ok("module.display_result", output_contract.get("output_object_type") == "display_gate_result_candidate")
    ok("module.exec_reads_display", output_contract.get("execution_layer_consumes_display_gate_result") is True)
    ok("module.no_display_out", output_contract.get("display_output_allowed") is False)

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
    for field in ENFORCEMENT_RESULT_INTAKE_FIELDS:
        ok(f"enforcement.{field[:15]}", field in (enforcement_intake.get("required_fields") or []))

    ok("user_intake.fields17", len(user_intake.get("required_fields") or []) == 17)
    u_defaults = user_intake.get("defaults") or {}
    ok("user_intake.no_facing", u_defaults.get("user_facing_output_allowed") is False)
    ok("user_intake.no_display", u_defaults.get("display_output_allowed") is False)
    ok("user_intake.not_fact", u_defaults.get("fact_status") == "not_fact")
    for field in USER_OUTPUT_INTAKE_FIELDS:
        ok(f"user.{field[:15]}", field in (user_intake.get("required_fields") or []))

    ok("result.fields22", len(result_contract.get("required_fields") or []) == 22)
    ok("result.not_execution", result_contract.get("not_execution_output") is True)
    r_defaults = result_contract.get("defaults") or {}
    ok("result.no_display_out", r_defaults.get("display_output_allowed") is False)
    for field in DISPLAY_GATE_RESULT_FIELDS:
        ok(f"result.{field[:15]}", field in (result_contract.get("required_fields") or []))

    ok("taxonomy.count13", taxonomy.get("action_count") == 13)
    for action in DISPLAY_ACTION_TAXONOMY:
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

    ok("privacy.count5", privacy.get("rule_count") == 5)
    for rule in PRIVACY_MASKING_RULES:
        ok(f"privacy.{rule[:18]}", rule in (privacy.get("rules") or []))

    ok("layout.count6", layout.get("rule_count") == 6)
    for rule in LAYOUT_BOUNDARY_RULES:
        ok(f"layout.{rule[:18]}", rule in (layout.get("rules") or []))

    ok("notification.count5", notification.get("rule_count") == 5)
    for rule in NOTIFICATION_BOUNDARY_RULES:
        ok(f"notification.{rule[:18]}", rule in (notification.get("rules") or []))

    ok("refusal.count6", refusal.get("mapping_count") == 6)
    for m in REFUSAL_HOLD_DEGRADE_MAPPINGS:
        ok(
            f"refusal.{m['safety_signal'][:18]}",
            any(
                x.get("safety_signal") == m["safety_signal"] and x.get("display_path") == m["display_path"]
                for x in (refusal.get("mappings") or [])
            ),
        )

    ok("handoff.count6", handoff.get("handoff_count") == 6)
    ok("handoff.display_exec_split", handoff.get("display_gate_enforcement_display_output_execution") is True)
    ok("handoff.no_runtime", handoff.get("no_downstream_runtime_invoked_now") is True)
    for m in DOWNSTREAM_HANDOFF_MAPPINGS:
        ok(
            f"handoff.{m['display_action'][:18]}",
            any(
                x.get("display_action") == m["display_action"] and x.get("handoff") == m["handoff"]
                for x in (handoff.get("handoffs") or [])
            ),
        )

    ok("no_raw.count6", no_raw.get("rule_count") == 6)
    ok("no_raw.enforcement_only", no_raw.get("consumes_enforcement_result_only") is True)
    for rule in NO_RAW_CONSTITUTION_RULES:
        ok(f"noraw.{rule[:18]}", rule in (no_raw.get("rules") or []))

    ok("exec_boundary.count7", exec_boundary.get("rule_count") == 7)
    ok("exec_boundary.not_ui", exec_boundary.get("display_pass_not_display_output_or_ui") is True)
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
    ok("decision.layer_pos", len(decision.get("display_gate_layer_positioning") or []) >= 6)

    ok("template_id", summary.get("template_id") == TEMPLATE_ID)
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("planning_pass") is True
    go = passed == total and pass_all and total > 0

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "HOLD",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": MIN_CHECKS if MIN_CHECKS else total,
        "planning_pass": pass_all,
        "checks": checks,
        "non_claims": list(NON_CLAIMS),
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
