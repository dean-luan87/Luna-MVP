# -*- coding: utf-8 -*-
"""Luna Model Manager Real Multi-Model Chain — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerRealMultiModelChainIntegrationPlanningV1"
PLANNING_ONLY = True

POLICY_REF = "collaboration/real_chain/real_chain_validation_policy_v1.json"
EXECUTION_TRACE_SCHEMA_REF = "collaboration/real_chain/schemas/execution_trace_schema.json"
EVIDENCE_PACKAGE_SCHEMA_REF = "collaboration/real_chain/schemas/evidence_package_schema.json"
FUSION_CANDIDATE_SCHEMA_REF = "collaboration/real_chain/schemas/fusion_candidate_schema.json"

CHAIN_ID = "shopfront_text_detection_ocr_qwen_context_v1"
SLOT_IDS = ("slot_1", "slot_2", "slot_3")
SLOT_CAPABILITIES = (
    "text_detection",
    "text_recognition",
    "context_reasoning",
)
SLOT_PROVIDERS = (
    "detection_v1",
    "ocr_v1",
    "qwen_vl",
)

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_PROVIDER_REGISTRY_GO",
)

FROZEN_PREREQUISITES = (
    "Model_OS_Foundation_Frozen",
    "Collaboration_Slot_Abstraction",
    "Collaboration_DryRun_GO",
    "Capability_Marketplace",
)

SMOKE_CASE_IDS = (
    "case_a_normal_shopfront_chain",
    "case_b_ocr_failure_challenge",
    "case_c_qwen_unsupported_claim_reject",
    "case_d_detector_unavailable_degradation",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-DryRun-v1-001"

DRYRUN_PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-DryRun-v1-001"
DRYRUN_POLICY_REF = "collaboration/real_chain/dryrun/real_chain_dryrun_policy_v1.json"
DRYRUN_CASE_IDS = (
    "case_a_standard_shopfront_chain",
    "case_b_slot_provider_upgrade",
    "case_c_ocr_failure_chain",
    "case_d_context_challenge",
    "case_e_evidence_conflict",
    "case_f_full_execution_trace",
)
DRYRUN_FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_GO"
DRYRUN_FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REAL_MULTI_MODEL_CHAIN_INTEGRATION_DRYRUN_BLOCKED"
DRYRUN_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "single_real_chain_only": True,
    "text_capability_first": True,
    "sam_not_target_discovery": True,
    "no_ocr_vs_qwen_competition": True,
    "no_auto_answer_fusion": True,
    "no_auto_model_replacement": True,
    "qwen_not_ocr": True,
    "ocr_failure_returns_to_l2": True,
    "candidate_only": True,
    "no_fact_write": True,
}
