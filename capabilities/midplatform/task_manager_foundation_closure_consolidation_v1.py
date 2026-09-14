# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Closure Consolidation v1.

Consolidate Task Manager foundation layer assets into a stable base package.
NOT final midplatform completion. No runtime / real execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
    RESULT_FIRST_MODULE_ENGINEERING_RULE_REF,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_broader_midplatform_closure_roadmap_v1 import (
    DEFAULT_OUTPUT as DEFAULT_BROADER_ROADMAP_ROOT,
    FINAL_DECISION_GO as BROADER_ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as BROADER_ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE,
    STATUS_INVENTORY,
)
from capabilities.midplatform.task_manager_foundation_closure_consolidation_lineage_v1 import (
    FOUNDATION_CLOSURE_CONSOLIDATION_STAGE_ADDITIONS,
    FOUNDATION_CLOSURE_CONSOLIDATION_STAGE_TERM_OVERRIDES,
    FOUNDATION_CLOSURE_CONSOLIDATION_WHITELIST_FILES,
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

PHASE_ID = "Phase-Midplatform-Task-Manager-Foundation-Closure-Consolidation-v1-001"
SCOPE = "midplatform_task_manager_foundation_closure_consolidation_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_closure_consolidation_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_CLOSURE_CONSOLIDATION_READY_FOR_BROADER_MIDPLATFORM_REMAINING_WORK_ROADMAP"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_CLOSURE_CONSOLIDATION_BLOCKED_BY_BROADER_ROADMAP_GAP"
)
FINAL_DECISION_CONSOLIDATION = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_CLOSURE_CONSOLIDATION_BLOCKED_BY_CONSOLIDATION_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_CLOSURE_CONSOLIDATION_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_CLOSURE_CONSOLIDATION_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_CLOSURE_CONSOLIDATION_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Broader-Midplatform-Remaining-Work-Roadmap-v1-001"
NEXT_PHASE_B = "Phase-Midplatform-Task-Manager-Module-Integration-Planning-v1-001"
NEXT_PHASE_C = "Phase-Midplatform-Task-Manager-Governance-Debt-Consolidation-v1-001"
NEXT_PHASE_D = "Phase-Midplatform-Task-Manager-Integration-Test-Planning-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Closure-Consolidation-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_foundation_closure_consolidation_v1_smoke_v0"
)
CONSOLIDATION_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_TASK_MANAGER_FOUNDATION_CLOSURE_CONSOLIDATION_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_closure_consolidation_v1.py",
    "capabilities/midplatform/task_manager_foundation_closure_consolidation_lineage_v1.py",
    "tools/evaluation/midplatform/run_task_manager_foundation_closure_consolidation_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_foundation_closure_consolidation_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = (
    "capabilities/midplatform/task_manager_foundation_closure_consolidation_lineage_v1.py"
)

CONSOLIDATION_ARTIFACTS: Tuple[str, ...] = (
    "foundation_consolidation_report_v1.json",
    "foundation_consolidation_report_v1.md",
    "foundation_consolidation_scope_v1.json",
    "foundation_asset_inventory_v1.json",
    "foundation_consolidation_matrix_v1.json",
    "foundation_boundary_statement_v1.json",
    "remaining_work_register_v1.json",
    "next_mainline_route_v1.json",
    "do_not_misclassify_rules_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_broader_midplatform_roadmap_go",
    "foundation_consolidation_scope_complete",
    "foundation_asset_inventory_complete",
    "foundation_consolidation_matrix_complete",
    "foundation_boundary_statement_complete",
    "remaining_work_register_complete",
    "next_mainline_route_complete",
    "do_not_misclassify_rules_complete",
    "foundation_consolidation_not_final_midplatform_completion",
    "midplatform_still_has_remaining_work",
    "future_runtime_debt_not_current_blocker",
    "owner_approval_request_chain_not_reopened",
    "real_execution_not_authorized",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)

FOUNDATION_ASSET_IDS: Tuple[str, ...] = (
    "task_manager_skeleton_foundation_handoff",
    "protocol_registry_input_output_traceability",
    "governance_constraints",
    "file_size_governance",
    "module_first_result_first_rules",
    "owner_approval_request_closed_module",
    "broader_midplatform_closure_roadmap",
)

REMAINING_WORK_ITEMS: Tuple[Dict[str, str], ...] = (
    {"work_id": "broader_module_completion", "category": "construction"},
    {"work_id": "module_integration_planning", "category": "planning"},
    {"work_id": "integration_test_planning", "category": "deferred_test"},
    {"work_id": "governance_debt_consolidation", "category": "optional_quality"},
    {"work_id": "future_runtime_debt_registry", "category": "future_runtime_debt"},
    {"work_id": "runtime_adapter_implementation", "category": "future_runtime_debt"},
    {"work_id": "whitebox_runtime_integration", "category": "future_runtime_debt"},
    {"work_id": "real_execution_preauthorization_gate", "category": "required_before_runtime"},
    {"work_id": "task_center_drive_brain_intelligence", "category": "future_design"},
    {"work_id": "time_bound_task_elasticity_tradeoff", "category": "future_design"},
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
        "foundation_closure_consolidation_only": True,
        "foundation_consolidation_not_final_midplatform_completion": True,
        "no_fragmentary_phase_expansion": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "integration_test_executed": False,
        "output_root": str(out),
        "broader_midplatform_closure_roadmap_root": str(upstream),
    }


def _status_for(asset_id: str, inventory: Dict[str, Dict[str, str]]) -> str:
    if asset_id == "broader_midplatform_closure_roadmap":
        return "consolidated"
    return inventory.get(asset_id, {}).get("status", "active")


def run_task_manager_foundation_closure_consolidation_v1(
    *,
    broader_midplatform_closure_roadmap_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(broader_midplatform_closure_roadmap_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    roadmap_summary = _read_json(upstream / "summary.json")
    roadmap_verifier = _read_json(upstream / "verifier_report.json")
    roadmap_inventory = _read_json(upstream / "broader_midplatform_status_inventory_v1.json")
    roadmap_gap = _read_json(upstream / "midplatform_closure_gap_matrix_v1.json")
    roadmap_file_size = _read_json(upstream / "file_size_governance_review_v1.json")

    prior_broader_midplatform_roadmap_go = (
        roadmap_summary.get("final_decision") == BROADER_ROADMAP_FINAL_GO
        and roadmap_summary.get("recommended_next_phase") == BROADER_ROADMAP_NEXT_PHASE
        and roadmap_verifier.get("verifier") == "GO"
        and int(roadmap_verifier.get("passed_checks", 0)) >= 260
        and roadmap_summary.get("broader_midplatform_closure_roadmap_pass") is True
        and roadmap_summary.get("selected_route") == SELECTED_ROUTE
        and roadmap_summary.get("owner_approval_request_chain_not_extended") is True
        and roadmap_summary.get("no_fragmentary_phase_expansion") is True
        and roadmap_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_broader_midplatform_roadmap_go:
        issues.append("broader_roadmap_not_go")

    inventory_map = {i.get("item_id"): i for i in roadmap_inventory.get("items") or list(STATUS_INVENTORY)}
    absence = {key: roadmap_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = roadmap_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(roadmap_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_broader_midplatform_roadmap_go
        and roadmap_summary.get("non_execution_boundary_ok") is True
        and roadmap_summary.get("real_execution_not_authorized") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    future_runtime_debt_not_current_blocker = roadmap_gap.get("future_runtime_debt_not_current_blocker") is True
    owner_approval_request_chain_not_reopened = (
        prior_broader_midplatform_roadmap_go
        and roadmap_summary.get("owner_approval_request_chain_not_extended") is True
        and inventory_map.get("owner_approval_request_closed_module", {}).get("status") == "governance_ready_handoff"
    )
    if not owner_approval_request_chain_not_reopened:
        issues.append("owner_chain_reopen_risk")

    foundation_consolidation_scope_complete = prior_broader_midplatform_roadmap_go
    foundation_asset_inventory_complete = prior_broader_midplatform_roadmap_go and len(FOUNDATION_ASSET_IDS) >= 7

    matrix_rows: List[Dict[str, Any]] = []
    for asset_id in FOUNDATION_ASSET_IDS:
        current = _status_for(asset_id, inventory_map)
        consolidated = current in ("active", "governance_ready_handoff", "consolidated", "in_progress")
        blocker = asset_id == "task_manager_skeleton_foundation_handoff" and current == "in_progress"
        matrix_rows.append(
            {
                "asset_id": asset_id,
                "current_status": current,
                "consolidation_status": "consolidated" if consolidated else "pending",
                "dependency_refs": ["migration_governance_development_constraints_v1"],
                "future_dependency": asset_id in ("runtime_adapter_implementation", "whitebox_runtime_integration"),
                "runtime_required_now": False,
                "test_required_now": False,
                "test_deferred": True,
                "blocker_status": "current_foundation_blocker" if blocker else "not_blocker",
            }
        )
    foundation_consolidation_matrix_complete = (
        foundation_asset_inventory_complete
        and len(matrix_rows) == len(FOUNDATION_ASSET_IDS)
        and all(r.get("runtime_required_now") is False for r in matrix_rows)
    )

    foundation_boundary_statement_complete = prior_broader_midplatform_roadmap_go
    remaining_work_register_complete = prior_broader_midplatform_roadmap_go and len(REMAINING_WORK_ITEMS) >= 8
    midplatform_still_has_remaining_work = remaining_work_register_complete
    foundation_consolidation_not_final_midplatform_completion = True

    next_mainline_route_complete = (
        foundation_consolidation_matrix_complete and foundation_consolidation_not_final_midplatform_completion
    )
    do_not_misclassify_rules_complete = (
        future_runtime_debt_not_current_blocker and foundation_consolidation_not_final_midplatform_completion
    )

    template_lineage = build_template_lineage(
        base_phase="Task-Manager-Broader-Midplatform-Closure-Roadmap-v1-001",
        base_capability=FOUNDATION_CLOSURE_CONSOLIDATION_WHITELIST_FILES[0],
        base_runner=FOUNDATION_CLOSURE_CONSOLIDATION_WHITELIST_FILES[1],
        base_verifier=FOUNDATION_CLOSURE_CONSOLIDATION_WHITELIST_FILES[2],
        base_go_no_go_pack=CONSOLIDATION_GO_NO_GO_PACK,
        stage_phase="Task-Manager-Foundation-Closure-Consolidation-v1-001",
        stage_term_overrides=FOUNDATION_CLOSURE_CONSOLIDATION_STAGE_TERM_OVERRIDES,
        stage_additions=FOUNDATION_CLOSURE_CONSOLIDATION_STAGE_ADDITIONS,
        template_files=FOUNDATION_CLOSURE_CONSOLIDATION_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Task-Manager-Broader-Midplatform-Closure-Roadmap-v1-001",
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

    consolidation_pass = (
        prior_broader_midplatform_roadmap_go
        and foundation_consolidation_scope_complete
        and foundation_asset_inventory_complete
        and foundation_consolidation_matrix_complete
        and foundation_boundary_statement_complete
        and remaining_work_register_complete
        and next_mainline_route_complete
        and do_not_misclassify_rules_complete
        and foundation_consolidation_not_final_midplatform_completion
        and midplatform_still_has_remaining_work
        and future_runtime_debt_not_current_blocker
        and owner_approval_request_chain_not_reopened
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase_readiness_ok = consolidation_pass
    next_phase = NEXT_PHASE_GO if consolidation_pass else NEXT_PHASE_HOLD

    if not prior_broader_midplatform_roadmap_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not foundation_consolidation_matrix_complete:
        final_decision = FINAL_DECISION_CONSOLIDATION
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_broader_midplatform_roadmap_go": prior_broader_midplatform_roadmap_go,
        "foundation_consolidation_scope_complete": foundation_consolidation_scope_complete,
        "foundation_asset_inventory_complete": foundation_asset_inventory_complete,
        "foundation_consolidation_matrix_complete": foundation_consolidation_matrix_complete,
        "foundation_boundary_statement_complete": foundation_boundary_statement_complete,
        "remaining_work_register_complete": remaining_work_register_complete,
        "next_mainline_route_complete": next_mainline_route_complete,
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "foundation_consolidation_not_final_midplatform_completion": foundation_consolidation_not_final_midplatform_completion,
        "midplatform_still_has_remaining_work": midplatform_still_has_remaining_work,
        "future_runtime_debt_not_current_blocker": future_runtime_debt_not_current_blocker,
        "owner_approval_request_chain_not_reopened": owner_approval_request_chain_not_reopened,
        "real_execution_not_authorized": roadmap_summary.get("real_execution_not_authorized") is True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "foundation_consolidation_pass": consolidation_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "integration_test_executed": False,
        "selected_route": SELECTED_ROUTE,
        "midplatform_construction_phase": "foundation_layer_consolidated",
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
            + ["task_manager_foundation_closure_consolidation"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    consolidation_scope = {
        "scope_id": "foundation_consolidation_scope_v1",
        "foundation_consolidation_scope_complete": foundation_consolidation_scope_complete,
        "layer": "task_manager_foundation_only",
        "not_entire_midplatform_completion": True,
        "not_runtime_implementation": True,
        "not_real_execution": True,
        "not_integration_test_execution": True,
        "purpose": "Merge foundation assets into stable base package for continued construction",
        **meta,
    }
    asset_inventory = {
        "inventory_id": "foundation_asset_inventory_v1",
        "foundation_asset_inventory_complete": foundation_asset_inventory_complete,
        "assets": [
            {"asset_id": aid, "current_status": _status_for(aid, inventory_map)} for aid in FOUNDATION_ASSET_IDS
        ],
        **meta,
    }
    consolidation_matrix = {
        "matrix_id": "foundation_consolidation_matrix_v1",
        "foundation_consolidation_matrix_complete": foundation_consolidation_matrix_complete,
        "rows": matrix_rows,
        **meta,
    }
    boundary_statement = {
        "statement_id": "foundation_boundary_statement_v1",
        "foundation_boundary_statement_complete": foundation_boundary_statement_complete,
        "statements": [
            "foundation consolidation is not final midplatform closure",
            "foundation consolidation is not runtime implementation",
            "foundation consolidation is not real issuance authorization",
            "foundation consolidation is not integration test execution",
            "foundation consolidation is base structure readiness package",
        ],
        "midplatform_overall_status": "construction_consolidation",
        **meta,
    }
    remaining_work = {
        "register_id": "remaining_work_register_v1",
        "remaining_work_register_complete": remaining_work_register_complete,
        "midplatform_still_has_remaining_work": midplatform_still_has_remaining_work,
        "items": list(REMAINING_WORK_ITEMS),
        **meta,
    }
    next_route = {
        "route_id": "next_mainline_route_v1",
        "next_mainline_route_complete": next_mainline_route_complete,
        "recommended_next_phase": next_phase,
        "selected_route": NEXT_PHASE_GO,
        "alternate_routes": [NEXT_PHASE_B, NEXT_PHASE_C, NEXT_PHASE_D],
        "do_not_declare_midplatform_completed": True,
        **meta,
    }
    misclassify_rules = {
        "rules_id": "do_not_misclassify_rules_v1",
        "do_not_misclassify_rules_complete": do_not_misclassify_rules_complete,
        "rules": [
            "future_runtime_debt_not_current_foundation_blocker",
            "remaining_work_not_closure_failure",
            "do_not_reopen_owner_approval_request_fragmentary_phases",
            "foundation_consolidated_not_midplatform_completed",
            "do_not_reopen_l1_protocol_review",
            "do_not_rerun_shared_protocol_validation",
        ],
        **meta,
    }
    consolidation_report = {
        "report_id": "foundation_consolidation_report_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "foundation_consolidation_pass": consolidation_pass,
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
            "# Foundation Consolidation Report v1",
            "",
            "Task Manager foundation layer consolidation only — NOT entire midplatform completion.",
            "",
            f"Layer: `task_manager_foundation_only`",
            f"Midplatform still has remaining work: `{midplatform_still_has_remaining_work}`",
            f"Foundation consolidated ≠ midplatform completed",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "foundation_consolidation_report": consolidation_report,
        "foundation_consolidation_report_md": markdown,
        "foundation_consolidation_scope": consolidation_scope,
        "foundation_asset_inventory": asset_inventory,
        "foundation_consolidation_matrix": consolidation_matrix,
        "foundation_boundary_statement": boundary_statement,
        "remaining_work_register": remaining_work,
        "next_mainline_route": next_route,
        "do_not_misclassify_rules": misclassify_rules,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
