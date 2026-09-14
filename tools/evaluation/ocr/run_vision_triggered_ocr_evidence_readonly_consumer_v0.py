#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-OCR-Evidence-ReadOnly-Consumer-001 — read Vision-triggered OCR submission collection."""

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


def _notes_md(summary: dict, view: dict, audit: dict) -> str:
    tj = view.get("text_joined_summary") if isinstance(view.get("text_joined_summary"), dict) else {}
    return "\n".join(
        [
            "# Vision-triggered OCR Evidence ReadOnly Consumer — Notes",
            "",
            f"- Phase: {summary.get('phase')}",
            f"- Submission root: `{summary.get('ocr_submission_from_vision_roi_root')}`",
            f"- Submissions: {summary.get('submission_count')} / success: {summary.get('success_count')}",
            f"- Provider: {summary.get('provider')}",
            f"- Indexed: candidate={summary.get('candidate_index_count')} frame={summary.get('frame_index_count')} roi={summary.get('roi_index_count')}",
            f"- text_joined_summary: {tj}",
            "",
            "## Boundary",
            "",
            "- Read-only; no fusion, no interpretation, no fact writes.",
            f"- fusion_status: {view.get('fusion_status')}",
            f"- cross_modal_fusion_invoked: {audit.get('cross_modal_fusion_invoked')}",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--ocr-submission-from-vision-roi-root",
        default=str(WS_ROOT / "_eval_out/ocr_request_submission_from_vision_roi_smoke_v0"),
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    sub_root = _require_abs(args.ocr_submission_from_vision_roi_root, "--ocr-submission-from-vision-roi-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.ocr_runtime.vision_triggered_ocr_evidence_readonly_consumer_v0 import (
        run_vision_triggered_ocr_evidence_readonly_consume_v0,
    )

    summary, view, matrix, chain, audit, errs = run_vision_triggered_ocr_evidence_readonly_consume_v0(
        ocr_submission_from_vision_roi_root=str(sub_root),
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "vision_triggered_ocr_evidence_readonly_consumer_summary.json", summary)
    _write_json(out / "vision_triggered_ocr_evidence_readonly_consumer_view.json", view)
    _write_json(out / "vision_triggered_ocr_evidence_matrix.json", matrix)
    _write_json(out / "vision_triggered_ocr_source_chain_summary.json", chain)
    _write_json(out / "vision_triggered_ocr_evidence_readonly_consumer_audit_report.json", audit)
    (out / "vision_triggered_ocr_evidence_readonly_consumer_notes.md").write_text(
        _notes_md(summary, view, audit), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "success_count": summary.get("success_count"),
                "provider": summary.get("provider"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("success_count", 0) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
