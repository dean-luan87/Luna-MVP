# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Core Orchestration Implementation Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_core_orchestration_implementation_items_v1 import (
    ALLOWED_DEPENDENCIES,
    DATA_STRUCTURE_PLAN,
    FORBIDDEN_DEPENDENCIES,
    FUNCTIONAL_UNIT_REQUIRED_FIELDS,
    IMPLEMENTATION_FILES,
    IMPLEMENTATION_GAPS,
    NEXT_ROUTE_A,
    NEXT_ROUTE_B,
    NEXT_ROUTE_C,
    NEXT_ROUTE_D,
    NEXT_ROUTE_E,
    NON_EXECUTION_GUARDS,
    ORCHESTRATION_FUNCTIONAL_UNITS,
    SELECTED_NEXT_ROUTE,
    STATIC_VALIDATORS,
)
from capabilities.midplatform.task_manager_core_orchestration_implementation_lineage_v1 import (
    ORCHESTRATION_IMPLEMENTATION_PLANNING_STAGE_ADDITIONS,
    ORCHESTRATION_IMPLEMENTATION_PLANNING_STAGE_TERM_OVERRIDES,
    ORCHESTRATION_IMPLEMENTATION_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_consolidation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ORCHESTRATION_CONSOLIDATION_ROOT,
    FINAL_DECISION_GO as ORCHESTRATION_CONSOLIDATION_FINAL_GO,
    NEXT_PHASE_GO as ORCHESTRATION_CONSOLIDATION_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_items_v1 import (
    SELECTED_NEXT_ROUTE as UPSTREAM_CONSOLIDATION_SELECTED_ROUTE,
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

PHASE_ID = "Phase-Midplatform-Task-Manager-Core-Orchestration-Skeleton-Implementation-Planning-v1-001"
SCOPE = "midplatform_task_manager_core_orchestration_implementation_planning_only"
SOURCE_CHAIN = "task_manager_core_orchestration_implementation_planning_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_IMPLEMENTATION_PLANNING_READY_FOR_CONTROLLED_SKELETON_IMPLEMENTATION"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_IMPLEMENTATION_PLANNING_BLOCKED_BY_CONSOLIDATION_GAP"
FINAL_DECISION_PLANNING = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_IMPLEMENTATION_PLANNING_BLOCKED_BY_PLANNING_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_IMPLEMENTATION_PLANNING_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_IMPLEMENTATION_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_IMPLEMENTATION_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = NEXT_ROUTE_A
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Core-Orchestration-Implementation-Planning-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/task_manager_core_orchestration_implementation_planning_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_CORE_ORCHESTRATION_IMPLEMENTATION_PLANNING_V1_GO_NO_GO_PACK_V0.md"
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_core_orchestration_implementation_planning_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_implementation_items_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_implementation_lineage_v1.py",
    "tools/evaluation/midplatform/run_task_manager_core_orchestration_implementation_planning_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_core_orchestration_implementation_planning_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_core_orchestration_implementation_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

PLANNING_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_core_orchestration_implementation_planning_report_v1.json",
    "task_manager_core_orchestration_implementation_planning_report_v1.md",
    "implementation_planning_scope_v1.json",
    "orchestration_functional_units_v1.json",
    "orchestration_data_structure_plan_v1.json",
    "static_validator_plan_v1.json",
    "implementation_file_plan_v1.json",
    "implementation_dependency_plan_v1.json",
    "non_execution_implementation_guard_plan_v1.json",
    "implementation_gap_register_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_orchestration_skeleton_consolidation_go",
    "implementation_planning_scope_complete",
    "orchestration_functional_units_complete",
    "orchestration_data_structure_plan_complete",
    "static_validator_plan_complete",
    "implementation_file_plan_complete",
    "implementation_dependency_plan_complete",
    "non_execution_implementation_guard_plan_complete",
    "implementation_gap_register_complete",
    "next_route_decision_complete",
    "do_not_misclassify_rules_complete",
    "implementation_files_split_by_responsibility",
    "controlled_implementation_ready",
    "non_execution_boundary_ok",
    "future_design_not_current_blocker",
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
        "orchestration_implementation_planning_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        "orchestration_skeleton_consolidation_root": str(upstream),
    }


def _unit_complete(row: Dict[str, Any]) -> bool:
    return all(row.get(f) is not None and row.get(f) != "" for f in FUNCTIONAL_UNIT_REQUIRED_FIELDS)


def run_task_manager_core_orchestration_implementation_planning_v1(
    *,
    orchestration_skeleton_consolidation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(orchestration_skeleton_consolidation_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    consolidation_summary = _read_json(upstream / "summary.json")
    consolidation_verifier = _read_json(upstream / "verifier_report.json")
    consolidation_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_orchestration_skeleton_consolidation_go = (
        consolidation_summary.get("final_decision") == ORCHESTRATION_CONSOLIDATION_FINAL_GO
        and consolidation_summary.get("recommended_next_phase") == ORCHESTRATION_CONSOLIDATION_NEXT_PHASE
        and consolidation_summary.get("selected_next_route") == UPSTREAM_CONSOLIDATION_SELECTED_ROUTE
        and consolidation_verifier.get("verifier") == "GO"
        and int(consolidation_verifier.get("passed_checks", 0)) >= 320
        and consolidation_summary.get("orchestration_skeleton_consolidation_pass") is True
        and consolidation_summary.get("orchestration_skeleton_not_runtime") is True
        and consolidation_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_orchestration_skeleton_consolidation_go:
        issues.append("orchestration_consolidation_not_go")

    absence = {key: consolidation_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = consolidation_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(consolidation_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_orchestration_skeleton_consolidation_go
        and consolidation_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    owner_approval_request_chain_not_reopened = consolidation_summary.get("owner_approval_request_chain_not_reopened") is True
    units = [dict(u) for u in ORCHESTRATION_FUNCTIONAL_UNITS]
    structures = [dict(s) for s in DATA_STRUCTURE_PLAN]
    gap_rows = [dict(g) for g in IMPLEMENTATION_GAPS]
    future_runtime_debt_not_current_blocker = all(not g.get("blocker_now") for g in gap_rows if g.get("status") == "future_runtime_debt")
    future_design_not_current_blocker = all(not g.get("blocker_now") for g in gap_rows if g.get("status") == "future_design")

    implementation_planning_scope_complete = prior_orchestration_skeleton_consolidation_go
    orchestration_functional_units_complete = len(units) >= 12 and all(_unit_complete(u) for u in units)
    orchestration_data_structure_plan_complete = len(structures) >= 10
    static_validator_plan_complete = len(STATIC_VALIDATORS) >= 10
    implementation_file_plan_complete = len(IMPLEMENTATION_FILES) >= 5
    implementation_files_split_by_responsibility = len(set(f["responsibility"] for f in IMPLEMENTATION_FILES)) >= 5
    no_monolithic_skeleton_planned = all("skeleton" in f["path"] or "types" in f["path"] or "validators" in f["path"] or "builders" in f["path"] or "contracts" in f["path"] for f in IMPLEMENTATION_FILES)
    implementation_dependency_plan_complete = len(ALLOWED_DEPENDENCIES) >= 6 and len(FORBIDDEN_DEPENDENCIES) >= 5
    non_execution_implementation_guard_plan_complete = len(NON_EXECUTION_GUARDS) >= 9
    implementation_gap_register_complete = len(gap_rows) >= 8
    next_route_decision_complete = SELECTED_NEXT_ROUTE == "Task Manager Core Orchestration Skeleton Controlled Implementation"
    do_not_misclassify_rules_complete = future_design_not_current_blocker and future_runtime_debt_not_current_blocker
    controlled_implementation_ready = (
        orchestration_functional_units_complete
        and orchestration_data_structure_plan_complete
        and static_validator_plan_complete
        and implementation_file_plan_complete
        and implementation_files_split_by_responsibility
        and no_monolithic_skeleton_planned
    )

    if not orchestration_functional_units_complete:
        issues.append("functional_units_incomplete")

    template_lineage = build_template_lineage(
        base_phase="Task-Manager-Core-Orchestration-Skeleton-Consolidation-v1-001",
        base_capability=ORCHESTRATION_IMPLEMENTATION_PLANNING_WHITELIST_FILES[0],
        base_runner=ORCHESTRATION_IMPLEMENTATION_PLANNING_WHITELIST_FILES[1],
        base_verifier=ORCHESTRATION_IMPLEMENTATION_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Task-Manager-Core-Orchestration-Implementation-Planning-v1-001",
        stage_term_overrides=ORCHESTRATION_IMPLEMENTATION_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=ORCHESTRATION_IMPLEMENTATION_PLANNING_STAGE_ADDITIONS,
        template_files=ORCHESTRATION_IMPLEMENTATION_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Task-Manager-Core-Orchestration-Skeleton-Consolidation-v1-001",
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
        previous_interruption_type=consolidation_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=consolidation_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=consolidation_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    planning_pass = (
        prior_orchestration_skeleton_consolidation_go
        and implementation_planning_scope_complete
        and orchestration_functional_units_complete
        and orchestration_data_structure_plan_complete
        and static_validator_plan_complete
        and implementation_file_plan_complete
        and implementation_dependency_plan_complete
        and non_execution_implementation_guard_plan_complete
        and implementation_gap_register_complete
        and next_route_decision_complete
        and do_not_misclassify_rules_complete
        and implementation_files_split_by_responsibility
        and no_monolithic_skeleton_planned
        and controlled_implementation_ready
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase = NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD

    if not prior_orchestration_skeleton_consolidation_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not controlled_implementation_ready:
        final_decision = FINAL_DECISION_PLANNING
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_orchestration_skeleton_consolidation_go": prior_orchestration_skeleton_consolidation_go,
        "implementation_planning_scope_complete": implementation_planning_scope_complete,
        "orchestration_functional_units_complete": orchestration_functional_units_complete,
        "orchestration_data_structure_plan_complete": orchestration_data_structure_plan_complete,
        "static_validator_plan_complete": static_validator_plan_complete,
        "implementation_file_plan_complete": implementation_file_plan_complete,
        "implementation_dependency_plan_complete": implementation_dependency_plan_complete,
        "non_execution_implementation_guard_plan_complete": non_execution_implementation_guard_plan_complete,
        "implementation_gap_register_complete": implementation_gap_register_complete,
        "next_route_decision_complete": next_route_decision_complete,
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "implementation_files_split_by_responsibility": implementation_files_split_by_responsibility,
        "no_monolithic_skeleton_planned": no_monolithic_skeleton_planned,
        "controlled_implementation_ready": controlled_implementation_ready,
        "runtime_dependency_absent": True,
        "whitebox_dependency_absent": True,
        "drive_brain_implementation_absent": True,
        "reflection_brain_implementation_absent": True,
        "midplatform_still_has_remaining_work": consolidation_summary.get("midplatform_still_has_remaining_work") is True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "future_runtime_debt_not_current_blocker": future_runtime_debt_not_current_blocker,
        "future_design_not_current_blocker": future_design_not_current_blocker,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "owner_approval_request_closed_module": "governance_ready_handoff",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": planning_pass,
        "orchestration_implementation_planning_pass": planning_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "candidate_promotion_executed": False,
        "route_execution_absent": True,
        "module_handoff_runtime_absent": True,
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
            list(consolidation_summary.get("chain_trace_nodes") or []) + ["task_manager_core_orchestration_implementation_planning"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    scope = {
        "scope_id": "implementation_planning_scope_v1",
        "implementation_planning_scope_complete": implementation_planning_scope_complete,
        "purpose": "Orchestration skeleton functional fill planning only",
        "not_runtime_orchestration": True,
        "not_real_routing": True,
        "not_record_grant_creation": True,
        "not_drive_brain_reflection": True,
        **meta,
    }
    functional_units = {
        "units_id": "orchestration_functional_units_v1",
        "orchestration_functional_units_complete": orchestration_functional_units_complete,
        "units": units,
        "unit_count": len(units),
        **meta,
    }
    data_structures = {
        "plan_id": "orchestration_data_structure_plan_v1",
        "orchestration_data_structure_plan_complete": orchestration_data_structure_plan_complete,
        "structures": structures,
        **meta,
    }
    validator_plan = {
        "plan_id": "static_validator_plan_v1",
        "static_validator_plan_complete": static_validator_plan_complete,
        "validators": list(STATIC_VALIDATORS),
        **meta,
    }
    file_plan = {
        "plan_id": "implementation_file_plan_v1",
        "implementation_file_plan_complete": implementation_file_plan_complete,
        "implementation_files_split_by_responsibility": implementation_files_split_by_responsibility,
        "no_monolithic_skeleton_planned": no_monolithic_skeleton_planned,
        "files": list(IMPLEMENTATION_FILES),
        "max_lines_per_file": 600,
        **meta,
    }
    dependency_plan = {
        "plan_id": "implementation_dependency_plan_v1",
        "implementation_dependency_plan_complete": implementation_dependency_plan_complete,
        "allowed_dependencies": list(ALLOWED_DEPENDENCIES),
        "forbidden_dependencies": list(FORBIDDEN_DEPENDENCIES),
        **meta,
    }
    guard_plan = {
        "plan_id": "non_execution_implementation_guard_plan_v1",
        "non_execution_implementation_guard_plan_complete": non_execution_implementation_guard_plan_complete,
        "guards": list(NON_EXECUTION_GUARDS),
        **meta,
    }
    gap_register = {
        "register_id": "implementation_gap_register_v1",
        "implementation_gap_register_complete": implementation_gap_register_complete,
        "gaps": gap_rows,
        **meta,
    }
    route_decision = {
        "decision_id": "next_route_decision_v1",
        "next_route_decision_complete": next_route_decision_complete,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": next_phase,
        "rationale": "Controlled skeleton implementation with split files (types/skeleton/validators/builders/contracts)",
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
            "implementation_planning_not_implementation",
            "controlled_implementation_not_runtime",
            "orchestration_skeleton_not_drive_brain",
            "builder_not_real_object_creator",
            "validator_not_runtime_executor",
            "route_candidate_not_route_execution",
            "handoff_candidate_not_handoff_execution",
            "future_brain_placeholder_not_implemented_brain_module",
            "future_runtime_debt_not_current_blocker",
            "owner_approval_request_chain_not_reopened",
        ],
        **meta,
    }
    report = {"report_id": "task_manager_core_orchestration_implementation_planning_report_v1", **go_values, "final_decision": final_decision, "recommended_next_phase": next_phase, **meta}
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "orchestration_implementation_planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join([
        "# Task Manager Core Orchestration Implementation Planning v1",
        "",
        f"Functional units: `{len(units)}` | Data structures: `{len(structures)}`",
        f"Implementation files: `{len(IMPLEMENTATION_FILES)}` | Validators: `{len(STATIC_VALIDATORS)}`",
        f"Selected next route: `{SELECTED_NEXT_ROUTE}`",
        f"Final decision: `{final_decision}`",
        f"Next phase: `{next_phase}`",
    ])
    return {
        "task_manager_core_orchestration_implementation_planning_report": report,
        "task_manager_core_orchestration_implementation_planning_report_md": markdown,
        "implementation_planning_scope": scope,
        "orchestration_functional_units": functional_units,
        "orchestration_data_structure_plan": data_structures,
        "static_validator_plan": validator_plan,
        "implementation_file_plan": file_plan,
        "implementation_dependency_plan": dependency_plan,
        "non_execution_implementation_guard_plan": guard_plan,
        "implementation_gap_register": gap_register,
        "next_route_decision": route_decision,
        "do_not_misclassify_rules": misclassify_rules,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
