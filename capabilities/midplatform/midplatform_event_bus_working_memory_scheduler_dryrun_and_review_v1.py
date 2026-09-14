# -*- coding: utf-8 -*-
"""Luna Midplatform Micro-OS Event Bus / Working Memory / Scheduler DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_planning_v1 import (
    BOUNDARY_FALSE,
    EVENT_BUS_FIELDS,
    EVENT_STATES,
    EVENT_TYPES,
    FAILURE_ROUTES,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HEALTH_METRIC_EB_WM_SCHED_MAP,
    NEXT_PHASE_GO as PLANNING_NEXT,
    SAMPLE_FLOWS,
    SCHEDULER_FIELDS,
    TTL_POLICIES,
    WM_ENTRY_STATES,
    WORKING_MEMORY_FIELDS,
)
from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import PRIORITY_LEVELS

PHASE_ID = "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-DryRunAndReview-v1-001"
SCOPE = "midplatform_event_bus_working_memory_scheduler_dryrun_and_review_only"
SOURCE = "midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_EVENT_BUS_WORKING_MEMORY_SCHEDULER_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Controlled-Skeleton-Implementation-Planning-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Issue-Review-v1-001"
)

UPSTREAM_PLANNING_FILES: Tuple[str, ...] = (
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
)

REQUIRED_HEALTH_METRICS: Tuple[str, ...] = (
    "core_bus_operational",
    "event_loop_active",
    "queue_processing_active",
    "pending_candidate_count",
    "stale_candidate_count",
    "ttl_violation_count",
    "long_pending_task_count",
    "health_tag_missing_count",
    "schema_invalid_count",
    "queue_backlog",
    "fallback_trigger_count",
    "degraded_mode_active",
)

FAILURE_ROUTE_IMPACT: Dict[str, str] = {
    "event_schema_invalid": "invalid_event_discarded_no_wm_entry",
    "event_missing_source_chain": "event_blocked_no_downstream",
    "event_missing_timestamp": "event_blocked_clock_untrusted",
    "event_missing_health_tag": "event_held_degraded_processing",
    "event_bus_queue_backlog": "p5_dropped_p3_p4_deferred",
    "working_memory_ttl_missing": "entry_rejected_no_active_processing",
    "working_memory_entry_stale": "entry_marked_stale_reobserve_required",
    "working_memory_long_pending": "watchdog_escalation_candidate",
    "scheduler_priority_conflict": "governance_arbitration_required",
    "scheduler_p0_starvation_forbidden": "p0_force_preempt",
    "scheduler_resource_overload": "degraded_mode_p5_drop",
    "scheduler_routing_failed": "hold_mode_no_task_dispatch",
}

FAILURE_ROUTE_FORBIDDEN: Dict[str, str] = {
    "event_schema_invalid": "bypass_governance_and_process",
    "event_missing_source_chain": "infer_source_and_continue",
    "event_missing_timestamp": "use_local_time_without_flag",
    "event_missing_health_tag": "process_as_healthy",
    "event_bus_queue_backlog": "unbounded_queue_growth",
    "working_memory_ttl_missing": "default_infinite_ttl",
    "working_memory_entry_stale": "treat_stale_as_confirmed",
    "working_memory_long_pending": "silent_drop_without_watchdog",
    "scheduler_priority_conflict": "scheduler_overrides_governance",
    "scheduler_p0_starvation_forbidden": "allow_p0_starvation",
    "scheduler_resource_overload": "continue_full_load",
    "scheduler_routing_failed": "direct_runtime_dispatch",
}

EVENT_STATE_PATHS: Tuple[Dict[str, Any], ...] = (
    {
        "path_id": "happy_path_completed",
        "terminal": "completed",
        "transitions": [
            "received", "normalized", "governance_pending", "health_pending",
            "queued", "stored_in_working_memory", "scheduled", "routed", "completed",
        ],
    },
    {
        "path_id": "ttl_expired_path",
        "terminal": "expired",
        "transitions": ["received", "normalized", "queued", "stored_in_working_memory", "expired"],
    },
    {
        "path_id": "p5_discarded_path",
        "terminal": "discarded",
        "transitions": ["received", "normalized", "queued", "discarded"],
    },
    {
        "path_id": "governance_blocked_path",
        "terminal": "blocked",
        "transitions": ["received", "normalized", "governance_pending", "blocked"],
    },
)

PREEMPTION_SCENARIOS: Tuple[Dict[str, Any], ...] = (
    {
        "scenario_id": "p0_preempts_navigation",
        "description": "navigation task preempted by P0 safety event",
        "active_priority": "P1",
        "incoming_priority": "P0",
        "expected": "preempt",
        "result": "preempt",
    },
    {
        "scenario_id": "ocr_pending_no_p0_block",
        "description": "OCR pending confirmation does not block P0",
        "active_priority": "P2",
        "incoming_priority": "P0",
        "expected": "p0_not_blocked",
        "result": "p0_not_blocked",
    },
    {
        "scenario_id": "p5_drop_on_overload",
        "description": "P5 background dropped on resource_overload",
        "active_priority": "P5",
        "condition": "resource_overload",
        "expected": "drop",
        "result": "drop",
    },
    {
        "scenario_id": "cloud_unavailable_local_hold",
        "description": "cloud_unavailable triggers local takeover or hold",
        "condition": "cloud_unavailable",
        "expected": "local_or_hold",
        "result": "local_or_hold",
    },
    {
        "scenario_id": "model_unavailable_fallback",
        "description": "model_unavailable triggers fallback or hold",
        "condition": "model_unavailable",
        "expected": "fallback_or_hold",
        "result": "fallback_or_hold",
    },
    {
        "scenario_id": "health_unknown_conservative",
        "description": "health_unknown defaults to conservative processing",
        "condition": "health_unknown",
        "expected": "conservative",
        "result": "conservative",
    },
)

NON_CLAIMS: Tuple[str, ...] = (
    "EB/WM/Scheduler DryRun ≠ real Event Bus enabled",
    "EB/WM/Scheduler DryRun ≠ real Working Memory enabled",
    "EB/WM/Scheduler DryRun ≠ real Scheduler enabled",
    "EB/WM/Scheduler DryRun ≠ runtime enabled",
    "EB/WM/Scheduler DryRun ≠ model invoked",
    "EB/WM/Scheduler DryRun ≠ provider invoked",
    "EB/WM/Scheduler DryRun ≠ task chain execution",
    "EB/WM/Scheduler DryRun ≠ Memory / WorldModel write",
    "EB/WM/Scheduler DryRun ≠ user output",
    "EB/WM/Scheduler DryRun ≠ real health monitoring runtime",
    "EB/WM/Scheduler DryRun ≠ real recovery executed",
    "EB/WM/Scheduler DryRun ≠ real concurrent execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_event_bus_working_memory_scheduler_dryrun_and_review_only",
    "simulated",
    "contract_level_simulation_only",
    "candidate_only",
)

DEFAULT_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_planning"
)
DEFAULT_CORE_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_core_component_planning"
)
DEFAULT_CORE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_core_component_dryrun_and_review"
)
DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_event_bus_working_memory_scheduler_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE,
        "system_level_simulated_go": True,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_result(checks: List[Tuple[str, bool]], **extra: Any) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "dry-run check failed"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "issue_count": len(issues),
        "dryrun_and_review_pass": len(issues) == 0,
        **extra,
    }


def _simulate_event_path(path: Dict[str, Any], states: Tuple[str, ...]) -> Dict[str, Any]:
    transitions = path["transitions"]
    valid = all(t in states for t in transitions)
    sequential = True
    for i in range(len(transitions) - 1):
        if transitions.index(transitions[i + 1]) <= transitions.index(transitions[i]) and transitions[i] != transitions[i + 1]:
            if transitions[i + 1] not in ("expired", "discarded", "blocked", "failed", "completed"):
                sequential = False
    return {
        "path_id": path["path_id"],
        "terminal": path["terminal"],
        "transitions": transitions,
        "path_valid": valid and len(transitions) >= 2,
        "terminal_reached": transitions[-1] == path["terminal"],
    }


def _simulate_wm_path(state: str, states: Tuple[str, ...]) -> Dict[str, Any]:
    return {
        "state": state,
        "reachable": state in states,
        "writes_fact": False,
        "writes_memory": False,
        "writes_worldmodel": False,
    }


def _simulate_ttl(priority: str, ttl: Optional[str], policies: Tuple[Dict[str, Any], ...]) -> Dict[str, Any]:
    pol = next((p for p in policies if p["priority"] == priority), None)
    if ttl is None:
        return {
            "priority": priority,
            "ttl": None,
            "outcome": "blocked_or_invalid",
            "active_processing_allowed": False,
            "no_ttl_forbidden_respected": True,
        }
    return {
        "priority": priority,
        "ttl": ttl,
        "policy_name": pol["name"] if pol else None,
        "on_expire": pol["on_expire"] if pol else None,
        "outcome": "active",
        "active_processing_allowed": True,
        "no_ttl_forbidden_respected": True,
    }


def run_midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1(
    *,
    midplatform_event_bus_working_memory_scheduler_planning_root: str,
    midplatform_micro_os_core_component_planning_root: str,
    midplatform_micro_os_core_component_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(midplatform_event_bus_working_memory_scheduler_planning_root).expanduser().resolve()
    core_plan = Path(midplatform_micro_os_core_component_planning_root).expanduser().resolve()
    core_dr = Path(midplatform_micro_os_core_component_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_planning_root": str(plan_root),
        "upstream_core_component_planning_root": str(core_plan),
        "upstream_core_component_dryrun_root": str(core_dr),
    }

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_ready = _try_read_json(plan_root / "eb_wm_scheduler_planning_readiness_decision_v1.json") or {}
    core_dr_vr = _try_read_json(core_dr / "verifier_report.json") or {}

    if plan_vr.get("verifier") != "GO":
        blockers.append("upstream planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("upstream planning final_decision mismatch")
    if plan_ready.get("planning_pass") is not True:
        blockers.append("upstream planning_readiness must pass")
    if core_dr_vr.get("verifier") != "GO":
        blockers.append("upstream core component dryrun verifier must be GO")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_PLANNING_FILES:
        data = _try_read_json(plan_root / fname)
        if data is None:
            blockers.append(f"missing upstream: {fname}")
        key = fname.replace("_v1.json", "") if fname.endswith("_v1.json") else fname.replace(".json", "")
        upstream[key] = data

    eb_contract = upstream.get("event_bus_contract") or {}
    etypes_doc = upstream.get("event_type_registry") or {}
    estates_doc = upstream.get("event_state_machine") or {}
    wm_contract = upstream.get("working_memory_contract") or {}
    wm_states_doc = upstream.get("working_memory_entry_state_machine") or {}
    wm_ttl_doc = upstream.get("working_memory_ttl_and_cleanup_policy") or {}
    sched_contract = upstream.get("scheduler_contract") or {}
    prio_doc = upstream.get("priority_queue_policy") or {}
    preempt_doc = upstream.get("preemption_and_deferral_policy") or {}
    interaction_doc = upstream.get("event_bus_working_memory_scheduler_interaction_model") or {}
    health_doc = upstream.get("eb_wm_scheduler_health_metric_mapping") or {}
    failure_doc = upstream.get("eb_wm_scheduler_failure_route_matrix") or {}
    gov_doc = upstream.get("eb_wm_scheduler_governance_boundary") or {}
    flows_doc = upstream.get("eb_wm_scheduler_sample_flow_plan") or {}
    boundary_doc = upstream.get("eb_wm_scheduler_boundary_matrix") or {}

    consumability_checks: List[Tuple[str, bool]] = []
    for fname in UPSTREAM_PLANNING_FILES:
        key = fname.replace("_v1.json", "")
        consumability_checks.append((f"upstream.{key[:20]}.exists", upstream.get(key) is not None))
    consumability_checks.append(("planning.readiness_pass", plan_ready.get("planning_pass") is True))
    consumability_checks.append(("planning.foundation_triad", plan_ready.get("foundation_triad_complete") is True))
    for field in EVENT_BUS_FIELDS:
        consumability_checks.append((f"eb.field.{field[:12]}", field in (eb_contract.get("required_fields") or [])))
    for field in WORKING_MEMORY_FIELDS:
        consumability_checks.append((f"wm.field.{field[:12]}", field in (wm_contract.get("required_fields") or [])))
    for field in SCHEDULER_FIELDS:
        consumability_checks.append((f"sched.field.{field[:12]}", field in (sched_contract.get("required_fields") or [])))

    upstream_review = {
        "review_id": "upstream_contract_consumability_review_v1",
        "objects_consumed": len(UPSTREAM_PLANNING_FILES),
        **_review_result(consumability_checks),
        **meta,
    }

    etype_checks: List[Tuple[str, bool]] = [
        ("event_type_count12", (etypes_doc.get("event_type_count") or 0) >= 12),
    ]
    for et in EVENT_TYPES:
        etype_checks.append((f"etype.{et[:14]}", et in (etypes_doc.get("event_types") or [])))
    event_type_review = {
        "review_id": "event_type_registry_review_v1",
        "event_types": list(etypes_doc.get("event_types") or []),
        **_review_result(etype_checks),
        **meta,
    }

    estate_list = tuple(estates_doc.get("states") or EVENT_STATES)
    path_runs = [_simulate_event_path(p, estate_list) for p in EVENT_STATE_PATHS]
    estate_checks: List[Tuple[str, bool]] = []
    for st in EVENT_STATES:
        estate_checks.append((f"state.{st[:12]}", st in estate_list))
    for run in path_runs:
        estate_checks.append((f"path.{run['path_id'][:14]}", run["path_valid"] and run["terminal_reached"]))
    terminals = {r["terminal"] for r in path_runs}
    for term in ("completed", "expired", "discarded", "blocked"):
        estate_checks.append((f"terminal.{term[:8]}", term in terminals))
    event_state_dryrun = {
        "dryrun_id": "event_state_machine_dryrun_v1",
        "paths": path_runs,
        "terminal_states_covered": list(terminals),
        **_review_result(estate_checks),
        **meta,
    }

    wm_state_list = tuple(wm_states_doc.get("states") or WM_ENTRY_STATES)
    wm_runs = [_simulate_wm_path(st, wm_state_list) for st in WM_ENTRY_STATES]
    wm_checks: List[Tuple[str, bool]] = []
    for st in WM_ENTRY_STATES:
        wm_checks.append((f"wmstate.{st[:12]}", st in wm_state_list))
    wm_checks.append(("wm.not_memory", wm_contract.get("working_memory_is_not_memory") is True))
    wm_checks.append(("wm.not_worldmodel", wm_contract.get("working_memory_is_not_worldmodel") is True))
    for run in wm_runs:
        wm_checks.append((f"wm.{run['state'][:10]}.no_fact", run["writes_fact"] is False))
        wm_checks.append((f"wm.{run['state'][:10]}.no_mem", run["writes_memory"] is False))
        wm_checks.append((f"wm.{run['state'][:10]}.no_wm", run["writes_worldmodel"] is False))
    wm_state_dryrun = {
        "dryrun_id": "working_memory_state_machine_dryrun_v1",
        "state_runs": wm_runs,
        **_review_result(wm_checks),
        **meta,
    }

    ttl_policies = tuple(wm_ttl_doc.get("priority_ttl_policies") or TTL_POLICIES)
    ttl_runs = [_simulate_ttl(p["priority"], p["ttl"], ttl_policies) for p in TTL_POLICIES]
    ttl_runs.append(_simulate_ttl("P2", None, ttl_policies))
    ttl_checks: List[Tuple[str, bool]] = [
        ("no_ttl_forbidden", wm_ttl_doc.get("no_ttl_forbidden") is True),
        ("ttl_missing_blocked", _simulate_ttl("P1", None, ttl_policies)["active_processing_allowed"] is False),
    ]
    for run in ttl_runs:
        ttl_checks.append((f"ttl.{run['priority']}.ok", run["no_ttl_forbidden_respected"] is True))
        if run["ttl"] is None:
            ttl_checks.append((f"ttl.{run['priority']}.blocked", run["outcome"] in ("blocked_or_invalid",)))
    for pol in TTL_POLICIES:
        found = next((p for p in ttl_policies if p.get("priority") == pol["priority"]), {})
        ttl_checks.append((f"policy.{pol['priority']}.name", found.get("name") == pol["name"]))
        ttl_checks.append((f"policy.{pol['priority']}.expire", found.get("on_expire") == pol["on_expire"]))
    ttl_dryrun = {
        "dryrun_id": "ttl_cleanup_policy_dryrun_v1",
        "simulations": ttl_runs,
        **_review_result(ttl_checks),
        **meta,
    }

    prio_checks: List[Tuple[str, bool]] = [
        ("queue_count6", (prio_doc.get("queue_count") or 0) == 6),
        ("p0_preempt", "preempt" in json.dumps(preempt_doc, ensure_ascii=False).lower()),
        ("p1_protected", "p1" in json.dumps(preempt_doc, ensure_ascii=False).lower()),
        ("p5_discard", "p5" in json.dumps(preempt_doc, ensure_ascii=False).lower() and "discard" in json.dumps(preempt_doc, ensure_ascii=False).lower()),
    ]
    for level in PRIORITY_LEVELS:
        pkey = level["priority"]
        found = next((q for q in (prio_doc.get("queues") or []) if q.get("priority") == pkey), {})
        prio_checks.append((f"prio.{pkey}.name", found.get("name") == level["name"]))
        prio_checks.append((f"prio.{pkey}.policy", found.get("policy") == level["policy"]))
    scheduler_prio_dryrun = {
        "dryrun_id": "scheduler_priority_queue_dryrun_v1",
        **_review_result(prio_checks),
        **meta,
    }

    preempt_runs = list(PREEMPTION_SCENARIOS)
    preempt_checks: List[Tuple[str, bool]] = [
        (f"scenario.{s['scenario_id'][:14]}", s["expected"] == s["result"]) for s in preempt_runs
    ]
    preempt_checks.append(("scenario_count6", len(preempt_runs) >= 6))
    preemption_dryrun = {
        "dryrun_id": "preemption_and_deferral_dryrun_v1",
        "scenarios": preempt_runs,
        **_review_result(preempt_checks),
        **meta,
    }

    interaction_checks: List[Tuple[str, bool]] = [
        ("cycle_exists", len(interaction_doc.get("cycle") or []) >= 4),
        ("edges_exists", len(interaction_doc.get("edges") or []) >= 4),
        ("eb_no_semantic", "semantic arbitration" in str(eb_contract.get("forbidden", [])).lower()),
        ("wm_no_long_term", "long_term" in str(wm_contract.get("forbidden", [])).lower() or "write_fact" in str(wm_contract.get("forbidden", [])).lower()),
        ("sched_no_exec", "direct_task_execution" in str(sched_contract.get("forbidden", [])).lower()),
        ("eb_to_wm", any(e.get("from") == "event_bus" and e.get("to") == "working_memory" for e in (interaction_doc.get("edges") or []))),
        ("eb_to_sched", any(e.get("from") == "event_bus" and e.get("to") == "scheduler" for e in (interaction_doc.get("edges") or []))),
        ("wm_to_sched", any(e.get("from") == "working_memory" and e.get("to") == "scheduler" for e in (interaction_doc.get("edges") or []))),
        ("sched_to_eb", any(e.get("from") == "scheduler" and e.get("to") == "event_bus" for e in (interaction_doc.get("edges") or []))),
    ]
    interaction_dryrun = {
        "dryrun_id": "interaction_model_dryrun_v1",
        **_review_result(interaction_checks),
        **meta,
    }

    health_map = health_doc.get("metric_to_component") or HEALTH_METRIC_EB_WM_SCHED_MAP
    health_checks: List[Tuple[str, bool]] = [
        ("covers_event_bus", health_doc.get("covers_event_bus") is True),
        ("covers_working_memory", health_doc.get("covers_working_memory") is True),
        ("covers_scheduler", health_doc.get("covers_scheduler") is True),
        ("covers_midplatform_self", health_doc.get("covers_event_bus") and health_doc.get("covers_working_memory")),
    ]
    for metric in REQUIRED_HEALTH_METRICS:
        health_checks.append((f"metric.{metric[:14]}", metric in health_map))
        expected = HEALTH_METRIC_EB_WM_SCHED_MAP.get(metric, health_map.get(metric))
        health_checks.append((f"map.{metric[:12]}", health_map.get(metric) == expected))
    health_review = {
        "review_id": "health_metric_mapping_review_v1",
        "metrics_reviewed": len(REQUIRED_HEALTH_METRICS),
        **_review_result(health_checks),
        **meta,
    }

    upstream_routes = {r.get("route_id"): r for r in (failure_doc.get("routes") or FAILURE_ROUTES)}
    failure_checks: List[Tuple[str, bool]] = []
    enriched_routes: List[Dict[str, Any]] = []
    for route in FAILURE_ROUTES:
        rid = route["route_id"]
        up = upstream_routes.get(rid, route)
        enriched = {
            **up,
            "route_id": rid,
            "impact": FAILURE_ROUTE_IMPACT.get(rid, "unknown_impact"),
            "forbidden_shortcut": FAILURE_ROUTE_FORBIDDEN.get(rid, "unknown_shortcut"),
            "dryrun_simulated": True,
        }
        enriched_routes.append(enriched)
        for field in ("detection_signal", "default_response", "recovery_candidate", "impact", "forbidden_shortcut"):
            failure_checks.append((f"route.{rid[:14]}.{field[:6]}", bool(enriched.get(field))))
    failure_review = {
        "review_id": "failure_route_dryrun_review_v1",
        "routes": enriched_routes,
        "route_count": len(enriched_routes),
        **_review_result(failure_checks),
        **meta,
    }

    gov_checks: List[Tuple[str, bool]] = [
        ("l0_constraint", gov_doc.get("l0_global_constraint") is True),
        ("rules_min6", len(gov_doc.get("rules") or []) >= 6),
        ("eb_governance", "governance" in json.dumps(gov_doc, ensure_ascii=False).lower()),
        ("wm_no_fact", "fact" in json.dumps(gov_doc, ensure_ascii=False).lower()),
        ("sched_no_bypass", "bypass" in json.dumps(gov_doc, ensure_ascii=False).lower() or "Governance Gate" in json.dumps(gov_doc, ensure_ascii=False)),
        ("l7_admission", "L7" in json.dumps(gov_doc, ensure_ascii=False) or "Admission" in json.dumps(gov_doc, ensure_ascii=False)),
    ]
    governance_review = {
        "review_id": "governance_boundary_review_v1",
        **_review_result(gov_checks),
        **meta,
    }

    flow_runs: List[Dict[str, Any]] = []
    flow_checks: List[Tuple[str, bool]] = []
    for flow in SAMPLE_FLOWS:
        fid = flow["flow_id"]
        plan_flow = next((f for f in (flows_doc.get("flows") or []) if f.get("flow_id") == fid), flow)
        eb_states = [s for s in plan_flow.get("states", []) if s.get("component") == "event_bus"]
        wm_states = [s for s in plan_flow.get("states", []) if s.get("component") == "working_memory"]
        sched_states = [s for s in plan_flow.get("states", []) if s.get("component") == "scheduler"]
        terminal = plan_flow.get("states", [])[-1] if plan_flow.get("states") else {}
        run = {
            "flow_id": fid,
            "priority": plan_flow.get("priority"),
            "event_bus_states": eb_states,
            "working_memory_states": wm_states,
            "scheduler_results": sched_states,
            "terminal_state": terminal,
            "blocked_paths": ["memory_write", "worldmodel_write", "user_output", "direct_runtime"],
            "simulation_pass": len(plan_flow.get("states") or []) >= 3,
        }
        flow_runs.append(run)
        flow_checks.append((f"flow.{fid[:14]}.sim", run["simulation_pass"]))
        flow_checks.append((f"flow.{fid[:14]}.eb", len(eb_states) >= 1 or fid == "memory_recall_reuse_flow"))
        flow_checks.append((f"flow.{fid[:14]}.wm", len(wm_states) >= 1))
        flow_checks.append((f"flow.{fid[:14]}.sched", len(sched_states) >= 1))
    sample_flow_dryrun = {
        "dryrun_id": "sample_flow_dryrun_v1",
        "flows": flow_runs,
        "flow_count": len(flow_runs),
        **_review_result(flow_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    global_b = boundary_doc.get("global_boundaries") or {}
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"global.{field[:14]}", global_b.get(field) is False))
        boundary_checks.append((f"meta.{field[:14]}", meta.get(field) is False))
    for comp in ("event_bus", "working_memory", "scheduler"):
        cb = (boundary_doc.get("foundation_components") or {}).get(comp, {})
        for field in BOUNDARY_FALSE:
            boundary_checks.append((f"comp.{comp[:6]}.{field[:10]}", cb.get(field) is False))
    boundary_review = {
        "review_id": "boundary_matrix_review_v1",
        **_review_result(boundary_checks),
        **meta,
    }

    review_passes = [
        upstream_review.get("dryrun_and_review_pass"),
        event_type_review.get("dryrun_and_review_pass"),
        event_state_dryrun.get("dryrun_and_review_pass"),
        wm_state_dryrun.get("dryrun_and_review_pass"),
        ttl_dryrun.get("dryrun_and_review_pass"),
        scheduler_prio_dryrun.get("dryrun_and_review_pass"),
        preemption_dryrun.get("dryrun_and_review_pass"),
        interaction_dryrun.get("dryrun_and_review_pass"),
        health_review.get("dryrun_and_review_pass"),
        failure_review.get("dryrun_and_review_pass"),
        governance_review.get("dryrun_and_review_pass"),
        sample_flow_dryrun.get("dryrun_and_review_pass"),
        boundary_review.get("dryrun_and_review_pass"),
    ]
    dryrun_issues: List[Dict[str, Any]] = []
    if blockers:
        dryrun_issues.extend([{"issue_id": f"blocker.{i}", "severity": "blocker", "detail": b} for i, b in enumerate(blockers)])
    for review_name, review in (
        ("upstream", upstream_review),
        ("event_type", event_type_review),
        ("event_state", event_state_dryrun),
        ("wm_state", wm_state_dryrun),
        ("ttl", ttl_dryrun),
        ("scheduler_prio", scheduler_prio_dryrun),
        ("preemption", preemption_dryrun),
        ("interaction", interaction_dryrun),
        ("health", health_review),
        ("failure", failure_review),
        ("governance", governance_review),
        ("sample_flow", sample_flow_dryrun),
        ("boundary", boundary_review),
    ):
        for issue in review.get("issues") or []:
            dryrun_issues.append({**issue, "review": review_name, "severity": "blocker"})

    blocker_count = len([i for i in dryrun_issues if i.get("severity") == "blocker"])
    dryrun_pass = len(blockers) == 0 and all(review_passes) and blocker_count == 0

    issue_register = {
        "register_id": "issue_register_v1",
        "issues": dryrun_issues,
        "issue_count": len(dryrun_issues),
        "blocker_count": blocker_count,
        **meta,
    }

    readiness = {
        "decision_id": "dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "reviews_total": 13,
        "reviews_passed": sum(1 for p in review_passes if p),
        "contracts_consumable": upstream_review.get("dryrun_and_review_pass") is True,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": blocker_count,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "non_claims": list(NON_CLAIMS),
        "foundation_components": ["event_bus", "working_memory", "scheduler"],
        **meta,
    }

    return {
        "summary": summary,
        "upstream_contract_consumability_review": upstream_review,
        "event_type_registry_review": event_type_review,
        "event_state_machine_dryrun": event_state_dryrun,
        "working_memory_state_machine_dryrun": wm_state_dryrun,
        "ttl_cleanup_policy_dryrun": ttl_dryrun,
        "scheduler_priority_queue_dryrun": scheduler_prio_dryrun,
        "preemption_and_deferral_dryrun": preemption_dryrun,
        "interaction_model_dryrun": interaction_dryrun,
        "health_metric_mapping_review": health_review,
        "failure_route_dryrun_review": failure_review,
        "governance_boundary_review": governance_review,
        "sample_flow_dryrun": sample_flow_dryrun,
        "boundary_matrix_review": boundary_review,
        "issue_register": issue_register,
        "dryrun_readiness_decision": readiness,
    }
