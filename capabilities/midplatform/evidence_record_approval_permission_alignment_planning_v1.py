# -*- coding: utf-8 -*-
"""Luna Midplatform Evidence Record Approval Permission Alignment Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.candidate_lifecycle_unification_items_v1 import SELECTED_NEXT_ROUTE as UPSTREAM_SELECTED_ROUTE
from capabilities.midplatform.candidate_lifecycle_unification_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CANDIDATE_LIFECYCLE_PLANNING_ROOT,
    FINAL_DECISION_GO as CANDIDATE_LIFECYCLE_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as CANDIDATE_LIFECYCLE_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.evidence_record_approval_permission_alignment_items_v1 import (
    ALIGNMENT_GAPS,
    ALIGNMENT_OBJECT_REGISTRY,
    ALIGNMENT_OBJECT_REQUIRED_FIELDS,
    ALIGNMENT_RESPONSIBILITY_MATRIX,
    CANDIDATE_REAL_BOUNDARY_MATRIX,
    FORBIDDEN_ALIGNMENT_TRANSITIONS,
    NEXT_ROUTE_A,
    NEXT_ROUTE_B,
    NEXT_ROUTE_C,
    NEXT_ROUTE_D,
    NEXT_ROUTE_E,
    PROMOTION_CREATION_PRECONDITIONS,
    SELECTED_NEXT_ROUTE,
    TRACEABILITY_CONTRACT,
)
from capabilities.midplatform.evidence_record_approval_permission_alignment_lineage_v1 import (
    ALIGNMENT_PLANNING_STAGE_ADDITIONS,
    ALIGNMENT_PLANNING_STAGE_TERM_OVERRIDES,
    ALIGNMENT_PLANNING_WHITELIST_FILES,
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

PHASE_ID = "Phase-Midplatform-Evidence-Record-Approval-Permission-Alignment-Planning-v1-001"
SCOPE = "midplatform_evidence_record_approval_permission_alignment_planning_only"
SOURCE_CHAIN = "evidence_record_approval_permission_alignment_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_EVIDENCE_RECORD_APPROVAL_PERMISSION_ALIGNMENT_PLANNING_READY_FOR_TASK_MANAGER_CORE_ORCHESTRATION_SKELETON_CONSOLIDATION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_EVIDENCE_RECORD_APPROVAL_PERMISSION_ALIGNMENT_PLANNING_BLOCKED_BY_LIFECYCLE_GAP"
FINAL_DECISION_PLANNING = "MIDPLATFORM_EVIDENCE_RECORD_APPROVAL_PERMISSION_ALIGNMENT_PLANNING_BLOCKED_BY_ALIGNMENT_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_EVIDENCE_RECORD_APPROVAL_PERMISSION_ALIGNMENT_PLANNING_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_EVIDENCE_RECORD_APPROVAL_PERMISSION_ALIGNMENT_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_EVIDENCE_RECORD_APPROVAL_PERMISSION_ALIGNMENT_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = NEXT_ROUTE_A
NEXT_PHASE_HOLD = "Phase-Midplatform-Evidence-Record-Approval-Permission-Alignment-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/evidence_record_approval_permission_alignment_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_EVIDENCE_RECORD_APPROVAL_PERMISSION_ALIGNMENT_PLANNING_V1_GO_NO_GO_PACK_V0.md"
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/evidence_record_approval_permission_alignment_planning_v1.py",
    "capabilities/midplatform/evidence_record_approval_permission_alignment_items_v1.py",
    "capabilities/midplatform/evidence_record_approval_permission_alignment_lineage_v1.py",
    "tools/evaluation/midplatform/run_evidence_record_approval_permission_alignment_planning_v1.py",
    "tools/evaluation/midplatform/verify_evidence_record_approval_permission_alignment_planning_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/evidence_record_approval_permission_alignment_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PLANNING_ARTIFACTS: Tuple[str, ...] = (
    "evidence_record_approval_permission_alignment_planning_report_v1.json",
    "evidence_record_approval_permission_alignment_planning_report_v1.md",
    "alignment_scope_v1.json",
    "alignment_object_registry_v1.json",
    "candidate_real_object_boundary_matrix_v1.json",
    "promotion_creation_preconditions_v1.json",
    "alignment_responsibility_matrix_v1.json",
    "forbidden_alignment_transitions_v1.json",
    "alignment_traceability_contract_v1.json",
    "alignment_gap_register_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_candidate_lifecycle_unification_go",
    "alignment_scope_complete",
    "alignment_object_registry_complete",
    "candidate_real_object_boundary_matrix_complete",
    "promotion_creation_preconditions_complete",
    "alignment_responsibility_matrix_complete",
    "forbidden_alignment_transitions_complete",
    "alignment_traceability_contract_complete",
    "alignment_gap_register_complete",
    "next_route_decision_complete",
    "do_not_misclassify_rules_complete",
    "real_objects_absent",
    "alignment_runtime_absent",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, upstream: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "alignment_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "candidate_lifecycle_unification_planning_root": str(upstream),
    }


def _object_complete(row: Dict[str, Any]) -> bool:
    return all(row.get(f) is not None and row.get(f) != "" for f in ALIGNMENT_OBJECT_REQUIRED_FIELDS)


def run_evidence_record_approval_permission_alignment_planning_v1(
    *,
    candidate_lifecycle_unification_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(candidate_lifecycle_unification_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    lifecycle_summary = _read_json(upstream / "summary.json")
    lifecycle_verifier = _read_json(upstream / "verifier_report.json")
    lifecycle_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_candidate_lifecycle_unification_go = (
        lifecycle_summary.get("final_decision") == CANDIDATE_LIFECYCLE_PLANNING_FINAL_GO
        and lifecycle_summary.get("recommended_next_phase") == CANDIDATE_LIFECYCLE_PLANNING_NEXT_PHASE
        and lifecycle_summary.get("selected_next_route") == UPSTREAM_SELECTED_ROUTE
        and lifecycle_verifier.get("verifier") == "GO"
        and int(lifecycle_verifier.get("passed_checks", 0)) >= 320
        and lifecycle_summary.get("candidate_lifecycle_unification_planning_pass") is True
        and lifecycle_summary.get("all_candidate_types_covered") is True
        and lifecycle_summary.get("candidate_lifecycle_runtime_absent") is True
        and lifecycle_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_candidate_lifecycle_unification_go:
        issues.append("lifecycle_planning_not_go")

    absence = {key: lifecycle_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = lifecycle_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(lifecycle_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_candidate_lifecycle_unification_go
        and lifecycle_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    owner_approval_request_chain_not_reopened = (
        prior_candidate_lifecycle_unification_go
        and lifecycle_summary.get("owner_approval_request_chain_not_reopened") is True
    )

    objects = [dict(o) for o in ALIGNMENT_OBJECT_REGISTRY]
    gap_rows = [dict(g) for g in ALIGNMENT_GAPS]
    future_runtime_debt_not_current_blocker = all(not g.get("blocker_now") for g in gap_rows)

    alignment_scope_complete = prior_candidate_lifecycle_unification_go
    alignment_object_registry_complete = len(objects) >= 13 and all(_object_complete(o) for o in objects)
    candidate_real_object_boundary_matrix_complete = len(CANDIDATE_REAL_BOUNDARY_MATRIX) >= 9
    promotion_creation_preconditions_complete = len(PROMOTION_CREATION_PRECONDITIONS) >= 10
    alignment_responsibility_matrix_complete = len(ALIGNMENT_RESPONSIBILITY_MATRIX) >= 8
    forbidden_alignment_transitions_complete = len(FORBIDDEN_ALIGNMENT_TRANSITIONS) >= 9
    alignment_traceability_contract_complete = len(TRACEABILITY_CONTRACT) >= 5
    alignment_gap_register_complete = len(gap_rows) >= 8
    next_route_decision_complete = SELECTED_NEXT_ROUTE == "Task Manager Core Orchestration Skeleton Consolidation"
    do_not_misclassify_rules_complete = future_runtime_debt_not_current_blocker

    if not alignment_object_registry_complete:
        issues.append("object_registry_incomplete")

    template_lineage = build_template_lineage(
        base_phase="Candidate-Lifecycle-Unification-Planning-v1-001",
        base_capability=ALIGNMENT_PLANNING_WHITELIST_FILES[0],
        base_runner=ALIGNMENT_PLANNING_WHITELIST_FILES[1],
        base_verifier=ALIGNMENT_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Evidence-Record-Approval-Permission-Alignment-Planning-v1-001",
        stage_term_overrides=ALIGNMENT_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=ALIGNMENT_PLANNING_STAGE_ADDITIONS,
        template_files=ALIGNMENT_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Candidate-Lifecycle-Unification-Planning-v1-001",
    )
    if not template_lineage.get("template_lineage_ok"):
        issues.append("template_lineage_gap")

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first",
        full_repo_scan=False,
        previous_interruption_type=lifecycle_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=lifecycle_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=lifecycle_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    planning_pass = (
        prior_candidate_lifecycle_unification_go
        and alignment_scope_complete
        and alignment_object_registry_complete
        and candidate_real_object_boundary_matrix_complete
        and promotion_creation_preconditions_complete
        and alignment_responsibility_matrix_complete
        and forbidden_alignment_transitions_complete
        and alignment_traceability_contract_complete
        and alignment_gap_register_complete
        and next_route_decision_complete
        and do_not_misclassify_rules_complete
        and owner_approval_request_chain_not_reopened
        and future_runtime_debt_not_current_blocker
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase = NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD

    if not prior_candidate_lifecycle_unification_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not alignment_object_registry_complete:
        final_decision = FINAL_DECISION_PLANNING
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_candidate_lifecycle_unification_go": prior_candidate_lifecycle_unification_go,
        "alignment_scope_complete": alignment_scope_complete,
        "alignment_object_registry_complete": alignment_object_registry_complete,
        "candidate_real_object_boundary_matrix_complete": candidate_real_object_boundary_matrix_complete,
        "promotion_creation_preconditions_complete": promotion_creation_preconditions_complete,
        "alignment_responsibility_matrix_complete": alignment_responsibility_matrix_complete,
        "forbidden_alignment_transitions_complete": forbidden_alignment_transitions_complete,
        "alignment_traceability_contract_complete": alignment_traceability_contract_complete,
        "alignment_gap_register_complete": alignment_gap_register_complete,
        "next_route_decision_complete": next_route_decision_complete,
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "real_objects_absent": True,
        "alignment_runtime_absent": True,
        "candidate_promotion_executed": False,
        "promotion_preconditions_not_promotion_execution": True,
        "evidence_candidate_not_evidence_record": True,
        "record_candidate_not_request_record": True,
        "approval_candidate_not_approval_record": True,
        "ack_record_candidate_not_ack_record": True,
        "permission_candidate_not_grant": True,
        "grant_candidate_not_grant_record": True,
        "authorization_request_candidate_not_authorization_request": True,
        "midplatform_still_has_remaining_work": lifecycle_summary.get("midplatform_still_has_remaining_work") is True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "future_runtime_debt_not_current_blocker": future_runtime_debt_not_current_blocker,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "owner_approval_request_closed_module": "governance_ready_handoff",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": planning_pass,
        "alignment_planning_pass": planning_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(lifecycle_summary.get("chain_trace_nodes") or []) + ["evidence_record_approval_permission_alignment_planning"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    scope = {
        "scope_id": "alignment_scope_v1",
        "alignment_scope_complete": alignment_scope_complete,
        "purpose": "Evidence/record/approval/permission alignment planning only",
        "not_promotion_execution": True,
        "not_real_object_creation": True,
        "not_runtime": True,
        "not_reopen_owner_approval_request": True,
        **meta,
    }
    object_registry = {
        "registry_id": "alignment_object_registry_v1",
        "alignment_object_registry_complete": alignment_object_registry_complete,
        "objects": objects,
        "object_count": len(objects),
        **meta,
    }
    boundary_matrix = {
        "matrix_id": "candidate_real_object_boundary_matrix_v1",
        "candidate_real_object_boundary_matrix_complete": candidate_real_object_boundary_matrix_complete,
        "pairs": list(CANDIDATE_REAL_BOUNDARY_MATRIX),
        **meta,
    }
    preconditions = {
        "preconditions_id": "promotion_creation_preconditions_v1",
        "promotion_creation_preconditions_complete": promotion_creation_preconditions_complete,
        "preconditions": list(PROMOTION_CREATION_PRECONDITIONS),
        "promotion_executed": False,
        **meta,
    }
    responsibility = {
        "matrix_id": "alignment_responsibility_matrix_v1",
        "alignment_responsibility_matrix_complete": alignment_responsibility_matrix_complete,
        "rows": list(ALIGNMENT_RESPONSIBILITY_MATRIX),
        **meta,
    }
    forbidden_transitions = {
        "transitions_id": "forbidden_alignment_transitions_v1",
        "forbidden_alignment_transitions_complete": forbidden_alignment_transitions_complete,
        "transitions": list(FORBIDDEN_ALIGNMENT_TRANSITIONS),
        **meta,
    }
    traceability = {
        "contract_id": "alignment_traceability_contract_v1",
        "alignment_traceability_contract_complete": alignment_traceability_contract_complete,
        "contracts": list(TRACEABILITY_CONTRACT),
        "no_real_trace_record_created": True,
        **meta,
    }
    gap_register = {
        "register_id": "alignment_gap_register_v1",
        "alignment_gap_register_complete": alignment_gap_register_complete,
        "gaps": gap_rows,
        **meta,
    }
    route_decision = {
        "decision_id": "next_route_decision_v1",
        "next_route_decision_complete": next_route_decision_complete,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": next_phase,
        "rationale": "Alignment planning complete; orchestration skeleton consolidation is next",
        "alternate_routes": [
            {"route_id": "B", "phase_id": NEXT_ROUTE_B},
            {"route_id": "C", "phase_id": NEXT_ROUTE_C},
            {"route_id": "D", "phase_id": NEXT_ROUTE_D},
            {"route_id": "E", "phase_id": NEXT_ROUTE_E},
        ],
        "do_not_declare_midplatform_completed": True,
        **meta,
    }
    misclassify_rules = {
        "rules_id": "do_not_misclassify_rules_v1",
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "rules": [
            "alignment_planning_not_alignment_runtime",
            "promotion_preconditions_not_promotion_execution",
            "candidate_boundary_matrix_not_real_record_creation",
            "grant_candidate_not_grant_record",
            "permission_candidate_not_grant",
            "authorization_request_candidate_not_authorization_request",
            "traceability_contract_not_real_trace_record",
            "future_runtime_debt_not_current_blocker",
            "owner_approval_request_chain_not_reopened",
        ],
        **meta,
    }
    report = {"report_id": "evidence_record_approval_permission_alignment_planning_report_v1", **go_values, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "alignment_planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join([
        "# Evidence Record Approval Permission Alignment Planning v1",
        "",
        f"Alignment objects: `{len(objects)}`",
        f"Boundary pairs: `{len(CANDIDATE_REAL_BOUNDARY_MATRIX)}`",
        f"Forbidden transitions: `{len(FORBIDDEN_ALIGNMENT_TRANSITIONS)}`",
        f"Selected next route: `{SELECTED_NEXT_ROUTE}`",
        f"Final decision: `{final_decision}`",
        f"Next phase: `{next_phase}`",
    ])
    return {
        "evidence_record_approval_permission_alignment_planning_report": report,
        "evidence_record_approval_permission_alignment_planning_report_md": markdown,
        "alignment_scope": scope,
        "alignment_object_registry": object_registry,
        "candidate_real_object_boundary_matrix": boundary_matrix,
        "promotion_creation_preconditions": preconditions,
        "alignment_responsibility_matrix": responsibility,
        "forbidden_alignment_transitions": forbidden_transitions,
        "alignment_traceability_contract": traceability,
        "alignment_gap_register": gap_register,
        "next_route_decision": route_decision,
        "do_not_misclassify_rules": misclassify_rules,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
