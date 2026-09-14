# -*- coding: utf-8 -*-
"""Luna Midplatform Owner Approval Request Authorization Preparation DryRun v1.

Candidate-level dry-run for integrated implementation authorization preparation package.
No real authorization, no real request issuance. No fragmentary sub-phases.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_STAGE_ADDITIONS,
    OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_STAGE_TERM_OVERRIDES,
    OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_WHITELIST_FILES,
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
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_v1 import (
    DEFAULT_OUTPUT as DEFAULT_INTEGRATED_IMPLEMENTATION_ROOT,
    FINAL_DECISION_GO as INTEGRATED_IMPLEMENTATION_FINAL_GO,
    FUNCTIONAL_SLICE_CHAINS,
    NEXT_PHASE_A,
    SELECTED_ROUTE,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Authorization-Preparation-DryRun-v1-001"
SCOPE = "midplatform_task_manager_owner_approval_request_authorization_preparation_dryrun_only"
SOURCE_CHAIN = "midplatform_task_manager_owner_approval_request_authorization_preparation_dryrun_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_READY_FOR_MODULE_LEVEL_FUNCTIONAL_SLICE_PLANNING_OR_AUTHORIZATION_PREPARATION_REVIEW"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_BLOCKED_BY_INTEGRATED_IMPLEMENTATION_GAP"
)
FINAL_DECISION_PACKAGE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_BLOCKED_BY_PACKAGE_ESCALATION"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_ROUTING = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_BLOCKED_BY_ROUTING_DRIFT"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Level-Functional-Slice-Planning-v1-001"
NEXT_PHASE_B = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Authorization-Preparation-Review-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Authorization-Preparation-DryRun-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_authorization_preparation_dryrun_v1_smoke_v0"
)
DRYRUN_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_authorization_preparation_dryrun_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_authorization_preparation_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_authorization_preparation_dryrun_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/owner_approval_request_governance_gate_template_lineage_v1.py"

DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "authorization_preparation_dryrun_report_v1.json",
    "authorization_preparation_dryrun_report_v1.md",
    "authorization_preparation_package_validation_v1.json",
    "authorization_precondition_validation_v1.json",
    "missing_conditions_routing_validation_v1.json",
    "real_issuance_safety_boundary_validation_v1.json",
    "functional_slice_followup_reference_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

UPSTREAM_INDEX: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "issuance_authorization_preparation_package_v1.json",
    "real_issuance_precondition_checklist_v1.json",
    "missing_conditions_routing_v1.json",
    "module_level_functional_slice_test_plan_v1.json",
)

EXPECTED_ROUTING_BUCKETS: Dict[str, str] = {
    "real_request_issuance": "blocker_before_real_issuance",
    "runtime_adapter_implementation": "future_runtime_debt",
    "whitebox_runtime_integration": "future_runtime_debt",
    "module_level_functional_slice_tests": "non_blocking_follow_up",
    "governance_debt_closure": "governance_debt",
    "record_approval_closure_candidate_chain": "resolved",
}

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_integrated_implementation_go",
    "authorization_preparation_package_validation_ok",
    "authorization_precondition_validation_ok",
    "missing_conditions_routing_validation_ok",
    "real_issuance_safety_boundary_ok",
    "file_size_governance_review_ok",
    "non_execution_boundary_ok",
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
        "authorization_preparation_dryrun_only": True,
        "no_fragmentary_phase_expansion": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "integrated_implementation_root": str(upstream),
    }


def run_task_manager_owner_approval_request_authorization_preparation_dryrun_v1(
    *,
    integrated_implementation_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(integrated_implementation_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    impl_summary = _read_json(upstream / "summary.json")
    impl_verifier = _read_json(upstream / "verifier_report.json")
    impl_file_size = _read_json(upstream / "file_size_governance_review_v1.json")
    auth_package = _read_json(upstream / UPSTREAM_INDEX[2])
    checklist = _read_json(upstream / UPSTREAM_INDEX[3])
    routing = _read_json(upstream / UPSTREAM_INDEX[4])
    slice_plan = _read_json(upstream / UPSTREAM_INDEX[5])

    prior_integrated_implementation_go = (
        impl_summary.get("final_decision") == INTEGRATED_IMPLEMENTATION_FINAL_GO
        and impl_summary.get("recommended_next_phase") == NEXT_PHASE_A
        and impl_verifier.get("verifier") == "GO"
        and int(impl_verifier.get("passed_checks", 0)) >= 300
        and impl_summary.get("integrated_implementation_pass") is True
        and impl_summary.get("selected_route") == SELECTED_ROUTE
        and impl_summary.get("no_fragmentary_phase_expansion") is True
        and impl_summary.get("real_request_issuance_authorized") is False
        and auth_package.get("issuance_authorization_preparation_package_complete") is True
    )
    if not prior_integrated_implementation_go:
        issues.append("integrated_implementation_not_go")

    authorization_preparation_package_validation_ok = (
        prior_integrated_implementation_go
        and auth_package.get("authorization_package_candidate") is True
        and auth_package.get("authorization_precondition_candidate") is True
        and auth_package.get("executes_real_authorization") is False
        and auth_package.get("authorization_request_absent") is True
        and auth_package.get("package_id") == "issuance_authorization_preparation_package_v1"
    )
    if not authorization_preparation_package_validation_ok:
        issues.append("package_escalation")

    checklist_items = {i.get("item_id"): i for i in checklist.get("items") or []}
    authorization_precondition_validation_ok = (
        prior_integrated_implementation_go
        and checklist.get("real_issuance_precondition_checklist_complete") is True
        and checklist_items.get("owner_operator_explicit_approval", {}).get("satisfied") is False
        and checklist_items.get("authorization_request_readiness", {}).get("satisfied") is False
        and checklist_items.get("record_approval_closure_candidate_chain", {}).get("satisfied") is True
        and checklist_items.get("runtime_boundary_readiness", {}).get("satisfied") is False
    )
    if not authorization_precondition_validation_ok:
        issues.append("precondition_gap")

    routes = {r.get("condition_id"): r for r in routing.get("routes") or []}
    missing_conditions_routing_validation_ok = (
        prior_integrated_implementation_go
        and routing.get("missing_conditions_routing_complete") is True
        and all(routes.get(cid, {}).get("routing_bucket") == bucket for cid, bucket in EXPECTED_ROUTING_BUCKETS.items())
    )
    if not missing_conditions_routing_validation_ok:
        issues.append("routing_drift")

    absence = {key: impl_summary.get(key) is True for key in ABSENCE_KEYS}
    real_issuance_safety_boundary_ok = (
        prior_integrated_implementation_go
        and impl_summary.get("non_execution_boundary_ok") is True
        and impl_summary.get("real_request_issuance_authorized") is False
        and auth_package.get("authorization_request_absent") is True
        and all(absence.values())
    )
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if impl_summary.get(flag) is True:
            real_issuance_safety_boundary_ok = False
            issues.append(f"runtime_flag:{flag}")
            break
    if not real_issuance_safety_boundary_ok:
        if "runtime_flag" not in "".join(issues):
            issues.append("safety_boundary_gap")

    slice_chains = list(slice_plan.get("chains") or [])
    functional_slice_followup_ok = (
        len(slice_chains) == len(FUNCTIONAL_SLICE_CHAINS)
        and all(not c.get("executed") for c in slice_chains)
        and all(not c.get("blocking_real_issuance_now") for c in slice_chains)
    )

    template_lineage = build_template_lineage(
        base_phase="Owner-Approval-Request-Governance-Gate-Integrated-Implementation-v1-001",
        base_capability=OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_WHITELIST_FILES[0],
        base_runner=OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_WHITELIST_FILES[1],
        base_verifier=OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_WHITELIST_FILES[2],
        base_go_no_go_pack=DRYRUN_GO_NO_GO_PACK,
        stage_phase="Owner-Approval-Request-Authorization-Preparation-DryRun-v1-001",
        stage_term_overrides=OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_STAGE_TERM_OVERRIDES,
        stage_additions=OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_STAGE_ADDITIONS,
        template_files=OWNER_APPROVAL_REQUEST_AUTHORIZATION_PREPARATION_DRYRUN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Owner-Approval-Request-Governance-Gate-Integrated-Implementation-v1-001",
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
        previous_interruption_type=impl_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=impl_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=impl_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    authorization_preparation_dryrun_pass = (
        prior_integrated_implementation_go
        and authorization_preparation_package_validation_ok
        and authorization_precondition_validation_ok
        and missing_conditions_routing_validation_ok
        and real_issuance_safety_boundary_ok
        and functional_slice_followup_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
    )

    next_phase_readiness_ok = authorization_preparation_dryrun_pass and real_issuance_safety_boundary_ok

    if not prior_integrated_implementation_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not authorization_preparation_package_validation_ok:
        final_decision = FINAL_DECISION_PACKAGE
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not real_issuance_safety_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not missing_conditions_routing_validation_ok:
        final_decision = FINAL_DECISION_ROUTING
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    elif not functional_slice_followup_ok:
        final_decision = FINAL_DECISION_ROUTING
    elif not authorization_preparation_dryrun_pass:
        final_decision = FINAL_DECISION_PACKAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_integrated_implementation_go": prior_integrated_implementation_go,
        "authorization_preparation_package_validation_ok": authorization_preparation_package_validation_ok,
        "authorization_precondition_validation_ok": authorization_precondition_validation_ok,
        "missing_conditions_routing_validation_ok": missing_conditions_routing_validation_ok,
        "real_issuance_safety_boundary_ok": real_issuance_safety_boundary_ok,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "non_execution_boundary_ok": real_issuance_safety_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "authorization_preparation_dryrun_pass": authorization_preparation_dryrun_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "no_fragmentary_phase_expansion": True,
        "selected_route": SELECTED_ROUTE,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    dryrun_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(go_values[k] for k in GO_CONDITIONS_KEYS)
    )
    next_phase = NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(impl_summary.get("chain_trace_nodes") or [])
            + ["owner_approval_request_authorization_preparation_dryrun"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    package_validation = {
        "validation_id": "authorization_preparation_package_validation_v1",
        "authorization_preparation_package_validation_ok": authorization_preparation_package_validation_ok,
        "package_still_candidate": auth_package.get("authorization_package_candidate") is True,
        "not_authorization_request": auth_package.get("authorization_request_absent") is True,
        "not_authorization_grant": True,
        "not_real_request_issuance": True,
        "package_ref": auth_package.get("package_id"),
        **meta,
    }
    precondition_validation = {
        "validation_id": "authorization_precondition_validation_v1",
        "authorization_precondition_validation_ok": authorization_precondition_validation_ok,
        "owner_operator_explicit_approval_satisfied": False,
        "authorization_request_readiness_satisfied": False,
        "record_evidence_candidate_level": True,
        "rollback_expiry_revocation_reference_only": True,
        "runtime_boundary_future_debt": True,
        "checklist_items": list(checklist.get("items") or []),
        **meta,
    }
    routing_validation = {
        "validation_id": "missing_conditions_routing_validation_v1",
        "missing_conditions_routing_validation_ok": missing_conditions_routing_validation_ok,
        "expected_buckets": EXPECTED_ROUTING_BUCKETS,
        "observed_routes": list(routing.get("routes") or []),
        **meta,
    }
    safety_boundary = {
        "validation_id": "real_issuance_safety_boundary_validation_v1",
        "real_issuance_safety_boundary_ok": real_issuance_safety_boundary_ok,
        "real_request_issuance_authorized": False,
        "request_issued": False,
        "notification_sent": False,
        **absence,
        **meta,
    }
    slice_followup = {
        "reference_id": "functional_slice_followup_reference_v1",
        "functional_slice_followup_ok": functional_slice_followup_ok,
        "chains": slice_chains,
        "blocking_real_issuance_now": False,
        **meta,
    }
    dryrun_report = {
        "report_id": "authorization_preparation_dryrun_report_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "next_phase_candidates": [NEXT_PHASE_GO, NEXT_PHASE_B],
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "authorization_preparation_dryrun_pass": dryrun_pass,
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
            "# Authorization Preparation DryRun Report v1",
            "",
            "Candidate-level dry-run for authorization preparation package. No real authorization or request.",
            "",
            f"Package validation OK: `{authorization_preparation_package_validation_ok}`",
            f"Safety boundary OK: `{real_issuance_safety_boundary_ok}`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "authorization_preparation_dryrun_report": dryrun_report,
        "authorization_preparation_dryrun_report_md": markdown,
        "authorization_preparation_package_validation": package_validation,
        "authorization_precondition_validation": precondition_validation,
        "missing_conditions_routing_validation": routing_validation,
        "real_issuance_safety_boundary_validation": safety_boundary,
        "functional_slice_followup_reference": slice_followup,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
