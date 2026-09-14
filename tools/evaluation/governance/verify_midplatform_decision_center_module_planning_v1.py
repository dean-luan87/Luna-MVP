#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Decision Center Module Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_decision_center_module_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONFLICT_RULES,
    CORE_PRINCIPLE,
    DECISION_ACTIONS,
    DECISION_CENTER_NOT,
    FINAL_DECISION_GO,
    GOVERNANCE_BINDINGS,
    INPUT_CONTRACT_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_CONTRACT_FIELDS,
    PHASE_ID,
    PRIORITY_LAYERS,
    RATIONALE_REQUIREMENTS,
    RUNTIME_BOUNDARY_MATRIX_FALSE,
    SCOPE,
    UPSTREAM_CORE_RESUME_FINAL,
)

MIN_CHECKS = 214

REQUIRED = (
    "decision_center_module_planning_policy_v1.json",
    "midplatform_core_resume_input_review_v1.json",
    "decision_center_module_definition_v1.json",
    "decision_center_governance_binding_model_v1.json",
    "constitution_to_decision_binding_plan_v1.json",
    "validation_to_decision_binding_plan_v1.json",
    "health_to_decision_binding_plan_v1.json",
    "whitebox_to_decision_binding_plan_v1.json",
    "factory_domain_candidate_to_decision_binding_plan_v1.json",
    "decision_center_input_contract_v1.json",
    "decision_center_output_contract_v1.json",
    "decision_action_taxonomy_v1.json",
    "decision_priority_and_conflict_policy_v1.json",
    "decision_rationale_and_traceability_plan_v1.json",
    "decision_to_task_response_boundary_plan_v1.json",
    "decision_center_runtime_boundary_matrix_v1.json",
    "decision_center_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "decision_center_module_planning_decision_v1.json",
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
            "midplatform_decision_center_module_planning"
        ),
    )
    p.add_argument(
        "--core-resume-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_core_architecture_resume"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    core_root = Path(args.core_resume_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    core_vr = _load(core_root / "verifier_report.json")
    core_sm = _load(core_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "decision_center_module_planning_policy_v1.json")
    resume_input = _load(root / "midplatform_core_resume_input_review_v1.json")
    module_def = _load(root / "decision_center_module_definition_v1.json")
    binding_model = _load(root / "decision_center_governance_binding_model_v1.json")
    constitution = _load(root / "constitution_to_decision_binding_plan_v1.json")
    validation = _load(root / "validation_to_decision_binding_plan_v1.json")
    health = _load(root / "health_to_decision_binding_plan_v1.json")
    whitebox = _load(root / "whitebox_to_decision_binding_plan_v1.json")
    factory = _load(root / "factory_domain_candidate_to_decision_binding_plan_v1.json")
    input_contract = _load(root / "decision_center_input_contract_v1.json")
    output_contract = _load(root / "decision_center_output_contract_v1.json")
    actions = _load(root / "decision_action_taxonomy_v1.json")
    priority = _load(root / "decision_priority_and_conflict_policy_v1.json")
    rationale = _load(root / "decision_rationale_and_traceability_plan_v1.json")
    task_boundary = _load(root / "decision_to_task_response_boundary_plan_v1.json")
    runtime_matrix = _load(root / "decision_center_runtime_boundary_matrix_v1.json")
    dryrun = _load(root / "decision_center_dryrun_plan_v1.json")
    planning_decision = _load(root / "decision_center_module_planning_decision_v1.json")

    ok("upstream.core_go", core_vr.get("verifier") == "GO")
    ok("upstream.core_final", core_sm.get("final_decision") == UPSTREAM_CORE_RESUME_FINAL)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.module_only", summary.get("decision_center_module_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.principle", summary.get("core_principle") == CORE_PRINCIPLE)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.module", policy.get("module_planning_not_runtime") is True)
    ok("policy.consumer", policy.get("decision_center_is_governance_consumer_not_author") is True)

    ok("resume.pass", resume_input.get("review_pass") is True)
    ok("resume.constitution", resume_input.get("constitution_remains_rule_source") is True)
    ok("resume.validation", resume_input.get("validation_remains_executor_gatekeeper") is True)
    ok("resume.health", resume_input.get("health_remains_pressure_signal_source") is True)
    ok("resume.whitebox", resume_input.get("whitebox_remains_visibility_layer") is True)
    ok("resume.no_replace", resume_input.get("decision_center_does_not_replace_upstream") is True)

    ok("module.id", module_def.get("module_id") == "midplatform_decision_center_v1")
    ok("module.type", module_def.get("module_type") == "core_midplatform_governance_module")
    ok("module.role", module_def.get("role") == "decision_arbitration_and_candidate_routing")
    ok("module.no_runtime", module_def.get("runtime_enabled_now") is False)
    ok("module.constitution", module_def.get("consumes_constitution") is True)
    ok("module.validation", module_def.get("consumes_validation") is True)
    ok("module.health", module_def.get("consumes_health") is True)
    ok("module.whitebox", module_def.get("consumes_whitebox_visibility") is True)
    ok("module.candidate", module_def.get("consumes_candidate_and_evidence") is True)
    ok("module.emit_later", module_def.get("emits_decision_candidate_later") is True)
    ok("module.not_kingdom", module_def.get("not_independent_kingdom") is True)

    for not_role in DECISION_CENTER_NOT:
        ok(f"not.{not_role[:15]}", not_role in (module_def.get("decision_center_is_not") or []))

    ok("binding.principle", binding_model.get("core_principle") == CORE_PRINCIPLE)
    ok("binding.count5", len(binding_model.get("bindings") or []) == 5)
    for b in GOVERNANCE_BINDINGS:
        ok(f"bind.{b['binding_id'][:12]}", any(
            x.get("binding_id") == b["binding_id"] for x in (binding_model.get("bindings") or [])
        ))
    ok("binding.consumes", binding_model.get("decision_center_consumes_bindings") is True)
    ok("binding.no_author", binding_model.get("decision_center_does_not_author_bindings") is True)
    ok("binding.no_override", binding_model.get("decision_center_cannot_override_constitution") is True)
    ok("binding.no_fail_allow", binding_model.get("failed_validation_cannot_become_allow_without_higher_rule") is True)
    ok("binding.no_health_score", binding_model.get("decision_center_cannot_invent_health_score") is True)

    ok("const.highest", constitution.get("general_constitution_highest_priority") is True)
    ok("const.domain", constitution.get("domain_constitution_constrains_domain_candidate") is True)
    ok("const.overlay", constitution.get("personalized_constitution_overlay_only") is True)
    ok("const.block", constitution.get("constitution_block_action") == "block_candidate")
    ok("const.conservative", constitution.get("constitution_conflict_conservative_decision") is True)

    ok("val.pass_cond", validation.get("validation_pass_may_proceed_if_no_higher_block") is True)
    ok("val.fail", "block_candidate" in (validation.get("validation_fail_action") or ""))
    ok("val.violation", "violation_report_candidate" in (validation.get("boundary_violation_action") or ""))
    ok("val.no_exec", validation.get("decision_center_does_not_execute_validation_gate") is True)

    ok("health.pressure", health.get("health_signal_is_pressure_status_context") is True)
    ok("health.reserved", health.get("health_metric_definition_status") == "reserved_not_defined")
    ok("health.no_score", health.get("no_numeric_health_score_invented") is True)
    ok("health.no_auth", health.get("health_does_not_authorize_execution_by_itself") is True)
    ok("health.no_override", health.get("health_cannot_override_constitution_validation") is True)

    ok("wb.rationale", whitebox.get("whitebox_visibility_provides_rationale_refs") is True)
    ok("wb.no_decide", whitebox.get("whitebox_does_not_decide") is True)
    ok("wb.node_not_global", whitebox.get("node_level_evidence_cannot_define_global_health") is True)

    ok("factory.produces", factory.get("capability_factory_produces_candidate") is True)
    ok("factory.inspects", factory.get("validation_factory_inspects_candidate") is True)
    ok("factory.domain", factory.get("domain_config_gives_domain_constraints") is True)
    ok("factory.no_module_logic", factory.get("no_module_specific_decision_logic_outside_decision_center") is True)

    ok("input.candidate", input_contract.get("candidate_only") is True)
    ok("input.fields16", len(input_contract.get("required_fields") or []) == 16)
    for field in INPUT_CONTRACT_FIELDS:
        ok(f"input.{field[:15]}", field in (input_contract.get("required_fields") or []))

    ok("output.type", output_contract.get("output_type") == "decision_candidate")
    ok("output.fields22", len(output_contract.get("required_fields") or []) == 22)
    for field in OUTPUT_CONTRACT_FIELDS:
        ok(f"output.{field[:15]}", field in (output_contract.get("required_fields") or []))
    defaults = output_contract.get("defaults") or {}
    ok("output.no_task", defaults.get("task_response_generation_allowed") is False)
    ok("output.no_user", defaults.get("user_output_allowed") is False)

    ok("actions.count13", len(actions.get("actions") or []) == 13)
    for action in DECISION_ACTIONS:
        ok(f"action.{action[:18]}", action in (actions.get("actions") or []))

    ok("priority.layers9", len(priority.get("priority_layers") or []) == 9)
    for layer in PRIORITY_LAYERS:
        ok(f"priority.{layer['priority']}", any(
            l.get("priority") == layer["priority"] for l in (priority.get("priority_layers") or [])
        ))
    for rule in CONFLICT_RULES:
        ok(f"conflict.{rule[:18]}", rule in (priority.get("conflict_rules") or []))

    ok("rationale.count11", len(rationale.get("requirements") or []) == 11)
    for req in RATIONALE_REQUIREMENTS:
        ok(f"rationale.{req[:18]}", req in (rationale.get("requirements") or []))

    ok("boundary.dec_not_task", task_boundary.get("decision_candidate_not_task_response_candidate") is True)
    ok("boundary.no_speak", task_boundary.get("decision_center_cannot_directly_speak_to_user") is True)

    ok("runtime.all_false", runtime_matrix.get("all_runtime_actions_false") is True)
    for field in RUNTIME_BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:15]}", runtime_matrix.get("matrix", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", planning_decision.get("planning_pass") is True)
    ok("decision.final", planning_decision.get("final_decision") == FINAL_DECISION_GO)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

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
        "core_principle": CORE_PRINCIPLE,
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
