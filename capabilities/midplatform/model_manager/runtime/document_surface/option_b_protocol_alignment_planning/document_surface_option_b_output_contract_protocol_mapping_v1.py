# -*- coding: utf-8 -*-
"""Document Surface — Option B output contract protocol mapping v1."""

from __future__ import annotations

from typing import Any, Dict

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


def build_output_contract_protocol_mapping(*, contract_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "mapping_id": "option_b_output_contract_protocol_mapping_v1",
        "candidate_fact_contract": "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1",
        "io_symmetry_contract": "Input / Output Symmetry Contract",
        "allowed_output_types": ALLOWED,
        "forbidden_output_types": FORBIDDEN,
        "no_fact_promotion": True,
        "no_ocr_text_caption_downstream": True,
        "wrapper_path_for_caption_models": any(
            r.get("output_contract_result_candidate") == "blocked_or_requires_wrapper_candidate"
            for r in contract_results
        ),
        "contract_results_summary": [
            {"result": r.get("output_contract_result_candidate"), "compliant": r.get("contract_compliant")}
            for r in contract_results
        ],
        "candidate_only": True,
        "not_fact": True,
    }
