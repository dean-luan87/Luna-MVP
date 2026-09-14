#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Foundation Closure Consolidation v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_foundation_closure_consolidation_v1 import (
    DEFAULT_BROADER_ROADMAP_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_foundation_closure_consolidation_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("foundation_consolidation_report", "foundation_consolidation_report_v1.json"),
    ("foundation_consolidation_scope", "foundation_consolidation_scope_v1.json"),
    ("foundation_asset_inventory", "foundation_asset_inventory_v1.json"),
    ("foundation_consolidation_matrix", "foundation_consolidation_matrix_v1.json"),
    ("foundation_boundary_statement", "foundation_boundary_statement_v1.json"),
    ("remaining_work_register", "remaining_work_register_v1.json"),
    ("next_mainline_route", "next_mainline_route_v1.json"),
    ("do_not_misclassify_rules", "do_not_misclassify_rules_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--broader-midplatform-closure-roadmap-root", default=DEFAULT_BROADER_ROADMAP_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_foundation_closure_consolidation_v1(
        broader_midplatform_closure_roadmap_root=args.broader_midplatform_closure_roadmap_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "foundation_consolidation_report_v1.md").write_text(
        result["foundation_consolidation_report_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "foundation_consolidation_pass": summary.get("foundation_consolidation_pass"),
                "not_final_midplatform": summary.get("foundation_consolidation_not_final_midplatform_completion"),
                "remaining_work": summary.get("midplatform_still_has_remaining_work"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("foundation_consolidation_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
