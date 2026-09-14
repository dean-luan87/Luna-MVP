# -*- coding: utf-8 -*-
"""Field Construction Depth / Geometry Model Integration Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_construction_depth_geometry_model_integration_items_v1 import (
    DEPTH_MODEL_ADAPTER_PLAN,
    DEPTH_OBSERVATION_CANDIDATE_CONTRACT,
    DEPTH_UNRELIABLE_FALLBACK_POLICY,
    DO_NOT_MISCLASSIFY,
    DOWNLOAD_AUTHORIZATION_STATUS,
    FIELD_CONSTRUCTION_MODEL_PRIORITY_PLAN,
    FIELD_GEOMETRY_ADAPTER_PLAN,
    FIELD_GEOMETRY_CANDIDATE_CONTRACT,
    FIELD_SCENE_ENHANCEMENT_PLAN,
    MOCK_PLANNING_CASES,
    OBJECT_DEPTH_HINT_CANDIDATE_CONTRACT,
    P0_DEPTH_MODELS,
    P2_DEFERRED,
    PLANNING_RULES,
    PROHIBITED_SCOPE,
    SCENE_GRAPH_CANDIDATE_REVIEW,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SLAM_CANDIDATE_REVIEW,
    SPATIAL_RELATION_CANDIDATE_CONTRACT,
    YOLO_DEPTH_FUSION_MAPPING,
)
from capabilities.midplatform.field_construction_depth_geometry_model_integration_lineage_v1 import (
    DEPTH_GEOMETRY_PLANNING_STAGE_ADDITIONS,
    DEPTH_GEOMETRY_PLANNING_STAGE_TERM_OVERRIDES,
    DEPTH_GEOMETRY_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.real_observation_candidate_ingestion_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_INGESTION_ROOT,
    FINAL_DECISION_GO as INGESTION_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Field-Construction-Depth-Geometry-Model-Integration-Planning-v1-001"
SCOPE = "field_construction_depth_geometry_model_integration_planning_only"
SOURCE_CHAIN = "field_construction_depth_geometry_model_integration_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_CONSTRUCTION_DEPTH_GEOMETRY_MODEL_INTEGRATION_PLANNING_READY_FOR_DEPTH_OBSERVATION_CANDIDATE_INGESTION_SKELETON"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_CONSTRUCTION_DEPTH_GEOMETRY_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_CONSTRUCTION_DEPTH_GEOMETRY_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-Construction-Depth-Geometry-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_construction_depth_geometry_model_integration_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_CONSTRUCTION_DEPTH_GEOMETRY_MODEL_INTEGRATION_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_construction_depth_geometry_model_integration_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_construction_depth_geometry_model_integration_planning_v1.py",
    "capabilities/midplatform/field_construction_depth_geometry_model_integration_items_v1.py",
    "capabilities/midplatform/field_construction_depth_geometry_model_integration_lineage_v1.py",
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "tools/evaluation/midplatform/run_field_construction_depth_geometry_model_integration_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_construction_depth_geometry_model_integration_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_real_observation_ingestion_skeleton_go",
    "field_construction_depth_geometry_model_integration_planning_complete",
    "depth_model_adapter_plan_complete",
    "depth_observation_candidate_contract_complete",
    "object_depth_hint_candidate_contract_complete",
    "field_geometry_candidate_contract_complete",
    "yolo_depth_fusion_mapping_complete",
    "spatial_relation_candidate_contract_complete",
    "field_construction_model_priority_plan_complete",
    "depth_unreliable_fallback_policy_complete",
    "no_repeat_detector_planning",
    "no_weight_download",
    "no_large_dependency_install",
    "no_production_depth_model_selection",
    "no_slam_runtime",
    "no_scene_graph_runtime",
    "no_field_simulation",
    "no_task_execution",
    "no_runtime_execution",
    "no_world_model_fact_creation",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
    "first_batch_scope_limited_to_depth_and_geometry",
    "yolo_depth_alignment_defined",
    "pseudo_3d_field_scene_path_defined",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, ingestion_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_construction_depth_geometry_model_integration_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "ingestion_root": str(ingestion_root),
        "route_correction": "shift_from_detector_to_field_construction_depth_geometry",
    }


def run_field_construction_depth_geometry_model_integration_planning_v1(
    *,
    ingestion_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(ingestion_root or DEFAULT_INGESTION_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    up_s = _read_json(upstream / "summary.json")
    up_v = _read_json(upstream / "verifier_report.json")
    prior_ingestion_go = (
        up_s.get("final_decision") == INGESTION_FINAL_GO
        and up_v.get("verifier") == "GO"
        and int(up_v.get("passed_checks", 0)) >= 380
        and up_s.get("real_observation_candidate_ingestion_skeleton_pass") is True
    )
    if not prior_ingestion_go:
        issues.append("ingestion_skeleton_not_go")

    absence = {k: up_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_ingestion_go and up_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    depth_model_adapter_plan_complete = (
        DEPTH_MODEL_ADAPTER_PLAN.get("candidate_only") is True
        and DEPTH_MODEL_ADAPTER_PLAN.get("near_term_primary") == "depth_anything_v2"
    )
    depth_observation_contract_complete = DEPTH_OBSERVATION_CANDIDATE_CONTRACT.get("contract_id") == "depth_observation_candidate_contract_v1"
    object_depth_hint_contract_complete = OBJECT_DEPTH_HINT_CANDIDATE_CONTRACT.get("contract_id") == "object_depth_hint_candidate_contract_v1"
    field_geometry_contract_complete = FIELD_GEOMETRY_CANDIDATE_CONTRACT.get("contract_id") == "field_geometry_candidate_contract_v1"
    yolo_depth_fusion_complete = YOLO_DEPTH_FUSION_MAPPING.get("mapping_id") == "yolo_depth_fusion_mapping_v1"
    spatial_relation_contract_complete = SPATIAL_RELATION_CANDIDATE_CONTRACT.get("contract_id") == "spatial_relation_candidate_contract_v1"
    priority_plan_complete = FIELD_CONSTRUCTION_MODEL_PRIORITY_PLAN.get("no_repeat_detector_planning") is True
    depth_fallback_complete = "when_depth_missing" in DEPTH_UNRELIABLE_FALLBACK_POLICY
    mock_cases_complete = len(MOCK_PLANNING_CASES) >= 10

    field_construction_depth_geometry_model_integration_planning_complete = (
        depth_model_adapter_plan_complete and depth_observation_contract_complete
        and object_depth_hint_contract_complete and field_geometry_contract_complete
        and yolo_depth_fusion_complete and spatial_relation_contract_complete
        and priority_plan_complete and depth_fallback_complete and mock_cases_complete
        and len(P0_DEPTH_MODELS) >= 3 and len(PLANNING_RULES) >= 8
    )

    depth_plan = {**DEPTH_MODEL_ADAPTER_PLAN, "depth_model_adapter_plan_complete": depth_model_adapter_plan_complete, "p0_depth_models": list(P0_DEPTH_MODELS), "p2_deferred": list(P2_DEFERRED), **meta}
    depth_obs_contract = {**DEPTH_OBSERVATION_CANDIDATE_CONTRACT, "depth_observation_candidate_contract_complete": depth_observation_contract_complete, **meta}
    depth_hint_contract = {**OBJECT_DEPTH_HINT_CANDIDATE_CONTRACT, "object_depth_hint_candidate_contract_complete": object_depth_hint_contract_complete, **meta}
    field_geom_contract = {**FIELD_GEOMETRY_CANDIDATE_CONTRACT, "field_geometry_candidate_contract_complete": field_geometry_contract_complete, **meta}
    fusion_mapping = {**YOLO_DEPTH_FUSION_MAPPING, "yolo_depth_fusion_mapping_complete": yolo_depth_fusion_complete, **meta}
    spatial_contract = {**SPATIAL_RELATION_CANDIDATE_CONTRACT, "spatial_relation_candidate_contract_complete": spatial_relation_contract_complete, **meta}
    priority_plan = {**FIELD_CONSTRUCTION_MODEL_PRIORITY_PLAN, "field_construction_model_priority_plan_complete": priority_plan_complete, **meta}
    geometry_adapter = {**FIELD_GEOMETRY_ADAPTER_PLAN, **meta}
    depth_fallback = {**DEPTH_UNRELIABLE_FALLBACK_POLICY, "depth_unreliable_fallback_policy_complete": depth_fallback_complete, **meta}
    slam_review = {**SLAM_CANDIDATE_REVIEW, **meta}
    scene_graph_review = {**SCENE_GRAPH_CANDIDATE_REVIEW, **meta}
    field_scene_enhancement = {**FIELD_SCENE_ENHANCEMENT_PLAN, **meta}
    download_status = {**DOWNLOAD_AUTHORIZATION_STATUS, **meta}
    mock_registry = {"registry_id": "field_construction_planning_case_registry_v1", "count": len(MOCK_PLANNING_CASES), "cases": list(MOCK_PLANNING_CASES), **meta}
    rule_reg = {"registry_id": "field_construction_planning_rules_v1", "rules": list(PLANNING_RULES), **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    planning_pass = (
        prior_ingestion_go and field_construction_depth_geometry_model_integration_planning_complete
        and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Real-Observation-Candidate-Ingestion-Skeleton-v1-001",
        base_capability=DEPTH_GEOMETRY_PLANNING_WHITELIST_FILES[0],
        base_runner=DEPTH_GEOMETRY_PLANNING_WHITELIST_FILES[1],
        base_verifier=DEPTH_GEOMETRY_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-Construction-Depth-Geometry-Model-Integration-Planning-v1-001",
        stage_term_overrides=DEPTH_GEOMETRY_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=DEPTH_GEOMETRY_PLANNING_STAGE_ADDITIONS,
        template_files=DEPTH_GEOMETRY_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Real-Observation-Candidate-Ingestion-Skeleton-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    up_fs = _read_json(upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=up_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    planning_pass = planning_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if planning_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if planning_pass else (FINAL_DECISION_UPSTREAM if not prior_ingestion_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_real_observation_ingestion_skeleton_go": prior_ingestion_go,
        "field_construction_depth_geometry_model_integration_planning_complete": field_construction_depth_geometry_model_integration_planning_complete,
        "depth_model_adapter_plan_complete": depth_model_adapter_plan_complete,
        "depth_observation_candidate_contract_complete": depth_observation_contract_complete,
        "object_depth_hint_candidate_contract_complete": object_depth_hint_contract_complete,
        "field_geometry_candidate_contract_complete": field_geometry_contract_complete,
        "yolo_depth_fusion_mapping_complete": yolo_depth_fusion_complete,
        "spatial_relation_candidate_contract_complete": spatial_relation_contract_complete,
        "field_construction_model_priority_plan_complete": priority_plan_complete,
        "depth_unreliable_fallback_policy_complete": depth_fallback_complete,
        "mock_cases_complete": mock_cases_complete,
        "common_validation_reuse_ok": True,
        "no_repeat_detector_planning": True,
        "first_batch_scope_limited_to_depth_and_geometry": True,
        "yolo_depth_alignment_defined": True,
        "pseudo_3d_field_scene_path_defined": True,
        "depth_anything_v2_primary_candidate": True,
        "slam_candidates_future_review_only": True,
        "scene_graph_candidates_future_review_only": True,
        "no_weight_download": True,
        "no_large_dependency_install": True,
        "no_production_depth_model_selection": True,
        "no_model_download": True,
        "no_real_inference_execution": True,
        "no_slam_runtime": True,
        "no_scene_graph_runtime": True,
        "no_field_simulation": True,
        "no_final_action_output": True,
        "no_task_execution": True,
        "no_runtime_execution": True,
        "no_world_model_fact_creation": True,
        "no_persistent_memory_write": True,
        "no_integration_test": True,
        "candidate_only_outputs": True,
        "field_first_route_preserved": True,
        "field_core_pipeline_unchanged": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": planning_pass,
        "field_construction_depth_geometry_model_integration_planning_pass": planning_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "mock_case_count": len(MOCK_PLANNING_CASES),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(up_s.get("chain_trace_nodes") or []) + ["field_construction_depth_geometry_model_integration_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field Construction Depth / Geometry Model Integration Planning v1",
        f"P0 depth models: `{len(P0_DEPTH_MODELS)}` | P2 deferred: `{len(P2_DEFERRED)}` | Planning cases: `{len(MOCK_PLANNING_CASES)}`",
        "Route: YOLO bbox → Depth Model → object_depth_hint → pseudo_3d → field_zone → FieldSceneCandidate",
        "SLAM / Scene Graph: future review only, not near-term integration",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "field_construction_depth_geometry_model_integration_planning_report": report,
        "field_construction_depth_geometry_model_integration_planning_report_md": md,
        "depth_model_adapter_plan": depth_plan,
        "depth_observation_candidate_contract": depth_obs_contract,
        "object_depth_hint_candidate_contract": depth_hint_contract,
        "field_geometry_candidate_contract": field_geom_contract,
        "yolo_depth_fusion_mapping": fusion_mapping,
        "spatial_relation_candidate_contract": spatial_contract,
        "field_construction_model_priority_plan": priority_plan,
        "field_geometry_adapter_plan": geometry_adapter,
        "depth_unreliable_fallback_execution_policy": depth_fallback,
        "streaming_3d_slam_candidate_review": slam_review,
        "scene_graph_spatial_relation_review": scene_graph_review,
        "field_scene_candidate_enhancement_plan": field_scene_enhancement,
        "depth_model_download_authorization_status": download_status,
        "field_construction_planning_case_registry": mock_registry,
        "field_construction_planning_rules": rule_reg,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
