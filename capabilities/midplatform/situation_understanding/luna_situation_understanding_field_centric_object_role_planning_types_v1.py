# -*- coding: utf-8 -*-
"""Luna Field-Centric Object Role — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-Planning-v1-001"
SYSTEM_ID = "LunaSituationUnderstandingFieldCentricObjectRolePlanningV1"
PLANNING_ONLY = True
LAYER_ID = "L1_Field_Understanding"
PARENT_LAYER = "L1_Situation_Understanding"

POLICY_REF = "situation_understanding/field_centric/planning/field_centric_object_role_policy_v1.json"
PLAN_REF = "situation_understanding/field_centric/planning/field_centric_object_role_plan_v1.md"
ADAPTER_REF = "situation_understanding/field_centric/planning/field_centric_adapter_v1.py"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_LIGHTWEIGHT_VISION_RUNTIME_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO",
)

SMOKE_CASE_IDS = (
    "case_a_same_object_different_field_role",
    "case_b_same_behavior_different_field_risk",
    "case_c_unknown_interaction_infers_role",
    "case_d_unknown_no_interaction_unresolved",
    "case_e_attention_field_goal_not_saliency",
    "case_f_field_constrains_unknown_space",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_FIELD_CENTRIC_OBJECT_ROLE_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_FIELD_CENTRIC_OBJECT_ROLE_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"

CORE_PRINCIPLE = "不是识别世界，而是在场中理解世界"

BOUNDARY_FLAGS = {
    "planning_only": True,
    "field_centric": True,
    "field_not_scene_label": True,
    "field_before_object_role": True,
    "attention_from_field_and_goal": True,
    "interaction_infers_role": True,
    "unresolved_object_memory": True,
    "not_object_first": True,
    "candidate_only": True,
    "no_fact_write": True,
}
