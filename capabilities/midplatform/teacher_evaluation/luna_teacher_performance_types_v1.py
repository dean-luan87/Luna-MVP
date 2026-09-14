# -*- coding: utf-8 -*-
"""Teacher Performance Evaluation — types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Teacher-Performance-Evaluation-v1-001"
SYSTEM_ID = "LunaTeacherPerformanceEvaluationV1"
POLICY_REF = "teacher_performance_evaluation_policy_v1"

PROVIDER_ID = "qwen_vl"
TEACHER_ROLE = "perception_teacher"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_REAL_PROVIDER_INTEGRATION_GO",
    "P1_MIDPLATFORM_SINGLE_TEACHER_QWENVL_INTEGRATION_DRYRUN_GO",
)

EVALUATION_CASE_IDS = (
    "case_a_high_value_unknown_scene",
    "case_b_low_value_shopfront_noop",
    "case_c_policy_rejection_slam",
    "case_d_unsupported_claim_hallucination",
)

RECOMMENDED_USAGE_LEVELS = ("low", "medium", "high")

SCENE_USAGE_HINTS = {
    "shopfront_sign": {"recommended_usage": "low", "reason": "OCR/specialized tool preferred"},
    "subway_platform": {"recommended_usage": "medium", "reason": "moderate_uncertainty"},
    "unknown_scene": {"recommended_usage": "high", "reason": "high_uncertainty"},
    "complex_environment": {"recommended_usage": "high", "reason": "visual_interpretation_needed"},
    "simple_object": {"recommended_usage": "low", "reason": "specialized_tool_sufficient"},
}

FINAL_GO = "P1_MIDPLATFORM_TEACHER_PERFORMANCE_EVALUATION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_TEACHER_PERFORMANCE_EVALUATION_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Multi-Teacher-Validation-Planning-v1-001"

BOUNDARY_FLAGS = {
    "evaluation_only": True,
    "does_not_affect_current_decision": True,
    "no_auto_policy_update": True,
    "no_auto_permission_escalation": True,
    "no_fact_write": True,
    "no_runner_invocation": True,
    "candidate_only": True,
}
