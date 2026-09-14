# -*- coding: utf-8 -*-
"""Information Processing Core Work Manual Definition template lineage."""

from __future__ import annotations

from typing import Dict, Tuple

IPC_WORK_MANUAL_WHITELIST_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/luna_project_organization_work_manual_and_existing_work_mapping_v1.py",
    "tools/evaluation/midplatform/run_luna_project_organization_work_manual_and_existing_work_mapping_v1.py",
    "tools/evaluation/midplatform/verify_luna_project_organization_work_manual_and_existing_work_mapping_v1.py",
)

IPC_WORK_MANUAL_STAGE_TERM_OVERRIDES: Tuple[Dict[str, str], ...] = (
    {"base_term": "luna_project_organization_work_manual_and_existing_work_mapping", "stage_term": "information_processing_core_work_manual_definition"},
    {"base_term": "luna_project_organization_work_manual_mapping_only", "stage_term": "information_processing_core_work_manual_definition_only"},
    {"base_term": "luna_project_organization_work_manual_mapping_pass", "stage_term": "information_processing_core_work_manual_definition_pass"},
)

IPC_WORK_MANUAL_STAGE_ADDITIONS: Tuple[str, ...] = (
    "prior_project_work_manual_go",
    "information_processing_core_work_manual_complete",
    "organization_context_complete",
    "core_work_definition_complete",
    "role_job_definition_complete",
    "internal_external_workflow_complete",
    "judge_referee_rules_complete",
    "workload_control_complete",
    "qualification_standard_complete",
    "future_expansion_complete",
    "implementation_readiness_ok",
    "information_processing_core_work_manual_definition_only",
    "file_size_governance_review_ok",
)
