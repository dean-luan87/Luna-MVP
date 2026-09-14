#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Owner Approval Request Module Handoff v1."""

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

from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_v1 import (
    DEFAULT_MODULE_GOVERNANCE_CLOSURE_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_owner_approval_request_module_handoff_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("owner_approval_request_module_handoff_report", "owner_approval_request_module_handoff_report_v1.json"),
    ("owner_approval_request_module_status_summary", "owner_approval_request_module_status_summary_v1.json"),
    (
        "owner_approval_request_midplatform_integration_position",
        "owner_approval_request_midplatform_integration_position_v1.json",
    ),
    ("owner_approval_request_handoff_boundary", "owner_approval_request_handoff_boundary_v1.json"),
    ("midplatform_mainline_return_plan", "midplatform_mainline_return_plan_v1.json"),
    ("future_test_strategy", "future_test_strategy_v1.json"),
    ("governance_debt_and_future_runtime_handoff", "governance_debt_and_future_runtime_handoff_v1.json"),
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
    parser.add_argument("--module-governance-closure-root", default=DEFAULT_MODULE_GOVERNANCE_CLOSURE_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_owner_approval_request_module_handoff_v1(
        module_governance_closure_root=args.module_governance_closure_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "owner_approval_request_module_handoff_report_v1.md").write_text(
        result["owner_approval_request_module_handoff_report_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "module_handoff_pass": summary.get("module_handoff_pass"),
                "current_module_state": summary.get("current_module_state"),
                "chain_not_extended": summary.get("owner_approval_request_chain_not_extended"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("module_handoff_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
