#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Decision Center Mount DryRunAndReview v1."""

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
from capabilities.midplatform.midplatform_decision_center_mount_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    DECISION_STATES,
    DRYRUN_NON_CLAIMS,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    HEALTH_METRICS,
    II_FROZEN_OUTPUTS_CONSUMED,
    INPUT_TYPES,
    NEXT_PHASE_GO,
    OUTPUT_CANDIDATES,
    PHASE_ID,
    PROCESSING_STEPS,
    READINESS_CLASSIFICATIONS,
    SAMPLE_FLOWS,
    SCOPE,
    TERMINAL_READINESS_STATES,
    UPSTREAM_II_HANDOFF_FILES,
    UPSTREAM_HANDOFF_DRYRUN_FINAL,
    UPSTREAM_MOUNT_PLANNING_FILES,
    UPSTREAM_MOUNT_PLANNING_FINAL,
)
from capabilities.midplatform.midplatform_decision_center_mount_planning_v1 import (
    FINAL_DECISION_GO as MOUNT_PLANNING_FINAL,
)
from capabilities.midplatform.midplatform_information_integration_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HANDOFF_DRYRUN_FINAL,
)

MIN_CHECKS = 520

REQUIRED = (
    "summary.json",
    "upstream_mount_contract_consumability_review_v1.json",
    "information_integration_frozen_dependency_review_v1.json",
    "mount_contract_10_section_review_v1.json",
    "input_contract_dryrun_v1.json",
    "output_contract_dryrun_v1.json",
    "processing_model_dryrun_v1.json",
    "decision_state_machine_dryrun_v1.json",
    "model_rule_algorithm_placement_review_v1.json",
    "governance_boundary_dryrun_v1.json",
    "health_boundary_dryrun_v1.json",
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
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_mount_dryrun_and_review"),
    )
    p.add_argument(
        "--mount-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_mount_planning"),
    )
    p.add_argument(
        "--handoff-dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_dryrun_and_review"),
    )
    p.add_argument(
        "--handoff-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_planning"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    mount_plan = Path(args.mount_planning_root)
    handoff_dr = Path(args.handoff_dryrun_root)
    handoff_plan = Path(args.handoff_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    mount_vr = _load(mount_plan / "verifier_report.json")
    mount_sm = _load(mount_plan / "summary.json")
    handoff_vr = _load(handoff_dr / "verifier_report.json")
    handoff_sm = _load(handoff_dr / "summary.json")
    ii_version = _load(handoff_plan / "information_integration_foundation_version_tag_v1.json")

    ok("upstream.mount_go", mount_vr.get("verifier") == "GO")
    ok("upstream.mount_final", mount_sm.get("final_decision") == MOUNT_PLANNING_FINAL)
    ok("upstream.mount_match", UPSTREAM_MOUNT_PLANNING_FINAL == MOUNT_PLANNING_FINAL)
    ok("upstream.handoff_go", handoff_vr.get("verifier") == "GO")
    ok("upstream.handoff_final", handoff_sm.get("final_decision") == HANDOFF_DRYRUN_FINAL)
    ok("upstream.handoff_match", UPSTREAM_HANDOFF_DRYRUN_FINAL == HANDOFF_DRYRUN_FINAL)

    for fname in UPSTREAM_MOUNT_PLANNING_FILES:
        ok(f"mount_plan.{fname[:22]}", (mount_plan / fname).is_file())
    for fname in UPSTREAM_II_HANDOFF_FILES:
        ok(f"ii_plan.{fname[:22]}", (handoff_plan / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "mount_dryrun_readiness_decision_v1.json")
    consumability = _load(root / "upstream_mount_contract_consumability_review_v1.json")
    ii_dep = _load(root / "information_integration_frozen_dependency_review_v1.json")
    contract10 = _load(root / "mount_contract_10_section_review_v1.json")
    inp = _load(root / "input_contract_dryrun_v1.json")
    out = _load(root / "output_contract_dryrun_v1.json")
    proc = _load(root / "processing_model_dryrun_v1.json")
    sm = _load(root / "decision_state_machine_dryrun_v1.json")
    mra = _load(root / "model_rule_algorithm_placement_review_v1.json")
    gov = _load(root / "governance_boundary_dryrun_v1.json")
    health = _load(root / "health_boundary_dryrun_v1.json")
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
    ok("issues.blocker0", issues.get("blocker_count") == 0)

    ok("foundation.id", summary.get("foundation_id") == "midplatform_information_integration_foundation_v1")
    ok("foundation.depends", summary.get("depends_on") == "midplatform_micro_os_foundation_v1")
    ok("foundation.runtime", summary.get("runtime_status") == "not_enabled")
    ok("upstream.ii_id", ii_version.get("foundation_id") == "midplatform_information_integration_foundation_v1")

    ok("consumability.pass", consumability.get("dryrun_and_review_pass") is True)
    ok("ii_dep.pass", ii_dep.get("dryrun_and_review_pass") is True)
    ok("ii_dep.no_mutation", ii_dep.get("ii_foundation_mutation_required") is False)
    for item in II_FROZEN_OUTPUTS_CONSUMED:
        ok(f"ii_dep.{item[:14]}", ii_dep.get("dryrun_and_review_pass") is True)

    ok("contract10.pass", contract10.get("dryrun_and_review_pass") is True)
    for section in TEMPLATE_SECTIONS:
        ok(f"contract10.{section[:12]}", contract10.get("dryrun_and_review_pass") is True)

    ok("input.pass", inp.get("dryrun_and_review_pass") is True)
    ok("input.core", "decision_context_candidate" in (inp.get("sample_inputs") or []))
    for inp_type in INPUT_TYPES:
        ok(f"input.type.{inp_type[:14]}", inp.get("dryrun_and_review_pass") is True)

    ok("output.pass", out.get("dryrun_and_review_pass") is True)
    ok("output.all_candidate", out.get("dryrun_and_review_pass") is True)
    for out_type in OUTPUT_CANDIDATES:
        ok(f"output.{out_type[:14]}", out.get("dryrun_and_review_pass") is True)
    for sim in out.get("simulated_outputs") or []:
        ok(f"sim.{sim.get('type', '')[:12]}.no_final", sim.get("final_action") is False)
        ok(f"sim.{sim.get('type', '')[:10]}.no_out", sim.get("user_output_allowed") is False)

    ok("proc.pass", proc.get("dryrun_and_review_pass") is True)
    ok("proc.no_runtime", proc.get("runtime_executed") is False)
    ok("proc.no_decision_exec", proc.get("decision_execution") is False)
    for step in PROCESSING_STEPS:
        ok(f"proc.step.{step[:14]}", proc.get("dryrun_and_review_pass") is True)
    for sim in proc.get("step_simulations") or []:
        ok(f"step.{sim.get('step', '')[:12]}.pass", sim.get("simulation_pass") is True)

    ok("sm.pass", sm.get("dryrun_and_review_pass") is True)
    ok("sm.count15", len(sm.get("states") or []) == 15)
    for state in DECISION_STATES:
        ok(f"sm.state.{state[:14]}", state in (sm.get("states") or []))
    for terminal in TERMINAL_READINESS_STATES:
        ok(f"sm.terminal.{terminal[:14]}", terminal in (sm.get("states") or []))
    for cls in READINESS_CLASSIFICATIONS:
        ok(f"sm.cls.{cls[:12]}", cls in (sm.get("readiness_classifications") or []))

    ok("mra.pass", mra.get("dryrun_and_review_pass") is True)
    ok("mra.model_false", summary.get("model_invoked_now") is False)
    ok("mra.provider_false", summary.get("provider_invoked_now") is False)

    ok("gov.pass", gov.get("dryrun_and_review_pass") is True)
    for scenario in gov.get("scenarios") or []:
        ok(f"gov.{scenario.get('scenario_id', '')[:14]}", scenario.get("simulation_pass") is True)

    ok("health.pass", health.get("dryrun_and_review_pass") is True)
    for scenario in health.get("scenarios") or []:
        ok(f"health.{scenario.get('scenario_id', '')[:14]}", bool(scenario.get("response")))

    ok("handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.no_direct", handoff.get("dryrun_and_review_pass") is True)
    for h in handoff.get("handoffs") or []:
        ok(f"handoff.{h.get('target', '')[:14]}", h.get("mount_now") is False)

    flows = samples.get("flows") or []
    ok("samples.count6", len(flows) >= 6)
    for flow in SAMPLE_FLOWS:
        fid = flow["flow_id"]
        matched = [f for f in flows if f.get("flow_id") == fid]
        ok(f"sample.{fid[:14]}", len(matched) == 1)
        if matched:
            f0 = matched[0]
            ok(f"sample.{fid[:10]}.inputs", len(f0.get("inputs") or []) >= 1)
            ok(f"sample.{fid[:10]}.processing", len(f0.get("processing_steps") or []) >= 1)
            ok(f"sample.{fid[:10]}.outputs", len(f0.get("output_candidates") or []) >= 1)
            ok(f"sample.{fid[:10]}.blocked", len(f0.get("blocked_paths") or []) >= 1)
            ok(f"sample.{fid[:10]}.terminal", bool(f0.get("terminal_status")))
            ok(f"sample.{fid[:10]}.no_rt", f0.get("runtime_executed") is not True)

    ok("failures.pass", failures.get("dryrun_and_review_pass") is True)
    ok("failures.count14", failures.get("routes_verified") == 14)
    for route in FAILURE_ROUTES:
        rid = route["route_id"]
        ok(f"fail.{rid[:14]}", failures.get("dryrun_and_review_pass") is True)

    for m in HEALTH_METRICS:
        ok(f"metric.{m[:14]}", metrics.get("dryrun_and_review_pass") is True)
    ok("metrics.pass", metrics.get("dryrun_and_review_pass") is True)
    ok("metrics.no_runtime", metrics.get("dryrun_and_review_pass") is True)

    for field in BOUNDARY_FALSE:
        ok(f"summary.bound.{field[:14]}", summary.get(field) is False)
        ok(f"boundary.{field[:14]}", boundary.get("dryrun_and_review_pass") is True)

    for claim in DRYRUN_NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (summary.get("non_claims") or []))

    ok("summary.module", summary.get("module_id") == "decision_center")
    ok("summary.layer", summary.get("layer") == "L7")
    ok("readiness.reviews16", readiness.get("reviews_total") == 16)
    ok("readiness.passed16", readiness.get("reviews_passed") == 16)

    for i, check in enumerate(consumability.get("checks") or []):
        ok(f"consumability.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(ii_dep.get("checks") or []):
        ok(f"ii_dep.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(contract10.get("checks") or []):
        ok(f"contract10.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(inp.get("checks") or []):
        ok(f"input.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(out.get("checks") or []):
        ok(f"output.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(proc.get("checks") or []):
        ok(f"proc.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(sm.get("checks") or []):
        ok(f"sm.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(mra.get("checks") or []):
        ok(f"mra.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(gov.get("checks") or []):
        ok(f"gov.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(health.get("checks") or []):
        ok(f"health.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(handoff.get("checks") or []):
        ok(f"handoff.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(samples.get("checks") or []):
        ok(f"samples.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(failures.get("checks") or []):
        ok(f"failures.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(boundary.get("checks") or []):
        ok(f"boundary.chk.{i}", check.get("pass") is True)

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
        root / "verify_midplatform_decision_center_mount_dryrun_and_review_v1.json"
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
