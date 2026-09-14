# -*- coding: utf-8 -*-
"""Lightweight Vision Runtime Registry — planning v1."""

from __future__ import annotations

from typing import Any, Dict, List

LIGHTWEIGHT_RUNTIMES: Dict[str, Dict[str, Any]] = {
    "document_surface_detector_v1": {
        "runtime_id": "document_surface_detector_v1",
        "capability": "detect_document_surface",
        "output_type": "document_surface_candidate",
        "scene_types": ["stacked_documents", "desk_documents"],
    },
    "layout_detector_v1": {
        "runtime_id": "layout_detector_v1",
        "capability": "detect_layout_blocks",
        "output_type": "layout_region_candidate",
        "scene_types": ["document_layout", "multi_block_page"],
    },
    "price_tag_detector_v1": {
        "runtime_id": "price_tag_detector_v1",
        "capability": "detect_price_tag",
        "output_type": "price_tag_candidate",
        "scene_types": ["retail_shelf"],
    },
    "screen_surface_detector_v1": {
        "runtime_id": "screen_surface_detector_v1",
        "capability": "detect_screen_surface",
        "output_type": "screen_surface_candidate",
        "scene_types": ["device_screen"],
    },
    "reflection_detector_v1": {
        "runtime_id": "reflection_detector_v1",
        "capability": "detect_reflection",
        "output_type": "reflection_candidate",
        "scene_types": ["glass_reflection"],
    },
    "overlap_occlusion_detector_v1": {
        "runtime_id": "overlap_occlusion_detector_v1",
        "capability": "detect_overlap_occlusion",
        "output_type": "occlusion_relation_candidate",
        "scene_types": ["stacked_documents", "retail_shelf", "glass_reflection"],
    },
}

SCENE_RUNTIME_SELECTION: Dict[str, List[str]] = {
    "stacked_documents": ["document_surface_detector_v1", "overlap_occlusion_detector_v1"],
    "retail_shelf": ["price_tag_detector_v1", "document_surface_detector_v1", "overlap_occlusion_detector_v1"],
    "device_screen": ["screen_surface_detector_v1"],
    "glass_reflection": ["document_surface_detector_v1", "reflection_detector_v1", "overlap_occlusion_detector_v1"],
    "document_layout": ["document_surface_detector_v1", "layout_detector_v1"],
    "attention_blocked": [],
    "runtime_unavailable": [],
}


def select_runtimes_for_scene(*, scene_type: str, attention_allowed: bool) -> List[str]:
    if not attention_allowed:
        return []
    return SCENE_RUNTIME_SELECTION.get(scene_type, [])
