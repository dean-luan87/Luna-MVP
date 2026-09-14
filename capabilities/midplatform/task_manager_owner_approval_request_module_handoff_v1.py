# -*- coding: utf-8 -*-
"""Luna Midplatform Owner Approval Request Module Handoff v1.

Hand completed governance chain back to broader Task Manager / Midplatform mainline.
No sub-chain extension. No real execution.
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
    OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_STAGE_ADDITIONS,
    OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_STAGE_TERM_OVERRIDES,
    OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_WHITELIST_FILES,
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
    FUNCTIONAL_SLICE_CHAINS,
    SELECTED_ROUTE,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_governance_closure_v1 import (
    CURRENT_MODULE_STATE,
    DEFAULT_OUTPUT as DEFAULT_MODULE_GOVERNANCE_CLOSURE_ROOT,
    FINAL_DECISION_GO as MODULE_GOVERNANCE_CLOSURE_FINAL_GO,
    NEXT_PHASE_A as MODULE_GOVERNANCE_CLOSURE_NEXT_PHASE,
    REAL_EXECUTION_STATE,
)

PHASE_ID = "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-v1-001"
SCOPE = "midplatform_task_manager_owner_approval_request_module_handoff_only"
SOURCE_CHAIN = "midplatform_task_manager_owner_approval_request_module_handoff_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_READY_FOR_BROADER_MIDPLATFORM_TASK_MANAGER_CLOSURE_ROADMAP"
)
FINAL_DECISION_UPSTREAM = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_BLOCKED_BY_MODULE_GOVERNANCE_CLOSURE_GAP"
)
FINAL_DECISION_HANDOFF = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_BLOCKED_BY_HANDOFF_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = "Phase-Midplatform-Task-Manager-Broader-Midplatform-Closure-Roadmap-v1-001"
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Owner-Approval-Request-Module-Handoff-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "task_manager_owner_approval_request_module_handoff_v1_smoke_v0"
)
HANDOFF_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_TASK_MANAGER_OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_owner_approval_request_module_handoff_v1.py",
    "tools/evaluation/midplatform/run_task_manager_owner_approval_request_module_handoff_v1.py",
    "tools/evaluation/midplatform/verify_task_manager_owner_approval_request_module_handoff_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/owner_approval_request_governance_gate_template_lineage_v1.py"

HANDOFF_ARTIFACTS: Tuple[str, ...] = (
    "owner_approval_request_module_handoff_report_v1.json",
    "owner_approval_request_module_handoff_report_v1.md",
    "owner_approval_request_module_status_summary_v1.json",
    "owner_approval_request_midplatform_integration_position_v1.json",
    "owner_approval_request_handoff_boundary_v1.json",
    "midplatform_mainline_return_plan_v1.json",
    "future_test_strategy_v1.json",
    "governance_debt_and_future_runtime_handoff_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

MIDPLATFORM_MAINLINE_ITEMS: Tuple[Dict[str, str], ...] = (
    {"item_id": "task_manager_skeleton_foundation_handoff", "status": "in_progress"},
    {"item_id": "protocol_registry_input_output_traceability", "status": "active"},
    {"item_id": "governance_constraints", "status": "active"},
    {"item_id": "file_size_governance", "status": "active"},
    {"item_id": "module_first_result_first_rules", "status": "active"},
    {"item_id": "owner_approval_request_closed_module", "status": "governance_ready_handoff"},
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_module_governance_closure_go",
    "module_handoff_report_complete",
    "module_status_summary_complete",
    "midplatform_integration_position_complete",
    "handoff_boundary_complete",
    "midplatform_mainline_return_plan_complete",
    "future_test_strategy_complete",
    "governance_debt_future_runtime_handoff_complete",
    "real_execution_not_authorized",
    "owner_approval_request_chain_not_extended",
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
        "module_handoff_only": True,
        "return_to_midplatform_mainline": True,
        "no_fragmentary_phase_expansion": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "module_governance_closure_root": str(upstream),
    }


def run_task_manager_owner_approval_request_module_handoff_v1(
    *,
    module_governance_closure_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    upstream = Path(module_governance_closure_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, upstream)
    issues: List[str] = []

    closure_summary = _read_json(upstream / "summary.json")
    closure_verifier = _read_json(upstream / "verifier_report.json")
    closure_handoff = _read_json(upstream / "module_closure_handoff_v1.json")
    closure_file_size = _read_json(upstream / "file_size_governance_review_v1.json")
    slice_closure = _read_json(upstream / "functional_slice_closure_summary_v1.json")

    prior_module_governance_closure_go = (
        closure_summary.get("final_decision") == MODULE_GOVERNANCE_CLOSURE_FINAL_GO
        and closure_summary.get("recommended_next_phase") == MODULE_GOVERNANCE_CLOSURE_NEXT_PHASE
        and closure_verifier.get("verifier") == "GO"
        and int(closure_verifier.get("passed_checks", 0)) >= 260
        and closure_summary.get("module_governance_closure_pass") is True
        and closure_handoff.get("chain_closed") is True
        and closure_handoff.get("do_not_extend_fragmentary_phases") is True
        and closure_summary.get("current_module_state") == CURRENT_MODULE_STATE
        and closure_summary.get("real_execution_state") == REAL_EXECUTION_STATE
        and closure_summary.get("no_fragmentary_phase_expansion") is True
        and closure_summary.get("real_request_issuance_authorized") is False
    )
    if not prior_module_governance_closure_go:
        issues.append("module_governance_closure_not_go")

    absence = {key: closure_summary.get(key) is True for key in ABSENCE_KEYS}
    record_creation_absent = (
        closure_summary.get("request_record_absent") is True
        and closure_summary.get("approval_record_absent") is True
        and closure_summary.get("ack_record_absent") is True
        and closure_summary.get("evidence_bound_record_absent") is True
    )
    runtime_forbidden_violation = any(closure_summary.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
    non_execution_boundary_ok = (
        prior_module_governance_closure_go
        and closure_summary.get("non_execution_boundary_ok") is True
        and closure_summary.get("real_execution_not_authorized") is True
        and all(absence.values())
        and record_creation_absent
        and not runtime_forbidden_violation
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")

    owner_approval_request_chain_not_extended = (
        prior_module_governance_closure_go
        and closure_handoff.get("chain_closed") is True
        and closure_handoff.get("do_not_extend_fragmentary_phases") is True
    )
    real_execution_not_authorized = closure_summary.get("real_request_issuance_authorized") is False

    module_status_summary_complete = (
        prior_module_governance_closure_go
        and slice_closure.get("all_slices_candidate_level_closed") is True
        and len(slice_closure.get("slices") or []) == len(FUNCTIONAL_SLICE_CHAINS)
    )
    midplatform_integration_position_complete = prior_module_governance_closure_go
    handoff_boundary_complete = non_execution_boundary_ok and record_creation_absent
    midplatform_mainline_return_plan_complete = prior_module_governance_closure_go
    future_test_strategy_complete = prior_module_governance_closure_go
    governance_debt_future_runtime_handoff_complete = prior_module_governance_closure_go

    module_handoff_report_complete = (
        module_status_summary_complete
        and midplatform_integration_position_complete
        and handoff_boundary_complete
        and midplatform_mainline_return_plan_complete
        and future_test_strategy_complete
        and governance_debt_future_runtime_handoff_complete
    )
    if not module_handoff_report_complete:
        issues.append("handoff_artifact_gap")

    template_lineage = build_template_lineage(
        base_phase="Owner-Approval-Request-Module-Governance-Closure-v1-001",
        base_capability=OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_WHITELIST_FILES[0],
        base_runner=OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_WHITELIST_FILES[1],
        base_verifier=OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_WHITELIST_FILES[2],
        base_go_no_go_pack=HANDOFF_GO_NO_GO_PACK,
        stage_phase="Owner-Approval-Request-Module-Handoff-v1-001",
        stage_term_overrides=OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_STAGE_TERM_OVERRIDES,
        stage_additions=OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_STAGE_ADDITIONS,
        template_files=OWNER_APPROVAL_REQUEST_MODULE_HANDOFF_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Owner-Approval-Request-Module-Governance-Closure-v1-001",
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
        previous_interruption_type=closure_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=closure_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=closure_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    handoff_pass = (
        prior_module_governance_closure_go
        and module_handoff_report_complete
        and owner_approval_request_chain_not_extended
        and real_execution_not_authorized
        and non_execution_boundary_ok
        and template_lineage.get("template_lineage_ok") is True
        and file_size_governance_review_ok
        and len(issues) == 0
    )
    next_phase_readiness_ok = handoff_pass

    if not prior_module_governance_closure_go:
        final_decision = FINAL_DECISION_UPSTREAM
    elif not all(absence.values()):
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not module_handoff_report_complete:
        final_decision = FINAL_DECISION_HANDOFF
    elif not template_lineage.get("template_lineage_ok"):
        final_decision = FINAL_DECISION_LINEAGE
    else:
        final_decision = FINAL_DECISION_GO

    go_values = {
        "prior_module_governance_closure_go": prior_module_governance_closure_go,
        "module_handoff_report_complete": module_handoff_report_complete,
        "module_status_summary_complete": module_status_summary_complete,
        "midplatform_integration_position_complete": midplatform_integration_position_complete,
        "handoff_boundary_complete": handoff_boundary_complete,
        "midplatform_mainline_return_plan_complete": midplatform_mainline_return_plan_complete,
        "future_test_strategy_complete": future_test_strategy_complete,
        "governance_debt_future_runtime_handoff_complete": governance_debt_future_runtime_handoff_complete,
        "real_execution_not_authorized": real_execution_not_authorized,
        "owner_approval_request_chain_not_extended": owner_approval_request_chain_not_extended,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "no_fragmentary_phase_expansion": True,
        "file_size_governance_review_ok": file_size_governance_review_ok,
        "file_size_governance_review_exists": file_size_governance_review.get("file_size_governance_review_exists") is True,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "module_handoff_pass": handoff_pass,
        "real_request_issuance_authorized": False,
        "authorization_request_absent": True,
        "record_creation_absent": record_creation_absent,
        "current_module_state": CURRENT_MODULE_STATE,
        "real_execution_state": REAL_EXECUTION_STATE,
        "chain_closed": closure_handoff.get("chain_closed") is True,
        "do_not_extend_fragmentary_phases": closure_handoff.get("do_not_extend_fragmentary_phases") is True,
        "selected_route": SELECTED_ROUTE,
        "template_lineage_ok": template_lineage.get("template_lineage_ok") is True,
        "monolithic_file_absent": file_size_governance_review.get("monolithic_file_absent") is True,
        "full_repo_scan_absent": file_size_governance_review.get("full_repo_scan_absent") is True,
        "tmp_eval_out_scan_absent": file_size_governance_review.get("tmp_eval_out_scan_absent") is True,
        "summary_index_first_reading_ok": file_size_governance_review.get("summary_index_first_reading_ok") is True,
        "limited_directory_scan_ok": file_size_governance_review.get("limited_directory_scan_ok") is True,
        **absence,
    }
    next_phase = NEXT_PHASE_GO if handoff_pass else NEXT_PHASE_HOLD
    core_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(closure_summary.get("chain_trace_nodes") or [])
            + ["owner_approval_request_module_handoff"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    module_status_summary = {
        "summary_id": "owner_approval_request_module_status_summary_v1",
        "module_status_summary_complete": module_status_summary_complete,
        "module_id": "task_manager_owner_approval_request",
        "current_module_state": CURRENT_MODULE_STATE,
        "real_execution_state": REAL_EXECUTION_STATE,
        "candidate_level_closure_complete": True,
        "real_execution_not_authorized": True,
        "chain_closed": closure_handoff.get("chain_closed") is True,
        "do_not_extend_fragmentary_phases": True,
        "functional_slices": list(FUNCTIONAL_SLICE_CHAINS),
        "all_slices_candidate_level_closed": slice_closure.get("all_slices_candidate_level_closed") is True,
        "closure_root": str(upstream),
        **meta,
    }
    integration_position = {
        "position_id": "owner_approval_request_midplatform_integration_position_v1",
        "midplatform_integration_position_complete": midplatform_integration_position_complete,
        "module_name": "Task Manager Owner Approval Request",
        "registration_status": "governance_ready_submodule",
        "midplatform_domains": [
            "task_manager",
            "permission",
            "approval",
            "evidence",
            "record_lifecycle",
        ],
        "requires_explicit_authorization_before_runtime": True,
        "handoff_to_mainline": True,
        **meta,
    }
    handoff_boundary = {
        "boundary_id": "owner_approval_request_handoff_boundary_v1",
        "handoff_boundary_complete": handoff_boundary_complete,
        "delivers": ["candidate_level_governance_closure_state"],
        "does_not_deliver": [
            "real_request_issuance",
            "real_authorization_request",
            "record_creation",
            "grant",
            "runtime",
            "module_adapter",
            "whitebox_integration",
        ],
        "record_creation_absent": record_creation_absent,
        "real_request_issuance_authorized": False,
        **absence,
        **meta,
    }
    mainline_return_plan = {
        "plan_id": "midplatform_mainline_return_plan_v1",
        "midplatform_mainline_return_plan_complete": midplatform_mainline_return_plan_complete,
        "recommended_next_phase": NEXT_PHASE_GO,
        "return_to_broader_midplatform": True,
        "do_not_open_real_issuance_preauth_unless_mainline_requires": True,
        "mainline_items": list(MIDPLATFORM_MAINLINE_ITEMS),
        "owner_approval_request_status": "handed_off_governance_ready",
        **meta,
    }
    future_test_strategy = {
        "strategy_id": "future_test_strategy_v1",
        "future_test_strategy_complete": future_test_strategy_complete,
        "no_fragmentary_phase_tests": True,
        "test_layers": [
            "module_level_test",
            "functional_slice_test",
            "midplatform_integration_test",
            "real_execution_preauthorization_gate",
        ],
        "owner_approval_request_slice_dryrun_available_as_input": True,
        "functional_slice_dryrun_root": closure_handoff.get("functional_slice_dryrun_root"),
        **meta,
    }
    governance_debt_handoff = {
        "handoff_id": "governance_debt_and_future_runtime_handoff_v1",
        "governance_debt_future_runtime_handoff_complete": governance_debt_future_runtime_handoff_complete,
        "future_runtime_debt": [
            "runtime_adapter_implementation",
            "whitebox_runtime_integration",
        ],
        "future_routes": [
            "real_request_issuance_preauthorization",
        ],
        "governance_debt_closure": "deferred_to_midplatform_mainline",
        **meta,
    }
    handoff_report = {
        "report_id": "owner_approval_request_module_handoff_report_v1",
        "module_handoff_report_complete": module_handoff_report_complete,
        **go_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "module_handoff_pass": handoff_pass,
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
            "# Owner Approval Request Module Handoff Report v1",
            "",
            "Hand governance-ready module back to broader Task Manager / Midplatform mainline.",
            "",
            f"Module state: `{CURRENT_MODULE_STATE}`",
            f"Real execution: `{REAL_EXECUTION_STATE}`",
            f"Chain closed: `{closure_handoff.get('chain_closed')}`",
            f"Handoff pass: `{handoff_pass}`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "owner_approval_request_module_handoff_report": handoff_report,
        "owner_approval_request_module_handoff_report_md": markdown,
        "owner_approval_request_module_status_summary": module_status_summary,
        "owner_approval_request_midplatform_integration_position": integration_position,
        "owner_approval_request_handoff_boundary": handoff_boundary,
        "midplatform_mainline_return_plan": mainline_return_plan,
        "future_test_strategy": future_test_strategy,
        "governance_debt_and_future_runtime_handoff": governance_debt_handoff,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
