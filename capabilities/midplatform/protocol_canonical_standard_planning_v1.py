# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Canonical Standard Planning v1.

Planning-only phase: defines protocol standards, shared code design, and existing protocol classification.
No runtime execution, no protocol migration, no module adapter implementation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.protocols.protocol_error_codes_v1 import ERROR_CLASSES, build_error_code
from capabilities.midplatform.protocols.protocol_execution_result_v1 import (
    REQUIRED_RESULT_KEYS,
    build_protocol_execution_result,
)
from capabilities.midplatform.protocols.protocol_separation_rule_v1 import build_separation_rule_document
from capabilities.midplatform.protocols.protocol_types_v1 import (
    ProtocolHeader,
    ProtocolRegistryEntry,
    build_protocol_id,
)
from capabilities.midplatform.task_manager_foundation_handoff_planning_v1 import (
    BOUNDARY_STATEMENT_EN,
    BOUNDARY_STATEMENT_ZH,
    FOUNDATION_ID,
)

PHASE_ID = "Phase-Midplatform-Protocol-Canonical-Standard-Planning-v1-001"
SCOPE = "midplatform_protocol_canonical_standard_planning_only"
SOURCE_CHAIN = "midplatform_protocol_canonical_standard_planning_v1"
FINAL_DECISION_GO = (
    "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_PLANNING_READY_FOR_SHARED_CODE_DRYRUN_OR_TASK_MANAGER_OWNER_APPROVAL_DRYRUN"
)
FINAL_DECISION_BLOCKED = "MIDPLATFORM_PROTOCOL_CANONICAL_STANDARD_PLANNING_BLOCKED"
NEXT_PHASE_PRIMARY = "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-DryRun-v1-001"
NEXT_PHASE_ALT = (
    "Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/"
    "midplatform_protocol_canonical_standard_planning_v1_smoke_v0"
)

PROTOCOL_DEFINITION_ZH = "协议 = 宪法约束下的流程契约"
PROTOCOL_DEFINITION_EN = "Protocol = Constitution-Guided Process Contract"

NUMBERING_FORMAT = "LUNA-PROTO-{LAYER}-{DOMAIN}-{NAME}-V{VERSION}"

BOUNDARY_CONTRACT_STATEMENTS: Tuple[str, ...] = (
    "protocol_standard_planning != protocol_runtime_execution",
    "protocol_code_template != runtime_protocol_engine",
    "protocol_classification != protocol_migration_execution",
    "protocol_error_code_standard != real_error_trigger",
    "whitebox_binding_contract != whitebox_runtime_integration",
    "existing_protocol_classification != module_adapter_implementation",
    "candidate_protocol != active_protocol_runtime",
    "foundation_freeze_candidate != foundation_frozen",
    "closure_candidate != closed",
)

L0_PROTOCOLS: Tuple[str, ...] = (
    "Safety Constitution",
    "Survival Constitution",
    "Non-Execution Boundary",
    "Owner/Operator Authority Principle",
    "Constitutional Violation Blocking Rule",
)

L1_PROTOCOLS: Tuple[Dict[str, str], ...] = (
    {"name": "Information Channel Governance", "domain": "INFORMATION-CHANNEL", "id_suffix": "GOVERNANCE"},
    {"name": "Protocol Lifecycle Governance", "domain": "PROTOCOL-LIFECYCLE", "id_suffix": "GOVERNANCE"},
    {"name": "Closure Channel Governance", "domain": "CLOSURE-CHANNEL", "id_suffix": "GOVERNANCE"},
    {"name": "Record Lifecycle Governance", "domain": "RECORD", "id_suffix": "LIFECYCLE"},
    {"name": "Evidence Binding Protocol", "domain": "EVIDENCE", "id_suffix": "BINDING"},
    {"name": "Approval & Ack Protocol", "domain": "APPROVAL", "id_suffix": "ACK"},
    {"name": "Revocation / Expiry / Rejection Protocol", "domain": "REVOCATION", "id_suffix": "EXPIRY-REJECTION"},
    {"name": "Field Schema Contract", "domain": "FIELD", "id_suffix": "SCHEMA"},
    {"name": "Protocol Assimilation Governance", "domain": "PROTOCOL", "id_suffix": "ASSIMILATION"},
    {"name": "Protocol Assimilation Supervision", "domain": "PROTOCOL", "id_suffix": "ASSIMILATION-SUPERVISION"},
    {"name": "Protocol Error Code Standard", "domain": "ERROR", "id_suffix": "CODE-STANDARD"},
    {"name": "Whitebox Diagnostic Binding Contract", "domain": "WHITEBOX", "id_suffix": "DIAGNOSTIC-BINDING"},
    {"name": "System Protocols Integration Contract", "domain": "SYSTEM", "id_suffix": "PROTOCOLS-INTEGRATION"},
)

L2_TASK_MANAGER_PROTOCOLS: Tuple[str, ...] = (
    "Task Manager Foundation Handoff Protocol",
    "Task Manager Closure Rehearsal Protocol",
    "Task Manager Freeze Authorization Protocol",
    "Task Manager Grant Planning Protocol",
    "Task Manager Grant Request Protocol",
    "Task Manager Request Issuance Protocol",
    "Task Manager Request Record Protocol",
    "Task Manager Owner Approval Protocol",
)

L2_FUTURE_MODULE_PROTOCOLS: Tuple[str, ...] = (
    "Vision Frame Candidate Protocol",
    "Vision Focus Candidate Protocol",
    "OCR Text Candidate Protocol",
    "Navigation Decision Candidate Protocol",
    "WorldModel Entry Candidate Protocol",
    "Memory Candidate Protocol",
    "Permission Candidate Protocol",
    "Health Signal Protocol",
)

GOVERNANCE_DEBTS: Tuple[Dict[str, Any], ...] = (
    {
        "debt_id": "closure_channel_governance_missing_canonical_protocol",
        "debt_title": "Closure Channel Governance Missing Canonical Protocol",
        "priority": "P1",
        "classification": "L1 Midplatform System Protocols",
        "debt_type": "missing_canonical_protocol",
        "current_handling": "deferred_acknowledged_in_planning",
        "risk": "closure_channel_semantics_drift_without_canonical_standard",
        "required_future_phase": "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-DryRun-v1-001",
        "must_not_implement_now": True,
    },
    {
        "debt_id": "system_protocols_integration_required_before_module_adapter",
        "debt_title": "System Protocols Integration Required Before Module Adapter Implementation",
        "priority": "P1",
        "classification": "L1 Midplatform System Protocols",
        "debt_type": "integration_prerequisite",
        "current_handling": "deferred_acknowledged_in_planning",
        "risk": "premature_module_adapter_without_system_protocols_integration",
        "required_future_phase": "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-DryRun-v1-001",
        "must_not_implement_now": True,
    },
    {
        "debt_id": "lifecycle_record_governance_protocol_missing_canonical_standard",
        "debt_title": "Lifecycle Record Governance Protocol Missing Canonical Standard",
        "priority": "P1",
        "classification": "L1 Midplatform System Protocols",
        "debt_type": "missing_canonical_protocol",
        "current_handling": "addressed_in_this_planning_phase",
        "risk": "candidate_record_boundary_drift_across_modules",
        "required_future_phase": "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-DryRun-v1-001",
        "must_not_implement_now": True,
    },
    {
        "debt_id": "protocol_assimilation_governance_missing_layered_standard",
        "debt_title": "Protocol Assimilation Governance Missing Layered Standard",
        "priority": "P1",
        "classification": "L1 Midplatform System Protocols",
        "debt_type": "missing_layered_standard",
        "current_handling": "addressed_in_this_planning_phase",
        "risk": "module_protocol_semantic_drift_without_assimilation_supervision",
        "required_future_phase": "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-DryRun-v1-001",
        "must_not_implement_now": True,
    },
    {
        "debt_id": "protocol_canonical_standard_error_code_standard_missing",
        "debt_title": "Protocol Canonical Standard / Error Code Standard Missing",
        "priority": "P1",
        "classification": "L1 Midplatform System Protocols",
        "debt_type": "missing_canonical_standard",
        "current_handling": "addressed_in_this_planning_phase",
        "risk": "duplicate_protocol_work_across_grant_request_record_approval_chain",
        "required_future_phase": "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-DryRun-v1-001",
        "must_not_implement_now": True,
    },
    {
        "debt_id": "whitebox_diagnostic_binding_contract_missing",
        "debt_title": "Whitebox Diagnostic Binding Contract Missing",
        "priority": "P1",
        "classification": "L1 Midplatform System Protocols",
        "debt_type": "missing_binding_contract",
        "current_handling": "addressed_in_this_planning_phase",
        "risk": "protocol_errors_not_traceable_without_whitebox_binding",
        "required_future_phase": "Phase-Midplatform-Protocol-Canonical-Standard-Shared-Code-DryRun-v1-001",
        "must_not_implement_now": True,
    },
)

SHARED_CODE_MODULES: Tuple[str, ...] = (
    "capabilities/midplatform/protocols/protocol_types_v1.py",
    "capabilities/midplatform/protocols/protocol_error_codes_v1.py",
    "capabilities/midplatform/protocols/protocol_execution_result_v1.py",
    "capabilities/midplatform/protocols/protocol_registry_v1.py",
    "capabilities/midplatform/protocols/protocol_checker_v1.py",
    "capabilities/midplatform/protocols/protocol_whitebox_binding_v1.py",
    "capabilities/midplatform/protocols/protocol_health_monitor_contract_v1.py",
)

STANDARD_API_FUNCTIONS: Tuple[str, ...] = (
    "ProtocolHeader",
    "ProtocolError",
    "ProtocolExecutionResult",
    "ProtocolHealthStatus",
    "ProtocolRegistryEntry",
    "ProtocolLayer",
    "ProtocolErrorClass",
    "ProtocolSeverity",
    "build_protocol_id",
    "build_error_code",
    "validate_protocol_header",
    "validate_error_code",
    "build_protocol_execution_result",
    "validate_protocol_execution_result",
    "classify_protocol_layer",
    "classify_error_class",
    "check_constitution_execution",
    "check_process_execution",
    "check_interface_execution",
    "check_assimilation_health",
    "check_whitebox_binding",
    "build_whitebox_diagnostic_ref",
    "register_protocol",
    "lookup_protocol",
    "run_protocol_checker_flow",
)

NON_EXECUTION_FLAGS: Tuple[str, ...] = (
    "runtime_execution_enabled",
    "protocol_migration_executed",
    "whitebox_runtime_integrated",
    "module_adapter_implementation_ready",
    "foundation_frozen",
    "closure_executed",
    "grant_issued",
    "owner_approval_record_created",
    "request_record_created",
)

GO_CONDITIONS_KEYS: Tuple[str, ...] = (
    "protocol_canonical_standard_plan_complete",
    "protocol_numbering_standard_complete",
    "protocol_error_code_standard_complete",
    "protocol_execution_result_schema_complete",
    "error_taxonomy_complete",
    "whitebox_diagnostic_binding_contract_complete",
    "protocol_first_development_rule_complete",
    "module_protocol_layering_complete",
    "protocol_assimilation_supervision_standard_complete",
    "shared_protocol_code_design_complete",
    "standard_checker_flow_complete",
    "standard_verifier_contract_complete",
    "existing_protocol_classification_complete",
    "existing_protocol_error_namespace_mapping_complete",
    "existing_protocol_whitebox_binding_candidate_map_complete",
    "governance_debt_update_complete",
    "runtime_execution_absent",
    "protocol_migration_execution_absent",
    "whitebox_runtime_integration_absent",
    "module_adapter_implementation_absent",
    "foundation_not_frozen",
    "closure_not_executed",
    "grant_not_issued",
    "owner_approval_record_absent",
    "request_record_absent",
    "non_execution_boundary_ok",
)

EXAMPLE_ERROR_CODES: Tuple[Dict[str, str], ...] = (
    {
        "error_code": "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1::CONST-001",
        "meaning": "record candidate upgraded to real record, violating candidate != record constitutional boundary",
    },
    {
        "error_code": "LUNA-PROTO-L1-EVIDENCE-BINDING-V1::EVID-001",
        "meaning": "upstream summary / verifier_report missing or not traceable",
    },
    {
        "error_code": "LUNA-PROTO-L1-APPROVAL-ACK-V1::AUTH-001",
        "meaning": "owner approval candidate misread as owner approval record",
    },
    {
        "error_code": "LUNA-PROTO-L1-PROTOCOL-ASSIMILATION-V1::ASSIM-001",
        "meaning": "module failed to assimilate L1 protocol fields, semantic drift detected",
    },
    {
        "error_code": "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1::WB-001",
        "meaning": "protocol error not bound to whitebox trace / diagnostic node",
    },
)


def _meta(out: Path) -> Dict[str, Any]:
    return {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "source_chain": SOURCE_CHAIN,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "foundation_id": FOUNDATION_ID,
        "runtime_status": "not_enabled",
        "protocol_standard_planning_only": True,
        "runtime_execution_enabled": False,
        "protocol_migration_executed": False,
        "whitebox_runtime_integrated": False,
        "module_adapter_implementation_ready": False,
        "foundation_frozen": False,
        "closure_executed": False,
        "grant_issued": False,
        "owner_approval_record_created": False,
        "request_record_created": False,
        "authorization_request_issued": False,
        "output_root": str(out),
        "boundary_statement_en": BOUNDARY_STATEMENT_EN,
        "boundary_statement_zh": BOUNDARY_STATEMENT_ZH,
    }


def _build_l1_registry_entries() -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for proto in L1_PROTOCOLS:
        pid = f"LUNA-PROTO-L1-{proto['domain']}-{proto['id_suffix']}-V1"
        entries.append(
            ProtocolRegistryEntry(
                protocol_name=proto["name"],
                suggested_protocol_id=pid,
                layer="L1",
                domain=proto["domain"].lower().replace("-", "_"),
                status="exposed_in_task_manager_chain",
                current_handling="partially_defined_in_evaluation_phases",
                canonical_required=True,
                module_extension_allowed=True,
                whitebox_binding_required=True,
                error_namespace=f"{pid}::*",
                related_governance_debt=[d["debt_title"] for d in GOVERNANCE_DEBTS[:2]],
                must_not_implement_now=True,
            ).to_dict()
        )
    return entries


def _build_l2_task_manager_entries() -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    domain_map = {
        "Task Manager Foundation Handoff Protocol": ("TASKMANAGER", "FOUNDATION-HANDOFF"),
        "Task Manager Closure Rehearsal Protocol": ("TASKMANAGER", "CLOSURE-REHEARSAL"),
        "Task Manager Freeze Authorization Protocol": ("TASKMANAGER", "FREEZE-AUTHORIZATION"),
        "Task Manager Grant Planning Protocol": ("TASKMANAGER", "GRANT-PLANNING"),
        "Task Manager Grant Request Protocol": ("TASKMANAGER", "GRANT-REQUEST"),
        "Task Manager Request Issuance Protocol": ("TASKMANAGER", "REQUEST-ISSUANCE"),
        "Task Manager Request Record Protocol": ("TASKMANAGER", "GRANT-REQUEST-RECORD"),
        "Task Manager Owner Approval Protocol": ("TASKMANAGER", "OWNER-APPROVAL"),
    }
    for name in L2_TASK_MANAGER_PROTOCOLS:
        domain, suffix = domain_map[name]
        pid = f"LUNA-PROTO-L2-{domain}-{suffix}-V1"
        entries.append(
            ProtocolRegistryEntry(
                protocol_name=name,
                suggested_protocol_id=pid,
                layer="L2",
                domain=domain.lower(),
                status="actively_used_in_evaluation_phases",
                current_handling="evaluation_phase_artifacts_without_canonical_registry",
                canonical_required=True,
                module_extension_allowed=True,
                whitebox_binding_required=True,
                error_namespace=f"{pid}::*",
                related_governance_debt=["Protocol Canonical Standard / Error Code Standard Missing"],
                must_not_implement_now=True,
            ).to_dict()
        )
    return entries


def _build_l2_future_entries() -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    domain_map = {
        "Vision Frame Candidate Protocol": ("VISION", "FRAME-CANDIDATE"),
        "Vision Focus Candidate Protocol": ("VISION", "FOCUS-CANDIDATE"),
        "OCR Text Candidate Protocol": ("OCR", "TEXT-CANDIDATE"),
        "Navigation Decision Candidate Protocol": ("NAVIGATION", "DECISION-CANDIDATE"),
        "WorldModel Entry Candidate Protocol": ("WORLDMODEL", "ENTRY-CANDIDATE"),
        "Memory Candidate Protocol": ("MEMORY", "CANDIDATE"),
        "Permission Candidate Protocol": ("PERMISSION", "APPROVAL-CANDIDATE"),
        "Health Signal Protocol": ("HEALTH", "SIGNAL"),
    }
    for name in L2_FUTURE_MODULE_PROTOCOLS:
        domain, suffix = domain_map[name]
        pid = f"LUNA-PROTO-L2-{domain}-{suffix}-V1"
        entries.append(
            ProtocolRegistryEntry(
                protocol_name=name,
                suggested_protocol_id=pid,
                layer="L2",
                domain=domain.lower(),
                status="future_module_extension",
                current_handling="not_yet_implemented",
                canonical_required=True,
                module_extension_allowed=True,
                whitebox_binding_required=True,
                error_namespace=f"{pid}::*",
                related_governance_debt=[],
                must_not_implement_now=True,
            ).to_dict()
        )
    return entries


def run_protocol_canonical_standard_planning_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[2]
    meta = _meta(out)
    issues: List[str] = []

    numbering_standard = {
        "standard_id": "protocol_numbering_standard_v1",
        "format": NUMBERING_FORMAT,
        "rules": [
            "L0 defines constitutional rules only, no module field details",
            "L1 defines cross-module system protocols",
            "L2 defines module extensions inheriting L1",
            "L3 defines capability / adapter local contracts",
            "L2/L3 must not define conflicting numbering systems",
            "every protocol must have protocol_id, protocol_layer, protocol_domain, protocol_version, governance_level",
        ],
        "examples": [
            "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1",
            "LUNA-PROTO-L1-EVIDENCE-BINDING-V1",
            "LUNA-PROTO-L1-APPROVAL-ACK-V1",
            "LUNA-PROTO-L1-REVOCATION-EXPIRY-REJECTION-V1",
            "LUNA-PROTO-L1-PROTOCOL-ASSIMILATION-V1",
            "LUNA-PROTO-L1-WHITEBOX-DIAGNOSTIC-BINDING-V1",
            "LUNA-PROTO-L2-TASKMANAGER-GRANT-REQUEST-RECORD-V1",
            "LUNA-PROTO-L2-VISION-FRAME-CANDIDATE-V1",
            "LUNA-PROTO-L2-OCR-TEXT-CANDIDATE-V1",
            "LUNA-PROTO-L2-PERMISSION-APPROVAL-CANDIDATE-V1",
        ],
        "protocol_numbering_standard_complete": True,
        **meta,
    }

    error_code_standard = {
        "standard_id": "protocol_error_code_standard_v1",
        "format": "{PROTOCOL_ID}::{ERROR_CLASS}-{NUMBER}",
        "error_classes": list(ERROR_CLASSES),
        "examples": list(EXAMPLE_ERROR_CODES),
        "protocol_error_code_standard_complete": True,
        **meta,
    }

    sample_protocol_id = "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1"
    execution_result_schema = {
        "schema_id": "protocol_execution_result_schema_v1",
        "definition_zh": PROTOCOL_DEFINITION_ZH,
        "definition_en": PROTOCOL_DEFINITION_EN,
        "result_dimensions": [
            "constitution_execution_result",
            "process_execution_result",
            "interface_execution_result",
            "assimilation_health_result",
            "whitebox_binding_result",
            "protocol_execution_result",
        ],
        "required_keys": list(REQUIRED_RESULT_KEYS),
        "example": build_protocol_execution_result(sample_protocol_id).to_dict(),
        "protocol_execution_result_schema_complete": True,
        **meta,
    }

    error_taxonomy = {
        "taxonomy_id": "constitution_process_interface_assimilation_error_taxonomy_v1",
        "layers": {
            "L0": list(L0_PROTOCOLS),
            "L1": [p["name"] for p in L1_PROTOCOLS],
            "L2_task_manager": list(L2_TASK_MANAGER_PROTOCOLS),
            "L2_future_modules": list(L2_FUTURE_MODULE_PROTOCOLS),
            "L3": [
                "Concrete Capability Contract",
                "Adapter Input/Output Contract",
                "Local Verifier",
                "Local Diagnostics",
                "Local Artifact Contract",
            ],
        },
        "error_taxonomy_complete": True,
        **meta,
    }

    whitebox_contract = {
        "contract_id": "whitebox_diagnostic_binding_contract_v1",
        "binding_mode": "contract_only",
        "whitebox_runtime_integration": False,
        "whitebox_binding_contract_not_runtime_integration": True,
        "binding_fields": ["whitebox_trace_ref", "diagnostic_node_ref"],
        "trace_ref_format": "wb://{phase_id}:{protocol_id}:{error_code}",
        "diagnostic_ref_format": "diag://{phase_id}/{artifact_ref}/{field_path}",
        "whitebox_diagnostic_binding_contract_complete": True,
        **meta,
    }

    protocol_first_rule = {
        "rule_id": "protocol_first_development_rule_v1",
        "principle": "protocol_before_module_development",
        "rules": [
            "new lifecycle/record/approval/evidence/revocation/expiry/rejection stages must check L1/L2 reuse first",
            "if protocol exists, must reference protocol_id and error_code_namespace",
            "if protocol missing, must create standard or register debt before module development",
            "forbidden to invent protocol fields and error codes ad-hoc during module development",
        ],
        "protocol_first_development_rule_complete": True,
        "separation_rule_ref": "protocol_constraint_vs_module_logic_separation_rule_v1",
        **meta,
    }

    separation_rule = build_separation_rule_document(**meta)

    module_layering = {
        "layering_id": "module_internal_vs_cross_module_protocol_layering_v1",
        "L1_cross_module": [p["name"] for p in L1_PROTOCOLS],
        "L2_module_internal": {
            "task_manager": list(L2_TASK_MANAGER_PROTOCOLS),
            "future_modules": list(L2_FUTURE_MODULE_PROTOCOLS),
        },
        "L2_must_inherit_L1": True,
        "L3_capability_adapter": [
            "Concrete Capability Contract",
            "Adapter Input/Output Contract",
            "Local Verifier",
            "Local Diagnostics",
            "Local Artifact Contract",
        ],
        "module_protocol_layering_complete": True,
        **meta,
    }

    assimilation_supervision = {
        "standard_id": "protocol_assimilation_supervision_standard_v1",
        "dimensions": ["health", "drift", "fallback", "quarantine", "notification"],
        "health_checks": [
            "field_drift_detection",
            "semantic_drift_detection",
            "candidate_record_misread_detection",
            "ttl_revocation_expiry_loss_detection",
        ],
        "fallback_modes": ["degraded_mode", "quarantine", "block_and_notify"],
        "notification_targets": ["owner", "operator", "governance_audit"],
        "protocol_assimilation_supervision_standard_complete": True,
        **meta,
    }

    failure_handling = {
        "standard_id": "protocol_failure_handling_notification_standard_v1",
        "severity_levels": ["blocker", "warning", "info"],
        "notification_required_on_blocker": True,
        "owner_operator_notification_required_on_constitutional_violation": True,
        "recommended_actions": ["block_and_quarantine", "notify_owner_operator", "register_governance_debt"],
        **meta,
    }

    shared_code_design = {
        "design_id": "protocol_shared_code_design_v1",
        "target_directory": "capabilities/midplatform/protocols/",
        "modules": list(SHARED_CODE_MODULES),
        "modules_exist": all((repo_root / m).is_file() for m in SHARED_CODE_MODULES),
        "runtime_side_effects": False,
        "shared_protocol_code_design_complete": True,
        **meta,
    }

    checker_flow = {
        "flow_id": "protocol_shared_checker_flow_v1",
        "steps": [
            "check_constitution_execution",
            "check_process_execution",
            "check_interface_execution",
            "check_assimilation_health",
            "check_whitebox_binding",
            "aggregate_protocol_execution_result",
        ],
        "orchestrator": "run_protocol_checker_flow",
        "standard_checker_flow_complete": True,
        **meta,
    }

    api_contract = {
        "contract_id": "protocol_standard_api_contract_v1",
        "dataclasses": [
            "ProtocolHeader",
            "ProtocolError",
            "ProtocolExecutionResult",
            "ProtocolHealthStatus",
            "ProtocolRegistryEntry",
        ],
        "enums": ["ProtocolLayer", "ProtocolErrorClass", "ProtocolSeverity"],
        "functions": list(STANDARD_API_FUNCTIONS),
        **meta,
    }

    verifier_contract = {
        "contract_id": "protocol_standard_verifier_contract_v1",
        "principle": "future_verifiers_must_reuse_shared_protocol_helpers",
        "required_imports": [
            "protocol_error_codes_v1.validate_error_code",
            "protocol_execution_result_v1.validate_protocol_execution_result",
            "protocol_registry_v1.validate_protocol_header",
            "protocol_checker_v1.run_protocol_checker_flow",
            "protocol_whitebox_binding_v1.build_whitebox_diagnostic_ref",
        ],
        "forbidden_patterns": [
            "handwritten_duplicate_error_code_format",
            "handwritten_duplicate_execution_result_schema",
            "inline_protocol_id_construction_without_build_protocol_id",
        ],
        "standard_verifier_contract_complete": True,
        **meta,
    }

    error_object_schema = {
        "schema_id": "protocol_error_object_schema_v1",
        "example": {
            "error_code": "LUNA-PROTO-L1-RECORD-LIFECYCLE-V1::CONST-001",
            "error_class": "constitutional_violation",
            "severity": "blocker",
            "detected_by": "verifier",
            "phase_id": PHASE_ID,
            "artifact_ref": "summary.json",
            "field_path": "go_conditions.request_record_absent",
            "expected": True,
            "actual": False,
            "whitebox_trace_ref": "wb://Phase-.../LUNA-PROTO-L1-RECORD-LIFECYCLE-V1::CONST-001",
            "diagnostic_node_ref": "diag://Phase-.../summary.json/go_conditions.request_record_absent",
            "recommended_action": "block_and_quarantine",
            "notification_required": True,
            "owner_operator_notification_required": True,
        },
        **meta,
    }

    health_monitor = {
        "contract_id": "protocol_health_monitor_contract_v1",
        "dimensions": [
            "assimilation_health",
            "semantic_drift",
            "field_drift",
            "candidate_record_misread",
            "ttl_revocation_expiry_loss",
            "fallback_degraded_mode",
            "quarantine_status",
            "notification_status",
        ],
        "runtime_monitoring_enabled": False,
        **meta,
    }

    template_reuse = {
        "contract_id": "protocol_template_reuse_contract_v1",
        "reuse_mode": "shared_protocol_helpers_first",
        "fallback": "whitelist_file_template_reuse",
        "full_repo_scan_allowed": False,
        **meta,
    }

    l1_entries = _build_l1_registry_entries()
    l2_tm_entries = _build_l2_task_manager_entries()
    l2_future_entries = _build_l2_future_entries()
    all_entries = l1_entries + l2_tm_entries + l2_future_entries

    classification_registry = {
        "registry_id": "existing_protocol_classification_registry_v1",
        "L1_system_protocols": l1_entries,
        "L2_task_manager_protocols": l2_tm_entries,
        "L2_future_module_protocols": l2_future_entries,
        "total_protocols": len(all_entries),
        "existing_protocol_classification_complete": len(all_entries) >= 29,
        **meta,
    }

    layer_mapping = {
        "mapping_id": "existing_protocol_layer_mapping_v1",
        "L0": list(L0_PROTOCOLS),
        "L1": [e["suggested_protocol_id"] for e in l1_entries],
        "L2_task_manager": [e["suggested_protocol_id"] for e in l2_tm_entries],
        "L2_future": [e["suggested_protocol_id"] for e in l2_future_entries],
        "L3": ["capability_contract", "adapter_io_contract", "local_verifier", "local_diagnostics", "local_artifact"],
        **meta,
    }

    error_namespace_mapping = {
        "mapping_id": "existing_protocol_error_namespace_mapping_v1",
        "entries": [
            {"protocol_id": e["suggested_protocol_id"], "error_namespace": e["error_namespace"]}
            for e in all_entries
        ],
        "existing_protocol_error_namespace_mapping_complete": all(
            e.get("error_namespace") for e in all_entries
        ),
        **meta,
    }

    whitebox_binding_map = {
        "mapping_id": "existing_protocol_whitebox_binding_candidate_map_v1",
        "entries": [
            {
                "protocol_id": e["suggested_protocol_id"],
                "whitebox_binding_required": e["whitebox_binding_required"],
                "whitebox_binding_candidate": f"wb-candidate://{e['suggested_protocol_id']}",
                "diagnostic_node_candidate": f"diag-candidate://{e['suggested_protocol_id']}",
                "runtime_integration": False,
            }
            for e in all_entries
        ],
        "existing_protocol_whitebox_binding_candidate_map_complete": all(
            e.get("whitebox_binding_required") for e in all_entries
        ),
        **meta,
    }

    governance_debt_update = {
        "update_id": "existing_protocol_governance_debt_update_v1",
        "debts": list(GOVERNANCE_DEBTS),
        "governance_debt_update_complete": len(GOVERNANCE_DEBTS) >= 6,
        **meta,
    }

    boundary_contract = {
        "contract_id": "protocol_canonical_standard_boundary_contract_v1",
        "statements": list(BOUNDARY_CONTRACT_STATEMENTS),
        "non_execution_boundary_ok": True,
        **meta,
    }

    protocol_canonical_standard_plan_complete = (
        numbering_standard["protocol_numbering_standard_complete"]
        and error_code_standard["protocol_error_code_standard_complete"]
        and execution_result_schema["protocol_execution_result_schema_complete"]
        and error_taxonomy["error_taxonomy_complete"]
        and whitebox_contract["whitebox_diagnostic_binding_contract_complete"]
        and protocol_first_rule["protocol_first_development_rule_complete"]
        and module_layering["module_protocol_layering_complete"]
        and assimilation_supervision["protocol_assimilation_supervision_standard_complete"]
        and shared_code_design["shared_protocol_code_design_complete"]
        and checker_flow["standard_checker_flow_complete"]
        and verifier_contract["standard_verifier_contract_complete"]
        and classification_registry["existing_protocol_classification_complete"]
        and error_namespace_mapping["existing_protocol_error_namespace_mapping_complete"]
        and whitebox_binding_map["existing_protocol_whitebox_binding_candidate_map_complete"]
        and governance_debt_update["governance_debt_update_complete"]
    )

    runtime_execution_absent = meta["runtime_execution_enabled"] is False
    protocol_migration_execution_absent = meta["protocol_migration_executed"] is False
    whitebox_runtime_integration_absent = meta["whitebox_runtime_integrated"] is False
    module_adapter_implementation_absent = meta["module_adapter_implementation_ready"] is False
    foundation_not_frozen = meta["foundation_frozen"] is False
    closure_not_executed = meta["closure_executed"] is False
    grant_not_issued = meta["grant_issued"] is False
    owner_approval_record_absent = meta["owner_approval_record_created"] is False
    request_record_absent = meta["request_record_created"] is False
    non_execution_boundary_ok = all(
        meta.get(flag) is False for flag in NON_EXECUTION_FLAGS
    )

    if not shared_code_design["modules_exist"]:
        issues.append("shared_code_modules_missing")

    go_condition_values = {
        "protocol_canonical_standard_plan_complete": protocol_canonical_standard_plan_complete,
        "protocol_numbering_standard_complete": numbering_standard["protocol_numbering_standard_complete"],
        "protocol_error_code_standard_complete": error_code_standard["protocol_error_code_standard_complete"],
        "protocol_execution_result_schema_complete": execution_result_schema[
            "protocol_execution_result_schema_complete"
        ],
        "error_taxonomy_complete": error_taxonomy["error_taxonomy_complete"],
        "whitebox_diagnostic_binding_contract_complete": whitebox_contract[
            "whitebox_diagnostic_binding_contract_complete"
        ],
        "protocol_first_development_rule_complete": protocol_first_rule[
            "protocol_first_development_rule_complete"
        ],
        "module_protocol_layering_complete": module_layering["module_protocol_layering_complete"],
        "protocol_assimilation_supervision_standard_complete": assimilation_supervision[
            "protocol_assimilation_supervision_standard_complete"
        ],
        "shared_protocol_code_design_complete": shared_code_design["shared_protocol_code_design_complete"],
        "standard_checker_flow_complete": checker_flow["standard_checker_flow_complete"],
        "standard_verifier_contract_complete": verifier_contract["standard_verifier_contract_complete"],
        "existing_protocol_classification_complete": classification_registry[
            "existing_protocol_classification_complete"
        ],
        "existing_protocol_error_namespace_mapping_complete": error_namespace_mapping[
            "existing_protocol_error_namespace_mapping_complete"
        ],
        "existing_protocol_whitebox_binding_candidate_map_complete": whitebox_binding_map[
            "existing_protocol_whitebox_binding_candidate_map_complete"
        ],
        "governance_debt_update_complete": governance_debt_update["governance_debt_update_complete"],
        "runtime_execution_absent": runtime_execution_absent,
        "protocol_migration_execution_absent": protocol_migration_execution_absent,
        "whitebox_runtime_integration_absent": whitebox_runtime_integration_absent,
        "module_adapter_implementation_absent": module_adapter_implementation_absent,
        "foundation_not_frozen": foundation_not_frozen,
        "closure_not_executed": closure_not_executed,
        "grant_not_issued": grant_not_issued,
        "owner_approval_record_absent": owner_approval_record_absent,
        "request_record_absent": request_record_absent,
        "non_execution_boundary_ok": non_execution_boundary_ok,
    }

    final_decision = FINAL_DECISION_GO if protocol_canonical_standard_plan_complete and not issues else FINAL_DECISION_BLOCKED
    planning_pass = len(issues) == 0 and final_decision == FINAL_DECISION_GO and all(go_condition_values.values())

    protocol_plan = {
        "plan_id": "protocol_canonical_standard_plan_v1",
        "definition_zh": PROTOCOL_DEFINITION_ZH,
        "definition_en": PROTOCOL_DEFINITION_EN,
        "objectives": [
            "define unified protocol numbering and error code standards",
            "design shared protocol code and checker flow for reuse",
            "classify existing protocols into L1/L2/L3 registry",
            "establish protocol-first development rule",
            "preserve non-execution boundary and governance debt",
        ],
        "boundary_contract": list(BOUNDARY_CONTRACT_STATEMENTS),
        **go_condition_values,
        "final_decision": final_decision,
        "recommended_next_phase_primary": NEXT_PHASE_PRIMARY,
        "recommended_next_phase_alt": NEXT_PHASE_ALT,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_pass": planning_pass,
        "blocker_count": len(issues),
        "issues": issues,
        "go_conditions": go_condition_values,
        "final_decision": final_decision,
        "recommended_next_phase_primary": NEXT_PHASE_PRIMARY,
        "recommended_next_phase_alt": NEXT_PHASE_ALT,
        **go_condition_values,
        **meta,
    }

    markdown = "\n".join(
        [
            "# Protocol Canonical Standard Plan v1",
            "",
            "This phase performs protocol canonical standard planning only. It does not execute protocol runtime, migrate existing protocols, or integrate whitebox runtime.",
            "",
            "本阶段仅执行 protocol canonical standard planning，不实现真实 runtime，不改动授权执行，不生成 grant / request record / owner approval record，不冻结 foundation，不执行 closure。",
            "",
            f"Protocol definition (ZH): `{PROTOCOL_DEFINITION_ZH}`",
            f"Protocol definition (EN): `{PROTOCOL_DEFINITION_EN}`",
            f"Numbering format: `{NUMBERING_FORMAT}`",
            f"Error code format: `{{PROTOCOL_ID}}::{{ERROR_CLASS}}-{{NUMBER}}`",
            f"Total classified protocols: `{len(all_entries)}`",
            f"Shared code modules: `{len(SHARED_CODE_MODULES)}`",
            f"Governance debts tracked: `{len(GOVERNANCE_DEBTS)}`",
            f"Final decision: `{final_decision}`",
            f"Recommended next phase (primary): `{NEXT_PHASE_PRIMARY}`",
            f"Recommended next phase (alt): `{NEXT_PHASE_ALT}`",
            "",
            "## Boundary Contract",
            *[f"- {stmt}" for stmt in BOUNDARY_CONTRACT_STATEMENTS],
            "",
            "## Protocol-First Development Rule",
            "- New lifecycle/record/approval/evidence stages must check L1/L2 reuse first",
            "- Forbidden to invent protocol fields and error codes ad-hoc during module development",
            "",
            "## Governance Debt (P1, not implemented now)",
            *[f"- {d['debt_title']}" for d in GOVERNANCE_DEBTS],
        ]
    )

    return {
        "protocol_canonical_standard_plan": protocol_plan,
        "protocol_canonical_standard_plan_md": markdown,
        "protocol_numbering_standard": numbering_standard,
        "protocol_error_code_standard": error_code_standard,
        "protocol_execution_result_schema": execution_result_schema,
        "constitution_process_interface_assimilation_error_taxonomy": error_taxonomy,
        "whitebox_diagnostic_binding_contract": whitebox_contract,
        "protocol_first_development_rule": protocol_first_rule,
        "protocol_constraint_vs_module_logic_separation_rule": separation_rule,
        "module_internal_vs_cross_module_protocol_layering": module_layering,
        "protocol_assimilation_supervision_standard": assimilation_supervision,
        "protocol_failure_handling_notification_standard": failure_handling,
        "protocol_shared_code_design": shared_code_design,
        "protocol_shared_checker_flow": checker_flow,
        "protocol_standard_api_contract": api_contract,
        "protocol_standard_verifier_contract": verifier_contract,
        "protocol_error_object_schema": error_object_schema,
        "protocol_health_monitor_contract": health_monitor,
        "protocol_template_reuse_contract": template_reuse,
        "existing_protocol_classification_registry": classification_registry,
        "existing_protocol_layer_mapping": layer_mapping,
        "existing_protocol_error_namespace_mapping": error_namespace_mapping,
        "existing_protocol_whitebox_binding_candidate_map": whitebox_binding_map,
        "existing_protocol_governance_debt_update": governance_debt_update,
        "protocol_boundary_contract": boundary_contract,
        "summary": summary,
    }
