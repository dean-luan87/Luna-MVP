#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Information Integration Layer DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    run_midplatform_information_integration_layer_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_planning"
)
DEFAULT_DS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_drive_signal_contract_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("information_integration_dryrun_review_policy", "information_integration_dryrun_review_policy_v1.json"),
    (
        "information_integration_planning_input_review",
        "information_integration_planning_input_review_v1.json",
    ),
    ("information_integration_model_candidate", "information_integration_model_candidate_v1.json"),
    ("sample_integrated_context_candidate", "sample_integrated_context_candidate_v1.json"),
    ("sample_context_conflict_candidate", "sample_context_conflict_candidate_v1.json"),
    ("sample_context_gap_candidate", "sample_context_gap_candidate_v1.json"),
    ("sample_context_freshness_status", "sample_context_freshness_status_v1.json"),
    ("sample_context_priority_map", "sample_context_priority_map_v1.json"),
    ("sample_decision_readiness_candidate", "sample_decision_readiness_candidate_v1.json"),
    (
        "integration_input_source_taxonomy_review",
        "integration_input_source_taxonomy_review_v1.json",
    ),
    ("drive_signal_integration_review", "drive_signal_integration_review_v1.json"),
    ("perception_context_integration_review", "perception_context_integration_review_v1.json"),
    (
        "memory_worldmodel_context_integration_review",
        "memory_worldmodel_context_integration_review_v1.json",
    ),
    ("task_route_map_context_integration_review", "task_route_map_context_integration_review_v1.json"),
    (
        "health_validation_whitebox_integration_review",
        "health_validation_whitebox_integration_review_v1.json",
    ),
    ("provider_status_integration_review", "provider_status_integration_review_v1.json"),
    ("conflict_gap_freshness_scoring_review", "conflict_gap_freshness_scoring_review_v1.json"),
    ("decision_center_handoff_review", "decision_center_handoff_review_v1.json"),
    ("no_universal_brain_boundary_review", "no_universal_brain_boundary_review_v1.json"),
    (
        "information_integration_traceability_review",
        "information_integration_traceability_review_v1.json",
    ),
    ("information_integration_boundary_audit", "information_integration_boundary_audit_v1.json"),
    (
        "information_integration_blocked_path_result",
        "information_integration_blocked_path_result_v1.json",
    ),
    ("information_integration_closure_decision", "information_integration_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--drive-signal-dryrun-root", default=DEFAULT_DS_DR)
    args = p.parse_args()

    result = run_midplatform_information_integration_layer_dryrun_and_review_v1(
        midplatform_information_integration_layer_planning_root=args.planning_root,
        seed_core_drive_signal_contract_dryrun_and_review_root=args.drive_signal_dryrun_root,
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
