#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Poster-OCR-ReferenceOnly-001 runner (reference-only; no OCR)."""

from __future__ import annotations

import argparse
import json
import subprocess
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


def _bootstrap_inputs(
    ws: Path,
    poster_gov: Path,
    ocr_plan: Path,
    visual: Path,
    metrics: Path,
) -> None:
    """Generate prerequisite smoke roots when missing (no OCR)."""
    poster_gov.mkdir(parents=True, exist_ok=True)
    ocr_plan.mkdir(parents=True, exist_ok=True)
    visual.mkdir(parents=True, exist_ok=True)
    metrics.mkdir(parents=True, exist_ok=True)
    rv_stub = ws / "_eval_out" / "_poster_bootstrap_realvideo_stub"
    rv_stub.mkdir(parents=True, exist_ok=True)

    if not (poster_gov / "poster_layout_governance_summary.json").is_file():
        subprocess.run(
            [
                sys.executable,
                str(ws / "tools/evaluation/ocr/run_poster_layout_segmentation_governance_v0.py"),
                "--output-root",
                str(poster_gov),
            ],
            cwd=str(ws),
            check=True,
        )

    if not (ocr_plan / "poster_region_ocr_plan_stub.json").is_file():
        subprocess.run(
            [
                sys.executable,
                str(ws / "tools/evaluation/ocr/run_poster_region_ocr_plan_stub_v0.py"),
                "--output-root",
                str(ocr_plan),
                "--poster-governance-root",
                str(poster_gov),
                "--realvideo-registry-root",
                str(rv_stub),
                "--metrics-collector-root",
                str(metrics),
            ],
            cwd=str(ws),
            check=True,
        )

    if not (visual / "poster_visual_symbol_evidence_items.json").is_file():
        subprocess.run(
            [
                sys.executable,
                str(ws / "tools/evaluation/ocr/run_poster_visual_symbol_evidence_stub_v0.py"),
                "--output-root",
                str(visual),
                "--poster-governance-root",
                str(poster_gov),
                "--poster-region-ocr-plan-root",
                str(ocr_plan),
                "--metrics-collector-root",
                str(metrics),
                "--realvideo-registry-root",
                str(rv_stub),
            ],
            cwd=str(ws),
            check=True,
        )

    if not (metrics / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json").is_file():
        _write_json(
            metrics / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json",
            {
                "schema_version": "cross_modal_vision_ocr_testboard_metrics_collection_summary_v0",
                "phase": "bootstrap_stub_for_poster_reference_only",
                "poster_governance_root": str(poster_gov),
                "bootstrap_only": True,
            },
        )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--poster-governance-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_layout_segmentation_governance_smoke_v0",
    )
    ap.add_argument(
        "--poster-region-ocr-plan-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_region_ocr_plan_stub_smoke_v0",
    )
    ap.add_argument(
        "--poster-visual-symbol-evidence-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/poster_visual_symbol_evidence_stub_smoke_v0",
    )
    ap.add_argument(
        "--metrics-collector-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_testboard_metrics_collector_smoke_v0",
    )
    ap.add_argument(
        "--simulation-lab-harness-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full",
    )
    ap.add_argument("--bootstrap-inputs", action="store_true", help="Generate missing prerequisite smoke roots")
    args = ap.parse_args()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    poster_gov = _require_abs(args.poster_governance_root, "--poster-governance-root")
    ocr_plan = _require_abs(args.poster_region_ocr_plan_root, "--poster-region-ocr-plan-root")
    visual = _require_abs(args.poster_visual_symbol_evidence_root, "--poster-visual-symbol-evidence-root")
    metrics = _require_abs(args.metrics_collector_root, "--metrics-collector-root")
    sim = _require_abs(args.simulation_lab_harness_root, "--simulation-lab-harness-root")

    if args.bootstrap_inputs:
        _bootstrap_inputs(ws, poster_gov, ocr_plan, visual, metrics)

    from capabilities.midplatform.cross_modal_poster_ocr_reference_only_v0 import (
        run_cross_modal_poster_ocr_reference_only_v0,
    )

    summary, candidate, text_mx, visual_mx, align, risk, gate, metrics_binding, chain, sim_report, audit, errs = (
        run_cross_modal_poster_ocr_reference_only_v0(
            poster_governance_root=str(poster_gov),
            poster_region_ocr_plan_root=str(ocr_plan),
            poster_visual_symbol_evidence_root=str(visual),
            metrics_collector_root=str(metrics),
            simulation_lab_harness_root=str(sim),
        )
    )

    summary["output_root"] = str(out)
    summary["errors"] = list(errs)
    if errs:
        summary["phase_verdict_hint"] = "NO_GO"
    else:
        summary["phase_verdict_hint"] = "GO"

    out.mkdir(parents=True, exist_ok=True)
    _write_json(out / "cross_modal_poster_ocr_reference_only_summary.json", summary)
    _write_json(out / "cross_modal_poster_reference_candidate.json", candidate)
    _write_json(out / "cross_modal_poster_text_plan_reference_matrix.json", text_mx)
    _write_json(out / "cross_modal_poster_visual_symbol_reference_matrix.json", visual_mx)
    _write_json(out / "cross_modal_poster_cross_track_alignment_matrix.json", align)
    _write_json(out / "cross_modal_poster_reference_risk_report.json", risk)
    _write_json(out / "cross_modal_poster_reference_gate_policy.json", gate)
    _write_json(out / "cross_modal_poster_reference_metrics_binding_report.json", metrics_binding)
    _write_json(out / "cross_modal_poster_reference_source_chain_summary.json", chain)
    _write_json(out / "cross_modal_poster_reference_simulation_context_report.json", sim_report)
    _write_json(out / "cross_modal_poster_reference_only_audit_report.json", audit)

    (out / "cross_modal_poster_reference_only_notes.md").write_text(
        "\n".join(
            [
                "# CrossModal Poster OCR ReferenceOnly",
                "",
                f"- output_root: `{out}`",
                f"- poster_governance: `{poster_gov}`",
                f"- ocr_plan: `{ocr_plan}`",
                f"- visual_symbol: `{visual}`",
                f"- metrics_collector: `{metrics}`",
                f"- simulation_lab: `{sim}`",
                "",
                "Reference-only: text OCR plan and VisualSymbolEvidence in parallel; no fusion, no OCR, no QR, no brand.",
                "",
                f"phase_verdict_hint: {summary.get('phase_verdict_hint')}",
                f"errors: {errs}",
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
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if not errs else 2


if __name__ == "__main__":
    raise SystemExit(main())
