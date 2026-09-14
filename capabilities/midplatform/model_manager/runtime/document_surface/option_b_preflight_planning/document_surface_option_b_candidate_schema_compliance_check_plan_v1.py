# -*- coding: utf-8 -*-
"""Document Surface — Option B candidate schema compliance check plan v1."""

from __future__ import annotations

from typing import Any, Dict, List

ALLOWED = [
    "surface_mask_candidate",
    "document_surface_candidate",
    "boundary_candidate",
    "partial_surface_candidate",
    "occlusion_surface_hint_candidate",
    "runtime_error_candidate",
]

FORBIDDEN = [
    "ocr_text",
    "caption",
    "natural_language_interpretation",
    "document_type_fact",
    "layout_semantic_fact",
    "final_owner_fact",
    "document_content",
    "relation_fact",
]


def build_candidate_schema_compliance_check_plan() -> Dict[str, Any]:
    return {
        "plan_id": "option_b_candidate_schema_compliance_check_plan_v1",
        "check_type": "candidate_schema_compliance_check",
        "output_type": "candidate_schema_compliance_check_candidate",
        "allowed_output_types": ALLOWED,
        "forbidden_output_types": FORBIDDEN,
        "abort_on": ["candidate_schema_violation"],
        "candidate_only": True,
        "not_fact": True,
    }
