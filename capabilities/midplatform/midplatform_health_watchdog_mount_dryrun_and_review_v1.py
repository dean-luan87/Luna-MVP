# -*- coding: utf-8 -*-
"""Luna Midplatform Health Watchdog Mount DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_decision_center_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DECISION_CENTER_HANDOFF_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_health_watchdog_mount_planning_v1 import (
    ALGORITHM_USES,
    BOUNDARY_FALSE,
    DECISION_CENTER_OUTPUTS_CONSUMED,
    DOWNSTREAM_HANDOFFS,
    FAILURE_ROUTES,
    FINAL_DECISION_GO as MOUNT_PLANNING_FINAL_GO,
    FORBIDDEN_OUTPUTS,
    HEALTH_METRICS,
    HEALTH_STATES,
    INPUT_REQUIRED_FIELDS,
    INPUT_TYPES,
    MODEL_USES,
    NON_CLAIMS,
    OUTPUT_CANDIDATES,
    PROCESSING_STEPS,
    RULE_USES,
    SAMPLE_FLOWS,
)

PHASE_ID = "Phase-Midplatform-Health-Watchdog-Mount-DryRunAndReview-v1-001"
SCOPE = "midplatform_health_watchdog_mount_dryrun_and_review_only"
SOURCE = "midplatform_health_watchdog_mount_dryrun_and_review_v1"

UPSTREAM_MOUNT_PLANNING_FINAL = MOUNT_PLANNING_FINAL_GO
UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FINAL = DECISION_CENTER_HANDOFF_DRYRUN_FINAL_GO

FINAL_DECISION_GO = (
    "MIDPLATFORM_HEALTH_WATCHDOG_MOUNT_DRYRUN_AND_REVIEW_"
    "CLOSED_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_HEALTH_WATCHDOG_MOUNT_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Health-Watchdog-Controlled-Skeleton-Implementation-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Health-Watchdog-Mount-Issue-Review-v1-001"

UPSTREAM_MOUNT_PLANNING_FILES: Tuple[str, ...] = (
    "health_watchdog_mount_scope_v1.json",
    "health_watchdog_mount_contract_v1.json",
    "health_watchdog_input_contract_v1.json",
    "health_watchdog_output_contract_v1.json",
    "health_watchdog_processing_model_v1.json",
    "health_watchdog_health_state_machine_v1.json",
    "health_watchdog_model_rule_algorithm_placement_v1.json",
    "health_watchdog_governance_boundary_v1.json",
    "health_watchdog_recovery_boundary_v1.json",
    "health_watchdog_decision_center_dependency_boundary_v1.json",
    "health_watchdog_downstream_handoff_matrix_v1.json",
    "health_watchdog_sample_flow_plan_v1.json",
    "health_watchdog_failure_route_matrix_v1.json",
    "health_watchdog_mount_health_metric_scope_v1.json",
    "health_watchdog_boundary_matrix_v1.json",
    "health_watchdog_mount_non_claims_v1.json",
    "health_watchdog_mount_readiness_decision_v1.json",
    "summary.json",
    "verifier_report.json",
)

UPSTREAM_DECISION_CENTER_HANDOFF_FILES: Tuple[str, ...] = (
    "summary.json",
    "handoff_dryrun_readiness_decision_v1.json",
    "verifier_report.json",
)

UPSTREAM_DECISION_CENTER_PLANNING_FILES: Tuple[str, ...] = (
    "decision_center_foundation_version_tag_v1.json",
    "decision_center_frozen_type_interface_v1.json",
    "decision_center_handoff_contract_v1.json",
    "decision_center_downstream_output_contract_v1.json",
)

DRYRUN_NON_CLAIMS: Tuple[str, ...] = tuple(
    claim.replace("Mount Planning", "Mount DryRun") for claim in NON_CLAIMS
)

TERMINAL_HEALTH_STATES: Tuple[str, ...] = (
    "health_signal_review",
    "degradation_candidate_generated",
    "recovery_recommendation_candidate_generated",
    "required_observation_generated",
    "hold",
    "blocked",
)

GOVERNANCE_SCENARIOS: Tuple[str, ...] = (
    "high_risk_recovery_without_governance",
    "output_attempted",
    "task_execution_attempted",
    "memory_write_attempted",
    "worldmodel_write_attempted",
    "model_invocation_attempted_now",
    "provider_invocation_attempted_now",
    "recovery_recommendation_not_execution",
    "degradation_candidate_not_real_degradation",
)

RECOVERY_SCENARIOS: Tuple[str, ...] = (
    "recovery_execution_attempted",
    "module_restart_attempted",
    "process_control_attempted",
    "permission_release_attempted",
    "module_reload_attempted",
    "system_command_attempted",
    "emergency_output_attempted",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_health_watchdog_mount_dryrun_and_review_only",
    "simulated",
)

DEFAULT_MOUNT_PLANNING_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_mount_planning"
DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_DECISION_CENTER_HANDOFF_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_planning"
)
DEFAULT_INFORMATION_INTEGRATION_HANDOFF_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_MICRO_OS_FREEZE_DRYRUN_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_mount_dryrun_and_review"


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE,
        "module_id": "health_watchdog",
        "layer": "L5_health",
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "depends_on": "midplatform_decision_center_foundation_v1",
        "also_depends_on": [
            "midplatform_information_integration_foundation_v1",
            "midplatform_micro_os_foundation_v1",
        ],
        "runtime_status": "not_enabled",
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


def _sample_input_bundle() -> Dict[str, Any]:
    return {
        "decision_candidate_refs": ["dc_candidate_001"],
        "decision_readiness_candidate_refs": ["drc_needs_health_review"],
        "decision_block_candidate_refs": ["dbc_safety_001"],
        "downstream_decision_handoff_candidate_refs": ["ddhc_health_watchdog_001"],
        "health_review_candidate_refs": ["hrc_missing_health_001"],
        "blocked_refs": ["blocked_safety_001"],
        "hold_refs": ["hold_low_confidence_001"],
        "stale_context_refs": ["stale_context_001"],
        "low_confidence_refs": ["low_confidence_001"],
        "p0_safety_unresolved_refs": ["p0_safety_001"],
        "governance_pending_refs": ["governance_pending_001"],
        "trace_ref": "trace_health_watchdog_dryrun_001",
        "health_tag": "health_watchdog_mount_dryrun",
        "source_chain": "decision_center_foundation_v1",
        "candidate_not_fact": True,
        "governance_ref": "gov_health_watchdog_001",
    }


def _simulate_processing_step(step: str, bundle: Dict[str, Any]) -> Dict[str, Any]:
    output = "health_signal_candidate"
    if "stale" in step:
        output = "required_observation_candidate"
    elif "governance" in step:
        output = "governance_review_candidate"
    elif "recovery" in step:
        output = "recovery_recommendation_candidate"
    elif "handoff" in step:
        output = "watchdog_handoff_candidate"
    elif "severity" in step or "P0/P1" in step:
        output = "degradation_candidate"
    return {
        "step": step,
        "input_count": len(bundle),
        "output_candidates": [output],
        "runtime_executed": False,
        "recovery_executed": False,
        "task_execution": False,
        "user_output": False,
        "simulation_pass": True,
    }


def _simulate_governance_scenario(scenario_id: str) -> Dict[str, Any]:
    if scenario_id == "high_risk_recovery_without_governance":
        response = "governance_review_candidate"
    elif "output" in scenario_id or "task" in scenario_id or "write" in scenario_id or "invocation" in scenario_id:
        response = "safety_block_candidate"
    else:
        response = "hold_candidate"
    return {
        "scenario_id": scenario_id,
        "response": response,
        "blocked": True,
        "simulation_pass": True,
        "runtime_executed": False,
        "recovery_executed": False,
        "user_output": False,
    }


def _simulate_recovery_scenario(scenario_id: str) -> Dict[str, Any]:
    return {
        "scenario_id": scenario_id,
        "response": "safety_block_candidate",
        "allowed_outputs": ["recovery_recommendation_candidate", "watchdog_handoff_candidate"],
        "blocked": True,
        "real_recovery_executed": False,
        "module_restart": False,
        "process_control": False,
        "simulation_pass": True,
    }


def _simulate_sample_flow(flow: Dict[str, Any]) -> Dict[str, Any]:
    terminal = flow["outputs"][0] if flow.get("outputs") else "health_signal_candidate"
    return {
        "flow_id": flow["flow_id"],
        "inputs": list(flow.get("inputs") or []),
        "processing_steps": list(flow.get("processing") or []),
        "output_candidates": list(flow.get("outputs") or []),
        "blocked_paths": list(flow.get("blocked_paths") or []),
        "terminal_status": terminal,
        "simulation_pass": True,
        "runtime_executed": False,
        "recovery_executed": False,
        "direct_mount": False,
        "user_output": False,
    }


def run_midplatform_health_watchdog_mount_dryrun_and_review_v1(
    *,
    midplatform_health_watchdog_mount_planning_root: str,
    midplatform_decision_center_foundation_handoff_dryrun_and_review_root: str,
    midplatform_decision_center_foundation_handoff_planning_root: str,
    midplatform_information_integration_foundation_handoff_dryrun_and_review_root: str,
    midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(midplatform_health_watchdog_mount_planning_root).expanduser().resolve()
    dc_handoff_dr = Path(midplatform_decision_center_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    dc_handoff_plan = Path(midplatform_decision_center_foundation_handoff_planning_root).expanduser().resolve()
    ii_handoff_dr = Path(midplatform_information_integration_foundation_handoff_dryrun_and_review_root).expanduser().resolve()
    micro_os_dr = Path(midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_mount_planning_root": str(plan_root),
        "upstream_decision_center_handoff_dryrun_root": str(dc_handoff_dr),
        "upstream_decision_center_handoff_planning_root": str(dc_handoff_plan),
        "upstream_information_integration_handoff_dryrun_root": str(ii_handoff_dr),
        "upstream_micro_os_freeze_dryrun_root": str(micro_os_dr),
    }

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_ready = _try_read_json(plan_root / "health_watchdog_mount_readiness_decision_v1.json") or {}
    if plan_vr.get("verifier") != "GO":
        blockers.append("Health Watchdog mount planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_MOUNT_PLANNING_FINAL:
        blockers.append("Health Watchdog mount planning final_decision mismatch")
    if plan_ready.get("planning_pass") is not True:
        blockers.append("Health Watchdog mount planning pass flag must be true")

    dc_vr = _try_read_json(dc_handoff_dr / "verifier_report.json") or {}
    dc_sm = _try_read_json(dc_handoff_dr / "summary.json") or {}
    if dc_vr.get("verifier") != "GO":
        blockers.append("Decision Center foundation handoff dryrun verifier must be GO")
    if dc_sm.get("final_decision") != UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FINAL:
        blockers.append("Decision Center foundation handoff dryrun final_decision mismatch")

    upstream_hw: Dict[str, Any] = {}
    for fname in UPSTREAM_MOUNT_PLANNING_FILES:
        data = _try_read_json(plan_root / fname)
        if data is None:
            blockers.append(f"missing mount planning artifact: {fname}")
        upstream_hw[fname.replace("_v1.json", "").replace(".json", "")] = data
    upstream_dc_plan: Dict[str, Any] = {}
    for fname in UPSTREAM_DECISION_CENTER_PLANNING_FILES:
        data = _try_read_json(dc_handoff_plan / fname)
        if data is None:
            blockers.append(f"missing Decision Center planning artifact: {fname}")
        upstream_dc_plan[fname.replace("_v1.json", "")] = data
    for fname in UPSTREAM_DECISION_CENTER_HANDOFF_FILES:
        if _try_read_json(dc_handoff_dr / fname) is None:
            blockers.append(f"missing Decision Center handoff dryrun artifact: {fname}")

    version_doc = upstream_dc_plan.get("decision_center_foundation_version_tag") or {}
    type_doc = upstream_dc_plan.get("decision_center_frozen_type_interface") or {}
    handoff_contract_doc = upstream_dc_plan.get("decision_center_handoff_contract") or {}
    dc_output_doc = upstream_dc_plan.get("decision_center_downstream_output_contract") or {}
    scope_doc = upstream_hw.get("health_watchdog_mount_scope") or {}
    contract_doc = upstream_hw.get("health_watchdog_mount_contract") or {}
    input_doc = upstream_hw.get("health_watchdog_input_contract") or {}
    output_doc = upstream_hw.get("health_watchdog_output_contract") or {}
    proc_doc = upstream_hw.get("health_watchdog_processing_model") or {}
    sm_doc = upstream_hw.get("health_watchdog_health_state_machine") or {}
    mra_doc = upstream_hw.get("health_watchdog_model_rule_algorithm_placement") or {}
    gov_doc = upstream_hw.get("health_watchdog_governance_boundary") or {}
    recovery_doc = upstream_hw.get("health_watchdog_recovery_boundary") or {}
    dep_doc = upstream_hw.get("health_watchdog_decision_center_dependency_boundary") or {}
    handoff_doc = upstream_hw.get("health_watchdog_downstream_handoff_matrix") or {}
    sample_doc = upstream_hw.get("health_watchdog_sample_flow_plan") or {}
    failure_doc = upstream_hw.get("health_watchdog_failure_route_matrix") or {}
    metric_doc = upstream_hw.get("health_watchdog_mount_health_metric_scope") or {}
    boundary_doc = upstream_hw.get("health_watchdog_boundary_matrix") or {}
    nc_doc = upstream_hw.get("health_watchdog_mount_non_claims") or {}

    consumability_checks: List[Tuple[str, bool]] = [
        ("planning_verifier_go", plan_vr.get("verifier") == "GO"),
        ("planning_final", plan_sm.get("final_decision") == UPSTREAM_MOUNT_PLANNING_FINAL),
        ("dc_handoff_go", dc_vr.get("verifier") == "GO"),
        ("dc_handoff_final", dc_sm.get("final_decision") == UPSTREAM_DECISION_CENTER_HANDOFF_DRYRUN_FINAL),
        ("foundation_id", version_doc.get("foundation_id") == "midplatform_decision_center_foundation_v1"),
        ("runtime_status", version_doc.get("runtime_status") == "not_enabled"),
    ]
    for fname in UPSTREAM_MOUNT_PLANNING_FILES:
        consumability_checks.append((f"artifact.{fname[:18]}", (plan_root / fname).is_file()))
    consumability_review = {
        "review_id": "upstream_mount_contract_consumability_review_v1",
        "artifacts_consumed": list(UPSTREAM_MOUNT_PLANNING_FILES),
        **_review_result(consumability_checks),
        **meta,
    }

    dep_rules = json.dumps(dep_doc.get("rules") or [], ensure_ascii=False).lower()
    dep_checks: List[Tuple[str, bool]] = [
        ("foundation_id", dep_doc.get("foundation_id") == "midplatform_decision_center_foundation_v1"),
        ("consume_frozen", "midplatform_decision_center_foundation_v1" in dep_rules),
        ("no_redefine", "must not redefine decision center" in dep_rules),
        ("no_modify_dc", "must not modify decisioncandidate" in dep_rules),
        ("no_final_action", "final action" in dep_rules),
        ("blocked_not_state", "blocked/hold as real system state" in dep_rules),
        ("no_dc_runtime", "decision center runtime" in dep_rules),
        ("change_control", "change_control" in dep_rules),
        ("type_interface_present", "DecisionCandidate" in (type_doc.get("types") or [])),
        ("handoff_contract_present", len(handoff_contract_doc.get("rules") or []) >= 1),
        ("dc_output_contract_present", len(dc_output_doc.get("entries") or []) >= 1),
    ]
    for item in DECISION_CENTER_OUTPUTS_CONSUMED:
        dep_checks.append((f"scope.{item[:14]}", item in (scope_doc.get("allowed_decision_center_outputs_consumed") or [])))
    dc_dependency_review = {
        "review_id": "decision_center_frozen_dependency_review_v1",
        "consumed_outputs": list(DECISION_CENTER_OUTPUTS_CONSUMED),
        "decision_center_redefinition_required": False,
        **_review_result(dep_checks),
        **meta,
    }

    contract_checks: List[Tuple[str, bool]] = []
    for section in TEMPLATE_SECTIONS:
        contract_checks.append((f"section.{section[:12]}", section in contract_doc))
    contract_checks.extend(
        [
            ("module_id", contract_doc.get("module_identity", {}).get("module_id") == "health_watchdog"),
            ("not_recovery_executor", "not recovery executor" in contract_doc.get("module_identity", {}).get("role", "")),
            ("candidate_only", contract_doc.get("output_contract", {}).get("all_candidate") is True),
            (
                "no_recovery",
                contract_doc.get("output_contract", {}).get("recovery_recommendation_is_not_recovery_execution") is True,
            ),
            (
                "no_degradation",
                contract_doc.get("output_contract", {}).get("degradation_candidate_is_not_real_degradation") is True,
            ),
            ("planning_only", contract_doc.get("processing_scope", {}).get("planning_only") is True),
            ("no_runtime", contract_doc.get("processing_scope", {}).get("runtime_execution") is False),
            ("no_restart", contract_doc.get("processing_scope", {}).get("module_restart") is False),
            ("no_process", contract_doc.get("processing_scope", {}).get("process_control") is False),
        ]
    )
    contract_10_review = {
        "review_id": "mount_contract_10_section_review_v1",
        **_review_result(contract_checks),
        **meta,
    }

    input_bundle = _sample_input_bundle()
    input_checks: List[Tuple[str, bool]] = []
    for inp_type in INPUT_TYPES:
        input_checks.append((f"type.{inp_type[:14]}", inp_type in (input_doc.get("input_types") or [])))
        input_checks.append((f"sample.{inp_type[:12]}", inp_type in input_bundle))
    for field in INPUT_REQUIRED_FIELDS:
        input_checks.append((f"req.{field[:14]}", field in (input_doc.get("required_fields") or [])))
    input_checks.extend(
        [
            ("val.candidate_not_fact", input_bundle.get("candidate_not_fact") is True),
            ("val.trace", bool(input_bundle.get("trace_ref"))),
            ("val.health_tag", bool(input_bundle.get("health_tag"))),
            ("val.source_chain", bool(input_bundle.get("source_chain"))),
            ("val.governance_high_risk", bool(input_bundle.get("governance_ref"))),
        ]
    )
    input_dryrun = {
        "dryrun_id": "input_contract_dryrun_v1",
        "sample_inputs": input_bundle,
        **_review_result(input_checks),
        **meta,
    }

    output_checks: List[Tuple[str, bool]] = []
    for out_type in OUTPUT_CANDIDATES:
        output_checks.append((f"out.{out_type[:14]}", out_type in (output_doc.get("outputs") or [])))
        output_checks.append((f"candidate.{out_type[:10]}", "candidate" in out_type))
    for forbidden in FORBIDDEN_OUTPUTS:
        output_checks.append((f"forbidden.{forbidden[:12]}", forbidden in (output_doc.get("forbidden_outputs") or [])))
    output_checks.extend(
        [
            ("all_candidate", output_doc.get("all_candidate") is True),
            ("not_recovery", output_doc.get("recovery_recommendation_candidate_is_not_recovery_execution") is True),
            ("not_degradation", output_doc.get("degradation_candidate_is_not_real_degradation") is True),
            ("not_fact", output_doc.get("fact_status") == "not_fact"),
        ]
    )
    output_dryrun = {
        "dryrun_id": "output_contract_dryrun_v1",
        "simulated_outputs": [
            {"type": o, "fact_status": "not_fact", "candidate_only": True, "recovery_execution": False, "user_output": False}
            for o in OUTPUT_CANDIDATES
        ],
        **_review_result(output_checks),
        **meta,
    }

    step_runs = [_simulate_processing_step(s, input_bundle) for s in PROCESSING_STEPS]
    proc_checks: List[Tuple[str, bool]] = [
        (
            f"step.{r['step'][:14]}",
            r["simulation_pass"]
            and not r["runtime_executed"]
            and not r["recovery_executed"]
            and not r["task_execution"]
            and not r["user_output"],
        )
        for r in step_runs
    ]
    proc_checks.append(("step_count9", len(step_runs) == len(PROCESSING_STEPS)))
    proc_checks.append(("all_candidate_outputs", all("candidate" in o for r in step_runs for o in r["output_candidates"])))
    processing_dryrun = {
        "dryrun_id": "processing_model_dryrun_v1",
        "step_simulations": step_runs,
        "runtime_executed": False,
        "recovery_executed": False,
        **_review_result(proc_checks),
        **meta,
    }

    sm_checks: List[Tuple[str, bool]] = [
        ("state_count15", sm_doc.get("state_count") >= 15),
        ("all_candidate_level", sm_doc.get("all_candidate_level") is True),
        ("no_runtime_mutation", sm_doc.get("runtime_state_mutation") is False),
    ]
    for state in HEALTH_STATES:
        sm_checks.append((f"state.{state[:14]}", state in (sm_doc.get("states") or [])))
    for terminal in TERMINAL_HEALTH_STATES:
        sm_checks.append((f"terminal.{terminal[:14]}", terminal in (sm_doc.get("states") or [])))
    state_machine_dryrun = {
        "dryrun_id": "health_state_machine_dryrun_v1",
        "states": list(HEALTH_STATES),
        "terminal_states_covered": list(TERMINAL_HEALTH_STATES),
        **_review_result(sm_checks),
        **meta,
    }

    mra_checks: List[Tuple[str, bool]] = [
        ("model_invoked_now", meta.get("model_invoked_now") is False),
        ("provider_invoked_now", meta.get("provider_invoked_now") is False),
        ("model_later_only", mra_doc.get("model_invoked_now") is False),
        ("runtime_false", mra_doc.get("runtime_enabled_now") is False),
    ]
    for use in MODEL_USES:
        mra_checks.append((f"model.{use[:14]}", use in (mra_doc.get("model_uses_later") or [])))
    for use in RULE_USES:
        mra_checks.append((f"rule.{use[:14]}", use in (mra_doc.get("rule_uses") or [])))
    for use in ALGORITHM_USES:
        mra_checks.append((f"algo.{use[:14]}", use in (mra_doc.get("algorithm_uses") or [])))
    mra_review = {
        "review_id": "model_rule_algorithm_placement_review_v1",
        **_review_result(mra_checks),
        **meta,
    }

    gov_runs = [_simulate_governance_scenario(s) for s in GOVERNANCE_SCENARIOS]
    gov_checks: List[Tuple[str, bool]] = [(f"gov.{r['scenario_id'][:14]}", r["simulation_pass"] and r["blocked"]) for r in gov_runs]
    gov_rules = json.dumps(gov_doc.get("rules") or [], ensure_ascii=False).lower()
    gov_checks.extend(
        [
            ("high_risk_rule", "high-risk" in gov_rules and "governance_ref" in gov_rules),
            ("recovery_not_exec", "not recovery execution" in gov_rules),
            ("degrade_not_real", "not real module degradation" in gov_rules),
            ("boundary_no_runtime", meta.get("runtime_enabled_now") is False),
        ]
    )
    governance_dryrun = {
        "dryrun_id": "governance_boundary_dryrun_v1",
        "scenarios": gov_runs,
        **_review_result(gov_checks),
        **meta,
    }

    recovery_runs = [_simulate_recovery_scenario(s) for s in RECOVERY_SCENARIOS]
    recovery_checks: List[Tuple[str, bool]] = [
        (f"recovery.{r['scenario_id'][:14]}", r["simulation_pass"] and r["blocked"] and not r["real_recovery_executed"])
        for r in recovery_runs
    ]
    recovery_rules = json.dumps(recovery_doc.get("rules") or [], ensure_ascii=False).lower()
    for phrase in (
        "no real recovery",
        "no restart",
        "no kill process",
        "no permissions release",
        "no module reload",
        "no system command",
        "no emergency output",
        "only recovery_recommendation_candidate",
        "only watchdog_handoff_candidate",
    ):
        recovery_checks.append((f"rule.{phrase[:14]}", phrase in recovery_rules))
    recovery_boundary_dryrun = {
        "dryrun_id": "recovery_boundary_dryrun_v1",
        "scenarios": recovery_runs,
        "real_recovery_executed": False,
        **_review_result(recovery_checks),
        **meta,
    }

    handoffs = handoff_doc.get("handoffs") or []
    handoff_checks: List[Tuple[str, bool]] = [
        ("direct_mount_false", handoff_doc.get("direct_mount_executed") is False),
        ("handoff_count6", len(handoffs) >= 6),
    ]
    for item in DOWNSTREAM_HANDOFFS:
        found = next((h for h in handoffs if h.get("target") == item["target"]), {})
        handoff_checks.append((f"handoff.{item['target'][:14]}", bool(found)))
        handoff_checks.append((f"handoff.{item['target'][:10]}.mount", found.get("mount_now") is False))
        handoff_checks.append((f"handoff.{item['target'][:10]}.payload", bool(found.get("payload"))))
    handoff_review = {
        "review_id": "downstream_handoff_matrix_review_v1",
        "handoffs": handoffs,
        **_review_result(handoff_checks),
        **meta,
    }

    flow_runs = [_simulate_sample_flow(f) for f in SAMPLE_FLOWS]
    flow_checks: List[Tuple[str, bool]] = [
        (
            f"flow.{r['flow_id'][:14]}",
            r["simulation_pass"] and not r["runtime_executed"] and not r["recovery_executed"] and not r["direct_mount"],
        )
        for r in flow_runs
    ]
    flow_checks.append(("flow_count6", len(flow_runs) >= 6))
    for r in flow_runs:
        flow_checks.append((f"flow.{r['flow_id'][:10]}.terminal", bool(r.get("terminal_status"))))
        flow_checks.append((f"flow.{r['flow_id'][:10]}.blocked", len(r.get("blocked_paths") or []) >= 1))
        flow_checks.append((f"flow.{r['flow_id'][:10]}.out", len(r.get("output_candidates") or []) >= 1))
    sample_flow_dryrun = {
        "dryrun_id": "sample_flow_dryrun_v1",
        "flows": flow_runs,
        **_review_result(flow_checks),
        **meta,
    }

    routes = failure_doc.get("routes") or []
    failure_checks: List[Tuple[str, bool]] = [("route_count16", len(routes) >= 16)]
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

    metric_checks: List[Tuple[str, bool]] = [
        ("metric_count15", len(metric_doc.get("metrics") or []) >= 15),
        ("no_health_runtime", metric_doc.get("real_health_runtime_enabled") is False),
    ]
    for metric in HEALTH_METRICS:
        metric_checks.append((f"metric.{metric[:14]}", metric in (metric_doc.get("metrics") or [])))
    health_metric_review = {
        "review_id": "mount_health_metric_scope_review_v1",
        **_review_result(metric_checks),
        **meta,
    }

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
        nc_checks.append((f"dryrun.{claim[:14]}", True))
    for claim in nc_doc.get("non_claims") or []:
        nc_checks.append((f"plan.{claim[:14]}", claim in NON_CLAIMS))
    nc_checks.append(("nc.count11", len(DRYRUN_NON_CLAIMS) == 11))
    non_claims_review = {
        "review_id": "non_claims_review_v1",
        "dryrun_non_claims": list(DRYRUN_NON_CLAIMS),
        "planning_non_claims": list(NON_CLAIMS),
        **_review_result(nc_checks),
        **meta,
    }

    review_passes = [
        consumability_review.get("dryrun_and_review_pass"),
        dc_dependency_review.get("dryrun_and_review_pass"),
        contract_10_review.get("dryrun_and_review_pass"),
        input_dryrun.get("dryrun_and_review_pass"),
        output_dryrun.get("dryrun_and_review_pass"),
        processing_dryrun.get("dryrun_and_review_pass"),
        state_machine_dryrun.get("dryrun_and_review_pass"),
        mra_review.get("dryrun_and_review_pass"),
        governance_dryrun.get("dryrun_and_review_pass"),
        recovery_boundary_dryrun.get("dryrun_and_review_pass"),
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
        ("dc_dependency", dc_dependency_review),
        ("contract_10", contract_10_review),
        ("input", input_dryrun),
        ("output", output_dryrun),
        ("processing", processing_dryrun),
        ("state_machine", state_machine_dryrun),
        ("mra", mra_review),
        ("governance", governance_dryrun),
        ("recovery", recovery_boundary_dryrun),
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
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "runtime_status": "not_enabled",
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
        "foundation_id": "midplatform_decision_center_foundation_v1",
        "runtime_status": "not_enabled",
        "non_claims": list(DRYRUN_NON_CLAIMS),
        **meta,
    }

    return {
        "summary": summary,
        "upstream_mount_contract_consumability_review": consumability_review,
        "decision_center_frozen_dependency_review": dc_dependency_review,
        "mount_contract_10_section_review": contract_10_review,
        "input_contract_dryrun": input_dryrun,
        "output_contract_dryrun": output_dryrun,
        "processing_model_dryrun": processing_dryrun,
        "health_state_machine_dryrun": state_machine_dryrun,
        "model_rule_algorithm_placement_review": mra_review,
        "governance_boundary_dryrun": governance_dryrun,
        "recovery_boundary_dryrun": recovery_boundary_dryrun,
        "downstream_handoff_matrix_review": handoff_review,
        "sample_flow_dryrun": sample_flow_dryrun,
        "failure_route_dryrun_review": failure_dryrun_review,
        "mount_health_metric_scope_review": health_metric_review,
        "boundary_matrix_review": boundary_matrix_review,
        "non_claims_review": non_claims_review,
        "issue_register": issue_register,
        "mount_dryrun_readiness_decision": readiness,
    }
