# -*- coding: utf-8 -*-
"""Luna Model Manager Multi-Provider Registry — types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Provider-Registry-v1-001"
SYSTEM_ID = "LunaModelManagerMultiProviderRegistryV1"

PROVIDER_REGISTRY_REF = "registry/provider_registry_v1.json"
CAPABILITY_REGISTRY_REF = "registries/capability_registry_v1.json"
MODEL_REGISTRY_REF = "registries/model_registry_v1.json"
PROVIDER_RELATIONS_REF = "registry/provider_relationships_v1.json"
MODEL_FAMILIES_REF = "registry/model_families_v1.json"
POLICY_REF = "registry/dryrun/multi_provider_registry_dryrun_policy_v1.json"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_DRYRUN_GO",
)

FROZEN_PREREQUISITES = (
    "External_API_Provider_Pattern",
    "Local_Runtime_Provider_Pattern",
    "Capability_First_Routing",
    "Model_Manager_Lifecycle",
)

SMOKE_CASE_IDS = (
    "case_a_same_capability_three_providers",
    "case_b_capability_mismatch_ocr_selected",
    "case_c_provider_version_replacement",
    "case_d_provider_conflict_not_auto_resolve",
    "case_e_provider_deprecation_routing_removal",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_PROVIDER_REGISTRY_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_PROVIDER_REGISTRY_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"

BOUNDARY_FLAGS = {
    "registry_only": True,
    "capability_first_routing": True,
    "provider_competition_not_voting": True,
    "no_multi_model_inference": True,
    "no_answer_fusion": True,
    "no_auto_training": True,
    "no_auto_weight_update": True,
    "provider_selection_candidate_only": True,
    "no_fact_write": True,
}
