#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Owner Approval Request Module Governance Closure v1."""

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

from capabilities.midplatform.task_manager_owner_approval_request_module_governance_closure_v1 import (
    DEFAULT_FUNCTIONAL_SLICE_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_owner_approval_request_module_governance_closure_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("module_governance_closure_report", "module_governance_closure_report_v1.json"),
    ("module_result_closure", "module_result_closure_v1.json"),
    ("functional_slice_closure_summary", "functional_slice_closure_summary_v1.json"),
    ("governance_rule_closure", "governance_rule_closure_v1.json"),
    ("non_execution_closure", "non_execution_closure_v1.json"),
    ("real_execution_preconditions", "real_execution_preconditions_v1.json"),
    ("module_closure_decision", "module_closure_decision_v1.json"),
    ("module_closure_handoff", "module_closure_handoff_v1.json"),
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
    parser.add_argument("--functional-slice-dryrun-root", default=DEFAULT_FUNCTIONAL_SLICE_DRYRUN_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_owner_approval_request_module_governance_closure_v1(
        functional_slice_dryrun_root=args.functional_slice_dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "module_governance_closure_report_v1.md").write_text(
        result["module_governance_closure_report_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "module_governance_closure_pass": summary.get("module_governance_closure_pass"),
                "current_module_state": summary.get("current_module_state"),
                "real_execution_state": summary.get("real_execution_state"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("module_governance_closure_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
