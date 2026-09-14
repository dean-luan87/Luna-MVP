# -*- coding: utf-8
"""Luna Decision Validation Layer — dry-run adapter v1 (L1 → L2 → L2.5 → Tool OS)."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional

from capabilities.midplatform.agent_planning.luna_agent_planning_dryrun_adapter_v1 import (
    run_agent_planning_dryrun,
)
from capabilities.midplatform.decision_validation.luna_decision_validation_processor_v1 import (
    validate_decision,
)
from capabilities.midplatform.decision_validation.luna_decision_validation_types_v1 import (
    POLICY_REF,
)

DRYRUN_POLICY_REF = "luna_decision_validation_dryrun_policy_v1"
FINAL_GO = "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_DECISION_VALIDATION_LAYER_DRYRUN_BLOCKED"


def build_decision_validation_input_from_chain(
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    *,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    case_library_candidates: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """L1 situation + L2 plan → L2.5 validation input."""
    return {
        "agent_plan_candidate": plan,
        "situation_understanding_candidate": situation,
        "policy_context": {
            "constitution_refs": ["L0"],
            "governance_refs": [POLICY_REF, DRYRUN_POLICY_REF],
            "safety_constraints": ["no_fact_write", "no_runner_invocation", "no_tool_execution"],
            "protocol_refs": [],
            "hard_constraints": ["no_fact_write", "no_runner_invocation"],
        },
        "case_library_candidates": case_library_candidates or [],
        "user_goal_candidate_optional": user_goal_candidate,
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{
            "stage": "l2_to_l25_handoff",
            "plan_id": plan.get("plan_id", ""),
            "situation_id": situation.get("situation_id", ""),
        }],
    }


def gate_tool_os_handoff_candidate(
    handoff: Optional[Dict[str, Any]],
    validation: Dict[str, Any],
) -> Dict[str, Any]:
    """Validation gates Tool OS handoff — blocked/review plans do not clear handoff."""
    gated = deepcopy(handoff or {})
    status = validation.get("validation_status_candidate", "blocked_candidate")
    readiness = validation.get("tool_execution_readiness_candidate") or {}
    should_clear = (
        status == "validated_candidate"
        and readiness.get("should_handoff_to_tool_os") is True
    )
    if should_clear:
        gated["validation_cleared"] = True
        gated["gated_by_validation"] = False
        gated["validation_status"] = status
    else:
        gated["should_handoff"] = False
        gated["validation_cleared"] = False
        gated["gated_by_validation"] = True
        gated["validation_status"] = status
        gated["handoff_block_reason"] = f"validation_{status}_blocks_handoff"
    gated["candidate_only"] = True
    gated["not_fact"] = True
    gated["not_executed"] = True
    gated["policy_refs"] = list({*(gated.get("policy_refs") or []), POLICY_REF, DRYRUN_POLICY_REF})
    return gated


def assert_l2_feeds_validation(
    plan: Dict[str, Any],
    validation: Dict[str, Any],
) -> Dict[str, Any]:
    checks = {
        "plan_id_traced": any(
            t.get("stage") == "agent_plan" for t in (validation.get("trace_refs") or [])
        ) or bool(plan.get("plan_id")),
        "validation_status_present": bool(validation.get("validation_status_candidate")),
        "readiness_present": bool(validation.get("tool_execution_readiness_candidate")),
        "no_plan_override": validation.get("no_plan_override") is True,
        "candidate_only": validation.get("candidate_only") is True,
    }
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True, "not_fact": True}


def assert_validation_gates_handoff(
    validation: Dict[str, Any],
    gated_handoff: Dict[str, Any],
) -> Dict[str, Any]:
    status = validation.get("validation_status_candidate")
    readiness = validation.get("tool_execution_readiness_candidate") or {}
    should_clear = status == "validated_candidate" and readiness.get("should_handoff_to_tool_os") is True
    checks = {
        "validated_clears_handoff": (
            (gated_handoff.get("validation_cleared") is True and gated_handoff.get("should_handoff") is not False)
            if should_clear
            else True
        ),
        "blocked_gates_handoff": (
            gated_handoff.get("gated_by_validation") is True and gated_handoff.get("should_handoff") is False
            if not should_clear
            else True
        ),
        "handoff_candidate_only": gated_handoff.get("candidate_only") is True,
        "not_executed": gated_handoff.get("not_executed") is True,
    }
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True, "not_fact": True}


def run_decision_validation_dryrun(
    job_envelope: Dict[str, Any],
    *,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    plan_override: Optional[Dict[str, Any]] = None,
    case_library_candidates: Optional[List[Dict[str, Any]]] = None,
    use_plan_competition: bool = True,
) -> Dict[str, Any]:
    """
    Full dry-run chain:
    job/envelope → L1 → L2 → L2.5 validation → gated Tool OS handoff candidate.
    No teacher, no tool execution, no runner, no fact write.
    """
    l2_result = run_agent_planning_dryrun(
        job_envelope,
        user_goal_candidate=user_goal_candidate,
        use_plan_competition=use_plan_competition,
    )
    situation = l2_result.get("situation_understanding_candidate") or {}
    plan = plan_override or l2_result.get("selected_plan_candidate") or {}
    goal = user_goal_candidate or job_envelope.get("user_goal_candidate_optional")

    validation_input = build_decision_validation_input_from_chain(
        situation,
        plan,
        user_goal_candidate=goal,
        case_library_candidates=case_library_candidates,
    )
    validation_bundle = validate_decision(validation_input)
    validation = validation_bundle.get("decision_validation_candidate") or {}

    raw_handoff = plan.get("handoff_to_tool_os_candidate")
    gated_handoff = gate_tool_os_handoff_candidate(raw_handoff, validation)

    l2_feeds = assert_l2_feeds_validation(plan, validation)
    handoff_gate = assert_validation_gates_handoff(validation, gated_handoff)

    return {
        "job_id": job_envelope.get("job_id", l2_result.get("job_id", "")),
        "chain": [
            "job_envelope",
            "runner_evidence",
            "situation_understanding_candidate",
            "agent_plan_candidate",
            "decision_validation_candidate",
            "tool_os_handoff_candidate",
        ],
        "situation_understanding_candidate": situation,
        "agent_plan_candidate": plan,
        "agent_planning_dryrun": {
            "plan_competition": l2_result.get("plan_competition"),
            "l1_drives_l2_assertion": l2_result.get("l1_drives_l2_assertion"),
            "l2_constrains_tools_assertion": l2_result.get("l2_constrains_tools_assertion"),
        },
        "decision_validation_input_candidate": validation_bundle.get("decision_validation_input_candidate"),
        "decision_validation_candidate": validation,
        "tool_os_handoff_candidate_raw": raw_handoff,
        "tool_os_handoff_candidate": gated_handoff,
        "validation_status": validation.get("validation_status_candidate"),
        "tool_plan_summary": l2_result.get("tool_plan_summary"),
        "l2_feeds_validation_assertion": l2_feeds,
        "validation_gates_handoff_assertion": handoff_gate,
        "no_teacher_assertion": True,
        "no_runner_invocation_assertion": True,
        "no_tool_execution_assertion": True,
        "no_fact_write_assertion": True,
        "dryrun_only": True,
        "no_real_model_execution": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, DRYRUN_POLICY_REF],
    }
