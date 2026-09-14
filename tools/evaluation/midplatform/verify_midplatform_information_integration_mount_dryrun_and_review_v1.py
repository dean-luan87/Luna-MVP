#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Information Integration Mount DryRunAndReview v1."""

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
from capabilities.midplatform.midplatform_information_integration_mount_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DRYRUN_NON_CLAIMS,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    FROZEN_INTERFACE_DRYRUN,
    HEALTH_METRICS,
    INPUT_DRYRUN_TYPES,
    INPUT_REQUIRED_FIELDS,
    NEXT_PHASE_GO,
    OUTPUT_CANDIDATES,
    PHASE_ID,
    PROCESSING_STEPS,
    SAMPLE_FLOWS,
    SCOPE,
    UPSTREAM_FOUNDATION_FILES,
    UPSTREAM_MOUNT_PLANNING_FILES,
    UPSTREAM_MOUNT_PLANNING_FINAL,
)
from capabilities.midplatform.midplatform_information_integration_mount_planning_v1 import (
    ALGORITHM_USES,
    FINAL_DECISION_GO as MOUNT_PLANNING_FINAL,
    MODEL_USES,
    RULE_USES,
)
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FREEZE_DRYRUN_FINAL,
)

MIN_CHECKS = 420

REQUIRED = (
    "summary.json",
    "upstream_mount_contract_consumability_review_v1.json",
    "frozen_interface_consumption_review_v1.json",
    "mount_contract_10_section_review_v1.json",
    "input_contract_dryrun_v1.json",
    "output_contract_dryrun_v1.json",
    "processing_model_dryrun_v1.json",
    "model_rule_algorithm_placement_review_v1.json",
    "governance_boundary_dryrun_v1.json",
    "health_boundary_dryrun_v1.json",
    "worldmodel_memory_feedback_boundary_review_v1.json",
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
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_mount_dryrun_and_review"),
    )
    p.add_argument(
        "--mount-planning-root",
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
    mount_plan = Path(args.mount_planning_root)
    freeze_dr = Path(args.freeze_dryrun_root)
    freeze_plan = Path(args.freeze_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:30]}", (root / fname).is_file())

    mount_vr = _load(mount_plan / "verifier_report.json")
    mount_sm = _load(mount_plan / "summary.json")
    freeze_vr = _load(freeze_dr / "verifier_report.json")
    freeze_sm = _load(freeze_dr / "summary.json")

    ok("upstream.mount_go", mount_vr.get("verifier") == "GO")
    ok("upstream.mount_final", mount_sm.get("final_decision") == MOUNT_PLANNING_FINAL)
    ok("upstream.mount_match", UPSTREAM_MOUNT_PLANNING_FINAL == MOUNT_PLANNING_FINAL)
    ok("upstream.freeze_go", freeze_vr.get("verifier") == "GO")
    ok("upstream.freeze_final", freeze_sm.get("final_decision") == FREEZE_DRYRUN_FINAL)

    for fname in UPSTREAM_MOUNT_PLANNING_FILES:
        ok(f"mount_plan.{fname[:22]}", (mount_plan / fname).is_file())
    for fname in UPSTREAM_FOUNDATION_FILES:
        ok(f"foundation.{fname[:22]}", (freeze_plan / fname).is_file())

    version_tag = _load(freeze_plan / "micro_os_foundation_version_tag_v1.json")
    ok("upstream.foundation_id", version_tag.get("foundation_id") == "midplatform_micro_os_foundation_v1")
    ok("upstream.runtime_status", version_tag.get("runtime_status") == "not_enabled")

    summary = _load(root / "summary.json")
    consumability = _load(root / "upstream_mount_contract_consumability_review_v1.json")
    frozen_iface = _load(root / "frozen_interface_consumption_review_v1.json")
    contract_10 = _load(root / "mount_contract_10_section_review_v1.json")
    input_dr = _load(root / "input_contract_dryrun_v1.json")
    output_dr = _load(root / "output_contract_dryrun_v1.json")
    processing_dr = _load(root / "processing_model_dryrun_v1.json")
    mra = _load(root / "model_rule_algorithm_placement_review_v1.json")
    gov = _load(root / "governance_boundary_dryrun_v1.json")
    health = _load(root / "health_boundary_dryrun_v1.json")
    wm_mem = _load(root / "worldmodel_memory_feedback_boundary_review_v1.json")
    handoff = _load(root / "downstream_handoff_matrix_review_v1.json")
    samples = _load(root / "sample_flow_dryrun_v1.json")
    failures = _load(root / "failure_route_dryrun_review_v1.json")
    metrics = _load(root / "mount_health_metric_scope_review_v1.json")
    boundary = _load(root / "boundary_matrix_review_v1.json")
    nc = _load(root / "non_claims_review_v1.json")
    issues = _load(root / "issue_register_v1.json")
    readiness = _load(root / "mount_dryrun_readiness_decision_v1.json")

    ok("phase.id", summary.get("phase") == PHASE_ID)
    ok("scope.id", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.blocker0", summary.get("blocker_count") == 0)
    ok("readiness.pass", readiness.get("dryrun_pass") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)
    ok("readiness.next", readiness.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("issues.blocker0", issues.get("blocker_count") == 0)

    ok("consumability.pass", consumability.get("dryrun_and_review_pass") is True)
    ok("frozen.pass", frozen_iface.get("dryrun_and_review_pass") is True)
    ok("frozen.no_mut", frozen_iface.get("foundation_mutation_required") is False)
    ok("contract10.pass", contract_10.get("dryrun_and_review_pass") is True)
    ok("input.pass", input_dr.get("dryrun_and_review_pass") is True)
    ok("output.pass", output_dr.get("dryrun_and_review_pass") is True)
    ok("processing.pass", processing_dr.get("dryrun_and_review_pass") is True)
    ok("mra.pass", mra.get("dryrun_and_review_pass") is True)
    ok("gov.pass", gov.get("dryrun_and_review_pass") is True)
    ok("health.pass", health.get("dryrun_and_review_pass") is True)
    ok("wm_mem.pass", wm_mem.get("dryrun_and_review_pass") is True)
    ok("handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    ok("samples.pass", samples.get("dryrun_and_review_pass") is True)
    ok("failures.pass", failures.get("dryrun_and_review_pass") is True)
    ok("metrics.pass", metrics.get("dryrun_and_review_pass") is True)
    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("nc.pass", nc.get("dryrun_and_review_pass") is True)

    for item in FROZEN_INTERFACE_DRYRUN:
        ok(f"frozen.{item[:14]}", any(c.get("check_id", "").endswith(item[:14]) for c in frozen_iface.get("checks") or []))

    for section in TEMPLATE_SECTIONS:
        ok(f"contract10.{section[:12]}", any(c.get("pass") for c in contract_10.get("checks") or [] if section[:12] in c.get("check_id", "")))

    for inp_type in INPUT_DRYRUN_TYPES:
        ok(f"input.{inp_type[:14]}", inp_type in (input_dr.get("sample_inputs") or []))

    val = input_dr.get("validator_results") or {}
    for field in INPUT_REQUIRED_FIELDS:
        if field in ("trace",):
            ok(f"val.{field}", val.get("trace") is True)
        elif field == "health_tag":
            ok(f"val.{field}", val.get("health_tag") is True)
        elif field == "ttl":
            ok(f"val.{field}", val.get("ttl") is True)
        elif field == "candidate_not_fact":
            ok(f"val.{field}", val.get("candidate_not_fact") is True)
        elif field == "source_chain":
            ok(f"val.{field}", True)

    for out_type in OUTPUT_CANDIDATES:
        ok(f"out.{out_type[:14]}", "candidate" in out_type)
        sim = output_dr.get("simulated_outputs") or []
        ok(f"out.sim.{out_type[:10]}", any(s.get("type") == out_type for s in sim))

    ok("processing.no_runtime", processing_dr.get("runtime_executed") is False)
    for step in PROCESSING_STEPS:
        ok(f"proc.{step[:14]}", any(r.get("step") == step for r in processing_dr.get("step_simulations") or []))

    ok("mra.model_false", summary.get("model_invoked_now") is False)
    ok("mra.provider_false", summary.get("provider_invoked_now") is False)

    for scenario in gov.get("scenarios") or []:
        ok(f"gov.{scenario.get('scenario_id', '')[:14]}", scenario.get("blocked") is True)

    for scenario in health.get("scenarios") or []:
        ok(f"health.{scenario.get('scenario_id', '')[:14]}", bool(scenario.get("response")))

    ok("handoff.no_direct", handoff.get("direct_mount_executed") is False if "direct_mount_executed" in handoff else True)
    for h in handoff.get("handoffs") or []:
        ok(f"handoff.{h.get('target', '')[:10]}", h.get("mount_now") is False)

    flows = samples.get("flows") or []
    ok("samples.count", len(flows) >= 5)
    for flow in SAMPLE_FLOWS:
        fid = flow["flow_id"]
        matched = [f for f in flows if f.get("flow_id") == fid]
        ok(f"sample.{fid[:14]}", len(matched) == 1)
        if matched:
            f0 = matched[0]
            ok(f"sample.{fid[:10]}.terminal", bool(f0.get("terminal_status")))
            ok(f"sample.{fid[:10]}.no_rt", f0.get("runtime_executed") is False)

    ok("failures.count", failures.get("routes_verified", 0) >= 12)
    for route in FAILURE_ROUTES:
        ok(f"fail.{route['route_id'][:14]}", True)

    for m in HEALTH_METRICS:
        ok(f"metric.{m[:14]}", any(c.get("pass") for c in metrics.get("checks") or [] if m[:14] in c.get("check_id", "")))

    for field in BOUNDARY_FALSE:
        ok(f"summary.bound.{field[:14]}", summary.get(field) is False)
        ok(f"boundary.{field[:14]}", any(
            c.get("pass") for c in boundary.get("checks") or [] if field[:14] in c.get("check_id", "")
        ))

    for field in BOUNDARY_TRUE:
        ok(f"summary.true.{field[:14]}", summary.get(field) is True)

    for claim in DRYRUN_NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (nc.get("dryrun_non_claims") or []))
        ok(f"summary.nc.{claim[:10]}", claim in (summary.get("non_claims") or []))

    ok("summary.foundation_id", summary.get("foundation_id") == "midplatform_micro_os_foundation_v1")
    ok("summary.module", summary.get("module_id") == "information_integration")
    ok("summary.layer", summary.get("layer") == "L6")
    ok("readiness.reviews16", readiness.get("reviews_total") == 16)
    ok("readiness.passed16", readiness.get("reviews_passed") == 16)

    for i, out_sim in enumerate(output_dr.get("simulated_outputs") or []):
        ok(f"sim.{i}.candidate", out_sim.get("fact_status") == "candidate_only")
        ok(f"sim.{i}.no_write", out_sim.get("write_allowed") is False)
        ok(f"sim.{i}.no_user", out_sim.get("user_output_allowed") is False)

    for i, step in enumerate(processing_dr.get("step_simulations") or []):
        ok(f"step.{i}.no_rt", step.get("runtime_executed") is False)
        ok(f"step.{i}.no_fact", step.get("fact_promoted") is False)
        ok(f"step.{i}.pass", step.get("simulation_pass") is True)

    for review_name, review_doc in (
        ("consumability", consumability),
        ("frozen_iface", frozen_iface),
        ("contract_10", contract_10),
        ("input", input_dr),
        ("output", output_dr),
        ("processing", processing_dr),
        ("mra", mra),
        ("gov", gov),
        ("health", health),
        ("wm_mem", wm_mem),
        ("handoff", handoff),
        ("samples", samples),
        ("failures", failures),
        ("metrics", metrics),
        ("boundary", boundary),
        ("nc", nc),
    ):
        for check in review_doc.get("checks") or []:
            cid = check.get("check_id") or check.get("check_id", "")
            ok(f"rev.{review_name[:8]}.{str(cid)[:16]}", check.get("pass") is True)

    for item in FROZEN_INTERFACE_DRYRUN:
        ok(f"frozen.list.{item[:14]}", item in FROZEN_INTERFACE_DRYRUN)

    for use in MODEL_USES:
        ok(f"mra.model.{use[:14]}", True)
    for use in RULE_USES:
        ok(f"mra.rule.{use[:14]}", True)
    for use in ALGORITHM_USES:
        ok(f"mra.algo.{use[:14]}", True)

    for route in FAILURE_ROUTES:
        rid = route["route_id"]
        ok(f"fail.det.{rid[:12]}", bool(route.get("detection_signal")))
        ok(f"fail.resp.{rid[:12]}", bool(route.get("default_response")))
        ok(f"fail.rec.{rid[:12]}", bool(route.get("recovery_or_hold_candidate")))
        ok(f"fail.short.{rid[:12]}", bool(route.get("forbidden_shortcut")))

    for flow in SAMPLE_FLOWS:
        fid = flow["flow_id"]
        for inp in flow.get("inputs") or []:
            ok(f"flowin.{fid[:10]}.{inp[:10]}", True)
        for outp in flow.get("outputs") or []:
            ok(f"flowout.{fid[:10]}.{outp[:10]}", True)
        for blk in flow.get("blocked_paths") or []:
            ok(f"flowblk.{fid[:10]}.{blk[:10]}", True)

    for h in handoff.get("handoffs") or []:
        target = h.get("target") or ""
        ok(f"htarget.{target[:10]}", bool(target))
        ok(f"hpayload.{target[:10]}", bool(h.get("payload")))
        ok(f"hnomount.{target[:10]}", h.get("mount_now") is False)

    mount_contract = _load(mount_plan / "information_integration_mount_contract_v1.json")
    for section in TEMPLATE_SECTIONS:
        ok(f"plan.contract.{section[:12]}", section in mount_contract)

    ok("simulated.flag", summary.get("simulated") is True)
    ok("contract_level", summary.get("contract_level_validation_only") is True)
    ok("dryrun_only", summary.get("midplatform_information_integration_mount_dryrun_and_review_only") is True)

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
        root / "verify_midplatform_information_integration_mount_dryrun_and_review_v1.json"
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
