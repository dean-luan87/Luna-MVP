#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Real Dependency Execution Authorization Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_execution_authorization_roadmap_decision_v1 import (
    run_ocr_real_dependency_execution_authorization_roadmap_decision_v1,
)

DEFAULT_VAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_OCR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_OCR_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_planning"
)
DEFAULT_AUTH_EXT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)
DEFAULT_EXPLAIN_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_HARNESS_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_roadmap_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "ocr_real_dependency_execution_authorization_roadmap_policy",
        "ocr_real_dependency_execution_authorization_roadmap_policy_v1.json",
    ),
    (
        "validation_engineering_separation_input_review",
        "validation_engineering_separation_input_review_v1.json",
    ),
    (
        "ocr_real_dep_via_factory_standard_input_review",
        "ocr_real_dep_via_factory_standard_input_review_v1.json",
    ),
    (
        "execution_authorization_readiness_review",
        "execution_authorization_readiness_review_v1.json",
    ),
    (
        "route_a_execution_authorization_planning_assessment",
        "route_a_execution_authorization_planning_assessment_v1.json",
    ),
    (
        "route_b_provider_selection_finalize_assessment",
        "route_b_provider_selection_finalize_assessment_v1.json",
    ),
    (
        "route_c_validation_runtime_activation_assessment",
        "route_c_validation_runtime_activation_assessment_v1.json",
    ),
    (
        "route_d_health_readiness_baseline_assessment",
        "route_d_health_readiness_baseline_assessment_v1.json",
    ),
    (
        "route_e_return_visual_context_governance_assessment",
        "route_e_return_visual_context_governance_assessment_v1.json",
    ),
    (
        "ocr_real_dependency_execution_authorization_route_selection_matrix",
        "ocr_real_dependency_execution_authorization_route_selection_matrix_v1.json",
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
        "--midplatform-validation-engineering-separation-dryrun-and-review-root",
        default=DEFAULT_VAL_DR,
    )
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-dryrun-and-review-root",
        default=DEFAULT_OCR_DR,
    )
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-planning-root",
        default=DEFAULT_OCR_PLAN,
    )
    p.add_argument(
        "--capability-factory-authorization-standard-extension-dryrun-and-review-root",
        default=DEFAULT_AUTH_EXT_DR,
    )
    p.add_argument(
        "--midplatform-constitution-governance-explanation-dryrun-and-review-root",
        default=DEFAULT_EXPLAIN_DR,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_HARNESS_POST,
    )
    args = p.parse_args()

    result = run_ocr_real_dependency_execution_authorization_roadmap_decision_v1(
        midplatform_validation_engineering_separation_dryrun_and_review_root=(
            args.midplatform_validation_engineering_separation_dryrun_and_review_root
        ),
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=(
            args.ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        ),
        ocr_real_dependency_authorization_via_factory_standard_planning_root=(
            args.ocr_real_dependency_authorization_via_factory_standard_planning_root
        ),
        capability_factory_authorization_standard_extension_dryrun_and_review_root=(
            args.capability_factory_authorization_standard_extension_dryrun_and_review_root
        ),
        midplatform_constitution_governance_explanation_dryrun_and_review_root=(
            args.midplatform_constitution_governance_explanation_dryrun_and_review_root
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
