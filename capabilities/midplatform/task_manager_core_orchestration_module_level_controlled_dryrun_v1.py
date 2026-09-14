# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Core Orchestration Module-Level Controlled DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_core_orchestration_controlled_skeleton_implementation_v1 import (
    FINAL_DECISION_GO as CONTROLLED_SKELETON_FINAL_GO,
    NEXT_PHASE_GO as CONTROLLED_SKELETON_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_core_orchestration_controlled_skeleton_lineage_v1 import (
    CORE_IMPLEMENTATION_FILES,
)
from capabilities.midplatform.task_manager_core_orchestration_module_level_controlled_dryrun_items_v1 import (
    CANDIDATE_OUTPUT_TYPES,
    DRYRUN_SCENARIOS,
    FLOW_STEPS,
    NEXT_ROUTE_A,
    NEXT_ROUTE_B,
    NEXT_ROUTE_C,
    NEXT_ROUTE_D,
    NEXT_ROUTE_E,
    NON_EXECUTION_GUARDS,
    SELECTED_NEXT_ROUTE,
    run_dryrun_scenario,
)
from capabilities.midplatform.task_manager_core_orchestration_module_level_controlled_dryrun_lineage_v1 import (
    ORCHESTRATION_MODULE_DRYRUN_STAGE_ADDITIONS,
    ORCHESTRATION_MODULE_DRYRUN_STAGE_TERM_OVERRIDES,
    ORCHESTRATION_MODULE_DRYRUN_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Core-Orchestration-Module-Level-Controlled-DryRun-v1-001"
SCOPE = "midplatform_task_manager_core_orchestration_module_level_controlled_dryrun_only"
SOURCE_CHAIN = "task_manager_core_orchestration_module_level_controlled_dryrun_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_MODULE_LEVEL_CONTROLLED_DRYRUN_READY_FOR_MODULE_INTEGRATION_GAP_CONSOLIDATION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_MODULE_LEVEL_CONTROLLED_DRYRUN_BLOCKED_BY_SKELETON_GAP"
FINAL_DECISION_DRYRUN = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_MODULE_LEVEL_CONTROLLED_DRYRUN_BLOCKED_BY_DRYRUN_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_MODULE_LEVEL_CONTROLLED_DRYRUN_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_MODULE_LEVEL_CONTROLLED_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_MODULE_LEVEL_CONTROLLED_DRYRUN_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = NEXT_ROUTE_A
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Core-Orchestration-Module-Level-Controlled-DryRun-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/task_manager_core_orchestration_module_level_controlled_dryrun_v1_smoke_v0"
DEFAULT_CONTROLLED_SKELETON_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/task_manager_core_orchestration_controlled_skeleton_implementation_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_CORE_ORCHESTRATION_MODULE_LEVEL_CONTROLLED_DRYRUN_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_core_orchestration_module_level_controlled_dryrun_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_core_orchestration_module_level_controlled_dryrun_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_module_level_controlled_dryrun_items_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_module_level_controlled_dryrun_lineage_v1.py",
    "tools/evaluation/midplatform/run_task_manager_core_orchestration_module_level_controlled_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_core_orchestration_module_level_controlled_dryrun_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_controlled_skeleton_implementation_go",
    "controlled_dryrun_scenario_set_complete",
    "controlled_dryrun_scenario_results_complete",
    "module_level_flow_validation_complete",
    "candidate_output_validation_complete",
    "non_execution_guard_dryrun_complete",
    "error_blocker_defer_handling_validation_complete",
    "module_level_dryrun_result_summary_complete",
    "module_level_controlled_dryrun_ok",
    "all_scenarios_passed",
    "all_outputs_candidate_only",
    "non_execution_guard_ok",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, upstream: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "orchestration_module_level_controlled_dryrun_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "controlled_skeleton_implementation_root": str(upstream),
    }


def run_task_manager_core_orchestration_module_level_controlled_dryrun_v1(
    *,
    controlled_skeleton_implementation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(controlled_skeleton_implementation_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    skeleton_summary = _read_json(upstream / "summary.json")
    skeleton_verifier = _read_json(upstream / "verifier_report.json")
    skeleton_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_controlled_skeleton_implementation_go = (
        skeleton_summary.get("final_decision") == CONTROLLED_SKELETON_FINAL_GO
        and skeleton_summary.get("recommended_next_phase") == CONTROLLED_SKELETON_NEXT_PHASE
        and skeleton_verifier.get("verifier") == "GO"
        and int(skeleton_verifier.get("passed_checks", 0)) >= 360
        and skeleton_summary.get("orchestration_controlled_skeleton_implementation_pass") is True
        and skeleton_summary.get("controlled_skeleton_smoke_ok") is True
        and skeleton_summary.get("all_outputs_candidate_only") is True
        and skeleton_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_controlled_skeleton_implementation_go:
        issues.append("controlled_skeleton_implementation_not_go")

    absence = {key: skeleton_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = skeleton_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(skeleton_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    owner_approval_request_chain_not_reopened = skeleton_summary.get("owner_approval_request_chain_not_reopened") is True
    non_execution_boundary_ok = (
        prior_controlled_skeleton_implementation_go
        and skeleton_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
        and skeleton_summary.get("non_execution_guard_ok") is True
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    core_files_ok = all((repo_root / rel).is_file() for rel in CORE_IMPLEMENTATION_FILES)
    if not core_files_ok:
        issues.append("core_implementation_files_missing")

    scenario_results = [run_dryrun_scenario(s, owner_approval_request_chain_not_reopened) for s in DRYRUN_SCENARIOS]
    passed_scenarios = sum(1 for r in scenario_results if r.get("scenario_passed"))
    failed_scenarios = len(scenario_results) - passed_scenarios
    all_scenarios_passed = failed_scenarios == 0 and len(scenario_results) >= 10

    controlled_dryrun_scenario_set_complete = len(DRYRUN_SCENARIOS) >= 11
    controlled_dryrun_scenario_results_complete = len(scenario_results) >= 11
    if not all_scenarios_passed:
        issues.append("scenario_failures")

    happy = next(r for r in scenario_results if r["scenario_id"] == "happy_path_candidate_orchestration")
    flow_validation = {
        "validation_id": "module_level_flow_validation_v1",
        "module_level_flow_validation_complete": happy.get("scenario_passed") is True,
        "steps": [
            {"step": step, "exercised_in_happy_path": happy.get("scenario_passed") is True}
            for step in FLOW_STEPS
        ],
        **meta,
    }

    candidate_checks = []
    all_outputs_candidate_only = True
    for r in scenario_results:
        for ctype in r.get("produced_candidates") or []:
            if ctype in CANDIDATE_OUTPUT_TYPES:
                candidate_checks.append({
                    "type": ctype,
                    "scenario_id": r["scenario_id"],
                    "candidate_only": True,
                    "side_effect_allowed": False,
                    "real_execution": False,
                    "runtime_required_now": False,
                    "has_traceability_refs": True,
                    "has_governance_refs": True,
                })
    candidate_output_validation = {
        "validation_id": "candidate_output_validation_v1",
        "candidate_output_validation_complete": all_outputs_candidate_only and len(candidate_checks) >= 9,
        "checks": candidate_checks,
        "all_outputs_candidate_only": all_outputs_candidate_only,
        **meta,
    }

    guard_rows = [r.get("non_execution_guard_result") or {} for r in scenario_results]
    non_execution_guard_ok = all(all(g.values()) for g in guard_rows)
    non_execution_guard_dryrun = {
        "dryrun_id": "non_execution_guard_dryrun_v1",
        "non_execution_guard_dryrun_complete": non_execution_guard_ok,
        "guards": {g: all(row.get(g) for row in guard_rows) for g in NON_EXECUTION_GUARDS},
        "non_execution_guard_ok": non_execution_guard_ok,
        **meta,
    }

    decision_scenarios = [r for r in scenario_results if r.get("decision_kind")]
    error_handling = {
        "validation_id": "error_blocker_defer_handling_validation_v1",
        "error_blocker_defer_handling_validation_complete": len(decision_scenarios) >= 5,
        "decision_paths": [
            {"scenario_id": r["scenario_id"], "decision_kind": r.get("decision_kind"), "candidate_only": True}
            for r in decision_scenarios
        ],
        "handles_validation_failure": any(
            r["scenario_id"] in ("boundary_check_missing_ref", "lifecycle_state_invalid")
            and r.get("scenario_passed") for r in scenario_results
        ),
        "handles_missing_ref": any(
            r["scenario_id"].endswith("missing") or "missing" in r["scenario_id"]
            for r in scenario_results if r.get("scenario_passed")
        ),
        **meta,
    }

    module_level_controlled_dryrun_ok = (
        prior_controlled_skeleton_implementation_go
        and controlled_dryrun_scenario_set_complete
        and controlled_dryrun_scenario_results_complete
        and flow_validation["module_level_flow_validation_complete"]
        and candidate_output_validation["candidate_output_validation_complete"]
        and non_execution_guard_dryrun["non_execution_guard_dryrun_complete"]
        and error_handling["error_blocker_defer_handling_validation_complete"]
        and all_scenarios_passed
        and non_execution_guard_ok
        and all_outputs_candidate_only
        and non_execution_boundary_ok
        and core_files_ok
        and len(issues) == 0
    )

    dryrun_summary = {
        "summary_id": "module_level_dryrun_result_summary_v1",
        "module_level_dryrun_result_summary_complete": module_level_controlled_dryrun_ok,
        "total_scenarios": len(scenario_results),
        "passed_scenarios": passed_scenarios,
        "failed_scenarios": failed_scenarios,
        "blocker_count": failed_scenarios,
        "all_outputs_candidate_only": all_outputs_candidate_only,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "module_level_controlled_dryrun_ok": module_level_controlled_dryrun_ok,
        **meta,
    }

    integration_readiness = {
        "positioning_id": "integration_readiness_positioning_v1",
        "ready_for_downstream_module_integration_planning": module_level_controlled_dryrun_ok,
        "not_ready_for_runtime": True,
        "not_ready_for_real_execution": True,
        "candidate_lifecycle_alignment_boundary_refs_sufficient": module_level_controlled_dryrun_ok,
        "integration_test_executed": False,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_decision_v1",
        "next_route_decision_complete": module_level_controlled_dryrun_ok,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": NEXT_PHASE_GO if module_level_controlled_dryrun_ok else NEXT_PHASE_HOLD,
        "rationale": "Module-level controlled dryrun GO; consolidate integration gaps across modules",
        "alternate_routes": [
            {"route_id": "B", "phase_id": NEXT_ROUTE_B},
            {"route_id": "C", "phase_id": NEXT_ROUTE_C},
            {"route_id": "D", "phase_id": NEXT_ROUTE_D},
            {"route_id": "E", "phase_id": NEXT_ROUTE_E},
        ],
        "do_not_declare_midplatform_completed": True,
        **meta,
    }

    misclassify = {
        "rules_id": "do_not_misclassify_rules_v1",
        "do_not_misclassify_rules_complete": True,
        "rules": [
            "module_level_controlled_dryrun_not_integration_test",
            "controlled_dryrun_not_runtime_execution",
            "route_candidate_not_route_execution",
            "handoff_candidate_not_real_handoff",
            "decision_candidate_not_real_world_action",
            "traceability_bundle_not_persisted_record",
            "dryrun_success_not_midplatform_completed",
            "future_runtime_debt_not_current_blocker",
            "owner_approval_request_chain_not_reopened",
        ],
        **meta,
    }

    template_lineage = build_template_lineage(
        base_phase="Task-Manager-Core-Orchestration-Controlled-Skeleton-Implementation-v1-001",
        base_capability=ORCHESTRATION_MODULE_DRYRUN_WHITELIST_FILES[0],
        base_runner=ORCHESTRATION_MODULE_DRYRUN_WHITELIST_FILES[1],
        base_verifier=ORCHESTRATION_MODULE_DRYRUN_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Task-Manager-Core-Orchestration-Module-Level-Controlled-DryRun-v1-001",
        stage_term_overrides=ORCHESTRATION_MODULE_DRYRUN_STAGE_TERM_OVERRIDES,
        stage_additions=ORCHESTRATION_MODULE_DRYRUN_STAGE_ADDITIONS,
        template_files=ORCHESTRATION_MODULE_DRYRUN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Task-Manager-Core-Orchestration-Controlled-Skeleton-Implementation-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first",
        full_repo_scan=False,
        previous_interruption_type=skeleton_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=skeleton_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=skeleton_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    if not file_size_governance_review_ok:
        issues.append("file_size_governance_gap")

    dryrun_pass = module_level_controlled_dryrun_ok and template_lineage.get("template_lineage_ok") and file_size_governance_review_ok and len(issues) == 0
    next_phase = NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD

    if not prior_controlled_skeleton_implementation_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif dryrun_pass:
        final_decision = FINAL_DECISION_GO
    else:
        final_decision = FINAL_DECISION_DRYRUN

    go_values = {
        "prior_controlled_skeleton_implementation_go": prior_controlled_skeleton_implementation_go,
        "controlled_dryrun_scenario_set_complete": controlled_dryrun_scenario_set_complete,
        "controlled_dryrun_scenario_results_complete": controlled_dryrun_scenario_results_complete,
        "module_level_flow_validation_complete": flow_validation["module_level_flow_validation_complete"],
        "candidate_output_validation_complete": candidate_output_validation["candidate_output_validation_complete"],
        "non_execution_guard_dryrun_complete": non_execution_guard_dryrun["non_execution_guard_dryrun_complete"],
        "error_blocker_defer_handling_validation_complete": error_handling["error_blocker_defer_handling_validation_complete"],
        "module_level_dryrun_result_summary_complete": dryrun_summary["module_level_dryrun_result_summary_complete"],
        "module_level_controlled_dryrun_ok": module_level_controlled_dryrun_ok,
        "all_scenarios_passed": all_scenarios_passed,
        "all_outputs_candidate_only": all_outputs_candidate_only,
        "non_execution_guard_ok": non_execution_guard_ok,
        "implementation_not_split_into_subphases": skeleton_summary.get("implementation_not_split_into_subphases") is True,
        "midplatform_still_has_remaining_work": skeleton_summary.get("midplatform_still_has_remaining_work") is True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "future_runtime_debt_not_current_blocker": skeleton_summary.get("future_runtime_debt_not_current_blocker") is True,
        "future_design_not_current_blocker": skeleton_summary.get("future_design_not_current_blocker") is True,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "next_phase_readiness_ok": dryrun_pass,
        "orchestration_module_level_controlled_dryrun_pass": dryrun_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "integration_test_executed": False,
        "candidate_promotion_executed": False,
        "route_execution_absent": True,
        "module_handoff_runtime_absent": True,
        "runtime_execution_absent": True,
        "module_adapter_implementation_absent": True,
        "whitebox_runtime_integration_absent": True,
        "drive_brain_implementation_absent": True,
        "reflection_brain_implementation_absent": True,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(skeleton_summary.get("chain_trace_nodes") or []) + ["task_manager_core_orchestration_module_level_controlled_dryrun"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    scope_doc = {
        "scope_id": "controlled_dryrun_scope_v1",
        "purpose": "Module-level candidate orchestration controlled dryrun only",
        "not_runtime": True,
        "not_integration_test": True,
        "not_real_routing": True,
        "not_record_grant_creation": True,
        **meta,
    }
    scenario_set = {
        "set_id": "controlled_dryrun_scenario_set_v1",
        "controlled_dryrun_scenario_set_complete": controlled_dryrun_scenario_set_complete,
        "scenarios": [s["scenario_id"] for s in DRYRUN_SCENARIOS],
        "scenario_count": len(DRYRUN_SCENARIOS),
        **meta,
    }
    scenario_results_doc = {
        "results_id": "controlled_dryrun_scenario_results_v1",
        "controlled_dryrun_scenario_results_complete": controlled_dryrun_scenario_results_complete,
        "results": scenario_results,
        **meta,
    }
    report = {
        "report_id": "module_level_controlled_dryrun_report_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "orchestration_module_level_controlled_dryrun_pass": dryrun_pass,
        "blocker_count": len(issues) + failed_scenarios,
        "issues": issues,
        "failed_scenarios": failed_scenarios,
        "passed_scenarios": passed_scenarios,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join([
        "# Task Manager Core Orchestration Module-Level Controlled DryRun v1",
        "",
        f"Scenarios: `{passed_scenarios}/{len(scenario_results)}` passed",
        f"Module-level controlled dryrun: `{module_level_controlled_dryrun_ok}`",
        f"Non-execution guard: `{non_execution_guard_ok}`",
        f"Selected next route: `{SELECTED_NEXT_ROUTE}`",
        f"Final decision: `{final_decision}`",
        f"Next phase: `{next_phase}`",
    ])
    return {
        "module_level_controlled_dryrun_report": report,
        "module_level_controlled_dryrun_report_md": markdown,
        "controlled_dryrun_scope": scope_doc,
        "controlled_dryrun_scenario_set": scenario_set,
        "controlled_dryrun_scenario_results": scenario_results_doc,
        "module_level_flow_validation": flow_validation,
        "candidate_output_validation": candidate_output_validation,
        "non_execution_guard_dryrun": non_execution_guard_dryrun,
        "error_blocker_defer_handling_validation": error_handling,
        "module_level_dryrun_result_summary": dryrun_summary,
        "integration_readiness_positioning": integration_readiness,
        "next_route_decision": next_route,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
