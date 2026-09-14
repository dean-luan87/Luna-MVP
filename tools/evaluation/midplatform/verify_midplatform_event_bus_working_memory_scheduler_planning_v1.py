#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform Event Bus / Working Memory / Scheduler Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_planning_v1 import (
    ARCH_UPSTREAM_FILES,
    BOUNDARY_FALSE,
    CORE_UPSTREAM_FILES,
    EVENT_BUS_FIELDS,
    EVENT_STATES,
    EVENT_TYPES,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    HEALTH_METRIC_EB_WM_SCHED_MAP,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SAMPLE_FLOWS,
    SCHEDULER_FIELDS,
    SCOPE,
    SOURCE_CHAIN,
    TTL_POLICIES,
    UPSTREAM_CORE_DRYRUN_FINAL,
    WM_ENTRY_STATES,
    WORKING_MEMORY_FIELDS,
)
from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import PRIORITY_LEVELS
from capabilities.midplatform.midplatform_micro_os_core_component_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CORE_DRYRUN_FINAL,
)

MIN_CHECKS = 469

REQUIRED = (
    "summary.json",
    "event_bus_contract_v1.json",
    "event_type_registry_v1.json",
    "event_state_machine_v1.json",
    "working_memory_contract_v1.json",
    "working_memory_entry_state_machine_v1.json",
    "working_memory_ttl_and_cleanup_policy_v1.json",
    "scheduler_contract_v1.json",
    "priority_queue_policy_v1.json",
    "preemption_and_deferral_policy_v1.json",
    "event_bus_working_memory_scheduler_interaction_model_v1.json",
    "eb_wm_scheduler_health_metric_mapping_v1.json",
    "eb_wm_scheduler_failure_route_matrix_v1.json",
    "eb_wm_scheduler_governance_boundary_v1.json",
    "eb_wm_scheduler_sample_flow_plan_v1.json",
    "eb_wm_scheduler_boundary_matrix_v1.json",
    "eb_wm_scheduler_planning_readiness_decision_v1.json",
    "eb_wm_scheduler_non_claims_register_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_planning"),
    )
    p.add_argument(
        "--architecture-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_planning"),
    )
    p.add_argument(
        "--architecture-dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_dryrun_and_review"),
    )
    p.add_argument(
        "--core-planning-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_planning"),
    )
    p.add_argument(
        "--core-dryrun-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_dryrun_and_review"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    arch_plan = Path(args.architecture_planning_root)
    arch_dr = Path(args.architecture_dryrun_root)
    core_plan = Path(args.core_planning_root)
    core_dr = Path(args.core_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:28]}", (root / fname).is_file())

    arch_vr = _load(arch_plan / "verifier_report.json")
    arch_dr_vr = _load(arch_dr / "verifier_report.json")
    core_vr = _load(core_plan / "verifier_report.json")
    core_dr_vr = _load(core_dr / "verifier_report.json")
    core_dr_sm = _load(core_dr / "summary.json")
    core_dr_ready = _load(core_dr / "core_component_dryrun_readiness_decision_v1.json")

    ok("upstream.arch_plan_go", arch_vr.get("verifier") == "GO")
    ok("upstream.arch_dr_go", arch_dr_vr.get("verifier") == "GO")
    ok("upstream.core_plan_go", core_vr.get("verifier") == "GO")
    ok("upstream.core_dr_go", core_dr_vr.get("verifier") == "GO")
    ok("upstream.core_dr_final", core_dr_sm.get("final_decision") == CORE_DRYRUN_FINAL)
    ok("upstream.core_dr_ready", core_dr_ready.get("dryrun_pass") is True)

    for fname in ARCH_UPSTREAM_FILES:
        ok(f"arch.up.{fname[:22]}", (arch_plan / fname).is_file())
    for fname in CORE_UPSTREAM_FILES:
        ok(f"core.up.{fname[:22]}", (core_plan / fname).is_file())

    summary = _load(root / "summary.json")
    readiness = _load(root / "eb_wm_scheduler_planning_readiness_decision_v1.json")
    eb = _load(root / "event_bus_contract_v1.json")
    etypes = _load(root / "event_type_registry_v1.json")
    estates = _load(root / "event_state_machine_v1.json")
    wm = _load(root / "working_memory_contract_v1.json")
    wm_states = _load(root / "working_memory_entry_state_machine_v1.json")
    wm_ttl = _load(root / "working_memory_ttl_and_cleanup_policy_v1.json")
    sched = _load(root / "scheduler_contract_v1.json")
    prio = _load(root / "priority_queue_policy_v1.json")
    preempt = _load(root / "preemption_and_deferral_policy_v1.json")
    interaction = _load(root / "event_bus_working_memory_scheduler_interaction_model_v1.json")
    health = _load(root / "eb_wm_scheduler_health_metric_mapping_v1.json")
    failure = _load(root / "eb_wm_scheduler_failure_route_matrix_v1.json")
    gov = _load(root / "eb_wm_scheduler_governance_boundary_v1.json")
    flows = _load(root / "eb_wm_scheduler_sample_flow_plan_v1.json")
    boundary = _load(root / "eb_wm_scheduler_boundary_matrix_v1.json")
    nc = _load(root / "eb_wm_scheduler_non_claims_register_v1.json")

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE == "midplatform_event_bus_working_memory_scheduler_planning_only")
    ok("source.chain", summary.get("source_chain") == SOURCE_CHAIN)
    ok("gov.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("reuse.rule", summary.get("phase_governance_standard_reuse_rule") is True)
    ok("reuse.no_new_gov", summary.get("new_governance_need_proven") is False)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.violations_empty", len(summary.get("violations") or []) == 0)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.triad3", summary.get("foundation_components") == ["event_bus", "working_memory", "scheduler"])
    ok("readiness.pass", readiness.get("planning_pass") is True)
    ok("readiness.triad", readiness.get("foundation_triad_complete") is True)
    ok("upstream.match", UPSTREAM_CORE_DRYRUN_FINAL == CORE_DRYRUN_FINAL)

    ok("eb.contract_id", eb.get("contract_id") == "event_bus_contract_v1")
    ok("eb.component", eb.get("component_id") == "event_bus")
    ok("eb.layer", eb.get("layer") == "L3")
    for field in EVENT_BUS_FIELDS:
        ok(f"eb.field.{field[:14]}", field in (eb.get("required_fields") or []))
    for inp in ("standardized_candidate", "signal", "health_report", "feedback"):
        ok(f"eb.in.{inp[:12]}", inp in (eb.get("inputs") or []))
    for out in ("event", "working_memory_entry_ref", "scheduler_notification", "health_notification"):
        ok(f"eb.out.{out[:12]}", out in (eb.get("outputs") or []))
    for resp in eb.get("responsibilities") or []:
        ok(f"eb.resp.{resp[:10]}", bool(resp))
    for forb in ("semantic arbitration", "rewrite candidate content", "generate facts", "bypass governance"):
        ok(f"eb.forb.{forb[:10]}", forb in (eb.get("forbidden") or []))

    ok("etypes.count12", etypes.get("event_type_count") >= 12)
    for et in EVENT_TYPES:
        ok(f"etype.{et[:14]}", et in (etypes.get("event_types") or []))

    ok("estates.count13", estates.get("state_count") == len(EVENT_STATES))
    ok("estates.initial", estates.get("initial_state") == "received")
    for st in EVENT_STATES:
        ok(f"estate.{st[:12]}", st in (estates.get("states") or []))
    for term in ("completed", "expired", "discarded", "failed"):
        ok(f"estate.term.{term[:8]}", term in (estates.get("terminal_states") or []))

    ok("wm.contract_id", wm.get("contract_id") == "working_memory_contract_v1")
    ok("wm.component", wm.get("component_id") == "working_memory")
    ok("wm.layer", wm.get("layer") == "L3")
    for field in WORKING_MEMORY_FIELDS:
        ok(f"wm.field.{field[:14]}", field in (wm.get("required_fields") or []))
    ok("wm.not_memory", wm.get("working_memory_is_not_memory") is True)
    ok("wm.not_worldmodel", wm.get("working_memory_is_not_worldmodel") is True)
    for forb in ("long_term_deposit", "write_fact", "substitute_memory_or_worldmodel"):
        ok(f"wm.forb.{forb[:10]}", forb in (wm.get("forbidden") or []))
    for resp in wm.get("responsibilities") or []:
        ok(f"wm.resp.{resp[:10]}", bool(resp))

    ok("wmstates.count12", wm_states.get("state_count") == len(WM_ENTRY_STATES))
    ok("wmstates.initial", wm_states.get("initial_state") == "new")
    for st in WM_ENTRY_STATES:
        ok(f"wmstate.{st[:12]}", st in (wm_states.get("states") or []))

    ok("ttl.no_forbidden", wm_ttl.get("no_ttl_forbidden") is True)
    ok("ttl.p0_p5", len(wm_ttl.get("priority_ttl_policies") or []) == len(TTL_POLICIES))
    for pol in TTL_POLICIES:
        pkey = pol["priority"]
        found = next((p for p in wm_ttl.get("priority_ttl_policies") or [] if p.get("priority") == pkey), {})
        ok(f"ttl.{pkey}.name", found.get("name") == pol["name"])
        ok(f"ttl.{pkey}.ttl", found.get("ttl") == pol["ttl"])
        ok(f"ttl.{pkey}.expire", found.get("on_expire") == pol["on_expire"])
    for rule in ("expire_by_ttl", "compress_p5", "admission_candidate_on_confirm", "never_write_fact"):
        ok(f"ttl.clean.{rule[:10]}", rule in (wm_ttl.get("cleanup_rules") or []))

    ok("sched.contract_id", sched.get("contract_id") == "scheduler_contract_v1")
    ok("sched.component", sched.get("component_id") == "scheduler")
    for field in SCHEDULER_FIELDS:
        ok(f"sched.field.{field[:14]}", field in (sched.get("required_fields") or []))
    for forb in ("direct_task_execution", "direct_runtime_call", "direct_user_output"):
        ok(f"sched.forb.{forb[:10]}", forb in (sched.get("forbidden") or []))
    for resp in sched.get("responsibilities") or []:
        ok(f"sched.resp.{resp[:10]}", bool(resp))

    ok("prio.queues6", prio.get("queue_count") == 6)
    for level in PRIORITY_LEVELS:
        pkey = level["priority"]
        found = next((q for q in prio.get("queues") or [] if q.get("priority") == pkey), {})
        ok(f"prio.{pkey}.name", found.get("name") == level["name"])
        ok(f"prio.{pkey}.policy", found.get("policy") == level["policy"])

    for idx, rule in enumerate(preempt.get("rules") or []):
        ok(f"preempt.rule{idx}", bool(rule))

    ok("interaction.cycle6", len(interaction.get("cycle") or []) >= 6)
    for idx, step in enumerate(interaction.get("cycle") or []):
        ok(f"interaction.cycle{idx}", bool(step))
    ok("interaction.edges4", len(interaction.get("edges") or []) >= 4)
    for edge in interaction.get("edges") or []:
        eid = f"{edge.get('from', '')[:4]}_{edge.get('to', '')[:4]}"
        ok(f"edge.{eid}.from", bool(edge.get("from")))
        ok(f"edge.{eid}.to", bool(edge.get("to")))
        ok(f"edge.{eid}.payload", bool(edge.get("payload")))

    ok("health.eb", health.get("covers_event_bus") is True)
    ok("health.wm", health.get("covers_working_memory") is True)
    ok("health.sched", health.get("covers_scheduler") is True)
    ok("health.queue_shared", health.get("scheduler_queue_processing_shared") is True)
    for metric, comp in HEALTH_METRIC_EB_WM_SCHED_MAP.items():
        ok(f"healthmap.{metric[:14]}", health.get("metric_to_component", {}).get(metric) == comp)

    ok("failure.count12", failure.get("route_count") == len(FAILURE_ROUTES))
    for route in FAILURE_ROUTES:
        rid = route["route_id"]
        found = next((r for r in failure.get("routes", []) if r.get("route_id") == rid), {})
        ok(f"fail.{rid[:14]}.exists", bool(found))
        ok(f"fail.{rid[:14]}.comp", found.get("component") == route["component"])
        ok(f"fail.{rid[:14]}.detect", found.get("detection_signal") == route["detection_signal"])
        ok(f"fail.{rid[:14]}.resp", bool(found.get("default_response")))
        ok(f"fail.{rid[:14]}.recover", bool(found.get("recovery_candidate")))

    ok("gov.l0", gov.get("l0_global_constraint") is True)
    for idx, rule in enumerate(gov.get("rules") or []):
        ok(f"gov.rule{idx}", bool(rule))

    ok("flows.count4", flows.get("flow_count") >= 4)
    for flow in SAMPLE_FLOWS:
        fid = flow["flow_id"]
        found = next((f for f in flows.get("flows", []) if f.get("flow_id") == fid), {})
        ok(f"flow.{fid[:14]}.exists", bool(found))
        ok(f"flow.{fid[:14]}.prio", found.get("priority") == flow["priority"])
        for idx, st in enumerate(flow.get("states") or []):
            fstates = found.get("states") or []
            ok(f"flow.{fid[:8]}.st{idx}", idx < len(fstates))
            if idx < len(fstates):
                ok(f"flow.{fid[:8]}.st{idx}.comp", fstates[idx].get("component") == st.get("component"))

    for field in BOUNDARY_FALSE:
        ok(f"boundary.global.{field[:14]}", boundary.get("global_boundaries", {}).get(field) is False)
        ok(f"summary.boundary.{field[:10]}", summary.get(field) is False)

    for comp in ("event_bus", "working_memory", "scheduler"):
        cb = (boundary.get("foundation_components") or {}).get(comp, {})
        ok(f"comp.{comp[:8]}.exists", bool(cb))
        for field in BOUNDARY_FALSE:
            ok(f"comp.{comp[:6]}.{field[:10]}", cb.get(field) is False)

    for claim in NON_CLAIMS:
        ok(f"nc.{claim[:12]}", claim in (nc.get("non_claims") or []))
        ok(f"summary.nc.{claim[:8]}", claim in (summary.get("non_claims") or []))

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
    out_path = Path(args.output) if args.output else (root / "verify_midplatform_event_bus_working_memory_scheduler_planning_v1.json")
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
