#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-004 — Verifier for OCR input image quality gate v0.

Evaluation Tools only. Does NOT invoke OCR providers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _nonempty(path: Path) -> bool:
    try:
        return path.is_file() and bool(path.read_text(encoding="utf-8").strip())
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--expected-count", type=int, default=0, help="0 = skip count check")
    args = ap.parse_args()

    outp = Path(args.output_root).expanduser()
    if not outp.is_absolute():
        raise SystemExit("ERROR: --output-root must be absolute")
    out_root = outp.resolve()
    if not out_root.is_dir():
        raise SystemExit(f"NO_GO: output_root_missing:{out_root}")

    blockers: List[str] = []
    required = [
        "ocr_input_quality_summary.json",
        "ocr_input_quality_image_matrix.jsonl",
        "ocr_input_quality_gate_counts.json",
        "ocr_input_quality_notes.md",
    ]
    for fn in required:
        p = out_root / fn
        if fn.endswith((".jsonl", ".md")):
            if not _nonempty(p):
                blockers.append(f"missing_or_empty:{fn}")
        else:
            if not p.is_file():
                blockers.append(f"missing:{fn}")

    if not blockers:
        summ: Dict[str, Any] = _read_json(out_root / "ocr_input_quality_summary.json")
        ha = (summ.get("hard_audit") or {}) if isinstance(summ, dict) else {}
        for k in ("ocr_provider_invoked", "runtime_integration", "whitebox_integration", "mainline_side_effect"):
            if ha.get(k) is not False:
                blockers.append(f"boundary_violation:{k}")
        # count check
        if int(args.expected_count) > 0:
            if int(summ.get("count") or -1) != int(args.expected_count):
                blockers.append(f"count_mismatch expected={args.expected_count} actual={summ.get('count')}")

    verdict = "GO" if not blockers else "NO_GO"
    report = {"phase": "Phase-EvaluationTools-OCR-004", "verdict": verdict, "blockers": blockers, "output_root": str(out_root)}
    (out_root / "ocr_input_quality_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

