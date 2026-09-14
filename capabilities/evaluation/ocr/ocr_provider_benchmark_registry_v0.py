# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-Foundation-001 — OCR provider benchmark registry v0 (Evaluation Tools).

This registry describes evaluation-only benchmark support and does NOT modify runtime provider selection.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, List, Optional


@dataclasses.dataclass(frozen=True)
class OcrProviderBenchmarkRegistryEntryV0:
    provider_id: str
    provider_family: str  # rapidocr | paddleocr | cnocr | ocr_vl | ...
    runtime_dependency_profile: str
    benchmark_supported: bool
    mainline_provider: bool
    evaluation_only: bool
    allowed_eval_modes: List[str]  # single_image | batch | stress
    metrics_supported: List[str]  # cer | chinese_recall | garbled_score | latency | ...


def validate_ocr_provider_benchmark_registry_entry_v0(entry: Dict[str, Any]) -> Dict[str, Any]:
    blockers: List[str] = []
    e = entry if isinstance(entry, dict) else {}
    for k in (
        "provider_id",
        "provider_family",
        "runtime_dependency_profile",
        "benchmark_supported",
        "mainline_provider",
        "evaluation_only",
        "allowed_eval_modes",
        "metrics_supported",
    ):
        if k not in e:
            blockers.append(f"missing:{k}")
    # Hard boundary: evaluation registry must not claim it can mutate mainline.
    if e.get("benchmark_supported") is True and e.get("evaluation_only") is not True and e.get("mainline_provider") is False:
        # allow mainline_provider==true for current provider, but still ensure registry is eval-only usage
        blockers.append("boundary:evaluation_registry_entry_should_be_evaluation_only")

    if "allowed_eval_modes" in e and not isinstance(e.get("allowed_eval_modes"), list):
        blockers.append("invalid:allowed_eval_modes_not_list")
    if "metrics_supported" in e and not isinstance(e.get("metrics_supported"), list):
        blockers.append("invalid:metrics_supported_not_list")

    return {"ok": not blockers, "blockers": blockers}


def build_default_ocr_provider_benchmark_registry_v0() -> Dict[str, Any]:
    """
    Default skeleton entries for future A/B benchmarks.
    No provider is invoked here.
    """
    return {
        "phase": "Phase-EvaluationTools-Foundation-001",
        "registry_kind": "ocr_provider_benchmark_registry_v0",
        "entries": [
            {
                "provider_id": "rapidocr_onnxruntime_v0",
                "provider_family": "rapidocr",
                "runtime_dependency_profile": "onnxruntime_local",
                "benchmark_supported": True,
                "mainline_provider": True,
                "evaluation_only": False,
                "allowed_eval_modes": ["single_image", "batch", "stress"],
                "metrics_supported": ["cer", "chinese_recall", "garbled_score", "latency", "empty_output_rate"],
            },
            {
                "provider_id": "paddleocr_system_v0",
                "provider_family": "paddleocr",
                "runtime_dependency_profile": "paddle_local_heavy",
                "benchmark_supported": True,
                "mainline_provider": False,
                "evaluation_only": True,
                "allowed_eval_modes": ["single_image", "batch", "stress"],
                "metrics_supported": ["cer", "chinese_recall", "garbled_score", "latency", "empty_output_rate"],
            },
            {
                "provider_id": "cnocr_system_v0",
                "provider_family": "cnocr",
                "runtime_dependency_profile": "pytorch_local_heavy",
                "benchmark_supported": True,
                "mainline_provider": False,
                "evaluation_only": True,
                "allowed_eval_modes": ["single_image", "batch"],
                "metrics_supported": ["cer", "chinese_recall", "garbled_score", "latency", "empty_output_rate"],
            },
        ],
        "notes": "Registry is evaluation-only metadata; must not auto-change runtime provider selection.",
    }

