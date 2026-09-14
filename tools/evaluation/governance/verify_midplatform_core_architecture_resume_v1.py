#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Core Architecture Resume v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_core_architecture_resume_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CEVDR_FLOW_STEPS,
    CHV_CONSUMPTION,
    DECISION_CENTER_DUTIES,
    DEFERRED_ROUTES,
    DOMAIN_CONFIG_DOMAINS,
    FACTORY_MARKET_FLOW,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    MIDPLATFORM_BOUNDARIES,
    MIDPLATFORM_CORE_RESPONSIBILITIES,
    MIDPLATFORM_NOT,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OBJECT_FLOW_TYPES,
    PHASE_ID,
    RUNTIME_BOUNDARY_MATRIX_FALSE,
    SCOPE,
    UPSTREAM_WHITEBOX_DR_FINAL,
)

MIN_CHECKS = 182

REQUIRED = (
    "midplatform_core_architecture_resume_policy_v1.json",
    "upstream_governance_input_review_v1.json",
    "midplatform_core_role_definition_v1.json",
    "midplatform_boundary_definition_v1.json",
    "midplatform_object_flow_model_v1.json",
    "candidate_evidence_validation_decision_response_flow_v1.json",
    "decision_center_role_plan_v1.json",
    "constitution_health_validation_consumption_plan_v1.json",
    "factory_validation_market_flow_plan_v1.json",
    "domain_config_consumption_plan_v1.json",
    "task_response_candidate_integration_plan_v1.json",
    "evidence_and_traceability_flow_plan_v1.json",
    "failure_route_and_escalation_plan_v1.json",
    "midplatform_runtime_boundary_matrix_v1.json",
    "next_mainline_route_decision_v1.json",
    "non_claims_register_v1.json",
    "midplatform_core_architecture_resume_decision_v1.json",
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
            "midplatform_core_architecture_resume"
        ),
    )
    p.add_argument(
        "--whitebox-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_whitebox_inspection_integration_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    whitebox_root = Path(args.whitebox_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    whitebox_vr = _load(whitebox_root / "verifier_report.json")
    whitebox_sm = _load(whitebox_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "midplatform_core_architecture_resume_policy_v1.json")
    upstream = _load(root / "upstream_governance_input_review_v1.json")
    core_role = _load(root / "midplatform_core_role_definition_v1.json")
    boundary = _load(root / "midplatform_boundary_definition_v1.json")
    object_flow = _load(root / "midplatform_object_flow_model_v1.json")
    cevdr = _load(root / "candidate_evidence_validation_decision_response_flow_v1.json")
    decision_center = _load(root / "decision_center_role_plan_v1.json")
    chv = _load(root / "constitution_health_validation_consumption_plan_v1.json")
    factory = _load(root / "factory_validation_market_flow_plan_v1.json")
    domain = _load(root / "domain_config_consumption_plan_v1.json")
    task_resp = _load(root / "task_response_candidate_integration_plan_v1.json")
    evidence = _load(root / "evidence_and_traceability_flow_plan_v1.json")
    failure = _load(root / "failure_route_and_escalation_plan_v1.json")
    runtime_matrix = _load(root / "midplatform_runtime_boundary_matrix_v1.json")
    next_route = _load(root / "next_mainline_route_decision_v1.json")
    resume_decision = _load(root / "midplatform_core_architecture_resume_decision_v1.json")

    ok("upstream.whitebox_go", whitebox_vr.get("verifier") == "GO")
    ok("upstream.whitebox_final", whitebox_sm.get("final_decision") == UPSTREAM_WHITEBOX_DR_FINAL)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.resume_only", summary.get("midplatform_core_architecture_resume_only") is True)
    ok("summary.pass", summary.get("resume_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.resume_only", policy.get("architecture_resume_not_runtime") is True)
    ok("policy.ocr_sealed", policy.get("ocr_branch_sealed") is True)
    ok("policy.whitebox_sealed", policy.get("whitebox_absorption_sealed") is True)

    ok("upstream.pass", upstream.get("review_pass") is True)
    ok("upstream.no_parallel", upstream.get("whitebox_absorption_not_parallel") is True)
    ok("upstream.val_gatekeeper", upstream.get("validation_engineering_remains_gatekeeper") is True)
    ok("upstream.constitution_source", upstream.get("constitution_remains_rule_source") is True)
    ok("upstream.health_source", upstream.get("health_remains_pressure_signal_source") is True)
    ok("upstream.ocr_readonly", upstream.get("ocr_real_dep_node_level_read_only") is True)

    ok("role.resp9", len(core_role.get("midplatform_core_responsibilities") or []) == 9)
    for resp in MIDPLATFORM_CORE_RESPONSIBILITIES:
        ok(f"role.{resp[:18]}", resp in (core_role.get("midplatform_core_responsibilities") or []))

    ok("role.not8", len(core_role.get("midplatform_is_not") or []) == 8)
    for not_role in MIDPLATFORM_NOT:
        ok(f"not.{not_role[:15]}", not_role in (core_role.get("midplatform_is_not") or []))

    ok("role.ocr_sealed", core_role.get("ocr_local_check_status") == "sealed_as_node_level_read_only_evidence")
    ok("role.whitebox_sealed", core_role.get("whitebox_status") == "absorption_integration_complete_not_parallel")

    ok("boundary.count6", len(boundary.get("boundaries") or []) == 6)
    for b in MIDPLATFORM_BOUNDARIES:
        ok(f"boundary.{b['boundary'][:15]}", any(
            x.get("boundary") == b["boundary"] for x in (boundary.get("boundaries") or [])
        ))

    ok("objects.count13", len(object_flow.get("object_types") or []) == 13)
    for obj in OBJECT_FLOW_TYPES:
        ok(f"object.{obj[:15]}", obj in (object_flow.get("object_types") or []))

    ok("cevdr.steps8", len(cevdr.get("steps") or []) == 8)
    for step in CEVDR_FLOW_STEPS:
        ok(f"cevdr.step{step['step']}", any(
            s.get("step") == step["step"] for s in (cevdr.get("steps") or [])
        ))
    ok("cevdr.node_drilldown", cevdr.get("node_level_evidence_drilldown_only") is True)

    ok("dc.duties8", len(decision_center.get("future_duties") or []) == 8)
    for duty in DECISION_CENTER_DUTIES:
        ok(f"dc.{duty[:18]}", duty in (decision_center.get("future_duties") or []))
    ok("dc.no_runtime", decision_center.get("runtime_enabled_now") is False)
    ok("dc.no_bypass", decision_center.get("never_bypass_validation_constitution") is True)

    ok("chv.layers5", len(chv.get("layers") or []) == 5)
    ok("chv.constitution", chv.get("constitution_is_rule_source") is True)
    ok("chv.health", chv.get("health_is_pressure_signal") is True)
    ok("chv.validation", chv.get("validation_is_enforcement") is True)
    ok("chv.whitebox", chv.get("whitebox_is_visibility_layer") is True)
    ok("chv.dc_consumes", chv.get("decision_center_consumes_all_does_not_replace") is True)
    for layer in CHV_CONSUMPTION:
        ok(f"chv.{layer['layer'][:12]}", any(
            x.get("layer") == layer["layer"] for x in (chv.get("layers") or [])
        ))

    ok("factory.count7", len(factory.get("factory_analogy") or []) == 7)
    ok("factory.inspection", factory.get("validation_factory_is_market_inspection") is True)
    ok("factory.midplatform", factory.get("midplatform_is_assembly_decision_center") is True)
    for actor in FACTORY_MARKET_FLOW:
        ok(f"factory.{actor['actor'][:12]}", any(
            x.get("actor") == actor["actor"] for x in (factory.get("factory_analogy") or [])
        ))

    ok("domain.count7", len(domain.get("domains_submit_domain_config") or []) == 7)
    for d in DOMAIN_CONFIG_DOMAINS:
        ok(f"domain.{d}", d in (domain.get("domains_submit_domain_config") or []))
    ok("domain.no_parallel", domain.get("no_parallel_standards_by_new_modules") is True)
    ok("domain.after_validation", domain.get("midplatform_consumes_domain_config_after_validation") is True)

    ok("task.not_output", task_resp.get("task_response_candidate_is_not_user_output") is True)
    ok("task.needs_decision", task_resp.get("task_response_requires_decision_pass") is True)
    ok("task.user_later", task_resp.get("user_output_candidate_requires_output_plane_later") is True)
    ok("task.refs_preserved", task_resp.get("evidence_and_validation_refs_preserved") is True)
    ok("task.uncertainty", task_resp.get("uncertainty_preserved") is True)

    ok("evidence.source_chain", evidence.get("evidence_pack_binds_source_chain") is True)
    ok("evidence.whitebox_consume", evidence.get("whitebox_visibility_consumed_not_replaced") is True)

    ok("failure.count7", len(failure.get("routes") or []) == 7)
    for route in FAILURE_ROUTES:
        ok(f"fail.{route['trigger'][:12]}", any(
            x.get("trigger") == route["trigger"] for x in (failure.get("routes") or [])
        ))

    ok("runtime.all_false", runtime_matrix.get("all_runtime_actions_false") is True)
    for field in RUNTIME_BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:15]}", runtime_matrix.get("matrix", {}).get(field) is False)

    ok("route.route_a", next_route.get("selected_route_id") == "Route A")
    ok("route.next_dc", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("route.ocr_deferred", next_route.get("ocr_provider_work_deferred") is True)
    ok("route.runtime_deferred", next_route.get("runtime_planning_deferred") is True)
    ok("route.defer4", len(next_route.get("deferred_routes") or []) == 4)
    for dr in DEFERRED_ROUTES:
        ok(f"defer.{dr['route_id']}", any(
            x.get("route_id") == dr["route_id"] and x.get("status") == "defer"
            for x in (next_route.get("deferred_routes") or [])
        ))

    ok("decision.pass", resume_decision.get("resume_pass") is True)
    ok("decision.final", resume_decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.mainline", resume_decision.get("mainline_restored") is True)
    ok("decision.ocr_sealed", resume_decision.get("ocr_local_check_sealed") is True)
    ok("decision.whitebox_sealed", resume_decision.get("whitebox_integration_sealed") is True)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("resume_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "resume_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "mainline_restored": True,
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
