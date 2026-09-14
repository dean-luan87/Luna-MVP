# -*- coding: utf-8 -*-
"""Document Surface — Option B output contract dryrun v1."""

from __future__ import annotations

from typing import Any, Dict

FORBIDDEN_PROFILES = frozenset({
    "document_type_fact_by_default",
    "caption_or_text_possible",
    "semantic_fact_by_default",
})


def run_output_contract_dryrun(*, candidate: Dict[str, Any]) -> Dict[str, Any]:
    raw = candidate.get("raw_output_profile", "mask_only")
    if raw == "caption_or_text_possible":
        return {
            "output_contract_result_candidate": "blocked_or_requires_wrapper_candidate",
            "contract_compliant": False,
            "blocked_or_requires_wrapper": True,
            "wrapper_required": True,
            "raw_output_must_be_normalized": True,
            "raw_output_not_allowed_downstream": True,
            "execution_allowed": False,
            "candidate_only": True,
            "not_fact": True,
        }
    if raw in FORBIDDEN_PROFILES or "fact" in raw:
        return {
            "output_contract_result_candidate": "blocked_output_contract_violation_candidate",
            "contract_compliant": False,
            "blocked_or_requires_wrapper": False,
            "candidate_only": True,
            "not_fact": True,
        }
    return {
        "output_contract_result_candidate": "output_contract_compatible_candidate",
        "contract_compliant": True,
        "blocked_or_requires_wrapper": False,
        "candidate_only": True,
        "not_fact": True,
    }
