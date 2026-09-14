#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-Evidence-Reference-Only-001 — reference-only alignment."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    candidates: list[Path] = []
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
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


def _notes_md(summary: dict, alignment: dict, audit: dict) -> str:
    return "\n".join(
        [
            "# CrossModal Vision OCR Reference Only — Notes",
            "",
            f"- Phase: {summary.get('phase')}",
            f"- Matched references: {summary.get('matched_reference_count')}",
            f"- Unmatched vision ROIs: {summary.get('unmatched_vision_roi_count')}",
            f"- Match strategy: {alignment.get('match_key_strategy')}",
            f"- reference_only: {alignment.get('reference_only')}",
            "",
            "## Boundary",
            "",
            "- Reference only; not fusion, not interpretation, no fact writes.",
            f"- cross_modal_fusion_invoked: {audit.get('cross_modal_fusion_invoked')}",
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
    ap.add_argument(
        "--vision-recognition-readonly-consumer-root",
        default=str(WS_ROOT / "_eval_out/vision_recognition_evidence_readonly_consumer_smoke_v0"),
    )
    ap.add_argument(
        "--vision-triggered-ocr-readonly-consumer-root",
        default=str(WS_ROOT / "_eval_out/vision_triggered_ocr_evidence_readonly_consumer_smoke_v0"),
    )
    ap.add_argument(
        "--vision-roi-to-ocr-bridge-root",
        default=str(WS_ROOT / "_eval_out/vision_roi_to_ocr_request_bridge_smoke_v0"),
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    from capabilities.midplatform.cross_modal_vision_ocr_reference_only_v0 import (
        run_cross_modal_vision_ocr_reference_only_v0,
    )

    summary, candidates_doc, matrix_doc, alignment, chain, audit, errs = run_cross_modal_vision_ocr_reference_only_v0(
        vision_roi_proposal_root=str(_require_abs(args.vision_roi_proposal_root, "--vision-roi-proposal-root")),
        vision_recognition_readonly_consumer_root=str(
            _require_abs(args.vision_recognition_readonly_consumer_root, "--vision-recognition-readonly-consumer-root")
        ),
        vision_triggered_ocr_readonly_consumer_root=str(
            _require_abs(args.vision_triggered_ocr_readonly_consumer_root, "--vision-triggered-ocr-readonly-consumer-root")
        ),
        vision_roi_to_ocr_bridge_root=str(_require_abs(args.vision_roi_to_ocr_bridge_root, "--vision-roi-to-ocr-bridge-root")),
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_vision_ocr_reference_only_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_reference_candidates.json", candidates_doc)
    _write_json(out / "cross_modal_vision_ocr_reference_matrix.json", matrix_doc)
    _write_json(out / "cross_modal_vision_ocr_alignment_summary.json", alignment)
    _write_json(out / "cross_modal_vision_ocr_source_chain_summary.json", chain)
    _write_json(out / "cross_modal_vision_ocr_reference_only_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_reference_only_notes.md").write_text(
        _notes_md(summary, alignment, audit), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "matched_reference_count": summary.get("matched_reference_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if int(summary.get("matched_reference_count") or 0) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
