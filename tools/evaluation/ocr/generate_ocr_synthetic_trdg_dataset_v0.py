#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-001 — Generate synthetic OCR dataset v0 (Evaluation Tools).

Absolute paths only. Does NOT invoke OCR providers.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_synthetic_dataset_generator_v0 import (  # noqa: E402
    generate_ocr_synthetic_samples_v0,
)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


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
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--count", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--prefer-trdg", action="store_true", help="Prefer TRDG; fall back to Pillow if unavailable")
    args = ap.parse_args()

    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    summary = generate_ocr_synthetic_samples_v0(
        output_root=out_root,
        count=int(args.count),
        seed=int(args.seed),
        prefer_trdg=bool(args.prefer_trdg),
    )

    _write_json(out_root / "dataset_summary.json", summary)
    _write_json(
        out_root / "generation_config.json",
        {
            "phase": "Phase-EvaluationTools-OCR-001",
            "ts": _now_iso(),
            "output_root": str(out_root),
            "count": int(args.count),
            "seed": int(args.seed),
            "prefer_trdg": bool(args.prefer_trdg),
        },
    )
    notes = "\n".join(
        [
            "# OCR Synthetic Dataset (TRDG preferred) v0 — Evaluation Tools",
            "",
            f"- **output_root:** `{str(out_root)}`",
            f"- **count:** `{int(args.count)}`",
            f"- **seed:** `{int(args.seed)}`",
            f"- **prefer_trdg:** `{bool(args.prefer_trdg)}`",
            f"- **generator_used:** `{summary.get('generator_used')}`",
            "",
            "## Boundary",
            "",
            "- This is Evaluation Tools / Test Harness only.",
            "- No OCR provider invocation in generation.",
            "- No runtime/MidPlatform/semantic integration.",
            "",
        ]
    )
    (out_root / "generation_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "count": summary.get("count"), "generator_used": summary.get("generator_used")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

