# -*- coding: utf-8 -*-
"""Luna Midplatform Owner Approval Request Module Governance Closure v1.

Module-level governance closure for the Owner Approval Request candidate chain.
No real execution. No fragmentary phase expansion.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_DOC,
    FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF,
    MODULE_FIRST_CADENCE_RULE_DOC,
    MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
    REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
    RESULT_FIRST_MODULE_ENGINEERING_RULE_DOC,
    RESULT_FIRST_MODULE_ENGINEERING_RULE_REF,
    TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_DOC,
    TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_REF,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_STAGE_ADDITIONS,
    OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_STAGE_TERM_OVERRIDES,
    OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_WHITELIST_FILES,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
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
from capabilities.midplatform.task_manager_owner_approval_request_functional_slice_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_FUNCTIONAL_SLICE_DRYRUN_ROOT,
    FINAL_DECISION_GO as FUNCTIONAL_SLICE_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as FUNCTIONAL_SLICE_DRYRUN_NEXT_PHASE,
    SLICE_DRYRUN_ARTIFACT_BY_ID,
)
from capabilities.midplatform.task_manager_owner_approval_request_governance_gate_integrated_implementation_v1 import (
    FUNCTIONAL_SLICE_CHAINS,
    SELECTED_ROUTE,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Governance-Closure-v1-001"
SCOPE = "midplatform_task_manager_owner_approval_request_module_governance_closure_only"
SOURCE_CHAIN = "midplatform_task_manager_owner_approval_request_module_governance_closure_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_READY_FOR_MIDPLATFORM_HANDOFF_OR_REAL_ISSUANCE_PREAUTH_PLANNING"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_BLOCKED_BY_FUNCTIONAL_SLICE_DRYRUN_GAP"
)
FINAL_DECISION_CLOSURE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_BLOCKED_BY_CLOSURE_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_A = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001"
NEXT_PHASE_B = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Real-Issuance-PreAuthorization-Planning-v1-001"
)
NEXT_PHASE_C = "Phase-Midplatform-Task-Manager-Foundation-Closure-Roadmap-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Governance-Closure-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_governance_closure_v1_smoke_v0"
)
CLOSURE_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_module_governance_closure_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_governance_closure_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_governance_closure_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/owner_approval_request_governance_gate_template_lineage_v1.py"

CLOSURE_ARTIFACTS: Tuple[str, ...] = (
    "module_governance_closure_report_v1.json",
    "module_governance_closure_report_v1.md",
    "module_result_closure_v1.json",
    "functional_slice_closure_summary_v1.json",
    "governance_rule_closure_v1.json",
    "non_execution_closure_v1.json",
    "real_execution_preconditions_v1.json",
    "module_closure_decision_v1.json",
    "module_closure_handoff_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

CURRENT_MODULE_STATE = "governance_candidate_chain_closed"
REAL_EXECUTION_STATE = "not_authorized"

FORBIDDEN_ROUTES: Tuple[str, ...] = (
    "real_request_issued",
    "authorization_request_created",
    "record_created",
    "grant_issued",
    "foundation_frozen",
    "runtime_enabled",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_functional_slice_dryrun_go",
    "module_result_closure_complete",
    "functional_slice_closure_summary_complete",
    "governance_rule_closure_complete",
    "non_execution_closure_complete",
    "real_execution_preconditions_complete",
    "module_closure_decision_complete",
    "module_closure_handoff_complete",
    "current_module_state_governance_candidate_chain_closed",
    "real_execution_not_authorized",
    "non_execution_boundary_ok",
    "no_fragmentary_phase_expansion",
    "file_size_governance_review_ok",
    "next_phase_readiness_ok",
)

SLICE_RESULT_LABELS: Dict[str, str] = {
    "owner_approval_request_candidate_lifecycle": (
        "Owner approval request candidate lifecycle achieved candidate-level result"
    ),
    "authorization_preparation_lifecycle": (
        "Authorization preparation lifecycle achieved candidate-level result"
    ),
    "record_approval_ack_evidence_closure_lifecycle": (
        "Record/approval/ack/evidence closure lifecycle achieved candidate-level result"
    ),
    "absence_and_rollback_safety_lifecycle": (
        "Absence and rollback safety lifecycle achieved candidate-level result"
    ),
}


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
        "module_governance_closure_only": True,
        "no_fragmentary_phase_expansion": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "functional_slice_dryrun_root": str(upstream),
    }


def run_task_manager_owner_approval_request_module_governance_closure_v1(
    *,
    functional_slice_dryrun_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(functional_slice_dryrun_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    dryrun_summary = _read_json(upstream / "summary.json")
    dryrun_verifier = _read_json(upstream / "verifier_report.json")
    dryrun_file_size = _read_json(upstream / "file_size_governance_review_v1.json")
    result_summary = _read_json(upstream / "functional_slice_result_summary_v1.json")
    slice_dryruns = {sid: _read_json(upstream / SLICE_DRYRUN_ARTIFACT_BY_ID[sid]) for sid in FUNCTIONAL_SLICE_CHAINS}

    plan_root = Path(dryrun_summary.get("functional_slice_planning_root") or "").expanduser()
    auth_dryrun_root = Path(
        _read_json(plan_root / "summary.json").get("authorization_preparation_dryrun_root") or ""
    ).expanduser()
    impl_root = Path(
        _read_json(auth_dryrun_root / "summary.json").get("integrated_implementation_root") or ""
    ).expanduser()
    checklist = _read_json(impl_root / "real_issuance_precondition_checklist_v1.json") if impl_root.is_dir() else {}
    checklist_items = {i.get("item_id"): i for i in checklist.get("items") or []}

    prior_functional_slice_dryrun_go = (
        dryrun_summary.get("final_decision") == FUNCTIONAL_SLICE_DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == FUNCTIONAL_SLICE_DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 260
        and dryrun_summary.get("functional_slice_dryrun_pass") is True
        and dryrun_summary.get("all_slice_primary_results_reached") is True
        and dryrun_summary.get("forbidden_state_transitions_absent") is True
        and dryrun_summary.get("functional_slice_real_execution_absent") is True
        and dryrun_summary.get("no_fragmentary_phase_expansion") is True
        and dryrun_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_functional_slice_dryrun_go:
        issues.append("functional_slice_dryrun_not_go")

    slice_dryrun_ok = {
        sid: dryrun_summary.get(f"{sid}_dryrun_ok") is True
        and slice_dryruns[sid].get(f"{sid}_dryrun_ok") is True
        for sid in FUNCTIONAL_SLICE_CHAINS
    }
    if not all(slice_dryrun_ok.values()):
        issues.append("slice_dryrun_not_all_ok")

    absence = {key: dryrun_summary.get(key) is True for key in ABSENCE_KEYS}
    runtime_forbidden_violation = any(dryrun_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_functional_slice_dryrun_go
        and dryrun_summary.get("non_execution_boundary_ok") is True
        and dryrun_summary.get("real_request_issuance_authorized") is False
        and all(absence.values())
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    slice_results = [
        {
            "slice_id": sid,
            "candidate_level_result_achieved": slice_dryrun_ok[sid],
            "primary_result_reached": slice_dryruns[sid].get("primary_result_reached") is True,
            "dryrun_ok": slice_dryrun_ok[sid],
            "result_label": SLICE_RESULT_LABELS[sid],
        }
        for sid in FUNCTIONAL_SLICE_CHAINS
    ]
    module_result_closure_complete = prior_functional_slice_dryrun_go and all(slice_dryrun_ok.values())
    functional_slice_closure_summary_complete = (
        module_result_closure_complete
        and result_summary.get("all_slice_primary_results_reached") is True
        and len(slice_results) == len(FUNCTIONAL_SLICE_CHAINS)
    )

    governance_rule_closure_complete = prior_functional_slice_dryrun_go
    non_execution_closure_complete = non_execution_boundary_ok and all(absence.values())

    preconditions = [
        {
            "precondition_id": "owner_operator_explicit_approval",
            "status": "not_satisfied",
            "level": "blocking_before_real_issuance",
            "satisfied": checklist_items.get("owner_operator_explicit_approval", {}).get("satisfied") is False,
        },
        {
            "precondition_id": "authorization_request_readiness",
            "status": "not_converted_to_real_request",
            "level": "blocking_before_real_issuance",
            "satisfied": checklist_items.get("authorization_request_readiness", {}).get("satisfied") is False,
        },
        {
            "precondition_id": "record_evidence_readiness",
            "status": "candidate_level_readiness",
            "level": "candidate_only",
            "satisfied": (
                checklist_items.get("record_readiness", {}).get("satisfied") is False
                and checklist_items.get("evidence_readiness", {}).get("satisfied") is False
            ),
        },
        {
            "precondition_id": "rollback_expiry_revocation_readiness",
            "status": "reference_candidate",
            "level": "reference_only",
            "satisfied": checklist_items.get("rollback_expiry_revocation_readiness", {}).get("satisfied") is False,
        },
        {
            "precondition_id": "runtime_boundary_readiness",
            "status": "future_runtime_debt",
            "level": "deferred",
            "satisfied": checklist_items.get("runtime_boundary_readiness", {}).get("satisfied") is False,
        },
    ]
    real_execution_preconditions_complete = (
        prior_functional_slice_dryrun_go
        and checklist.get("real_issuance_precondition_checklist_complete") is True
        and all(p.get("satisfied") for p in preconditions[:2])
        and preconditions[2].get("status") == "candidate_level_readiness"
        and preconditions[4].get("status") == "future_runtime_debt"
    )
    if not real_execution_preconditions_complete:
        issues.append("real_execution_preconditions_gap")

    current_module_state_governance_candidate_chain_closed = (
        module_result_closure_complete and CURRENT_MODULE_STATE == "governance_candidate_chain_closed"
    )
    real_execution_not_authorized = (
        dryrun_summary.get("real_request_issuance_authorized") is False and REAL_EXECUTION_STATE == "not_authorized"
    )

    allowed_routes = [
        {"route_id": "A", "phase_id": NEXT_PHASE_A, "intent": "Module handoff to broader midplatform"},
        {"route_id": "B", "phase_id": NEXT_PHASE_B, "intent": "Real issuance pre-authorization planning"},
        {"route_id": "C", "phase_id": NEXT_PHASE_C, "intent": "Return to broader midplatform task manager closure roadmap"},
    ]
    module_closure_decision_complete = (
        current_module_state_governance_candidate_chain_closed
        and real_execution_not_authorized
        and len(allowed_routes) == 3
        and module_result_closure_complete
    )
    module_closure_handoff_complete = module_closure_decision_complete and non_execution_closure_complete

    template_lineage = build_template_lineage(
        base_phase="Owner-Approval-Request-Functional-Slice-DryRun-v1-001",
        base_capability=OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_WHITELIST_FILES[0],
        base_runner=OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_WHITELIST_FILES[1],
        base_verifier=OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_WHITELIST_FILES[2],
        base_go_no_go_pack=CLOSURE_GO_NO_GO_PACK,
        stage_phase="Owner-Approval-Request-Module-Governance-Closure-v1-001",
        stage_term_overrides=OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_STAGE_TERM_OVERRIDES,
        stage_additions=OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_STAGE_ADDITIONS,
        template_files=OWNER_APPROVAL_REQUEST_MODULE_GOVERNANCE_CLOSURE_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Owner-Approval-Request-Functional-Slice-DryRun-v1-001",
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
        previous_interruption_type=dryrun_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=dryrun_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=dryrun_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    closure_pass = (
        prior_functional_slice_dryrun_go
        and module_result_closure_complete
        and functional_slice_closure_summary_complete
        and governance_rule_closure_complete
        and non_execution_closure_complete
        and real_execution_preconditions_complete
        and module_closure_decision_complete
        and module_closure_handoff_complete
        and current_module_state_governance_candidate_chain_closed
        and real_execution_not_authorized
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase_readiness_ok = closure_pass

    if not prior_functional_slice_dryrun_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not module_closure_decision_complete:
        final_decision = FINAL_DECISION_CLOSURE
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_functional_slice_dryrun_go": prior_functional_slice_dryrun_go,
        "module_result_closure_complete": module_result_closure_complete,
        "functional_slice_closure_summary_complete": functional_slice_closure_summary_complete,
        "governance_rule_closure_complete": governance_rule_closure_complete,
        "non_execution_closure_complete": non_execution_closure_complete,
        "real_execution_preconditions_complete": real_execution_preconditions_complete,
        "module_closure_decision_complete": module_closure_decision_complete,
        "module_closure_handoff_complete": module_closure_handoff_complete,
        "current_module_state_governance_candidate_chain_closed": current_module_state_governance_candidate_chain_closed,
        "real_execution_not_authorized": real_execution_not_authorized,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "module_governance_closure_pass": closure_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "selected_route": SELECTED_ROUTE,
        "current_module_state": CURRENT_MODULE_STATE,
        "real_execution_state": REAL_EXECUTION_STATE,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    next_phase = NEXT_PHASE_A if closure_pass else NEXT_PHASE_HOLD
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(dryrun_summary.get("chain_trace_nodes") or [])
            + ["owner_approval_request_module_governance_closure"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    module_result_closure = {
        "closure_id": "module_result_closure_v1",
        "module_result_closure_complete": module_result_closure_complete,
        "module_governance_question_1": "Owner Approval Request governance chain achieved candidate-level results across 4 functional slices.",
        "slice_results": slice_results,
        "selected_route": SELECTED_ROUTE,
        **meta,
    }
    functional_slice_closure_summary = {
        "summary_id": "functional_slice_closure_summary_v1",
        "functional_slice_closure_summary_complete": functional_slice_closure_summary_complete,
        "slice_count": len(FUNCTIONAL_SLICE_CHAINS),
        "all_slices_candidate_level_closed": all(slice_dryrun_ok.values()),
        "all_slice_primary_results_reached": result_summary.get("all_slice_primary_results_reached") is True,
        "forbidden_state_transitions_absent": dryrun_summary.get("forbidden_state_transitions_absent") is True,
        "functional_slice_real_execution_absent": dryrun_summary.get("functional_slice_real_execution_absent") is True,
        "slices": slice_results,
        **meta,
    }
    governance_rule_closure = {
        "closure_id": "governance_rule_closure_v1",
        "governance_rule_closure_complete": governance_rule_closure_complete,
        "result_first_module_engineering_rule_ref": RESULT_FIRST_MODULE_ENGINEERING_RULE_REF,
        "result_first_module_engineering_rule_doc": RESULT_FIRST_MODULE_ENGINEERING_RULE_DOC,
        "top_level_objective_priority_rule_ref": TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_REF,
        "top_level_objective_priority_rule_doc": TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_DOC,
        "module_first_development_verification_cadence_rule_ref": MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
        "module_first_cadence_rule_doc": MODULE_FIRST_CADENCE_RULE_DOC,
        "reuse_first_protocol_engineering_rule_ref": REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
        "file_size_module_split_governance_rule_ref": FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF,
        "file_size_module_split_governance_rule_doc": FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_DOC,
        "lightweight_protocol_refs_only": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "no_fragmentary_phase_expansion": True,
        **meta,
    }
    non_execution_closure = {
        "closure_id": "non_execution_closure_v1",
        "non_execution_closure_complete": non_execution_closure_complete,
        "module_governance_question_3": "Real execution capabilities remain unauthorized and absent.",
        "absence_matrix": absence,
        "real_request_issuance_authorized": False,
        "forbidden_routes": list(FORBIDDEN_ROUTES),
        **meta,
    }
    real_execution_preconditions_doc = {
        "preconditions_id": "real_execution_preconditions_v1",
        "real_execution_preconditions_complete": real_execution_preconditions_complete,
        "module_governance_question_4": "Subsequent routes require explicit authorization before real execution.",
        "preconditions": preconditions,
        "real_execution_not_authorized": True,
        **meta,
    }
    module_closure_decision = {
        "decision_id": "module_closure_decision_v1",
        "module_closure_decision_complete": module_closure_decision_complete,
        "current_module_state": CURRENT_MODULE_STATE,
        "real_execution_state": REAL_EXECUTION_STATE,
        "allowed_routes": allowed_routes,
        "forbidden_routes": list(FORBIDDEN_ROUTES),
        "closure_statement": "Owner Approval Request governance candidate chain is closed; no further fragmentary phases on this chain.",
        **meta,
    }
    module_closure_handoff = {
        "handoff_id": "module_closure_handoff_v1",
        "module_closure_handoff_complete": module_closure_handoff_complete,
        "module_governance_question_2": "Candidate-level closure achieved for all 4 functional slices.",
        "handoff_status": "governance_ready",
        "recommended_next_phase": next_phase,
        "next_phase_candidates": [NEXT_PHASE_A, NEXT_PHASE_B, NEXT_PHASE_C],
        "chain_closed": True,
        "do_not_extend_fragmentary_phases": True,
        "integrated_implementation_root": str(impl_root) if impl_root.is_dir() else None,
        "functional_slice_dryrun_root": str(upstream),
        **meta,
    }
    closure_report = {
        "report_id": "module_governance_closure_report_v1",
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "next_phase_candidates": [NEXT_PHASE_A, NEXT_PHASE_B, NEXT_PHASE_C],
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "module_governance_closure_pass": closure_pass,
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
            "# Module Governance Closure Report v1",
            "",
            "Owner Approval Request governance chain module-level closure. No real execution.",
            "",
            f"Current module state: `{CURRENT_MODULE_STATE}`",
            f"Real execution state: `{REAL_EXECUTION_STATE}`",
            f"Module result closure complete: `{module_result_closure_complete}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
        ]
    )
    return {
        "module_governance_closure_report": closure_report,
        "module_governance_closure_report_md": markdown,
        "module_result_closure": module_result_closure,
        "functional_slice_closure_summary": functional_slice_closure_summary,
        "governance_rule_closure": governance_rule_closure,
        "non_execution_closure": non_execution_closure,
        "real_execution_preconditions": real_execution_preconditions_doc,
        "module_closure_decision": module_closure_decision,
        "module_closure_handoff": module_closure_handoff,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
