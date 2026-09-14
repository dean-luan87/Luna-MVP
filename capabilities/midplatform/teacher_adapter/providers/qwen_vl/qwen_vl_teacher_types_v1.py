# -*- coding: utf-8 -*-
"""Qwen-VL Teacher Adapter — planning types v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

PHASE_REF = "Phase-P1-Midplatform-Single-Teacher-QwenVL-Integration-Planning-v1-001"
SYSTEM_ID = "LunaQwenVLTeacherAdapterPlanningV1"
PLANNING_ONLY = True
PROVIDER_ID = "qwen_vl"
PROVIDER_LABEL = "Qwen-VL Teacher v1"
TEACHER_ROLE = "perception_teacher"

POLICY_REF = "qwen_vl_teacher_governance_policy_v1"
PARENT_POLICY_REF = "luna_teacher_adapter_policy_v1"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_DRYRUN_GO",
    "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_DRYRUN_GO",
)

EVIDENCE_TYPES = (
    "scene_hypothesis_candidate",
    "visual_attention_candidate",
    "task_clue_candidate",
)

FORBIDDEN_OUTPUT_TYPES = (
    "fact_label",
    "confirmed_scene",
    "final_plan",
    "tool_execution",
    "teacher_result",
    "teacher_fact",
    "teacher_decision",
)

ALLOWED_INPUT_FIELDS = (
    "image_ref",
    "image_reference",
    "observation_candidate",
    "situation_candidate",
    "plan_candidate",
    "missing_information",
    "policy_context",
)

FORBIDDEN_INPUT_FIELDS = (
    "internal_state",
    "fact_database",
    "private_memory",
    "policy_hidden_rules",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_possible_text_region",
    "case_b_slam_mapping_rejected",
    "case_c_unknown_scene_hypothesis",
    "case_d_unsupported_brand_claim",
    "case_e_navigate_task_clue_only",
)

FINAL_GO = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_PLANNING_BLOCKED"
DRYRUN_GO = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_DRYRUN_GO"
DRYRUN_BLOCKED = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Single-Teacher-QwenVL-Integration-DryRun-v1-001"
DRYRUN_NEXT_PHASE = "Phase-P1-Midplatform-Single-Teacher-QwenVL-Real-Provider-Integration-v1-001"
REAL_PROVIDER_GO = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO"
REAL_PROVIDER_BLOCKED = "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_BLOCKED"
REAL_PROVIDER_NEXT_PHASE = "Phase-P1-Midplatform-Teacher-Performance-Evaluation-v1-001"

INTEGRATION_CASE_IDS = (
    "case_a_unknown_scene_real_evidence",
    "case_b_shopfront_teacher_noop",
    "case_c_slam_suggestion_rejected",
    "case_d_unsupported_claim_rejected",
)

DRYRUN_CASE_IDS = (
    "case_a_teacher_admission_noop",
    "case_b_unknown_scene_request_teacher",
    "case_c_teacher_challenge_plan",
    "case_d_teacher_wrong_scene_rejected",
    "case_e_unsupported_claim_rejected",
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "deterministic_mock_only": True,
    "no_real_api": True,
    "no_network": True,
    "no_tool_execution": True,
    "no_runner_invocation": True,
    "no_fact_write": True,
    "no_direct_training": True,
    "qwen_not_scene_owner": True,
    "qwen_not_plan_owner": True,
    "qwen_not_fact_source": True,
    "qwen_not_execution_controller": True,
    "evidence_only_output": True,
    "validation_required": True,
    "trace_required": True,
    "uncertainty_required": True,
    "perception_teacher_only": True,
    "future_multi_teacher_ready": True,
}


def candidate_meta(
    *,
    trace_refs: Optional[List[Dict[str, Any]]] = None,
    policy_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "teacher_provider": PROVIDER_ID,
        "teacher_role": TEACHER_ROLE,
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": trace_refs or [],
        "policy_refs": policy_refs or [POLICY_REF, PARENT_POLICY_REF],
    }
