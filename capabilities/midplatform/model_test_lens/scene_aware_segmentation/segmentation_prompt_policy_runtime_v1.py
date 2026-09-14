# -*- coding: utf-8 -*-
"""Scene-aware segmentation prompt policy runtime v1 — test-only, no fact."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_storage_v1 import (
    repo_root,
    resolve_path,
)

SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/scene_aware_segmentation"

LEGACY_OUTDOOR_PROMPTS = frozenset({
    "road_sign",
    "left_building",
    "center_advertisement_screen",
    "front_vehicle",
    "crosswalk_or_road_region",
})

SUBWAY_KEYWORDS = (
    "subway",
    "station",
    "platform",
    "jiahuihu",
    "metro",
    "地铁站",
    "站台",
)
STREET_KEYWORDS = (
    "street",
    "urban",
    "road_scene",
    "街景",
)


def _load_json(rel: str) -> Dict[str, Any]:
    path = resolve_path(rel)
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _norm_box_prompt(
    prompt_id: str,
    prompt_target_label: str,
    normalized_box_approx: List[float],
    *,
    source_prompt_hint: Optional[str] = None,
    display_task_semantic: str = "观察候选",
    ocr_route_candidate: bool = False,
) -> Dict[str, Any]:
    return {
        "prompt_id": prompt_id,
        "prompt_target_label": prompt_target_label,
        "prompt_type_preferred": "box",
        "normalized_box_approx": normalized_box_approx,
        "source_prompt_hint": source_prompt_hint or f"{prompt_id}_prompt",
        "display_task_semantic": display_task_semantic,
        "semantic_label": "candidate_only",
        "prompt_is_not_fact": True,
        "ocr_route_candidate": ocr_route_candidate,
    }


def _prompts_from_schema(schema: Dict[str, Any], default_boxes: Dict[str, List[float]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for p in schema.get("prompts", []):
        pid = p.get("segmentation_prompt_id") or p.get("prompt_id")
        if not pid:
            continue
        box = default_boxes.get(pid)
        if not box:
            continue
        out.append(
            _norm_box_prompt(
                pid,
                p.get("prompt_target_label", pid),
                box,
                source_prompt_hint=p.get("source_prompt_hint"),
                display_task_semantic=p.get("display_task_semantic", "观察候选"),
                ocr_route_candidate=bool(p.get("ocr_route_candidate")),
            )
        )
    return out


OUTDOOR_DEFAULT_BOXES: Dict[str, List[float]] = {
    "road_sign_candidate": [0.62, 0.42, 0.88, 0.63],
    "crosswalk_or_road_region": [0.48, 0.75, 0.98, 0.98],
    "vehicle_candidate": [0.37, 0.70, 0.51, 0.79],
    "advertisement_panel": [0.31, 0.43, 0.55, 0.68],
    "building_structure": [0.03, 0.05, 0.34, 0.78],
}

SUBWAY_DEFAULT_BOXES: Dict[str, List[float]] = {
    "station_direction_sign": [0.22, 0.02, 0.78, 0.20],
    "station_name_board": [0.20, 0.05, 0.80, 0.24],
    "route_map_or_line_info": [0.25, 0.08, 0.75, 0.28],
    "platform_screen_door": [0.28, 0.32, 0.72, 0.62],
    "train_door_area": [0.32, 0.28, 0.68, 0.72],
    "advertisement_panel": [0.30, 0.38, 0.58, 0.62],
    "warning_line_or_platform_edge": [0.08, 0.72, 0.92, 0.96],
    "floor_walkable_area": [0.12, 0.68, 0.88, 0.98],
    "people_region": [0.58, 0.32, 0.95, 0.88],
    "large_static_structure": [0.0, 0.0, 0.22, 0.55],
}

GENERIC_DEFAULT_BOXES: Dict[str, List[float]] = {
    "generic_region_candidate_1": [0.05, 0.05, 0.45, 0.45],
    "generic_region_candidate_2": [0.50, 0.05, 0.95, 0.45],
    "generic_region_candidate_3": [0.05, 0.50, 0.45, 0.95],
    "generic_region_candidate_4": [0.50, 0.50, 0.95, 0.95],
    "generic_region_candidate_5": [0.30, 0.30, 0.70, 0.70],
}


def infer_scene_profile_candidate(
    *,
    image_path: Optional[Path] = None,
    file_name: str = "",
    envelope_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    envelope_metadata = envelope_metadata or {}
    hints: List[str] = []
    name = (file_name or (str(image_path) if image_path else "")).lower()
    scene = envelope_metadata.get("scene_type_candidate")

    if scene in ("subway_platform", "indoor_station", "outdoor_street", "unknown_scene"):
        scene_type = scene
        confidence = float(envelope_metadata.get("confidence", 0.85))
    elif any(k in name for k in SUBWAY_KEYWORDS):
        scene_type = "subway_platform"
        confidence = 0.82
        hints.append(f"filename:{name}")
    elif any(k in name for k in STREET_KEYWORDS):
        scene_type = "outdoor_street"
        confidence = 0.78
        hints.append(f"filename:{name}")
    else:
        scene_type = "unknown_scene"
        confidence = 0.55
        hints.append("heuristic:unknown_scene")

    return {
        "scene_profile_id": f"spc_{uuid4().hex[:12]}",
        "scene_type_candidate": scene_type,
        "confidence": confidence,
        "evidence_refs": hints or [f"asset:{name or 'unknown'}"],
        "candidate_only": True,
        "not_fact": True,
        "scene_profile_candidate_not_fact": True,
    }


def select_prompt_execution_plan(
    scene_profile: Dict[str, Any],
    *,
    max_prompts: int = 10,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    scene_type = scene_profile.get("scene_type_candidate", "unknown_scene")
    subway_schema = _load_json(f"{SCHEMA_REL}/scene_prompt_set_subway_platform_v1.json")
    street_schema = _load_json(f"{SCHEMA_REL}/scene_prompt_set_outdoor_street_v1.json")

    if scene_type in ("subway_platform", "indoor_station"):
        specs = _prompts_from_schema(subway_schema, SUBWAY_DEFAULT_BOXES)
        prompt_set_id = "scene_prompt_set_subway_platform_v1"
        forbidden = list(LEGACY_OUTDOOR_PROMPTS)
    elif scene_type == "outdoor_street":
        specs = _prompts_from_schema(street_schema, OUTDOOR_DEFAULT_BOXES)
        prompt_set_id = "scene_prompt_set_outdoor_street_v1"
        forbidden = []
    else:
        specs = [
            _norm_box_prompt(
                f"generic_region_candidate_{i}",
                f"generic_region_candidate_{i}",
                GENERIC_DEFAULT_BOXES[f"generic_region_candidate_{i}"],
                source_prompt_hint=f"generic_region_{i}_prompt",
                display_task_semantic="P1 静态区域候选",
            )
            for i in range(1, 6)
        ]
        prompt_set_id = "scene_prompt_set_generic_v1"
        forbidden = list(LEGACY_OUTDOOR_PROMPTS)

    policy = {
        "policy_id": f"spp_{uuid4().hex[:10]}",
        "scene_profile_id": scene_profile.get("scene_profile_id"),
        "scene_type_candidate": scene_type,
        "prompt_set_id": prompt_set_id,
        "prompt_ids": [s["prompt_id"] for s in specs[:max_prompts]],
        "forbidden_legacy_prompts": forbidden,
        "candidate_only": True,
        "not_fact": True,
        "prompt_is_not_fact": True,
    }
    return specs[:max_prompts], policy


def build_scene_aware_runner_context(
    *,
    image_path: Path,
    file_name: str = "",
    max_prompts: int = 10,
) -> Dict[str, Any]:
    scene_profile = infer_scene_profile_candidate(image_path=image_path, file_name=file_name)
    specs, policy = select_prompt_execution_plan(scene_profile, max_prompts=max_prompts)
    return {
        "scene_profile_candidate": scene_profile,
        "segmentation_prompt_policy": policy,
        "prompt_execution_plan": specs,
    }
