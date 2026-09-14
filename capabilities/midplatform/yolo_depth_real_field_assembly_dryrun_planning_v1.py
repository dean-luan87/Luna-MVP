# -*- coding: utf-8 -*-
"""YOLO + Depth Real Field Assembly DryRun Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_assembly_skeleton_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ASSEMBLY_ROOT,
    FINAL_DECISION_GO as ASSEMBLY_FINAL_GO,
)
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
from capabilities.midplatform.yolo_depth_real_field_assembly_dryrun_planning_items_v1 import (
    DEPTH_REAL_OUTPUT_PACKAGE_CONTRACT,
    DO_NOT_MISCLASSIFY,
    DRYRUN_FAILURE_POINT_POLICY,
    DRYRUN_PLANNING_CASES,
    DRYRUN_TRACEABILITY_POLICY,
    NEXT_CONTROLLED_DRYRUN_PLAN,
    NON_EXECUTION_FLAGS,
    PIPELINE_CHAIN,
    PLANNING_RULES,
    PROHIBITED_SCOPE,
    REAL_FIELD_ASSEMBLY_DRYRUN_RESULT_CONTRACT,
    REAL_FIELD_ASSEMBLY_SUCCESS_CRITERIA,
    REAL_FRAME_INPUT_PACKAGE_CONTRACT,
    REAL_MODEL_EXECUTION_AUTHORIZATION_MATRIX,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    YOLO_REAL_OUTPUT_PACKAGE_CONTRACT,
)
from capabilities.midplatform.yolo_depth_real_field_assembly_dryrun_planning_lineage_v1 import (
    PLANNING_STAGE_ADDITIONS,
    PLANNING_STAGE_TERM_OVERRIDES,
    PLANNING_WHITELIST_FILES,
)

PHASE_ID = "Phase-Midplatform-YOLO-Depth-Real-Field-Assembly-DryRun-Planning-v1-001"
SCOPE = "yolo_depth_real_field_assembly_dryrun_planning_only"
SOURCE_CHAIN = "yolo_depth_real_field_assembly_dryrun_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING_READY_FOR_CONTROLLED_REAL_MODEL_DRYRUN"
)
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-YOLO-Depth-Real-Field-Assembly-DryRun-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/yolo_depth_real_field_assembly_dryrun_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_v1.py",
    "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_items_v1.py",
    "capabilities/midplatform/yolo_depth_real_field_assembly_dryrun_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_yolo_depth_real_field_assembly_dryrun_planning_v1.py",
    "tools/evaluation/midplatform/verify_yolo_depth_real_field_assembly_dryrun_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_assembly_skeleton_go",
    "yolo_depth_real_field_assembly_dryrun_planning_complete",
    "success_criteria_complete",
    "real_input_output_contracts_complete",
    "dryrun_case_registry_complete",
    "authorization_matrix_complete",
    "traceability_policy_complete",
    "controlled_dryrun_plan_complete",
    "yolo_already_integrated_acknowledged",
    "depth_model_or_adapter_required",
    "controlled_dryrun_deferred_to_next_phase",
    "no_real_model_execution",
    "no_field_simulation",
    "no_world_model_fact_creation",
    "common_validation_reuse_ok",
    "no_model_download",
    "no_weight_download",
    "no_runtime_execution",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _validate_non_execution(flags: Dict[str, bool]) -> bool:
    return all(flags.get(k) is True for k in NON_EXECUTION_FLAGS)


def _meta(out: Path, assembly_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "yolo_depth_real_field_assembly_dryrun_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "assembly_root": str(assembly_root),
        "route": "mock_skeleton_to_real_input_dryrun_planning",
    }


def run_yolo_depth_real_field_assembly_dryrun_planning_v1(
    *,
    assembly_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    asm_upstream = Path(assembly_root or DEFAULT_ASSEMBLY_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, asm_upstream)
    issues: List[str] = []

    asm_s = _read_json(asm_upstream / "summary.json")
    asm_v = _read_json(asm_upstream / "verifier_report.json")
    prior_asm_go = (
        asm_s.get("final_decision") == ASSEMBLY_FINAL_GO
        and asm_v.get("verifier") == "GO"
        and int(asm_v.get("passed_checks", 0)) >= 440
        and asm_s.get("field_assembly_skeleton_pass") is True
    )
    if not prior_asm_go:
        issues.append("field_assembly_skeleton_not_go")

    absence = {k: asm_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = (
        prior_asm_go and asm_s.get("non_execution_boundary_ok") is True
        and _validate_non_execution(NON_EXECUTION_FLAGS) and all(absence.values())
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    frame_contract_ok = REAL_FRAME_INPUT_PACKAGE_CONTRACT.get("contract_id") == "real_frame_input_package_contract_v1"
    yolo_contract_ok = YOLO_REAL_OUTPUT_PACKAGE_CONTRACT.get("contract_id") == "yolo_real_output_package_contract_v1"
    depth_contract_ok = DEPTH_REAL_OUTPUT_PACKAGE_CONTRACT.get("contract_id") == "depth_real_output_package_contract_v1"
    result_contract_ok = REAL_FIELD_ASSEMBLY_DRYRUN_RESULT_CONTRACT.get("contract_id") == "real_field_assembly_dryrun_result_candidate_contract_v1"
    real_input_output_contracts_complete = all([
        frame_contract_ok, yolo_contract_ok, depth_contract_ok, result_contract_ok,
    ])

    success_criteria_complete = REAL_FIELD_ASSEMBLY_SUCCESS_CRITERIA.get("criteria_id") == "real_field_assembly_success_criteria_v1"
    dryrun_case_registry_complete = len(DRYRUN_PLANNING_CASES) >= 8
    authorization_matrix_complete = REAL_MODEL_EXECUTION_AUTHORIZATION_MATRIX.get("matrix_id") == "real_model_execution_authorization_matrix_v1"
    traceability_policy_complete = DRYRUN_TRACEABILITY_POLICY.get("policy_id") == "dryrun_traceability_policy_v1"
    failure_policy_complete = DRYRUN_FAILURE_POINT_POLICY.get("policy_id") == "dryrun_failure_point_policy_v1"
    controlled_dryrun_plan_complete = NEXT_CONTROLLED_DRYRUN_PLAN.get("plan_id") == "next_controlled_dryrun_plan_v1"

    yolo_depth_real_field_assembly_dryrun_planning_complete = (
        real_input_output_contracts_complete and success_criteria_complete
        and dryrun_case_registry_complete and authorization_matrix_complete
        and traceability_policy_complete and failure_policy_complete
        and controlled_dryrun_plan_complete and len(PLANNING_RULES) >= 8
    )

    dryrun_registry = {
        "registry_id": "yolo_depth_real_dryrun_case_registry_v1",
        "count": len(DRYRUN_PLANNING_CASES),
        "cases": list(DRYRUN_PLANNING_CASES),
        "pipeline_chain": list(PIPELINE_CHAIN),
        **meta,
    }
    non_exec_review = {
        "review_id": "non_execution_boundary_review_v1",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "flags": dict(NON_EXECUTION_FLAGS),
        "controlled_dryrun_deferred_to_next_phase": True,
        **meta,
    }
    prohibited = {**PROHIBITED_SCOPE, **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    planning_pass = (
        prior_asm_go and yolo_depth_real_field_assembly_dryrun_planning_complete
        and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-Assembly-Skeleton-v1-001",
        base_capability=PLANNING_WHITELIST_FILES[0],
        base_runner=PLANNING_WHITELIST_FILES[1],
        base_verifier=PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-YOLO-Depth-Real-Field-Assembly-DryRun-Planning-v1-001",
        stage_term_overrides=PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=PLANNING_STAGE_ADDITIONS,
        template_files=PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-Assembly-Skeleton-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    asm_fs = _read_json(asm_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=asm_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    planning_pass = planning_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if planning_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if planning_pass else (
        FINAL_DECISION_UPSTREAM if not prior_asm_go else FINAL_DECISION_RECAL
    )

    go_values = {
        "prior_field_assembly_skeleton_go": prior_asm_go,
        "yolo_depth_real_field_assembly_dryrun_planning_complete": yolo_depth_real_field_assembly_dryrun_planning_complete,
        "success_criteria_complete": success_criteria_complete,
        "real_input_output_contracts_complete": real_input_output_contracts_complete,
        "dryrun_case_registry_complete": dryrun_case_registry_complete,
        "authorization_matrix_complete": authorization_matrix_complete,
        "traceability_policy_complete": traceability_policy_complete,
        "failure_point_policy_complete": failure_policy_complete,
        "controlled_dryrun_plan_complete": controlled_dryrun_plan_complete,
        "yolo_already_integrated_acknowledged": YOLO_REAL_OUTPUT_PACKAGE_CONTRACT.get("yolo_already_integrated") is True,
        "depth_model_or_adapter_required": True,
        "controlled_dryrun_deferred_to_next_phase": True,
        "no_real_model_execution": True,
        "no_real_yolo_execution": True,
        "no_real_depth_execution": True,
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
        "next_phase_readiness_ok": planning_pass,
        "yolo_depth_real_field_assembly_dryrun_planning_pass": planning_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "dryrun_case_count": len(DRYRUN_PLANNING_CASES),
        "planning_rule_count": len(PLANNING_RULES),
        "readiness_for_field_first_core_upstream": asm_s.get("readiness_for_field_first_core_ok") is True,
        "readiness_for_real_model_success_path_upstream": asm_s.get("readiness_for_real_model_success_path_ok") is True,
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        "midplatform_still_has_remaining_work": True,
        **absence,
    }

    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS if k in go_values},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(asm_s.get("chain_trace_nodes") or []) + ["yolo_depth_real_field_assembly_dryrun_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# YOLO + Depth Real Field Assembly DryRun Planning v1",
        f"Planning cases: `{len(DRYRUN_PLANNING_CASES)}` | Pipeline stages: `{len(PIPELINE_CHAIN)}`",
        "Planning only — no real model execution in this phase",
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "final_decision": final_decision, "planning_rules": list(PLANNING_RULES), **meta}
    return {
        "yolo_depth_real_field_assembly_dryrun_planning_report": report,
        "yolo_depth_real_field_assembly_dryrun_planning_report_md": md,
        "real_frame_input_package_contract": {**REAL_FRAME_INPUT_PACKAGE_CONTRACT, **meta},
        "yolo_real_output_package_contract": {**YOLO_REAL_OUTPUT_PACKAGE_CONTRACT, **meta},
        "depth_real_output_package_contract": {**DEPTH_REAL_OUTPUT_PACKAGE_CONTRACT, **meta},
        "real_field_assembly_dryrun_result_candidate_contract": {**REAL_FIELD_ASSEMBLY_DRYRUN_RESULT_CONTRACT, **meta},
        "real_field_assembly_success_criteria": {**REAL_FIELD_ASSEMBLY_SUCCESS_CRITERIA, **meta},
        "yolo_depth_real_dryrun_case_registry": dryrun_registry,
        "real_model_execution_authorization_matrix": {**REAL_MODEL_EXECUTION_AUTHORIZATION_MATRIX, **meta},
        "dryrun_failure_point_policy": {**DRYRUN_FAILURE_POINT_POLICY, **meta},
        "dryrun_traceability_policy": {**DRYRUN_TRACEABILITY_POLICY, **meta},
        "next_controlled_dryrun_plan": {**NEXT_CONTROLLED_DRYRUN_PLAN, **meta},
        "non_execution_boundary_review": non_exec_review,
        "prohibited_scope": prohibited,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
