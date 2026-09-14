# -*- coding: utf-8 -*-
"""Luna Midplatform Candidate Lifecycle Unification Planning v1. Planning only — no lifecycle runtime."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.candidate_lifecycle_unification_items_v1 import (
    ALLOWED_TRANSITIONS,
    ANY_TO_TERMINAL,
    CANDIDATE_TYPE_REGISTRY,
    CANDIDATE_TYPE_REQUIRED_FIELDS,
    CLOSURE_REJECTION_DEFERRAL_RULES,
    FORBIDDEN_PROMOTION_RULES,
    FORBIDDEN_TRANSITIONS,
    LIFECYCLE_INTEGRATION_GAPS,
    NEXT_ROUTE_A,
    NEXT_ROUTE_B,
    NEXT_ROUTE_C,
    NEXT_ROUTE_D,
    NEXT_ROUTE_E,
    PROMOTION_PRECONDITIONS,
    RESPONSIBILITY_MATRIX,
    SELECTED_NEXT_ROUTE,
    STATE_MACHINE_DEFINITIONS,
    STATE_MACHINE_SEMANTICS,
    UNIFIED_LIFECYCLE_STATES,
)
from capabilities.midplatform.candidate_lifecycle_unification_lineage_v1 import (
    CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_STAGE_ADDITIONS,
    CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_STAGE_TERM_OVERRIDES,
    CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.module_boundary_registry_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_BOUNDARY_REGISTRY_PLANNING_ROOT,
    FINAL_DECISION_GO as BOUNDARY_REGISTRY_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as BOUNDARY_REGISTRY_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.module_boundary_registry_items_v1 import SELECTED_NEXT_ROUTE as UPSTREAM_SELECTED_ROUTE
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

PHASE_ID = "Phase-Midplatform-Candidate-Lifecycle-Unification-Planning-v1-001"
SCOPE = "midplatform_candidate_lifecycle_unification_planning_only"
SOURCE_CHAIN = "candidate_lifecycle_unification_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_READY_FOR_EVIDENCE_RECORD_APPROVAL_PERMISSION_ALIGNMENT_PLANNING"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_BLOCKED_BY_BOUNDARY_REGISTRY_GAP"
FINAL_DECISION_PLANNING = "MIDPLATFORM_CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_BLOCKED_BY_LIFECYCLE_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = NEXT_ROUTE_A
NEXT_PHASE_HOLD = "Phase-Midplatform-Candidate-Lifecycle-Unification-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/candidate_lifecycle_unification_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_V1_GO_NO_GO_PACK_V0.md"
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/candidate_lifecycle_unification_planning_v1.py",
    "capabilities/midplatform/candidate_lifecycle_unification_items_v1.py",
    "capabilities/midplatform/candidate_lifecycle_unification_lineage_v1.py",
    "tools/evaluation/midplatform/run_candidate_lifecycle_unification_planning_v1.py",
    "tools/evaluation/midplatform/verify_candidate_lifecycle_unification_planning_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/candidate_lifecycle_unification_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PLANNING_ARTIFACTS: Tuple[str, ...] = (
    "candidate_lifecycle_unification_planning_report_v1.json",
    "candidate_lifecycle_unification_planning_report_v1.md",
    "candidate_lifecycle_scope_v1.json",
    "candidate_type_registry_v1.json",
    "unified_lifecycle_state_machine_v1.json",
    "state_transition_rules_v1.json",
    "forbidden_candidate_promotion_rules_v1.json",
    "candidate_lifecycle_responsibility_matrix_v1.json",
    "promotion_preconditions_v1.json",
    "candidate_closure_rejection_deferral_rules_v1.json",
    "lifecycle_integration_gap_register_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_module_boundary_registry_planning_go",
    "candidate_lifecycle_scope_complete",
    "candidate_type_registry_complete",
    "unified_lifecycle_state_machine_complete",
    "state_transition_rules_complete",
    "forbidden_candidate_promotion_rules_complete",
    "candidate_lifecycle_responsibility_matrix_complete",
    "promotion_preconditions_complete",
    "candidate_closure_rejection_deferral_rules_complete",
    "lifecycle_integration_gap_register_complete",
    "next_route_decision_complete",
    "do_not_misclassify_rules_complete",
    "all_candidate_types_covered",
    "promotion_ready_not_promotion_executed",
    "candidate_lifecycle_runtime_absent",
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
        "candidate_lifecycle_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "module_boundary_registry_planning_root": str(upstream),
    }


def _type_entry_complete(row: Dict[str, Any]) -> bool:
    return all(row.get(f) is not None and row.get(f) != "" for f in CANDIDATE_TYPE_REQUIRED_FIELDS)


def run_candidate_lifecycle_unification_planning_v1(
    *,
    module_boundary_registry_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(module_boundary_registry_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    boundary_summary = _read_json(upstream / "summary.json")
    boundary_verifier = _read_json(upstream / "verifier_report.json")
    boundary_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_module_boundary_registry_planning_go = (
        boundary_summary.get("final_decision") == BOUNDARY_REGISTRY_PLANNING_FINAL_GO
        and boundary_summary.get("recommended_next_phase") == BOUNDARY_REGISTRY_PLANNING_NEXT_PHASE
        and boundary_summary.get("selected_next_route") == UPSTREAM_SELECTED_ROUTE
        and boundary_verifier.get("verifier") == "GO"
        and int(boundary_verifier.get("passed_checks", 0)) >= 300
        and boundary_summary.get("boundary_registry_planning_pass") is True
        and boundary_summary.get("all_required_modules_have_registry_entries") is True
        and boundary_summary.get("no_forbidden_ownership_detected") is True
        and boundary_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_module_boundary_registry_planning_go:
        issues.append("boundary_registry_planning_not_go")

    absence = {key: boundary_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = boundary_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(boundary_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_module_boundary_registry_planning_go
        and boundary_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    owner_approval_request_chain_not_reopened = (
        prior_module_boundary_registry_planning_go
        and boundary_summary.get("owner_approval_request_chain_not_reopened") is True
    )

    type_registry = [dict(t) for t in CANDIDATE_TYPE_REGISTRY]
    gap_rows = [dict(g) for g in LIFECYCLE_INTEGRATION_GAPS]
    future_runtime_debt_not_current_blocker = all(not g.get("blocker_now") for g in gap_rows)

    candidate_lifecycle_scope_complete = prior_module_boundary_registry_planning_go
    all_candidate_types_covered = len(type_registry) >= 11 and all(_type_entry_complete(t) for t in type_registry)
    candidate_type_registry_complete = all_candidate_types_covered
    unified_lifecycle_state_machine_complete = len(STATE_MACHINE_DEFINITIONS) >= 11 and len(UNIFIED_LIFECYCLE_STATES) >= 11
    state_transition_rules_complete = len(ALLOWED_TRANSITIONS) >= 10 and len(FORBIDDEN_TRANSITIONS) >= 9
    forbidden_candidate_promotion_rules_complete = len(FORBIDDEN_PROMOTION_RULES) >= 9
    candidate_lifecycle_responsibility_matrix_complete = len(RESPONSIBILITY_MATRIX) >= 8
    promotion_preconditions_complete = len(PROMOTION_PRECONDITIONS) >= 8
    candidate_closure_rejection_deferral_rules_complete = len(CLOSURE_REJECTION_DEFERRAL_RULES) >= 7
    lifecycle_integration_gap_register_complete = len(gap_rows) >= 7
    next_route_decision_complete = SELECTED_NEXT_ROUTE == "Evidence Record Approval Permission Alignment Planning"
    do_not_misclassify_rules_complete = future_runtime_debt_not_current_blocker

    if not all_candidate_types_covered:
        issues.append("candidate_types_incomplete")
    if not unified_lifecycle_state_machine_complete:
        issues.append("state_machine_incomplete")

    template_lineage = build_template_lineage(
        base_phase="Module-Boundary-Registry-Planning-v1-001",
        base_capability=CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_WHITELIST_FILES[0],
        base_runner=CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_WHITELIST_FILES[1],
        base_verifier=CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Candidate-Lifecycle-Unification-Planning-v1-001",
        stage_term_overrides=CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_STAGE_ADDITIONS,
        template_files=CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Module-Boundary-Registry-Planning-v1-001",
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
        previous_interruption_type=boundary_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=boundary_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=boundary_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    planning_pass = (
        prior_module_boundary_registry_planning_go
        and candidate_lifecycle_scope_complete
        and candidate_type_registry_complete
        and unified_lifecycle_state_machine_complete
        and state_transition_rules_complete
        and forbidden_candidate_promotion_rules_complete
        and candidate_lifecycle_responsibility_matrix_complete
        and promotion_preconditions_complete
        and candidate_closure_rejection_deferral_rules_complete
        and lifecycle_integration_gap_register_complete
        and next_route_decision_complete
        and do_not_misclassify_rules_complete
        and all_candidate_types_covered
        and owner_approval_request_chain_not_reopened
        and future_runtime_debt_not_current_blocker
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase = NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD

    if not prior_module_boundary_registry_planning_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not all_candidate_types_covered:
        final_decision = FINAL_DECISION_PLANNING
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_module_boundary_registry_planning_go": prior_module_boundary_registry_planning_go,
        "candidate_lifecycle_scope_complete": candidate_lifecycle_scope_complete,
        "candidate_type_registry_complete": candidate_type_registry_complete,
        "unified_lifecycle_state_machine_complete": unified_lifecycle_state_machine_complete,
        "state_transition_rules_complete": state_transition_rules_complete,
        "forbidden_candidate_promotion_rules_complete": forbidden_candidate_promotion_rules_complete,
        "candidate_lifecycle_responsibility_matrix_complete": candidate_lifecycle_responsibility_matrix_complete,
        "promotion_preconditions_complete": promotion_preconditions_complete,
        "candidate_closure_rejection_deferral_rules_complete": candidate_closure_rejection_deferral_rules_complete,
        "lifecycle_integration_gap_register_complete": lifecycle_integration_gap_register_complete,
        "next_route_decision_complete": next_route_decision_complete,
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "all_candidate_types_covered": all_candidate_types_covered,
        "promotion_ready_not_promotion_executed": True,
        "upgraded_not_real_record_or_grant": True,
        "candidate_closed_not_runtime_closure": True,
        "candidate_lifecycle_runtime_absent": True,
        "midplatform_still_has_remaining_work": boundary_summary.get("midplatform_still_has_remaining_work") is True,
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
        "candidate_lifecycle_unification_planning_pass": planning_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "candidate_not_promoted_to_record": True,
        "permission_candidate_not_promoted_to_grant": True,
        "authorization_request_candidate_not_promoted_to_authorization_request": True,
        "evidence_candidate_not_promoted_to_evidence_record": True,
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
            list(boundary_summary.get("chain_trace_nodes") or []) + ["candidate_lifecycle_unification_planning"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    scope = {
        "scope_id": "candidate_lifecycle_scope_v1",
        "candidate_lifecycle_scope_complete": candidate_lifecycle_scope_complete,
        "purpose": "Unified candidate lifecycle planning only",
        "not_lifecycle_runtime": True,
        "not_state_promotion_execution": True,
        "not_record_grant_creation": True,
        "not_reopen_owner_approval_request": True,
        **meta,
    }
    type_reg = {
        "registry_id": "candidate_type_registry_v1",
        "candidate_type_registry_complete": candidate_type_registry_complete,
        "types": type_registry,
        "type_count": len(type_registry),
        **meta,
    }
    state_machine = {
        "machine_id": "unified_lifecycle_state_machine_v1",
        "unified_lifecycle_state_machine_complete": unified_lifecycle_state_machine_complete,
        "states": list(UNIFIED_LIFECYCLE_STATES),
        "definitions": list(STATE_MACHINE_DEFINITIONS),
        "semantics": list(STATE_MACHINE_SEMANTICS),
        **meta,
    }
    transition_rules = {
        "rules_id": "state_transition_rules_v1",
        "state_transition_rules_complete": state_transition_rules_complete,
        "allowed_transitions": list(ALLOWED_TRANSITIONS),
        "any_to_terminal": list(ANY_TO_TERMINAL),
        "forbidden_transitions": list(FORBIDDEN_TRANSITIONS),
        **meta,
    }
    forbidden_promotion = {
        "rules_id": "forbidden_candidate_promotion_rules_v1",
        "forbidden_candidate_promotion_rules_complete": forbidden_candidate_promotion_rules_complete,
        "rules": list(FORBIDDEN_PROMOTION_RULES),
        **meta,
    }
    responsibility = {
        "matrix_id": "candidate_lifecycle_responsibility_matrix_v1",
        "candidate_lifecycle_responsibility_matrix_complete": candidate_lifecycle_responsibility_matrix_complete,
        "rows": list(RESPONSIBILITY_MATRIX),
        **meta,
    }
    preconditions = {
        "preconditions_id": "promotion_preconditions_v1",
        "promotion_preconditions_complete": promotion_preconditions_complete,
        "preconditions": list(PROMOTION_PRECONDITIONS),
        "promotion_executed": False,
        **meta,
    }
    closure_rules = {
        "rules_id": "candidate_closure_rejection_deferral_rules_v1",
        "candidate_closure_rejection_deferral_rules_complete": candidate_closure_rejection_deferral_rules_complete,
        "rules": list(CLOSURE_REJECTION_DEFERRAL_RULES),
        **meta,
    }
    gap_register = {
        "register_id": "lifecycle_integration_gap_register_v1",
        "lifecycle_integration_gap_register_complete": lifecycle_integration_gap_register_complete,
        "gaps": gap_rows,
        **meta,
    }
    route_decision = {
        "decision_id": "next_route_decision_v1",
        "next_route_decision_complete": next_route_decision_complete,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": next_phase,
        "rationale": "Unified lifecycle state machine complete; evidence/record/approval/permission alignment is next",
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
            "lifecycle_planning_not_lifecycle_runtime",
            "promotion_ready_not_promotion_executed",
            "upgraded_not_real_record_grant_auth_request",
            "candidate_closed_not_runtime_closure",
            "lifecycle_manager_not_direct_authorization_engine",
            "future_runtime_debt_not_current_blocker",
            "owner_approval_request_chain_not_reopened",
        ],
        **meta,
    }
    report = {"report_id": "candidate_lifecycle_unification_planning_report_v1", **go_values, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "candidate_lifecycle_unification_planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join([
        "# Candidate Lifecycle Unification Planning v1",
        "",
        f"Candidate types: `{len(type_registry)}`",
        f"Lifecycle states: `{len(UNIFIED_LIFECYCLE_STATES)}`",
        f"Forbidden promotion rules: `{len(FORBIDDEN_PROMOTION_RULES)}`",
        f"Selected next route: `{SELECTED_NEXT_ROUTE}`",
        f"Final decision: `{final_decision}`",
        f"Next phase: `{next_phase}`",
    ])
    return {
        "candidate_lifecycle_unification_planning_report": report,
        "candidate_lifecycle_unification_planning_report_md": markdown,
        "candidate_lifecycle_scope": scope,
        "candidate_type_registry": type_reg,
        "unified_lifecycle_state_machine": state_machine,
        "state_transition_rules": transition_rules,
        "forbidden_candidate_promotion_rules": forbidden_promotion,
        "candidate_lifecycle_responsibility_matrix": responsibility,
        "promotion_preconditions": preconditions,
        "candidate_closure_rejection_deferral_rules": closure_rules,
        "lifecycle_integration_gap_register": gap_register,
        "next_route_decision": route_decision,
        "do_not_misclassify_rules": misclassify_rules,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
