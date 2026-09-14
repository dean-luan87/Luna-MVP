#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Information Integration Mount Planning v1."""

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
from capabilities.midplatform.midplatform_information_integration_mount_planning_v1 import (
    ALGORITHM_USES,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    FROZEN_INTERFACE_CONSUMED,
    HEALTH_METRICS,
    INPUT_REQUIRED_FIELDS,
    INPUT_TYPES,
    INTEGRATION_STATES,
    MODEL_USES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_CANDIDATES,
    PHASE_ID,
    PROCESSING_STEPS,
    RULE_USES,
    SAMPLE_FLOWS,
    SCOPE,
    UPSTREAM_FREEZE_DRYRUN_FILES,
    UPSTREAM_FREEZE_DRYRUN_FINAL,
    UPSTREAM_FREEZE_PLANNING_FILES,
)
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FREEZE_DRYRUN_FINAL,
)

MIN_CHECKS = 360

REQUIRED = (
    "summary.json",
    "information_integration_mount_scope_v1.json",
    "information_integration_mount_contract_v1.json",
    "information_integration_input_contract_v1.json",
    "information_integration_output_contract_v1.json",
    "information_integration_processing_model_v1.json",
    "information_integration_model_rule_algorithm_placement_v1.json",
    "information_integration_governance_boundary_v1.json",
    "information_integration_health_boundary_v1.json",
    "information_integration_worldmodel_memory_feedback_boundary_v1.json",
    "information_integration_downstream_handoff_matrix_v1.json",
    "information_integration_sample_flow_plan_v1.json",
    "information_integration_failure_route_matrix_v1.json",
    "information_integration_mount_health_metric_scope_v1.json",
    "information_integration_boundary_matrix_v1.json",
    "information_integration_mount_non_claims_v1.json",
    "information_integration_mount_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_mount_planning"),
    )
    p.add_argument(
        "--freeze-dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"),
    )
    p.add_argument(
        "--freeze-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_planning"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    freeze_dr = Path(args.freeze_dryrun_root)
    freeze_plan = Path(args.freeze_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:30]}", (root / fname).is_file())

    freeze_vr = _load(freeze_dr / "verifier_report.json")
    freeze_sm = _load(freeze_dr / "summary.json")
    ok("upstream.freeze_go", freeze_vr.get("verifier") == "GO")
    ok("upstream.freeze_final", freeze_sm.get("final_decision") == FREEZE_DRYRUN_FINAL)
    ok("upstream.match", UPSTREAM_FREEZE_DRYRUN_FINAL == FREEZE_DRYRUN_FINAL)

    for fname in UPSTREAM_FREEZE_DRYRUN_FILES:
        ok(f"freeze_dr.{fname[:22]}", (freeze_dr / fname).is_file())
    for fname in UPSTREAM_FREEZE_PLANNING_FILES:
        ok(f"freeze_plan.{fname[:22]}", (freeze_plan / fname).is_file())

    version_tag = _load(freeze_plan / "micro_os_foundation_version_tag_v1.json")
    route_dec = _load(freeze_plan / "micro_os_foundation_route_decision_v1.json")
    ok("upstream.foundation_id", version_tag.get("foundation_id") == "midplatform_micro_os_foundation_v1")
    ok("upstream.runtime_status", version_tag.get("runtime_status") == "not_enabled")
    ok(
        "upstream.primary_route",
        route_dec.get("primary_next_phase") == "Phase-Midplatform-Information-Integration-Mount-Planning-v1-001",
    )

    summary = _load(root / "summary.json")
    scope = _load(root / "information_integration_mount_scope_v1.json")
    contract = _load(root / "information_integration_mount_contract_v1.json")
    inp = _load(root / "information_integration_input_contract_v1.json")
    out = _load(root / "information_integration_output_contract_v1.json")
    proc = _load(root / "information_integration_processing_model_v1.json")
    mra = _load(root / "information_integration_model_rule_algorithm_placement_v1.json")
    gov = _load(root / "information_integration_governance_boundary_v1.json")
    health = _load(root / "information_integration_health_boundary_v1.json")
    wm_mem = _load(root / "information_integration_worldmodel_memory_feedback_boundary_v1.json")
    handoff = _load(root / "information_integration_downstream_handoff_matrix_v1.json")
    samples = _load(root / "information_integration_sample_flow_plan_v1.json")
    failures = _load(root / "information_integration_failure_route_matrix_v1.json")
    metrics = _load(root / "information_integration_mount_health_metric_scope_v1.json")
    boundary = _load(root / "information_integration_boundary_matrix_v1.json")
    nc = _load(root / "information_integration_mount_non_claims_v1.json")
    readiness = _load(root / "information_integration_mount_readiness_decision_v1.json")

    ok("phase.id", summary.get("phase") == PHASE_ID)
    ok("scope.id", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.violations0", len(summary.get("violations") or []) == 0)
    ok("readiness.pass", readiness.get("planning_pass") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("readiness.foundation", readiness.get("foundation_consumed") is True)

    ok("scope.layer", scope.get("layer") == "L6")
    ok("scope.module", scope.get("module_id") == "information_integration")
    ok("scope.planning_only", scope.get("mount_planning_only") is True)
    ok("scope.no_direct_mount", scope.get("direct_mount_executed") is False)
    ok("scope.foundation_id", scope.get("foundation_id") == "midplatform_micro_os_foundation_v1")

    for item in FROZEN_INTERFACE_CONSUMED:
        ok(f"scope.frozen.{item[:14]}", item in (scope.get("frozen_interface_consumed") or []))
        ok(f"contract.frozen.{item[:14]}", item in (contract.get("input_contract", {}).get("frozen_interface_refs") or []))

    for section in TEMPLATE_SECTIONS:
        ok(f"contract.section.{section[:12]}", section in contract)

    ok("contract.layer", contract.get("module_identity", {}).get("layer") == "L6")
    ok("contract.candidate_only", contract.get("output_contract", {}).get("all_candidate") is True)
    ok("contract.no_write", contract.get("output_contract", {}).get("write_allowed") is False)
    ok("contract.no_user_out", contract.get("output_contract", {}).get("user_output_allowed") is False)
    ok("contract.planning_only", contract.get("processing_scope", {}).get("planning_only") is True)
    ok("contract.no_runtime", contract.get("processing_scope", {}).get("runtime_execution") is False)

    for inp_type in INPUT_TYPES:
        ok(f"inp.type.{inp_type[:14]}", inp_type in (inp.get("input_types") or []))
        ok(f"contract.inp.{inp_type[:14]}", inp_type in (contract.get("input_contract", {}).get("input_types") or []))

    for field in INPUT_REQUIRED_FIELDS:
        ok(f"inp.req.{field[:12]}", field in (inp.get("required_fields") or []))

    for core in ("Event", "WorkingMemoryEntry", "SchedulingDecisionCandidate"):
        ok(f"inp.core.{core[:12]}", core in (inp.get("core_inputs") or []))

    for out_type in OUTPUT_CANDIDATES:
        ok(f"out.type.{out_type[:14]}", out_type in (out.get("outputs") or []))
        ok(f"contract.out.{out_type[:14]}", out_type in (contract.get("output_contract", {}).get("output_types") or []))

    ok("out.all_candidate", out.get("all_candidate") is True)
    for forbidden in ("fact", "runtime_action", "user_output", "memory_write", "worldmodel_write"):
        ok(f"out.forbidden.{forbidden[:10]}", forbidden in (out.get("forbidden_outputs") or []))

    for step in PROCESSING_STEPS:
        ok(f"proc.step.{step[:14]}", step in (proc.get("steps") or []))
        ok(f"contract.proc.{step[:14]}", step in (contract.get("processing_scope", {}).get("steps") or []))

    for state in INTEGRATION_STATES:
        ok(f"proc.state.{state[:12]}", state in (proc.get("state_machine_states") or []))

    ok("proc.planning_only", proc.get("planning_only") is True)

    for use in MODEL_USES:
        ok(f"mra.model.{use[:14]}", use in (mra.get("model_uses") or []))
    for use in RULE_USES:
        ok(f"mra.rule.{use[:14]}", use in (mra.get("rule_uses") or []))
    for use in ALGORITHM_USES:
        ok(f"mra.algo.{use[:14]}", use in (mra.get("algorithm_uses") or []))
    for state in INTEGRATION_STATES:
        ok(f"mra.sm.{state[:12]}", state in (mra.get("state_machine_uses") or []))

    ok("mra.no_model_now", mra.get("no_model_in_mount_planning_now") is True)
    ok("mra.no_runtime_now", mra.get("no_runtime_now") is True)

    gov_rules = gov.get("rules") or []
    ok("gov.count", len(gov_rules) >= 10)
    for i, rule in enumerate(gov_rules):
        ok(f"gov.rule.{i}", bool(rule))

    health_rules = health.get("rules") or []
    ok("health.count", len(health_rules) >= 7)
    for i, rule in enumerate(health_rules):
        ok(f"health.rule.{i}", bool(rule))

    wm_rules = wm_mem.get("rules") or []
    ok("wm_mem.count", len(wm_rules) >= 7)
    for i, rule in enumerate(wm_rules):
        ok(f"wm_mem.rule.{i}", bool(rule))

    handoffs = handoff.get("handoffs") or []
    ok("handoff.count", len(handoffs) >= 8)
    ok("handoff.no_direct", handoff.get("direct_mount_executed") is False)
    for i, h in enumerate(handoffs):
        ok(f"handoff.{i}.target", bool(h.get("target")))
        ok(f"handoff.{i}.payload", bool(h.get("payload")))
        ok(f"handoff.{i}.no_mount", h.get("mount_now") is False)

    flows = samples.get("flows") or []
    ok("samples.count", len(flows) >= 5)
    ok("samples.match", samples.get("flow_count") == len(SAMPLE_FLOWS))
    for flow in SAMPLE_FLOWS:
        fid = flow["flow_id"]
        matched = [f for f in flows if f.get("flow_id") == fid]
        ok(f"sample.{fid[:14]}", len(matched) == 1)
        if matched:
            f0 = matched[0]
            ok(f"sample.{fid[:10]}.inputs", len(f0.get("inputs") or []) >= 1)
            ok(f"sample.{fid[:10]}.outputs", len(f0.get("outputs") or []) >= 1)
            ok(f"sample.{fid[:10]}.blocked", len(f0.get("blocked_paths") or []) >= 1)

    routes = failures.get("routes") or []
    ok("failures.count", len(routes) >= 12)
    ok("failures.match", failures.get("route_count") == len(FAILURE_ROUTES))
    for route in FAILURE_ROUTES:
        rid = route["route_id"]
        matched = [r for r in routes if r.get("route_id") == rid]
        ok(f"fail.{rid[:14]}", len(matched) == 1)
        if matched:
            r0 = matched[0]
            ok(f"fail.{rid[:10]}.detect", bool(r0.get("detection_signal")))
            ok(f"fail.{rid[:10]}.response", bool(r0.get("default_response")))
            ok(f"fail.{rid[:10]}.recovery", bool(r0.get("recovery_or_hold_candidate")))
            ok(f"fail.{rid[:10]}.forbidden", bool(r0.get("forbidden_shortcut")))

    metric_list = metrics.get("metrics") or []
    ok("metrics.count", len(metric_list) >= 13)
    ok("metrics.match", metrics.get("metric_count") == len(HEALTH_METRICS))
    ok("metrics.no_runtime", metrics.get("real_health_runtime_enabled") is False)
    for m in HEALTH_METRICS:
        ok(f"metric.{m[:14]}", m in metric_list)

    for field in BOUNDARY_FALSE:
        ok(f"summary.bound.{field[:14]}", summary.get(field) is False)
        ok(f"boundary.{field[:14]}", boundary.get("global_boundaries", {}).get(field) is False)
        ok(f"contract.bound.{field[:14]}", contract.get("runtime_boundaries", {}).get(field) is False)

    for field in BOUNDARY_TRUE:
        ok(f"summary.true.{field[:14]}", summary.get(field) is True)

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (nc.get("non_claims") or []))
        ok(f"summary.nc.{claim[:10]}", claim in (summary.get("non_claims") or []))

    ok("summary.module", summary.get("module_id") == "information_integration")
    ok("summary.layer", summary.get("layer") == "L6")
    ok("reuse.rule", summary.get("phase_governance_standard_reuse_rule") is True)
    ok("reuse.no_new_gov", summary.get("new_governance_need_proven") is False)

    for i, principle in enumerate(contract.get("module_principles") or []):
        ok(f"principle.{i}", bool(principle))

    ok("contract.failure_count", contract.get("failure_and_traceability", {}).get("failure_route_count") >= 12)
    ok("contract.trace", contract.get("failure_and_traceability", {}).get("trace_required") is True)
    ok("contract.audit", contract.get("failure_and_traceability", {}).get("audit_required") is True)

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
    out_path = Path(args.output) if args.output else (
        root / "verify_midplatform_information_integration_mount_planning_v1.json"
    )
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
