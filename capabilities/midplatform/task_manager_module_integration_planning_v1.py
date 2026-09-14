# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Module Integration Planning v1.

Plan module boundaries, lifecycle, alignment, and orchestration positioning. No runtime / no integration test.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_broader_midplatform_remaining_work_roadmap_v1 import (
    DEFAULT_OUTPUT as DEFAULT_REMAINING_WORK_ROADMAP_ROOT,
    FINAL_DECISION_GO as REMAINING_WORK_ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as REMAINING_WORK_ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE as UPSTREAM_SELECTED_ROUTE,
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
from capabilities.midplatform.task_manager_module_integration_planning_items_v1 import (
    ALIGNMENT_OBJECT_PAIRS,
    ALIGNMENT_PLAN_RULES,
    CANDIDATE_LIFECYCLE_INTEGRATION_PLAN,
    CANDIDATE_LIFECYCLE_TYPES,
    DEPENDENCY_GRAPH_EDGES,
    DEPENDENCY_GRAPH_NODES,
    INTEGRATION_GAPS,
    MODULE_BOUNDARY_INTEGRATION_MAP,
    MODULE_BOUNDARY_REQUIRED_FIELDS,
    NEXT_ROUTE_A,
    NEXT_ROUTE_B,
    NEXT_ROUTE_C,
    NEXT_ROUTE_D,
    NEXT_ROUTE_E,
    ORCHESTRATION_SKELETON_EXCLUSIONS,
    ORCHESTRATION_SKELETON_RESPONSIBILITIES,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.task_manager_module_integration_planning_lineage_v1 import (
    MODULE_INTEGRATION_PLANNING_STAGE_ADDITIONS,
    MODULE_INTEGRATION_PLANNING_STAGE_TERM_OVERRIDES,
    MODULE_INTEGRATION_PLANNING_WHITELIST_FILES,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Module-Integration-Planning-v1-001"
SCOPE = "midplatform_task_manager_module_integration_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_module_integration_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_MODULE_INTEGRATION_PLANNING_READY_FOR_MODULE_BOUNDARY_REGISTRY_OR_CANDIDATE_LIFECYCLE_UNIFICATION"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_MODULE_INTEGRATION_PLANNING_BLOCKED_BY_REMAINING_WORK_ROADMAP_GAP"
)
FINAL_DECISION_PLANNING = (
    "MIDPLATFORM_TASK_MANAGER_MODULE_INTEGRATION_PLANNING_BLOCKED_BY_PLANNING_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_MODULE_INTEGRATION_PLANNING_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_MODULE_INTEGRATION_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_MODULE_INTEGRATION_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = NEXT_ROUTE_A
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Module-Integration-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_module_integration_planning_v1_smoke_v0"
)
GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_TASK_MANAGER_MODULE_INTEGRATION_PLANNING_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_module_integration_planning_v1.py",
    "capabilities/midplatform/task_manager_module_integration_planning_items_v1.py",
    "capabilities/midplatform/task_manager_module_integration_planning_lineage_v1.py",
    "tools/evaluation/midplatform/run_task_manager_module_integration_planning_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_module_integration_planning_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_module_integration_planning_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PLANNING_ARTIFACTS: Tuple[str, ...] = (
    "module_integration_planning_report_v1.json",
    "module_integration_planning_report_v1.md",
    "integration_planning_scope_v1.json",
    "module_boundary_integration_map_v1.json",
    "candidate_lifecycle_integration_plan_v1.json",
    "evidence_record_approval_permission_alignment_plan_v1.json",
    "task_manager_core_orchestration_skeleton_positioning_v1.json",
    "module_integration_dependency_graph_v1.json",
    "integration_gap_register_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_remaining_work_roadmap_go",
    "integration_planning_scope_complete",
    "module_boundary_integration_map_complete",
    "candidate_lifecycle_integration_plan_complete",
    "evidence_record_approval_permission_alignment_plan_complete",
    "task_manager_core_orchestration_skeleton_positioning_complete",
    "module_integration_dependency_graph_complete",
    "integration_gap_register_complete",
    "next_route_decision_complete",
    "do_not_misclassify_rules_complete",
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
        "module_integration_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "remaining_work_roadmap_root": str(upstream),
    }


def _module_row_complete(row: Dict[str, Any]) -> bool:
    return all(row.get(f) is not None and row.get(f) != "" for f in MODULE_BOUNDARY_REQUIRED_FIELDS)


def run_task_manager_module_integration_planning_v1(
    *,
    remaining_work_roadmap_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(remaining_work_roadmap_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    roadmap_summary = _read_json(upstream / "summary.json")
    roadmap_verifier = _read_json(upstream / "verifier_report.json")
    roadmap_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_remaining_work_roadmap_go = (
        roadmap_summary.get("final_decision") == REMAINING_WORK_ROADMAP_FINAL_GO
        and roadmap_summary.get("recommended_next_phase") == REMAINING_WORK_ROADMAP_NEXT_PHASE
        and roadmap_summary.get("selected_route") == UPSTREAM_SELECTED_ROUTE
        and roadmap_verifier.get("verifier") == "GO"
        and int(roadmap_verifier.get("passed_checks", 0)) >= 280
        and roadmap_summary.get("remaining_work_roadmap_pass") is True
        and roadmap_summary.get("midplatform_still_has_remaining_work") is True
        and roadmap_summary.get("no_fragmentary_phase_expansion") is True
        and roadmap_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_remaining_work_roadmap_go:
        issues.append("remaining_work_roadmap_not_go")

    absence = {key: roadmap_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = roadmap_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(roadmap_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_remaining_work_roadmap_go
        and roadmap_summary.get("non_execution_boundary_ok") is True
        and roadmap_summary.get("real_execution_not_authorized") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    owner_approval_request_chain_not_reopened = (
        prior_remaining_work_roadmap_go
        and roadmap_summary.get("owner_approval_request_chain_not_reopened") is True
    )

    module_rows = [dict(m) for m in MODULE_BOUNDARY_INTEGRATION_MAP]
    lifecycle_plan = [dict(c) for c in CANDIDATE_LIFECYCLE_INTEGRATION_PLAN]
    gap_rows = [dict(g) for g in INTEGRATION_GAPS]

    future_runtime_debt_not_current_blocker = all(
        not g.get("blocker_now") for g in gap_rows if g.get("status") == "future_runtime_debt"
    )
    if not future_runtime_debt_not_current_blocker:
        issues.append("runtime_debt_misclassified_as_blocker")

    integration_planning_scope_complete = prior_remaining_work_roadmap_go
    module_boundary_integration_map_complete = (
        len(module_rows) >= 8 and all(_module_row_complete(r) for r in module_rows)
        and all(r.get("runtime_required_now") is False for r in module_rows)
    )
    candidate_lifecycle_integration_plan_complete = len(lifecycle_plan) >= len(CANDIDATE_LIFECYCLE_TYPES)
    alignment_plan_complete = (
        len(ALIGNMENT_OBJECT_PAIRS) >= 6
        and len(ALIGNMENT_PLAN_RULES) >= 8
    )
    orchestration_positioning_complete = (
        len(ORCHESTRATION_SKELETON_RESPONSIBILITIES) >= 2
        and len(ORCHESTRATION_SKELETON_EXCLUSIONS) >= 5
    )
    dependency_graph_complete = len(DEPENDENCY_GRAPH_NODES) >= 8 and len(DEPENDENCY_GRAPH_EDGES) >= 10
    integration_gap_register_complete = len(gap_rows) >= 8
    next_route_decision_complete = SELECTED_NEXT_ROUTE == "Module Boundary Registry Planning"
    do_not_misclassify_rules_complete = (
        future_runtime_debt_not_current_blocker
        and roadmap_summary.get("foundation_consolidation_not_final_midplatform_completion") is True
    )

    if not module_boundary_integration_map_complete:
        issues.append("module_boundary_map_incomplete")
    if not candidate_lifecycle_integration_plan_complete:
        issues.append("lifecycle_plan_incomplete")
    if not alignment_plan_complete:
        issues.append("alignment_plan_incomplete")

    template_lineage = build_template_lineage(
        base_phase="Task-Manager-Broader-Midplatform-Remaining-Work-Roadmap-v1-001",
        base_capability=MODULE_INTEGRATION_PLANNING_WHITELIST_FILES[0],
        base_runner=MODULE_INTEGRATION_PLANNING_WHITELIST_FILES[1],
        base_verifier=MODULE_INTEGRATION_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Task-Manager-Module-Integration-Planning-v1-001",
        stage_term_overrides=MODULE_INTEGRATION_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=MODULE_INTEGRATION_PLANNING_STAGE_ADDITIONS,
        template_files=MODULE_INTEGRATION_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Task-Manager-Broader-Midplatform-Remaining-Work-Roadmap-v1-001",
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
        previous_interruption_type=roadmap_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=roadmap_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=roadmap_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    planning_pass = (
        prior_remaining_work_roadmap_go
        and integration_planning_scope_complete
        and module_boundary_integration_map_complete
        and candidate_lifecycle_integration_plan_complete
        and alignment_plan_complete
        and orchestration_positioning_complete
        and dependency_graph_complete
        and integration_gap_register_complete
        and next_route_decision_complete
        and do_not_misclassify_rules_complete
        and owner_approval_request_chain_not_reopened
        and future_runtime_debt_not_current_blocker
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase_readiness_ok = planning_pass
    next_phase = NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD

    if not prior_remaining_work_roadmap_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not (module_boundary_integration_map_complete and candidate_lifecycle_integration_plan_complete):
        final_decision = FINAL_DECISION_PLANNING
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_remaining_work_roadmap_go": prior_remaining_work_roadmap_go,
        "integration_planning_scope_complete": integration_planning_scope_complete,
        "module_boundary_integration_map_complete": module_boundary_integration_map_complete,
        "candidate_lifecycle_integration_plan_complete": candidate_lifecycle_integration_plan_complete,
        "evidence_record_approval_permission_alignment_plan_complete": alignment_plan_complete,
        "task_manager_core_orchestration_skeleton_positioning_complete": orchestration_positioning_complete,
        "module_integration_dependency_graph_complete": dependency_graph_complete,
        "integration_gap_register_complete": integration_gap_register_complete,
        "next_route_decision_complete": next_route_decision_complete,
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "midplatform_still_has_remaining_work": roadmap_summary.get("midplatform_still_has_remaining_work") is True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "future_runtime_debt_not_current_blocker": future_runtime_debt_not_current_blocker,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "owner_approval_request_closed_module": "governance_ready_handoff",
        "real_execution_not_authorized": roadmap_summary.get("real_execution_not_authorized") is True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "module_integration_planning_pass": planning_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "selected_route": UPSTREAM_SELECTED_ROUTE,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "candidate_not_promoted_to_record": True,
        "permission_candidate_not_promoted_to_grant": True,
        "authorization_request_candidate_not_promoted_to_authorization_request": True,
        "module_integration_planning_not_integration_test": True,
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
            list(roadmap_summary.get("chain_trace_nodes") or [])
            + ["task_manager_module_integration_planning"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    scope = {
        "scope_id": "integration_planning_scope_v1",
        "integration_planning_scope_complete": integration_planning_scope_complete,
        "purpose": "Module integration planning only — boundaries, lifecycle, alignment, orchestration positioning",
        "not_runtime": True,
        "not_integration_test": True,
        "not_real_execution": True,
        "not_reopen_owner_approval_request": True,
        **meta,
    }
    boundary_map = {
        "map_id": "module_boundary_integration_map_v1",
        "module_boundary_integration_map_complete": module_boundary_integration_map_complete,
        "modules": module_rows,
        "module_count": len(module_rows),
        **meta,
    }
    lifecycle = {
        "plan_id": "candidate_lifecycle_integration_plan_v1",
        "candidate_lifecycle_integration_plan_complete": candidate_lifecycle_integration_plan_complete,
        "candidate_types": list(CANDIDATE_LIFECYCLE_TYPES),
        "plans": lifecycle_plan,
        "runtime_implementation": False,
        **meta,
    }
    alignment = {
        "plan_id": "evidence_record_approval_permission_alignment_plan_v1",
        "evidence_record_approval_permission_alignment_plan_complete": alignment_plan_complete,
        "object_pairs": list(ALIGNMENT_OBJECT_PAIRS),
        "rules": list(ALIGNMENT_PLAN_RULES),
        "no_real_record_created": True,
        "no_real_grant_created": True,
        "no_real_authorization_request_created": True,
        **meta,
    }
    orchestration = {
        "positioning_id": "task_manager_core_orchestration_skeleton_positioning_v1",
        "task_manager_core_orchestration_skeleton_positioning_complete": orchestration_positioning_complete,
        "responsibilities": list(ORCHESTRATION_SKELETON_RESPONSIBILITIES),
        "exclusions": list(ORCHESTRATION_SKELETON_EXCLUSIONS),
        "future_drive_brain_base": True,
        "drive_brain_implementation_now": False,
        **meta,
    }
    dependency_graph = {
        "graph_id": "module_integration_dependency_graph_v1",
        "module_integration_dependency_graph_complete": dependency_graph_complete,
        "nodes": list(DEPENDENCY_GRAPH_NODES),
        "edges": list(DEPENDENCY_GRAPH_EDGES),
        **meta,
    }
    gap_register = {
        "register_id": "integration_gap_register_v1",
        "integration_gap_register_complete": integration_gap_register_complete,
        "gaps": gap_rows,
        **meta,
    }
    route_decision = {
        "decision_id": "next_route_decision_v1",
        "next_route_decision_complete": next_route_decision_complete,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": next_phase,
        "rationale": "Module boundary is foundational prerequisite for lifecycle and alignment modules",
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
            "module_integration_planning_not_integration_test",
            "module_integration_planning_not_runtime_implementation",
            "module_integration_planning_not_final_midplatform_completion",
            "candidate_lifecycle_plan_not_lifecycle_runtime",
            "alignment_plan_not_record_grant_creation",
            "future_runtime_debt_not_current_blocker",
            "owner_approval_request_chain_not_reopened",
        ],
        **meta,
    }
    report = {
        "report_id": "module_integration_planning_report_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "module_integration_planning_pass": planning_pass,
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
            "# Module Integration Planning v1",
            "",
            "Task Manager / Midplatform module integration planning.",
            "",
            f"Overall status: `{MIDPLATFORM_OVERALL_STATUS}` (NOT midplatform completed)",
            f"Modules mapped: `{len(module_rows)}`",
            f"Candidate types: `{len(CANDIDATE_LIFECYCLE_TYPES)}`",
            f"Integration gaps: `{len(gap_rows)}`",
            f"Selected next route: `{SELECTED_NEXT_ROUTE}`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "module_integration_planning_report": report,
        "module_integration_planning_report_md": markdown,
        "integration_planning_scope": scope,
        "module_boundary_integration_map": boundary_map,
        "candidate_lifecycle_integration_plan": lifecycle,
        "evidence_record_approval_permission_alignment_plan": alignment,
        "task_manager_core_orchestration_skeleton_positioning": orchestration,
        "module_integration_dependency_graph": dependency_graph,
        "integration_gap_register": gap_register,
        "next_route_decision": route_decision,
        "do_not_misclassify_rules": misclassify_rules,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
