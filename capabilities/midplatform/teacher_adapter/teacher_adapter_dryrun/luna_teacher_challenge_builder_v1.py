# -*- coding: utf-8
"""Build teacher challenge from dry-run chain + fixtures."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.teacher_adapter.luna_teacher_adapter_processor_v1 import (
    evaluate_teacher_admission,
    route_teacher_provider,
)
from capabilities.midplatform.teacher_adapter.luna_teacher_adapter_types_v1 import POLICY_REF


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_teacher_input_from_chain(decision_validation_result: Dict[str, Any]) -> Dict[str, Any]:
    """After L2.5 validation — teacher challenges existing plan (not before planning)."""
    situation = decision_validation_result.get("situation_understanding_candidate") or {}
    plan = decision_validation_result.get("agent_plan_candidate") or {}
    return {
        "situation_understanding_candidate": situation,
        "agent_plan_candidate_optional": plan,
        "available_capabilities": [
            {"capability_type": c, "availability": "available"}
            for c in ("ocr", "detection", "depth", "tracking", "slam", "vlm", "sam")
        ],
        "policy_context": {
            "constitution_refs": ["L0"],
            "hard_constraints": ["no_fact_write", "no_runner_invocation", "no_tool_execution"],
            "active_policy_refs": [POLICY_REF, "luna_teacher_adapter_dryrun_policy_v1"],
        },
        "task_type": "plan_challenge",
        "required_output_type": "teacher_evidence_candidate",
        "input_evidence": [],
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{
            "stage": "l25_to_teacher_challenge",
            "plan_id": plan.get("plan_id"),
            "validation_id": (decision_validation_result.get("decision_validation_candidate") or {}).get("validation_id"),
        }],
    }


def build_teacher_evidence_from_challenge(
    teacher_input: Dict[str, Any],
    challenge: Dict[str, Any],
    *,
    admission: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Materialize teacher_evidence_candidate from dry-run fixture (no network)."""
    role = challenge.get("teacher_role", "planning_teacher")
    provider = challenge.get("provider_id", "gpt_vision")
    tid = _uid("tec")
    suggestion_type = challenge.get("suggestion_type", "supporting_hint")

    evidence: Dict[str, Any] = {
        "teacher_id": tid,
        "evidence_id": tid,
        "teacher_role": role,
        "provider_id": provider,
        "task_type": teacher_input.get("task_type", "plan_challenge"),
        "suggestion_type": suggestion_type,
        "suggestion_text": challenge.get("suggestion_text", ""),
        "supporting_evidence": challenge.get("supporting_evidence", []),
        "tools_suggested": challenge.get("tools_suggested", []),
        "confidence_candidate": float(challenge.get("confidence", 0.65)),
        "conflict_candidates": [],
        "policy_risk_candidates": list(challenge.get("policy_risk_candidates") or []),
        "supports_plan": challenge.get("supports_plan", False),
        "alternative_plan_goal": challenge.get("alternative_plan_goal"),
        "alternative_strategy": challenge.get("alternative_strategy"),
        "teacher_suggests": challenge.get("teacher_suggests"),
        "proposed_scene_type": challenge.get("proposed_scene_type"),
        "scene_override_candidate": challenge.get("scene_override_candidate"),
        "asserts_as_fact": challenge.get("asserts_as_fact", False),
        "candidate_only": True,
        "not_fact": True,
        "does_not_override_l1_scene": True,
        "does_not_override_l2_selected_plan": True,
        "no_runner_invocation": True,
        "no_fact_write": True,
        "requires_policy_review": True,
        "trace_refs": [{"stage": "teacher_evidence_candidate", "ref": tid}],
        "policy_refs": [POLICY_REF],
    }

    if role == "perception_teacher":
        evidence["perception_output_optional"] = challenge.get("perception_output") or {
            "scene_hypothesis_candidates": challenge.get("scene_hypothesis_candidates", []),
            "visual_evidence_candidates": challenge.get("visual_evidence_candidates", []),
            "uncertainty": challenge.get("uncertainty", 0.4),
            "candidate_only": True,
            "not_fact": True,
        }
    if role == "planning_teacher" or suggestion_type == "alternative_plan":
        alt_goal = challenge.get("alternative_plan_goal", "read_text")
        evidence["planning_output_optional"] = challenge.get("planning_output") or {
            "alternative_plan_candidate": {
                "plan_goal_type": alt_goal,
                "strategy_type": challenge.get("alternative_strategy", "information_gathering"),
                "tools_suggested": challenge.get("tools_suggested", ["ocr"]),
                "suggested_summary": challenge.get("suggestion_text", ""),
                "does_not_override_selected_plan": True,
                "candidate_only": True,
                "not_fact": True,
            },
            "candidate_only": True,
            "not_fact": True,
        }
    if role == "learning_teacher":
        evidence["learning_output_optional"] = challenge.get("learning_output") or {
            "learning_summary": challenge.get("suggestion_text", "teacher learning case candidate"),
            "review_status": "pending_policy_review",
            "candidate_only": True,
            "not_fact": True,
        }

    if admission:
        evidence["admission_ref"] = admission.get("admission_status")
    return evidence


def build_teacher_challenge_from_fixture(
    teacher_input: Dict[str, Any],
    challenge_fixture: Dict[str, Any],
) -> Dict[str, Any]:
    """Synthesize teacher assistance result from deterministic fixture."""
    admission = evaluate_teacher_admission({
        **teacher_input,
        "task_type": challenge_fixture.get("task_type", teacher_input.get("task_type", "plan_challenge")),
        "required_output_type": challenge_fixture.get("required_output_type", "teacher_evidence_candidate"),
        "input_evidence": challenge_fixture.get("input_evidence", []),
    })

    if challenge_fixture.get("force_admission"):
        admission = {**admission, **challenge_fixture["force_admission"]}

    result: Dict[str, Any] = {
        "request_id": _uid("tar"),
        "admission_decision": admission,
        "teacher_evidence_candidate": None,
        "candidate_only": True,
        "not_fact": True,
        "dryrun_fixture": True,
        "no_network": True,
        "policy_refs": [POLICY_REF],
    }

    if admission.get("admission_status") == "rejected" and not challenge_fixture.get("force_evidence"):
        return result

    if challenge_fixture.get("use_provider_stub"):
        provider_payload = route_teacher_provider(
            challenge_fixture.get("provider_id", "gemini"),
            teacher_role=challenge_fixture.get("teacher_role", "planning_teacher"),
            task_type=teacher_input.get("task_type", "plan_challenge"),
            input_evidence=challenge_fixture.get("input_evidence", []),
            situation=teacher_input.get("situation_understanding_candidate") or {},
            agent_plan=teacher_input.get("agent_plan_candidate_optional"),
        )
        if challenge_fixture.get("teacher_suggests"):
            provider_payload["teacher_suggests"] = challenge_fixture["teacher_suggests"]
        evidence = build_teacher_evidence_from_challenge(teacher_input, {
            **challenge_fixture,
            "provider_id": provider_payload.get("provider_id"),
            "confidence": provider_payload.get("confidence"),
            "planning_output": provider_payload.get("planning_output"),
            "perception_output": provider_payload.get("perception_output"),
        }, admission=admission)
    else:
        evidence = build_teacher_evidence_from_challenge(teacher_input, challenge_fixture, admission=admission)

    result["teacher_evidence_candidate"] = evidence
    result["teacher_role"] = evidence.get("teacher_role")
    result["provider_route"] = evidence.get("provider_id")
    return result
