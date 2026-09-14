# -*- coding: utf-8 -*-
"""IPC Self-Work Core Design item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

DESIGN_PRINCIPLES: Tuple[Dict[str, str], ...] = (
    {"principle_id": "self_first", "summary": "Define IPC internal processing before upstream handshake and downstream delivery"},
    {"principle_id": "downstream_emerges", "summary": "Downstream roles emerge from IPC outputs; no premature contract"},
    {"principle_id": "explainable_conclusions", "summary": "Every conclusion must include reasons, gaps, risks, and next-step hints"},
    {"principle_id": "unknown_is_valid", "summary": "unknown_information is legal; silent drop and forced misclassification are errors"},
    {"principle_id": "no_downstream_swallow", "summary": "IPC does not absorb lifecycle, orchestration, execution, memory, or world model admission"},
)

THREE_PART_WORK_MODEL: Dict[str, Any] = {
    "model_id": "three_part_work_model_positioning_v1",
    "upstream_work": ("reception", "handshake", "rhythm", "return", "feedback", "supervision"),
    "self_work": (
        "internal_processing", "type_identification", "normalization", "conclusion_generation",
        "traceability", "self_check", "workload_control",
    ),
    "downstream_work": ("candidate_delivery", "downstream_selection", "delivery_standard", "feedback_recovery"),
    "this_phase_scope": "self_work_design_only",
    "upstream_scope": "minimum_assumption_register_only",
    "downstream_scope": "need_observation_only_no_contract",
    "self_work_first": True,
    "downstream_contract_not_defined_yet": True,
    "upstream_protocol_not_rewritten_yet": True,
}

SELF_WORK_SCOPE: Dict[str, Any] = {
    "scope_id": "ipc_self_work_scope_v1",
    "responsibilities": (
        "receive_single_raw_envelope", "judge_information_source", "identify_information_type",
        "check_completeness", "check_risk_attributes", "normalize_information",
        "generate_information_candidate", "generate_processing_conclusion",
        "generate_explanation_chain", "self_check_processing",
    ),
    "not_responsibilities": (
        "final_task_decision", "lifecycle_state_management", "real_execution",
        "long_term_memory_write", "world_model_fact_admission", "record_grant_auth_request",
    ),
}

INFORMATION_TYPES: Tuple[str, ...] = (
    "task_input", "user_instruction", "system_signal", "evidence_input",
    "governance_signal", "approval_signal", "permission_signal",
    "memory_signal", "world_model_signal", "health_signal", "unknown_information",
)

INTERNAL_PROCESSING_FLOW: Tuple[Dict[str, Any], ...] = (
    {"step_id": "receive_information", "input": "raw_information_envelope", "output": "processing_id_envelope", "on_failure": "reject_missing_content"},
    {"step_id": "source_check", "input": "processing_id_envelope", "output": "source_check_result", "on_failure": "mark_source_missing_or_untrusted"},
    {"step_id": "type_signal_detection", "input": "envelope_with_source", "output": "type_signals", "on_failure": "mark_unknown_signal"},
    {"step_id": "information_classification", "input": "type_signals", "output": "information_type", "on_failure": "unknown_information"},
    {"step_id": "input_normalization", "input": "classified_envelope", "output": "normalized_structure", "on_failure": "reject_unnormalizable"},
    {"step_id": "completeness_check", "input": "normalized_structure", "output": "completeness_result", "on_failure": "incomplete_information_defer"},
    {"step_id": "risk_check", "input": "normalized_structure", "output": "risk_check_result", "on_failure": "governance_review_candidate"},
    {"step_id": "duplicate_check", "input": "envelope_with_idempotency", "output": "duplicate_check_result", "on_failure": "idempotency_dedup_result"},
    {"step_id": "candidate_construction", "input": "normalized_structure", "output": "InformationCandidate", "on_failure": "reject_invalid_candidate"},
    {"step_id": "traceability_and_governance_attachment", "input": "InformationCandidate", "output": "candidate_with_refs", "on_failure": "weak_traceability_or_governance_marker"},
    {"step_id": "conclusion_generation", "input": "candidate_with_refs", "output": "ipc_conclusion", "on_failure": "deferred_or_rejected_conclusion"},
    {"step_id": "self_check_and_result_assembly", "input": "ipc_conclusion", "output": "InformationProcessingResultCandidate", "on_failure": "self_check_block_or_defer"},
)

CONCLUSION_TYPES: Tuple[Dict[str, Any], ...] = tuple(
    {"conclusion_type": ct, "requires_downstream": req, "requires_upstream": up}
    for ct, req, up in (
        ("classified_as_type", False, False),
        ("normalized_candidate_ready", False, False),
        ("unknown_needs_more_context", False, True),
        ("incomplete_needs_upstream_fix", False, True),
        ("high_risk_needs_governance_review", True, False),
        ("duplicate_can_be_deduped", False, False),
        ("ambiguous_needs_referee_or_context", True, True),
        ("ready_for_lifecycle", True, False),
        ("ready_for_orchestration", True, False),
        ("rejected_as_unprocessable", False, True),
        ("deferred_for_later", False, False),
    )
)

CONCLUSION_REQUIRED_FIELDS: Tuple[str, ...] = (
    "conclusion_id", "conclusion_type", "source_basis", "classification_reason",
    "normalization_reason", "risk_reason", "missing_fields", "downstream_need_hint",
    "traceability_refs", "governance_refs", "non_execution_flags",
)

TRANSPARENCY_FIELDS: Tuple[str, ...] = (
    "input_ref", "source_ref", "raw_content_hash_or_summary", "detected_signals",
    "selected_information_type", "alternative_information_types", "classification_reason",
    "normalization_steps", "completeness_result", "risk_check_result", "duplicate_check_result",
    "candidate_build_reason", "conclusion_reason", "self_check_result", "downstream_need_hint",
)

SELF_CHECK_REFEREE_RULES: Tuple[Dict[str, Any], ...] = (
    {"check_id": "classification_check", "question": "classified or correctly marked unknown"},
    {"check_id": "completeness_check", "question": "incomplete not treated as complete"},
    {"check_id": "risk_check", "question": "high-risk not treated as normal"},
    {"check_id": "downstream_swallow_check", "question": "no lifecycle orchestration execution memory worldmodel absorption"},
    {"check_id": "side_effect_check", "question": "no record grant auth_request runtime action"},
    {"check_id": "traceability_check", "question": "minimum traceability present"},
    {"check_id": "governance_check", "question": "governance ref or risk marker present when required"},
    {"check_id": "unknown_handling_check", "question": "unknown not silently dropped"},
    {"check_id": "workload_check", "question": "single envelope scope respected overload not forced"},
    {"check_id": "conclusion_explainability_check", "question": "conclusion explainable and traceable"},
)

WORKLOAD_CONTROL_RULES: Tuple[Dict[str, Any], ...] = (
    {"rule_id": "single_envelope_processing", "value": True},
    {"rule_id": "classification_scope_bounded", "value": True, "bounded_types": list(INFORMATION_TYPES)},
    {"rule_id": "unknown_allowed", "value": True},
    {"rule_id": "incomplete_can_defer", "value": True},
    {"rule_id": "high_risk_governance_review_candidate", "value": True},
    {"rule_id": "duplicate_idempotency", "value": True},
    {"rule_id": "overload_can_defer", "value": True},
    {"rule_id": "downstream_work_not_swallowed", "value": True},
)

DOWNSTREAM_NEED_OBSERVATIONS: Tuple[Dict[str, Any], ...] = (
    {"need_id": "lifecycle_state_needed", "likely_role": "Candidate Lifecycle Manager", "is_contract": False},
    {"need_id": "orchestration_decision_needed", "likely_role": "Core Orchestration", "is_contract": False},
    {"need_id": "governance_review_needed", "likely_role": "Governance", "is_contract": False},
    {"need_id": "traceability_registry_needed", "likely_role": "Traceability / Protocol Registry", "is_contract": False},
    {"need_id": "upstream_fix_needed", "likely_role": "Upstream Source", "is_contract": False},
    {"need_id": "referee_needed", "likely_role": "Judge / Referee", "is_contract": False},
)

UPSTREAM_MINIMUM_ASSUMPTIONS: Tuple[Dict[str, Any], ...] = (
    {"assumption_id": "raw_content_must_exist", "tier": "required_now", "failure_handling": "reject", "blocks_self_work": True},
    {"assumption_id": "source_ref_preferred", "tier": "preferred", "failure_handling": "mark_source_missing", "blocks_self_work": False},
    {"assumption_id": "context_ref_optional", "tier": "optional", "failure_handling": "may_cause_unknown_or_ambiguous", "blocks_self_work": False},
    {"assumption_id": "traceability_ref_preferred", "tier": "preferred", "failure_handling": "weak_traceability_or_defer", "blocks_self_work": False},
    {"assumption_id": "governance_ref_for_sensitive", "tier": "preferred", "failure_handling": "governance_review_candidate", "blocks_self_work": False},
    {"assumption_id": "incomplete_input_legal_marked", "tier": "required_now", "failure_handling": "defer_not_fake_complete", "blocks_self_work": False},
)

CURRENT_NON_GOALS: Tuple[str, ...] = (
    "full_upstream_handshake_protocol", "full_downstream_delivery_protocol",
    "module_handoff_contract", "candidate_lifecycle_manager_implementation",
    "runtime", "integration_test", "record_creation", "grant_creation",
    "authorization_request_creation", "persistent_write", "memory_fact_admission",
    "world_model_fact_admission", "drive_brain", "reflection_brain",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Information-Processing-Core-Self-Work-Core-Capability-DryRun-v1-001"
SELECTED_NEXT_ROUTE = "IPC Self-Work Core Capability DryRun"
