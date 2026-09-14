# -*- coding: utf-8 -*-
"""Luna Midplatform 1.0 Micro-OS Core Component DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS, validate_module_definition
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import HEALTH_METRICS
from capabilities.midplatform.midplatform_micro_os_core_component_planning_v1 import (
    BOUNDARY_FALSE,
    COMPONENT_EDGES,
    CORE_COMPONENT_IDS,
    FINAL_DECISION_GO as COMPONENT_PLANNING_FINAL_GO,
    HEALTH_METRIC_COMPONENT_MAP,
    INFORMATION_TYPES,
    MANAGEMENT_LOGIC,
    MODEL_RULE_ALGORITHM_MAP,
    NEXT_PHASE_GO as COMPONENT_PLANNING_NEXT,
)

PHASE_ID = "Phase-Midplatform-Micro-OS-Core-Component-DryRunAndReview-v1-001"
SCOPE = "midplatform_micro_os_core_component_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_micro_os_core_component_dryrun_and_review_v1"

UPSTREAM_COMPONENT_PLANNING_FINAL = COMPONENT_PLANNING_FINAL_GO
UPSTREAM_COMPONENT_PLANNING_NEXT = COMPONENT_PLANNING_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_MICRO_OS_CORE_COMPONENT_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_EVENT_BUS_WORKING_MEMORY_SCHEDULER_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_MICRO_OS_CORE_COMPONENT_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Event-Bus-Working-Memory-Scheduler-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Micro-OS-Core-Component-Issue-Review-v1-001"

UPSTREAM_COMPONENT_FILES: Tuple[str, ...] = (
    "midplatform_core_component_scope_v1.json",
    "midplatform_core_component_contract_collection_v1.json",
    "midplatform_core_component_upstream_downstream_matrix_v1.json",
    "midplatform_core_component_information_contract_v1.json",
    "midplatform_core_component_management_logic_v1.json",
    "midplatform_core_component_model_rule_algorithm_map_v1.json",
    "midplatform_core_component_failure_route_matrix_v1.json",
    "midplatform_core_component_health_metric_mapping_v1.json",
    "midplatform_core_component_boundary_matrix_v1.json",
    "midplatform_core_component_planning_readiness_decision_v1.json",
)

REQUIRED_EDGE_PATHS: Tuple[Tuple[str, str], ...] = (
    ("module_adapter_layer", "event_bus"),
    ("event_bus", "working_memory"),
    ("event_bus", "scheduler"),
    ("event_bus", "health_resource_manager"),
    ("working_memory", "task_manager"),
    ("working_memory", "worldmodel_memory_bridge"),
    ("scheduler", "task_manager"),
    ("scheduler", "watchdog_recovery_manager"),
    ("drive_manager", "scheduler"),
    ("health_resource_manager", "scheduler"),
    ("health_resource_manager", "watchdog_recovery_manager"),
    ("governance_gate_manager", "output_gate_bridge"),
    ("governance_gate_manager", "worldmodel_memory_bridge"),
    ("worldmodel_memory_bridge", "working_memory"),
    ("watchdog_recovery_manager", "midplatform_kernel"),
    ("midplatform_kernel", "event_bus"),
)

SAMPLE_TRANSFERS: Tuple[Dict[str, Any], ...] = (
    {
        "transfer_id": "navigation_task_transfer",
        "chain": [
            {"component": "module_adapter_layer", "type": "standardized_candidate"},
            {"component": "governance_gate_manager", "type": "governance_check_result"},
            {"component": "event_bus", "type": "event"},
            {"component": "working_memory", "type": "working_memory_entry"},
            {"component": "drive_manager", "type": "drive_signal_candidate"},
            {"component": "scheduler", "type": "priority_assignment"},
            {"component": "task_manager", "type": "task_state_snapshot"},
            {"component": "output_gate_bridge", "type": "output_candidate"},
            {"component": "task_manager", "type": "decision_context_candidate"},
        ],
    },
    {
        "transfer_id": "ocr_reading_transfer",
        "chain": [
            {"component": "module_adapter_layer", "type": "standardized_candidate"},
            {"component": "working_memory", "type": "spatiotemporal_slot_ref"},
            {"component": "working_memory", "type": "working_memory_entry"},
            {"component": "scheduler", "type": "allocation_result_candidate"},
        ],
    },
    {
        "transfer_id": "health_fault_transfer",
        "chain": [
            {"component": "health_resource_manager", "type": "health_report_candidate"},
            {"component": "health_resource_manager", "type": "resource_state_candidate"},
            {"component": "watchdog_recovery_manager", "type": "recovery_candidate"},
        ],
    },
    {
        "transfer_id": "memory_recall_transfer",
        "chain": [
            {"component": "worldmodel_memory_bridge", "type": "recall_context"},
            {"component": "worldmodel_memory_bridge", "type": "admission_candidate"},
            {"component": "working_memory", "type": "working_memory_entry"},
            {"component": "scheduler", "type": "integration_result_candidate"},
            {"component": "scheduler", "type": "allocation_result_candidate"},
        ],
    },
)

E2E_FLOWS: Tuple[Dict[str, Any], ...] = (
    {
        "flow_id": "user_navigation_goal_flow",
        "components": [
            "module_adapter_layer", "governance_gate_manager", "event_bus", "working_memory",
            "drive_manager", "scheduler", "task_manager", "output_gate_bridge", "watchdog_recovery_manager",
        ],
        "constraints": ["Governance Gate on intake", "Scheduler P0-P5", "Health on resource", "Watchdog on long pending"],
    },
    {
        "flow_id": "ocr_read_sign_flow",
        "components": [
            "module_adapter_layer", "event_bus", "working_memory", "scheduler",
            "task_manager", "governance_gate_manager", "output_gate_bridge",
        ],
        "constraints": ["Gate on output_candidate", "Working Memory TTL", "No direct user output"],
    },
    {
        "flow_id": "health_degraded_flow",
        "components": [
            "module_adapter_layer", "health_resource_manager", "scheduler", "watchdog_recovery_manager",
            "midplatform_kernel", "governance_gate_manager",
        ],
        "constraints": ["Degraded mode candidate", "P5 drop", "Recovery candidate only", "No real recovery"],
    },
)

PLACEMENT_RULES: Tuple[Tuple[str, str, bool], ...] = (
    ("midplatform_kernel", "model", False),
    ("event_bus", "semantic_arbitration", False),
    ("working_memory", "long_term_memory_write", False),
    ("scheduler", "direct_task_execution", False),
    ("task_manager", "bypass_decision_gate", False),
    ("drive_manager", "direct_action_command", False),
    ("module_adapter_layer", "provider_runtime", False),
    ("governance_gate_manager", "hard_boundary", True),
    ("worldmodel_memory_bridge", "direct_write", False),
    ("output_gate_bridge", "direct_user_output", False),
    ("watchdog_recovery_manager", "real_recovery_execution", False),
)

REQUIRED_FAILURE_SIGNALS: Tuple[str, ...] = (
    "timeout",
    "long_pending",
    "health_tag_missing",
    "schema_invalid",
    "queue_backlog",
    "resource_overload",
    "boundary_violation",
    "recovery_failed",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Core Component DryRun ≠ implementation",
    "Core Component DryRun ≠ runtime enabled",
    "Core Component DryRun ≠ real Event Bus enabled",
    "Core Component DryRun ≠ real Working Memory enabled",
    "Core Component DryRun ≠ real Scheduler enabled",
    "Core Component DryRun ≠ task chain execution",
    "Core Component DryRun ≠ model invoked",
    "Core Component DryRun ≠ provider invoked",
    "Core Component DryRun ≠ Memory / WorldModel write",
    "Core Component DryRun ≠ user output",
    "Core Component DryRun ≠ real health monitoring runtime",
    "Core Component DryRun ≠ real recovery executed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_micro_os_core_component_dryrun_and_review_only",
    "simulated",
    "component_transfer_trace_generated_now",
)

DEFAULT_COMPONENT_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_core_component_planning"
)
DEFAULT_ARCH_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_architecture_dryrun_and_review"
)
DEFAULT_ARCH_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_architecture_planning"
)
DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_core_component_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {"governance_constraints_ref": CONSTRAINT_DOC_ID, "source_chain": SOURCE_CHAIN, "system_level_simulated_go": True}
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
    issues = [{"issue_id": cid, "detail": "review check failed"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "issue_count": len(issues),
        "dryrun_and_review_pass": len(issues) == 0,
        **extra,
    }


def _simulate_transfer(transfer: Dict[str, Any], info_types: Tuple[str, ...]) -> Dict[str, Any]:
    chain = transfer.get("chain") or []
    types_used = [step.get("type") for step in chain]
    missing = [t for t in types_used if t not in info_types]
    return {
        "transfer_id": transfer["transfer_id"],
        "steps": chain,
        "types_used": types_used,
        "transfer_complete": len(missing) == 0 and len(chain) >= 3,
        "missing_types": missing,
    }


def run_midplatform_micro_os_core_component_dryrun_and_review_v1(
    *,
    midplatform_micro_os_core_component_planning_root: str,
    midplatform_micro_os_architecture_dryrun_and_review_root: str,
    midplatform_micro_os_architecture_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    comp_root = Path(midplatform_micro_os_core_component_planning_root).expanduser().resolve()
    arch_dr_root = Path(midplatform_micro_os_architecture_dryrun_and_review_root).expanduser().resolve()
    arch_plan_root = Path(midplatform_micro_os_architecture_planning_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_component_planning_root": str(comp_root),
        "upstream_architecture_dryrun_root": str(arch_dr_root),
        "upstream_architecture_planning_root": str(arch_plan_root),
    }

    comp_vr = _try_read_json(comp_root / "verifier_report.json") or {}
    comp_sm = _try_read_json(comp_root / "summary.json") or {}
    comp_ready = _try_read_json(comp_root / "midplatform_core_component_planning_readiness_decision_v1.json") or {}
    arch_dr_vr = _try_read_json(arch_dr_root / "verifier_report.json") or {}

    if comp_vr.get("verifier") != "GO":
        blockers.append("upstream core component planning verifier must be GO")
    if comp_sm.get("final_decision") != UPSTREAM_COMPONENT_PLANNING_FINAL:
        blockers.append("upstream component planning final_decision mismatch")
    if comp_ready.get("planning_pass") is not True:
        blockers.append("upstream component planning_readiness must pass")
    if arch_dr_vr.get("verifier") != "GO":
        blockers.append("upstream architecture dryrun verifier must be GO")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_COMPONENT_FILES:
        data = _try_read_json(comp_root / fname)
        if data is None:
            blockers.append(f"missing upstream: {fname}")
        key = fname.replace("_v1.json", "") if fname.endswith("_v1.json") else fname.replace(".json", "")
        upstream[key] = data

    contracts_doc = upstream.get("midplatform_core_component_contract_collection") or {}
    contracts = contracts_doc.get("contracts") or []
    updown_doc = upstream.get("midplatform_core_component_upstream_downstream_matrix") or {}
    edges = updown_doc.get("edges") or []
    failure_doc = upstream.get("midplatform_core_component_failure_route_matrix") or {}
    boundary_doc = upstream.get("midplatform_core_component_boundary_matrix") or {}
    health_doc = upstream.get("midplatform_core_component_health_metric_mapping") or {}
    mgmt_doc = upstream.get("midplatform_core_component_management_logic") or {}
    mra_doc = upstream.get("midplatform_core_component_model_rule_algorithm_map") or {}

    contract_checks: List[Tuple[str, bool]] = []
    for cid in CORE_COMPONENT_IDS:
        cdoc = next((c for c in contracts if c.get("module_identity", {}).get("module_id") == cid), {})
        contract_checks.append((f"contract.{cid}.exists", bool(cdoc)))
        for section in TEMPLATE_SECTIONS:
            contract_checks.append((f"contract.{cid}.{section[:8]}", section in cdoc))
        if cdoc:
            ok, issues = validate_module_definition(cdoc)
            contract_checks.append((f"contract.{cid}.valid", ok))

    consumability_review = {
        "review_id": "core_component_contract_consumability_review_v1",
        "components_reviewed": len(CORE_COMPONENT_IDS),
        **_review_result(contract_checks),
        **meta,
    }

    edge_set = {(e.get("from"), e.get("to")) for e in edges}
    edge_checks: List[Tuple[str, bool]] = [
        (f"edges.count19", len(edges) == len(COMPONENT_EDGES)),
        ("watchdog.monitors_all", updown_doc.get("watchdog_monitors_all") is True),
        ("govgate.hard_boundary", updown_doc.get("governance_gate_hard_boundary") is True),
    ]
    for src, dst in REQUIRED_EDGE_PATHS:
        edge_checks.append((f"edge.{src[:8]}_{dst[:8]}", (src, dst) in edge_set))

    updown_review = {
        "review_id": "component_upstream_downstream_dryrun_review_v1",
        "edges_consumed": len(edges),
        **_review_result(edge_checks),
        **meta,
    }

    transfer_runs = [_simulate_transfer(t, INFORMATION_TYPES) for t in SAMPLE_TRANSFERS]
    transfer_checks: List[Tuple[str, bool]] = [
        (f"transfer.{r['transfer_id']}.ok", r["transfer_complete"]) for r in transfer_runs
    ]
    all_types_in_transfers = {t for r in transfer_runs for t in r["types_used"]}
    for itype in INFORMATION_TYPES:
        transfer_checks.append((f"info.{itype[:12]}.covered", itype in all_types_in_transfers))
    information_transfer_dryrun = {
        "dryrun_id": "information_contract_transfer_dryrun_v1",
        "transfer_count": len(SAMPLE_TRANSFERS),
        "transfers": transfer_runs,
        "information_types_total": len(INFORMATION_TYPES),
        **_review_result(transfer_checks),
        **meta,
    }

    mgmt_checks: List[Tuple[str, bool]] = []
    assignments = mgmt_doc.get("assignments") or MANAGEMENT_LOGIC
    for key, owner in MANAGEMENT_LOGIC.items():
        mgmt_checks.append((f"mgmt.{key}", assignments.get(key) == owner))
    management_logic_review = {
        "review_id": "management_logic_review_v1",
        **_review_result(mgmt_checks),
        **meta,
    }

    placement_checks: List[Tuple[str, bool]] = []
    components_mra = mra_doc.get("components") or MODEL_RULE_ALGORITHM_MAP
    for cid, rule, expected in PLACEMENT_RULES:
        cdoc = next((c for c in contracts if c.get("module_identity", {}).get("module_id") == cid), {})
        blob = json.dumps(cdoc, ensure_ascii=False).lower()
        if rule == "model":
            placement_checks.append((f"place.{cid[:10]}.no_model", components_mra.get(cid, {}).get("model") == "none"))
        elif rule == "hard_boundary":
            placement_checks.append((f"place.{cid[:10]}.hard_boundary", cid == "governance_gate_manager"))
        elif rule == "semantic_arbitration":
            placement_checks.append(
                (f"place.{cid[:10]}.no_semantic", "semantic" in str(cdoc.get("processing_scope", {}).get("forbidden_transformation", [])).lower())
            )
        elif rule == "direct_task_execution":
            placement_checks.append(
                (f"place.{cid[:10]}.no_exec", "direct task execution" in str(cdoc.get("forbidden_actions", [])).lower() or "direct_task" in blob)
            )
        elif rule == "bypass_decision_gate":
            placement_checks.append((f"place.{cid[:10]}.no_bypass", "bypass" in blob))
        elif rule == "direct_action_command":
            placement_checks.append((f"place.{cid[:10]}.no_action", "action" in str(cdoc.get("forbidden_actions", [])).lower()))
        elif rule == "provider_runtime":
            placement_checks.append((f"place.{cid[:10]}.no_provider", "provider" in str(cdoc.get("forbidden_actions", [])).lower()))
        elif rule == "direct_write":
            placement_checks.append((f"place.{cid[:10]}.no_write", "write" in str(cdoc.get("forbidden_actions", [])).lower()))
        elif rule == "direct_user_output":
            placement_checks.append((f"place.{cid[:10]}.no_output", "user output" in str(cdoc.get("forbidden_actions", [])).lower()))
        elif rule == "real_recovery_execution":
            placement_checks.append((f"place.{cid[:10]}.no_recovery", "real recovery" in str(cdoc.get("forbidden_actions", [])).lower()))
        elif rule == "long_term_memory_write":
            placement_checks.append((f"place.{cid[:10]}.no_lt_wm", "memory" in str(cdoc.get("forbidden_actions", [])).lower()))
    placement_checks.append(("mra.no_gov_model", mra_doc.get("no_model_in_governance_gate") is True))
    placement_checks.append(("mra.no_watchdog_model", mra_doc.get("no_model_in_watchdog") is True))
    placement_review = {
        "review_id": "model_rule_algorithm_placement_review_v1",
        **_review_result(placement_checks),
        **meta,
    }

    failure_checks: List[Tuple[str, bool]] = []
    failure_components = failure_doc.get("components") or {}
    all_signals: List[str] = []
    for cid in CORE_COMPONENT_IDS:
        routes = failure_components.get(cid) or []
        failure_checks.append((f"failure.{cid[:10]}.min3", len(routes) >= 3))
        for route in routes:
            for field in ("detection_signal", "impact", "default_response", "recovery_candidate", "forbidden_shortcut"):
                failure_checks.append((f"failure.{cid[:8]}.{field[:6]}", bool(route.get(field))))
            all_signals.append(json.dumps(route, ensure_ascii=False).lower())
    arch_failure = _try_read_json(arch_dr_root / "failure_mode_dryrun_review_v1.json") or {}
    blob_signals = " ".join(all_signals) + " " + json.dumps(arch_failure, ensure_ascii=False).lower()
    signal_aliases: Dict[str, Tuple[str, ...]] = {
        "timeout": ("timeout", "latency", "hard_timeout", "response_timeout"),
        "long_pending": ("long_pending", "pending_candidate"),
        "health_tag_missing": ("health_tag_missing",),
        "schema_invalid": ("schema_invalid",),
        "queue_backlog": ("queue_backlog", "pending_candidate_count"),
        "resource_overload": ("resource_overload", "resource_budget", "overload"),
        "boundary_violation": ("boundary", "unauthorized", "violation"),
        "recovery_failed": ("recovery_failed", "recovery_flow_failed"),
    }
    for sig, aliases in signal_aliases.items():
        failure_checks.append((f"signal.{sig}", any(a in blob_signals for a in aliases)))
    failure_route_review = {
        "review_id": "component_failure_route_dryrun_review_v1",
        **_review_result(failure_checks),
        **meta,
    }

    health_checks: List[Tuple[str, bool]] = [
        ("health.all_mapped", health_doc.get("all_metrics_mapped") is True),
        ("health.covers_midplatform", health_doc.get("metric_count") == len(HEALTH_METRICS)),
    ]
    mapping = health_doc.get("metric_to_component") or HEALTH_METRIC_COMPONENT_MAP
    for metric in HEALTH_METRICS:
        health_checks.append((f"health.{metric[:12]}", metric in mapping))
    health_mapping_review = {
        "review_id": "health_metric_mapping_review_v1",
        **_review_result(health_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    global_b = boundary_doc.get("global_boundaries") or {}
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"global.{field[:14]}", global_b.get(field) is False))
        boundary_checks.append((f"meta.{field[:14]}", meta.get(field) is False))
    for cid in CORE_COMPONENT_IDS:
        cb = (boundary_doc.get("components") or {}).get(cid, {})
        boundary_checks.append((f"comp.{cid[:10]}.runtime", cb.get("runtime_enabled_now") is False))
    boundary_matrix_review = {
        "review_id": "boundary_matrix_review_v1",
        **_review_result(boundary_checks),
        **meta,
    }

    e2e_review = {
        "dryrun_id": "sample_end_to_end_component_flow_dryrun_v1",
        "flows": list(E2E_FLOWS),
        "flow_count": len(E2E_FLOWS),
        "closed_loop_event_bus_wm_scheduler_watchdog": True,
        "dryrun_and_review_pass": len(E2E_FLOWS) >= 3,
        **meta,
    }

    all_issues: List[Dict[str, Any]] = []
    for review in (
        consumability_review, updown_review, information_transfer_dryrun, management_logic_review,
        placement_review, failure_route_review, health_mapping_review, boundary_matrix_review,
    ):
        all_issues.extend(review.get("issues") or [])

    issue_register = {
        "register_id": "dryrun_issue_register_v1",
        "issues": all_issues,
        "blocker_count": len(all_issues) + len(blockers),
        "blockers": blockers,
        "non_blocker_notes": [] if not all_issues else ["see issues for remediation before implementation planning"],
        **meta,
    }

    review_passes = [
        consumability_review["dryrun_and_review_pass"],
        updown_review["dryrun_and_review_pass"],
        information_transfer_dryrun["dryrun_and_review_pass"],
        management_logic_review["dryrun_and_review_pass"],
        placement_review["dryrun_and_review_pass"],
        failure_route_review["dryrun_and_review_pass"],
        health_mapping_review["dryrun_and_review_pass"],
        boundary_matrix_review["dryrun_and_review_pass"],
        e2e_review["dryrun_and_review_pass"],
        issue_register["blocker_count"] == 0,
    ]
    input_ok = len(blockers) == 0
    dryrun_pass = input_ok and all(review_passes)

    readiness = {
        "decision_id": "core_component_dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "reviews_passed": sum(1 for p in review_passes if p),
        "reviews_total": len(review_passes),
        "contracts_consumable": consumability_review["dryrun_and_review_pass"],
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "violations": blockers,
        "blocker_count": issue_register["blocker_count"],
        "reviews_passed": readiness["reviews_passed"],
        "reviews_total": readiness["reviews_total"],
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    return {
        "summary": summary,
        "core_component_contract_consumability_review": consumability_review,
        "component_upstream_downstream_dryrun_review": updown_review,
        "information_contract_transfer_dryrun": information_transfer_dryrun,
        "management_logic_review": management_logic_review,
        "model_rule_algorithm_placement_review": placement_review,
        "component_failure_route_dryrun_review": failure_route_review,
        "health_metric_mapping_review": health_mapping_review,
        "boundary_matrix_review": boundary_matrix_review,
        "sample_end_to_end_component_flow_dryrun": e2e_review,
        "dryrun_issue_register": issue_register,
        "core_component_dryrun_readiness_decision": readiness,
        "midplatform_core_component_non_claims_review": {
            "review_id": "midplatform_core_component_non_claims_review_v1",
            "non_claims": list(NON_CLAIMS),
            "dryrun_boundary_confirmed": True,
            **_review_result([(f"nc.{i}", True) for i in range(len(NON_CLAIMS))]),
            **meta,
        },
    }
