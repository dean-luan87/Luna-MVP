#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Event Bus / Working Memory / Scheduler Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_event_bus_working_memory_scheduler_planning_v1 import (
    run_midplatform_event_bus_working_memory_scheduler_planning_v1,
)

DEFAULT_ARCH_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_planning"
DEFAULT_ARCH_DR = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_dryrun_and_review"
DEFAULT_CORE_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_planning"
DEFAULT_CORE_DR = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_core_component_dryrun_and_review"
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_planning"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("event_bus_contract", "event_bus_contract_v1.json"),
    ("event_type_registry", "event_type_registry_v1.json"),
    ("event_state_machine", "event_state_machine_v1.json"),
    ("working_memory_contract", "working_memory_contract_v1.json"),
    ("working_memory_entry_state_machine", "working_memory_entry_state_machine_v1.json"),
    ("working_memory_ttl_and_cleanup_policy", "working_memory_ttl_and_cleanup_policy_v1.json"),
    ("scheduler_contract", "scheduler_contract_v1.json"),
    ("priority_queue_policy", "priority_queue_policy_v1.json"),
    ("preemption_and_deferral_policy", "preemption_and_deferral_policy_v1.json"),
    (
        "event_bus_working_memory_scheduler_interaction_model",
        "event_bus_working_memory_scheduler_interaction_model_v1.json",
    ),
    ("eb_wm_scheduler_health_metric_mapping", "eb_wm_scheduler_health_metric_mapping_v1.json"),
    ("eb_wm_scheduler_failure_route_matrix", "eb_wm_scheduler_failure_route_matrix_v1.json"),
    ("eb_wm_scheduler_governance_boundary", "eb_wm_scheduler_governance_boundary_v1.json"),
    ("eb_wm_scheduler_sample_flow_plan", "eb_wm_scheduler_sample_flow_plan_v1.json"),
    ("eb_wm_scheduler_boundary_matrix", "eb_wm_scheduler_boundary_matrix_v1.json"),
    ("eb_wm_scheduler_planning_readiness_decision", "eb_wm_scheduler_planning_readiness_decision_v1.json"),
    ("eb_wm_scheduler_non_claims_register", "eb_wm_scheduler_non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--architecture-planning-root", default=str(DEFAULT_ARCH_PLAN))
    p.add_argument("--architecture-dryrun-root", default=str(DEFAULT_ARCH_DR))
    p.add_argument("--core-component-planning-root", default=str(DEFAULT_CORE_PLAN))
    p.add_argument("--core-component-dryrun-root", default=str(DEFAULT_CORE_DR))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_event_bus_working_memory_scheduler_planning_v1(
        midplatform_micro_os_architecture_planning_root=args.architecture_planning_root,
        midplatform_micro_os_architecture_dryrun_and_review_root=args.architecture_dryrun_root,
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
