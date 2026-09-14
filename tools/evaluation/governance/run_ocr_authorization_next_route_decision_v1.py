#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Authorization Next Route Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_authorization_next_route_decision_v1 import (
    run_ocr_authorization_next_route_decision_v1,
)

DEFAULT_CLEANUP_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
)
DEFAULT_LIFECYCLE_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "compressed_ocr_authorization_lifecycle_dryrun_and_review"
)
DEFAULT_FACTORY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)
DEFAULT_FACTORY_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_REAL_DEP_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_post_dryrun_review"
)
DEFAULT_SELECTION_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_authorization_next_route_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_authorization_next_route_decision_policy", "ocr_authorization_next_route_decision_policy_v1.json"),
    ("cleanup_dryrun_review_input_review", "cleanup_dryrun_review_input_review_v1.json"),
    ("compressed_lifecycle_readiness_review", "compressed_lifecycle_readiness_review_v1.json"),
    ("ocr_provider_readiness_state_review", "ocr_provider_readiness_state_review_v1.json"),
    (
        "route_a_real_dependency_check_authorization_assessment",
        "route_a_real_dependency_check_authorization_assessment_v1.json",
    ),
    (
        "route_b_provider_selection_finalize_assessment",
        "route_b_provider_selection_finalize_assessment_v1.json",
    ),
    (
        "route_c_controlled_trial_authorization_assessment",
        "route_c_controlled_trial_authorization_assessment_v1.json",
    ),
    (
        "route_d_return_visual_context_governance_assessment",
        "route_d_return_visual_context_governance_assessment_v1.json",
    ),
    (
        "ocr_authorization_next_route_selection_matrix",
        "ocr_authorization_next_route_selection_matrix_v1.json",
    ),
    ("selected_route_preconditions", "selected_route_preconditions_v1.json"),
    ("deferred_routes_register", "deferred_routes_register_v1.json"),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--factory-standard-historical-redundancy-cleanup-dryrun-and-review-root",
        default=DEFAULT_CLEANUP_DR,
    )
    p.add_argument(
        "--compressed-ocr-authorization-lifecycle-dryrun-and-review-root",
        default=DEFAULT_LIFECYCLE_DR,
    )
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-dryrun-and-review-root",
        default=DEFAULT_FACTORY_DR,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_FACTORY_POST,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=DEFAULT_REAL_DEP_POST,
    )
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-post-dryrun-review-root",
        default=DEFAULT_SELECTION_POST,
    )
    args = p.parse_args()

    result = run_ocr_authorization_next_route_decision_v1(
        factory_standard_historical_redundancy_cleanup_dryrun_and_review_root=(
            args.factory_standard_historical_redundancy_cleanup_dryrun_and_review_root
        ),
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root=(
            args.compressed_ocr_authorization_lifecycle_dryrun_and_review_root
        ),
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
        ),
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=(
            args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        ),
        ocr_provider_real_dependency_check_post_dryrun_review_root=(
            args.ocr_provider_real_dependency_check_post_dryrun_review_root
        ),
        ocr_provider_selection_dependency_environment_post_dryrun_review_root=(
            args.ocr_provider_selection_dependency_environment_post_dryrun_review_root
        ),
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
                "selected_route": sm.get("selected_route"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
