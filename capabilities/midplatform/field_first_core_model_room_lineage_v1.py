# -*- coding: utf-8 -*-
"""Field-First Core Model Room template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_FIRST_MODEL_ROOM_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_role_function_redefinition_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_role_function_redefinition_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_role_function_redefinition_v1.py",
)

FIELD_FIRST_MODEL_ROOM_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_first_core_role_function_redefinition", "stage_term": "field_first_core_model_room_interface_logic_definition"},
    {"base_term": "field_first_core_role_function_redefinition_only", "stage_term": "field_first_core_model_room_interface_logic_definition_only"},
    {"base_term": "field_first_core_role_function_redefinition_pass", "stage_term": "field_first_core_model_room_interface_logic_definition_pass"},
)

FIELD_FIRST_MODEL_ROOM_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_field_first_role_redef_go",
    "model_room_definition_complete",
    "open_source_reference_inventory_complete",
    "model_adapter_interface_complete",
    "candidate_output_registry_complete",
    "field_model_model_interface_complete",
    "field_simulation_interface_complete",
    "midplatform_reasoning_interface_complete",
    "model_integration_deferred",
    "field_first_core_model_room_interface_logic_definition_only",
    "file_size_governance_review_ok",
)
