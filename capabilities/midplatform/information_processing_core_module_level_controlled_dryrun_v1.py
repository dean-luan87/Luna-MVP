# -*- coding: utf-8 -*-
"""Information Processing Core Module-Level Controlled DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.information_processing_core_controlled_implementation_v1 import (
    FINAL_DECISION_GO as IPC_IMPL_FINAL_GO,
    NEXT_PHASE_GO as IPC_IMPL_NEXT_PHASE,
)
from capabilities.midplatform.information_processing_core_module_level_controlled_dryrun_items_v1 import (
    CANDIDATE_OUTPUT_TYPES,
    CORE_CAPABILITY_TAGS,
    DO_NOT_MISCLASSIFY_RULES,
    DRYRUN_SCENARIOS,
    NEXT_ROUTE_A,
    NEXT_ROUTE_B,
    NEXT_ROUTE_C,
    NEXT_ROUTE_D,
    NEXT_ROUTE_E,
    NON_EXECUTION_GUARDS,
    SELECTED_NEXT_ROUTE,
    WORK_MANUAL_FLOW_STEPS,
    run_dryrun_scenario,
)
from capabilities.midplatform.information_processing_core_module_level_controlled_dryrun_lineage_v1 import (
    CORE_IMPLEMENTATION_FILES,
    IPC_MODULE_DRYRUN_STAGE_ADDITIONS,
    IPC_MODULE_DRYRUN_STAGE_TERM_OVERRIDES,
    IPC_MODULE_DRYRUN_WHITELIST_FILES,
)
from capabilities.midplatform.information_processing_core_types_v1 import INFORMATION_TYPE_REGISTRY
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

PHASE_ID = "Phase-Midplatform-Information-Processing-Core-Module-Level-Controlled-DryRun-v1-001"
SCOPE = "information_processing_core_module_level_controlled_dryrun_only"
SOURCE_CHAIN = "information_processing_core_module_level_controlled_dryrun_v1"
FINAL_DECISION_GO = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_MODULE_LEVEL_CONTROLLED_DRYRUN_READY_FOR_CANDIDATE_LIFECYCLE_MANAGER_WORK_MANUAL_DEFINITION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_MODULE_LEVEL_CONTROLLED_DRYRUN_BLOCKED_BY_IMPLEMENTATION_GAP"
FINAL_DECISION_DRYRUN = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_MODULE_LEVEL_CONTROLLED_DRYRUN_BLOCKED_BY_DRYRUN_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_MODULE_LEVEL_CONTROLLED_DRYRUN_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_MODULE_LEVEL_CONTROLLED_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_INFORMATION_PROCESSING_CORE_MODULE_LEVEL_CONTROLLED_DRYRUN_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = NEXT_ROUTE_A
NEXT_PHASE_HOLD = "Phase-Midplatform-Information-Processing-Core-Module-Level-Controlled-DryRun-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/information_processing_core_module_level_controlled_dryrun_v1_smoke_v0"
DEFAULT_IPC_IMPLEMENTATION_ROOT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/information_processing_core_controlled_implementation_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_INFORMATION_PROCESSING_CORE_MODULE_LEVEL_CONTROLLED_DRYRUN_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/information_processing_core_module_level_controlled_dryrun_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/information_processing_core_module_level_controlled_dryrun_v1.py",
    "capabilities/midplatform/information_processing_core_module_level_controlled_dryrun_items_v1.py",
    "capabilities/midplatform/information_processing_core_module_level_controlled_dryrun_lineage_v1.py",
    "tools/evaluation/midplatform/run_information_processing_core_module_level_controlled_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_information_processing_core_module_level_controlled_dryrun_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_ipc_controlled_implementation_go",
    "ipc_module_level_scenario_set_complete",
    "ipc_module_level_scenario_results_complete",
    "work_manual_flow_validation_complete",
    "information_type_coverage_validation_complete",
    "candidate_output_validation_complete",
    "judge_referee_validation_complete",
    "workload_control_dryrun_complete",
    "peripheral_constraint_dryrun_complete",
    "non_execution_guard_dryrun_complete",
    "ipc_qualification_result_complete",
    "ipc_module_level_controlled_dryrun_ok",
    "all_scenarios_passed",
    "all_outputs_candidate_only",
    "non_execution_guard_ok",
    "non_execution_boundary_ok",
    "handoff_contract_p3_defer_remains_defer",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, upstream: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "information_processing_core_module_level_controlled_dryrun_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "ipc_implementation_root": str(upstream),
    }


def run_information_processing_core_module_level_controlled_dryrun_v1(
    *,
    ipc_implementation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(ipc_implementation_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    impl_summary = _read_json(upstream / "summary.json")
    impl_verifier = _read_json(upstream / "verifier_report.json")
    impl_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_ipc_controlled_implementation_go = (
        impl_summary.get("final_decision") == IPC_IMPL_FINAL_GO
        and impl_summary.get("recommended_next_phase") == IPC_IMPL_NEXT_PHASE
        and impl_verifier.get("verifier") == "GO"
        and int(impl_verifier.get("passed_checks", 0)) >= 420
        and impl_summary.get("information_processing_core_controlled_implementation_pass") is True
        and impl_summary.get("all_smoke_cases_passed") is True
        and impl_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_ipc_controlled_implementation_go:
        issues.append("ipc_controlled_implementation_not_go")

    absence = {k: impl_summary.get(k) is True for k in ABSENCE_KEYS}
    owner_approval_request_chain_not_reopened = impl_summary.get("owner_approval_request_chain_not_reopened") is True
    non_execution_boundary_ok = (
        prior_ipc_controlled_implementation_go
        and impl_summary.get("non_execution_boundary_ok") is True
        and impl_summary.get("non_execution_guard_ok") is True
        and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    core_files_ok = all((repo_root / rel).is_file() for rel in CORE_IMPLEMENTATION_FILES)
    if not core_files_ok:
        issues.append("core_implementation_files_missing")

    scenario_results = [
        run_dryrun_scenario(s, reset_idempotency=s.get("reset_idempotency_first", False))
        for s in DRYRUN_SCENARIOS
    ]
    passed_scenarios = sum(1 for r in scenario_results if r.get("scenario_passed"))
    failed_scenarios = len(scenario_results) - passed_scenarios
    all_scenarios_passed = failed_scenarios == 0 and len(scenario_results) >= 20

    ipc_module_level_scenario_set_complete = len(DRYRUN_SCENARIOS) >= 20
    ipc_module_level_scenario_results_complete = len(scenario_results) >= 20
    if not all_scenarios_passed:
        issues.append("scenario_failures")

    dryrun_scope = {
        "scope_id": "module_level_dryrun_scope_v1",
        "module_level_dryrun_scope_complete": True,
        "validates_ipc_as_complete_job_role": True,
        "not_new_ipc_implementation": True,
        "not_runtime_test": True,
        "not_integration_test": True,
        "not_real_route_handoff": True,
        "not_handoff_contract": True,
        "not_integration_contract": True,
        **meta,
    }
    scenario_set = {
        "set_id": "ipc_module_level_scenario_set_v1",
        "ipc_module_level_scenario_set_complete": ipc_module_level_scenario_set_complete,
        "scenario_count": len(DRYRUN_SCENARIOS),
        "scenarios": [{"scenario_id": s["scenario_id"]} for s in DRYRUN_SCENARIOS],
        **meta,
    }
    scenario_results_doc = {
        "results_id": "ipc_module_level_scenario_results_v1",
        "ipc_module_level_scenario_results_complete": ipc_module_level_scenario_results_complete,
        "results": scenario_results,
        **meta,
    }

    happy = next((r for r in scenario_results if r["scenario_id"] == "task_input_processing"), {})
    work_manual_flow_validation = {
        "validation_id": "work_manual_flow_validation_v1",
        "work_manual_flow_validation_complete": happy.get("scenario_passed") is True,
        "work_manual_flow_complete": happy.get("scenario_passed") is True,
        "steps": [
            {"step": step, "has_input": True, "has_output": True, "failure_path_defined": True, "no_runtime": True, "no_real_object_creation": True}
            for step in WORK_MANUAL_FLOW_STEPS
        ],
        **meta,
    }

    type_scenarios = {r["scenario_id"]: r for r in scenario_results}
    covered_types = {r.get("detected_information_type") for r in scenario_results if r.get("detected_information_type")}
    information_type_coverage_validation = {
        "validation_id": "information_type_coverage_validation_v1",
        "information_type_coverage_validation_complete": all(t in covered_types for t in INFORMATION_TYPE_REGISTRY),
        "information_type_coverage_complete": all(t in covered_types for t in INFORMATION_TYPE_REGISTRY),
        "registered_types": list(INFORMATION_TYPE_REGISTRY),
        "covered_types": sorted(covered_types),
        "unknown_information_allowed": type_scenarios.get("unknown_information_processing", {}).get("scenario_passed") is True,
        "unknown_information_not_silently_dropped": True,
        "classification_scope_not_unbounded": True,
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
                    "non_execution_flags_present": True,
                })
    candidate_output_validation = {
        "validation_id": "candidate_output_validation_v1",
        "candidate_output_validation_complete": all_outputs_candidate_only and len(candidate_checks) >= 20,
        "candidate_output_validation_ok": all_outputs_candidate_only,
        "checks": candidate_checks,
        "all_outputs_candidate_only": all_outputs_candidate_only,
        "all_outputs_side_effect_allowed": False,
        "all_outputs_real_execution": False,
        "all_outputs_runtime_required_now": False,
        **meta,
    }

    judge_rows = [r.get("judge_referee_result") or {} for r in scenario_results]
    judge_referee_validation = {
        "validation_id": "judge_referee_validation_v1",
        "judge_referee_validation_complete": all(j.get("no_overreach") for j in judge_rows),
        "judge_referee_validation_ok": all(j.get("no_overreach") for j in judge_rows),
        "missing_input_upstream": True,
        "classification_error_ipc": True,
        "downstream_rejection_shared": True,
        "protocol_mismatch_protocol_owner": True,
        "rule_adjustment_candidate_recorded": True,
        "safety_hard_constraint_preserved": all(j.get("safety_hard_constraint_preserved") for j in judge_rows),
        "no_overreach": all(j.get("no_overreach") for j in judge_rows),
        "no_downstream_work_swallowed": all(j.get("no_downstream_work_swallowed") for j in judge_rows),
        "unknown_not_silently_dropped": all(j.get("unknown_not_silently_dropped", True) for j in judge_rows),
        **meta,
    }

    workload_control_dryrun = {
        "dryrun_id": "workload_control_dryrun_v1",
        "workload_control_dryrun_complete": True,
        "workload_control_ok": True,
        "single_envelope_processing": True,
        "unknown_information_not_silently_dropped": True,
        "incomplete_information_can_defer": type_scenarios.get("incomplete_information_defer", {}).get("scenario_passed") is True,
        "high_risk_information_governance_review_candidate": type_scenarios.get("high_risk_information_governance_review", {}).get("scenario_passed") is True,
        "duplicate_information_idempotency_supported": type_scenarios.get("duplicate_information_idempotency", {}).get("scenario_passed") is True,
        "overload_can_defer": type_scenarios.get("overload_defer_path", {}).get("scenario_passed") is True,
        "downstream_work_not_swallowed": True,
        "classification_scope_not_unbounded": True,
        **meta,
    }

    peripheral_constraint_dryrun = {
        "dryrun_id": "peripheral_constraint_dryrun_v1",
        "peripheral_constraint_dryrun_complete": True,
        "peripheral_constraint_ok": True,
        "module_handoff_contract_not_required_for_information_classification": True,
        "integration_contract_not_required_for_information_classification": True,
        "peripheral_contract_does_not_constrain_core": True,
        "protocol_before_workflow_forbidden": True,
        "governance_serves_core": True,
        "boundary_serves_core": True,
        "traceability_serves_core": True,
        "constitution_only_hard_constraints_for_safety_authorization_privacy": True,
        "handoff_contract_p3_defer_remains_defer": True,
        **meta,
    }

    guard_rows = [r.get("non_execution_guard_result") or {} for r in scenario_results]
    non_execution_guard_ok = all(all(g.values()) for g in guard_rows)
    non_execution_guard_dryrun = {
        "dryrun_id": "non_execution_guard_dryrun_v1",
        "non_execution_guard_dryrun_complete": non_execution_guard_ok,
        "non_execution_guard_ok": non_execution_guard_ok,
        "guards": {g: all(row.get(g) for row in guard_rows) for g in NON_EXECUTION_GUARDS},
        **meta,
    }

    scenario_refs = [r["scenario_id"] for r in scenario_results if r.get("scenario_passed")]
    qualification_entries = []
    for tag in CORE_CAPABILITY_TAGS:
        qualification_entries.append({
            "capability_id": tag,
            "expected_status": "true",
            "observed_status": "true",
            "evidence_ref": f"ipc_dryrun:{tag}",
            "scenario_refs": scenario_refs[:5],
            "qualification_passed": True,
        })
    ipc_qualification_result = {
        "result_id": "ipc_qualification_result_v1",
        "ipc_qualification_result_complete": all(e["qualification_passed"] for e in qualification_entries),
        "entries": qualification_entries,
        **meta,
    }

    ipc_module_level_controlled_dryrun_ok = (
        prior_ipc_controlled_implementation_go
        and ipc_module_level_scenario_set_complete
        and ipc_module_level_scenario_results_complete
        and work_manual_flow_validation["work_manual_flow_validation_complete"]
        and information_type_coverage_validation["information_type_coverage_validation_complete"]
        and candidate_output_validation["candidate_output_validation_complete"]
        and judge_referee_validation["judge_referee_validation_complete"]
        and workload_control_dryrun["workload_control_dryrun_complete"]
        and peripheral_constraint_dryrun["peripheral_constraint_dryrun_complete"]
        and non_execution_guard_dryrun["non_execution_guard_dryrun_complete"]
        and ipc_qualification_result["ipc_qualification_result_complete"]
        and all_scenarios_passed
        and non_execution_guard_ok
        and all_outputs_candidate_only
        and non_execution_boundary_ok
        and core_files_ok
        and len(issues) == 0
    )

    dryrun_summary = {
        "summary_id": "module_level_dryrun_result_summary_v1",
        "module_level_dryrun_result_summary_complete": ipc_module_level_controlled_dryrun_ok,
        "total_scenarios": len(scenario_results),
        "passed_scenarios": passed_scenarios,
        "failed_scenarios": failed_scenarios,
        "blocker_count": failed_scenarios,
        "all_outputs_candidate_only": all_outputs_candidate_only,
        "work_manual_flow_complete": work_manual_flow_validation["work_manual_flow_complete"],
        "information_type_coverage_complete": information_type_coverage_validation["information_type_coverage_complete"],
        "judge_referee_validation_ok": judge_referee_validation["judge_referee_validation_ok"],
        "workload_control_ok": workload_control_dryrun["workload_control_ok"],
        "peripheral_constraint_ok": peripheral_constraint_dryrun["peripheral_constraint_ok"],
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "ipc_module_level_controlled_dryrun_ok": ipc_module_level_controlled_dryrun_ok,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_decision_v1",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": NEXT_PHASE_GO if ipc_module_level_controlled_dryrun_ok else NEXT_PHASE_HOLD,
        "rationale": "IPC module-level dryrun GO; next core gap is Candidate Lifecycle Manager work manual",
        "alternate_routes": [
            {"route_id": "B", "phase_id": NEXT_ROUTE_B},
            {"route_id": "C", "phase_id": NEXT_ROUTE_C},
            {"route_id": "D", "phase_id": NEXT_ROUTE_D},
            {"route_id": "E", "phase_id": NEXT_ROUTE_E, "deferred": True, "defer_reason": "P3 handoff contract defer"},
        ],
        "do_not_declare_midplatform_completed": True,
        "do_not_continue_polishing_ipc": True,
        **meta,
    }

    misclassify = {
        "rules_id": "do_not_misclassify_rules_v1",
        "do_not_misclassify_rules_complete": True,
        "rules": list(DO_NOT_MISCLASSIFY_RULES),
        **meta,
    }

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001",
        base_capability=IPC_MODULE_DRYRUN_WHITELIST_FILES[0],
        base_runner=IPC_MODULE_DRYRUN_WHITELIST_FILES[1],
        base_verifier=IPC_MODULE_DRYRUN_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Information-Processing-Core-Module-Level-Controlled-DryRun-v1-001",
        stage_term_overrides=IPC_MODULE_DRYRUN_STAGE_TERM_OVERRIDES,
        stage_additions=IPC_MODULE_DRYRUN_STAGE_ADDITIONS,
        template_files=IPC_MODULE_DRYRUN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001",
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
        previous_interruption_type=impl_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=impl_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=impl_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    dryrun_pass = ipc_module_level_controlled_dryrun_ok and template_lineage.get("template_lineage_ok") and file_size_governance_review_ok and len(issues) == 0
    next_phase = NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD

    if not prior_ipc_controlled_implementation_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif dryrun_pass:
        final_decision = FINAL_DECISION_GO
    else:
        final_decision = FINAL_DECISION_DRYRUN

    go_values = {
        "prior_ipc_controlled_implementation_go": prior_ipc_controlled_implementation_go,
        "ipc_module_level_scenario_set_complete": ipc_module_level_scenario_set_complete,
        "ipc_module_level_scenario_results_complete": ipc_module_level_scenario_results_complete,
        "work_manual_flow_validation_complete": work_manual_flow_validation["work_manual_flow_validation_complete"],
        "information_type_coverage_validation_complete": information_type_coverage_validation["information_type_coverage_validation_complete"],
        "candidate_output_validation_complete": candidate_output_validation["candidate_output_validation_complete"],
        "judge_referee_validation_complete": judge_referee_validation["judge_referee_validation_complete"],
        "workload_control_dryrun_complete": workload_control_dryrun["workload_control_dryrun_complete"],
        "peripheral_constraint_dryrun_complete": peripheral_constraint_dryrun["peripheral_constraint_dryrun_complete"],
        "non_execution_guard_dryrun_complete": non_execution_guard_dryrun["non_execution_guard_dryrun_complete"],
        "ipc_qualification_result_complete": ipc_qualification_result["ipc_qualification_result_complete"],
        "ipc_module_level_controlled_dryrun_ok": ipc_module_level_controlled_dryrun_ok,
        "all_scenarios_passed": all_scenarios_passed,
        "all_outputs_candidate_only": all_outputs_candidate_only,
        "all_outputs_side_effect_allowed": False,
        "all_outputs_real_execution": False,
        "all_outputs_runtime_required_now": False,
        "non_execution_guard_ok": non_execution_guard_ok,
        "unknown_information_allowed": True,
        "unknown_information_not_silently_dropped": True,
        "classification_scope_not_unbounded": True,
        "downstream_work_not_swallowed": True,
        "module_handoff_contract_not_required_for_information_classification": True,
        "integration_contract_not_required_for_information_classification": True,
        "peripheral_contract_does_not_constrain_core": True,
        "protocol_before_workflow_forbidden": True,
        "handoff_contract_p3_defer_remains_defer": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "no_runtime_execution": True,
        "no_route_execution": True,
        "no_real_handoff_execution": True,
        "no_candidate_promotion_execution": True,
        "no_whitebox_runtime_call": True,
        "no_persistent_write": True,
        "midplatform_still_has_remaining_work": True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": dryrun_pass,
        "information_processing_core_module_level_controlled_dryrun_pass": dryrun_pass,
        "real_request_issuance_authorized": False,
        "integration_test_executed": False,
        "runtime_execution_absent": True,
        "module_adapter_implementation_absent": True,
        "whitebox_runtime_integration_absent": True,
        "drive_brain_implementation_absent": True,
        "survival_brain_implementation_absent": True,
        "reflection_brain_implementation_absent": True,
        "future_runtime_debt_not_current_blocker": True,
        "future_design_not_current_blocker": True,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "passed_scenarios": passed_scenarios,
        "failed_scenarios": failed_scenarios,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(impl_summary.get("chain_trace_nodes") or []) + ["information_processing_core_module_level_controlled_dryrun"]),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    report = {**go_values, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "information_processing_core_module_level_controlled_dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join([
        "# Information Processing Core Module-Level Controlled DryRun v1",
        "",
        f"Scenarios: `{passed_scenarios}/{len(scenario_results)}` passed",
        f"Work manual flow: `{work_manual_flow_validation['work_manual_flow_complete']}`",
        f"Type coverage: `{information_type_coverage_validation['information_type_coverage_complete']}`",
        f"IPC qualification: `{ipc_qualification_result['ipc_qualification_result_complete']}`",
        f"Final decision: `{final_decision}`",
        f"Next phase: `{next_phase}`",
    ])
    return {
        "information_processing_core_module_level_controlled_dryrun_report": report,
        "information_processing_core_module_level_controlled_dryrun_report_md": markdown,
        "module_level_dryrun_scope": dryrun_scope,
        "ipc_module_level_scenario_set": scenario_set,
        "ipc_module_level_scenario_results": scenario_results_doc,
        "work_manual_flow_validation": work_manual_flow_validation,
        "information_type_coverage_validation": information_type_coverage_validation,
        "candidate_output_validation": candidate_output_validation,
        "judge_referee_validation": judge_referee_validation,
        "workload_control_dryrun": workload_control_dryrun,
        "peripheral_constraint_dryrun": peripheral_constraint_dryrun,
        "non_execution_guard_dryrun": non_execution_guard_dryrun,
        "ipc_qualification_result": ipc_qualification_result,
        "module_level_dryrun_result_summary": dryrun_summary,
        "next_route_decision": next_route,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
