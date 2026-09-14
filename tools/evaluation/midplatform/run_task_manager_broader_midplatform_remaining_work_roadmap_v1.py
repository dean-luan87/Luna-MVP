#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Broader Midplatform Remaining Work Roadmap v1."""

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

from capabilities.midplatform.task_manager_broader_midplatform_remaining_work_roadmap_v1 import (
    DEFAULT_FOUNDATION_CONSOLIDATION_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_broader_midplatform_remaining_work_roadmap_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("broader_midplatform_remaining_work_roadmap", "broader_midplatform_remaining_work_roadmap_v1.json"),
    ("remaining_work_scope", "remaining_work_scope_v1.json"),
    ("remaining_work_inventory", "remaining_work_inventory_v1.json"),
    ("work_classification_matrix", "work_classification_matrix_v1.json"),
    ("mainline_priority_plan", "mainline_priority_plan_v1.json"),
    ("module_completion_candidates", "module_completion_candidates_v1.json"),
    ("governance_debt_positioning", "governance_debt_positioning_v1.json"),
    ("test_readiness_positioning", "test_readiness_positioning_v1.json"),
    ("next_route_decision", "next_route_decision_v1.json"),
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
    parser.add_argument("--foundation-consolidation-root", default=DEFAULT_FOUNDATION_CONSOLIDATION_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_broader_midplatform_remaining_work_roadmap_v1(
        foundation_consolidation_root=args.foundation_consolidation_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "broader_midplatform_remaining_work_roadmap_v1.md").write_text(
        result["broader_midplatform_remaining_work_roadmap_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "remaining_work_roadmap_pass": summary.get("remaining_work_roadmap_pass"),
                "midplatform_still_has_remaining_work": summary.get("midplatform_still_has_remaining_work"),
                "selected_route": summary.get("selected_route"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
