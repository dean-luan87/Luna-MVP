#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-002 — Verifier for Chinese font cross validation v0.

Checks existence of expected cross-validation artifacts and critical fields.
Evaluation Tools only. Does NOT invoke OCR providers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _must_exist(p: Path, name: str, blockers: List[str]) -> None:
    if not p.exists():
        blockers.append(f"missing:{name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cross-validation-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.cross_validation_root, "--cross-validation-root")
    blockers: List[str] = []
    if not root.is_dir():
        raise SystemExit(f"NO_GO: cross_validation_root_missing:{root}")

    paths = {
        "summary": root / "chinese_font_cross_validation_summary.json",
        "glyph": root / "glyph_diversity_cross_check.json",
        "tofu": root / "tofu_shape_similarity_report.json",
        "rapidocr": root / "rapidocr_probe_cross_check.json",
        "contact_sheet": root / "human_review_contact_sheet.png",
        "human_index": root / "human_review_index.json",
        "trace": root / "cross_validation_trace.jsonl",
        "replay": root / "cross_validation_replay.jsonl",
        "notes": root / "cross_validation_notes.md",
    }
    for k, p in paths.items():
        _must_exist(p, k, blockers)

    # Field presence checks (best-effort)
    try:
        if paths["glyph"].is_file():
            g = json.loads(paths["glyph"].read_text(encoding="utf-8"))
            if "glyph_diversity_score" not in g:
                blockers.append("glyph_missing:glyph_diversity_score")
            if "tofu_suspected" not in g:
                blockers.append("glyph_missing:tofu_suspected")
    except Exception as e:
        blockers.append(f"glyph_parse_error:{e!r}")

    try:
        if paths["tofu"].is_file():
            t = json.loads(paths["tofu"].read_text(encoding="utf-8"))
            if "tofu_suspected_rate" not in t:
                blockers.append("tofu_missing:tofu_suspected_rate")
            if "result" not in t:
                blockers.append("tofu_missing:result")
    except Exception as e:
        blockers.append(f"tofu_parse_error:{e!r}")

    try:
        if paths["rapidocr"].is_file():
            r = json.loads(paths["rapidocr"].read_text(encoding="utf-8"))
            if "provider" not in r:
                blockers.append("rapidocr_missing:provider")
            if "result" not in r:
                blockers.append("rapidocr_missing:result")
    except Exception as e:
        blockers.append(f"rapidocr_parse_error:{e!r}")

    try:
        if paths["summary"].is_file():
            s = json.loads(paths["summary"].read_text(encoding="utf-8"))
            hard = s.get("hard_audit") or {}
            for k in ("runtime_integration", "whitebox_integration", "midplatform_invoked", "world_context_invoked"):
                if k not in hard:
                    blockers.append(f"summary_missing_hard_audit:{k}")
    except Exception as e:
        blockers.append(f"summary_parse_error:{e!r}")

    verdict = "GO" if not blockers else "NO_GO"
    report: Dict[str, Any] = {
        "phase": "Phase-EvaluationTools-OCR-002",
        "verifier": "verify_ocr_chinese_font_cross_validation_v0",
        "cross_validation_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "hard_boundary": {
            "runtime_integration": False,
            "whitebox_integration": False,
        },
    }
    (root / "cross_validation_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

