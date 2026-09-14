# -*- coding: utf-8
"""Scene-aware segmentation prompt policy — execution smoke v1 (no model call)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.model_test_lens.scene_aware_segmentation.segmentation_prompt_policy_runtime_v1 import (
    LEGACY_OUTDOOR_PROMPTS,
    build_scene_aware_runner_context,
    infer_scene_profile_candidate,
    select_prompt_execution_plan,
)

FINAL_GO = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_SMOKE_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_SMOKE_BLOCKED"

SUBWAY_IMAGE = "ocr_real_image_subway_platform_jiahuihu_v1_001.png"
STREET_IMAGE = "mobile_sam_real_local_image_street_scene_v1.png"

FORBIDDEN_MAIN_LABELS = ("路牌", "前方车辆", "广告屏", "道路区域")


def _read_static(rel: str) -> str:
    root = Path(__file__).resolve().parents[1]
    p = root / "static_site" / rel
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def smoke_case_a_subway() -> Dict[str, Any]:
    ctx = build_scene_aware_runner_context(
        image_path=Path(SUBWAY_IMAGE),
        file_name=SUBWAY_IMAGE,
    )
    scene = ctx["scene_profile_candidate"]
    policy = ctx["segmentation_prompt_policy"]
    prompt_ids = {p["prompt_id"] for p in ctx["prompt_execution_plan"]}
    legacy_hit = prompt_ids.intersection(LEGACY_OUTDOOR_PROMPTS)
    ocr_prompts = {"station_direction_sign", "station_name_board", "route_map_or_line_info"}
    passed = (
        scene.get("scene_type_candidate") in ("subway_platform", "indoor_station")
        and policy.get("prompt_set_id") == "scene_prompt_set_subway_platform_v1"
        and not legacy_hit
        and bool(prompt_ids.intersection(ocr_prompts))
        and "people_region" in prompt_ids
    )
    return {
        "case_id": "case_a_subway_jiahuihu",
        "passed": passed,
        "scene_type": scene.get("scene_type_candidate"),
        "prompt_set_id": policy.get("prompt_set_id"),
        "legacy_prompts_used": sorted(legacy_hit),
        "no_fact_write": True,
        "no_ocr_execution": True,
    }


def smoke_case_b_outdoor_street() -> Dict[str, Any]:
    ctx = build_scene_aware_runner_context(
        image_path=Path(STREET_IMAGE),
        file_name=STREET_IMAGE,
    )
    policy = ctx["segmentation_prompt_policy"]
    hud = _read_static("hud_label_layout_policy_v1.js")
    display = _read_static("prompt_label_display_policy_v1.js")
    passed = (
        ctx["scene_profile_candidate"].get("scene_type_candidate") == "outdoor_street"
        and policy.get("prompt_set_id") == "scene_prompt_set_outdoor_street_v1"
        and "road_sign_candidate" in policy.get("prompt_ids", [])
        and "FORBIDDEN_MAIN_LABELS" in display
        and "taskSemanticShort" in hud
    )
    return {"case_id": "case_b_outdoor_street", "passed": passed, "no_fact_write": True}


def smoke_case_c_unknown_scene() -> Dict[str, Any]:
    ctx = build_scene_aware_runner_context(
        image_path=Path("unknown_scene_sample.png"),
        file_name="unknown_scene_sample.png",
    )
    policy = ctx["segmentation_prompt_policy"]
    prompt_ids = policy.get("prompt_ids", [])
    passed = (
        ctx["scene_profile_candidate"].get("scene_type_candidate") == "unknown_scene"
        and policy.get("prompt_set_id") == "scene_prompt_set_generic_v1"
        and not set(prompt_ids).intersection(LEGACY_OUTDOOR_PROMPTS)
        and all("generic_region_candidate" in pid for pid in prompt_ids)
    )
    return {"case_id": "case_c_unknown_scene", "passed": passed}


def smoke_case_d_prompt_label_audit() -> Dict[str, Any]:
    files = [
        "prompt_label_display_policy_v1.js",
        "hud_label_layout_policy_v1.js",
        "perception_hud_mobile_sam_adapter_v1.js",
        "hud_selected_object_detail_v1.js",
    ]
    blob = "\n".join(_read_static(f) for f in files)
    passed = (
        "prompt_is_not_fact" in blob
        and "source_prompt_hint" in blob
        and "isForbiddenMainLabel" in blob
        and all(label in blob for label in ("路牌", "前方车辆"))
    )
    for label in FORBIDDEN_MAIN_LABELS:
        if f'"{label}"' in blob and "FORBIDDEN" in blob:
            continue
    return {
        "case_id": "case_d_prompt_label_audit",
        "passed": passed,
        "prompt_is_not_fact": True,
    }


def smoke_people_not_road_sign_label() -> Dict[str, Any]:
    display = _read_static("prompt_label_display_policy_v1.js")
    policy_js = _read_static("segmentation_prompt_policy_v1.js")
    passed = (
        "people_region" in display
        and "station_direction_sign" in display
        and "LEGACY_OUTDOOR" in policy_js
    )
    return {"case_id": "people_region_not_road_sign", "passed": passed}


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        smoke_case_a_subway(),
        smoke_case_b_outdoor_street(),
        smoke_case_c_unknown_scene(),
        smoke_case_d_prompt_label_audit(),
        smoke_people_not_road_sign_label(),
    ]
    failed: List[str] = []
    for c in cases:
        if not c.get("passed"):
            failed.append(f"smoke.fail={c.get('case_id')}")

    scene = infer_scene_profile_candidate(file_name=SUBWAY_IMAGE)
    _, policy = select_prompt_execution_plan(scene)
    if set(policy.get("prompt_ids", [])).intersection(LEGACY_OUTDOOR_PROMPTS):
        failed.append("smoke.subway_uses_legacy_outdoor")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    return {
        "smoke_cases": cases,
        "smoke_case_count": len(cases),
        "smoke_passed": len(cases) - len([f for f in failed if f.startswith("smoke.fail")]),
        "failed_checks": failed,
        "final_decision": decision,
        "planning_only": False,
        "no_model_call": True,
        "no_ocr_execution": True,
    }
