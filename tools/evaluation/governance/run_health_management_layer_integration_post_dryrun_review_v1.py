#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Health Management Layer Integration Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.health_management_layer_integration_post_dryrun_review_v1 import (
    run_health_management_layer_integration_post_dryrun_review_v1,
)

DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_dryrun"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("health_management_dryrun_input_review", "health_management_dryrun_input_review_v1.json"),
    ("health_signal_candidate_review", "health_signal_candidate_review_v1.json"),
    ("fallback_candidate_review", "fallback_candidate_review_v1.json"),
    ("degradation_candidate_review", "degradation_candidate_review_v1.json"),
    ("survival_drive_candidate_review", "survival_drive_candidate_review_v1.json"),
    ("recovery_plan_candidate_review", "recovery_plan_candidate_review_v1.json"),
    ("health_to_drive_bridge_review", "health_to_drive_bridge_review_v1.json"),
    ("health_runtime_boundary_review", "health_runtime_boundary_review_v1.json"),
    ("health_metric_reserved_review", "health_metric_reserved_review_v1.json"),
    ("health_management_blocked_path_review", "health_management_blocked_path_review_v1.json"),
    (
        "health_management_integration_closure_decision",
        "health_management_integration_closure_decision_v1.json",
    ),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--health-management-layer-integration-dryrun-root",
        default=DEFAULT_DRYRUN,
    )
    args = p.parse_args()

    result = run_health_management_layer_integration_post_dryrun_review_v1(
        health_management_layer_integration_dryrun_root=(
            args.health_management_layer_integration_dryrun_root
        ),
        review_output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "health_management_integration_dryrun_closed": sm.get(
                    "health_management_integration_dryrun_closed"
                ),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
