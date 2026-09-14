#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Health Watchdog Foundation Handoff DryRunAndReview v1."""

from __future__ import annotations

import dataclasses
import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1 import (
    DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT,
    DEFAULT_HANDOFF_PLANNING_ROOT,
    DEFAULT_II_HANDOFF_DRYRUN_ROOT,
    DEFAULT_MICRO_OS_FREEZE_DRYRUN_ROOT,
    DEFAULT_MOUNT_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    DEFAULT_POST_DRYRUN_ROOT,
    DEFAULT_SKELETON_DRYRUN_ROOT,
    run_midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("upstream_go_chain_review", "upstream_go_chain_review_v1.json"),
    ("foundation_version_tag_review", "foundation_version_tag_review_v1.json"),
    ("skeleton_file_consistency_review", "skeleton_file_consistency_review_v1.json"),
    ("frozen_type_interface_review", "frozen_type_interface_review_v1.json"),
    ("frozen_function_interface_review", "frozen_function_interface_review_v1.json"),
    ("frozen_validator_interface_review", "frozen_validator_interface_review_v1.json"),
    ("handoff_contract_dryrun", "handoff_contract_dryrun_v1.json"),
    ("downstream_output_contract_review", "downstream_output_contract_review_v1.json"),
    ("forbidden_mutation_policy_review", "forbidden_mutation_policy_review_v1.json"),
    ("change_control_policy_review", "change_control_policy_review_v1.json"),
    ("boundary_freeze_review", "boundary_freeze_review_v1.json"),
    ("downstream_readiness_matrix_review", "downstream_readiness_matrix_review_v1.json"),
    ("non_claims_review", "non_claims_review_v1.json"),
    ("route_decision_review", "route_decision_review_v1.json"),
    ("issue_register", "issue_register_v1.json"),
    ("handoff_dryrun_readiness_decision", "handoff_dryrun_readiness_decision_v1.json"),
)


def _json_default(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return str(obj)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=_json_default) + "\n", encoding="utf-8")


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--handoff-planning-root", default=DEFAULT_HANDOFF_PLANNING_ROOT)
    parser.add_argument("--post-dryrun-root", default=DEFAULT_POST_DRYRUN_ROOT)
    parser.add_argument("--skeleton-dryrun-root", default=DEFAULT_SKELETON_DRYRUN_ROOT)
    parser.add_argument("--mount-dryrun-root", default=DEFAULT_MOUNT_DRYRUN_ROOT)
    parser.add_argument("--decision-center-handoff-dryrun-root", default=DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT)
    parser.add_argument("--information-integration-handoff-dryrun-root", default=DEFAULT_II_HANDOFF_DRYRUN_ROOT)
    parser.add_argument("--micro-os-freeze-dryrun-root", default=DEFAULT_MICRO_OS_FREEZE_DRYRUN_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = run_midplatform_health_watchdog_foundation_handoff_dryrun_and_review_v1(
        midplatform_health_watchdog_foundation_handoff_planning_root=args.handoff_planning_root,
        midplatform_health_watchdog_controlled_skeleton_implementation_post_dryrun_review_root=args.post_dryrun_root,
        midplatform_health_watchdog_controlled_skeleton_implementation_dryrun_root=args.skeleton_dryrun_root,
        midplatform_health_watchdog_mount_dryrun_and_review_root=args.mount_dryrun_root,
        midplatform_decision_center_foundation_handoff_dryrun_and_review_root=args.decision_center_handoff_dryrun_root,
        midplatform_information_integration_foundation_handoff_dryrun_and_review_root=args.information_integration_handoff_dryrun_root,
        midplatform_micro_os_foundation_freeze_and_handoff_dryrun_and_review_root=args.micro_os_freeze_dryrun_root,
        output_root=args.output_root,
    )
    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])
    summary = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "dryrun_pass": summary.get("dryrun_pass"),
                "blocker_count": summary.get("blocker_count"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "foundation_id": summary.get("foundation_id"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("dryrun_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
