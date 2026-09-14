# -*- coding: utf-8 -*-
"""Luna Midplatform Owner Approval Request Governance Gate Integrated Planning v1.

One-shot integrated planning: roadmap decision, issuance authorization planning,
missing conditions routing, record/approval/ack/evidence closure boundary,
module-level functional slice test planning. No real execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_STAGE_ADDITIONS,
    OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_STAGE_TERM_OVERRIDES,
    OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_WHITELIST_FILES,
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
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_dryrun_v1 import (
    CANDIDATE_BOUNDARY_PAIRS,
    CORE_CANDIDATE_IDS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Governance-Gate-Integrated-Planning-v1-001"
SCOPE = "midplatform_task_manager_owner_approval_request_governance_gate_integrated_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_owner_approval_request_governance_gate_integrated_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_READY_FOR_INTEGRATED_DRYRUN"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_BLOCKED_BY_FINAL_GATE_PLANNING_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_INTEGRATED = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_BLOCKED_BY_INTEGRATED_PLAN_GAP"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Governance-Gate-Integrated-DryRun-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Governance-Gate-Integrated-Planning-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_owner_approval_request_governance_gate_integrated_planning_v1_smoke_v0"
)
INTEGRATED_PLANNING_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_governance_gate_integrated_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_owner_approval_request_governance_gate_integrated_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_owner_approval_request_governance_gate_integrated_planning_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_foundation_handoff_evaluation_template_lineage_v1.py"

INTEGRATED_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.json",
    "task_manager_owner_approval_request_governance_gate_integrated_plan_v1.md",
    "task_manager_owner_approval_request_governance_gate_route_matrix_v1.json",
    "task_manager_owner_approval_request_governance_gate_missing_conditions_route_mapping_v1.json",
    "task_manager_owner_approval_request_governance_gate_issuance_authorization_plan_v1.json",
    "task_manager_owner_approval_request_governance_gate_record_approval_ack_evidence_closure_boundary_v1.json",
    "task_manager_owner_approval_request_governance_gate_module_level_functional_slice_test_plan_v1.json",
    "task_manager_owner_approval_request_governance_gate_non_execution_boundary_v1.json",
    "task_manager_owner_approval_request_governance_gate_next_phase_readiness_v1.json",
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
        "disposition": "classified_not_resolved_at_integrated_planning",
    },
    "record_approval_closure_candidate_chain": {
        "category": "non_blocking",
        "primary_route": ROUTE_A,
        "secondary_route": ROUTE_B,
        "disposition": "resolved_prerequisite_for_authorization_planning",
    },
}

SLICE_TEST_SCOPES: Tuple[str, ...] = (
    "owner_approval_request_record_candidate",
    "owner_approval_record_candidate",
    "owner_operator_ack_record_candidate",
    "approval_evidence_bound_record_candidate",
    "owner_approval_request_record_approval_closure_candidate",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_final_gate_planning_go",
    "integrated_planning_complete",
    "roadmap_decision_integrated",
    "missing_conditions_route_mapping_complete",
    "issuance_authorization_plan_complete",
    "record_approval_ack_evidence_boundary_complete",
    "module_level_slice_test_plan_complete",
    "route_matrix_complete",
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
        "integrated_planning_only": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "final_gate_planning_root": str(final_gate),
    }


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [
        {"route_id": "A", "route_label": ROUTE_A, "role": "primary", "executes_real_issuance": False},
        {"route_id": "B", "route_label": ROUTE_B, "role": "secondary", "executes_real_issuance": False},
        {"route_id": "C", "route_label": ROUTE_C, "role": "secondary_parallel", "executes_real_issuance": False},
        {"route_id": "D", "route_label": ROUTE_D, "role": "secondary_future_runtime", "executes_real_issuance": False},
        {"route_id": "E", "route_label": ROUTE_E, "role": "secondary_governance_debt", "executes_real_issuance": False},
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
                "primary_route": template.get("primary_route"),
                "secondary_route": template.get("secondary_route"),
                "disposition": template.get("disposition"),
            }
        )
    return mapped


def _build_closure_boundary_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for candidate, forbidden in CANDIDATE_BOUNDARY_PAIRS:
        rows.append(
            {
                "candidate_id": candidate,
                "forbidden_final_state": forbidden,
                "still_candidate": True,
                "record_created": False,
                "closure_executed": False,
            }
        )
    return rows


def _build_slice_test_plan() -> List[Dict[str, Any]]:
    return [
        {
            "scope_id": scope,
            "test_type": "functional_slice",
            "blocking_governance_gate": False,
            "planned": True,
            "executed": False,
            "note": "Module-First cadence: slice test after module fill, before release gate.",
        }
        for scope in SLICE_TEST_SCOPES
    ]


def run_task_manager_owner_approval_request_governance_gate_integrated_planning_v1(
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

    conditions = list(missing_doc.get("conditions") or [])
    real_request_cond = next((c for c in conditions if c.get("condition_id") == "real_request_issuance"), {})
    chain_cond = next(
        (c for c in conditions if c.get("condition_id") == "record_approval_closure_candidate_chain"), {}
    )
    real_request_blocker_active = any(
        b.get("blocker_id") == "real_request_issuance_not_authorized" and b.get("active")
        for b in blocker_doc.get("blockers") or []
    )

    prior_final_gate_planning_go = (
        gate_summary.get("final_decision") == FINAL_GATE_PLANNING_FINAL_GO
        and gate_summary.get("recommended_next_phase") == FINAL_GATE_PLANNING_NEXT_PHASE
        and gate_verifier.get("verifier") == "GO"
        and int(gate_verifier.get("passed_checks", 0)) >= 300
        and gate_verifier.get("failed_checks") == 0
        and gate_summary.get("final_gate_planning_pass") is True
        and gate_summary.get("final_gate_plan_complete") is True
        and gate_summary.get("missing_conditions_matrix_complete") is True
        and real_request_cond.get("category") == "blocker"
        and real_request_cond.get("resolved") is False
        and real_request_blocker_active
    )
    if not prior_final_gate_planning_go:
        issues.append("final_gate_planning_not_go")

    route_mappings = _map_conditions(conditions)
    missing_conditions_route_mapping_complete = (
        prior_final_gate_planning_go
        and len(route_mappings) >= 6
        and all(m.get("primary_route") for m in route_mappings)
    )
    if not missing_conditions_route_mapping_complete:
        issues.append("route_mapping_incomplete")

    route_matrix = _build_route_matrix()
    route_matrix_complete = len(route_matrix) == 5 and route_matrix[0].get("route_label") == ROUTE_A
    roadmap_decision_integrated = (
        prior_final_gate_planning_go
        and route_matrix_complete
        and missing_conditions_route_mapping_complete
        and route_matrix[0].get("role") == "primary"
    )
    if not roadmap_decision_integrated:
        issues.append("roadmap_decision_not_integrated")

    authorization_steps = [
        "define_owner_operator_authorization_prerequisites",
        "define_request_issuance_authorization_scope_candidate_only",
        "define_notification_authorization_boundary_candidate_only",
        "define_pre_issuance_absence_checks",
        "define_post_authorization_planning_handoff_to_dryrun",
    ]
    issuance_authorization_plan_complete = (
        roadmap_decision_integrated
        and chain_cond.get("resolved") is True
        and len(authorization_steps) >= 4
    )
    if not issuance_authorization_plan_complete:
        issues.append("authorization_plan_incomplete")

    closure_rows = _build_closure_boundary_rows()
    record_approval_ack_evidence_boundary_complete = (
        prior_final_gate_planning_go
        and len(closure_rows) == len(CORE_CANDIDATE_IDS)
        and all(r.get("still_candidate") for r in closure_rows)
        and all(r.get("record_created") is False for r in closure_rows)
    )
    if not record_approval_ack_evidence_boundary_complete:
        issues.append("closure_boundary_incomplete")

    slice_tests = _build_slice_test_plan()
    module_level_slice_test_plan_complete = (
        prior_final_gate_planning_go
        and len(slice_tests) == len(SLICE_TEST_SCOPES)
        and all(not t.get("blocking_governance_gate") for t in slice_tests)
        and all(t.get("executed") is False for t in slice_tests)
    )
    if not module_level_slice_test_plan_complete:
        issues.append("slice_test_plan_incomplete")

    absence = {key: gate_summary.get(key) is True for key in ABSENCE_KEYS}
    non_execution_boundary_ok = (
        prior_final_gate_planning_go
        and gate_summary.get("non_execution_boundary_ok") is True
        and all(absence.values())
    )
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if gate_summary.get(flag) is True:
            non_execution_boundary_ok = False
            issues.append(f"runtime_flag:{flag}")
            break

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Planning-v1-001",
        base_capability=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_WHITELIST_FILES[0],
        base_runner=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_WHITELIST_FILES[1],
        base_verifier=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=INTEGRATED_PLANNING_GO_NO_GO_PACK,
        stage_phase="Owner-Approval-Request-Governance-Gate-Integrated-Planning-v1-001",
        stage_term_overrides=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_STAGE_ADDITIONS,
        template_files=OWNER_APPROVAL_REQUEST_GOVERNANCE_GATE_INTEGRATED_PLANNING_WHITELIST_FILES,
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

    integrated_planning_complete = (
        roadmap_decision_integrated
        and issuance_authorization_plan_complete
        and record_approval_ack_evidence_boundary_complete
        and module_level_slice_test_plan_complete
        and template_lineage_ok
        and file_size_governance_review_ok
    )

    next_phase_readiness_ok = (
        integrated_planning_complete
        and non_execution_boundary_ok
        and prior_final_gate_planning_go
    )

    if not prior_final_gate_planning_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not template_lineage_ok:
        final_decision = FINAL_DECISION_LINEAGE
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not integrated_planning_complete:
        final_decision = FINAL_DECISION_INTEGRATED
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_final_gate_planning_go": prior_final_gate_planning_go,
        "integrated_planning_complete": integrated_planning_complete,
        "roadmap_decision_integrated": roadmap_decision_integrated,
        "missing_conditions_route_mapping_complete": missing_conditions_route_mapping_complete,
        "issuance_authorization_plan_complete": issuance_authorization_plan_complete,
        "record_approval_ack_evidence_boundary_complete": record_approval_ack_evidence_boundary_complete,
        "module_level_slice_test_plan_complete": module_level_slice_test_plan_complete,
        "route_matrix_complete": route_matrix_complete,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "real_request_issuance_authorized": False,
        "real_request_issuance_not_executed": True,
        "selected_route": ROUTE_A,
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
    integrated_planning_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(go_condition_values[k] for k in GO_CONDITIONS_KEYS)
    )
    next_phase = NEXT_PHASE_GO if integrated_planning_pass else NEXT_PHASE_HOLD
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_condition_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(gate_summary.get("chain_trace_nodes") or [])
            + ["owner_approval_request_governance_gate_integrated_planning"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    integrated_plan = {
        "plan_id": "task_manager_owner_approval_request_governance_gate_integrated_plan_v1",
        "integrated_planning_complete": integrated_planning_complete,
        "integrated_blocks": [
            "roadmap_decision",
            "issuance_authorization_planning",
            "missing_conditions_routing",
            "record_approval_ack_evidence_closure_boundary",
            "module_level_functional_slice_test_planning",
        ],
        "selected_route": ROUTE_A,
        "real_request_issuance_authorized": False,
        **go_condition_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    route_matrix_doc = {
        "matrix_id": "task_manager_owner_approval_request_governance_gate_route_matrix_v1",
        "route_matrix_complete": route_matrix_complete,
        "selected_route": ROUTE_A,
        "routes": route_matrix,
        **meta,
    }
    route_mapping_doc = {
        "mapping_id": "task_manager_owner_approval_request_governance_gate_missing_conditions_route_mapping_v1",
        "missing_conditions_route_mapping_complete": missing_conditions_route_mapping_complete,
        "mappings": route_mappings,
        **meta,
    }
    authorization_plan = {
        "plan_id": "task_manager_owner_approval_request_governance_gate_issuance_authorization_plan_v1",
        "issuance_authorization_plan_complete": issuance_authorization_plan_complete,
        "authorization_steps": authorization_steps,
        "executes_real_issuance": False,
        "executes_real_notification": False,
        "real_request_issuance_authorized": False,
        **meta,
    }
    closure_boundary = {
        "boundary_id": "task_manager_owner_approval_request_governance_gate_record_approval_ack_evidence_closure_boundary_v1",
        "record_approval_ack_evidence_boundary_complete": record_approval_ack_evidence_boundary_complete,
        "core_candidate_ids": list(CORE_CANDIDATE_IDS),
        "boundary_pairs": [{"candidate": c, "forbidden_final": f} for c, f in CANDIDATE_BOUNDARY_PAIRS],
        "rows": closure_rows,
        **meta,
    }
    slice_test_plan = {
        "plan_id": "task_manager_owner_approval_request_governance_gate_module_level_functional_slice_test_plan_v1",
        "module_level_slice_test_plan_complete": module_level_slice_test_plan_complete,
        "slice_tests": slice_tests,
        **meta,
    }
    non_execution_boundary = {
        "boundary_id": "task_manager_owner_approval_request_governance_gate_non_execution_boundary_v1",
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "request_issued": False,
        "notification_sent": False,
        "real_request_issuance_authorized": False,
        **absence,
        **meta,
    }
    next_phase_readiness = {
        "readiness_id": "task_manager_owner_approval_request_governance_gate_next_phase_readiness_v1",
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "recommended_next_phase": next_phase,
        "target": "owner_approval_request_governance_gate_integrated_dryrun",
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "integrated_planning_pass": integrated_planning_pass,
        "integrated_planning_only": True,
        "blocker_count": len(issues),
        "issues": issues,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Owner Approval Request Governance Gate Integrated Planning v1",
            "",
            "One-shot integrated planning. No real request issuance, notification, record, approval, grant, or runtime.",
            "",
            f"Selected route: `{ROUTE_A}`",
            f"Integrated planning complete: `{integrated_planning_complete}`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "task_manager_owner_approval_request_governance_gate_integrated_plan": integrated_plan,
        "task_manager_owner_approval_request_governance_gate_integrated_plan_md": markdown,
        "task_manager_owner_approval_request_governance_gate_route_matrix": route_matrix_doc,
        "task_manager_owner_approval_request_governance_gate_missing_conditions_route_mapping": route_mapping_doc,
        "task_manager_owner_approval_request_governance_gate_issuance_authorization_plan": authorization_plan,
        "task_manager_owner_approval_request_governance_gate_record_approval_ack_evidence_closure_boundary": closure_boundary,
        "task_manager_owner_approval_request_governance_gate_module_level_functional_slice_test_plan": slice_test_plan,
        "task_manager_owner_approval_request_governance_gate_non_execution_boundary": non_execution_boundary,
        "task_manager_owner_approval_request_governance_gate_next_phase_readiness": next_phase_readiness,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
