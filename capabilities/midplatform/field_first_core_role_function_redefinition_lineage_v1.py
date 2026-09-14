# -*- coding: utf-8 -*-
"""Field-First Core Role Function Redefinition template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_FIRST_ROLE_REDEF_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/field_first_core_recalibration_and_next_work_definition_v1.py",
    "tools/evaluation/midplatform/run_field_first_core_recalibration_and_next_work_definition_v1.py",
    "tools/evaluation/midplatform/verify_field_first_core_recalibration_and_next_work_definition_v1.py",
)

FIELD_FIRST_ROLE_REDEF_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "field_first_core_recalibration_and_next_work_definition", "stage_term": "field_first_core_role_function_redefinition"},
    {"base_term": "field_first_core_recalibration_only", "stage_term": "field_first_core_role_function_redefinition_only"},
    {"base_term": "field_first_core_recalibration_pass", "stage_term": "field_first_core_role_function_redefinition_pass"},
)

FIELD_FIRST_ROLE_REDEF_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_field_first_recal_go",
    "role_principles_defined",
    "core_roles_defined",
    "drive_roles_defined",
    "support_roles_defined",
    "role_main_chain_defined",
    "role_priority_defined",
    "role_separation_complete",
    "prior_work_repositioning_complete",
    "field_first_core_role_function_redefinition_only",
    "file_size_governance_review_ok",
)
