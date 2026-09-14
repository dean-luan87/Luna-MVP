# -*- coding: utf-8 -*-
"""Document Surface Implementation — benchmark reviewer v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_benchmark_plan_v1 import (
    BENCHMARK_METRICS,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_dryrun_adapter_v1 import (
    run_full_implementation_dryrun,
)

REQUIRED_METRICS = (
    "surface_detection_candidate_rate", "false_surface_candidate_rate",
    "overlap_relation_candidate_rate", "occlusion_hint_candidate_rate",
    "attention_blocked_runtime_call_rate", "no_ocr_leak_rate",
    "candidate_only_compliance_rate", "runtime_error_handling_rate",
    "ownership_package_compatibility_rate", "text_owner_assignment_ready_rate",
)


def review_implementation_benchmark(*, repo_root: Path) -> Dict[str, Any]:
    full = run_full_implementation_dryrun(repo_root=repo_root, write_outputs=False)
    benchmark = full.get("benchmark_summary") or {}
    metrics = benchmark.get("metrics") or {}
    non_acc = all(not m.get("accuracy_only") for m in BENCHMARK_METRICS)

    targets = (
        metrics.get("attention_blocked_runtime_call_rate") == 0
        and metrics.get("no_ocr_leak_rate") == 1
        and metrics.get("candidate_only_compliance_rate") == 1
    )

    return {
        "review_id": "document_surface_implementation_benchmark_review_v1",
        "metric_count": benchmark.get("metric_count"),
        "metrics_present": all(m in metrics for m in REQUIRED_METRICS),
        "non_accuracy_only": non_acc and benchmark.get("non_accuracy_only") is True,
        "targets_met": targets,
        "metrics": metrics,
        "passed": targets and all(m in metrics for m in REQUIRED_METRICS),
    }
