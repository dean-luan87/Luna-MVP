#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Boundary Object Registry Generation Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.boundary_object_registry_generation_post_dryrun_review_v1 import (
    run_boundary_object_registry_generation_post_dryrun_review_v1,
)

DEFAULT_OUTPUT_ROOT = (
    REPO_ROOT / "_eval_out" / "boundary_object_registry_generation_post_dryrun_review_v1_smoke_v0"
)
DEFAULT_DRYRUN_ROOT = (
    REPO_ROOT / "_eval_out" / "boundary_object_registry_generation_dryrun_v1_smoke_v0"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "boundary_object_registry_generation_post_dryrun_review_policy",
        "boundary_object_registry_generation_post_dryrun_review_policy_v1.json",
    ),
    (
        "registry_generation_dryrun_completeness_review",
        "registry_generation_dryrun_completeness_review_v1.json",
    ),
    (
        "registry_generation_non_execution_review",
        "registry_generation_non_execution_review_v1.json",
    ),
    (
        "registry_source_validation_non_final_review",
        "registry_source_validation_non_final_review_v1.json",
    ),
    (
        "registry_contamination_check_non_final_review",
        "registry_contamination_check_non_final_review_v1.json",
    ),
    ("registry_entry_non_generation_review", "registry_entry_non_generation_review_v1.json"),
    ("registry_source_misuse_review", "registry_source_misuse_review_v1.json"),
    (
        "registry_protected_object_integrity_review",
        "registry_protected_object_integrity_review_v1.json",
    ),
    ("registry_policy_entry_boundary_review", "registry_policy_entry_boundary_review_v1.json"),
    (
        "registry_owner_operator_dependency_review",
        "registry_owner_operator_dependency_review_v1.json",
    ),
    (
        "registry_verifier_non_modification_review",
        "registry_verifier_non_modification_review_v1.json",
    ),
    ("registry_non_claims_non_write_review", "registry_non_claims_non_write_review_v1.json"),
    (
        "boundary_object_registry_generation_post_dryrun_review_readiness_decision",
        "boundary_object_registry_generation_post_dryrun_review_readiness_decision_v1.json",
    ),
)


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Boundary Object Registry Generation Post-DryRun Review v1"
    )
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--boundary-object-registry-generation-dryrun-root",
        default=str(DEFAULT_DRYRUN_ROOT),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    result = run_boundary_object_registry_generation_post_dryrun_review_v1(
        boundary_object_registry_generation_dryrun_root=args.boundary_object_registry_generation_dryrun_root,
    )
    for key, filename in OUTPUT_FILES:
        _write_json(output_root / filename, result[key])

    summary = result["summary"]
    print(
        json.dumps(
            {
                "phase": summary.get("phase"),
                "boundary_ok": summary.get("boundary_ok"),
                "final_decision": summary.get("final_decision"),
                "recommended_next_phase": summary.get("recommended_next_phase"),
                "violations": summary.get("violations"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if summary.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
