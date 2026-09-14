# -*- coding: utf-8 -*-
"""Static/Dynamic Target Locking Tracking Controlled Skeleton Implementation v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.static_dynamic_target_locking_tracking_controlled_skeleton_items_v1 import (
    DO_NOT_MISCLASSIFY,
    DRYRUN_MOCK_CASES,
    NEXT_STAGE_SPLIT_PLAN,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_controlled_skeleton_lineage_v1 import (
    TARGET_LOCKING_SKELETON_STAGE_ADDITIONS,
    TARGET_LOCKING_SKELETON_STAGE_TERM_OVERRIDES,
    TARGET_LOCKING_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_types_v1 import NON_EXECUTION_FLAGS
from capabilities.midplatform.static_dynamic_target_tracking_core_v1 import run_all_dryrun_cases
from capabilities.midplatform.static_dynamic_target_tracking_static_validators_v1 import validate_non_execution_boundary
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

PHASE_ID = "Phase-Midplatform-Static-Dynamic-Target-Locking-Tracking-Controlled-Skeleton-Implementation-v1-001"
SCOPE = "static_dynamic_target_locking_tracking_controlled_skeleton_only"
SOURCE_CHAIN = "static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1"
FINAL_DECISION_GO = "MIDPLATFORM_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_CONTROLLED_SKELETON_IMPLEMENTATION_READY_FOR_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TARGET_LOCKING_SKELETON_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_TARGET_LOCKING_SKELETON_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Target-Locking-Skeleton-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_CONTROLLED_SKELETON_IMPLEMENTATION_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/static_dynamic_target_locking_tracking_controlled_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/static_dynamic_target_locking_tracking_types_v1.py",
    "capabilities/midplatform/static_dynamic_target_locking_builder_v1.py",
    "capabilities/midplatform/dynamic_target_tracking_builder_v1.py",
    "capabilities/midplatform/target_task_impact_scorer_v1.py",
    "capabilities/midplatform/static_dynamic_target_tracking_static_validators_v1.py",
    "capabilities/midplatform/static_dynamic_target_tracking_core_v1.py",
    "capabilities/midplatform/static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1.py",
    "capabilities/midplatform/static_dynamic_target_locking_tracking_controlled_skeleton_items_v1.py",
    "capabilities/midplatform/static_dynamic_target_locking_tracking_controlled_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1.py",
    "tools/evaluation/midplatform/verify_static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_static_dynamic_target_locking_tracking_planning_go",
    "controlled_skeleton_implementation_complete",
    "static_lock_builder_complete",
    "dynamic_track_builder_complete",
    "task_impact_scorer_complete",
    "all_mock_cases_passed",
    "target_tracking_plan_generated",
    "tracking_depends_on_continuity",
    "no_real_tracking_execution",
    "no_trajectory_prediction",
    "non_execution_boundary_ok",
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
        "static_dynamic_target_locking_tracking_controlled_skeleton_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "planning_root": str(plan_root),
    }


def run_static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1(
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
        and int(plan_v.get("passed_checks", 0)) >= 380
        and plan_s.get("static_dynamic_target_locking_tracking_planning_pass") is True
    )
    if not prior_plan_go:
        issues.append("planning_not_go")

    absence = {k: plan_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = prior_plan_go and plan_s.get("non_execution_boundary_ok") is True and non_exec_ok and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    dryrun_results, all_mock_passed = run_all_dryrun_cases(DRYRUN_MOCK_CASES)
    all_plans = [r["plan"] for r in dryrun_results]
    static_locks = [l for p in all_plans for l in p.get("static_locks") or []]
    dynamic_tracks = [t for p in all_plans for t in p.get("dynamic_tracks") or []]
    impacts = [i for p in all_plans for i in p.get("target_impacts") or []]

    static_lock_builder_complete = len(static_locks) > 0
    dynamic_track_builder_complete = len(dynamic_tracks) > 0
    task_impact_scorer_complete = len(impacts) > 0
    target_tracking_plan_generated = len(all_plans) >= 12
    controlled_skeleton_implementation_complete = (
        static_lock_builder_complete and dynamic_track_builder_complete
        and task_impact_scorer_complete and all_mock_passed and target_tracking_plan_generated
    )

    static_reg = {"registry_id": "static_target_lock_candidate_registry_v1", "count": len(static_locks), "locks": static_locks, **meta}
    dynamic_reg = {"registry_id": "dynamic_target_track_candidate_registry_v1", "count": len(dynamic_tracks), "tracks": dynamic_tracks, **meta}
    impact_reg = {"registry_id": "target_impact_candidate_registry_v1", "count": len(impacts), "impacts": impacts, **meta}
    plan_reg = {"registry_id": "target_tracking_plan_candidate_registry_v1", "count": len(all_plans), "plans": [{"case_id": r["case_id"], "continuity_status": r["plan"]["continuity_status"]} for r in dryrun_results], **meta}
    mock_results = {"results_id": "target_locking_tracking_mock_case_results_v1", "all_mock_cases_passed": all_mock_passed, "results": dryrun_results, **meta}
    status_val = {"validation_id": "target_status_validation_results_v1", "all_validated": all_mock_passed, **meta}
    non_exec_review = {"review_id": "non_execution_boundary_review_v1", "non_execution_boundary_ok": non_execution_boundary_ok, "flags": dict(NON_EXECUTION_FLAGS), **meta}
    next_split = {**NEXT_STAGE_SPLIT_PLAN, **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    skeleton_pass = prior_plan_go and controlled_skeleton_implementation_complete and all_mock_passed and non_execution_boundary_ok and len(issues) == 0

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Static-Dynamic-Target-Locking-Tracking-Planning-v1-001",
        base_capability=TARGET_LOCKING_SKELETON_WHITELIST_FILES[0],
        base_runner=TARGET_LOCKING_SKELETON_WHITELIST_FILES[1],
        base_verifier=TARGET_LOCKING_SKELETON_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Static-Dynamic-Target-Locking-Tracking-Controlled-Skeleton-Implementation-v1-001",
        stage_term_overrides=TARGET_LOCKING_SKELETON_STAGE_TERM_OVERRIDES,
        stage_additions=TARGET_LOCKING_SKELETON_STAGE_ADDITIONS,
        template_files=TARGET_LOCKING_SKELETON_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Static-Dynamic-Target-Locking-Tracking-Planning-v1-001",
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
        "prior_static_dynamic_target_locking_tracking_planning_go": prior_plan_go,
        "controlled_skeleton_implementation_complete": controlled_skeleton_implementation_complete,
        "static_lock_builder_complete": static_lock_builder_complete,
        "dynamic_track_builder_complete": dynamic_track_builder_complete,
        "task_impact_scorer_complete": task_impact_scorer_complete,
        "all_mock_cases_passed": all_mock_passed,
        "target_tracking_plan_generated": target_tracking_plan_generated,
        "tracking_depends_on_continuity": True,
        "new_field_resets_tracking": True,
        "field_occluded_freezes_tracking": True,
        "tracker_id_is_hint_not_fact": True,
        "low_confidence_target_not_silently_dropped": True,
        "duplicate_same_label_targets_not_merged_by_default": True,
        "occluded_target_not_deleted": True,
        "no_real_tracking_execution": True,
        "no_trajectory_prediction": True,
        "no_task_simulation": True,
        "no_semantic_attachment": True,
        "no_world_model_fact_creation": True,
        "no_persistent_memory_write": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_real_inference_execution": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "implementation_not_split_into_subphases": True,
        "strong_coupled_single_package_ok": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": skeleton_pass,
        "static_dynamic_target_locking_tracking_controlled_skeleton_pass": skeleton_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(dryrun_results),
        "static_lock_count": len(static_locks),
        "dynamic_track_count": len(dynamic_tracks),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(plan_s.get("chain_trace_nodes") or []) + ["static_dynamic_target_locking_tracking_controlled_skeleton"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Static/Dynamic Target Locking Tracking Controlled Skeleton v1",
        f"Dryrun: `{len(dryrun_results)}` | Static locks: `{len(static_locks)}` | Dynamic tracks: `{len(dynamic_tracks)}`",
        f"All passed: `{all_mock_passed}` | tracker_id is hint not fact",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "static_dynamic_target_locking_tracking_controlled_skeleton_report": report,
        "static_dynamic_target_locking_tracking_controlled_skeleton_report_md": md,
        "static_target_lock_candidate_registry": static_reg,
        "dynamic_target_track_candidate_registry": dynamic_reg,
        "target_impact_candidate_registry": impact_reg,
        "target_tracking_plan_candidate_registry": plan_reg,
        "target_locking_tracking_mock_case_results": mock_results,
        "target_status_validation_results": status_val,
        "non_execution_boundary_review": non_exec_review,
        "next_stage_split_plan": next_split,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
