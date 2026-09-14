# -*- coding: utf-8 -*-
"""Field-First Model I/O Compatibility Precheck template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_FIRST_IO_PRECHECK_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_model_document_capability_review_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_model_document_capability_review_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_model_document_capability_review_v1.py",
)

FIELD_FIRST_IO_PRECHECK_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_first_core_model_document_capability_review", "stage_term": "field_first_core_model_io_compatibility_precheck"},
    {"base_term": "field_first_core_model_document_review_only", "stage_term": "field_first_core_model_io_precheck_only"},
    {"base_term": "field_first_core_model_document_capability_review_pass", "stage_term": "field_first_core_model_io_compatibility_precheck_pass"},
)

FIELD_FIRST_IO_PRECHECK_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_model_document_review_go",
    "model_io_compatibility_precheck_complete",
    "model_io_to_candidate_mapping_complete",
    "candidate_schema_compatibility_matrix_complete",
    "skeleton_schema_adjustment_plan_complete",
    "field_first_skeleton_io_requirements_complete",
    "field_first_core_model_io_precheck_only",
    "file_size_governance_review_ok",
)
