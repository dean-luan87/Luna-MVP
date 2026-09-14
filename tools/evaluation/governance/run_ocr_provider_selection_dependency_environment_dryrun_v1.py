#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Selection / Dependency / Environment DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_selection_dependency_environment_dryrun_v1 import (
    run_ocr_provider_selection_dependency_environment_dryrun_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_planning"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_controlled_provider_authorization_roadmap_decision"
)
DEFAULT_POST_REVIEW = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_post_dryrun_review"
)
DEFAULT_OCR_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_controlled_provider_dryrun"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "ocr_provider_selection_dependency_environment_dryrun_policy",
        "ocr_provider_selection_dependency_environment_dryrun_policy_v1.json",
    ),
    ("provider_selection_planning_input_review", "provider_selection_planning_input_review_v1.json"),
    ("provider_selection_candidate", "provider_selection_candidate_v1.json"),
    ("dependency_readiness_candidate_matrix", "dependency_readiness_candidate_matrix_v1.json"),
    ("environment_readiness_candidate", "environment_readiness_candidate_v1.json"),
    ("provider_comparison_matrix_sample", "provider_comparison_matrix_sample_v1.json"),
    ("provider_cost_latency_resource_sample", "provider_cost_latency_resource_sample_v1.json"),
    ("provider_capability_fit_sample", "provider_capability_fit_sample_v1.json"),
    ("provider_health_binding_dryrun_result", "provider_health_binding_dryrun_result_v1.json"),
    ("provider_fallback_strategy_dryrun_result", "provider_fallback_strategy_dryrun_result_v1.json"),
    ("provider_security_boundary_dryrun_result", "provider_security_boundary_dryrun_result_v1.json"),
    ("provider_no_import_no_install_audit", "provider_no_import_no_install_audit_v1.json"),
    ("provider_selection_blocked_path_result", "provider_selection_blocked_path_result_v1.json"),
    ("provider_selection_dryrun_readiness_decision", "provider_selection_dryrun_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-planning-root",
        default=DEFAULT_PLANNING,
    )
    p.add_argument(
        "--ocr-controlled-provider-authorization-roadmap-decision-root",
        default=DEFAULT_ROADMAP,
    )
    p.add_argument("--ocr-controlled-provider-post-dryrun-review-root", default=DEFAULT_POST_REVIEW)
    p.add_argument("--ocr-controlled-provider-dryrun-root", default=DEFAULT_OCR_DRYRUN)
    args = p.parse_args()

    result = run_ocr_provider_selection_dependency_environment_dryrun_v1(
        ocr_provider_selection_dependency_environment_planning_root=(
            args.ocr_provider_selection_dependency_environment_planning_root
        ),
        ocr_controlled_provider_authorization_roadmap_decision_root=(
            args.ocr_controlled_provider_authorization_roadmap_decision_root
        ),
        ocr_controlled_provider_post_dryrun_review_root=args.ocr_controlled_provider_post_dryrun_review_root,
        ocr_controlled_provider_dryrun_root=args.ocr_controlled_provider_dryrun_root,
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
