# -*- coding: utf-8 -*-
"""Document Surface — implementation planning adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_implementation_options_v1 import (
    FIRST_REAL_IMPLEMENTATION_CANDIDATE,
    evaluate_implementation_options,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_benchmark_plan_v1 import (
    build_benchmark_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_contract_v1 import (
    build_implementation_input_contract,
    build_implementation_output_contract,
    validate_contract_alignment,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_failure_modes_v1 import (
    build_failure_modes_registry,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_test_image_registry_v1 import (
    build_test_image_registry_plan,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_PLANNING_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-DryRun-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"


def run_document_surface_implementation_planning(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    """Implementation Planning — 路径选择、契约、失败模式、基准、测试图集规划。"""
    options = evaluate_implementation_options()
    inp = build_implementation_input_contract()
    out = build_implementation_output_contract()
    alignment = validate_contract_alignment(input_contract=inp, output_contract=out)
    failures = build_failure_modes_registry()
    benchmark = build_benchmark_plan()
    test_images = build_test_image_registry_plan()
    registry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Implementation-Planning-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "implementation_planning_only": True,
        "first_real_implementation_candidate": FIRST_REAL_IMPLEMENTATION_CANDIDATE,
        "deferred_candidates": options.get("deferred_candidates"),
        "contract_aligned": alignment.get("aligned_with_dryrun"),
        "failure_modes_count": failures.get("failure_mode_count"),
        "test_image_categories_count": test_images.get("category_count"),
        "benchmark_metrics_count": benchmark.get("metric_count"),
        "implementation_ready_candidate": alignment.get("aligned_with_dryrun") and failures.get("all_modes_complete"),
        "real_execution_enabled": False,
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE,
        "parallel_next_track": PARALLEL_NEXT_TRACK,
        "model_manager_registry_aligned": registry.get("runtime_id") == "document_surface_detector_v1",
        "no_real_model_execution": True,
        "no_ocr_execution": True,
        "no_vlm_call": True,
        "no_image_segmentation_execution": True,
        "candidate_only": True,
        "not_fact": True,
        "planned_at": datetime.now(timezone.utc).isoformat(),
    }

    root = repo_root or Path.cwd()
    out_dir = root / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_v1"
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "implementation_planning_summary.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_dir / "implementation_options_review.json").write_text(
            json.dumps(options, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_dir / "real_runtime_contract_summary.json").write_text(
            json.dumps({"input": inp, "output": out, "alignment": alignment}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        (out_dir / "failure_modes_registry.json").write_text(
            json.dumps(failures, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_dir / "benchmark_plan_summary.json").write_text(
            json.dumps(benchmark, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_dir / "test_image_registry_plan.json").write_text(
            json.dumps(test_images, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "options_review": options,
        "contract_summary": {"input": inp, "output": out, "alignment": alignment},
        "failure_modes_registry": failures,
        "benchmark_plan": benchmark,
        "test_image_registry": test_images,
    }
