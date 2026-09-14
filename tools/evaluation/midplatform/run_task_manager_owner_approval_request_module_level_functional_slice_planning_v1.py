#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Owner Approval Request Module-Level Functional Slice Planning v1."""

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

from capabilities.midplatform.task_manager_owner_approval_request_module_level_functional_slice_planning_v1 import (
    DEFAULT_AUTHORIZATION_PREPARATION_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_owner_approval_request_module_level_functional_slice_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("module_level_functional_slice_plan", "module_level_functional_slice_plan_v1.json"),
    ("functional_slice_registry", "functional_slice_registry_v1.json"),
    ("owner_approval_request_candidate_lifecycle_slice", "owner_approval_request_candidate_lifecycle_slice_v1.json"),
    ("authorization_preparation_lifecycle_slice", "authorization_preparation_lifecycle_slice_v1.json"),
    (
        "record_approval_ack_evidence_closure_lifecycle_slice",
        "record_approval_ack_evidence_closure_lifecycle_slice_v1.json",
    ),
    ("absence_and_rollback_safety_lifecycle_slice", "absence_and_rollback_safety_lifecycle_slice_v1.json"),
    ("result_first_module_engineering_rule_reference", "result_first_module_engineering_rule_reference_v1.json"),
    ("functional_slice_next_phase_readiness", "functional_slice_next_phase_readiness_v1.json"),
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
    parser.add_argument("--authorization-preparation-dryrun-root", default=DEFAULT_AUTHORIZATION_PREPARATION_DRYRUN_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_owner_approval_request_module_level_functional_slice_planning_v1(
        authorization_preparation_dryrun_root=args.authorization_preparation_dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "module_level_functional_slice_plan_v1.md").write_text(
        result["module_level_functional_slice_plan_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "functional_slice_planning_pass": summary.get("functional_slice_planning_pass"),
                "functional_slice_plan_complete": summary.get("functional_slice_plan_complete"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("functional_slice_planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
