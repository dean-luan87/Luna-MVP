#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Owner Approval Request Authorization Preparation DryRun v1."""

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

from capabilities.midplatform.task_manager_owner_approval_request_authorization_preparation_dryrun_v1 import (
    DEFAULT_INTEGRATED_IMPLEMENTATION_ROOT,
    DEFAULT_OUTPUT,
    run_task_manager_owner_approval_request_authorization_preparation_dryrun_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("authorization_preparation_dryrun_report", "authorization_preparation_dryrun_report_v1.json"),
    ("authorization_preparation_package_validation", "authorization_preparation_package_validation_v1.json"),
    ("authorization_precondition_validation", "authorization_precondition_validation_v1.json"),
    ("missing_conditions_routing_validation", "missing_conditions_routing_validation_v1.json"),
    ("real_issuance_safety_boundary_validation", "real_issuance_safety_boundary_validation_v1.json"),
    ("functional_slice_followup_reference", "functional_slice_followup_reference_v1.json"),
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
    parser.add_argument("--integrated-implementation-root", default=DEFAULT_INTEGRATED_IMPLEMENTATION_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_task_manager_owner_approval_request_authorization_preparation_dryrun_v1(
        integrated_implementation_root=args.integrated_implementation_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write_json(out / fname, result[key])
    (out / "authorization_preparation_dryrun_report_v1.md").write_text(
        result["authorization_preparation_dryrun_report_md"] + "\n",
        encoding="utf-8",
    )
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "authorization_preparation_dryrun_pass": summary.get("authorization_preparation_dryrun_pass"),
                "package_validation_ok": summary.get("authorization_preparation_package_validation_ok"),
                "safety_boundary_ok": summary.get("real_issuance_safety_boundary_ok"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("authorization_preparation_dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
