#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Owner Approval Request Functional Slice DryRun v1."""

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

from capabilities.midplatform.task_manager_owner_approval_request_functional_slice_dryrun_v1 import (
    DEFAULT_FUNCTIONAL_SLICE_PLANNING_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_owner_approval_request_functional_slice_dryrun_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("functional_slice_dryrun_report", "functional_slice_dryrun_report_v1.json"),
    ("functional_slice_dryrun_registry", "functional_slice_dryrun_registry_v1.json"),
    ("owner_approval_request_candidate_lifecycle_dryrun", "owner_approval_request_candidate_lifecycle_dryrun_v1.json"),
    ("authorization_preparation_lifecycle_dryrun", "authorization_preparation_lifecycle_dryrun_v1.json"),
    (
        "record_approval_ack_evidence_closure_lifecycle_dryrun",
        "record_approval_ack_evidence_closure_lifecycle_dryrun_v1.json",
    ),
    ("absence_and_rollback_safety_lifecycle_dryrun", "absence_and_rollback_safety_lifecycle_dryrun_v1.json"),
    ("functional_slice_result_summary", "functional_slice_result_summary_v1.json"),
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
    parser.add_argument("--functional-slice-planning-root", default=DEFAULT_FUNCTIONAL_SLICE_PLANNING_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_owner_approval_request_functional_slice_dryrun_v1(
        functional_slice_planning_root=args.functional_slice_planning_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "functional_slice_dryrun_report_v1.md").write_text(
        result["functional_slice_dryrun_report_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "functional_slice_dryrun_pass": summary.get("functional_slice_dryrun_pass"),
                "all_slice_primary_results_reached": summary.get("all_slice_primary_results_reached"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("functional_slice_dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
