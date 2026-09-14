#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Real Dependency Check Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_real_dependency_check_planning_v1 import (
    run_ocr_provider_real_dependency_check_planning_v1,
)

DEFAULT_POST_REVIEW = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_post_dryrun_review"
)
DEFAULT_SEL_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_dryrun"
)
DEFAULT_SEL_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_planning"
)
DEFAULT_OCR_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_real_dependency_check_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_real_dependency_check_planning_policy", "ocr_real_dependency_check_planning_policy_v1.json"),
    ("provider_selection_post_review_input_review", "provider_selection_post_review_input_review_v1.json"),
    ("real_dependency_check_scope", "real_dependency_check_scope_v1.json"),
    ("provider_dependency_check_sequence_plan", "provider_dependency_check_sequence_plan_v1.json"),
    ("paddleocr_real_dependency_check_plan", "paddleocr_real_dependency_check_plan_v1.json"),
    ("rapidocr_real_dependency_check_plan", "rapidocr_real_dependency_check_plan_v1.json"),
    ("external_ocr_real_dependency_check_plan", "external_ocr_real_dependency_check_plan_v1.json"),
    ("model_cache_and_file_integrity_check_plan", "model_cache_and_file_integrity_check_plan_v1.json"),
    ("import_check_authorization_boundary_plan", "import_check_authorization_boundary_plan_v1.json"),
    ("environment_isolation_and_sandbox_plan", "environment_isolation_and_sandbox_plan_v1.json"),
    ("evidence_package_plan", "evidence_package_plan_v1.json"),
    ("failure_handling_and_rollback_plan", "failure_handling_and_rollback_plan_v1.json"),
    ("real_dependency_check_blocked_path_matrix", "real_dependency_check_blocked_path_matrix_v1.json"),
    ("real_dependency_check_future_execution_gate", "real_dependency_check_future_execution_gate_v1.json"),
    ("real_dependency_check_non_claims_register", "real_dependency_check_non_claims_register_v1.json"),
    ("real_dependency_check_planning_decision", "real_dependency_check_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-post-dryrun-review-root",
        default=DEFAULT_POST_REVIEW,
    )
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-dryrun-root",
        default=DEFAULT_SEL_DRYRUN,
    )
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-planning-root",
        default=DEFAULT_SEL_PLANNING,
    )
    p.add_argument(
        "--ocr-controlled-provider-post-dryrun-review-root",
        default=DEFAULT_OCR_POST,
    )
    args = p.parse_args()

    result = run_ocr_provider_real_dependency_check_planning_v1(
        ocr_provider_selection_dependency_environment_post_dryrun_review_root=(
            args.ocr_provider_selection_dependency_environment_post_dryrun_review_root
        ),
        ocr_provider_selection_dependency_environment_dryrun_root=(
            args.ocr_provider_selection_dependency_environment_dryrun_root
        ),
        ocr_provider_selection_dependency_environment_planning_root=(
            args.ocr_provider_selection_dependency_environment_planning_root
        ),
        ocr_controlled_provider_post_dryrun_review_root=args.ocr_controlled_provider_post_dryrun_review_root,
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
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
