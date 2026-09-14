# -*- coding: utf-8 -*-
"""Luna Model Manager Multi-Model Collaboration — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-Planning-v1-001"
SYSTEM_ID = "LunaModelManagerMultiModelCollaborationPlanningV1"
PLANNING_ONLY = True

POLICY_REF = "collaboration/collaboration_policy_v1.json"
COLLABORATION_PLAN_SCHEMA_REF = "collaboration/schemas/collaboration_plan_schema.json"
EVIDENCE_FUSION_SCHEMA_REF = "collaboration/schemas/evidence_fusion_schema.json"
CONFLICT_SCHEMA_REF = "collaboration/schemas/conflict_schema.json"

COLLABORATION_MODES = (
    "pipeline",
    "parallel_evidence",
    "challenge",
)

COLLABORATION_NOT = (
    "competition",
    "voting",
    "auto_answer_fusion",
    "simultaneous_all_models",
)

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_PROVIDER_REGISTRY_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_DRYRUN_GO",
)

FROZEN_PREREQUISITES = (
    "Capability_Marketplace",
    "Provider_Registry",
    "Capability_First_Routing",
    "Provider_Selection_Candidate",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_pipeline_collaboration",
    "case_b_unknown_scene_parallel_evidence",
    "case_c_model_conflict_validation",
    "case_d_resource_collaboration_degradation",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-DryRun-v1-001"

DRYRUN_PHASE_REF = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-DryRun-v1-001"
DRYRUN_POLICY_REF = "collaboration/dryrun/multi_model_collaboration_dryrun_policy_v1.json"
DRYRUN_CASE_IDS = (
    "case_a_pipeline_collaboration_shopfront",
    "case_b_parallel_evidence_unknown_scene",
    "case_c_challenge_mode_teacher",
    "case_d_evidence_conflict_semantic",
    "case_e_resource_collaboration_degradation",
)
DRYRUN_FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_DRYRUN_GO"
DRYRUN_FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_DRYRUN_BLOCKED"
DRYRUN_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "collaboration_not_competition": True,
    "collaboration_not_voting": True,
    "no_auto_answer_fusion": True,
    "no_simultaneous_all_models": True,
    "evidence_fusion_not_fact": True,
    "challenge_does_not_override_plan": True,
    "degradation_explicit_not_silent": True,
    "candidate_only": True,
    "no_fact_write": True,
}
