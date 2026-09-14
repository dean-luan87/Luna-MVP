# -*- coding: utf-8 -*-
"""Document Surface — Option B admission output contract reviewer v1."""

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


def review_output_contract(*, registry: Dict[str, Any]) -> Dict[str, Any]:
    fixtures: List[Dict[str, Any]] = registry.get("fixtures") or []
    allowed_ok = all(set(ALLOWED).issubset(set(f.get("output_types_allowed") or [])) for f in fixtures)
    forbidden_ok = all(set(FORBIDDEN).issubset(set(f.get("output_types_forbidden") or [])) for f in fixtures)
    checks = {
        "allowed_outputs_complete": allowed_ok,
        "forbidden_outputs_complete": forbidden_ok,
        "no_ocr_in_allowed": all("ocr" not in str(o).lower() or "runtime_error" in o for f in fixtures for o in (f.get("output_types_allowed") or [])),
        "caption_forbidden": all("caption" in (f.get("output_types_forbidden") or []) for f in fixtures),
        "document_type_fact_forbidden": all("document_type_fact" in (f.get("output_types_forbidden") or []) for f in fixtures),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_output_contract_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "allowed_output_types": ALLOWED,
        "forbidden_output_types": FORBIDDEN,
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
