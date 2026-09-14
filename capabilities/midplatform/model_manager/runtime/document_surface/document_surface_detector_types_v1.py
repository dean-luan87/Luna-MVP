# -*- coding: utf-8 -*-
"""Document Surface Detector — planning types v1."""

from __future__ import annotations

RUNTIME_ID = "document_surface_detector_v1"
CAPABILITY = "detect_document_surface"
OUTPUT_TYPE = "document_surface_candidate"
EXECUTION_MODE_PLANNING = "planning_fixture"

ALLOWED_CAPABILITIES = ("detect_document_surface", "detect_overlap_occlusion")
FORBIDDEN_CAPABILITIES = (
    "text_recognition",
    "ocr",
    "global_ocr",
    "vlm",
    "full_scene_segmentation",
    "layout_semantic_parse",
)

VISIBILITY_STATUSES = ("visible", "partial", "occluded", "uncertain")
RELATION_TYPES = ("overlaps", "occludes", "behind", "attached_to", "uncertain", "reflection_of")

SURFACE_CANDIDATE_REQUIRED = (
    "surface_id",
    "source_region_id",
    "visibility_status_candidate",
    "candidate_only",
    "not_fact",
)
