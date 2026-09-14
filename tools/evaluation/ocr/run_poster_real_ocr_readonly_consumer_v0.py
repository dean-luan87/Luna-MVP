#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Poster-Real-OCR-ReadOnly-Consumer-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    candidates: list[Path] = []
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
            candidates.append(parent)
    for parent in candidates:
        if (parent / "_eval_out").is_dir():
            return parent
        sibling = parent.parent / "Luna-Workspace-Min"
        if (sibling / "_eval_out").is_dir():
            return sibling
    return candidates[0] if candidates else here.parents[3]


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
    ap.add_argument("--poster-real-ocr-gated-execution-root", required=True)
    ap.add_argument("--poster-reference-only-root", required=True)
    ap.add_argument("--poster-track-b-closure-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.ocr_runtime.poster_real_ocr_readonly_consumer_v0 import (
        run_poster_real_ocr_readonly_consumer_v0,
    )

    (
        summary,
        view,
        matrix,
        indexes,
        ttl_risk,
        reading,
        visual_sep,
        metrics,
        benchmark,
        health,
        boundary,
        sim,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_poster_real_ocr_readonly_consumer_v0(
        poster_real_ocr_gated_execution_root=str(
            _require_abs(args.poster_real_ocr_gated_execution_root, "poster-real-ocr")
        ),
        poster_reference_only_root=str(_require_abs(args.poster_reference_only_root, "reference")),
        poster_track_b_closure_root=str(_require_abs(args.poster_track_b_closure_root, "track_b")),
        benchmark_real_values_smoke_root=str(_require_abs(args.benchmark_real_values_smoke_root, "benchmark")),
        system_health_governance_root=str(_require_abs(args.system_health_governance_root, "health")),
        simulation_lab_harness_root=str(_require_abs(args.simulation_lab_harness_root, "sim")),
    )

    summary["output_root"] = str(out.resolve())
    summary["input_roots"] = {
        "poster_real_ocr_gated_execution_root": str(
            _require_abs(args.poster_real_ocr_gated_execution_root, "poster-real-ocr")
        ),
        "poster_reference_only_root": str(_require_abs(args.poster_reference_only_root, "reference")),
        "poster_track_b_closure_root": str(_require_abs(args.poster_track_b_closure_root, "track_b")),
        "benchmark_real_values_smoke_root": str(_require_abs(args.benchmark_real_values_smoke_root, "benchmark")),
        "system_health_governance_root": str(_require_abs(args.system_health_governance_root, "health")),
        "simulation_lab_harness_root": str(_require_abs(args.simulation_lab_harness_root, "sim")),
    }

    _write_json(out / "poster_real_ocr_readonly_consumer_summary.json", summary)
    _write_json(out / "poster_real_ocr_region_text_consumer_view.json", view)
    _write_json(out / "poster_real_ocr_region_text_matrix.json", matrix)
    _write_json(out / "poster_real_ocr_readonly_consumer_indexes.json", indexes)
    _write_json(out / "poster_real_ocr_readonly_ttl_risk_report.json", ttl_risk)
    _write_json(out / "poster_real_ocr_readonly_reading_order_guard.json", reading)
    _write_json(out / "poster_real_ocr_readonly_visual_track_separation_check.json", visual_sep)
    _write_json(out / "poster_real_ocr_readonly_metrics_update_candidate_report.json", metrics)
    _write_json(out / "poster_real_ocr_readonly_benchmark_link_report.json", benchmark)
    _write_json(out / "poster_real_ocr_readonly_system_health_link_report.json", health)
    _write_json(out / "poster_real_ocr_readonly_no_write_boundary_report.json", boundary)
    _write_json(out / "poster_real_ocr_readonly_simulation_context_report.json", sim)
    _write_json(out / "poster_real_ocr_readonly_non_claims_report.json", non_claims)
    _write_json(out / "poster_real_ocr_readonly_open_followups.json", followups)
    _write_json(out / "poster_real_ocr_readonly_audit_report.json", audit)

    (out / "poster_real_ocr_readonly_notes.md").write_text(
        "\n".join(
            [
                "# Poster Real OCR ReadOnly Consumer",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- consumer_scope: {summary.get('consumer_scope')}",
                f"- evidence_count: {summary.get('evidence_count_observed')}",
                f"- non_empty: {summary.get('non_empty_region_count')} / empty: {summary.get('empty_region_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Read-only index/archive only; no OCR re-run, no semantic join, no writes.",
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
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
