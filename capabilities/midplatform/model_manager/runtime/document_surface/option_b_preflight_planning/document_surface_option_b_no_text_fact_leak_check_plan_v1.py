# -*- coding: utf-8 -*-
"""Document Surface — Option B no text/fact leak check plan v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_no_text_fact_leak_check_plan() -> Dict[str, Any]:
    return {
        "plan_id": "option_b_no_text_fact_leak_check_plan_v1",
        "check_type": "no_text_fact_leak_check",
        "output_type": "no_text_fact_leak_check_candidate",
        "scan_targets": [
            "ocr_text",
            "caption",
            "natural_language_interpretation",
            "document_type_fact",
            "layout_semantic_fact",
            "relation_fact",
            "document_content",
        ],
        "rules": [
            "scan_output_for_text_fact_leak",
            "no_rename_bypass",
            "any_leak_aborts",
        ],
        "abort_on": ["text_or_fact_leak_detected"],
        "candidate_only": True,
        "not_fact": True,
    }
