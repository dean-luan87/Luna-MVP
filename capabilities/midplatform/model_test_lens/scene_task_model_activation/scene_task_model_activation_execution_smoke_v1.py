# -*- coding: utf-8 -*-
"""Scene-Task Model Activation — execution smoke v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.model_test_lens.scene_task_model_activation.scene_task_model_activation_execution_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SHOP_SIGN_IMAGE_REF,
    SMOKE_CASE_IDS,
    STREET_IMAGE_REF,
    SUBWAY_IMAGE_REF,
)
from capabilities.midplatform.model_test_lens.scene_task_model_activation.scene_task_model_activation_executor_v1 import (
    build_model_activation_plan,
    build_scene_profile_candidate,
    build_task_intent_candidate,
)
from capabilities.midplatform.model_test_lens.scene_task_model_activation.scene_task_model_activation_types_v1 import (
    MODELS,
)

STATIC_REL = Path(__file__).resolve().parents[1] / "static_site"
ALL_MODELS: Tuple[str, ...] = MODELS


def _read_static(name: str) -> str:
    p = STATIC_REL / name
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def _active_names(plan: Dict[str, Any]) -> set[str]:
    return {a["model_name"] for a in plan.get("activated_model_set", [])}


def _noop_names(plan: Dict[str, Any]) -> set[str]:
    return {n["model_name"] for n in plan.get("model_noop_set", [])}


def _inactive_must_not_generate_task(plan: Dict[str, Any]) -> bool:
    active = _active_names(plan)
    for task in plan.get("followup_runner_task_candidates", []):
        if task.get("model_name") not in active:
            return False
    for noop in plan.get("model_noop_set", []):
        model = noop["model_name"]
        if any(t.get("model_name") == model for t in plan.get("followup_runner_task_candidates", [])):
            return False
    return True


def smoke_case_a_shopfront_sign() -> Dict[str, Any]:
    case_id = "case_a_shopfront_sign"
    plan = build_model_activation_plan(
        SHOP_SIGN_IMAGE_REF,
        build_scene_profile_candidate("shopfront_sign", 0.91),
        build_task_intent_candidate("read_text"),
        text_region_ids=["shop_sign_text_region_001"],
    )
    active = _active_names(plan)
    noop = _noop_names(plan)
    passed = (
        "ocr_text_detector" in active
        and "slam" in noop
        and "tracking" in noop
        and "depth" in noop
        and plan["recommended_followup_runner_task_candidate"] == "ocr_task_candidate"
        and _inactive_must_not_generate_task(plan)
    )
    return {"case_id": case_id, "passed": passed, "plan": plan, "no_slam_for_text_task": True}


def smoke_case_b_subway_direction_sign() -> Dict[str, Any]:
    case_id = "case_b_subway_direction_sign"
    scene = build_scene_profile_candidate("subway_platform", 0.89)
    plan = build_model_activation_plan(
        SUBWAY_IMAGE_REF,
        scene,
        build_task_intent_candidate("read_text"),
        text_region_ids=["subway_direction_sign_region_001"],
    )
    plan_nav = build_model_activation_plan(
        SUBWAY_IMAGE_REF,
        scene,
        build_task_intent_candidate("find_direction"),
        text_region_ids=["subway_direction_sign_region_001"],
        navigation_context=True,
        spatial_continuity_requested=True,
    )
    passed = (
        "ocr_text_detector" in _active_names(plan)
        and "slam" in _noop_names(plan)
        and "slam" in _active_names(plan_nav)
    )
    return {"case_id": case_id, "passed": passed, "plan": plan}


def smoke_case_c_street_crossing() -> Dict[str, Any]:
    case_id = "case_c_street_crossing"
    sign_rid = "street_sign_text_region_001"
    plan = build_model_activation_plan(
        STREET_IMAGE_REF,
        build_scene_profile_candidate("outdoor_street_crossing", 0.87),
        build_task_intent_candidate("assess_walkable_area"),
        text_region_ids=[sign_rid],
        object_candidates=True,
        dynamic_targets=True,
        region_ids=["crosswalk_candidate", "vehicle_lane_candidate"],
    )
    active = _active_names(plan)
    ocr_assign = [a for a in plan["model_region_assignment"] if a["model_name"] == "ocr_text_detector"]
    passed = (
        {"detection", "depth", "tracking", "ocr_text_detector"}.issubset(active)
        and ocr_assign
        and ocr_assign[0]["assigned_text_region_ids"] == [sign_rid]
    )
    return {"case_id": case_id, "passed": passed, "plan": plan}


def smoke_case_d_spatial_navigation() -> Dict[str, Any]:
    case_id = "case_d_spatial_navigation"
    plan = build_model_activation_plan(
        "corridor_fixture.png",
        build_scene_profile_candidate("corridor", 0.85),
        build_task_intent_candidate("assess_walkable_area"),
        region_ids=["corridor_walkable_candidate"],
    )
    active = _active_names(plan)
    noop = _noop_names(plan)
    passed = "depth" in active and "slam" in active and "ocr_text_detector" in noop
    return {"case_id": case_id, "passed": passed, "plan": plan}


def smoke_case_e_unknown_scene() -> Dict[str, Any]:
    case_id = "case_e_unknown_scene"
    plan = build_model_activation_plan(
        "unknown_fixture.png",
        build_scene_profile_candidate("unknown_scene", 0.42),
        build_task_intent_candidate("manual_review", source="default_policy", confidence=0.40),
    )
    passed = (
        "vlm_route_enhancer" in _active_names(plan)
        and plan["recommended_followup_runner_task_candidate"] == "vlm_route_candidate"
    )
    return {"case_id": case_id, "passed": passed, "plan": plan}


def smoke_ui_static_audit() -> Dict[str, Any]:
    panel = _read_static("scene_task_model_activation_panel_v1.js")
    copy = _read_static("scene_task_model_activation_copy_v1.js")
    state = _read_static("scene_task_model_activation_state_v1.js")
    app = _read_static("app.js")
    compact = _read_static("luna_observation_compact_ui_v1.js")
    passed = (
        "模型激活计划" in panel
        and "candidate_only" in panel
        and "not_fact" in panel
        and "Activated" in panel
        and "No-op" in panel
        and "buildPackage" in state
        and "model_activation_candidate_not_fact" in state
        and "activationPkg" in app
        and "lol-right-activation-host" in compact
        and "no_runner_execution" in copy
    )
    return {"case_id": "case_ui_static_audit", "passed": passed}


SMOKE_RUNNERS: Tuple[Any, ...] = (
    smoke_case_a_shopfront_sign,
    smoke_case_b_subway_direction_sign,
    smoke_case_c_street_crossing,
    smoke_case_d_spatial_navigation,
    smoke_case_e_unknown_scene,
    smoke_ui_static_audit,
)


def run_smoke_cases() -> Dict[str, Any]:
    cases = [fn() for fn in SMOKE_RUNNERS]
    failed: List[str] = []
    for c in cases:
        if not c.get("passed"):
            failed.append(f"smoke.fail={c.get('case_id')}")
    for expected in SMOKE_CASE_IDS:
        if expected not in {c["case_id"] for c in cases}:
            failed.append(f"smoke.missing_case={expected}")

    decision = FINAL_GO.replace("_GO", "_SMOKE_GO") if not failed else FINAL_BLOCKED.replace(
        "_BLOCKED", "_SMOKE_BLOCKED"
    )
    if not failed:
        decision = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_SMOKE_GO"
    else:
        decision = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_SMOKE_BLOCKED"

    return {
        "smoke_cases": cases,
        "smoke_case_count": len(cases),
        "smoke_passed": len(cases) - len([f for f in failed if f.startswith("smoke.fail")]),
        "failed_checks": failed,
        "final_decision": decision,
        "execution_only": True,
        "no_model_call": True,
        "no_runner_execution_in_activation_execution": True,
        "no_fact_write": True,
    }
