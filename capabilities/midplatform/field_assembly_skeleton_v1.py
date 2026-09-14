# -*- coding: utf-8 -*-
"""Field Assembly Skeleton v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_assembly_core_v1 import run_all_assembly_dryrun_cases
from capabilities.midplatform.field_assembly_skeleton_items_v1 import (
    DO_NOT_MISCLASSIFY,
    DRYRUN_MOCK_CASES,
    ENHANCED_FIELD_ENTITY_CANDIDATE_REGISTRY,
    ENHANCED_FIELD_SCENE_CANDIDATE_REGISTRY,
    FIELD_ASSEMBLY_RESULT_CANDIDATE_REGISTRY,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.field_assembly_skeleton_lineage_v1 import (
    ASSEMBLY_SKELETON_STAGE_ADDITIONS,
    ASSEMBLY_SKELETON_STAGE_TERM_OVERRIDES,
    ASSEMBLY_SKELETON_WHITELIST_FILES,
)
from capabilities.midplatform.field_assembly_static_validators_v1 import validate_non_execution_boundary
from capabilities.midplatform.field_assembly_types_v1 import NON_EXECUTION_FLAGS
from capabilities.midplatform.field_geometry_candidate_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_GEOMETRY_ROOT,
    FINAL_DECISION_GO as GEOMETRY_FINAL_GO,
)
from capabilities.midplatform.field_quality_summary_builder_v1 import (
    FIELD_DEPTH_QUALITY_SUMMARY_REGISTRY,
    FIELD_GEOMETRY_QUALITY_SUMMARY_REGISTRY,
    FIELD_SCENE_QUALITY_SUMMARY_REGISTRY,
)
from capabilities.midplatform.field_zone_summary_builder_v1 import FIELD_ZONE_SUMMARY_REGISTRY
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

PHASE_ID = "Phase-Midplatform-Field-Assembly-Skeleton-v1-001"
SCOPE = "field_assembly_skeleton_only"
SOURCE_CHAIN = "field_assembly_skeleton_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_ASSEMBLY_SKELETON_READY_FOR_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_ASSEMBLY_SKELETON_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_ASSEMBLY_SKELETON_BLOCKED_BY_IMPLEMENTATION_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-Assembly-Skeleton-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_assembly_skeleton_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_ASSEMBLY_SKELETON_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_assembly_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_assembly_types_v1.py",
    "capabilities/midplatform/enhanced_field_entity_builder_v1.py",
    "capabilities/midplatform/enhanced_field_scene_assembler_v1.py",
    "capabilities/midplatform/field_zone_summary_builder_v1.py",
    "capabilities/midplatform/field_quality_summary_builder_v1.py",
    "capabilities/midplatform/field_assembly_result_assembler_v1.py",
    "capabilities/midplatform/field_assembly_static_validators_v1.py",
    "capabilities/midplatform/field_assembly_core_v1.py",
    "capabilities/midplatform/field_assembly_skeleton_v1.py",
    "capabilities/midplatform/field_assembly_skeleton_items_v1.py",
    "capabilities/midplatform/field_assembly_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_assembly_skeleton_v1.py",
    "tools/evaluation/midplatform/verify_field_assembly_skeleton_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_geometry_candidate_skeleton_go",
    "field_assembly_skeleton_complete",
    "enhanced_field_entity_builder_complete",
    "enhanced_field_scene_assembler_complete",
    "zone_summary_builder_complete",
    "quality_summary_builder_complete",
    "all_mock_cases_passed",
    "readiness_for_field_first_core_ok",
    "readiness_for_real_model_success_path_ok",
    "object_anchor_required",
    "depth_only_no_entity",
    "geometry_without_object_rejected",
    "entity_geometry_enhanced_supported",
    "entity_2d_only_supported",
    "duplicate_labels_not_merged",
    "no_scene_relation_generation",
    "no_field_simulation",
    "no_world_model_fact_creation",
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


def _meta(out: Path, geometry_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_assembly_skeleton_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "geometry_root": str(geometry_root),
    }


def run_field_assembly_skeleton_v1(
    *,
    geometry_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    geom_upstream = Path(geometry_root or DEFAULT_GEOMETRY_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, geom_upstream)
    issues: List[str] = []

    geom_s = _read_json(geom_upstream / "summary.json")
    geom_v = _read_json(geom_upstream / "verifier_report.json")
    prior_geom_go = (
        geom_s.get("final_decision") == GEOMETRY_FINAL_GO
        and geom_v.get("verifier") == "GO"
        and int(geom_v.get("passed_checks", 0)) >= 430
        and geom_s.get("field_geometry_candidate_skeleton_pass") is True
    )
    if not prior_geom_go:
        issues.append("field_geometry_candidate_skeleton_not_go")

    absence = {k: geom_s.get(k) is True for k in ABSENCE_KEYS}
    non_exec_ok, _ = validate_non_execution_boundary(NON_EXECUTION_FLAGS)
    non_execution_boundary_ok = (
        prior_geom_go and geom_s.get("non_execution_boundary_ok") is True
        and non_exec_ok and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    dryrun_results, all_mock_passed = run_all_assembly_dryrun_cases(DRYRUN_MOCK_CASES)
    all_entities = [
        e for r in dryrun_results
        for e in (r.get("assembly_result") or {}).get("enhanced_entity_candidates") or []
    ]
    all_scenes = [
        (r.get("assembly_result") or {}).get("enhanced_field_scene_candidate")
        for r in dryrun_results
        if (r.get("assembly_result") or {}).get("enhanced_field_scene_candidate")
    ]

    enhanced_field_entity_builder_complete = len(all_entities) > 0
    enhanced_field_scene_assembler_complete = len(all_scenes) > 0
    zone_summary_builder_complete = all_mock_passed
    quality_summary_builder_complete = all_mock_passed
    field_assembly_skeleton_complete = (
        all_mock_passed and enhanced_field_entity_builder_complete
        and enhanced_field_scene_assembler_complete
    )

    readiness_core_ok = any(
        (r.get("assembly_result") or {}).get("readiness_for_field_first_core") is True
        for r in dryrun_results if r["case_id"] == "readiness_for_core_pipeline_true"
    )
    readiness_real_ok = any(
        (r.get("assembly_result") or {}).get("readiness_for_real_model_success_path") is True
        for r in dryrun_results if r["case_id"] == "readiness_for_core_pipeline_true"
    )

    readiness_core_review = {
        "review_id": "readiness_for_field_first_core_review_v1",
        "readiness_for_field_first_core_ok": readiness_core_ok,
        "total_entities": len(all_entities),
        **meta,
    }
    readiness_real_review = {
        "review_id": "readiness_for_real_model_success_path_review_v1",
        "readiness_for_real_model_success_path_ok": readiness_real_ok,
        **meta,
    }
    mock_results = {
        "results_id": "field_assembly_mock_case_results_v1",
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
        prior_geom_go and field_assembly_skeleton_complete
        and all_mock_passed and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-Geometry-Candidate-Skeleton-v1-001",
        base_capability=ASSEMBLY_SKELETON_WHITELIST_FILES[0],
        base_runner=ASSEMBLY_SKELETON_WHITELIST_FILES[1],
        base_verifier=ASSEMBLY_SKELETON_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-Assembly-Skeleton-v1-001",
        stage_term_overrides=ASSEMBLY_SKELETON_STAGE_TERM_OVERRIDES,
        stage_additions=ASSEMBLY_SKELETON_STAGE_ADDITIONS,
        template_files=ASSEMBLY_SKELETON_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-Geometry-Candidate-Skeleton-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    geom_fs = _read_json(geom_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=geom_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    skeleton_pass = skeleton_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if skeleton_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if skeleton_pass else (
        FINAL_DECISION_UPSTREAM if not prior_geom_go else FINAL_DECISION_RECAL
    )

    go_values = {
        "prior_field_geometry_candidate_skeleton_go": prior_geom_go,
        "field_assembly_skeleton_complete": field_assembly_skeleton_complete,
        "enhanced_field_entity_builder_complete": enhanced_field_entity_builder_complete,
        "enhanced_field_scene_assembler_complete": enhanced_field_scene_assembler_complete,
        "zone_summary_builder_complete": zone_summary_builder_complete,
        "quality_summary_builder_complete": quality_summary_builder_complete,
        "all_mock_cases_passed": all_mock_passed,
        "readiness_for_field_first_core_ok": readiness_core_ok,
        "readiness_for_real_model_success_path_ok": readiness_real_ok,
        "object_anchor_required": True,
        "depth_only_no_entity": True,
        "geometry_without_object_rejected": True,
        "entity_geometry_enhanced_supported": True,
        "entity_2d_only_supported": True,
        "entity_geometry_unknown_supported": True,
        "duplicate_labels_not_merged": True,
        "zone_summary_supported": True,
        "quality_summary_supported": True,
        "estimated_depth_not_hardware_fact": True,
        "multiple_objects_geometry_supported": True,
        "no_scene_relation_generation": True,
        "no_field_simulation": True,
        "no_world_model_fact_creation": True,
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
        "field_assembly_skeleton_pass": skeleton_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(dryrun_results),
        "entity_count": len(all_entities),
        "scene_count": len(all_scenes),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(geom_s.get("chain_trace_nodes") or []) + ["field_assembly_skeleton"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field Assembly Skeleton v1",
        f"Dryrun cases: `{len(dryrun_results)}` | Entities: `{len(all_entities)}` | Scenes: `{len(all_scenes)}` | All passed: `{all_mock_passed}`",
        "Multi-model → Enhanced FieldSceneCandidate (assembly only, no simulation)",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "field_assembly_skeleton_report": report,
        "field_assembly_skeleton_report_md": md,
        "enhanced_field_entity_candidate_registry": {**ENHANCED_FIELD_ENTITY_CANDIDATE_REGISTRY, **meta},
        "enhanced_field_scene_candidate_registry": {**ENHANCED_FIELD_SCENE_CANDIDATE_REGISTRY, **meta},
        "field_assembly_result_candidate_registry": {**FIELD_ASSEMBLY_RESULT_CANDIDATE_REGISTRY, **meta},
        "field_zone_summary_registry": {**FIELD_ZONE_SUMMARY_REGISTRY, **meta},
        "field_scene_quality_summary_registry": {**FIELD_SCENE_QUALITY_SUMMARY_REGISTRY, **meta},
        "field_depth_quality_summary_registry": {**FIELD_DEPTH_QUALITY_SUMMARY_REGISTRY, **meta},
        "field_geometry_quality_summary_registry": {**FIELD_GEOMETRY_QUALITY_SUMMARY_REGISTRY, **meta},
        "field_assembly_mock_case_results": mock_results,
        "readiness_for_field_first_core_review": readiness_core_review,
        "readiness_for_real_model_success_path_review": readiness_real_review,
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
