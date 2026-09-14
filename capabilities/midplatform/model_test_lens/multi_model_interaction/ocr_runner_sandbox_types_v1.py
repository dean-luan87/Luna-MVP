# -*- coding: utf-8 -*-
"""OCR Runner Sandbox integration planning — types v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

PHASE_REF = (
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Planning-v1-001"
)
SYSTEM_ID = "LunaMidplatformMobileSamOcrRunnerSandboxIntegrationPlanningV1"
PLANNING_ONLY = True
PLANNING_ENDPOINT = "ocr_runner_sandbox_integration_plan"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO",
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_EXPLORATION_SMOKE_GO",
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_PLANNING_GO",
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_CONTROLLED_EXECUTION_UI_EXECUTION_GO",
)

FROZEN_CHAIN_STAGES = (
    "ocr_task_candidate",
    "ocr_invocation_request",
    "ocr_admission",
    "ocr_controlled_execution_candidate",
    "ocr_runner_sandbox",
    "ocr_runtime",
    "ocr_result_envelope",
    "midplatform_fusion",
    "fact_admission",
)

SANDBOX_ENTRY_ONLY = "ocr_controlled_execution_candidate"

FORBIDDEN_SANDBOX_ENTRY_PATHS = (
    "ui_direct_ocr_runner_call",
    "mobile_sam_result_direct_to_ocr_runner",
    "ocr_task_candidate_direct_to_ocr_runner",
    "human_correction_direct_to_ocr_runner",
    "bypass_admission",
    "bypass_execution_candidate",
)

OCR_ADAPTER_ALLOWED_INPUTS = (
    "source_image_ref",
    "source_region_id",
    "region_crop_ref",
    "region_geometry_ref",
    "source_ocr_execution_candidate_id",
    "source_ocr_task_candidate_id",
    "source_analysis_record_id",
    "ocr_target_reason",
    "trace_chain",
)

OCR_ADAPTER_FORBIDDEN_INPUTS = (
    "confirmed_text",
    "fact_label",
    "confirmed_object_type",
    "confirmed_sign_type",
    "human_correction_as_truth",
    "navigation_decision",
    "mobilesam_prompt_label_as_fact",
)

OCR_EXECUTION_STATUSES = ("pending", "running", "completed", "failed", "cancelled")

OCR_ERROR_TYPES = (
    "timeout",
    "runner_unavailable",
    "invalid_crop",
    "empty_text",
    "low_confidence",
    "invalid_output_schema",
    "unreadable_region",
    "route_mismatch",
    "cancelled",
)

OCR_RESULT_ENVELOPE_REQUIRED = (
    "ocr_result_envelope_id",
    "source_ocr_execution_id",
    "source_ocr_execution_candidate_id",
    "source_region_id",
    "text_candidate_list",
    "text_region_candidate",
    "reading_order_candidate",
    "confidence",
    "model_name",
    "model_version",
    "output_payload_ref",
    "candidate_only",
    "not_fact",
    "needs_fact_admission",
    "trace_chain",
)

HUMAN_CORRECTION_RUNTIME_ROUTING = (
    ("text_read_wrong", "ocr_model_error", "ocr_training_candidate_pending_review"),
    ("wrong_region", "mobilesam_region_selection_error", "mobile_sam_rerun_candidate"),
    ("should_not_read", "ocr_route_strategy_error", "ocr_route_policy_update_candidate"),
    ("should_not_read_alt", "attention_priority_error", "priority_update_signal"),
    ("read_more_sign_type", "user_preference", "preference_memory_candidate"),
)

SCHEMA_REFS = {
    "adapter_input": "schemas/multi_model_interaction/ocr_adapter_input_schema_v1.json",
    "execution_record": "schemas/multi_model_interaction/ocr_runner_execution_record_schema_v1.json",
    "result_envelope": "schemas/multi_model_interaction/ocr_result_envelope_schema_v1.json",
    "error_candidate": "schemas/multi_model_interaction/ocr_runner_error_candidate_schema_v1.json",
    "bridge_contract": "schemas/multi_model_interaction/ocr_local_runner_bridge_contract_v1.json",
    "fusion_input": "schemas/multi_model_interaction/mobile_sam_ocr_fusion_input_schema_v1.json",
}

RECOMMENDED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Execution-v1-001"
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "ocr_runner_execution_allowed_future": True,
    "ocr_runner_execution_in_this_phase": False,
    "ocr_runner_requires_execution_candidate": True,
    "no_ui_direct_ocr_runner_call": True,
    "no_mobile_sam_direct_to_ocr_runner": True,
    "ocr_output_requires_result_envelope": True,
    "ocr_output_not_fact": True,
    "ocr_completed_not_fact": True,
    "ocr_error_not_fact": True,
    "fusion_candidate_not_fact": True,
    "no_visual_expression_mutation": True,
    "no_ocr_box_on_canvas": True,
}


def validate_ocr_execution_candidate(candidate: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Planning stub — validate sandbox entry candidate."""
    if not candidate:
        return False, "missing_execution_candidate"
    if candidate.get("execution_status") not in ("planned_only", "ready_for_execution_review"):
        return False, "invalid_execution_status"
    if not candidate.get("ocr_execution_candidate_id"):
        return False, "missing_candidate_id"
    if not candidate.get("trace_chain"):
        return False, "trace_chain_incomplete"
    blob = str(candidate).lower()
    for forbidden in OCR_ADAPTER_FORBIDDEN_INPUTS:
        if forbidden in blob:
            return False, f"forbidden_input_{forbidden}"
    return True, None


def build_ocr_adapter_input(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Planning stub — build adapter input from execution candidate."""
    ok, reason = validate_ocr_execution_candidate(candidate)
    if not ok:
        raise ValueError(reason or "invalid_candidate")
    return {
        "adapter_type": "ocr_adapter_input",
        "source_image_ref": candidate.get("input_crop_ref", "").split("#")[0],
        "source_region_id": candidate.get("source_region_id"),
        "region_crop_ref": candidate.get("input_crop_ref"),
        "region_geometry_ref": candidate.get("input_region_geometry_ref"),
        "source_ocr_execution_candidate_id": candidate.get("ocr_execution_candidate_id"),
        "source_ocr_task_candidate_id": candidate.get("source_ocr_task_candidate_id"),
        "source_analysis_record_id": candidate.get("source_analysis_record_id"),
        "ocr_target_reason": candidate.get("ocr_target_reason", "text_observation_candidate"),
        "trace_chain": candidate.get("trace_chain", []),
        "candidate_only": True,
        "not_fact": True,
        "planning_only": True,
    }


def build_ocr_runner_error_candidate(
    error_type: str,
    *,
    execution_candidate_id: str,
    reason: str,
    recoverable: bool = False,
    trace_chain: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """Planning stub — error candidate builder."""
    if error_type not in OCR_ERROR_TYPES:
        error_type = "invalid_output_schema"
    return {
        "error_candidate_id": f"oerr_ocr_{execution_candidate_id}",
        "error_type": error_type,
        "error_stage": "ocr_runner_sandbox",
        "error_reason": reason,
        "source_ocr_execution_candidate_id": execution_candidate_id,
        "recoverable": recoverable,
        "not_fact": True,
        "not_navigation_decision": True,
        "trace_chain": trace_chain or [],
        "planning_only": True,
    }
