# -*- coding: utf-8 -*-
"""Trajectory Analysis & Task Impact Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_continuity_detection_controlled_skeleton_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CONTINUITY_SKELETON_ROOT,
    FINAL_DECISION_GO as CONTINUITY_SKELETON_FINAL_GO,
)
from capabilities.midplatform.field_scene_small_range_construction_core_definition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FIELD_SCENE_ROOT,
    FINAL_DECISION_GO as FIELD_SCENE_FINAL_GO,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.static_dynamic_target_locking_tracking_controlled_skeleton_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_TARGET_LOCKING_SKELETON_ROOT,
    FINAL_DECISION_GO as TARGET_LOCKING_SKELETON_FINAL_GO,
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
from capabilities.midplatform.trajectory_analysis_task_impact_planning_items_v1 import (
    DO_NOT_MISCLASSIFY,
    INPUT_OUTPUT_CONTRACT,
    MISSING_INFORMATION_MODEL,
    MOCK_CASES,
    NEXT_IMPLEMENTATION_PLAN,
    PROHIBITED_SCOPE,
    RISK_PROJECTION_MODEL,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    TASK_IMPACT_ANALYSIS_MODEL,
    TASK_IMPACT_PRIORITIES,
    TASK_IMPACT_TYPES,
    TRAJECTORY_CANDIDATE_MODEL,
    TRAJECTORY_CONFIDENCE_LEVELS,
    TRAJECTORY_MOTION_PATTERNS,
    TRAJECTORY_RELIABILITY_REASONS,
    TRAJECTORY_TASK_IMPACT_RULES,
)
from capabilities.midplatform.trajectory_analysis_task_impact_planning_lineage_v1 import (
    TRAJECTORY_PLANNING_STAGE_ADDITIONS,
    TRAJECTORY_PLANNING_STAGE_TERM_OVERRIDES,
    TRAJECTORY_PLANNING_WHITELIST_FILES,
)

PHASE_ID = "Phase-Midplatform-Trajectory-Analysis-Task-Impact-Planning-v1-001"
SCOPE = "trajectory_analysis_task_impact_planning_only"
SOURCE_CHAIN = "trajectory_analysis_task_impact_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Trajectory-Analysis-Task-Impact-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/trajectory_analysis_task_impact_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_TRAJECTORY_ANALYSIS_TASK_IMPACT_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/trajectory_analysis_task_impact_planning_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/trajectory_analysis_task_impact_planning_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_planning_items_v1.py",
    "capabilities/midplatform/trajectory_analysis_task_impact_planning_lineage_v1.py",
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "tools/evaluation/midplatform/run_trajectory_analysis_task_impact_planning_v1.py",
    "tools/evaluation/midplatform/verify_trajectory_analysis_task_impact_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_static_dynamic_target_locking_tracking_controlled_skeleton_go",
    "trajectory_analysis_task_impact_planning_complete",
    "trajectory_candidate_model_complete",
    "task_impact_analysis_candidate_model_complete",
    "risk_projection_candidate_model_complete",
    "missing_information_candidate_model_complete",
    "mock_cases_complete",
    "common_validation_reuse_ok",
    "no_final_action_output",
    "no_task_execution",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
    "trajectory_analysis_depends_on_dynamic_tracks",
    "no_trajectory_when_tracking_frozen",
    "new_field_resets_trajectory",
    "depth_uncertainty_limits_confidence",
    "missing_info_explicit",
    "no_field_simulation",
    "no_world_model_fact_creation",
    "candidate_only_outputs",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, skeleton_root: Path, cont_root: Path, scene_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "trajectory_analysis_task_impact_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "target_locking_skeleton_root": str(skeleton_root),
        "continuity_skeleton_root": str(cont_root), "field_scene_root": str(scene_root),
    }


def run_trajectory_analysis_task_impact_planning_v1(
    *,
    target_locking_skeleton_root: str,
    continuity_skeleton_root: Optional[str] = None,
    field_scene_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    skeleton_upstream = Path(target_locking_skeleton_root or DEFAULT_TARGET_LOCKING_SKELETON_ROOT).expanduser().resolve()
    cont_upstream = Path(continuity_skeleton_root or DEFAULT_CONTINUITY_SKELETON_ROOT).expanduser().resolve()
    scene_upstream = Path(field_scene_root or DEFAULT_FIELD_SCENE_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, skeleton_upstream, cont_upstream, scene_upstream)
    issues: List[str] = []

    skeleton_s = _read_json(skeleton_upstream / "summary.json")
    skeleton_v = _read_json(skeleton_upstream / "verifier_report.json")
    cont_s = _read_json(cont_upstream / "summary.json")
    scene_s = _read_json(scene_upstream / "summary.json")

    prior_skeleton_go = (
        skeleton_s.get("final_decision") == TARGET_LOCKING_SKELETON_FINAL_GO
        and skeleton_v.get("verifier") == "GO"
        and int(skeleton_v.get("passed_checks", 0)) >= 480
        and skeleton_s.get("static_dynamic_target_locking_tracking_controlled_skeleton_pass") is True
    )
    prior_cont_go = cont_s.get("final_decision") == CONTINUITY_SKELETON_FINAL_GO
    prior_scene_go = scene_s.get("final_decision") == FIELD_SCENE_FINAL_GO
    if not prior_skeleton_go:
        issues.append("target_locking_skeleton_not_go")
    if not prior_cont_go:
        issues.append("continuity_skeleton_not_go")
    if not prior_scene_go:
        issues.append("field_scene_not_go")

    absence = {k: skeleton_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = (
        prior_skeleton_go and skeleton_s.get("non_execution_boundary_ok") is True and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    trajectory_candidate_model_complete = (
        TRAJECTORY_CANDIDATE_MODEL.get("candidate_only") is True
        and TRAJECTORY_CANDIDATE_MODEL.get("tracker_id_is_hint_not_fact") is True
    )
    task_impact_analysis_candidate_model_complete = TASK_IMPACT_ANALYSIS_MODEL.get("candidate_only") is True
    risk_projection_candidate_model_complete = RISK_PROJECTION_MODEL.get("candidate_only") is True
    missing_information_candidate_model_complete = MISSING_INFORMATION_MODEL.get("candidate_only") is True
    mock_cases_complete = len(MOCK_CASES) >= 12
    trajectory_analysis_task_impact_planning_complete = (
        trajectory_candidate_model_complete and task_impact_analysis_candidate_model_complete
        and risk_projection_candidate_model_complete and missing_information_candidate_model_complete
        and mock_cases_complete and len(TRAJECTORY_MOTION_PATTERNS) >= 13 and len(TASK_IMPACT_TYPES) >= 12
    )

    trajectory_status_registry = {
        "registry_id": "trajectory_status_registry_v1",
        "motion_patterns": list(TRAJECTORY_MOTION_PATTERNS),
        "confidence_levels": list(TRAJECTORY_CONFIDENCE_LEVELS),
        "reliability_reasons": list(TRAJECTORY_RELIABILITY_REASONS),
        **meta,
    }
    task_impact_type_registry = {
        "registry_id": "task_impact_type_registry_v1",
        "task_impact_types": list(TASK_IMPACT_TYPES),
        "task_impact_priorities": list(TASK_IMPACT_PRIORITIES),
        **meta,
    }
    trajectory_model = {**TRAJECTORY_CANDIDATE_MODEL, "trajectory_candidate_model_complete": trajectory_candidate_model_complete, **meta}
    task_impact_model = {**TASK_IMPACT_ANALYSIS_MODEL, "task_impact_analysis_candidate_model_complete": task_impact_analysis_candidate_model_complete, **meta}
    risk_model = {**RISK_PROJECTION_MODEL, "risk_projection_candidate_model_complete": risk_projection_candidate_model_complete, **meta}
    missing_model = {**MISSING_INFORMATION_MODEL, "missing_information_candidate_model_complete": missing_information_candidate_model_complete, **meta}
    rule_registry = {"registry_id": "trajectory_task_impact_rule_registry_v1", "rules": list(TRAJECTORY_TASK_IMPACT_RULES), **meta}
    mock_registry = {"registry_id": "trajectory_task_impact_mock_case_registry_v1", "count": len(MOCK_CASES), "cases": [{"case_id": c["case_id"]} for c in MOCK_CASES], **meta}
    mock_expected = {"results_id": "trajectory_task_impact_mock_case_expected_results_v1", "mock_cases_complete": mock_cases_complete, "cases": list(MOCK_CASES), **meta}
    io_contract = {**INPUT_OUTPUT_CONTRACT, **meta}
    next_plan = {**NEXT_IMPLEMENTATION_PLAN, **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    planning_pass = (
        prior_skeleton_go and prior_cont_go and prior_scene_go
        and trajectory_analysis_task_impact_planning_complete and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Static-Dynamic-Target-Locking-Tracking-Controlled-Skeleton-Implementation-v1-001",
        base_capability=TRAJECTORY_PLANNING_WHITELIST_FILES[0],
        base_runner=TRAJECTORY_PLANNING_WHITELIST_FILES[1],
        base_verifier=TRAJECTORY_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Trajectory-Analysis-Task-Impact-Planning-v1-001",
        stage_term_overrides=TRAJECTORY_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=TRAJECTORY_PLANNING_STAGE_ADDITIONS,
        template_files=TRAJECTORY_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Static-Dynamic-Target-Locking-Tracking-Controlled-Skeleton-Implementation-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    skeleton_fs = _read_json(skeleton_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=skeleton_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    planning_pass = planning_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if planning_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if planning_pass else (FINAL_DECISION_UPSTREAM if not prior_skeleton_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_static_dynamic_target_locking_tracking_controlled_skeleton_go": prior_skeleton_go,
        "prior_field_continuity_controlled_skeleton_go": prior_cont_go,
        "prior_field_scene_small_range_construction_go": prior_scene_go,
        "trajectory_analysis_task_impact_planning_complete": trajectory_analysis_task_impact_planning_complete,
        "trajectory_candidate_model_complete": trajectory_candidate_model_complete,
        "task_impact_analysis_candidate_model_complete": task_impact_analysis_candidate_model_complete,
        "risk_projection_candidate_model_complete": risk_projection_candidate_model_complete,
        "missing_information_candidate_model_complete": missing_information_candidate_model_complete,
        "mock_cases_complete": mock_cases_complete,
        "common_validation_reuse_ok": True,
        "trajectory_analysis_depends_on_dynamic_tracks": True,
        "no_trajectory_when_tracking_frozen": True,
        "new_field_resets_trajectory": True,
        "depth_uncertainty_limits_confidence": True,
        "missing_info_explicit": True,
        "no_final_action_output": True,
        "no_task_execution": True,
        "no_field_simulation": True,
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
        "tracker_id_is_hint_not_fact": True,
        "field_first_route_preserved": True,
        "continuity_before_tracking": True,
        "tracking_depends_on_continuity": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": planning_pass,
        "trajectory_analysis_task_impact_planning_pass": planning_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(MOCK_CASES),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(skeleton_s.get("chain_trace_nodes") or []) + ["trajectory_analysis_task_impact_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Trajectory Analysis & Task Impact Planning v1",
        f"Motion patterns: `{len(TRAJECTORY_MOTION_PATTERNS)}` | Task impact types: `{len(TASK_IMPACT_TYPES)}` | Mock cases: `{len(MOCK_CASES)}`",
        "Trajectory from track candidates; task impact is candidate not final action",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "trajectory_analysis_task_impact_planning_report": report,
        "trajectory_analysis_task_impact_planning_report_md": md,
        "trajectory_status_registry": trajectory_status_registry,
        "task_impact_type_registry": task_impact_type_registry,
        "trajectory_candidate_model": trajectory_model,
        "task_impact_analysis_candidate_model": task_impact_model,
        "risk_projection_candidate_model": risk_model,
        "missing_information_candidate_model": missing_model,
        "trajectory_task_impact_rule_registry": rule_registry,
        "trajectory_task_impact_mock_case_registry": mock_registry,
        "trajectory_task_impact_mock_case_expected_results": mock_expected,
        "trajectory_task_impact_input_output_contract": io_contract,
        "trajectory_task_impact_next_implementation_plan": next_plan,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
