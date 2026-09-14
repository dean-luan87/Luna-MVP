# -*- coding: utf-8
"""Route B execution stub — VLM route candidate (no real VLM)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_test_lens.multi_model_interaction.dual_route_perception_execution_types_v1 import (
    ROUTE_B_ID,
)


def _trace(stage: str, ref: str) -> Dict[str, str]:
    return {"stage": stage, "ref": ref}


def _subway_attention() -> List[Dict[str, Any]]:
    return [
        {
            "region_hint": "top_direction_sign",
            "region_description_candidate": "上方导视/站名区域候选",
            "bbox_hint": {"x1": 0.22, "y1": 0.02, "x2": 0.78, "y2": 0.20},
            "attention_reason_candidate": "text_likely_region_candidate",
        },
        {
            "region_hint": "platform_screen_door",
            "region_description_candidate": "站台屏蔽门区域候选",
            "bbox_hint": {"x1": 0.28, "y1": 0.32, "x2": 0.72, "y2": 0.62},
            "attention_reason_candidate": "structure_observation_candidate",
        },
    ]


def _street_attention() -> List[Dict[str, Any]]:
    return [
        {
            "region_hint": "road_sign_area",
            "region_description_candidate": "路侧标识区域候选",
            "bbox_hint": {"x1": 0.62, "y1": 0.42, "x2": 0.88, "y2": 0.63},
            "attention_reason_candidate": "text_likely_region_candidate",
        },
        {
            "region_hint": "vehicle_area",
            "region_description_candidate": "动态目标区域候选",
            "bbox_hint": {"x1": 0.37, "y1": 0.70, "x2": 0.51, "y2": 0.79},
            "attention_reason_candidate": "dynamic_target_candidate",
        },
    ]


def _conflict_attention() -> List[Dict[str, Any]]:
    return [
        {
            "region_hint": "top_sign_area",
            "region_description_candidate": "上方导视文字区域候选",
            "bbox_hint": {"x1": 0.22, "y1": 0.02, "x2": 0.78, "y2": 0.20},
            "attention_reason_candidate": "ocr_task_semantic_candidate",
        },
    ]


def generate_vlm_route_candidate(
    *,
    image_ref: str,
    scene_profile_candidate: Optional[Dict[str, Any]] = None,
    fixture_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    fixture_config = fixture_config or {}
    scene_type = (
        fixture_config.get("scene_type_candidate")
        or (scene_profile_candidate or {}).get("scene_type_candidate")
        or "unknown_scene"
    )
    cid = f"vlmrc_{uuid4().hex[:10]}"

    if fixture_config.get("route_conflict"):
        attention = _conflict_attention()
        followups = ["ocr", "detection"]
        reasoning = "VLM 建议关注上方导视文字区域候选；需与 Route A 区域对照，不确认类别。"
        uncertainty = 0.62
    elif scene_type in ("subway_platform", "indoor_station"):
        attention = _subway_attention()
        followups = ["ocr", "detection"]
        reasoning = "地铁站场景候选；上方导视/站名区域值得 OCR route candidate。"
        uncertainty = 0.35
    elif scene_type == "outdoor_street":
        attention = _street_attention()
        followups = ["ocr", "detection", "depth"]
        reasoning = "街景场景候选；标识与车辆区域分别进入 OCR / Detection route candidate。"
        uncertainty = 0.41
    else:
        attention = []
        followups = ["detection", "human_review"]
        reasoning = "场景不确定；建议人工复核。"
        uncertainty = 0.72

    return {
        "candidate_id": cid,
        "source_image_ref": image_ref,
        "route_id": ROUTE_B_ID,
        "scene_profile_candidate": scene_type,
        "vlm_scene_candidate": scene_type,
        "vlm_attention_candidate": attention,
        "suggested_attention_regions": attention,
        "suggested_followup_models": followups,
        "reasoning_summary": reasoning,
        "uncertainty": uncertainty,
        "confidence_or_uncertainty": uncertainty,
        "candidate_only": True,
        "not_fact": True,
        "vlm_output_not_fact": True,
        "trace_chain": [
            _trace("input_image", image_ref),
            _trace("route_b_vlm_observation", cid),
            _trace("route_b_attention_route", cid),
        ],
    }


def run_route_b_stub(
    *,
    image_ref: str,
    scene_profile_candidate: Optional[Dict[str, Any]] = None,
    fixture_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    vlm = generate_vlm_route_candidate(
        image_ref=image_ref,
        scene_profile_candidate=scene_profile_candidate,
        fixture_config=fixture_config,
    )
    return {
        "route_id": ROUTE_B_ID,
        "execution_mode": "deterministic_stub",
        "no_vlm_real_model_call": True,
        "vlm_route_candidate": vlm,
        "candidate_only": True,
        "not_fact": True,
        "route_b_candidate_only": True,
    }
