#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Poster-Real-OCR-Reference-Closure-001 runner."""

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
    ap.add_argument("--poster-layout-governance-root", required=True)
    ap.add_argument("--poster-region-ocr-plan-root", required=True)
    ap.add_argument("--poster-visual-symbol-evidence-root", required=True)
    ap.add_argument("--poster-original-reference-only-root", required=True)
    ap.add_argument("--poster-track-b-closure-root", required=True)
    ap.add_argument("--poster-real-ocr-gated-execution-root", required=True)
    ap.add_argument("--poster-real-ocr-readonly-consumer-root", required=True)
    ap.add_argument("--poster-real-ocr-reference-update-root", required=True)
    ap.add_argument("--benchmark-real-values-smoke-root", required=True)
    ap.add_argument("--system-health-governance-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.poster_real_ocr_reference_closure_v0 import (
        run_poster_real_ocr_reference_closure_v0,
    )

    roots = {
        "layout": _require_abs(args.poster_layout_governance_root, "layout"),
        "plan": _require_abs(args.poster_region_ocr_plan_root, "plan"),
        "visual": _require_abs(args.poster_visual_symbol_evidence_root, "visual"),
        "orig_ref": _require_abs(args.poster_original_reference_only_root, "orig-ref"),
        "track_b": _require_abs(args.poster_track_b_closure_root, "track-b"),
        "ocr_exec": _require_abs(args.poster_real_ocr_gated_execution_root, "ocr-exec"),
        "consumer": _require_abs(args.poster_real_ocr_readonly_consumer_root, "consumer"),
        "ref_upd": _require_abs(args.poster_real_ocr_reference_update_root, "ref-upd"),
        "bench": _require_abs(args.benchmark_real_values_smoke_root, "bench"),
        "health": _require_abs(args.system_health_governance_root, "health"),
        "sim": _require_abs(args.simulation_lab_harness_root, "sim"),
    }

    (
        summary,
        phase_matrix,
        lineage,
        track_matrix,
        alignment_closure,
        visual_closure,
        reading_closure,
        ttl_closure,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    ) = run_poster_real_ocr_reference_closure_v0(
        poster_layout_governance_root=str(roots["layout"]),
        poster_region_ocr_plan_root=str(roots["plan"]),
        poster_visual_symbol_evidence_root=str(roots["visual"]),
        poster_original_reference_only_root=str(roots["orig_ref"]),
        poster_track_b_closure_root=str(roots["track_b"]),
        poster_real_ocr_gated_execution_root=str(roots["ocr_exec"]),
        poster_real_ocr_readonly_consumer_root=str(roots["consumer"]),
        poster_real_ocr_reference_update_root=str(roots["ref_upd"]),
        benchmark_real_values_smoke_root=str(roots["bench"]),
        system_health_governance_root=str(roots["health"]),
        simulation_lab_harness_root=str(roots["sim"]),
        output_root=str(out),
    )

    summary["input_roots"] = {k: str(v) for k, v in roots.items()}

    _write_json(out / "poster_real_ocr_reference_closure_summary.json", summary)
    _write_json(out / "poster_real_ocr_reference_closure_phase_matrix.json", phase_matrix)
    _write_json(out / "poster_real_ocr_reference_lineage_closure_report.json", lineage)
    _write_json(out / "poster_real_ocr_reference_track_closure_matrix.json", track_matrix)
    _write_json(out / "poster_real_ocr_reference_alignment_closure_report.json", alignment_closure)
    _write_json(out / "poster_real_ocr_reference_visual_symbol_closure_report.json", visual_closure)
    _write_json(out / "poster_real_ocr_reference_reading_order_closure_report.json", reading_closure)
    _write_json(out / "poster_real_ocr_reference_ttl_risk_closure_report.json", ttl_closure)
    _write_json(out / "poster_real_ocr_reference_metrics_closure_candidate_report.json", metrics)
    _write_json(out / "poster_real_ocr_reference_closure_benchmark_link_report.json", benchmark_link)
    _write_json(out / "poster_real_ocr_reference_closure_system_health_link_report.json", health_link)
    _write_json(out / "poster_real_ocr_reference_closure_no_write_boundary_report.json", boundary)
    _write_json(out / "poster_real_ocr_reference_closure_simulation_context_report.json", sim_report)
    _write_json(out / "poster_real_ocr_reference_closure_non_claims_report.json", non_claims)
    _write_json(out / "poster_real_ocr_reference_closure_open_followups.json", followups)
    _write_json(out / "poster_real_ocr_reference_closure_audit_report.json", audit)

    (out / "poster_real_ocr_reference_closure_notes.md").write_text(
        "\n".join(
            [
                "# Poster Real OCR Reference Closure",
                "",
                f"- Phase: {summary.get('phase')}",
                f"- closure_scope: {summary.get('closure_scope')}",
                f"- poster_real_ocr_reference_status: {summary.get('poster_real_ocr_reference_status')}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                "",
                "Reference chain closure only; no OCR re-run, no fusion, no writes.",
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
