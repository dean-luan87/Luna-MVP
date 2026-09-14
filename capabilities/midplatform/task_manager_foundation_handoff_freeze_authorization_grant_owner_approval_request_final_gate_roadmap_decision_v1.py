# -*- coding: utf-8 -*-
"""Luna Midplatform Final Gate Roadmap Decision v1 — route missing conditions, no real issuance.

Accepts Final Gate Planning GO; maps missing conditions to routes A–E.
Primary route: Issuance Authorization Planning. No protocol body revalidation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FINAL_GATE_PLANNING_ROOT,
    FINAL_DECISION_GO as FINAL_GATE_PLANNING_FINAL_GO,
    NEXT_PHASE_GO as FINAL_GATE_PLANNING_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Roadmap-Decision-v1-001"
)
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_READY_FOR_ISSUANCE_AUTHORIZATION_PLANNING"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_BLOCKED_BY_FINAL_GATE_PLANNING_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_ROUTE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_BLOCKED_BY_ROUTE_SELECTION_GAP"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Authorization-Planning-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Roadmap-Decision-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1_smoke_v0"
)
ROADMAP_DECISION_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_foundation_handoff_evaluation_template_lineage_v1.py"

ROADMAP_DECISION_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_route_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions_route_mapping_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_selected_route_rationale_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_non_execution_boundary_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_next_phase_readiness_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

FINAL_GATE_INDEX_FILES: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_blocker_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_readiness_matrix_v1.json",
    "file_size_governance_review_v1.json",
)

ROUTE_A = "Route A — Owner Approval Request Issuance Authorization Planning"
ROUTE_B = "Route B — Missing Conditions Closure Planning"
ROUTE_C = "Route C — Module-Level Functional Slice Test Planning"
ROUTE_D = "Route D — Runtime / Adapter Readiness Roadmap"
ROUTE_E = "Route E — Governance Debt Closure Roadmap"

ALL_ROUTES: Tuple[str, ...] = (ROUTE_A, ROUTE_B, ROUTE_C, ROUTE_D, ROUTE_E)

CONDITION_ROUTE_MAP: Dict[str, Dict[str, str]] = {
    "real_request_issuance": {
        "category": "blocker",
        "primary_route": ROUTE_A,
        "secondary_route": ROUTE_B,
        "disposition": "authorization_planning_prerequisite",
    },
    "runtime_adapter_implementation": {
        "category": "future_runtime",
        "primary_route": ROUTE_D,
        "secondary_route": ROUTE_E,
        "disposition": "future_runtime_debt_preserved",
    },
    "whitebox_runtime_integration": {
        "category": "future_runtime",
        "primary_route": ROUTE_D,
        "secondary_route": ROUTE_E,
        "disposition": "designed_absent_not_blocking_authorization_planning",
    },
    "module_level_functional_slice_tests": {
        "category": "non_blocking",
        "primary_route": ROUTE_C,
        "secondary_route": ROUTE_A,
        "disposition": "parallel_follow_up_not_blocking_governance_gate",
    },
    "governance_debt_closure": {
        "category": "governance_debt",
        "primary_route": ROUTE_E,
        "secondary_route": ROUTE_B,
        "disposition": "classified_not_resolved_at_roadmap_decision",
    },
    "record_approval_closure_candidate_chain": {
        "category": "non_blocking",
        "primary_route": ROUTE_A,
        "secondary_route": ROUTE_B,
        "disposition": "resolved_prerequisite_for_authorization_planning",
    },
}

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_final_gate_planning_go",
    "roadmap_decision_complete",
    "route_matrix_complete",
    "missing_conditions_route_mapping_complete",
    "selected_route_rationale_complete",
    "selected_route_is_authorization_planning",
    "real_request_issuance_not_executed",
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


def _meta(out: Path, final_gate: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "roadmap_decision_only": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "final_gate_planning_root": str(final_gate),
    }


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [
        {
            "route_id": "A",
            "route_label": ROUTE_A,
            "role": "primary",
            "targets": "issuance_authorization_planning",
            "executes_real_issuance": False,
        },
        {
            "route_id": "B",
            "route_label": ROUTE_B,
            "role": "secondary",
            "targets": "missing_conditions_closure_planning",
            "executes_real_issuance": False,
        },
        {
            "route_id": "C",
            "route_label": ROUTE_C,
            "role": "secondary_parallel",
            "targets": "module_level_functional_slice_test_planning",
            "executes_real_issuance": False,
        },
        {
            "route_id": "D",
            "route_label": ROUTE_D,
            "role": "secondary_future_runtime",
            "targets": "runtime_adapter_readiness_roadmap",
            "executes_real_issuance": False,
        },
        {
            "route_id": "E",
            "route_label": ROUTE_E,
            "role": "secondary_governance_debt",
            "targets": "governance_debt_closure_roadmap",
            "executes_real_issuance": False,
        },
    ]


def _map_conditions(conditions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    mapped: List[Dict[str, Any]] = []
    for cond in conditions:
        cid = cond.get("condition_id") or ""
        template = CONDITION_ROUTE_MAP.get(cid, {})
        mapped.append(
            {
                "condition_id": cid,
                "source_category": cond.get("category"),
                "source_resolved": cond.get("resolved"),
                "source_note": cond.get("note"),
                "routed_category": template.get("category", cond.get("category")),
                "primary_route": template.get("primary_route"),
                "secondary_route": template.get("secondary_route"),
                "disposition": template.get("disposition"),
            }
        )
    return mapped


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1(
    *,
    final_gate_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    final_gate = Path(final_gate_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, final_gate)
    issues: List[str] = []

    gate_summary = _read_json(final_gate / "summary.json")
    gate_verifier = _read_json(final_gate / "verifier_report.json")
    gate_file_size = _read_json(final_gate / "file_size_governance_review_v1.json")
    missing_doc = _read_json(final_gate / FINAL_GATE_INDEX_FILES[2])
    blocker_doc = _read_json(final_gate / FINAL_GATE_INDEX_FILES[3])
    readiness_doc = _read_json(final_gate / FINAL_GATE_INDEX_FILES[4])

    conditions = list(missing_doc.get("conditions") or [])
    real_request_cond = next((c for c in conditions if c.get("condition_id") == "real_request_issuance"), {})
    real_request_blocker_active = any(
        b.get("blocker_id") == "real_request_issuance_not_authorized" and b.get("active")
        for b in blocker_doc.get("blockers") or []
    )
    real_request_issuance_authorized = False

    prior_final_gate_planning_go = (
        gate_summary.get("final_decision") == FINAL_GATE_PLANNING_FINAL_GO
        and gate_summary.get("recommended_next_phase") == FINAL_GATE_PLANNING_NEXT_PHASE
        and gate_verifier.get("verifier") == "GO"
        and int(gate_verifier.get("passed_checks", 0)) >= 300
        and gate_verifier.get("failed_checks") == 0
        and gate_verifier.get("blocker_count") == 0
        and gate_summary.get("final_gate_planning_pass") is True
        and gate_summary.get("final_gate_plan_complete") is True
        and gate_summary.get("missing_conditions_matrix_complete") is True
        and gate_summary.get("blocker_matrix_complete") is True
        and gate_summary.get("module_first_cadence_rule_ref_ok") is True
        and gate_summary.get("file_size_governance_review_ok") is True
        and real_request_cond.get("category") == "blocker"
        and real_request_cond.get("resolved") is False
        and real_request_blocker_active
    )
    if not prior_final_gate_planning_go:
        issues.append("final_gate_planning_not_go")

    route_mappings = _map_conditions(conditions)
    missing_conditions_route_mapping_complete = (
        prior_final_gate_planning_go
        and missing_doc.get("missing_conditions_matrix_complete") is True
        and len(route_mappings) >= 6
        and all(m.get("primary_route") for m in route_mappings)
    )
    if not missing_conditions_route_mapping_complete:
        issues.append("route_mapping_incomplete")

    route_matrix = _build_route_matrix()
    route_matrix_complete = (
        prior_final_gate_planning_go
        and len(route_matrix) == 5
        and route_matrix[0].get("route_label") == ROUTE_A
        and route_matrix[0].get("role") == "primary"
    )
    if not route_matrix_complete:
        issues.append("route_matrix_incomplete")

    real_request_cond = next((c for c in conditions if c.get("condition_id") == "real_request_issuance"), {})
    chain_cond = next(
        (c for c in conditions if c.get("condition_id") == "record_approval_closure_candidate_chain"), {}
    )
    real_request_issuance_not_executed = (
        prior_final_gate_planning_go
        and real_request_cond.get("resolved") is False
        and real_request_cond.get("category") == "blocker"
        and real_request_issuance_authorized is False
    )
    if not real_request_issuance_not_executed:
        issues.append("real_request_issuance_escalation")

    absence = {key: gate_summary.get(key) is True for key in ABSENCE_KEYS}
    non_execution_boundary_ok = (
        prior_final_gate_planning_go
        and gate_summary.get("non_execution_boundary_ok") is True
        and blocker_doc.get("blocker_matrix_complete") is True
        and all(absence.values())
    )
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if gate_summary.get(flag) is True:
            non_execution_boundary_ok = False
            issues.append(f"runtime_flag:{flag}")
            break

    selected_route = ROUTE_A
    secondary_routes = [ROUTE_B, ROUTE_C, ROUTE_D, ROUTE_E]
    selected_route_is_authorization_planning = selected_route == ROUTE_A
    rationale_points = [
        "Record/Approval Closure candidate chain resolved — prerequisite for authorization planning.",
        "Final Gate Planning GO — missing conditions consolidated and ready for route disposition.",
        "real_request_issuance remains blocker/unresolved — next step is authorization planning, not execution.",
        "runtime_adapter and whitebox integration are future_runtime debt — do not block authorization planning.",
        "module_level_functional_slice_tests is non_blocking parallel follow-up per Module-First cadence.",
        "governance_debt_closure classified only — not resolved at roadmap decision.",
    ]
    selected_route_rationale_complete = (
        prior_final_gate_planning_go
        and selected_route_is_authorization_planning
        and chain_cond.get("resolved") is True
        and len(rationale_points) >= 5
    )
    if not selected_route_rationale_complete:
        issues.append("rationale_incomplete")

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Planning-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_WHITELIST_FILES[2],
        base_go_no_go_pack=ROADMAP_DECISION_GO_NO_GO_PACK,
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Roadmap-Decision-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_ROADMAP_DECISION_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Planning-v1-001",
    )
    template_lineage_ok = template_lineage.get("template_lineage_ok") is True
    if not template_lineage_ok:
        issues.append("template_lineage_gap")

    file_size_governance_review = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=repo_root,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path=TEMPLATE_LINEAGE_MODULE_PATH,
        read_strategy="summary_index_first",
        full_repo_scan=False,
        previous_interruption_type=gate_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=gate_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=gate_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    roadmap_decision_complete = (
        prior_final_gate_planning_go
        and route_matrix_complete
        and missing_conditions_route_mapping_complete
        and selected_route_rationale_complete
        and template_lineage_ok
        and file_size_governance_review_ok
    )

    next_phase_readiness_ok = (
        roadmap_decision_complete
        and non_execution_boundary_ok
        and real_request_issuance_not_executed
        and selected_route_is_authorization_planning
    )

    if not prior_final_gate_planning_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not template_lineage_ok:
        final_decision = FINAL_DECISION_LINEAGE
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not selected_route_rationale_complete or not route_matrix_complete:
        final_decision = FINAL_DECISION_ROUTE
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_final_gate_planning_go": prior_final_gate_planning_go,
        "roadmap_decision_complete": roadmap_decision_complete,
        "route_matrix_complete": route_matrix_complete,
        "missing_conditions_route_mapping_complete": missing_conditions_route_mapping_complete,
        "selected_route_rationale_complete": selected_route_rationale_complete,
        "selected_route_is_authorization_planning": selected_route_is_authorization_planning,
        "real_request_issuance_not_executed": real_request_issuance_not_executed,
        "real_request_issuance_authorized": real_request_issuance_authorized,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "template_lineage_ok": template_lineage_ok,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "large_file_read_avoidance_ok": file_size_governance_review.get("large_file_read_avoidance_ok") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "verifier_large_file_scan_absent": file_size_governance_review.get("verifier_large_file_scan_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    roadmap_decision_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(go_condition_values[k] for k in GO_CONDITIONS_KEYS if k != "real_request_issuance_authorized")
        and go_condition_values["real_request_issuance_authorized"] is False
    )
    next_phase = NEXT_PHASE_GO if roadmap_decision_pass else NEXT_PHASE_HOLD
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_condition_values[k] for k in GO_CONDITIONS_KEYS if k != "real_request_issuance_authorized"},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(gate_summary.get("chain_trace_nodes") or [])
            + ["freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    roadmap_decision = {
        "decision_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_v1",
        "roadmap_decision_complete": roadmap_decision_complete,
        "selected_route": selected_route,
        "secondary_routes": secondary_routes,
        "selected_route_is_authorization_planning": selected_route_is_authorization_planning,
        "real_request_issuance_authorized": False,
        "real_request_issuance_not_executed": real_request_issuance_not_executed,
        "final_gate_final_decision": gate_summary.get("final_decision"),
        "readiness_matrix_ref": readiness_doc.get("matrix_id"),
        **go_condition_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    route_matrix_doc = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_route_matrix_v1",
        "route_matrix_complete": route_matrix_complete,
        "selected_route": selected_route,
        "routes": route_matrix,
        **meta,
    }
    route_mapping_doc = {
        "mapping_id": "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions_route_mapping_v1",
        "missing_conditions_route_mapping_complete": missing_conditions_route_mapping_complete,
        "mappings": route_mappings,
        **meta,
    }
    rationale_doc = {
        "rationale_id": "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_selected_route_rationale_v1",
        "selected_route_rationale_complete": selected_route_rationale_complete,
        "selected_route": selected_route,
        "secondary_routes": secondary_routes,
        "rationale_points": rationale_points,
        **meta,
    }
    non_execution_boundary = {
        "boundary_id": "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_non_execution_boundary_v1",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "request_issued": False,
        "notification_sent": False,
        "request_record_created": False,
        "approval_record_created": False,
        "grant_issued": False,
        "foundation_frozen": False,
        "closure_executed": False,
        "runtime_execution_absent": True,
        "real_request_issuance_authorized": False,
        **absence,
        **meta,
    }
    next_phase_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_next_phase_readiness_v1",
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_request_issuance_authorization_planning",
        "issuance_authorization_planning_readiness": next_phase_readiness_ok,
        "request_issued": False,
        "real_request_issuance_authorized": False,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "roadmap_decision_pass": roadmap_decision_pass,
        "roadmap_decision_only": True,
        "selected_route": selected_route,
        "blocker_count": len(issues),
        "issues": issues,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Final Gate Roadmap Decision Report v1",
            "",
            "Route disposition for missing conditions. No real request issuance.",
            "",
            f"Prior Final Gate Planning GO: `{prior_final_gate_planning_go}`",
            f"Selected route: `{selected_route}`",
            f"real_request_issuance authorized: `False`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision": roadmap_decision,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_route_matrix": route_matrix_doc,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions_route_mapping": route_mapping_doc,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_selected_route_rationale": rationale_doc,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_non_execution_boundary": non_execution_boundary,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_next_phase_readiness": next_phase_readiness,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
