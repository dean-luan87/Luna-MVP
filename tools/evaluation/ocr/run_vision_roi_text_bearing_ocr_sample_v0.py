#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-ROI-Text-Bearing-Sample-For-OCR-001 runner."""

from __future__ import annotations

import argparse
import json
import os
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


def _apply_rapidocr_env() -> None:
    os.environ["LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_REAL_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_STUB_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0"] = "false"
    os.environ["LUNA_OCR_SUBMISSION_EVAL_ONLY"] = "true"
    os.environ.setdefault("LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX", "512")


def _prepare_governance(ws: Path, out: Path, gov_arg: str) -> Path:
    gov_src = (
        Path(gov_arg).expanduser()
        if gov_arg.strip()
        else (ws / "configs/ocr/ocr_image_input_governance_lightweight_normalized_smoke_v0.example.json")
    )
    if not gov_src.is_absolute():
        gov_src = (ws / gov_src).resolve()
    gov = out / "vision_roi_text_bearing_ocr_sample_governance.json"
    if gov_src.is_file():
        gov.write_text(gov_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        fallback = ws / "configs/ocr/ocr_image_input_governance_v0.example.json"
        gov.write_text(fallback.read_text(encoding="utf-8"), encoding="utf-8")
    return _require_abs(str(gov), "governance under output-root")


def _notes_md(summary: dict, audit: dict, sample: dict) -> str:
    return "\n".join(
        [
            "# Vision ROI Text-Bearing OCR Sample — Notes",
            "",
            f"- Phase: {summary.get('phase')}",
            f"- Sample work root: `{summary.get('text_bearing_sample_path')}`",
            f"- Image: `{sample.get('image_ref')}`",
            f"- Expected hint: {sample.get('expected_text_hint')}",
            f"- text_joined: `{summary.get('text_joined')}`",
            f"- empty_text: {summary.get('empty_text')}",
            f"- phase_verdict_hint: {summary.get('phase_verdict_hint')}",
            "",
            "## Boundary",
            "",
            "- Text-bearing local fixture only; network_request_invoked=false.",
            "- OCR via ocr_mainline_bridge only.",
            f"- direct_rapidocr_invoked: {audit.get('direct_rapidocr_invoked')}",
            f"- cross_modal_fusion_invoked: {audit.get('cross_modal_fusion_invoked')}",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--governance-config", default="")
    args = ap.parse_args()

    _apply_rapidocr_env()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)
    gov = _prepare_governance(ws, out, args.governance_config)
    work = out / "_sample_work"

    from capabilities.ocr_runtime.vision_roi_text_bearing_ocr_sample_v0 import (
        run_vision_roi_text_bearing_ocr_sample_v0,
    )

    summary, sample_report, ocr_candidate, submission, consumer, reference, audit, errs = (
        run_vision_roi_text_bearing_ocr_sample_v0(
            workspace_root=ws,
            governance_config_path=gov,
            sample_work_root=work,
        )
    )

    text_joined = str(submission.get("evidence_text_joined") or submission.get("text_joined") or "")
    submission_out = dict(submission)
    submission_out["text_joined"] = text_joined

    summary["output_root"] = str(out.resolve())
    summary["errors"] = list(errs)
    summary["text_joined"] = text_joined
    summary["empty_text"] = not text_joined.strip()

    _write_json(out / "vision_roi_text_bearing_ocr_sample_summary.json", summary)
    _write_json(out / "vision_roi_text_bearing_sample_report.json", sample_report)
    _write_json(out / "vision_roi_text_bearing_ocr_request_candidate.json", ocr_candidate)
    _write_json(out / "vision_roi_text_bearing_rapidocr_submission_result.json", submission_out)
    _write_json(out / "vision_roi_text_bearing_rapidocr_consumer_view.json", consumer)
    _write_json(out / "vision_roi_text_bearing_cross_modal_reference_candidate.json", reference)
    _write_json(out / "vision_roi_text_bearing_ocr_sample_audit_report.json", audit)
    (out / "vision_roi_text_bearing_ocr_sample_notes.md").write_text(
        _notes_md(summary, audit, sample_report), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "text_joined": text_joined,
                "empty_text": summary.get("empty_text"),
                "rapidocr_invoked": submission.get("rapidocr_invoked"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
