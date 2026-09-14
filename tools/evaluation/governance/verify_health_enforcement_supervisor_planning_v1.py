#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Health Enforcement Supervisor Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.health_enforcement_supervisor_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_FALSE,
    BOUNDARY_TRUE,
    BOUNDARY_VIOLATION_DETECTION_RULES,
    BYPASS_PREVENTION_RULES,
    CORE_CHAIN_BOUNDARY,
    DEGRADATION_HOLD_MAPPINGS,
    DOWNSTREAM_HANDOFF_MAPPINGS,
    ENFORCEMENT_OVERRIDE_FORBIDDEN_RULES,
    FINAL_DECISION_GO,
    GATE_COMPLIANCE_MONITORING_RULES,
    GATE_RESULT_INTAKE_FIELDS,
    HEALTH_SIGNAL_BINDING_RULES,
    HEALTH_SIGNAL_INTAKE_FIELDS,
    NEXT_PHASE_GO,
    NO_RAW_CONSTITUTION_RULES,
    NON_CLAIMS,
    PHASE_ID,
    RUNTIME_RECOMMENDATION_RULES,
    SCOPE,
    SUPERVISED_GATES,
    SUPERVISION_ACTION_TAXONOMY,
    SUPERVISION_RESULT_FIELDS,
    SUPERVISOR_LAYER_POSITIONING,
    TRACEABILITY_REQUIREMENTS,
)
from capabilities.governance.midplatform_display_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DISPLAY_DR_FINAL,
    NEXT_PHASE_GO as DISPLAY_DR_NEXT,
)
from capabilities.governance.midplatform_module_definition_template_v1 import (
    TEMPLATE_ID,
    TEMPLATE_SECTIONS,
    validate_module_definition,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE

MIN_CHECKS = 280

REQUIRED = (
    "health_enforcement_supervisor_planning_policy_v1.json",
    "display_gate_dryrun_input_review_v1.json",
    "health_management_input_review_v1.json",
    "health_enforcement_supervisor_module_definition_v1.json",
    "health_enforcement_supervisor_health_signal_intake_contract_v1.json",
    "health_enforcement_supervisor_gate_result_intake_contract_v1.json",
    "health_enforcement_supervision_result_candidate_contract_v1.json",
    "health_enforcement_supervision_action_taxonomy_v1.json",
    "gate_compliance_monitoring_rule_plan_v1.json",
    "health_signal_binding_rule_plan_v1.json",
    "boundary_violation_detection_rule_plan_v1.json",
    "bypass_prevention_rule_plan_v1.json",
    "enforcement_override_forbidden_rule_plan_v1.json",
    "runtime_recommendation_rule_plan_v1.json",
    "health_enforcement_degrade_hold_plan_v1.json",
    "health_enforcement_supervisor_downstream_handoff_plan_v1.json",
    "health_enforcement_supervisor_no_raw_constitution_binding_policy_v1.json",
    "health_enforcement_supervisor_traceability_plan_v1.json",
    "health_enforcement_supervisor_boundary_matrix_v1.json",
    "health_enforcement_supervisor_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "health_enforcement_supervisor_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/health_enforcement_supervisor_planning",
    )
    p.add_argument(
        "--display-gate-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_display_gate_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--health-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "health_management_layer_integration_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    display_dr_root = Path(args.display_gate_dryrun_root)
    health_post_root = Path(args.health_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    display_dr_vr = _load(display_dr_root / "verifier_report.json")
    display_dr_sm = _load(display_dr_root / "summary.json")
    next_route = _load(display_dr_root / "next_route_readiness_decision_v1.json")
    display_model = _load(display_dr_root / "display_gate_model_candidate_v1.json")
    health_post_vr = _load(health_post_root / "verifier_report.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "health_enforcement_supervisor_planning_policy_v1.json")
    display_review = _load(root / "display_gate_dryrun_input_review_v1.json")
    health_review = _load(root / "health_management_input_review_v1.json")
    module_def = _load(root / "health_enforcement_supervisor_module_definition_v1.json")
    health_intake = _load(root / "health_enforcement_supervisor_health_signal_intake_contract_v1.json")
    gate_intake = _load(root / "health_enforcement_supervisor_gate_result_intake_contract_v1.json")
    result_contract = _load(root / "health_enforcement_supervision_result_candidate_contract_v1.json")
    taxonomy = _load(root / "health_enforcement_supervision_action_taxonomy_v1.json")
    compliance = _load(root / "gate_compliance_monitoring_rule_plan_v1.json")
    health_binding = _load(root / "health_signal_binding_rule_plan_v1.json")
    boundary_violation = _load(root / "boundary_violation_detection_rule_plan_v1.json")
    bypass = _load(root / "bypass_prevention_rule_plan_v1.json")
    override_forbidden = _load(root / "enforcement_override_forbidden_rule_plan_v1.json")
    runtime_rec = _load(root / "runtime_recommendation_rule_plan_v1.json")
    degrade_hold = _load(root / "health_enforcement_degrade_hold_plan_v1.json")
    handoff = _load(root / "health_enforcement_supervisor_downstream_handoff_plan_v1.json")
    no_raw = _load(root / "health_enforcement_supervisor_no_raw_constitution_binding_policy_v1.json")
    trace = _load(root / "health_enforcement_supervisor_traceability_plan_v1.json")
    boundary = _load(root / "health_enforcement_supervisor_boundary_matrix_v1.json")
    dryrun = _load(root / "health_enforcement_supervisor_dryrun_plan_v1.json")
    decision = _load(root / "health_enforcement_supervisor_planning_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("upstream.display_dr_go", display_dr_vr.get("verifier") == "GO")
    ok("upstream.display_dr_final", display_dr_sm.get("final_decision") == DISPLAY_DR_FINAL)
    ok("upstream.display_dr_next", display_dr_sm.get("recommended_next_phase") == DISPLAY_DR_NEXT)
    ok("upstream.ready_for_supervisor", next_route.get("ready_for_health_enforcement_supervisor_planning") is True)
    ok("upstream.display_enforcement", display_model.get("architectural_layer") == "Enforcement")
    ok("upstream.health_post_go", health_post_vr.get("verifier") == "GO")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("health_enforcement_supervisor_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.boundary", summary.get("core_chain_boundary") == CORE_CHAIN_BOUNDARY)
    ok("summary.controlled_runtime_defer", summary.get("controlled_runtime_deferred_not_cancelled") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.gate_health_only", policy.get("gate_results_and_health_signals_only_not_raw_clauses") is True)
    ok("policy.supervisory", policy.get("supervisor_is_supervisory_not_enforcement") is True)
    ok("policy.runtime_later", policy.get("controlled_runtime_consumes_supervision_result_later") is True)
    ok("policy.four_layer", policy.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)
    for pos in SUPERVISOR_LAYER_POSITIONING:
        ok(f"policy.pos.{pos[:18]}", pos in (policy.get("supervisor_layer_positioning") or []))

    ok("display_review.pass", display_review.get("review_pass") is True)
    ok("display_review.supervisor_not_gate", display_review.get("supervisor_is_not_enforcement_gate") is True)
    ok("display_review.monitors", display_review.get("supervisor_monitors_enforcement_compliance") is True)
    ok("health_review.pass", health_review.get("review_pass") is True)
    ok("health_review.metric_reserved", health_review.get("health_metric_reserved_not_defined") is True)

    identity = module_def.get("module_identity") or {}
    processing = module_def.get("processing_scope") or {}
    runtime = module_def.get("runtime_boundaries") or {}
    valid, issues = validate_module_definition(module_def)
    ok("module.valid", valid and len(issues) == 0)
    ok("module.id", identity.get("module_id") == "health_enforcement_supervisor_v1")
    ok("module.type", identity.get("module_type") == "health_management_supervisory_module")
    ok("module.role", identity.get("role") == "enforcement_layer_health_supervisor")
    ok("module.layer", identity.get("system_layer") == "Health Management")
    ok("module.arch_layer", identity.get("architectural_layer") == "Supervision")
    ok("module.runtime_off", identity.get("runtime_enabled_now") is False)
    ok("module.no_write", processing.get("write_allowed") is False)
    ok("module.no_gate_invoke", runtime.get("gate_invocation_allowed_now") is False)
    ok("module.no_override", runtime.get("enforcement_override_allowed_now") is False)

    principles = module_def.get("module_principles") or {}
    for gate in SUPERVISED_GATES:
        ok(f"module.supervised.{gate}", gate in (principles.get("supervised_gates") or []))

    output_contract = module_def.get("output_contract") or {}
    ok(
        "module.supervision_result",
        output_contract.get("output_object_type") == "health_enforcement_supervision_result_candidate",
    )
    ok("module.no_runtime_enable", output_contract.get("runtime_enable_allowed") is False)

    for section in TEMPLATE_SECTIONS:
        ok(f"section.{section[:12]}", section in module_def)

    ok("health_intake.fields17", len(health_intake.get("required_fields") or []) == 17)
    ok("health_intake.not_generated", health_intake.get("health_signal_generated_now") is False)
    for field in HEALTH_SIGNAL_INTAKE_FIELDS:
        ok(f"health.{field[:15]}", field in (health_intake.get("required_fields") or []))

    ok("gate_intake.fields15", len(gate_intake.get("required_fields") or []) == 15)
    ok("gate_intake.gates5", len(gate_intake.get("supervised_gates") or []) == 5)
    ok("gate_intake.no_raw", gate_intake.get("raw_constitution_clause_binding_forbidden") is True)
    for field in GATE_RESULT_INTAKE_FIELDS:
        ok(f"gate.{field[:15]}", field in (gate_intake.get("required_fields") or []))

    ok("result.fields18", len(result_contract.get("required_fields") or []) == 18)
    ok("result.not_runtime", result_contract.get("not_runtime_output") is True)
    for field in SUPERVISION_RESULT_FIELDS:
        ok(f"result.{field[:15]}", field in (result_contract.get("required_fields") or []))

    ok("taxonomy.count12", taxonomy.get("action_count") == 12)
    for action in SUPERVISION_ACTION_TAXONOMY:
        ok(f"action.{action[:18]}", action in (taxonomy.get("actions") or []))

    ok("compliance.count7", compliance.get("rule_count") == 7)
    for rule in GATE_COMPLIANCE_MONITORING_RULES:
        ok(f"compliance.{rule[:18]}", rule in (compliance.get("rules") or []))

    ok("health_binding.count6", health_binding.get("rule_count") == 6)
    for rule in HEALTH_SIGNAL_BINDING_RULES:
        ok(f"health_bind.{rule[:18]}", rule in (health_binding.get("rules") or []))

    ok("boundary_violation.count6", boundary_violation.get("rule_count") == 6)
    for rule in BOUNDARY_VIOLATION_DETECTION_RULES:
        ok(f"boundary.{rule[:18]}", rule in (boundary_violation.get("rules") or []))

    ok("bypass.count6", bypass.get("rule_count") == 6)
    for rule in BYPASS_PREVENTION_RULES:
        ok(f"bypass.{rule[:18]}", rule in (bypass.get("rules") or []))

    ok("override.count6", override_forbidden.get("rule_count") == 6)
    for rule in ENFORCEMENT_OVERRIDE_FORBIDDEN_RULES:
        ok(f"override.{rule[:18]}", rule in (override_forbidden.get("rules") or []))

    ok("runtime_rec.count6", runtime_rec.get("rule_count") == 6)
    for rule in RUNTIME_RECOMMENDATION_RULES:
        ok(f"runtime.{rule[:18]}", rule in (runtime_rec.get("rules") or []))

    ok("degrade_hold.count6", degrade_hold.get("mapping_count") == 6)
    for m in DEGRADATION_HOLD_MAPPINGS:
        key = m.get("health_signal") or m.get("gate_signal") or ""
        ok(
            f"degrade.{key[:18]}",
            any(
                (x.get("health_signal") == m.get("health_signal") or x.get("gate_signal") == m.get("gate_signal"))
                and x.get("supervision_path") == m.get("supervision_path")
                for x in (degrade_hold.get("mappings") or [])
            ),
        )

    ok("handoff.count5", handoff.get("handoff_count") == 5)
    ok("handoff.not_runtime", handoff.get("supervision_not_runtime_enable") is True)
    for m in DOWNSTREAM_HANDOFF_MAPPINGS:
        ok(
            f"handoff.{m['supervision_action'][:18]}",
            any(
                x.get("supervision_action") == m["supervision_action"]
                and x.get("handoff") == m["handoff"]
                for x in (handoff.get("handoffs") or [])
            ),
        )

    ok("no_raw.count5", no_raw.get("rule_count") == 5)
    ok("no_raw.consumes_only", no_raw.get("consumes_gate_results_and_health_signals_only") is True)
    for rule in NO_RAW_CONSTITUTION_RULES:
        ok(f"no_raw.{rule[:18]}", rule in (no_raw.get("rules") or []))

    ok("trace.count8", trace.get("requirement_count") == 8)
    for req in TRACEABILITY_REQUIREMENTS:
        ok(f"trace.{req[:18]}", req in (trace.get("requirements") or []))

    ok("boundary.matrix21", len(boundary.get("matrix") or {}) == 21)
    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:18]}", (boundary.get("matrix") or {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.next", decision.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("decision.gates5", len(decision.get("supervised_gates") or []) == 5)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

    ok("template.id", summary.get("template_id") == TEMPLATE_ID)

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    verifier = "GO" if passed == total and passed >= (MIN_CHECKS if MIN_CHECKS else total) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": MIN_CHECKS if MIN_CHECKS else total,
        "planning_pass": summary.get("planning_pass"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
