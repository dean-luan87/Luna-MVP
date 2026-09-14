#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-001 — Verify synthetic OCR dataset v0 (Evaluation Tools).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_synthetic_dataset_generator_v0 import (  # noqa: E402
    validate_synthetic_dataset_v0,
)


def _case(name: str, ok: bool, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--expected-count", type=int, default=200)
    args = ap.parse_args()

    outp = Path(args.output_root).expanduser()
    if not outp.is_absolute():
        raise SystemExit("ERROR: --output-root must be absolute")
    root = outp.resolve()

    results: List[Dict[str, Any]] = []
    results.append(_case("A_output_root_exists", root.is_dir(), {"output_root": str(root)}))
    results.append(_case("B_manifest_exists", (root / "manifest.jsonl").is_file(), {"path": str(root / "manifest.jsonl")}))
    results.append(_case("C_images_dir_exists", (root / "images").is_dir(), {"path": str(root / "images")}))
    results.append(_case("D_ground_truth_dir_exists", (root / "ground_truth").is_dir(), {"path": str(root / "ground_truth")}))

    val = validate_synthetic_dataset_v0(dataset_root=root, expected_count=int(args.expected_count))
    results.append(_case("E_dataset_validation_ok", bool(val.get("ok")), {"validation": val}))

    all_ok = all(r["ok"] for r in results)
    verdict = "GO" if all_ok else "NO_GO"
    print(json.dumps({"verifier": "verify_ocr_synthetic_trdg_dataset_v0", "verdict": verdict, "output_root": str(root), "hard_blockers": [r["case"] for r in results if not r["ok"]], "results": results}, ensure_ascii=False, indent=2))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

