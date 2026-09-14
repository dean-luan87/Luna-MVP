#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-Foundation-001 — Verifier for Evaluation Tools foundation v0.

Verifies outputs of run_evaluation_tools_foundation_check_v0.py and checks for boundary flags.
Does NOT invoke any providers.
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


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.output_root, "--output-root")
    blockers: List[str] = []
    if not root.is_dir():
        raise SystemExit(f"NO_GO: output_root_missing:{root}")

    required = [
        "evaluation_tools_foundation_summary.json",
        "evaluation_tools_directory_matrix.json",
        "evaluation_tools_boundary_check.json",
        "ocr_evaluation_framework_matrix.json",
        "evaluation_report_schema_check.json",
        "reserved_extension_matrix.json",
        "foundation_notes.md",
    ]
    for name in required:
        if not (root / name).exists():
            blockers.append(f"missing:{name}")

    if not blockers:
        summary: Dict[str, Any] = _read_json(root / "evaluation_tools_foundation_summary.json")
        b = summary.get("boundary_check") or {}
        for k in ("runtime_integration", "whitebox_integration", "mainline_side_effect"):
            if b.get(k) is not False:
                blockers.append(f"boundary_violation:{k}")
        schema = summary.get("evaluation_report_schema_check") or {}
        if schema.get("ok") is not True:
            blockers.append("schema_check_failed")

        dm = summary.get("directory_matrix") or {}
        if isinstance(dm, dict):
            for k, v in dm.items():
                if isinstance(v, dict) and v.get("exists") is not True:
                    blockers.append(f"dir_missing:{k}")

        docs = summary.get("docs_matrix") or {}
        if isinstance(docs, dict):
            for k, v in docs.items():
                if isinstance(v, dict) and v.get("exists") is not True:
                    blockers.append(f"doc_missing:{k}")

    verdict = "GO" if not blockers else "NO_GO"
    report = {"phase": "Phase-EvaluationTools-Foundation-001", "verdict": verdict, "blockers": blockers, "output_root": str(root)}
    (root / "foundation_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

