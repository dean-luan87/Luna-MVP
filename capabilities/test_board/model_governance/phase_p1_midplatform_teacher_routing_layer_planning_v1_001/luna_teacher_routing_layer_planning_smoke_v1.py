# -*- coding: utf-8 -*-
"""Teacher Routing Layer — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.teacher_routing.luna_teacher_routing_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)
from capabilities.midplatform.teacher_routing.teacher_routing_processor_v1 import (
    route_teacher_request,
)


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
        "missing_information_candidates": missing,
        "uncertainty": uncertainty or {
            "needs_user_goal": scene == "unknown_scene",
            "needs_manual_review": scene == "unknown_scene",
        },
        "candidate_only": True,
        "not_fact": True,
    }


def _missing(info_type: str) -> Dict[str, Any]:
    return {"info_type": info_type, "candidate_only": True, "not_fact": True}


def _ocr_plan() -> Dict[str, Any]:
    return {
        "plan_id": "plan_shopfront_ocr",
        "plan_goal_candidate": {"goal_type": "identify_place", "candidate_only": True, "not_fact": True},
        "tool_plan_candidates": [{"capability_type": "ocr", "candidate_only": True}],
        "selected_plan_candidate": True,
        "candidate_only": True,
        "not_fact": True,
    }


def _validation_validated() -> Dict[str, Any]:
    return {
        "validation_id": "dv_smoke",
        "validation_status_candidate": "validated_candidate",
        "candidate_only": True,
        "not_fact": True,
    }


def _caps() -> List[Dict[str, Any]]:
    return [
        {"capability_type": "ocr", "availability": "available"},
        {"capability_type": "detection", "availability": "available"},
        {"capability_type": "vlm", "availability": "available"},
    ]


def smoke_case_a_shopfront_ocr_not_qwen() -> Dict[str, Any]:
    """Case A: shopfront + text → OCR tool, not Qwen."""
    case_id = "case_a_shopfront_ocr_not_qwen"
    route = route_teacher_request(
        situation_understanding_candidate=_situation(
            "shopfront_sign",
            [_missing("text_content"), _missing("place_identity")],
        ),
        agent_plan_candidate=_ocr_plan(),
        decision_validation_candidate=_validation_validated(),
        available_capabilities=_caps(),
    )
    passed = (
        route.get("route_type") == "tool_os"
        and route.get("selected_tool") == "ocr"
        and route.get("should_request_teacher") is False
        and route.get("selected_teacher") is None
        and "ocr" in (route.get("routing_reason") or "").lower() or route.get("rule_matched") == "shopfront_text_use_ocr_not_teacher"
        and route.get("does_not_override_l2_plan") is True
    )
    return {"case_id": case_id, "passed": passed, "route": route}


def smoke_case_b_unknown_scene_qwen_vl() -> Dict[str, Any]:
    """Case B: unknown_scene → Qwen-VL perception teacher."""
    case_id = "case_b_unknown_scene_qwen_vl"
    route = route_teacher_request(
        situation_understanding_candidate=_situation(
            "unknown_scene",
            [_missing("scene_identity"), _missing("environment_type")],
            uncertainty={"needs_manual_review": True, "needs_user_goal": True},
        ),
        agent_plan_candidate=_ocr_plan(),
        decision_validation_candidate={"validation_status_candidate": "insufficient_information"},
        available_capabilities=_caps(),
    )
    passed = (
        route.get("route_type") == "teacher_single"
        and route.get("selected_teacher") == "qwen_vl"
        and route.get("should_request_teacher") is True
        and route.get("selected_teacher_role") == "perception_teacher"
        and route.get("rule_matched") == "unknown_scene_high_uncertainty_qwen"
    )
    return {"case_id": case_id, "passed": passed, "route": route}


def smoke_case_c_complex_multi_teacher_candidate() -> Dict[str, Any]:
    """Case C: complex mall dining goal → Qwen + Planning Teacher candidates."""
    case_id = "case_c_complex_multi_teacher_candidate"
    route = route_teacher_request(
        situation_understanding_candidate=_situation(
            "indoor_mall",
            [_missing("best_dining_option"), _missing("environment_layout")],
        ),
        agent_plan_candidate={
            "plan_id": "plan_find_dining",
            "plan_goal_candidate": {"goal_type": "find_best_option", "candidate_only": True, "not_fact": True},
            "tool_plan_candidates": [{"capability_type": "detection", "candidate_only": True}],
            "candidate_only": True,
            "not_fact": True,
        },
        user_goal_candidate={
            "goal_type": "find_best_option",
            "interpreted_goal": "帮我找到这个商场里面最适合吃饭的位置",
            "candidate_only": True,
        },
        complex_decision=True,
        available_capabilities=_caps(),
    )
    candidates = route.get("teacher_candidates") or []
    teacher_ids = [c.get("teacher_id") for c in candidates]
    passed = (
        route.get("route_type") == "teacher_multi_candidate"
        and route.get("should_request_teacher") is True
        and "qwen_vl" in teacher_ids
        and "gpt_vision" in teacher_ids
        and route.get("no_multi_teacher_voting") is True
        and route.get("sequential_consultation_only") is True
    )
    return {"case_id": case_id, "passed": passed, "route": route}


def smoke_case_d_precise_ocr_tool_route() -> Dict[str, Any]:
    """Case D: precise OCR need → OCR tool, Qwen excluded."""
    case_id = "case_d_precise_ocr_tool_route"
    route = route_teacher_request(
        situation_understanding_candidate=_situation(
            "shopfront_sign",
            [_missing("text_content")],
        ),
        agent_plan_candidate=_ocr_plan(),
        need_capability="precise_ocr",
        available_capabilities=_caps(),
    )
    passed = (
        route.get("route_type") == "tool_os"
        and route.get("selected_tool") == "ocr"
        and route.get("should_request_teacher") is False
        and "qwen_vl" in (route.get("exclude_teachers") or [])
        and "precise_ocr" in (route.get("routing_reason") or "") or route.get("rule_matched") == "precise_ocr_not_qwen"
    )
    return {"case_id": case_id, "passed": passed, "route": route}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_shopfront_ocr_not_qwen,
        smoke_case_b_unknown_scene_qwen_vl,
        smoke_case_c_complex_multi_teacher_candidate,
        smoke_case_d_precise_ocr_tool_route,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Teacher-Routing-Layer-Planning-v1-001",
        "planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "no_multi_teacher_voting": all(
            (c.get("route") or {}).get("no_multi_teacher_voting") is not False
            or (c.get("route") or {}).get("route_type") in ("tool_os", "noop", "teacher_single")
            for c in cases
        ),
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
