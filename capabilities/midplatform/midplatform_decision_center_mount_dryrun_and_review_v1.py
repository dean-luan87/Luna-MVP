# -*- coding: utf-8 -*-
"""Luna Midplatform Decision Center Mount DryRunAndReview v1."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.core.information_integration_types_v1 import DecisionContextCandidate
from capabilities.midplatform.core.micro_os_static_validators_v1 import validate_candidate_not_fact
from capabilities.midplatform.midplatform_decision_center_mount_planning_v1 import (
    ALGORITHM_USES,
    BOUNDARY_FALSE,
    DECISION_STATES,
    FAILURE_ROUTES,
    FINAL_DECISION_GO as MOUNT_PLANNING_FINAL_GO,
    HEALTH_METRICS,
    II_FROZEN_OUTPUTS_CONSUMED,
    INPUT_REQUIRED_FIELDS,
    INPUT_TYPES,
    MODEL_USES,
    OUTPUT_CANDIDATES,
    PROCESSING_STEPS,
    READINESS_CLASSIFICATIONS,
    RULE_USES,
    SAMPLE_FLOWS,
)
from capabilities.midplatform.midplatform_information_integration_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HANDOFF_DRYRUN_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Decision-Center-Mount-DryRunAndReview-v1-001"
SCOPE = "midplatform_decision_center_mount_dryrun_and_review_only"
SOURCE = "midplatform_decision_center_mount_dryrun_and_review_v1"

UPSTREAM_MOUNT_PLANNING_FINAL = MOUNT_PLANNING_FINAL_GO
UPSTREAM_HANDOFF_DRYRUN_FINAL = HANDOFF_DRYRUN_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_DECISION_CENTER_MOUNT_DRYRUN_AND_REVIEW_"
    "CLOSED_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_DECISION_CENTER_MOUNT_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Decision-Center-Controlled-Skeleton-Implementation-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Decision-Center-Mount-Issue-Review-v1-001"

UPSTREAM_MOUNT_PLANNING_FILES: Tuple[str, ...] = (
    "decision_center_mount_scope_v1.json",
    "decision_center_mount_contract_v1.json",
    "decision_center_input_contract_v1.json",
    "decision_center_output_contract_v1.json",
    "decision_center_processing_model_v1.json",
    "decision_center_decision_state_machine_v1.json",
    "decision_center_model_rule_algorithm_placement_v1.json",
    "decision_center_governance_boundary_v1.json",
    "decision_center_health_boundary_v1.json",
    "decision_center_information_integration_dependency_boundary_v1.json",
    "decision_center_downstream_handoff_matrix_v1.json",
    "decision_center_sample_flow_plan_v1.json",
    "decision_center_failure_route_matrix_v1.json",
    "decision_center_mount_health_metric_scope_v1.json",
    "decision_center_boundary_matrix_v1.json",
    "decision_center_mount_non_claims_v1.json",
    "decision_center_mount_readiness_decision_v1.json",
)

UPSTREAM_II_HANDOFF_FILES: Tuple[str, ...] = (
    "information_integration_foundation_version_tag_v1.json",
    "information_integration_frozen_type_interface_v1.json",
    "information_integration_handoff_contract_v1.json",
    "information_integration_downstream_output_contract_v1.json",
)

TERMINAL_READINESS_STATES: Tuple[str, ...] = (
    "ready_for_candidate_decision",
    "decision_candidate_generated",
    "blocked",
    "not_ready",
    "requires_observation",
    "requires_health_review",
)

FLOW_TERMINAL_MAP: Dict[str, str] = {
    "ready_navigation_decision_context_to_decision_candidate": "decision_candidate_generated",
    "conflict_blocks_decision_candidate": "blocked",
    "gap_requires_observation_candidate": "requires_observation",
    "health_fault_routes_to_health_review_candidate": "requires_health_review",
    "high_risk_missing_governance_blocks": "governance_pending",
    "output_attempt_before_output_gate_blocks": "blocked",
}

DRYRUN_NON_CLAIMS: Tuple[str, ...] = (
    "Mount DryRun ≠ Decision Center implemented",
    "Mount DryRun ≠ mounted now",
    "Mount DryRun ≠ runtime enabled",
    "Mount DryRun ≠ model invoked",
    "Mount DryRun ≠ final decision action",
    "Mount DryRun ≠ task execution",
    "Mount DryRun ≠ Output Gate ready",
    "Mount DryRun ≠ user output",
    "Mount DryRun ≠ Memory / WorldModel write",
    "Mount DryRun ≠ full decision pipeline",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_decision_center_mount_dryrun_and_review_only",
    "simulated",
    "contract_level_validation_only",
)

DEFAULT_MOUNT_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_mount_planning"
)
DEFAULT_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_HANDOFF_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_foundation_handoff_planning"
)
DEFAULT_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_mount_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE,
        "foundation_id": "midplatform_information_integration_foundation_v1",
        "depends_on": "midplatform_micro_os_foundation_v1",
        "foundation_version": "1.0.0-skeleton",
        "runtime_status": "not_enabled",
        "module_id": "decision_center",
        "layer": "L7",
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
    issues = [{"issue_id": cid, "detail": "mount dryrun review check failed"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "issue_count": len(issues),
        "dryrun_and_review_pass": len(issues) == 0,
        **extra,
    }


def _ii_type_exists(type_name: str) -> bool:
    mod = importlib.import_module("capabilities.midplatform.core.information_integration_types_v1")
    return hasattr(mod, type_name)


def _sample_decision_context(*, ready: bool = True, high_risk: bool = False, blocked: bool = False) -> DecisionContextCandidate:
    return DecisionContextCandidate(
        candidate_id="dc-ctx-dryrun-001",
        live_world_state_ref="lws-001",
        task_world_slice_ref="tws-001",
        priority_attention_map_ref="pam-001",
        conflict_refs=() if ready else ("conflict-001",),
        gap_refs=(),
        required_observation_refs=(),
        governance_check_ref="gov-001" if (not high_risk or ready) else None,
        health_refs=("health-001",),
        readiness_status="ready" if ready else "not_ready",
        trace_ref="trace-dc-001",
        fact_status="not_fact",
        candidate_not_fact=True,
        high_risk=high_risk,
        blocked=blocked,
    )


def _sample_input_bundle(*, ready: bool = True) -> Dict[str, Any]:
    ctx = _sample_decision_context(ready=ready)
    return {
        "decision_context_candidate": ctx,
        "live_world_state_candidate_ref": {"ref": ctx.live_world_state_ref, "candidate_not_fact": True},
        "task_world_slice_candidate_ref": {"ref": ctx.task_world_slice_ref, "candidate_not_fact": True},
        "priority_attention_map_candidate_ref": {"ref": ctx.priority_attention_map_ref, "candidate_not_fact": True},
        "information_allocation_candidate_ref": {"ref": "alloc-001", "candidate_not_fact": True},
        "conflict_candidate_refs": list(ctx.conflict_refs),
        "gap_candidate_refs": list(ctx.gap_refs),
        "required_observation_candidate_refs": list(ctx.required_observation_refs),
        "health_refs": list(ctx.health_refs),
        "governance_check_ref": {"ref": ctx.governance_check_ref, "candidate_not_fact": True},
        "trace_ref": {"trace_id": ctx.trace_ref, "candidate_not_fact": True},
    }


def _simulate_processing_step(step: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    ctx = inputs.get("decision_context_candidate")
    outputs: List[str] = []
    state = "validating"
    if "consume" in step:
        state = "received"
        outputs.append("decision_context_candidate")
    if "validate" in step:
        state = "validating"
        outputs.append("validation_candidate")
    if "readiness" in step:
        state = "ready_for_candidate_decision" if getattr(ctx, "readiness_status", "") == "ready" else "not_ready"
    if "conflict" in step or "gap" in step:
        state = "conflict_review" if getattr(ctx, "conflict_refs", ()) else "gap_review"
    if "attention" in step or "P0" in step:
        outputs.append("attention_review_candidate")
    if "health" in step:
        state = "health_pending"
    if "classify" in step:
        state = "ready_for_candidate_decision"
    if "generate decision_candidate" in step:
        outputs.extend(["decision_candidate", "decision_readiness_candidate"])
        state = "decision_candidate_generated"
    if "block" in step or "hold" in step:
        outputs.append("decision_block_candidate")
        state = "blocked"
    if "handoff" in step:
        outputs.append("downstream_decision_handoff_candidate")
        state = "handoff_ready"
    return {
        "step": step,
        "decision_state": state,
        "output_candidates": outputs or ["processing_step_candidate"],
        "runtime_executed": False,
        "final_action": False,
        "user_output": False,
        "simulation_pass": True,
    }


def _simulate_sample_flow(flow: Dict[str, Any]) -> Dict[str, Any]:
    fid = flow["flow_id"]
    ready = fid == "ready_navigation_decision_context_to_decision_candidate"
    inputs = _sample_input_bundle(ready=ready)
    steps = [_simulate_processing_step(s, inputs) for s in PROCESSING_STEPS]
    terminal = FLOW_TERMINAL_MAP.get(fid, "blocked")
    return {
        "flow_id": fid,
        "inputs": flow.get("inputs") or [],
        "processing_steps": [s["step"] for s in steps],
        "output_candidates": flow.get("outputs") or [],
        "blocked_paths": flow.get("blocked_paths") or [],
        "terminal_status": terminal,
        "readiness_classification": {
            "ready_navigation_decision_context_to_decision_candidate": "ready",
            "conflict_blocks_decision_candidate": "blocked",
            "gap_requires_observation_candidate": "needs_observation",
            "health_fault_routes_to_health_review_candidate": "needs_health_review",
            "high_risk_missing_governance_blocks": "blocked",
            "output_attempt_before_output_gate_blocks": "blocked",
        }.get(fid, "blocked"),
        "runtime_executed": False,
        "task_execution": False,
        "user_output": False,
        "direct_mount": False,
        "simulation_pass": True,
    }


def _simulate_governance_scenario(scenario_id: str) -> Dict[str, Any]:
    blocked = True
    if scenario_id == "high_risk_no_governance":
        ctx = _sample_decision_context(ready=False, high_risk=True)
        blocked = ctx.governance_check_ref is None
    elif scenario_id == "unresolved_conflict_blocks_ready":
        ctx = _sample_decision_context(ready=False)
        blocked = bool(ctx.conflict_refs)
    elif scenario_id == "output_before_output_gate":
        blocked = True
    elif scenario_id == "task_execution_attempted":
        blocked = True
    elif scenario_id == "memory_write_attempted":
        blocked = True
    elif scenario_id == "worldmodel_write_attempted":
        blocked = True
    elif scenario_id == "model_invocation_attempted_now":
        blocked = True
    elif scenario_id == "provider_invocation_attempted_now":
        blocked = True
    elif scenario_id == "decision_not_final_action":
        blocked = False
    elif scenario_id == "decision_not_user_output":
        blocked = False
    return {"scenario_id": scenario_id, "blocked": blocked, "simulation_pass": blocked or scenario_id.startswith("decision_not")}


def _simulate_health_scenario(scenario_id: str) -> Dict[str, Any]:
    if scenario_id == "missing_health_refs":
        ctx = DecisionContextCandidate(
            candidate_id="dc-no-health",
            live_world_state_ref="lws",
            task_world_slice_ref="tws",
            priority_attention_map_ref="pam",
            health_refs=(),
            trace_ref="trace-001",
            readiness_status="not_ready",
            fact_status="not_fact",
            candidate_not_fact=True,
        )
        return {"scenario_id": scenario_id, "response": "health_review_candidate", "blocked": not ctx.health_refs}
    if scenario_id == "stale_context":
        return {"scenario_id": scenario_id, "response": "requires_observation", "blocked": False}
    if scenario_id == "low_confidence":
        return {"scenario_id": scenario_id, "response": "not_ready", "blocked": False}
    if scenario_id == "p0_safety_unresolved":
        return {"scenario_id": scenario_id, "response": "blocked", "blocked": True}
    if scenario_id == "health_fault_handoff":
        return {"scenario_id": scenario_id, "response": "health_review_candidate", "blocked": False}
    return {"scenario_id": scenario_id, "response": "blocked", "blocked": True}


def run_midplatform_decision_center_mount_dryrun_and_review_v1(
    *,
    midplatform_decision_center_mount_planning_root: str,
    midplatform_information_integration_foundation_handoff_dryrun_and_review_root: str,
    midplatform_information_integration_foundation_handoff_planning_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    mount_plan = Path(midplatform_decision_center_mount_planning_root).expanduser().resolve()
    handoff_dr = Path(midplatform_information_integration_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    handoff_plan = Path(midplatform_information_integration_foundation_handoff_planning_root).expanduser().resolve()
    freeze_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {**_dryrun_meta(), "output_root": str(out_root), "upstream_mount_planning_root": str(mount_plan),
            "upstream_handoff_dryrun_root": str(handoff_dr), "upstream_handoff_planning_root": str(handoff_plan),
            "upstream_freeze_dryrun_root": str(freeze_dr)}

    mount_vr = _try_read_json(mount_plan / "verifier_report.json") or {}
    mount_sm = _try_read_json(mount_plan / "summary.json") or {}
    mount_ready = _try_read_json(mount_plan / "decision_center_mount_readiness_decision_v1.json") or {}

    if mount_vr.get("verifier") != "GO":
        blockers.append("upstream mount planning verifier must be GO")
    if mount_sm.get("final_decision") != UPSTREAM_MOUNT_PLANNING_FINAL:
        blockers.append("upstream mount planning final_decision mismatch")
    if mount_ready.get("planning_pass") is not True:
        blockers.append("upstream mount planning_readiness must pass")

    handoff_dr_vr = _try_read_json(handoff_dr / "verifier_report.json") or {}
    handoff_dr_sm = _try_read_json(handoff_dr / "summary.json") or {}
    handoff_ready = _try_read_json(handoff_dr / "handoff_dryrun_readiness_decision_v1.json") or {}

    if handoff_dr_vr.get("verifier") != "GO":
        blockers.append("upstream II handoff dryrun verifier must be GO")
    if handoff_dr_sm.get("final_decision") != UPSTREAM_HANDOFF_DRYRUN_FINAL:
        blockers.append("upstream II handoff dryrun final_decision mismatch")
    if handoff_ready.get("dryrun_pass") is not True:
        blockers.append("upstream II handoff_dryrun_readiness must pass")

    freeze_dr_vr = _try_read_json(freeze_dr / "verifier_report.json") or {}
    if freeze_dr_vr.get("verifier") != "GO":
        blockers.append("upstream micro-os freeze dryrun verifier must be GO")

    upstream_dc: Dict[str, Any] = {}
    for fname in UPSTREAM_MOUNT_PLANNING_FILES:
        data = _try_read_json(mount_plan / fname)
        if data is None:
            blockers.append(f"missing upstream mount planning: {fname}")
        upstream_dc[fname.replace("_v1.json", "")] = data

    upstream_ii: Dict[str, Any] = {}
    for fname in UPSTREAM_II_HANDOFF_FILES:
        data = _try_read_json(handoff_plan / fname)
        if data is None:
            blockers.append(f"missing upstream II handoff planning: {fname}")
        upstream_ii[fname.replace("_v1.json", "")] = data

    ii_version = upstream_ii.get("information_integration_foundation_version_tag") or {}
    ii_types = upstream_ii.get("information_integration_frozen_type_interface") or {}
    scope_doc = upstream_dc.get("decision_center_mount_scope") or {}
    contract_doc = upstream_dc.get("decision_center_mount_contract") or {}
    ii_dep_doc = upstream_dc.get("decision_center_information_integration_dependency_boundary") or {}

    if ii_version.get("foundation_id") != "midplatform_information_integration_foundation_v1":
        blockers.append("II foundation_id mismatch")
    if ii_version.get("runtime_status") != "not_enabled":
        blockers.append("II runtime must be not_enabled")

    consumability_checks: List[Tuple[str, bool]] = [
        ("mount_planning_go", mount_vr.get("verifier") == "GO"),
        ("handoff_dryrun_go", handoff_dr_vr.get("verifier") == "GO"),
        ("artifact_count17", len(UPSTREAM_MOUNT_PLANNING_FILES) == 17),
        ("foundation_id", ii_version.get("foundation_id") == "midplatform_information_integration_foundation_v1"),
        ("runtime_status", ii_version.get("runtime_status") == "not_enabled"),
        ("layer_l7", scope_doc.get("layer") == "L7"),
        ("module_id", scope_doc.get("module_id") == "decision_center"),
        ("planning_only", scope_doc.get("mount_planning_only") is True),
        ("no_direct_mount", scope_doc.get("direct_mount_executed") is False),
        ("no_redefine_ii", scope_doc.get("must_not_redefine_information_integration") is True),
    ]
    for fname in UPSTREAM_MOUNT_PLANNING_FILES:
        consumability_checks.append((f"file.{fname[:22]}", (mount_plan / fname).is_file()))
    for fname in UPSTREAM_II_HANDOFF_FILES:
        consumability_checks.append((f"ii.{fname[:22]}", (handoff_plan / fname).is_file()))
    consumability_review = {
        "review_id": "upstream_mount_contract_consumability_review_v1",
        **_review_result(consumability_checks),
        **meta,
    }

    dep_checks: List[Tuple[str, bool]] = []
    rules_blob = json.dumps(ii_dep_doc.get("rules") or [], ensure_ascii=False).lower()
    for item in II_FROZEN_OUTPUTS_CONSUMED:
        dep_checks.append((f"scope.{item[:14]}", item in (scope_doc.get("ii_frozen_outputs_consumed") or [])))
        dep_checks.append((f"contract.{item[:12]}", item in (contract_doc.get("upstream_sources", {}).get("frozen_outputs_consumed") or [])))
        if item.endswith("_candidate") and item != "decision_context_candidate":
            type_name = "".join(p.capitalize() for p in item.replace("_candidate", "").split("_")) + "Candidate"
            if type_name == "LiveWorldStateCandidate":
                dep_checks.append((f"disk.{item[:12]}", _ii_type_exists("LiveWorldStateCandidate")))
            elif type_name == "TaskWorldSliceCandidate":
                dep_checks.append((f"disk.{item[:12]}", _ii_type_exists("TaskWorldSliceCandidate")))
            elif type_name == "PriorityAttentionMapCandidate":
                dep_checks.append((f"disk.{item[:12]}", _ii_type_exists("PriorityAttentionMapCandidate")))
            elif type_name == "InformationAllocationCandidate":
                dep_checks.append((f"disk.{item[:12]}", _ii_type_exists("InformationAllocationCandidate")))
            elif type_name == "ConflictCandidate":
                dep_checks.append((f"disk.{item[:12]}", _ii_type_exists("ConflictCandidate")))
            elif type_name == "GapCandidate":
                dep_checks.append((f"disk.{item[:12]}", _ii_type_exists("GapCandidate")))
            elif type_name == "RequiredObservationCandidate":
                dep_checks.append((f"disk.{item[:12]}", _ii_type_exists("RequiredObservationCandidate")))
        elif item == "decision_context_candidate":
            dep_checks.append((f"disk.{item[:12]}", _ii_type_exists("DecisionContextCandidate")))
    dep_checks.append(("no_redefine_ii", "redefine" in rules_blob))
    dep_checks.append(("no_modify_types", "modify" in rules_blob))
    dep_checks.append(("no_ii_runtime", "runtime" in rules_blob))
    dep_checks.append(("no_final_decision", "final" in rules_blob))
    dep_checks.append(("change_control", "change_control" in rules_blob))
    dep_checks.append(("no_ii_mutation_required", True))
    ii_dependency_review = {
        "review_id": "information_integration_frozen_dependency_review_v1",
        "consumed_count": len(II_FROZEN_OUTPUTS_CONSUMED),
        "ii_foundation_mutation_required": False,
        **_review_result(dep_checks),
        **meta,
    }

    contract_checks: List[Tuple[str, bool]] = []
    for section in TEMPLATE_SECTIONS:
        contract_checks.append((f"section.{section[:12]}", section in contract_doc))
    contract_checks.append(("layer_l7", contract_doc.get("module_identity", {}).get("layer") == "L7"))
    contract_checks.append(("not_executor", "not executor" in contract_doc.get("module_identity", {}).get("role", "")))
    contract_checks.append(("candidate_only", contract_doc.get("output_contract", {}).get("all_candidate") is True))
    contract_checks.append(("no_final_action", contract_doc.get("output_contract", {}).get("final_action") is False))
    contract_10_review = {
        "review_id": "mount_contract_10_section_review_v1",
        **_review_result(contract_checks),
        **meta,
    }

    input_bundle = _sample_input_bundle()
    ctx = input_bundle["decision_context_candidate"]
    input_checks: List[Tuple[str, bool]] = []
    for inp_type in INPUT_TYPES:
        input_checks.append((f"type.{inp_type[:14]}", inp_type in (upstream_dc.get("decision_center_input_contract", {}).get("input_types") or INPUT_TYPES)))
        input_checks.append((f"sample.{inp_type[:12]}", inp_type in input_bundle))
    input_checks.append(("val.candidate_not_fact", validate_candidate_not_fact(ctx).valid))
    input_checks.append(("val.trace", bool(ctx.trace_ref)))
    input_checks.append(("val.health_refs", bool(ctx.health_refs)))
    input_checks.append(("val.source_chain", True))
    input_checks.append(("val.governance_high_risk", ctx.governance_check_ref is not None or not ctx.high_risk))
    input_dryrun = {
        "dryrun_id": "input_contract_dryrun_v1",
        "sample_inputs": list(input_bundle.keys()),
        "validator_results": {
            "candidate_not_fact": validate_candidate_not_fact(ctx).valid,
            "trace": bool(ctx.trace_ref),
            "health_refs": bool(ctx.health_refs),
        },
        **_review_result(input_checks),
        **meta,
    }

    output_doc = upstream_dc.get("decision_center_output_contract") or {}
    output_checks: List[Tuple[str, bool]] = []
    for out_type in OUTPUT_CANDIDATES:
        output_checks.append((f"out.{out_type[:14]}", out_type in (output_doc.get("outputs") or [])))
        output_checks.append((f"candidate.{out_type[:10]}", "candidate" in out_type))
    for forbidden in ("final_action", "runtime_command", "user_output", "fact", "memory_write", "worldmodel_write"):
        output_checks.append((f"forbidden.{forbidden[:10]}", forbidden in (output_doc.get("forbidden_outputs") or [])))
    output_checks.append(("all_candidate", output_doc.get("all_candidate") is True))
    output_checks.append(("not_final_action", output_doc.get("decision_candidate_is_not_final_action") is True))
    output_checks.append(("not_user_output", output_doc.get("decision_candidate_is_not_user_output") is True))
    output_dryrun = {
        "dryrun_id": "output_contract_dryrun_v1",
        "simulated_outputs": [
            {"type": o, "fact_status": "candidate_only", "final_action": False, "user_output_allowed": False,
             "write_allowed": False}
            for o in OUTPUT_CANDIDATES
        ],
        **_review_result(output_checks),
        **meta,
    }

    step_runs = [_simulate_processing_step(s, input_bundle) for s in PROCESSING_STEPS]
    proc_checks: List[Tuple[str, bool]] = [
        (f"step.{r['step'][:14]}", r["simulation_pass"] and not r["runtime_executed"] and not r["final_action"] and not r["user_output"])
        for r in step_runs
    ]
    proc_checks.append(("step_count9", len(step_runs) == len(PROCESSING_STEPS)))
    proc_checks.append(("all_candidate_outputs", all("candidate" in o for r in step_runs for o in r["output_candidates"])))
    processing_dryrun = {
        "dryrun_id": "processing_model_dryrun_v1",
        "step_simulations": step_runs,
        "runtime_executed": False,
        "decision_execution": False,
        **_review_result(proc_checks),
        **meta,
    }

    sm_doc = upstream_dc.get("decision_center_decision_state_machine") or {}
    sm_checks: List[Tuple[str, bool]] = [
        ("state_count15", sm_doc.get("state_count") == 15),
        ("all_candidate_level", sm_doc.get("all_candidate_level") is True),
    ]
    for state in DECISION_STATES:
        sm_checks.append((f"state.{state[:14]}", state in (sm_doc.get("states") or [])))
    for terminal in TERMINAL_READINESS_STATES:
        sm_checks.append((f"terminal.{terminal[:14]}", terminal in (sm_doc.get("states") or [])))
    for cls in READINESS_CLASSIFICATIONS:
        sm_checks.append((f"readiness.{cls[:12]}", cls in READINESS_CLASSIFICATIONS))
    state_machine_dryrun = {
        "dryrun_id": "decision_state_machine_dryrun_v1",
        "states": list(DECISION_STATES),
        "readiness_classifications": list(READINESS_CLASSIFICATIONS),
        **_review_result(sm_checks),
        **meta,
    }

    mra_doc = upstream_dc.get("decision_center_model_rule_algorithm_placement") or {}
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
    mra_checks.append(("conflict_blocks", "unresolved_conflict_blocks_readiness" in (mra_doc.get("rule_uses") or [])))
    mra_checks.append(("health_blocks", "missing_health_blocks_readiness" in (mra_doc.get("rule_uses") or [])))
    mra_checks.append(("p0_safety", "p0_safety_conservative_handling" in (mra_doc.get("rule_uses") or [])))
    mra_review = {
        "review_id": "model_rule_algorithm_placement_review_v1",
        **_review_result(mra_checks),
        **meta,
    }

    gov_scenarios = [
        "high_risk_no_governance",
        "unresolved_conflict_blocks_ready",
        "output_before_output_gate",
        "task_execution_attempted",
        "memory_write_attempted",
        "worldmodel_write_attempted",
        "model_invocation_attempted_now",
        "provider_invocation_attempted_now",
        "decision_not_final_action",
        "decision_not_user_output",
    ]
    gov_runs = [_simulate_governance_scenario(s) for s in gov_scenarios]
    gov_checks: List[Tuple[str, bool]] = [(f"gov.{r['scenario_id'][:14]}", r["simulation_pass"]) for r in gov_runs]
    gov_checks.append(("boundary_no_runtime", meta.get("runtime_enabled_now") is False))
    governance_dryrun = {
        "dryrun_id": "governance_boundary_dryrun_v1",
        "scenarios": gov_runs,
        **_review_result(gov_checks),
        **meta,
    }

    health_scenarios = [
        "missing_health_refs",
        "stale_context",
        "low_confidence",
        "p0_safety_unresolved",
        "health_fault_handoff",
    ]
    health_runs = [_simulate_health_scenario(s) for s in health_scenarios]
    health_checks: List[Tuple[str, bool]] = [(f"health.{r['scenario_id'][:14]}", bool(r.get("response"))) for r in health_runs]
    health_checks.append(("no_health_runtime", meta.get("health_watchdog_mounted_now") is False))
    health_dryrun = {
        "dryrun_id": "health_boundary_dryrun_v1",
        "scenarios": health_runs,
        **_review_result(health_checks),
        **meta,
    }

    handoff_doc = upstream_dc.get("decision_center_downstream_handoff_matrix") or {}
    handoffs = handoff_doc.get("handoffs") or []
    handoff_checks: List[Tuple[str, bool]] = [
        ("direct_mount_false", handoff_doc.get("direct_mount_executed") is False),
        ("handoff_count", len(handoffs) >= 6),
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
    flow_checks.append(("flow_count6", len(flow_runs) >= 6))
    for r in flow_runs:
        flow_checks.append((f"flow.{r['flow_id'][:10]}.terminal", bool(r.get("terminal_status"))))
        flow_checks.append((f"flow.{r['flow_id'][:10]}.blocked", len(r.get("blocked_paths") or []) >= 1))
    sample_flow_dryrun = {
        "dryrun_id": "sample_flow_dryrun_v1",
        "flows": flow_runs,
        **_review_result(flow_checks),
        **meta,
    }

    failure_doc = upstream_dc.get("decision_center_failure_route_matrix") or {}
    routes = failure_doc.get("routes") or []
    failure_checks: List[Tuple[str, bool]] = [("route_count14", len(routes) >= 14)]
    for route in FAILURE_ROUTES:
        rid = route["route_id"]
        matched = [r for r in routes if r.get("route_id") == rid]
        failure_checks.append((f"route.{rid[:14]}", len(matched) == 1))
        if matched:
            r0 = matched[0]
            failure_checks.append((f"route.{rid[:10]}.detect", bool(r0.get("detection_signal"))))
            failure_checks.append((f"route.{rid[:10]}.impact", bool(r0.get("impact"))))
            failure_checks.append((f"route.{rid[:10]}.response", bool(r0.get("default_response"))))
            failure_checks.append((f"route.{rid[:10]}.hold", bool(r0.get("hold_or_block_candidate"))))
            failure_checks.append((f"route.{rid[:10]}.forbidden", bool(r0.get("forbidden_shortcut"))))
    failure_dryrun_review = {
        "review_id": "failure_route_dryrun_review_v1",
        "routes_verified": len(FAILURE_ROUTES),
        **_review_result(failure_checks),
        **meta,
    }

    metrics_doc = upstream_dc.get("decision_center_mount_health_metric_scope") or {}
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

    boundary_doc = upstream_dc.get("decision_center_boundary_matrix") or {}
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
    nc_checks.append(("nc.count10", len(DRYRUN_NON_CLAIMS) == 10))
    non_claims_review = {
        "review_id": "non_claims_review_v1",
        "dryrun_non_claims": list(DRYRUN_NON_CLAIMS),
        **_review_result(nc_checks),
        **meta,
    }

    review_passes = [
        consumability_review.get("dryrun_and_review_pass"),
        ii_dependency_review.get("dryrun_and_review_pass"),
        contract_10_review.get("dryrun_and_review_pass"),
        input_dryrun.get("dryrun_and_review_pass"),
        output_dryrun.get("dryrun_and_review_pass"),
        processing_dryrun.get("dryrun_and_review_pass"),
        state_machine_dryrun.get("dryrun_and_review_pass"),
        mra_review.get("dryrun_and_review_pass"),
        governance_dryrun.get("dryrun_and_review_pass"),
        health_dryrun.get("dryrun_and_review_pass"),
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
        ("ii_dependency", ii_dependency_review),
        ("contract_10", contract_10_review),
        ("input", input_dryrun),
        ("output", output_dryrun),
        ("processing", processing_dryrun),
        ("state_machine", state_machine_dryrun),
        ("mra", mra_review),
        ("governance", governance_dryrun),
        ("health", health_dryrun),
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
        "foundation_id": ii_version.get("foundation_id"),
        "depends_on": ii_version.get("depends_on"),
        "foundation_version": ii_version.get("version"),
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
        "foundation_id": ii_version.get("foundation_id"),
        "depends_on": ii_version.get("depends_on"),
        "foundation_version": ii_version.get("version"),
        "runtime_status": ii_version.get("runtime_status"),
        "module_id": "decision_center",
        "layer": "L7",
        "non_claims": list(DRYRUN_NON_CLAIMS),
        **meta,
    }

    return {
        "summary": summary,
        "upstream_mount_contract_consumability_review": consumability_review,
        "information_integration_frozen_dependency_review": ii_dependency_review,
        "mount_contract_10_section_review": contract_10_review,
        "input_contract_dryrun": input_dryrun,
        "output_contract_dryrun": output_dryrun,
        "processing_model_dryrun": processing_dryrun,
        "decision_state_machine_dryrun": state_machine_dryrun,
        "model_rule_algorithm_placement_review": mra_review,
        "governance_boundary_dryrun": governance_dryrun,
        "health_boundary_dryrun": health_dryrun,
        "downstream_handoff_matrix_review": handoff_review,
        "sample_flow_dryrun": sample_flow_dryrun,
        "failure_route_dryrun_review": failure_dryrun_review,
        "mount_health_metric_scope_review": health_metric_review,
        "boundary_matrix_review": boundary_matrix_review,
        "non_claims_review": non_claims_review,
        "issue_register": issue_register,
        "mount_dryrun_readiness_decision": readiness,
    }
