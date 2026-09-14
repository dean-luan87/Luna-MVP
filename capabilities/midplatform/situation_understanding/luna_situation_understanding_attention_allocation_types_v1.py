# -*- coding: utf-8 -*-
"""Luna Situation Understanding Attention Allocation — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Situation-Understanding-Attention-Allocation-Planning-v1-001"
SYSTEM_ID = "LunaSituationUnderstandingAttentionAllocationPlanningV1"
PLANNING_ONLY = True
LAYER_ID = "L1_Attention_Allocation"
PARENT_LAYER = "L1_Situation_Understanding"

POLICY_REF = "situation_understanding/attention_allocation/attention_allocation_policy_v1.json"
PLAN_REF = "situation_understanding/attention_allocation/observation_attention_plan_v1.json"
ADAPTER_REF = "situation_understanding/attention_allocation/attention_allocation_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MIXED_REGION_UNDERSTANDING_PLANNING_GO",
)

SMOKE_CASE_IDS = (
    "case_a_l0_scan_no_heavy_models",
    "case_b_subway_value_by_goal",
    "case_c_exit_goal_budget_allocation",
    "case_d_not_all_regions_deep",
    "case_e_same_text_different_value",
    "case_f_attention_gates_region_intelligence",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_ALLOCATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_ALLOCATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Situation-Understanding-Attention-Gated-Region-Intelligence-DryRun-v1-001"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "attention_before_region_intelligence": True,
    "l0_low_cost_scan": True,
    "value_assessment_by_goal": True,
    "observation_budget_manager": True,
    "selective_deep_understanding": True,
    "not_all_models_start": True,
    "active_perception": True,
    "candidate_only": True,
    "no_fact_write": True,
}
