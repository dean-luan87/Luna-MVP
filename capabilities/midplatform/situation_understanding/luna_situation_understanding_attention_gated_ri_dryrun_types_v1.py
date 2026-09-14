# -*- coding: utf-8 -*-
"""Luna Attention-Gated Region Intelligence — dryrun types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Situation-Understanding-Attention-Gated-Region-Intelligence-DryRun-v1-001"
SYSTEM_ID = "LunaSituationUnderstandingAttentionGatedRegionIntelligenceDryrunV1"
DRYRUN_ONLY = True
LAYER_ID = "L1_Attention_Gated_Region_Intelligence"
PARENT_LAYER = "L1_Situation_Understanding"

POLICY_REF = "situation_understanding/attention_gated_ri/dryrun/attention_gated_ri_dryrun_policy_v1.json"
ADAPTER_REF = "situation_understanding/attention_gated_ri/dryrun/attention_gated_ri_dryrun_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_ALLOCATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_GO",
)

DRYRUN_CASE_IDS = (
    "case_a_attention_gate_blocks_models",
    "case_b_goal_find_exit_budget",
    "case_c_goal_find_coffee_shop",
    "case_d_goal_assess_danger",
    "case_e_scene_graph_ownership_attention",
    "case_f_information_efficiency_score",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Integration-Planning-v1-001"

BOUNDARY_FLAGS = {
    "dryrun_only": True,
    "attention_gates_region_intelligence": True,
    "observation_priority_graph": True,
    "scene_graph_ownership_plus_attention": True,
    "information_efficiency_score": True,
    "goal_plus_situation_drives_attention": True,
    "not_attention_label_only": True,
    "deterministic_fixture_only": True,
    "candidate_only": True,
    "no_fact_write": True,
}
