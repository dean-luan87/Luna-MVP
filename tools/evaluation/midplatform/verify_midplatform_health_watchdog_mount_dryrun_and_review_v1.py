#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Health Watchdog Mount DryRunAndReview v1."""

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
from capabilities.midplatform.midplatform_health_watchdog_mount_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    DECISION_CENTER_OUTPUTS_CONSUMED,
    DRYRUN_NON_CLAIMS,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    GOVERNANCE_SCENARIOS,
    HEALTH_METRICS,
    HEALTH_STATES,
    INPUT_REQUIRED_FIELDS,
    INPUT_TYPES,
    MODEL_USES,
    NEXT_PHASE_GO,
    OUTPUT_CANDIDATES,
    PHASE_ID,
    PROCESSING_STEPS,
    RECOVERY_SCENARIOS,
    RULE_USES,
    SAMPLE_FLOWS,
    SCOPE,
    TERMINAL_HEALTH_STATES,
    UPSTREAM_DECISION_CENTER_HANDOFF_FILES,
    UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FINAL,
    UPSTREAM_DECISION_CENTER_PLANNING_FILES,
    UPSTREAM_MOUNT_PLANNING_FILES,
    UPSTREAM_MOUNT_PLANNING_FINAL,
)
from capabilities.midplatform.midplatform_health_watchdog_mount_planning_v1 import (
    FINAL_DECISION_GO as MOUNT_PLANNING_FINAL,
)

MIN_CHECKS = 520

REQUIRED = (
    "summary.json",
    "upstream_mount_contract_consumability_review_v1.json",
    "decision_center_frozen_dependency_review_v1.json",
    "mount_contract_10_section_review_v1.json",
    "input_contract_dryrun_v1.json",
    "output_contract_dryrun_v1.json",
    "processing_model_dryrun_v1.json",
    "health_state_machine_dryrun_v1.json",
    "model_rule_algorithm_placement_review_v1.json",
    "governance_boundary_dryrun_v1.json",
    "recovery_boundary_dryrun_v1.json",
    "downstream_handoff_matrix_review_v1.json",
    "sample_flow_dryrun_v1.json",
    "failure_route_dryrun_review_v1.json",
    "mount_health_metric_scope_review_v1.json",
    "boundary_matrix_review_v1.json",
    "non_claims_review_v1.json",
    "issue_register_v1.json",
    "mount_dryrun_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_mount_dryrun_and_review"),
    )
    p.add_argument(
        "--mount-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_health_watchdog_mount_planning"),
    )
    p.add_argument(
        "--decision-center-handoff-dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_foundation_handoff_dryrun_and_review"),
    )
    p.add_argument(
        "--decision-center-handoff-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_foundation_handoff_planning"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.mount_planning_root)
    dc_dr = Path(args.decision_center_handoff_dryrun_root)
    dc_plan = Path(args.decision_center_handoff_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:30]}", (root / fname).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")
    dc_vr = _load(dc_dr / "verifier_report.json")
    dc_sm = _load(dc_dr / "summary.json")
    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == MOUNT_PLANNING_FINAL)
    ok("upstream.plan_match", UPSTREAM_MOUNT_PLANNING_FINAL == MOUNT_PLANNING_FINAL)
    ok("upstream.dc_go", dc_vr.get("verifier") == "GO")
    ok("upstream.dc_final", dc_sm.get("final_decision") == DC_HANDOFF_DRYRUN_FINAL)
    ok("upstream.dc_match", UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FINAL == DC_HANDOFF_DRYRUN_FINAL)

    for fname in UPSTREAM_MOUNT_PLANNING_FILES:
        ok(f"plan.up.{fname[:22]}", (plan_root / fname).is_file())
    for fname in UPSTREAM_DECISION_CENTER_HANDOFF_FILES:
        ok(f"dcdr.up.{fname[:22]}", (dc_dr / fname).is_file())
    for fname in UPSTREAM_DECISION_CENTER_PLANNING_FILES:
        ok(f"dcplan.up.{fname[:22]}", (dc_plan / fname).is_file())

    dc_version = _load(dc_plan / "decision_center_foundation_version_tag_v1.json")
    ok("dc.foundation", dc_version.get("foundation_id") == "midplatform_decision_center_foundation_v1")
    ok("dc.runtime", dc_version.get("runtime_status") == "not_enabled")

    summary = _load(root / "summary.json")
    readiness = _load(root / "mount_dryrun_readiness_decision_v1.json")
    consumability = _load(root / "upstream_mount_contract_consumability_review_v1.json")
    dc_dep = _load(root / "decision_center_frozen_dependency_review_v1.json")
    contract = _load(root / "mount_contract_10_section_review_v1.json")
    inp = _load(root / "input_contract_dryrun_v1.json")
    out = _load(root / "output_contract_dryrun_v1.json")
    proc = _load(root / "processing_model_dryrun_v1.json")
    state = _load(root / "health_state_machine_dryrun_v1.json")
    mra = _load(root / "model_rule_algorithm_placement_review_v1.json")
    gov = _load(root / "governance_boundary_dryrun_v1.json")
    recovery = _load(root / "recovery_boundary_dryrun_v1.json")
    handoff = _load(root / "downstream_handoff_matrix_review_v1.json")
    samples = _load(root / "sample_flow_dryrun_v1.json")
    failures = _load(root / "failure_route_dryrun_review_v1.json")
    metrics = _load(root / "mount_health_metric_scope_review_v1.json")
    boundary = _load(root / "boundary_matrix_review_v1.json")
    nc = _load(root / "non_claims_review_v1.json")
    issues = _load(root / "issue_register_v1.json")

    ok("phase.id", summary.get("phase") == PHASE_ID)
    ok("scope.id", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.blocker0", summary.get("blocker_count") == 0)
    ok("readiness.pass", readiness.get("dryrun_pass") is True)
    ok("readiness.reviews16", readiness.get("reviews_total") == 16)
    ok("readiness.passed16", readiness.get("reviews_passed") == 16)
    ok("issues.blocker0", issues.get("blocker_count") == 0)
    ok("foundation.id", summary.get("foundation_id") == "midplatform_decision_center_foundation_v1")
    ok("foundation.runtime", summary.get("runtime_status") == "not_enabled")

    for doc_name, doc in (
        ("consumability", consumability),
        ("dc_dep", dc_dep),
        ("contract", contract),
        ("input", inp),
        ("output", out),
        ("processing", proc),
        ("state", state),
        ("mra", mra),
        ("gov", gov),
        ("recovery", recovery),
        ("handoff", handoff),
        ("samples", samples),
        ("failures", failures),
        ("metrics", metrics),
        ("boundary", boundary),
        ("nonclaims", nc),
    ):
        ok(f"{doc_name}.pass", doc.get("dryrun_and_review_pass") is True)
        for i, check in enumerate(doc.get("checks") or []):
            ok(f"{doc_name}.chk.{i}", check.get("pass") is True)

    ok("consumability.artifacts", len(consumability.get("artifacts_consumed") or []) >= 17)
    ok("dcdep.no_mutation", dc_dep.get("decision_center_redefinition_required") is False)
    for item in DECISION_CENTER_OUTPUTS_CONSUMED:
        ok(f"dcdep.consumes.{item[:14]}", item in (dc_dep.get("consumed_outputs") or []))

    for section in TEMPLATE_SECTIONS:
        ok(f"contract.section.{section[:12]}", any(section[:12] in str(c.get("check_id")) for c in contract.get("checks") or []))

    sample_inputs = inp.get("sample_inputs") or {}
    for inp_type in INPUT_TYPES:
        ok(f"input.type.{inp_type[:14]}", inp_type in sample_inputs or any(inp_type[:14] in str(c.get("check_id")) for c in inp.get("checks") or []))
    for field in INPUT_REQUIRED_FIELDS:
        ok(f"input.req.{field[:14]}", any(field[:14] in str(c.get("check_id")) for c in inp.get("checks") or []))
    ok("input.candidate", sample_inputs.get("candidate_not_fact") is True)
    ok("input.trace", bool(sample_inputs.get("trace_ref")))
    ok("input.health_tag", bool(sample_inputs.get("health_tag")))
    ok("input.source_chain", bool(sample_inputs.get("source_chain")))
    ok("input.governance_ref", bool(sample_inputs.get("governance_ref")))

    simulated_outputs = out.get("simulated_outputs") or []
    for out_type in OUTPUT_CANDIDATES:
        ok(f"output.type.{out_type[:14]}", any(o.get("type") == out_type for o in simulated_outputs))
    for item in simulated_outputs:
        ok(f"output.candidate.{item.get('type', '')[:10]}", item.get("candidate_only") is True)
        ok(f"output.no_recovery.{item.get('type', '')[:8]}", item.get("recovery_execution") is False)
        ok(f"output.no_user.{item.get('type', '')[:8]}", item.get("user_output") is False)
    for forbidden in ("real_recovery_command", "restart_command", "kill_process_command", "runtime_command", "user_output"):
        ok(f"output.forbidden.{forbidden[:10]}", any(forbidden[:12] in str(c.get("check_id")) for c in out.get("checks") or []))

    for run in proc.get("step_simulations") or []:
        ok(f"proc.run.{run.get('step', '')[:12]}", run.get("simulation_pass") is True)
        ok(f"proc.no_rt.{run.get('step', '')[:10]}", run.get("runtime_executed") is False)
        ok(f"proc.no_rec.{run.get('step', '')[:10]}", run.get("recovery_executed") is False)
        ok(f"proc.output.{run.get('step', '')[:10]}", all("candidate" in o for o in run.get("output_candidates") or []))

    for st in HEALTH_STATES:
        ok(f"state.{st[:14]}", st in (state.get("states") or []))
    for terminal in TERMINAL_HEALTH_STATES:
        ok(f"terminal.{terminal[:14]}", terminal in (state.get("terminal_states_covered") or []))

    for use in MODEL_USES:
        ok(f"mra.model.{use[:14]}", any(use[:14] in str(c.get("check_id")) for c in mra.get("checks") or []))
    for use in RULE_USES:
        ok(f"mra.rule.{use[:14]}", any(use[:14] in str(c.get("check_id")) for c in mra.get("checks") or []))

    for scenario in GOVERNANCE_SCENARIOS:
        ok(f"gov.scenario.{scenario[:14]}", any(r.get("scenario_id") == scenario and r.get("blocked") for r in gov.get("scenarios") or []))
    for scenario in RECOVERY_SCENARIOS:
        ok(
            f"recovery.scenario.{scenario[:14]}",
            any(r.get("scenario_id") == scenario and r.get("blocked") and not r.get("real_recovery_executed") for r in recovery.get("scenarios") or []),
        )

    for item in handoff.get("handoffs") or []:
        ok(f"handoff.target.{item.get('target', '')[:12]}", bool(item.get("target")))
        ok(f"handoff.no_mount.{item.get('target', '')[:10]}", item.get("mount_now") is False)
    ok("handoff.count6", len(handoff.get("handoffs") or []) >= 6)

    for flow in SAMPLE_FLOWS:
        matched = [f for f in samples.get("flows") or [] if f.get("flow_id") == flow["flow_id"]]
        ok(f"sample.{flow['flow_id'][:14]}", len(matched) == 1)
        if matched:
            f0 = matched[0]
            ok(f"sample.{flow['flow_id'][:10]}.pass", f0.get("simulation_pass") is True)
            ok(f"sample.{flow['flow_id'][:10]}.no_rt", f0.get("runtime_executed") is False)
            ok(f"sample.{flow['flow_id'][:10]}.no_rec", f0.get("recovery_executed") is False)
            ok(f"sample.{flow['flow_id'][:10]}.terminal", bool(f0.get("terminal_status")))
            ok(f"sample.{flow['flow_id'][:10]}.blocked", len(f0.get("blocked_paths") or []) >= 1)

    ok("failure.count16", failures.get("routes_verified") >= 16)
    for route in FAILURE_ROUTES:
        ok(f"failure.{route['route_id'][:14]}", any(route["route_id"][:14] in str(c.get("check_id")) for c in failures.get("checks") or []))

    for metric in HEALTH_METRICS:
        ok(f"metric.{metric[:14]}", any(metric[:14] in str(c.get("check_id")) for c in metrics.get("checks") or []))
    ok("metrics.no_runtime", any(c.get("check_id") == "no_health_runtime" and c.get("pass") for c in metrics.get("checks") or []))

    for field in BOUNDARY_FALSE:
        ok(f"summary.bound.{field[:14]}", summary.get(field) is False)
        ok(f"boundary.{field[:14]}", any(field[:14] in str(c.get("check_id")) and c.get("pass") for c in boundary.get("checks") or []))

    for claim in DRYRUN_NON_CLAIMS:
        ok(f"nc.{claim[:14]}", claim in (summary.get("non_claims") or []))

    ok("no.recovery.summary", summary.get("recovery_execution_now") is False)
    ok("no.restart.summary", summary.get("module_restart_now") is False)
    ok("no.process.summary", summary.get("process_control_now") is False)
    ok("no.task.summary", summary.get("task_execution_now") is False)
    ok("no.output.summary", summary.get("user_output_allowed_now") is False)
    ok("no.memory.summary", summary.get("memory_write_allowed_now") is False)
    ok("no.world.summary", summary.get("worldmodel_write_allowed_now") is False)
    ok("no.model.summary", summary.get("model_invoked_now") is False)
    ok("no.provider.summary", summary.get("provider_invoked_now") is False)

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
    out_path = Path(args.output) if args.output else root / "verify_midplatform_health_watchdog_mount_dryrun_and_review_v1.json"
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
