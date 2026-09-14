#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Poster-VisualSymbolEvidence-Stub-001 runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "ocr_runtime").is_dir():
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
    ap.add_argument("--poster-governance-root", required=True)
    ap.add_argument("--poster-region-ocr-plan-root", required=True)
    ap.add_argument("--metrics-collector-root", required=True)
    ap.add_argument("--realvideo-registry-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.ocr_runtime.poster_visual_symbol_evidence_stub_v0 import run_poster_visual_symbol_evidence_stub_v0

    summary, schema_stub, items, matrix, exclusion, qr_logo, risks, metrics_binding, gate, audit, errs = (
        run_poster_visual_symbol_evidence_stub_v0(
            poster_governance_root=str(_require_abs(args.poster_governance_root, "--poster-governance-root")),
            poster_region_ocr_plan_root=str(_require_abs(args.poster_region_ocr_plan_root, "--poster-region-ocr-plan-root")),
            metrics_collector_root=str(_require_abs(args.metrics_collector_root, "--metrics-collector-root")),
            realvideo_registry_root=str(_require_abs(args.realvideo_registry_root, "--realvideo-registry-root")),
        )
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "poster_visual_symbol_evidence_stub_summary.json", summary)
    _write_json(out / "poster_visual_symbol_evidence_schema_stub.json", schema_stub)
    _write_json(out / "poster_visual_symbol_evidence_items.json", items)
    _write_json(out / "poster_visual_symbol_evidence_matrix.json", matrix)
    _write_json(out / "poster_visual_symbol_ocr_exclusion_link_report.json", exclusion)
    _write_json(out / "poster_visual_symbol_qr_logo_policy_report.json", qr_logo)
    _write_json(out / "poster_visual_symbol_risk_report.json", risks)
    _write_json(out / "poster_visual_symbol_metrics_binding_report.json", metrics_binding)
    _write_json(out / "poster_visual_symbol_gate_policy_report.json", gate)
    _write_json(out / "poster_visual_symbol_evidence_stub_audit_report.json", audit)

    (out / "poster_visual_symbol_evidence_stub_notes.md").write_text(
        "\n".join(
            [
                "# Poster VisualSymbolEvidence Stub",
                "",
                "Dual-track: text → OCR plan; visual → VisualSymbolEvidence (no OCR/QR decode/brand).",
                "",
                f"items: {items.get('item_count')}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "item_count": items.get("item_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("phase_verdict_hint") in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
