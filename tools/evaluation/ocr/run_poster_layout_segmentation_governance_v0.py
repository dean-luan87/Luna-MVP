#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Poster-Layout-Segmentation-Governance-001 runner."""

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
    ap.add_argument("--v1-planning-root", default="")
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    v1_root = args.v1_planning_root.strip() or None
    if v1_root:
        v1_root = str(_require_abs(v1_root, "--v1-planning-root"))

    from capabilities.ocr_runtime.poster_layout_segmentation_governance_v0 import (
        run_poster_layout_segmentation_governance_v0,
    )

    (
        summary,
        manifest,
        layout,
        text_regions,
        non_text,
        visual,
        ocr_plan,
        reading,
        risks,
        gate_report,
        audit,
        errs,
    ) = run_poster_layout_segmentation_governance_v0(
        v1_planning_root=v1_root,
        work_dir=out / "_work",
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)
    phase_verdict = "GO" if not errs else "CONDITIONAL_GO"
    summary["phase_verdict_hint"] = phase_verdict

    _write_json(out / "poster_layout_governance_summary.json", summary)
    _write_json(out / "poster_synthetic_fixture_manifest.json", manifest)
    _write_json(out / "poster_layout_candidate.json", layout)
    _write_json(out / "poster_text_region_candidates.json", text_regions)
    _write_json(out / "poster_non_text_region_candidates.json", non_text)
    _write_json(out / "poster_visual_symbol_candidates.json", visual)
    _write_json(out / "poster_ocr_region_plan.json", ocr_plan)
    _write_json(out / "poster_reading_order_candidate.json", reading)
    _write_json(out / "poster_layout_risk_report.json", risks)
    _write_json(out / "poster_layout_gate_policy_report.json", gate_report)
    _write_json(out / "poster_layout_governance_audit_report.json", audit)

    notes = [
        "# Poster Layout Segmentation Governance",
        "",
        "Governance-only stub — no OCR, no Vision provider, no VLM.",
        "",
        f"source_image_ref: {summary.get('source_image_ref')}",
        f"full_image_ocr_allowed: {summary.get('full_image_ocr_allowed')}",
        f"ocr_strategy: {summary.get('ocr_strategy')}",
        "",
    ]
    if v1_root:
        notes.append(f"v1_planning_root: {v1_root}")
    (out / "poster_layout_governance_notes.md").write_text("\n".join(notes), encoding="utf-8")

    print(
        json.dumps(
            {
                "output_root": str(out),
                "phase_verdict_hint": phase_verdict,
                "full_image_ocr_allowed": summary.get("full_image_ocr_allowed"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if phase_verdict in ("GO", "CONDITIONAL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
