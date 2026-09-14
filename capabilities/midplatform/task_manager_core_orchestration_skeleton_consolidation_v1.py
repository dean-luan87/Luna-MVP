# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Core Orchestration Skeleton Consolidation v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.candidate_lifecycle_unification_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_CANDIDATE_LIFECYCLE_PLANNING_ROOT,
    FINAL_DECISION_GO as CANDIDATE_LIFECYCLE_PLANNING_FINAL_GO,
)
from capabilities.midplatform.evidence_record_approval_permission_alignment_items_v1 import (
    SELECTED_NEXT_ROUTE as UPSTREAM_ALIGNMENT_SELECTED_ROUTE,
)
from capabilities.midplatform.evidence_record_approval_permission_alignment_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_ALIGNMENT_PLANNING_ROOT,
    FINAL_DECISION_GO as ALIGNMENT_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as ALIGNMENT_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.module_boundary_registry_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_BOUNDARY_REGISTRY_PLANNING_ROOT,
    FINAL_DECISION_GO as BOUNDARY_REGISTRY_PLANNING_FINAL_GO,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_items_v1 import (
    CORE_ORCHESTRATION_EXCLUSIONS,
    CORE_ORCHESTRATION_RESPONSIBILITIES,
    FLOW_SKELETON_SEMANTICS,
    FLOW_SKELETON_STEPS,
    FUTURE_BRAIN_INTERFACES,
    NEXT_ROUTE_A,
    NEXT_ROUTE_B,
    NEXT_ROUTE_C,
    NEXT_ROUTE_D,
    NEXT_ROUTE_E,
    NON_EXECUTION_FORBIDDEN,
    ORCHESTRATION_GAPS,
    ORCHESTRATION_INPUTS,
    ORCHESTRATION_OUTPUTS,
    RESPONSIBILITY_MATRIX,
    SELECTED_NEXT_ROUTE,
)
from capabilities.midplatform.task_manager_core_orchestration_skeleton_lineage_v1 import (
    ORCHESTRATION_SKELETON_CONSOLIDATION_STAGE_ADDITIONS,
    ORCHESTRATION_SKELETON_CONSOLIDATION_STAGE_TERM_OVERRIDES,
    ORCHESTRATION_SKELETON_CONSOLIDATION_WHITELIST_FILES,
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

PHASE_ID = "Phase-Midplatform-Task-Manager-Core-Orchestration-Skeleton-Consolidation-v1-001"
SCOPE = "midplatform_task_manager_core_orchestration_skeleton_consolidation_only"
SOURCE_CHAIN = "task_manager_core_orchestration_skeleton_consolidation_v1"
FINAL_DECISION_GO = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_SKELETON_CONSOLIDATION_READY_FOR_ORCHESTRATION_SKELETON_IMPLEMENTATION_PLANNING"
FINAL_DECISION_UPSTREAM = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_SKELETON_CONSOLIDATION_BLOCKED_BY_UPSTREAM_GAP"
FINAL_DECISION_CONSOLIDATION = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_SKELETON_CONSOLIDATION_BLOCKED_BY_SKELETON_GAP"
FINAL_DECISION_ABSENCE = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_SKELETON_CONSOLIDATION_BLOCKED_BY_ABSENCE_DRIFT"
FINAL_DECISION_RUNTIME = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_SKELETON_CONSOLIDATION_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
FINAL_DECISION_LINEAGE = "MIDPLATFORM_TASK_MANAGER_CORE_ORCHESTRATION_SKELETON_CONSOLIDATION_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
NEXT_PHASE_GO = NEXT_ROUTE_A
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Core-Orchestration-Skeleton-Consolidation-Issue-Review-v1-001"
DEFAULT_OUTPUT = "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/task_manager_core_orchestration_skeleton_consolidation_v1_smoke_v0"
GO_NO_GO_PACK = "docs/architecture/evaluation/LUNA_EVALUATION_TASK_MANAGER_CORE_ORCHESTRATION_SKELETON_CONSOLIDATION_V1_GO_NO_GO_PACK_V0.md"
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_core_orchestration_skeleton_consolidation_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_skeleton_items_v1.py",
    "capabilities/midplatform/task_manager_core_orchestration_skeleton_lineage_v1.py",
    "tools/evaluation/midplatform/run_task_manager_core_orchestration_skeleton_consolidation_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_core_orchestration_skeleton_consolidation_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_core_orchestration_skeleton_lineage_v1.py"
MIDPLATFORM_OVERALL_STATUS = "construction_consolidation"

CONSOLIDATION_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_core_orchestration_skeleton_consolidation_report_v1.json",
    "task_manager_core_orchestration_skeleton_consolidation_report_v1.md",
    "orchestration_consolidation_scope_v1.json",
    "core_orchestration_skeleton_role_definition_v1.json",
    "orchestration_input_output_contract_v1.json",
    "orchestration_flow_skeleton_v1.json",
    "orchestration_responsibility_matrix_v1.json",
    "orchestration_non_execution_boundary_v1.json",
    "orchestration_gap_register_v1.json",
    "future_brain_interface_placeholder_v1.json",
    "next_route_decision_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_boundary_registry_go",
    "prior_candidate_lifecycle_go",
    "prior_alignment_planning_go",
    "orchestration_consolidation_scope_complete",
    "core_orchestration_role_definition_complete",
    "orchestration_input_output_contract_complete",
    "orchestration_flow_skeleton_complete",
    "orchestration_responsibility_matrix_complete",
    "orchestration_non_execution_boundary_complete",
    "orchestration_gap_register_complete",
    "future_brain_interface_placeholder_complete",
    "next_route_decision_complete",
    "do_not_misclassify_rules_complete",
    "orchestration_skeleton_not_runtime",
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


def _meta(out: Path, roots: Dict[str, str]) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "orchestration_consolidation_only": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "integration_test_executed": False,
        "real_issuance_preauthorization_not_opened": True,
        "output_root": str(out),
        **roots,
    }


def run_task_manager_core_orchestration_skeleton_consolidation_v1(
    *,
    module_boundary_registry_planning_root: str,
    candidate_lifecycle_unification_planning_root: str,
    alignment_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    boundary_root = Path(module_boundary_registry_planning_root).expanduser().resolve()
    lifecycle_root = Path(candidate_lifecycle_unification_planning_root).expanduser().resolve()
    alignment_root = Path(alignment_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    roots_meta = {
        "module_boundary_registry_planning_root": str(boundary_root),
        "candidate_lifecycle_unification_planning_root": str(lifecycle_root),
        "alignment_planning_root": str(alignment_root),
    }
    meta = _meta(out, roots_meta)
    issues: List[str] = []

    boundary_summary = _read_json(boundary_root / "summary.json")
    boundary_verifier = _read_json(boundary_root / "verifier_report.json")
    lifecycle_summary = _read_json(lifecycle_root / "summary.json")
    lifecycle_verifier = _read_json(lifecycle_root / "verifier_report.json")
    alignment_summary = _read_json(alignment_root / "summary.json")
    alignment_verifier = _read_json(alignment_root / "verifier_report.json")
    alignment_file_size = _read_json(alignment_root / "file_size_governance_review_v1.json")

    prior_boundary_registry_go = (
        boundary_summary.get("final_decision") == BOUNDARY_REGISTRY_PLANNING_FINAL_GO
        and boundary_verifier.get("verifier") == "GO"
        and int(boundary_verifier.get("passed_checks", 0)) >= 300
        and boundary_summary.get("boundary_registry_planning_pass") is True
    )
    prior_candidate_lifecycle_go = (
        lifecycle_summary.get("final_decision") == CANDIDATE_LIFECYCLE_PLANNING_FINAL_GO
        and lifecycle_verifier.get("verifier") == "GO"
        and int(lifecycle_verifier.get("passed_checks", 0)) >= 320
        and lifecycle_summary.get("candidate_lifecycle_unification_planning_pass") is True
    )
    prior_alignment_planning_go = (
        alignment_summary.get("final_decision") == ALIGNMENT_PLANNING_FINAL_GO
        and alignment_summary.get("recommended_next_phase") == ALIGNMENT_PLANNING_NEXT_PHASE
        and alignment_summary.get("selected_next_route") == UPSTREAM_ALIGNMENT_SELECTED_ROUTE
        and alignment_verifier.get("verifier") == "GO"
        and int(alignment_verifier.get("passed_checks", 0)) >= 320
        and alignment_summary.get("alignment_planning_pass") is True
        and alignment_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_boundary_registry_go:
        issues.append("boundary_registry_not_go")
    if not prior_candidate_lifecycle_go:
        issues.append("lifecycle_not_go")
    if not prior_alignment_planning_go:
        issues.append("alignment_not_go")

    absence = {key: alignment_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = alignment_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(alignment_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_alignment_planning_go
        and alignment_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    owner_approval_request_chain_not_reopened = alignment_summary.get("owner_approval_request_chain_not_reopened") is True
    gap_rows = [dict(g) for g in ORCHESTRATION_GAPS]
    brain_interfaces = [dict(b) for b in FUTURE_BRAIN_INTERFACES]
    future_runtime_debt_not_current_blocker = all(not g.get("blocker_now") for g in gap_rows if g.get("status") == "future_runtime_debt")
    future_design_not_current_blocker = all(not g.get("blocker_now") for g in gap_rows if g.get("status") == "future_design") and all(
        not b.get("implemented_now") for b in brain_interfaces
    )

    orchestration_consolidation_scope_complete = prior_boundary_registry_go and prior_candidate_lifecycle_go and prior_alignment_planning_go
    core_orchestration_role_definition_complete = len(CORE_ORCHESTRATION_RESPONSIBILITIES) >= 7 and len(CORE_ORCHESTRATION_EXCLUSIONS) >= 8
    orchestration_input_output_contract_complete = len(ORCHESTRATION_INPUTS) >= 12 and len(ORCHESTRATION_OUTPUTS) >= 8
    orchestration_flow_skeleton_complete = len(FLOW_SKELETON_STEPS) >= 9 and len(FLOW_SKELETON_SEMANTICS) >= 4
    orchestration_responsibility_matrix_complete = len(RESPONSIBILITY_MATRIX) >= 9
    orchestration_non_execution_boundary_complete = len(NON_EXECUTION_FORBIDDEN) >= 10
    orchestration_gap_register_complete = len(gap_rows) >= 10
    future_brain_interface_placeholder_complete = len(brain_interfaces) >= 5
    next_route_decision_complete = SELECTED_NEXT_ROUTE == "Task Manager Core Orchestration Skeleton Implementation Planning"
    do_not_misclassify_rules_complete = future_design_not_current_blocker and future_runtime_debt_not_current_blocker

    template_lineage = build_template_lineage(
        base_phase="Evidence-Record-Approval-Permission-Alignment-Planning-v1-001",
        base_capability=ORCHESTRATION_SKELETON_CONSOLIDATION_WHITELIST_FILES[0],
        base_runner=ORCHESTRATION_SKELETON_CONSOLIDATION_WHITELIST_FILES[1],
        base_verifier=ORCHESTRATION_SKELETON_CONSOLIDATION_WHITELIST_FILES[2],
        base_go_no_go_pack=GO_NO_GO_PACK,
        stage_phase="Task-Manager-Core-Orchestration-Skeleton-Consolidation-v1-001",
        stage_term_overrides=ORCHESTRATION_SKELETON_CONSOLIDATION_STAGE_TERM_OVERRIDES,
        stage_additions=ORCHESTRATION_SKELETON_CONSOLIDATION_STAGE_ADDITIONS,
        template_files=ORCHESTRATION_SKELETON_CONSOLIDATION_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Evidence-Record-Approval-Permission-Alignment-Planning-v1-001",
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
        previous_interruption_type=alignment_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=alignment_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=alignment_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    consolidation_pass = (
        prior_boundary_registry_go
        and prior_candidate_lifecycle_go
        and prior_alignment_planning_go
        and orchestration_consolidation_scope_complete
        and core_orchestration_role_definition_complete
        and orchestration_input_output_contract_complete
        and orchestration_flow_skeleton_complete
        and orchestration_responsibility_matrix_complete
        and orchestration_non_execution_boundary_complete
        and orchestration_gap_register_complete
        and future_brain_interface_placeholder_complete
        and next_route_decision_complete
        and do_not_misclassify_rules_complete
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase = NEXT_PHASE_GO if consolidation_pass else NEXT_PHASE_HOLD

    if not (prior_boundary_registry_go and prior_candidate_lifecycle_go and prior_alignment_planning_go):
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not orchestration_flow_skeleton_complete:
        final_decision = FINAL_DECISION_CONSOLIDATION
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_boundary_registry_go": prior_boundary_registry_go,
        "prior_candidate_lifecycle_go": prior_candidate_lifecycle_go,
        "prior_alignment_planning_go": prior_alignment_planning_go,
        "orchestration_consolidation_scope_complete": orchestration_consolidation_scope_complete,
        "core_orchestration_role_definition_complete": core_orchestration_role_definition_complete,
        "orchestration_input_output_contract_complete": orchestration_input_output_contract_complete,
        "orchestration_flow_skeleton_complete": orchestration_flow_skeleton_complete,
        "orchestration_responsibility_matrix_complete": orchestration_responsibility_matrix_complete,
        "orchestration_non_execution_boundary_complete": orchestration_non_execution_boundary_complete,
        "orchestration_gap_register_complete": orchestration_gap_register_complete,
        "future_brain_interface_placeholder_complete": future_brain_interface_placeholder_complete,
        "next_route_decision_complete": next_route_decision_complete,
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "orchestration_skeleton_not_runtime": True,
        "orchestration_plan_candidate_not_executed_plan": True,
        "route_candidate_not_route_execution": True,
        "lifecycle_transition_request_candidate_not_promotion_executed": True,
        "module_handoff_candidate_not_runtime_handoff": True,
        "drive_brain_placeholder_not_implementation": True,
        "reflection_brain_placeholder_not_implementation": True,
        "future_design_not_current_blocker": future_design_not_current_blocker,
        "future_runtime_debt_not_current_blocker": future_runtime_debt_not_current_blocker,
        "midplatform_still_has_remaining_work": alignment_summary.get("midplatform_still_has_remaining_work") is True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "midplatform_overall_status": MIDPLATFORM_OVERALL_STATUS,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "owner_approval_request_closed_module": "governance_ready_handoff",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": consolidation_pass,
        "orchestration_skeleton_consolidation_pass": consolidation_pass,
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
            list(alignment_summary.get("chain_trace_nodes") or []) + ["task_manager_core_orchestration_skeleton_consolidation"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    scope = {
        "scope_id": "orchestration_consolidation_scope_v1",
        "orchestration_consolidation_scope_complete": orchestration_consolidation_scope_complete,
        "purpose": "Task Manager core orchestration skeleton consolidation only",
        "not_runtime_orchestration": True,
        "not_task_center_drive_brain": True,
        "not_record_grant_creation": True,
        "not_reopen_owner_approval_request": True,
        **meta,
    }
    role_def = {
        "definition_id": "core_orchestration_skeleton_role_definition_v1",
        "core_orchestration_role_definition_complete": core_orchestration_role_definition_complete,
        "responsibilities": list(CORE_ORCHESTRATION_RESPONSIBILITIES),
        "exclusions": list(CORE_ORCHESTRATION_EXCLUSIONS),
        **meta,
    }
    io_contract = {
        "contract_id": "orchestration_input_output_contract_v1",
        "orchestration_input_output_contract_complete": orchestration_input_output_contract_complete,
        "inputs": list(ORCHESTRATION_INPUTS),
        "outputs": list(ORCHESTRATION_OUTPUTS),
        "all_outputs_candidate_layer": True,
        **meta,
    }
    flow_skeleton = {
        "skeleton_id": "orchestration_flow_skeleton_v1",
        "orchestration_flow_skeleton_complete": orchestration_flow_skeleton_complete,
        "steps": list(FLOW_SKELETON_STEPS),
        "semantics": list(FLOW_SKELETON_SEMANTICS),
        **meta,
    }
    responsibility = {
        "matrix_id": "orchestration_responsibility_matrix_v1",
        "orchestration_responsibility_matrix_complete": orchestration_responsibility_matrix_complete,
        "rows": list(RESPONSIBILITY_MATRIX),
        **meta,
    }
    non_exec = {
        "boundary_id": "orchestration_non_execution_boundary_v1",
        "orchestration_non_execution_boundary_complete": orchestration_non_execution_boundary_complete,
        "forbidden_actions": list(NON_EXECUTION_FORBIDDEN),
        **meta,
    }
    gap_register = {
        "register_id": "orchestration_gap_register_v1",
        "orchestration_gap_register_complete": orchestration_gap_register_complete,
        "gaps": gap_rows,
        **meta,
    }
    brain_placeholder = {
        "placeholder_id": "future_brain_interface_placeholder_v1",
        "future_brain_interface_placeholder_complete": future_brain_interface_placeholder_complete,
        "interfaces": brain_interfaces,
        "future_design_not_current_blocker": future_design_not_current_blocker,
        **meta,
    }
    route_decision = {
        "decision_id": "next_route_decision_v1",
        "next_route_decision_complete": next_route_decision_complete,
        "selected_next_route": SELECTED_NEXT_ROUTE,
        "selected_route_id": "A",
        "recommended_next_phase": next_phase,
        "rationale": "Orchestration skeleton consolidation complete; implementation planning is next",
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
            "orchestration_skeleton_consolidation_not_runtime_orchestration",
            "orchestration_plan_candidate_not_executed_plan",
            "route_candidate_not_route_execution",
            "lifecycle_transition_request_candidate_not_promotion_executed",
            "module_handoff_candidate_not_runtime_handoff",
            "drive_brain_placeholder_not_intelligence_implementation",
            "reflection_brain_placeholder_not_reflection_module_implementation",
            "future_runtime_debt_not_current_blocker",
            "owner_approval_request_chain_not_reopened",
        ],
        **meta,
    }
    report = {
        "report_id": "task_manager_core_orchestration_skeleton_consolidation_report_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "orchestration_skeleton_consolidation_pass": consolidation_pass,
        "blocker_count": len(issues),
        "issues": issues,
        **go_values,
        **core_fields,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    markdown = "\n".join([
        "# Task Manager Core Orchestration Skeleton Consolidation v1",
        "",
        f"Inputs: `{len(ORCHESTRATION_INPUTS)}` | Outputs: `{len(ORCHESTRATION_OUTPUTS)}`",
        f"Flow steps: `{len(FLOW_SKELETON_STEPS)}` | Future brain interfaces: `{len(brain_interfaces)}`",
        f"Selected next route: `{SELECTED_NEXT_ROUTE}`",
        f"Final decision: `{final_decision}`",
        f"Next phase: `{next_phase}`",
    ])
    return {
        "task_manager_core_orchestration_skeleton_consolidation_report": report,
        "task_manager_core_orchestration_skeleton_consolidation_report_md": markdown,
        "orchestration_consolidation_scope": scope,
        "core_orchestration_skeleton_role_definition": role_def,
        "orchestration_input_output_contract": io_contract,
        "orchestration_flow_skeleton": flow_skeleton,
        "orchestration_responsibility_matrix": responsibility,
        "orchestration_non_execution_boundary": non_exec,
        "orchestration_gap_register": gap_register,
        "future_brain_interface_placeholder": brain_placeholder,
        "next_route_decision": route_decision,
        "do_not_misclassify_rules": misclassify_rules,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
