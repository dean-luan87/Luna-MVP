# -*- coding: utf-8 -*-
"""Luna Midplatform Owner Approval Request Functional Slice DryRun v1.

Single-phase module-level dryrun for all 4 functional slices. No real execution.
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
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_STAGE_ADDITIONS,
    OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_STAGE_TERM_OVERRIDES,
    OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_WHITELIST_FILES,
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
from capabilities.midplatform.task_manager_owner_approval_request_functional_slice_dryrun_evaluators_v1 import (
    SLICE_EVALUATORS,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_v1 import (
    FINAL_DECISION_GO as INTEGRATED_IMPLEMENTATION_FINAL_GO,
    FUNCTIONAL_SLICE_CHAINS,
    SELECTED_ROUTE,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_level_functional_slice_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FUNCTIONAL_SLICE_PLANNING_ROOT,
    FINAL_DECISION_GO as FUNCTIONAL_SLICE_PLANNING_FINAL_GO,
    NEXT_PHASE_A as FUNCTIONAL_SLICE_PLANNING_NEXT_PHASE,
    SLICE_ARTIFACT_BY_ID,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Functional-Slice-DryRun-v1-001"
SCOPE = "midplatform_task_manager_owner_approval_request_functional_slice_dryrun_only"
SOURCE_CHAIN = "midplatform_task_manager_owner_approval_request_functional_slice_dryrun_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_READY_FOR_MODULE_GOVERNANCE_CLOSURE"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_BLOCKED_BY_FUNCTIONAL_SLICE_PLANNING_GAP"
)
FINAL_DECISION_SLICE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_BLOCKED_BY_SLICE_DRYRUN_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Governance-Closure-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Functional-Slice-DryRun-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_functional_slice_dryrun_v1_smoke_v0"
)
DRYRUN_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_functional_slice_dryrun_v1.py",
    "capabilities/midplatform/task_manager_owner_approval_request_functional_slice_dryrun_evaluators_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_functional_slice_dryrun_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_functional_slice_dryrun_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/owner_approval_request_governance_gate_template_lineage_v1.py"

DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "functional_slice_dryrun_report_v1.json",
    "functional_slice_dryrun_report_v1.md",
    "functional_slice_dryrun_registry_v1.json",
    "owner_approval_request_candidate_lifecycle_dryrun_v1.json",
    "authorization_preparation_lifecycle_dryrun_v1.json",
    "record_approval_ack_evidence_closure_lifecycle_dryrun_v1.json",
    "absence_and_rollback_safety_lifecycle_dryrun_v1.json",
    "functional_slice_result_summary_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

SLICE_DRYRUN_ARTIFACT_BY_ID: Dict[str, str] = {
    "owner_approval_request_candidate_lifecycle": "owner_approval_request_candidate_lifecycle_dryrun_v1.json",
    "authorization_preparation_lifecycle": "authorization_preparation_lifecycle_dryrun_v1.json",
    "record_approval_ack_evidence_closure_lifecycle": "record_approval_ack_evidence_closure_lifecycle_dryrun_v1.json",
    "absence_and_rollback_safety_lifecycle": "absence_and_rollback_safety_lifecycle_dryrun_v1.json",
}

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_functional_slice_planning_go",
    "functional_slice_dryrun_registry_complete",
    "owner_approval_request_candidate_lifecycle_dryrun_ok",
    "authorization_preparation_lifecycle_dryrun_ok",
    "record_approval_ack_evidence_closure_lifecycle_dryrun_ok",
    "absence_and_rollback_safety_lifecycle_dryrun_ok",
    "all_slice_primary_results_reached",
    "forbidden_state_transitions_absent",
    "functional_slice_real_execution_absent",
    "non_execution_boundary_ok",
    "no_fragmentary_phase_expansion",
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
        "functional_slice_dryrun_only": True,
        "single_phase_all_slices": True,
        "no_fragmentary_phase_expansion": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "functional_slice_planning_root": str(upstream),
    }


def run_task_manager_owner_approval_request_functional_slice_dryrun_v1(
    *,
    functional_slice_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(functional_slice_planning_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    plan_summary = _read_json(upstream / "summary.json")
    plan_verifier = _read_json(upstream / "verifier_report.json")
    plan_file_size = _read_json(upstream / "file_size_governance_review_v1.json")
    slice_plans = {sid: _read_json(upstream / SLICE_ARTIFACT_BY_ID[sid]) for sid in FUNCTIONAL_SLICE_CHAINS}

    dryrun_root = Path(plan_summary.get("authorization_preparation_dryrun_root") or "").expanduser()
    dryrun_summary = _read_json(dryrun_root / "summary.json") if dryrun_root.is_dir() else {}
    impl_root = Path(dryrun_summary.get("integrated_implementation_root") or "").expanduser()
    impl_summary = _read_json(impl_root / "summary.json") if impl_root.is_dir() else {}
    auth_package = _read_json(impl_root / "issuance_authorization_preparation_package_v1.json") if impl_root.is_dir() else {}
    routing = _read_json(impl_root / "missing_conditions_routing_v1.json") if impl_root.is_dir() else {}
    checklist = _read_json(impl_root / "real_issuance_precondition_checklist_v1.json") if impl_root.is_dir() else {}
    closure_boundary = (
        _read_json(impl_root / "record_approval_ack_evidence_closure_boundary_v1.json") if impl_root.is_dir() else {}
    )

    prior_functional_slice_planning_go = (
        plan_summary.get("final_decision") == FUNCTIONAL_SLICE_PLANNING_FINAL_GO
        and plan_summary.get("recommended_next_phase") == FUNCTIONAL_SLICE_PLANNING_NEXT_PHASE
        and plan_verifier.get("verifier") == "GO"
        and int(plan_verifier.get("passed_checks", 0)) >= 260
        and plan_summary.get("functional_slice_planning_pass") is True
        and plan_summary.get("functional_slice_plan_complete") is True
        and plan_summary.get("no_fragmentary_phase_expansion") is True
        and plan_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_functional_slice_planning_go:
        issues.append("functional_slice_planning_not_go")

    prior_integrated_implementation_go = (
        prior_functional_slice_planning_go
        and plan_summary.get("prior_integrated_implementation_go") is True
        and impl_summary.get("final_decision") == INTEGRATED_IMPLEMENTATION_FINAL_GO
    )
    prior_authorization_preparation_dryrun_go = (
        prior_functional_slice_planning_go and plan_summary.get("prior_authorization_preparation_dryrun_go") is True
    )

    absence = {key: plan_summary.get(key) is True for key in ABSENCE_KEYS}
    runtime_forbidden_violation = any(plan_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_functional_slice_planning_go
        and plan_summary.get("non_execution_boundary_ok") is True
        and plan_summary.get("real_request_issuance_authorized") is False
        and all(absence.values())
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    ctx: Dict[str, Any] = {
        "prior_functional_slice_planning_go": prior_functional_slice_planning_go,
        "prior_integrated_implementation_go": prior_integrated_implementation_go,
        "prior_authorization_preparation_dryrun_go": prior_authorization_preparation_dryrun_go,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "real_request_issuance_authorized": False,
        "runtime_forbidden_violation": runtime_forbidden_violation,
        "auth_package": auth_package,
        "routing": routing,
        "checklist": checklist,
        "closure_boundary": closure_boundary,
        "absence": absence,
        **absence,
    }

    dryrun_results: Dict[str, Dict[str, Any]] = {}
    for sid in FUNCTIONAL_SLICE_CHAINS:
        plan_doc = slice_plans[sid]
        if not plan_doc or plan_doc.get("execution_allowed") is not False:
            issues.append(f"plan_not_ready:{sid}")
        evaluator = SLICE_EVALUATORS[sid]
        result = evaluator(plan_doc, ctx=ctx, meta=meta)
        dryrun_results[sid] = result
        if not result.get(f"{sid}_dryrun_ok"):
            issues.append(f"slice_dryrun_failed:{sid}")

    dryrun_ok_flags = {sid: dryrun_results[sid].get(f"{sid}_dryrun_ok") is True for sid in FUNCTIONAL_SLICE_CHAINS}
    all_slice_primary_results_reached = all(dryrun_results[sid].get("primary_result_reached") for sid in FUNCTIONAL_SLICE_CHAINS)
    forbidden_state_transitions_absent = all(
        dryrun_results[sid].get("forbidden_state_transitions_absent") for sid in FUNCTIONAL_SLICE_CHAINS
    )
    functional_slice_real_execution_absent = all(
        dryrun_results[sid].get("real_execution") is False and dryrun_results[sid].get("test_executed") is True
        for sid in FUNCTIONAL_SLICE_CHAINS
    )
    functional_slice_dryrun_registry_complete = all(dryrun_ok_flags.values())

    template_lineage = build_template_lineage(
        base_phase="Owner-Approval-Request-Module-Level-Functional-Slice-Planning-v1-001",
        base_capability=OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_WHITELIST_FILES[0],
        base_runner=OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_WHITELIST_FILES[1],
        base_verifier=OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_WHITELIST_FILES[2],
        base_go_no_go_pack=DRYRUN_GO_NO_GO_PACK,
        stage_phase="Owner-Approval-Request-Functional-Slice-DryRun-v1-001",
        stage_term_overrides=OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_STAGE_TERM_OVERRIDES,
        stage_additions=OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_STAGE_ADDITIONS,
        template_files=OWNER_APPROVAL_REQUEST_FUNCTIONAL_SLICE_DRYRUN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Owner-Approval-Request-Module-Level-Functional-Slice-Planning-v1-001",
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
        previous_interruption_type=plan_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=plan_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=plan_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    dryrun_pass = (
        prior_functional_slice_planning_go
        and functional_slice_dryrun_registry_complete
        and all_slice_primary_results_reached
        and forbidden_state_transitions_absent
        and functional_slice_real_execution_absent
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase_readiness_ok = dryrun_pass

    if not prior_functional_slice_planning_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not functional_slice_dryrun_registry_complete:
        final_decision = FINAL_DECISION_SLICE
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_functional_slice_planning_go": prior_functional_slice_planning_go,
        "functional_slice_dryrun_registry_complete": functional_slice_dryrun_registry_complete,
        "owner_approval_request_candidate_lifecycle_dryrun_ok": dryrun_ok_flags[
            "owner_approval_request_candidate_lifecycle"
        ],
        "authorization_preparation_lifecycle_dryrun_ok": dryrun_ok_flags["authorization_preparation_lifecycle"],
        "record_approval_ack_evidence_closure_lifecycle_dryrun_ok": dryrun_ok_flags[
            "record_approval_ack_evidence_closure_lifecycle"
        ],
        "absence_and_rollback_safety_lifecycle_dryrun_ok": dryrun_ok_flags["absence_and_rollback_safety_lifecycle"],
        "all_slice_primary_results_reached": all_slice_primary_results_reached,
        "forbidden_state_transitions_absent": forbidden_state_transitions_absent,
        "functional_slice_real_execution_absent": functional_slice_real_execution_absent,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "functional_slice_dryrun_pass": dryrun_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "selected_route": SELECTED_ROUTE,
        "result_first_module_engineering_rule_ref": RESULT_FIRST_MODULE_ENGINEERING_RULE_REF,
        "module_first_development_verification_cadence_rule_ref": MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    next_phase = NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(plan_summary.get("chain_trace_nodes") or []) + ["owner_approval_request_functional_slice_dryrun"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    registry = {
        "registry_id": "functional_slice_dryrun_registry_v1",
        "functional_slice_dryrun_registry_complete": functional_slice_dryrun_registry_complete,
        "single_phase_all_slices": True,
        "slices": [
            {
                "slice_id": sid,
                "artifact": SLICE_DRYRUN_ARTIFACT_BY_ID[sid],
                "dryrun_ok": dryrun_ok_flags[sid],
                "test_executed": True,
                "real_execution": False,
                "execution_allowed": False,
            }
            for sid in FUNCTIONAL_SLICE_CHAINS
        ],
        **meta,
    }
    result_summary = {
        "summary_id": "functional_slice_result_summary_v1",
        "slice_count": len(FUNCTIONAL_SLICE_CHAINS),
        "all_slice_primary_results_reached": all_slice_primary_results_reached,
        "forbidden_state_transitions_absent": forbidden_state_transitions_absent,
        "functional_slice_real_execution_absent": functional_slice_real_execution_absent,
        "slice_results": [
            {
                "slice_id": sid,
                "primary_result_reached": dryrun_results[sid].get("primary_result_reached"),
                "dryrun_ok": dryrun_ok_flags[sid],
            }
            for sid in FUNCTIONAL_SLICE_CHAINS
        ],
        **meta,
    }
    dryrun_report = {
        "report_id": "functional_slice_dryrun_report_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "functional_slice_dryrun_pass": dryrun_pass,
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
            "# Functional Slice DryRun Report v1",
            "",
            "Single-phase module-level dryrun for 4 functional slices. No real execution.",
            "",
            f"Selected route: `{SELECTED_ROUTE}`",
            f"All primary results reached: `{all_slice_primary_results_reached}`",
            f"Slice dryrun pass: `{dryrun_pass}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
        ]
    )
    return {
        "functional_slice_dryrun_report": dryrun_report,
        "functional_slice_dryrun_report_md": markdown,
        "functional_slice_dryrun_registry": registry,
        "owner_approval_request_candidate_lifecycle_dryrun": dryrun_results[
            "owner_approval_request_candidate_lifecycle"
        ],
        "authorization_preparation_lifecycle_dryrun": dryrun_results["authorization_preparation_lifecycle"],
        "record_approval_ack_evidence_closure_lifecycle_dryrun": dryrun_results[
            "record_approval_ack_evidence_closure_lifecycle"
        ],
        "absence_and_rollback_safety_lifecycle_dryrun": dryrun_results["absence_and_rollback_safety_lifecycle"],
        "functional_slice_result_summary": result_summary,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
