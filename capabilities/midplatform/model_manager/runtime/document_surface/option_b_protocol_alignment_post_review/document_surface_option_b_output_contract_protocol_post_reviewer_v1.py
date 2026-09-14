# -*- coding: utf-8 -*-
"""Document Surface — Option B output contract protocol post-reviewer v1."""

from __future__ import annotations

from typing import Any, Dict


def review_output_contract_protocol(*, output_results: Dict[str, Any]) -> Dict[str, Any]:
    records = output_results.get("records") or []
    first = records[0] if records else {}
    b3 = next((r for r in records if r.get("model_candidate_id") == "family_b_sam_like_caption_or_text_default"), {})
    c2 = next((r for r in records if r.get("model_candidate_id") == "family_c_document_model_outputs_document_type_fact"), {})
    allowed = first.get("allowed_output_types") or output_results.get("allowed_output_types") or []
    forbidden = first.get("forbidden_output_types") or output_results.get("forbidden_output_types") or []
    checks = {
        "allowed_types": len(allowed) >= 6,
        "forbidden_types": len(forbidden) >= 8,
        "b3_wrapper": b3.get("protocol_mapping") == "blocked_or_requires_wrapper",
        "b3_raw_blocked": b3.get("raw_output_not_allowed_downstream") is True,
        "c2_fact_blocked": c2.get("protocol_mapping") == "fact_output_blocked",
        "c2_no_disguise": c2.get("fact_normalization_disallowed") is True,
        "all_forbidden_blocked": output_results.get("all_forbidden_blocked") is True,
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_output_contract_protocol_post_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
