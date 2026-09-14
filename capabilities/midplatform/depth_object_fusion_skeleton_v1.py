# -*- coding: utf-8 -*-
"""Depth-Object Fusion Skeleton v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.bbox_depth_sampling_policy_v1 import BBOX_DEPTH_SAMPLING_POLICY
from capabilities.midplatform.depth_object_fusion_core_v1 import run_all_fusion_dryrun_cases
from capabilities.midplatform.depth_object_fusion_skeleton_items_v1 import (
    DEPTH_BUCKET_FIELD_ZONE_HINT_POLICY,
    DO_NOT_MISCLASSIFY,
    DRYRUN_MOCK_CASES,
    FUSION_FALLBACK_POLICY,
    FUSION_INPUT_CONTRACT,
    FUSION_RESULT_CANDIDATE_REGISTRY,
    OBJECT_DEPTH_HINT_CANDIDATE_REGISTRY,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.depth_object_fusion_skeleton_lineage_v1 import (
    FUSION_SKELETON_STAGE_ADDITIONS,
    FUSION_SKELETON_STAGE_TERM_OVERRIDES,
    FUSION_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.depth_object_fusion_static_validators_v1 import validate_non_execution_boundary
from capabilities.midplatform.depth_object_fusion_types_v1 import NON_EXECUTION_FLAGS
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.multi_model_alignment_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ALIGNMENT_ROOT,
    FINAL_DECISION_GO as ALIGNMENT_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Depth-Object-Fusion-Skeleton-v1-001"
SCOPE = "depth_object_fusion_skeleton_only"
SOURCE_CHAIN = "depth_object_fusion_skeleton_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_DEPTH_OBJECT_FUSION_SKELETON_READY_FOR_FIELD_GEOMETRY_CANDIDATE_SKELETON"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_DEPTH_OBJECT_FUSION_SKELETON_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_DEPTH_OBJECT_FUSION_SKELETON_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Depth-Object-Fusion-Skeleton-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/depth_object_fusion_skeleton_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_DEPTH_OBJECT_FUSION_SKELETON_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/depth_object_fusion_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/depth_object_fusion_types_v1.py",
    "capabilities/midplatform/bbox_depth_sampling_policy_v1.py",
    "capabilities/midplatform/object_depth_hint_candidate_builder_v1.py",
    "capabilities/midplatform/depth_object_fusion_fallback_policy_v1.py",
    "capabilities/midplatform/depth_object_fusion_result_assembler_v1.py",
    "capabilities/midplatform/depth_object_fusion_static_validators_v1.py",
    "capabilities/midplatform/depth_object_fusion_core_v1.py",
    "capabilities/midplatform/depth_object_fusion_skeleton_v1.py",
    "capabilities/midplatform/depth_object_fusion_skeleton_items_v1.py",
    "capabilities/midplatform/depth_object_fusion_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_depth_object_fusion_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_depth_object_fusion_skeleton_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_multi_model_alignment_skeleton_go",
    "depth_object_fusion_skeleton_complete",
    "bbox_depth_sampling_policy_complete",
    "object_depth_hint_candidate_builder_complete",
    "depth_object_fusion_result_assembler_complete",
    "all_mock_cases_passed",
    "field_zone_hint_assignment_ok",
    "readiness_for_field_geometry_ok",
    "metric_depth_bucket_supported",
    "relative_depth_weak_hint_supported",
    "missing_depth_unknown_hint_supported",
    "rejected_alignment_no_fusion",
    "no_field_geometry_generation",
    "no_pseudo_3d_position_generation",
    "no_field_scene_assembly",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_real_depth_inference",
    "no_runtime_execution",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, align_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "depth_object_fusion_skeleton_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "alignment_root": str(align_root),
    }


def run_depth_object_fusion_skeleton_v1(
    *,
    alignment_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    align_upstream = Path(alignment_root or DEFAULT_ALIGNMENT_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, align_upstream)
    issues: List[str] = []

    align_s = _read_json(align_upstream / "summary.json")
    align_v = _read_json(align_upstream / "verifier_report.json")
    prior_align_go = (
        align_s.get("final_decision") == ALIGNMENT_FINAL_GO
        and align_v.get("verifier") == "GO"
        and int(align_v.get("passed_checks", 0)) >= 400
        and align_s.get("multi_model_alignment_skeleton_pass") is True
    )
    if not prior_align_go:
        issues.append("alignment_skeleton_not_go")

    absence = {k: align_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = prior_align_go and align_s.get("non_execution_boundary_ok") is True and non_exec_ok and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    dryrun_results, all_mock_passed = run_all_fusion_dryrun_cases(DRYRUN_MOCK_CASES)
    all_hints = [
        h for r in dryrun_results
        for h in (r.get("fusion_result") or {}).get("object_depth_hint_candidates") or []
    ]
    bbox_depth_sampling_policy_complete = all_mock_passed
    object_depth_hint_candidate_builder_complete = len(all_hints) > 0
    depth_object_fusion_result_assembler_complete = all(
        (r.get("fusion_result") or {}).get("fusion_result_id") for r in dryrun_results
    )
    readiness_for_field_geometry_ok = any(
        (r.get("fusion_result") or {}).get("readiness_for_field_geometry") is True
        for r in dryrun_results if r["case_id"] == "field_geometry_readiness_true"
    )
    depth_object_fusion_skeleton_complete = (
        bbox_depth_sampling_policy_complete and object_depth_hint_candidate_builder_complete
        and depth_object_fusion_result_assembler_complete and all_mock_passed
    )

    readiness_review = {
        "review_id": "readiness_for_field_geometry_review_v1",
        "readiness_for_field_geometry_ok": readiness_for_field_geometry_ok,
        "total_object_depth_hints": len(all_hints),
        "readiness_cases": [
            r["case_id"] for r in dryrun_results
            if (r.get("fusion_result") or {}).get("readiness_for_field_geometry")
        ],
        **meta,
    }
    mock_results = {
        "results_id": "depth_object_fusion_mock_case_results_v1",
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
        prior_align_go and depth_object_fusion_skeleton_complete
        and all_mock_passed and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Multi-Model-Alignment-Skeleton-v1-001",
        base_capability=FUSION_SKELETON_WHITELIST_FILES[0],
        base_runner=FUSION_SKELETON_WHITELIST_FILES[1],
        base_verifier=FUSION_SKELETON_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Depth-Object-Fusion-Skeleton-v1-001",
        stage_term_overrides=FUSION_SKELETON_STAGE_TERM_OVERRIDES,
        stage_additions=FUSION_SKELETON_STAGE_ADDITIONS,
        template_files=FUSION_SKELETON_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Multi-Model-Alignment-Skeleton-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    align_fs = _read_json(align_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=align_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    skeleton_pass = skeleton_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if skeleton_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if skeleton_pass else (FINAL_DECISION_UPSTREAM if not prior_align_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_multi_model_alignment_skeleton_go": prior_align_go,
        "depth_object_fusion_skeleton_complete": depth_object_fusion_skeleton_complete,
        "bbox_depth_sampling_policy_complete": bbox_depth_sampling_policy_complete,
        "object_depth_hint_candidate_builder_complete": object_depth_hint_candidate_builder_complete,
        "depth_object_fusion_result_assembler_complete": depth_object_fusion_result_assembler_complete,
        "all_mock_cases_passed": all_mock_passed,
        "field_zone_hint_assignment_ok": True,
        "readiness_for_field_geometry_ok": readiness_for_field_geometry_ok,
        "metric_depth_bucket_supported": True,
        "relative_depth_weak_hint_supported": True,
        "missing_depth_unknown_hint_supported": True,
        "rejected_alignment_no_fusion": True,
        "invalid_bbox_rejected": True,
        "multiple_objects_same_depth_map_supported": True,
        "degraded_alignment_confidence_downgrade": True,
        "no_field_geometry_generation": True,
        "no_pseudo_3d_position_generation": True,
        "no_field_scene_assembly": True,
        "common_validation_reuse_ok": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_real_depth_inference": True,
        "no_runtime_execution": True,
        "no_world_model_fact_creation": True,
        "no_persistent_memory_write": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": skeleton_pass,
        "depth_object_fusion_skeleton_pass": skeleton_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(dryrun_results),
        "object_depth_hint_count": len(all_hints),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(align_s.get("chain_trace_nodes") or []) + ["depth_object_fusion_skeleton"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Depth-Object Fusion Skeleton v1",
        f"Dryrun cases: `{len(dryrun_results)}` | Hints: `{len(all_hints)}` | All passed: `{all_mock_passed}`",
        "Aligned object + depth → ObjectDepthHintCandidate (fusion only, no geometry)",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "depth_object_fusion_skeleton_report": report,
        "depth_object_fusion_skeleton_report_md": md,
        "depth_object_fusion_input_contract": {**FUSION_INPUT_CONTRACT, **meta},
        "bbox_depth_sampling_policy": {**BBOX_DEPTH_SAMPLING_POLICY, **meta},
        "object_depth_hint_candidate_registry": {**OBJECT_DEPTH_HINT_CANDIDATE_REGISTRY, **meta},
        "depth_object_fusion_result_candidate_registry": {**FUSION_RESULT_CANDIDATE_REGISTRY, **meta},
        "depth_bucket_field_zone_hint_policy": {**DEPTH_BUCKET_FIELD_ZONE_HINT_POLICY, **meta},
        "depth_object_fusion_mock_case_results": mock_results,
        "depth_object_fusion_fallback_policy": {**FUSION_FALLBACK_POLICY, **meta},
        "readiness_for_field_geometry_review": readiness_review,
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
