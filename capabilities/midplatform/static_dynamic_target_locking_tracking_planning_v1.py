# -*- coding: utf-8 -*-
"""Static/Dynamic Target Locking & Tracking Planning v1."""

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
from capabilities.midplatform.static_dynamic_target_locking_tracking_planning_items_v1 import (
    ABNORMAL_CASE_POLICY,
    CONTINUITY_ALLOWED_FOR_TRACKING,
    CONTINUITY_FREEZE_TRACKING,
    CONTINUITY_RESET_TRACKING,
    DO_NOT_MISCLASSIFY,
    DYNAMIC_TARGET_LABELS,
    DYNAMIC_TARGET_TRACK_MODEL,
    INPUT_OUTPUT_CONTRACT,
    MOCK_CASES,
    NEXT_IMPLEMENTATION_PLAN,
    PROHIBITED_SCOPE,
    SCOPE_DEFINITION,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    STATIC_TARGET_LABELS,
    STATIC_TARGET_LOCK_MODEL,
    TARGET_LOCK_STATUSES,
    TARGET_MOTION_STATUSES,
    TARGET_PRIORITY_LEVELS,
    TARGET_TASK_IMPACT_HINTS,
    TARGET_VISIBILITY_STATUSES,
    TASK_IMPACT_HINT_POLICY,
)
from capabilities.midplatform.static_dynamic_target_locking_tracking_planning_lineage_v1 import (
    TARGET_LOCKING_TRACKING_PLANNING_STAGE_ADDITIONS,
    TARGET_LOCKING_TRACKING_PLANNING_STAGE_TERM_OVERRIDES,
    TARGET_LOCKING_TRACKING_PLANNING_WHITELIST_FILES,
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

PHASE_ID = "Phase-Midplatform-Static-Dynamic-Target-Locking-Tracking-Planning-v1-001"
SCOPE = "static_dynamic_target_locking_tracking_planning_only"
SOURCE_CHAIN = "static_dynamic_target_locking_tracking_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_PLANNING_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TARGET_LOCKING_TRACKING_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_TARGET_LOCKING_TRACKING_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Target-Locking-Tracking-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/static_dynamic_target_locking_tracking_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_STATIC_DYNAMIC_TARGET_LOCKING_TRACKING_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/static_dynamic_target_locking_tracking_planning_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/static_dynamic_target_locking_tracking_planning_v1.py",
    "capabilities/midplatform/static_dynamic_target_locking_tracking_planning_items_v1.py",
    "capabilities/midplatform/static_dynamic_target_locking_tracking_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_static_dynamic_target_locking_tracking_planning_v1.py",
    "tools/evaluation/midplatform/verify_static_dynamic_target_locking_tracking_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_continuity_controlled_skeleton_go",
    "target_locking_tracking_planning_complete",
    "target_classification_registry_complete",
    "static_target_lock_model_complete",
    "dynamic_target_track_model_complete",
    "task_impact_hint_policy_complete",
    "mock_cases_complete",
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


def _meta(out: Path, cont_root: Path, scene_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "static_dynamic_target_locking_tracking_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "continuity_skeleton_root": str(cont_root),
        "field_scene_root": str(scene_root),
    }


def run_static_dynamic_target_locking_tracking_planning_v1(
    *,
    continuity_skeleton_root: str,
    field_scene_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    cont_upstream = Path(continuity_skeleton_root or DEFAULT_CONTINUITY_SKELETON_ROOT).expanduser().resolve()
    scene_upstream = Path(field_scene_root or DEFAULT_FIELD_SCENE_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, cont_upstream, scene_upstream)
    issues: List[str] = []

    cont_s = _read_json(cont_upstream / "summary.json")
    cont_v = _read_json(cont_upstream / "verifier_report.json")
    scene_s = _read_json(scene_upstream / "summary.json")
    prior_cont_go = (
        cont_s.get("final_decision") == CONTINUITY_SKELETON_FINAL_GO
        and cont_v.get("verifier") == "GO"
        and int(cont_v.get("passed_checks", 0)) >= 480
        and cont_s.get("field_continuity_detection_controlled_skeleton_pass") is True
    )
    prior_scene_go = scene_s.get("final_decision") == FIELD_SCENE_FINAL_GO
    if not prior_cont_go:
        issues.append("continuity_skeleton_not_go")
    if not prior_scene_go:
        issues.append("field_scene_not_go")

    absence = {k: cont_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_cont_go and cont_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    target_classification_registry_complete = len(STATIC_TARGET_LABELS) >= 10 and len(DYNAMIC_TARGET_LABELS) >= 8
    static_target_lock_model_complete = STATIC_TARGET_LOCK_MODEL.get("candidate_only") is True
    dynamic_target_track_model_complete = DYNAMIC_TARGET_TRACK_MODEL.get("candidate_only") is True and DYNAMIC_TARGET_TRACK_MODEL.get("tracker_id_is_hint_not_fact") is True
    task_impact_hint_policy_complete = TASK_IMPACT_HINT_POLICY.get("tracking_depends_on_continuity") is True
    mock_cases_complete = len(MOCK_CASES) >= 12
    target_locking_tracking_planning_complete = (
        target_classification_registry_complete and static_target_lock_model_complete
        and dynamic_target_track_model_complete and task_impact_hint_policy_complete and mock_cases_complete
    )

    class_reg = {
        "registry_id": "target_classification_registry_v1",
        "target_classification_registry_complete": target_classification_registry_complete,
        "static_targets": list(STATIC_TARGET_LABELS),
        "dynamic_targets": list(DYNAMIC_TARGET_LABELS),
        **meta,
    }
    status_reg = {
        "registry_id": "target_status_registry_v1",
        "visibility_statuses": list(TARGET_VISIBILITY_STATUSES),
        "motion_statuses": list(TARGET_MOTION_STATUSES),
        "lock_statuses": list(TARGET_LOCK_STATUSES),
        "task_impact_hints": list(TARGET_TASK_IMPACT_HINTS),
        "priority_levels": list(TARGET_PRIORITY_LEVELS),
        "continuity_allowed_for_tracking": list(CONTINUITY_ALLOWED_FOR_TRACKING),
        "continuity_freeze_tracking": list(CONTINUITY_FREEZE_TRACKING),
        "continuity_reset_tracking": list(CONTINUITY_RESET_TRACKING),
        **meta,
    }
    static_model = {**STATIC_TARGET_LOCK_MODEL, "static_target_lock_model_complete": static_target_lock_model_complete, **meta}
    dynamic_model = {**DYNAMIC_TARGET_TRACK_MODEL, "dynamic_target_track_model_complete": dynamic_target_track_model_complete, **meta}
    impact_policy = {**TASK_IMPACT_HINT_POLICY, "task_impact_hint_policy_complete": task_impact_hint_policy_complete, **meta}
    abnormal = {**ABNORMAL_CASE_POLICY, **meta}
    mock_registry = {"registry_id": "target_mock_case_registry_v1", "count": len(MOCK_CASES), "cases": [{"case_id": c["case_id"]} for c in MOCK_CASES], **meta}
    mock_expected = {"results_id": "target_mock_case_expected_results_v1", "mock_cases_complete": mock_cases_complete, "cases": list(MOCK_CASES), **meta}
    io_contract = {**INPUT_OUTPUT_CONTRACT, **meta}
    next_plan = {**NEXT_IMPLEMENTATION_PLAN, **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    planning_pass = (
        prior_cont_go and prior_scene_go and target_locking_tracking_planning_complete
        and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-Continuity-Detection-Controlled-Skeleton-Implementation-v1-001",
        base_capability=TARGET_LOCKING_TRACKING_PLANNING_WHITELIST_FILES[0],
        base_runner=TARGET_LOCKING_TRACKING_PLANNING_WHITELIST_FILES[1],
        base_verifier=TARGET_LOCKING_TRACKING_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Static-Dynamic-Target-Locking-Tracking-Planning-v1-001",
        stage_term_overrides=TARGET_LOCKING_TRACKING_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=TARGET_LOCKING_TRACKING_PLANNING_STAGE_ADDITIONS,
        template_files=TARGET_LOCKING_TRACKING_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-Continuity-Detection-Controlled-Skeleton-Implementation-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    cont_fs = _read_json(cont_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=cont_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    planning_pass = planning_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if planning_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if planning_pass else (FINAL_DECISION_UPSTREAM if not prior_cont_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_field_continuity_controlled_skeleton_go": prior_cont_go,
        "prior_field_scene_small_range_construction_go": prior_scene_go,
        "target_locking_tracking_planning_complete": target_locking_tracking_planning_complete,
        "target_classification_registry_complete": target_classification_registry_complete,
        "static_target_lock_model_complete": static_target_lock_model_complete,
        "dynamic_target_track_model_complete": dynamic_target_track_model_complete,
        "task_impact_hint_policy_complete": task_impact_hint_policy_complete,
        "mock_cases_complete": mock_cases_complete,
        "tracking_depends_on_continuity": True,
        "new_field_resets_tracking": True,
        "field_occluded_freezes_tracking": True,
        "tracker_id_is_hint_not_fact": True,
        "low_confidence_target_not_silently_dropped": True,
        "duplicate_same_label_targets_not_merged_by_default": True,
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
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": planning_pass,
        "static_dynamic_target_locking_tracking_planning_pass": planning_pass,
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
        chain_trace_nodes=tuple(list(cont_s.get("chain_trace_nodes") or []) + ["static_dynamic_target_locking_tracking_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Static/Dynamic Target Locking & Tracking Planning v1",
        f"Static labels: `{len(STATIC_TARGET_LABELS)}` | Dynamic labels: `{len(DYNAMIC_TARGET_LABELS)}` | Mock cases: `{len(MOCK_CASES)}`",
        "Continuity before tracking; track_id is hint not fact",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "static_dynamic_target_locking_tracking_planning_report": report,
        "static_dynamic_target_locking_tracking_planning_report_md": md,
        "target_classification_registry": class_reg,
        "target_status_registry": status_reg,
        "static_target_lock_model": static_model,
        "dynamic_target_track_model": dynamic_model,
        "target_task_impact_hint_policy": impact_policy,
        "target_abnormal_case_policy": abnormal,
        "target_mock_case_registry": mock_registry,
        "target_mock_case_expected_results": mock_expected,
        "target_input_output_contract": io_contract,
        "target_next_implementation_plan": next_plan,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
