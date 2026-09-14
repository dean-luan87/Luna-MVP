#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Recognition-Evidence-Pack-Stub-001 — stub results → Luna evidence pack."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WS_ROOT = Path(__file__).resolve().parents[3]
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
    ap.add_argument("--repo-root", default="")
    ap.add_argument(
        "--adapter-selection-root",
        required=True,
        help="Absolute path to vision_lightweight_recognition_adapter_selection smoke output.",
    )
    ap.add_argument("--output-root", required=True, help="Absolute path to write evidence pack artifacts.")
    args = ap.parse_args()

    adapter_root = _require_abs(args.adapter_selection_root, "--adapter-selection-root")
    out = _require_abs(args.output_root, "--output-root")

    for name in (
        "vision_provider_stub_result.json",
        "vision_recognition_candidate_matrix.json",
        "vision_provider_selection_report.json",
        "vision_recognition_adapter_selection_audit_report.json",
        "vision_recognition_adapter_selection_summary.json",
    ):
        p = adapter_root / name
        if not p.is_file():
            raise SystemExit(f"ERROR: missing adapter selection input: {p}")

    if args.repo_root.strip():
        repo = _require_abs(args.repo_root, "--repo-root")
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))

    from capabilities.vision_runtime.vision_recognition_evidence_pack_v0 import (
        build_vision_recognition_evidence_pack_from_adapter_selection_v0,
    )

    bundle = build_vision_recognition_evidence_pack_from_adapter_selection_v0(adapter_root)

    _write_json(out / "vision_recognition_evidence_pack_summary.json", bundle["summary"])
    _write_json(out / "vision_recognition_evidence_pack.json", bundle["evidence_pack"])
    _write_json(out / "vision_recognition_evidence_matrix.json", bundle["evidence_matrix"])
    _write_json(out / "vision_recognition_provider_summary.json", bundle["provider_summary"])
    _write_json(out / "vision_recognition_evidence_audit_report.json", bundle["audit"])

    notes = (
        "# Phase-Vision-Recognition-Evidence-Pack-Stub-001\n\n"
        "Luna **VisionRecognitionEvidencePack v0** from **vision_stub** outputs only. "
        "All items are **`synthetic` / `not_fact`** — not MidPlatform truth. "
        "**No** YOLO, Supervision mainline, VLM, OCR, AI interpretation, navigation, "
        "Scene Delta, or WorldModel writes.\n"
    )
    (out / "vision_recognition_evidence_pack_notes.md").write_text(notes, encoding="utf-8")

    print(
        json.dumps(
            {
                "vision_recognition_evidence_pack_root": str(out),
                "adapter_selection_root": str(adapter_root),
                "evidence_items_count": bundle["summary"].get("evidence_items_count"),
                "status": "success",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
