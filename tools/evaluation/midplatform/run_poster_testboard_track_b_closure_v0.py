#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Poster-TestBoard-Closure-001 runner (closure-only aggregate; no OCR)."""

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
    ap.add_argument("--poster-governance-root", required=True)
    ap.add_argument("--poster-region-ocr-plan-root", required=True)
    ap.add_argument("--poster-visual-symbol-evidence-root", required=True)
    ap.add_argument("--poster-reference-only-root", required=True)
    ap.add_argument("--metrics-collector-root", required=True)
    ap.add_argument("--simulation-lab-harness-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.poster_testboard_track_b_closure_v0 import (
        run_poster_testboard_track_b_closure_v0,
    )

    (
        summary,
        phase_matrix,
        lineage,
        separation,
        boundary,
        capability,
        non_claims,
        followups,
        metrics_snap,
        sim_report,
        audit,
        errs,
    ) = run_poster_testboard_track_b_closure_v0(
        poster_governance_root=str(_require_abs(args.poster_governance_root, "--poster-governance-root")),
        poster_region_ocr_plan_root=str(_require_abs(args.poster_region_ocr_plan_root, "--poster-region-ocr-plan-root")),
        poster_visual_symbol_evidence_root=str(
            _require_abs(args.poster_visual_symbol_evidence_root, "--poster-visual-symbol-evidence-root")
        ),
        poster_reference_only_root=str(_require_abs(args.poster_reference_only_root, "--poster-reference-only-root")),
        metrics_collector_root=str(_require_abs(args.metrics_collector_root, "--metrics-collector-root")),
        simulation_lab_harness_root=str(_require_abs(args.simulation_lab_harness_root, "--simulation-lab-harness-root")),
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)
    summary["phase_verdict_hint"] = "GO" if not errs and summary.get("track_status") == "closed_for_evaluation" else "NO_GO"

    _write_json(out / "poster_testboard_track_b_closure_summary.json", summary)
    _write_json(out / "poster_testboard_track_b_phase_matrix.json", phase_matrix)
    _write_json(out / "poster_testboard_track_b_lineage_matrix.json", lineage)
    _write_json(out / "poster_testboard_track_b_track_separation_report.json", separation)
    _write_json(out / "poster_testboard_track_b_no_write_boundary_matrix.json", boundary)
    _write_json(out / "poster_testboard_track_b_capability_closure_report.json", capability)
    _write_json(out / "poster_testboard_track_b_non_claims_report.json", non_claims)
    _write_json(out / "poster_testboard_track_b_open_followups.json", followups)
    _write_json(out / "poster_testboard_track_b_metrics_snapshot_report.json", metrics_snap)
    _write_json(out / "poster_testboard_track_b_simulation_context_report.json", sim_report)
    _write_json(out / "poster_testboard_track_b_closure_audit_report.json", audit)
    (out / "poster_testboard_track_b_closure_notes.md").write_text(
        "\n".join(
            [
                "# Poster TestBoard Track B Closure v0",
                "",
                f"- phase: Poster-TestBoard-Closure-001",
                f"- track_id: TVOCR_V1_B_POSTER_LAYOUT",
                f"- output_root: {out}",
                f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                f"- errors: {errs or '[]'}",
                "",
                "Closure-only: aggregates Layout Governance, OCR Plan Stub, VisualSymbolEvidence Stub, ReferenceOnly.",
                "No OCR, QR decode, brand, visual symbol registry, fusion, semantic join, or fact writes.",
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
                "track_status": summary.get("track_status"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
