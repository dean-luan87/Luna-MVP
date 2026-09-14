# -*- coding: utf-8 -*-
"""Luna Midplatform Final Gate Planning v1 — consolidated readiness before Roadmap Decision.

Accepts Post-DryRun Review GO; consolidates 8 readiness dimensions, missing conditions,
blocker matrix, governance rule references (Module-First / Reuse-First / Validate-Once).
No real request issuance, no protocol body revalidation.
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
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.protocols.module_first_development_verification_cadence_rule_v1 import (
    DOC_REL_PATH as MODULE_FIRST_DOC_REL_PATH,
    RULE_NAME_EN as MODULE_FIRST_RULE_NAME,
    build_module_first_cadence_rule_document,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
)
from capabilities.midplatform.owner_approval_request_governance_gate_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_WHITELIST_FILES,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_final_closure_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_post_dryrun_review_v1 import (
    RUNTIME_FORBIDDEN_FLAGS,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
    CORE_CANDIDATE_IDS,
    DEFAULT_OUTPUT as DEFAULT_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Planning-v1-001"
)
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_READY_FOR_ROADMAP_DECISION"
)
FINAL_DECISION_POST_REVIEW = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_BLOCKED_BY_POST_REVIEW_GAP"
)
FINAL_DECISION_ABSENCE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_BLOCKED_BY_ABSENCE_DRIFT"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_GOVERNANCE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_BLOCKED_BY_GOVERNANCE_RULE_GAP"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Roadmap-Decision-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Planning-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1_smoke_v0"
)
FINAL_GATE_PLANNING_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_V1_GO_NO_GO_PACK_V0.md"
)
PHASE_PYTHON_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1.py",
    "tools/evaluation/midplatform/run_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1.py",
    "tools/evaluation/midplatform/verify_midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1.py",
)
TEMPLATE_LINEAGE_MODULE_PATH = "capabilities/midplatform/task_manager_foundation_handoff_evaluation_template_lineage_v1.py"

FINAL_GATE_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_readiness_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_blocker_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_non_execution_boundary_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_governance_rule_reference_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_next_phase_readiness_v1.json",
    "module_first_development_verification_cadence_rule_reference_v1.json",
    "file_size_governance_review_v1.json",
    "summary.json",
    "verifier_report.json",
)

POST_REVIEW_INDEX_FILES: Tuple[str, ...] = (
    "summary.json",
    "verifier_report.json",
    "file_size_governance_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_candidate_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_absence_review_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_record_approval_closure_next_phase_readiness_v1.json",
)

READINESS_DIMENSIONS: Tuple[str, ...] = (
    "request_issuance_readiness",
    "record_readiness",
    "approval_readiness",
    "evidence_binding_readiness",
    "permission_authorization_readiness",
    "runtime_adapter_readiness",
    "governance_readiness",
    "final_missing_conditions",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_record_approval_closure_post_review_go",
    "final_gate_plan_complete",
    "final_gate_readiness_matrix_complete",
    "missing_conditions_matrix_complete",
    "blocker_matrix_complete",
    "module_first_cadence_rule_ref_ok",
    "reuse_first_rule_ref_ok",
    "validate_once_rule_ref_ok",
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


def _meta(out: Path, post_review: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": "midplatform_task_manager_foundation_v1",
        "runtime_status": "not_enabled",
        "final_gate_planning_only": True,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        "output_root": str(out),
        "record_approval_closure_post_review_root": str(post_review),
    }


def _build_readiness_rows(post_review_ok: bool) -> List[Dict[str, Any]]:
    return [
        {
            "dimension_id": "request_issuance_readiness",
            "status": "candidate_planning_complete" if post_review_ok else "blocked",
            "real_issuance_authorized": False,
            "blocker": True,
            "note": "Candidate planning chain complete; real request issuance not authorized at final gate planning.",
        },
        {
            "dimension_id": "record_readiness",
            "status": "candidate_ready" if post_review_ok else "blocked",
            "blocker": False,
            "note": "Record-approval-closure candidate matrices validated through DryRun and Post-Review.",
        },
        {
            "dimension_id": "approval_readiness",
            "status": "candidate_ready" if post_review_ok else "blocked",
            "blocker": False,
            "note": "Approval candidate closure matrices present; no real approval record created.",
        },
        {
            "dimension_id": "evidence_binding_readiness",
            "status": "candidate_ready" if post_review_ok else "blocked",
            "blocker": False,
            "note": "Evidence binding candidate matrices validated; no evidence bound record created.",
        },
        {
            "dimension_id": "permission_authorization_readiness",
            "status": "candidate_ready" if post_review_ok else "blocked",
            "blocker": False,
            "note": "Authorization/grant/freeze remain absent; permission model at candidate level only.",
        },
        {
            "dimension_id": "runtime_adapter_readiness",
            "status": "governance_debt",
            "blocker": True,
            "note": "Runtime adapter and whitebox integration deferred per governance debt.",
        },
        {
            "dimension_id": "governance_readiness",
            "status": "ready",
            "blocker": False,
            "note": "Reuse-First, Validate-Once, Module-First cadence, and file-size governance referenced.",
        },
        {
            "dimension_id": "final_missing_conditions",
            "status": "documented",
            "blocker": False,
            "note": "Missing conditions consolidated in missing_conditions and blocker matrices.",
        },
    ]


def _build_missing_conditions() -> List[Dict[str, Any]]:
    return [
        {
            "condition_id": "real_request_issuance",
            "category": "blocker",
            "resolved": False,
            "note": "Real owner approval request issuance requires Roadmap Decision and subsequent authorization planning.",
        },
        {
            "condition_id": "runtime_adapter_implementation",
            "category": "future_runtime",
            "resolved": False,
            "note": "Module adapter and runtime integration not implemented; governance debt carryover.",
        },
        {
            "condition_id": "whitebox_runtime_integration",
            "category": "future_runtime",
            "resolved": False,
            "note": "Whitebox runtime integration absent by design at this gate.",
        },
        {
            "condition_id": "module_level_functional_slice_tests",
            "category": "non_blocking",
            "resolved": False,
            "note": "Per Module-First cadence: complete module fill and slice tests before release gate.",
        },
        {
            "condition_id": "governance_debt_closure",
            "category": "governance_debt",
            "resolved": False,
            "note": "Governance debts preserved; must not implement now flags remain.",
        },
        {
            "condition_id": "record_approval_closure_candidate_chain",
            "category": "non_blocking",
            "resolved": True,
            "note": "Planning, DryRun, and Post-DryRun Review GO achieved.",
        },
    ]


def _build_blocker_rows() -> List[Dict[str, Any]]:
    return [
        {
            "blocker_id": "real_request_issuance_not_authorized",
            "active": True,
            "severity": "blocker",
            "note": "Final gate planning does not authorize real request issuance.",
        },
        {
            "blocker_id": "runtime_execution_absent_required",
            "active": True,
            "severity": "blocker",
            "note": "Runtime execution must remain absent until explicit Roadmap Decision path.",
        },
        {
            "blocker_id": "module_adapter_not_implemented",
            "active": True,
            "severity": "governance_debt",
            "note": "Adapter implementation deferred per governance debt.",
        },
        {
            "blocker_id": "candidate_escalation_absent",
            "active": False,
            "severity": "info",
            "note": "All core candidates remain candidate-only.",
        },
    ]


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_planning_v1(
    *,
    record_approval_closure_post_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    post_review = Path(record_approval_closure_post_review_root).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, post_review)
    issues: List[str] = []

    post_summary = _read_json(post_review / "summary.json")
    post_verifier = _read_json(post_review / "verifier_report.json")
    post_file_size = _read_json(post_review / "file_size_governance_review_v1.json")
    candidate_review = _read_json(post_review / POST_REVIEW_INDEX_FILES[3])
    absence_review = _read_json(post_review / POST_REVIEW_INDEX_FILES[4])
    post_next_phase = _read_json(post_review / POST_REVIEW_INDEX_FILES[5])

    prior_record_approval_closure_post_review_go = (
        post_summary.get("final_decision") == POST_REVIEW_FINAL_GO
        and post_summary.get("recommended_next_phase") == POST_REVIEW_NEXT_PHASE
        and post_verifier.get("verifier") == "GO"
        and int(post_verifier.get("passed_checks", 0)) >= 300
        and post_verifier.get("failed_checks") == 0
        and post_verifier.get("blocker_count") == 0
        and post_summary.get("post_review_pass") is True
        and post_summary.get("lightweight_compliance_post_review_only") is True
        and post_summary.get("file_size_governance_review_ok") is True
        and post_summary.get("candidate_review_ok") is True
        and post_summary.get("absence_review_ok") is True
    )
    if not prior_record_approval_closure_post_review_go:
        issues.append("post_review_not_go")

    absence = {key: post_summary.get(key) is True for key in ABSENCE_KEYS}
    if absence_review:
        absence = {key: absence.get(key) and absence_review.get(key) is True for key in ABSENCE_KEYS}
    absence_ok = prior_record_approval_closure_post_review_go and all(absence.values())
    if not absence_ok:
        issues.append("absence_drift")

    non_execution_boundary_ok = (
        prior_record_approval_closure_post_review_go
        and post_summary.get("non_execution_boundary_ok") is True
        and post_next_phase.get("request_issued") is False
        and post_next_phase.get("grant_issued") is False
        and post_next_phase.get("closure_executed") is False
    )
    for flag in RUNTIME_FORBIDDEN_FLAGS:
        if post_summary.get(flag) is True:
            non_execution_boundary_ok = False
            issues.append(f"runtime_flag:{flag}")
            break

    readiness_rows = _build_readiness_rows(prior_record_approval_closure_post_review_go)
    final_gate_readiness_matrix_complete = (
        prior_record_approval_closure_post_review_go
        and len(readiness_rows) == len(READINESS_DIMENSIONS)
        and all(row.get("dimension_id") in READINESS_DIMENSIONS for row in readiness_rows)
    )
    if not final_gate_readiness_matrix_complete:
        issues.append("readiness_matrix_incomplete")

    missing_conditions = _build_missing_conditions()
    missing_conditions_matrix_complete = (
        prior_record_approval_closure_post_review_go
        and len(missing_conditions) >= 5
        and any(c.get("category") == "blocker" for c in missing_conditions)
        and any(c.get("category") == "future_runtime" for c in missing_conditions)
    )
    if not missing_conditions_matrix_complete:
        issues.append("missing_conditions_incomplete")

    blocker_rows = _build_blocker_rows()
    blocker_matrix_complete = (
        prior_record_approval_closure_post_review_go
        and len(blocker_rows) >= 3
        and any(b.get("active") for b in blocker_rows)
    )
    if not blocker_matrix_complete:
        issues.append("blocker_matrix_incomplete")

    module_first_doc = build_module_first_cadence_rule_document()
    module_first_cadence_rule_ref_ok = (
        module_first_doc.get("module_first_cadence_rule_complete") is True
        and MODULE_FIRST_RULE_NAME == MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF
        and (repo_root / MODULE_FIRST_DOC_REL_PATH).is_file()
        and (repo_root / MODULE_FIRST_CADENCE_RULE_DOC).is_file()
    )
    if not module_first_cadence_rule_ref_ok:
        issues.append("module_first_rule_gap")

    reuse_first_rule_ref_ok = REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF == "Reuse-First Protocol Engineering Rule"
    validate_once_rule_ref_ok = VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN == "Protocol Validate Once Per Module Rule"
    governance_rule_ref_ok = (
        module_first_cadence_rule_ref_ok
        and reuse_first_rule_ref_ok
        and validate_once_rule_ref_ok
        and (repo_root / FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_DOC).is_file()
    )
    if not governance_rule_ref_ok:
        issues.append("governance_rule_gap")

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Post-DryRun-Review-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=FINAL_GATE_PLANNING_GO_NO_GO_PACK,
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Final-Gate-Planning-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_REQUEST_FINAL_GATE_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Record-Approval-Closure-Post-DryRun-Review-v1-001",
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
        previous_interruption_type=post_file_size.get("previous_interruption_type"),
        previous_interruption_duration_seconds=post_file_size.get("previous_interruption_duration_seconds"),
        previous_interruption_not_logic_loop=post_file_size.get("previous_interruption_not_logic_loop"),
    )
    file_size_governance_review_ok = file_size_governance_review.get("file_size_governance_review_ok") is True

    final_gate_plan_complete = (
        prior_record_approval_closure_post_review_go
        and final_gate_readiness_matrix_complete
        and missing_conditions_matrix_complete
        and blocker_matrix_complete
        and governance_rule_ref_ok
        and template_lineage_ok
        and file_size_governance_review_ok
    )

    next_phase_readiness_ok = (
        final_gate_plan_complete
        and non_execution_boundary_ok
        and absence_ok
        and module_first_cadence_rule_ref_ok
        and reuse_first_rule_ref_ok
        and validate_once_rule_ref_ok
    )

    if not prior_record_approval_closure_post_review_go:
        final_decision = FINAL_DECISION_POST_REVIEW
    elif not template_lineage_ok:
        final_decision = FINAL_DECISION_LINEAGE
    elif not absence_ok:
        final_decision = FINAL_DECISION_ABSENCE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    elif not governance_rule_ref_ok:
        final_decision = FINAL_DECISION_GOVERNANCE
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_record_approval_closure_post_review_go": prior_record_approval_closure_post_review_go,
        "final_gate_plan_complete": final_gate_plan_complete,
        "final_gate_readiness_matrix_complete": final_gate_readiness_matrix_complete,
        "missing_conditions_matrix_complete": missing_conditions_matrix_complete,
        "blocker_matrix_complete": blocker_matrix_complete,
        "module_first_cadence_rule_ref_ok": module_first_cadence_rule_ref_ok,
        "reuse_first_rule_ref_ok": reuse_first_rule_ref_ok,
        "validate_once_rule_ref_ok": validate_once_rule_ref_ok,
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
    final_gate_planning_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(go_condition_values[k] for k in GO_CONDITIONS_KEYS)
    )
    next_phase = NEXT_PHASE_GO if final_gate_planning_pass else NEXT_PHASE_HOLD
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions={k: go_condition_values[k] for k in GO_CONDITIONS_KEYS},
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=tuple(
            list(post_summary.get("chain_trace_nodes") or [])
            + ["freeze_authorization_grant_owner_approval_request_final_gate_planning"]
        ),
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    final_gate_plan = {
        "plan_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan_v1",
        "final_gate_plan_complete": final_gate_plan_complete,
        "readiness_dimensions": list(READINESS_DIMENSIONS),
        "core_candidate_ids": list(CORE_CANDIDATE_IDS),
        "post_review_final_decision": post_summary.get("final_decision"),
        "real_request_issuance_authorized": False,
        "real_record_creation_authorized": False,
        **go_condition_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    readiness_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_readiness_matrix_v1",
        "final_gate_readiness_matrix_complete": final_gate_readiness_matrix_complete,
        "rows": readiness_rows,
        **meta,
    }
    missing_conditions_doc = {
        "doc_id": "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions_v1",
        "missing_conditions_matrix_complete": missing_conditions_matrix_complete,
        "conditions": missing_conditions,
        **meta,
    }
    blocker_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_blocker_matrix_v1",
        "blocker_matrix_complete": blocker_matrix_complete,
        "blockers": blocker_rows,
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
        **absence,
        **meta,
    }
    governance_rule_reference = {
        "reference_id": "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_governance_rule_reference_v1",
        "reuse_first_protocol_engineering_rule_ref": REUSE_FIRST_PROTOCOL_ENGINEERING_RULE_REF,
        "module_first_development_verification_cadence_rule_ref": MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_REF,
        "module_first_cadence_rule_doc": MODULE_FIRST_CADENCE_RULE_DOC,
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
        "file_size_module_split_governance_rule_ref": FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_REF,
        "file_size_module_split_governance_rule_doc": FILE_SIZE_MODULE_SPLIT_GOVERNANCE_RULE_DOC,
        "reuse_first_rule_ref_ok": reuse_first_rule_ref_ok,
        "module_first_cadence_rule_ref_ok": module_first_cadence_rule_ref_ok,
        "validate_once_rule_ref_ok": validate_once_rule_ref_ok,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_protocol_revalidation": False,
        **meta,
    }
    module_first_reference = {
        **module_first_doc,
        "reference_id": "module_first_development_verification_cadence_rule_reference_v1",
        "module_first_cadence_rule_ref_ok": module_first_cadence_rule_ref_ok,
        **meta,
    }
    next_phase_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_next_phase_readiness_v1",
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_request_final_gate_roadmap_decision",
        "roadmap_decision_readiness": next_phase_readiness_ok,
        "request_issued": False,
        "real_request_issuance_authorized": False,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "final_gate_planning_pass": final_gate_planning_pass,
        "final_gate_planning_only": True,
        "blocker_count": len(issues),
        "issues": issues,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Final Gate Planning Report v1",
            "",
            "Consolidated readiness assessment before Roadmap Decision. No real request issuance.",
            "",
            f"Post-Review GO accepted: `{prior_record_approval_closure_post_review_go}`",
            f"Readiness matrix complete: `{final_gate_readiness_matrix_complete}`",
            f"Module-First cadence rule ref OK: `{module_first_cadence_rule_ref_ok}`",
            f"Final decision: `{final_decision}`",
            f"Next phase: `{next_phase}`",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan": final_gate_plan,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_final_gate_plan_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_readiness_matrix": readiness_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_missing_conditions": missing_conditions_doc,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_blocker_matrix": blocker_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_non_execution_boundary": non_execution_boundary,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_governance_rule_reference": governance_rule_reference,
        "task_manager_freeze_authorization_grant_owner_approval_request_final_gate_next_phase_readiness": next_phase_readiness,
        "module_first_development_verification_cadence_rule_reference": module_first_reference,
        "file_size_governance_review": {**file_size_governance_review, **meta},
        "summary": summary,
    }
