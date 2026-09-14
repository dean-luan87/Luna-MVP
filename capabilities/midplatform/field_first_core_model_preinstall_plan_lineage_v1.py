# -*- coding: utf-8 -*-
"""Field-First Model Preinstall Plan template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_FIRST_PREINSTALL_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_ideal_operation_mechanism_and_model_requirement_mapping_v1.py",
)

FIELD_FIRST_PREINSTALL_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_first_core_ideal_operation_mechanism_and_model_requirement_mapping", "stage_term": "field_first_core_model_preinstall_plan"},
    {"base_term": "field_first_core_ideal_operation_mechanism_only", "stage_term": "field_first_core_model_preinstall_plan_only"},
    {"base_term": "field_first_core_ideal_operation_mechanism_pass", "stage_term": "field_first_core_model_preinstall_plan_pass"},
)

FIELD_FIRST_PREINSTALL_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_ideal_operation_go",
    "preinstall_manifest_complete",
    "model_room_registry_complete",
    "adapter_placeholder_registry_complete",
    "capability_review_queue_complete",
    "download_authorization_all_false",
    "field_first_core_model_preinstall_plan_only",
    "file_size_governance_review_ok",
)
