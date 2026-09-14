#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Readiness-001 — Aggregate verifier (outputs + docs + manifest; no inference).
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

from tools.evaluation.ocr.verify_paddleocr_model_manifest_v0 import (  # noqa: E402
    validate_paddleocr_evaluation_readiness_manifest_v0,
)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--readiness-root", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).expanduser().resolve()
    root = Path(args.readiness_root).expanduser().resolve()
    blockers: List[str] = []

    required = [
        "paddleocr_readiness_summary.json",
        "paddleocr_dependency_matrix.json",
        "paddleocr_import_probe_report.json",
        "paddleocr_runtime_environment_report.json",
        "paddleocr_readiness_notes.md",
    ]
    for fn in required:
        if not (root / fn).is_file():
            blockers.append(f"A_missing:{fn}")

    man_path = repo / "configs" / "models" / "ocr" / "paddleocr_evaluation_readiness_manifest_v0.json"
    if not man_path.is_file():
        blockers.append("D_manifest_missing_repo")
    else:
        mv = validate_paddleocr_evaluation_readiness_manifest_v0(_read_json(man_path))
        if mv.get("verdict") != "GO":
            blockers.append(f"D_manifest_invalid:{mv.get('blockers')}")

    doc_dir = repo / "docs" / "architecture" / "evaluation"
    for name in (
        "LUNA_EVALUATION_OCR_PADDLEOCR_READINESS_V0.md",
        "LUNA_EVALUATION_OCR_PADDLEOCR_MODEL_MANIFEST_V0.md",
        "LUNA_EVALUATION_OCR_PADDLEOCR_ADAPTER_CONTRACT_V0.md",
        "LUNA_EVALUATION_OCR_PADDLEOCR_VS_RAPIDOCR_AB_PLAN_V0.md",
        "LUNA_EVALUATION_OCR_PADDLEOCR_READINESS_GO_NO_GO_PACK_V0.md",
    ):
        if not (doc_dir / name).is_file():
            blockers.append(f"doc_missing:{name}")

    summ_path = root / "paddleocr_readiness_summary.json"
    if summ_path.is_file():
        sm = _read_json(summ_path)
        c = sm.get("constraints") or {}
        for k in (
            "paddleocr_inference_invoked",
            "paddleocr_constructor_invoked",
            "ocr_provider_trial_executed",
            "rapidocr_replaced",
            "mainline_routing_changed",
            "runtime_integration",
            "whitebox_integration",
            "mainline_side_effect",
            "midplatform_invoked",
        ):
            if c.get(k) is not False:
                blockers.append(f"I_constraint:{k}")

    if man_path.is_file():
        mdoc = _read_json(man_path)
        if mdoc.get("runtime_default_enabled") is not False:
            blockers.append("G_runtime_default")
        if mdoc.get("mainline_provider") is not False:
            blockers.append("H_mainline_provider")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "phase": "Phase-PaddleOCR-Readiness-001",
        "verdict": verdict,
        "blockers": blockers,
        "readiness_root": str(root),
        "repo_root": str(repo),
    }
    (root / "paddleocr_readiness_aggregate_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
