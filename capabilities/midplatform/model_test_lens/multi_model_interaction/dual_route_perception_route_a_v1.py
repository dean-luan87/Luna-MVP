# -*- coding: utf-8 -*-
"""Route A execution stub — Grounding/Detection → SAM refine candidate (no real models)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_test_lens.multi_model_interaction.dual_route_perception_execution_types_v1 import (
    ROUTE_A_ID,
)

REFINE_METHOD = "sam_refine_stub"
SOURCE_MODEL = "planning_stub_v1"

SUBWAY_FIXTURE: List[Dict[str, Any]] = [
    {
        "grounding_prompt": "station direction sign candidate",
        "detected_label_candidate": "direction_sign",
        "bbox": {"x1": 0.22, "y1": 0.02, "x2": 0.78, "y2": 0.20},
        "confidence": 0.81,
        "text_likelihood": 0.88,
    },
    {
        "grounding_prompt": "text region candidate",
        "detected_label_candidate": "text_region",
        "bbox": {"x1": 0.20, "y1": 0.05, "x2": 0.80, "y2": 0.24},
        "confidence": 0.76,
        "text_likelihood": 0.85,
    },
]

STREET_FIXTURE: List[Dict[str, Any]] = [
    {
        "grounding_prompt": "road sign candidate",
        "detected_label_candidate": "sign",
        "bbox": {"x1": 0.62, "y1": 0.42, "x2": 0.88, "y2": 0.63},
        "confidence": 0.79,
        "text_likelihood": 0.82,
    },
    {
        "grounding_prompt": "vehicle candidate",
        "detected_label_candidate": "vehicle_candidate",
        "bbox": {"x1": 0.37, "y1": 0.70, "x2": 0.51, "y2": 0.79},
        "confidence": 0.74,
        "text_likelihood": 0.12,
    },
    {
        "grounding_prompt": "advertisement panel candidate",
        "detected_label_candidate": "advertisement_panel",
        "bbox": {"x1": 0.31, "y1": 0.43, "x2": 0.55, "y2": 0.68},
        "confidence": 0.71,
        "text_likelihood": 0.55,
    },
]

CONFLICT_FIXTURE: List[Dict[str, Any]] = [
    {
        "grounding_prompt": "person candidate",
        "detected_label_candidate": "person_candidate",
        "bbox": {"x1": 0.58, "y1": 0.32, "x2": 0.95, "y2": 0.88},
        "confidence": 0.77,
        "text_likelihood": 0.05,
    },
]


def _trace(stage: str, ref: str) -> Dict[str, str]:
    return {"stage": stage, "ref": ref}


def _fixture_for_scene(
    scene_type: str,
    *,
    force_miss: bool = False,
    force_conflict: bool = False,
) -> List[Dict[str, Any]]:
    if force_miss:
        return []
    if force_conflict:
        return list(CONFLICT_FIXTURE)
    if scene_type in ("subway_platform", "indoor_station"):
        return list(SUBWAY_FIXTURE)
    if scene_type == "outdoor_street":
        return list(STREET_FIXTURE)
    return []


def generate_grounding_detection_candidates(
    *,
    image_ref: str,
    scene_profile_candidate: Optional[Dict[str, Any]] = None,
    fixture_config: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    fixture_config = fixture_config or {}
    scene_type = (
        fixture_config.get("scene_type_candidate")
        or (scene_profile_candidate or {}).get("scene_type_candidate")
        or "unknown_scene"
    )
    specs = _fixture_for_scene(
        scene_type,
        force_miss=bool(fixture_config.get("route_a_miss")),
        force_conflict=bool(fixture_config.get("route_conflict")),
    )
    out: List[Dict[str, Any]] = []
    for spec in specs:
        cid = f"gdc_{uuid4().hex[:10]}"
        out.append({
            "candidate_id": cid,
            "source_image_ref": image_ref,
            "route_id": ROUTE_A_ID,
            "grounding_prompt": spec["grounding_prompt"],
            "detected_label_candidate": spec["detected_label_candidate"],
            "bbox": dict(spec["bbox"]),
            "confidence": spec["confidence"],
            "text_likelihood": spec.get("text_likelihood", 0.0),
            "source_model": SOURCE_MODEL,
            "candidate_only": True,
            "not_fact": True,
            "detected_label_not_fact": True,
            "trace_chain": [
                _trace("input_image", image_ref),
                _trace("route_a_grounding_detection", cid),
            ],
        })
    return out


def generate_sam_refine_mask_candidates(
    grounding_candidates: List[Dict[str, Any]],
    *,
    image_ref: str,
) -> List[Dict[str, Any]]:
    masks: List[Dict[str, Any]] = []
    for g in grounding_candidates:
        bbox = g.get("bbox") or {}
        cid = f"srmc_{uuid4().hex[:10]}"
        masks.append({
            "candidate_id": cid,
            "source_grounding_candidate_id": g["candidate_id"],
            "source_bbox_candidate_id": g["candidate_id"],
            "source_image_ref": image_ref,
            "bbox_ref": g["candidate_id"],
            "mask_candidate_ref": f"mask_stub/{cid}.png",
            "sam_mask_ref": f"mask_stub/{cid}.png",
            "refine_method": REFINE_METHOD,
            "refine_source": SOURCE_MODEL,
            "pixel_box": [
                int(bbox.get("x1", 0) * 1000),
                int(bbox.get("y1", 0) * 1000),
                int(bbox.get("x2", 1) * 1000),
                int(bbox.get("y2", 1) * 1000),
            ],
            "confidence": g.get("confidence", 0.0),
            "candidate_only": True,
            "not_fact": True,
            "sam_mask_not_semantic_fact": True,
            "trace_chain": list(g.get("trace_chain", [])) + [
                _trace("route_a_sam_refine", cid),
            ],
        })
    return masks


def run_route_a_stub(
    *,
    image_ref: str,
    scene_profile_candidate: Optional[Dict[str, Any]] = None,
    fixture_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    grounding = generate_grounding_detection_candidates(
        image_ref=image_ref,
        scene_profile_candidate=scene_profile_candidate,
        fixture_config=fixture_config,
    )
    masks = generate_sam_refine_mask_candidates(grounding, image_ref=image_ref)
    return {
        "route_id": ROUTE_A_ID,
        "execution_mode": "deterministic_stub",
        "no_grounding_real_model_call": True,
        "grounding_detection_candidates": grounding,
        "sam_refine_mask_candidates": masks,
        "candidate_only": True,
        "not_fact": True,
        "route_a_candidate_only": True,
    }
