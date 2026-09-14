#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Broader Midplatform Closure Roadmap v1."""

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

from capabilities.midplatform.task_manager_broader_midplatform_closure_roadmap_v1 import (
    DEFAULT_MODULE_HANDOFF_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_broader_midplatform_closure_roadmap_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("broader_midplatform_closure_roadmap", "broader_midplatform_closure_roadmap_v1.json"),
    ("broader_midplatform_status_inventory", "broader_midplatform_status_inventory_v1.json"),
    ("midplatform_closure_gap_matrix", "midplatform_closure_gap_matrix_v1.json"),
    ("module_integration_map", "module_integration_map_v1.json"),
    ("mainline_closure_route_decision", "mainline_closure_route_decision_v1.json"),
    ("future_test_strategy_consolidation", "future_test_strategy_consolidation_v1.json"),
    ("do_not_reopen_rules", "do_not_reopen_rules_v1.json"),
    ("next_phase_recommendation", "next_phase_recommendation_v1.json"),
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
    parser.add_argument("--module-handoff-root", default=DEFAULT_MODULE_HANDOFF_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_broader_midplatform_closure_roadmap_v1(
        module_handoff_root=args.module_handoff_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "broader_midplatform_closure_roadmap_v1.md").write_text(
        result["broader_midplatform_closure_roadmap_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "broader_midplatform_closure_roadmap_pass": summary.get("broader_midplatform_closure_roadmap_pass"),
                "selected_route": summary.get("selected_route"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("broader_midplatform_closure_roadmap_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
