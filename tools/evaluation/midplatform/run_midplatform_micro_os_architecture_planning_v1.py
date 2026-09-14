#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform 1.0 Micro-OS Architecture Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import (
    run_midplatform_micro_os_architecture_planning_v1,
)

DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_planning"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("midplatform_micro_os_architecture_planning_policy", "midplatform_micro_os_architecture_planning_policy_v1.json"),
    ("midplatform_micro_os_definition", "midplatform_micro_os_definition_v1.json"),
    ("midplatform_micro_os_layer_architecture", "midplatform_micro_os_layer_architecture_v1.json"),
    (
        "midplatform_existing_governance_relocation_matrix",
        "midplatform_existing_governance_relocation_matrix_v1.json",
    ),
    ("midplatform_upstream_downstream_matrix", "midplatform_upstream_downstream_matrix_v1.json"),
    ("midplatform_information_lifecycle", "midplatform_information_lifecycle_v1.json"),
    ("midplatform_component_responsibility_map", "midplatform_component_responsibility_map_v1.json"),
    (
        "midplatform_model_rule_algorithm_placement_matrix",
        "midplatform_model_rule_algorithm_placement_matrix_v1.json",
    ),
    ("midplatform_priority_and_scheduling_policy", "midplatform_priority_and_scheduling_policy_v1.json"),
    ("midplatform_working_memory_policy", "midplatform_working_memory_policy_v1.json"),
    ("midplatform_health_metric_scope", "midplatform_health_metric_scope_v1.json"),
    ("midplatform_failure_mode_matrix", "midplatform_failure_mode_matrix_v1.json"),
    (
        "midplatform_degraded_and_recovery_mode_policy",
        "midplatform_degraded_and_recovery_mode_policy_v1.json",
    ),
    (
        "midplatform_worldmodel_memory_feedback_boundary",
        "midplatform_worldmodel_memory_feedback_boundary_v1.json",
    ),
    (
        "midplatform_local_cloud_model_routing_boundary",
        "midplatform_local_cloud_model_routing_boundary_v1.json",
    ),
    ("midplatform_non_claims_register", "midplatform_non_claims_register_v1.json"),
    ("midplatform_micro_os_dryrun_plan", "midplatform_micro_os_dryrun_plan_v1.json"),
    (
        "midplatform_micro_os_architecture_planning_decision",
        "midplatform_micro_os_architecture_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    p.add_argument("--upstream-inventory-root", default="")
    args = p.parse_args()

    kwargs: Dict[str, Any] = {"output_root": args.output_root}
    if args.upstream_inventory_root:
        kwargs["upstream_inventory_root"] = args.upstream_inventory_root

    result = run_midplatform_micro_os_architecture_planning_v1(**kwargs)
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
