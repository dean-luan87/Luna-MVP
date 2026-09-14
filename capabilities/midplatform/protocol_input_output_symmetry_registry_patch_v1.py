# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Input-Output Symmetry Registry Patch v1.

Lightweight registry patch: register Input Candidate Governance, Output Candidate Governance,
and Input-Output Symmetry as L1 protocol standards. No runtime, no protocol migration, no module logic.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.protocol_canonical_standard_planning_v1 import (
    DEFAULT_OUTPUT as DEFAULT_PLANNING_ROOT,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GOVERNANCE_DEBTS,
)
from capabilities.midplatform.protocol_canonical_standard_shared_code_smoke_v1 import (
    DEFAULT_OUTPUT as DEFAULT_SMOKE_ROOT,
    FINAL_DECISION_GO as SMOKE_FINAL_GO,
)
from capabilities.midplatform.protocols.protocol_error_codes_v1 import build_error_code, validate_error_code
from capabilities.midplatform.protocols.protocol_registry_v1 import (
    INPUT_OUTPUT_SYMMETRY_PROTOCOL_IDS,
    build_input_output_symmetry_protocol_headers,
    register_input_output_symmetry_protocol_patch,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import (
    RULE_NAME_EN as SEPARATION_RULE_NAME_EN,
    RULE_NAME_ZH as SEPARATION_RULE_NAME_ZH,
    build_separation_rule_document,
)
from capabilities.midplatform.protocols.protocol_whitebox_binding_v1 import build_whitebox_diagnostic_ref
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_post_dryrun_review_v1 import (
    DEFAULT_OUTPUT as DEFAULT_POST_REVIEW_ROOT,
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Protocol-Input-Output-Symmetry-Registry-Patch-v1-001"
SCOPE = "midplatform_protocol_input_output_symmetry_registry_patch_only"
SOURCE_CHAIN = "midplatform_protocol_input_output_symmetry_registry_patch_v1"
PRINCIPLE_EN = "Protocol Standard Validate Once, Reference Many Times"
PRINCIPLE_ZH = "协议标准一次验证，多处引用"
SEPARATION_RULE_REF = "Protocol Constraint vs Module Logic Separation Rule"
PROTOCOL_STANDARD_REF = (
    "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_SHARED_CODE_SMOKE_READY_FOR_TASK_MANAGER_OWNER_APPROVAL_DRYRUN"
)
FINAL_DECISION_GO = (
    "MIDPLATFORM_PROTOCOL_INPUT_OUTPUT_SYMMETRY_REGISTRY_PATCH_READY_FOR_OWNER_APPROVAL_REQUEST_PLANNING"
)
FINAL_DECISION_BLOCKED = "MIDPLATFORM_PROTOCOL_INPUT_OUTPUT_SYMMETRY_REGISTRY_PATCH_BLOCKED"
NEXT_PHASE_GO = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Planning-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_protocol_input_output_symmetry_registry_patch_v1_smoke_v0"
)

PROTOCOL_INPUT_CANDIDATE_ID = "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1"
PROTOCOL_OUTPUT_CANDIDATE_ID = "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1"
PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID = "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1"
PROTOCOL_TRACEABILITY_ID = "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1"
REGISTRY_PATCH_PROTOCOL_IDS: Tuple[str, ...] = (
    PROTOCOL_INPUT_CANDIDATE_ID,
    PROTOCOL_OUTPUT_CANDIDATE_ID,
    PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
    PROTOCOL_TRACEABILITY_ID,
)
PROTOCOL_EXECUTION_RESULT_SCHEMA_REF = "protocol_execution_result_schema_v1"
GOVERNANCE_DEBT_REF = (
    "protocol_canonical_standard_planning_v1.GOVERNANCE_DEBTS+input_output_symmetry_canonicalization_debt"
)

SHARED_L1_PROTOCOL_REFS: Tuple[str, ...] = (
    "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
    "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
    "LUNA-PROTO-L1-APPROVAL-ACK-V1",
    "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
    "LUNA-PROTO-L1-FIELD-SCHEMA-V1",
    "LUNA-PROTO-L1-PROTOCOL-ASSIMILATION-V1",
)

PROTOCOL_DEPENDENCY_GRAPH: Dict[str, Dict[str, Tuple[str, ...]]] = {
    PROTOCOL_INPUT_CANDIDATE_ID: {
        "upstream_protocol_refs": (
            "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
            "LUNA-PROTO-L1-FIELD-SCHEMA-V1",
            "LUNA-PROTO-L1-PROTOCOL-ASSIMILATION-V1",
        ),
        "downstream_protocol_refs": (
            PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
            "LUNA-PROTO-L1-APPROVAL-ACK-V1",
            "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
            "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-REQUEST-V1",
        ),
        "related_protocol_ids": (
            "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
            "LUNA-PROTO-L1-FIELD-SCHEMA-V1",
            "LUNA-PROTO-L1-PROTOCOL-ASSIMILATION-V1",
            "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
            PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
        ),
    },
    PROTOCOL_OUTPUT_CANDIDATE_ID: {
        "upstream_protocol_refs": (
            PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
            PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
            "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
        ),
        "downstream_protocol_refs": (
            "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
            "LUNA-PROTO-L2-MEMORY-CANDIDATE-V1",
            "LUNA-PROTO-L2-WORLDMODEL-ENTRY-CANDIDATE-V1",
            "LUNA-PROTO-L2-PERMISSION-CANDIDATE-V1",
            "LUNA-PROTO-L2-NAVIGATION-DECISION-CANDIDATE-V1",
        ),
        "related_protocol_ids": (
            PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
            "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
            "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
            PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        ),
    },
    PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID: {
        "upstream_protocol_refs": (
            PROTOCOL_INPUT_CANDIDATE_ID,
            PROTOCOL_OUTPUT_CANDIDATE_ID,
            "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
            "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
            "LUNA-PROTO-L1-FIELD-SCHEMA-V1",
            "LUNA-PROTO-L1-PROTOCOL-ASSIMILATION-V1",
        ),
        "downstream_protocol_refs": (
            "LUNA-PROTO-L1-APPROVAL-ACK-V1",
            "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
            PROTOCOL_TRACEABILITY_ID,
            "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-REQUEST-V1",
        ),
        "related_protocol_ids": (
            PROTOCOL_INPUT_CANDIDATE_ID,
            PROTOCOL_OUTPUT_CANDIDATE_ID,
            "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
            "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
            "LUNA-PROTO-L1-APPROVAL-ACK-V1",
            "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
            PROTOCOL_TRACEABILITY_ID,
        ),
    },
    PROTOCOL_TRACEABILITY_ID: {
        "upstream_protocol_refs": (
            PROTOCOL_INPUT_CANDIDATE_ID,
            PROTOCOL_OUTPUT_CANDIDATE_ID,
            PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
            "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
            "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
            "LUNA-PROTO-L1-PROTOCOL-ASSIMILATION-V1",
        ),
        "downstream_protocol_refs": (
            "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
            "LUNA-PROTO-L1-APPROVAL-ACK-V1",
            "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-REQUEST-V1",
        ),
        "related_protocol_ids": (
            PROTOCOL_INPUT_CANDIDATE_ID,
            PROTOCOL_OUTPUT_CANDIDATE_ID,
            PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
            "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
            "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
            "LUNA-PROTO-L1-APPROVAL-ACK-V1",
            "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
            "LUNA-PROTO-L1-PROTOCOL-ASSIMILATION-V1",
        ),
    },
}

LEGACY_INPUT_CONSOLIDATION_ENTRIES: Tuple[Dict[str, str], ...] = (
    {"legacy_candidate_name": "grant_request_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-GRANT-REQUEST-V1", "source_module": "task_manager", "source_phase_family": "Freeze-Authorization-Grant-Request", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "request_issuance_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-REQUEST-ISSUANCE-V1", "source_module": "task_manager", "source_phase_family": "Freeze-Authorization-Grant-Request-Issuance", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "request_record_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-REQUEST-RECORD-V1", "source_module": "task_manager", "source_phase_family": "Freeze-Authorization-Grant-Request-Record", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "owner_approval_request_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-REQUEST-V1", "source_module": "task_manager", "source_phase_family": "Freeze-Authorization-Grant-Owner-Approval-Request", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "owner_approval_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-V1", "source_module": "task_manager", "source_phase_family": "Freeze-Authorization-Grant-Owner-Approval", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "owner_operator_ack_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-OWNER-OPERATOR-ACK-V1", "source_module": "task_manager", "source_phase_family": "Freeze-Authorization-Grant-Owner-Approval", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "approval_evidence_binding_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-APPROVAL-EVIDENCE-BINDING-V1", "source_module": "task_manager", "source_phase_family": "Freeze-Authorization-Grant-Owner-Approval", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "request_record_binding_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-REQUEST-RECORD-BINDING-V1", "source_module": "task_manager", "source_phase_family": "Freeze-Authorization-Grant-Owner-Approval", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "freeze_authorization_grant_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-FREEZE-AUTHORIZATION-GRANT-V1", "source_module": "task_manager", "source_phase_family": "Freeze-Authorization-Grant", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "closure_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-CLOSURE-V1", "source_module": "task_manager", "source_phase_family": "Foundation-Handoff-Closure", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "foundation_freeze_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-FOUNDATION-FREEZE-V1", "source_module": "task_manager", "source_phase_family": "Foundation-Handoff-Freeze", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "frame_candidate", "module_extension_protocol": "LUNA-PROTO-L2-VISION-FRAME-CANDIDATE-V1", "source_module": "vision", "source_phase_family": "Vision-Frame", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "focus_candidate", "module_extension_protocol": "LUNA-PROTO-L2-VISION-FOCUS-CANDIDATE-V1", "source_module": "vision", "source_phase_family": "Vision-Focus", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "visual_evidence_candidate", "module_extension_protocol": "LUNA-PROTO-L2-VISION-VISUAL-EVIDENCE-CANDIDATE-V1", "source_module": "vision", "source_phase_family": "Vision-Evidence", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "text_candidate", "module_extension_protocol": "LUNA-PROTO-L2-OCR-TEXT-CANDIDATE-V1", "source_module": "ocr", "source_phase_family": "OCR-Text", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "route_candidate", "module_extension_protocol": "LUNA-PROTO-L2-NAVIGATION-ROUTE-CANDIDATE-V1", "source_module": "navigation", "source_phase_family": "Navigation-Route", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "world_model_entry_candidate", "module_extension_protocol": "LUNA-PROTO-L2-WORLDMODEL-ENTRY-CANDIDATE-V1", "source_module": "worldmodel", "source_phase_family": "WorldModel-Entry", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "memory_candidate", "module_extension_protocol": "LUNA-PROTO-L2-MEMORY-CANDIDATE-V1", "source_module": "memory", "source_phase_family": "Memory", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "permission_candidate", "module_extension_protocol": "LUNA-PROTO-L2-PERMISSION-CANDIDATE-V1", "source_module": "permission", "source_phase_family": "Permission", "candidate_role": "input_candidate"},
    {"legacy_candidate_name": "health_signal_candidate", "module_extension_protocol": "LUNA-PROTO-L2-HEALTH-SIGNAL-V1", "source_module": "health", "source_phase_family": "Health-Signal", "candidate_role": "input_candidate"},
)

LEGACY_OUTPUT_CONSOLIDATION_ENTRIES: Tuple[Dict[str, str], ...] = (
    {"legacy_candidate_name": "request_record_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-REQUEST-RECORD-V1", "producing_module": "task_manager", "producing_phase_family": "Freeze-Authorization-Grant-Request-Record", "candidate_role": "output_candidate"},
    {"legacy_candidate_name": "owner_approval_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-V1", "producing_module": "task_manager", "producing_phase_family": "Freeze-Authorization-Grant-Owner-Approval", "candidate_role": "output_candidate"},
    {"legacy_candidate_name": "grant_candidate", "module_extension_protocol": "LUNA-PROTO-L2-TASKMANAGER-GRANT-V1", "producing_module": "task_manager", "producing_phase_family": "Freeze-Authorization-Grant", "candidate_role": "output_candidate"},
    {"legacy_candidate_name": "decision_candidate", "module_extension_protocol": "LUNA-PROTO-L2-NAVIGATION-DECISION-CANDIDATE-V1", "producing_module": "navigation", "producing_phase_family": "Navigation-Decision", "candidate_role": "output_candidate"},
    {"legacy_candidate_name": "world_model_entry_candidate", "module_extension_protocol": "LUNA-PROTO-L2-WORLDMODEL-ENTRY-CANDIDATE-V1", "producing_module": "worldmodel", "producing_phase_family": "WorldModel-Entry", "candidate_role": "output_candidate"},
    {"legacy_candidate_name": "memory_write_candidate", "module_extension_protocol": "LUNA-PROTO-L2-MEMORY-WRITE-CANDIDATE-V1", "producing_module": "memory", "producing_phase_family": "Memory-Write", "candidate_role": "output_candidate"},
    {"legacy_candidate_name": "route_decision_candidate", "module_extension_protocol": "LUNA-PROTO-L2-NAVIGATION-ROUTE-DECISION-CANDIDATE-V1", "producing_module": "navigation", "producing_phase_family": "Navigation-Route-Decision", "candidate_role": "output_candidate"},
    {"legacy_candidate_name": "visual_observation_candidate", "module_extension_protocol": "LUNA-PROTO-L2-VISION-VISUAL-OBSERVATION-CANDIDATE-V1", "producing_module": "vision", "producing_phase_family": "Vision-Observation", "candidate_role": "output_candidate"},
    {"legacy_candidate_name": "text_candidate", "module_extension_protocol": "LUNA-PROTO-L2-OCR-TEXT-CANDIDATE-V1", "producing_module": "ocr", "producing_phase_family": "OCR-Text", "candidate_role": "output_candidate"},
    {"legacy_candidate_name": "health_signal_candidate", "module_extension_protocol": "LUNA-PROTO-L2-HEALTH-SIGNAL-V1", "producing_module": "health", "producing_phase_family": "Health-Signal", "candidate_role": "output_candidate"},
)

LEGACY_DUAL_ROLE_ENTRIES: Tuple[Dict[str, Any], ...] = (
    {"candidate_name": "request_record_candidate", "allowed_roles": ["input_candidate", "output_candidate"], "role_switch_requires_traceability": True, "source_input_ref_required_when_output": True, "upstream_output_ref_required_when_input": True},
    {"candidate_name": "owner_approval_candidate", "allowed_roles": ["input_candidate", "output_candidate"], "role_switch_requires_traceability": True, "source_input_ref_required_when_output": True, "upstream_output_ref_required_when_input": True},
    {"candidate_name": "text_candidate", "allowed_roles": ["input_candidate", "output_candidate"], "role_switch_requires_traceability": True, "source_input_ref_required_when_output": True, "upstream_output_ref_required_when_input": True},
    {"candidate_name": "world_model_entry_candidate", "allowed_roles": ["input_candidate", "output_candidate"], "role_switch_requires_traceability": True, "source_input_ref_required_when_output": True, "upstream_output_ref_required_when_input": True},
    {"candidate_name": "health_signal_candidate", "allowed_roles": ["input_candidate", "output_candidate"], "role_switch_requires_traceability": True, "source_input_ref_required_when_output": True, "upstream_output_ref_required_when_input": True},
)

REQUIRED_LEGACY_INPUT_NAMES: Tuple[str, ...] = tuple(e["legacy_candidate_name"] for e in LEGACY_INPUT_CONSOLIDATION_ENTRIES)
REQUIRED_LEGACY_OUTPUT_NAMES: Tuple[str, ...] = tuple(e["legacy_candidate_name"] for e in LEGACY_OUTPUT_CONSOLIDATION_ENTRIES)
REQUIRED_DUAL_ROLE_NAMES: Tuple[str, ...] = tuple(e["candidate_name"] for e in LEGACY_DUAL_ROLE_ENTRIES)

INPUT_CANDIDATE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "candidate_id",
    "candidate_type",
    "source_phase",
    "source_module",
    "source_artifacts",
    "source_protocol_id",
    "target_phase",
    "target_module",
    "candidate_state",
    "candidate_scope",
    "candidate_payload",
    "evidence_refs",
    "approval_refs",
    "dependency_refs",
    "ttl",
    "expires_at",
    "revocation_refs",
    "rejection_refs",
    "confidence",
    "risk_level",
    "write_allowed",
    "action_allowed",
    "sync_allowed",
    "promotion_allowed",
    "promotion_target",
    "promotion_blockers",
    "constitution_refs",
    "protocol_refs",
    "error_namespace",
    "whitebox_candidate_ref",
    "created_by_phase",
    "created_at",
    "final_decision_ref",
)

OUTPUT_CANDIDATE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "output_candidate_id",
    "output_candidate_type",
    "source_input_ref",
    "source_input_candidate_id",
    "source_phase",
    "source_module",
    "producing_phase",
    "producing_module",
    "output_state",
    "output_scope",
    "output_payload",
    "derived_from_evidence_refs",
    "protocol_execution_result_ref",
    "checker_result_ref",
    "evidence_refs",
    "approval_refs",
    "ttl",
    "expires_at",
    "revocation_refs",
    "rejection_refs",
    "confidence",
    "risk_level",
    "write_allowed",
    "action_allowed",
    "sync_allowed",
    "promotion_allowed",
    "promotion_target",
    "promotion_blockers",
    "protocol_refs",
    "error_namespace",
    "whitebox_candidate_ref",
    "created_by_phase",
    "created_at",
    "final_decision_ref",
)

TRACEABILITY_REQUIRED_FIELDS: Tuple[str, ...] = (
    "input_ref",
    "input_candidate_id",
    "input_candidate_type",
    "input_protocol_id",
    "input_error_namespace",
    "input_evidence_refs",
    "input_whitebox_candidate_ref",
    "process_ref",
    "phase_id",
    "module_id",
    "capability_id",
    "protocol_execution_result_ref",
    "checker_result_ref",
    "output_ref",
    "output_candidate_id",
    "output_candidate_type",
    "output_protocol_id",
    "output_error_namespace",
    "output_evidence_refs",
    "output_whitebox_candidate_ref",
    "source_input_ref",
    "derived_output_refs",
    "reverse_trace_ref",
    "lineage_status",
)

BOUNDARY_CONTRACT_STATEMENTS: Tuple[str, ...] = (
    "input_candidate != accepted_input",
    "input_candidate != record",
    "input_candidate != approval",
    "input_candidate != grant",
    "input_candidate != fact",
    "input_candidate != action",
    "output_candidate != accepted_output",
    "output_candidate != record",
    "result_candidate != final_result",
    "record_candidate != record",
    "input_output_mapping != runtime_execution",
    "traceability_ref != write_permission",
    "whitebox_candidate_ref != whitebox_runtime_integration",
)

INPUT_CANDIDATE_ERROR_CODES: Tuple[str, ...] = (
    "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1::CONST-001",
    "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1::IFACE-001",
    "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1::EVID-001",
    "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1::STATE-001",
    "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1::TTL-001",
    "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1::AUTH-001",
    "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1::ASSIM-001",
)

OUTPUT_CANDIDATE_ERROR_CODES: Tuple[str, ...] = (
    "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1::CONST-001",
    "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1::IFACE-001",
    "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1::STATE-001",
    "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1::EVID-001",
)

SYMMETRY_ERROR_CODES: Tuple[str, ...] = (
    "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1::TRACE-001",
    "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1::IFACE-001",
    "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1::STATE-001",
    "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1::EVID-001",
    "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1::ASSIM-001",
    "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1::WB-001",
)

TRACEABILITY_ERROR_CODES: Tuple[str, ...] = (
    "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1::TRACE-001",
    "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1::TRACE-002",
    "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1::TRACE-003",
    "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1::TRACE-004",
    "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1::TRACE-005",
    "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1::TRACE-006",
    "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1::ASSIM-001",
    "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1::WB-001",
)

TRACEABILITY_RULE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "trace_id",
    "trace_type",
    "source_error_code",
    "source_protocol_id",
    "source_phase_id",
    "source_artifact_ref",
    "source_field_path",
    "source_candidate_ref",
    "source_input_ref",
    "derived_output_refs",
    "upstream_protocol_refs",
    "downstream_protocol_refs",
    "evidence_refs",
    "protocol_execution_result_ref",
    "whitebox_candidate_ref",
    "diagnostic_node_ref",
    "recommended_action",
    "trace_status",
    "trace_blockers",
)

TRACEABILITY_QUERY_PATH_STEPS: Tuple[Dict[str, str], ...] = (
    {"step": "1", "path": "error_code → protocol_id"},
    {"step": "2", "path": "protocol_id → protocol registration"},
    {"step": "3", "path": "protocol_id → error_namespace / error_class"},
    {"step": "4", "path": "error_code → error_class / severity / recommended_action"},
    {"step": "5", "path": "artifact_ref + field_path → failing phase / failing artifact"},
    {"step": "6", "path": "candidate_ref → candidate role / candidate state"},
    {"step": "7", "path": "candidate_ref → source_input_ref / derived_output_refs"},
    {"step": "8", "path": "source_input_ref → upstream phase / upstream artifact / upstream protocol"},
    {"step": "9", "path": "derived_output_refs → downstream phase / downstream artifact / downstream protocol"},
    {"step": "10", "path": "protocol_id → upstream_protocol_refs / downstream_protocol_refs"},
    {"step": "11", "path": "evidence_refs → evidence chain / verifier report / summary"},
    {"step": "12", "path": "whitebox_candidate_ref → diagnostic candidate node"},
    {"step": "13", "path": "governance_debt_ref → known missing protocol / must_not_implement_now"},
    {"step": "14", "path": "separation_rule_ref → protocol violation vs module implementation failure"},
)

ERROR_CLASS_TRACE_RULES: Tuple[Dict[str, str], ...] = (
    {"error_class": "CONST", "trace_priority": "constitution_refs / boundary_contract / non_execution_constraints"},
    {"error_class": "PROC", "trace_priority": "module local artifact / runner / verifier / missing matrix"},
    {"error_class": "IFACE", "trace_priority": "schema / field_path / protocol header"},
    {"error_class": "ASSIM", "trace_priority": "protocol assimilation / downstream interpretation"},
    {"error_class": "EVID", "trace_priority": "evidence_refs / source_artifacts / verifier_report"},
    {"error_class": "STATE", "trace_priority": "lifecycle / state transition / candidate-role mapping"},
    {"error_class": "AUTH", "trace_priority": "approval_refs / owner_operator_ack / permission boundary"},
    {"error_class": "TTL", "trace_priority": "ttl / expires_at / revocation_refs / rejection_refs"},
    {"error_class": "WB", "trace_priority": "whitebox_candidate_ref / diagnostic_node_ref"},
    {"error_class": "HEALTH", "trace_priority": "health monitor / drift / fallback / quarantine"},
)

CURSOR_QUERY_RULE_STEPS: Tuple[str, ...] = (
    "confirm error_code exists",
    "parse protocol_id and error_class from error_code",
    "query protocol registry for L0/L1/L2/L3 layer",
    "classify error_class: constitution / process / interface / assimilation / evidence / state / auth / ttl / whitebox / health",
    "if protocol violation: trace upstream_protocol_refs and downstream_protocol_refs",
    "if module local PROC failure: locate module artifact/runner/verifier; do not default to protocol layer",
    "if candidate_ref exists: query source_input_ref and derived_output_refs",
    "if evidence_refs exist: query summary / verifier_report / artifact path",
    "if whitebox_candidate_ref exists: generate diagnostic candidate only; no real whitebox runtime",
    "output trace_status, trace_blockers, recommended_action",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "prior_protocol_standard_planning_go",
    "prior_shared_code_smoke_go",
    "input_candidate_protocol_registered",
    "output_candidate_protocol_registered",
    "input_output_symmetry_protocol_registered",
    "input_candidate_field_contract_complete",
    "output_candidate_field_contract_complete",
    "input_output_traceability_contract_complete",
    "input_output_error_namespace_mapping_complete",
    "input_output_whitebox_candidate_ref_mapping_complete",
    "protocol_reference_rule_patch_complete",
    "existing_protocol_classification_patch_complete",
    "input_output_governance_debt_patch_complete",
    "input_output_protocol_dependency_graph_complete",
    "legacy_input_protocol_consolidation_complete",
    "legacy_output_protocol_consolidation_complete",
    "legacy_candidate_role_dual_mapping_complete",
    "protocol_full_metadata_complete",
    "protocol_traceability_governance_registered",
    "protocol_traceability_rule_contract_complete",
    "protocol_traceability_query_path_contract_complete",
    "protocol_traceability_error_to_source_mapping_complete",
    "protocol_traceability_candidate_lineage_mapping_complete",
    "protocol_traceability_whitebox_candidate_mapping_complete",
    "protocol_traceability_cursor_query_rule_complete",
    "protocol_traceability_runtime_absent",
    "runtime_execution_absent",
    "protocol_migration_absent",
    "whitebox_runtime_integration_absent",
    "module_adapter_implementation_absent",
    "authorization_request_absent",
    "request_record_absent",
    "owner_approval_record_absent",
    "grant_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "non_execution_boundary_ok",
    "next_phase_readiness_ok",
)

RUNTIME_FORBIDDEN_FLAGS: Tuple[str, ...] = (
    "runtime_executor_created_now",
    "scheduler_binding_created_now",
    "task_execution_authority_granted_now",
    "output_authorization_granted_now",
    "module_adapter_integration_created_now",
    "information_channel_governance_implemented_now",
    "protocol_governance_implemented_now",
    "closure_channel_governance_implemented_now",
    "system_protocols_integration_implemented_now",
    "authorization_request_created_now",
    "authorization_grant_created_now",
    "grant_token_created_now",
    "grant_record_created_now",
    "owner_approval_record_created_now",
    "protocol_migration_executed_now",
    "whitebox_runtime_integrated_now",
    "l1_protocol_runtime_implemented_now",
)


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _meta(out: Path, planning: Path, smoke: Path, post_review: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "principle_en": PRINCIPLE_EN,
        "principle_zh": PRINCIPLE_ZH,
        "separation_rule_ref": SEPARATION_RULE_REF,
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "shared_protocol_system_revalidation": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "registry_patch_only": True,
        "protocol_migration_executed": False,
        "whitebox_runtime_integrated": False,
        "l1_protocol_runtime_implemented": False,
        "production_ready_declared": False,
        "output_root": str(out),
        "planning_root": str(planning),
        "shared_code_smoke_root": str(smoke),
        "owner_approval_post_review_root": str(post_review),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def _build_whitebox_mapping(protocol_id: str, error_codes: Tuple[str, ...]) -> Dict[str, Any]:
    mappings = []
    for code in error_codes:
        mappings.append(
            {
                "error_code": code,
                "whitebox_candidate_ref": build_whitebox_diagnostic_ref(
                    phase_id=PHASE_ID,
                    protocol_id=protocol_id,
                    error_code=code,
                    artifact_ref="summary.json",
                    field_path="go_conditions",
                ),
            }
        )
    return {
        "protocol_id": protocol_id,
        "whitebox_candidate_ref_mapping": mappings,
        "binding_mode": "contract_only",
        "runtime_integration": False,
    }


def _build_protocol_registration(
    protocol_id: str,
    header_dict: Dict[str, Any],
    registered: Dict[str, Any],
    deps: Dict[str, Tuple[str, ...]],
) -> Dict[str, Any]:
    error_codes = {
        PROTOCOL_INPUT_CANDIDATE_ID: INPUT_CANDIDATE_ERROR_CODES,
        PROTOCOL_OUTPUT_CANDIDATE_ID: OUTPUT_CANDIDATE_ERROR_CODES,
        PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID: SYMMETRY_ERROR_CODES,
        PROTOCOL_TRACEABILITY_ID: TRACEABILITY_ERROR_CODES,
    }.get(protocol_id, ())
    whitebox_mapping = _build_whitebox_mapping(protocol_id, error_codes)
    return {
        "registration_id": f"{protocol_id.lower().replace('-', '_')}_registration_v1",
        "protocol_id": protocol_id,
        "protocol_layer": header_dict.get("protocol_layer"),
        "protocol_domain": header_dict.get("protocol_domain"),
        "protocol_version": "V1",
        "protocol_name": header_dict.get("protocol_name"),
        "governance_level": header_dict.get("governance_level"),
        "error_namespace": header_dict.get("error_code_namespace"),
        "error_code_set": list(error_codes),
        "protocol_execution_result_schema_ref": PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "separation_rule_ref": SEPARATION_RULE_REF,
        "governance_debt_ref": GOVERNANCE_DEBT_REF,
        "upstream_protocol_refs": list(deps.get("upstream_protocol_refs", ())),
        "downstream_protocol_refs": list(deps.get("downstream_protocol_refs", ())),
        "related_protocol_ids": list(deps.get("related_protocol_ids", ())),
        "whitebox_candidate_ref_mapping": whitebox_mapping,
        "whitebox_binding_required": header_dict.get("whitebox_binding_required"),
        "runtime_execution_allowed": header_dict.get("runtime_execution_allowed"),
        "registered": registered is not None and bool(registered),
        "registry_entry": registered,
        "must_not_implement_now": True,
        "classification_only": True,
        "must_not_migrate_now": True,
    }


def _build_legacy_input_consolidation_map() -> Dict[str, Any]:
    entries = []
    for row in LEGACY_INPUT_CONSOLIDATION_ENTRIES:
        entries.append(
            {
                **row,
                "canonical_parent_protocol": PROTOCOL_INPUT_CANDIDATE_ID,
                "migration_status": "classification_only",
                "must_not_migrate_now": True,
            }
        )
    return {
        "map_id": "legacy_input_protocol_consolidation_map_v1",
        "consolidation_mode": "classification_only",
        "must_not_migrate_now": True,
        "must_not_rewrite_historical_artifacts": True,
        "is_runtime_registry": False,
        "entry_count": len(entries),
        "entries": entries,
    }


def _build_legacy_output_consolidation_map() -> Dict[str, Any]:
    entries = []
    for row in LEGACY_OUTPUT_CONSOLIDATION_ENTRIES:
        entries.append(
            {
                **row,
                "canonical_parent_protocol": PROTOCOL_OUTPUT_CANDIDATE_ID,
                "migration_status": "classification_only",
                "must_not_migrate_now": True,
            }
        )
    return {
        "map_id": "legacy_output_protocol_consolidation_map_v1",
        "consolidation_mode": "classification_only",
        "must_not_migrate_now": True,
        "must_not_rewrite_historical_artifacts": True,
        "is_runtime_registry": False,
        "entry_count": len(entries),
        "entries": entries,
    }


def _build_legacy_dual_role_mapping() -> Dict[str, Any]:
    return {
        "map_id": "legacy_candidate_role_dual_mapping_v1",
        "dual_role_allowed": True,
        "role_switch_requires_traceability": True,
        "entry_count": len(LEGACY_DUAL_ROLE_ENTRIES),
        "entries": list(LEGACY_DUAL_ROLE_ENTRIES),
    }


def _build_protocol_dependency_graph() -> Dict[str, Any]:
    nodes = []
    edges = []
    for protocol_id, deps in PROTOCOL_DEPENDENCY_GRAPH.items():
        nodes.append({"protocol_id": protocol_id, "protocol_layer": "L1"})
        for upstream in deps.get("upstream_protocol_refs", ()):
            edges.append({"from": upstream, "to": protocol_id, "edge_type": "upstream"})
        for downstream in deps.get("downstream_protocol_refs", ()):
            edges.append({"from": protocol_id, "to": downstream, "edge_type": "downstream"})
    l1_connections = {
        "evidence_binding": "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
        "field_schema": "LUNA-PROTO-L1-FIELD-SCHEMA-V1",
        "record_lifecycle": "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
        "approval_ack": "LUNA-PROTO-L1-APPROVAL-ACK-V1",
        "whitebox_diagnostic_binding": "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
        "protocol_assimilation": "LUNA-PROTO-L1-PROTOCOL-ASSIMILATION-V1",
        "protocol_traceability": PROTOCOL_TRACEABILITY_ID,
    }
    return {
        "graph_id": "input_output_protocol_dependency_graph_v1",
        "graph_complete": True,
        "protocols": {
            pid: {
                "protocol_id": pid,
                "upstream_protocol_refs": list(deps.get("upstream_protocol_refs", ())),
                "downstream_protocol_refs": list(deps.get("downstream_protocol_refs", ())),
                "related_protocol_ids": list(deps.get("related_protocol_ids", ())),
            }
            for pid, deps in PROTOCOL_DEPENDENCY_GRAPH.items()
        },
        "l1_connection_refs": l1_connections,
        "nodes": nodes,
        "edges": edges,
    }


def _protocol_full_metadata_complete(*regs: Dict[str, Any]) -> bool:
    required_keys = (
        "protocol_id",
        "protocol_layer",
        "protocol_domain",
        "protocol_version",
        "error_namespace",
        "error_code_set",
        "protocol_execution_result_schema_ref",
        "whitebox_candidate_ref_mapping",
        "upstream_protocol_refs",
        "downstream_protocol_refs",
        "related_protocol_ids",
        "protocol_standard_ref",
        "separation_rule_ref",
        "governance_debt_ref",
    )
    for reg in regs:
        if not all(reg.get(k) for k in required_keys):
            return False
        if not reg.get("error_code_set"):
            return False
        wb = reg.get("whitebox_candidate_ref_mapping") or {}
        if not wb.get("whitebox_candidate_ref_mapping"):
            return False
    return True


def _build_traceability_rule_contract() -> Dict[str, Any]:
    return {
        "contract_id": "protocol_traceability_rule_contract_v1",
        "protocol_id": PROTOCOL_TRACEABILITY_ID,
        "protocol_name_en": "Protocol Traceability Governance Protocol",
        "protocol_name_zh": "协议溯源治理协议",
        "required_fields": list(TRACEABILITY_RULE_REQUIRED_FIELDS),
        "trace_types": [
            "error_trace",
            "candidate_trace",
            "evidence_trace",
            "protocol_trace",
            "whitebox_trace",
        ],
        "trace_status_values": ["traceable", "partially_traceable", "untraceable"],
        "contract_complete": len(TRACEABILITY_RULE_REQUIRED_FIELDS) >= 18,
        "runtime_execution_allowed": False,
        "classification_only": True,
    }


def _build_traceability_query_path_contract() -> Dict[str, Any]:
    return {
        "contract_id": "protocol_traceability_query_path_contract_v1",
        "protocol_id": PROTOCOL_TRACEABILITY_ID,
        "query_path_steps": list(TRACEABILITY_QUERY_PATH_STEPS),
        "step_count": len(TRACEABILITY_QUERY_PATH_STEPS),
        "contract_complete": len(TRACEABILITY_QUERY_PATH_STEPS) == 14,
        "canonical_trace_chain": (
            "error_code → protocol_id → protocol registry → upstream/downstream protocol → "
            "candidate lineage → evidence refs → whitebox candidate ref → recommended_action"
        ),
    }


def _build_traceability_error_to_source_mapping() -> Dict[str, Any]:
    return {
        "mapping_id": "protocol_traceability_error_to_source_mapping_v1",
        "protocol_id": PROTOCOL_TRACEABILITY_ID,
        "error_class_trace_rules": list(ERROR_CLASS_TRACE_RULES),
        "traceability_error_codes": list(TRACEABILITY_ERROR_CODES),
        "mapping_complete": len(ERROR_CLASS_TRACE_RULES) >= 10,
    }


def _build_traceability_candidate_lineage_mapping() -> Dict[str, Any]:
    return {
        "mapping_id": "protocol_traceability_candidate_lineage_mapping_v1",
        "protocol_id": PROTOCOL_TRACEABILITY_ID,
        "lineage_rules": [
            {
                "candidate_type": "input_candidate",
                "required_trace_fields": [
                    "source_phase",
                    "source_module",
                    "source_artifacts",
                    "evidence_refs",
                ],
            },
            {
                "candidate_type": "output_candidate",
                "required_trace_fields": ["source_input_ref"],
            },
            {
                "candidate_type": "result_candidate",
                "required_trace_fields": ["process_ref", "checker_result_ref"],
            },
            {
                "candidate_type": "record_candidate",
                "required_trace_fields": [
                    "source_input_ref",
                    "source_output_ref",
                    "approval_refs",
                ],
            },
            {
                "candidate_type": "dual_role_candidate",
                "required_trace_fields": [
                    "upstream_output_ref",
                    "source_input_ref",
                    "role_switch_requires_traceability",
                ],
            },
        ],
        "dual_role_requires_traceability": True,
        "mapping_complete": True,
    }


def _build_traceability_whitebox_candidate_mapping() -> Dict[str, Any]:
    mappings = []
    for code in TRACEABILITY_ERROR_CODES:
        mappings.append(
            {
                "error_code": code,
                "whitebox_candidate_ref": build_whitebox_diagnostic_ref(
                    phase_id=PHASE_ID,
                    protocol_id=PROTOCOL_TRACEABILITY_ID,
                    error_code=code,
                    artifact_ref="summary.json",
                    field_path="go_conditions",
                ),
            }
        )
    return {
        "mapping_id": "protocol_traceability_whitebox_candidate_mapping_v1",
        "protocol_id": PROTOCOL_TRACEABILITY_ID,
        "mappings": mappings,
        "mapping_complete": len(mappings) == len(TRACEABILITY_ERROR_CODES),
        "whitebox_runtime_integration": False,
        "binding_mode": "contract_only",
    }


def _build_traceability_cursor_query_rule() -> Dict[str, Any]:
    return {
        "rule_id": "protocol_traceability_cursor_query_rule_v1",
        "protocol_id": PROTOCOL_TRACEABILITY_ID,
        "cursor_query_steps": list(CURSOR_QUERY_RULE_STEPS),
        "step_count": len(CURSOR_QUERY_RULE_STEPS),
        "rule_complete": len(CURSOR_QUERY_RULE_STEPS) == 10,
        "must_not_use_as_runtime_engine": True,
        "must_not_integrate_whitebox_runtime": True,
        "must_not_rewrite_historical_artifacts": True,
        "protocol_violation_vs_proc_failure": SEPARATION_RULE_REF,
    }


def run_protocol_input_output_symmetry_registry_patch_v1(
    *,
    planning_root: Optional[str] = None,
    shared_code_smoke_root: Optional[str] = None,
    owner_approval_post_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    planning = Path(planning_root or DEFAULT_PLANNING_ROOT).expanduser().resolve()
    smoke = Path(shared_code_smoke_root or DEFAULT_SMOKE_ROOT).expanduser().resolve()
    post_review = Path(owner_approval_post_review_root or DEFAULT_POST_REVIEW_ROOT).expanduser().resolve()
    meta = _meta(out, planning, smoke, post_review)
    issues: List[str] = []

    plan_summary = _read_json(planning / "summary.json")
    plan_verifier = _read_json(planning / "verifier_report.json")
    smoke_summary = _read_json(smoke / "summary.json")
    smoke_verifier = _read_json(smoke / "verifier_report.json")
    post_summary = _read_json(post_review / "summary.json")
    post_verifier = _read_json(post_review / "verifier_report.json")

    prior_protocol_standard_planning_go = (
        plan_summary.get("final_decision") == PLANNING_FINAL_GO
        and plan_verifier.get("verifier") == "GO"
        and int(plan_verifier.get("passed_checks", 0)) >= 420
        and plan_verifier.get("failed_checks") == 0
        and plan_verifier.get("blocker_count") == 0
    )
    if not prior_protocol_standard_planning_go:
        issues.append("protocol_standard_planning_not_go")

    prior_shared_code_smoke_go = (
        smoke_summary.get("final_decision") == SMOKE_FINAL_GO
        and smoke_verifier.get("verifier") == "GO"
        and int(smoke_verifier.get("passed_checks", 0)) >= 420
        and smoke_verifier.get("failed_checks") == 0
        and smoke_verifier.get("blocker_count") == 0
    )
    if not prior_shared_code_smoke_go:
        issues.append("shared_code_smoke_not_go")

    prior_owner_approval_post_review_go = (
        post_summary.get("final_decision") == POST_REVIEW_FINAL_GO
        and post_verifier.get("verifier") == "GO"
        and int(post_verifier.get("passed_checks", 0)) >= 420
        and post_verifier.get("failed_checks") == 0
        and post_verifier.get("blocker_count") == 0
    )
    downstream_readiness_gaps: List[str] = []
    if not prior_owner_approval_post_review_go:
        downstream_readiness_gaps.append("owner_approval_post_review_not_go")

    registered_entries = register_input_output_symmetry_protocol_patch()
    headers = build_input_output_symmetry_protocol_headers()
    header_by_id = {h.protocol_id: h.to_dict() for h in headers}

    input_reg = _build_protocol_registration(
        PROTOCOL_INPUT_CANDIDATE_ID,
        header_by_id[PROTOCOL_INPUT_CANDIDATE_ID],
        next((e for e in registered_entries if e.get("suggested_protocol_id") == PROTOCOL_INPUT_CANDIDATE_ID), {}),
        PROTOCOL_DEPENDENCY_GRAPH[PROTOCOL_INPUT_CANDIDATE_ID],
    )
    output_reg = _build_protocol_registration(
        PROTOCOL_OUTPUT_CANDIDATE_ID,
        header_by_id[PROTOCOL_OUTPUT_CANDIDATE_ID],
        next((e for e in registered_entries if e.get("suggested_protocol_id") == PROTOCOL_OUTPUT_CANDIDATE_ID), {}),
        PROTOCOL_DEPENDENCY_GRAPH[PROTOCOL_OUTPUT_CANDIDATE_ID],
    )
    symmetry_reg = _build_protocol_registration(
        PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
        header_by_id[PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID],
        next((e for e in registered_entries if e.get("suggested_protocol_id") == PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID), {}),
        PROTOCOL_DEPENDENCY_GRAPH[PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID],
    )
    traceability_reg = _build_protocol_registration(
        PROTOCOL_TRACEABILITY_ID,
        header_by_id[PROTOCOL_TRACEABILITY_ID],
        next((e for e in registered_entries if e.get("suggested_protocol_id") == PROTOCOL_TRACEABILITY_ID), {}),
        PROTOCOL_DEPENDENCY_GRAPH[PROTOCOL_TRACEABILITY_ID],
    )

    dependency_graph = {**_build_protocol_dependency_graph(), **meta}
    legacy_input_map = {**_build_legacy_input_consolidation_map(), **meta}
    legacy_output_map = {**_build_legacy_output_consolidation_map(), **meta}
    legacy_dual_role_map = {**_build_legacy_dual_role_mapping(), **meta}

    input_candidate_protocol_registered = bool(
        input_reg.get("registered") is True and input_reg.get("registry_entry")
    )
    output_candidate_protocol_registered = bool(
        output_reg.get("registered") is True and output_reg.get("registry_entry")
    )
    input_output_symmetry_protocol_registered = bool(
        symmetry_reg.get("registered") is True and symmetry_reg.get("registry_entry")
    )
    protocol_traceability_governance_registered = bool(
        traceability_reg.get("registered") is True and traceability_reg.get("registry_entry")
    )

    traceability_rule_contract = {**_build_traceability_rule_contract(), **meta}
    traceability_query_path_contract = {**_build_traceability_query_path_contract(), **meta}
    traceability_error_to_source_mapping = {**_build_traceability_error_to_source_mapping(), **meta}
    traceability_candidate_lineage_mapping = {**_build_traceability_candidate_lineage_mapping(), **meta}
    traceability_whitebox_candidate_mapping = {**_build_traceability_whitebox_candidate_mapping(), **meta}
    traceability_cursor_query_rule = {**_build_traceability_cursor_query_rule(), **meta}

    input_field_contract = {
        "contract_id": "input_candidate_required_field_contract_v1",
        "protocol_id": PROTOCOL_INPUT_CANDIDATE_ID,
        "required_fields": list(INPUT_CANDIDATE_REQUIRED_FIELDS),
        "field_count": len(INPUT_CANDIDATE_REQUIRED_FIELDS),
        "contract_complete": len(INPUT_CANDIDATE_REQUIRED_FIELDS) >= 30,
        "boundary_statements": [
            "input_candidate != accepted_input",
            "input_candidate != record",
            "input_candidate != approval",
            "input_candidate != grant",
            "input_candidate != fact",
            "input_candidate != action",
        ],
        **meta,
    }
    output_field_contract = {
        "contract_id": "output_candidate_required_field_contract_v1",
        "protocol_id": PROTOCOL_OUTPUT_CANDIDATE_ID,
        "required_fields": list(OUTPUT_CANDIDATE_REQUIRED_FIELDS),
        "field_count": len(OUTPUT_CANDIDATE_REQUIRED_FIELDS),
        "contract_complete": len(OUTPUT_CANDIDATE_REQUIRED_FIELDS) >= 30,
        "boundary_statements": [
            "output_candidate != accepted_output",
            "output_candidate != record",
            "result_candidate != final_result",
            "record_candidate != record",
        ],
        **meta,
    }
    traceability_contract = {
        "contract_id": "input_output_traceability_contract_v1",
        "protocol_id": PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
        "required_fields": list(TRACEABILITY_REQUIRED_FIELDS),
        "field_count": len(TRACEABILITY_REQUIRED_FIELDS),
        "contract_complete": len(TRACEABILITY_REQUIRED_FIELDS) >= 20,
        "symmetry_rules": [
            "each output_candidate must reverse-lookup source_input_candidate",
            "each input_candidate must track derived_output_refs",
            "input and output fields need not match exactly but traceability contract is mandatory",
        ],
        "boundary_statements": [
            "input_output_mapping != runtime_execution",
            "traceability_ref != write_permission",
        ],
        **meta,
    }

    error_namespace_mapping = {
        "mapping_id": "input_output_error_namespace_mapping_v1",
        "protocols": [
            {
                "protocol_id": PROTOCOL_INPUT_CANDIDATE_ID,
                "error_namespace": f"{PROTOCOL_INPUT_CANDIDATE_ID}::*",
                "error_codes": list(INPUT_CANDIDATE_ERROR_CODES),
                "all_validated": all(validate_error_code(c) for c in INPUT_CANDIDATE_ERROR_CODES),
            },
            {
                "protocol_id": PROTOCOL_OUTPUT_CANDIDATE_ID,
                "error_namespace": f"{PROTOCOL_OUTPUT_CANDIDATE_ID}::*",
                "error_codes": list(OUTPUT_CANDIDATE_ERROR_CODES),
                "all_validated": all(validate_error_code(c) for c in OUTPUT_CANDIDATE_ERROR_CODES),
            },
            {
                "protocol_id": PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
                "error_namespace": f"{PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID}::*",
                "error_codes": list(SYMMETRY_ERROR_CODES),
                "all_validated": all(validate_error_code(c) for c in SYMMETRY_ERROR_CODES),
            },
            {
                "protocol_id": PROTOCOL_TRACEABILITY_ID,
                "error_namespace": f"{PROTOCOL_TRACEABILITY_ID}::*",
                "error_codes": list(TRACEABILITY_ERROR_CODES),
                "all_validated": all(validate_error_code(c) for c in TRACEABILITY_ERROR_CODES),
            },
        ],
        "mapping_complete": True,
        **meta,
    }

    whitebox_mappings = [
        input_reg.get("whitebox_candidate_ref_mapping"),
        output_reg.get("whitebox_candidate_ref_mapping"),
        symmetry_reg.get("whitebox_candidate_ref_mapping"),
        traceability_reg.get("whitebox_candidate_ref_mapping"),
    ]
    whitebox_ref_mapping = {
        "mapping_id": "input_output_whitebox_candidate_ref_mapping_v1",
        "mappings": whitebox_mappings,
        "mapping_complete": len(whitebox_mappings) == 4 and all(m.get("whitebox_candidate_ref_mapping") for m in whitebox_mappings),
        "whitebox_runtime_integration": False,
        **meta,
    }

    reference_rule_patch = {
        "patch_id": "input_output_protocol_reference_rule_patch_v1",
        "principle_en": PRINCIPLE_EN,
        "principle_zh": PRINCIPLE_ZH,
        "separation_rule_ref": SEPARATION_RULE_REF,
        "protocol_standard_ref": PROTOCOL_STANDARD_REF,
        "protocol_execution_result_schema_ref": PROTOCOL_EXECUTION_RESULT_SCHEMA_REF,
        "governance_debt_ref": GOVERNANCE_DEBT_REF,
        "shared_protocol_system_revalidation": False,
        "required_references_for_owner_approval_request_planning": [
            PROTOCOL_INPUT_CANDIDATE_ID,
            PROTOCOL_OUTPUT_CANDIDATE_ID,
            PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
            PROTOCOL_TRACEABILITY_ID,
        ],
        "required_reference_fields": [
            "protocol_id",
            "error_namespace",
            "error_code",
            "protocol_execution_result_schema_ref",
            "whitebox_candidate_ref",
            "protocol_standard_ref",
            "related_protocol_ids",
            "upstream_protocol_refs",
            "downstream_protocol_refs",
            "separation_rule_ref",
            "governance_debt_ref",
        ],
        "reference_mode": "lightweight_reference_only",
        "must_not_full_revalidate_29_protocol_classification": True,
        "approval_request_candidate_classification": "input_candidate_type",
        "patch_complete": True,
        **meta,
    }

    classification_patch = {
        "patch_id": "input_output_existing_protocol_classification_patch_v1",
        "patch_mode": "incremental_classification_patch",
        "full_29_protocol_reclassification_executed": False,
        "new_classifications": [
            {
                "object_type": "approval_request_candidate",
                "classified_as": "input_candidate",
                "governing_protocol_id": PROTOCOL_INPUT_CANDIDATE_ID,
                "symmetry_protocol_id": PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
                "notes": "Owner Approval Request Planning must treat approval_request_candidate as input candidate",
            },
            {
                "object_type": "owner_approval_request_result_candidate",
                "classified_as": "output_candidate",
                "governing_protocol_id": PROTOCOL_OUTPUT_CANDIDATE_ID,
                "symmetry_protocol_id": PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
            },
            {
                "object_type": "derived_approval_planning_artifact",
                "classified_as": "output_candidate",
                "governing_protocol_id": PROTOCOL_OUTPUT_CANDIDATE_ID,
            },
        ],
        "patch_complete": True,
        **meta,
    }

    governance_debt_patch = {
        "patch_id": "input_output_governance_debt_patch_v1",
        "governance_debt_ref": GOVERNANCE_DEBT_REF,
        "prior_debts_carried": list(GOVERNANCE_DEBTS),
        "new_or_updated_debts": [
            {
                "debt_id": "input_output_symmetry_canonicalization_debt",
                "debt_title": "Input / Output Symmetry Canonicalization Debt",
                "priority": "P1",
                "classification": "L1 Midplatform System Protocols",
                "debt_type": "partially_addressed_by_registry_patch",
                "current_handling": "registry_patch_defined_contracts_and_consolidation_maps_only",
                "risk": "module_phases_may_drift_without_symmetry_reference",
                "required_future_phase": NEXT_PHASE_GO,
                "must_not_implement_now": True,
                "addressed_by_this_patch": [
                    "input_candidate_field_contract",
                    "output_candidate_field_contract",
                    "input_output_traceability_contract",
                    "input_output_protocol_dependency_graph",
                    "legacy_input_protocol_consolidation_map",
                    "legacy_output_protocol_consolidation_map",
                    "legacy_candidate_role_dual_mapping",
                    "protocol_traceability_governance_protocol_registration",
                    "protocol_traceability_rule_contract",
                    "protocol_traceability_query_path_contract",
                    "protocol_traceability_cursor_query_rule",
                ],
            },
        ],
        "all_prior_p1_must_not_implement_now": all(d.get("must_not_implement_now") is True for d in GOVERNANCE_DEBTS),
        "patch_complete": True,
        **meta,
    }

    non_runtime_constraints = {
        "constraints_id": "input_output_non_runtime_constraints_v1",
        "boundary_contract_statements": list(BOUNDARY_CONTRACT_STATEMENTS),
        "forbidden_runtime_flags": list(RUNTIME_FORBIDDEN_FLAGS),
        "runtime_execution_absent": True,
        "protocol_migration_absent": True,
        "whitebox_runtime_integration_absent": True,
        "module_adapter_implementation_absent": True,
        "authorization_request_absent": True,
        "request_record_absent": True,
        "owner_approval_record_absent": True,
        "grant_absent": True,
        "grant_token_absent": True,
        "grant_record_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "l1_protocol_runtime_implemented": False,
        "production_ready_declared": False,
        "protocol_traceability_runtime_absent": True,
        "traceability_registry_is_not_runtime_engine": True,
        **meta,
    }

    next_phase_readiness = {
        "readiness_id": "input_output_next_phase_readiness_v1",
        "next_phase_primary": NEXT_PHASE_GO,
        "next_phase_rationale": (
            "Owner Approval Request Planning should reference Input Candidate Governance and "
            "Input-Output Symmetry instead of inventing approval_request_candidate base rules"
        ),
        "required_protocol_refs_for_next_phase": [
            PROTOCOL_INPUT_CANDIDATE_ID,
            PROTOCOL_OUTPUT_CANDIDATE_ID,
            PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID,
            PROTOCOL_TRACEABILITY_ID,
        ],
        "l2_extension_expected": "L2 Task Manager owner approval request extension",
        "readiness_ok": True,
        **meta,
    }

    input_candidate_field_contract_complete = input_field_contract.get("contract_complete") is True
    output_candidate_field_contract_complete = output_field_contract.get("contract_complete") is True
    input_output_traceability_contract_complete = traceability_contract.get("contract_complete") is True
    input_output_error_namespace_mapping_complete = error_namespace_mapping.get("mapping_complete") is True
    input_output_whitebox_candidate_ref_mapping_complete = whitebox_ref_mapping.get("mapping_complete") is True
    protocol_reference_rule_patch_complete = reference_rule_patch.get("patch_complete") is True
    existing_protocol_classification_patch_complete = classification_patch.get("patch_complete") is True
    input_output_governance_debt_patch_complete = governance_debt_patch.get("patch_complete") is True
    input_output_protocol_dependency_graph_complete = dependency_graph.get("graph_complete") is True
    legacy_input_protocol_consolidation_complete = (
        legacy_input_map.get("entry_count") == len(REQUIRED_LEGACY_INPUT_NAMES)
        and legacy_input_map.get("consolidation_mode") == "classification_only"
        and legacy_input_map.get("must_not_migrate_now") is True
    )
    legacy_output_protocol_consolidation_complete = (
        legacy_output_map.get("entry_count") == len(REQUIRED_LEGACY_OUTPUT_NAMES)
        and legacy_output_map.get("consolidation_mode") == "classification_only"
        and legacy_output_map.get("must_not_migrate_now") is True
    )
    legacy_candidate_role_dual_mapping_complete = (
        legacy_dual_role_map.get("entry_count") == len(REQUIRED_DUAL_ROLE_NAMES)
        and legacy_dual_role_map.get("dual_role_allowed") is True
    )
    protocol_full_metadata_complete = _protocol_full_metadata_complete(
        input_reg, output_reg, symmetry_reg, traceability_reg
    )
    protocol_traceability_rule_contract_complete = traceability_rule_contract.get("contract_complete") is True
    protocol_traceability_query_path_contract_complete = traceability_query_path_contract.get("contract_complete") is True
    protocol_traceability_error_to_source_mapping_complete = traceability_error_to_source_mapping.get("mapping_complete") is True
    protocol_traceability_candidate_lineage_mapping_complete = traceability_candidate_lineage_mapping.get("mapping_complete") is True
    protocol_traceability_whitebox_candidate_mapping_complete = traceability_whitebox_candidate_mapping.get("mapping_complete") is True
    protocol_traceability_cursor_query_rule_complete = traceability_cursor_query_rule.get("rule_complete") is True
    protocol_traceability_runtime_absent = non_runtime_constraints.get("protocol_traceability_runtime_absent") is True

    go_conditions = {
        "prior_protocol_standard_planning_go": prior_protocol_standard_planning_go,
        "prior_shared_code_smoke_go": prior_shared_code_smoke_go,
        "prior_owner_approval_post_review_go": prior_owner_approval_post_review_go,
        "input_candidate_protocol_registered": input_candidate_protocol_registered,
        "output_candidate_protocol_registered": output_candidate_protocol_registered,
        "input_output_symmetry_protocol_registered": input_output_symmetry_protocol_registered,
        "input_candidate_field_contract_complete": input_candidate_field_contract_complete,
        "output_candidate_field_contract_complete": output_candidate_field_contract_complete,
        "input_output_traceability_contract_complete": input_output_traceability_contract_complete,
        "input_output_error_namespace_mapping_complete": input_output_error_namespace_mapping_complete,
        "input_output_whitebox_candidate_ref_mapping_complete": input_output_whitebox_candidate_ref_mapping_complete,
        "protocol_reference_rule_patch_complete": protocol_reference_rule_patch_complete,
        "existing_protocol_classification_patch_complete": existing_protocol_classification_patch_complete,
        "input_output_governance_debt_patch_complete": input_output_governance_debt_patch_complete,
        "input_output_protocol_dependency_graph_complete": input_output_protocol_dependency_graph_complete,
        "legacy_input_protocol_consolidation_complete": legacy_input_protocol_consolidation_complete,
        "legacy_output_protocol_consolidation_complete": legacy_output_protocol_consolidation_complete,
        "legacy_candidate_role_dual_mapping_complete": legacy_candidate_role_dual_mapping_complete,
        "protocol_full_metadata_complete": protocol_full_metadata_complete,
        "protocol_traceability_governance_registered": protocol_traceability_governance_registered,
        "protocol_traceability_rule_contract_complete": protocol_traceability_rule_contract_complete,
        "protocol_traceability_query_path_contract_complete": protocol_traceability_query_path_contract_complete,
        "protocol_traceability_error_to_source_mapping_complete": protocol_traceability_error_to_source_mapping_complete,
        "protocol_traceability_candidate_lineage_mapping_complete": protocol_traceability_candidate_lineage_mapping_complete,
        "protocol_traceability_whitebox_candidate_mapping_complete": protocol_traceability_whitebox_candidate_mapping_complete,
        "protocol_traceability_cursor_query_rule_complete": protocol_traceability_cursor_query_rule_complete,
        "protocol_traceability_runtime_absent": protocol_traceability_runtime_absent,
        "runtime_execution_absent": True,
        "protocol_migration_absent": True,
        "whitebox_runtime_integration_absent": True,
        "module_adapter_implementation_absent": True,
        "authorization_request_absent": True,
        "request_record_absent": True,
        "owner_approval_record_absent": True,
        "grant_absent": True,
        "foundation_not_frozen": True,
        "closure_not_executed": True,
        "non_execution_boundary_ok": True,
        "next_phase_readiness_ok": next_phase_readiness.get("readiness_ok") is True,
    }

    registry_patch_pass = all(go_conditions.get(k) is True for k in GO_CONDITIONS_KEYS) and not issues
    blocker_count = len(issues) + sum(1 for k in GO_CONDITIONS_KEYS if go_conditions.get(k) is not True)

    if not registry_patch_pass:
        if not prior_protocol_standard_planning_go or not prior_shared_code_smoke_go:
            final_decision = FINAL_DECISION_BLOCKED
        else:
            final_decision = FINAL_DECISION_BLOCKED
    else:
        final_decision = FINAL_DECISION_GO

    separation_doc = build_separation_rule_document()
    review_report = {
        "report_id": "protocol_input_output_symmetry_registry_patch_report_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "registry_patch_pass": registry_patch_pass,
        "blocker_count": blocker_count,
        "issues": issues,
        "go_conditions": go_conditions,
        "registered_protocol_ids": list(REGISTRY_PATCH_PROTOCOL_IDS),
        "boundary_contract_statements": list(BOUNDARY_CONTRACT_STATEMENTS),
        "final_decision": final_decision,
        "next_phase": NEXT_PHASE_GO,
        "separation_rule": separation_doc,
        **meta,
    }

    summary = {
        **meta,
        "candidate_only": True,
        "registry_patch_pass": registry_patch_pass,
        "input_output_symmetry_patch_complete": registry_patch_pass,
        "blocker_count": blocker_count,
        "issues": issues,
        "downstream_readiness_gaps": downstream_readiness_gaps,
        "downstream_readiness_refs": {
            "owner_approval_post_review_root": str(post_review),
            "prior_owner_approval_post_review_go": prior_owner_approval_post_review_go,
            "owner_approval_post_review_final_decision": post_summary.get("final_decision"),
        },
        "go_conditions": go_conditions,
        "prior_protocol_standard_planning_go": prior_protocol_standard_planning_go,
        "prior_shared_code_smoke_go": prior_shared_code_smoke_go,
        "prior_owner_approval_post_review_go": prior_owner_approval_post_review_go,
        "input_candidate_protocol_registered": input_candidate_protocol_registered,
        "output_candidate_protocol_registered": output_candidate_protocol_registered,
        "input_output_symmetry_protocol_registered": input_output_symmetry_protocol_registered,
        "protocol_traceability_governance_registered": protocol_traceability_governance_registered,
        "protocol_reference_rule_patch_complete": protocol_reference_rule_patch_complete,
        "existing_protocol_classification_patch_complete": existing_protocol_classification_patch_complete,
        "input_output_governance_debt_patch_complete": input_output_governance_debt_patch_complete,
        "input_output_protocol_dependency_graph_complete": input_output_protocol_dependency_graph_complete,
        "legacy_input_protocol_consolidation_complete": legacy_input_protocol_consolidation_complete,
        "legacy_output_protocol_consolidation_complete": legacy_output_protocol_consolidation_complete,
        "legacy_candidate_role_dual_mapping_complete": legacy_candidate_role_dual_mapping_complete,
        "protocol_full_metadata_complete": protocol_full_metadata_complete,
        "protocol_traceability_rule_contract_complete": protocol_traceability_rule_contract_complete,
        "protocol_traceability_cursor_query_rule_complete": protocol_traceability_cursor_query_rule_complete,
        "protocol_traceability_runtime_absent": protocol_traceability_runtime_absent,
        "runtime_execution_absent": True,
        "protocol_migration_absent": True,
        "whitebox_runtime_integration_absent": True,
        "non_execution_boundary_ok": True,
        "next_phase_readiness_ok": next_phase_readiness.get("readiness_ok") is True,
        "go_no_go_decision": final_decision,
        "final_decision": final_decision,
        "next_phase": NEXT_PHASE_GO,
        "recommended_next_phase": NEXT_PHASE_GO,
        "registered_protocol_ids": list(REGISTRY_PATCH_PROTOCOL_IDS),
    }

    markdown = "\n".join(
        [
            "# Protocol Input-Output Symmetry Registry Patch v1",
            "",
            f"- Phase: `{PHASE_ID}`",
            f"- Registry Patch Pass: `{registry_patch_pass}`",
            f"- Final Decision: `{final_decision}`",
            f"- Next Phase: `{NEXT_PHASE_GO}`",
            "",
            "## Registered L1 Protocols",
            "",
            f"- `{PROTOCOL_INPUT_CANDIDATE_ID}`",
            f"- `{PROTOCOL_OUTPUT_CANDIDATE_ID}`",
            f"- `{PROTOCOL_INPUT_OUTPUT_SYMMETRY_ID}`",
            f"- `{PROTOCOL_TRACEABILITY_ID}` (协议溯源治理)",
            "",
            "## Protocol Traceability",
            "",
            f"- traceability rule contract: `{protocol_traceability_rule_contract_complete}`",
            f"- cursor query rule: `{protocol_traceability_cursor_query_rule_complete}`",
            "",
            "## Protocol Dependency Graph",
            "",
            f"- dependency graph complete: `{input_output_protocol_dependency_graph_complete}`",
            f"- legacy input consolidation: `{legacy_input_protocol_consolidation_complete}`",
            f"- legacy output consolidation: `{legacy_output_protocol_consolidation_complete}`",
            f"- dual role mapping: `{legacy_candidate_role_dual_mapping_complete}`",
            "",
            "## Protocol Reference",
            "",
            f"- protocol_standard_ref: `{PROTOCOL_STANDARD_REF}`",
            f"- shared_protocol_system_revalidation: `false`",
            f"- separation_rule_ref: `{SEPARATION_RULE_REF}`",
            "",
            "## Boundary Contracts",
            "",
            *[f"- {s}" for s in BOUNDARY_CONTRACT_STATEMENTS],
            "",
            "## GO Conditions",
            "",
            *[f"- {k}: `{go_conditions.get(k)}`" for k in GO_CONDITIONS_KEYS],
        ]
    )

    return {
        "protocol_input_output_symmetry_registry_patch_report": review_report,
        "protocol_input_output_symmetry_registry_patch_report_md": markdown,
        "input_candidate_governance_protocol_registration": input_reg,
        "output_candidate_governance_protocol_registration": output_reg,
        "input_output_symmetry_protocol_registration": symmetry_reg,
        "protocol_traceability_governance_protocol_registration": traceability_reg,
        "input_candidate_required_field_contract": input_field_contract,
        "output_candidate_required_field_contract": output_field_contract,
        "input_output_traceability_contract": traceability_contract,
        "input_output_error_namespace_mapping": error_namespace_mapping,
        "input_output_whitebox_candidate_ref_mapping": whitebox_ref_mapping,
        "input_output_protocol_reference_rule_patch": reference_rule_patch,
        "input_output_existing_protocol_classification_patch": classification_patch,
        "input_output_governance_debt_patch": governance_debt_patch,
        "input_output_protocol_dependency_graph": dependency_graph,
        "legacy_input_protocol_consolidation_map": legacy_input_map,
        "legacy_output_protocol_consolidation_map": legacy_output_map,
        "legacy_candidate_role_dual_mapping": legacy_dual_role_map,
        "protocol_traceability_rule_contract": traceability_rule_contract,
        "protocol_traceability_query_path_contract": traceability_query_path_contract,
        "protocol_traceability_error_to_source_mapping": traceability_error_to_source_mapping,
        "protocol_traceability_candidate_lineage_mapping": traceability_candidate_lineage_mapping,
        "protocol_traceability_whitebox_candidate_mapping": traceability_whitebox_candidate_mapping,
        "protocol_traceability_cursor_query_rule": traceability_cursor_query_rule,
        "input_output_non_runtime_constraints": non_runtime_constraints,
        "input_output_next_phase_readiness": next_phase_readiness,
        "summary": summary,
    }
