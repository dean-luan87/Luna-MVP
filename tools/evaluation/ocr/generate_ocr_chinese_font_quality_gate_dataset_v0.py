#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-002 — Generate Chinese font quality gate dataset v0.

Evaluation Tools only. Does NOT invoke OCR providers.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_chinese_font_quality_gate_dataset_generator_v0 import (  # noqa: E402
    generate_ocr_chinese_font_quality_gate_dataset_v0,
)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--font-validation-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--count", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    font_root = _require_abs(args.font_validation_root, "--font-validation-root")
    out_root = _require_abs(args.output_root, "--output-root")
    summary_path = font_root / "font_validation_summary.json"
    if not summary_path.is_file():
        raise SystemExit(f"ERROR: missing font_validation_summary.json at: {summary_path}")

    font_validation = _read_json(summary_path)
    res: Dict[str, Any] = generate_ocr_chinese_font_quality_gate_dataset_v0(
        output_root=out_root, seed=int(args.seed), count=int(args.count), font_validation=font_validation
    )
    print(json.dumps(res, ensure_ascii=False))
    return 0 if res.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())

