# -*- coding: utf-8 -*-
"""Field-First Ideal Operation Mechanism template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_FIRST_IDEAL_OP_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_role_function_redefinition_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_role_function_redefinition_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_role_function_redefinition_v1.py",
)

FIELD_FIRST_IDEAL_OP_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_first_core_role_function_redefinition", "stage_term": "field_first_core_ideal_operation_mechanism_and_model_requirement_mapping"},
    {"base_term": "field_first_core_role_function_redefinition_only", "stage_term": "field_first_core_ideal_operation_mechanism_only"},
    {"base_term": "field_first_core_role_function_redefinition_pass", "stage_term": "field_first_core_ideal_operation_mechanism_pass"},
)

FIELD_FIRST_IDEAL_OP_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_field_first_role_redef_go",
    "ideal_operation_mechanism_complete",
    "operation_node_registry_complete",
    "operation_node_model_mapping_complete",
    "model_requirement_matrix_complete",
    "model_document_review_template_complete",
    "model_room_alignment_update_complete",
    "next_research_targets_complete",
    "field_first_core_ideal_operation_mechanism_only",
    "file_size_governance_review_ok",
)
