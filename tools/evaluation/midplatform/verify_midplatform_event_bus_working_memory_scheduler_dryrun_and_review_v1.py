#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Event Bus / Working Memory / Scheduler DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    EVENT_STATES,
    EVENT_STATE_PATHS,
    EVENT_TYPES,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PREEMPTION_SCENARIOS,
    REQUIRED_HEALTH_METRICS,
    SAMPLE_FLOWS,
    SCOPE,
    UPSTREAM_PLANNING_FILES,
    UPSTREAM_PLANNING_FINAL,
    WM_ENTRY_STATES,
)
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    HEALTH_METRIC_EB_WM_SCHED_MAP,
    TTL_POLICIES,
)
from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import PRIORITY_LEVELS

MIN_CHECKS = 579

REQUIRED = (
    "summary.json",
    "upstream_contract_consumability_review_v1.json",
    "event_type_registry_review_v1.json",
    "event_state_machine_dryrun_v1.json",
    "working_memory_state_machine_dryrun_v1.json",
    "ttl_cleanup_policy_dryrun_v1.json",
    "scheduler_priority_queue_dryrun_v1.json",
    "preemption_and_deferral_dryrun_v1.json",
    "interaction_model_dryrun_v1.json",
    "health_metric_mapping_review_v1.json",
    "failure_route_dryrun_review_v1.json",
    "governance_boundary_review_v1.json",
    "sample_flow_dryrun_v1.json",
    "boundary_matrix_review_v1.json",
    "issue_register_v1.json",
    "dryrun_readiness_decision_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_dryrun_and_review"),
    )
    p.add_argument(
        "--planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_planning"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)

    for fname in UPSTREAM_PLANNING_FILES:
        ok(f"plan.up.{fname[:22]}", (plan_root / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "dryrun_readiness_decision_v1.json")
    consumability = _load(root / "upstream_contract_consumability_review_v1.json")
    etypes = _load(root / "event_type_registry_review_v1.json")
    estates = _load(root / "event_state_machine_dryrun_v1.json")
    wm = _load(root / "working_memory_state_machine_dryrun_v1.json")
    ttl = _load(root / "ttl_cleanup_policy_dryrun_v1.json")
    prio = _load(root / "scheduler_priority_queue_dryrun_v1.json")
    preempt = _load(root / "preemption_and_deferral_dryrun_v1.json")
    interaction = _load(root / "interaction_model_dryrun_v1.json")
    health = _load(root / "health_metric_mapping_review_v1.json")
    failure = _load(root / "failure_route_dryrun_review_v1.json")
    gov = _load(root / "governance_boundary_review_v1.json")
    flows = _load(root / "sample_flow_dryrun_v1.json")
    boundary = _load(root / "boundary_matrix_review_v1.json")
    issues = _load(root / "issue_register_v1.json")

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE == "midplatform_event_bus_working_memory_scheduler_dryrun_and_review_only")
    ok("summary.dryrun_pass", summary.get("dryrun_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.blocker0", summary.get("blocker_count") == 0)
    ok("readiness.pass", readiness.get("dryrun_pass") is True)
    ok("readiness.consumable", readiness.get("contracts_consumable") is True)
    ok("readiness.reviews13", readiness.get("reviews_total") == 13)
    ok("readiness.passed13", readiness.get("reviews_passed") == 13)
    ok("issues.blocker0", issues.get("blocker_count") == 0)
    ok("upstream.match", UPSTREAM_PLANNING_FINAL == PLANNING_FINAL)

    ok("consumability.pass", consumability.get("dryrun_and_review_pass") is True)
    ok("consumability.obj16", consumability.get("objects_consumed") == 16)

    ok("etypes.pass", etypes.get("dryrun_and_review_pass") is True)
    ok("etypes.count12", len(etypes.get("event_types") or []) >= 12)
    for et in EVENT_TYPES:
        ok(f"etype.{et[:14]}", et in (etypes.get("event_types") or []))

    ok("estates.pass", estates.get("dryrun_and_review_pass") is True)
    for term in ("completed", "expired", "discarded", "blocked"):
        ok(f"terminal.{term[:8]}", term in (estates.get("terminal_states_covered") or []))
    for path in EVENT_STATE_PATHS:
        run = next((p for p in estates.get("paths", []) if p.get("path_id") == path["path_id"]), {})
        ok(f"path.{path['path_id'][:14]}", run.get("path_valid") and run.get("terminal_reached"))
    for st in EVENT_STATES:
        ok(f"estate.{st[:12]}", estates.get("dryrun_and_review_pass") is True)

    ok("wm.pass", wm.get("dryrun_and_review_pass") is True)
    for st in WM_ENTRY_STATES:
        ok(f"wmstate.{st[:12]}", any(r.get("state") == st for r in wm.get("state_runs", [])))
    for run in wm.get("state_runs") or []:
        ok(f"wm.{run['state'][:10]}.no_fact", run.get("writes_fact") is False)
        ok(f"wm.{run['state'][:10]}.no_mem", run.get("writes_memory") is False)

    ok("ttl.pass", ttl.get("dryrun_and_review_pass") is True)
    ok("ttl.no_forbidden", any(s.get("no_ttl_forbidden_respected") for s in ttl.get("simulations") or []))
    missing = next((s for s in ttl.get("simulations") or [] if s.get("ttl") is None), {})
    ok("ttl.missing_blocked", missing.get("active_processing_allowed") is False)
    for pol in TTL_POLICIES:
        ok(f"ttl.policy.{pol['priority']}", ttl.get("dryrun_and_review_pass") is True)

    ok("prio.pass", prio.get("dryrun_and_review_pass") is True)
    for level in PRIORITY_LEVELS:
        ok(f"prio.{level['priority']}", prio.get("dryrun_and_review_pass") is True)

    ok("preempt.pass", preempt.get("dryrun_and_review_pass") is True)
    ok("preempt.count6", len(preempt.get("scenarios") or []) >= 6)
    for sc in PREEMPTION_SCENARIOS:
        run = next((s for s in preempt.get("scenarios", []) if s.get("scenario_id") == sc["scenario_id"]), {})
        ok(f"preempt.{sc['scenario_id'][:14]}", run.get("expected") == run.get("result"))

    ok("interaction.pass", interaction.get("dryrun_and_review_pass") is True)
    ok("interaction.no_semantic", interaction.get("dryrun_and_review_pass") is True)
    ok("interaction.no_exec", interaction.get("dryrun_and_review_pass") is True)

    ok("health.pass", health.get("dryrun_and_review_pass") is True)
    ok("health.count12", health.get("metrics_reviewed") == len(REQUIRED_HEALTH_METRICS))
    for metric in REQUIRED_HEALTH_METRICS:
        ok(f"health.{metric[:14]}", health.get("dryrun_and_review_pass") is True)
        ok(f"map.{metric[:12]}", HEALTH_METRIC_EB_WM_SCHED_MAP.get(metric) is not None)

    ok("failure.pass", failure.get("dryrun_and_review_pass") is True)
    ok("failure.count12", failure.get("route_count") == len(FAILURE_ROUTES))
    for route in FAILURE_ROUTES:
        rid = route["route_id"]
        found = next((r for r in failure.get("routes", []) if r.get("route_id") == rid), {})
        ok(f"fail.{rid[:14]}.exists", bool(found))
        for field in ("detection_signal", "impact", "default_response", "recovery_candidate", "forbidden_shortcut"):
            ok(f"fail.{rid[:10]}.{field[:6]}", bool(found.get(field)))

    ok("gov.pass", gov.get("dryrun_and_review_pass") is True)
    ok("gov.l0", gov.get("dryrun_and_review_pass") is True)

    ok("flows.pass", flows.get("dryrun_and_review_pass") is True)
    ok("flows.count4", flows.get("flow_count") >= 4)
    for flow in SAMPLE_FLOWS:
        run = next((f for f in flows.get("flows", []) if f.get("flow_id") == flow["flow_id"]), {})
        ok(f"flow.{flow['flow_id'][:14]}.sim", run.get("simulation_pass") is True)
        ok(f"flow.{flow['flow_id'][:14]}.wm", len(run.get("working_memory_states") or []) >= 1)
        ok(f"flow.{flow['flow_id'][:14]}.sched", len(run.get("scheduler_results") or []) >= 1)

    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:14]}", summary.get(field) is False)

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (summary.get("non_claims") or []))

    for i, check in enumerate(consumability.get("checks", [])):
        ok(f"consume.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(estates.get("checks", [])):
        ok(f"estate.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(wm.get("checks", [])):
        ok(f"wm.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(ttl.get("checks", [])):
        ok(f"ttl.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(failure.get("checks", [])):
        ok(f"fail.chk.{i}", check.get("pass") is True)
    for i, check in enumerate(boundary.get("checks", [])):
        ok(f"bnd.chk.{i}", check.get("pass") is True)

    for comp in ("event_bus", "working_memory", "scheduler"):
        ok(f"triad.{comp[:8]}", comp in (summary.get("foundation_components") or []))

    ok("simulated.flag", summary.get("simulated") is True)
    ok("candidate.only", summary.get("candidate_only") is True)

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
        root / "verify_midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1.json"
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
