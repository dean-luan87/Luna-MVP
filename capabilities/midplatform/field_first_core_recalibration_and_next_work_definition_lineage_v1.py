# -*- coding: utf-8 -*-
"""Field-First Core Recalibration template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

FIELD_FIRST_RECAL_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/information_processing_core_self_work_core_design_v1.py",
    "tools/evaluation/midplatform/run_information_processing_core_self_work_core_design_v1.py",
    "tools/evaluation/midplatform/verify_information_processing_core_self_work_core_design_v1.py",
)

FIELD_FIRST_RECAL_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "information_processing_core_self_work_core_design", "stage_term": "field_first_core_recalibration_and_next_work_definition"},
    {"base_term": "information_processing_core_self_work_core_design_only", "stage_term": "field_first_core_recalibration_only"},
    {"base_term": "information_processing_core_self_work_core_design_pass", "stage_term": "field_first_core_recalibration_pass"},
)

FIELD_FIRST_RECAL_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_ipc_self_work_design_go",
    "field_first_core_route_defined",
    "core_route_adjustment_complete",
    "field_first_core_concept_complete",
    "field_model_architecture_sketch_complete",
    "next_work_definition_complete",
    "ipc_repositioned_not_invalidated",
    "peripheral_not_prematurely_fixed",
    "field_first_core_recalibration_only",
    "file_size_governance_review_ok",
)
