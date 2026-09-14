# -*- coding: utf-8 -*-
"""Field-First Adapter Priority Download Authorization Planning template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_FIRST_ADAPTER_PLAN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_model_document_capability_review_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_model_document_capability_review_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_model_document_capability_review_v1.py",
)

FIELD_FIRST_ADAPTER_PLAN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_first_core_model_document_capability_review", "stage_term": "field_first_core_adapter_priority_download_authorization_planning"},
    {"base_term": "field_first_core_model_document_review_only", "stage_term": "field_first_core_adapter_priority_planning_only"},
    {"base_term": "field_first_core_model_document_capability_review_pass", "stage_term": "field_first_core_adapter_priority_planning_pass"},
)

FIELD_FIRST_ADAPTER_PLAN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_model_document_review_go",
    "adapter_priority_queue_complete",
    "adapter_batch_plan_complete",
    "download_authorization_plan_complete",
    "owner_review_candidate_downloads_complete",
    "all_download_authorized_remain_false",
    "self_developed_skeletons_prioritized",
    "field_first_core_adapter_priority_planning_only",
    "file_size_governance_review_ok",
)
