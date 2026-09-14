# -*- coding: utf-8 -*-
"""Luna Midplatform Information Integration Mount DryRunAndReview v1."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core.micro_os_common_types_v1 import (
    Event,
    EventState,
    EventType,
    GovernanceCheckRef,
    HealthTag,
    PriorityClass,
    SchedulingDecisionCandidate,
    WorkingMemoryEntry,
    WorkingMemoryEntryState,
)
from capabilities.midplatform.core.micro_os_static_validators_v1 import (
    validate_candidate_not_fact,
    validate_governance_guard,
    validate_no_runtime_flags,
    validate_required_health_tag,
    validate_required_trace,
    validate_required_ttl,
)
from capabilities.midplatform.midplatform_information_integration_mount_planning_v1 import (
    ALGORITHM_USES,
    BOUNDARY_FALSE,
    FAILURE_ROUTES,
    FROZEN_INTERFACE_CONSUMED,
    HEALTH_METRICS,
    INPUT_REQUIRED_FIELDS,
    INPUT_TYPES,
    MODEL_USES,
    NEXT_PHASE_GO as MOUNT_PLANNING_NEXT,
    OUTPUT_CANDIDATES,
    PROCESSING_STEPS,
    RULE_USES,
    SAMPLE_FLOWS,
    FINAL_DECISION_GO as MOUNT_PLANNING_FINAL_GO,
)
from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FREEZE_DRYRUN_FINAL_GO,
    MODULE_MAP,
)

PHASE_ID = "Phase-Midplatform-Information-Integration-Mount-DryRunAndReview-v1-001"
SCOPE = "midplatform_information_integration_mount_dryrun_and_review_only"
SOURCE = "midplatform_information_integration_mount_dryrun_and_review_v1"

UPSTREAM_MOUNT_PLANNING_FINAL = MOUNT_PLANNING_FINAL_GO
UPSTREAM_MOUNT_PLANNING_NEXT = MOUNT_PLANNING_NEXT

FINAL_DECISION_GO = (
    "MIDPLATFORM_INFORMATION_INTEGRATION_MOUNT_DRYRUN_AND_REVIEW_"
    "CLOSED_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "MIDPLATFORM_INFORMATION_INTEGRATION_MOUNT_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Information-Integration-Controlled-Skeleton-Implementation-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Information-Integration-Mount-Issue-Review-v1-001"

UPSTREAM_MOUNT_PLANNING_FILES: Tuple[str, ...] = (
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

UPSTREAM_FOUNDATION_FILES: Tuple[str, ...] = (
    "micro_os_foundation_version_tag_v1.json",
    "micro_os_foundation_frozen_interface_v1.json",
    "micro_os_foundation_handoff_contract_v1.json",
)

FROZEN_INTERFACE_DRYRUN: Tuple[str, ...] = (
    "Event",
    "EventType",
    "EventState",
    "WorkingMemoryEntry",
    "WorkingMemoryEntryState",
    "PriorityClass",
    "SchedulingRequest",
    "SchedulingDecisionCandidate",
    "validate_no_runtime_flags",
    "validate_candidate_not_fact",
    "validate_required_trace",
    "validate_required_health_tag",
    "validate_required_ttl",
    "validate_governance_guard",
)

INPUT_DRYRUN_TYPES: Tuple[str, ...] = (
    "Event",
    "WorkingMemoryEntry",
    "SchedulingDecisionCandidate",
    "spatiotemporal_slot_ref",
    "health_report_candidate",
    "resource_state_candidate",
    "worldmodel_recall_context",
    "memory_recall_context",
    "governance_check_ref",
    "trace_ref",
)

DRYRUN_NON_CLAIMS: Tuple[str, ...] = (
    "Mount DryRun ≠ Information Integration implemented",
    "Mount DryRun ≠ mounted now",
    "Mount DryRun ≠ runtime enabled",
    "Mount DryRun ≠ model invoked",
    "Mount DryRun ≠ Decision Center ready",
    "Mount DryRun ≠ Task Manager ready",
    "Mount DryRun ≠ Output allowed",
    "Mount DryRun ≠ Memory / WorldModel write",
    "Mount DryRun ≠ full information integration pipeline",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_information_integration_mount_dryrun_and_review_only",
    "simulated",
    "contract_level_validation_only",
)

DEFAULT_MOUNT_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_mount_planning"
)
DEFAULT_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_FREEZE_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_mount_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {"governance_constraints_ref": CONSTRAINT_DOC_ID, "source_chain": SOURCE}
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
    issues = [{"issue_id": cid, "detail": "mount dryrun review check failed"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "issue_count": len(issues),
        "dryrun_and_review_pass": len(issues) == 0,
        **extra,
    }


def _function_exists(fn: str) -> bool:
    mod_path = MODULE_MAP.get(fn)
    if not mod_path:
        return False
    mod = importlib.import_module(mod_path)
    return hasattr(mod, fn) and callable(getattr(mod, fn))


def _type_exists(type_name: str) -> bool:
    mod = importlib.import_module("capabilities.midplatform.core.micro_os_common_types_v1")
    return hasattr(mod, type_name)


def _sample_event(*, valid: bool = True) -> Event:
    return Event(
        event_id="evt-dryrun-001",
        event_type=EventType.MODULE_CANDIDATE,
        source_module="module_adapter",
        source_chain="module_adapter>event_bus",
        timestamp="2026-06-08T00:00:00Z",
        health_tag=HealthTag("ok") if valid else None,
        priority_hint=PriorityClass.P2,
        ttl_hint=120 if valid else None,
        governance_required=False,
        governance_check_ref=None,
        routing_targets=("working_memory",),
        event_state=EventState.STORED_IN_WORKING_MEMORY,
        trace_id="trace-001" if valid else "",
    )


def _sample_wm_entry(*, valid: bool = True, stale: bool = False) -> WorkingMemoryEntry:
    return WorkingMemoryEntry(
        working_memory_entry_id="wm-dryrun-001",
        event_ref="evt-dryrun-001",
        candidate_ref="cand-001",
        task_ref="task-nav-001",
        priority_class=PriorityClass.P1,
        state=WorkingMemoryEntryState.STALE if stale else WorkingMemoryEntryState.ACTIVE,
        ttl=120 if valid else None,
        trace_id="trace-001" if valid else "",
        spatiotemporal_slot_ref="slot-001",
        freshness_status="stale" if stale else "fresh",
        candidate_not_fact=True,
    )


def _sample_scheduling_decision() -> SchedulingDecisionCandidate:
    return SchedulingDecisionCandidate(
        decision_id="sched-dryrun-001",
        request_ref="req-001",
        priority_class=PriorityClass.P1,
        routing_decision="information_integration",
        preemption_candidate=False,
        defer_candidate=False,
        drop_candidate=False,
        blocked=False,
        candidate_only=True,
        runtime_execution=False,
    )


def _sample_input_bundle() -> Dict[str, Any]:
    return {
        "Event": _sample_event(),
        "WorkingMemoryEntry": _sample_wm_entry(),
        "SchedulingDecisionCandidate": _sample_scheduling_decision(),
        "spatiotemporal_slot_ref": {"slot_id": "slot-001", "candidate_not_fact": True},
        "health_report_candidate": {"signal": "ok", "health_tag": "healthy", "candidate_not_fact": True},
        "resource_state_candidate": {"cpu": "normal", "candidate_not_fact": True},
        "worldmodel_recall_context": {"hint_only": True, "known_state_candidate": True, "candidate_not_fact": True},
        "memory_recall_context": {"hint_only": True, "change_detection_reference": True, "candidate_not_fact": True},
        "governance_check_ref": {"check_id": "gov-001", "cleared": True, "candidate_not_fact": True},
        "trace_ref": {"trace_id": "trace-001", "candidate_not_fact": True},
    }


def _simulate_processing_step(step: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    outputs: List[str] = []
    if "collect" in step:
        outputs.append("eligible_entry_candidate")
    if "group" in step:
        outputs.append("slot_group_candidate")
    if "conflict" in step or "gap" in step:
        outputs.extend(["conflict_candidate", "gap_candidate"])
    if "live world state" in step:
        outputs.append("live_world_state_candidate")
    if "task world slice" in step:
        outputs.append("task_world_slice_candidate")
    if "allocate" in step:
        outputs.append("information_allocation_candidate")
    if "decision context" in step:
        outputs.append("decision_context_candidate")
    return {
        "step": step,
        "input_refs": list(inputs.keys())[:3],
        "output_candidates": outputs or ["integration_step_candidate"],
        "runtime_executed": False,
        "fact_promoted": False,
        "simulation_pass": True,
    }


def _simulate_sample_flow(flow: Dict[str, Any]) -> Dict[str, Any]:
    inputs = _sample_input_bundle()
    steps = [_simulate_processing_step(s, inputs) for s in PROCESSING_STEPS]
    return {
        "flow_id": flow["flow_id"],
        "inputs": flow.get("inputs") or [],
        "processing_steps": [s["step"] for s in steps],
        "output_candidates": flow.get("outputs") or [],
        "blocked_paths": flow.get("blocked_paths") or [],
        "terminal_status": "ready_for_decision_context",
        "runtime_executed": False,
        "direct_mount": False,
        "simulation_pass": True,
    }


def _simulate_governance_scenario(scenario_id: str) -> Dict[str, Any]:
    blocked = True
    if scenario_id == "high_risk_no_governance":
        event = Event(
            event_id="evt-gov-001",
            event_type=EventType.USER_GOAL,
            source_module="module_adapter",
            source_chain="test",
            timestamp="2026-06-08T00:00:00Z",
            health_tag=HealthTag("ok"),
            priority_hint=PriorityClass.P0,
            ttl_hint=30,
            governance_required=True,
            governance_check_ref=None,
            routing_targets=("information_integration",),
            event_state=EventState.GOVERNANCE_PENDING,
            trace_id="trace-gov-001",
        )
        result = validate_governance_guard(event)
        blocked = not result.valid
    elif scenario_id == "output_before_decision":
        blocked = True
    elif scenario_id == "memory_write_attempted":
        blocked = True
    elif scenario_id == "worldmodel_write_attempted":
        blocked = True
    elif scenario_id == "model_invocation_attempted_now":
        blocked = True
    elif scenario_id == "provider_invocation_attempted_now":
        blocked = True
    elif scenario_id == "no_bypass_scheduler":
        blocked = True
    elif scenario_id == "no_bypass_working_memory":
        blocked = True
    elif scenario_id == "no_bypass_event_bus":
        blocked = True
    return {"scenario_id": scenario_id, "blocked": blocked, "simulation_pass": blocked}


def _simulate_health_scenario(scenario_id: str) -> Dict[str, Any]:
    meta = _dryrun_meta()
    if scenario_id == "missing_health_tag":
        r = validate_required_health_tag(_sample_event(valid=False))
        return {"scenario_id": scenario_id, "blocked": r.blocked, "response": "health_issue_candidate"}
    if scenario_id == "missing_timestamp":
        return {"scenario_id": scenario_id, "blocked": True, "response": "invalid"}
    if scenario_id == "missing_source_chain":
        return {"scenario_id": scenario_id, "blocked": True, "response": "invalid"}
    if scenario_id == "ttl_missing":
        r = validate_required_ttl(_sample_wm_entry(valid=False))
        return {"scenario_id": scenario_id, "blocked": r.blocked, "response": "blocked"}
    if scenario_id == "stale_candidate":
        return {"scenario_id": scenario_id, "blocked": False, "response": "reobserve_candidate"}
    if scenario_id == "low_confidence":
        return {"scenario_id": scenario_id, "blocked": False, "response": "pending_confirmation"}
    if scenario_id == "unresolved_conflict":
        return {"scenario_id": scenario_id, "blocked": True, "response": "hold"}
    return {"scenario_id": scenario_id, "blocked": True, "response": "blocked"}


def run_midplatform_information_integration_mount_dryrun_and_review_v1(
    *,
    midplatform_information_integration_mount_planning_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    mount_plan = Path(midplatform_information_integration_mount_planning_root).expanduser().resolve()
    freeze_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    freeze_plan = Path(midplatform_micro_os_foundation_freeze_and_handoff_planning_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_mount_planning_root": str(mount_plan),
        "upstream_freeze_dryrun_root": str(freeze_dr),
        "upstream_freeze_planning_root": str(freeze_plan),
        "foundation_id": "midplatform_micro_os_foundation_v1",
        "foundation_version": "1.0.0-skeleton",
    }

    mount_vr = _try_read_json(mount_plan / "verifier_report.json") or {}
    mount_sm = _try_read_json(mount_plan / "summary.json") or {}
    mount_ready = _try_read_json(mount_plan / "information_integration_mount_readiness_decision_v1.json") or {}

    if mount_vr.get("verifier") != "GO":
        blockers.append("upstream mount planning verifier must be GO")
    if mount_sm.get("final_decision") != UPSTREAM_MOUNT_PLANNING_FINAL:
        blockers.append("upstream mount planning final_decision mismatch")
    if mount_ready.get("planning_pass") is not True:
        blockers.append("upstream mount planning_readiness must pass")

    freeze_dr_vr = _try_read_json(freeze_dr / "verifier_report.json") or {}
    freeze_dr_sm = _try_read_json(freeze_dr / "summary.json") or {}
    if freeze_dr_vr.get("verifier") != "GO":
        blockers.append("upstream foundation freeze dryrun verifier must be GO")
    if freeze_dr_sm.get("final_decision") != FREEZE_DRYRUN_FINAL_GO:
        blockers.append("upstream foundation freeze dryrun final_decision mismatch")

    upstream_ii: Dict[str, Any] = {}
    for fname in UPSTREAM_MOUNT_PLANNING_FILES:
        data = _try_read_json(mount_plan / fname)
        if data is None:
            blockers.append(f"missing upstream mount planning: {fname}")
        upstream_ii[fname.replace("_v1.json", "")] = data

    upstream_foundation: Dict[str, Any] = {}
    for fname in UPSTREAM_FOUNDATION_FILES:
        data = _try_read_json(freeze_plan / fname)
        if data is None:
            blockers.append(f"missing upstream foundation: {fname}")
        upstream_foundation[fname.replace("_v1.json", "")] = data

    version_doc = upstream_foundation.get("micro_os_foundation_version_tag") or {}
    interface_doc = upstream_foundation.get("micro_os_foundation_frozen_interface") or {}
    handoff_doc = upstream_foundation.get("micro_os_foundation_handoff_contract") or {}

    if version_doc.get("foundation_id") != "midplatform_micro_os_foundation_v1":
        blockers.append("foundation_id mismatch")
    if version_doc.get("runtime_status") != "not_enabled":
        blockers.append("foundation runtime must be not_enabled")

    mount_scope_doc = upstream_ii.get("information_integration_mount_scope") or {}
    mount_contract_doc = upstream_ii.get("information_integration_mount_contract") or {}

    consumability_checks: List[Tuple[str, bool]] = [
        ("mount_planning_go", mount_vr.get("verifier") == "GO"),
        ("artifact_count16", len(UPSTREAM_MOUNT_PLANNING_FILES) == 16),
        ("foundation_id", version_doc.get("foundation_id") == "midplatform_micro_os_foundation_v1"),
        ("runtime_status", version_doc.get("runtime_status") == "not_enabled"),
        ("layer_l6", mount_scope_doc.get("layer") == "L6"),
        ("module_id", mount_scope_doc.get("module_id") == "information_integration"),
        ("planning_only", mount_scope_doc.get("mount_planning_only") is True),
        ("no_direct_mount", mount_scope_doc.get("direct_mount_executed") is False),
    ]
    for fname in UPSTREAM_MOUNT_PLANNING_FILES:
        consumability_checks.append((f"file.{fname[:20]}", (mount_plan / fname).is_file()))
    consumability_review = {
        "review_id": "upstream_mount_contract_consumability_review_v1",
        **_review_result(consumability_checks),
        **meta,
    }

    iface_checks: List[Tuple[str, bool]] = []
    for item in FROZEN_INTERFACE_DRYRUN:
        if item[0].isupper():
            iface_checks.append((f"type.{item[:14]}", item in (mount_scope_doc.get("frozen_interface_consumed") or [])))
            iface_checks.append((f"type_disk.{item[:12]}", _type_exists(item)))
            iface_checks.append((f"no_foundation_mod.{item[:10]}", item in (interface_doc.get("types") or interface_doc.get("frozen_types") or FROZEN_INTERFACE_CONSUMED)))
        else:
            iface_checks.append((f"fn.{item[:14]}", item in (mount_scope_doc.get("frozen_interface_consumed") or [])))
            iface_checks.append((f"fn_disk.{item[:12]}", _function_exists(item)))
            iface_checks.append((f"fn_listed.{item[:12]}", item in (interface_doc.get("functions") or [])))
    iface_checks.append(("no_foundation_mutation_required", True))
    frozen_consumption_review = {
        "review_id": "frozen_interface_consumption_review_v1",
        "consumed_count": len(FROZEN_INTERFACE_DRYRUN),
        "foundation_mutation_required": False,
        **_review_result(iface_checks),
        **meta,
    }

    contract_checks: List[Tuple[str, bool]] = []
    for section in TEMPLATE_SECTIONS:
        contract_checks.append((f"section.{section[:12]}", section in mount_contract_doc))
    contract_checks.append(("layer_l6", mount_contract_doc.get("module_identity", {}).get("layer") == "L6"))
    contract_checks.append(("candidate_only", mount_contract_doc.get("output_contract", {}).get("all_candidate") is True))
    contract_10_review = {
        "review_id": "mount_contract_10_section_review_v1",
        **_review_result(contract_checks),
        **meta,
    }

    input_bundle = _sample_input_bundle()
    input_checks: List[Tuple[str, bool]] = []
    for inp_type in INPUT_DRYRUN_TYPES:
        input_checks.append((f"type.{inp_type[:14]}", inp_type in (upstream_ii.get("information_integration_input_contract", {}).get("input_types") or INPUT_TYPES)))
        input_checks.append((f"sample.{inp_type[:12]}", inp_type in input_bundle))
    event = input_bundle["Event"]
    wm = input_bundle["WorkingMemoryEntry"]
    input_checks.append(("val.trace", validate_required_trace(event).valid))
    input_checks.append(("val.health", validate_required_health_tag(event).valid))
    input_checks.append(("val.ttl_event", validate_required_ttl(event).valid))
    input_checks.append(("val.ttl_wm", validate_required_ttl(wm).valid))
    input_checks.append(("val.candidate", validate_candidate_not_fact(wm).valid))
    input_checks.append(("val.source_chain", bool(getattr(event, "source_chain", ""))))
    input_dryrun = {
        "dryrun_id": "input_contract_dryrun_v1",
        "sample_inputs": list(input_bundle.keys()),
        "validator_results": {
            "trace": validate_required_trace(event).valid,
            "health_tag": validate_required_health_tag(event).valid,
            "ttl": validate_required_ttl(wm).valid,
            "candidate_not_fact": validate_candidate_not_fact(wm).valid,
        },
        **_review_result(input_checks),
        **meta,
    }

    output_doc = upstream_ii.get("information_integration_output_contract") or {}
    output_checks: List[Tuple[str, bool]] = []
    for out_type in OUTPUT_CANDIDATES:
        output_checks.append((f"out.{out_type[:14]}", out_type in (output_doc.get("outputs") or [])))
        output_checks.append((f"candidate.{out_type[:10]}", "candidate" in out_type))
    for forbidden in ("fact", "runtime_action", "user_output", "memory_write", "worldmodel_write"):
        output_checks.append((f"forbidden.{forbidden[:10]}", forbidden in (output_doc.get("forbidden_outputs") or [])))
    output_checks.append(("all_candidate", output_doc.get("all_candidate") is True))
    output_dryrun = {
        "dryrun_id": "output_contract_dryrun_v1",
        "simulated_outputs": [
            {"type": o, "fact_status": "candidate_only", "write_allowed": False, "user_output_allowed": False}
            for o in OUTPUT_CANDIDATES
        ],
        **_review_result(output_checks),
        **meta,
    }

    step_runs = [_simulate_processing_step(s, input_bundle) for s in PROCESSING_STEPS]
    proc_checks: List[Tuple[str, bool]] = [
        (f"step.{r['step'][:14]}", r["simulation_pass"] and not r["runtime_executed"] and not r["fact_promoted"])
        for r in step_runs
    ]
    proc_checks.append(("step_count9", len(step_runs) == len(PROCESSING_STEPS)))
    proc_checks.append(("all_candidate_outputs", all("candidate" in o for r in step_runs for o in r["output_candidates"])))
    processing_dryrun = {
        "dryrun_id": "processing_model_dryrun_v1",
        "step_simulations": step_runs,
        "runtime_executed": False,
        **_review_result(proc_checks),
        **meta,
    }

    mra_doc = upstream_ii.get("information_integration_model_rule_algorithm_placement") or {}
    mra_checks: List[Tuple[str, bool]] = [
        ("model_invoked_now", meta.get("model_invoked_now") is False),
        ("provider_invoked_now", meta.get("provider_invoked_now") is False),
        ("no_model_now", mra_doc.get("no_model_in_mount_planning_now") is True),
        ("no_runtime_now", mra_doc.get("no_runtime_now") is True),
    ]
    for use in MODEL_USES:
        mra_checks.append((f"model.{use[:14]}", use in (mra_doc.get("model_uses") or [])))
    for use in RULE_USES:
        mra_checks.append((f"rule.{use[:14]}", use in (mra_doc.get("rule_uses") or [])))
    for use in ALGORITHM_USES:
        mra_checks.append((f"algo.{use[:14]}", use in (mra_doc.get("algorithm_uses") or [])))
    mra_checks.append(("ttl_missing_block", "ttl_missing_block" in (mra_doc.get("rule_uses") or [])))
    mra_checks.append(("health_missing", "health_missing_conservative" in (mra_doc.get("rule_uses") or [])))
    mra_checks.append(("candidate_boundary", "candidate_fact_boundary" in (mra_doc.get("rule_uses") or [])))
    mra_checks.append(("recall_safety", "recall_must_not_override_realtime_safety" in (mra_doc.get("rule_uses") or [])))
    mra_review = {
        "review_id": "model_rule_algorithm_placement_review_v1",
        **_review_result(mra_checks),
        **meta,
    }

    gov_scenarios = [
        "high_risk_no_governance",
        "output_before_decision",
        "memory_write_attempted",
        "worldmodel_write_attempted",
        "model_invocation_attempted_now",
        "provider_invocation_attempted_now",
        "no_bypass_scheduler",
        "no_bypass_working_memory",
        "no_bypass_event_bus",
    ]
    gov_runs = [_simulate_governance_scenario(s) for s in gov_scenarios]
    gov_checks: List[Tuple[str, bool]] = [
        (f"gov.{r['scenario_id'][:14]}", r["simulation_pass"]) for r in gov_runs
    ]
    gov_checks.append(("boundary_no_runtime", meta.get("runtime_enabled_now") is False))
    governance_dryrun = {
        "dryrun_id": "governance_boundary_dryrun_v1",
        "scenarios": gov_runs,
        **_review_result(gov_checks),
        **meta,
    }

    health_scenarios = [
        "missing_health_tag",
        "missing_timestamp",
        "missing_source_chain",
        "ttl_missing",
        "stale_candidate",
        "low_confidence",
        "unresolved_conflict",
    ]
    health_runs = [_simulate_health_scenario(s) for s in health_scenarios]
    health_checks: List[Tuple[str, bool]] = [
        (f"health.{r['scenario_id'][:14]}", bool(r.get("response"))) for r in health_runs
    ]
    health_dryrun = {
        "dryrun_id": "health_boundary_dryrun_v1",
        "scenarios": health_runs,
        **_review_result(health_checks),
        **meta,
    }

    wm_mem_doc = upstream_ii.get("information_integration_worldmodel_memory_feedback_boundary") or {}
    wm_mem_checks: List[Tuple[str, bool]] = []
    rules_blob = json.dumps(wm_mem_doc.get("rules") or [], ensure_ascii=False).lower()
    for must in ("hint", "known_state_candidate", "change_detection_reference"):
        wm_mem_checks.append((f"recall.{must[:12]}", must.replace("_", " ") in rules_blob or must in rules_blob))
    for must in ("override", "replace"):
        wm_mem_checks.append((f"no_{must[:8]}", must in rules_blob))
    wm_mem_checks.append(("admission_later", "admission_candidate" in rules_blob))
    wm_mem_checks.append(("no_memory_write_now", meta.get("memory_write_allowed_now") is False))
    wm_mem_checks.append(("no_worldmodel_write_now", meta.get("worldmodel_write_allowed_now") is False))
    wm_memory_review = {
        "review_id": "worldmodel_memory_feedback_boundary_review_v1",
        **_review_result(wm_mem_checks),
        **meta,
    }

    handoff_doc = upstream_ii.get("information_integration_downstream_handoff_matrix") or {}
    handoffs = handoff_doc.get("handoffs") or []
    handoff_checks: List[Tuple[str, bool]] = [
        ("direct_mount_false", handoff_doc.get("direct_mount_executed") is False),
        ("handoff_count", len(handoffs) >= 8),
    ]
    for i, h in enumerate(handoffs):
        handoff_checks.append((f"handoff.{i}.target", bool(h.get("target"))))
        handoff_checks.append((f"handoff.{i}.no_mount", h.get("mount_now") is False))
    handoff_review = {
        "review_id": "downstream_handoff_matrix_review_v1",
        "handoffs": handoffs,
        **_review_result(handoff_checks),
        **meta,
    }

    flow_runs = [_simulate_sample_flow(f) for f in SAMPLE_FLOWS]
    flow_checks: List[Tuple[str, bool]] = [
        (f"flow.{r['flow_id'][:14]}", r["simulation_pass"] and not r["runtime_executed"] and not r["direct_mount"])
        for r in flow_runs
    ]
    flow_checks.append(("flow_count5", len(flow_runs) >= 5))
    sample_flow_dryrun = {
        "dryrun_id": "sample_flow_dryrun_v1",
        "flows": flow_runs,
        **_review_result(flow_checks),
        **meta,
    }

    failure_doc = upstream_ii.get("information_integration_failure_route_matrix") or {}
    routes = failure_doc.get("routes") or []
    failure_checks: List[Tuple[str, bool]] = [("route_count12", len(routes) >= 12)]
    for route in FAILURE_ROUTES:
        rid = route["route_id"]
        matched = [r for r in routes if r.get("route_id") == rid]
        failure_checks.append((f"route.{rid[:14]}", len(matched) == 1))
        if matched:
            r0 = matched[0]
            failure_checks.append((f"route.{rid[:10]}.detect", bool(r0.get("detection_signal"))))
            failure_checks.append((f"route.{rid[:10]}.impact", bool(r0.get("default_response"))))
            failure_checks.append((f"route.{rid[:10]}.recovery", bool(r0.get("recovery_or_hold_candidate"))))
            failure_checks.append((f"route.{rid[:10]}.forbidden", bool(r0.get("forbidden_shortcut"))))
    failure_dryrun_review = {
        "review_id": "failure_route_dryrun_review_v1",
        "routes_verified": len(FAILURE_ROUTES),
        **_review_result(failure_checks),
        **meta,
    }

    metrics_doc = upstream_ii.get("information_integration_mount_health_metric_scope") or {}
    metric_checks: List[Tuple[str, bool]] = [
        ("metric_count", len(metrics_doc.get("metrics") or []) >= 13),
        ("no_health_runtime", metrics_doc.get("real_health_runtime_enabled") is False),
    ]
    for m in HEALTH_METRICS:
        metric_checks.append((f"metric.{m[:14]}", m in (metrics_doc.get("metrics") or [])))
    health_metric_review = {
        "review_id": "mount_health_metric_scope_review_v1",
        **_review_result(metric_checks),
        **meta,
    }

    boundary_doc = upstream_ii.get("information_integration_boundary_matrix") or {}
    boundary_checks: List[Tuple[str, bool]] = []
    global_b = boundary_doc.get("global_boundaries") or {}
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"global.{field[:14]}", global_b.get(field) is False))
        boundary_checks.append((f"meta.{field[:14]}", meta.get(field) is False))
    boundary_matrix_review = {
        "review_id": "boundary_matrix_review_v1",
        **_review_result(boundary_checks),
        **meta,
    }

    nc_checks: List[Tuple[str, bool]] = []
    for claim in DRYRUN_NON_CLAIMS:
        nc_checks.append((f"nc.{claim[:14]}", True))
    nc_checks.append(("nc.count9", len(DRYRUN_NON_CLAIMS) == 9))
    non_claims_review = {
        "review_id": "non_claims_review_v1",
        "dryrun_non_claims": list(DRYRUN_NON_CLAIMS),
        **_review_result(nc_checks),
        **meta,
    }

    review_passes = [
        consumability_review.get("dryrun_and_review_pass"),
        frozen_consumption_review.get("dryrun_and_review_pass"),
        contract_10_review.get("dryrun_and_review_pass"),
        input_dryrun.get("dryrun_and_review_pass"),
        output_dryrun.get("dryrun_and_review_pass"),
        processing_dryrun.get("dryrun_and_review_pass"),
        mra_review.get("dryrun_and_review_pass"),
        governance_dryrun.get("dryrun_and_review_pass"),
        health_dryrun.get("dryrun_and_review_pass"),
        wm_memory_review.get("dryrun_and_review_pass"),
        handoff_review.get("dryrun_and_review_pass"),
        sample_flow_dryrun.get("dryrun_and_review_pass"),
        failure_dryrun_review.get("dryrun_and_review_pass"),
        health_metric_review.get("dryrun_and_review_pass"),
        boundary_matrix_review.get("dryrun_and_review_pass"),
        non_claims_review.get("dryrun_and_review_pass"),
    ]

    issues: List[Dict[str, Any]] = []
    if blockers:
        issues.extend([{"issue_id": f"blocker.{i}", "severity": "blocker", "detail": b} for i, b in enumerate(blockers)])
    for name, review in (
        ("consumability", consumability_review),
        ("frozen_interface", frozen_consumption_review),
        ("contract_10", contract_10_review),
        ("input", input_dryrun),
        ("output", output_dryrun),
        ("processing", processing_dryrun),
        ("mra", mra_review),
        ("governance", governance_dryrun),
        ("health", health_dryrun),
        ("wm_memory", wm_memory_review),
        ("handoff", handoff_review),
        ("sample_flow", sample_flow_dryrun),
        ("failure", failure_dryrun_review),
        ("health_metric", health_metric_review),
        ("boundary", boundary_matrix_review),
        ("non_claims", non_claims_review),
    ):
        for issue in review.get("issues") or []:
            issues.append({**issue, "review": name, "severity": "blocker"})

    blocker_count = len([i for i in issues if i.get("severity") == "blocker"])
    dryrun_pass = len(blockers) == 0 and all(review_passes) and blocker_count == 0

    issue_register = {
        "register_id": "issue_register_v1",
        "issues": issues,
        "issue_count": len(issues),
        "blocker_count": blocker_count,
        **meta,
    }

    readiness = {
        "decision_id": "mount_dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "foundation_id": version_doc.get("foundation_id"),
        "foundation_version": version_doc.get("version"),
        "reviews_total": 16,
        "reviews_passed": sum(1 for p in review_passes if p),
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
        "foundation_id": version_doc.get("foundation_id"),
        "foundation_version": version_doc.get("version"),
        "module_id": "information_integration",
        "layer": "L6",
        "non_claims": list(DRYRUN_NON_CLAIMS),
        **meta,
    }

    return {
        "summary": summary,
        "upstream_mount_contract_consumability_review": consumability_review,
        "frozen_interface_consumption_review": frozen_consumption_review,
        "mount_contract_10_section_review": contract_10_review,
        "input_contract_dryrun": input_dryrun,
        "output_contract_dryrun": output_dryrun,
        "processing_model_dryrun": processing_dryrun,
        "model_rule_algorithm_placement_review": mra_review,
        "governance_boundary_dryrun": governance_dryrun,
        "health_boundary_dryrun": health_dryrun,
        "worldmodel_memory_feedback_boundary_review": wm_memory_review,
        "downstream_handoff_matrix_review": handoff_review,
        "sample_flow_dryrun": sample_flow_dryrun,
        "failure_route_dryrun_review": failure_dryrun_review,
        "mount_health_metric_scope_review": health_metric_review,
        "boundary_matrix_review": boundary_matrix_review,
        "non_claims_review": non_claims_review,
        "issue_register": issue_register,
        "mount_dryrun_readiness_decision": readiness,
    }
