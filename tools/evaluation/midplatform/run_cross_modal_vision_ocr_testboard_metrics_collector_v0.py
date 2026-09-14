#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-TestBoard-Metrics-Collector-Smoke-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            return parent
    return here.parents[3]


WS_ROOT = _find_ws_root()
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
    ap.add_argument("--schema-root", required=True)
    ap.add_argument("--v0-closure-root", required=True)
    ap.add_argument("--poster-governance-root", required=True)
    ap.add_argument("--rapidocr-submission-root", required=True)
    ap.add_argument("--rapidocr-readonly-consumer-root", required=True)
    ap.add_argument("--reference-only-rapidocr-root", required=True)
    ap.add_argument("--fusion-dryrun-root", required=True)
    ap.add_argument("--gate-evaluator-root", required=True)
    ap.add_argument("--executor-trace-stub-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.cross_modal_vision_ocr_testboard_metrics_collector_v0 import (
        run_cross_modal_vision_ocr_testboard_metrics_collector_v0,
    )

    summary, value_matrix, missing_report, boundary_report, poster_report, guard, audit, errs = (
        run_cross_modal_vision_ocr_testboard_metrics_collector_v0(
            schema_root=str(_require_abs(args.schema_root, "--schema-root")),
            v0_closure_root=str(_require_abs(args.v0_closure_root, "--v0-closure-root")),
            poster_governance_root=str(_require_abs(args.poster_governance_root, "--poster-governance-root")),
            rapidocr_submission_root=str(_require_abs(args.rapidocr_submission_root, "--rapidocr-submission-root")),
            rapidocr_readonly_consumer_root=str(
                _require_abs(args.rapidocr_readonly_consumer_root, "--rapidocr-readonly-consumer-root")
            ),
            reference_only_rapidocr_root=str(
                _require_abs(args.reference_only_rapidocr_root, "--reference-only-rapidocr-root")
            ),
            fusion_dryrun_root=str(_require_abs(args.fusion_dryrun_root, "--fusion-dryrun-root")),
            gate_evaluator_root=str(_require_abs(args.gate_evaluator_root, "--gate-evaluator-root")),
            executor_trace_stub_root=str(_require_abs(args.executor_trace_stub_root, "--executor-trace-stub-root")),
        )
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_value_matrix.json", value_matrix)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_missing_artifact_report.json", missing_report)
    _write_json(out / "cross_modal_vision_ocr_testboard_boundary_metrics_report.json", boundary_report)
    _write_json(out / "cross_modal_vision_ocr_testboard_poster_metrics_report.json", poster_report)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_interpretation_guard_report.json", guard)
    _write_json(out / "cross_modal_vision_ocr_testboard_metrics_collector_audit_report.json", audit)

    (out / "cross_modal_vision_ocr_testboard_metrics_collector_notes.md").write_text(
        "\n".join(
            [
                "# Metrics Collector Smoke",
                "",
                "Readonly aggregation — no OCR re-run.",
                "",
                f"metrics_collected_count: {summary.get('metrics_collected_count')}",
                f"no_write_boundary_pass_rate: {boundary_report.get('no_write_boundary_pass_rate')}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "metrics_collected_count": summary.get("metrics_collected_count"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
