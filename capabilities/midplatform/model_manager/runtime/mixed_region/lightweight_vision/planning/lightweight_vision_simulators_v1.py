# -*- coding: utf-8 -*-
"""Lightweight Vision Runtime Simulators — planning deterministic outputs v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.lightweight_vision.planning.lightweight_vision_runtime_registry_v1 import (
    LIGHTWEIGHT_RUNTIMES,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _runtime_meta(runtime_id: str) -> Dict[str, Any]:
    return LIGHTWEIGHT_RUNTIMES.get(runtime_id, {})


def simulate_document_surface(*, scene_type: str) -> Dict[str, Any]:
    entities = {
        "stacked_documents": [
            {"entity_id": "paper_A", "entity_type_candidate": "document_surface"},
            {"entity_id": "paper_B", "entity_type_candidate": "document_surface"},
        ],
        "retail_shelf": [
            {"entity_id": "product_a", "entity_type_candidate": "product_package"},
        ],
        "glass_reflection": [
            {"entity_id": "sign_real", "entity_type_candidate": "business_sign"},
        ],
        "document_layout": [
            {"entity_id": "doc_page_1", "entity_type_candidate": "document_surface"},
        ],
    }.get(scene_type, [])

    return {
        "runtime_id": "document_surface_detector_v1",
        "candidates": [
            {**e, "source_runtime": "document_surface_detector_v1", "candidate_only": True, "not_fact": True}
            for e in entities
        ],
    }


def simulate_layout_blocks() -> Dict[str, Any]:
    blocks = [
        {"block_id": "block_title", "block_type": "title"},
        {"block_id": "block_body", "block_type": "body"},
        {"block_id": "block_image", "block_type": "image"},
        {"block_id": "block_table", "block_type": "table"},
    ]
    return {
        "runtime_id": "layout_detector_v1",
        "candidates": [
            {
                "layout_region_id": b["block_id"],
                "layout_type_candidate": b["block_type"],
                "output_type": "layout_region_candidate",
                "source_runtime": "layout_detector_v1",
                "not_flat_text_merge": True,
                "candidate_only": True,
            }
            for b in blocks
        ],
    }


def simulate_price_tags() -> Dict[str, Any]:
    return {
        "runtime_id": "price_tag_detector_v1",
        "candidates": [
            {
                "entity_id": "price_tag",
                "entity_type_candidate": "price_tag",
                "source_runtime": "price_tag_detector_v1",
                "not_bound_to_product_package": True,
                "candidate_only": True,
                "not_fact": True,
            }
        ],
    }


def simulate_screen_surface() -> Dict[str, Any]:
    return {
        "runtime_id": "screen_surface_detector_v1",
        "candidates": [
            {
                "entity_id": "phone_device",
                "entity_type_candidate": "device_surface",
                "source_runtime": "screen_surface_detector_v1",
                "candidate_only": True,
            },
            {
                "entity_id": "phone_screen",
                "entity_type_candidate": "screen_content",
                "source_runtime": "screen_surface_detector_v1",
                "candidate_only": True,
            },
        ],
    }


def simulate_reflection() -> Dict[str, Any]:
    return {
        "runtime_id": "reflection_detector_v1",
        "candidates": [
            {
                "entity_id": "sign_reflection",
                "entity_type_candidate": "reflection",
                "reflected_text": True,
                "not_real_sign": True,
                "source_runtime": "reflection_detector_v1",
                "candidate_only": True,
            }
        ],
    }


def simulate_occlusion_relations(*, scene_type: str) -> Dict[str, Any]:
    relations = {
        "stacked_documents": [
            {"entity_a": "paper_A", "entity_b": "paper_B", "relation_type": "occludes"},
        ],
        "retail_shelf": [
            {"entity_a": "product_a", "entity_b": "bg_ad", "relation_type": "spatial_layer"},
        ],
        "glass_reflection": [
            {"entity_a": "sign_real", "entity_b": "sign_reflection", "relation_type": "reflection_of"},
        ],
    }.get(scene_type, [])

    return {
        "runtime_id": "overlap_occlusion_detector_v1",
        "candidates": [
            {
                **r,
                "source_runtime": "overlap_occlusion_detector_v1",
                "candidate_only": True,
            }
            for r in relations
        ],
    }


def run_selected_runtimes(
    *,
    runtime_ids: List[str],
    scene_type: str,
    fixture: Dict[str, Any],
) -> Dict[str, Any]:
    """Execute selected lightweight runtimes — selective, not all models."""
    runtime_candidates: List[Dict[str, Any]] = []
    entity_candidates: List[Dict[str, Any]] = []
    relation_candidates: List[Dict[str, Any]] = []
    layout_candidates: List[Dict[str, Any]] = []

    for rid in runtime_ids:
        meta = _runtime_meta(rid)
        runtime_candidates.append({
            "runtime_id": rid,
            "capability": meta.get("capability"),
            "output_type": meta.get("output_type"),
            "candidate_only": True,
        })

        if rid == "document_surface_detector_v1":
            out = simulate_document_surface(scene_type=scene_type)
            entity_candidates.extend(out.get("candidates") or [])
        elif rid == "layout_detector_v1":
            out = simulate_layout_blocks()
            layout_candidates.extend(out.get("candidates") or [])
        elif rid == "price_tag_detector_v1":
            out = simulate_price_tags()
            entity_candidates.extend(out.get("candidates") or [])
        elif rid == "screen_surface_detector_v1":
            out = simulate_screen_surface()
            entity_candidates.extend(out.get("candidates") or [])
        elif rid == "reflection_detector_v1":
            out = simulate_reflection()
            entity_candidates.extend(out.get("candidates") or [])
        elif rid == "overlap_occlusion_detector_v1":
            out = simulate_occlusion_relations(scene_type=scene_type)
            relation_candidates.extend(out.get("candidates") or [])

    conflict = fixture.get("runtime_conflict") and (
        "document_surface_detector_v1" in runtime_ids and "layout_detector_v1" in runtime_ids
    )

    return {
        "execution_id": _uid("lve"),
        "runtime_candidates": runtime_candidates,
        "entity_candidates": entity_candidates,
        "relation_candidates": relation_candidates,
        "layout_region_candidates": layout_candidates,
        "runtime_conflict_detected": conflict,
        "not_all_model_activation": len(runtime_ids) < len(LIGHTWEIGHT_RUNTIMES),
        "no_global_ocr": True,
        "candidate_only": True,
    }
