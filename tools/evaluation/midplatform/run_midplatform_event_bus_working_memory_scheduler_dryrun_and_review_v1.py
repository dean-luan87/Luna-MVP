#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Event Bus / Working Memory / Scheduler DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1 import (
    run_midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1,
)

DEFAULT_PLANNING = REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_planning"
DEFAULT_CORE_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_planning"
DEFAULT_CORE_DR = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_dryrun_and_review"
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_dryrun_and_review"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("upstream_contract_consumability_review", "upstream_contract_consumability_review_v1.json"),
    ("event_type_registry_review", "event_type_registry_review_v1.json"),
    ("event_state_machine_dryrun", "event_state_machine_dryrun_v1.json"),
    ("working_memory_state_machine_dryrun", "working_memory_state_machine_dryrun_v1.json"),
    ("ttl_cleanup_policy_dryrun", "ttl_cleanup_policy_dryrun_v1.json"),
    ("scheduler_priority_queue_dryrun", "scheduler_priority_queue_dryrun_v1.json"),
    ("preemption_and_deferral_dryrun", "preemption_and_deferral_dryrun_v1.json"),
    ("interaction_model_dryrun", "interaction_model_dryrun_v1.json"),
    ("health_metric_mapping_review", "health_metric_mapping_review_v1.json"),
    ("failure_route_dryrun_review", "failure_route_dryrun_review_v1.json"),
    ("governance_boundary_review", "governance_boundary_review_v1.json"),
    ("sample_flow_dryrun", "sample_flow_dryrun_v1.json"),
    ("boundary_matrix_review", "boundary_matrix_review_v1.json"),
    ("issue_register", "issue_register_v1.json"),
    ("dryrun_readiness_decision", "dryrun_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--planning-root", default=str(DEFAULT_PLANNING))
    p.add_argument("--core-component-planning-root", default=str(DEFAULT_CORE_PLAN))
    p.add_argument("--core-component-dryrun-root", default=str(DEFAULT_CORE_DR))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_event_bus_working_memory_scheduler_dryrun_and_review_v1(
        midplatform_event_bus_working_memory_scheduler_planning_root=args.planning_root,
        midplatform_micro_os_core_component_planning_root=args.core_component_planning_root,
        midplatform_micro_os_core_component_dryrun_and_review_root=args.core_component_dryrun_root,
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
