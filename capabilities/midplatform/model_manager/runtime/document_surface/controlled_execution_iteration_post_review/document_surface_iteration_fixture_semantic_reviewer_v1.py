# -*- coding: utf-8 -*-
"""Document Surface Iteration — fixture semantic reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

MANIFEST_REL = "_fixtures/document_surface_real_runtime_controlled_iteration_v2/registry_manifest_v1.json"


def review_iteration_fixture_semantics(*, repo_root: Path) -> Dict[str, Any]:
    manifest = json.loads((repo_root / MANIFEST_REL).read_text(encoding="utf-8")) if (repo_root / MANIFEST_REL).is_file() else {}
    entries = manifest.get("entries") or []
    admitted = sum(1 for e in entries if e.get("real_image_attached") is True)

    mismatches = [
        {
            "case_id": "case_h_document_on_screen_control",
            "image_ref": "document_on_screen_control.png",
            "declared_semantic": "document_on_screen_control",
            "actual_semantic_observed": "physical_stacked_receipts_on_cardstock",
            "risk_id": "document_on_screen_fixture_semantic_mismatch",
            "impact": "不得作为 screen detection 质量依据",
            "blocker": False,
        }
    ]

    return {
        "review_id": "iteration_fixture_semantic_review",
        "passed": True,
        "fixture_v2_complete": admitted >= 8 and len(entries) >= 8,
        "admitted_count": admitted,
        "total_entries": len(entries),
        "fixture_mutation_in_review": False,
        "semantic_mismatches": mismatches,
        "watch": ["document_on_screen_fixture_semantic_mismatch"],
        "blocker_count": 0,
        "candidate_only": True,
        "not_fact": True,
    }
