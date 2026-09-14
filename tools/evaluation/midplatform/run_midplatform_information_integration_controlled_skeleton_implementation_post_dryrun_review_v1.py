#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Luna Midplatform Information Integration Controlled Skeleton Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_v1 import (
    run_midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_v1,
)

DEFAULT_SK_DRYRUN = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_information_integration_controlled_skeleton_implementation_dryrun"
)
DEFAULT_SK_PLAN = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_information_integration_controlled_skeleton_implementation_planning"
)
DEFAULT_MOUNT_DR = REPO_ROOT / "_tmp_eval_out" / "midplatform_information_integration_mount_dryrun_and_review"
DEFAULT_OUTPUT = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("skeleton_file_integrity_review", "skeleton_file_integrity_review_v1.json"),
    ("forbidden_runtime_import_review", "forbidden_runtime_import_review_v1.json"),
    ("pure_function_boundary_review", "pure_function_boundary_review_v1.json"),
    ("type_contract_review", "type_contract_review_v1.json"),
    ("function_contract_review", "function_contract_review_v1.json"),
    ("static_validator_review", "static_validator_review_v1.json"),
    ("sample_dryrun_output_review", "sample_dryrun_output_review_v1.json"),
    ("processing_chain_review", "processing_chain_review_v1.json"),
    ("governance_guard_review", "governance_guard_review_v1.json"),
    ("health_guard_review", "health_guard_review_v1.json"),
    ("recall_boundary_review", "recall_boundary_review_v1.json"),
    ("downstream_readiness_review", "downstream_readiness_review_v1.json"),
    ("boundary_matrix_post_review", "boundary_matrix_post_review_v1.json"),
    ("post_dryrun_issue_register", "post_dryrun_issue_register_v1.json"),
    ("post_dryrun_readiness_decision", "post_dryrun_readiness_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--skeleton-dryrun-root", default=str(DEFAULT_SK_DRYRUN))
    p.add_argument("--skeleton-planning-root", default=str(DEFAULT_SK_PLAN))
    p.add_argument("--mount-dryrun-root", default=str(DEFAULT_MOUNT_DR))
    p.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = p.parse_args()

    result = run_midplatform_information_integration_controlled_skeleton_implementation_post_dryrun_review_v1(
        midplatform_information_integration_controlled_skeleton_implementation_dryrun_root=args.skeleton_dryrun_root,
        midplatform_information_integration_controlled_skeleton_implementation_planning_root=args.skeleton_planning_root,
        midplatform_information_integration_mount_dryrun_and_review_root=args.mount_dryrun_root,
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
                "post_dryrun_review_pass": sm.get("post_dryrun_review_pass"),
                "blocker_count": sm.get("blocker_count"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "recommended_alternate_next_phase": sm.get("recommended_alternate_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("post_dryrun_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
