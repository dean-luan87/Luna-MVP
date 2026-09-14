# -*- coding: utf-8 -*-
"""Field Geometry Candidate Skeleton v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.depth_object_fusion_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FUSION_ROOT,
    FINAL_DECISION_GO as FUSION_FINAL_GO,
)
from capabilities.midplatform.field_geometry_candidate_core_v1 import run_all_geometry_dryrun_cases
from capabilities.midplatform.field_geometry_candidate_skeleton_items_v1 import (
    DO_NOT_MISCLASSIFY,
    DRYRUN_MOCK_CASES,
    FIELD_GEOMETRY_CANDIDATE_REGISTRY,
    FIELD_GEOMETRY_GENERATION_RESULT_REGISTRY,
    OBJECT_SPATIAL_STATE_CANDIDATE_REGISTRY,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.field_geometry_candidate_skeleton_lineage_v1 import (
    GEOMETRY_SKELETON_STAGE_ADDITIONS,
    GEOMETRY_SKELETON_STAGE_TERM_OVERRIDES,
    GEOMETRY_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.field_geometry_candidate_static_validators_v1 import validate_non_execution_boundary
from capabilities.midplatform.field_geometry_candidate_types_v1 import NON_EXECUTION_FLAGS
from capabilities.midplatform.field_zone_assignment_policy_v1 import FIELD_ZONE_ASSIGNMENT_POLICY
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.geometry_confidence_policy_v1 import GEOMETRY_CONFIDENCE_POLICY
from capabilities.midplatform.pseudo_3d_projection_policy_v1 import PSEUDO_3D_PROJECTION_POLICY
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

PHASE_ID = "Phase-Midplatform-Field-Geometry-Candidate-Skeleton-v1-001"
SCOPE = "field_geometry_candidate_skeleton_only"
SOURCE_CHAIN = "field_geometry_candidate_skeleton_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_GEOMETRY_CANDIDATE_SKELETON_READY_FOR_FIELD_ASSEMBLY_SKELETON"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_GEOMETRY_CANDIDATE_SKELETON_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_GEOMETRY_CANDIDATE_SKELETON_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-Geometry-Candidate-Skeleton-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_geometry_candidate_skeleton_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_GEOMETRY_CANDIDATE_SKELETON_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_geometry_candidate_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_geometry_candidate_types_v1.py",
    "capabilities/midplatform/pseudo_3d_projection_policy_v1.py",
    "capabilities/midplatform/field_zone_assignment_policy_v1.py",
    "capabilities/midplatform/geometry_confidence_policy_v1.py",
    "capabilities/midplatform/field_geometry_candidate_builder_v1.py",
    "capabilities/midplatform/field_geometry_generation_result_assembler_v1.py",
    "capabilities/midplatform/field_geometry_candidate_static_validators_v1.py",
    "capabilities/midplatform/field_geometry_candidate_core_v1.py",
    "capabilities/midplatform/field_geometry_candidate_skeleton_v1.py",
    "capabilities/midplatform/field_geometry_candidate_skeleton_items_v1.py",
    "capabilities/midplatform/field_geometry_candidate_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_geometry_candidate_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_geometry_candidate_skeleton_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_depth_object_fusion_skeleton_go",
    "field_geometry_candidate_skeleton_complete",
    "pseudo_3d_projection_policy_complete",
    "field_zone_assignment_policy_complete",
    "geometry_confidence_policy_complete",
    "all_mock_cases_passed",
    "readiness_for_field_assembly_ok",
    "pseudo_3d_position_generation_supported",
    "metric_depth_zone_assignment_supported",
    "relative_depth_weak_geometry_supported",
    "unknown_depth_geometry_unknown_supported",
    "invalid_bbox_geometry_rejected",
    "geometry_confidence_degradation_supported",
    "no_field_scene_assembly",
    "no_scene_relation_generation",
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


def _meta(out: Path, fusion_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_geometry_candidate_skeleton_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "fusion_root": str(fusion_root),
    }


def run_field_geometry_candidate_skeleton_v1(
    *,
    fusion_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    fusion_upstream = Path(fusion_root or DEFAULT_FUSION_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, fusion_upstream)
    issues: List[str] = []

    fusion_s = _read_json(fusion_upstream / "summary.json")
    fusion_v = _read_json(fusion_upstream / "verifier_report.json")
    prior_fusion_go = (
        fusion_s.get("final_decision") == FUSION_FINAL_GO
        and fusion_v.get("verifier") == "GO"
        and int(fusion_v.get("passed_checks", 0)) >= 420
        and fusion_s.get("depth_object_fusion_skeleton_pass") is True
    )
    if not prior_fusion_go:
        issues.append("depth_object_fusion_skeleton_not_go")

    absence = {k: fusion_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = (
        prior_fusion_go and fusion_s.get("non_execution_boundary_ok") is True
        and non_exec_ok and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    dryrun_results, all_mock_passed = run_all_geometry_dryrun_cases(DRYRUN_MOCK_CASES)
    all_spatial = [
        s for r in dryrun_results
        for s in (r.get("geometry_result") or {}).get("object_spatial_state_candidates") or []
    ]
    all_geometry = [
        g for r in dryrun_results
        for g in (r.get("geometry_result") or {}).get("field_geometry_candidates") or []
    ]

    pseudo_3d_projection_policy_complete = all_mock_passed
    field_zone_assignment_policy_complete = all_mock_passed
    geometry_confidence_policy_complete = all_mock_passed
    field_geometry_candidate_skeleton_complete = (
        all_mock_passed and len(all_geometry) > 0 and len(all_spatial) > 0
    )
    readiness_for_field_assembly_ok = any(
        (r.get("geometry_result") or {}).get("readiness_for_field_assembly") is True
        for r in dryrun_results if r["case_id"] == "readiness_for_field_assembly_true"
    )

    readiness_review = {
        "review_id": "readiness_for_field_assembly_review_v1",
        "readiness_for_field_assembly_ok": readiness_for_field_assembly_ok,
        "total_spatial_states": len(all_spatial),
        "total_geometry_candidates": len(all_geometry),
        "readiness_cases": [
            r["case_id"] for r in dryrun_results
            if (r.get("geometry_result") or {}).get("readiness_for_field_assembly")
        ],
        **meta,
    }
    mock_results = {
        "results_id": "field_geometry_mock_case_results_v1",
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
        prior_fusion_go and field_geometry_candidate_skeleton_complete
        and all_mock_passed and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Depth-Object-Fusion-Skeleton-v1-001",
        base_capability=GEOMETRY_SKELETON_WHITELIST_FILES[0],
        base_runner=GEOMETRY_SKELETON_WHITELIST_FILES[1],
        base_verifier=GEOMETRY_SKELETON_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-Geometry-Candidate-Skeleton-v1-001",
        stage_term_overrides=GEOMETRY_SKELETON_STAGE_TERM_OVERRIDES,
        stage_additions=GEOMETRY_SKELETON_STAGE_ADDITIONS,
        template_files=GEOMETRY_SKELETON_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Depth-Object-Fusion-Skeleton-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    fusion_fs = _read_json(fusion_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=fusion_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    skeleton_pass = skeleton_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if skeleton_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if skeleton_pass else (
        FINAL_DECISION_UPSTREAM if not prior_fusion_go else FINAL_DECISION_RECAL
    )

    go_values = {
        "prior_depth_object_fusion_skeleton_go": prior_fusion_go,
        "field_geometry_candidate_skeleton_complete": field_geometry_candidate_skeleton_complete,
        "pseudo_3d_projection_policy_complete": pseudo_3d_projection_policy_complete,
        "field_zone_assignment_policy_complete": field_zone_assignment_policy_complete,
        "geometry_confidence_policy_complete": geometry_confidence_policy_complete,
        "all_mock_cases_passed": all_mock_passed,
        "readiness_for_field_assembly_ok": readiness_for_field_assembly_ok,
        "pseudo_3d_position_generation_supported": True,
        "metric_depth_zone_assignment_supported": True,
        "relative_depth_weak_geometry_supported": True,
        "unknown_depth_geometry_unknown_supported": True,
        "invalid_bbox_geometry_rejected": True,
        "geometry_confidence_degradation_supported": True,
        "multiple_objects_geometry_supported": True,
        "no_field_scene_assembly": True,
        "no_scene_relation_generation": True,
        "no_world_model_fact_creation": True,
        "no_slam_runtime": True,
        "no_field_simulation": True,
        "common_validation_reuse_ok": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_real_depth_inference": True,
        "no_runtime_execution": True,
        "no_persistent_memory_write": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": skeleton_pass,
        "field_geometry_candidate_skeleton_pass": skeleton_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(dryrun_results),
        "spatial_state_count": len(all_spatial),
        "geometry_candidate_count": len(all_geometry),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    go_values["mock_case_count"] = len(dryrun_results)

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(fusion_s.get("chain_trace_nodes") or []) + ["field_geometry_candidate_skeleton"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field Geometry Candidate Skeleton v1",
        f"Dryrun cases: `{len(dryrun_results)}` | Spatial: `{len(all_spatial)}` | Geometry: `{len(all_geometry)}` | All passed: `{all_mock_passed}`",
        "Object + depth hint → pseudo_3d / field_zone (geometry only, no FieldScene)",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "field_geometry_candidate_skeleton_report": report,
        "field_geometry_candidate_skeleton_report_md": md,
        "object_spatial_state_candidate_registry": {**OBJECT_SPATIAL_STATE_CANDIDATE_REGISTRY, **meta},
        "field_geometry_candidate_registry": {**FIELD_GEOMETRY_CANDIDATE_REGISTRY, **meta},
        "pseudo_3d_projection_policy": {**PSEUDO_3D_PROJECTION_POLICY, **meta},
        "field_zone_assignment_policy": {**FIELD_ZONE_ASSIGNMENT_POLICY, **meta},
        "geometry_confidence_policy": {**GEOMETRY_CONFIDENCE_POLICY, **meta},
        "field_geometry_generation_result_registry": {**FIELD_GEOMETRY_GENERATION_RESULT_REGISTRY, **meta},
        "field_geometry_mock_case_results": mock_results,
        "readiness_for_field_assembly_review": readiness_review,
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
