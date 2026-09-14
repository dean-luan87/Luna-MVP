#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Main Project Structure Migration Real Rollback Rehearsal Pre-Authorization Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1 import (
    run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT
    / "_eval_out"
    / "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("input_root_matrix", "input_root_matrix.json"),
    (
        "real_rollback_rehearsal_pre_authorization_post_dryrun_review_policy",
        "real_rollback_rehearsal_pre_authorization_post_dryrun_review_policy_v1.json",
    ),
    (
        "pre_authorization_dryrun_artifact_completeness_review",
        "pre_authorization_dryrun_artifact_completeness_review_v1.json",
    ),
    ("authorization_non_release_review_matrix", "authorization_non_release_review_matrix_v1.json"),
    ("pre_authorization_chain_continuity_review", "pre_authorization_chain_continuity_review_v1.json"),
    ("boundary_freeze_review_matrix", "boundary_freeze_review_matrix_v1.json"),
    ("success_claim_post_dryrun_review", "success_claim_post_dryrun_review_v1.json"),
    ("non_executable_dryrun_asset_review", "non_executable_dryrun_asset_review_v1.json"),
    ("pre_authorization_post_dryrun_issue_register", "pre_authorization_post_dryrun_issue_register_v1.json"),
    (
        "permission_and_authorization_terminology_review",
        "permission_and_authorization_terminology_review_v1.json",
    ),
    (
        "real_rollback_rehearsal_pre_authorization_post_dryrun_review_readiness_decision",
        "real_rollback_rehearsal_pre_authorization_post_dryrun_review_readiness_decision_v1.json",
    ),
    ("next_phase_recommendation", "next_phase_recommendation.json"),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Real Rollback Rehearsal Pre-Authorization Post-DryRun Review v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--pre-authorization-dryrun-root",
        default=str(
            REPO_ROOT
            / "_eval_out"
            / "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1(
        pre_authorization_dryrun_root=args.pre_authorization_dryrun_root,
    )
    for key, filename in OUTPUT_FILES:
        _write_json(output_root / filename, result[key])

    summary = result["summary"]
    _write_json(
        output_root / "verifier_report.json",
        {
            "phase": summary.get("phase"),
            "verifier_status": "PENDING",
            "check_count": 0,
            "passed": None,
            "source_chain": summary.get("source_chain"),
        },
    )

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "boundary_ok": summary.get("boundary_ok"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())

