# -*- coding: utf-8 -*-
"""Information Processing Core Work Manual item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

ORGANIZATION_CONTEXT: Dict[str, Any] = {
    "context_id": "organization_context_v1",
    "organization": "Midplatform",
    "parent_framework": "information_processing_candidate_governance_module_coordination_traceability_state_transition",
    "role_positioning": (
        "midplatform_information_receptionist",
        "information_classifier",
        "information_normalizer",
        "candidate_object_generator",
    ),
    "stage_positioning": "candidate_level_non_runtime_controlled",
    "luna_relationship": "unified_information_entry_for_task_perception_memory_worldmodel_governance_reflection_modules",
}

CORE_WORK_DEFINITION: Dict[str, Any] = {
    "definition_id": "core_work_definition_v1",
    "primary_core_function": "Information Processing Core",
    "core_work_items": (
        "receive_upstream_information",
        "identify_information_type",
        "judge_processability",
        "normalize_information",
        "form_information_candidate",
        "bind_traceability_refs",
        "bind_governance_refs",
        "decide_lifecycle_manager_handoff",
        "decide_core_orchestration_handoff",
        "output_candidate_level_processing_result",
    ),
    "not_core_work": (
        "final_task_decision",
        "real_world_action",
        "record_grant_authorization_request_creation",
        "runtime_route",
        "long_term_memory_write",
        "world_model_fact_admission",
        "drive_brain_reflection_brain",
    ),
}

ROLE_JOB_DEFINITION: Dict[str, Any] = {
    "definition_id": "role_job_definition_v1",
    "job_title": "Information Processing Core Operator",
    "job_mission": "Receive, classify, normalize, and candidate-wrap information without runtime execution",
    "job_metaphors": ("information_front_desk", "information_sorter", "information_normalizer", "candidate_generator"),
    "internal_external": {"internal": "midplatform_core_processing_lane", "external": "upstream_intake_downstream_candidate_delivery"},
    "upstream_sources": ("user_input", "perception", "ocr_vision", "task_manager", "governance", "health_signal", "system_signal", "future_memory_worldmodel_hooks"),
    "downstream_targets": ("candidate_lifecycle_manager", "core_orchestration", "alignment_support", "governance_constraints", "traceability_registry"),
    "inputs": ("raw_information", "source_ref", "context_refs", "optional_type_hint"),
    "outputs": ("InformationCandidate", "classification_candidate", "normalization_candidate", "processing_result_candidate"),
    "permissions": ("candidate_construction", "type_classification", "normalization", "defer_reject_close_marking"),
    "forbidden": ("record_creation", "grant_issuance", "authorization_request", "runtime_execution", "memory_worldmodel_write", "downstream_work_absorption"),
    "minimum_capability_tags": (
        "can_receive_raw_information", "can_identify_information_type", "can_allow_unknown_information",
        "can_normalize_information_input", "can_build_information_candidate",
    ),
}

INFORMATION_TYPES: Tuple[str, ...] = (
    "task_input", "user_instruction", "system_signal", "evidence_input",
    "governance_signal", "approval_signal", "permission_signal",
    "memory_signal", "world_model_signal", "health_signal", "unknown_information",
)

WORK_DETAIL_ITEMS: Tuple[Dict[str, Any], ...] = (
    {"work_id": "receive_raw_information", "action": "accept_raw_payload_with_source_ref", "output": "received_information_envelope"},
    {"work_id": "judge_information_source", "action": "validate_source_ref_and_trust_tier", "output": "source_check_result"},
    {"work_id": "judge_information_type", "action": "classify_into_information_type_registry", "output": "classification_candidate"},
    {"work_id": "check_missing_fields", "action": "completeness_check_against_type_schema", "output": "completeness_result"},
    {"work_id": "handle_unknown_information", "action": "mark_unknown_and_defer_or_reject", "output": "unknown_information_candidate"},
    {"work_id": "normalize_information", "action": "standardize_to_candidate_schema", "output": "normalization_candidate"},
    {"work_id": "build_information_candidate", "action": "assemble_information_candidate", "output": "InformationCandidate"},
    {"work_id": "attach_traceability_refs", "action": "bind_protocol_and_chain_refs", "output": "traceability_bundle_ref"},
    {"work_id": "attach_governance_refs", "action": "bind_governance_constraint_refs", "output": "governance_ref_set"},
    {"work_id": "mark_processing_status", "action": "set_ready_defer_reject_unknown_close", "output": "processing_status_candidate"},
    {"work_id": "output_to_downstream", "action": "route_candidate_to_lifecycle_or_orchestration", "output": "downstream_handoff_candidate"},
)

INTERNAL_WORKFLOW_STEPS: Tuple[Dict[str, Any], ...] = tuple(
    {
        "step_id": sid,
        "input": inp,
        "output": out,
        "on_failure": fail,
        "may_continue": cont,
        "may_handoff": handoff,
        "may_defer": defer,
        "may_reject": reject,
    }
    for sid, inp, out, fail, cont, handoff, defer, reject in (
        ("receive_information", "raw_information", "received_envelope", "reject_missing_source", True, False, False, True),
        ("source_check", "received_envelope", "source_check_result", "reject_untrusted_source", True, False, True, True),
        ("type_signal_detection", "received_envelope", "type_signal", "mark_unknown", True, False, True, False),
        ("information_classification", "type_signal", "classification_candidate", "defer_ambiguous", True, False, True, True),
        ("input_normalization", "classification_candidate", "normalization_candidate", "reject_unnormalizable", True, False, True, True),
        ("completeness_check", "normalization_candidate", "completeness_result", "defer_incomplete", True, False, True, True),
        ("traceability_attachment", "normalization_candidate", "traceability_refs", "reject_missing_trace", False, False, True, True),
        ("governance_attachment", "normalization_candidate", "governance_refs", "reject_missing_gov_when_required", True, False, True, True),
        ("candidate_construction", "normalization_candidate", "InformationCandidate", "reject_invalid_candidate", True, True, False, True),
        ("downstream_readiness_marking", "InformationCandidate", "readiness_marker", "defer_not_ready", True, True, True, False),
        ("processing_result_assembly", "InformationCandidate", "processing_result_candidate", "close_on_fatal", True, True, False, False),
        ("close_defer_reject_unknown", "processing_result_candidate", "terminal_status_candidate", "none", False, True, True, True),
    )
)

EXTERNAL_WORKFLOW: Dict[str, Any] = {
    "workflow_id": "external_workflow_v1",
    "upstream_sources": list(ROLE_JOB_DEFINITION["upstream_sources"]),
    "downstream_targets": list(ROLE_JOB_DEFINITION["downstream_targets"]),
    "to_lifecycle_manager_when": ("lifecycle_state_unknown", "candidate_state_transition_needed", "feedback_state_update_needed"),
    "to_core_orchestration_when": ("boundary_alignment_governance_check_needed", "route_decision_needed", "orchestration_plan_needed"),
    "unknown_rejected_deferred_only_when": ("type_unresolvable", "completeness_blocked", "governance_hard_block", "overload"),
    "upstream_supplement_when": ("missing_required_fields", "ambiguous_classification", "missing_traceability_ref"),
    "must_not_continue_downstream_when": ("non_execution_violation", "safety_critical_block", "authorization_critical_block", "privacy_critical_block"),
}

JUDGE_REFEREE_RULES: Dict[str, Any] = {
    "rules_id": "judge_referee_rules_v1",
    "judges": ("static_validator", "module_dryrun_verifier", "governance_constraints", "work_manual_compliance_checker"),
    "correctness_criteria": (
        "classification_matches_evidence", "unknown_marked_when_unresolvable",
        "normalization_preserves_meaning", "traceability_complete", "governance_refs_complete_when_required",
    ),
    "overreach_signals": ("record_created", "grant_issued", "runtime_executed", "downstream_work_absorbed"),
    "omission_signals": ("unprocessed_input", "missing_type_mark", "missing_traceability", "wrong_downstream_handoff"),
    "responsibility": {
        "missing_input": "upstream_source",
        "classification_error": "information_processing_core",
        "downstream_rejection": "shared_with_downstream_judge",
        "protocol_mismatch": "protocol_owner_modify_protocol",
        "rule_blocks_core": "modify_rule_not_weaken_core_unless_safety_critical",
    },
}

GOVERNANCE_SERVICE_RULES: Dict[str, Any] = {
    "rules_id": "governance_protocol_boundary_service_rules_v1",
    "protocol_serves": "input_output_standardization_without_limiting_classification",
    "boundary_serves": "role_ownership_without_locking_type_extension",
    "governance_serves": "safety_overreach_protection_without_blocking_candidate_processing",
    "traceability_serves": "auditability_without_write_blocking",
    "handoff_serves": "downstream_carry_not_classification_prerequisite",
    "constitution_hard_constraint_only": ("safety", "authorization", "privacy"),
    "module_handoff_contract_not_required_for_information_classification": True,
    "integration_contract_not_required_for_information_classification": True,
    "peripheral_contract_does_not_constrain_core": True,
    "protocol_before_workflow_forbidden": True,
}

WORKLOAD_CONTROL: Dict[str, Any] = {
    "control_id": "workload_control_v1",
    "single_processing_scope": "one_information_envelope_per_processing_unit",
    "accepted_input_types": list(INFORMATION_TYPES),
    "unknown_handling": "mark_unknown_defer_or_reject_never_silent_drop",
    "missing_field_handling": "defer_with_missing_field_marker",
    "high_risk_handling": "governance_review_candidate_no_runtime",
    "duplicate_handling": "idempotency_ref_dedup_candidate",
    "queue_defer_rules": "fifo_with_priority_for_safety_critical",
    "reject_rules": "reject_when_non_execution_violation_or_fatal_schema_break",
    "overload_marker": "overload_candidate_with_defer_recommendation",
    "no_unbounded_classification_expansion": True,
    "no_downstream_work_absorption": True,
}

QUALIFICATION_STANDARD: Dict[str, Any] = {
    "standard_id": "qualification_standard_v1",
    "minimum_capability_tags": (
        "can_receive_raw_information", "can_identify_information_type", "can_allow_unknown_information",
        "can_normalize_information_input", "can_build_information_candidate",
        "can_attach_traceability_refs", "can_attach_governance_refs",
        "can_prepare_candidate_for_lifecycle", "can_prepare_candidate_for_orchestration",
        "can_reject_unprocessable_information", "can_defer_incomplete_information",
        "can_hold_non_execution_boundary",
    ),
    "go_criteria": (
        "work_manual_complete", "core_work_clear", "internal_external_workflow_clear",
        "judge_rules_clear", "workload_control_clear", "peripheral_rules_serve_core", "future_expansion_reserved",
    ),
}

FUTURE_EXPANSION: Dict[str, Any] = {
    "expansion_id": "future_expansion_v1",
    "reserved": (
        "external_model_classifier", "multimodal_input", "ocr_vision_audio_sensor",
        "memory_candidate_hook", "world_model_entry_hook", "health_signal_hook",
        "distributed_ready_fields", "feedback_based_state_update",
        "reflection_brain_review_hook", "task_drive_brain_intent_hook", "runtime_adapter_future_handoff",
    ),
}

SELECTED_NEXT_PHASE = "Phase-Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001"
SELECTED_NEXT_ROUTE = "Information Processing Core Controlled Implementation"
