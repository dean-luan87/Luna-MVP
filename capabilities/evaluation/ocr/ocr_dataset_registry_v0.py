# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-Foundation-001 — OCR dataset registry v0 (Evaluation Tools).

Registry is evaluation-only metadata; must not be used by runtime.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, List, Optional


ALLOWED_DATASET_TYPES = {
    "synthetic_trdg",
    "synthetic_pillow",
    "realworld_user_sample",
    "public_dataset",
    "human_reviewed",
    "difficult_cases",
    "failure_cases",
    "layout_samples",
    "symbol_glyph_samples",
}


@dataclasses.dataclass(frozen=True)
class OcrDatasetRegistryEntryV0:
    dataset_id: str
    dataset_type: str
    root: str  # absolute path or repo-relative ref; evaluation-only
    sample_count: int
    has_ground_truth: bool
    ground_truth_quality: str  # verified | partial | missing
    language_coverage: List[str]  # ["zh","en","mixed"]
    sample_categories: List[str]
    intended_use: str  # provider_eval | layout_eval | stress_test | regression | dataset_quality_gate
    runtime_allowed: bool


def validate_ocr_dataset_registry_entry_v0(entry: Dict[str, Any]) -> Dict[str, Any]:
    blockers: List[str] = []
    e = entry if isinstance(entry, dict) else {}
    for k in (
        "dataset_id",
        "dataset_type",
        "root",
        "sample_count",
        "has_ground_truth",
        "ground_truth_quality",
        "language_coverage",
        "sample_categories",
        "intended_use",
        "runtime_allowed",
    ):
        if k not in e:
            blockers.append(f"missing:{k}")

    dt = e.get("dataset_type")
    if dt is not None and dt not in ALLOWED_DATASET_TYPES:
        blockers.append(f"invalid:dataset_type:{dt}")

    if e.get("runtime_allowed") is not False:
        blockers.append("boundary:runtime_allowed_must_be_false")

    try:
        if int(e.get("sample_count") or 0) < 0:
            blockers.append("invalid:sample_count_negative")
    except Exception:
        blockers.append("invalid:sample_count_not_int")

    lc = e.get("language_coverage")
    if lc is not None and not isinstance(lc, list):
        blockers.append("invalid:language_coverage_not_list")

    ok = not blockers
    return {"ok": ok, "blockers": blockers}


def build_default_ocr_dataset_registry_v0() -> Dict[str, Any]:
    """
    Returns a minimal registry document describing reserved roots under repo.
    No filesystem access; no dataset generation.
    """
    return {
        "phase": "Phase-EvaluationTools-Foundation-001",
        "registry_kind": "ocr_dataset_registry_v0",
        "entries": [
            {
                "dataset_id": "reserved_ocr_synthetic",
                "dataset_type": "synthetic_pillow",
                "root": "datasets/evaluation/ocr_synthetic/",
                "sample_count": 0,
                "has_ground_truth": True,
                "ground_truth_quality": "partial",
                "language_coverage": ["zh", "en", "mixed"],
                "sample_categories": [],
                "intended_use": "dataset_quality_gate",
                "runtime_allowed": False,
            },
            {
                "dataset_id": "reserved_ocr_realworld",
                "dataset_type": "realworld_user_sample",
                "root": "datasets/evaluation/ocr_realworld/",
                "sample_count": 0,
                "has_ground_truth": False,
                "ground_truth_quality": "missing",
                "language_coverage": ["zh", "en", "mixed"],
                "sample_categories": [],
                "intended_use": "provider_eval",
                "runtime_allowed": False,
            },
            {
                "dataset_id": "reserved_human_review",
                "dataset_type": "human_reviewed",
                "root": "datasets/evaluation/human_review/",
                "sample_count": 0,
                "has_ground_truth": False,
                "ground_truth_quality": "partial",
                "language_coverage": ["zh", "en", "mixed"],
                "sample_categories": [],
                "intended_use": "regression",
                "runtime_allowed": False,
            },
        ],
    }

