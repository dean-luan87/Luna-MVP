#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform EB/WM/Scheduler Controlled Skeleton Implementation DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_v1 import (
    run_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_v1,
)

DEFAULT_SK_PLAN = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning"
)
DEFAULT_EBWM_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_planning"
DEFAULT_EBWM_DR = REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_dryrun_and_review"
DEFAULT_OUTPUT = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("skeleton_implementation_scope_report", "skeleton_implementation_scope_report_v1.json"),
    ("skeleton_file_creation_report", "skeleton_file_creation_report_v1.json"),
    ("skeleton_type_contract_validation", "skeleton_type_contract_validation_v1.json"),
    ("event_bus_skeleton_static_validation", "event_bus_skeleton_static_validation_v1.json"),
    ("working_memory_skeleton_static_validation", "working_memory_skeleton_static_validation_v1.json"),
    ("scheduler_skeleton_static_validation", "scheduler_skeleton_static_validation_v1.json"),
    ("static_validator_review", "static_validator_review_v1.json"),
    ("skeleton_sample_dryrun", "skeleton_sample_dryrun_v1.json"),
    ("governance_guard_dryrun", "governance_guard_dryrun_v1.json"),
    ("health_guard_dryrun", "health_guard_dryrun_v1.json"),
    ("skeleton_boundary_matrix", "skeleton_boundary_matrix_v1.json"),
    ("skeleton_issue_register", "skeleton_issue_register_v1.json"),
    ("skeleton_implementation_dryrun_readiness_decision", "skeleton_implementation_dryrun_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--skeleton-planning-root", default=str(DEFAULT_SK_PLAN))
    p.add_argument("--ebwm-planning-root", default=str(DEFAULT_EBWM_PLAN))
    p.add_argument("--ebwm-dryrun-root", default=str(DEFAULT_EBWM_DR))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_v1(
        midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_root=args.skeleton_planning_root,
        midplatform_event_bus_working_memory_scheduler_planning_root=args.ebwm_planning_root,
        midplatform_event_bus_working_memory_scheduler_dryrun_and_review_root=args.ebwm_dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "dryrun_pass": sm.get("dryrun_pass"),
                "blocker_count": sm.get("blocker_count"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
