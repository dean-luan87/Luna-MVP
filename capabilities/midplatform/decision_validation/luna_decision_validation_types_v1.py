# -*- coding: utf-8
"""Luna Decision Validation Layer — planning types v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

PHASE_REF = "Phase-P1-Midplatform-Luna-Decision-Validation-Layer-Planning-v1-001"
SYSTEM_ID = "LunaDecisionValidationLayerPlanningV1"
PLANNING_ONLY = True
LAYER_ID = "L2_5_Decision_Validation"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_TESTBOARD_UI_EXECUTION_GO",
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_CONCEPT_PLANNING_GO",
)

POLICY_REF = "decision_validation_policy_v1"

VALIDATION_STATUSES = (
    "validated_candidate",
    "needs_review",
    "blocked_candidate",
    "insufficient_information",
)

RISK_LEVELS = ("low", "medium", "high", "critical")

VALIDATION_SOURCE_TYPES = (
    "policy_validator",
    "case_library_validator",
    "rule_validator",
    "single_teacher_validator_future",
    "multi_teacher_validator_future",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_ocr_validated",
    "case_b_user_goal_needs_review",
    "case_c_street_crossing_validated",
    "case_d_unknown_blanket_blocked",
    "case_e_slam_for_text_blocked",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_PLANNING_BLOCKED"
SMOKE_GO = "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_PLANNING_SMOKE_GO"
SMOKE_BLOCKED = "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_PLANNING_SMOKE_BLOCKED"

RECOMMENDED_NEXT_PHASES = (
    "Phase-P1-Midplatform-Luna-Decision-Validation-Layer-DryRun-v1-001",
    "Phase-P1-Midplatform-Third-Party-Teacher-Adapter-DryRun-v1-001",
)
RECOMMENDED_NEXT_PHASE = RECOMMENDED_NEXT_PHASES[0]

BOUNDARY_FLAGS = {
    "planning_only": True,
    "candidate_only": True,
    "validation_not_fact": True,
    "no_plan_ownership": True,
    "no_plan_override": True,
    "no_tool_execution": True,
    "tool_os_boundary_preserved": True,
    "constitution_priority": True,
    "situation_alignment_required": True,
    "single_teacher_future_ready": True,
    "multi_teacher_future_ready": True,
    "deterministic_smoke_only": True,
    "no_real_network": True,
}


def candidate_meta(
    *,
    trace_refs: Optional[List[Dict[str, Any]]] = None,
    policy_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": trace_refs or [],
        "policy_refs": policy_refs or [POLICY_REF],
    }


@dataclass
class DecisionValidationInput:
    agent_plan_candidate: Dict[str, Any]
    situation_understanding_candidate: Dict[str, Any]
    policy_context: Dict[str, Any]
    case_library_candidates: List[Dict[str, Any]]
    user_goal_candidate_optional: Optional[Dict[str, Any]] = None
    candidate_only: bool = True
    not_fact: bool = True


@dataclass
class ValidationResultCandidate:
    plan_alignment_score_candidate: float
    risk_level_candidate: str
    missing_information_detected: List[str]
    policy_conflict_detected: List[str]
    contradiction_candidates: List[Dict[str, Any]]
    candidate_only: bool = True
    not_fact: bool = True


@dataclass
class ValidationReason:
    reason_code: str
    reason_text: str
    polarity: str
    candidate_only: bool = True
    not_fact: bool = True


@dataclass
class AlternativePlanCandidate:
    plan_goal_type: str
    strategy_type: str
    tools_suggested: List[str]
    does_not_override_selected_plan: bool = True
    candidate_only: bool = True
    not_fact: bool = True


@dataclass
class ToolOSReadinessCandidate:
    should_handoff_to_tool_os: bool
    required_checks: List[str]
    admission_required: bool
    candidate_only: bool = True
    not_fact: bool = True
