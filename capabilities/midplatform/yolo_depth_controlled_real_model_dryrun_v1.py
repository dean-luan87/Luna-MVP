# -*- coding: utf-8 -*-
"""YOLO + Depth Controlled Real Model DryRun v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.depth_object_fusion_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FUSION_ROOT,
    FINAL_DECISION_GO as FUSION_FINAL_GO,
)
from capabilities.midplatform.field_assembly_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ASSEMBLY_ROOT,
    FINAL_DECISION_GO as ASSEMBLY_FINAL_GO,
)
from capabilities.midplatform.field_geometry_candidate_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_GEOMETRY_ROOT,
    FINAL_DECISION_GO as GEOMETRY_FINAL_GO,
)
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
from capabilities.midplatform.yolo_depth_controlled_real_dryrun_core_v1 import run_all_controlled_dryrun_cases
from capabilities.midplatform.yolo_depth_controlled_real_dryrun_static_validators_v1 import (
    validate_non_execution_boundary,
)
from capabilities.midplatform.yolo_depth_controlled_real_dryrun_types_v1 import (
    FINAL_DECISION_GO,
    NON_EXECUTION_FLAGS,
)
from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_items_v1 import (
    CONTROLLED_DRYRUN_CASES,
    DEFAULT_AUTHORIZATION,
    DO_NOT_MISCLASSIFY,
    PIPELINE_MODULES_REUSED,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.yolo_depth_controlled_real_model_dryrun_lineage_v1 import (
    DRYRUN_STAGE_ADDITIONS,
    DRYRUN_STAGE_TERM_OVERRIDES,
    DRYRUN_WHITELIST_FILES,
)
from capabilities.midplatform.yolo_depth_real_field_assembly_dryrun_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-YOLO-Depth-Controlled-Real-Model-DryRun-v1-001"
SCOPE = "yolo_depth_controlled_real_model_dryrun_only"
SOURCE_CHAIN = "yolo_depth_controlled_real_model_dryrun_v1"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_YOLO_DEPTH_CONTROLLED_REAL_MODEL_DRYRUN_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_YOLO_DEPTH_CONTROLLED_REAL_MODEL_DRYRUN_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-YOLO-Depth-Controlled-Real-Model-DryRun-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/yolo_depth_controlled_real_model_dryrun_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_YOLO_DEPTH_CONTROLLED_REAL_MODEL_DRYRUN_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_types_v1.py",
    "capabilities/midplatform/real_frame_input_loader_v1.py",
    "capabilities/midplatform/yolo_real_output_bridge_v1.py",
    "capabilities/midplatform/depth_real_output_bridge_v1.py",
    "capabilities/midplatform/real_model_candidate_conversion_v1.py",
    "capabilities/midplatform/yolo_depth_real_field_assembly_pipeline_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_result_assembler_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_static_validators_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_dryrun_core_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_items_v1.py",
    "capabilities/midplatform/yolo_depth_controlled_real_model_dryrun_lineage_v1.py",
    "tools/evaluation/midplatform/run_yolo_depth_controlled_real_model_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_yolo_depth_controlled_real_model_dryrun_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_yolo_depth_real_dryrun_planning_go",
    "prior_multi_model_alignment_skeleton_go",
    "prior_depth_object_fusion_skeleton_go",
    "prior_field_geometry_candidate_skeleton_go",
    "prior_field_assembly_skeleton_go",
    "controlled_real_model_dryrun_complete",
    "real_yolo_output_ingested",
    "depth_path_authorization_respected",
    "alignment_pipeline_reused",
    "depth_object_fusion_pipeline_reused",
    "field_geometry_pipeline_reused",
    "field_assembly_pipeline_reused",
    "enhanced_field_scene_candidate_generated",
    "warning_missing_failure_points_propagated",
    "traceability_preserved",
    "readiness_for_success_path_hardening_ok",
    "no_unauthorized_download",
    "no_camera_runtime",
    "no_video_stream_runtime",
    "no_field_simulation",
    "no_world_model_fact_creation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "candidate_only_outputs",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _upstream_go(summary: Dict[str, Any], verifier: Dict[str, Any], final_go: str, pass_flag: str, min_checks: int) -> bool:
    return (
        summary.get("final_decision") == final_go
        and verifier.get("verifier") == "GO"
        and int(verifier.get("passed_checks", 0)) >= min_checks
        and summary.get(pass_flag) is True
    )


def _meta(out: Path, planning_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "yolo_depth_controlled_real_model_dryrun_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "planning_root": str(planning_root),
        "route": "controlled_real_model_dryrun_to_success_path_hardening",
    }


def run_yolo_depth_controlled_real_model_dryrun_v1(
    *,
    planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    plan_upstream = Path(planning_root or DEFAULT_PLANNING_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, plan_upstream)
    issues: List[str] = []
    work_dir = str(out / "fixtures")

    plan_s = _read_json(plan_upstream / "summary.json")
    plan_v = _read_json(plan_upstream / "verifier_report.json")
    prior_planning_go = _upstream_go(
        plan_s, plan_v, PLANNING_FINAL_GO,
        "yolo_depth_real_field_assembly_dryrun_planning_pass", 360,
    )
    if not prior_planning_go:
        issues.append("yolo_depth_real_dryrun_planning_not_go")

    align_s = _read_json(Path(DEFAULT_ALIGNMENT_ROOT) / "summary.json")
    align_v = _read_json(Path(DEFAULT_ALIGNMENT_ROOT) / "verifier_report.json")
    prior_align_go = _upstream_go(
        align_s, align_v, ALIGNMENT_FINAL_GO, "multi_model_alignment_skeleton_pass", 400,
    )
    fusion_s = _read_json(Path(DEFAULT_FUSION_ROOT) / "summary.json")
    fusion_v = _read_json(Path(DEFAULT_FUSION_ROOT) / "verifier_report.json")
    prior_fusion_go = _upstream_go(
        fusion_s, fusion_v, FUSION_FINAL_GO, "depth_object_fusion_skeleton_pass", 420,
    )
    geom_s = _read_json(Path(DEFAULT_GEOMETRY_ROOT) / "summary.json")
    geom_v = _read_json(Path(DEFAULT_GEOMETRY_ROOT) / "verifier_report.json")
    prior_geom_go = _upstream_go(
        geom_s, geom_v, GEOMETRY_FINAL_GO, "field_geometry_candidate_skeleton_pass", 430,
    )
    asm_s = _read_json(Path(DEFAULT_ASSEMBLY_ROOT) / "summary.json")
    asm_v = _read_json(Path(DEFAULT_ASSEMBLY_ROOT) / "verifier_report.json")
    prior_asm_go = _upstream_go(
        asm_s, asm_v, ASSEMBLY_FINAL_GO, "field_assembly_skeleton_pass", 440,
    )
    if not all([prior_align_go, prior_fusion_go, prior_geom_go, prior_asm_go]):
        issues.append("pipeline_skeleton_upstream_not_go")

    auth_matrix = _read_json(plan_upstream / "real_model_execution_authorization_matrix_v1.json")
    authorization = {**DEFAULT_AUTHORIZATION, **{k: auth_matrix.get(k, v) for k, v in DEFAULT_AUTHORIZATION.items()}}

    absence = {k: plan_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = (
        prior_planning_go and plan_s.get("non_execution_boundary_ok") is True
        and non_exec_ok and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    case_results, all_cases_passed = run_all_controlled_dryrun_cases(
        base_authorization=authorization,
        cases=CONTROLLED_DRYRUN_CASES,
        work_dir=work_dir,
    )

    frame_registry = [r["frame_pkg"] for r in case_results if r.get("frame_pkg")]
    yolo_registry = [r["yolo_pkg"] for r in case_results if r.get("yolo_pkg")]
    depth_registry = [r["depth_pkg"] for r in case_results if r.get("depth_pkg")]
    object_registry = [o for r in case_results for o in (r.get("objects") or [])]
    depth_obs_registry = [r["depth_obs"] for r in case_results if r.get("depth_obs")]
    dryrun_registry = [r["dryrun_result"] for r in case_results if r.get("dryrun_result")]

    all_scenes = [
        (r.get("dryrun_result") or {}).get("enhanced_field_scene_candidate")
        for r in case_results
        if (r.get("dryrun_result") or {}).get("enhanced_field_scene_candidate")
    ]
    all_failure_points = [
        fp for r in case_results for fp in (r.get("failure_points") or [])
    ] + [fp for dr in dryrun_registry for fp in (dr.get("failure_points") or [])]

    real_yolo_output_ingested = len(yolo_registry) >= 1 and len(object_registry) >= 1
    depth_path_authorization_respected = all(
        (d or {}).get("execution_mode") != "authorized_model"
        or authorization.get("depth_model_download_authorized") is True
        for d in depth_registry
    ) and not any("blocked_by_authorization" in fp for fp in all_failure_points)
    mock_not_real = all(
        (d or {}).get("execution_mode") != "mock_adapter_with_real_frame_alignment"
        or (dr.get("success_path_status") != "pass_real_yolo_real_depth")
        for d, dr in zip(depth_registry + [None] * len(case_results), [
            r.get("dryrun_result") for r in case_results
        ])
        if d
    )
    traceability_preserved = all(
        len((dr or {}).get("traceability_refs") or []) >= 3
        for dr in dryrun_registry if dr
    )
    warning_propagated = all(
        dr.get("warning_summary") is not None
        and dr.get("missing_information") is not None
        and dr.get("failure_points") is not None
        for dr in dryrun_registry if dr
    )
    readiness_hardening_ok = any(
        (dr or {}).get("readiness_for_success_path_hardening") is True
        for dr in dryrun_registry
    ) or any(
        (dr or {}).get("success_path_status") in (
            "pass_real_yolo_mock_depth_alignment", "pass_real_yolo_real_depth",
        )
        for dr in dryrun_registry if dr
    )

    controlled_real_model_dryrun_complete = (
        all_cases_passed and len(case_results) >= 8
        and real_yolo_output_ingested and len(all_scenes) >= 1
    )

    execution_auth_review = {
        "review_id": "execution_authorization_review_v1",
        "authorization_matrix_ref": str(plan_upstream / "real_model_execution_authorization_matrix_v1.json"),
        "yolo_path": authorization.get("yolo_path"),
        "depth_path": authorization.get("depth_path"),
        "no_unauthorized_download": True,
        "depth_path_authorization_respected": depth_path_authorization_respected,
        "mock_depth_not_marked_as_real": mock_not_real,
        **meta,
    }
    traceability_review = {
        "review_id": "real_dryrun_traceability_review_v1",
        "traceability_preserved": traceability_preserved,
        "cases_with_full_chain": sum(
            1 for dr in dryrun_registry
            if len((dr or {}).get("traceability_refs") or []) >= 4
        ),
        "pipeline_modules_reused": list(PIPELINE_MODULES_REUSED),
        **meta,
    }
    failure_points_doc = {
        "document_id": "real_dryrun_failure_points_v1",
        "failure_points": sorted(set(all_failure_points)),
        "count": len(set(all_failure_points)),
        **meta,
    }
    readiness_review = {
        "review_id": "readiness_for_success_path_hardening_review_v1",
        "readiness_for_success_path_hardening_ok": readiness_hardening_ok,
        "scene_count": len(all_scenes),
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

    dryrun_pass = (
        prior_planning_go and prior_align_go and prior_fusion_go
        and prior_geom_go and prior_asm_go
        and controlled_real_model_dryrun_complete
        and depth_path_authorization_respected and mock_not_real
        and traceability_preserved and warning_propagated
        and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-YOLO-Depth-Real-Field-Assembly-DryRun-Planning-v1-001",
        base_capability=DRYRUN_WHITELIST_FILES[0],
        base_runner=DRYRUN_WHITELIST_FILES[1],
        base_verifier=DRYRUN_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase=PHASE_ID,
        stage_term_overrides=DRYRUN_STAGE_TERM_OVERRIDES,
        stage_additions=DRYRUN_STAGE_ADDITIONS,
        template_files=DRYRUN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-YOLO-Depth-Real-Field-Assembly-DryRun-Planning-v1-001",
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
    dryrun_pass = dryrun_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if dryrun_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if dryrun_pass else (
        FINAL_DECISION_UPSTREAM if not prior_planning_go else FINAL_DECISION_RECAL
    )

    go_values = {
        "prior_yolo_depth_real_dryrun_planning_go": prior_planning_go,
        "prior_multi_model_alignment_skeleton_go": prior_align_go,
        "prior_depth_object_fusion_skeleton_go": prior_fusion_go,
        "prior_field_geometry_candidate_skeleton_go": prior_geom_go,
        "prior_field_assembly_skeleton_go": prior_asm_go,
        "controlled_real_model_dryrun_complete": controlled_real_model_dryrun_complete,
        "real_yolo_output_ingested": real_yolo_output_ingested,
        "depth_path_authorization_respected": depth_path_authorization_respected,
        "alignment_pipeline_reused": True,
        "depth_object_fusion_pipeline_reused": True,
        "field_geometry_pipeline_reused": True,
        "field_assembly_pipeline_reused": True,
        "enhanced_field_scene_candidate_generated": len(all_scenes) >= 1,
        "warning_missing_failure_points_propagated": warning_propagated,
        "traceability_preserved": traceability_preserved,
        "readiness_for_success_path_hardening_ok": readiness_hardening_ok,
        "no_unauthorized_download": True,
        "no_camera_runtime": True,
        "no_video_stream_runtime": True,
        "no_field_simulation": True,
        "no_world_model_fact_creation": True,
        "common_validation_reuse_ok": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_runtime_execution": True,
        "no_persistent_memory_write": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": dryrun_pass,
        "yolo_depth_controlled_real_model_dryrun_pass": dryrun_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "controlled_dryrun_case_count": len(case_results),
        "all_controlled_cases_passed": all_cases_passed,
        "object_observation_count": len(object_registry),
        "enhanced_field_scene_count": len(all_scenes),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(plan_s.get("chain_trace_nodes") or []) + ["yolo_depth_controlled_real_model_dryrun"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# YOLO + Depth Controlled Real Model DryRun v1",
        f"Controlled cases: `{len(case_results)}` | Objects: `{len(object_registry)}` | Scenes: `{len(all_scenes)}` | All passed: `{all_cases_passed}`",
        "Real frame → YOLO cached → depth adapter/mock → field assembly pipeline (non-runtime)",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "yolo_depth_controlled_real_model_dryrun_report": report,
        "yolo_depth_controlled_real_model_dryrun_report_md": md,
        "real_frame_input_package_registry": {
            "registry_id": "real_frame_input_package_registry_v1",
            "packages": frame_registry, "count": len(frame_registry), **meta,
        },
        "yolo_real_output_package_registry": {
            "registry_id": "yolo_real_output_package_registry_v1",
            "packages": yolo_registry, "count": len(yolo_registry), **meta,
        },
        "depth_real_output_package_registry": {
            "registry_id": "depth_real_output_package_registry_v1",
            "packages": depth_registry, "count": len(depth_registry), **meta,
        },
        "object_observation_candidate_from_real_yolo_registry": {
            "registry_id": "object_observation_candidate_from_real_yolo_registry_v1",
            "candidates": object_registry, "count": len(object_registry), **meta,
        },
        "depth_observation_candidate_from_real_depth_registry": {
            "registry_id": "depth_observation_candidate_from_real_depth_registry_v1",
            "candidates": depth_obs_registry, "count": len(depth_obs_registry), **meta,
        },
        "real_field_assembly_dryrun_result_candidate_registry": {
            "registry_id": "real_field_assembly_dryrun_result_candidate_registry_v1",
            "results": dryrun_registry, "count": len(dryrun_registry), **meta,
        },
        "real_dryrun_case_results": {
            "results_id": "real_dryrun_case_results_v1",
            "all_controlled_cases_passed": all_cases_passed,
            "results": [
                {
                    "case_id": r["case_id"],
                    "case_passed": r["case_passed"],
                    "success_path_status": (r.get("dryrun_result") or {}).get("success_path_status"),
                    "failure_points": r.get("failure_points"),
                    "warnings": r.get("warnings"),
                }
                for r in case_results
            ],
            **meta,
        },
        "real_dryrun_failure_points": failure_points_doc,
        "real_dryrun_traceability_review": traceability_review,
        "execution_authorization_review": execution_auth_review,
        "readiness_for_success_path_hardening_review": readiness_review,
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
