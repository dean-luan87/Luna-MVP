#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Planning-001 runner."""

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
    ap.add_argument("--v1-track-closures-root", required=True)
    ap.add_argument("--regression-comparison-root", required=True)
    ap.add_argument("--metrics-schema-root", required=True)
    ap.add_argument("--metrics-collector-smoke-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.cross_modal_vision_ocr_benchmark_real_values_planning_v0 import (
        run_cross_modal_vision_ocr_benchmark_real_values_planning_v0,
    )

    (
        summary,
        tier_matrix,
        source_map,
        gate_policy,
        interp_policy,
        gt_report,
        sim_plan,
        output_contract,
        regression_link,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_cross_modal_vision_ocr_benchmark_real_values_planning_v0(
        v1_track_closures_root=str(_require_abs(args.v1_track_closures_root, "--v1-track-closures-root")),
        regression_comparison_root=str(_require_abs(args.regression_comparison_root, "--regression-comparison-root")),
        metrics_schema_root=str(_require_abs(args.metrics_schema_root, "--metrics-schema-root")),
        metrics_collector_smoke_root=str(_require_abs(args.metrics_collector_smoke_root, "--metrics-collector-smoke-root")),
        simulation_lab_harness_root=str(_require_abs(args.simulation_lab_harness_root, "--simulation-lab-harness-root")),
    )

    summary["output_root"] = str(out)
    summary["errors"] = list(errs)
    summary["phase_verdict_hint"] = "GO" if not errs else "NO_GO"

    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_planning_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_benchmark_metric_tier_matrix.json", tier_matrix)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_source_map.json", source_map)
    _write_json(out / "cross_modal_vision_ocr_benchmark_collector_gate_policy.json", gate_policy)
    _write_json(out / "cross_modal_vision_ocr_benchmark_metric_interpretation_policy.json", interp_policy)
    _write_json(out / "cross_modal_vision_ocr_benchmark_ground_truth_requirement_report.json", gt_report)
    _write_json(out / "cross_modal_vision_ocr_benchmark_simulation_profile_binding_plan.json", sim_plan)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_collector_output_contract.json", output_contract)
    _write_json(out / "cross_modal_vision_ocr_benchmark_regression_link_report.json", regression_link)
    _write_json(out / "cross_modal_vision_ocr_benchmark_non_claims_report.json", non_claims)
    _write_json(out / "cross_modal_vision_ocr_benchmark_open_followups.json", followups)
    _write_json(out / "cross_modal_vision_ocr_benchmark_real_values_planning_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_benchmark_real_values_planning_notes.md").write_text(
        "\n".join(
            [
                "# Benchmark Collector Real Values Planning",
                "",
                f"- phase: {summary.get('phase')}",
                f"- planning_scope: {summary.get('planning_scope')}",
                f"- benchmark_values_collected: {summary.get('benchmark_values_collected')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Planning only; no OCR, no benchmark values, no provider comparison.",
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
                "planning_scope": summary.get("planning_scope"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
