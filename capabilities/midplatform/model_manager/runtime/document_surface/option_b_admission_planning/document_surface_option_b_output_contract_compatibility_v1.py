# -*- coding: utf-8 -*-
"""Document Surface — Option B output contract compatibility v1."""

from __future__ import annotations

from typing import Any, Dict, List

ALLOWED = frozenset({
    "surface_mask_candidate",
    "document_surface_candidate",
    "boundary_candidate",
    "partial_surface_candidate",
    "occlusion_surface_hint_candidate",
    "runtime_error_candidate",
})

FORBIDDEN = frozenset({
    "ocr_text",
    "document_type_fact",
    "layout_semantic_fact",
    "final_owner_fact",
    "document_content",
    "relation_fact",
    "caption",
    "natural_language_interpretation",
})


def build_output_contract_compatibility() -> Dict[str, Any]:
    text_default_models = [
        {
            "model_pattern": "vlm_like_caption_default",
            "default_output": "caption",
            "admission_status_candidate": "blocked_or_requires_wrapper",
            "wrapper_required": True,
            "raw_output_must_be_normalized": True,
            "raw_output_not_allowed_downstream": True,
        },
        {
            "model_pattern": "sam_with_semantic_head",
            "default_output": "semantic_label",
            "admission_status_candidate": "blocked_or_requires_wrapper",
            "wrapper_required": True,
            "raw_output_must_be_normalized": True,
            "raw_output_not_allowed_downstream": True,
        },
    ]
    return {
        "compatibility_id": "document_surface_option_b_output_contract_compatibility_v1",
        "allowed_output_types": sorted(ALLOWED),
        "forbidden_output_types": sorted(FORBIDDEN),
        "caption_text_semantic_blocked_or_wrapper": len(text_default_models) >= 2,
        "text_default_model_policies": text_default_models,
        "downstream_caption_forbidden": True,
        "candidate_only": True,
        "not_fact": True,
    }
