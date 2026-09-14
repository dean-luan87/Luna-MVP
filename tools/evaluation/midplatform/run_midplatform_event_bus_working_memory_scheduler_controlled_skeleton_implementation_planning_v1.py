#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform EB/WM/Scheduler Controlled Skeleton Implementation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1 import (
    run_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1,
)

DEFAULT_PLANNING = REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_planning"
DEFAULT_DRYRUN = REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_dryrun_and_review"
DEFAULT_OUTPUT = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("controlled_skeleton_scope", "controlled_skeleton_scope_v1.json"),
    ("controlled_skeleton_file_plan", "controlled_skeleton_file_plan_v1.json"),
    ("controlled_skeleton_type_contract", "controlled_skeleton_type_contract_v1.json"),
    ("event_bus_skeleton_contract", "event_bus_skeleton_contract_v1.json"),
    ("working_memory_skeleton_contract", "working_memory_skeleton_contract_v1.json"),
    ("scheduler_skeleton_contract", "scheduler_skeleton_contract_v1.json"),
    ("controlled_skeleton_interaction_plan", "controlled_skeleton_interaction_plan_v1.json"),
    ("controlled_skeleton_governance_guard", "controlled_skeleton_governance_guard_v1.json"),
    ("controlled_skeleton_health_guard", "controlled_skeleton_health_guard_v1.json"),
    ("controlled_skeleton_sample_plan", "controlled_skeleton_sample_plan_v1.json"),
    ("controlled_skeleton_test_plan", "controlled_skeleton_test_plan_v1.json"),
    ("controlled_skeleton_boundary_matrix", "controlled_skeleton_boundary_matrix_v1.json"),
    ("controlled_skeleton_non_claims", "controlled_skeleton_non_claims_v1.json"),
    ("controlled_skeleton_planning_readiness_decision", "controlled_skeleton_planning_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--planning-root", default=str(DEFAULT_PLANNING))
    p.add_argument("--dryrun-root", default=str(DEFAULT_DRYRUN))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_v1(
        midplatform_event_bus_working_memory_scheduler_planning_root=args.planning_root,
        midplatform_event_bus_working_memory_scheduler_dryrun_and_review_root=args.dryrun_root,
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
                "planning_pass": sm.get("planning_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
