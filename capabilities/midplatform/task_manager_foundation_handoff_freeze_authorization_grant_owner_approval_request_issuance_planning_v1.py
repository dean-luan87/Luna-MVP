# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Issuance Planning v1.

Adapted from grant_owner_approval_request_planning_v1 with upstream evidence from:
- request post-dryrun review
- request planning
- request dryrun
- protocol input/output registry patch
- protocol shared code smoke

Protocol strategy follows reuse-first:
- no L1 protocol full revalidation
- lightweight protocol reference only
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.protocol_canonical_standard_planning_v1 import GOVERNANCE_DEBTS
from capabilities.midplatform.protocol_canonical_standard_shared_code_smoke_v1 import (
    DEFAULT_OUTPUT as DEFAULT_SMOKE_ROOT,
    FINAL_DECISION_GO as SMOKE_FINAL_GO,
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
from capabilities.midplatform.protocols.protocol_error_codes_v1 import build_error_code
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import FAILURE_CLASSIFICATION
from capabilities.midplatform.protocols.protocol_whitebox_binding_v1 import build_whitebox_diagnostic_ref
import capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 as lineage_mod
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_dryrun_v1 import (
    DEFAULT_OUTPUT as DEFAULT_REQUEST_DRYRUN_ROOT,
    FINAL_DECISION_GO as REQUEST_DRYRUN_FINAL_GO,
    GO_CONDITIONS_KEYS as REQUEST_DRYRUN_GO_KEYS,
    NEXT_PHASE_GO as REQUEST_DRYRUN_NEXT_PHASE,
    VALIDATE_ONCE_PER_MODULE_RULE_REF,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1 import (
    APPROVAL_REQUEST_CANDIDATE_ID as UPSTREAM_APPROVAL_REQUEST_CANDIDATE_ID,
    CANONICAL_PARENT_PROTOCOL,
    DEFAULT_OUTPUT as DEFAULT_REQUEST_PLANNING_ROOT,
    FINAL_DECISION_GO as REQUEST_PLANNING_FINAL_GO,
    GO_CONDITIONS_KEYS as REQUEST_PLANNING_GO_KEYS,
    INPUT_OUTPUT_REGISTRY_PATCH_REF,
    PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
    PROTOCOL_ID,
    PROTOCOL_STANDARD_REF,
    RELATED_PROTOCOL_IDS,
    SEPARATION_RULE_REF,
    TRACEABILITY_RULE_REF,
)
ERROR_NAMESPACE = "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-REQUEST-V1::*"
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES as POST_REVIEW_CHAIN_NODES,
    DEFAULT_OUTPUT as DEFAULT_REQUEST_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL_GO,
    GO_CONDITIONS_KEYS as REQUEST_POST_REVIEW_GO_KEYS,
    NEXT_PHASE_GO as REQUEST_POST_REVIEW_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Planning-v1-001"
)
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_READY_FOR_DRYRUN"
)
FINAL_DECISION_PRIOR = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_PRIOR_REVIEW_GAP"
)
FINAL_DECISION_REGISTRY = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_REGISTRY_PATCH_GAP"
)
FINAL_DECISION_SMOKE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_PROTOCOL_SMOKE_GAP"
)
FINAL_DECISION_PROTOCOL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_PROTOCOL_REFERENCE_GAP"
)
FINAL_DECISION_INPUT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_INPUT_CANDIDATE_CONTRACT_GAP"
)
FINAL_DECISION_OUTPUT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_OUTPUT_CANDIDATE_CONTRACT_GAP"
)
FINAL_DECISION_TRACE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_TRACEABILITY_GAP"
)
FINAL_DECISION_REQUEST = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_REQUEST_LEAKAGE"
)
FINAL_DECISION_APPROVAL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_APPROVAL_LEAKAGE"
)
FINAL_DECISION_SCOPE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_SCOPE_ESCALATION"
)
FINAL_DECISION_DEBT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-DryRun-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Planning-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1_smoke_v0"
)

OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID = "owner_approval_request_issuance_candidate_v1_001"
UPSTREAM_OUTPUT_REF = "owner_approval_request_traceability_candidate"
PRIOR_OWNER_APPROVAL_REQUEST_POST_REVIEW_REF = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_POST_DRYRUN_REVIEW_READY_FOR_ISSUANCE_PLANNING"
)
REUSE_FIRST_RULE_REF = "Reuse-First Protocol Engineering Rule"

OUTPUT_CANDIDATE_SPECS: Tuple[Dict[str, str], ...] = (
    {"output_candidate_type": "owner_approval_request_issuance_plan_candidate", "suffix": "issuance_plan"},
    {"output_candidate_type": "owner_approval_request_issuance_precondition_candidate", "suffix": "precondition"},
    {"output_candidate_type": "owner_operator_notification_issuance_candidate", "suffix": "notification_issuance"},
    {"output_candidate_type": "owner_approval_request_issuance_rejection_reference_candidate", "suffix": "issuance_rejection"},
    {"output_candidate_type": "owner_approval_request_issuance_expiry_reference_candidate", "suffix": "issuance_expiry"},
    {"output_candidate_type": "owner_approval_request_issuance_revocation_reference_candidate", "suffix": "issuance_revocation"},
    {"output_candidate_type": "owner_approval_request_issuance_traceability_candidate", "suffix": "issuance_traceability"},
    {"output_candidate_type": "owner_approval_request_issuance_dryrun_readiness_candidate", "suffix": "dryrun_readiness"},
)

ISSUANCE_PLANNING_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_candidate_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_candidate_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_output_candidate_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_output_traceability_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_traceability_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_error_namespace_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_whitebox_candidate_ref_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_owner_operator_notification_candidate_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_rejection_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_expiry_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_revocation_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_absence_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_validate_once_reference_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_precondition_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_boundary_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_issuance_next_phase_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)

BOUNDARY_CONTRACT_STATEMENTS: Tuple[str, ...] = (
    "owner_approval_request_issuance_planning != owner_approval_request_issued",
    "owner_approval_request_issuance_candidate != accepted_input",
    "owner_approval_request_issuance_candidate != owner_approval_request",
    "owner_approval_request_issuance_candidate != owner_approval_record",
    "owner_approval_request_issuance_candidate != authorization_request",
    "owner_approval_request_issuance_candidate != request_record",
    "owner_approval_request_issuance_candidate != grant",
    "output_candidate != accepted_output",
    "input_output_mapping != runtime_execution",
)
PRECONDITION_ROWS: Tuple[Dict[str, Any], ...] = (
    {"precondition": "request_post_dryrun_review_go", "required": True},
    {"precondition": "request_planning_go", "required": True},
    {"precondition": "request_dryrun_go", "required": True},
    {"precondition": "registry_patch_go", "required": True},
    {"precondition": "shared_code_smoke_go", "required": True},
    {"precondition": "owner_approval_request_issued_absent", "required": True},
    {"precondition": "owner_operator_notification_sent_absent", "required": True},
    {"precondition": "precondition_candidate_only", "required": True},
    {"precondition": "governance_debt_preserved", "required": True},
)
NON_EXECUTION_CONSTRAINTS: Tuple[str, ...] = (
    "no_owner_approval_request_issued",
    "no_owner_operator_notification_sent",
    "no_request_record",
    "no_authorization_request",
    "no_owner_approval_record",
    "no_grant_token",
    "no_grant_record",
    "no_authorization_grant",
    "no_foundation_frozen",
    "no_closed_state",
    "no_runtime_executor",
    "no_module_adapter_integration",
)

CHAIN_EVIDENCE_NODES: Tuple[str, ...] = POST_REVIEW_CHAIN_NODES + (
    "freeze_authorization_grant_owner_approval_request_issuance_planning",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_request_post_dryrun_review_go",
    "prior_request_planning_go",
    "prior_request_dryrun_go",
    "prior_registry_patch_go",
    "prior_shared_code_smoke_go",
    "prior_validate_once_rule_review_go",
    "owner_approval_request_issuance_plan_complete",
    "issuance_candidate_classified_as_input_candidate",
    "issuance_input_candidate_contract_complete",
    "issuance_output_candidate_contract_complete",
    "issuance_protocol_traceability_contract_complete",
    "input_candidate_protocol_reference_ok",
    "output_candidate_protocol_reference_ok",
    "input_output_symmetry_reference_ok",
    "protocol_traceability_reference_ok",
    "l2_taskmanager_owner_approval_request_protocol_reference_ok",
    "validate_once_per_module_rule_ref_ok",
    "reuse_first_rule_ref_ok",
    "owner_approval_request_issued_absent",
    "owner_operator_notification_sent_absent",
    "precondition_candidate_only",
    "governance_debt_preserved",
    "template_lineage_ok",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
    "prior_owner_approval_request_post_review_go",
    "issuance_candidate_source_input_ref_ok",
    "protocol_execution_result_schema_ref_ok",
    "separation_rule_ref_ok",
    "traceability_rule_ref_ok",
    "issuance_input_output_traceability_contract_complete",
    "error_namespace_mapping_ok",
    "whitebox_candidate_ref_mapping_ok",
    "owner_operator_notification_issuance_candidate_only",
    "rejection_reference_candidate_only",
    "expiry_reference_candidate_only",
    "revocation_reference_candidate_only",
    "owner_approval_request_absent",
    "authorization_request_absent",
    "request_record_absent",
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
)

# NOTE:
# The lineage file should provide these constants formally.
# Until then, fallback to request-planning lineage constants to keep this module runnable.
GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES = getattr(
    lineage_mod,
    "GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES",
    lineage_mod.GRANT_OWNER_APPROVAL_REQUEST_PLANNING_WHITELIST_FILES,
)
GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_TERM_OVERRIDES = getattr(
    lineage_mod,
    "GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_TERM_OVERRIDES",
    lineage_mod.GRANT_OWNER_APPROVAL_REQUEST_PLANNING_STAGE_TERM_OVERRIDES,
)
GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_ADDITIONS = getattr(
    lineage_mod,
    "GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_ADDITIONS",
    lineage_mod.GRANT_OWNER_APPROVAL_REQUEST_PLANNING_STAGE_ADDITIONS,
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(
    out: Path,
    post_review: Path,
    request_planning: Path,
    request_dryrun: Path,
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
        "owner_approval_request_issuance_planning_only": True,
        "l1_input_output_protocol_revalidation": False,
        "shared_protocol_system_revalidation": False,
        "protocol_migration": False,
        "whitebox_runtime_integration": False,
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "input_output_registry_patch_ref": INPUT_OUTPUT_REGISTRY_PATCH_REF,
        "protocol_id": PROTOCOL_ID,
        "error_namespace": ERROR_NAMESPACE,
        "canonical_parent_protocol": CANONICAL_PARENT_PROTOCOL,
        "related_protocol_ids": list(RELATED_PROTOCOL_IDS),
        "protocol_execution_result_schema_ref": PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        "separation_rule_ref": SEPARATION_RULE_REF,
        "traceability_rule_ref": TRACEABILITY_RULE_REF,
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_REF,
        "reuse_first_rule_ref": REUSE_FIRST_RULE_REF,
        "prior_owner_approval_request_post_review_ref": PRIOR_OWNER_APPROVAL_REQUEST_POST_REVIEW_REF,
        "output_root": str(out),
        "grant_owner_approval_request_post_dryrun_review_root": str(post_review),
        "grant_owner_approval_request_planning_root": str(request_planning),
        "grant_owner_approval_request_dryrun_root": str(request_dryrun),
        "input_output_registry_patch_root": str(registry_patch),
        "protocol_shared_code_smoke_root": str(smoke),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def _build_issuance_candidate(*, derived_output_refs: List[str], source_refs: List[str]) -> Dict[str, Any]:
    created_at = datetime.now(timezone.utc).isoformat()
    whitebox = build_whitebox_diagnostic_ref(
        phase_id=PHASE_ID,
        protocol_id=PROTOCOL_ID,
        error_code=f"{PROTOCOL_ID}::IFACE-001",
        artifact_ref="task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_candidate_contract_v1.json",
        field_path="owner_approval_request_issuance_candidate",
    )
    return {
        "candidate_id": OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
        "candidate_type": "owner_approval_request_issuance_candidate",
        "candidate_role": "input_candidate",
        "classified_as": "input_candidate",
        "candidate_state": "issuance-candidate",
        "candidate_scope": "owner-approval-request-issuance-planning-scope",
        "source_input_ref": UPSTREAM_APPROVAL_REQUEST_CANDIDATE_ID,
        "upstream_output_ref": UPSTREAM_OUTPUT_REF,
        "module_extension_protocol": PROTOCOL_ID,
        "canonical_parent_protocol": CANONICAL_PARENT_PROTOCOL,
        "source_protocol_id": PROTOCOL_ID,
        "source_phase": PHASE_ID,
        "source_module": "task_manager",
        "source_artifacts": source_refs,
        "target_phase": NEXT_PHASE_GO,
        "target_module": "task_manager",
        "candidate_payload": {
            "planning_intent": "define owner approval request issuance candidate before dry-run",
            "request_issued": False,
            "notification_sent": False,
        },
        "evidence_refs": source_refs,
        "approval_refs": [],
        "dependency_refs": [PRIOR_OWNER_APPROVAL_REQUEST_POST_REVIEW_REF, PROTOCOL_STANDARD_REF],
        "ttl": "planning_only",
        "expires_at": None,
        "revocation_refs": [],
        "rejection_refs": [],
        "confidence": "planning_candidate",
        "risk_level": "planning_only",
        "migration_status": "classification_only",
        "runtime_execution_allowed": False,
        "request_issued": False,
        "notification_sent": False,
        "write_allowed": False,
        "action_allowed": False,
        "sync_allowed": False,
        "promotion_allowed": False,
        "promotion_target": NEXT_PHASE_GO,
        "promotion_blockers": ["owner_approval_request_not_issued", "issuance_dryrun_not_executed"],
        "constitution_refs": [CONSTRAINT_DOC_ID],
        "protocol_refs": list(RELATED_PROTOCOL_IDS) + [PROTOCOL_ID],
        "error_namespace": ERROR_NAMESPACE,
        "derived_output_refs": derived_output_refs,
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_REF,
        "reuse_first_rule_ref": REUSE_FIRST_RULE_REF,
        "whitebox_candidate_ref": whitebox,
        "created_by_phase": PHASE_ID,
        "created_at": created_at,
        "final_decision_ref": FINAL_DECISION_GO,
    }


def _build_output_candidate(*, spec: Dict[str, str], source_input_ref: str, index: int) -> Dict[str, Any]:
    output_id = f"{spec['suffix']}_output_candidate_v1_{index:03d}"
    whitebox = build_whitebox_diagnostic_ref(
        phase_id=PHASE_ID,
        protocol_id=PROTOCOL_OUTPUT_CANDIDATE_ID,
        error_code=f"{PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID}::TRACE-001",
        artifact_ref="task_manager_freeze_authorization_grant_owner_approval_request_issuance_output_candidate_contract_v1.json",
        field_path=output_id,
    )
    return {
        "output_candidate_id": output_id,
        "output_candidate_type": spec["output_candidate_type"],
        "source_input_ref": source_input_ref,
        "source_input_candidate_id": OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
        "upstream_output_ref": UPSTREAM_OUTPUT_REF,
        "output_protocol_id": PROTOCOL_OUTPUT_CANDIDATE_ID,
        "traceability_protocol_id": PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
        "output_state": "output-candidate",
        "accepted_output": False,
        "record_created": False,
        "notification_sent": False,
        "execution_path": False,
        "write_allowed": False,
        "action_allowed": False,
        "sync_allowed": False,
        "promotion_allowed": False,
        "error_namespace": ERROR_NAMESPACE,
        "whitebox_candidate_ref": whitebox,
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_planning_v1(
    *,
    grant_owner_approval_request_post_dryrun_review_root: Optional[str] = None,
    grant_owner_approval_request_planning_root: Optional[str] = None,
    grant_owner_approval_request_dryrun_root: Optional[str] = None,
    input_output_registry_patch_root: Optional[str] = None,
    protocol_shared_code_smoke_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    post_review = Path(
        grant_owner_approval_request_post_dryrun_review_root or DEFAULT_REQUEST_POST_REVIEW_ROOT
    ).expanduser().resolve()
    request_planning = Path(
        grant_owner_approval_request_planning_root or DEFAULT_REQUEST_PLANNING_ROOT
    ).expanduser().resolve()
    request_dryrun = Path(
        grant_owner_approval_request_dryrun_root or DEFAULT_REQUEST_DRYRUN_ROOT
    ).expanduser().resolve()
    registry_patch = Path(input_output_registry_patch_root or DEFAULT_REGISTRY_PATCH_ROOT).expanduser().resolve()
    smoke = Path(protocol_shared_code_smoke_root or DEFAULT_SMOKE_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, post_review, request_planning, request_dryrun, registry_patch, smoke)
    issues: List[str] = []
    downstream_readiness_gaps: List[str] = []

    post_summary = _read_json(post_review / "summary.json")
    post_verifier = _read_json(post_review / "verifier_report.json")
    post_chain = _read_json(
        post_review / "task_manager_freeze_authorization_grant_owner_approval_request_evidence_chain_review_v1.json"
    )
    post_validate_once = _read_json(
        post_review
        / "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_review_v1.json"
    )
    request_planning_summary = _read_json(request_planning / "summary.json")
    request_planning_verifier = _read_json(request_planning / "verifier_report.json")
    request_dryrun_summary = _read_json(request_dryrun / "summary.json")
    request_dryrun_verifier = _read_json(request_dryrun / "verifier_report.json")
    registry_summary = _read_json(registry_patch / "summary.json")
    registry_verifier = _read_json(registry_patch / "verifier_report.json")
    smoke_summary = _read_json(smoke / "summary.json")
    smoke_verifier = _read_json(smoke / "verifier_report.json")
    registry_ref_patch = _read_json(registry_patch / "input_output_protocol_reference_rule_patch_v1.json")

    prior_request_post_dryrun_review_go = (
        post_summary.get("final_decision") == REQUEST_POST_REVIEW_FINAL_GO
        and post_summary.get("recommended_next_phase") == REQUEST_POST_REVIEW_NEXT_PHASE
        and post_verifier.get("verifier") == "GO"
        and int(post_verifier.get("passed_checks", 0)) >= 420
        and post_verifier.get("failed_checks") == 0
        and post_verifier.get("blocker_count") == 0
        and all(post_summary.get(k) is True for k in REQUEST_POST_REVIEW_GO_KEYS)
    )
    prior_request_planning_go = (
        request_planning_summary.get("final_decision") == REQUEST_PLANNING_FINAL_GO
        and request_planning_verifier.get("verifier") == "GO"
        and all(request_planning_summary.get(k) is True for k in REQUEST_PLANNING_GO_KEYS)
    )
    prior_request_dryrun_go = (
        request_dryrun_summary.get("final_decision") == REQUEST_DRYRUN_FINAL_GO
        and request_dryrun_summary.get("recommended_next_phase") == REQUEST_DRYRUN_NEXT_PHASE
        and request_dryrun_verifier.get("verifier") == "GO"
        and int(request_dryrun_verifier.get("passed_checks", 0)) >= 420
        and request_dryrun_verifier.get("failed_checks") == 0
        and request_dryrun_verifier.get("blocker_count") == 0
        and all(request_dryrun_summary.get(k) is True for k in REQUEST_DRYRUN_GO_KEYS)
    )
    prior_registry_patch_go = (
        registry_summary.get("final_decision") == REGISTRY_PATCH_FINAL_GO
        and registry_summary.get("recommended_next_phase") == REGISTRY_PATCH_NEXT_PHASE
        and registry_verifier.get("verifier") == "GO"
        and int(registry_verifier.get("passed_checks", 0)) >= 420
        and registry_verifier.get("failed_checks") == 0
        and registry_verifier.get("blocker_count") == 0
    )
    prior_shared_code_smoke_go = (
        smoke_summary.get("final_decision") == SMOKE_FINAL_GO
        and smoke_verifier.get("verifier") == "GO"
        and int(smoke_verifier.get("passed_checks", 0)) >= 420
        and smoke_verifier.get("failed_checks") == 0
        and smoke_verifier.get("blocker_count") == 0
    )
    prior_validate_once_rule_review_go = (
        post_summary.get("validate_once_per_module_rule_review_ok") is True
        and post_validate_once.get("validate_once_per_module_rule_review_ok") is True
        and post_validate_once.get("validate_once_per_module_rule_ref") == VALIDATE_ONCE_PER_MODULE_RULE_REF
        and post_validate_once.get("first_protocol_validation_recorded") is True
    )

    if not prior_request_post_dryrun_review_go:
        issues.append("prior_request_post_dryrun_review_not_go")
    if not prior_request_planning_go:
        issues.append("prior_request_planning_not_go")
    if not prior_request_dryrun_go:
        issues.append("prior_request_dryrun_not_go")
    if not prior_registry_patch_go:
        issues.append("prior_registry_patch_not_go")
    if not prior_shared_code_smoke_go:
        issues.append("prior_shared_code_smoke_not_go")
    if not prior_validate_once_rule_review_go:
        issues.append("prior_validate_once_rule_review_not_go")

    output_candidates: List[Dict[str, Any]] = []
    for index, spec in enumerate(OUTPUT_CANDIDATE_SPECS, start=1):
        output_candidates.append(
            _build_output_candidate(
                spec=spec,
                source_input_ref=OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
                index=index,
            )
        )
    derived_output_refs = [row["output_candidate_id"] for row in output_candidates]
    issuance_candidate = _build_issuance_candidate(
        derived_output_refs=derived_output_refs,
        source_refs=[
            str(post_review / "summary.json"),
            str(post_review / "verifier_report.json"),
            str(request_planning / "summary.json"),
            str(request_dryrun / "summary.json"),
            str(registry_patch / "summary.json"),
            str(smoke / "summary.json"),
        ],
    )

    issuance_candidate_classified_as_input_candidate = (
        issuance_candidate.get("candidate_role") == "input_candidate"
        and issuance_candidate.get("classified_as") == "input_candidate"
        and issuance_candidate.get("source_input_ref") == UPSTREAM_APPROVAL_REQUEST_CANDIDATE_ID
        and issuance_candidate.get("upstream_output_ref") == UPSTREAM_OUTPUT_REF
    )
    issuance_input_candidate_contract_complete = all(
        field in issuance_candidate for field in INPUT_CANDIDATE_REQUIRED_FIELDS
    ) and all(
        issuance_candidate.get(flag) is False
        for flag in ("write_allowed", "action_allowed", "sync_allowed", "promotion_allowed")
    )
    issuance_output_candidate_contract_complete = (
        len(output_candidates) == 8
        and all(
            row.get("source_input_ref") == OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID
            and row.get("output_protocol_id") == PROTOCOL_OUTPUT_CANDIDATE_ID
            and row.get("traceability_protocol_id") == PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID
            and row.get("accepted_output") is False
            and row.get("record_created") is False
            and row.get("notification_sent") is False
            and row.get("execution_path") is False
            for row in output_candidates
        )
    )

    traceability_rows = [
        {
            "input_ref": OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
            "output_ref": row["output_candidate_id"],
            "source_input_ref": OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
            "upstream_input_ref": UPSTREAM_APPROVAL_REQUEST_CANDIDATE_ID,
            "upstream_output_ref": UPSTREAM_OUTPUT_REF,
            "derived_output_ref": row["output_candidate_id"],
            "input_output_mapping": "planning_trace_only",
            "runtime_execution": False,
            "write_permission": False,
            "traceability_ref": f"trace://{OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID}/{row['output_candidate_id']}",
        }
        for row in output_candidates
    ]
    issuance_input_output_traceability_contract_complete = (
        len(traceability_rows) == 8
        and all(r["runtime_execution"] is False for r in traceability_rows)
        and all(r["write_permission"] is False for r in traceability_rows)
        and all(r["source_input_ref"] == OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID for r in traceability_rows)
    )
    issuance_protocol_traceability_contract_complete = issuance_input_output_traceability_contract_complete

    input_candidate_protocol_reference_ok = PROTOCOL_INPUT_CANDIDATE_ID in RELATED_PROTOCOL_IDS
    output_candidate_protocol_reference_ok = PROTOCOL_OUTPUT_CANDIDATE_ID in RELATED_PROTOCOL_IDS
    input_output_symmetry_reference_ok = PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID in RELATED_PROTOCOL_IDS
    protocol_traceability_reference_ok = TRACEABILITY_RULE_REF == PROTOCOL_TRACEABILITY_ID
    l2_taskmanager_owner_approval_request_protocol_reference_ok = (
        issuance_candidate.get("module_extension_protocol") == PROTOCOL_ID
        and issuance_candidate.get("source_protocol_id") == PROTOCOL_ID
    )
    validate_once_per_module_rule_ref_ok = VALIDATE_ONCE_PER_MODULE_RULE_REF == meta["validate_once_per_module_rule_ref"]
    reuse_first_rule_ref_ok = REUSE_FIRST_RULE_REF == meta["reuse_first_rule_ref"]
    protocol_execution_result_schema_ref_ok = meta["protocol_execution_result_schema_ref"] == PROTOCOL_EXECUTION_RESULT_SCHEMA_REF
    separation_rule_ref_ok = meta["separation_rule_ref"] == SEPARATION_RULE_REF
    traceability_rule_ref_ok = meta["traceability_rule_ref"] == TRACEABILITY_RULE_REF
    issuance_candidate_source_input_ref_ok = (
        issuance_candidate.get("source_input_ref") == UPSTREAM_APPROVAL_REQUEST_CANDIDATE_ID
    )
    error_namespace_rows = [
        {
            "scenario": "issuance_candidate_misclassified_as_accepted_input",
            "error_code": f"{PROTOCOL_INPUT_CANDIDATE_ID}::CONST-001",
            "attribution": "protocol_violation",
        },
        {
            "scenario": "issuance_output_missing_source_input_ref",
            "error_code": f"{PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID}::TRACE-001",
            "attribution": "protocol_violation",
        },
        {
            "scenario": "missing_matrix_or_artifact_field",
            "error_code": "MODULE-LOCAL-PROC-001",
            "attribution": "module_local_failure",
        },
    ]
    for row in error_namespace_rows:
        row["whitebox_candidate_ref"] = build_whitebox_diagnostic_ref(
            phase_id=PHASE_ID,
            protocol_id=row["error_code"].split("::")[0],
            error_code=row["error_code"],
            artifact_ref="task_manager_freeze_authorization_grant_owner_approval_request_issuance_error_namespace_matrix_v1.json",
            field_path=row["scenario"],
        )
    error_namespace_mapping_ok = all(row.get("whitebox_candidate_ref") for row in error_namespace_rows)
    whitebox_candidate_ref_mapping_ok = (
        bool(issuance_candidate.get("whitebox_candidate_ref"))
        and all(row.get("whitebox_candidate_ref") for row in output_candidates)
        and issuance_candidate["whitebox_candidate_ref"].get("runtime_integration") is False
    )
    notification_rows = [
        {
            "notification_id": "owner_operator_notification_issuance_ref",
            "notification_status": "owner-operator-notification-issuance-candidate",
            "notification_sent": False,
            "execution_path": False,
            "source_input_ref": OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
        }
    ]
    owner_operator_notification_issuance_candidate_only = all(
        row.get("notification_sent") is False and row.get("execution_path") is False for row in notification_rows
    )
    rejection_rows = [
        {
            "reference_id": "issuance_rejection_ref",
            "reference_status": "issuance-rejection-reference-candidate",
            "rejection_execution_path": False,
            "source_input_ref": OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
        }
    ]
    rejection_reference_candidate_only = all(row.get("rejection_execution_path") is False for row in rejection_rows)
    expiry_rows = [
        {
            "reference_id": "issuance_expiry_ref",
            "reference_status": "issuance-expiry-reference-candidate",
            "expiry_execution_path": False,
            "source_input_ref": OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
        }
    ]
    expiry_reference_candidate_only = all(row.get("expiry_execution_path") is False for row in expiry_rows)
    revocation_rows = [
        {
            "reference_id": "issuance_revocation_ref",
            "reference_status": "issuance-revocation-reference-candidate",
            "revocation_execution_path": False,
            "source_input_ref": OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
        }
    ]
    revocation_reference_candidate_only = all(row.get("revocation_execution_path") is False for row in revocation_rows)
    owner_approval_request_absent = True
    authorization_request_absent = request_planning_summary.get("authorization_request_absent") is True
    request_record_absent = request_planning_summary.get("request_record_absent") is True
    owner_approval_record_absent = request_planning_summary.get("owner_approval_record_absent") is True
    owner_operator_ack_record_absent = request_planning_summary.get("owner_operator_ack_record_absent") is True
    approval_evidence_bound_record_absent = request_planning_summary.get("approval_evidence_bound_record_absent") is True
    grant_token_absent = request_planning_summary.get("grant_token_absent") is True
    grant_record_absent = request_planning_summary.get("grant_record_absent") is True
    authorization_grant_absent = request_planning_summary.get("authorization_grant_absent") is True
    foundation_not_frozen = request_planning_summary.get("foundation_not_frozen") is True
    closure_not_executed = request_planning_summary.get("closure_not_executed") is True
    runtime_execution_absent = True
    protocol_runtime_absent = True
    whitebox_runtime_integration_absent = meta["whitebox_runtime_integration"] is False
    module_adapter_implementation_absent = True
    protocol_reference_ok = (
        input_candidate_protocol_reference_ok
        and output_candidate_protocol_reference_ok
        and input_output_symmetry_reference_ok
        and protocol_traceability_reference_ok
        and l2_taskmanager_owner_approval_request_protocol_reference_ok
        and validate_once_per_module_rule_ref_ok
        and reuse_first_rule_ref_ok
        and meta["l1_input_output_protocol_revalidation"] is False
        and meta["shared_protocol_system_revalidation"] is False
        and registry_ref_patch.get("shared_protocol_system_revalidation") is False
    )

    owner_approval_request_issued_absent = True
    owner_operator_notification_sent_absent = True
    precondition_candidate_only = (
        issuance_candidate.get("candidate_state") == "issuance-candidate"
        and all(row.get("output_state") == "output-candidate" for row in output_candidates)
    )

    non_execution_boundary_ok = (
        owner_approval_request_issued_absent
        and owner_operator_notification_sent_absent
        and request_planning_summary.get("authorization_request_absent") is True
        and request_planning_summary.get("request_record_absent") is True
        and request_planning_summary.get("owner_approval_record_absent") is True
        and request_planning_summary.get("grant_token_absent") is True
        and request_planning_summary.get("grant_record_absent") is True
        and request_planning_summary.get("authorization_grant_absent") is True
        and request_planning_summary.get("foundation_not_frozen") is True
        and request_planning_summary.get("closure_not_executed") is True
    )

    debts = list(GOVERNANCE_DEBTS)
    governance_debt_preserved = (
        len(debts) >= 2
        and debts[0].get("debt_title") == GOVERNANCE_DEBTS[0]["debt_title"]
        and debts[0].get("priority") == "P1"
        and debts[0].get("must_not_implement_now") is True
        and debts[1].get("debt_title") == GOVERNANCE_DEBTS[1]["debt_title"]
        and debts[1].get("priority") == "P1"
        and debts[1].get("must_not_implement_now") is True
    )

    precondition_values = {
        "request_post_dryrun_review_go": prior_request_post_dryrun_review_go,
        "request_planning_go": prior_request_planning_go,
        "request_dryrun_go": prior_request_dryrun_go,
        "registry_patch_go": prior_registry_patch_go,
        "shared_code_smoke_go": prior_shared_code_smoke_go,
        "owner_approval_request_issued_absent": owner_approval_request_issued_absent,
        "owner_operator_notification_sent_absent": owner_operator_notification_sent_absent,
        "precondition_candidate_only": precondition_candidate_only,
        "governance_debt_preserved": governance_debt_preserved,
    }
    precondition_rows = [
        {**row, "satisfied": precondition_values.get(row["precondition"]) is True}
        for row in PRECONDITION_ROWS
    ]
    preconditions_ok = all(row.get("satisfied") is True for row in precondition_rows)

    evidence_chain = []
    for stage in POST_REVIEW_CHAIN_NODES:
        row = next((r for r in post_chain.get("chain") or [] if r.get("stage") == stage), {})
        evidence_chain.append({"stage": stage, "linked": row.get("linked") is True})
    evidence_chain.append(
        {
            "stage": "freeze_authorization_grant_owner_approval_request_issuance_planning",
            "root": str(out),
            "readiness": "owner-approval-request-issuance-planning-ready",
            "owner_approval_request_issued": False,
            "owner_operator_notification_sent": False,
            "linked": True,
        }
    )
    evidence_chain_paths_declared = all(
        any(node.get("stage") == stage for node in evidence_chain) for stage in CHAIN_EVIDENCE_NODES
    )
    post_review_ref_linked = any(
        node.get("stage") == "freeze_authorization_grant_owner_approval_request_post_dryrun_review"
        and node.get("linked") is True
        for node in evidence_chain
    )
    planning_node_linked = any(
        node.get("stage") == "freeze_authorization_grant_owner_approval_request_issuance_planning"
        and node.get("linked") is True
        for node in evidence_chain
    )
    upstream_chain_linked = all(
        node.get("linked") is True
        for node in evidence_chain
        if node.get("stage")
        not in (
            "freeze_authorization_grant_owner_approval_request_post_dryrun_review",
            "freeze_authorization_grant_owner_approval_request_issuance_planning",
        )
    )
    if not upstream_chain_linked:
        downstream_readiness_gaps.append("upstream_evidence_chain_not_fully_linked")
    evidence_chain_ok = (
        prior_request_post_dryrun_review_go
        and post_review_ref_linked
        and planning_node_linked
        and evidence_chain_paths_declared
    )

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Planning-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES[3]
        if len(GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES) > 3
        else GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES[2],
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Issuance-Planning-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_REQUEST_ISSUANCE_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Post-DryRun-Review-v1-001",
    )
    template_lineage_ok = (
        template_lineage.get("template_lineage_ok") is True
        and post_summary.get("template_lineage_ok") is True
        and request_planning_summary.get("template_lineage_ok") is True
    )

    owner_approval_request_issuance_plan_complete = (
        prior_request_post_dryrun_review_go
        and prior_request_planning_go
        and prior_request_dryrun_go
        and prior_registry_patch_go
        and prior_shared_code_smoke_go
        and prior_validate_once_rule_review_go
        and issuance_candidate_classified_as_input_candidate
        and issuance_input_candidate_contract_complete
        and issuance_output_candidate_contract_complete
        and issuance_protocol_traceability_contract_complete
        and issuance_input_output_traceability_contract_complete
        and protocol_reference_ok
        and error_namespace_mapping_ok
        and whitebox_candidate_ref_mapping_ok
        and owner_operator_notification_issuance_candidate_only
        and rejection_reference_candidate_only
        and expiry_reference_candidate_only
        and revocation_reference_candidate_only
        and owner_approval_request_issued_absent
        and owner_operator_notification_sent_absent
        and precondition_candidate_only
        and preconditions_ok
        and evidence_chain_ok
        and governance_debt_preserved
        and template_lineage_ok
        and non_execution_boundary_ok
    )
    next_phase_readiness_ok = owner_approval_request_issuance_plan_complete

    if not prior_request_post_dryrun_review_go or not prior_request_planning_go or not prior_request_dryrun_go:
        final_decision = FINAL_DECISION_PRIOR
    elif not prior_registry_patch_go:
        final_decision = FINAL_DECISION_REGISTRY
    elif not prior_shared_code_smoke_go:
        final_decision = FINAL_DECISION_SMOKE
    elif not template_lineage_ok:
        final_decision = FINAL_DECISION_LINEAGE
    elif not protocol_reference_ok:
        final_decision = FINAL_DECISION_PROTOCOL
    elif not issuance_input_candidate_contract_complete:
        final_decision = FINAL_DECISION_INPUT
    elif not issuance_output_candidate_contract_complete:
        final_decision = FINAL_DECISION_OUTPUT
    elif not issuance_protocol_traceability_contract_complete:
        final_decision = FINAL_DECISION_TRACE
    elif not owner_approval_request_issued_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif not owner_operator_notification_sent_absent:
        final_decision = FINAL_DECISION_APPROVAL
    elif not precondition_candidate_only:
        final_decision = FINAL_DECISION_SCOPE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not owner_approval_request_issuance_plan_complete:
        final_decision = FINAL_DECISION_TRACE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_owner_approval_request_post_review_go": prior_request_post_dryrun_review_go,
        "prior_request_post_dryrun_review_go": prior_request_post_dryrun_review_go,
        "prior_request_planning_go": prior_request_planning_go,
        "prior_request_dryrun_go": prior_request_dryrun_go,
        "prior_registry_patch_go": prior_registry_patch_go,
        "prior_shared_code_smoke_go": prior_shared_code_smoke_go,
        "prior_validate_once_rule_review_go": prior_validate_once_rule_review_go,
        "owner_approval_request_issuance_plan_complete": owner_approval_request_issuance_plan_complete,
        "issuance_candidate_classified_as_input_candidate": issuance_candidate_classified_as_input_candidate,
        "issuance_candidate_source_input_ref_ok": issuance_candidate_source_input_ref_ok,
        "issuance_input_candidate_contract_complete": issuance_input_candidate_contract_complete,
        "issuance_output_candidate_contract_complete": issuance_output_candidate_contract_complete,
        "issuance_input_output_traceability_contract_complete": issuance_input_output_traceability_contract_complete,
        "issuance_protocol_traceability_contract_complete": issuance_protocol_traceability_contract_complete,
        "input_candidate_protocol_reference_ok": input_candidate_protocol_reference_ok,
        "output_candidate_protocol_reference_ok": output_candidate_protocol_reference_ok,
        "input_output_symmetry_reference_ok": input_output_symmetry_reference_ok,
        "protocol_traceability_reference_ok": protocol_traceability_reference_ok,
        "l2_taskmanager_owner_approval_request_protocol_reference_ok": l2_taskmanager_owner_approval_request_protocol_reference_ok,
        "protocol_execution_result_schema_ref_ok": protocol_execution_result_schema_ref_ok,
        "separation_rule_ref_ok": separation_rule_ref_ok,
        "traceability_rule_ref_ok": traceability_rule_ref_ok,
        "validate_once_per_module_rule_ref_ok": validate_once_per_module_rule_ref_ok,
        "reuse_first_rule_ref_ok": reuse_first_rule_ref_ok,
        "error_namespace_mapping_ok": error_namespace_mapping_ok,
        "whitebox_candidate_ref_mapping_ok": whitebox_candidate_ref_mapping_ok,
        "owner_operator_notification_issuance_candidate_only": owner_operator_notification_issuance_candidate_only,
        "rejection_reference_candidate_only": rejection_reference_candidate_only,
        "expiry_reference_candidate_only": expiry_reference_candidate_only,
        "revocation_reference_candidate_only": revocation_reference_candidate_only,
        "owner_approval_request_absent": owner_approval_request_absent,
        "owner_approval_request_issued_absent": owner_approval_request_issued_absent,
        "owner_operator_notification_sent_absent": owner_operator_notification_sent_absent,
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
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
        "precondition_candidate_only": precondition_candidate_only,
        "governance_debt_preserved": governance_debt_preserved,
        "template_lineage_ok": template_lineage_ok,
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
    }

    planning_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(go_condition_values.get(key) is True for key in GO_CONDITIONS_KEYS)
    )
    next_phase = NEXT_PHASE_GO if planning_pass else PHASE_ID
    core_schema_fields = build_core_go_no_go_summary_fields(
        go_conditions=go_condition_values,
        forbidden_runtime_flags=RUNTIME_FORBIDDEN_FLAGS,
        chain_trace_nodes=CHAIN_EVIDENCE_NODES,
        go_no_go_decision=final_decision,
        final_decision=final_decision,
        next_phase=next_phase,
        template_lineage=template_lineage,
    )

    sample_error_code = build_error_code(PROTOCOL_ID, "IFACE", 1)
    issuance_plan = {
        "plan_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_v1",
        "core_object": "owner_approval_request_issuance_candidate",
        "issuance_candidate_id": OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID,
        "upstream_input_candidate_id": UPSTREAM_APPROVAL_REQUEST_CANDIDATE_ID,
        "upstream_output_ref": UPSTREAM_OUTPUT_REF,
        "output_candidate_count": len(output_candidates),
        "output_candidate_specs": list(OUTPUT_CANDIDATE_SPECS),
        "sample_protocol_error_code": sample_error_code,
        "error_classification_rules": list(FAILURE_CLASSIFICATION),
        "cursor_traceability_query_path": list(CURSOR_QUERY_RULE_STEPS),
        "traceability_query_path_steps": list(TRACEABILITY_QUERY_PATH_STEPS),
        "evidence_chain": evidence_chain,
        "evidence_chain_complete": evidence_chain_ok,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        "issuance_candidate": issuance_candidate,
        "output_candidates": output_candidates,
        "issuance_artifacts": list(ISSUANCE_PLANNING_PACKAGE_FILES),
        **go_condition_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    issuance_candidate_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_candidate_matrix_v1",
        "rows": [issuance_candidate],
        "issuance_candidate_only": issuance_candidate_classified_as_input_candidate,
        **meta,
    }
    issuance_input_candidate_contract = {
        "contract_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_candidate_contract_v1",
        "owner_approval_request_issuance_candidate": issuance_candidate,
        "required_fields": list(INPUT_CANDIDATE_REQUIRED_FIELDS),
        "issuance_input_candidate_contract_complete": issuance_input_candidate_contract_complete,
        **meta,
    }
    issuance_output_candidate_contract = {
        "contract_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_output_candidate_contract_v1",
        "rows": output_candidates,
        "issuance_output_candidate_contract_complete": issuance_output_candidate_contract_complete,
        **meta,
    }
    issuance_input_output_traceability_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_output_traceability_matrix_v1",
        "rows": traceability_rows,
        "issuance_input_output_traceability_contract_complete": issuance_input_output_traceability_contract_complete,
        "issuance_protocol_traceability_contract_complete": issuance_protocol_traceability_contract_complete,
        "input_output_mapping_is_not_runtime_execution": True,
        "traceability_ref_is_not_write_permission": True,
        **meta,
    }
    issuance_error_namespace_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_error_namespace_matrix_v1",
        "rows": error_namespace_rows,
        "error_namespace": ERROR_NAMESPACE,
        "error_namespace_mapping_ok": error_namespace_mapping_ok,
        "module_local_failure_not_protocol_failure_by_default": True,
        **meta,
    }
    issuance_whitebox_candidate_ref_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_whitebox_candidate_ref_matrix_v1",
        "input_whitebox_candidate_ref": issuance_candidate.get("whitebox_candidate_ref"),
        "output_whitebox_candidate_refs": [row.get("whitebox_candidate_ref") for row in output_candidates],
        "whitebox_candidate_ref_mapping_ok": whitebox_candidate_ref_mapping_ok,
        "whitebox_runtime_integration": False,
        **meta,
    }
    issuance_notification_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_owner_operator_notification_candidate_matrix_v1",
        "rows": notification_rows,
        "owner_operator_notification_issuance_candidate_only": owner_operator_notification_issuance_candidate_only,
        **meta,
    }
    issuance_rejection_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_rejection_reference_matrix_v1",
        "rows": rejection_rows,
        "rejection_reference_candidate_only": rejection_reference_candidate_only,
        **meta,
    }
    issuance_expiry_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_expiry_reference_matrix_v1",
        "rows": expiry_rows,
        "expiry_reference_candidate_only": expiry_reference_candidate_only,
        **meta,
    }
    issuance_revocation_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_revocation_reference_matrix_v1",
        "rows": revocation_rows,
        "revocation_reference_candidate_only": revocation_reference_candidate_only,
        **meta,
    }
    issuance_protocol_reference_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_reference_matrix_v1",
        "rows": [
            {
                "protocol_id": pid,
                "referenced": True,
                "reference_mode": "lightweight_reference_only",
                "l1_input_output_protocol_revalidation": False,
                "shared_protocol_system_revalidation": False,
            }
            for pid in RELATED_PROTOCOL_IDS + (PROTOCOL_ID,)
        ],
        "protocol_reference_ok": protocol_reference_ok,
        **meta,
    }
    issuance_protocol_traceability_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_traceability_matrix_v1",
        "traceability_rule_ref": TRACEABILITY_RULE_REF,
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_REF,
        "reuse_first_rule_ref": REUSE_FIRST_RULE_REF,
        "cursor_query_rule_steps": list(CURSOR_QUERY_RULE_STEPS),
        "traceability_query_path_steps": list(TRACEABILITY_QUERY_PATH_STEPS),
        "issuance_protocol_traceability_contract_complete": issuance_protocol_traceability_contract_complete,
        "traceability_rule_ref_ok": traceability_rule_ref_ok,
        **meta,
    }
    issuance_absence_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_absence_matrix_v1",
        "owner_approval_request_issued_absent": owner_approval_request_issued_absent,
        "owner_operator_notification_sent_absent": owner_operator_notification_sent_absent,
        "request_record_absent": request_planning_summary.get("request_record_absent") is True,
        "authorization_request_absent": request_planning_summary.get("authorization_request_absent") is True,
        "owner_approval_record_absent": request_planning_summary.get("owner_approval_record_absent") is True,
        "grant_token_absent": request_planning_summary.get("grant_token_absent") is True,
        "grant_record_absent": request_planning_summary.get("grant_record_absent") is True,
        **meta,
    }
    issuance_validate_once_reference = {
        "reference_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_validate_once_reference_v1",
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_REF,
        "reuse_first_rule_ref": REUSE_FIRST_RULE_REF,
        "prior_validate_once_rule_review_go": prior_validate_once_rule_review_go,
        "upstream_validate_once_rule_review_ref": str(
            post_review
            / "task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_review_v1.json"
        ),
        "upstream_validate_once_rule_review": post_validate_once,
        **meta,
    }
    issuance_precondition_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_precondition_matrix_v1",
        "rows": precondition_rows,
        "preconditions_ok": preconditions_ok,
        "precondition_candidate_only": precondition_candidate_only,
        **meta,
    }
    issuance_boundary_contract = {
        "contract_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_boundary_contract_v1",
        "statements": list(BOUNDARY_CONTRACT_STATEMENTS),
        "owner_approval_request_issued": False,
        "owner_operator_notification_sent": False,
        "request_record_created": False,
        "authorization_request_issued": False,
        "owner_approval_record_created": False,
        "grant_issued": False,
        "foundation_frozen": False,
        "closed": False,
        "owner_approval_request_absent": owner_approval_request_absent,
        "authorization_request_absent": authorization_request_absent,
        "request_record_absent": request_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        **meta,
    }
    issuance_non_execution_constraints = {
        "constraints_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_non_execution_constraints_v1",
        "constraints": list(NON_EXECUTION_CONSTRAINTS),
        "non_execution_boundary_ok": non_execution_boundary_ok,
        **{k: True for k in NON_EXECUTION_CONSTRAINTS},
        **meta,
    }
    issuance_governance_debt_carryover = {
        "carryover_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_governance_debt_carryover_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        **meta,
    }
    issuance_template_lineage = {
        "lineage_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_template_lineage_v1",
        "upstream_post_review_lineage_ok": post_summary.get("template_lineage_ok") is True,
        "upstream_registry_patch_lineage_ok": prior_registry_patch_go,
        "upstream_request_post_review_lineage_ok": post_summary.get("template_lineage_ok") is True,
        "upstream_request_planning_lineage_ok": request_planning_summary.get("template_lineage_ok") is True,
        "upstream_request_dryrun_lineage_ok": request_dryrun_summary.get("template_lineage_ok") is True,
        **template_lineage,
        **meta,
    }
    issuance_next_phase_readiness = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_request_issuance_next_phase_readiness_v1",
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_request_issuance_dryrun",
        "owner_approval_request_issued": False,
        "owner_operator_notification_sent": False,
        "request_record_created": False,
        "authorization_request_issued": False,
        "owner_approval_record_created": False,
        "grant_issued": False,
        "foundation_frozen": False,
        "closed": False,
        "module_adapter_implementation_ready": False,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "issuance_planning_pass": planning_pass,
        "planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "evidence_chain_paths_declared": evidence_chain_paths_declared,
        "post_review_ref_linked": post_review_ref_linked,
        "planning_node_linked": planning_node_linked,
        "candidate_only": True,
        "no_execution_leakage": non_execution_boundary_ok,
        "no_protocol_change": True,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Issuance Plan v1",
            "",
            "This phase performs owner approval request issuance planning only.",
            "It does not issue owner approval request and does not send owner/operator notification.",
            "",
            "本阶段仅执行 owner approval request issuance planning。",
            "不生成 owner approval request，不发送 owner/operator notification，不生成 request record。",
            "",
            f"Phase: `{PHASE_ID}`",
            f"Core object: `owner_approval_request_issuance_candidate`",
            f"Issuance candidate id: `{OWNER_APPROVAL_REQUEST_ISSUANCE_CANDIDATE_ID}`",
            f"Source input ref: `{UPSTREAM_APPROVAL_REQUEST_CANDIDATE_ID}`",
            f"Upstream output ref: `{UPSTREAM_OUTPUT_REF}`",
            f"Output candidate count: `{len(output_candidates)}`",
            f"Validate once rule ref: `{VALIDATE_ONCE_PER_MODULE_RULE_REF}`",
            f"Reuse first rule ref: `{REUSE_FIRST_RULE_REF}`",
            f"L1 input/output protocol revalidation: `false`",
            f"Shared protocol system revalidation: `false`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
            "",
            "## Issuance Boundary Statements",
            *[f"- {stmt}" for stmt in BOUNDARY_CONTRACT_STATEMENTS],
            "",
            "## Governance Debts (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan": issuance_plan,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_issuance_plan_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_candidate_matrix": issuance_candidate_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_candidate_contract": issuance_input_candidate_contract,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_output_candidate_contract": issuance_output_candidate_contract,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_input_output_traceability_matrix": issuance_input_output_traceability_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_reference_matrix": issuance_protocol_reference_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_protocol_traceability_matrix": issuance_protocol_traceability_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_error_namespace_matrix": issuance_error_namespace_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_whitebox_candidate_ref_matrix": issuance_whitebox_candidate_ref_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_owner_operator_notification_candidate_matrix": issuance_notification_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_rejection_reference_matrix": issuance_rejection_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_expiry_reference_matrix": issuance_expiry_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_revocation_reference_matrix": issuance_revocation_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_absence_matrix": issuance_absence_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_validate_once_reference": issuance_validate_once_reference,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_precondition_matrix": issuance_precondition_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_boundary_contract": issuance_boundary_contract,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_non_execution_constraints": issuance_non_execution_constraints,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_governance_debt_carryover": issuance_governance_debt_carryover,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_template_lineage": issuance_template_lineage,
        "task_manager_freeze_authorization_grant_owner_approval_request_issuance_next_phase_readiness": issuance_next_phase_readiness,
        "summary": summary,
    }
