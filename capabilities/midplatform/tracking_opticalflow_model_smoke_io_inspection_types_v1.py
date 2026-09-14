# -*- coding: utf-8 -*-
"""Tracking / Optical Flow model smoke IO inspection types v1."""

from __future__ import annotations

from typing import Dict, Tuple

MODEL_SMOKE_RUN_FIELDS: Tuple[str, ...] = (
    "smoke_run_id", "model_role", "model_name", "model_ref", "execution_mode",
    "input_refs", "output_refs", "execution_status", "runtime_environment_summary",
    "failure_points", "warning_codes", "candidate_only",
)

MODEL_IO_INSPECTION_FIELDS: Tuple[str, ...] = (
    "io_inspection_id", "smoke_run_ref", "input_format_observed", "output_format_observed",
    "output_payload_type", "output_schema_summary", "output_sample_refs",
    "parseability_status", "candidate_mapping_feasibility", "missing_information",
    "warning_codes", "candidate_only",
)

MAPPING_FEASIBILITY_FIELDS: Tuple[str, ...] = (
    "mapping_feasibility_id", "model_role", "source_output_refs", "reusable_existing_candidates",
    "candidate_mapping_targets", "mapping_status", "mapping_blockers",
    "reason_if_new_candidate_needed", "owner_approval_required_for_new_protocol", "candidate_only",
)

EXECUTION_MODES: Tuple[str, ...] = (
    "local_real_model", "local_adapter", "cached_output", "adapter_stub",
    "blocked_by_authorization", "blocked_by_missing_dependency", "blocked_by_missing_weight",
    "failed_runtime_error",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_field_simulation": True,
    "no_adapter_skeleton_yet": True,
    "no_world_model_assembly": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_task_reasoning": True,
    "no_task_action_output": True,
    "no_navigation_suggestion": True,
    "no_unauthorized_download": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_large_dependency_install": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_production_runtime": True,
    "no_new_protocol_without_reason": True,
    "model_smoke_io_inspection_only": True,
    "cached_output_not_marked_as_real_run": True,
    "adapter_stub_not_marked_as_real_run": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_TRACKING_OPTICALFLOW_MODEL_SMOKE_IO_INSPECTION_READY_FOR_TRACKING_OPTICALFLOW_ADAPTER_SKELETON"
)
