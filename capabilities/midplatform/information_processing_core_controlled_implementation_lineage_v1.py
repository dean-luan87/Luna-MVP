# -*- coding: utf-8 -*-
"""Information Processing Core Controlled Implementation template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

IPC_CONTROLLED_IMPLEMENTATION_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/information_processing_core_work_manual_definition_v1.py",
    "tools/evaluation/midplatform/run_information_processing_core_work_manual_definition_v1.py",
    "tools/evaluation/midplatform/verify_information_processing_core_work_manual_definition_v1.py",
)

IPC_CONTROLLED_IMPLEMENTATION_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "information_processing_core_work_manual_definition", "stage_term": "information_processing_core_controlled_implementation"},
    {"base_term": "information_processing_core_work_manual_definition_only", "stage_term": "information_processing_core_controlled_implementation_only"},
    {"base_term": "information_processing_core_work_manual_definition_pass", "stage_term": "information_processing_core_controlled_implementation_pass"},
)

IPC_CONTROLLED_IMPLEMENTATION_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_information_processing_core_work_manual_go",
    "information_processing_core_implemented",
    "information_type_registry_complete",
    "controlled_information_processing_smoke_ok",
    "all_smoke_cases_passed",
    "core_capability_marking_ok",
    "workload_control_validation_ok",
    "strong_coupled_single_package_ok",
    "all_outputs_candidate_only",
    "non_execution_guard_ok",
    "implementation_not_split_into_subphases",
    "information_processing_core_controlled_implementation_only",
    "file_size_governance_review_ok",
)

CORE_IMPLEMENTATION_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/information_processing_core_types_v1.py",
    "capabilities/midplatform/information_processing_core_contracts_v1.py",
    "capabilities/midplatform/information_processing_core_classifiers_v1.py",
    "capabilities/midplatform/information_processing_core_builders_v1.py",
    "capabilities/midplatform/information_processing_core_static_validators_v1.py",
    "capabilities/midplatform/information_processing_core_v1.py",
)

NON_EXECUTION_GUARDS: Tuple[str, ...] = (
    "no_record_creation",
    "no_grant_creation",
    "no_authorization_request_creation",
    "no_runtime_execution",
    "no_route_execution",
    "no_real_handoff_execution",
    "no_candidate_promotion_execution",
    "no_whitebox_runtime_call",
    "no_persistent_write",
)

CORE_CAPABILITY_TAGS: Tuple[str, ...] = (
    "can_receive_raw_information",
    "can_identify_information_type",
    "can_allow_unknown_information",
    "can_normalize_information_input",
    "can_build_information_candidate",
    "can_attach_traceability_refs",
    "can_attach_governance_refs",
    "can_prepare_candidate_for_lifecycle",
    "can_prepare_candidate_for_orchestration",
    "can_reject_unprocessable_information",
    "can_defer_incomplete_information",
    "can_hold_non_execution_boundary",
)

SMOKE_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "task_input", "type_hint": "task_input", "payload_kind": "task", "content_summary": "task input payload"},
    {"case_id": "user_instruction", "type_hint": "user_instruction", "payload_kind": "instruction", "content_summary": "user instruction payload"},
    {"case_id": "system_signal", "type_hint": "system_signal", "payload_kind": "system", "content_summary": "system signal payload"},
    {"case_id": "evidence_input", "type_hint": "evidence_input", "payload_kind": "evidence", "content_summary": "evidence input payload"},
    {"case_id": "governance_signal", "type_hint": "governance_signal", "payload_kind": "governance", "content_summary": "governance safety signal"},
    {"case_id": "approval_signal", "type_hint": "approval_signal", "payload_kind": "approval", "content_summary": "approval signal payload"},
    {"case_id": "permission_signal", "type_hint": "permission_signal", "payload_kind": "permission", "content_summary": "permission signal payload"},
    {"case_id": "memory_signal", "type_hint": "memory_signal", "payload_kind": "memory", "content_summary": "memory signal payload"},
    {"case_id": "world_model_signal", "type_hint": "world_model_signal", "payload_kind": "world_model", "content_summary": "world model signal payload"},
    {"case_id": "health_signal", "type_hint": "health_signal", "payload_kind": "health", "content_summary": "health signal payload"},
    {"case_id": "unknown_information", "type_hint": "unknown_information", "payload_kind": "opaque", "content_summary": "unrecognized opaque payload"},
    {"case_id": "incomplete_information_defer", "type_hint": "task_input", "payload_kind": "task", "content_summary": "incomplete task", "required_fields": "task_id,source", "present_fields": "task_id"},
    {"case_id": "high_risk_information_governance_review", "type_hint": "governance_signal", "payload_kind": "governance", "content_summary": "high_risk safety authorization privacy signal"},
    {"case_id": "duplicate_information_idempotency", "type_hint": "task_input", "payload_kind": "task", "content_summary": "duplicate task input", "idempotency_ref": "idem:ipc:smoke:001"},
)
