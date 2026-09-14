# -*- coding: utf-8 -*-
"""Document Surface — real runtime failure modes v1."""

from __future__ import annotations

from typing import Any, Dict, List

FAILURE_MODES: List[Dict[str, Any]] = [
    {
        "failure_mode_id": "no_document_surface_found",
        "output_candidate": "empty_surface_candidates",
        "validation_status": "needs_more_evidence",
        "next_action": "request_more_evidence_or_replan_attention",
        "forbidden_fallback": ["ocr", "vlm", "full_scene_segmentation"],
    },
    {
        "failure_mode_id": "low_contrast_boundary",
        "output_candidate": "uncertain_surface_candidate",
        "validation_status": "needs_more_evidence",
        "next_action": "lower_confidence_candidate_only",
        "forbidden_fallback": ["ocr", "vlm", "layout_parser"],
    },
    {
        "failure_mode_id": "severe_occlusion",
        "output_candidate": "partial_surface_candidate_with_occlusion_hint",
        "validation_status": "pending_validation",
        "next_action": "emit_relation_hint_occludes",
        "forbidden_fallback": ["merge_documents", "ocr"],
    },
    {
        "failure_mode_id": "curved_or_folded_surface",
        "output_candidate": "polygon_candidate_uncertain",
        "validation_status": "needs_more_evidence",
        "next_action": "request_more_evidence",
        "forbidden_fallback": ["document_fact", "vlm"],
    },
    {
        "failure_mode_id": "multiple_overlapping_surfaces",
        "output_candidate": "multiple_surface_candidates_with_overlap_relation",
        "validation_status": "pending_validation",
        "next_action": "emit_overlap_relation_hints",
        "forbidden_fallback": ["merge_overlapped_documents", "global_ocr"],
    },
    {
        "failure_mode_id": "reflective_surface_confusion",
        "output_candidate": "uncertain_surface_candidate",
        "validation_status": "validation_review",
        "next_action": "defer_or_request_more_evidence",
        "forbidden_fallback": ["vlm", "layout_fact"],
    },
    {
        "failure_mode_id": "screen_surface_confusion",
        "output_candidate": "possible_screen_document_content_candidate",
        "validation_status": "defer_to_screen_surface_detector",
        "next_action": "handoff_screen_surface_detector",
        "forbidden_fallback": ["paper_document_fact", "ocr"],
    },
    {
        "failure_mode_id": "background_texture_false_positive",
        "output_candidate": "low_confidence_surface_candidate",
        "validation_status": "validation_review",
        "next_action": "suppress_or_review",
        "forbidden_fallback": ["full_scene_segmentation", "ocr"],
    },
    {
        "failure_mode_id": "runtime_dependency_missing",
        "output_candidate": "document_surface_runtime_error_candidate",
        "validation_status": "runtime_error",
        "next_action": "handoff_to_l2_or_attention_replan",
        "forbidden_fallback": ["ocr", "vlm", "silent_fallback"],
    },
    {
        "failure_mode_id": "runtime_timeout",
        "output_candidate": "document_surface_runtime_error_candidate",
        "validation_status": "runtime_error",
        "next_action": "handoff_to_l2_or_attention_replan",
        "forbidden_fallback": ["ocr", "vlm", "full_scene_segmentation"],
    },
    {
        "failure_mode_id": "unsupported_image_format",
        "output_candidate": "document_surface_runtime_error_candidate",
        "validation_status": "runtime_error",
        "next_action": "reject_input_candidate_only",
        "forbidden_fallback": ["ocr", "vlm"],
    },
]


def build_failure_modes_registry() -> Dict[str, Any]:
    complete = all(
        fm.get("output_candidate") and fm.get("validation_status")
        and fm.get("next_action") and fm.get("forbidden_fallback")
        for fm in FAILURE_MODES
    )
    return {
        "registry_id": "document_surface_failure_modes_v1",
        "failure_mode_count": len(FAILURE_MODES),
        "failure_modes": FAILURE_MODES,
        "all_modes_complete": complete,
        "candidate_only": True,
        "not_fact": True,
    }
