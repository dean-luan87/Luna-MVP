#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Triggered-OCR-RapidOCR-ReadOnly-Consumer-001."""

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


def _notes_md(summary: dict, view: dict, comparison: dict, audit: dict) -> str:
    return "\n".join(
        [
            "# Vision-triggered RapidOCR Evidence ReadOnly Consumer — Notes",
            "",
            f"- Phase: {summary.get('phase')}",
            f"- RapidOCR submission root: `{summary.get('rapidocr_submission_from_vision_roi_root')}`",
            f"- Success: {summary.get('success_count')} / empty_text: {summary.get('empty_text_count')}",
            f"- Provider: {view.get('provider')} ({view.get('provider_level')})",
            f"- Comparison: {comparison}",
            "",
            "## Boundary",
            "",
            "- Read-only; empty text = valid real provider result, not failure.",
            f"- rapidocr_invoked_upstream: {audit.get('rapidocr_invoked_upstream')}",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--rapidocr-submission-from-vision-roi-root",
        default=str(WS_ROOT / "_eval_out/rapidocr_submission_from_vision_roi_smoke_v0"),
    )
    ap.add_argument(
        "--stub-ocr-consumer-root",
        default=str(WS_ROOT / "_eval_out/vision_triggered_ocr_evidence_readonly_consumer_smoke_v0"),
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    rapid_root = _require_abs(args.rapidocr_submission_from_vision_roi_root, "--rapidocr-submission-from-vision-roi-root")
    stub_root = _require_abs(args.stub_ocr_consumer_root, "--stub-ocr-consumer-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.ocr_runtime.vision_triggered_rapidocr_evidence_readonly_consumer_v0 import (
        run_vision_triggered_rapidocr_evidence_readonly_consume_v0,
    )

    summary, view, matrix, comparison, chain, audit, errs = run_vision_triggered_rapidocr_evidence_readonly_consume_v0(
        rapidocr_submission_from_vision_roi_root=str(rapid_root),
        stub_ocr_consumer_root=str(stub_root),
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "vision_triggered_rapidocr_evidence_readonly_consumer_summary.json", summary)
    _write_json(out / "vision_triggered_rapidocr_evidence_readonly_consumer_view.json", view)
    _write_json(out / "vision_triggered_rapidocr_evidence_matrix.json", matrix)
    _write_json(out / "vision_triggered_rapidocr_provider_comparison_summary.json", comparison)
    _write_json(out / "vision_triggered_rapidocr_source_chain_summary.json", chain)
    _write_json(out / "vision_triggered_rapidocr_evidence_readonly_consumer_audit_report.json", audit)
    (out / "vision_triggered_rapidocr_evidence_readonly_consumer_notes.md").write_text(
        _notes_md(summary, view, comparison, audit), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "success_count": summary.get("success_count"),
                "empty_text_count": summary.get("empty_text_count"),
                "rapidocr_success_count": summary.get("rapidocr_success_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if int(summary.get("success_count") or 0) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
