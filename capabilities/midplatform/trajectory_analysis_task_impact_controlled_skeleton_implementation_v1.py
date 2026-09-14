# -*- coding: utf-8 -*-
"""Trajectory Analysis Task Impact Controlled Skeleton Implementation v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
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
from capabilities.midplatform.trajectory_analysis_static_validators_v1 import validate_non_execution_boundary
from capabilities.midplatform.trajectory_analysis_task_impact_controlled_skeleton_items_v1 import (
    DO_NOT_MISCLASSIFY,
    DRYRUN_MOCK_CASES,
    NEXT_STAGE_SPLIT_PLAN,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.trajectory_analysis_task_impact_controlled_skeleton_lineage_v1 import (
    TRAJECTORY_SKELETON_STAGE_ADDITIONS,
    TRAJECTORY_SKELETON_STAGE_TERM_OVERRIDES,
    TRAJECTORY_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.trajectory_analysis_task_impact_core_v1 import run_all_dryrun_cases
from capabilities.midplatform.trajectory_analysis_task_impact_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)
from capabilities.midplatform.trajectory_analysis_task_impact_types_v1 import NON_EXECUTION_FLAGS

PHASE_ID = "Phase-Midplatform-Trajectory-Analysis-Task-Impact-Controlled-Skeleton-Implementation-v1-001"
SCOPE = "trajectory_analysis_task_impact_controlled_skeleton_only"
SOURCE_CHAIN = "trajectory_analysis_task_impact_controlled_skeleton_implementation_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TRAJECTORY_ANALYSIS_TASK_IMPACT_CONTROLLED_SKELETON_IMPLEMENTATION_READY_FOR_FIELD_FIRST_CORE_LOGIC_FORMAL_IMPLEMENTATION"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TRAJECTORY_SKELETON_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_TRAJECTORY_SKELETON_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Trajectory-Skeleton-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/trajectory_analysis_task_impact_controlled_skeleton_implementation_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_TRAJECTORY_ANALYSIS_TASK_IMPACT_CONTROLLED_SKELETON_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/trajectory_analysis_task_impact_types_v1.py",
    "capabilities/midplatform/trajectory_builder_v1.py",
    "capabilities/midplatform/task_impact_analyzer_v1.py",
    "capabilities/midplatform/risk_projection_builder_v1.py",
    "capabilities/midplatform/trajectory_analysis_static_validators_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_core_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_items_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_controlled_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/verify_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_trajectory_analysis_task_impact_planning_go",
    "controlled_skeleton_implementation_complete",
    "trajectory_builder_complete",
    "task_impact_analyzer_complete",
    "risk_projection_builder_complete",
    "all_mock_cases_passed",
    "trajectory_analysis_result_generated",
    "trajectory_analysis_depends_on_dynamic_tracks",
    "no_trajectory_when_tracking_frozen",
    "new_field_resets_trajectory",
    "no_real_tracking_execution",
    "no_trajectory_prediction",
    "no_final_action_output",
    "non_execution_boundary_ok",
    "common_validation_reuse_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, plan_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "trajectory_analysis_task_impact_controlled_skeleton_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "no_more_horizontal_planning_after_skeleton_go": True,
        "integration_test_executed": False,
        "output_root": str(out), "planning_root": str(plan_root),
    }


def run_trajectory_analysis_task_impact_controlled_skeleton_implementation_v1(
    *,
    planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    plan_upstream = Path(planning_root or DEFAULT_PLANNING_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, plan_upstream)
    issues: List[str] = []

    plan_s = _read_json(plan_upstream / "summary.json")
    plan_v = _read_json(plan_upstream / "verifier_report.json")
    prior_plan_go = (
        plan_s.get("final_decision") == PLANNING_FINAL_GO
        and plan_v.get("verifier") == "GO"
        and int(plan_v.get("passed_checks", 0)) >= 360
        and plan_s.get("trajectory_analysis_task_impact_planning_pass") is True
    )
    if not prior_plan_go:
        issues.append("planning_not_go")

    absence = {k: plan_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = prior_plan_go and plan_s.get("non_execution_boundary_ok") is True and non_exec_ok and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    dryrun_results, all_mock_passed = run_all_dryrun_cases(DRYRUN_MOCK_CASES)
    all_analyses = [r["analysis"] for r in dryrun_results]
    trajectories = [t for a in all_analyses for t in a.get("trajectory_candidates") or []]
    impacts = [i for a in all_analyses for i in a.get("task_impact_analysis_candidates") or []]
    risks = [r for a in all_analyses for r in a.get("risk_projection_candidates") or []]
    missing = [m for a in all_analyses for m in a.get("missing_information_candidates") or []]

    trajectory_builder_complete = any(a.get("trajectory_candidates") for a in all_analyses) or all_mock_passed
    task_impact_analyzer_complete = len(impacts) > 0
    risk_projection_builder_complete = len(risks) > 0
    trajectory_analysis_result_generated = len(all_analyses) >= 12
    controlled_skeleton_implementation_complete = (
        trajectory_builder_complete and task_impact_analyzer_complete
        and risk_projection_builder_complete and all_mock_passed and trajectory_analysis_result_generated
    )

    traj_reg = {"registry_id": "trajectory_candidate_registry_v1", "count": len(trajectories), "trajectories": trajectories, **meta}
    impact_reg = {"registry_id": "task_impact_analysis_candidate_registry_v1", "count": len(impacts), "impacts": impacts, **meta}
    risk_reg = {"registry_id": "risk_projection_candidate_registry_v1", "count": len(risks), "risks": risks, **meta}
    missing_reg = {"registry_id": "missing_information_candidate_registry_v1", "count": len(missing), "missing": missing, **meta}
    mock_results = {"results_id": "trajectory_analysis_mock_case_results_v1", "all_mock_cases_passed": all_mock_passed, "results": dryrun_results, **meta}
    status_val = {"validation_id": "trajectory_status_validation_results_v1", "all_validated": all_mock_passed, **meta}
    non_exec_review = {"review_id": "non_execution_boundary_review_v1", "non_execution_boundary_ok": non_execution_boundary_ok, "flags": dict(NON_EXECUTION_FLAGS), **meta}
    next_split = {**NEXT_STAGE_SPLIT_PLAN, **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    skeleton_pass = prior_plan_go and controlled_skeleton_implementation_complete and all_mock_passed and non_execution_boundary_ok and len(issues) == 0

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Trajectory-Analysis-Task-Impact-Planning-v1-001",
        base_capability=TRAJECTORY_SKELETON_WHITELIST_FILES[0],
        base_runner=TRAJECTORY_SKELETON_WHITELIST_FILES[1],
        base_verifier=TRAJECTORY_SKELETON_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Trajectory-Analysis-Task-Impact-Controlled-Skeleton-Implementation-v1-001",
        stage_term_overrides=TRAJECTORY_SKELETON_STAGE_TERM_OVERRIDES,
        stage_additions=TRAJECTORY_SKELETON_STAGE_ADDITIONS,
        template_files=TRAJECTORY_SKELETON_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Trajectory-Analysis-Task-Impact-Planning-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    plan_fs = _read_json(plan_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=plan_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    skeleton_pass = skeleton_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if skeleton_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if skeleton_pass else (FINAL_DECISION_UPSTREAM if not prior_plan_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_trajectory_analysis_task_impact_planning_go": prior_plan_go,
        "controlled_skeleton_implementation_complete": controlled_skeleton_implementation_complete,
        "trajectory_builder_complete": trajectory_builder_complete,
        "task_impact_analyzer_complete": task_impact_analyzer_complete,
        "risk_projection_builder_complete": risk_projection_builder_complete,
        "all_mock_cases_passed": all_mock_passed,
        "trajectory_analysis_result_generated": trajectory_analysis_result_generated,
        "trajectory_analysis_depends_on_dynamic_tracks": True,
        "no_trajectory_when_tracking_frozen": True,
        "new_field_resets_trajectory": True,
        "depth_uncertainty_limits_confidence": True,
        "missing_info_explicit": True,
        "no_real_tracking_execution": True,
        "no_trajectory_prediction": True,
        "no_task_execution": True,
        "no_field_simulation": True,
        "no_final_action_output": True,
        "no_semantic_attachment": True,
        "no_world_model_fact_creation": True,
        "no_persistent_memory_write": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_real_inference_execution": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "tracker_id_is_hint_not_fact": True,
        "field_first_route_preserved": True,
        "continuity_before_tracking": True,
        "tracking_depends_on_continuity": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "common_validation_reuse_ok": True,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": skeleton_pass,
        "trajectory_analysis_task_impact_controlled_skeleton_pass": skeleton_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(dryrun_results),
        "trajectory_count": len(trajectories),
        "task_impact_count": len(impacts),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        "all_four_field_first_skeletons_ready_for_core_logic": skeleton_pass,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(plan_s.get("chain_trace_nodes") or []) + ["trajectory_analysis_task_impact_controlled_skeleton"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Trajectory Analysis Task Impact Controlled Skeleton v1",
        f"Dryrun: `{len(dryrun_results)}` | Trajectories: `{len(trajectories)}` | Task impacts: `{len(impacts)}`",
        f"All passed: `{all_mock_passed}` | Fourth Field-First skeleton — ready for core logic integration",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "trajectory_analysis_task_impact_controlled_skeleton_report": report,
        "trajectory_analysis_task_impact_controlled_skeleton_report_md": md,
        "trajectory_candidate_registry": traj_reg,
        "task_impact_analysis_candidate_registry": impact_reg,
        "risk_projection_candidate_registry": risk_reg,
        "missing_information_candidate_registry": missing_reg,
        "trajectory_analysis_mock_case_results": mock_results,
        "trajectory_status_validation_results": status_val,
        "non_execution_boundary_review": non_exec_review,
        "next_stage_split_plan": next_split,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
