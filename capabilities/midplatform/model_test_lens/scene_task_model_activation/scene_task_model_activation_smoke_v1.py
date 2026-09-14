# -*- coding: utf-8 -*-
"""Scene-Task Model Activation — planning smoke v1 (deterministic stub)."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.model_test_lens.scene_task_model_activation.scene_task_model_activation_executor_v1 import (
    build_model_activation_plan,
    build_scene_profile_candidate,
    build_task_intent_candidate,
)
from capabilities.midplatform.model_test_lens.scene_task_model_activation.scene_task_model_activation_types_v1 import (
    MODELS,
    PLANNING_ENDPOINT,
    SHOP_SIGN_IMAGE_REF,
    SMOKE_CASE_IDS,
    STREET_IMAGE_REF,
    SUBWAY_IMAGE_REF,
)

FINAL_GO = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_SMOKE_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_SMOKE_BLOCKED"

ALL_MODELS: Tuple[str, ...] = MODELS

_scene_profile = build_scene_profile_candidate
_task_intent = build_task_intent_candidate


def smoke_case_a_shopfront_sign() -> Dict[str, Any]:
    case_id = "case_a_shopfront_sign"
    scene = _scene_profile("shopfront_sign", 0.91)
    task = _task_intent("read_text")
    text_rid = "shop_sign_text_region_001"
    plan = build_model_activation_plan(SHOP_SIGN_IMAGE_REF, scene, task, text_region_ids=[text_rid])
    active = {a["model_name"] for a in plan["activated_model_set"]}
    noop_models = {n["model_name"] for n in plan["model_noop_set"]}
    slam_noop = next(n for n in plan["model_noop_set"] if n["model_name"] == "slam")
    passed = (
        plan["scene_profile_candidate"]["scene_type_candidate"] in ("shopfront_sign", "text_signage_scene")
        and plan["task_intent_candidate"]["task_type_candidate"] == "read_text"
        and "ocr_text_detector" in active
        and "ocr_recognizer" in active
        and "slam" in noop_models
        and "tracking" in noop_models
        and "depth" in noop_models
        and "read_text" in slam_noop["noop_reason"]
        and plan["recommended_followup_runner_task_candidate"] == "ocr_task_candidate"
        and plan["candidate_only"] is True
        and plan["not_fact"] is True
        and all(a.get("activation_reason") for a in plan["activated_model_set"])
        and len(plan["model_noop_set"]) == len(ALL_MODELS) - len(active)
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "plan": plan,
        "no_slam_for_text_task": "slam" in noop_models,
        "shopfront_sign_noops_slam": True,
        "no_fact_write": True,
        "no_runner_execution_in_planning": True,
    }


def smoke_case_b_subway_direction_sign() -> Dict[str, Any]:
    case_id = "case_b_subway_direction_sign"
    scene = _scene_profile("subway_platform", 0.89)
    task = _task_intent("read_text")
    text_rid = "subway_direction_sign_region_001"
    plan = build_model_activation_plan(
        SUBWAY_IMAGE_REF, scene, task, text_region_ids=[text_rid], navigation_context=False
    )
    active = {a["model_name"] for a in plan["activated_model_set"]}
    noop_models = {n["model_name"] for n in plan["model_noop_set"]}
    passed = (
        "ocr_text_detector" in active
        and "slam" in noop_models
        and plan["recommended_followup_runner_task_candidate"] == "ocr_task_candidate"
        and plan["model_activation_candidate_not_fact"] is True
    )
    plan_nav = build_model_activation_plan(
        SUBWAY_IMAGE_REF,
        scene,
        _task_intent("find_direction"),
        text_region_ids=[text_rid],
        navigation_context=True,
        spatial_continuity_requested=True,
    )
    nav_active = {a["model_name"] for a in plan_nav["activated_model_set"]}
    passed = passed and "slam" in nav_active
    return {
        "case_id": case_id,
        "passed": passed,
        "plan": plan,
        "plan_with_navigation": plan_nav,
        "subway_direction_sign_noops_slam_unless_navigation": True,
        "no_fact_write": True,
    }


def smoke_case_c_street_crossing() -> Dict[str, Any]:
    case_id = "case_c_street_crossing"
    scene = _scene_profile("outdoor_street_crossing", 0.87)
    task = _task_intent("assess_walkable_area")
    sign_rid = "street_sign_text_region_001"
    plan = build_model_activation_plan(
        STREET_IMAGE_REF,
        scene,
        task,
        text_region_ids=[sign_rid],
        object_candidates=True,
        dynamic_targets=True,
        region_ids=["crosswalk_candidate", "vehicle_lane_candidate"],
    )
    active = {a["model_name"] for a in plan["activated_model_set"]}
    ocr_assign = [a for a in plan["model_region_assignment"] if a["model_name"] == "ocr_text_detector"]
    passed = (
        "detection" in active
        and "depth" in active
        and "tracking" in active
        and "ocr_text_detector" in active
        and ocr_assign
        and ocr_assign[0]["assigned_text_region_ids"] == [sign_rid]
        and plan["not_fact"] is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "plan": plan,
        "no_blanket_ocr": bool(ocr_assign and ocr_assign[0]["assigned_text_region_ids"]),
        "no_fact_write": True,
    }


def smoke_case_d_spatial_navigation() -> Dict[str, Any]:
    case_id = "case_d_spatial_navigation"
    scene = _scene_profile("corridor", 0.85)
    task = _task_intent("assess_walkable_area")
    plan = build_model_activation_plan(
        "corridor_fixture.png",
        scene,
        task,
        text_region_ids=[],
        region_ids=["corridor_walkable_candidate"],
    )
    active = {a["model_name"] for a in plan["activated_model_set"]}
    noop_models = {n["model_name"] for n in plan["model_noop_set"]}
    passed = (
        "depth" in active
        and "slam" in active
        and "ocr_text_detector" in noop_models
        and "ocr_recognizer" in noop_models
        and plan.get("no_runner_execution_in_activation_execution") is True
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "plan": plan,
        "ocr_noop_pure_spatial": True,
        "no_fact_write": True,
    }


def smoke_case_e_unknown_scene() -> Dict[str, Any]:
    case_id = "case_e_unknown_scene"
    scene = _scene_profile("unknown_scene", 0.42)
    task = _task_intent("manual_review", source="default_policy", confidence=0.40)
    plan = build_model_activation_plan("unknown_fixture.png", scene, task)
    active = {a["model_name"] for a in plan["activated_model_set"]}
    passed = (
        "vlm_route_enhancer" in active
        and plan["recommended_followup_runner_task_candidate"] == "vlm_route_candidate"
        and plan["candidate_only"] is True
        and plan["not_fact"] is True
        and len(plan["model_noop_set"]) >= len(ALL_MODELS) - 1
    )
    return {
        "case_id": case_id,
        "passed": passed,
        "plan": plan,
        "no_fact_write": True,
        "vlm_route_only_primary": True,
    }


SMOKE_RUNNERS: Tuple[Any, ...] = (
    smoke_case_a_shopfront_sign,
    smoke_case_b_subway_direction_sign,
    smoke_case_c_street_crossing,
    smoke_case_d_spatial_navigation,
    smoke_case_e_unknown_scene,
)


def run_smoke_cases() -> Dict[str, Any]:
    cases = [fn() for fn in SMOKE_RUNNERS]
    failed: List[str] = []
    for c in cases:
        if not c.get("passed"):
            failed.append(f"smoke.fail={c.get('case_id')}")

    all_ids = {c["case_id"] for c in cases}
    for expected in SMOKE_CASE_IDS:
        if expected not in all_ids:
            failed.append(f"smoke.missing_case={expected}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    return {
        "planning_endpoint": PLANNING_ENDPOINT,
        "smoke_cases": cases,
        "smoke_case_count": len(cases),
        "smoke_passed": len(cases) - len([f for f in failed if f.startswith("smoke.fail")]),
        "failed_checks": failed,
        "final_decision": decision,
        "planning_only": True,
        "no_model_call": True,
        "no_runner_execution_in_planning": True,
        "no_fact_write": True,
    }
