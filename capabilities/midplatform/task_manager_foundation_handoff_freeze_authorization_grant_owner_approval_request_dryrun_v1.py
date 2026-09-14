# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request DryRun v1.

Structure inherited from grant_owner_approval_dryrun_v1 with upstream input from
grant_owner_approval_request_planning_v1, registry patch, post-dryrun review, and shared_code_smoke.
Protocol Standard Validate Once, Reference Many Times — light protocol reference only.
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
    NEXT_PHASE_GO as REGISTRY_PATCH_NEXT_PHASE,
    PROTOCOL_INPUT_CANDIDATE_ID,
    PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
    PROTOCOL_OUTPUT_CANDIDATE_ID,
    PROTOCOL_TRACEABILITY_ID,
    RUNTIME_FORBIDDEN_FLAGS,
    TRACEABILITY_QUERY_PATH_STEPS,
)
from capabilities.midplatform.protocols.protocol_error_codes_v1 import build_error_code, validate_error_code
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    FAILURE_CLASSIFICATION,
    RULE_NAME_EN as SEPARATION_RULE_NAME_EN,
    VALIDATE_ONCE_ATTRIBUTION_RULES,
    VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
    build_validate_once_per_module_rule_document,
)
from capabilities.midplatform.protocols.protocol_whitebox_binding_v1 import build_whitebox_diagnostic_ref
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_OWNER_APPROVAL_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    GO_CONDITIONS_KEYS as POST_REVIEW_GO_KEYS,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1 import (
    APPROVAL_REQUEST_CANDIDATE_ID,
    BOUNDARY_CONTRACT_STATEMENTS,
    CANONICAL_PARENT_PROTOCOL,
    CHAIN_EVIDENCE_NODES,
    DEFAULT_OUTPUT as DEFAULT_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_ROOT,
    ERROR_NAMESPACE,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GO_CONDITIONS_KEYS as PLANNING_TRUE_KEYS,
    INPUT_OUTPUT_REGISTRY_PATCH_REF,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    OUTPUT_CANDIDATE_SPECS,
    PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    PROTOCOL_ID,
    PROTOCOL_STANDARD_REF,
    RELATED_PROTOCOL_IDS,
    REQUEST_PLANNING_PACKAGE_FILES,
    SEPARATION_RULE_REF,
    TRACEABILITY_RULE_REF,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-DryRun-v1-001"
)
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_validation_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)
FINAL_DECISION_PLAN_GAP = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_PLANNING_PACKAGE_GAP"
)
FINAL_DECISION_REGISTRY = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_REGISTRY_PATCH_GAP"
)
FINAL_DECISION_SMOKE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_PROTOCOL_SMOKE_GAP"
)
FINAL_DECISION_SCOPE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_APPROVAL_SCOPE_ESCALATION"
)
FINAL_DECISION_PROTOCOL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_PROTOCOL_REFERENCE_GAP"
)
FINAL_DECISION_INPUT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_INPUT_CANDIDATE_CONTRACT_GAP"
)
FINAL_DECISION_OUTPUT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_OUTPUT_CANDIDATE_CONTRACT_GAP"
)
FINAL_DECISION_TRACE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_TRACEABILITY_GAP"
)
FINAL_DECISION_REQUEST = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
)
FINAL_DECISION_APPROVAL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_OWNER_APPROVAL_RECORD_LEAKAGE"
)
FINAL_DECISION_FREEZE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_FREEZE_STATE_ESCALATION"
)
FINAL_DECISION_DEBT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
)
FINAL_DECISION_L1 = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Post-DryRun-Review-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-DryRun-Issue-Review-v1-001"
)
VALIDATE_ONCE_PER_MODULE_RULE_REF = VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN
MODULE_ID = "task_manager_owner_approval_request"
FIRST_PROTOCOL_VALIDATION_PHASE = PHASE_ID
VALIDATE_ONCE_PER_MODULE_NOTE_EN = (
    "This phase is the first protocol integration validation for Task Manager owner approval request. "
    "If this phase GO, later phases in the same chain perform lightweight protocol reference checks only; "
    "later failures default to module local PROC / implementation failure unless "
    "protocol_id, error_namespace, schema_ref, traceability_rule_ref, or shared helper drift."
)
VALIDATE_ONCE_PER_MODULE_NOTE_ZH = (
    "本阶段作为 Task Manager owner approval request 协议首次接入验证阶段。"
    "若本阶段 GO，后续 Task Manager owner approval request 链路不再完整验证该协议标准；"
    "后续失败默认归为模块本地流程/实现问题，"
    "除非 protocol_id、error_namespace、schema_ref、traceability_rule_ref 或 shared helper 发生漂移。"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1_smoke_v0"
)

GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_ARTIFACTS: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_plan_integrity_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_absence_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_boundary_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_evidence_traceability_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_validation_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_post_review_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)
CHAIN_TRACE_NODES: Tuple[str, ...] = CHAIN_EVIDENCE_NODES + ("freeze_authorization_grant_owner_approval_request_dryrun",)
DRYRUN_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "owner_approval_request_dryrun != owner_approval_request",
) + BOUNDARY_CONTRACT_STATEMENTS
ALLOWED_SCOPE_CLASSIFICATIONS: Tuple[str, ...] = (
    "owner-approval-request-planning-scope",
    "owner-approval-request-dryrun-scope",
)
FORBIDDEN_CANDIDATE_STATES: Tuple[str, ...] = (
    "accepted_input",
    "owner_approval_record",
    "owner_approval",
    "grant",
    "fact",
    "action",
    "accepted_output",
    "record",
    "final_result",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_owner_approval_request_planning_go",
    "prior_input_output_registry_patch_go",
    "prior_shared_code_smoke_go",
    "owner_approval_request_plan_integrity_ok",
    "approval_request_candidate_validation_ok",
    "input_candidate_protocol_reference_ok",
    "output_candidate_protocol_reference_ok",
    "input_output_symmetry_reference_ok",
    "protocol_traceability_reference_ok",
    "l2_taskmanager_owner_approval_request_protocol_reference_ok",
    "protocol_execution_result_schema_ref_ok",
    "separation_rule_ref_ok",
    "traceability_rule_ref_ok",
    "input_candidate_contract_validation_ok",
    "output_candidate_contract_validation_ok",
    "input_output_traceability_validation_ok",
    "protocol_traceability_validation_ok",
    "error_namespace_validation_ok",
    "whitebox_candidate_ref_validation_ok",
    "owner_operator_notification_candidate_only",
    "rejection_reference_candidate_only",
    "expiry_reference_candidate_only",
    "revocation_reference_candidate_only",
    "authorization_request_absent",
    "request_record_absent",
    "owner_approval_request_absent",
    "owner_approval_record_absent",
    "owner_operator_ack_record_absent",
    "approval_evidence_bound_record_absent",
    "grant_token_absent",
    "grant_record_absent",
    "authorization_grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "runtime_execution_absent",
    "protocol_runtime_absent",
    "whitebox_runtime_integration_absent",
    "module_adapter_implementation_absent",
    "governance_debt_preserved",
    "template_lineage_ok",
    "owner_approval_request_dryrun_only",
    "non_execution_boundary_ok",
    "post_review_readiness_ok",
    "validate_once_per_module_rule_ok",
    "first_protocol_validation_recorded",
    "candidate_only",
    "grant_owner_approval_request_dryrun_complete",
    "evidence_traceability_paths_declared",
    "no_execution_leakage",
    "no_protocol_change",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(
    out: Path,
    planning: Path,
    post_review: Path,
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
        "owner_approval_request_dryrun_only": True,
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
        "first_protocol_validation_for_module": True,
        "first_protocol_validation_phase": FIRST_PROTOCOL_VALIDATION_PHASE,
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
        "runtime_execution_absent": True,
        "protocol_runtime_absent": True,
        "whitebox_runtime_integration_absent": True,
        "module_adapter_implementation_absent": True,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        "output_root": str(out),
        "grant_owner_approval_request_planning_root": str(planning),
        "grant_owner_approval_post_dryrun_review_root": str(post_review),
        "input_output_registry_patch_root": str(registry_patch),
        "protocol_shared_code_smoke_root": str(smoke),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1(
    *,
    grant_owner_approval_request_planning_root: str,
    grant_owner_approval_post_dryrun_review_root: Optional[str] = None,
    input_output_registry_patch_root: Optional[str] = None,
    protocol_shared_code_smoke_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(grant_owner_approval_request_planning_root or DEFAULT_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_ROOT).expanduser().resolve()
    post_review = Path(grant_owner_approval_post_dryrun_review_root or DEFAULT_OWNER_APPROVAL_POST_REVIEW_ROOT).expanduser().resolve()
    registry_patch = Path(input_output_registry_patch_root or DEFAULT_REGISTRY_PATCH_ROOT).expanduser().resolve()
    smoke = Path(protocol_shared_code_smoke_root or DEFAULT_PROTOCOL_SHARED_CODE_SMOKE_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, planning, post_review, registry_patch, smoke)
    issues: List[str] = []
    downstream_readiness_gaps: List[str] = []

    planning_summary = _read_json(planning / "summary.json")
    planning_verifier = _read_json(planning / "verifier_report.json")
    post_summary = _read_json(post_review / "summary.json")
    post_verifier = _read_json(post_review / "verifier_report.json")
    registry_summary = _read_json(registry_patch / "summary.json")
    registry_verifier = _read_json(registry_patch / "verifier_report.json")
    smoke_summary = _read_json(smoke / "summary.json")
    smoke_verifier = _read_json(smoke / "verifier_report.json")

    approval_plan = _read_json(
        planning / "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_plan_v1.json"
    )
    input_candidate_contract = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_contract_v1.json"
    )
    output_candidate_contract = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_contract_v1.json"
    )
    traceability_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_matrix_v1.json"
    )
    protocol_reference_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_matrix_v1.json"
    )
    traceability_rule_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_traceability_rule_matrix_v1.json"
    )
    error_namespace_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_matrix_v1.json"
    )
    whitebox_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_matrix_v1.json"
    )
    notification_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_matrix_v1.json"
    )
    rejection_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_matrix_v1.json"
    )
    expiry_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_matrix_v1.json"
    )
    revocation_matrix = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_matrix_v1.json"
    )
    boundary_contract = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_boundary_contract_v1.json"
    )
    non_execution_doc = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_non_execution_constraints_v1.json"
    )
    debt_carryover = _read_json(
        planning / "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_carryover_v1.json"
    )

    integrity_rows = []
    for fname in REQUEST_PLANNING_PACKAGE_FILES:
        path = planning / fname
        if fname.endswith(".json"):
            non_placeholder = bool(_read_json(path))
        else:
            non_placeholder = path.is_file() and len(path.read_text(encoding="utf-8").strip()) > 200
        integrity_rows.append({"file": fname, "exists": path.is_file(), "non_placeholder": non_placeholder})
        if not path.is_file() or not non_placeholder:
            issues.append(f"missing_or_placeholder:{fname}")

    prior_owner_approval_request_planning_go = (
        planning_summary.get("final_decision") == PLANNING_FINAL_GO
        and planning_summary.get("recommended_next_phase") == PLANNING_NEXT_PHASE
        and planning_verifier.get("verifier") == "GO"
        and int(planning_verifier.get("passed_checks", 0)) >= 420
        and planning_verifier.get("failed_checks") == 0
        and planning_verifier.get("blocker_count") == 0
        and planning_summary.get("next_phase_readiness_ok") is True
    )
    if not prior_owner_approval_request_planning_go:
        issues.append("owner_approval_request_planning_not_go")
    for key in PLANNING_TRUE_KEYS:
        if planning_summary.get(key) is not True:
            issues.append(f"planning_key_false:{key}")

    prior_owner_approval_post_review_go = (
        post_summary.get("final_decision") == POST_REVIEW_FINAL_GO
        and post_summary.get("recommended_next_phase") == POST_REVIEW_NEXT_PHASE
        and post_verifier.get("verifier") == "GO"
        and int(post_verifier.get("passed_checks", 0)) >= 420
        and post_verifier.get("failed_checks") == 0
        and post_verifier.get("blocker_count") == 0
        and all(post_summary.get(k) is True for k in POST_REVIEW_GO_KEYS)
    )
    if not prior_owner_approval_post_review_go:
        downstream_readiness_gaps.append("prior_owner_approval_post_dryrun_review_not_go")

    prior_input_output_registry_patch_go = (
        registry_summary.get("final_decision") == REGISTRY_PATCH_FINAL_GO
        and registry_summary.get("recommended_next_phase") == REGISTRY_PATCH_NEXT_PHASE
        and registry_verifier.get("verifier") == "GO"
        and int(registry_verifier.get("passed_checks", 0)) >= 420
        and registry_verifier.get("failed_checks") == 0
        and registry_verifier.get("blocker_count") == 0
    )
    if not prior_input_output_registry_patch_go:
        issues.append("prior_input_output_registry_patch_not_go")

    prior_shared_code_smoke_go = (
        smoke_summary.get("final_decision") == PROTOCOL_SMOKE_FINAL_GO
        and smoke_summary.get("final_decision") == PROTOCOL_STANDARD_REF
        and smoke_verifier.get("verifier") == "GO"
        and int(smoke_verifier.get("passed_checks", 0)) >= 420
        and smoke_verifier.get("failed_checks") == 0
        and smoke_verifier.get("blocker_count") == 0
        and smoke_summary.get("ready_for_task_manager_owner_approval_dryrun") is True
    )
    if not prior_shared_code_smoke_go:
        issues.append("prior_shared_code_smoke_not_go")

    approval_request_candidate = (
        input_candidate_contract.get("approval_request_candidate")
        or approval_plan.get("approval_request_candidate")
        or {}
    )
    output_candidates = output_candidate_contract.get("rows") or approval_plan.get("output_candidates") or []

    approval_request_candidate_validation_ok = (
        approval_request_candidate.get("candidate_role") == "input_candidate"
        and approval_request_candidate.get("candidate_type") == "owner_approval_request_candidate"
        and approval_request_candidate.get("classified_as") == "input_candidate"
        and approval_request_candidate.get("canonical_parent_protocol") == CANONICAL_PARENT_PROTOCOL
        and approval_request_candidate.get("module_extension_protocol") == PROTOCOL_ID
        and approval_request_candidate.get("migration_status") == "classification_only"
        and approval_request_candidate.get("runtime_execution_allowed") is False
        and approval_request_candidate.get("candidate_state") == "approval-request-candidate"
        and all(field in approval_request_candidate for field in INPUT_CANDIDATE_REQUIRED_FIELDS)
        and all(approval_request_candidate.get(field) is False for field in ("write_allowed", "action_allowed", "sync_allowed", "promotion_allowed"))
        and approval_request_candidate.get("candidate_state") not in FORBIDDEN_CANDIDATE_STATES
        and approval_request_candidate.get("classified_as") != "accepted_input"
    )
    if not approval_request_candidate_validation_ok:
        issues.append("approval_request_candidate_validation_gap")

    input_candidate_contract_validation_ok = (
        input_candidate_contract.get("input_candidate_contract_complete") is True
        and approval_request_candidate_validation_ok
    )
    if not input_candidate_contract_validation_ok:
        issues.append("input_candidate_contract_validation_gap")

    output_candidate_contract_validation_ok = (
        len(output_candidates) == len(OUTPUT_CANDIDATE_SPECS)
        and output_candidate_contract.get("output_candidate_contract_complete") is True
        and all(
            row.get("source_input_ref") == APPROVAL_REQUEST_CANDIDATE_ID
            and row.get("output_protocol_id") == PROTOCOL_OUTPUT_CANDIDATE_ID
            and row.get("traceability_protocol_id") == PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID
            and row.get("output_state") == "output-candidate"
            and row.get("accepted_output") is False
            and row.get("record_created") is False
            and row.get("notification_sent") is False
            and row.get("execution_path") is False
            and row.get("whitebox_candidate_ref")
            and row.get("error_namespace") == ERROR_NAMESPACE
            for row in output_candidates
        )
    )
    if not output_candidate_contract_validation_ok:
        issues.append("output_candidate_contract_validation_gap")

    input_output_traceability_validation_ok = (
        traceability_matrix.get("input_output_traceability_contract_complete") is True
        and traceability_matrix.get("input_output_mapping_is_not_runtime_execution") is True
        and traceability_matrix.get("traceability_ref_is_not_write_permission") is True
        and len(approval_request_candidate.get("derived_output_refs") or []) == len(OUTPUT_CANDIDATE_SPECS)
        and all(
            row.get("source_input_ref") == APPROVAL_REQUEST_CANDIDATE_ID and row.get("runtime_execution") is False
            for row in traceability_matrix.get("rows") or []
        )
    )
    if not input_output_traceability_validation_ok:
        issues.append("input_output_traceability_validation_gap")

    input_candidate_protocol_reference_ok = PROTOCOL_INPUT_CANDIDATE_ID in RELATED_PROTOCOL_IDS
    output_candidate_protocol_reference_ok = PROTOCOL_OUTPUT_CANDIDATE_ID in RELATED_PROTOCOL_IDS
    input_output_symmetry_reference_ok = PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID in RELATED_PROTOCOL_IDS
    protocol_traceability_reference_ok = TRACEABILITY_RULE_REF == PROTOCOL_TRACEABILITY_ID
    l2_taskmanager_owner_approval_request_protocol_reference_ok = (
        approval_request_candidate.get("module_extension_protocol") == PROTOCOL_ID
        and approval_request_candidate.get("source_protocol_id") == PROTOCOL_ID
    )
    protocol_execution_result_schema_ref_ok = bool(PROTOCOL_EXECUTION_RESULT_SCHEMA_REF)
    separation_rule_ref_ok = SEPARATION_RULE_REF == SEPARATION_RULE_NAME_EN
    traceability_rule_ref_ok = TRACEABILITY_RULE_REF == PROTOCOL_TRACEABILITY_ID
    validate_once_per_module_rule_doc = build_validate_once_per_module_rule_document(
        module_id=MODULE_ID,
        first_protocol_validation_phase=FIRST_PROTOCOL_VALIDATION_PHASE,
        protocol_refs={
            "protocol_id": PROTOCOL_ID,
            "error_namespace": ERROR_NAMESPACE,
            "protocol_execution_result_schema_ref": PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
            "traceability_rule_ref": TRACEABILITY_RULE_REF,
            "separation_rule_ref": SEPARATION_RULE_REF,
        },
        first_protocol_validation_for_module=True,
        subsequent_failures_default_to_module_local_proc=True,
        validate_once_per_module_note_en=VALIDATE_ONCE_PER_MODULE_NOTE_EN,
        validate_once_per_module_note_zh=VALIDATE_ONCE_PER_MODULE_NOTE_ZH,
    )
    validate_once_per_module_rule_ok = (
        validate_once_per_module_rule_doc.get("protocol_validate_once_per_module_rule_complete") is True
        and VALIDATE_ONCE_PER_MODULE_RULE_REF == VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN
    )
    protocol_reference_ok = (
        input_candidate_protocol_reference_ok
        and output_candidate_protocol_reference_ok
        and input_output_symmetry_reference_ok
        and protocol_traceability_reference_ok
        and l2_taskmanager_owner_approval_request_protocol_reference_ok
        and protocol_execution_result_schema_ref_ok
        and separation_rule_ref_ok
        and traceability_rule_ref_ok
        and protocol_reference_matrix.get("protocol_reference_ok") is True
    )
    first_protocol_validation_recorded = validate_once_per_module_rule_ok and protocol_reference_ok
    if not validate_once_per_module_rule_ok:
        issues.append("validate_once_per_module_rule_gap")
    if not protocol_reference_ok:
        issues.append("protocol_reference_gap")

    protocol_traceability_validation_ok = (
        len(traceability_rule_matrix.get("cursor_query_rule_steps") or []) >= 8
        and len(traceability_rule_matrix.get("traceability_query_path_steps") or []) >= 8
        and len(approval_plan.get("cursor_traceability_query_path") or []) >= 8
        and traceability_rule_matrix.get("traceability_rule_ref_ok") is True
    )
    if not protocol_traceability_validation_ok:
        issues.append("protocol_traceability_validation_gap")

    error_namespace_validation_ok = (
        error_namespace_matrix.get("error_namespace_mapping_ok") is True
        and error_namespace_matrix.get("error_namespace") == ERROR_NAMESPACE
        and len(error_namespace_matrix.get("rows") or []) >= 6
        and all(row.get("whitebox_candidate_ref") for row in error_namespace_matrix.get("rows") or [])
    )
    if not error_namespace_validation_ok:
        issues.append("error_namespace_validation_gap")

    sample_protocol_error_code = build_error_code(PROTOCOL_ID, "IFACE", 1)
    whitebox_candidate_ref = build_whitebox_diagnostic_ref(
        phase_id=PHASE_ID,
        protocol_id=PROTOCOL_ID,
        error_code=sample_protocol_error_code,
        artifact_ref="summary.json",
        field_path="go_conditions.approval_request_candidate_validation_ok",
    )
    whitebox_candidate_ref_validation_ok = (
        bool(approval_request_candidate.get("whitebox_candidate_ref"))
        and all(row.get("whitebox_candidate_ref") for row in output_candidates)
        and whitebox_matrix.get("whitebox_candidate_ref_mapping_ok") is True
        and whitebox_matrix.get("whitebox_runtime_integration") is False
        and whitebox_candidate_ref.get("binding_mode") == "contract_only"
        and whitebox_candidate_ref.get("runtime_integration") is False
        and validate_error_code(sample_protocol_error_code)
    )
    if not whitebox_candidate_ref_validation_ok:
        issues.append("whitebox_candidate_ref_validation_gap")

    notification_rows = notification_matrix.get("rows") or []
    owner_operator_notification_candidate_only = all(
        row.get("notification_status") == "owner-operator-notification-candidate"
        and row.get("notification_sent") is False
        and row.get("execution_path") is False
        for row in notification_rows
    ) if notification_rows else notification_matrix.get("owner_operator_notification_candidate_only") is True
    if not owner_operator_notification_candidate_only:
        issues.append("notification_execution_leakage")

    rejection_rows = rejection_matrix.get("rows") or []
    rejection_reference_candidate_only = all(
        row.get("reference_status") == "rejection-reference-candidate"
        and row.get("rejection_execution_path") is False
        for row in rejection_rows
    ) if rejection_rows else rejection_matrix.get("rejection_reference_candidate_only") is True
    if not rejection_reference_candidate_only:
        issues.append("rejection_execution_leakage")

    expiry_rows = expiry_matrix.get("rows") or []
    expiry_reference_candidate_only = all(
        row.get("reference_status") == "expiry-reference-candidate"
        and row.get("expiry_execution_path") is False
        for row in expiry_rows
    ) if expiry_rows else expiry_matrix.get("expiry_reference_candidate_only") is True
    if not expiry_reference_candidate_only:
        issues.append("expiry_execution_leakage")

    revocation_rows = revocation_matrix.get("rows") or []
    revocation_reference_candidate_only = all(
        row.get("reference_status") == "revocation-reference-candidate"
        and row.get("revocation_execution_path") is False
        for row in revocation_rows
    ) if revocation_rows else revocation_matrix.get("revocation_reference_candidate_only") is True
    if not revocation_reference_candidate_only:
        issues.append("revocation_execution_leakage")

    authorization_request_absent = boundary_contract.get("authorization_request_absent") is True
    request_record_absent = boundary_contract.get("request_record_absent") is True
    owner_approval_request_absent = boundary_contract.get("owner_approval_request_absent") is True
    owner_approval_record_absent = boundary_contract.get("owner_approval_record_absent") is True
    owner_operator_ack_record_absent = planning_summary.get("owner_operator_ack_record_absent") is True
    approval_evidence_bound_record_absent = planning_summary.get("approval_evidence_bound_record_absent") is True
    grant_token_absent = planning_summary.get("grant_token_absent") is True
    grant_record_absent = planning_summary.get("grant_record_absent") is True
    authorization_grant_absent = planning_summary.get("authorization_grant_absent") is True
    foundation_not_frozen = boundary_contract.get("foundation_frozen") is False
    closure_not_executed = (
        boundary_contract.get("closure_applied") is False
        and boundary_contract.get("closed") is False
    )
    runtime_execution_absent = True
    protocol_runtime_absent = True
    whitebox_runtime_integration_absent = meta["whitebox_runtime_integration"] is False
    module_adapter_implementation_absent = True
    non_execution_boundary_ok = (
        non_execution_doc.get("non_execution_boundary_ok") is True
        and authorization_request_absent
        and request_record_absent
        and owner_approval_request_absent
        and owner_approval_record_absent
        and owner_operator_ack_record_absent
        and approval_evidence_bound_record_absent
        and grant_token_absent
        and grant_record_absent
        and authorization_grant_absent
        and foundation_not_frozen
        and closure_not_executed
        and runtime_execution_absent
        and protocol_runtime_absent
        and whitebox_runtime_integration_absent
        and module_adapter_implementation_absent
    )
    if not non_execution_boundary_ok:
        issues.append("non_execution_boundary_gap")
    if not authorization_request_absent or not owner_approval_request_absent:
        issues.append("authorization_request_leakage")
    if (
        not request_record_absent
        or not owner_approval_record_absent
        or not owner_operator_ack_record_absent
        or not approval_evidence_bound_record_absent
        or not grant_token_absent
        or not grant_record_absent
    ):
        issues.append("owner_approval_record_leakage")
    if not authorization_grant_absent:
        issues.append("grant_issuance_leakage")
    if not foundation_not_frozen:
        issues.append("freeze_state_escalation")

    trace_rows = list(approval_plan.get("evidence_chain") or [])
    trace_rows.append(
        {
            "stage": "freeze_authorization_grant_owner_approval_request_dryrun",
            "root": str(out),
            "readiness": "owner-approval-request-dryrun-scope",
            "authorization_request_issued": False,
            "owner_approval_request_issued": False,
            "request_record": False,
            "owner_approval_record": False,
            "owner_operator_ack_record": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    evidence_traceability_paths_declared = all(
        any(r.get("stage") == stage for r in trace_rows) for stage in CHAIN_TRACE_NODES
    )
    planning_ref_linked = any(
        r.get("stage") == "freeze_authorization_grant_owner_approval_request_planning"
        and r.get("linked") is True
        for r in trace_rows
    )
    upstream_chain_linked = all(
        next((r for r in trace_rows if r.get("stage") == stage), {}).get("linked") is True
        for stage in CHAIN_EVIDENCE_NODES
        if stage
        not in (
            "input_output_registry_patch",
            "freeze_authorization_grant_owner_approval_request_planning",
        )
    )
    if not upstream_chain_linked:
        downstream_readiness_gaps.append("owner_approval_upstream_evidence_chain_not_linked")
    dryrun_node = next(
        (r for r in trace_rows if r.get("stage") == "freeze_authorization_grant_owner_approval_request_dryrun"),
        {},
    )
    evidence_traceability_ok = (
        dryrun_node.get("linked") is True
        and evidence_traceability_paths_declared
        and planning_ref_linked
    )
    if (
        dryrun_node.get("authorization_request_issued") is True
        or dryrun_node.get("owner_approval_request_issued") is True
        or dryrun_node.get("request_record") is True
        or dryrun_node.get("owner_approval_record") is True
        or dryrun_node.get("grant_issued") is True
    ):
        evidence_traceability_ok = False
    if not evidence_traceability_ok:
        issues.append("evidence_traceability_gap")

    planning_debts = debt_carryover.get("debts") or []
    debts = list(GOVERNANCE_DEBTS)
    for pd in planning_debts:
        for i, cd in enumerate(debts):
            if cd.get("debt_title") == pd.get("debt_title"):
                debts[i] = {**cd, **pd}
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

    l1_protocols_not_implemented = debt_carryover.get("l1_protocols_not_implemented") is True
    system_protocols_integration_not_implemented = (
        debt_carryover.get("system_protocols_integration_not_implemented") is True
    )
    if not l1_protocols_not_implemented or not system_protocols_integration_not_implemented:
        issues.append("l1_protocol_scope_leakage")

    owner_approval_request_plan_integrity_ok = all(r["exists"] and r["non_placeholder"] for r in integrity_rows)
    owner_approval_request_dryrun_only = True

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_WHITELIST_FILES[2],
        base_go_no_go_pack=GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_WHITELIST_FILES[3],
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Request-DryRun-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_REQUEST_DRYRUN_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Planning-v1-001",
    )
    upstream_lineage_ok = planning_summary.get("template_lineage_ok") is True and prior_input_output_registry_patch_go
    template_lineage_ok = template_lineage.get("template_lineage_ok") is True and upstream_lineage_ok
    if not template_lineage_ok:
        issues.append("template_lineage_gap")

    post_review_readiness_ok = (
        prior_owner_approval_request_planning_go
        and prior_input_output_registry_patch_go
        and prior_shared_code_smoke_go
        and evidence_traceability_ok
        and governance_debt_preserved
        and protocol_reference_ok
        and input_candidate_contract_validation_ok
        and output_candidate_contract_validation_ok
        and input_output_traceability_validation_ok
        and protocol_traceability_validation_ok
        and error_namespace_validation_ok
        and whitebox_candidate_ref_validation_ok
        and template_lineage_ok
        and validate_once_per_module_rule_ok
        and first_protocol_validation_recorded
    )

    if not prior_owner_approval_request_planning_go or not owner_approval_request_plan_integrity_ok:
        final_decision = FINAL_DECISION_PLAN_GAP
    elif not prior_input_output_registry_patch_go:
        final_decision = FINAL_DECISION_REGISTRY
    elif not prior_shared_code_smoke_go:
        final_decision = FINAL_DECISION_SMOKE
    elif not template_lineage_ok:
        final_decision = FINAL_DECISION_LINEAGE
    elif not protocol_reference_ok:
        final_decision = FINAL_DECISION_PROTOCOL
    elif not input_candidate_contract_validation_ok:
        final_decision = FINAL_DECISION_INPUT
    elif not output_candidate_contract_validation_ok:
        final_decision = FINAL_DECISION_OUTPUT
    elif not input_output_traceability_validation_ok or not evidence_traceability_ok:
        final_decision = FINAL_DECISION_TRACE
    elif not authorization_request_absent or not owner_approval_request_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif (
        not request_record_absent
        or not owner_approval_record_absent
        or not owner_operator_ack_record_absent
        or not approval_evidence_bound_record_absent
        or not grant_token_absent
        or not grant_record_absent
        or not authorization_grant_absent
    ):
        final_decision = FINAL_DECISION_APPROVAL
    elif not foundation_not_frozen:
        final_decision = FINAL_DECISION_FREEZE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not l1_protocols_not_implemented:
        final_decision = FINAL_DECISION_L1
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_owner_approval_request_planning_go": prior_owner_approval_request_planning_go,
        "prior_input_output_registry_patch_go": prior_input_output_registry_patch_go,
        "prior_shared_code_smoke_go": prior_shared_code_smoke_go,
        "owner_approval_request_plan_integrity_ok": owner_approval_request_plan_integrity_ok,
        "approval_request_candidate_validation_ok": approval_request_candidate_validation_ok,
        "input_candidate_protocol_reference_ok": input_candidate_protocol_reference_ok,
        "output_candidate_protocol_reference_ok": output_candidate_protocol_reference_ok,
        "input_output_symmetry_reference_ok": input_output_symmetry_reference_ok,
        "protocol_traceability_reference_ok": protocol_traceability_reference_ok,
        "l2_taskmanager_owner_approval_request_protocol_reference_ok": l2_taskmanager_owner_approval_request_protocol_reference_ok,
        "protocol_execution_result_schema_ref_ok": protocol_execution_result_schema_ref_ok,
        "separation_rule_ref_ok": separation_rule_ref_ok,
        "traceability_rule_ref_ok": traceability_rule_ref_ok,
        "input_candidate_contract_validation_ok": input_candidate_contract_validation_ok,
        "output_candidate_contract_validation_ok": output_candidate_contract_validation_ok,
        "input_output_traceability_validation_ok": input_output_traceability_validation_ok,
        "protocol_traceability_validation_ok": protocol_traceability_validation_ok,
        "error_namespace_validation_ok": error_namespace_validation_ok,
        "whitebox_candidate_ref_validation_ok": whitebox_candidate_ref_validation_ok,
        "owner_operator_notification_candidate_only": owner_operator_notification_candidate_only,
        "rejection_reference_candidate_only": rejection_reference_candidate_only,
        "expiry_reference_candidate_only": expiry_reference_candidate_only,
        "revocation_reference_candidate_only": revocation_reference_candidate_only,
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "owner_approval_request_absent": owner_approval_request_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "owner_operator_ack_record_absent": owner_operator_ack_record_absent,
        "approval_evidence_bound_record_absent": approval_evidence_bound_record_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "runtime_execution_absent": runtime_execution_absent,
        "protocol_runtime_absent": protocol_runtime_absent,
        "whitebox_runtime_integration_absent": whitebox_runtime_integration_absent,
        "module_adapter_implementation_absent": module_adapter_implementation_absent,
        "governance_debt_preserved": governance_debt_preserved,
        "template_lineage_ok": template_lineage_ok,
        "owner_approval_request_dryrun_only": owner_approval_request_dryrun_only,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "post_review_readiness_ok": post_review_readiness_ok,
        "validate_once_per_module_rule_ok": validate_once_per_module_rule_ok,
        "first_protocol_validation_recorded": first_protocol_validation_recorded,
        "candidate_only": True,
        "grant_owner_approval_request_dryrun_complete": False,
        "evidence_traceability_paths_declared": evidence_traceability_paths_declared,
        "no_execution_leakage": non_execution_boundary_ok,
        "no_protocol_change": True,
    }
    dryrun_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(
            go_condition_values.get(k)
            for k in GO_CONDITIONS_KEYS
            if k != "grant_owner_approval_request_dryrun_complete"
        )
    )
    go_condition_values["grant_owner_approval_request_dryrun_complete"] = dryrun_pass
    next_phase = NEXT_PHASE_GO if dryrun_pass else PHASE_ID
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions=go_condition_values,
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=CHAIN_TRACE_NODES,
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    dryrun_report = {
        "report_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report_v1",
        "planning_final_decision": planning_summary.get("final_decision"),
        "planning_verifier": planning_verifier.get("verifier"),
        "registry_patch_final_decision": registry_summary.get("final_decision"),
        "protocol_smoke_final_decision": smoke_summary.get("final_decision"),
        "protocol_smoke_verifier": smoke_verifier.get("verifier"),
        **go_condition_values,
        "boundary_statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "approval_request_candidate_id": APPROVAL_REQUEST_CANDIDATE_ID,
        "output_candidate_count": len(output_candidates),
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    plan_integrity_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_plan_integrity_validation_v1",
        "rows": integrity_rows,
        "owner_approval_request_plan_integrity_ok": owner_approval_request_plan_integrity_ok,
        **meta,
    }
    input_candidate_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_validation_v1",
        "approval_request_candidate": approval_request_candidate,
        "required_fields": list(INPUT_CANDIDATE_REQUIRED_FIELDS),
        "approval_request_candidate_validation_ok": approval_request_candidate_validation_ok,
        "input_candidate_contract_validation_ok": input_candidate_contract_validation_ok,
        "forbidden_states": list(FORBIDDEN_CANDIDATE_STATES),
        **meta,
    }
    output_candidate_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_validation_v1",
        "rows": output_candidates,
        "output_candidate_contract_validation_ok": output_candidate_contract_validation_ok,
        "output_candidate_specs": list(OUTPUT_CANDIDATE_SPECS),
        **meta,
    }
    input_output_traceability_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_validation_v1",
        "rows": traceability_matrix.get("rows") or [],
        "input_output_traceability_validation_ok": input_output_traceability_validation_ok,
        "input_output_mapping_is_not_runtime_execution": True,
        "traceability_ref_is_not_write_permission": True,
        "derived_output_refs": approval_request_candidate.get("derived_output_refs") or [],
        **meta,
    }
    protocol_reference_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_validation_v1",
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
        "first_protocol_validation_for_module": True,
        "first_protocol_validation_phase": FIRST_PROTOCOL_VALIDATION_PHASE,
        "subsequent_failures_default_to_module_local_proc": True,
        "validate_once_per_module_rule_ok": validate_once_per_module_rule_ok,
        "first_protocol_validation_recorded": first_protocol_validation_recorded,
        "validate_once_per_module_note_en": VALIDATE_ONCE_PER_MODULE_NOTE_EN,
        "validate_once_per_module_note_zh": VALIDATE_ONCE_PER_MODULE_NOTE_ZH,
        "validate_once_attribution_rules": list(VALIDATE_ONCE_ATTRIBUTION_RULES),
        "shared_protocol_system_revalidation": False,
        "input_candidate_protocol_reference_ok": input_candidate_protocol_reference_ok,
        "output_candidate_protocol_reference_ok": output_candidate_protocol_reference_ok,
        "input_output_symmetry_reference_ok": input_output_symmetry_reference_ok,
        "protocol_traceability_reference_ok": protocol_traceability_reference_ok,
        "l2_taskmanager_owner_approval_request_protocol_reference_ok": l2_taskmanager_owner_approval_request_protocol_reference_ok,
        "protocol_execution_result_schema_ref_ok": protocol_execution_result_schema_ref_ok,
        "separation_rule_ref_ok": separation_rule_ref_ok,
        "traceability_rule_ref_ok": traceability_rule_ref_ok,
        "protocol_error_code_light_check_ok": validate_error_code(sample_protocol_error_code),
        "sample_protocol_error_code": sample_protocol_error_code,
        "error_classification_rules": list(FAILURE_CLASSIFICATION),
        "protocol_violation_examples": [
            {
                "violation": "approval_request_candidate upgraded to accepted_input",
                "error_code": f"{PROTOCOL_INPUT_CANDIDATE_ID}::CONST-001",
            },
            {
                "violation": "approval_request_candidate missing required field",
                "error_code": f"{PROTOCOL_INPUT_CANDIDATE_ID}::IFACE-001",
            },
            {
                "violation": "output_candidate missing source_input_ref",
                "error_code": f"{PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID}::TRACE-001",
            },
            {
                "violation": "protocol_id not traceable",
                "error_code": f"{PROTOCOL_TRACEABILITY_ID}::TRACE-001",
            },
        ],
        "module_local_failure_not_protocol_failure_by_default": True,
        **meta,
    }
    protocol_traceability_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_validation_v1",
        "traceability_rule_ref": TRACEABILITY_RULE_REF,
        "cursor_query_rule_steps": list(CURSOR_QUERY_RULE_STEPS),
        "traceability_query_path_steps": list(TRACEABILITY_QUERY_PATH_STEPS),
        "protocol_traceability_validation_ok": protocol_traceability_validation_ok,
        "query_path": "error_code → protocol_id → protocol registry → upstream/downstream protocol → candidate lineage → evidence refs → whitebox candidate ref → recommended_action",
        **meta,
    }
    error_namespace_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_validation_v1",
        "rows": error_namespace_matrix.get("rows") or [],
        "error_namespace": ERROR_NAMESPACE,
        "error_namespace_validation_ok": error_namespace_validation_ok,
        "module_local_failure_not_protocol_failure_by_default": True,
        **meta,
    }
    whitebox_candidate_ref_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_validation_v1",
        "input_whitebox_candidate_ref": approval_request_candidate.get("whitebox_candidate_ref"),
        "output_whitebox_candidate_refs": [row.get("whitebox_candidate_ref") for row in output_candidates],
        "error_whitebox_candidate_refs": [row.get("whitebox_candidate_ref") for row in error_namespace_matrix.get("rows") or []],
        "whitebox_candidate_ref_validation_ok": whitebox_candidate_ref_validation_ok,
        "whitebox_candidate_ref": whitebox_candidate_ref,
        "whitebox_runtime_integration": False,
        **meta,
    }
    notification_candidate_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_validation_v1",
        "rows": notification_rows,
        "owner_operator_notification_candidate_only": owner_operator_notification_candidate_only,
        **meta,
    }
    rejection_reference_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_validation_v1",
        "rows": rejection_rows,
        "rejection_reference_candidate_only": rejection_reference_candidate_only,
        **meta,
    }
    expiry_reference_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_validation_v1",
        "rows": expiry_rows,
        "expiry_reference_candidate_only": expiry_reference_candidate_only,
        **meta,
    }
    revocation_reference_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_validation_v1",
        "rows": revocation_rows,
        "revocation_reference_candidate_only": revocation_reference_candidate_only,
        **meta,
    }
    absence_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_absence_validation_v1",
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "owner_approval_request_absent": owner_approval_request_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "owner_operator_ack_record_absent": owner_operator_ack_record_absent,
        "approval_evidence_bound_record_absent": approval_evidence_bound_record_absent,
        "authorization_grant_absent": authorization_grant_absent,
        "grant_token_absent": grant_token_absent,
        "grant_record_absent": grant_record_absent,
        "no_approval_request_notification_sent": True,
        "no_rejection_execution_path": rejection_reference_candidate_only,
        "no_expiry_execution_path": expiry_reference_candidate_only,
        "no_revocation_execution_path": revocation_reference_candidate_only,
        "no_freeze_execution_path": True,
        "no_rollback_execution_path": True,
        **meta,
    }
    boundary_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_boundary_validation_v1",
        "statements": list(DRYRUN_BOUNDARY_STATEMENTS),
        "owner_approval_request_dryrun_only": owner_approval_request_dryrun_only,
        "authorization_request_issued": False,
        "owner_approval_request_issued": False,
        "request_record_created": False,
        "owner_approval_record_created": False,
        "owner_operator_ack_record_created": False,
        "approval_evidence_bound_record_created": False,
        "grant_issued": False,
        "foundation_frozen": False,
        "closed": False,
        **meta,
    }
    evidence_traceability = {
        "trace_id": "task_manager_freeze_authorization_grant_owner_approval_request_evidence_traceability_v1",
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_chain_traceability_matrix_v1",
        "rows": trace_rows,
        "evidence_traceability_ok": evidence_traceability_ok,
        "evidence_traceability_paths_declared": evidence_traceability_paths_declared,
        "planning_ref_linked": planning_ref_linked,
        "points_to_dryrun_not_request": True,
        "points_to_dryrun_not_issued": True,
        **meta,
    }
    governance_debt_validation = {
        "validation_id": "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_validation_v1",
        "debts": debts,
        "debt_rows": debt_rows,
        "required_debt_count": len(GOVERNANCE_DEBTS),
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": l1_protocols_not_implemented,
        "system_protocols_integration_not_implemented": system_protocols_integration_not_implemented,
        **meta,
    }
    validate_once_per_module_rule = {
        "rule_record_id": "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_v1",
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_REF,
        "validate_once_per_module_rule_ok": validate_once_per_module_rule_ok,
        "first_protocol_validation_recorded": first_protocol_validation_recorded,
        "validate_once_per_module_note_en": VALIDATE_ONCE_PER_MODULE_NOTE_EN,
        "validate_once_per_module_note_zh": VALIDATE_ONCE_PER_MODULE_NOTE_ZH,
        "subsequent_phases_lightweight_protocol_check_only": True,
        **validate_once_per_module_rule_doc,
        **meta,
    }
    post_review_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_request_post_review_readiness_v1",
        "post_review_readiness_ok": post_review_readiness_ok,
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_request_post_dryrun_review",
        "validate_once_per_module_note_en": VALIDATE_ONCE_PER_MODULE_NOTE_EN,
        "validate_once_per_module_note_zh": VALIDATE_ONCE_PER_MODULE_NOTE_ZH,
        "subsequent_phases_lightweight_protocol_check_only": True,
        "first_protocol_validation_recorded": first_protocol_validation_recorded,
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
    template_lineage_doc = {
        "lineage_id": "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage_v1",
        "upstream_request_planning_lineage_ok": planning_summary.get("template_lineage_ok") is True,
        "upstream_registry_patch_lineage_ok": prior_input_output_registry_patch_go,
        **template_lineage,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_pass": dryrun_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "downstream_readiness_refs": {
            "grant_owner_approval_post_dryrun_review_root": str(post_review),
            "grant_owner_approval_request_planning_root": str(planning),
            "prior_owner_approval_post_review_go": prior_owner_approval_post_review_go,
        },
        "expected_next_phase_refs": {
            "next_phase_on_go": NEXT_PHASE_GO,
            "post_dryrun_review_target": "freeze_authorization_grant_owner_approval_request_post_dryrun_review",
        },
        "dryrun_downstream_review_refs": {
            "post_dryrun_review_root": str(post_review),
            "post_review_readiness_ok": post_review_readiness_ok,
        },
        "prior_owner_approval_post_review_go": prior_owner_approval_post_review_go,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request DryRun Report v1",
            "",
            "This phase performs freeze authorization grant owner approval request dry-run validation only. "
            "It does not issue owner approval request, send owner/operator notification, create approval records, "
            "create request records, or issue authorization requests.",
            "",
            "本阶段仅执行 freeze authorization grant owner approval request dry-run validation，"
            "不生成真实 owner approval request，不发送 owner/operator notification，"
            "不生成 owner approval record，不生成 owner/operator ack record，"
            "不绑定 approval evidence record，不生成 request record，不发起 authorization request，不签发 grant。",
            "",
            f"Owner approval request planning GO: `{prior_owner_approval_request_planning_go}`",
            f"Input/output registry patch GO: `{prior_input_output_registry_patch_go}`",
            f"Protocol shared code smoke GO: `{prior_shared_code_smoke_go}`",
            f"Approval request candidate validation OK: `{approval_request_candidate_validation_ok}`",
            f"Protocol standard ref: `{PROTOCOL_STANDARD_REF}`",
            f"Protocol ID: `{PROTOCOL_ID}`",
            f"Canonical parent protocol: `{CANONICAL_PARENT_PROTOCOL}`",
            f"Validate once per module rule: `{VALIDATE_ONCE_PER_MODULE_RULE_REF}`",
            f"First protocol validation for module: `true`",
            f"Validate once per module rule OK: `{validate_once_per_module_rule_ok}`",
            f"First protocol validation recorded: `{first_protocol_validation_recorded}`",
            "",
            "## Protocol Validate Once Per Module",
            VALIDATE_ONCE_PER_MODULE_NOTE_EN,
            VALIDATE_ONCE_PER_MODULE_NOTE_ZH,
            f"Owner approval request absent: `{owner_approval_request_absent}`",
            f"Authorization request absent: `{authorization_request_absent}`",
            f"Request record absent: `{request_record_absent}`",
            f"Freeze status: `freeze-candidate` (not frozen)",
            f"Governance debt preserved: `{governance_debt_preserved}`",
            f"Template lineage OK: `{template_lineage_ok}`",
            f"Shared protocol system revalidation: `false`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{summary['recommended_next_phase']}`",
            "",
            "## Owner Approval Request DryRun Boundary Statements",
            *[f"- {stmt}" for stmt in DRYRUN_BOUNDARY_STATEMENTS],
            "",
            "owner approval request dryrun ≠ owner approval request",
            "approval_request_candidate ≠ accepted_input",
            "",
            "## Governance Debts (P1, not implemented)",
            *[f"- {d['debt_title']}" for d in GOVERNANCE_DEBTS],
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report": dryrun_report,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_report_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_request_plan_integrity_validation": plan_integrity_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_validation": input_candidate_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_validation": output_candidate_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_validation": input_output_traceability_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_validation": protocol_reference_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_traceability_validation": protocol_traceability_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_validation": error_namespace_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_validation": whitebox_candidate_ref_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_validation": notification_candidate_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_validation": rejection_reference_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_validation": expiry_reference_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_validation": revocation_reference_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_absence_validation": absence_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_boundary_validation": boundary_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_evidence_traceability": evidence_traceability,
        "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_validation": governance_debt_validation,
        "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage": template_lineage_doc,
        "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule": validate_once_per_module_rule,
        "task_manager_freeze_authorization_grant_owner_approval_request_post_review_readiness": post_review_readiness,
        "summary": summary,
    }
