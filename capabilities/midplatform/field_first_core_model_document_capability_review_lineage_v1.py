# -*- coding: utf-8 -*-
"""Field-First Model Document Capability Review template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_FIRST_DOC_REVIEW_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_model_preinstall_plan_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_model_preinstall_plan_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_model_preinstall_plan_v1.py",
)

FIELD_FIRST_DOC_REVIEW_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_first_core_model_preinstall_plan", "stage_term": "field_first_core_model_document_capability_review"},
    {"base_term": "field_first_core_model_preinstall_plan_only", "stage_term": "field_first_core_model_document_review_only"},
    {"base_term": "field_first_core_model_preinstall_plan_pass", "stage_term": "field_first_core_model_document_capability_review_pass"},
)

FIELD_FIRST_DOC_REVIEW_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_model_preinstall_plan_go",
    "prior_ideal_operation_go",
    "model_document_capability_review_complete",
    "review_item_registry_complete",
    "operation_node_model_fit_matrix_complete",
    "model_requirement_satisfaction_matrix_complete",
    "model_status_classification_complete",
    "field_first_core_model_document_review_only",
    "file_size_governance_review_ok",
)
