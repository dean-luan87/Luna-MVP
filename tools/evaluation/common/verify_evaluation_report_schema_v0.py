#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-Foundation-001 — Verify EvaluationReport schema v0.

Evaluation Tools only. Does NOT run any providers.
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

from capabilities.evaluation.common.evaluation_report_schema_v0 import (  # noqa: E402
    validate_evaluation_report_schema_v0,
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
    ap.add_argument("--report-json", required=True)
    args = ap.parse_args()

    report_path = _require_abs(args.report_json, "--report-json")
    if not report_path.is_file():
        raise SystemExit(f"NO_GO: report_missing:{report_path}")

    report: Dict[str, Any] = _read_json(report_path)
    res = validate_evaluation_report_schema_v0(report)
    verdict = "GO" if res.get("ok") else "NO_GO"
    out = {"verdict": verdict, "blockers": res.get("blockers") or [], "report_path": str(report_path)}
    print(json.dumps(out, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

