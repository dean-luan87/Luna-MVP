# -*- coding: utf-8
"""Third-Party Teacher Adapter — planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.teacher_adapter.luna_teacher_adapter_processor_v1 import (
    build_learning_chain_from_teacher,
    request_teacher_assistance,
)
from capabilities.midplatform.teacher_adapter.luna_teacher_adapter_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)

FINAL_SMOKE_GO = FINAL_GO.replace("_GO", "_SMOKE_GO") if FINAL_GO.endswith("_GO") else FINAL_GO + "_SMOKE_GO"
FINAL_SMOKE_BLOCKED = FINAL_BLOCKED.replace("_BLOCKED", "_SMOKE_BLOCKED")


def _situation(
    scene: str,
    missing: List[Dict[str, Any]],
    *,
    uncertainty: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    return {
        "situation_id": f"sit_{scene}",
        "scene_profile_candidate": {
            "scene_type": scene,
            "confidence": 0.35 if scene == "unknown_scene" else 0.85,
            "owned_by": "situation_understanding_layer",
            "candidate_only": True,
            "not_fact": True,
        },
        "task_clue_candidates": [],
        "missing_information_candidates": missing,
        "model_need_hints": {"likely_needed": [], "optional": [], "not_needed": []},
        "uncertainty": uncertainty or {
            "needs_user_goal": scene == "unknown_scene",
            "needs_manual_review": scene == "unknown_scene",
            "fallback_suggestion": "ask_user / vlm_advisor" if scene == "unknown_scene" else "",
        },
        "candidate_only": True,
        "not_fact": True,
    }


def _missing(info_type: str, cap: str = "ocr") -> Dict[str, Any]:
    return {
        "info_type": info_type,
        "required_for": info_type,
        "suggested_capability": cap,
        "candidate_only": True,
        "not_fact": True,
    }


def _caps(*available: str) -> List[Dict[str, Any]]:
    all_caps = ("ocr", "detection", "depth", "tracking", "slam", "vlm", "sam")
    return [
        {
            "capability_id": f"cap_{c}",
            "capability_type": c,
            "availability": "available" if c in available else "unavailable",
        }
        for c in all_caps
    ]


def _input(
    situation: Dict[str, Any],
    *,
    task_type: str = "scene_hypothesis",
    required_output_type: str = "teacher_evidence_candidate",
    agent_plan: Dict[str, Any] | None = None,
    input_evidence: List[Dict[str, Any]] | None = None,
    capabilities: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    return {
        "situation_understanding_candidate": situation,
        "agent_plan_candidate_optional": agent_plan,
        "available_capabilities": capabilities if capabilities is not None else _caps("ocr", "vlm"),
        "policy_context": {
            "constitution_refs": ["L0"],
            "active_policy_refs": ["luna_teacher_adapter_policy_v1"],
            "hard_constraints": ["no_fact_write", "no_runner_invocation", "no_direct_training"],
        },
        "task_type": task_type,
        "required_output_type": required_output_type,
        "input_evidence": input_evidence or [],
        "candidate_only": True,
        "not_fact": True,
    }


def _agent_ocr_plan() -> Dict[str, Any]:
    return {
        "plan_id": "plan_agent_ocr",
        "plan_goal_candidate": {"goal_type": "identify_place", "candidate_only": True, "not_fact": True},
        "plan_strategy": {"strategy_type": "information_gathering"},
        "tool_plan_candidates": [{"capability_type": "ocr", "candidate_only": True}],
        "selected_plan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
    }


def smoke_case_a_shopfront_ocr_no_teacher() -> Dict[str, Any]:
    """Case A: shopfront + text_content + OCR available → Teacher noop."""
    case_id = "case_a_shopfront_ocr_no_teacher"
    sit = _situation("shopfront_sign", [_missing("text_content"), _missing("place_identity")])
    result = request_teacher_assistance(_input(sit, task_type="scene_hypothesis"))
    admission = result.get("admission_decision") or {}
    noop_reason = (admission.get("noop_reason") or "").lower()
    passed = (
        admission.get("admission_status") == "noop"
        and admission.get("should_request_teacher") is False
        and result.get("teacher_evidence_candidate") is None
        and ("ocr" in noop_reason or "specialized" in noop_reason)
        and result.get("no_runner_invocation") is True
        and result.get("no_fact_write") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_unknown_scene_teacher_candidate() -> Dict[str, Any]:
    """Case B: unknown_scene + high uncertainty → Teacher evidence candidate."""
    case_id = "case_b_unknown_scene_teacher_candidate"
    sit = _situation(
        "unknown_scene",
        [_missing("scene_identity", "vlm"), _missing("environment_type", "vlm")],
        uncertainty={"needs_manual_review": True, "needs_user_goal": True, "fallback_suggestion": "ask_user"},
    )
    result = request_teacher_assistance(_input(sit, capabilities=_caps("vlm", "ocr")))
    admission = result.get("admission_decision") or {}
    evidence = result.get("teacher_evidence_candidate") or {}
    perception = evidence.get("perception_output_optional") or {}
    hypotheses = perception.get("scene_hypothesis_candidates") or []
    passed = (
        admission.get("admission_status") == "admitted"
        and admission.get("teacher_role") == "perception_teacher"
        and evidence.get("output_type") == "scene_hypothesis_candidate"
        and len(hypotheses) >= 1
        and all(h.get("candidate_only") for h in hypotheses)
        and evidence.get("does_not_override_l1_scene") is True
        and evidence.get("not_fact") is True
        and result.get("no_network") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_planning_conflict_alternative_only() -> Dict[str, Any]:
    """Case C: Agent OCR plan vs Teacher Navigation alternative — Agent retains ownership."""
    case_id = "case_c_planning_conflict_alternative_only"
    sit = _situation("shopfront_sign", [_missing("text_content")])
    agent_plan = _agent_ocr_plan()
    result = request_teacher_assistance(_input(
        sit,
        task_type="alternative_plan",
        required_output_type="alternative_plan_candidate",
        agent_plan=agent_plan,
        capabilities=_caps("ocr", "detection", "depth"),
    ))
    evidence = result.get("teacher_evidence_candidate") or {}
    planning = evidence.get("planning_output_optional") or {}
    alt = planning.get("alternative_plan_candidate") or {}
    passed = (
        result.get("admission_decision", {}).get("admission_status") == "admitted"
        and evidence.get("teacher_role") == "planning_teacher"
        and alt.get("does_not_override_selected_plan") is True
        and alt.get("plan_goal_type") == "navigate"
        and agent_plan.get("plan_goal_candidate", {}).get("goal_type") == "identify_place"
        and evidence.get("does_not_override_l2_selected_plan") is True
        and evidence.get("not_fact") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_d_bad_teacher_policy_reject() -> Dict[str, Any]:
    """Case D: Teacher suggests SLAM for text → policy reject."""
    case_id = "case_d_bad_teacher_policy_reject"
    sit = _situation("shopfront_sign", [_missing("text_content")])
    result = request_teacher_assistance(_input(
        sit,
        task_type="alternative_plan",
        agent_plan=_agent_ocr_plan(),
        input_evidence=[{"teacher_suggests": "slam_for_text", "candidate_only": True}],
        capabilities=_caps("ocr", "slam"),
    ))
    admission = result.get("admission_decision") or {}
    passed = (
        admission.get("admission_status") == "rejected"
        and "slam_for_text" in (admission.get("reject_reason") or "")
        and result.get("teacher_evidence_candidate") is None
        and result.get("no_fact_write") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_e_learning_teacher_candidate_chain() -> Dict[str, Any]:
    """Case E: Learning Teacher → learning_candidate pending policy review."""
    case_id = "case_e_learning_teacher_candidate_chain"
    sit = _situation("unknown_scene", [_missing("scene_identity", "vlm")])
    result = request_teacher_assistance(_input(
        sit,
        task_type="learning_case",
        required_output_type="learning_candidate",
        capabilities=_caps("vlm"),
    ))
    evidence = result.get("teacher_evidence_candidate") or {}
    learning_chain = build_learning_chain_from_teacher(result)
    passed = (
        result.get("admission_decision", {}).get("teacher_role") == "learning_teacher"
        and evidence.get("output_type") == "learning_candidate"
        and learning_chain.get("review_status") == "pending_policy_review"
        and learning_chain.get("no_direct_training") is True
        and learning_chain.get("candidate_only") is True
        and evidence.get("requires_policy_review") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result, "learning_chain": learning_chain}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_shopfront_ocr_no_teacher,
        smoke_case_b_unknown_scene_teacher_candidate,
        smoke_case_c_planning_conflict_alternative_only,
        smoke_case_d_bad_teacher_policy_reject,
        smoke_case_e_learning_teacher_candidate_chain,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Third-Party-Teacher-Adapter-Planning-v1-001",
        "planning_only": True,
        "deterministic_smoke_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_SMOKE_GO if not failed else FINAL_SMOKE_BLOCKED,
    }
