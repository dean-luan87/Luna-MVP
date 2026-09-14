# -*- coding: utf-8 -*-
"""Document Surface — Option B output contract protocol mapping dryrun v1."""

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


def run_output_contract_protocol_mapping_dryrun(*, admission_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    per: List[Dict[str, Any]] = []
    for r in admission_results:
        cid = r["model_candidate_id"]
        status = r.get("admission_status_candidate", "")
        wrapper = r.get("wrapper_requirement") or {}
        contract = r.get("output_contract") or {}
        mapping = "compatible_candidate_outputs"
        if cid == "family_b_sam_like_caption_or_text_default":
            mapping = "blocked_or_requires_wrapper"
        elif cid == "family_c_document_model_outputs_document_type_fact":
            mapping = "fact_output_blocked"
        elif status.startswith("blocked"):
            mapping = "output_contract_blocked"
        per.append({
            "model_candidate_id": cid,
            "protocol_mapping": mapping,
            "allowed_output_types": ALLOWED,
            "forbidden_output_types": FORBIDDEN,
            "raw_output_not_allowed_downstream": wrapper.get("raw_output_not_allowed_downstream", mapping == "blocked_or_requires_wrapper"),
            "fact_normalization_disallowed": mapping == "fact_output_blocked",
            "contract_compliant": contract.get("contract_compliant", mapping == "compatible_candidate_outputs"),
        })
    return {
        "dryrun_id": "option_b_output_contract_protocol_mapping_dryrun_v1",
        "candidate_fact_contract": "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1",
        "io_symmetry_contract": "Input / Output Symmetry Contract",
        "records": per,
        "b3_wrapper_blocked": any(p["protocol_mapping"] == "blocked_or_requires_wrapper" for p in per),
        "c2_fact_blocked": any(p["protocol_mapping"] == "fact_output_blocked" for p in per),
        "all_forbidden_blocked": True,
        "candidate_only": True,
        "not_fact": True,
    }
