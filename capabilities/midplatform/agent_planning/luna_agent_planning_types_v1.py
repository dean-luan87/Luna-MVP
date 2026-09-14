# -*- coding: utf-8
"""Luna Agent Planning Layer — concept planning types v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

PHASE_REF = "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-Concept-Planning-v1-001"
SYSTEM_ID = "LunaAgentPlanningLayerConceptPlanningV1"
PLANNING_ONLY = True
LAYER_ID = "L2_Agent_Planning"

UPSTREAM_GO = (
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_TESTBOARD_UI_EXECUTION_GO",
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_MODEL_PLANNING_GO",
)

POLICY_REF = "luna_agent_planning_policy_v1"

PLAN_GOAL_TYPES = (
    "read_text", "identify_place", "find_direction", "assess_walkable",
    "navigate", "find_object", "understand_environment", "monitor_change",
    "ask_user", "manual_review", "unknown",
)

STRATEGY_TYPES = (
    "information_gathering", "navigation_support", "risk_assessment",
    "object_search", "place_identification", "environment_understanding",
    "monitoring", "ask_user_first", "manual_review",
)

STEP_TYPES = (
    "observe", "request_tool", "evaluate_result", "ask_user",
    "wait", "fallback", "stop",
)

CAPABILITY_TYPES = (
    "ocr", "detection", "sam", "slam", "depth", "tracking",
    "vlm", "search", "map", "speech", "other",
)

EXECUTION_MODES = (
    "not_executed", "request_tool_os_admission", "manual_review_required",
)

FALLBACK_TYPES = (
    "ask_user", "use_vlm_advisor", "manual_review",
    "retry_with_different_tool", "lower_confidence_output", "stop",
)

STOP_CONDITION_TYPES = (
    "required_info_obtained", "confidence_sufficient", "user_goal_unclear",
    "risk_high", "tool_unavailable", "max_retry_reached", "manual_review_required",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_sign",
    "case_b_subway_platform",
    "case_c_street_crossing",
    "case_d_corridor",
    "case_e_unknown_scene",
    "case_f_tool_unavailable",
    "case_g_user_goal_override",
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_CONCEPT_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_CONCEPT_PLANNING_BLOCKED"
SMOKE_GO = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_CONCEPT_PLANNING_SMOKE_GO"
SMOKE_BLOCKED = "P1_MIDPLATFORM_LUNA_AGENT_PLANNING_LAYER_CONCEPT_PLANNING_SMOKE_BLOCKED"

RECOMMENDED_NEXT_PHASES = (
    "Phase-P1-Midplatform-Luna-Agent-Planning-Layer-DryRun-v1-001",
    "Phase-P1-Midplatform-Third-Party-Teacher-Model-Adapter-Planning-v1-001",
)
RECOMMENDED_NEXT_PHASE = RECOMMENDED_NEXT_PHASES[0]

BOUNDARY_FLAGS = {
    "planning_only": True,
    "candidate_only": True,
    "agent_plan_candidate_not_fact": True,
    "no_runner_invocation": True,
    "no_tool_execution": True,
    "no_tool_install": True,
    "tool_os_handoff_required": True,
    "runner_admission_required": True,
    "fact_admission_required_after_result": True,
    "situation_input_required": True,
    "missing_information_drives_plan": True,
    "no_blanket_tool_plan": True,
    "deterministic_smoke_only": True,
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
class AgentPlanningInput:
    situation_understanding_candidate: Dict[str, Any]
    user_goal_candidate: Dict[str, Any]
    available_capabilities: List[Dict[str, Any]]
    policy_context: Dict[str, Any]
    memory_context_candidates: List[Dict[str, Any]]
    learning_case_refs: List[Dict[str, Any]]
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class PlanGoalCandidate:
    interpreted_goal: str
    goal_type: str
    source: str
    confidence: float
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class PlanStrategy:
    strategy_type: str
    reason: str
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentPlanStep:
    step_id: str
    step_order: int
    step_type: str
    step_goal: str
    required_information: List[str]
    expected_output: str
    depends_on_step_ids: List[str]
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ToolPlanCandidate:
    tool_plan_id: str
    capability_type: str
    tool_purpose: str
    input_target_hint_refs: List[str]
    required_information_refs: List[str]
    execution_mode: str
    priority: str
    reason: str
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class NoopToolPlanCandidate:
    capability_type: str
    noop_reason: str
    policy_ref: str
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class FallbackStrategy:
    fallback_type: str
    trigger_condition: str
    reason: str
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AskUserStrategy:
    should_ask_user: bool
    question_candidate: str
    ask_reason: str
    trigger_condition: str
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class StopCondition:
    condition_type: str
    reason: str
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ToolOSHandoffCandidate:
    should_handoff: bool
    handoff_reason: str
    required_tool_os_checks: List[str]
    runner_admission_required: bool
    fact_admission_required_after_result: bool
    candidate_only: bool = True
    not_fact: bool = True
    trace_refs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentPlanningTrace:
    trace_id: str
    stage: str
    input_refs: List[str]
    output_refs: List[str]
    candidate_only: bool = True
    not_fact: bool = True


@dataclass
class AgentPlanCandidate:
    plan_id: str
    plan_goal_candidate: Dict[str, Any]
    plan_strategy: Dict[str, Any]
    plan_steps: List[Dict[str, Any]]
    tool_plan_candidates: List[Dict[str, Any]]
    noop_tool_plan_candidates: List[Dict[str, Any]]
    fallback_strategy: Dict[str, Any]
    ask_user_strategy: Dict[str, Any]
    stop_conditions: List[Dict[str, Any]]
    handoff_to_tool_os_candidate: Dict[str, Any]
    trace_refs: List[Dict[str, Any]]
    candidate_only: bool = True
    not_fact: bool = True
    policy_refs: List[str] = field(default_factory=lambda: [POLICY_REF])
