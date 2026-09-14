#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Task Manager Controlled Skeleton Post-DryRun Review v1."""

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

from capabilities.midplatform.midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    DEFAULT_DECISION_CENTER_HANDOFF_ROOT,
    DEFAULT_DRYRUN_ROOT,
    DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT,
    DEFAULT_MOUNT_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    DEFAULT_PLANNING_ROOT,
    run_midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("skeleton_file_integrity_review", "skeleton_file_integrity_review_v1.json"),
    ("forbidden_runtime_import_review", "forbidden_runtime_import_review_v1.json"),
    ("pure_function_boundary_review", "pure_function_boundary_review_v1.json"),
    ("type_contract_review", "type_contract_review_v1.json"),
    ("function_contract_review", "function_contract_review_v1.json"),
    ("static_validator_review", "static_validator_review_v1.json"),
    ("sample_dryrun_output_review", "sample_dryrun_output_review_v1.json"),
    ("processing_chain_review", "processing_chain_review_v1.json"),
    ("governance_guard_review", "governance_guard_review_v1.json"),
    ("execution_guard_review", "execution_guard_review_v1.json"),
    ("health_watchdog_dependency_review", "health_watchdog_dependency_review_v1.json"),
    ("decision_center_dependency_review", "decision_center_dependency_review_v1.json"),
    ("downstream_readiness_review", "downstream_readiness_review_v1.json"),
    ("boundary_matrix_post_review", "boundary_matrix_post_review_v1.json"),
    ("post_dryrun_issue_register", "post_dryrun_issue_register_v1.json"),
    ("post_dryrun_readiness_decision", "post_dryrun_readiness_decision_v1.json"),
    ("summary", "summary.json"),
)


def _default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_default) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--dryrun-root", default=DEFAULT_DRYRUN_ROOT)
    parser.add_argument("--planning-root", default=DEFAULT_PLANNING_ROOT)
    parser.add_argument("--mount-dryrun-root", default=DEFAULT_MOUNT_DRYRUN_ROOT)
    parser.add_argument("--health-watchdog-handoff-root", default=DEFAULT_HEALTH_WATCHDOG_HANDOFF_ROOT)
    parser.add_argument("--decision-center-handoff-root", default=DEFAULT_DECISION_CENTER_HANDOFF_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run_midplatform_task_manager_controlled_skeleton_implementation_post_dryrun_review_v1(
        dryrun_root=args.dryrun_root,
        planning_root=args.planning_root,
        mount_dryrun_root=args.mount_dryrun_root,
        health_watchdog_handoff_root=args.health_watchdog_handoff_root,
        decision_center_handoff_root=args.decision_center_handoff_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "post_dryrun_review_pass": summary.get("post_dryrun_review_pass"),
                "blocker_count": summary.get("blocker_count"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("post_dryrun_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
