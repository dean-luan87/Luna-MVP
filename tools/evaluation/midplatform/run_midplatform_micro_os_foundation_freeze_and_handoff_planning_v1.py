#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Micro-OS Foundation Freeze and Handoff Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_micro_os_foundation_freeze_and_handoff_planning_v1 import (
    run_midplatform_micro_os_foundation_freeze_and_handoff_planning_v1,
)

DEFAULT_POST_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_SK_DR = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun"
)
DEFAULT_SK_PLAN = (
    REPO_ROOT / "_tmp_eval_out" / "midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning"
)
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_foundation_freeze_and_handoff_planning"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("micro_os_foundation_freeze_scope", "micro_os_foundation_freeze_scope_v1.json"),
    ("micro_os_foundation_frozen_interface", "micro_os_foundation_frozen_interface_v1.json"),
    ("micro_os_foundation_version_tag", "micro_os_foundation_version_tag_v1.json"),
    ("micro_os_foundation_handoff_contract", "micro_os_foundation_handoff_contract_v1.json"),
    ("micro_os_foundation_allowed_mount_points", "micro_os_foundation_allowed_mount_points_v1.json"),
    ("micro_os_foundation_forbidden_mutation_policy", "micro_os_foundation_forbidden_mutation_policy_v1.json"),
    ("micro_os_foundation_change_control_policy", "micro_os_foundation_change_control_policy_v1.json"),
    ("micro_os_foundation_downstream_readiness_matrix", "micro_os_foundation_downstream_readiness_matrix_v1.json"),
    ("micro_os_foundation_health_and_boundary_freeze", "micro_os_foundation_health_and_boundary_freeze_v1.json"),
    ("micro_os_foundation_non_claims", "micro_os_foundation_non_claims_v1.json"),
    ("micro_os_foundation_route_decision", "micro_os_foundation_route_decision_v1.json"),
    ("micro_os_foundation_freeze_readiness_decision", "micro_os_foundation_freeze_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--post-dryrun-root", default=str(DEFAULT_POST_DR))
    p.add_argument("--skeleton-dryrun-root", default=str(DEFAULT_SK_DR))
    p.add_argument("--skeleton-planning-root", default=str(DEFAULT_SK_PLAN))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_micro_os_foundation_freeze_and_handoff_planning_v1(
        midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_post_dryrun_review_root=args.post_dryrun_root,
        midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_dryrun_root=args.skeleton_dryrun_root,
        midplatform_event_bus_working_memory_scheduler_controlled_skeleton_implementation_planning_root=args.skeleton_planning_root,
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
                "primary_route": sm.get("primary_route_after_freeze"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
