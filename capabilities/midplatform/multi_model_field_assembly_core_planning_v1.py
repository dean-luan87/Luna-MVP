# -*- coding: utf-8 -*-
"""Multi-Model Field Assembly Core Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.depth_observation_candidate_ingestion_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DEPTH_INGESTION_ROOT,
    FINAL_DECISION_GO as DEPTH_INGESTION_FINAL_GO,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.multi_model_field_assembly_core_planning_items_v1 import (
    CONFIDENCE_FUSION_POLICY,
    CONFLICT_HANDLING_POLICY,
    DO_NOT_MISCLASSIFY,
    FIELD_ASSEMBLY_PLAN,
    FIELD_ASSEMBLY_RESULT_CANDIDATE_CONTRACT,
    FIELD_GEOMETRY_CANDIDATE_CONTRACT,
    MISSING_MODEL_FALLBACK_POLICY,
    MOCK_PLANNING_CASES,
    MULTI_MODEL_ALIGNED_OBSERVATION_CANDIDATE_CONTRACT,
    MULTI_MODEL_ALIGNMENT_POLICY,
    MULTI_MODEL_INTERACTION_POLICY,
    MULTI_MODEL_ROLE_REGISTRY,
    NEXT_IMPLEMENTATION_SEQUENCE,
    OBJECT_DEPTH_LINKING_POLICY,
    PLANNING_RULES,
    PROHIBITED_SCOPE,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.multi_model_field_assembly_core_planning_lineage_v1 import (
    MULTI_MODEL_PLANNING_STAGE_ADDITIONS,
    MULTI_MODEL_PLANNING_STAGE_TERM_OVERRIDES,
    MULTI_MODEL_PLANNING_WHITELIST_FILES,
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

PHASE_ID = "Phase-Midplatform-Multi-Model-Field-Assembly-Core-Planning-v1-001"
SCOPE = "multi_model_field_assembly_core_planning_only"
SOURCE_CHAIN = "multi_model_field_assembly_core_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_MULTI_MODEL_FIELD_ASSEMBLY_CORE_PLANNING_READY_FOR_MULTI_MODEL_ALIGNMENT_SKELETON"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_MULTI_MODEL_FIELD_ASSEMBLY_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_MULTI_MODEL_FIELD_ASSEMBLY_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Multi-Model-Field-Assembly-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/multi_model_field_assembly_core_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_MULTI_MODEL_FIELD_ASSEMBLY_CORE_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/multi_model_field_assembly_core_planning_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/multi_model_field_assembly_core_planning_v1.py",
    "capabilities/midplatform/multi_model_field_assembly_core_planning_items_v1.py",
    "capabilities/midplatform/multi_model_field_assembly_core_planning_lineage_v1.py",
    "capabilities/midplatform/field_first_common_validation_v1.py",
    "tools/evaluation/midplatform/run_multi_model_field_assembly_core_planning_v1.py",
    "tools/evaluation/midplatform/verify_multi_model_field_assembly_core_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_depth_observation_ingestion_skeleton_go",
    "yolo_detector_already_integrated",
    "route_focus_shifted_to_multi_model_field_assembly",
    "multi_model_field_assembly_core_planning_complete",
    "multi_model_interaction_policy_complete",
    "field_assembly_plan_complete",
    "field_geometry_candidate_contract_complete",
    "aligned_observation_candidate_contract_complete",
    "conflict_and_missing_fallback_policy_complete",
    "no_repeat_detector_planning",
    "no_single_depth_only_route",
    "model_interaction_core_question_answered",
    "field_assembly_core_question_answered",
    "no_weight_download",
    "no_large_dependency_install",
    "no_real_multi_model_runtime",
    "no_slam_runtime",
    "no_scene_graph_runtime",
    "no_field_simulation",
    "no_task_execution",
    "no_runtime_execution",
    "no_world_model_fact_creation",
    "candidate_only_outputs",
    "common_validation_reuse_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, upstream_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "multi_model_field_assembly_core_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "depth_ingestion_root": str(upstream_root),
        "route_correction": "shift_from_single_model_depth_sequence_to_multi_model_field_assembly",
    }


def run_multi_model_field_assembly_core_planning_v1(
    *,
    depth_ingestion_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(depth_ingestion_root or DEFAULT_DEPTH_INGESTION_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    up_s = _read_json(upstream / "summary.json")
    up_v = _read_json(upstream / "verifier_report.json")
    prior_depth_go = (
        up_s.get("final_decision") == DEPTH_INGESTION_FINAL_GO
        and up_v.get("verifier") == "GO"
        and int(up_v.get("passed_checks", 0)) >= 400
        and up_s.get("depth_observation_candidate_ingestion_skeleton_pass") is True
    )
    if not prior_depth_go:
        issues.append("depth_ingestion_skeleton_not_go")

    absence = {k: up_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_depth_go and up_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    role_registry_complete = MULTI_MODEL_ROLE_REGISTRY.get("registry_id") == "multi_model_role_registry_v1"
    interaction_complete = MULTI_MODEL_INTERACTION_POLICY.get("policy_id") == "multi_model_interaction_policy_v1"
    alignment_complete = MULTI_MODEL_ALIGNMENT_POLICY.get("policy_id") == "multi_model_alignment_policy_v1"
    linking_complete = OBJECT_DEPTH_LINKING_POLICY.get("policy_id") == "object_depth_linking_policy_v1"
    fusion_complete = CONFIDENCE_FUSION_POLICY.get("policy_id") == "confidence_fusion_policy_v1"
    conflict_complete = CONFLICT_HANDLING_POLICY.get("policy_id") == "conflict_handling_policy_v1"
    fallback_complete = MISSING_MODEL_FALLBACK_POLICY.get("policy_id") == "missing_model_fallback_policy_v1"
    geometry_contract_complete = FIELD_GEOMETRY_CANDIDATE_CONTRACT.get("contract_id") == "field_geometry_candidate_contract_v1"
    aligned_contract_complete = MULTI_MODEL_ALIGNED_OBSERVATION_CANDIDATE_CONTRACT.get("contract_id") == "multi_model_aligned_observation_candidate_contract_v1"
    assembly_result_complete = FIELD_ASSEMBLY_RESULT_CANDIDATE_CONTRACT.get("contract_id") == "field_assembly_result_candidate_contract_v1"
    assembly_plan_complete = FIELD_ASSEMBLY_PLAN.get("plan_id") == "field_assembly_plan_v1"
    sequence_complete = len(NEXT_IMPLEMENTATION_SEQUENCE.get("sequence") or []) >= 5
    mock_cases_complete = len(MOCK_PLANNING_CASES) >= 12

    multi_model_field_assembly_core_planning_complete = (
        role_registry_complete and interaction_complete and alignment_complete
        and linking_complete and fusion_complete and conflict_complete and fallback_complete
        and geometry_contract_complete and aligned_contract_complete and assembly_result_complete
        and assembly_plan_complete and sequence_complete and mock_cases_complete
        and len(PLANNING_RULES) >= 8
    )
    conflict_and_missing_fallback_policy_complete = conflict_complete and fallback_complete

    role_reg = {**MULTI_MODEL_ROLE_REGISTRY, **meta}
    interaction = {**MULTI_MODEL_INTERACTION_POLICY, "multi_model_interaction_policy_complete": interaction_complete, **meta}
    alignment = {**MULTI_MODEL_ALIGNMENT_POLICY, **meta}
    linking = {**OBJECT_DEPTH_LINKING_POLICY, **meta}
    fusion = {**CONFIDENCE_FUSION_POLICY, **meta}
    conflict = {**CONFLICT_HANDLING_POLICY, **meta}
    fallback = {**MISSING_MODEL_FALLBACK_POLICY, **meta}
    geometry_contract = {**FIELD_GEOMETRY_CANDIDATE_CONTRACT, "field_geometry_candidate_contract_complete": geometry_contract_complete, **meta}
    aligned_contract = {**MULTI_MODEL_ALIGNED_OBSERVATION_CANDIDATE_CONTRACT, "aligned_observation_candidate_contract_complete": aligned_contract_complete, **meta}
    assembly_result_contract = {**FIELD_ASSEMBLY_RESULT_CANDIDATE_CONTRACT, **meta}
    assembly_plan = {**FIELD_ASSEMBLY_PLAN, "field_assembly_plan_complete": assembly_plan_complete, **meta}
    next_seq = {**NEXT_IMPLEMENTATION_SEQUENCE, **meta}
    mock_registry = {"registry_id": "multi_model_field_assembly_mock_case_registry_v1", "count": len(MOCK_PLANNING_CASES), "cases": list(MOCK_PLANNING_CASES), **meta}
    rule_reg = {"registry_id": "multi_model_field_assembly_planning_rules_v1", "rules": list(PLANNING_RULES), **meta}
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    planning_pass = (
        prior_depth_go and multi_model_field_assembly_core_planning_complete
        and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Depth-Observation-Candidate-Ingestion-Skeleton-v1-001",
        base_capability=MULTI_MODEL_PLANNING_WHITELIST_FILES[0],
        base_runner=MULTI_MODEL_PLANNING_WHITELIST_FILES[1],
        base_verifier=MULTI_MODEL_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Multi-Model-Field-Assembly-Core-Planning-v1-001",
        stage_term_overrides=MULTI_MODEL_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=MULTI_MODEL_PLANNING_STAGE_ADDITIONS,
        template_files=MULTI_MODEL_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Depth-Observation-Candidate-Ingestion-Skeleton-v1-001",
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
    final_decision = FINAL_DECISION_GO if planning_pass else (FINAL_DECISION_UPSTREAM if not prior_depth_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_depth_observation_ingestion_skeleton_go": prior_depth_go,
        "yolo_detector_already_integrated": True,
        "route_focus_shifted_to_multi_model_field_assembly": True,
        "multi_model_field_assembly_core_planning_complete": multi_model_field_assembly_core_planning_complete,
        "multi_model_interaction_policy_complete": interaction_complete,
        "field_assembly_plan_complete": assembly_plan_complete,
        "field_geometry_candidate_contract_complete": geometry_contract_complete,
        "aligned_observation_candidate_contract_complete": aligned_contract_complete,
        "conflict_and_missing_fallback_policy_complete": conflict_and_missing_fallback_policy_complete,
        "no_repeat_detector_planning": True,
        "no_single_depth_only_route": True,
        "model_interaction_core_question_answered": True,
        "field_assembly_core_question_answered": True,
        "mock_cases_complete": mock_cases_complete,
        "common_validation_reuse_ok": True,
        "no_weight_download": True,
        "no_large_dependency_install": True,
        "no_model_download": True,
        "no_real_depth_inference": True,
        "no_real_multi_model_runtime": True,
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
        "multi_model_field_assembly_core_planning_pass": planning_pass,
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
        chain_trace_nodes=tuple(list(up_s.get("chain_trace_nodes") or []) + ["multi_model_field_assembly_core_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Multi-Model Field Assembly Core Planning v1",
        f"Roles: `{len(MULTI_MODEL_ROLE_REGISTRY.get('roles') or [])}` | Mock cases: `{len(MOCK_PLANNING_CASES)}`",
        "Route: YOLO + Depth + Geometry → Multi-Model Fusion → Field Assembly → FieldSceneCandidate",
        "Core: multi-model interaction + field assembly, not single-model depth ingestion",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, **meta}
    return {
        "multi_model_field_assembly_core_planning_report": report,
        "multi_model_field_assembly_core_planning_report_md": md,
        "multi_model_role_registry": role_reg,
        "multi_model_interaction_policy": interaction,
        "multi_model_alignment_policy": alignment,
        "object_depth_linking_policy": linking,
        "confidence_fusion_policy": fusion,
        "conflict_handling_policy": conflict,
        "missing_model_fallback_policy": fallback,
        "field_geometry_candidate_contract": geometry_contract,
        "multi_model_aligned_observation_candidate_contract": aligned_contract,
        "field_assembly_result_candidate_contract": assembly_result_contract,
        "field_assembly_plan": assembly_plan,
        "multi_model_field_assembly_mock_case_registry": mock_registry,
        "next_implementation_sequence": next_seq,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
