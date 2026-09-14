# -*- coding: utf-8 -*-
"""No text/fact leak check dryrun."""

from __future__ import annotations

from typing import Any, Dict


def run_no_text_fact_leak_check_dryrun(*, fixture: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    raw = fixture.get("raw_output_profile", "mask_only")
    leak = raw in ("caption_or_text_possible", "document_type_fact_by_default") or "fact" in raw
    return {
        "model_candidate_id": fixture["model_candidate_id"],
        "no_text_fact_leak_check_candidate": "leak_blocked_candidate" if leak else "no_leak_candidate",
        "leak_detected": leak,
        "abort_reason": "text_or_fact_leak_detected" if leak else None,
        "preflight_run_id": run_id,
        "candidate_only": True,
        "not_fact": True,
    }
