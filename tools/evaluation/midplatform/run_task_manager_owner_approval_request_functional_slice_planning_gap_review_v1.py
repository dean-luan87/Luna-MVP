#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run functional slice planning gap review v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.task_manager_owner_approval_request_functional_slice_planning_gap_review_items_v1 import DEFAULT_OUTPUT
from capabilities.midplatform.task_manager_owner_approval_request_functional_slice_planning_gap_review_v1 import (
    run_task_manager_owner_approval_request_functional_slice_planning_gap_review_v1,
)

OUTPUT_FILES = (
    ("task_manager_owner_approval_request_functional_slice_planning_gap_review_report", "task_manager_owner_approval_request_functional_slice_planning_gap_review_report_v1.json"),
    ("functional_slice_planning_gap_review", "functional_slice_planning_gap_review_v1.json"),
    ("authorization_preparation_dryrun_gap_review", "authorization_preparation_dryrun_gap_review_v1.json"),
    ("authorization_preparation_dryrun_artifact_visibility_review", "authorization_preparation_dryrun_artifact_visibility_review_v1.json"),
    ("authorization_preparation_dryrun_boundary_gap_review", "authorization_preparation_dryrun_boundary_gap_review_v1.json"),
    ("authorization_preparation_dryrun_precondition_review", "authorization_preparation_dryrun_precondition_review_v1.json"),
    ("functional_slice_planning_rerun_review", "functional_slice_planning_rerun_review_v1.json"),
    ("functional_slice_dryrun_rerun_readiness_review", "functional_slice_dryrun_rerun_readiness_review_v1.json"),
    ("first_unresolved_gap_review", "first_unresolved_gap_review_v1.json"),
    ("no_protocol_change_review", "no_protocol_change_review_v1.json"),
    ("owner_constraint_compliance_review", "owner_constraint_compliance_review_v1.json"),
    ("file_size_governance_review", "file_size_governance_review_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_owner_approval_request_functional_slice_planning_gap_review_v1(
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    out.mkdir(parents=True, exist_ok=True)
    for key, fname in OUTPUT_FILES:
        (out / fname).write_text(
            json.dumps(result[key], ensure_ascii=False, indent=2, default=_default) + "\n",
            encoding="utf-8",
        )
    (out / "task_manager_owner_approval_request_functional_slice_planning_gap_review_report_v1.md").write_text(
        result["task_manager_owner_approval_request_functional_slice_planning_gap_review_report_md"] + "\n",
        encoding="utf-8",
    )
    s = result["summary"]
    print(json.dumps({
        "output_root": str(out),
        "task_manager_owner_approval_request_functional_slice_planning_gap_review_pass": s.get("task_manager_owner_approval_request_functional_slice_planning_gap_review_pass"),
        "authorization_preparation_dryrun_go": s.get("authorization_preparation_dryrun_go"),
        "functional_slice_planning_go": s.get("functional_slice_planning_go"),
        "first_unresolved_authorization_preparation_gap": s.get("first_unresolved_authorization_preparation_gap"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
