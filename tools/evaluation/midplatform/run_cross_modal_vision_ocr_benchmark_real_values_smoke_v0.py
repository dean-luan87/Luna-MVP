#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Smoke-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
            if (parent / "_eval_out").is_dir():
                return parent
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--benchmark-planning-root", required=True)
    ap.add_argument("--v1-track-closures-root", required=True)
    ap.add_argument("--regression-comparison-root", required=True)
    ap.add_argument("--metrics-schema-root", required=True)
    ap.add_argument("--metrics-collector-smoke-root", required=True)
    ap.add_argument("--public-facility-runtime-dryrun-root", required=True)
    ap.add_argument("--poster-track-b-closure-root", required=True)
    ap.add_argument("--realvideo-roi-to-ocr-reference-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.cross_modal_vision_ocr_benchmark_real_values_smoke_v0 import (
        run_cross_modal_vision_ocr_benchmark_real_values_smoke_v0,
    )

    (
        summary,
        value_matrix,
        source_matrix,
        missing_report,
        boundary_report,
        functional_report,
        quality_placeholder,
        interp_guard,
        carryover,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_benchmark_real_values_smoke_v0(
        benchmark_planning_root=str(_require_abs(args.benchmark_planning_root, "--benchmark-planning-root")),
        v1_track_closures_root=str(_require_abs(args.v1_track_closures_root, "--v1-track-closures-root")),
        regression_comparison_root=str(_require_abs(args.regression_comparison_root, "--regression-comparison-root")),
        metrics_schema_root=str(_require_abs(args.metrics_schema_root, "--metrics-schema-root")),
        metrics_collector_smoke_root=str(_require_abs(args.metrics_collector_smoke_root, "--metrics-collector-smoke-root")),
        public_facility_runtime_dryrun_root=str(
            _require_abs(args.public_facility_runtime_dryrun_root, "--public-facility-runtime-dryrun-root")
        ),
        poster_track_b_closure_root=str(_require_abs(args.poster_track_b_closure_root, "--poster-track-b-closure-root")),
        realvideo_roi_to_ocr_reference_root=str(
            _require_abs(args.realvideo_roi_to_ocr_reference_root, "--realvideo-roi-to-ocr-reference-root")
        ),
        simulation_lab_harness_root=str(_require_abs(args.simulation_lab_harness_root, "--simulation-lab-harness-root")),
    )

    summary["output_root"] = str(out)
    summary["errors"] = list(errs)
    summary["phase_verdict_hint"] = "GO" if not errs else "NO_GO"

    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_smoke_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_metric_value_matrix.json", value_matrix)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_source_artifact_matrix.json", source_matrix)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_missing_metric_report.json", missing_report)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_boundary_metrics_report.json", boundary_report)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_functional_smoke_report.json", functional_report)
    _write_json(
        out / "cross_modal_vision_ocr_benchmark_real_values_quality_performance_placeholder_report.json",
        quality_placeholder,
    )
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_interpretation_guard_report.json", interp_guard)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_regression_carryover_report.json", carryover)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_simulation_context_report.json", sim_report)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_non_claims_report.json", non_claims)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_open_followups.json", followups)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_smoke_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_benchmark_real_values_smoke_notes.md").write_text(
        "\n".join(
            [
                "# Benchmark Real Values Smoke",
                "",
                f"- phase: {summary.get('phase')}",
                f"- collection_scope: {summary.get('collection_scope')}",
                f"- t2_collected: {summary.get('t2_quality_performance_values_collected')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Readonly T0/T1 only; not benchmark.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "collection_scope": summary.get("collection_scope"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
