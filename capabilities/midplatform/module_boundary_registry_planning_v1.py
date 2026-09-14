# -*- coding: utf-8 -*-
"""Luna Midplatform Module Boundary Registry Planning v1. Planning only — no runtime registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.module_boundary_registry_items_v1 import (
    BOUNDARY_CONFLICT_DETECTION_CHECKS,
    BOUNDARY_DEPENDENCY_EDGES,
    BOUNDARY_DEPENDENCY_NODES,
    FORBIDDEN_OWNERSHIP_PAIRS,
    MODULE_BOUNDARY_REGISTRY_DRAFT,
    NOT_OWNED_FORBIDDEN_TRANSITIONS,
    OWNERSHIP_MATRIX,
    OWNERSHIP_STATEMENTS,
    REGISTRY_ENTRY_REQUIRED_FIELDS,
    NEXT_ROUTE_A,
    NEXT_ROUTE_B,
    NEXT_ROUTE_C,
    NEXT_ROUTE_D,
    NEXT_ROUTE_E,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.module_boundary_registry_lineage_v1 import (
    MODULE_BOUNDARY_REGISTRY_PLANNING_STAGE_ADDITIONS,
    MODULE_BOUNDARY_REGISTRY_PLANNING_STAGE_TERM_OVERRIDES,
    MODULE_BOUNDARY_REGISTRY_PLANNING_WHITELIST_FILES,
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
from capabilities.midplatform.task_manager_module_integration_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_MODULE_INTEGRATION_PLANNING_ROOT,
    FINAL_DECISION_GO as MODULE_INTEGRATION_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as MODULE_INTEGRATION_PLANNING_NEXT_PHASE,
)

PHASE_ID = "Phase-Midplatform-Module-Boundary-Registry-Planning-v1-001"
SCOPE = "midplatform_module_boundary_registry_planning_only"
SOURCE_CHAIN = "module_boundary_registry_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_MODULE_BOUNDARY_REGISTRY_PLANNING_READY_FOR_CANDIDATE_LIFECYCLE_UNIFICATION_PLANNING"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_MODULE_BOUNDARY_REGISTRY_PLANNING_BLOCKED_BY_MODULE_INTEGRATION_PLANNING_GAP"
FINAL_DECISION_PLANNING = "MIDPLATFORM_MODULE_BOUNDARY_REGISTRY_PLANNING_BLOCKED_BY_REGISTRY_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_MODULE_BOUNDARY_REGISTRY_PLANNING_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_MODULE_BOUNDARY_REGISTRY_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_MODULE_BOUNDARY_REGISTRY_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
UPSTREAM_SELECTED_ROUTE = "Module Boundary Registry Planning"
NEXT_PHASE_GO = NEXT_ROUTE_A
NEXT_PHASE_HOLD = "Phase-Midplatform-Module-Boundary-Registry-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/module_boundary_registry_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_MODULE_BOUNDARY_REGISTRY_PLANNING_V1_GO_NO_GO_PACK_V0.md"
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/module_boundary_registry_planning_v1.py",
    "capabilities/midplatform/module_boundary_registry_items_v1.py",
    "capabilities/midplatform/module_boundary_registry_lineage_v1.py",
    "tools/evaluation/midplatform/run_module_boundary_registry_planning_v1.py",
    "tools/evaluation/midplatform/verify_module_boundary_registry_planning_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/module_boundary_registry_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PLANNING_ARTIFACTS: Tuple[str, ...] = (
    "module_boundary_registry_planning_report_v1.json",
    "module_boundary_registry_planning_report_v1.md",
    "boundary_registry_scope_v1.json",
    "module_boundary_registry_draft_v1.json",
    "ownership_matrix_v1.json",
    "not_owned_forbidden_transition_statement_v1.json",
    "boundary_conflict_detection_plan_v1.json",
    "boundary_dependency_graph_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_module_integration_planning_go",
    "boundary_registry_scope_complete",
    "module_boundary_registry_draft_complete",
    "ownership_matrix_complete",
    "not_owned_forbidden_transition_statement_complete",
    "boundary_conflict_detection_plan_complete",
    "boundary_dependency_graph_complete",
    "next_route_decision_complete",
    "do_not_misclassify_rules_complete",
    "all_required_modules_have_registry_entries",
    "no_forbidden_ownership_detected",
    "owner_approval_request_chain_not_reopened",
    "future_runtime_debt_not_current_blocker",
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
        "boundary_registry_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "module_integration_planning_root": str(upstream),
    }


def _entry_complete(row: Dict[str, Any]) -> bool:
    return all(row.get(f) is not None and row.get(f) != "" for f in REGISTRY_ENTRY_REQUIRED_FIELDS)


def _no_forbidden_ownership(entries: List[Dict[str, Any]]) -> bool:
    for module_id, obj in FORBIDDEN_OWNERSHIP_PAIRS:
        entry = next((e for e in entries if e.get("module_id") == module_id), {})
        owned = entry.get("owned_objects") or []
        if obj in owned:
            return False
    return True


def run_module_boundary_registry_planning_v1(
    *,
    module_integration_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(module_integration_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    planning_summary = _read_json(upstream / "summary.json")
    planning_verifier = _read_json(upstream / "verifier_report.json")
    planning_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_module_integration_planning_go = (
        planning_summary.get("final_decision") == MODULE_INTEGRATION_PLANNING_FINAL_GO
        and planning_summary.get("recommended_next_phase") == MODULE_INTEGRATION_PLANNING_NEXT_PHASE
        and planning_summary.get("selected_next_route") == UPSTREAM_SELECTED_ROUTE
        and planning_verifier.get("verifier") == "GO"
        and int(planning_verifier.get("passed_checks", 0)) >= 300
        and planning_summary.get("module_integration_planning_pass") is True
        and planning_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_module_integration_planning_go:
        issues.append("module_integration_planning_not_go")

    absence = {key: planning_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = planning_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(planning_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_module_integration_planning_go
        and planning_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    owner_approval_request_chain_not_reopened = (
        prior_module_integration_planning_go
        and planning_summary.get("owner_approval_request_chain_not_reopened") is True
    )

    registry_entries = [dict(e) for e in MODULE_BOUNDARY_REGISTRY_DRAFT]
    forbidden_transitions = [dict(t) for t in NOT_OWNED_FORBIDDEN_TRANSITIONS]
    ownership_rows = [dict(o) for o in OWNERSHIP_MATRIX]

    future_runtime_debt_not_current_blocker = all(
        e.get("runtime_required_now") is False for e in registry_entries
    )
    no_forbidden_ownership_detected = _no_forbidden_ownership(registry_entries)
    all_required_modules_have_registry_entries = len(registry_entries) >= 8 and all(_entry_complete(e) for e in registry_entries)

    boundary_registry_scope_complete = prior_module_integration_planning_go
    module_boundary_registry_draft_complete = all_required_modules_have_registry_entries
    ownership_matrix_complete = len(ownership_rows) >= 11 and len(OWNERSHIP_STATEMENTS) >= 7
    not_owned_forbidden_transition_statement_complete = len(forbidden_transitions) >= 8
    boundary_conflict_detection_plan_complete = len(BOUNDARY_CONFLICT_DETECTION_CHECKS) >= 8
    boundary_dependency_graph_complete = len(BOUNDARY_DEPENDENCY_NODES) >= 8 and len(BOUNDARY_DEPENDENCY_EDGES) >= 10
    next_route_decision_complete = SELECTED_NEXT_ROUTE == "Candidate Lifecycle Unification Planning"
    do_not_misclassify_rules_complete = future_runtime_debt_not_current_blocker and no_forbidden_ownership_detected

    if not no_forbidden_ownership_detected:
        issues.append("forbidden_ownership_detected")
    if not module_boundary_registry_draft_complete:
        issues.append("registry_draft_incomplete")

    template_lineage = build_template_lineage(
        base_phase="Task-Manager-Module-Integration-Planning-v1-001",
        base_capability=MODULE_BOUNDARY_REGISTRY_PLANNING_WHITELIST_FILES[0],
        base_runner=MODULE_BOUNDARY_REGISTRY_PLANNING_WHITELIST_FILES[1],
        base_verifier=MODULE_BOUNDARY_REGISTRY_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Module-Boundary-Registry-Planning-v1-001",
        stage_term_overrides=MODULE_BOUNDARY_REGISTRY_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=MODULE_BOUNDARY_REGISTRY_PLANNING_STAGE_ADDITIONS,
        template_files=MODULE_BOUNDARY_REGISTRY_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Task-Manager-Module-Integration-Planning-v1-001",
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
        previous_interruption_type=planning_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=planning_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=planning_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    planning_pass = (
        prior_module_integration_planning_go
        and boundary_registry_scope_complete
        and module_boundary_registry_draft_complete
        and ownership_matrix_complete
        and not_owned_forbidden_transition_statement_complete
        and boundary_conflict_detection_plan_complete
        and boundary_dependency_graph_complete
        and next_route_decision_complete
        and do_not_misclassify_rules_complete
        and all_required_modules_have_registry_entries
        and no_forbidden_ownership_detected
        and owner_approval_request_chain_not_reopened
        and future_runtime_debt_not_current_blocker
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase = NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD

    if not prior_module_integration_planning_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not module_boundary_registry_draft_complete:
        final_decision = FINAL_DECISION_PLANNING
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_module_integration_planning_go": prior_module_integration_planning_go,
        "boundary_registry_scope_complete": boundary_registry_scope_complete,
        "module_boundary_registry_draft_complete": module_boundary_registry_draft_complete,
        "ownership_matrix_complete": ownership_matrix_complete,
        "not_owned_forbidden_transition_statement_complete": not_owned_forbidden_transition_statement_complete,
        "boundary_conflict_detection_plan_complete": boundary_conflict_detection_plan_complete,
        "boundary_dependency_graph_complete": boundary_dependency_graph_complete,
        "next_route_decision_complete": next_route_decision_complete,
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "all_required_modules_have_registry_entries": all_required_modules_have_registry_entries,
        "no_forbidden_ownership_detected": no_forbidden_ownership_detected,
        "midplatform_still_has_remaining_work": planning_summary.get("midplatform_still_has_remaining_work") is True,
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
        "boundary_registry_planning_pass": planning_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "module_boundary_registry_planning_not_runtime_registry": True,
        "boundary_conflict_detection_plan_not_full_repo_scan": True,
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
            list(planning_summary.get("chain_trace_nodes") or []) + ["module_boundary_registry_planning"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    scope = {
        "scope_id": "boundary_registry_scope_v1",
        "boundary_registry_scope_complete": boundary_registry_scope_complete,
        "purpose": "Module boundary registry planning only — ownership, consumption, forbidden transitions",
        "not_runtime_registry": True,
        "not_integration_test": True,
        "not_real_execution": True,
        "not_reopen_owner_approval_request": True,
        **meta,
    }
    registry_draft = {
        "draft_id": "module_boundary_registry_draft_v1",
        "module_boundary_registry_draft_complete": module_boundary_registry_draft_complete,
        "entries": registry_entries,
        "entry_count": len(registry_entries),
        **meta,
    }
    ownership = {
        "matrix_id": "ownership_matrix_v1",
        "ownership_matrix_complete": ownership_matrix_complete,
        "rows": ownership_rows,
        "statements": list(OWNERSHIP_STATEMENTS),
        **meta,
    }
    forbidden_stmt = {
        "statement_id": "not_owned_forbidden_transition_statement_v1",
        "not_owned_forbidden_transition_statement_complete": not_owned_forbidden_transition_statement_complete,
        "transitions": forbidden_transitions,
        **meta,
    }
    conflict_plan = {
        "plan_id": "boundary_conflict_detection_plan_v1",
        "boundary_conflict_detection_plan_complete": boundary_conflict_detection_plan_complete,
        "checks": list(BOUNDARY_CONFLICT_DETECTION_CHECKS),
        "full_repo_scan": False,
        "execution_deferred": True,
        **meta,
    }
    dep_graph = {
        "graph_id": "boundary_dependency_graph_v1",
        "boundary_dependency_graph_complete": boundary_dependency_graph_complete,
        "nodes": list(BOUNDARY_DEPENDENCY_NODES),
        "edges": list(BOUNDARY_DEPENDENCY_EDGES),
        **meta,
    }
    route_decision = {
        "decision_id": "next_route_decision_v1",
        "next_route_decision_complete": next_route_decision_complete,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": next_phase,
        "rationale": "Boundary registry planning complete; candidate lifecycle unification is next structural layer",
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
            "boundary_registry_planning_not_runtime_registry",
            "ownership_matrix_not_write_permission_grant",
            "boundary_registry_not_module_adapter",
            "boundary_dependency_graph_not_execution_graph",
            "conflict_detection_plan_not_full_repo_scan",
            "future_runtime_debt_not_current_blocker",
            "owner_approval_request_chain_not_reopened",
        ],
        **meta,
    }
    report = {"report_id": "module_boundary_registry_planning_report_v1", **go_values, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_registry_planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join([
        "# Module Boundary Registry Planning v1",
        "",
        f"Registry entries: `{len(registry_entries)}`",
        f"Ownership matrix rows: `{len(ownership_rows)}`",
        f"Forbidden transitions: `{len(forbidden_transitions)}`",
        f"Selected next route: `{SELECTED_NEXT_ROUTE}`",
        f"Final decision: `{final_decision}`",
        f"Next phase: `{next_phase}`",
    ])
    return {
        "module_boundary_registry_planning_report": report,
        "module_boundary_registry_planning_report_md": markdown,
        "boundary_registry_scope": scope,
        "module_boundary_registry_draft": registry_draft,
        "ownership_matrix": ownership,
        "not_owned_forbidden_transition_statement": forbidden_stmt,
        "boundary_conflict_detection_plan": conflict_plan,
        "boundary_dependency_graph": dep_graph,
        "next_route_decision": route_decision,
        "do_not_misclassify_rules": misclassify_rules,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
