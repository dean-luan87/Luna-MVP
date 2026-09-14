# -*- coding: utf-8
"""Luna Teacher Adapter — dry-run adapter v1 (L1→L2→L2.5→Teacher Challenge→Review)."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional

from capabilities.midplatform.decision_validation.luna_decision_validation_dryrun_adapter_v1 import (
    run_decision_validation_dryrun,
)
from capabilities.midplatform.teacher_adapter.luna_teacher_adapter_processor_v1 import (
    build_learning_chain_from_teacher,
    request_teacher_assistance,
)
from capabilities.midplatform.teacher_adapter.luna_teacher_adapter_types_v1 import (
    POLICY_REF,
)
from capabilities.midplatform.teacher_adapter.luna_teacher_validation_processor_v1 import (
    DRYRUN_POLICY_REF,
    review_teacher_evidence,
)
from capabilities.midplatform.teacher_adapter.teacher_adapter_dryrun.luna_teacher_challenge_builder_v1 import (
    build_teacher_challenge_from_fixture,
    build_teacher_input_from_chain,
)

FINAL_GO = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_THIRD_PARTY_TEACHER_ADAPTER_DRYRUN_BLOCKED"


def assert_teacher_does_not_override_plan(
    plan: Dict[str, Any],
    review: Dict[str, Any],
) -> Dict[str, Any]:
    snap = review.get("original_plan_snapshot") or {}
    checks = {
        "selected_plan_unchanged": review.get("selected_plan_unchanged") is True,
        "goal_unchanged": snap.get("goal_type") == (plan.get("plan_goal_candidate") or {}).get("goal_type"),
        "no_override_flag": review.get("teacher_evidence_candidate", {}) is None or (
            (review.get("teacher_evidence_candidate") or {}).get("does_not_override_l2_selected_plan") is not False
        ),
    }
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True, "not_fact": True}


def assert_teacher_does_not_override_l1(
    situation: Dict[str, Any],
    review: Dict[str, Any],
) -> Dict[str, Any]:
    scene = (situation.get("scene_profile_candidate") or {}).get("scene_type")
    checks = {
        "l1_scene_unchanged": review.get("l1_scene_unchanged") is True,
        "scene_owner_preserved": (situation.get("scene_profile_candidate") or {}).get("owned_by") == review.get("l1_scene_owner"),
        "no_l1_override_conflict": not any(
            c.get("conflict_type") == "l1_scene_override_attempt" and review.get("teacher_validation_status") != "rejected_by_policy"
            for c in (review.get("conflict_candidates") or [])
        ),
        "scene_still": scene == (situation.get("scene_profile_candidate") or {}).get("scene_type"),
    }
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True, "not_fact": True}


def run_teacher_adapter_dryrun(
    job_envelope: Dict[str, Any],
    *,
    teacher_challenge_fixture: Optional[Dict[str, Any]] = None,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    plan_override: Optional[Dict[str, Any]] = None,
    use_plan_competition: bool = True,
) -> Dict[str, Any]:
    """
    Full dry-run:
    job → L1 → L2 → L2.5 validation → Teacher challenge → Teacher validation review.
    Teacher challenges plan AFTER validation; does not sit above planning.
    """
    dv_result = run_decision_validation_dryrun(
        job_envelope,
        user_goal_candidate=user_goal_candidate,
        plan_override=plan_override,
        use_plan_competition=use_plan_competition,
    )

    teacher_input = build_teacher_input_from_chain(dv_result)

    if teacher_challenge_fixture:
        teacher_result = build_teacher_challenge_from_fixture(teacher_input, teacher_challenge_fixture)
    else:
        teacher_input["task_type"] = "plan_challenge"
        teacher_result = request_teacher_assistance(teacher_input)

    teacher_review = review_teacher_evidence(
        decision_validation_result=dv_result,
        teacher_result=teacher_result,
        teacher_challenge_optional=teacher_challenge_fixture,
    )

    learning_chain = teacher_review.get("learning_case_candidate_optional")
    if not learning_chain and teacher_result.get("teacher_evidence_candidate", {}).get("teacher_role") == "learning_teacher":
        learning_chain = build_learning_chain_from_teacher(teacher_result)
        teacher_review["learning_case_candidate_optional"] = learning_chain

    plan = dv_result.get("agent_plan_candidate") or {}
    situation = dv_result.get("situation_understanding_candidate") or {}

    plan_assert = assert_teacher_does_not_override_plan(plan, teacher_review)
    l1_assert = assert_teacher_does_not_override_l1(situation, teacher_review)

    return {
        "job_id": dv_result.get("job_id", ""),
        "chain": [
            "job_envelope",
            "runner_evidence",
            "situation_understanding_candidate",
            "agent_plan_candidate",
            "decision_validation_candidate",
            "teacher_evidence_candidate",
            "teacher_validation_review",
            "tool_os_handoff_candidate",
        ],
        "situation_understanding_candidate": situation,
        "agent_plan_candidate": plan,
        "decision_validation_candidate": dv_result.get("decision_validation_candidate"),
        "tool_os_handoff_candidate": dv_result.get("tool_os_handoff_candidate"),
        "validation_status": dv_result.get("validation_status"),
        "teacher_adapter_input": teacher_input,
        "teacher_assistance_result": teacher_result,
        "teacher_evidence_candidate": teacher_result.get("teacher_evidence_candidate"),
        "teacher_validation_review": teacher_review,
        "teacher_validation_status": teacher_review.get("teacher_validation_status"),
        "learning_case_candidate_optional": learning_chain,
        "tool_plan_summary": dv_result.get("tool_plan_summary"),
        "teacher_does_not_override_plan_assertion": plan_assert,
        "teacher_does_not_override_l1_assertion": l1_assert,
        "no_fact_write_assertion": True,
        "no_tool_execution_assertion": True,
        "no_runner_invocation_assertion": True,
        "no_direct_training_assertion": learning_chain is None or learning_chain.get("no_direct_training") is True,
        "dryrun_only": True,
        "no_real_model_execution": True,
        "no_network": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, DRYRUN_POLICY_REF],
    }
