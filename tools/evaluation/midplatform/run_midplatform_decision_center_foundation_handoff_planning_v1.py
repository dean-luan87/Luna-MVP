#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Decision Center Foundation Handoff Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_decision_center_foundation_handoff_planning_v1 import (
    run_midplatform_decision_center_foundation_handoff_planning_v1,
)

DEFAULT_POST_DR = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review"
)
DEFAULT_SK_DR = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_decision_center_controlled_skeleton_implementation_dryrun"
)
DEFAULT_MOUNT_DR = REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_mount_dryrun_and_review"
DEFAULT_HANDOFF_DR = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_information_integration_foundation_handoff_dryrun_and_review"
)
DEFAULT_OUTPUT = REPO_ROOT / "_tmp_eval_out" / "midplatform_decision_center_foundation_handoff_planning"

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("decision_center_foundation_handoff_scope", "decision_center_foundation_handoff_scope_v1.json"),
    ("decision_center_foundation_version_tag", "decision_center_foundation_version_tag_v1.json"),
    ("decision_center_frozen_type_interface", "decision_center_frozen_type_interface_v1.json"),
    ("decision_center_frozen_function_interface", "decision_center_frozen_function_interface_v1.json"),
    ("decision_center_frozen_validator_interface", "decision_center_frozen_validator_interface_v1.json"),
    ("decision_center_handoff_contract", "decision_center_handoff_contract_v1.json"),
    ("decision_center_downstream_output_contract", "decision_center_downstream_output_contract_v1.json"),
    ("decision_center_forbidden_mutation_policy", "decision_center_forbidden_mutation_policy_v1.json"),
    ("decision_center_change_control_policy", "decision_center_change_control_policy_v1.json"),
    ("decision_center_boundary_freeze", "decision_center_boundary_freeze_v1.json"),
    ("decision_center_downstream_readiness_matrix", "decision_center_downstream_readiness_matrix_v1.json"),
    ("decision_center_non_claims", "decision_center_non_claims_v1.json"),
    ("decision_center_route_decision", "decision_center_route_decision_v1.json"),
    (
        "decision_center_foundation_handoff_readiness_decision",
        "decision_center_foundation_handoff_readiness_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--post-dryrun-root", default=str(DEFAULT_POST_DR))
    p.add_argument("--skeleton-dryrun-root", default=str(DEFAULT_SK_DR))
    p.add_argument("--mount-dryrun-root", default=str(DEFAULT_MOUNT_DR))
    p.add_argument("--handoff-dryrun-root", default=str(DEFAULT_HANDOFF_DR))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_decision_center_foundation_handoff_planning_v1(
        midplatform_decision_center_controlled_skeleton_implementation_post_dryrun_review_root=args.post_dryrun_root,
        midplatform_decision_center_controlled_skeleton_implementation_dryrun_root=args.skeleton_dryrun_root,
        midplatform_decision_center_mount_dryrun_and_review_root=args.mount_dryrun_root,
        midplatform_information_integration_foundation_handoff_dryrun_and_review_root=args.handoff_dryrun_root,
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
                "primary_route_after_handoff": sm.get("primary_route_after_handoff"),
                "foundation_id": sm.get("foundation_id"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
