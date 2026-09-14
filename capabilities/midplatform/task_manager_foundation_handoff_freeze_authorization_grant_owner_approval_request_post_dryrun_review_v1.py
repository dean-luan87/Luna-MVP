# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Post-DryRun Review v1.

Structure inherited from grant_owner_approval_post_dryrun_review_v1 with upstream input from
grant_owner_approval_request_dryrun_v1. Confirms first protocol integration validation and
solidifies Protocol Validate Once Per Module Rule for subsequent chain attribution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.protocol_canonical_standard_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.protocol_canonical_standard_shared_code_smoke_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PROTOCOL_SHARED_CODE_SMOKE_ROOT,
    FINAL_DECISION_GO as PROTOCOL_SMOKE_FINAL_GO,
)
from capabilities.midplatform.protocol_input_output_symmetry_registry_patch_v1 import (
    CURSOR_QUERY_RULE_STEPS,
    DEFAULT_OUTPUT as DEFAULT_REGISTRY_PATCH_ROOT,
    FINAL_DECISION_GO as REGISTRY_PATCH_FINAL_GO,
    INPUT_CANDIDATE_REQUIRED_FIELDS,
    PROTOCOL_INPUT_CANDIDATE_ID,
    PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
    PROTOCOL_OUTPUT_CANDIDATE_ID,
    TRACEABILITY_QUERY_PATH_STEPS,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    FAILURE_CLASSIFICATION,
    VALIDATE_ONCE_ATTRIBUTION_RULES,
    VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
)
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1 import (
    CHAIN_TRACE_NODES,
    DEFAULT_OUTPUT as DEFAULT_DRYRUN_ROOT,
    DRYRUN_BOUNDARY_STATEMENTS,
    ERROR_NAMESPACE,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    GO_CONDITIONS_KEYS as DRYRUN_TRUE_KEYS,
    GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_ARTIFACTS,
    MODULE_ID,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    PROTOCOL_ID,
    PROTOCOL_STANDARD_REF,
    RELATED_PROTOCOL_IDS,
    RUNTIME_FORBIDDEN_FLAGS,
    SEPARATION_RULE_REF,
    TRACEABILITY_RULE_REF,
    VALIDATE_ONCE_PER_MODULE_NOTE_EN,
    VALIDATE_ONCE_PER_MODULE_NOTE_ZH,
    VALIDATE_ONCE_PER_MODULE_RULE_REF,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1 import (
    APPROVAL_REQUEST_CANDIDATE_ID,
    CANONICAL_PARENT_PROTOCOL,
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GO_CONDITIONS_KEYS as PLANNING_TRUE_KEYS,
    INPUT_OUTPUT_REGISTRY_PATCH_REF,
    OUTPUT_CANDIDATE_SPECS,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Post-DryRun-Review-v1-001"
)
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_only"
SOURCE_CHAIN = (
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1"
)
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_READY_FOR_ISSUANCE_PLANNING"
)
FINAL_DECISION_EVIDENCE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_DRYRUN_EVIDENCE_GAP"
)
FINAL_DECISION_BOUNDARY = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_BOUNDARY_DRIFT"
)
FINAL_DECISION_PROTOCOL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_PROTOCOL_REFERENCE_GAP"
)
FINAL_DECISION_VALIDATE_ONCE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_VALIDATE_ONCE_RULE_GAP"
)
FINAL_DECISION_APPROVAL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_OWNER_APPROVAL_RECORD_LEAKAGE"
)
FINAL_DECISION_REQUEST = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
)
FINAL_DECISION_FREEZE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_FREEZE_STATE_ESCALATION"
)
FINAL_DECISION_DEBT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
)
FINAL_DECISION_L1 = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Planning-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Post-DryRun-Review-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1_smoke_v0"
)
POST_REVIEW_SCOPE = "owner-approval-request-post-review-scope"
FORBIDDEN_SCOPE_CLASSIFICATIONS: Tuple[str, ...] = (
    "approval-granted-scope",
    "authorized-scope",
    "owner-approval-request-issued-scope",
)
POST_REVIEW_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "owner_approval_request_post_dryrun_review != owner_approval_request",
    "approval_request_candidate != accepted_input",
    "approval_request_candidate != owner_approval_record",
    "approval_request_candidate != owner_approval",
    "approval_request_candidate != grant",
    "output_candidate != accepted_output",
    "output_candidate != record",
    "owner_operator_notification_candidate != notification_sent",
    "rejection_reference_candidate != rejection_execution_path",
    "expiry_reference_candidate != expiry_execution_path",
    "revocation_reference_candidate != revocation_execution_path",
    "authorization_request_candidate != authorization_request_issued",
    "grant_token_candidate != grant_token",
    "grant_candidate != grant_record",
    "freeze_candidate != frozen",
    "closure_candidate != closed",
)
CHAIN_EVIDENCE_NODES: Tuple[str, ...] = CHAIN_TRACE_NODES + (
    "freeze_authorization_grant_owner_approval_request_post_dryrun_review",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_owner_approval_request_dryrun_go",
    "owner_approval_request_dryrun_result_accepted",
    "approval_request_candidate_review_ok",
    "output_candidate_review_ok",
    "input_output_traceability_review_ok",
    "protocol_traceability_review_ok",
    "protocol_reference_review_ok",
    "error_namespace_review_ok",
    "whitebox_candidate_ref_review_ok",
    "validate_once_per_module_rule_review_ok",
    "separation_rule_review_ok",
    "owner_operator_notification_candidate_only",
    "rejection_reference_candidate_only",
    "expiry_reference_candidate_only",
    "revocation_reference_candidate_only",
    "absence_review_ok",
    "boundary_drift_absent",
    "evidence_chain_review_ok",
    "governance_debt_preserved",
    "template_lineage_ok",
    "post_review_only",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(
    out: Path,
    dryrun: Path,
    planning: Path,
    registry_patch: Path,
    smoke: Path,
) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "post_review_only": True,
        "post_review_scope": POST_REVIEW_SCOPE,
        "shared_protocol_system_revalidation": False,
        "protocol_migration": False,
        "whitebox_runtime_integration": False,
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "input_output_registry_patch_ref": INPUT_OUTPUT_REGISTRY_PATCH_REF,
        "protocol_id": PROTOCOL_ID,
        "canonical_parent_protocol": CANONICAL_PARENT_PROTOCOL,
        "related_protocol_ids": list(RELATED_PROTOCOL_IDS),
        "error_namespace": ERROR_NAMESPACE,
        "protocol_execution_result_schema_ref": PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        "separation_rule_ref": SEPARATION_RULE_REF,
        "traceability_rule_ref": TRACEABILITY_RULE_REF,
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_REF,
        "module_id": MODULE_ID,
        "first_protocol_validation_confirmed": True,
        "subsequent_failures_default_to_module_local_proc": True,
        "authorization_request_absent": True,
        "authorization_request_issued": False,
        "request_record_absent": True,
        "owner_approval_request_absent": True,
        "owner_approval_record_absent": True,
        "owner_operator_ack_record_absent": True,
        "approval_evidence_bound_record_absent": True,
        "authorization_grant_absent": True,
        "grant_token_absent": True,
        "grant_record_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "grant_owner_approval_request_dryrun_root": str(dryrun),
        "grant_owner_approval_request_planning_root": str(planning),
        "input_output_registry_patch_root": str(registry_patch),
        "protocol_shared_code_smoke_root": str(smoke),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1(
    *,
    grant_owner_approval_request_dryrun_root: str,
    grant_owner_approval_request_planning_root: Optional[str] = None,
    input_output_registry_patch_root: Optional[str] = None,
    protocol_shared_code_smoke_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    dryrun = Path(grant_owner_approval_request_dryrun_root or DEFAULT_DRYRUN_ROOT).expanduser().resolve()
    planning = Path(grant_owner_approval_request_planning_root or DEFAULT_PLANNING_ROOT).expanduser().resolve()
    registry_patch = Path(input_output_registry_patch_root or DEFAULT_REGISTRY_PATCH_ROOT).expanduser().resolve()
    smoke = Path(protocol_shared_code_smoke_root or DEFAULT_PROTOCOL_SHARED_CODE_SMOKE_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, dryrun, planning, registry_patch, smoke)
    issues: List[str] = []
    downstream_readiness_gaps: List[str] = []

    dryrun_summary = _read_json(dryrun / "summary.json")
    dryrun_verifier = _read_json(dryrun / "verifier_report.json")
    planning_summary = _read_json(planning / "summary.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    registry_summary = _read_json(registry_patch / "summary.json")
    registry_verifier = _read_json(registry_patch / "verifier_report.json")
    smoke_summary = _read_json(smoke / "summary.json")
    smoke_verifier = _read_json(smoke / "verifier_report.json")
    dryrun_lineage = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage_v1.json"
    )
    trace_matrix = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_evidence_traceability_v1.json"
    )
    input_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_validation_v1.json"
    )
    output_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_validation_v1.json"
    )
    trace_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_validation_v1.json"
    )
    protocol_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_validation_v1.json"
    )
    protocol_trace_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_validation_v1.json"
    )
    error_ns_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_validation_v1.json"
    )
    whitebox_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_validation_v1.json"
    )
    validate_once_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_v1.json"
    )
    notification_val = _read_json(
        dryrun
        / "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_validation_v1.json"
    )
    rejection_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_validation_v1.json"
    )
    expiry_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_validation_v1.json"
    )
    revocation_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_validation_v1.json"
    )
    absence_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_absence_validation_v1.json"
    )
    boundary_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_boundary_validation_v1.json"
    )
    debt_val = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_validation_v1.json"
    )
    post_review_readiness_upstream = _read_json(
        dryrun / "task_manager_freeze_authorization_grant_owner_approval_request_post_review_readiness_v1.json"
    )

    review_rows = []
    for fname in GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_ARTIFACTS:
        path = dryrun / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        review_rows.append({"artifact": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_dryrun_artifact:{fname}")

    prior_planning_go = (
        planning_summary.get("final_decision") == PLANNING_FINAL_GO
        and planning_verifier.get("verifier") == "GO"
        and all(planning_summary.get(k) is True for k in PLANNING_TRUE_KEYS)
    )
    prior_registry_go = (
        registry_summary.get("final_decision") == REGISTRY_PATCH_FINAL_GO
        and registry_verifier.get("verifier") == "GO"
    )
    prior_smoke_go = (
        smoke_summary.get("final_decision") == PROTOCOL_SMOKE_FINAL_GO
        and smoke_verifier.get("verifier") == "GO"
    )
    if not prior_planning_go:
        issues.append("owner_approval_request_planning_not_go")
    if not prior_registry_go:
        issues.append("registry_patch_not_go")
    if not prior_smoke_go:
        issues.append("protocol_smoke_not_go")

    prior_owner_approval_request_dryrun_go = (
        dryrun_summary.get("final_decision") == DRYRUN_FINAL_GO
        and dryrun_summary.get("recommended_next_phase") == DRYRUN_NEXT_PHASE
        and dryrun_verifier.get("verifier") == "GO"
        and int(dryrun_verifier.get("passed_checks", 0)) >= 420
        and dryrun_verifier.get("failed_checks") == 0
        and dryrun_verifier.get("blocker_count") == 0
        and dryrun_summary.get("post_review_readiness_ok") is True
        and prior_planning_go
        and prior_registry_go
        and prior_smoke_go
    )
    if not prior_owner_approval_request_dryrun_go:
        issues.append("owner_approval_request_dryrun_not_go")

    owner_approval_request_dryrun_result_accepted = (
        prior_owner_approval_request_dryrun_go
        and all(dryrun_summary.get(k) is True for k in DRYRUN_TRUE_KEYS)
        and dryrun_summary.get("template_lineage_ok") is True
        and dryrun_summary.get("dryrun_pass") is True
    )
    if not owner_approval_request_dryrun_result_accepted:
        issues.append("owner_approval_request_dryrun_not_accepted")

    approval_request_candidate = input_val.get("approval_request_candidate") or {}
    output_candidates = output_val.get("rows") or []

    approval_request_candidate_review_ok = (
        input_val.get("approval_request_candidate_validation_ok") is True
        and input_val.get("input_candidate_contract_validation_ok") is True
        and approval_request_candidate.get("candidate_role") == "input_candidate"
        and approval_request_candidate.get("classified_as") == "input_candidate"
        and approval_request_candidate.get("canonical_parent_protocol") == CANONICAL_PARENT_PROTOCOL
        and approval_request_candidate.get("module_extension_protocol") == PROTOCOL_ID
        and approval_request_candidate.get("candidate_state") not in (
            "accepted_input",
            "owner_approval_record",
            "owner_approval",
            "grant",
            "fact",
            "action",
        )
        and all(field in approval_request_candidate for field in INPUT_CANDIDATE_REQUIRED_FIELDS)
        and len(approval_request_candidate.get("derived_output_refs") or []) == len(OUTPUT_CANDIDATE_SPECS)
    )
    if not approval_request_candidate_review_ok:
        issues.append("approval_request_candidate_review_gap")

    output_candidate_review_ok = (
        output_val.get("output_candidate_contract_validation_ok") is True
        and len(output_candidates) == len(OUTPUT_CANDIDATE_SPECS)
        and all(
            row.get("source_input_ref") == APPROVAL_REQUEST_CANDIDATE_ID
            and row.get("accepted_output") is not True
            and row.get("record_created") is not True
            and row.get("notification_sent") is not True
            and row.get("execution_path") is not True
            for row in output_candidates
        )
    )
    if not output_candidate_review_ok:
        issues.append("output_candidate_review_gap")

    input_output_traceability_review_ok = (
        trace_val.get("input_output_traceability_validation_ok") is True
        and trace_val.get("input_output_mapping_is_not_runtime_execution") is True
        and trace_val.get("traceability_ref_is_not_write_permission") is True
        and all(
            row.get("source_input_ref") == APPROVAL_REQUEST_CANDIDATE_ID and row.get("runtime_execution") is False
            for row in trace_val.get("rows") or []
        )
    )
    if not input_output_traceability_review_ok:
        issues.append("input_output_traceability_review_gap")

    protocol_traceability_review_ok = (
        protocol_trace_val.get("protocol_traceability_validation_ok") is True
        and protocol_trace_val.get("traceability_rule_ref") == TRACEABILITY_RULE_REF
        and len(protocol_trace_val.get("cursor_query_rule_steps") or []) >= 8
        and len(protocol_trace_val.get("traceability_query_path_steps") or []) >= 8
    )
    if not protocol_traceability_review_ok:
        issues.append("protocol_traceability_review_gap")

    protocol_reference_review_ok = (
        protocol_val.get("shared_protocol_system_revalidation") is False
        and protocol_val.get("protocol_standard_ref") == PROTOCOL_STANDARD_REF
        and protocol_val.get("input_output_registry_patch_ref") == INPUT_OUTPUT_REGISTRY_PATCH_REF
        and protocol_val.get("protocol_id") == PROTOCOL_ID
        and protocol_val.get("canonical_parent_protocol") == CANONICAL_PARENT_PROTOCOL
        and protocol_val.get("error_namespace") == ERROR_NAMESPACE
        and protocol_val.get("protocol_execution_result_schema_ref") == PROTOCOL_EXECUTION_RESULT_SCHEMA_REF
        and protocol_val.get("separation_rule_ref") == SEPARATION_RULE_REF
        and protocol_val.get("traceability_rule_ref") == TRACEABILITY_RULE_REF
        and protocol_val.get("validate_once_per_module_rule_ref") == VALIDATE_ONCE_PER_MODULE_RULE_REF
        and protocol_val.get("input_candidate_protocol_reference_ok") is True
        and protocol_val.get("output_candidate_protocol_reference_ok") is True
        and protocol_val.get("input_output_symmetry_reference_ok") is True
        and protocol_val.get("protocol_traceability_reference_ok") is True
        and protocol_val.get("l2_taskmanager_owner_approval_request_protocol_reference_ok") is True
        and PROTOCOL_INPUT_CANDIDATE_ID in (protocol_val.get("related_protocol_ids") or [])
        and PROTOCOL_OUTPUT_CANDIDATE_ID in (protocol_val.get("related_protocol_ids") or [])
        and PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID in (protocol_val.get("related_protocol_ids") or [])
    )
    if not protocol_reference_review_ok:
        issues.append("protocol_reference_review_gap")

    error_namespace_review_ok = (
        error_ns_val.get("error_namespace_validation_ok") is True
        and error_ns_val.get("error_namespace") == ERROR_NAMESPACE
        and error_ns_val.get("module_local_failure_not_protocol_failure_by_default") is True
    )
    if not error_namespace_review_ok:
        issues.append("error_namespace_review_gap")

    whitebox_candidate_ref_review_ok = (
        whitebox_val.get("whitebox_candidate_ref_validation_ok") is True
        and whitebox_val.get("whitebox_runtime_integration") is False
        and bool(approval_request_candidate.get("whitebox_candidate_ref"))
        and all(row.get("whitebox_candidate_ref") for row in output_candidates)
    )
    if not whitebox_candidate_ref_review_ok:
        issues.append("whitebox_candidate_ref_review_gap")

    validate_once_per_module_rule_review_ok = (
        validate_once_val.get("validate_once_per_module_rule_ok") is True
        and validate_once_val.get("first_protocol_validation_recorded") is True
        and dryrun_summary.get("validate_once_per_module_rule_ok") is True
        and dryrun_summary.get("first_protocol_validation_recorded") is True
        and protocol_val.get("first_protocol_validation_recorded") is True
        and validate_once_val.get("module_id") == MODULE_ID
        and validate_once_val.get("protocol_validate_once_per_module_rule_complete") is True
    )
    if not validate_once_per_module_rule_review_ok:
        issues.append("validate_once_per_module_rule_review_gap")

    separation_rule_review_ok = (
        protocol_val.get("separation_rule_ref_ok") is True
        and protocol_val.get("module_local_failure_not_protocol_failure_by_default") is True
        and list(protocol_val.get("error_classification_rules") or []) == list(FAILURE_CLASSIFICATION)
    )
    if not separation_rule_review_ok:
        issues.append("separation_rule_review_gap")

    notification_rows = notification_val.get("rows") or []
    owner_operator_notification_candidate_only = (
        notification_val.get("owner_operator_notification_candidate_only") is True
        and all(
            row.get("notification_sent") is False and row.get("execution_path") is False for row in notification_rows
        )
        if notification_rows
        else True
    )
    rejection_reference_candidate_only = (
        rejection_val.get("rejection_reference_candidate_only") is True
        and all(row.get("rejection_execution_path") is False for row in rejection_val.get("rows") or [])
    )
    expiry_reference_candidate_only = (
        expiry_val.get("expiry_reference_candidate_only") is True
        and all(row.get("expiry_execution_path") is False for row in expiry_val.get("rows") or [])
    )
    revocation_reference_candidate_only = (
        revocation_val.get("revocation_reference_candidate_only") is True
        and all(row.get("revocation_execution_path") is False for row in revocation_val.get("rows") or [])
    )
    if not owner_operator_notification_candidate_only:
        issues.append("notification_execution_leakage")
    if not rejection_reference_candidate_only:
        issues.append("rejection_execution_leakage")
    if not expiry_reference_candidate_only:
        issues.append("expiry_execution_leakage")
    if not revocation_reference_candidate_only:
        issues.append("revocation_execution_leakage")

    boundary_drift_rows = []
    for fname in GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_ARTIFACTS:
        if not fname.endswith(".json"):
            continue
        doc = _read_json(dryrun / fname)
        runtime_leak = any(doc.get(flag) is True for flag in RUNTIME_FORBIDDEN_FLAGS)
        scope_leak = doc.get("scope") in FORBIDDEN_SCOPE_CLASSIFICATIONS or doc.get(
            "classification"
        ) in FORBIDDEN_SCOPE_CLASSIFICATIONS
        boundary_drift_rows.append(
            {
                "artifact": fname,
                "runtime_scope_leak_absent": not runtime_leak,
                "post_review_added_runtime": False,
                "scope_classification": POST_REVIEW_SCOPE,
                "scope_escalation_absent": not scope_leak,
            }
        )
        if runtime_leak:
            issues.append(f"runtime_scope_leakage:{fname}")
        if scope_leak:
            issues.append(f"scope_escalation:{fname}")

    chain_evidence = []
    for stage in CHAIN_TRACE_NODES:
        row = next((r for r in trace_matrix.get("rows") or [] if r.get("stage") == stage), {})
        chain_evidence.append({"stage": stage, "linked": row.get("linked") is True})
    chain_evidence.append(
        {
            "stage": "freeze_authorization_grant_owner_approval_request_post_dryrun_review",
            "root": str(out),
            "readiness": POST_REVIEW_SCOPE,
            "authorization_request_issued": False,
            "owner_approval_request_issued": False,
            "request_record": False,
            "owner_approval_record": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    evidence_chain_paths_declared = all(
        any(node.get("stage") == stage for node in chain_evidence) for stage in CHAIN_EVIDENCE_NODES
    )
    dryrun_ref_linked = any(
        node.get("stage") == "freeze_authorization_grant_owner_approval_request_dryrun"
        and node.get("linked") is True
        for node in chain_evidence
    )
    review_node_linked = any(
        node.get("stage") == "freeze_authorization_grant_owner_approval_request_post_dryrun_review"
        and node.get("linked") is True
        for node in chain_evidence
    )
    upstream_chain_linked = all(
        node.get("linked") is True
        for node in chain_evidence
        if node.get("stage")
        not in (
            "freeze_authorization_grant_owner_approval_request_dryrun",
            "freeze_authorization_grant_owner_approval_request_post_dryrun_review",
        )
    )
    if not upstream_chain_linked:
        downstream_readiness_gaps.append("upstream_evidence_chain_not_fully_linked")
    evidence_chain_review_ok = (
        owner_approval_request_dryrun_result_accepted
        and dryrun_ref_linked
        and review_node_linked
        and evidence_chain_paths_declared
    )
    if not evidence_chain_review_ok:
        issues.append("evidence_chain_gap")

    authorization_request_issued = boundary_val.get("authorization_request_issued") is True
    authorization_request_absent = absence_val.get("authorization_request_absent") is True
    request_record_absent = absence_val.get("request_record_absent") is True
    owner_approval_request_absent = absence_val.get("owner_approval_request_absent") is True
    owner_approval_record_absent = absence_val.get("owner_approval_record_absent") is True
    owner_operator_ack_record_absent = absence_val.get("owner_operator_ack_record_absent") is True
    approval_evidence_bound_record_absent = absence_val.get("approval_evidence_bound_record_absent") is True
    authorization_grant_absent = absence_val.get("authorization_grant_absent") is True
    grant_token_absent = absence_val.get("grant_token_absent") is True
    grant_record_absent = absence_val.get("grant_record_absent") is True
    no_freeze_execution_path = absence_val.get("no_freeze_execution_path") is True
    no_rollback_execution_path = absence_val.get("no_rollback_execution_path") is True
    no_rejection_execution_path = absence_val.get("no_rejection_execution_path") is True
    no_expiry_execution_path = absence_val.get("no_expiry_execution_path") is True
    no_revocation_execution_path = absence_val.get("no_revocation_execution_path") is True
    absence_review_ok = (
        not authorization_request_issued
        and authorization_request_absent
        and request_record_absent
        and owner_approval_request_absent
        and owner_approval_record_absent
        and owner_operator_ack_record_absent
        and approval_evidence_bound_record_absent
        and authorization_grant_absent
        and grant_token_absent
        and grant_record_absent
        and no_freeze_execution_path
        and no_rollback_execution_path
        and no_rejection_execution_path
        and no_expiry_execution_path
        and no_revocation_execution_path
        and absence_val.get("no_approval_request_notification_sent") is True
    )
    foundation_not_frozen = boundary_val.get("foundation_frozen") is False
    closure_not_executed = boundary_val.get("closed") is False
    non_execution_boundary_ok = boundary_val.get("owner_approval_request_dryrun_only") is True
    if authorization_request_issued:
        issues.append("authorization_request_issued_leakage")
    if not absence_review_ok:
        issues.append("owner_approval_record_leakage")
    if not foundation_not_frozen:
        issues.append("freeze_state_escalation")
    if not closure_not_executed:
        issues.append("closure_state_escalation")
    if not non_execution_boundary_ok:
        issues.append("runtime_scope_leakage")

    dryrun_debts = debt_val.get("debts") or []
    debts = list(GOVERNANCE_DEBTS)
    for dd in dryrun_debts:
        for i, cd in enumerate(debts):
            if cd.get("debt_title") == dd.get("debt_title"):
                debts[i] = {**cd, **dd}
    required_titles = [d["debt_title"] for d in GOVERNANCE_DEBTS]
    debt_rows: List[Dict[str, Any]] = []
    governance_debt_preserved = len(debts) >= len(GOVERNANCE_DEBTS)
    for title in required_titles:
        match = next((d for d in debts if d.get("debt_title") == title), {})
        ok = (
            bool(match)
            and match.get("priority") == "P1"
            and match.get("classification") == "L1 Midplatform System Protocols"
            and match.get("must_not_implement_now") is True
        )
        debt_rows.append(
            {
                "debt_title": title,
                "preserved": ok,
                "priority": match.get("priority"),
                "must_not_implement_now": match.get("must_not_implement_now"),
            }
        )
        if not ok:
            governance_debt_preserved = False
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    l1_protocols_not_implemented = debt_val.get("l1_protocols_not_implemented") is True
    system_protocols_integration_not_implemented = debt_val.get("system_protocols_integration_not_implemented") is True
    if not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        issues.append("l1_protocol_scope_leakage")

    boundary_drift_absent = all(
        r["runtime_scope_leak_absent"] and r.get("scope_escalation_absent", True) for r in boundary_drift_rows
    )

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Owner-Approval-Post-DryRun-Review-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_WHITELIST_FILES[2],
        base_go_no_go_pack=GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_WHITELIST_FILES[3],
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Post-DryRun-Review-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_REQUEST_POST_REVIEW_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-Request-DryRun-v1-001",
    )
    upstream_lineage_ok = (
        dryrun_lineage.get("template_lineage_ok") is True and dryrun_summary.get("template_lineage_ok") is True
    )
    template_lineage_ok = template_lineage.get("template_lineage_ok") is True and upstream_lineage_ok
    if not template_lineage_ok:
        issues.append("template_lineage_gap")

    owner_approval_request_issuance_planning_ready = (
        owner_approval_request_dryrun_result_accepted
        and approval_request_candidate_review_ok
        and output_candidate_review_ok
        and input_output_traceability_review_ok
        and protocol_traceability_review_ok
        and protocol_reference_review_ok
        and error_namespace_review_ok
        and whitebox_candidate_ref_review_ok
        and validate_once_per_module_rule_review_ok
        and separation_rule_review_ok
        and boundary_drift_absent
        and evidence_chain_review_ok
        and absence_review_ok
        and foundation_not_frozen
        and closure_not_executed
        and governance_debt_preserved
        and non_execution_boundary_ok
        and post_review_readiness_upstream.get("post_review_readiness_ok") is True
        and template_lineage_ok
    )
    next_phase_readiness_ok = owner_approval_request_issuance_planning_ready

    if not owner_approval_request_dryrun_result_accepted:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not evidence_chain_review_ok:
        final_decision = FINAL_DECISION_EVIDENCE
    elif not template_lineage_ok:
        final_decision = FINAL_DECISION_LINEAGE
    elif not validate_once_per_module_rule_review_ok:
        final_decision = FINAL_DECISION_VALIDATE_ONCE
    elif not protocol_reference_review_ok:
        final_decision = FINAL_DECISION_PROTOCOL
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not boundary_drift_absent or not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_BOUNDARY if not boundary_drift_absent else FINAL_DECISION_RUNTIME
    elif authorization_request_issued:
        final_decision = FINAL_DECISION_REQUEST
    elif not absence_review_ok:
        final_decision = FINAL_DECISION_APPROVAL
    elif not foundation_not_frozen or not approval_request_candidate_review_ok or not output_candidate_review_ok:
        final_decision = FINAL_DECISION_FREEZE
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_owner_approval_request_dryrun_go": prior_owner_approval_request_dryrun_go,
        "owner_approval_request_dryrun_result_accepted": owner_approval_request_dryrun_result_accepted,
        "approval_request_candidate_review_ok": approval_request_candidate_review_ok,
        "output_candidate_review_ok": output_candidate_review_ok,
        "input_output_traceability_review_ok": input_output_traceability_review_ok,
        "protocol_traceability_review_ok": protocol_traceability_review_ok,
        "protocol_reference_review_ok": protocol_reference_review_ok,
        "error_namespace_review_ok": error_namespace_review_ok,
        "whitebox_candidate_ref_review_ok": whitebox_candidate_ref_review_ok,
        "validate_once_per_module_rule_review_ok": validate_once_per_module_rule_review_ok,
        "separation_rule_review_ok": separation_rule_review_ok,
        "owner_operator_notification_candidate_only": owner_operator_notification_candidate_only,
        "rejection_reference_candidate_only": rejection_reference_candidate_only,
        "expiry_reference_candidate_only": expiry_reference_candidate_only,
        "revocation_reference_candidate_only": revocation_reference_candidate_only,
        "absence_review_ok": absence_review_ok,
        "boundary_drift_absent": boundary_drift_absent,
        "evidence_chain_review_ok": evidence_chain_review_ok,
        "governance_debt_preserved": governance_debt_preserved,
        "template_lineage_ok": template_lineage_ok,
        "post_review_only": True,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
    }
    review_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(go_condition_values.get(key) is True for key in GO_CONDITIONS_KEYS)
    )
    next_phase = NEXT_PHASE_GO if review_pass else PHASE_ID
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions=go_condition_values,
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=CHAIN_EVIDENCE_NODES,
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    review_report = {
        "review_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1",
        **go_condition_values,
        "authorization_request_issued": authorization_request_issued,
        "owner_approval_request_issuance_planning_ready": owner_approval_request_issuance_planning_ready,
        "post_review_scope": POST_REVIEW_SCOPE,
        "validate_once_per_module_note_en": VALIDATE_ONCE_PER_MODULE_NOTE_EN,
        "validate_once_per_module_note_zh": VALIDATE_ONCE_PER_MODULE_NOTE_ZH,
        "subsequent_phases_lightweight_protocol_check_only": True,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    dryrun_result_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_dryrun_result_review_v1",
        "rows": review_rows,
        "prior_owner_approval_request_dryrun_go": prior_owner_approval_request_dryrun_go,
        "owner_approval_request_dryrun_result_accepted": owner_approval_request_dryrun_result_accepted,
        "dryrun_final_decision": dryrun_summary.get("final_decision"),
        "dryrun_recommended_next_phase": dryrun_summary.get("recommended_next_phase"),
        "dryrun_pass": dryrun_summary.get("dryrun_pass") is True,
        **meta,
    }
    input_candidate_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_review_v1",
        "approval_request_candidate": approval_request_candidate,
        "approval_request_candidate_review_ok": approval_request_candidate_review_ok,
        "required_field_count": len(INPUT_CANDIDATE_REQUIRED_FIELDS),
        "derived_output_refs": approval_request_candidate.get("derived_output_refs") or [],
        **meta,
    }
    output_candidate_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_review_v1",
        "rows": output_candidates,
        "output_candidate_review_ok": output_candidate_review_ok,
        "output_candidate_specs": list(OUTPUT_CANDIDATE_SPECS),
        **meta,
    }
    input_output_traceability_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_review_v1",
        "rows": trace_val.get("rows") or [],
        "input_output_traceability_review_ok": input_output_traceability_review_ok,
        **meta,
    }
    protocol_traceability_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_review_v1",
        "traceability_rule_ref": TRACEABILITY_RULE_REF,
        "cursor_query_rule_steps": list(CURSOR_QUERY_RULE_STEPS),
        "traceability_query_path_steps": list(TRACEABILITY_QUERY_PATH_STEPS),
        "protocol_traceability_review_ok": protocol_traceability_review_ok,
        **meta,
    }
    protocol_reference_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_review_v1",
        "source_validation_id": protocol_val.get("validation_id"),
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "input_output_registry_patch_ref": INPUT_OUTPUT_REGISTRY_PATCH_REF,
        "protocol_id": PROTOCOL_ID,
        "canonical_parent_protocol": CANONICAL_PARENT_PROTOCOL,
        "related_protocol_ids": list(RELATED_PROTOCOL_IDS),
        "error_namespace": ERROR_NAMESPACE,
        "protocol_execution_result_schema_ref": PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        "separation_rule_ref": SEPARATION_RULE_REF,
        "traceability_rule_ref": TRACEABILITY_RULE_REF,
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_REF,
        "shared_protocol_system_revalidation": False,
        "l1_input_output_standard_revalidation": False,
        "protocol_reference_review_ok": protocol_reference_review_ok,
        "protocol_violation_examples": protocol_val.get("protocol_violation_examples") or [],
        **meta,
    }
    error_namespace_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_review_v1",
        "rows": error_ns_val.get("rows") or [],
        "error_namespace": ERROR_NAMESPACE,
        "error_namespace_review_ok": error_namespace_review_ok,
        "module_local_failure_not_protocol_failure_by_default": True,
        **meta,
    }
    whitebox_candidate_ref_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_review_v1",
        "whitebox_candidate_ref_review_ok": whitebox_candidate_ref_review_ok,
        "whitebox_runtime_integration": False,
        "input_whitebox_candidate_ref": approval_request_candidate.get("whitebox_candidate_ref"),
        **meta,
    }
    validate_once_per_module_rule_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_review_v1",
        "validate_once_per_module_rule_review_ok": validate_once_per_module_rule_review_ok,
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_REF,
        "first_protocol_validation_recorded": validate_once_val.get("first_protocol_validation_recorded") is True,
        "subsequent_failures_default_to_module_local_proc": True,
        "attribution_rules": list(VALIDATE_ONCE_ATTRIBUTION_RULES),
        "validate_once_per_module_note_en": VALIDATE_ONCE_PER_MODULE_NOTE_EN,
        "validate_once_per_module_note_zh": VALIDATE_ONCE_PER_MODULE_NOTE_ZH,
        "upstream_validate_once_rule": validate_once_val,
        **meta,
    }
    separation_rule_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_separation_rule_review_v1",
        "separation_rule_ref": SEPARATION_RULE_REF,
        "separation_rule_review_ok": separation_rule_review_ok,
        "error_classification_rules": list(FAILURE_CLASSIFICATION),
        "module_local_failure_not_protocol_failure_by_default": True,
        **meta,
    }
    notification_candidate_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_review_v1",
        "rows": notification_rows,
        "owner_operator_notification_candidate_only": owner_operator_notification_candidate_only,
        **meta,
    }
    rejection_reference_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_review_v1",
        "rows": rejection_val.get("rows") or [],
        "rejection_reference_candidate_only": rejection_reference_candidate_only,
        **meta,
    }
    expiry_reference_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_review_v1",
        "rows": expiry_val.get("rows") or [],
        "expiry_reference_candidate_only": expiry_reference_candidate_only,
        **meta,
    }
    revocation_reference_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_review_v1",
        "rows": revocation_val.get("rows") or [],
        "revocation_reference_candidate_only": revocation_reference_candidate_only,
        **meta,
    }
    absence_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_absence_review_v1",
        "absence_review_ok": absence_review_ok,
        "authorization_request_issued": authorization_request_issued,
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "owner_approval_request_absent": owner_approval_request_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "owner_operator_ack_record_absent": owner_operator_ack_record_absent,
        "approval_evidence_bound_record_absent": approval_evidence_bound_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "no_freeze_execution_path": no_freeze_execution_path,
        "no_rollback_execution_path": no_rollback_execution_path,
        **meta,
    }
    boundary_drift_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_boundary_drift_review_v1",
        "rows": boundary_drift_rows,
        "boundary_drift_absent": boundary_drift_absent,
        "boundary_statements": list(POST_REVIEW_BOUNDARY_STATEMENTS),
        "upstream_boundary_statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "post_review_scope": POST_REVIEW_SCOPE,
        "forbidden_scope_classifications": list(FORBIDDEN_SCOPE_CLASSIFICATIONS),
        **meta,
    }
    evidence_chain_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_evidence_chain_review_v1",
        "chain": chain_evidence,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        "evidence_chain_paths_declared": evidence_chain_paths_declared,
        "dryrun_ref_linked": dryrun_ref_linked,
        "review_node_linked": review_node_linked,
        "upstream_chain_linked": upstream_chain_linked,
        "evidence_chain_review_ok": evidence_chain_review_ok,
        **meta,
    }
    governance_debt_review = {
        "review_id": "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_review_v1",
        "debts": debts,
        "debt_rows": debt_rows,
        "required_debt_count": len(GOVERNANCE_DEBTS),
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    template_lineage_doc = {
        "lineage_id": "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage_v1",
        "upstream_owner_approval_request_dryrun_lineage_ok": upstream_lineage_ok,
        **template_lineage,
        **meta,
    }
    next_phase_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_request_next_phase_readiness_v1",
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "owner_approval_request_issuance_planning_ready": owner_approval_request_issuance_planning_ready,
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_request_issuance_planning",
        "module_adapter_implementation_ready": False,
        "authorization_request_issued": False,
        "owner_approval_request_issued": False,
        "request_record_created": False,
        "owner_approval_record_created": False,
        "owner_operator_ack_record_created": False,
        "approval_evidence_bound_record_created": False,
        "grant_issued": False,
        "freeze_authorization_granted": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "post_dryrun_review_pass": review_pass,
        "post_dryrun_review_complete": review_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "candidate_only": True,
        "no_execution_leakage": non_execution_boundary_ok,
        "no_protocol_change": True,
        "evidence_chain_paths_declared": evidence_chain_paths_declared,
        "dryrun_ref_linked": dryrun_ref_linked,
        "review_node_linked": review_node_linked,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Post-DryRun Review v1",
            "",
            "This phase reviews freeze authorization grant owner approval request dry-run results only. "
            "It confirms first protocol integration validation and solidifies Protocol Validate Once Per Module Rule. "
            "It does not issue owner approval request, send notifications, create approval records, "
            "create request records, or issue authorization requests.",
            "",
            "本阶段仅审查 freeze authorization grant owner approval request dry-run 结果，"
            "确认首次协议接入验证可接受，并固化 Protocol Validate Once Per Module Rule。"
            "不生成真实 owner approval request，不发送 owner/operator notification，"
            "不生成 owner approval record，不生成 request record，不发起 authorization request，不签发 grant。",
            "",
            f"Prior owner approval request dry-run GO: `{prior_owner_approval_request_dryrun_go}`",
            f"Owner approval request dry-run accepted: `{owner_approval_request_dryrun_result_accepted}`",
            f"Approval request candidate review OK: `{approval_request_candidate_review_ok}`",
            f"Validate once per module rule review OK: `{validate_once_per_module_rule_review_ok}`",
            f"Protocol reference review OK: `{protocol_reference_review_ok}`",
            f"Protocol traceability review OK: `{protocol_traceability_review_ok}`",
            f"Absence review OK: `{absence_review_ok}`",
            f"Owner approval request absent: `{owner_approval_request_absent}`",
            f"Request record absent: `{request_record_absent}`",
            f"Owner approval request issuance planning ready: `{owner_approval_request_issuance_planning_ready}`",
            f"Template lineage OK: `{template_lineage_ok}`",
            f"Post-review scope: `{POST_REVIEW_SCOPE}`",
            f"Shared protocol system revalidation: `false`",
            f"Freeze status: `freeze-candidate` (not frozen)",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
            "",
            "## Protocol Validate Once Per Module",
            VALIDATE_ONCE_PER_MODULE_NOTE_EN,
            VALIDATE_ONCE_PER_MODULE_NOTE_ZH,
            "",
            "## Owner Approval Request Post-Review Boundary Statements",
            *[f"- {stmt}" for stmt in POST_REVIEW_BOUNDARY_STATEMENTS],
            "",
            "owner approval request post-dryrun review ≠ owner approval request",
            "approval_request_candidate ≠ accepted_input",
            "",
            "## Governance Debts (P1, not implemented)",
            *[f"- {d['debt_title']}" for d in GOVERNANCE_DEBTS],
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_report": review_report,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_request_dryrun_result_review": dryrun_result_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_review": input_candidate_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_review": output_candidate_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_review": input_output_traceability_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_review": protocol_traceability_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_review": protocol_reference_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_review": error_namespace_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_review": whitebox_candidate_ref_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_review": validate_once_per_module_rule_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_separation_rule_review": separation_rule_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_review": notification_candidate_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_review": rejection_reference_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_review": expiry_reference_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_review": revocation_reference_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_absence_review": absence_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_boundary_drift_review": boundary_drift_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_evidence_chain_review": evidence_chain_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_review": governance_debt_review,
        "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage": template_lineage_doc,
        "task_manager_freeze_authorization_grant_owner_approval_request_next_phase_readiness": next_phase_readiness,
        "summary": summary,
    }
