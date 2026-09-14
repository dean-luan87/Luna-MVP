#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-ROI-to-OCR-Request-Bridge-001 — Vision ROI → OCRRequest candidate bridge."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    candidates: list[Path] = []
    for parent in here.parents:
        if (parent / "capabilities" / "vision_runtime").is_dir():
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


def _notes_md(summary: dict, audit: dict) -> str:
    return "\n".join(
        [
            "# Vision ROI → OCRRequest Bridge v0 — Notes",
            "",
            f"- Phase: {summary.get('phase')}",
            f"- Vision ROI proposal root: `{summary.get('vision_roi_proposal_root')}`",
            f"- ROI items total: {summary.get('roi_items_total')}",
            f"- OCR request candidates: {summary.get('candidate_count')}",
            f"- Rejections: {summary.get('rejection_count')}",
            f"- Phase verdict hint: {summary.get('phase_verdict_hint')}",
            "",
            "## Boundary",
            "",
            "- Bridge only: trigger + reference, no OCR invoke, no fusion, no fact writes.",
            f"- ocr_provider_invoked: {audit.get('ocr_provider_invoked')}",
            f"- ocr_runtime_invoked: {audit.get('ocr_runtime_invoked')}",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--vision-roi-proposal-root",
        default=str(WS_ROOT / "_eval_out/vision_roi_proposal_stub_smoke_v0"),
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    proposal_root = _require_abs(args.vision_roi_proposal_root, "--vision-roi-proposal-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.vision_runtime.vision_roi_to_ocr_request_bridge_v0 import (
        run_vision_roi_to_ocr_request_bridge_v0,
    )

    summary, candidates_doc, matrix_doc, rejection_doc, audit, errs = run_vision_roi_to_ocr_request_bridge_v0(
        vision_roi_proposal_root=str(proposal_root),
    )

    audit["ocr_request_candidates_generated"] = int(summary.get("candidate_count") or 0) > 0
    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "vision_roi_to_ocr_request_bridge_summary.json", summary)
    _write_json(out / "vision_roi_to_ocr_request_candidates.json", candidates_doc)
    _write_json(out / "vision_roi_to_ocr_request_candidate_matrix.json", matrix_doc)
    _write_json(out / "vision_roi_to_ocr_rejection_matrix.json", rejection_doc)
    _write_json(out / "vision_roi_to_ocr_request_bridge_audit_report.json", audit)
    (out / "vision_roi_to_ocr_request_bridge_notes.md").write_text(
        _notes_md(summary, audit), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "candidate_count": summary.get("candidate_count"),
                "rejection_count": summary.get("rejection_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if not errs else 1


if __name__ == "__main__":
    raise SystemExit(main())
