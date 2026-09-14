#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Validation Engineering Separation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_validation_engineering_separation_planning_v1 import (
    run_midplatform_validation_engineering_separation_planning_v1,
)

DEFAULT_EXPLAIN_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_HIERARCHY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_hierarchy_dryrun_and_review"
)
DEFAULT_AUTH_EXT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)
DEFAULT_OCR_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_planning"
)
DEFAULT_HARNESS_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_FACTORY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "validation_engineering_separation_planning_policy",
        "validation_engineering_separation_planning_policy_v1.json",
    ),
    (
        "upstream_constitution_and_factory_input_review",
        "upstream_constitution_and_factory_input_review_v1.json",
    ),
    (
        "constitution_engineering_role_definition",
        "constitution_engineering_role_definition_v1.json",
    ),
    (
        "validation_engineering_role_definition",
        "validation_engineering_role_definition_v1.json",
    ),
    ("rule_source_to_validator_mapping", "rule_source_to_validator_mapping_v1.json"),
    ("validation_engineering_scope_matrix", "validation_engineering_scope_matrix_v1.json"),
    ("validation_gate_taxonomy", "validation_gate_taxonomy_v1.json"),
    ("validation_issue_traceback_contract", "validation_issue_traceback_contract_v1.json"),
    ("validation_violation_report_contract", "validation_violation_report_contract_v1.json"),
    ("validation_health_check_boundary_plan", "validation_health_check_boundary_plan_v1.json"),
    (
        "validation_authorization_check_boundary_plan",
        "validation_authorization_check_boundary_plan_v1.json",
    ),
    (
        "validation_to_constitution_feedback_loop_plan",
        "validation_to_constitution_feedback_loop_plan_v1.json",
    ),
    (
        "validation_engineering_non_rulemaking_policy",
        "validation_engineering_non_rulemaking_policy_v1.json",
    ),
    (
        "ocr_real_dep_validation_engineering_mapping",
        "ocr_real_dep_validation_engineering_mapping_v1.json",
    ),
    ("validation_engineering_dryrun_plan", "validation_engineering_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "validation_engineering_separation_planning_decision",
        "validation_engineering_separation_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--midplatform-constitution-governance-explanation-dryrun-and-review-root",
        default=DEFAULT_EXPLAIN_DR,
    )
    p.add_argument(
        "--midplatform-constitution-governance-hierarchy-dryrun-and-review-root",
        default=DEFAULT_HIERARCHY_DR,
    )
    p.add_argument(
        "--capability-factory-authorization-standard-extension-dryrun-and-review-root",
        default=DEFAULT_AUTH_EXT_DR,
    )
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-planning-root",
        default=DEFAULT_OCR_PLAN,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_HARNESS_POST,
    )
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-dryrun-and-review-root",
        default=DEFAULT_FACTORY_DR,
    )
    args = p.parse_args()

    result = run_midplatform_validation_engineering_separation_planning_v1(
        midplatform_constitution_governance_explanation_dryrun_and_review_root=(
            args.midplatform_constitution_governance_explanation_dryrun_and_review_root
        ),
        midplatform_constitution_governance_hierarchy_dryrun_and_review_root=(
            args.midplatform_constitution_governance_hierarchy_dryrun_and_review_root
        ),
        capability_factory_authorization_standard_extension_dryrun_and_review_root=(
            args.capability_factory_authorization_standard_extension_dryrun_and_review_root
        ),
        ocr_real_dependency_authorization_via_factory_standard_planning_root=(
            args.ocr_real_dependency_authorization_via_factory_standard_planning_root
        ),
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=(
            args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        ),
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
