# -*- coding: utf-8 -*-
"""Luna Region Intelligence Ownership — dryrun types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-DryRun-v1-001"
SYSTEM_ID = "LunaModelManagerRegionIntelligenceOwnershipDryrunV1"
DRYRUN_ONLY = True

POLICY_REF = "runtime/mixed_region/dryrun/region_intelligence_ownership_dryrun_policy_v1.json"
ADAPTER_REF = "runtime/mixed_region/dryrun/region_intelligence_ownership_dryrun_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MIXED_REGION_UNDERSTANDING_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_OCR_RECOGNITION_RUNTIME_INTEGRATION_PLANNING_GO",
)

DRYRUN_CASE_IDS = (
    "case_a_ownership_first_stacked_menus",
    "case_b_missing_information_occlusion",
    "case_c_channel_conflict_same_region",
    "case_d_selective_channel_not_all_models",
    "case_e_ownership_graph_structure",
    "case_f_runtime_unavailable_replan",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"

BOUNDARY_FLAGS = {
    "dryrun_only": True,
    "information_ownership_graph": True,
    "selective_channel_activation": True,
    "ownership_before_ocr": True,
    "missing_information_reasoning": True,
    "not_global_model_activation": True,
    "deterministic_fixture_only": True,
    "candidate_only": True,
    "no_fact_write": True,
}
