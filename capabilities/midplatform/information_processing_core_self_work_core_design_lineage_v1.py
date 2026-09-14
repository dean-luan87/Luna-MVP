# -*- coding: utf-8 -*-
"""IPC Self-Work Core Design template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

IPC_SELF_WORK_DESIGN_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/information_processing_core_controlled_implementation_v1.py",
    "tools/evaluation/midplatform/run_information_processing_core_controlled_implementation_v1.py",
    "tools/evaluation/midplatform/verify_information_processing_core_controlled_implementation_v1.py",
)

IPC_SELF_WORK_DESIGN_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "information_processing_core_controlled_implementation", "stage_term": "information_processing_core_self_work_core_design"},
    {"base_term": "information_processing_core_controlled_implementation_only", "stage_term": "information_processing_core_self_work_core_design_only"},
    {"base_term": "information_processing_core_controlled_implementation_pass", "stage_term": "information_processing_core_self_work_core_design_pass"},
)

IPC_SELF_WORK_DESIGN_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_ipc_controlled_implementation_go",
    "ipc_self_work_scope_complete",
    "ipc_internal_processing_flow_complete",
    "ipc_conclusion_model_complete",
    "ipc_transparency_traceability_model_complete",
    "ipc_self_check_referee_model_complete",
    "ipc_workload_control_model_complete",
    "downstream_need_observation_model_complete",
    "upstream_minimum_assumption_register_complete",
    "self_work_first",
    "downstream_contract_not_defined_yet",
    "ipc_internal_processing_defined",
    "information_processing_core_self_work_core_design_only",
    "file_size_governance_review_ok",
)
