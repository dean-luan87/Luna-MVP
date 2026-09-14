# -*- coding: utf-8 -*-
"""Field-First Core Adapter Priority and Download Authorization Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.field_first_core_adapter_priority_download_authorization_items_v1 import (
    ADAPTER_BATCH_PLAN,
    DO_NOT_MISCLASSIFY,
    P0_SELF_DEVELOPED,
    P1_NEAR_TERM,
    P2_FUTURE,
    P3_REFERENCE_DEFERRED,
    PLANNING_PRINCIPLES,
    RISK_CONTROL_RULES,
    SELECTED_NEXT_PHASE,
    SELECTED_NEXT_ROUTE,
    SKELETON_BATCH_RECOMMENDATION,
    _all_priority_items,
)
from capabilities.midplatform.field_first_core_adapter_priority_download_authorization_lineage_v1 import (
    FIELD_FIRST_ADAPTER_PLAN_STAGE_ADDITIONS,
    FIELD_FIRST_ADAPTER_PLAN_STAGE_TERM_OVERRIDES,
    FIELD_FIRST_ADAPTER_PLAN_WHITELIST_FILES,
)
from capabilities.midplatform.field_first_core_model_document_capability_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_DOC_REVIEW_ROOT,
    FINAL_DECISION_GO as DOC_REVIEW_FINAL_GO,
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

PHASE_ID = "Phase-Midplatform-Field-First-Core-Adapter-Priority-and-Download-Authorization-Planning-v1-001"
SCOPE = "field_first_core_adapter_priority_planning_only"
SOURCE_CHAIN = "field_first_core_adapter_priority_download_authorization_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_FIELD_FIRST_CORE_ADAPTER_PRIORITY_AND_DOWNLOAD_AUTHORIZATION_PLANNING_READY_FOR_SELF_DEVELOPED_FIELD_FIRST_SKELETON_IMPLEMENTATION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_FIELD_FIRST_CORE_ADAPTER_PRIORITY_PLANNING_BLOCKED_BY_PRIOR_GAP"
FINAL_DECISION_RECAL = "MIDPLATFORM_FIELD_FIRST_CORE_ADAPTER_PRIORITY_PLANNING_BLOCKED_BY_PLANNING_GAP"
NEXT_PHASE_HOLD = "Phase-Midplatform-Field-First-Core-Adapter-Priority-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_first_core_adapter_priority_download_authorization_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_FIELD_FIRST_CORE_ADAPTER_PRIORITY_DOWNLOAD_AUTHORIZATION_PLANNING_V1_GO_NO_GO_PACK_V0.md"
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/field_first_core_adapter_priority_download_authorization_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_adapter_priority_download_authorization_planning_v1.py",
    "capabilities/midplatform/field_first_core_adapter_priority_download_authorization_items_v1.py",
    "capabilities/midplatform/field_first_core_adapter_priority_download_authorization_lineage_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_adapter_priority_download_authorization_planning_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_adapter_priority_download_authorization_planning_v1.py",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_model_document_review_go",
    "adapter_priority_queue_complete",
    "adapter_batch_plan_complete",
    "download_authorization_plan_complete",
    "owner_review_candidate_downloads_complete",
    "all_download_authorized_remain_false",
    "self_developed_skeletons_prioritized",
    "no_download_execution",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _meta(out: Path, doc_root: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID, "scope": SCOPE, "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "field_first_core_adapter_priority_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "output_root": str(out), "doc_review_root": str(doc_root),
    }


def _upstream_go(path: Path, final_go: str, pass_key: str, min_checks: int) -> bool:
    s, v = _read_json(path / "summary.json"), _read_json(path / "verifier_report.json")
    return s.get("final_decision") == final_go and v.get("verifier") == "GO" and int(v.get("passed_checks", 0)) >= min_checks and s.get(pass_key) is True


def run_field_first_core_adapter_priority_download_authorization_planning_v1(
    *,
    doc_review_root: str,
    preinstall_root: str = DEFAULT_PREINSTALL_ROOT,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    doc_upstream = Path(doc_review_root or DEFAULT_DOC_REVIEW_ROOT).expanduser().resolve()
    preinstall_upstream = Path(preinstall_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, doc_upstream)
    issues: List[str] = []

    prior_model_document_review_go = _upstream_go(doc_upstream, DOC_REVIEW_FINAL_GO, "field_first_core_model_document_capability_review_pass", 460)
    prior_preinstall_go = _upstream_go(preinstall_upstream, PREINSTALL_FINAL_GO, "field_first_core_model_preinstall_plan_pass", 420)
    if not prior_model_document_review_go:
        issues.append("doc_review_not_go")
    if not prior_preinstall_go:
        issues.append("preinstall_not_go")

    doc_s = _read_json(doc_upstream / "summary.json")
    absence = {k: doc_s.get(k) is True for k in ABSENCE_KEYS}
    non_execution_boundary_ok = prior_model_document_review_go and doc_s.get("non_execution_boundary_ok") is True and all(absence.values())
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    priority_queue = list(_all_priority_items())
    adapter_priority_queue_complete = len(priority_queue) >= 17 and len(P0_SELF_DEVELOPED) >= 5
    adapter_batch_plan_complete = len(ADAPTER_BATCH_PLAN) >= 3
    all_items = list(P0_SELF_DEVELOPED) + list(P1_NEAR_TERM) + list(P2_FUTURE) + list(P3_REFERENCE_DEFERRED)
    download_plan_entries = [{"model_project_id": i.get("model_project_id"), "adapter_id": i.get("adapter_id"), "download_authorization_status": i.get("download_auth"), "download_authorized": False, "reason": i.get("reason")} for i in all_items]
    download_authorization_plan_complete = len(download_plan_entries) >= 25
    owner_review = [e for e in download_plan_entries if e["download_authorization_status"] == "eligible_for_owner_review"]
    owner_review_candidate_downloads_complete = len(owner_review) >= 5
    all_download_authorized_remain_false = all(e["download_authorized"] is False for e in download_plan_entries)
    self_developed_skeletons_prioritized = priority_queue[0].get("priority") == "P0"

    priority_doc = {"queue_id": "adapter_priority_queue_v1", "adapter_priority_queue_complete": adapter_priority_queue_complete, "p0": list(P0_SELF_DEVELOPED), "p1": list(P1_NEAR_TERM), "p2": list(P2_FUTURE), "p3": list(P3_REFERENCE_DEFERRED), **meta}
    batch_doc = {"plan_id": "adapter_batch_plan_v1", "adapter_batch_plan_complete": adapter_batch_plan_complete, "batches": list(ADAPTER_BATCH_PLAN), **meta}
    dl_plan = {"plan_id": "download_authorization_plan_v1", "download_authorization_plan_complete": download_authorization_plan_complete, "all_download_authorized_remain_false": all_download_authorized_remain_false, "entries": download_plan_entries, **meta}
    owner_doc = {"register_id": "owner_review_candidate_downloads_v1", "owner_review_candidate_downloads_complete": owner_review_candidate_downloads_complete, "candidates": owner_review, **meta}
    self_dev = {"register_id": "no_download_required_self_developed_items_v1", "items": list(P0_SELF_DEVELOPED), **meta}
    conditional = {"register_id": "conditional_future_download_review_v1", "items": [e for e in download_plan_entries if e["download_authorization_status"] == "conditional_future_review"], **meta}
    reference = {"register_id": "reference_only_no_download_v1", "items": [e for e in download_plan_entries if e["download_authorization_status"] == "reference_only_no_download"], **meta}
    deferred = {"register_id": "deferred_no_download_v1", "items": [e for e in download_plan_entries if e["download_authorization_status"] == "deferred_no_download"], **meta}
    skeleton = {"recommendation_id": "adapter_skeleton_batch_recommendation_v1", "recommendations": list(SKELETON_BATCH_RECOMMENDATION), "batches": list(ADAPTER_BATCH_PLAN), **meta}
    transition = {"plan_id": "model_status_transition_plan_v1", "transitions": [{"from": "document_review", "to": "adapter_priority_planning", "next": "skeleton_implementation_then_owner_review"}] + [{"model_project_id": e["model_project_id"], "planned_status": e["download_authorization_status"]} for e in download_plan_entries[:10]], **meta}
    risk = {"plan_id": "risk_control_plan_v1", "rules": list(RISK_CONTROL_RULES), **meta}
    next_route = {"decision_id": "next_route_decision_v1", "selected_next_route": SELECTED_NEXT_ROUTE, "recommended_next_phase": SELECTED_NEXT_PHASE, "rationale": "Self-developed skeletons first; model download after owner review", **meta}
    misclassify = {"rules_id": "do_not_misclassify_rules_v1", "rules": list(DO_NOT_MISCLASSIFY), **meta}

    plan_pass = (
        prior_model_document_review_go and prior_preinstall_go and adapter_priority_queue_complete
        and adapter_batch_plan_complete and download_authorization_plan_complete
        and owner_review_candidate_downloads_complete and all_download_authorized_remain_false
        and self_developed_skeletons_prioritized and non_execution_boundary_ok and len(issues) == 0
    )

    template_lineage = build_template_lineage(
        base_phase="Midplatform-Field-First-Core-Model-Document-Capability-Review-v1-001",
        base_capability=FIELD_FIRST_ADAPTER_PLAN_WHITELIST_FILES[0],
        base_runner=FIELD_FIRST_ADAPTER_PLAN_WHITELIST_FILES[1],
        base_verifier=FIELD_FIRST_ADAPTER_PLAN_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Midplatform-Field-First-Core-Adapter-Priority-and-Download-Authorization-Planning-v1-001",
        stage_term_overrides=FIELD_FIRST_ADAPTER_PLAN_STAGE_TERM_OVERRIDES,
        stage_additions=FIELD_FIRST_ADAPTER_PLAN_STAGE_ADDITIONS,
        template_files=FIELD_FIRST_ADAPTER_PLAN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Midplatform-Field-First-Core-Model-Document-Capability-Review-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    doc_fs = _read_json(doc_upstream / "file_size_governance_review_v1.json")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID, scope_paths=list(PHASE_PYTHON_FILES), repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES, template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first", full_repo_scan=False,
        previous_interruption_type=doc_fs.get("previous_interruption_type"),
    )
    fs_ok = file_size.get("file_size_governance_review_ok") is True
    plan_pass = plan_pass and template_lineage.get("template_lineage_ok") and fs_ok and len(issues) == 0
    next_phase = SELECTED_NEXT_PHASE if plan_pass else NEXT_PHASE_HOLD
    final_decision = FINAL_DECISION_GO if plan_pass else (FINAL_DECISION_UPSTREAM if not prior_model_document_review_go else FINAL_DECISION_RECAL)

    go_values = {
        "prior_model_document_review_go": prior_model_document_review_go,
        "adapter_priority_queue_complete": adapter_priority_queue_complete,
        "adapter_batch_plan_complete": adapter_batch_plan_complete,
        "download_authorization_plan_complete": download_authorization_plan_complete,
        "owner_review_candidate_downloads_complete": owner_review_candidate_downloads_complete,
        "all_download_authorized_remain_false": all_download_authorized_remain_false,
        "self_developed_skeletons_prioritized": self_developed_skeletons_prioritized,
        "no_download_execution": True,
        "owner_review_required_before_any_download": True,
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
        "no_model_selected_as_production": True,
        "no_model_marked_ready": True,
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "midplatform_still_has_remaining_work": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": fs_ok,
        "next_phase_readiness_ok": plan_pass,
        "field_first_core_adapter_priority_planning_pass": plan_pass,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "p0_count": len(P0_SELF_DEVELOPED),
        "p1_count": len(P1_NEAR_TERM),
        "p2_count": len(P2_FUTURE),
        "p3_count": len(P3_REFERENCE_DEFERRED),
        "owner_review_count": len(owner_review),
        "full_repo_scan_absent": file_size.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size.get("summary_index_first_reading_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(list(doc_s.get("chain_trace_nodes") or []) + ["field_first_adapter_priority_planning"]),
        go_no_go_decision=final_decision, final_decision=final_decision, next_phase=next_phase,
        template_lineage=template_lineage,
    )
    summary = {
        "phase": PHASE_ID, "scope": SCOPE, "blocker_count": len(issues), "issues": issues,
        **go_values, **core_fields, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta,
    }
    md = "\n".join([
        "# Adapter Priority & Download Authorization Planning v1",
        f"P0 self-developed: `{len(P0_SELF_DEVELOPED)}` | P1 near-term: `{len(P1_NEAR_TERM)}` | P2 future: `{len(P2_FUTURE)}` | P3 ref/defer: `{len(P3_REFERENCE_DEFERRED)}`",
        f"Owner review candidates: `{len(owner_review)}` | download_authorized: all false",
        "## P0 First (no download)",
    ] + [f"- {i['adapter_id']}" for i in P0_SELF_DEVELOPED] + [
        f"Final decision: `{final_decision}`", f"Next: `{next_phase}`",
    ])
    report = {**go_values, "principles": PLANNING_PRINCIPLES, "final_decision": final_decision, **meta}
    return {
        "adapter_priority_and_download_authorization_plan_report": report,
        "adapter_priority_and_download_authorization_plan_report_md": md,
        "adapter_priority_queue": priority_doc,
        "adapter_batch_plan": batch_doc,
        "download_authorization_plan": dl_plan,
        "owner_review_candidate_downloads": owner_doc,
        "no_download_required_self_developed_items": self_dev,
        "conditional_future_download_review": conditional,
        "reference_only_no_download": reference,
        "deferred_no_download": deferred,
        "adapter_skeleton_batch_recommendation": skeleton,
        "model_status_transition_plan": transition,
        "risk_control_plan": risk,
        "next_route_decision": next_route,
        "do_not_misclassify_rules": misclassify,
        "file_size_governance_review": {**file_size, **meta},
        "summary": summary,
    }
