#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Micro-OS Architecture DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_micro_os_architecture_dryrun_and_review_v1 import (
    run_midplatform_micro_os_architecture_dryrun_and_review_v1,
)

DEFAULT_PLANNING = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_planning"
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_dryrun_and_review"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("micro_os_layer_consumability_review", "micro_os_layer_consumability_review_v1.json"),
    ("governance_relocation_dryrun_review", "governance_relocation_dryrun_review_v1.json"),
    ("upstream_downstream_consistency_review", "upstream_downstream_consistency_review_v1.json"),
    ("information_lifecycle_dryrun", "information_lifecycle_dryrun_v1.json"),
    ("component_responsibility_review", "component_responsibility_review_v1.json"),
    ("model_rule_algorithm_placement_review", "model_rule_algorithm_placement_review_v1.json"),
    ("priority_scheduler_dryrun_review", "priority_scheduler_dryrun_review_v1.json"),
    ("working_memory_boundary_review", "working_memory_boundary_review_v1.json"),
    ("health_metric_scope_review", "health_metric_scope_review_v1.json"),
    ("failure_mode_dryrun_review", "failure_mode_dryrun_review_v1.json"),
    ("degraded_recovery_mode_review", "degraded_recovery_mode_review_v1.json"),
    (
        "worldmodel_memory_feedback_boundary_review",
        "worldmodel_memory_feedback_boundary_review_v1.json",
    ),
    (
        "local_cloud_model_routing_boundary_review",
        "local_cloud_model_routing_boundary_review_v1.json",
    ),
    ("non_claims_review", "non_claims_review_v1.json"),
    ("dryrun_readiness_decision", "dryrun_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--planning-root", default=str(DEFAULT_PLANNING))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_micro_os_architecture_dryrun_and_review_v1(
        midplatform_micro_os_architecture_planning_root=args.planning_root,
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
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
