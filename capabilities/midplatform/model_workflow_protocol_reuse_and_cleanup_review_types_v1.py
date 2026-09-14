# -*- coding: utf-8 -*-
"""Model workflow protocol reuse and cleanup review — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_field_simulation": True,
    "no_simulation_test_route": True,
    "no_task_reasoning_execution": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_task_action_output": True,
    "no_model_runtime": True,
    "no_unauthorized_download": True,
    "no_new_protocol_without_reason": True,
    "cleanup_review_only": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_MODEL_WORKFLOW_PROTOCOL_REUSE_AND_CLEANUP_REVIEW_READY_FOR_MODEL_ADAPTER_PRIORITY_SEQUENCE_PLANNING"
)

CLASSIFICATION_STATUSES: Tuple[str, ...] = (
    "active",
    "keep_as_reference",
    "deprecated",
    "disabled",
    "cleanup_required",
    "reject_from_mainline",
)
