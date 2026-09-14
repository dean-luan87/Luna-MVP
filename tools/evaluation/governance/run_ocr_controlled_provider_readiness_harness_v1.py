#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Controlled Provider Readiness Harness extraction v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.controlled_provider_readiness_harness_v1 import (
    run_controlled_provider_readiness_harness_extraction_v1,
)

DEFAULT_REAL_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_post_dryrun_review"
)
DEFAULT_REAL_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_real_dependency_check_dryrun"
)
DEFAULT_REAL_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_real_dependency_check_planning"
)
DEFAULT_SEL_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_post_dryrun_review"
)
DEFAULT_SEL_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_dryrun"
)
DEFAULT_OCR_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("controlled_provider_readiness_harness_policy", "controlled_provider_readiness_harness_policy_v1.json"),
    ("ocr_first_consumer_input_review", "ocr_first_consumer_input_review_v1.json"),
    ("controlled_provider_readiness_harness_contract", "controlled_provider_readiness_harness_contract_v1.json"),
    ("provider_candidate_contract", "provider_candidate_contract_v1.json"),
    ("dependency_readiness_contract", "dependency_readiness_contract_v1.json"),
    ("environment_readiness_contract", "environment_readiness_contract_v1.json"),
    ("provider_comparison_matrix_contract", "provider_comparison_matrix_contract_v1.json"),
    ("real_dependency_check_contract", "real_dependency_check_contract_v1.json"),
    ("provider_evidence_package_contract", "provider_evidence_package_contract_v1.json"),
    ("provider_failure_route_contract", "provider_failure_route_contract_v1.json"),
    ("provider_rollback_contract", "provider_rollback_contract_v1.json"),
    ("provider_boundary_guard_contract", "provider_boundary_guard_contract_v1.json"),
    ("provider_authorization_readiness_contract", "provider_authorization_readiness_contract_v1.json"),
    ("ocr_first_consumer_mapping", "ocr_first_consumer_mapping_v1.json"),
    ("future_consumer_adoption_plan", "future_consumer_adoption_plan_v1.json"),
    ("controlled_provider_readiness_harness_validation_result", (
        "controlled_provider_readiness_harness_validation_result_v1.json"
    )),
    ("controlled_provider_readiness_harness_decision", "controlled_provider_readiness_harness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=DEFAULT_REAL_POST,
    )
    p.add_argument("--ocr-provider-real-dependency-check-dryrun-root", default=DEFAULT_REAL_DRYRUN)
    p.add_argument("--ocr-provider-real-dependency-check-planning-root", default=DEFAULT_REAL_PLANNING)
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-post-dryrun-review-root",
        default=DEFAULT_SEL_POST,
    )
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-dryrun-root",
        default=DEFAULT_SEL_DRYRUN,
    )
    p.add_argument("--ocr-controlled-provider-post-dryrun-review-root", default=DEFAULT_OCR_POST)
    args = p.parse_args()

    result = run_controlled_provider_readiness_harness_extraction_v1(
        ocr_provider_real_dependency_check_post_dryrun_review_root=(
            args.ocr_provider_real_dependency_check_post_dryrun_review_root
        ),
        ocr_provider_real_dependency_check_dryrun_root=args.ocr_provider_real_dependency_check_dryrun_root,
        ocr_provider_real_dependency_check_planning_root=args.ocr_provider_real_dependency_check_planning_root,
        ocr_provider_selection_dependency_environment_post_dryrun_review_root=(
            args.ocr_provider_selection_dependency_environment_post_dryrun_review_root
        ),
        ocr_provider_selection_dependency_environment_dryrun_root=(
            args.ocr_provider_selection_dependency_environment_dryrun_root
        ),
        ocr_controlled_provider_post_dryrun_review_root=args.ocr_controlled_provider_post_dryrun_review_root,
        output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    guide_path = out / "harness_usage_guide_v1.md"
    guide_path.write_text(result["harness_usage_guide_markdown"] + "\n", encoding="utf-8")

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "harness_id": sm.get("harness_id"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
