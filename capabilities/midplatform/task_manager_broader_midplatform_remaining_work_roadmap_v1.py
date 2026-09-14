# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Broader Midplatform Remaining Work Roadmap v1.

Inventory and reprioritize midplatform remaining work. No runtime / no integration test.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_broader_midplatform_remaining_work_items_v1 import (
    MODULE_COMPLETION_CANDIDATES,
    REMAINING_WORK_ITEMS,
    WORK_MATRIX_REQUIRED_FIELDS,
)
from capabilities.midplatform.task_manager_broader_midplatform_remaining_work_lineage_v1 import (
    BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_STAGE_ADDITIONS,
    BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_STAGE_TERM_OVERRIDES,
    BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_WHITELIST_FILES,
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
from capabilities.midplatform.task_manager_foundation_closure_consolidation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FOUNDATION_CONSOLIDATION_ROOT,
    FINAL_DECISION_GO as FOUNDATION_CONSOLIDATION_FINAL_GO,
    NEXT_PHASE_GO as FOUNDATION_CONSOLIDATION_NEXT_PHASE,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Broader-Midplatform-Remaining-Work-Roadmap-v1-001"
SCOPE = "midplatform_task_manager_broader_midplatform_remaining_work_roadmap_only"
SOURCE_CHAIN = "midplatform_task_manager_broader_midplatform_remaining_work_roadmap_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_READY_FOR_MODULE_INTEGRATION_PLANNING_OR_GOVERNANCE_DEBT_CONSOLIDATION"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_BLOCKED_BY_FOUNDATION_CONSOLIDATION_GAP"
)
FINAL_DECISION_ROADMAP = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_BLOCKED_BY_ROADMAP_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
SELECTED_ROUTE = "Midplatform Module Integration Planning"
ROUTE_A = "Phase-Midplatform-Task-Manager-Module-Integration-Planning-v1-001"
ROUTE_B = "Phase-Midplatform-Governance-Debt-Consolidation-v1-001"
ROUTE_C = "Phase-Midplatform-Candidate-Lifecycle-Unification-Planning-v1-001"
ROUTE_D = "Phase-Midplatform-Module-Boundary-Registry-Planning-v1-001"
ROUTE_E = "Phase-Midplatform-Task-Manager-Integration-Test-Planning-v1-001"
NEXT_PHASE_GO = ROUTE_A
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Broader-Midplatform-Remaining-Work-Roadmap-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_broader_midplatform_remaining_work_roadmap_v1_smoke_v0"
)
ROADMAP_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_TASK_MANAGER_BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_broader_midplatform_remaining_work_roadmap_v1.py",
    "capabilities/midplatform/task_manager_broader_midplatform_remaining_work_items_v1.py",
    "capabilities/midplatform/task_manager_broader_midplatform_remaining_work_lineage_v1.py",
    "tools/evaluation/midplatform/run_task_manager_broader_midplatform_remaining_work_roadmap_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_broader_midplatform_remaining_work_roadmap_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = (
    "capabilities/midplatform/task_manager_broader_midplatform_remaining_work_lineage_v1.py"
)
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

ROADMAP_ARTIFACTS: Tuple[str, ...] = (
    "broader_midplatform_remaining_work_roadmap_v1.json",
    "broader_midplatform_remaining_work_roadmap_v1.md",
    "remaining_work_scope_v1.json",
    "remaining_work_inventory_v1.json",
    "work_classification_matrix_v1.json",
    "mainline_priority_plan_v1.json",
    "module_completion_candidates_v1.json",
    "governance_debt_positioning_v1.json",
    "test_readiness_positioning_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_foundation_consolidation_go",
    "remaining_work_scope_complete",
    "remaining_work_inventory_complete",
    "work_classification_matrix_complete",
    "mainline_priority_plan_complete",
    "module_completion_candidates_complete",
    "governance_debt_positioning_complete",
    "test_readiness_positioning_complete",
    "next_route_decision_complete",
    "do_not_misclassify_rules_complete",
    "midplatform_still_has_remaining_work",
    "future_runtime_debt_not_current_blocker",
    "future_design_not_current_blocker",
    "owner_approval_request_chain_not_reopened",
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
        "remaining_work_roadmap_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "foundation_consolidation_root": str(upstream),
    }


def _matrix_row_complete(row: Dict[str, Any]) -> bool:
    return all(row.get(f) is not None and row.get(f) != "" for f in WORK_MATRIX_REQUIRED_FIELDS)


def run_task_manager_broader_midplatform_remaining_work_roadmap_v1(
    *,
    foundation_consolidation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(foundation_consolidation_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    foundation_summary = _read_json(upstream / "summary.json")
    foundation_verifier = _read_json(upstream / "verifier_report.json")
    foundation_remaining = _read_json(upstream / "remaining_work_register_v1.json")
    foundation_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_foundation_consolidation_go = (
        foundation_summary.get("final_decision") == FOUNDATION_CONSOLIDATION_FINAL_GO
        and foundation_summary.get("recommended_next_phase") == FOUNDATION_CONSOLIDATION_NEXT_PHASE
        and foundation_verifier.get("verifier") == "GO"
        and int(foundation_verifier.get("passed_checks", 0)) >= 260
        and foundation_summary.get("foundation_consolidation_pass") is True
        and foundation_summary.get("foundation_consolidation_not_final_midplatform_completion") is True
        and foundation_summary.get("midplatform_still_has_remaining_work") is True
        and foundation_summary.get("no_fragmentary_phase_expansion") is True
        and foundation_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_foundation_consolidation_go:
        issues.append("foundation_consolidation_not_go")

    absence = {key: foundation_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = foundation_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(foundation_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_foundation_consolidation_go
        and foundation_summary.get("non_execution_boundary_ok") is True
        and foundation_summary.get("real_execution_not_authorized") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    owner_approval_request_chain_not_reopened = (
        prior_foundation_consolidation_go
        and foundation_summary.get("owner_approval_request_chain_not_reopened") is True
    )

    work_rows = [dict(item) for item in REMAINING_WORK_ITEMS]
    future_runtime_debt_not_current_blocker = all(
        not row.get("blocker_now") for row in work_rows if row.get("category") == "future_runtime_debt"
    )
    future_design_not_current_blocker = all(
        not row.get("blocker_now") for row in work_rows if row.get("category") == "future_design"
    )
    if not future_runtime_debt_not_current_blocker:
        issues.append("runtime_debt_misclassified_as_blocker")
    if not future_design_not_current_blocker:
        issues.append("future_design_misclassified_as_blocker")

    remaining_work_scope_complete = prior_foundation_consolidation_go
    remaining_work_inventory_complete = len(work_rows) >= 15
    work_classification_matrix_complete = (
        remaining_work_inventory_complete and all(_matrix_row_complete(r) for r in work_rows)
    )
    if not work_classification_matrix_complete:
        issues.append("work_matrix_incomplete")

    mainline_priority_plan_complete = prior_foundation_consolidation_go
    module_completion_candidates_complete = len(MODULE_COMPLETION_CANDIDATES) >= 6
    governance_debt_positioning_complete = prior_foundation_consolidation_go
    test_readiness_positioning_complete = prior_foundation_consolidation_go
    next_route_decision_complete = SELECTED_ROUTE == "Midplatform Module Integration Planning"
    do_not_misclassify_rules_complete = (
        future_runtime_debt_not_current_blocker
        and future_design_not_current_blocker
        and foundation_summary.get("foundation_consolidation_not_final_midplatform_completion") is True
    )
    midplatform_still_has_remaining_work = foundation_remaining.get("midplatform_still_has_remaining_work") is True

    template_lineage = build_template_lineage(
        base_phase="Task-Manager-Foundation-Closure-Consolidation-v1-001",
        base_capability=BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_WHITELIST_FILES[0],
        base_runner=BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_WHITELIST_FILES[1],
        base_verifier=BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_WHITELIST_FILES[2],
        base_go_no_go_pack=ROADMAP_GO_NO_GO_PACK,
        stage_phase="Task-Manager-Broader-Midplatform-Remaining-Work-Roadmap-v1-001",
        stage_term_overrides=BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_STAGE_TERM_OVERRIDES,
        stage_additions=BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_STAGE_ADDITIONS,
        template_files=BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Task-Manager-Foundation-Closure-Consolidation-v1-001",
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
        previous_interruption_type=foundation_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=foundation_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=foundation_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    roadmap_pass = (
        prior_foundation_consolidation_go
        and remaining_work_scope_complete
        and remaining_work_inventory_complete
        and work_classification_matrix_complete
        and mainline_priority_plan_complete
        and module_completion_candidates_complete
        and governance_debt_positioning_complete
        and test_readiness_positioning_complete
        and next_route_decision_complete
        and do_not_misclassify_rules_complete
        and midplatform_still_has_remaining_work
        and future_runtime_debt_not_current_blocker
        and future_design_not_current_blocker
        and owner_approval_request_chain_not_reopened
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase_readiness_ok = roadmap_pass
    next_phase = NEXT_PHASE_GO if roadmap_pass else NEXT_PHASE_HOLD

    if not prior_foundation_consolidation_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not work_classification_matrix_complete:
        final_decision = FINAL_DECISION_ROADMAP
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    deferred_items = [r["work_id"] for r in work_rows if r.get("can_defer") is True]
    go_values = {
        "prior_foundation_consolidation_go": prior_foundation_consolidation_go,
        "remaining_work_scope_complete": remaining_work_scope_complete,
        "remaining_work_inventory_complete": remaining_work_inventory_complete,
        "work_classification_matrix_complete": work_classification_matrix_complete,
        "mainline_priority_plan_complete": mainline_priority_plan_complete,
        "module_completion_candidates_complete": module_completion_candidates_complete,
        "governance_debt_positioning_complete": governance_debt_positioning_complete,
        "test_readiness_positioning_complete": test_readiness_positioning_complete,
        "next_route_decision_complete": next_route_decision_complete,
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "midplatform_still_has_remaining_work": midplatform_still_has_remaining_work,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "foundation_layer_consolidated": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "future_runtime_debt_not_current_blocker": future_runtime_debt_not_current_blocker,
        "future_design_not_current_blocker": future_design_not_current_blocker,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "owner_approval_request_closed_module": "governance_ready_handoff",
        "real_execution_not_authorized": foundation_summary.get("real_execution_not_authorized") is True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "remaining_work_roadmap_pass": roadmap_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "selected_route": SELECTED_ROUTE,
        "deferred_item_count": len(deferred_items),
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
            list(foundation_summary.get("chain_trace_nodes") or [])
            + ["task_manager_broader_midplatform_remaining_work_roadmap"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    remaining_scope = {
        "scope_id": "remaining_work_scope_v1",
        "remaining_work_scope_complete": remaining_work_scope_complete,
        "purpose": "Inventory and reprioritize midplatform remaining work only",
        "not_runtime": True,
        "not_integration_test": True,
        "not_real_issuance_preauth": True,
        "not_midplatform_completed": True,
        **meta,
    }
    work_inventory = {
        "inventory_id": "remaining_work_inventory_v1",
        "remaining_work_inventory_complete": remaining_work_inventory_complete,
        "work_item_count": len(work_rows),
        "items": [{"work_id": r["work_id"], "work_name": r["work_name"], "category": r["category"]} for r in work_rows],
        **meta,
    }
    work_matrix = {
        "matrix_id": "work_classification_matrix_v1",
        "work_classification_matrix_complete": work_classification_matrix_complete,
        "rows": work_rows,
        "deferred_items": deferred_items,
        **meta,
    }
    priority_plan = {
        "plan_id": "mainline_priority_plan_v1",
        "mainline_priority_plan_complete": mainline_priority_plan_complete,
        "phases": [
            {"priority": "P1", "phase": "Remaining Work Roadmap", "status": "current"},
            {"priority": "P2", "phase": "Module Integration Planning / Governance Debt", "status": "next"},
            {"priority": "P3", "phase": "Integration Test Planning", "status": "deferred"},
            {"priority": "P4", "phase": "Runtime Adapter / Whitebox / Real Execution Preauth", "status": "future"},
            {"priority": "future", "phase": "Task Center / Drive Brain / Elasticity", "status": "future_design"},
        ],
        **meta,
    }
    module_candidates = {
        "candidates_id": "module_completion_candidates_v1",
        "module_completion_candidates_complete": module_completion_candidates_complete,
        "candidates": list(MODULE_COMPLETION_CANDIDATES),
        "implementation_now": False,
        **meta,
    }
    governance_positioning = {
        "positioning_id": "governance_debt_positioning_v1",
        "governance_debt_positioning_complete": governance_debt_positioning_complete,
        "governance_debt_consolidation_first": False,
        "structural_debt": ["module_boundary_gaps", "candidate_lifecycle_fragmentation"],
        "future_runtime_debt": ["runtime_adapter_implementation", "whitebox_runtime_integration"],
        "optional_quality": ["governance_debt_consolidation"],
        "future_runtime_debt_not_current_blocker": future_runtime_debt_not_current_blocker,
        **meta,
    }
    test_positioning = {
        "positioning_id": "test_readiness_positioning_v1",
        "test_readiness_positioning_complete": test_readiness_positioning_complete,
        "integration_test_executed": False,
        "integration_test_planning_deferred": True,
        "preconditions_for_integration_test_planning": [
            "module_integration_planning_complete",
            "module_boundary_registry_planned",
            "foundation_consolidation_package_available",
        ],
        "owner_approval_request_slice_dryrun_as_input": True,
        "foundation_consolidation_package_as_input": True,
        **meta,
    }
    route_decision = {
        "decision_id": "next_route_decision_v1",
        "next_route_decision_complete": next_route_decision_complete,
        "selected_route": SELECTED_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": next_phase,
        "alternate_routes": [
            {"route_id": "B", "phase_id": ROUTE_B},
            {"route_id": "C", "phase_id": ROUTE_C},
            {"route_id": "D", "phase_id": ROUTE_D},
            {"route_id": "E", "phase_id": ROUTE_E, "defer_reason": "After module integration planning"},
        ],
        "do_not_declare_midplatform_completed": True,
        **meta,
    }
    misclassify_rules = {
        "rules_id": "do_not_misclassify_rules_v1",
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "rules": [
            "remaining_work_roadmap_not_implementation",
            "remaining_work_roadmap_not_integration_test",
            "remaining_work_roadmap_not_runtime_readiness",
            "remaining_work_roadmap_not_midplatform_completed",
            "future_design_not_current_blocker",
            "future_runtime_debt_not_current_blocker",
            "owner_approval_request_chain_not_reopened",
        ],
        **meta,
    }
    roadmap = {
        "roadmap_id": "broader_midplatform_remaining_work_roadmap_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "remaining_work_roadmap_pass": roadmap_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Broader Midplatform Remaining Work Roadmap v1",
            "",
            "Midplatform remaining work inventory and mainline reprioritization.",
            "",
            f"Overall status: `{MIDPLATFORM_OVERALL_STATUS}` (NOT midplatform completed)",
            f"Work items: `{len(work_rows)}`",
            f"Deferred items: `{len(deferred_items)}`",
            f"Selected route: `{SELECTED_ROUTE}`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "broader_midplatform_remaining_work_roadmap": roadmap,
        "broader_midplatform_remaining_work_roadmap_md": markdown,
        "remaining_work_scope": remaining_scope,
        "remaining_work_inventory": work_inventory,
        "work_classification_matrix": work_matrix,
        "mainline_priority_plan": priority_plan,
        "module_completion_candidates": module_candidates,
        "governance_debt_positioning": governance_positioning,
        "test_readiness_positioning": test_positioning,
        "next_route_decision": route_decision,
        "do_not_misclassify_rules": misclassify_rules,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
