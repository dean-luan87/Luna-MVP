# -*- coding: utf-8
"""Luna Teacher Validation — review teacher evidence after L2.5 validation (dry-run)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.teacher_adapter.luna_teacher_adapter_types_v1 import (
    POLICY_REF,
    TEACHER_VALIDATION_STATUSES,
)

DRYRUN_POLICY_REF = "luna_teacher_adapter_dryrun_policy_v1"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _plan_goal(plan: Dict[str, Any]) -> str:
    return (plan.get("plan_goal_candidate") or {}).get("goal_type", "unknown")


def _scene(situation: Dict[str, Any]) -> str:
    return (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")


def _active_tools(plan: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in plan.get("tool_plan_candidates", [])]


def _detect_teacher_conflicts(
    evidence: Dict[str, Any],
    situation: Dict[str, Any],
    plan: Dict[str, Any],
) -> List[Dict[str, Any]]:
    conflicts: List[Dict[str, Any]] = []
    scene = _scene(situation)
    plan_goal = _plan_goal(plan)
    tools = evidence.get("tools_suggested") or []
    suggestion = (evidence.get("suggestion_text") or "").lower()
    perception = evidence.get("perception_output_optional") or {}

    if evidence.get("teacher_suggests") == "slam_for_text" or (
        "slam" in tools and scene == "shopfront_sign" and plan_goal in ("read_text", "identify_place")
    ):
        conflicts.append({
            "conflict_type": "tool_mismatch",
            "reason": "text task ≠ spatial mapping (SLAM for text)",
            "candidate_only": True,
            "not_fact": True,
        })

    if evidence.get("override_selected_plan"):
        conflicts.append({
            "conflict_type": "plan_override_attempt",
            "reason": "teacher must not override selected plan",
            "candidate_only": True,
            "not_fact": True,
        })

    wrong_scene = evidence.get("proposed_scene_type") or evidence.get("scene_override_candidate")
    if wrong_scene and wrong_scene != scene:
        conflicts.append({
            "conflict_type": "l1_scene_override_attempt",
            "reason": f"teacher scene {wrong_scene} ≠ L1 scene {scene}",
            "proposed": wrong_scene,
            "l1_scene": scene,
            "candidate_only": True,
            "not_fact": True,
        })

    hypotheses = (perception.get("scene_hypothesis_candidates") or [])
    for h in hypotheses:
        if h.get("scene_type") and h.get("scene_type") != scene and h.get("confidence", 0) > 0.7:
            if evidence.get("asserts_as_fact"):
                conflicts.append({
                    "conflict_type": "l1_scene_fact_assertion",
                    "reason": "teacher must not assert scene as fact",
                    "candidate_only": True,
                    "not_fact": True,
                })

    if "slam" in suggestion and ("文字" in suggestion or "ocr" in suggestion or "text" in suggestion):
        conflicts.append({
            "conflict_type": "tool_mismatch",
            "reason": "SLAM suggested for text reading",
            "candidate_only": True,
            "not_fact": True,
        })

    if evidence.get("unsupported_claim") or evidence.get("hallucination_risk"):
        if not evidence.get("supporting_ocr_evidence", False):
            conflicts.append({
                "conflict_type": "unsupported_claim",
                "reason": "unsupported brand/entity claim without OCR evidence",
                "candidate_only": True,
                "not_fact": True,
            })

    return conflicts


def review_teacher_evidence(
    *,
    decision_validation_result: Dict[str, Any],
    teacher_result: Dict[str, Any],
    teacher_challenge_optional: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Plan → Teacher Challenge → Validation Review.
    Teacher does not sit above Agent Planning; evidence is reviewed, not executed.
    """
    plan = decision_validation_result.get("agent_plan_candidate") or {}
    situation = decision_validation_result.get("situation_understanding_candidate") or {}
    validation = decision_validation_result.get("decision_validation_candidate") or {}
    evidence = teacher_result.get("teacher_evidence_candidate")
    admission = teacher_result.get("admission_decision") or {}

    review_id = _uid("tvr")
    plan_goal = _plan_goal(plan)
    plan_id = plan.get("plan_id", "unknown")
    original_plan_snapshot = {
        "plan_id": plan_id,
        "goal_type": plan_goal,
        "active_tools": _active_tools(plan),
        "candidate_only": True,
        "not_fact": True,
    }

    if not evidence and admission.get("admission_status") == "rejected":
        return {
            "review_id": review_id,
            "teacher_validation_status": "rejected_by_policy",
            "teacher_evidence_candidate": None,
            "reject_reason": admission.get("reject_reason", "admission_rejected"),
            "selected_plan_unchanged": True,
            "original_plan_snapshot": original_plan_snapshot,
            "l1_scene_unchanged": True,
            "no_tool_execution": True,
            "no_fact_write": True,
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [
                {"stage": "teacher_validation_review", "ref": review_id},
                {"stage": "admission_rejected", "reason": admission.get("reject_reason")},
            ],
            "policy_refs": [POLICY_REF, DRYRUN_POLICY_REF],
        }

    if not evidence:
        return {
            "review_id": review_id,
            "teacher_validation_status": "insufficient_information",
            "teacher_evidence_candidate": None,
            "selected_plan_unchanged": True,
            "original_plan_snapshot": original_plan_snapshot,
            "l1_scene_unchanged": True,
            "l1_scene_owner": (situation.get("scene_profile_candidate") or {}).get("owned_by"),
            "noop_reason": admission.get("noop_reason", "no_teacher_evidence"),
            "no_tool_execution": True,
            "no_runner_invocation": True,
            "no_fact_write": True,
            "candidate_only": True,
            "not_fact": True,
            "trace_refs": [{"stage": "teacher_validation_noop", "ref": review_id}],
            "policy_refs": [POLICY_REF, DRYRUN_POLICY_REF],
        }

    conflicts = _detect_teacher_conflicts(evidence, situation, plan)
    policy_risks = list(evidence.get("policy_risk_candidates") or [])
    for c in conflicts:
        policy_risks.append(c.get("reason", c.get("conflict_type", "conflict")))

    suggestion_type = evidence.get("suggestion_type", "unknown")
    supports_plan = evidence.get("supports_plan") is True or suggestion_type == "supporting_hint"
    alt_goal = evidence.get("alternative_plan_goal") or (
        (evidence.get("planning_output_optional") or {}).get("alternative_plan_candidate") or {}
    ).get("plan_goal_type")

    status = "insufficient_information"
    alternative_attached: Optional[Dict[str, Any]] = None
    reject_reason = ""

    if conflicts:
        status = "rejected_by_policy"
        reject_reason = conflicts[0].get("reason", "policy_conflict")
    elif supports_plan and plan_goal in ("read_text", "identify_place", "find_direction"):
        status = "accepted_as_evidence"
    elif suggestion_type == "alternative_plan" or (
        alt_goal and alt_goal != plan_goal
    ):
        alt = evidence.get("planning_output_optional", {}).get("alternative_plan_candidate") or {
            "plan_goal_type": alt_goal or evidence.get("alternative_plan_goal"),
            "strategy_type": evidence.get("alternative_strategy", "navigation_support"),
            "tools_suggested": evidence.get("tools_suggested", []),
            "suggested_summary": evidence.get("suggestion_text", ""),
            "does_not_override_selected_plan": True,
            "candidate_only": True,
            "not_fact": True,
        }
        alternative_attached = alt
        status = "accepted_as_alternative"
    elif evidence.get("teacher_role") == "learning_teacher":
        status = "requires_human_review"
    elif float(evidence.get("confidence_candidate") or evidence.get("confidence") or 0) < 0.4:
        status = "insufficient_information"
    else:
        status = "accepted_as_evidence"

    if teacher_challenge_optional and teacher_challenge_optional.get("force_status"):
        status = teacher_challenge_optional["force_status"]

    learning_chain = None
    if evidence.get("teacher_role") == "learning_teacher" or suggestion_type == "learning_case":
        learning_chain = {
            "learning_candidate_id": _uid("slc"),
            "source_type": "teacher_model",
            "source_ref": evidence.get("teacher_id") or evidence.get("evidence_id"),
            "review_status": "pending_policy_review",
            "no_direct_training": True,
            "candidate_only": True,
            "not_fact": True,
        }

    return {
        "review_id": review_id,
        "teacher_validation_status": status,
        "teacher_evidence_candidate": evidence,
        "conflict_candidates": conflicts,
        "policy_risk_candidates": policy_risks,
        "alternative_plan_candidate_optional": alternative_attached,
        "learning_case_candidate_optional": learning_chain,
        "selected_plan_unchanged": True,
        "keep_original_plan": status == "accepted_as_alternative",
        "original_plan_snapshot": original_plan_snapshot,
        "l1_scene_unchanged": _scene(situation) == _scene(situation),
        "l1_scene_owner": (situation.get("scene_profile_candidate") or {}).get("owned_by"),
        "reject_reason": reject_reason,
        "decision_validation_status_unchanged_by_teacher": True,
        "no_tool_execution": True,
        "no_runner_invocation": True,
        "no_fact_write": True,
        "no_direct_training": True,
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [
            {"stage": "agent_plan", "ref": plan_id},
            {"stage": "decision_validation", "ref": validation.get("validation_id")},
            {"stage": "teacher_evidence", "ref": evidence.get("teacher_id") or evidence.get("evidence_id")},
            {"stage": "teacher_validation_review", "ref": review_id, "status": status},
        ],
        "policy_refs": [POLICY_REF, DRYRUN_POLICY_REF],
    }
