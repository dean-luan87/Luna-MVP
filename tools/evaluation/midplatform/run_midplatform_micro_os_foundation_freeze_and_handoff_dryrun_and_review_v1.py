#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Micro-OS Foundation Freeze and Handoff DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1 import (
    run_midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1,
)

DEFAULT_PLAN = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_planning"
DEFAULT_POST_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_SK_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun"
)
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("freeze_scope_consumability_review", "freeze_scope_consumability_review_v1.json"),
    ("frozen_interface_integrity_review", "frozen_interface_integrity_review_v1.json"),
    ("version_tag_review", "version_tag_review_v1.json"),
    ("handoff_contract_review", "handoff_contract_review_v1.json"),
    ("allowed_mount_points_dryrun", "allowed_mount_points_dryrun_v1.json"),
    ("forbidden_mutation_policy_review", "forbidden_mutation_policy_review_v1.json"),
    ("change_control_policy_review", "change_control_policy_review_v1.json"),
    ("downstream_readiness_matrix_review", "downstream_readiness_matrix_review_v1.json"),
    ("health_and_boundary_freeze_review", "health_and_boundary_freeze_review_v1.json"),
    ("route_decision_review", "route_decision_review_v1.json"),
    ("non_claims_review", "non_claims_review_v1.json"),
    ("issue_register", "issue_register_v1.json"),
    ("freeze_dryrun_readiness_decision", "freeze_dryrun_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--freeze-planning-root", default=str(DEFAULT_PLAN))
    p.add_argument("--post-dryrun-root", default=str(DEFAULT_POST_DR))
    p.add_argument("--skeleton-dryrun-root", default=str(DEFAULT_SK_DR))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_v1(
        midplatform_micro_os_foundation_freeze_and_handoff_planning_root=args.freeze_planning_root,
        midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_root=args.post_dryrun_root,
        midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_root=args.skeleton_dryrun_root,
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
