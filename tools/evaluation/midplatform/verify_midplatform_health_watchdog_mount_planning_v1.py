#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Health Watchdog Mount Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS
from capabilities.midplatform.midplatform_decision_center_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DC_HANDOFF_DRYRUN_FINAL,
)
from capabilities.midplatform.midplatform_health_watchdog_mount_planning_v1 import (
    ALGORITHM_USES,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DECISION_CENTER_OUTPUTS_CONSUMED,
    DOWNSTREAM_HANDOFFS,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    FORBIDDEN_OUTPUTS,
    HEALTH_METRICS,
    HEALTH_STATES,
    INPUT_REQUIRED_FIELDS,
    INPUT_TYPES,
    MODEL_USES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_CANDIDATES,
    PHASE_ID,
    PROCESSING_STEPS,
    RESPONSIBILITIES,
    RULE_USES,
    SAMPLE_FLOWS,
    SCOPE,
    UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FILES,
    UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FINAL,
    UPSTREAM_DECISION_CENTER_HANDOFF_PLANNING_FILES,
    UPSTREAM_INFORMATION_INTEGRATION_FILES,
    UPSTREAM_MICRO_OS_FILES,
)

MIN_CHECKS = 440

REQUIRED = (
    "summary.json",
    "health_watchdog_mount_scope_v1.json",
    "health_watchdog_mount_contract_v1.json",
    "health_watchdog_input_contract_v1.json",
    "health_watchdog_output_contract_v1.json",
    "health_watchdog_processing_model_v1.json",
    "health_watchdog_health_state_machine_v1.json",
    "health_watchdog_model_rule_algorithm_placement_v1.json",
    "health_watchdog_governance_boundary_v1.json",
    "health_watchdog_recovery_boundary_v1.json",
    "health_watchdog_decision_center_dependency_boundary_v1.json",
    "health_watchdog_downstream_handoff_matrix_v1.json",
    "health_watchdog_sample_flow_plan_v1.json",
    "health_watchdog_failure_route_matrix_v1.json",
    "health_watchdog_mount_health_metric_scope_v1.json",
    "health_watchdog_boundary_matrix_v1.json",
    "health_watchdog_mount_non_claims_v1.json",
    "health_watchdog_mount_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_mount_planning"))
    p.add_argument(
        "--decision-center-handoff-dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_foundation_handoff_dryrun_and_review"),
    )
    p.add_argument(
        "--decision-center-handoff-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_foundation_handoff_planning"),
    )
    p.add_argument(
        "--information-integration-handoff-dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_dryrun_and_review"),
    )
    p.add_argument(
        "--micro-os-freeze-dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    dc_dr = Path(args.decision_center_handoff_dryrun_root)
    dc_plan = Path(args.decision_center_handoff_planning_root)
    ii_dr = Path(args.information_integration_handoff_dryrun_root)
    micro_dr = Path(args.micro_os_freeze_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:30]}", (root / fname).is_file())

    dc_vr = _load(dc_dr / "verifier_report.json")
    dc_sm = _load(dc_dr / "summary.json")
    ok("upstream.dc_go", dc_vr.get("verifier") == "GO")
    ok("upstream.dc_final", dc_sm.get("final_decision") == DC_HANDOFF_DRYRUN_FINAL)
    ok("upstream.dc_match", UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FINAL == DC_HANDOFF_DRYRUN_FINAL)
    ok("upstream.dc_foundation", dc_sm.get("foundation_id") == "midplatform_decision_center_foundation_v1")
    ok("upstream.dc_runtime", dc_sm.get("runtime_status") == "not_enabled")

    for fname in UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FILES:
        ok(f"dcdr.up.{fname[:22]}", (dc_dr / fname).is_file())
    for fname in UPSTREAM_DECISION_CENTER_HANDOFF_PLANNING_FILES:
        ok(f"dcplan.up.{fname[:22]}", (dc_plan / fname).is_file())
    for fname in UPSTREAM_INFORMATION_INTEGRATION_FILES:
        ok(f"ii.up.{fname[:22]}", (ii_dr / fname).is_file())
    for fname in UPSTREAM_MICRO_OS_FILES:
        ok(f"micro.up.{fname[:22]}", (micro_dr / fname).is_file())

    dc_version = _load(dc_plan / "decision_center_foundation_version_tag_v1.json")
    ii_summary = _load(ii_dr / "summary.json")
    micro_summary = _load(micro_dr / "summary.json")
    ok("dc.foundation_id", dc_version.get("foundation_id") == "midplatform_decision_center_foundation_v1")
    ok("dc.depends_on", dc_version.get("depends_on") == "midplatform_information_integration_foundation_v1")
    ok("dc.also_depends", dc_version.get("also_depends_on") == "midplatform_micro_os_foundation_v1")
    ok("dc.version", dc_version.get("version") == "1.0.0-skeleton")
    ok("dc.status", dc_version.get("status") == "frozen_for_downstream_mount_planning")
    ok("dc.runtime", dc_version.get("runtime_status") == "not_enabled")
    ok("ii.foundation", ii_summary.get("foundation_id") == "midplatform_information_integration_foundation_v1")
    ok("micro.foundation", micro_summary.get("foundation_id") == "midplatform_micro_os_foundation_v1")

    summary = _load(root / "summary.json")
    scope = _load(root / "health_watchdog_mount_scope_v1.json")
    contract = _load(root / "health_watchdog_mount_contract_v1.json")
    inp = _load(root / "health_watchdog_input_contract_v1.json")
    out = _load(root / "health_watchdog_output_contract_v1.json")
    proc = _load(root / "health_watchdog_processing_model_v1.json")
    sm = _load(root / "health_watchdog_health_state_machine_v1.json")
    mra = _load(root / "health_watchdog_model_rule_algorithm_placement_v1.json")
    gov = _load(root / "health_watchdog_governance_boundary_v1.json")
    recovery = _load(root / "health_watchdog_recovery_boundary_v1.json")
    dc_dep = _load(root / "health_watchdog_decision_center_dependency_boundary_v1.json")
    handoff = _load(root / "health_watchdog_downstream_handoff_matrix_v1.json")
    samples = _load(root / "health_watchdog_sample_flow_plan_v1.json")
    failures = _load(root / "health_watchdog_failure_route_matrix_v1.json")
    metrics = _load(root / "health_watchdog_mount_health_metric_scope_v1.json")
    boundary = _load(root / "health_watchdog_boundary_matrix_v1.json")
    nc = _load(root / "health_watchdog_mount_non_claims_v1.json")
    readiness = _load(root / "health_watchdog_mount_readiness_decision_v1.json")

    ok("phase.id", summary.get("phase") == PHASE_ID)
    ok("scope.id", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.violations0", len(summary.get("violations") or []) == 0)
    ok("readiness.pass", readiness.get("planning_pass") is True)
    ok("readiness.dc", readiness.get("decision_center_foundation_consumed") is True)
    ok("readiness.no_redefine", readiness.get("must_not_redefine_decision_center") is True)
    ok("readiness.no_recovery", readiness.get("no_real_recovery") is True)

    ok("summary.foundation", summary.get("foundation_id") == "midplatform_decision_center_foundation_v1")
    ok("summary.version", summary.get("foundation_version") == "1.0.0-skeleton")
    ok("summary.runtime", summary.get("runtime_status") == "not_enabled")
    ok("summary.module", summary.get("module_id") == "health_watchdog")

    ok("scope.module", scope.get("module_id") == "health_watchdog")
    ok("scope.layer", scope.get("layer") == "L5_health")
    ok("scope.planning_only", scope.get("mount_planning_only") is True)
    ok("scope.dc_foundation", scope.get("upstream_foundation") == "midplatform_decision_center_foundation_v1")
    ok("scope.no_redefine_dc", scope.get("must_not_redefine_decision_center") is True)
    ok("scope.no_direct_mount", scope.get("direct_mount_executed") is False)

    for item in DECISION_CENTER_OUTPUTS_CONSUMED:
        ok(f"scope.dc_out.{item[:14]}", item in (scope.get("allowed_decision_center_outputs_consumed") or []))
        ok(f"contract.dc_out.{item[:14]}", item in (contract.get("upstream_sources", {}).get("frozen_outputs_consumed") or []))

    for resp in RESPONSIBILITIES:
        ok(f"scope.resp.{resp[:14]}", resp in (scope.get("responsibilities") or []))

    for section in TEMPLATE_SECTIONS:
        ok(f"contract.section.{section[:12]}", section in contract)

    ok("contract.layer", contract.get("module_identity", {}).get("layer") == "L5_health")
    ok("contract.role", "not recovery executor" in contract.get("module_identity", {}).get("role", ""))
    ok("contract.candidate_only", contract.get("output_contract", {}).get("all_candidate") is True)
    ok(
        "contract.no_recovery",
        contract.get("output_contract", {}).get("recovery_recommendation_is_not_recovery_execution") is True,
    )
    ok(
        "contract.no_degrade",
        contract.get("output_contract", {}).get("degradation_candidate_is_not_real_degradation") is True,
    )
    ok("contract.planning_only", contract.get("processing_scope", {}).get("planning_only") is True)
    ok("contract.no_runtime", contract.get("processing_scope", {}).get("runtime_execution") is False)
    ok("contract.no_restart", contract.get("processing_scope", {}).get("module_restart") is False)
    ok("contract.no_process", contract.get("processing_scope", {}).get("process_control") is False)

    for inp_type in INPUT_TYPES:
        ok(f"inp.type.{inp_type[:14]}", inp_type in (inp.get("input_types") or []))
        ok(f"contract.inp.{inp_type[:14]}", inp_type in (contract.get("input_contract", {}).get("input_types") or []))
    for field in INPUT_REQUIRED_FIELDS:
        ok(f"inp.req.{field[:14]}", field in (inp.get("required_fields") or []))
    ok("inp.candidate", inp.get("candidate_not_fact_required") is True)
    ok("inp.trace", inp.get("trace_required") is True)
    ok("inp.health", inp.get("health_tag_required") is True)
    ok("inp.source", inp.get("source_chain_required") is True)
    ok("inp.gov", inp.get("governance_ref_required_for_high_risk_recovery_recommendation") is True)

    for out_type in OUTPUT_CANDIDATES:
        ok(f"out.type.{out_type[:14]}", out_type in (out.get("outputs") or []))
        ok(f"contract.out.{out_type[:14]}", out_type in (contract.get("output_contract", {}).get("outputs") or []))
    ok("out.all_candidate", out.get("all_candidate") is True)
    ok("out.not_recovery", out.get("recovery_recommendation_candidate_is_not_recovery_execution") is True)
    ok("out.not_degrade", out.get("degradation_candidate_is_not_real_degradation") is True)
    ok("out.not_fact", out.get("fact_status") == "not_fact")
    for forbidden in FORBIDDEN_OUTPUTS:
        ok(f"out.forbidden.{forbidden[:12]}", forbidden in (out.get("forbidden_outputs") or []))

    for step in PROCESSING_STEPS:
        ok(f"proc.step.{step[:14]}", step in (proc.get("steps") or []))
    ok("proc.planning_only", proc.get("planning_only") is True)
    ok("proc.no_runtime", proc.get("real_watchdog_runtime_enabled") is False)
    ok("proc.no_recovery", proc.get("recovery_execution") is False)

    for state in HEALTH_STATES:
        ok(f"state.{state[:14]}", state in (sm.get("states") or []))
    ok("state.count15", sm.get("state_count") >= 15)
    ok("state.candidate", sm.get("all_candidate_level") is True)
    ok("state.no_mutation", sm.get("runtime_state_mutation") is False)

    ok("mra.no_model", mra.get("model_invoked_now") is False)
    ok("mra.no_provider", mra.get("provider_invoked_now") is False)
    ok("mra.no_runtime", mra.get("runtime_enabled_now") is False)
    for use in MODEL_USES:
        ok(f"mra.model.{use[:14]}", use in (mra.get("model_uses_later") or []))
    for use in RULE_USES:
        ok(f"mra.rule.{use[:14]}", use in (mra.get("rule_uses") or []))
    for use in ALGORITHM_USES:
        ok(f"mra.algo.{use[:14]}", use in (mra.get("algorithm_uses") or []))

    gov_rules = json.dumps(gov.get("rules") or []).lower()
    ok("gov.no_bypass", "do not bypass" in gov_rules)
    ok("gov.high_risk", "high-risk" in gov_rules and "governance_ref" in gov_rules)
    ok("gov.rec_not_exec", "not recovery execution" in gov_rules)
    ok("gov.degrade_not_real", "not real module degradation" in gov_rules)
    ok("gov.no_runtime", "runtime" in gov_rules)
    ok("gov.no_scheduler", "scheduler priority" in gov_rules)

    rec_rules = json.dumps(recovery.get("rules") or []).lower()
    for phrase in (
        "no real recovery",
        "no restart",
        "no kill process",
        "no permissions release",
        "no module reload",
        "no system command",
        "no emergency output",
        "only recovery_recommendation_candidate",
        "only watchdog_handoff_candidate",
    ):
        ok(f"recovery.{phrase[:14]}", phrase in rec_rules)
    ok("recovery.protocol", "owner-operator" in rec_rules and "recovery protocol" in rec_rules)

    dc_rules = json.dumps(dc_dep.get("rules") or []).lower()
    ok("dcdep.foundation", dc_dep.get("foundation_id") == "midplatform_decision_center_foundation_v1")
    for phrase in (
        "only consume midplatform_decision_center_foundation_v1",
        "must not redefine decision center",
        "must not modify decisioncandidate",
        "must not treat decision_candidate as final action",
        "must not treat blocked/hold as real system state",
        "must not require decision center runtime",
        "new fields require change_control",
    ):
        ok(f"dcdep.{phrase[:14]}", phrase in dc_rules)

    ok("handoff.no_direct", handoff.get("direct_mount_executed") is False)
    for item in DOWNSTREAM_HANDOFFS:
        matched = [h for h in handoff.get("handoffs") or [] if h.get("target") == item["target"]]
        ok(f"handoff.{item['target'][:14]}", len(matched) == 1)
        if matched:
            ok(f"handoff.{item['target'][:10]}.payload", bool(matched[0].get("payload")))
            ok(f"handoff.{item['target'][:10]}.mount", matched[0].get("mount_now") is False)

    ok("samples.count6", samples.get("flow_count") >= 6)
    for flow in SAMPLE_FLOWS:
        matched = [f for f in samples.get("flows") or [] if f.get("flow_id") == flow["flow_id"]]
        ok(f"sample.{flow['flow_id'][:14]}", len(matched) == 1)
        if matched:
            ok(f"sample.{flow['flow_id'][:10]}.inputs", len(matched[0].get("inputs") or []) >= 1)
            ok(f"sample.{flow['flow_id'][:10]}.proc", len(matched[0].get("processing") or []) >= 1)
            ok(f"sample.{flow['flow_id'][:10]}.outs", len(matched[0].get("outputs") or []) >= 1)
            ok(f"sample.{flow['flow_id'][:10]}.blocked", len(matched[0].get("blocked_paths") or []) >= 1)

    ok("failure.count16", failures.get("route_count") >= 16)
    for route in FAILURE_ROUTES:
        matched = [r for r in failures.get("routes") or [] if r.get("route_id") == route["route_id"]]
        ok(f"fail.{route['route_id'][:14]}", len(matched) == 1)
        if matched:
            r0 = matched[0]
            ok(f"fail.{route['route_id'][:10]}.detect", bool(r0.get("detection_signal")))
            ok(f"fail.{route['route_id'][:10]}.impact", bool(r0.get("impact")))
            ok(f"fail.{route['route_id'][:10]}.response", bool(r0.get("default_response")))
            ok(f"fail.{route['route_id'][:10]}.hold", bool(r0.get("hold_or_block_candidate")))
            ok(f"fail.{route['route_id'][:10]}.forbid", bool(r0.get("forbidden_shortcut")))

    ok("metrics.count15", metrics.get("metric_count") >= 15)
    ok("metrics.no_runtime", metrics.get("real_health_runtime_enabled") is False)
    for metric in HEALTH_METRICS:
        ok(f"metric.{metric[:14]}", metric in (metrics.get("metrics") or []))

    global_b = boundary.get("global_boundaries") or {}
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:14]}", global_b.get(field) is False)
        ok(f"summary.{field[:14]}", summary.get(field) is False)
    for field in BOUNDARY_TRUE:
        ok(f"summary.true.{field[:14]}", summary.get(field) is True)

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:14]}", claim in (nc.get("non_claims") or []))
        ok(f"summary.nc.{claim[:12]}", claim in (summary.get("non_claims") or []))

    ok("no.recovery.summary", summary.get("recovery_execution_now") is False)
    ok("no.restart.summary", summary.get("module_restart_now") is False)
    ok("no.process.summary", summary.get("process_control_now") is False)
    ok("no.output.summary", summary.get("user_output_allowed_now") is False)
    ok("no.task.summary", summary.get("task_execution_now") is False)
    ok("no.memory.summary", summary.get("memory_write_allowed_now") is False)
    ok("no.world.summary", summary.get("worldmodel_write_allowed_now") is False)

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    all_pass = passed == total and passed >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "min_checks": MIN_CHECKS,
        "checks_run": total,
        "checks_passed": passed,
        "all_pass": all_pass,
        "verifier": "GO" if all_pass else "HOLD",
        "checks": checks,
    }
    out_path = Path(args.output) if args.output else root / "verify_midplatform_health_watchdog_mount_planning_v1.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "verifier_report.json").write_text(
        json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_run": total}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(str(out_path))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
