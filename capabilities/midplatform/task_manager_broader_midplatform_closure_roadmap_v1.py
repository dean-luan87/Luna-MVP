# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Broader Midplatform Closure Roadmap v1.

Inventory midplatform mainline status and decide closure route. No sub-chain extension.
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
from capabilities.midplatform.task_manager_broader_midplatform_closure_lineage_v1 import (
    BROADER_MIDPLATFORM_CLOSURE_ROADMAP_STAGE_ADDITIONS,
    BROADER_MIDPLATFORM_CLOSURE_ROADMAP_STAGE_TERM_OVERRIDES,
    BROADER_MIDPLATFORM_CLOSURE_ROADMAP_WHITELIST_FILES,
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
from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_v1 import (
    DEFAULT_OUTPUT as DEFAULT_MODULE_HANDOFF_ROOT,
    FINAL_DECISION_GO as MODULE_HANDOFF_FINAL_GO,
    MIDPLATFORM_MAINLINE_ITEMS,
    NEXT_PHASE_GO as MODULE_HANDOFF_NEXT_PHASE,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Broader-Midplatform-Closure-Roadmap-v1-001"
SCOPE = "midplatform_task_manager_broader_midplatform_closure_roadmap_only"
SOURCE_CHAIN = "midplatform_task_manager_broader_midplatform_closure_roadmap_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_CLOSURE_ROADMAP_READY_FOR_FOUNDATION_CLOSURE_CONSOLIDATION"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_CLOSURE_ROADMAP_BLOCKED_BY_MODULE_HANDOFF_GAP"
)
FINAL_DECISION_ROADMAP = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_CLOSURE_ROADMAP_BLOCKED_BY_ROADMAP_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_CLOSURE_ROADMAP_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_CLOSURE_ROADMAP_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_BROADER_MIDPLATFORM_CLOSURE_ROADMAP_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
SELECTED_ROUTE = "Midplatform Task Manager Foundation Closure Consolidation"
ROUTE_A = "Midplatform Task Manager Foundation Closure Consolidation"
ROUTE_B = "Midplatform Integration Test Planning"
ROUTE_C = "Governance Debt Consolidation"
ROUTE_D = "Future Runtime Debt Registry"
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Foundation-Closure-Consolidation-v1-001"
NEXT_PHASE_ALT = "Phase-Midplatform-Task-Manager-Closure-Gap-Consolidation-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Task-Manager-Broader-Midplatform-Closure-Roadmap-Issue-Review-v1-001"
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_broader_midplatform_closure_roadmap_v1_smoke_v0"
)
ROADMAP_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_TASK_MANAGER_BROADER_MIDPLATFORM_CLOSURE_ROADMAP_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_broader_midplatform_closure_roadmap_v1.py",
    "capabilities/midplatform/task_manager_broader_midplatform_closure_lineage_v1.py",
    "tools/evaluation/midplatform/run_task_manager_broader_midplatform_closure_roadmap_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_broader_midplatform_closure_roadmap_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_broader_midplatform_closure_lineage_v1.py"

ROADMAP_ARTIFACTS: Tuple[str, ...] = (
    "broader_midplatform_closure_roadmap_v1.json",
    "broader_midplatform_closure_roadmap_v1.md",
    "broader_midplatform_status_inventory_v1.json",
    "midplatform_closure_gap_matrix_v1.json",
    "module_integration_map_v1.json",
    "mainline_closure_route_decision_v1.json",
    "future_test_strategy_consolidation_v1.json",
    "do_not_reopen_rules_v1.json",
    "next_phase_recommendation_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_owner_approval_request_module_handoff_go",
    "broader_midplatform_status_inventory_complete",
    "midplatform_closure_gap_matrix_complete",
    "module_integration_map_complete",
    "mainline_closure_route_decision_complete",
    "future_test_strategy_consolidation_complete",
    "do_not_reopen_rules_complete",
    "next_phase_recommendation_complete",
    "owner_approval_request_chain_not_extended",
    "future_runtime_debt_not_current_blocker",
    "real_execution_not_authorized",
    "non_execution_boundary_ok",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)

STATUS_INVENTORY: Tuple[Dict[str, str], ...] = (
    {"item_id": "task_manager_skeleton_foundation_handoff", "status": "in_progress"},
    {"item_id": "protocol_registry_input_output_traceability", "status": "active"},
    {"item_id": "governance_constraints", "status": "active"},
    {"item_id": "file_size_governance", "status": "active"},
    {"item_id": "module_first_result_first_rules", "status": "active"},
    {"item_id": "owner_approval_request_closed_module", "status": "governance_ready_handoff"},
    {"item_id": "runtime_adapter_implementation", "status": "future_runtime_debt"},
    {"item_id": "whitebox_runtime_integration", "status": "future_runtime_debt"},
    {"item_id": "real_request_issuance_preauthorization", "status": "deferred"},
)

GAP_ROWS: Tuple[Dict[str, str], ...] = (
    {
        "gap_id": "foundation_closure_consolidation",
        "bucket": "required_before_midplatform_closure",
        "blocking_now": "true",
    },
    {
        "gap_id": "integration_test_planning",
        "bucket": "deferred_test",
        "blocking_now": "false",
    },
    {
        "gap_id": "runtime_adapter_implementation",
        "bucket": "future_runtime_debt",
        "blocking_now": "false",
    },
    {
        "gap_id": "whitebox_runtime_integration",
        "bucket": "future_runtime_debt",
        "blocking_now": "false",
    },
    {
        "gap_id": "real_request_issuance_preauthorization",
        "bucket": "required_before_runtime",
        "blocking_now": "false",
    },
    {
        "gap_id": "governance_debt_consolidation",
        "bucket": "optional_quality_improvement",
        "blocking_now": "false",
    },
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
        "broader_midplatform_closure_roadmap_only": True,
        "no_fragmentary_phase_expansion": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "module_handoff_root": str(upstream),
    }


def run_task_manager_broader_midplatform_closure_roadmap_v1(
    *,
    module_handoff_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(module_handoff_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    handoff_summary = _read_json(upstream / "summary.json")
    handoff_verifier = _read_json(upstream / "verifier_report.json")
    handoff_mainline = _read_json(upstream / "midplatform_mainline_return_plan_v1.json")
    handoff_file_size = _read_json(upstream / "file_size_governance_review_v1.json")
    handoff_test = _read_json(upstream / "future_test_strategy_v1.json")

    prior_owner_approval_request_module_handoff_go = (
        handoff_summary.get("final_decision") == MODULE_HANDOFF_FINAL_GO
        and handoff_summary.get("recommended_next_phase") == MODULE_HANDOFF_NEXT_PHASE
        and handoff_verifier.get("verifier") == "GO"
        and int(handoff_verifier.get("passed_checks", 0)) >= 240
        and handoff_summary.get("module_handoff_pass") is True
        and handoff_summary.get("owner_approval_request_chain_not_extended") is True
        and handoff_mainline.get("do_not_open_real_issuance_preauth_unless_mainline_requires") is True
        and handoff_summary.get("no_fragmentary_phase_expansion") is True
        and handoff_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_owner_approval_request_module_handoff_go:
        issues.append("module_handoff_not_go")

    owner_item = next(
        (i for i in handoff_mainline.get("mainline_items") or [] if i.get("item_id") == "owner_approval_request_closed_module"),
        {},
    )
    owner_approval_request_chain_not_extended = (
        prior_owner_approval_request_module_handoff_go
        and handoff_summary.get("owner_approval_request_chain_not_extended") is True
        and handoff_summary.get("do_not_extend_fragmentary_phases") is True
        and owner_item.get("status") == "governance_ready_handoff"
    )
    if not owner_approval_request_chain_not_extended:
        issues.append("owner_chain_extension_risk")

    absence = {key: handoff_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = handoff_summary.get("record_creation_absent") is True
    runtime_forbidden_violation = any(handoff_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_owner_approval_request_module_handoff_go
        and handoff_summary.get("non_execution_boundary_ok") is True
        and handoff_summary.get("real_execution_not_authorized") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    inventory_items = list(STATUS_INVENTORY)
    broader_midplatform_status_inventory_complete = (
        prior_owner_approval_request_module_handoff_go and len(inventory_items) >= 6
    )
    gap_rows = [{**row, "blocking_now": row["blocking_now"] == "true"} for row in GAP_ROWS]
    future_runtime_debt_not_current_blocker = all(
        not row.get("blocking_now") for row in gap_rows if row.get("bucket") == "future_runtime_debt"
    )
    midplatform_closure_gap_matrix_complete = (
        broader_midplatform_status_inventory_complete
        and len(gap_rows) >= 6
        and future_runtime_debt_not_current_blocker
    )

    integration_modules = [
        {
            "module_id": item["item_id"],
            "status": item["status"],
            "triggers_real_issuance": False,
            "integration_role": "mainline_asset",
        }
        for item in inventory_items
        if item["status"] != "future_runtime_debt"
    ]
    integration_modules.append(
        {
            "module_id": "owner_approval_request_closed_module",
            "status": "governance_ready_handoff",
            "triggers_real_issuance": False,
            "integration_role": "governance_ready_submodule_only",
        }
    )
    module_integration_map_complete = (
        midplatform_closure_gap_matrix_complete and len(integration_modules) >= 6
    )

    deferred_routes = [
        {"route_id": "B", "route": ROUTE_B, "defer_reason": "After foundation closure consolidation"},
        {"route_id": "C", "route": ROUTE_C, "defer_reason": "Optional quality improvement track"},
        {"route_id": "D", "route": ROUTE_D, "defer_reason": "Registry only; not current blocker"},
    ]
    mainline_closure_route_decision_complete = (
        module_integration_map_complete and SELECTED_ROUTE == ROUTE_A
    )

    future_test_strategy_consolidation_complete = (
        prior_owner_approval_request_module_handoff_go
        and handoff_test.get("no_fragmentary_phase_tests") is True
        and handoff_test.get("owner_approval_request_slice_dryrun_available_as_input") is True
    )

    do_not_reopen_rules_complete = prior_owner_approval_request_module_handoff_go
    next_phase_recommendation_complete = mainline_closure_route_decision_complete

    template_lineage = build_template_lineage(
        base_phase="Owner-Approval-Request-Module-Handoff-v1-001",
        base_capability=BROADER_MIDPLATFORM_CLOSURE_ROADMAP_WHITELIST_FILES[0],
        base_runner=BROADER_MIDPLATFORM_CLOSURE_ROADMAP_WHITELIST_FILES[1],
        base_verifier=BROADER_MIDPLATFORM_CLOSURE_ROADMAP_WHITELIST_FILES[2],
        base_go_no_go_pack=ROADMAP_GO_NO_GO_PACK,
        stage_phase="Task-Manager-Broader-Midplatform-Closure-Roadmap-v1-001",
        stage_term_overrides=BROADER_MIDPLATFORM_CLOSURE_ROADMAP_STAGE_TERM_OVERRIDES,
        stage_additions=BROADER_MIDPLATFORM_CLOSURE_ROADMAP_STAGE_ADDITIONS,
        template_files=BROADER_MIDPLATFORM_CLOSURE_ROADMAP_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Owner-Approval-Request-Module-Handoff-v1-001",
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
        previous_interruption_type=handoff_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=handoff_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=handoff_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    roadmap_pass = (
        prior_owner_approval_request_module_handoff_go
        and broader_midplatform_status_inventory_complete
        and midplatform_closure_gap_matrix_complete
        and module_integration_map_complete
        and mainline_closure_route_decision_complete
        and future_test_strategy_consolidation_complete
        and do_not_reopen_rules_complete
        and next_phase_recommendation_complete
        and owner_approval_request_chain_not_extended
        and future_runtime_debt_not_current_blocker
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase_readiness_ok = roadmap_pass
    next_phase = NEXT_PHASE_GO if roadmap_pass else NEXT_PHASE_HOLD

    if not prior_owner_approval_request_module_handoff_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not mainline_closure_route_decision_complete:
        final_decision = FINAL_DECISION_ROADMAP
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_owner_approval_request_module_handoff_go": prior_owner_approval_request_module_handoff_go,
        "broader_midplatform_status_inventory_complete": broader_midplatform_status_inventory_complete,
        "midplatform_closure_gap_matrix_complete": midplatform_closure_gap_matrix_complete,
        "module_integration_map_complete": module_integration_map_complete,
        "mainline_closure_route_decision_complete": mainline_closure_route_decision_complete,
        "future_test_strategy_consolidation_complete": future_test_strategy_consolidation_complete,
        "do_not_reopen_rules_complete": do_not_reopen_rules_complete,
        "next_phase_recommendation_complete": next_phase_recommendation_complete,
        "owner_approval_request_chain_not_extended": owner_approval_request_chain_not_extended,
        "future_runtime_debt_not_current_blocker": future_runtime_debt_not_current_blocker,
        "real_execution_not_authorized": handoff_summary.get("real_execution_not_authorized") is True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "broader_midplatform_closure_roadmap_pass": roadmap_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "do_not_open_real_issuance_preauth_unless_mainline_requires": True,
        "selected_route": SELECTED_ROUTE,
        "owner_approval_request_closed_module_status": "governance_ready_handoff",
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
            list(handoff_summary.get("chain_trace_nodes") or [])
            + ["task_manager_broader_midplatform_closure_roadmap"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    status_inventory = {
        "inventory_id": "broader_midplatform_status_inventory_v1",
        "broader_midplatform_status_inventory_complete": broader_midplatform_status_inventory_complete,
        "items": inventory_items,
        "source_mainline_items": list(MIDPLATFORM_MAINLINE_ITEMS),
        **meta,
    }
    gap_matrix = {
        "matrix_id": "midplatform_closure_gap_matrix_v1",
        "midplatform_closure_gap_matrix_complete": midplatform_closure_gap_matrix_complete,
        "future_runtime_debt_not_current_blocker": future_runtime_debt_not_current_blocker,
        "gaps": gap_rows,
        **meta,
    }
    integration_map = {
        "map_id": "module_integration_map_v1",
        "module_integration_map_complete": module_integration_map_complete,
        "modules": integration_modules,
        "owner_approval_request_note": "governance_ready_submodule_only; does not trigger real issuance",
        **meta,
    }
    route_decision = {
        "decision_id": "mainline_closure_route_decision_v1",
        "mainline_closure_route_decision_complete": mainline_closure_route_decision_complete,
        "selected_route": SELECTED_ROUTE,
        "selected_route_id": "A",
        "deferred_routes": deferred_routes,
        "not_selected_real_issuance_preauth": True,
        **meta,
    }
    test_consolidation = {
        "consolidation_id": "future_test_strategy_consolidation_v1",
        "future_test_strategy_consolidation_complete": future_test_strategy_consolidation_complete,
        "test_layers": list(handoff_test.get("test_layers") or [
            "module_level_test",
            "functional_slice_test",
            "midplatform_integration_test",
            "real_execution_preauthorization_gate",
        ]),
        "no_runtime_test_now": True,
        "owner_approval_request_slice_dryrun_as_input": True,
        "functional_slice_dryrun_root": handoff_test.get("functional_slice_dryrun_root"),
        **meta,
    }
    do_not_reopen = {
        "rules_id": "do_not_reopen_rules_v1",
        "do_not_reopen_rules_complete": do_not_reopen_rules_complete,
        "rules": [
            "do_not_extend_owner_approval_request_fragmentary_phases",
            "do_not_reopen_l1_protocol_review",
            "do_not_rerun_shared_protocol_validation",
            "do_not_rerun_29_protocol_classification",
            "file_size_governance_remains_active",
            "do_not_open_real_issuance_preauth_unless_mainline_requires",
        ],
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        **meta,
    }
    next_phase_rec = {
        "recommendation_id": "next_phase_recommendation_v1",
        "next_phase_recommendation_complete": next_phase_recommendation_complete,
        "recommended_next_phase": next_phase,
        "alternate_if_gap_obvious": NEXT_PHASE_ALT,
        "rationale": "Foundation closure consolidation before integration test or runtime debt registry",
        **meta,
    }
    roadmap = {
        "roadmap_id": "broader_midplatform_closure_roadmap_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "broader_midplatform_closure_roadmap_pass": roadmap_pass,
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
            "# Broader Midplatform Closure Roadmap v1",
            "",
            "Task Manager / Midplatform mainline inventory and closure route decision.",
            "",
            f"Selected route: `{SELECTED_ROUTE}`",
            f"Owner approval request: `governance_ready_handoff` (not extended)",
            f"Future runtime debt not current blocker: `{future_runtime_debt_not_current_blocker}`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "broader_midplatform_closure_roadmap": roadmap,
        "broader_midplatform_closure_roadmap_md": markdown,
        "broader_midplatform_status_inventory": status_inventory,
        "midplatform_closure_gap_matrix": gap_matrix,
        "module_integration_map": integration_map,
        "mainline_closure_route_decision": route_decision,
        "future_test_strategy_consolidation": test_consolidation,
        "do_not_reopen_rules": do_not_reopen,
        "next_phase_recommendation": next_phase_rec,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
