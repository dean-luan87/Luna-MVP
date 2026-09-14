#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Decision Center Mount Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_decision_center_mount_planning_v1 import (
    run_midplatform_decision_center_mount_planning_v1,
)

DEFAULT_HANDOFF_DRYRUN = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_HANDOFF_PLANNING = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_foundation_handoff_planning"
)
DEFAULT_POST_DRYRUN = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_FREEZE_DRYRUN = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"
)
DEFAULT_FREEZE_PLANNING = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_planning"
)
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_mount_planning"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("decision_center_mount_scope", "decision_center_mount_scope_v1.json"),
    ("decision_center_mount_contract", "decision_center_mount_contract_v1.json"),
    ("decision_center_input_contract", "decision_center_input_contract_v1.json"),
    ("decision_center_output_contract", "decision_center_output_contract_v1.json"),
    ("decision_center_processing_model", "decision_center_processing_model_v1.json"),
    ("decision_center_decision_state_machine", "decision_center_decision_state_machine_v1.json"),
    (
        "decision_center_model_rule_algorithm_placement",
        "decision_center_model_rule_algorithm_placement_v1.json",
    ),
    ("decision_center_governance_boundary", "decision_center_governance_boundary_v1.json"),
    ("decision_center_health_boundary", "decision_center_health_boundary_v1.json"),
    (
        "decision_center_information_integration_dependency_boundary",
        "decision_center_information_integration_dependency_boundary_v1.json",
    ),
    ("decision_center_downstream_handoff_matrix", "decision_center_downstream_handoff_matrix_v1.json"),
    ("decision_center_sample_flow_plan", "decision_center_sample_flow_plan_v1.json"),
    ("decision_center_failure_route_matrix", "decision_center_failure_route_matrix_v1.json"),
    ("decision_center_mount_health_metric_scope", "decision_center_mount_health_metric_scope_v1.json"),
    ("decision_center_boundary_matrix", "decision_center_boundary_matrix_v1.json"),
    ("decision_center_mount_non_claims", "decision_center_mount_non_claims_v1.json"),
    ("decision_center_mount_readiness_decision", "decision_center_mount_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--handoff-dryrun-root", default=str(DEFAULT_HANDOFF_DRYRUN))
    p.add_argument("--handoff-planning-root", default=str(DEFAULT_HANDOFF_PLANNING))
    p.add_argument("--post-dryrun-root", default=str(DEFAULT_POST_DRYRUN))
    p.add_argument("--freeze-dryrun-root", default=str(DEFAULT_FREEZE_DRYRUN))
    p.add_argument("--freeze-planning-root", default=str(DEFAULT_FREEZE_PLANNING))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_decision_center_mount_planning_v1(
        midplatform_information_integration_foundation_handoff_dryrun_and_review_root=args.handoff_dryrun_root,
        midplatform_information_integration_foundation_handoff_planning_root=args.handoff_planning_root,
        midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_root=args.post_dryrun_root,
        midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root=args.freeze_dryrun_root,
        midplatform_micro_os_foundation_freeze_and_handoff_planning_root=args.freeze_planning_root,
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
                "module_id": sm.get("module_id"),
                "layer": sm.get("layer"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
