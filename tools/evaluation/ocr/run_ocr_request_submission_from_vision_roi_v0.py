#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-OCR-Request-Submission-Gated-Smoke-001 — submit Vision ROI OCRRequest candidates via mainline bridge."""

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


def _apply_submission_env() -> None:
    os.environ["LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_STUB_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_REAL_PROVIDER_V0"] = "false"
    os.environ["LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0"] = "false"
    os.environ["LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0"] = "false"
    os.environ["LUNA_OCR_SUBMISSION_EVAL_ONLY"] = "true"


def _notes_md(summary: dict, plan: dict, audit: dict) -> str:
    return "\n".join(
        [
            "# OCR Request Submission from Vision ROI — Notes",
            "",
            f"- Phase: {summary.get('phase')}",
            f"- Bridge root: `{summary.get('vision_roi_to_ocr_bridge_root')}`",
            f"- Candidates: {summary.get('candidate_count')} / selected: {summary.get('selected_candidate_count')}",
            f"- Submitted OK: {summary.get('success_count')} / failed: {summary.get('failed_count')}",
            f"- Mode: {plan.get('submission_mode')} / provider: {plan.get('ocr_provider_mode')}",
            "",
            "## Boundary",
            "",
            "- Submissions go only through `ocr_mainline_bridge_v0` (stub).",
            "- No MidPlatform / Scene Delta / WorldModel / fusion / navigation.",
            f"- ocr_mainline_bridge_invoked: {audit.get('ocr_mainline_bridge_invoked')}",
            f"- rapidocr_invoked: {audit.get('rapidocr_invoked')}",
            f"- paddleocr_invoked: {audit.get('paddleocr_invoked')}",
            "",
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default=str(WS_ROOT))
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--vision-roi-to-ocr-bridge-root",
        default=str(WS_ROOT / "_eval_out/vision_roi_to_ocr_request_bridge_smoke_v0"),
    )
    ap.add_argument(
        "--governance-config",
        default="",
        help="Defaults to configs/ocr/ocr_image_input_governance_v0.example.json",
    )
    args = ap.parse_args()

    _apply_submission_env()

    ws = _require_abs(args.workspace_root, "--workspace-root")
    out = _require_abs(args.output_root, "--output-root")
    bridge_root = _require_abs(args.vision_roi_to_ocr_bridge_root, "--vision-roi-to-ocr-bridge-root")
    out.mkdir(parents=True, exist_ok=True)

    gov = Path(args.governance_config).expanduser() if args.governance_config.strip() else (
        ws / "configs/ocr/ocr_image_input_governance_v0.example.json"
    )
    if not gov.is_absolute():
        gov = (ws / gov).resolve()
    gov = _require_abs(str(gov), "--governance-config")

    from capabilities.ocr_runtime.ocr_request_submission_from_vision_roi_v0 import (
        run_ocr_request_submission_from_vision_roi_v0,
    )

    summary, plan, matrix, collection, audit, errs = run_ocr_request_submission_from_vision_roi_v0(
        vision_roi_to_ocr_bridge_root=str(bridge_root),
        workspace_root=ws,
        governance_config_path=gov,
        submission_work_root=out / "_submission_work",
    )

    summary["output_root"] = str(out.resolve())

    _write_json(out / "ocr_request_submission_from_vision_roi_summary.json", summary)
    _write_json(out / "ocr_request_submission_plan_from_vision_roi.json", plan)
    _write_json(out / "ocr_request_submission_result_matrix.json", matrix)
    _write_json(out / "ocr_submission_from_vision_roi_collection.json", collection)
    _write_json(out / "ocr_request_submission_from_vision_roi_audit_report.json", audit)
    (out / "ocr_request_submission_from_vision_roi_notes.md").write_text(
        _notes_md(summary, plan, audit), encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "output_root": str(out),
                "success_count": summary.get("success_count"),
                "failed_count": summary.get("failed_count"),
                "phase_verdict_hint": summary.get("phase_verdict_hint"),
                "errors": errs,
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("success_count", 0) > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
