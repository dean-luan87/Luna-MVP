# -*- coding: utf-8 -*-
"""Field-First Core Ideal Operation Mechanism and Model Requirement Mapping v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_ideal_operation_mechanism_items_v1 import (
    DO_NOT_MISCLASSIFY,
    IDEAL_OPERATION_MECHANISM,
    MODEL_DOCUMENT_REVIEW_TEMPLATE_FIELDS,
    MODEL_ROOM_ALIGNMENT,
    NEXT_RESEARCH_TARGETS,
    OPERATION_NODES,
    RECOMMENDED_STATUS_OPTIONS,
    REQUIREMENT_MATRIX_FIELDS,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SELF_WORK_VS_MODEL_DEPENDENCY,
)
from capabilities.midplatform.field_first_core_ideal_operation_mechanism_lineage_v1 import (
    FIELD_FIRST_IDEAL_OP_STAGE_ADDITIONS,
    FIELD_FIRST_IDEAL_OP_STAGE_TERM_OVERRIDES,
    FIELD_FIRST_IDEAL_OP_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_role_function_redefinition_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ROLE_REDEF_ROOT,
    FINAL_DECISION_GO as ROLE_REDEF_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Field-First-Core-Ideal-Operation-Mechanism-and-Model-Requirement-Mapping-v1-001"
SCOPE = "field_first_core_ideal_operation_mechanism_only"
SOURCE_CHAIN = "field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_FIRST_CORE_IDEAL_OPERATION_MECHANISM_AND_MODEL_REQUIREMENT_MAPPING_READY_FOR_MODEL_DOCUMENT_CAPABILITY_REVIEW"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_FIRST_CORE_IDEAL_OPERATION_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_FIRST_CORE_IDEAL_OPERATION_BLOCKED_BY_MAPPING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-First-Core-Ideal-Operation-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_IDEAL_OPERATION_MECHANISM_AND_MODEL_REQUIREMENT_MAPPING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_first_core_ideal_operation_mechanism_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1.py",
    "capabilities/midplatform/field_first_core_ideal_operation_mechanism_items_v1.py",
    "capabilities/midplatform/field_first_core_ideal_operation_mechanism_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_field_first_role_redef_go",
    "ideal_operation_mechanism_complete",
    "operation_node_registry_complete",
    "operation_node_model_mapping_complete",
    "model_requirement_matrix_complete",
    "model_document_review_template_complete",
    "model_room_alignment_update_complete",
    "next_research_targets_complete",
    "model_selection_not_executed",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, upstream: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_first_core_ideal_operation_mechanism_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "role_redef_root": str(upstream),
    }


def _build_requirement_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for node in OPERATION_NODES:
        for cap in node.get("required_capabilities") or ():
            rows.append({
                "operation_node_id": node["operation_node_id"],
                "node_role": node.get("node_role", ""),
                "required_capability": cap,
                "acceptable_model_type": node.get("reference_models") or node.get("reference_capabilities") or (),
                "expected_input": "operation_node_specific",
                "expected_output_candidate": node.get("expected_outputs") or (),
                "latency_requirement": "task_dependent",
                "update_frequency": "node_dependent",
                "confidence_required": True,
                "traceability_required": True,
                "failure_modes_required": True,
                "edge_runtime_importance": node.get("model_dependency", "medium"),
                "safety_critical": node["operation_node_id"] in ("field_simulation", "midplatform_reasoning", "drive_layer"),
                "can_be_reference_only": node.get("can_be_reference_only", False),
                "must_have_now": node.get("luna_self_work") == "primary_self_developed",
                "can_defer": node.get("can_be_reference_only", False),
            })
    return rows


def run_field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1(
    *,
    role_redef_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(role_redef_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    role_s = _read_json(upstream / "summary.json")
    role_v = _read_json(upstream / "verifier_report.json")
    role_fs = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_field_first_role_redef_go = (
        role_s.get("final_decision") == ROLE_REDEF_FINAL_GO
        and role_v.get("verifier") == "GO"
        and int(role_v.get("passed_checks", 0)) >= 380
        and role_s.get("field_first_core_role_function_redefinition_pass") is True
    )
    if not prior_field_first_role_redef_go:
        issues.append("field_first_role_redef_not_go")

    absence = {k: role_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_field_first_role_redef_go and role_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    ideal_operation_mechanism_complete = len(IDEAL_OPERATION_MECHANISM.get("chain") or ()) >= 13
    operation_node_registry_complete = len(OPERATION_NODES) >= 12
    operation_node_model_mapping_complete = all(n.get("operation_node_id") for n in OPERATION_NODES)
    matrix_rows = _build_requirement_matrix()
    model_requirement_matrix_complete = len(matrix_rows) >= 50
    model_document_review_template_complete = len(MODEL_DOCUMENT_REVIEW_TEMPLATE_FIELDS) >= 20
    model_room_alignment_update_complete = len(MODEL_ROOM_ALIGNMENT) >= 12
    next_research_targets_complete = len(NEXT_RESEARCH_TARGETS) >= 10
    model_selection_not_executed = True

    ideal_op = {**IDEAL_OPERATION_MECHANISM, "ideal_operation_mechanism_complete": ideal_operation_mechanism_complete, **meta}
    node_reg = {"registry_id": "operation_node_registry_v1", "operation_node_registry_complete": operation_node_registry_complete, "count": len(OPERATION_NODES), "nodes": list(OPERATION_NODES), **meta}
    node_map = {
        "mapping_id": "operation_node_model_mapping_v1",
        "operation_node_model_mapping_complete": operation_node_model_mapping_complete,
        "mappings": [{"operation_node_id": n["operation_node_id"], "reference_models": n.get("reference_models") or n.get("reference_capabilities"), "operation_position": n.get("operation_position", ""), "expected_outputs": n.get("expected_outputs")} for n in OPERATION_NODES],
        **meta,
    }
    matrix = {"matrix_id": "model_requirement_matrix_v1", "model_requirement_matrix_complete": model_requirement_matrix_complete, "fields": list(REQUIREMENT_MATRIX_FIELDS), "row_count": len(matrix_rows), "rows": matrix_rows, **meta}
    doc_template = {
        "template_id": "model_document_review_template_v1",
        "model_document_review_template_complete": model_document_review_template_complete,
        "fields": list(MODEL_DOCUMENT_REVIEW_TEMPLATE_FIELDS),
        "recommended_status_options": list(RECOMMENDED_STATUS_OPTIONS),
        "model_document_review_deferred_to_next_phase": True,
        **meta,
    }
    room_align = {"update_id": "model_room_alignment_update_v1", "model_room_alignment_update_complete": model_room_alignment_update_complete, "alignments": list(MODEL_ROOM_ALIGNMENT), **meta}
    boundary = {"boundary_id": "self_work_vs_model_dependency_boundary_v1", "entries": list(SELF_WORK_VS_MODEL_DEPENDENCY), **meta}
    research = {"targets_id": "next_research_targets_v1", "next_research_targets_complete": next_research_targets_complete, "targets": list(NEXT_RESEARCH_TARGETS), **meta}
    next_route = {
        "decision_id": "next_route_decision_v1",
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "recommended_next_phase": SELECTED_NEXT_PHASE,
        "rationale": "Ideal operation and requirements defined; next review model docs against requirement matrix",
        **meta,
    }
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    mech_pass = (
        prior_field_first_role_redef_go and ideal_operation_mechanism_complete
        and operation_node_registry_complete and operation_node_model_mapping_complete
        and model_requirement_matrix_complete and model_document_review_template_complete
        and model_room_alignment_update_complete and next_research_targets_complete
        and model_selection_not_executed and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-First-Core-Role-Function-Redefinition-v1-001",
        base_capability=FIELD_FIRST_IDEAL_OP_WHITELIST_FILES[0],
        base_runner=FIELD_FIRST_IDEAL_OP_WHITELIST_FILES[1],
        base_verifier=FIELD_FIRST_IDEAL_OP_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-First-Core-Ideal-Operation-Mechanism-and-Model-Requirement-Mapping-v1-001",
        stage_term_overrides=FIELD_FIRST_IDEAL_OP_STAGE_TERM_OVERRIDES,
        stage_additions=FIELD_FIRST_IDEAL_OP_STAGE_ADDITIONS,
        template_files=FIELD_FIRST_IDEAL_OP_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-First-Core-Role-Function-Redefinition-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=role_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    mech_pass = mech_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if mech_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if mech_pass else (FINAL_DECISION_UPSTREAM if not prior_field_first_role_redef_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_field_first_role_redef_go": prior_field_first_role_redef_go,
        "ideal_operation_mechanism_complete": ideal_operation_mechanism_complete,
        "operation_node_registry_complete": operation_node_registry_complete,
        "operation_node_model_mapping_complete": operation_node_model_mapping_complete,
        "model_requirement_matrix_complete": model_requirement_matrix_complete,
        "model_document_review_template_complete": model_document_review_template_complete,
        "model_room_alignment_update_complete": model_room_alignment_update_complete,
        "next_research_targets_complete": next_research_targets_complete,
        "model_selection_not_executed": model_selection_not_executed,
        "ideal_operation_before_model_selection": True,
        "model_requirements_derived_from_operation_nodes": True,
        "model_document_review_deferred_to_next_phase": True,
        "field_first_route_preserved": True,
        "ipc_repositioned_as_source_normalization_asset": True,
        "handoff_contract_p3_defer_remains_defer": True,
        "clm_deferred": True,
        "model_output_candidate_only": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_inference_execution": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_real_field_model_creation": True,
        "no_world_model_fact_creation": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "midplatform_still_has_remaining_work": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": mech_pass,
        "field_first_core_ideal_operation_mechanism_pass": mech_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "operation_node_count": len(OPERATION_NODES),
        "requirement_matrix_row_count": len(matrix_rows),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(role_s.get("chain_trace_nodes") or []) + ["field_first_ideal_operation_mechanism"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Field-First Ideal Operation Mechanism & Model Requirement Mapping v1",
        f"Ideal chain steps: `{len(IDEAL_OPERATION_MECHANISM['chain'])}` | Operation nodes: `{len(OPERATION_NODES)}`",
        f"Requirement matrix rows: `{len(matrix_rows)}` | Research targets: `{len(NEXT_RESEARCH_TARGETS)}`",
        f"Ideal operation before model selection: `True`",
        f"Final decision: `{final_decision}`",
        f"Next: `{next_phase}`",
    ])
    return {
        "ideal_operation_mechanism_report": {**go_values, "final_decision": final_decision, **meta},
        "ideal_operation_mechanism_report_md": md,
        "ideal_operation_mechanism": ideal_op,
        "operation_node_registry": node_reg,
        "operation_node_model_mapping": node_map,
        "model_requirement_matrix": matrix,
        "model_document_review_template": doc_template,
        "model_room_alignment_update": room_align,
        "self_work_vs_model_dependency_boundary": boundary,
        "next_research_targets": research,
        "next_route_decision": next_route,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
