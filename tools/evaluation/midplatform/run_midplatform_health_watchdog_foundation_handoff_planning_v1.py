#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Health Watchdog Foundation Handoff Planning v1."""

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

from capabilities.midplatform.midplatform_health_watchdog_foundation_handoff_planning_v1 import (
    DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT,
    DEFAULT_MOUNT_DRYRUN_ROOT,
    DEFAULT_OUTPUT,
    DEFAULT_POST_DRYRUN_ROOT,
    DEFAULT_SKELETON_DRYRUN_ROOT,
    run_midplatform_health_watchdog_foundation_handoff_planning_v1,
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("health_watchdog_foundation_handoff_scope", "health_watchdog_foundation_handoff_scope_v1.json"),
    ("health_watchdog_foundation_version_tag", "health_watchdog_foundation_version_tag_v1.json"),
    ("health_watchdog_frozen_type_interface", "health_watchdog_frozen_type_interface_v1.json"),
    ("health_watchdog_frozen_function_interface", "health_watchdog_frozen_function_interface_v1.json"),
    ("health_watchdog_frozen_validator_interface", "health_watchdog_frozen_validator_interface_v1.json"),
    ("health_watchdog_handoff_contract", "health_watchdog_handoff_contract_v1.json"),
    ("health_watchdog_downstream_output_contract", "health_watchdog_downstream_output_contract_v1.json"),
    ("health_watchdog_forbidden_mutation_policy", "health_watchdog_forbidden_mutation_policy_v1.json"),
    ("health_watchdog_change_control_policy", "health_watchdog_change_control_policy_v1.json"),
    ("health_watchdog_boundary_freeze", "health_watchdog_boundary_freeze_v1.json"),
    ("health_watchdog_downstream_readiness_matrix", "health_watchdog_downstream_readiness_matrix_v1.json"),
    ("health_watchdog_non_claims", "health_watchdog_non_claims_v1.json"),
    ("health_watchdog_route_decision", "health_watchdog_route_decision_v1.json"),
    (
        "health_watchdog_foundation_handoff_readiness_decision",
        "health_watchdog_foundation_handoff_readiness_decision_v1.json",
    ),
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
    parser.add_argument("--post-dryrun-root", default=DEFAULT_POST_DRYRUN_ROOT)
    parser.add_argument("--skeleton-dryrun-root", default=DEFAULT_SKELETON_DRYRUN_ROOT)
    parser.add_argument("--mount-dryrun-root", default=DEFAULT_MOUNT_DRYRUN_ROOT)
    parser.add_argument("--decision-center-handoff-dryrun-root", default=DEFAULT_DECISION_CENTER_HANDOFF_DRYRUN_ROOT)
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    result = run_midplatform_health_watchdog_foundation_handoff_planning_v1(
        post_dryrun_root=args.post_dryrun_root,
        skeleton_dryrun_root=args.skeleton_dryrun_root,
        mount_dryrun_root=args.mount_dryrun_root,
        decision_center_handoff_dryrun_root=args.decision_center_handoff_dryrun_root,
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
                "planning_pass": summary.get("planning_pass"),
                "blocker_count": summary.get("blocker_count"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "recommended_route_primary_next_phase": summary.get("recommended_route_primary_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
