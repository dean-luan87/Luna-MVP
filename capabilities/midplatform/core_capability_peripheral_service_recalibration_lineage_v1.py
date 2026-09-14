# -*- coding: utf-8 -*-
"""Core Capability and Peripheral Service Recalibration template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

RECALIBRATION_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/module_integration_gap_consolidation_v1.py",
    "tools/evaluation/midplatform/run_module_integration_gap_consolidation_v1.py",
    "tools/evaluation/midplatform/verify_module_integration_gap_consolidation_v1.py",
)

RECALIBRATION_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "module_integration_gap_consolidation", "stage_term": "core_capability_peripheral_service_recalibration"},
    {"base_term": "module_integration_gap_consolidation_only", "stage_term": "core_capability_peripheral_service_recalibration_only"},
    {"base_term": "module_integration_gap_consolidation_pass", "stage_term": "core_capability_peripheral_service_recalibration_pass"},
    {"base_term": "module-integration-gap-consolidation-scope", "stage_term": "core-capability-peripheral-service-recalibration-scope"},
)

RECALIBRATION_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_module_integration_gap_consolidation_go",
    "midplatform_capability_framework_defined",
    "midplatform_core_function_defined",
    "core_module_selection_complete",
    "peripheral_service_principle_matrix_complete",
    "core_capability_marking_baseline_complete",
    "conflict_resolution_rule_complete",
    "route_reassessment_complete",
    "core_over_peripheral_conflict_rule_defined",
    "peripheral_services_marked_as_supporting_core",
    "prior_go_results_not_invalidated",
    "handoff_contract_not_auto_selected",
    "core_capability_peripheral_service_recalibration_only",
    "real_request_issuance_authorized",
    "file_size_governance_review_ok",
    "file_size_governance_review_exists",
)
