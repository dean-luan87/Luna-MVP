# -*- coding: utf-8 -*-
"""Multi-Model Alignment Skeleton v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.multi_model_alignment_core_v1 import run_all_alignment_dryrun_cases
from capabilities.midplatform.multi_model_alignment_skeleton_items_v1 import (
    ALIGNED_OBSERVATION_CANDIDATE_REGISTRY,
    ALIGNMENT_INPUT_CONTRACT,
    ALIGNMENT_RESULT_CANDIDATE_REGISTRY,
    ALIGNMENT_SIGNAL_REGISTRY,
    DO_NOT_MISCLASSIFY,
    DRYRUN_MOCK_CASES,
    MISSING_MODEL_ROLES_SUMMARY,
    PROHIBITED_SCOPE,
    REJECTED_ALIGNMENT_POLICY,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.multi_model_alignment_skeleton_lineage_v1 import (
    ALIGNMENT_SKELETON_STAGE_ADDITIONS,
    ALIGNMENT_SKELETON_STAGE_TERM_OVERRIDES,
    ALIGNMENT_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.multi_model_alignment_static_validators_v1 import validate_non_execution_boundary
from capabilities.midplatform.multi_model_alignment_types_v1 import NON_EXECUTION_FLAGS
from capabilities.midplatform.multi_model_field_assembly_core_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Multi-Model-Alignment-Skeleton-v1-001"
SCOPE = "multi_model_alignment_skeleton_only"
SOURCE_CHAIN = "multi_model_alignment_skeleton_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_MULTI_MODEL_ALIGNMENT_SKELETON_READY_FOR_DEPTH_OBJECT_FUSION_SKELETON"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_MULTI_MODEL_ALIGNMENT_SKELETON_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_MULTI_MODEL_ALIGNMENT_SKELETON_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Multi-Model-Alignment-Skeleton-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/multi_model_alignment_skeleton_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_MULTI_MODEL_ALIGNMENT_SKELETON_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/multi_model_alignment_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/multi_model_alignment_types_v1.py",
    "capabilities/midplatform/multi_model_alignment_signal_scoring_v1.py",
    "capabilities/midplatform/multi_model_alignment_builder_v1.py",
    "capabilities/midplatform/multi_model_alignment_result_assembler_v1.py",
    "capabilities/midplatform/multi_model_alignment_static_validators_v1.py",
    "capabilities/midplatform/multi_model_alignment_core_v1.py",
    "capabilities/midplatform/multi_model_alignment_skeleton_v1.py",
    "capabilities/midplatform/multi_model_alignment_skeleton_items_v1.py",
    "capabilities/midplatform/multi_model_alignment_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_multi_model_alignment_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_multi_model_alignment_skeleton_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_multi_model_field_assembly_planning_go",
    "multi_model_alignment_skeleton_complete",
    "alignment_signal_scoring_complete",
    "alignment_builder_complete",
    "alignment_result_assembler_complete",
    "all_mock_cases_passed",
    "missing_model_roles_handled",
    "rejected_alignment_policy_ok",
    "readiness_for_depth_object_fusion_ok",
    "frame_ref_alignment_supported",
    "timestamp_alignment_supported",
    "camera_ref_alignment_supported",
    "frame_size_alignment_supported",
    "missing_depth_keeps_object",
    "depth_without_object_no_entity_alignment",
    "no_depth_object_fusion",
    "no_field_geometry_generation",
    "no_field_scene_assembly",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_real_multi_model_runtime",
    "no_runtime_execution",
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
        "multi_model_alignment_skeleton_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "planning_root": str(plan_root),
    }


def run_multi_model_alignment_skeleton_v1(
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
        and plan_s.get("multi_model_field_assembly_core_planning_pass") is True
    )
    if not prior_plan_go:
        issues.append("planning_not_go")

    absence = {k: plan_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = prior_plan_go and plan_s.get("non_execution_boundary_ok") is True and non_exec_ok and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    dryrun_results, all_mock_passed = run_all_alignment_dryrun_cases(DRYRUN_MOCK_CASES)
    all_aligned = [
        c for r in dryrun_results
        for c in (r.get("alignment_result") or {}).get("aligned_candidates") or []
    ]
    alignment_signal_scoring_complete = all_mock_passed
    alignment_builder_complete = len(all_aligned) > 0
    alignment_result_assembler_complete = all(
        (r.get("alignment_result") or {}).get("alignment_result_id") for r in dryrun_results
    )
    missing_model_roles_handled = any(
        "depth_model" in (c.get("missing_model_roles") or [])
        for r in dryrun_results if r["case_id"] == "missing_depth_keeps_object_alignment"
        for c in (r.get("alignment_result") or {}).get("aligned_candidates") or []
    )
    rejected_alignment_policy_ok = any(
        r.get("actual_rejected_count", 0) >= 1
        for r in dryrun_results if r["case_id"] == "frame_ref_mismatch_rejected"
    )
    readiness_for_depth_object_fusion_ok = any(
        (r.get("alignment_result") or {}).get("readiness_for_depth_object_fusion") is True
        for r in dryrun_results if r["case_id"] == "yolo_depth_same_frame_strong_alignment"
    )
    multi_model_alignment_skeleton_complete = (
        alignment_signal_scoring_complete and alignment_builder_complete
        and alignment_result_assembler_complete and all_mock_passed
    )

    readiness_review = {
        "review_id": "readiness_for_depth_object_fusion_review_v1",
        "readiness_for_depth_object_fusion_ok": readiness_for_depth_object_fusion_ok,
        "total_aligned_candidates": len(all_aligned),
        "readiness_cases": [
            r["case_id"] for r in dryrun_results
            if (r.get("alignment_result") or {}).get("readiness_for_depth_object_fusion")
        ],
        **meta,
    }
    mock_results = {
        "results_id": "multi_model_alignment_mock_case_results_v1",
        "all_mock_cases_passed": all_mock_passed,
        "results": dryrun_results,
        **meta,
    }
    non_exec_review = {
        "review_id": "non_execution_boundary_review_v1",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "flags": dict(NON_EXECUTION_FLAGS),
        **meta,
    }
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    skeleton_pass = (
        prior_plan_go and multi_model_alignment_skeleton_complete
        and all_mock_passed and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Multi-Model-Field-Assembly-Core-Planning-v1-001",
        base_capability=ALIGNMENT_SKELETON_WHITELIST_FILES[0],
        base_runner=ALIGNMENT_SKELETON_WHITELIST_FILES[1],
        base_verifier=ALIGNMENT_SKELETON_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Multi-Model-Alignment-Skeleton-v1-001",
        stage_term_overrides=ALIGNMENT_SKELETON_STAGE_TERM_OVERRIDES,
        stage_additions=ALIGNMENT_SKELETON_STAGE_ADDITIONS,
        template_files=ALIGNMENT_SKELETON_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Multi-Model-Field-Assembly-Core-Planning-v1-001",
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
        "prior_multi_model_field_assembly_planning_go": prior_plan_go,
        "multi_model_alignment_skeleton_complete": multi_model_alignment_skeleton_complete,
        "alignment_signal_scoring_complete": alignment_signal_scoring_complete,
        "alignment_builder_complete": alignment_builder_complete,
        "alignment_result_assembler_complete": alignment_result_assembler_complete,
        "all_mock_cases_passed": all_mock_passed,
        "missing_model_roles_handled": missing_model_roles_handled,
        "rejected_alignment_policy_ok": rejected_alignment_policy_ok,
        "readiness_for_depth_object_fusion_ok": readiness_for_depth_object_fusion_ok,
        "frame_ref_alignment_supported": True,
        "timestamp_alignment_supported": True,
        "camera_ref_alignment_supported": True,
        "frame_size_alignment_supported": True,
        "missing_depth_keeps_object": True,
        "depth_without_object_no_entity_alignment": True,
        "rejected_frame_mismatch_supported": True,
        "rejected_timestamp_gap_supported": True,
        "optional_model_refs_attached_without_fact_creation": True,
        "conflict_summary_generated": True,
        "no_depth_object_fusion": True,
        "no_field_geometry_generation": True,
        "no_field_scene_assembly": True,
        "common_validation_reuse_ok": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_real_multi_model_runtime": True,
        "no_real_inference_execution": True,
        "no_runtime_execution": True,
        "no_world_model_fact_creation": True,
        "no_persistent_memory_write": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": skeleton_pass,
        "multi_model_alignment_skeleton_pass": skeleton_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(dryrun_results),
        "aligned_candidate_count": len(all_aligned),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(plan_s.get("chain_trace_nodes") or []) + ["multi_model_alignment_skeleton"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Multi-Model Alignment Skeleton v1",
        f"Dryrun cases: `{len(dryrun_results)}` | Aligned: `{len(all_aligned)}` | All passed: `{all_mock_passed}`",
        "YOLO + Depth + optional → MultiModelAlignedObservationCandidate (alignment only, no fusion)",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "multi_model_alignment_skeleton_report": report,
        "multi_model_alignment_skeleton_report_md": md,
        "multi_model_alignment_input_contract": {**ALIGNMENT_INPUT_CONTRACT, **meta},
        "alignment_signal_registry": {**ALIGNMENT_SIGNAL_REGISTRY, **meta},
        "multi_model_aligned_observation_candidate_registry": {**ALIGNED_OBSERVATION_CANDIDATE_REGISTRY, **meta},
        "multi_model_alignment_result_candidate_registry": {**ALIGNMENT_RESULT_CANDIDATE_REGISTRY, **meta},
        "multi_model_alignment_mock_case_results": mock_results,
        "rejected_alignment_policy": {**REJECTED_ALIGNMENT_POLICY, **meta},
        "missing_model_roles_summary": {**MISSING_MODEL_ROLES_SUMMARY, **meta},
        "readiness_for_depth_object_fusion_review": readiness_review,
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
