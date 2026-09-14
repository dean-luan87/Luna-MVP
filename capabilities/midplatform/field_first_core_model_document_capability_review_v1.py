# -*- coding: utf-8 -*-
"""Field-First Core Model Document Capability Review v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1 import (
    DEFAULT_OUTPUT as DEFAULT_IDEAL_OP_ROOT,
    FINAL_DECISION_GO as IDEAL_OP_FINAL_GO,
)
from capabilities.midplatform.field_first_core_model_document_capability_review_items_v1 import (
    DO_NOT_MISCLASSIFY,
    MODEL_REVIEW_ITEMS,
    OPERATION_NODES_COVERED,
    REVIEW_ITEM_FIELDS,
    REVIEW_PRINCIPLES,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.field_first_core_model_document_capability_review_lineage_v1 import (
    FIELD_FIRST_DOC_REVIEW_STAGE_ADDITIONS,
    FIELD_FIRST_DOC_REVIEW_STAGE_TERM_OVERRIDES,
    FIELD_FIRST_DOC_REVIEW_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_model_preinstall_plan_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PREINSTALL_ROOT,
    FINAL_DECISION_GO as PREINSTALL_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Field-First-Core-Model-Document-Capability-Review-v1-001"
SCOPE = "field_first_core_model_document_review_only"
SOURCE_CHAIN = "field_first_core_model_document_capability_review_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_DOCUMENT_CAPABILITY_REVIEW_READY_FOR_ADAPTER_PRIORITY_AND_DOWNLOAD_AUTHORIZATION_PLANNING"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_DOCUMENT_REVIEW_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_FIRST_CORE_MODEL_DOCUMENT_REVIEW_BLOCKED_BY_REVIEW_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-First-Core-Model-Document-Review-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_first_core_model_document_capability_review_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_MODEL_DOCUMENT_CAPABILITY_REVIEW_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_first_core_model_document_capability_review_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_model_document_capability_review_v1.py",
    "capabilities/midplatform/field_first_core_model_document_capability_review_items_v1.py",
    "capabilities/midplatform/field_first_core_model_document_capability_review_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_model_document_capability_review_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_model_document_capability_review_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_ideal_operation_go",
    "prior_model_preinstall_plan_go",
    "model_document_capability_review_complete",
    "review_item_registry_complete",
    "operation_node_model_fit_matrix_complete",
    "model_requirement_satisfaction_matrix_complete",
    "model_status_classification_complete",
    "download_authorization_all_false",
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


def _meta(out: Path, preinstall_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_first_core_model_document_review_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "preinstall_root": str(preinstall_root),
    }


def _upstream_go(path: Path, final_go: str, pass_key: str, min_checks: int) -> bool:
    s, v = _read_json(path / "summary.json"), _read_json(path / "verifier_report.json")
    return s.get("final_decision") == final_go and v.get("verifier") == "GO" and int(v.get("passed_checks", 0)) >= min_checks and s.get(pass_key) is True


def _classify(items: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    return [i for i in items if i.get("recommended_status") == status]


def run_field_first_core_model_document_capability_review_v1(
    *,
    preinstall_root: str,
    ideal_operation_root: str = DEFAULT_IDEAL_OP_ROOT,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    preinstall_upstream = Path(preinstall_root or DEFAULT_PREINSTALL_ROOT).expanduser().resolve()
    ideal_upstream = Path(ideal_operation_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, preinstall_upstream)
    issues: List[str] = []

    prior_ideal_operation_go = _upstream_go(ideal_upstream, IDEAL_OP_FINAL_GO, "field_first_core_ideal_operation_mechanism_pass", 380)
    prior_model_preinstall_plan_go = _upstream_go(preinstall_upstream, PREINSTALL_FINAL_GO, "field_first_core_model_preinstall_plan_pass", 420)
    if not prior_ideal_operation_go:
        issues.append("ideal_operation_not_go")
    if not prior_model_preinstall_plan_go:
        issues.append("preinstall_plan_not_go")

    preinstall_s = _read_json(preinstall_upstream / "summary.json")
    absence = {k: preinstall_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_model_preinstall_plan_go and preinstall_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    items = [dict(i) for i in MODEL_REVIEW_ITEMS]
    review_item_registry_complete = len(items) >= 20
    rooms_covered = len({i["model_room"] for i in items}) >= 8
    nodes_covered = len({n for i in items for n in i.get("operation_node_refs", [])}) >= 10
    all_status_assigned = all(i.get("recommended_status") for i in items)
    model_document_capability_review_complete = review_item_registry_complete and rooms_covered and nodes_covered and all_status_assigned

    fit_rows = [{"operation_node_id": n, "models": [i["model_project_id"] for i in items if n in i.get("operation_node_refs", [])]} for n in OPERATION_NODES_COVERED]
    operation_node_model_fit_matrix_complete = len(fit_rows) >= 10

    sat_rows = [{"model_project_id": i["model_project_id"], "satisfies_phase1_minimum": i.get("satisfies_phase1_minimum"), "missing": i.get("missing_required_capabilities"), "status": i.get("recommended_status")} for i in items]
    model_requirement_satisfaction_matrix_complete = len(sat_rows) >= 20

    near_term = _classify(items, "candidate_for_near_term_adapter")
    future = _classify(items, "candidate_for_future_adapter")
    reference = _classify(items, "reference_only")
    unsuitable = [i for i in items if i.get("recommended_status") in ("unsuitable_for_phase_1", "deferred_due_to_runtime_cost", "deferred_due_to_missing_outputs")]

    gaps = [{"model_project_id": i["model_project_id"], "gaps": i.get("missing_required_capabilities"), "reason": i.get("reason_for_status")} for i in items if i.get("missing_required_capabilities")]
    risks = [{"model_project_id": i["model_project_id"], "integration_risk": i.get("integration_risk"), "runtime_risk": i.get("runtime_risk"), "hardware_risk": i.get("hardware_risk"), "governance_risk": i.get("governance_risk")} for i in items]

    download_rec = {
        "recommendation_id": "download_authorization_recommendation_v1",
        "download_authorization_all_false": True,
        "entries": [{"model_project_id": i["model_project_id"], "download_authorized": False, "recommendation": "keep_false_until_adapter_priority_planning"} for i in items],
        **meta,
    }
    adapter_prio = {
        "recommendation_id": "adapter_priority_recommendation_v1",
        "priority_order": [i["model_project_id"] for i in near_term] + [i["model_project_id"] for i in future],
        "note": "planning_only_not_runtime_adapter_creation",
        **meta,
    }

    model_status_classification_complete = all_status_assigned and len(near_term) + len(future) + len(reference) + len(unsuitable) == len(items)

    registry = {"registry_id": "model_review_item_registry_v1", "review_item_registry_complete": review_item_registry_complete, "count": len(items), "fields": list(REVIEW_ITEM_FIELDS), "items": items, **meta}
    fit_matrix = {"matrix_id": "operation_node_model_fit_matrix_v1", "operation_node_model_fit_matrix_complete": operation_node_model_fit_matrix_complete, "rows": fit_rows, **meta}
    sat_matrix = {"matrix_id": "model_requirement_satisfaction_matrix_v1", "model_requirement_satisfaction_matrix_complete": model_requirement_satisfaction_matrix_complete, "rows": sat_rows, **meta}
    near_matrix = {"matrix_id": "near_term_adapter_candidate_matrix_v1", "candidates": near_term, **meta}
    future_matrix = {"matrix_id": "future_adapter_candidate_matrix_v1", "candidates": future, **meta}
    ref_matrix = {"matrix_id": "reference_only_model_matrix_v1", "models": reference, **meta}
    defer_matrix = {"matrix_id": "unsuitable_or_deferred_model_matrix_v1", "models": unsuitable, **meta}
    gap_reg = {"register_id": "model_document_gap_register_v1", "gaps": gaps, **meta}
    risk_reg = {"register_id": "model_risk_register_v1", "risks": risks, **meta}
    next_route = {"decision_id": "next_route_decision_v1", "selected_next_route": SELECTED_NEXT_ROUTE, "recommended_next_phase": SELECTED_NEXT_PHASE, "rationale": "Document review complete; next plan adapter priority and download authorization", **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    review_pass = (
        prior_ideal_operation_go and prior_model_preinstall_plan_go and model_document_capability_review_complete
        and review_item_registry_complete and operation_node_model_fit_matrix_complete
        and model_requirement_satisfaction_matrix_complete and model_status_classification_complete
        and download_rec["download_authorization_all_false"] and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-First-Core-Model-Preinstall-Plan-and-Cache-Manifest-Prepare-v1-001",
        base_capability=FIELD_FIRST_DOC_REVIEW_WHITELIST_FILES[0],
        base_runner=FIELD_FIRST_DOC_REVIEW_WHITELIST_FILES[1],
        base_verifier=FIELD_FIRST_DOC_REVIEW_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-First-Core-Model-Document-Capability-Review-v1-001",
        stage_term_overrides=FIELD_FIRST_DOC_REVIEW_STAGE_TERM_OVERRIDES,
        stage_additions=FIELD_FIRST_DOC_REVIEW_STAGE_ADDITIONS,
        template_files=FIELD_FIRST_DOC_REVIEW_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-First-Core-Model-Preinstall-Plan-and-Cache-Manifest-Prepare-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    preinstall_fs = _read_json(preinstall_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=preinstall_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    review_pass = review_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if review_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if review_pass else (FINAL_DECISION_UPSTREAM if not prior_model_preinstall_plan_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_ideal_operation_go": prior_ideal_operation_go,
        "prior_model_preinstall_plan_go": prior_model_preinstall_plan_go,
        "model_document_capability_review_complete": model_document_capability_review_complete,
        "review_item_registry_complete": review_item_registry_complete,
        "operation_node_model_fit_matrix_complete": operation_node_model_fit_matrix_complete,
        "model_requirement_satisfaction_matrix_complete": model_requirement_satisfaction_matrix_complete,
        "model_status_classification_complete": model_status_classification_complete,
        "download_authorization_all_false": True,
        "download_authorized_all_remain_false": True,
        "model_selection_not_executed": True,
        "review_based_on_requirement_matrix": True,
        "model_does_not_define_core": True,
        "adapter_still_required_for_all_models": True,
        "field_first_route_preserved": True,
        "ipc_repositioned_as_source_normalization_asset": True,
        "handoff_contract_p3_defer_remains_defer": True,
        "clm_deferred": True,
        "no_model_download": True,
        "no_weight_download": True,
        "no_repo_clone": True,
        "no_large_dependency_install": True,
        "no_inference_execution": True,
        "no_runtime_execution": True,
        "no_integration_test": True,
        "no_real_field_model_creation": True,
        "no_world_model_fact_creation": True,
        "no_model_selected_as_production": True,
        "no_model_marked_ready": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "midplatform_still_has_remaining_work": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": review_pass,
        "field_first_core_model_document_capability_review_pass": review_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "review_item_count": len(items),
        "near_term_count": len(near_term),
        "future_count": len(future),
        "reference_only_count": len(reference),
        "deferred_unsuitable_count": len(unsuitable),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(preinstall_s.get("chain_trace_nodes") or []) + ["field_first_model_document_capability_review"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md_lines = [
        "# Field-First Model Document Capability Review v1",
        f"Reviewed: `{len(items)}` models | Rooms: `{len({i['model_room'] for i in items})}`",
        f"Near-term: `{len(near_term)}` | Future: `{len(future)}` | Reference: `{len(reference)}` | Deferred: `{len(unsuitable)}`",
        "## Near-term adapter candidates",
    ] + [f"- {i['model_project_id']}: {i['reason_for_status']}" for i in near_term[:8]] + [
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ]
    md = "\n".join(md_lines)
    report = {**go_values, "principles": REVIEW_PRINCIPLES, "final_decision": final_decision, **meta}
    return {
        "model_document_capability_review_report": report,
        "model_document_capability_review_report_md": md,
        "model_review_item_registry": registry,
        "operation_node_model_fit_matrix": fit_matrix,
        "model_requirement_satisfaction_matrix": sat_matrix,
        "near_term_adapter_candidate_matrix": near_matrix,
        "future_adapter_candidate_matrix": future_matrix,
        "reference_only_model_matrix": ref_matrix,
        "unsuitable_or_deferred_model_matrix": defer_matrix,
        "model_document_gap_register": gap_reg,
        "model_risk_register": risk_reg,
        "download_authorization_recommendation": download_rec,
        "adapter_priority_recommendation": adapter_prio,
        "next_route_decision": next_route,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
