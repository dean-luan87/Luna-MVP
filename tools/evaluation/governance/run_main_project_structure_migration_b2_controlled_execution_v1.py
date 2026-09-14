#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration B2 Controlled Execution v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_b2_controlled_execution_v1 import (
    run_main_project_structure_migration_b2_controlled_execution_v1,
)

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_b2_controlled_execution_v1_smoke_v0"
DEFAULT_PREFLIGHT_ROOT = REPO_ROOT / "_eval_out" / "main_project_structure_migration_b2_preflight_via_harness_v1_smoke_v0"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("b2_before_manifest", "b2_before_manifest_v1.json"),
    ("b2_execution_result", "b2_execution_result_v1.json"),
    ("b2_after_manifest", "b2_after_manifest_v1.json"),
    ("b2_migration_refactor_opportunity_scan", "b2_migration_refactor_opportunity_scan_v1.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    p.add_argument("--b2-preflight-via-harness-root", default=str(DEFAULT_PREFLIGHT_ROOT))
    p.add_argument("--repo-root", default=str(REPO_ROOT))
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run_main_project_structure_migration_b2_controlled_execution_v1(
        b2_preflight_via_harness_root=args.b2_preflight_via_harness_root,
        repo_root=args.repo_root,
    )
    out_root = Path(args.output_root)
    for key, filename in OUTPUT_FILES:
        _write_json(out_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "phase": summary.get("phase"),
                "boundary_ok": summary.get("boundary_ok"),
                "candidate_path_count": summary.get("candidate_path_count"),
                "operations_unchanged": summary.get("operations_unchanged"),
                "b2_execution_completed_now": summary.get("b2_execution_completed_now"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
