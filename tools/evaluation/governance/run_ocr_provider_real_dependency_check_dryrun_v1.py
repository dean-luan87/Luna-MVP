#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Real Dependency Check DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_real_dependency_check_dryrun_v1 import (
    run_ocr_provider_real_dependency_check_dryrun_v1,
)

DEFAULT_PLANNING = (
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
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_real_dependency_check_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_real_dependency_check_dryrun_policy", "ocr_real_dependency_check_dryrun_policy_v1.json"),
    ("real_dependency_check_planning_input_review", "real_dependency_check_planning_input_review_v1.json"),
    ("dependency_check_sequence_dryrun_result", "dependency_check_sequence_dryrun_result_v1.json"),
    ("paddleocr_dependency_check_dryrun_result", "paddleocr_dependency_check_dryrun_result_v1.json"),
    ("rapidocr_dependency_check_dryrun_result", "rapidocr_dependency_check_dryrun_result_v1.json"),
    ("external_ocr_dependency_check_dryrun_result", "external_ocr_dependency_check_dryrun_result_v1.json"),
    ("evidence_package_candidate", "evidence_package_candidate_v1.json"),
    ("failure_route_candidate_matrix", "failure_route_candidate_matrix_v1.json"),
    ("rollback_plan_candidate_result", "rollback_plan_candidate_result_v1.json"),
    ("environment_isolation_boundary_dryrun_result", "environment_isolation_boundary_dryrun_result_v1.json"),
    ("future_execution_gate_dryrun_result", "future_execution_gate_dryrun_result_v1.json"),
    ("real_dependency_check_blocked_path_result", "real_dependency_check_blocked_path_result_v1.json"),
    ("real_dependency_check_no_execution_audit", "real_dependency_check_no_execution_audit_v1.json"),
    ("real_dependency_check_dryrun_readiness_decision", "real_dependency_check_dryrun_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--ocr-provider-real-dependency-check-planning-root", default=DEFAULT_PLANNING)
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

    result = run_ocr_provider_real_dependency_check_dryrun_v1(
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
