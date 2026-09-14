#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Validation Engineering Separation DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    run_midplatform_validation_engineering_separation_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_planning"
)
DEFAULT_EXPLAIN_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_OCR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_AUTH_EXT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)
DEFAULT_HARNESS_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "validation_engineering_separation_dryrun_and_review_policy",
        "validation_engineering_separation_dryrun_and_review_policy_v1.json",
    ),
    (
        "validation_engineering_planning_input_review",
        "validation_engineering_planning_input_review_v1.json",
    ),
    (
        "validation_engineering_model_candidate",
        "validation_engineering_model_candidate_v1.json",
    ),
    (
        "constitution_engineering_role_review",
        "constitution_engineering_role_review_v1.json",
    ),
    (
        "validation_engineering_role_review",
        "validation_engineering_role_review_v1.json",
    ),
    (
        "rule_source_to_validator_mapping_review",
        "rule_source_to_validator_mapping_review_v1.json",
    ),
    (
        "validation_engineering_scope_matrix_review",
        "validation_engineering_scope_matrix_review_v1.json",
    ),
    ("validation_gate_taxonomy_review", "validation_gate_taxonomy_review_v1.json"),
    (
        "ocr_real_dep_validation_path_dryrun_review",
        "ocr_real_dep_validation_path_dryrun_review_v1.json",
    ),
    ("issue_traceback_contract_review", "issue_traceback_contract_review_v1.json"),
    ("violation_report_contract_review", "violation_report_contract_review_v1.json"),
    (
        "health_check_consumption_boundary_review",
        "health_check_consumption_boundary_review_v1.json",
    ),
    (
        "authorization_check_boundary_review",
        "authorization_check_boundary_review_v1.json",
    ),
    (
        "validation_to_constitution_feedback_loop_review",
        "validation_to_constitution_feedback_loop_review_v1.json",
    ),
    (
        "validation_engineering_non_rulemaking_review",
        "validation_engineering_non_rulemaking_review_v1.json",
    ),
    (
        "validation_engineering_boundary_audit",
        "validation_engineering_boundary_audit_v1.json",
    ),
    (
        "validation_engineering_blocked_path_result",
        "validation_engineering_blocked_path_result_v1.json",
    ),
    (
        "validation_engineering_closure_decision",
        "validation_engineering_closure_decision_v1.json",
    ),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--midplatform-validation-engineering-separation-planning-root",
        default=DEFAULT_PLAN,
    )
    p.add_argument(
        "--midplatform-constitution-governance-explanation-dryrun-and-review-root",
        default=DEFAULT_EXPLAIN_DR,
    )
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-dryrun-and-review-root",
        default=DEFAULT_OCR_DR,
    )
    p.add_argument(
        "--capability-factory-authorization-standard-extension-dryrun-and-review-root",
        default=DEFAULT_AUTH_EXT_DR,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_HARNESS_POST,
    )
    args = p.parse_args()

    result = run_midplatform_validation_engineering_separation_dryrun_and_review_v1(
        midplatform_validation_engineering_separation_planning_root=(
            args.midplatform_validation_engineering_separation_planning_root
        ),
        midplatform_constitution_governance_explanation_dryrun_and_review_root=(
            args.midplatform_constitution_governance_explanation_dryrun_and_review_root
        ),
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=(
            args.ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        ),
        capability_factory_authorization_standard_extension_dryrun_and_review_root=(
            args.capability_factory_authorization_standard_extension_dryrun_and_review_root
        ),
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=(
            args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
