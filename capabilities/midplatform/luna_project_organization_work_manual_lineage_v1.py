# -*- coding: utf-8 -*-
"""Luna Project Organization Work Manual template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

WORK_MANUAL_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/core_capability_peripheral_service_recalibration_v1.py",
    "tools/evaluation/midplatform/run_core_capability_peripheral_service_recalibration_v1.py",
    "tools/evaluation/midplatform/verify_core_capability_peripheral_service_recalibration_v1.py",
)

WORK_MANUAL_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "core_capability_peripheral_service_recalibration", "stage_term": "luna_project_organization_work_manual_and_existing_work_mapping"},
    {"base_term": "core_capability_peripheral_service_recalibration_only", "stage_term": "luna_project_organization_work_manual_mapping_only"},
    {"base_term": "core_capability_peripheral_service_recalibration_pass", "stage_term": "luna_project_organization_work_manual_mapping_pass"},
)

WORK_MANUAL_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_recalibration_go",
    "project_work_mode_defined",
    "standard_work_manual_template_complete",
    "midplatform_organization_manual_complete",
    "existing_work_mapping_complete",
    "missing_work_manual_gap_register_complete",
    "next_work_governance_rules_complete",
    "work_manual_first_rule_defined",
    "core_work_before_peripheral_rules",
    "peripheral_rules_must_serve_core",
    "prior_go_results_not_invalidated",
    "information_processing_core_should_have_work_manual_before_implementation",
    "next_route_not_direct_controlled_implementation_unless_manual_ready",
    "luna_project_organization_work_manual_mapping_only",
    "file_size_governance_review_ok",
)
