#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-CrossModal-Vision-OCR-Fusion-Candidate-DryRun-001 runner."""

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


def _notes_md(summary: dict, risk: dict, audit: dict) -> str:
    flags = risk.get("risk_flags") if isinstance(risk.get("risk_flags"), dict) else {}
    return "\n".join(
        [
            "# CrossModal Vision OCR Fusion Candidate DryRun — Notes",
            "",
            f"- Phase: {summary.get('phase')}",
            f"- Fusion candidates: {summary.get('fusion_candidate_count')}",
            f"- Non-empty text: {summary.get('non_empty_text_candidate_count')}",
            f"- Text-bearing root: `{summary.get('text_bearing_sample_root')}`",
            "",
            "## Boundary",
            "",
            "- Fusion candidate dry-run only; not fact; no-write.",
            f"- cross_modal_fusion_committed: {audit.get('cross_modal_fusion_committed')}",
            f"- rapidocr_invoked: {audit.get('rapidocr_invoked')}",
            f"- fusion_candidate_not_confirmed: {flags.get('fusion_candidate_not_confirmed')}",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--text-bearing-sample-root",
        default=str(WS_ROOT / "_eval_out/vision_roi_text_bearing_ocr_sample_smoke_v0"),
    )
    ap.add_argument(
        "--rapidocr-reference-only-root",
        default=str(WS_ROOT / "_eval_out/cross_modal_vision_ocr_reference_only_rapidocr_smoke_v0"),
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    tb_root = _require_abs(args.text_bearing_sample_root, "--text-bearing-sample-root")
    rr_root = _require_abs(args.rapidocr_reference_only_root, "--rapidocr-reference-only-root")

    from capabilities.midplatform.cross_modal_vision_ocr_fusion_candidate_dryrun_v0 import (
        run_cross_modal_vision_ocr_fusion_candidate_dryrun_v0,
    )

    summary, candidates_doc, matrix_doc, risk, chain, audit, errs = (
        run_cross_modal_vision_ocr_fusion_candidate_dryrun_v0(
            text_bearing_sample_root=str(tb_root),
            rapidocr_reference_only_root=str(rr_root),
        )
    )

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)

    _write_json(out / "cross_modal_vision_ocr_fusion_candidate_dryrun_summary.json", summary)
    _write_json(out / "cross_modal_vision_ocr_fusion_candidates.json", candidates_doc)
    _write_json(out / "cross_modal_vision_ocr_fusion_dryrun_matrix.json", matrix_doc)
    _write_json(out / "cross_modal_vision_ocr_fusion_risk_report.json", risk)
    _write_json(out / "cross_modal_vision_ocr_fusion_source_chain_summary.json", chain)
    _write_json(out / "cross_modal_vision_ocr_fusion_dryrun_audit_report.json", audit)
    (out / "cross_modal_vision_ocr_fusion_dryrun_notes.md").write_text(
        _notes_md(summary, risk, audit), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "fusion_candidate_count": summary.get("fusion_candidate_count"),
                "non_empty_text_candidate_count": summary.get("non_empty_text_candidate_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if int(summary.get("fusion_candidate_count") or 0) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
