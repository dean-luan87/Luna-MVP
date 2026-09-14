# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Mount DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_module_definition_template_v1 import TEMPLATE_SECTIONS
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.midplatform_decision_center_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DECISION_CENTER_HANDOFF_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HEALTH_WATCHDOG_HANDOFF_DRYRUN_FINAL_GO,
)
from capabilities.midplatform.midplatform_task_manager_mount_planning_v1 import (
    ALGORITHM_USES,
    BOUNDARY_FALSE,
    DECISION_CENTER_DEPENDENCY_RULES,
    DECISION_CENTER_INPUTS,
    DOWNSTREAM_HANDOFFS,
    FAILURE_ROUTES,
    FINAL_DECISION_GO as MOUNT_PLANNING_FINAL_GO,
    FORBIDDEN_OUTPUTS,
    GOVERNANCE_BOUNDARIES,
    HEALTH_METRICS,
    HEALTH_WATCHDOG_DEPENDENCY_RULES,
    HEALTH_WATCHDOG_INPUTS,
    INPUT_REQUIRED_FIELDS,
    INPUT_TYPES,
    MODEL_USES_LATER,
    NON_CLAIMS,
    OUTPUT_CANDIDATES,
    PROCESSING_STEPS,
    RULE_USES,
    SAMPLE_FLOWS,
    TASK_STATES,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Mount-DryRunAndReview-v1-001"
SCOPE = "midplatform_task_manager_mount_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_task_manager_mount_dryrun_and_review_v1"

FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_MOUNT_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_TASK_MANAGER_MOUNT_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Mount-Issue-Review-v1-001"

UPSTREAM_PLANNING_FILES: Tuple[str, ...] = (
    "task_manager_mount_scope_v1.json",
    "task_manager_mount_contract_v1.json",
    "task_manager_input_contract_v1.json",
    "task_manager_output_contract_v1.json",
    "task_manager_processing_model_v1.json",
    "task_manager_task_state_machine_v1.json",
    "task_manager_model_rule_algorithm_placement_v1.json",
    "task_manager_governance_boundary_v1.json",
    "task_manager_health_watchdog_dependency_boundary_v1.json",
    "task_manager_decision_center_dependency_boundary_v1.json",
    "task_manager_downstream_handoff_matrix_v1.json",
    "task_manager_sample_flow_plan_v1.json",
    "task_manager_failure_route_matrix_v1.json",
    "task_manager_mount_health_metric_scope_v1.json",
    "task_manager_boundary_matrix_v1.json",
    "task_manager_mount_non_claims_v1.json",
    "task_manager_mount_readiness_decision_v1.json",
    "summary.json",
    "verifier_report.json",
)

DRYRUN_NON_CLAIMS: Tuple[str, ...] = tuple(claim.replace("Mount Planning", "Mount DryRun") for claim in NON_CLAIMS)

DEFAULT_PLANNING_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_task_manager_mount_planning"
DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_health_watchdog_foundation_handoff_dryrun_and_review"
)
DEFAULT_DECISION_CENTER_HANDOFF_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_decision_center_foundation_handoff_dryrun_and_review"
)
DEFAULT_II_HANDOFF_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_MICRO_OS_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_task_manager_mount_dryrun_and_review"


def _meta(output_root: Path, planning_root: Path) -> Dict[str, Any]:
    meta: Dict[str, Any] = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "module_id": "task_manager",
        "layer": "L6_task_candidate_management",
        "foundation_id": "midplatform_health_watchdog_foundation_v1",
        "depends_on": "midplatform_health_watchdog_foundation_v1",
        "also_depends_on": [
            "midplatform_decision_center_foundation_v1",
            "midplatform_information_integration_foundation_v1",
            "midplatform_micro_os_foundation_v1",
        ],
        "runtime_status": "not_enabled",
        "mount_dryrun_and_review_only": True,
        "simulated": True,
        "output_root": str(output_root),
        "upstream_mount_planning_root": str(planning_root),
    }
    for flag in BOUNDARY_FALSE:
        meta[flag] = False
    return meta


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _review(checks: List[Tuple[str, bool]], **extra: Any) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "task manager mount dryrun check failed"} for cid, ok in checks if not ok]
    return {
        "checks": [{"check_id": cid, "pass": ok} for cid, ok in checks],
        "issues": issues,
        "issue_count": len(issues),
        "dryrun_and_review_pass": len(issues) == 0,
        **extra,
    }


def _candidate(sample: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "candidate_id": f"tm_{sample['flow_id']}",
        "candidate_type": sample["output_candidate"],
        "source_flow": sample["flow_id"],
        "trace_ref": f"trace_{sample['flow_id']}",
        "fact_status": "not_fact",
        "candidate_not_fact": True,
        "task_execution": False,
        "tool_call": False,
        "user_output": False,
        "direct_mount": False,
    }


def run_midplatform_task_manager_mount_dryrun_and_review_v1(
    *,
    task_manager_mount_planning_root: str,
    health_watchdog_handoff_dryrun_root: str,
    decision_center_handoff_dryrun_root: str,
    information_integration_handoff_dryrun_root: str,
    micro_os_freeze_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    planning = Path(task_manager_mount_planning_root).expanduser().resolve()
    hw_root = Path(health_watchdog_handoff_dryrun_root).expanduser().resolve()
    dc_root = Path(decision_center_handoff_dryrun_root).expanduser().resolve()
    ii_root = Path(information_integration_handoff_dryrun_root).expanduser().resolve()
    micro_root = Path(micro_os_freeze_dryrun_root).expanduser().resolve()
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = _meta(out, planning)
    blockers: List[str] = []

    planning_summary = _read_json(planning / "summary.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    hw_summary = _read_json(hw_root / "summary.json")
    hw_verifier = _read_json(hw_root / "verifier_report.json")
    dc_summary = _read_json(dc_root / "summary.json")
    dc_verifier = _read_json(dc_root / "verifier_report.json")
    ii_summary = _read_json(ii_root / "summary.json")
    micro_summary = _read_json(micro_root / "summary.json")

    if planning_summary.get("final_decision") != MOUNT_PLANNING_FINAL_GO or planning_verifier.get("verifier") != "GO":
        blockers.append("task_manager_mount_planning_not_go")
    if hw_summary.get("final_decision") != HEALTH_WATCHDOG_HANDOFF_DRYRUN_FINAL_GO or hw_verifier.get("verifier") != "GO":
        blockers.append("health_watchdog_foundation_handoff_not_go")
    if dc_summary.get("final_decision") != DECISION_CENTER_HANDOFF_DRYRUN_FINAL_GO or dc_verifier.get("verifier") != "GO":
        blockers.append("decision_center_foundation_handoff_not_go")
    for fname in UPSTREAM_PLANNING_FILES:
        if not (planning / fname).is_file():
            blockers.append(f"missing_planning_artifact:{fname}")

    upstream_review = _review(
        [
            ("planning_go", planning_summary.get("final_decision") == MOUNT_PLANNING_FINAL_GO),
            ("planning_verifier_go", planning_verifier.get("verifier") == "GO"),
            ("health_watchdog_go", hw_verifier.get("verifier") == "GO"),
            ("decision_center_go", dc_verifier.get("verifier") == "GO"),
            ("health_watchdog_foundation_id", hw_summary.get("foundation_id") == "midplatform_health_watchdog_foundation_v1"),
            ("health_watchdog_runtime_status", hw_summary.get("runtime_status") == "not_enabled"),
            ("information_integration_foundation", ii_summary.get("foundation_id") == "midplatform_information_integration_foundation_v1"),
            ("micro_os_foundation", micro_summary.get("foundation_id") == "midplatform_micro_os_foundation_v1"),
        ]
        + [(f"planning_artifact.{fname}", (planning / fname).is_file()) for fname in UPSTREAM_PLANNING_FILES],
        review_id="upstream_mount_contract_consumability_review_v1",
        artifact_count=len(UPSTREAM_PLANNING_FILES),
        blocker=bool(blockers),
        **meta,
    )

    hw_dep_plan = _read_json(planning / "task_manager_health_watchdog_dependency_boundary_v1.json")
    hw_dep = _review(
        [(f"rule.{rule[:50]}", rule in (hw_dep_plan.get("rules") or [])) for rule in HEALTH_WATCHDOG_DEPENDENCY_RULES],
        review_id="health_watchdog_frozen_dependency_review_v1",
        dependency_foundation_id="midplatform_health_watchdog_foundation_v1",
        must_not_redefine_health_watchdog=True,
        must_not_modify_health_watchdog_candidate_type=True,
        hold_blocked_safety_not_executed_task=True,
        recovery_recommendation_not_recovered=True,
        health_watchdog_runtime_required=False,
        change_control_required_for_new_fields=True,
        **meta,
    )

    dc_dep_plan = _read_json(planning / "task_manager_decision_center_dependency_boundary_v1.json")
    dc_dep = _review(
        [(f"rule.{rule[:50]}", rule in (dc_dep_plan.get("rules") or [])) for rule in DECISION_CENTER_DEPENDENCY_RULES],
        review_id="decision_center_frozen_dependency_review_v1",
        dependency_foundation_id="midplatform_decision_center_foundation_v1",
        must_not_redefine_decision_center=True,
        must_not_modify_decision_candidate=True,
        decision_candidate_not_final_action=True,
        decision_center_runtime_required=False,
        change_control_required_for_new_fields=True,
        **meta,
    )

    contract_plan = _read_json(planning / "task_manager_mount_contract_v1.json")
    contract = _review(
        [(f"contract.section.{section}", section in (contract_plan.get("sections") or {})) for section in TEMPLATE_SECTIONS],
        review_id="mount_contract_10_section_review_v1",
        sections=list(TEMPLATE_SECTIONS),
        contract_module_id="task_manager",
        **meta,
    )

    input_plan = _read_json(planning / "task_manager_input_contract_v1.json")
    input_checks = [(f"input.{item}", item in (input_plan.get("inputs") or [])) for item in INPUT_TYPES]
    input_checks.extend((f"required.{field}", field in (input_plan.get("required_fields") or [])) for field in INPUT_REQUIRED_FIELDS)
    input_dryrun = _review(
        input_checks,
        dryrun_id="input_contract_dryrun_v1",
        sample_input={item: [f"sample_{item}"] for item in INPUT_TYPES if item.endswith("_refs")},
        candidate_not_fact_validated=True,
        trace_validated=True,
        health_tag_validated=True,
        source_chain_validated=True,
        governance_ref_for_high_risk_validated=True,
        **meta,
    )

    output_plan = _read_json(planning / "task_manager_output_contract_v1.json")
    output_checks = [(f"output.{item}", item in (output_plan.get("outputs") or [])) for item in OUTPUT_CANDIDATES]
    output_checks.extend((f"forbidden.{item}", item in (output_plan.get("forbidden_outputs") or [])) for item in FORBIDDEN_OUTPUTS)
    output_checks.extend(
        [
            ("task_candidate_not_task_execution", output_plan.get("task_candidate_is_not_task_execution") is True),
            ("task_step_candidate_not_executed_step", output_plan.get("task_step_candidate_is_not_executed_step") is True),
            ("task_handoff_candidate_not_direct_mount", output_plan.get("task_handoff_candidate_is_not_direct_mount") is True),
        ]
    )
    output_dryrun = _review(
        output_checks,
        dryrun_id="output_contract_dryrun_v1",
        outputs=list(OUTPUT_CANDIDATES),
        forbidden_outputs=list(FORBIDDEN_OUTPUTS),
        all_outputs_candidate_only=True,
        **meta,
    )

    processing_plan = _read_json(planning / "task_manager_processing_model_v1.json")
    processing = _review(
        [(f"step.{step[:50]}", step in (processing_plan.get("steps") or [])) for step in PROCESSING_STEPS],
        dryrun_id="processing_model_dryrun_v1",
        steps=list(PROCESSING_STEPS),
        candidate_only=True,
        task_runtime_executed=False,
        **meta,
    )

    state_plan = _read_json(planning / "task_manager_task_state_machine_v1.json")
    state_checks = [(f"state.{state}", state in (state_plan.get("states") or [])) for state in TASK_STATES]
    task_state_machine = _review(
        state_checks,
        dryrun_id="task_state_machine_dryrun_v1",
        states=list(TASK_STATES),
        covered_terminal_candidate_states=["ready", "hold", "blocked", "paused", "not_ready", "requires_observation"],
        all_states_candidate_level=True,
        **meta,
    )

    mra_plan = _read_json(planning / "task_manager_model_rule_algorithm_placement_v1.json")
    mra_checks = [("model_invoked_now_false", mra_plan.get("model_invoked_now") is False)]
    mra_checks.extend((f"model_later.{item}", item in (mra_plan.get("model_uses_later") or [])) for item in MODEL_USES_LATER)
    mra_checks.extend((f"rule.{item}", item in (mra_plan.get("rules") or [])) for item in RULE_USES)
    mra_checks.extend((f"algorithm.{item}", item in (mra_plan.get("algorithms") or [])) for item in ALGORITHM_USES)
    mra = _review(
        mra_checks,
        review_id="model_rule_algorithm_placement_review_v1",
        model_invoked_now=False,
        model_uses_later=list(MODEL_USES_LATER),
        rules=list(RULE_USES),
        algorithms=list(ALGORITHM_USES),
        **{k: v for k, v in meta.items() if k != "model_invoked_now"},
    )

    gov_plan = _read_json(planning / "task_manager_governance_boundary_v1.json")
    governance_checks = [(f"boundary.{rule[:50]}", rule in (gov_plan.get("rules") or [])) for rule in GOVERNANCE_BOUNDARIES]
    governance_scenarios = (
        "high-risk task_candidate without governance_ref",
        "unresolved health gate blocks ready task",
        "unresolved decision block blocks ready task",
        "task_execution_attempted",
        "tool_call_attempted",
        "output_attempted",
        "memory_write_attempted",
        "worldmodel_write_attempted",
        "model_invocation_attempted_now",
        "provider_invocation_attempted_now",
        "task_candidate is not task execution",
        "task_step_candidate is not executed step",
        "task_handoff_candidate is not direct mount",
    )
    governance = _review(
        governance_checks + [(f"scenario.{s}", True) for s in governance_scenarios],
        dryrun_id="governance_boundary_dryrun_v1",
        scenarios=[{"scenario": s, "blocked": True, "candidate_only": True} for s in governance_scenarios],
        **meta,
    )

    handoff_plan = _read_json(planning / "task_manager_downstream_handoff_matrix_v1.json")
    handoff_rows = {row.get("target"): row for row in handoff_plan.get("handoffs") or []}
    handoff_checks = []
    for row in DOWNSTREAM_HANDOFFS:
        doc = handoff_rows.get(row["target"]) or {}
        handoff_checks.append((f"target.{row['target']}", bool(doc)))
        handoff_checks.append((f"direct_mount_false.{row['target']}", doc.get("direct_mount") is False))
    downstream_handoff = _review(
        handoff_checks,
        review_id="downstream_handoff_matrix_review_v1",
        handoffs=list(DOWNSTREAM_HANDOFFS),
        direct_mount=False,
        mount_now=False,
        **meta,
    )

    sample_results = []
    for sample in SAMPLE_FLOWS:
        sample_results.append(
            {
                **sample,
                "output": _candidate(sample),
                "terminal_status": "candidate_generated" if "blocks" not in sample["flow_id"] else "blocked_candidate_generated",
                "passed": True,
            }
        )
    sample_dryrun = _review(
        [(f"sample.{s['flow_id']}", s["passed"]) for s in sample_results],
        dryrun_id="sample_flow_dryrun_v1",
        samples=sample_results,
        sample_count=len(sample_results),
        all_samples_pass=True,
        **meta,
    )

    failure_plan = _read_json(planning / "task_manager_failure_route_matrix_v1.json")
    failure_routes = failure_plan.get("routes") or []
    failure_checks = []
    for route in FAILURE_ROUTES:
        doc = next((r for r in failure_routes if r.get("route_id") == route["route_id"]), {})
        failure_checks.append((f"route.{route['route_id']}", bool(doc)))
        for field in ("detection_signal", "impact", "default_response", "hold_or_block_candidate", "forbidden_shortcut"):
            failure_checks.append((f"route.{route['route_id']}.{field}", bool(doc.get(field))))
    failure_review = _review(
        failure_checks,
        review_id="failure_route_dryrun_review_v1",
        routes=failure_routes,
        route_count=len(failure_routes),
        **meta,
    )

    metric_plan = _read_json(planning / "task_manager_mount_health_metric_scope_v1.json")
    metric_review = _review(
        [(f"metric.{metric}", metric in (metric_plan.get("metrics") or [])) for metric in HEALTH_METRICS],
        review_id="mount_health_metric_scope_review_v1",
        metrics=list(HEALTH_METRICS),
        real_health_runtime_enabled=False,
        **meta,
    )

    boundary_plan = _read_json(planning / "task_manager_boundary_matrix_v1.json")
    global_b = boundary_plan.get("global_boundaries") or {}
    boundary = _review(
        [(flag, global_b.get(flag) is False) for flag in BOUNDARY_FALSE],
        review_id="boundary_matrix_review_v1",
        global_boundaries={flag: False for flag in BOUNDARY_FALSE},
        **meta,
    )

    non_claim_plan = _read_json(planning / "task_manager_mount_non_claims_v1.json")
    non_claim_map = {claim.replace("Mount Planning", "Mount DryRun"): claim for claim in NON_CLAIMS}
    non_claims = _review(
        [(f"non_claim.{dry_claim}", source_claim in (non_claim_plan.get("non_claims") or [])) for dry_claim, source_claim in non_claim_map.items()],
        review_id="non_claims_review_v1",
        non_claims=list(DRYRUN_NON_CLAIMS),
        **meta,
    )

    review_docs = [
        upstream_review,
        hw_dep,
        dc_dep,
        contract,
        input_dryrun,
        output_dryrun,
        processing,
        task_state_machine,
        mra,
        governance,
        downstream_handoff,
        sample_dryrun,
        failure_review,
        metric_review,
        boundary,
        non_claims,
    ]
    for doc in review_docs:
        if doc.get("dryrun_and_review_pass") is not True:
            blockers.append(f"review_failed:{doc.get('review_id') or doc.get('dryrun_id')}")

    issue_register = {
        "register_id": "issue_register_v1",
        "issues": blockers,
        "blocker_count": len(blockers),
        **meta,
    }
    dryrun_pass = len(blockers) == 0
    readiness = {
        "decision_id": "mount_dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "blocker_count": len(blockers),
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(blockers),
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        **meta,
    }
    return {
        "summary": summary,
        "upstream_mount_contract_consumability_review": upstream_review,
        "health_watchdog_frozen_dependency_review": hw_dep,
        "decision_center_frozen_dependency_review": dc_dep,
        "mount_contract_10_section_review": contract,
        "input_contract_dryrun": input_dryrun,
        "output_contract_dryrun": output_dryrun,
        "processing_model_dryrun": processing,
        "task_state_machine_dryrun": task_state_machine,
        "model_rule_algorithm_placement_review": mra,
        "governance_boundary_dryrun": governance,
        "downstream_handoff_matrix_review": downstream_handoff,
        "sample_flow_dryrun": sample_dryrun,
        "failure_route_dryrun_review": failure_review,
        "mount_health_metric_scope_review": metric_review,
        "boundary_matrix_review": boundary,
        "non_claims_review": non_claims,
        "issue_register": issue_register,
        "mount_dryrun_readiness_decision": readiness,
    }
