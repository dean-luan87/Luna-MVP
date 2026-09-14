#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Poster-Real-OCR-Reference-Update-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if (parent / "_eval_out").is_dir():
                return parent
            sibling = parent.parent / "Luna-Workspace-Min"
            if (sibling / "_eval_out").is_dir():
                return sibling
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
    ap.add_argument("--poster-real-ocr-gated-execution-root", required=True)
    ap.add_argument("--poster-real-ocr-readonly-consumer-root", required=True)
    ap.add_argument("--poster-original-reference-only-root", required=True)
    ap.add_argument("--poster-visual-symbol-evidence-root", required=True)
    ap.add_argument("--poster-track-b-closure-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.poster_real_ocr_reference_update_v0 import (
        run_poster_real_ocr_reference_update_v0,
    )

    (
        summary,
        candidate,
        alignment,
        visual_preserve,
        track_sep,
        reading,
        ttl_risk,
        source_chain,
        metrics,
        benchmark,
        health,
        boundary,
        sim,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_poster_real_ocr_reference_update_v0(
        poster_real_ocr_gated_execution_root=str(
            _require_abs(args.poster_real_ocr_gated_execution_root, "gated-execution")
        ),
        poster_real_ocr_readonly_consumer_root=str(
            _require_abs(args.poster_real_ocr_readonly_consumer_root, "readonly-consumer")
        ),
        poster_original_reference_only_root=str(
            _require_abs(args.poster_original_reference_only_root, "original-reference")
        ),
        poster_visual_symbol_evidence_root=str(
            _require_abs(args.poster_visual_symbol_evidence_root, "visual-symbol")
        ),
        poster_track_b_closure_root=str(_require_abs(args.poster_track_b_closure_root, "track-b")),
        benchmark_real_values_smoke_root=str(_require_abs(args.benchmark_real_values_smoke_root, "benchmark")),
        system_health_governance_root=str(_require_abs(args.system_health_governance_root, "health")),
        simulation_lab_harness_root=str(_require_abs(args.simulation_lab_harness_root, "sim")),
    )

    summary["output_root"] = str(out.resolve())
    summary["input_roots"] = {
        "poster_real_ocr_gated_execution_root": str(
            _require_abs(args.poster_real_ocr_gated_execution_root, "gated-execution")
        ),
        "poster_real_ocr_readonly_consumer_root": str(
            _require_abs(args.poster_real_ocr_readonly_consumer_root, "readonly-consumer")
        ),
        "poster_original_reference_only_root": str(
            _require_abs(args.poster_original_reference_only_root, "original-reference")
        ),
        "poster_visual_symbol_evidence_root": str(
            _require_abs(args.poster_visual_symbol_evidence_root, "visual-symbol")
        ),
        "poster_track_b_closure_root": str(_require_abs(args.poster_track_b_closure_root, "track-b")),
        "benchmark_real_values_smoke_root": str(_require_abs(args.benchmark_real_values_smoke_root, "benchmark")),
        "system_health_governance_root": str(_require_abs(args.system_health_governance_root, "health")),
        "simulation_lab_harness_root": str(_require_abs(args.simulation_lab_harness_root, "sim")),
    }

    _write_json(out / "poster_real_ocr_reference_update_summary.json", summary)
    _write_json(out / "poster_real_ocr_updated_reference_candidate.json", candidate)
    _write_json(out / "poster_real_ocr_text_plan_alignment_matrix.json", alignment)
    _write_json(out / "poster_real_ocr_visual_symbol_reference_preservation_report.json", visual_preserve)
    _write_json(out / "poster_real_ocr_reference_update_track_separation_report.json", track_sep)
    _write_json(out / "poster_real_ocr_reference_update_reading_order_guard.json", reading)
    _write_json(out / "poster_real_ocr_reference_update_ttl_risk_report.json", ttl_risk)
    _write_json(out / "poster_real_ocr_reference_update_source_chain_report.json", source_chain)
    _write_json(out / "poster_real_ocr_reference_update_metrics_candidate_report.json", metrics)
    _write_json(out / "poster_real_ocr_reference_update_benchmark_link_report.json", benchmark)
    _write_json(out / "poster_real_ocr_reference_update_system_health_link_report.json", health)
    _write_json(out / "poster_real_ocr_reference_update_no_write_boundary_report.json", boundary)
    _write_json(out / "poster_real_ocr_reference_update_simulation_context_report.json", sim)
    _write_json(out / "poster_real_ocr_reference_update_non_claims_report.json", non_claims)
    _write_json(out / "poster_real_ocr_reference_update_open_followups.json", followups)
    _write_json(out / "poster_real_ocr_reference_update_audit_report.json", audit)

    (out / "poster_real_ocr_reference_update_notes.md").write_text(
        "\n".join(
            [
                "# Poster Real OCR Reference Update",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- reference_scope: {summary.get('reference_scope')}",
                f"- plan refs: {summary.get('original_text_plan_ref_count')}",
                f"- real OCR refs: {summary.get('real_ocr_text_evidence_ref_count')}",
                f"- visual refs: {summary.get('visual_symbol_ref_count')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Parallel reference update only; no OCR re-run, no fusion, no writes.",
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
