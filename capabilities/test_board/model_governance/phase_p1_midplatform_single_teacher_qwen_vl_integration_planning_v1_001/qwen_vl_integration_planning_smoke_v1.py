# -*- coding: utf-8 -*-
"""Qwen-VL Single Teacher Integration — planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.teacher_adapter.luna_teacher_validation_processor_v1 import (
    review_teacher_evidence,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_adapter_v1 import (
    QwenVLTeacherAdapter,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    PROVIDER_ID,
    SMOKE_CASE_IDS,
    TEACHER_ROLE,
)

JOB_564F1AA93983 = "job_564f1aa93983"
IMAGE_REF = "asset_d19f5fe2972f/ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png"

_adapter = QwenVLTeacherAdapter()


def _policy_context() -> Dict[str, Any]:
    return {
        "constitution_refs": ["L0"],
        "active_policy_refs": ["qwen_vl_teacher_governance_policy_v1", "luna_teacher_adapter_policy_v1"],
        "hard_constraints": ["no_fact_write", "no_runner_invocation", "no_direct_training"],
    }


def _situation(
    scene: str,
    *,
    job_id: Optional[str] = None,
    missing: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    return {
        "situation_id": f"sit_{scene}",
        "job_id": job_id,
        "scene_profile_candidate": {
            "scene_type": scene,
            "confidence": 0.35 if scene == "unknown_scene" else 0.85,
            "owned_by": "situation_understanding_layer",
            "candidate_only": True,
            "not_fact": True,
        },
        "task_clue_candidates": [],
        "missing_information_candidates": missing or [],
        "uncertainty": {
            "needs_user_goal": scene == "unknown_scene",
            "needs_manual_review": scene == "unknown_scene",
        },
        "candidate_only": True,
        "not_fact": True,
    }


def _ocr_plan() -> Dict[str, Any]:
    return {
        "plan_id": "plan_shopfront_ocr",
        "plan_goal_candidate": {
            "goal_type": "identify_place",
            "interpreted_goal": "read_shop_sign",
            "candidate_only": True,
            "not_fact": True,
        },
        "tool_plan_candidates": [
            {"capability_type": "ocr", "execution_mode": "request_tool_os_admission", "candidate_only": True},
        ],
        "selected_plan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
    }


def _navigate_plan() -> Dict[str, Any]:
    return {
        "plan_id": "plan_navigate_entrance",
        "plan_goal_candidate": {
            "goal_type": "navigate",
            "interpreted_goal": "navigate_to_entrance",
            "candidate_only": True,
            "not_fact": True,
        },
        "tool_plan_candidates": [
            {"capability_type": "detection", "candidate_only": True},
            {"capability_type": "depth", "candidate_only": True},
        ],
        "selected_plan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
    }


def _validation_envelope(
    situation: Dict[str, Any],
    plan: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "situation_understanding_candidate": situation,
        "agent_plan_candidate": plan,
        "decision_validation_candidate": {
            "validation_id": "dv_smoke_qwen",
            "validation_status": "plan_admitted",
            "selected_plan_confirmed": True,
            "candidate_only": True,
            "not_fact": True,
        },
    }


def _run_case(
    *,
    mock_scenario: str,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    image_ref: Optional[str] = None,
) -> Dict[str, Any]:
    qwen_result = _adapter.request_teacher_assistance(
        teacher_role=TEACHER_ROLE,
        input_evidence=[],
        required_output_type="teacher_evidence_candidate",
        policy_context=_policy_context(),
        situation_candidate=situation,
        plan_candidate=plan,
        image_reference=image_ref,
        mock_scenario=mock_scenario,
    )
    validation = review_teacher_evidence(
        decision_validation_result=_validation_envelope(situation, plan),
        teacher_result={
            "teacher_evidence_candidate": qwen_result.get("teacher_evidence_candidate"),
            "admission_decision": {
                "admission_status": qwen_result.get("admission_status", "admitted"),
            },
        },
    )
    return {
        "qwen_result": qwen_result,
        "teacher_validation_review": validation,
    }


def smoke_case_a_shopfront_possible_text_region() -> Dict[str, Any]:
    """Case A: shopfront + OCR plan + Qwen possible_text_region → accepted_as_evidence."""
    case_id = "case_a_shopfront_possible_text_region"
    situation = _situation(
        "shopfront_sign",
        job_id=JOB_564F1AA93983,
        missing=[{"info_type": "text_content", "candidate_only": True}],
    )
    plan = _ocr_plan()
    out = _run_case(
        mock_scenario=case_id,
        situation=situation,
        plan=plan,
        image_ref=IMAGE_REF,
    )
    qwen = out["qwen_result"]
    review = out["teacher_validation_review"]
    evidence = qwen.get("teacher_evidence_candidate") or {}
    visual = evidence.get("visual_attention_candidate") or {}
    passed = (
        qwen.get("admission_status") == "admitted"
        and qwen.get("provider_id") == PROVIDER_ID
        and review.get("teacher_validation_status") == "accepted_as_evidence"
        and review.get("selected_plan_unchanged") is True
        and visual.get("attention_type") == "possible_text_region"
        and (plan.get("plan_goal_candidate") or {}).get("goal_type") == "identify_place"
        and qwen.get("no_network") is True
        and qwen.get("no_fact_write") is True
    )
    return {"case_id": case_id, "passed": passed, **out}


def smoke_case_b_slam_mapping_rejected() -> Dict[str, Any]:
    """Case B: Qwen suggests SLAM for text → rejected_by_policy."""
    case_id = "case_b_slam_mapping_rejected"
    situation = _situation("shopfront_sign", job_id=JOB_564F1AA93983)
    plan = _ocr_plan()
    out = _run_case(mock_scenario=case_id, situation=situation, plan=plan, image_ref=IMAGE_REF)
    review = out["teacher_validation_review"]
    passed = (
        review.get("teacher_validation_status") == "rejected_by_policy"
        and review.get("selected_plan_unchanged") is True
        and any(
            c.get("conflict_type") == "tool_mismatch"
            for c in (review.get("conflict_candidates") or [])
        )
        and review.get("no_fact_write") is True
    )
    return {"case_id": case_id, "passed": passed, **out}


def smoke_case_c_unknown_scene_hypothesis() -> Dict[str, Any]:
    """Case C: unknown_scene + Qwen hypothesis → accepted, L1 owner unchanged."""
    case_id = "case_c_unknown_scene_hypothesis"
    situation = _situation(
        "unknown_scene",
        missing=[
            {"info_type": "scene_identity", "candidate_only": True},
            {"info_type": "environment_type", "candidate_only": True},
        ],
    )
    plan = _ocr_plan()
    out = _run_case(mock_scenario=case_id, situation=situation, plan=plan)
    review = out["teacher_validation_review"]
    l1_scene = (situation.get("scene_profile_candidate") or {}).get("scene_type")
    evidence = (out["qwen_result"].get("teacher_evidence_candidate") or {})
    passed = (
        review.get("teacher_validation_status") == "accepted_as_evidence"
        and l1_scene == "unknown_scene"
        and evidence.get("does_not_override_l1_scene") is True
        and evidence.get("not_fact") is True
        and review.get("l1_scene_unchanged") is True
    )
    return {"case_id": case_id, "passed": passed, **out}


def smoke_case_d_unsupported_brand_claim() -> Dict[str, Any]:
    """Case D: Qwen 'This is Starbucks' without OCR → unsupported_claim reject."""
    case_id = "case_d_unsupported_brand_claim"
    situation = _situation("shopfront_sign", job_id=JOB_564F1AA93983)
    plan = _ocr_plan()
    out = _run_case(mock_scenario=case_id, situation=situation, plan=plan, image_ref=IMAGE_REF)
    review = out["teacher_validation_review"]
    passed = (
        review.get("teacher_validation_status") == "rejected_by_policy"
        and any(
            c.get("conflict_type") == "unsupported_claim"
            for c in (review.get("conflict_candidates") or [])
        )
        and review.get("no_fact_write") is True
        and review.get("selected_plan_unchanged") is True
    )
    return {"case_id": case_id, "passed": passed, **out}


def smoke_case_e_navigate_task_clue_only() -> Dict[str, Any]:
    """Case E: L2 navigate + Qwen OCR clue → alternative_evidence_only, plan unchanged."""
    case_id = "case_e_navigate_task_clue_only"
    situation = _situation("shopfront_sign", job_id=JOB_564F1AA93983)
    plan = _navigate_plan()
    out = _run_case(mock_scenario=case_id, situation=situation, plan=plan, image_ref=IMAGE_REF)
    review = out["teacher_validation_review"]
    evidence = (out["qwen_result"].get("teacher_evidence_candidate") or {})
    clue = evidence.get("task_clue_candidate") or {}
    passed = (
        review.get("teacher_validation_status") == "accepted_as_evidence"
        and review.get("selected_plan_unchanged") is True
        and (plan.get("plan_goal_candidate") or {}).get("goal_type") == "navigate"
        and clue.get("alternative_evidence_only") is True
        and evidence.get("does_not_override_l2_selected_plan") is True
    )
    return {"case_id": case_id, "passed": passed, **out}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_shopfront_possible_text_region,
        smoke_case_b_slam_mapping_rejected,
        smoke_case_c_unknown_scene_hypothesis,
        smoke_case_d_unsupported_brand_claim,
        smoke_case_e_navigate_task_clue_only,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    case_a = next((c for c in cases if c["case_id"] == "case_a_shopfront_possible_text_region"), {})
    a_review = (case_a.get("teacher_validation_review") or {})
    return {
        "phase_id": "Phase-P1-Midplatform-Single-Teacher-QwenVL-Integration-Planning-v1-001",
        "provider": PROVIDER_ID,
        "teacher_role": TEACHER_ROLE,
        "planning_only": True,
        "deterministic_mock_only": True,
        "no_real_api": True,
        "execution": False,
        "fact_write": False,
        "plan_override": False,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "job_564f1aa93983_qwen_result": {
            "job_id": JOB_564F1AA93983,
            "teacher_validation_status": a_review.get("teacher_validation_status"),
            "selected_plan_unchanged": a_review.get("selected_plan_unchanged"),
            "provider": PROVIDER_ID,
        },
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
