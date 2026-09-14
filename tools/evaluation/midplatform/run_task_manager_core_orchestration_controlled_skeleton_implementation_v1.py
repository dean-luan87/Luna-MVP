#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Core Orchestration Controlled Skeleton Implementation v1."""

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

from capabilities.midplatform.task_manager_core_orchestration_controlled_skeleton_implementation_v1 import (
    DEFAULT_IMPLEMENTATION_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_core_orchestration_controlled_skeleton_implementation_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("controlled_skeleton_implementation_report", "controlled_skeleton_implementation_report_v1.json"),
    ("implemented_files_inventory", "implemented_files_inventory_v1.json"),
    ("implemented_types_summary", "implemented_types_summary_v1.json"),
    ("implemented_contracts_summary", "implemented_contracts_summary_v1.json"),
    ("implemented_builders_summary", "implemented_builders_summary_v1.json"),
    ("implemented_validators_summary", "implemented_validators_summary_v1.json"),
    ("implemented_skeleton_summary", "implemented_skeleton_summary_v1.json"),
    ("non_execution_guard_validation", "non_execution_guard_validation_v1.json"),
    ("controlled_skeleton_smoke_result", "controlled_skeleton_smoke_result_v1.json"),
    ("strong_coupled_single_package_review", "strong_coupled_single_package_review_v1.json"),
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
    parser.add_argument("--implementation-planning-root", default=DEFAULT_IMPLEMENTATION_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_core_orchestration_controlled_skeleton_implementation_v1(
        implementation_planning_root=args.implementation_planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "controlled_skeleton_implementation_report_v1.md").write_text(
        result["controlled_skeleton_implementation_report_md"] + "\n", encoding="utf-8",
    )
    summary = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "orchestration_controlled_skeleton_implementation_pass": summary.get("orchestration_controlled_skeleton_implementation_pass"),
        "controlled_skeleton_smoke_ok": summary.get("controlled_skeleton_smoke_ok"),
        "strong_coupled_single_package_ok": summary.get("strong_coupled_single_package_ok"),
        "selected_next_route": summary.get("selected_next_route"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
