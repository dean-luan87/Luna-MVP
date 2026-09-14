# -*- coding: utf-8 -*-
"""Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Planning v1.

Structure inherited from grant_owner_approval_planning_v1 and grant_owner_approval_post_dryrun_review_v1
with upstream evidence from post_dryrun_review, input_output_registry_patch, and shared_code_smoke.
Protocol Standard Validate Once, Reference Many Times — light protocol reference only.
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
from capabilities.midplatform.task_manager_foundation_handoff_evaluation_template_lineage_v1 import (
    GRANT_OWNER_APPROVAL_REQUEST_PLANNING_STAGE_ADDITIONS,
    GRANT_OWNER_APPROVAL_REQUEST_PLANNING_STAGE_TERM_OVERRIDES,
    GRANT_OWNER_APPROVAL_REQUEST_PLANNING_WHITELIST_FILES,
    build_core_go_no_go_summary_fields,
    build_template_lineage,
)
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1 import (
    CHAIN_EVIDENCE_NODES as POST_REVIEW_CHAIN_NODES,
    DEFAULT_OUTPUT as DEFAULT_OWNER_APPROVAL_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    GO_CONDITIONS_KEYS as POST_REVIEW_GO_KEYS,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Planning-v1-001"
)
SCOPE = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_only"
SOURCE_CHAIN = "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_READY_FOR_DRYRUN"
)
FINAL_DECISION_PRIOR = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_PRIOR_REVIEW_GAP"
)
FINAL_DECISION_REGISTRY = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_REGISTRY_PATCH_GAP"
)
FINAL_DECISION_SMOKE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_PROTOCOL_SMOKE_GAP"
)
FINAL_DECISION_SCOPE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_APPROVAL_SCOPE_ESCALATION"
)
FINAL_DECISION_PROTOCOL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_PROTOCOL_REFERENCE_GAP"
)
FINAL_DECISION_INPUT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_INPUT_CANDIDATE_CONTRACT_GAP"
)
FINAL_DECISION_OUTPUT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_OUTPUT_CANDIDATE_CONTRACT_GAP"
)
FINAL_DECISION_TRACE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_TRACEABILITY_GAP"
)
FINAL_DECISION_REQUEST = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_AUTHORIZATION_REQUEST_LEAKAGE"
)
FINAL_DECISION_APPROVAL = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_OWNER_APPROVAL_RECORD_LEAKAGE"
)
FINAL_DECISION_FREEZE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_FREEZE_STATE_ESCALATION"
)
FINAL_DECISION_DEBT = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_GOVERNANCE_DEBT_GAP"
)
FINAL_DECISION_L1 = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_L1_PROTOCOL_SCOPE_LEAKAGE"
)
FINAL_DECISION_RUNTIME = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_RUNTIME_SCOPE_LEAKAGE"
)
FINAL_DECISION_LINEAGE = (
    "MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_BLOCKED_BY_TEMPLATE_LINEAGE_GAP"
)
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-DryRun-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Planning-Issue-Review-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1_smoke_v0"
)

PROTOCOL_STANDARD_REF = (
    "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_SHARED_CODE_SMOKE_READY_FOR_TASK_MANAGER_OWNER_APPROVAL_DRYRUN"
)
INPUT_OUTPUT_REGISTRY_PATCH_REF = (
    "MIDPLATFORM_PROTOCOL_INPUT_OUTPUT_SYMMETRY_REGISTRY_PATCH_READY_FOR_OWNER_APPROVAL_REQUEST_PLANNING"
)
PROTOCOL_ID = "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-REQUEST-V1"
CANONICAL_PARENT_PROTOCOL = PROTOCOL_INPUT_CANDIDATE_ID
RELATED_PROTOCOL_IDS: Tuple[str, ...] = (
    PROTOCOL_INPUT_CANDIDATE_ID,
    PROTOCOL_OUTPUT_CANDIDATE_ID,
    PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
    PROTOCOL_TRACEABILITY_ID,
    "LUNA-PROTO-L1-APPROVAL-ACK-V1",
    "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
    "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
    "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
)
ERROR_NAMESPACE = "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-REQUEST-V1::*"
PROTOCOL_EXECUTION_RESULT_SCHEMA_REF = "protocol_execution_result_schema_v1"
SEPARATION_RULE_REF = "Protocol Constraint vs Module Logic Separation Rule"
TRACEABILITY_RULE_REF = PROTOCOL_TRACEABILITY_ID

APPROVAL_REQUEST_CANDIDATE_ID = "approval_request_candidate_v1_001"
OUTPUT_CANDIDATE_SPECS: Tuple[Dict[str, str], ...] = (
    {"output_candidate_type": "owner_approval_request_plan_candidate", "suffix": "plan"},
    {"output_candidate_type": "owner_operator_notification_candidate", "suffix": "notification"},
    {"output_candidate_type": "owner_approval_rejection_reference_candidate", "suffix": "rejection"},
    {"output_candidate_type": "owner_approval_expiry_reference_candidate", "suffix": "expiry"},
    {"output_candidate_type": "owner_approval_revocation_reference_candidate", "suffix": "revocation"},
    {"output_candidate_type": "owner_approval_request_traceability_candidate", "suffix": "traceability"},
)

REQUEST_PLANNING_PACKAGE_FILES: Tuple[str, ...] = (
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_plan_v1.json",
    "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_plan_v1.md",
    "task_manager_freeze_authorization_grant_owner_approval_request_candidate_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_traceability_rule_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_prerequisite_matrix_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_boundary_contract_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_non_execution_constraints_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_carryover_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage_v1.json",
    "task_manager_freeze_authorization_grant_owner_approval_request_next_phase_readiness_v1.json",
    "summary.json",
    "verifier_report.json",
)
REQUEST_PLANNING_GO_NO_GO_PACK = (
    "docs/architecture/evaluation/"
    "LUNA_EVALUATION_MIDPLATFORM_TASK_MANAGER_FOUNDATION_HANDOFF_FREEZE_AUTHORIZATION_GRANT_OWNER_APPROVAL_REQUEST_PLANNING_V1_GO_NO_GO_PACK_V0.md"
)

BOUNDARY_CONTRACT_STATEMENTS: Tuple[str, ...] = (
    "owner_approval_request_planning != owner_approval_request",
    "approval_request_candidate != accepted_input",
    "approval_request_candidate != owner_approval_record",
    "approval_request_candidate != owner_approval",
    "approval_request_candidate != grant",
    "approval_request_candidate != fact",
    "approval_request_candidate != action",
    "output_candidate != accepted_output",
    "output_candidate != record",
    "output_candidate != fact",
    "output_candidate != action",
    "output_candidate != final_result",
    "input_output_mapping != runtime_execution",
    "traceability_ref != write_permission",
    "whitebox_candidate_ref != whitebox_runtime_integration",
    "owner_operator_notification_candidate != notification_sent",
    "rejection_reference_candidate != rejection_execution_path",
    "expiry_reference_candidate != expiry_execution_path",
    "revocation_reference_candidate != revocation_execution_path",
)
REQUEST_SCOPE_ROWS: Tuple[Dict[str, str], ...] = (
    {"scope": "approval_request_candidate_definition", "classification": "owner-approval-request-planning-scope"},
    {"scope": "input_candidate_contract_boundary", "classification": "owner-approval-request-planning-scope"},
    {"scope": "output_candidate_contract_boundary", "classification": "owner-approval-request-planning-scope"},
    {"scope": "input_output_traceability_boundary", "classification": "owner-approval-request-planning-scope"},
    {"scope": "protocol_reference_boundary", "classification": "owner-approval-request-planning-scope"},
    {"scope": "owner_operator_notification_candidate_boundary", "classification": "owner-approval-request-planning-scope"},
    {"scope": "rejection_expiry_revocation_reference_boundary", "classification": "owner-approval-request-planning-scope"},
    {"scope": "governance_debt_acknowledgement", "classification": "owner-approval-request-planning-scope"},
    {"scope": "non_execution_constraints", "classification": "owner-approval-request-planning-scope"},
)
PREREQUISITE_ROWS: Tuple[Dict[str, Any], ...] = (
    {"prerequisite": "owner_approval_post_review_go", "required": True},
    {"prerequisite": "input_output_registry_patch_go", "required": True},
    {"prerequisite": "shared_code_smoke_go", "required": True},
    {"prerequisite": "owner_approval_request_absent", "required": True},
    {"prerequisite": "authorization_request_absent", "required": True},
    {"prerequisite": "request_record_absent", "required": True},
    {"prerequisite": "owner_approval_record_absent", "required": True},
    {"prerequisite": "owner_operator_ack_record_absent", "required": True},
    {"prerequisite": "approval_evidence_bound_record_absent", "required": True},
    {"prerequisite": "grant_token_absent", "required": True},
    {"prerequisite": "grant_record_absent", "required": True},
    {"prerequisite": "authorization_grant_absent", "required": True},
    {"prerequisite": "foundation_not_frozen", "required": True},
    {"prerequisite": "closure_not_executed", "required": True},
    {"prerequisite": "governance_debt_preserved", "required": True},
)
NON_EXECUTION_CONSTRAINTS: Tuple[str, ...] = (
    "no_owner_approval_request_issued",
    "no_owner_approval_record",
    "no_owner_operator_ack_record",
    "no_approval_evidence_bound_record",
    "no_request_record",
    "no_authorization_request",
    "no_grant_token",
    "no_grant_record",
    "no_authorization_grant",
    "no_approval_request_notification_sent",
    "no_rejection_execution_path",
    "no_expiry_execution_path",
    "no_revocation_execution_path",
    "no_freeze_execution_path",
    "no_rollback_execution_path",
    "no_foundation_frozen",
    "no_closed_state",
    "no_foundation_finalized",
    "no_runtime_executor",
    "no_scheduler_binding",
    "no_task_execution_authority",
    "no_output_authorization",
    "no_memory_worldmodel_write_path",
    "no_module_adapter_integration",
    "no_l1_protocol_runtime_implementation",
    "no_whitebox_runtime_integration",
    "no_protocol_migration",
    "no_information_channel_governance_implementation",
    "no_protocol_governance_implementation",
    "no_closure_channel_governance_implementation",
    "no_system_protocols_integration_implementation",
)
ERROR_NAMESPACE_ROWS: Tuple[Dict[str, str], ...] = (
    {
        "scenario": "approval_request_candidate_misclassified_as_accepted_input",
        "error_code": f"{PROTOCOL_INPUT_CANDIDATE_ID}::CONST-001",
        "error_class": "CONST",
        "attribution": "protocol_violation",
    },
    {
        "scenario": "approval_request_candidate_missing_required_field",
        "error_code": f"{PROTOCOL_INPUT_CANDIDATE_ID}::IFACE-001",
        "error_class": "IFACE",
        "attribution": "protocol_violation",
    },
    {
        "scenario": "approval_request_candidate_missing_l2_field",
        "error_code": f"{PROTOCOL_ID}::IFACE-001",
        "error_class": "IFACE",
        "attribution": "protocol_violation",
    },
    {
        "scenario": "approval_request_candidate_missing_evidence_refs",
        "error_code": f"{PROTOCOL_INPUT_CANDIDATE_ID}::EVID-001",
        "error_class": "EVID",
        "attribution": "protocol_violation",
    },
    {
        "scenario": "output_candidate_missing_source_input_ref",
        "error_code": f"{PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID}::TRACE-001",
        "error_class": "TRACE",
        "attribution": "protocol_violation",
    },
    {
        "scenario": "protocol_id_not_traceable",
        "error_code": f"{PROTOCOL_TRACEABILITY_ID}::TRACE-001",
        "error_class": "TRACE",
        "attribution": "protocol_violation",
    },
    {
        "scenario": "missing_matrix_or_artifact_field",
        "error_code": "MODULE-LOCAL-PROC-001",
        "error_class": "PROC",
        "attribution": "module_local_failure",
    },
    {
        "scenario": "module_business_logic_error",
        "error_code": "MODULE-BUSINESS-001",
        "error_class": "PROC",
        "attribution": "module_business_logic_failure",
    },
)

CHAIN_EVIDENCE_NODES: Tuple[str, ...] = POST_REVIEW_CHAIN_NODES + (
    "input_output_registry_patch",
    "freeze_authorization_grant_owner_approval_request_planning",
)
GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_input_output_registry_patch_go",
    "prior_shared_code_smoke_go",
    "owner_approval_request_plan_complete",
    "grant_owner_approval_request_planning_complete",
    "approval_request_candidate_classified_as_input_candidate",
    "input_candidate_protocol_reference_ok",
    "output_candidate_protocol_reference_ok",
    "input_output_symmetry_reference_ok",
    "protocol_traceability_reference_ok",
    "l2_taskmanager_owner_approval_request_protocol_reference_ok",
    "protocol_execution_result_schema_ref_ok",
    "separation_rule_ref_ok",
    "traceability_rule_ref_ok",
    "input_candidate_contract_complete",
    "output_candidate_contract_complete",
    "input_output_traceability_contract_complete",
    "error_namespace_mapping_ok",
    "whitebox_candidate_ref_mapping_ok",
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
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
    "candidate_only",
    "prerequisite_refs_declared",
    "evidence_chain_paths_declared",
    "owner_approval_request_scope_complete",
    "no_execution_performed",
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
        "owner_approval_request_planning_only": True,
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
        "grant_owner_approval_post_dryrun_review_root": str(post_review),
        "input_output_registry_patch_root": str(registry_patch),
        "protocol_shared_code_smoke_root": str(smoke),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def _build_approval_request_candidate(
    *,
    post_review: Path,
    registry_patch: Path,
    derived_output_refs: List[str],
) -> Dict[str, Any]:
    created_at = datetime.now(timezone.utc).isoformat()
    whitebox = build_whitebox_diagnostic_ref(
        phase_id=PHASE_ID,
        protocol_id=PROTOCOL_ID,
        error_code=f"{PROTOCOL_ID}::IFACE-001",
        artifact_ref="task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_contract_v1.json",
        field_path="approval_request_candidate",
    )
    candidate: Dict[str, Any] = {
        "candidate_id": APPROVAL_REQUEST_CANDIDATE_ID,
        "candidate_type": "owner_approval_request_candidate",
        "candidate_role": "input_candidate",
        "canonical_parent_protocol": CANONICAL_PARENT_PROTOCOL,
        "module_extension_protocol": PROTOCOL_ID,
        "migration_status": "classification_only",
        "runtime_execution_allowed": False,
        "source_phase": PHASE_ID,
        "source_module": "task_manager",
        "source_artifacts": [
            str(post_review / "summary.json"),
            str(post_review / "verifier_report.json"),
            str(registry_patch / "summary.json"),
        ],
        "source_protocol_id": PROTOCOL_ID,
        "target_phase": NEXT_PHASE_GO,
        "target_module": "task_manager",
        "candidate_state": "approval-request-candidate",
        "candidate_scope": "owner-approval-request-planning-scope",
        "candidate_payload": {
            "planning_intent": "define owner approval request candidate before dry-run",
            "request_issued": False,
            "owner_approval_record_created": False,
        },
        "evidence_refs": [
            str(post_review / "task_manager_freeze_authorization_grant_owner_approval_evidence_chain_review_v1.json"),
            str(registry_patch / "input_output_protocol_reference_rule_patch_v1.json"),
        ],
        "approval_refs": [],
        "dependency_refs": [
            POST_REVIEW_FINAL_GO,
            REGISTRY_PATCH_FINAL_GO,
            PROTOCOL_STANDARD_REF,
        ],
        "ttl": "planning_only",
        "expires_at": None,
        "revocation_refs": [],
        "rejection_refs": [],
        "confidence": "planning_candidate",
        "risk_level": "planning_only",
        "write_allowed": False,
        "action_allowed": False,
        "sync_allowed": False,
        "promotion_allowed": False,
        "promotion_target": NEXT_PHASE_GO,
        "promotion_blockers": [
            "owner_approval_request_not_issued",
            "dryrun_not_executed",
            "owner_approval_record_absent",
        ],
        "constitution_refs": [CONSTRAINT_DOC_ID],
        "protocol_refs": list(RELATED_PROTOCOL_IDS) + [PROTOCOL_ID],
        "error_namespace": ERROR_NAMESPACE,
        "whitebox_candidate_ref": whitebox,
        "created_by_phase": PHASE_ID,
        "created_at": created_at,
        "final_decision_ref": FINAL_DECISION_GO,
        "derived_output_refs": derived_output_refs,
        "classified_as": "input_candidate",
    }
    return candidate


def _build_output_candidate(
    *,
    spec: Dict[str, str],
    source_input_ref: str,
    index: int,
) -> Dict[str, Any]:
    output_id = f"{spec['suffix']}_output_candidate_v1_{index:03d}"
    whitebox = build_whitebox_diagnostic_ref(
        phase_id=PHASE_ID,
        protocol_id=PROTOCOL_OUTPUT_CANDIDATE_ID,
        error_code=f"{PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID}::TRACE-001",
        artifact_ref=f"task_manager_freeze_authorization_grant_owner_approval_request_{spec['suffix']}_reference_matrix_v1.json"
        if spec["suffix"] != "plan"
        else "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_contract_v1.json",
        field_path=output_id,
    )
    return {
        "output_candidate_id": output_id,
        "output_candidate_type": spec["output_candidate_type"],
        "source_input_ref": source_input_ref,
        "source_input_candidate_id": APPROVAL_REQUEST_CANDIDATE_ID,
        "output_protocol_id": PROTOCOL_OUTPUT_CANDIDATE_ID,
        "traceability_protocol_id": PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
        "output_state": "output-candidate",
        "output_scope": "owner-approval-request-planning-scope",
        "write_allowed": False,
        "action_allowed": False,
        "sync_allowed": False,
        "promotion_allowed": False,
        "accepted_output": False,
        "record_created": False,
        "notification_sent": False,
        "execution_path": False,
        "error_namespace": ERROR_NAMESPACE,
        "whitebox_candidate_ref": whitebox,
        "created_by_phase": PHASE_ID,
        "protocol_refs": [PROTOCOL_OUTPUT_CANDIDATE_ID, PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID, PROTOCOL_TRACEABILITY_ID],
    }


def run_task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_planning_v1(
    *,
    grant_owner_approval_post_dryrun_review_root: str,
    input_output_registry_patch_root: str,
    protocol_shared_code_smoke_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    post_review = Path(grant_owner_approval_post_dryrun_review_root or DEFAULT_OWNER_APPROVAL_POST_REVIEW_ROOT).expanduser().resolve()
    registry_patch = Path(input_output_registry_patch_root or DEFAULT_REGISTRY_PATCH_ROOT).expanduser().resolve()
    smoke = Path(protocol_shared_code_smoke_root or DEFAULT_SMOKE_ROOT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out, post_review, registry_patch, smoke)
    issues: List[str] = []
    downstream_readiness_gaps: List[str] = []

    post_summary = _read_json(post_review / "summary.json")
    post_verifier = _read_json(post_review / "verifier_report.json")
    post_chain = _read_json(
        post_review / "task_manager_freeze_authorization_grant_owner_approval_evidence_chain_review_v1.json"
    )
    post_absence = _read_json(post_review / "task_manager_freeze_authorization_grant_owner_approval_absence_review_v1.json")

    registry_summary = _read_json(registry_patch / "summary.json")
    registry_verifier = _read_json(registry_patch / "verifier_report.json")
    registry_ref_patch = _read_json(registry_patch / "input_output_protocol_reference_rule_patch_v1.json")
    registry_class_patch = _read_json(registry_patch / "input_output_existing_protocol_classification_patch_v1.json")

    smoke_summary = _read_json(smoke / "summary.json")
    smoke_verifier = _read_json(smoke / "verifier_report.json")

    prior_owner_approval_post_review_go = (
        post_summary.get("final_decision") == POST_REVIEW_FINAL_GO
        and post_summary.get("recommended_next_phase") == POST_REVIEW_NEXT_PHASE
        and post_verifier.get("verifier") == "GO"
        and int(post_verifier.get("passed_checks", 0)) >= 420
        and post_verifier.get("failed_checks") == 0
        and post_verifier.get("blocker_count") == 0
        and post_summary.get("next_phase_readiness_ok") is True
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
        smoke_summary.get("final_decision") == SMOKE_FINAL_GO
        and smoke_verifier.get("verifier") == "GO"
        and int(smoke_verifier.get("passed_checks", 0)) >= 420
        and smoke_verifier.get("failed_checks") == 0
        and smoke_verifier.get("blocker_count") == 0
    )
    if not prior_shared_code_smoke_go:
        issues.append("prior_shared_code_smoke_not_go")

    output_candidates: List[Dict[str, Any]] = []
    for index, spec in enumerate(OUTPUT_CANDIDATE_SPECS, start=1):
        output_candidates.append(
            _build_output_candidate(
                spec=spec,
                source_input_ref=APPROVAL_REQUEST_CANDIDATE_ID,
                index=index,
            )
        )
    derived_output_refs = [row["output_candidate_id"] for row in output_candidates]
    approval_request_candidate = _build_approval_request_candidate(
        post_review=post_review,
        registry_patch=registry_patch,
        derived_output_refs=derived_output_refs,
    )

    registry_classifies_approval_request = any(
        row.get("object_type") == "approval_request_candidate" and row.get("classified_as") == "input_candidate"
        for row in registry_class_patch.get("new_classifications") or []
    )
    approval_request_candidate_classified_as_input_candidate = (
        approval_request_candidate.get("candidate_role") == "input_candidate"
        and approval_request_candidate.get("classified_as") == "input_candidate"
        and approval_request_candidate.get("canonical_parent_protocol") == CANONICAL_PARENT_PROTOCOL
        and approval_request_candidate.get("module_extension_protocol") == PROTOCOL_ID
        and (
            registry_ref_patch.get("approval_request_candidate_classification") == "input_candidate_type"
            or registry_classifies_approval_request
        )
    )
    input_candidate_contract_complete = all(
        field in approval_request_candidate for field in INPUT_CANDIDATE_REQUIRED_FIELDS
    ) and all(
        approval_request_candidate.get(field) is False
        for field in ("write_allowed", "action_allowed", "sync_allowed", "promotion_allowed")
    )
    if not input_candidate_contract_complete:
        issues.append("input_candidate_contract_gap")

    output_candidate_contract_complete = all(
        row.get("source_input_ref") == APPROVAL_REQUEST_CANDIDATE_ID
        and row.get("output_protocol_id") == PROTOCOL_OUTPUT_CANDIDATE_ID
        and row.get("traceability_protocol_id") == PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID
        and row.get("whitebox_candidate_ref")
        and row.get("error_namespace") == ERROR_NAMESPACE
        for row in output_candidates
    )
    if not output_candidate_contract_complete:
        issues.append("output_candidate_contract_gap")

    traceability_rows = [
        {
            "input_ref": APPROVAL_REQUEST_CANDIDATE_ID,
            "output_ref": row["output_candidate_id"],
            "source_input_ref": APPROVAL_REQUEST_CANDIDATE_ID,
            "derived_output_ref": row["output_candidate_id"],
            "input_output_mapping": "planning_trace_only",
            "runtime_execution": False,
            "traceability_ref": f"trace://{APPROVAL_REQUEST_CANDIDATE_ID}/{row['output_candidate_id']}",
            "write_permission": False,
        }
        for row in output_candidates
    ]
    input_output_traceability_contract_complete = (
        len(traceability_rows) == len(OUTPUT_CANDIDATE_SPECS)
        and all(r["source_input_ref"] == APPROVAL_REQUEST_CANDIDATE_ID for r in traceability_rows)
        and all(r["runtime_execution"] is False for r in traceability_rows)
        and len(approval_request_candidate.get("derived_output_refs") or []) == len(OUTPUT_CANDIDATE_SPECS)
    )
    if not input_output_traceability_contract_complete:
        issues.append("input_output_traceability_gap")

    protocol_reference_rows = [
        {
            "protocol_id": pid,
            "referenced": True,
            "reference_mode": "lightweight_reference_only",
            "shared_protocol_system_revalidation": False,
        }
        for pid in RELATED_PROTOCOL_IDS + (PROTOCOL_ID,)
    ]
    input_candidate_protocol_reference_ok = PROTOCOL_INPUT_CANDIDATE_ID in RELATED_PROTOCOL_IDS
    output_candidate_protocol_reference_ok = PROTOCOL_OUTPUT_CANDIDATE_ID in RELATED_PROTOCOL_IDS
    input_output_symmetry_reference_ok = PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID in RELATED_PROTOCOL_IDS
    protocol_traceability_reference_ok = TRACEABILITY_RULE_REF == PROTOCOL_TRACEABILITY_ID
    l2_taskmanager_owner_approval_request_protocol_reference_ok = (
        approval_request_candidate.get("module_extension_protocol") == PROTOCOL_ID
        and approval_request_candidate.get("source_protocol_id") == PROTOCOL_ID
    )
    protocol_execution_result_schema_ref_ok = (
        meta["protocol_execution_result_schema_ref"] == PROTOCOL_EXECUTION_RESULT_SCHEMA_REF
    )
    separation_rule_ref_ok = meta["separation_rule_ref"] == SEPARATION_RULE_REF
    traceability_rule_ref_ok = meta["traceability_rule_ref"] == TRACEABILITY_RULE_REF
    protocol_reference_ok = (
        input_candidate_protocol_reference_ok
        and output_candidate_protocol_reference_ok
        and input_output_symmetry_reference_ok
        and protocol_traceability_reference_ok
        and l2_taskmanager_owner_approval_request_protocol_reference_ok
        and protocol_execution_result_schema_ref_ok
        and separation_rule_ref_ok
        and traceability_rule_ref_ok
        and meta["shared_protocol_system_revalidation"] is False
        and registry_ref_patch.get("shared_protocol_system_revalidation") is False
    )
    if not protocol_reference_ok:
        issues.append("protocol_reference_gap")

    error_namespace_rows = []
    for row in ERROR_NAMESPACE_ROWS:
        wb = build_whitebox_diagnostic_ref(
            phase_id=PHASE_ID,
            protocol_id=row["error_code"].split("::")[0],
            error_code=row["error_code"],
            artifact_ref="task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_matrix_v1.json",
            field_path=row["scenario"],
        )
        error_namespace_rows.append({**row, "whitebox_candidate_ref": wb})
    error_namespace_mapping_ok = len(error_namespace_rows) >= 6 and all(
        r.get("whitebox_candidate_ref") for r in error_namespace_rows
    )
    whitebox_candidate_ref_mapping_ok = (
        bool(approval_request_candidate.get("whitebox_candidate_ref"))
        and all(row.get("whitebox_candidate_ref") for row in output_candidates)
        and all(row.get("whitebox_candidate_ref") for row in error_namespace_rows)
        and approval_request_candidate["whitebox_candidate_ref"].get("runtime_integration") is False
    )

    notification_rows = [
        {
            "notification_id": "owner_operator_notification_ref",
            "notification_status": "owner-operator-notification-candidate",
            "notification_sent": False,
            "execution_path": False,
            "source_input_ref": APPROVAL_REQUEST_CANDIDATE_ID,
        }
    ]
    owner_operator_notification_candidate_only = all(
        row.get("notification_status") == "owner-operator-notification-candidate"
        and row.get("notification_sent") is False
        and row.get("execution_path") is False
        for row in notification_rows
    )

    rejection_rows = [
        {
            "reference_id": "approval_rejection_ref",
            "reference_status": "rejection-reference-candidate",
            "rejection_execution_path": False,
            "source_input_ref": APPROVAL_REQUEST_CANDIDATE_ID,
        }
    ]
    rejection_reference_candidate_only = all(
        row.get("reference_status") == "rejection-reference-candidate" and row.get("rejection_execution_path") is False
        for row in rejection_rows
    )

    expiry_rows = [
        {
            "reference_id": "approval_expiry_ref",
            "reference_status": "expiry-reference-candidate",
            "expiry_execution_path": False,
            "source_input_ref": APPROVAL_REQUEST_CANDIDATE_ID,
        }
    ]
    expiry_reference_candidate_only = all(
        row.get("reference_status") == "expiry-reference-candidate" and row.get("expiry_execution_path") is False
        for row in expiry_rows
    )

    revocation_rows = [
        {
            "reference_id": "approval_revocation_ref",
            "reference_status": "revocation-reference-candidate",
            "revocation_execution_path": False,
            "source_input_ref": APPROVAL_REQUEST_CANDIDATE_ID,
        }
    ]
    revocation_reference_candidate_only = all(
        row.get("reference_status") == "revocation-reference-candidate"
        and row.get("revocation_execution_path") is False
        for row in revocation_rows
    )

    authorization_request_absent = post_absence.get("authorization_request_absent") is True
    request_record_absent = post_absence.get("request_record_absent") is True
    owner_approval_request_absent = True
    owner_approval_record_absent = post_absence.get("owner_approval_record_absent") is True
    owner_operator_ack_record_absent = post_absence.get("owner_operator_ack_record_absent") is True
    approval_evidence_bound_record_absent = post_absence.get("approval_evidence_bound_record_absent") is True
    grant_token_absent = post_absence.get("grant_token_absent") is True
    grant_record_absent = post_absence.get("grant_record_absent") is True
    authorization_grant_absent = post_absence.get("authorization_grant_absent") is True
    foundation_not_frozen = post_summary.get("foundation_not_frozen") is True
    closure_not_executed = post_summary.get("closure_not_executed") is True
    runtime_execution_absent = True
    protocol_runtime_absent = True
    whitebox_runtime_integration_absent = meta["whitebox_runtime_integration"] is False
    module_adapter_implementation_absent = True
    non_execution_boundary_ok = (
        authorization_request_absent
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

    prerequisite_values = {
        "owner_approval_post_review_go": prior_owner_approval_post_review_go,
        "input_output_registry_patch_go": prior_input_output_registry_patch_go,
        "shared_code_smoke_go": prior_shared_code_smoke_go,
        "owner_approval_request_absent": owner_approval_request_absent,
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
        "governance_debt_preserved": True,
    }
    DOWNSTREAM_PREREQUISITES = {"owner_approval_post_review_go"}
    prerequisite_rows = [
        {**row, "satisfied": prerequisite_values.get(row["prerequisite"]) is True}
        for row in PREREQUISITE_ROWS
    ]
    for row in prerequisite_rows:
        if row["prerequisite"] in DOWNSTREAM_PREREQUISITES and not row.get("satisfied"):
            if "prior_owner_approval_post_dryrun_review_not_go" not in downstream_readiness_gaps:
                downstream_readiness_gaps.append("prior_owner_approval_post_dryrun_review_not_go")
    prerequisites_ok = all(
        row.get("satisfied")
        for row in prerequisite_rows
        if row["prerequisite"] not in DOWNSTREAM_PREREQUISITES
    )
    if not prerequisites_ok:
        issues.append("prerequisite_gap")

    scope_rows = list(REQUEST_SCOPE_ROWS)
    approval_scope_planning_only = all(
        row["classification"] == "owner-approval-request-planning-scope"
        and row["classification"] not in ("approval-granted-scope", "authorized-scope")
        for row in scope_rows
    )
    if not approval_scope_planning_only:
        issues.append("approval_scope_escalation")

    evidence_chain = []
    for stage in POST_REVIEW_CHAIN_NODES:
        row = next((r for r in post_chain.get("chain") or [] if r.get("stage") == stage), {})
        evidence_chain.append({"stage": stage, "linked": row.get("linked") is True})
    evidence_chain.append(
        {
            "stage": "input_output_registry_patch",
            "root": str(registry_patch),
            "readiness": "input-output-registry-patch-ready",
            "linked": prior_input_output_registry_patch_go,
        }
    )
    evidence_chain.append(
        {
            "stage": "freeze_authorization_grant_owner_approval_request_planning",
            "root": str(out),
            "readiness": "owner-approval-request-planning-ready",
            "authorization_request_issued": False,
            "owner_approval_request_issued": False,
            "request_record": False,
            "owner_approval_record": False,
            "grant_issued": False,
            "linked": True,
        }
    )
    evidence_chain_paths_declared = len(evidence_chain) >= len(CHAIN_EVIDENCE_NODES)
    post_review_chain_linked = all(
        node.get("linked") is True
        for node in evidence_chain
        if node.get("stage") in POST_REVIEW_CHAIN_NODES
    )
    planning_node_linked = any(
        node.get("stage") == "freeze_authorization_grant_owner_approval_request_planning"
        and node.get("linked") is True
        for node in evidence_chain
    )
    registry_node_linked = any(
        node.get("stage") == "input_output_registry_patch" and node.get("linked") is True
        for node in evidence_chain
    )
    if not post_review_chain_linked:
        downstream_readiness_gaps.append("owner_approval_post_dryrun_evidence_chain_not_linked")
    evidence_chain_complete = (
        planning_node_linked
        and registry_node_linked
        and evidence_chain_paths_declared
        and prior_input_output_registry_patch_go
    )
    if not evidence_chain_complete:
        issues.append("evidence_chain_gap")

    debts = list(GOVERNANCE_DEBTS)
    governance_debt_preserved = (
        len(debts) >= 2
        and debts[0]["debt_title"] == GOVERNANCE_DEBTS[0]["debt_title"]
        and debts[0]["priority"] == "P1"
        and debts[0]["must_not_implement_now"] is True
        and debts[1]["debt_title"] == GOVERNANCE_DEBTS[1]["debt_title"]
        and debts[1]["priority"] == "P1"
        and debts[1]["must_not_implement_now"] is True
    )
    if not governance_debt_preserved:
        issues.append("governance_debt_gap")

    template_lineage = build_template_lineage(
        base_phase="Freeze-Authorization-Grant-Owner-Approval-Post-DryRun-Review-v1-001",
        base_capability=GRANT_OWNER_APPROVAL_REQUEST_PLANNING_WHITELIST_FILES[0],
        base_runner=GRANT_OWNER_APPROVAL_REQUEST_PLANNING_WHITELIST_FILES[1],
        base_verifier=GRANT_OWNER_APPROVAL_REQUEST_PLANNING_WHITELIST_FILES[2],
        base_go_no_go_pack=REQUEST_PLANNING_GO_NO_GO_PACK,
        stage_phase="Freeze-Authorization-Grant-Owner-Approval-Request-Planning-v1-001",
        stage_term_overrides=GRANT_OWNER_APPROVAL_REQUEST_PLANNING_STAGE_TERM_OVERRIDES,
        stage_additions=GRANT_OWNER_APPROVAL_REQUEST_PLANNING_STAGE_ADDITIONS,
        template_files=GRANT_OWNER_APPROVAL_REQUEST_PLANNING_WHITELIST_FILES,
        repo_root=repo_root,
        upstream_review_phase="Protocol-Input-Output-Symmetry-Registry-Patch-v1-001",
    )
    upstream_lineage_ok = (
        prior_input_output_registry_patch_go and template_lineage.get("template_lineage_ok") is True
    )
    template_lineage_ok = template_lineage.get("template_lineage_ok") is True and upstream_lineage_ok
    if not template_lineage_ok:
        issues.append("template_lineage_gap")

    owner_approval_request_plan_complete = (
        prior_input_output_registry_patch_go
        and prior_shared_code_smoke_go
        and evidence_chain_complete
        and approval_request_candidate_classified_as_input_candidate
        and input_candidate_contract_complete
        and output_candidate_contract_complete
        and input_output_traceability_contract_complete
        and protocol_reference_ok
        and error_namespace_mapping_ok
        and whitebox_candidate_ref_mapping_ok
        and owner_operator_notification_candidate_only
        and rejection_reference_candidate_only
        and expiry_reference_candidate_only
        and revocation_reference_candidate_only
        and prerequisites_ok
        and approval_scope_planning_only
        and governance_debt_preserved
        and non_execution_boundary_ok
        and template_lineage_ok
    )
    next_phase_readiness_ok = owner_approval_request_plan_complete

    if not prior_input_output_registry_patch_go:
        final_decision = FINAL_DECISION_REGISTRY
    elif not prior_shared_code_smoke_go:
        final_decision = FINAL_DECISION_SMOKE
    elif not template_lineage_ok:
        final_decision = FINAL_DECISION_LINEAGE
    elif not protocol_reference_ok:
        final_decision = FINAL_DECISION_PROTOCOL
    elif not input_candidate_contract_complete:
        final_decision = FINAL_DECISION_INPUT
    elif not output_candidate_contract_complete:
        final_decision = FINAL_DECISION_OUTPUT
    elif not input_output_traceability_contract_complete:
        final_decision = FINAL_DECISION_TRACE
    elif not authorization_request_absent or not owner_approval_request_absent:
        final_decision = FINAL_DECISION_REQUEST
    elif not owner_approval_record_absent or not owner_operator_ack_record_absent:
        final_decision = FINAL_DECISION_APPROVAL
    elif not foundation_not_frozen:
        final_decision = FINAL_DECISION_FREEZE
    elif not governance_debt_preserved:
        final_decision = FINAL_DECISION_DEBT
    elif not approval_scope_planning_only:
        final_decision = FINAL_DECISION_SCOPE
    elif not non_execution_boundary_ok:
        final_decision = FINAL_DECISION_RUNTIME
    else:
        final_decision = FINAL_DECISION_GO

    go_condition_values = {
        "prior_input_output_registry_patch_go": prior_input_output_registry_patch_go,
        "prior_shared_code_smoke_go": prior_shared_code_smoke_go,
        "owner_approval_request_plan_complete": owner_approval_request_plan_complete,
        "grant_owner_approval_request_planning_complete": False,
        "approval_request_candidate_classified_as_input_candidate": approval_request_candidate_classified_as_input_candidate,
        "input_candidate_protocol_reference_ok": input_candidate_protocol_reference_ok,
        "output_candidate_protocol_reference_ok": output_candidate_protocol_reference_ok,
        "input_output_symmetry_reference_ok": input_output_symmetry_reference_ok,
        "protocol_traceability_reference_ok": protocol_traceability_reference_ok,
        "l2_taskmanager_owner_approval_request_protocol_reference_ok": l2_taskmanager_owner_approval_request_protocol_reference_ok,
        "protocol_execution_result_schema_ref_ok": protocol_execution_result_schema_ref_ok,
        "separation_rule_ref_ok": separation_rule_ref_ok,
        "traceability_rule_ref_ok": traceability_rule_ref_ok,
        "input_candidate_contract_complete": input_candidate_contract_complete,
        "output_candidate_contract_complete": output_candidate_contract_complete,
        "input_output_traceability_contract_complete": input_output_traceability_contract_complete,
        "error_namespace_mapping_ok": error_namespace_mapping_ok,
        "whitebox_candidate_ref_mapping_ok": whitebox_candidate_ref_mapping_ok,
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
        "non_execution_boundary_ok": non_execution_boundary_ok,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        "candidate_only": True,
        "prerequisite_refs_declared": len(prerequisite_rows) >= len(PREREQUISITE_ROWS),
        "evidence_chain_paths_declared": evidence_chain_paths_declared,
        "owner_approval_request_scope_complete": approval_scope_planning_only,
        "no_execution_performed": non_execution_boundary_ok,
        "no_protocol_change": True,
    }
    planning_pass = (
        len(issues) == 0
        and final_decision == FINAL_DECISION_GO
        and all(go_condition_values.get(k) for k in GO_CONDITIONS_KEYS if k != "grant_owner_approval_request_planning_complete")
    )
    go_condition_values["grant_owner_approval_request_planning_complete"] = planning_pass
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

    boundary_contract = {
        "contract_id": "task_manager_freeze_authorization_grant_owner_approval_request_boundary_contract_v1",
        "statements": list(BOUNDARY_CONTRACT_STATEMENTS),
        "owner_approval_request_planning_only": True,
        "authorization_request_absent": authorization_request_absent,
        "owner_approval_request_absent": owner_approval_request_absent,
        "request_record_absent": request_record_absent,
        "owner_approval_record_absent": owner_approval_record_absent,
        "grant_issued": False,
        "freeze_status": "freeze-candidate",
        "foundation_frozen": False,
        "closure_applied": False,
        "closed": False,
    }

    approval_plan = {
        "plan_id": "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_plan_v1",
        "approval_scope": [
            "define approval_request_candidate as standard input_candidate before owner approval request dry-run",
            "define output_candidate contracts without accepted output / record / approval / grant",
            "define input-output traceability without runtime execution",
            "reference L1 Input/Output/Symmetry/Traceability protocols lightly",
            "overlay L2 Task Manager Owner Approval Request extension",
            "preserve governance debt carryover",
            "define non-execution constraints for future owner approval request dry-run",
        ],
        "evidence_chain": evidence_chain,
        "evidence_chain_complete": evidence_chain_complete,
        "evidence_chain_paths_declared": evidence_chain_paths_declared,
        "node_count": len(CHAIN_EVIDENCE_NODES),
        "approval_request_candidate": approval_request_candidate,
        "output_candidates": output_candidates,
        "cursor_traceability_query_path": list(CURSOR_QUERY_RULE_STEPS),
        "traceability_query_path_steps": list(TRACEABILITY_QUERY_PATH_STEPS),
        "error_classification_rules": list(FAILURE_CLASSIFICATION),
        "sample_protocol_error_code": sample_error_code,
        **go_condition_values,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }
    candidate_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_candidate_matrix_v1",
        "rows": [approval_request_candidate],
        "approval_request_candidate_only": approval_request_candidate_classified_as_input_candidate,
        **meta,
    }
    input_candidate_contract = {
        "contract_id": "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_contract_v1",
        "approval_request_candidate": approval_request_candidate,
        "required_fields": list(INPUT_CANDIDATE_REQUIRED_FIELDS),
        "input_candidate_contract_complete": input_candidate_contract_complete,
        **meta,
    }
    output_candidate_contract = {
        "contract_id": "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_contract_v1",
        "rows": output_candidates,
        "output_candidate_contract_complete": output_candidate_contract_complete,
        **meta,
    }
    traceability_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_matrix_v1",
        "rows": traceability_rows,
        "input_output_traceability_contract_complete": input_output_traceability_contract_complete,
        "input_output_mapping_is_not_runtime_execution": True,
        "traceability_ref_is_not_write_permission": True,
        **meta,
    }
    protocol_reference_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_matrix_v1",
        "rows": protocol_reference_rows,
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "input_output_registry_patch_ref": INPUT_OUTPUT_REGISTRY_PATCH_REF,
        "protocol_id": PROTOCOL_ID,
        "canonical_parent_protocol": CANONICAL_PARENT_PROTOCOL,
        "related_protocol_ids": list(RELATED_PROTOCOL_IDS),
        "shared_protocol_system_revalidation": False,
        "protocol_reference_ok": protocol_reference_ok,
        **meta,
    }
    traceability_rule_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_traceability_rule_matrix_v1",
        "traceability_rule_ref": TRACEABILITY_RULE_REF,
        "cursor_query_rule_steps": list(CURSOR_QUERY_RULE_STEPS),
        "traceability_query_path_steps": list(TRACEABILITY_QUERY_PATH_STEPS),
        "traceability_rule_ref_ok": traceability_rule_ref_ok,
        **meta,
    }
    error_namespace_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_matrix_v1",
        "rows": error_namespace_rows,
        "error_namespace": ERROR_NAMESPACE,
        "error_namespace_mapping_ok": error_namespace_mapping_ok,
        "module_local_failure_not_protocol_failure_by_default": True,
        **meta,
    }
    whitebox_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_matrix_v1",
        "input_whitebox_candidate_ref": approval_request_candidate.get("whitebox_candidate_ref"),
        "output_whitebox_candidate_refs": [row.get("whitebox_candidate_ref") for row in output_candidates],
        "error_whitebox_candidate_refs": [row.get("whitebox_candidate_ref") for row in error_namespace_rows],
        "whitebox_candidate_ref_mapping_ok": whitebox_candidate_ref_mapping_ok,
        "whitebox_runtime_integration": False,
        **meta,
    }
    notification_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_matrix_v1",
        "rows": notification_rows,
        "owner_operator_notification_candidate_only": owner_operator_notification_candidate_only,
        **meta,
    }
    rejection_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_matrix_v1",
        "rows": rejection_rows,
        "rejection_reference_candidate_only": rejection_reference_candidate_only,
        **meta,
    }
    expiry_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_matrix_v1",
        "rows": expiry_rows,
        "expiry_reference_candidate_only": expiry_reference_candidate_only,
        **meta,
    }
    revocation_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_matrix_v1",
        "rows": revocation_rows,
        "revocation_reference_candidate_only": revocation_reference_candidate_only,
        **meta,
    }
    prerequisite_matrix = {
        "matrix_id": "task_manager_freeze_authorization_grant_owner_approval_request_prerequisite_matrix_v1",
        "rows": prerequisite_rows,
        "prerequisites_ok": prerequisites_ok,
        **meta,
    }
    non_execution = {
        "constraints_id": "task_manager_freeze_authorization_grant_owner_approval_request_non_execution_constraints_v1",
        "constraints": list(NON_EXECUTION_CONSTRAINTS),
        "non_execution_boundary_ok": non_execution_boundary_ok,
        **{c: True for c in NON_EXECUTION_CONSTRAINTS},
        **meta,
    }
    debt_carryover = {
        "carryover_id": "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_carryover_v1",
        "debts": debts,
        "governance_debt_preserved": governance_debt_preserved,
        "l1_protocols_not_implemented": True,
        "system_protocols_integration_not_implemented": True,
        **meta,
    }
    template_lineage_doc = {
        "lineage_id": "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage_v1",
        "upstream_post_review_lineage_ok": post_summary.get("template_lineage_ok") is True,
        "upstream_registry_patch_lineage_ok": prior_input_output_registry_patch_go,
        **template_lineage,
        **meta,
    }
    next_phase_doc = {
        "readiness_id": "task_manager_freeze_authorization_grant_owner_approval_request_next_phase_readiness_v1",
        "recommended_next_phase": next_phase,
        "target": "freeze_authorization_grant_owner_approval_request_dryrun",
        "readiness": "freeze-authorization-grant-owner-approval-request-dryrun-ready",
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
        "module_adapter_implementation_ready": False,
        "next_phase_readiness_ok": next_phase_readiness_ok,
        **meta,
    }
    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "downstream_readiness_refs": {
            "grant_owner_approval_post_dryrun_review_root": str(post_review),
            "prior_owner_approval_post_review_go": prior_owner_approval_post_review_go,
            "post_review_final_decision": post_summary.get("final_decision"),
        },
        "downstream_chain_refs": {
            "post_review_chain_nodes": list(POST_REVIEW_CHAIN_NODES),
            "post_review_chain_linked": post_review_chain_linked,
        },
        "expected_next_phase_refs": {
            "next_phase_on_go": NEXT_PHASE_GO,
            "dryrun_readiness": "freeze-authorization-grant-owner-approval-request-dryrun-ready",
        },
        "prior_owner_approval_post_review_go": prior_owner_approval_post_review_go,
        **go_condition_values,
        **core_schema_fields,
        **meta,
    }
    markdown = "\n".join(
        [
            "# Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Plan v1",
            "",
            "This phase performs freeze authorization grant owner approval request planning only. "
            "It does not issue owner approval request, create approval records, or bind approval evidence records.",
            "",
            "本阶段仅执行 freeze authorization grant owner approval request planning，"
            "不生成真实 owner approval request，不生成 owner approval record，"
            "不生成 owner/operator ack record，不绑定 approval evidence record，"
            "不生成 request record，不发起 authorization request，不签发 grant。",
            "",
            f"Prior owner approval post-dryrun review GO: `{prior_owner_approval_post_review_go}`",
            f"Prior input/output registry patch GO: `{prior_input_output_registry_patch_go}`",
            f"Prior shared code smoke GO: `{prior_shared_code_smoke_go}`",
            f"Approval request candidate classified as input_candidate: `{approval_request_candidate_classified_as_input_candidate}`",
            f"Protocol ID: `{PROTOCOL_ID}`",
            f"Canonical parent protocol: `{CANONICAL_PARENT_PROTOCOL}`",
            f"Shared protocol system revalidation: `false`",
            f"Input candidate contract complete: `{input_candidate_contract_complete}`",
            f"Output candidate contract complete: `{output_candidate_contract_complete}`",
            f"Input-output traceability contract complete: `{input_output_traceability_contract_complete}`",
            f"Owner approval request absent: `{owner_approval_request_absent}`",
            f"Template lineage OK: `{template_lineage_ok}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase: `{next_phase}`",
            "",
            "## Owner Approval Request Planning Boundary Contract",
            *[f"- {stmt}" for stmt in BOUNDARY_CONTRACT_STATEMENTS],
            "",
            "owner approval request planning ≠ owner approval request",
            "approval_request_candidate ≠ accepted_input",
            "",
            "## Governance Debt Carryover (P1, not implemented)",
            f"- {GOVERNANCE_DEBTS[0]['debt_title']}",
            f"- {GOVERNANCE_DEBTS[1]['debt_title']}",
        ]
    )
    return {
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_plan": approval_plan,
        "task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_plan_md": markdown,
        "task_manager_freeze_authorization_grant_owner_approval_request_candidate_matrix": candidate_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_input_candidate_contract": input_candidate_contract,
        "task_manager_freeze_authorization_grant_owner_approval_request_output_candidate_contract": output_candidate_contract,
        "task_manager_freeze_authorization_grant_owner_approval_request_input_output_traceability_matrix": traceability_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_protocol_reference_matrix": protocol_reference_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_traceability_rule_matrix": traceability_rule_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_error_namespace_matrix": error_namespace_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_whitebox_candidate_ref_matrix": whitebox_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_owner_operator_notification_candidate_matrix": notification_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_rejection_reference_matrix": rejection_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_expiry_reference_matrix": expiry_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_revocation_reference_matrix": revocation_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_prerequisite_matrix": prerequisite_matrix,
        "task_manager_freeze_authorization_grant_owner_approval_request_boundary_contract": {**boundary_contract, **meta},
        "task_manager_freeze_authorization_grant_owner_approval_request_non_execution_constraints": non_execution,
        "task_manager_freeze_authorization_grant_owner_approval_request_governance_debt_carryover": debt_carryover,
        "task_manager_freeze_authorization_grant_owner_approval_request_template_lineage": template_lineage_doc,
        "task_manager_freeze_authorization_grant_owner_approval_request_next_phase_readiness": next_phase_doc,
        "summary": summary,
    }
