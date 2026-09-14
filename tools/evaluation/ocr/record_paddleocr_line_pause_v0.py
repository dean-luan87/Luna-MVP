#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-LinePause-001 — Freeze PaddleOCR candidate line pause + resume criteria (no side effects).

No downloads, no PaddleOCR(), no OCR inference, no routing changes.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_line_pause_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    phase = "Phase-PaddleOCR-LinePause-001"
    ts = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    summary: Dict[str, Any] = {
        "phase": phase,
        "recorded_at": ts,
        "line_status": "paused",
        "pause_reason": "missing_det_rec_cls_weights",
        "blocked_by": "missing_det_rec_cls_weights",
        "frozen_facts": {
            "paddleocr_readiness_001": "GO",
            "paddleocr_weights_001": "CONDITIONAL_GO",
            "paddleocr_weights_002": "CONDITIONAL_GO",
            "missing_weight_file_count": 6,
            "download_authorized": False,
            "network_request_invoked": False,
            "files_downloaded": [],
            "rapidocr_mainline_provider": True,
            "paddleocr_role": "evaluation_candidate_only",
        },
        "constraints": {
            "weights_downloaded_in_this_phase": False,
            "paddleocr_constructor_invoked": False,
            "paddleocr_inference_invoked": False,
            "rapidocr_replaced": False,
            "ocr_routing_changed": False,
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
            "midplatform_invoked": False,
        },
        "verdict": "GO",
        "readiness_posture": "LINE_PAUSED_pending_weights_then_snapshot_GO",
    }

    resume: Dict[str, Any] = {
        "phase": phase,
        "resume_when_all_true": [
            "Six planned files exist under repo: det/rec/cls each has inference.pdmodel + inference.pdiparams per model_files_manifest.",
            "run_paddleocr_weights_snapshot_v0 reports missing_count=0 and verdict=GO.",
            "verify_paddleocr_weights_snapshot_v0 verdict=GO.",
            "paddleocr_pinned_model_manifest_candidate has non-empty sha256 for every planned file.",
            "pinned candidate keeps runtime_default_enabled=false and mainline_provider=false.",
        ],
        "do_not_enter_until": [
            "Phase-PaddleOCR-Controlled-Trial-001 until Weights-001 snapshot GO (missing_count=0, sha256 pinned).",
        ],
    }

    blockers: List[Dict[str, Any]] = [
        {
            "id": "missing_weights",
            "severity": "blocking_for_trial",
            "detail": "det/rec/cls inference.pdmodel and inference.pdiparams not present in repo (count=6 missing).",
        },
        {
            "id": "download_not_authorized",
            "severity": "informational",
            "detail": "No authorized acquisition executed; use Weights-002 copy-from or allow-download+URL manifest when user authorizes.",
        },
    ]

    next_action: Dict[str, Any] = {
        "phase": phase,
        "next_allowed": [
            "Local copy or authorized download via prepare_paddleocr_evaluation_weights_v0.py (Weights-002).",
            "Re-run run_paddleocr_weights_snapshot_v0.py then verify_paddleocr_weights_snapshot_v0.py until GO.",
        ],
        "next_forbidden_until_snapshot_go": [
            "Phase-PaddleOCR-Controlled-Trial-001",
            "OCR-ProviderAB-001 RapidOCR vs PaddleOCR comparative run using Paddle inference",
        ],
        "mainline_backlog": "Resume main Luna backlog; PaddleOCR remains frozen candidate line until weights pinned.",
    }

    _write_json(out / "paddleocr_line_pause_summary.json", summary)
    _write_json(out / "paddleocr_resume_criteria.json", resume)
    _write_json(out / "paddleocr_blocker_register.json", {"blockers": blockers})
    _write_json(out / "paddleocr_next_allowed_action.json", next_action)

    notes = out / "notes.md"
    notes.write_text(
        "\n".join(
            [
                "# PaddleOCR candidate line — pause record (LinePause-001)",
                "",
                f"- **recorded_at**: `{ts}`",
                "",
                "## Pause",
                "",
                "- **Reason**: `missing_det_rec_cls_weights` (6 planned files not on disk).",
                "- **RapidOCR**: remains current mainline lightweight OCR provider.",
                "- **PaddleOCR**: evaluation candidate only; **do not** start Controlled-Trial until Weights-001 snapshot is GO.",
                "",
                "## Resume",
                "",
                "See `paddleocr_resume_criteria.json` and `paddleocr_next_allowed_action.json`.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "verdict": summary["verdict"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
