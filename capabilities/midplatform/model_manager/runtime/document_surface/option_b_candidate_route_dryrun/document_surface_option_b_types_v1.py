# -*- coding: utf-8 -*-
"""Document Surface — Option B types v1."""

from __future__ import annotations

OPTION_B_STATUS = "candidate_route_only"
OPTION_B_ROUTE_ID = "option_b_lightweight_segmentation_candidate"

ALLOWED_OUTPUT_TYPES = frozenset({
    "surface_mask_candidate",
    "document_surface_candidate",
    "boundary_candidate",
    "partial_surface_candidate",
    "occlusion_surface_hint_candidate",
    "runtime_error_candidate",
})

FORBIDDEN_OUTPUT_TYPES = frozenset({
    "ocr_text",
    "document_type_fact",
    "layout_semantic_fact",
    "final_owner_fact",
    "document_content",
    "relation_fact",
})

DRYRUN_CASES = (
    "case_a_clear_edges",
    "case_b_low_overlap",
    "case_c_high_overlap",
    "case_e_texture_false_positive",
    "case_f_receipt_clear",
    "case_h_screen_control",
)
