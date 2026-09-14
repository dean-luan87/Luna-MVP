#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Real Dependency Authorization via Factory Standard DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_dryrun_and_review_v1 import (
    run_ocr_provider_real_dependency_check_authorization_via_factory_standard_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_planning"
)
DEFAULT_EXPLAIN_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_AUTH_EXT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)
DEFAULT_HARNESS_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_LEGACY_AUTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_authorization_planning"
)
DEFAULT_LEGACY_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "ocr_real_dependency_authorization_via_factory_standard_dryrun_review_policy",
        "ocr_real_dependency_authorization_via_factory_standard_dryrun_review_policy_v1.json",
    ),
    ("planning_input_review", "planning_input_review_v1.json"),
    ("ocr_real_dependency_domain_config_candidate", "ocr_real_dependency_domain_config_candidate_v1.json"),
    ("ocr_constitution_consumption_review", "ocr_constitution_consumption_review_v1.json"),
    (
        "factory_authorization_standard_consumption_review",
        "factory_authorization_standard_consumption_review_v1.json",
    ),
    ("validation_factory_consumption_review", "validation_factory_consumption_review_v1.json"),
    (
        "controlled_provider_readiness_harness_consumption_review",
        "controlled_provider_readiness_harness_consumption_review_v1.json",
    ),
    ("allowed_check_domain_config_dryrun_review", "allowed_check_domain_config_dryrun_review_v1.json"),
    ("forbidden_action_domain_config_dryrun_review", "forbidden_action_domain_config_dryrun_review_v1.json"),
    ("evidence_rollback_ref_binding_review", "evidence_rollback_ref_binding_review_v1.json"),
    ("provider_candidate_ref_binding_review", "provider_candidate_ref_binding_review_v1.json"),
    ("no_generic_logic_redefinition_review", "no_generic_logic_redefinition_review_v1.json"),
    ("standard_reuse_enforcement_review", "standard_reuse_enforcement_review_v1.json"),
    (
        "optional_legacy_real_dep_post_review_binding",
        "optional_legacy_real_dep_post_review_binding_v1.json",
    ),
    ("ocr_real_dep_via_factory_standard_boundary_audit", "ocr_real_dep_via_factory_standard_boundary_audit_v1.json"),
    (
        "ocr_real_dep_via_factory_standard_blocked_path_result",
        "ocr_real_dep_via_factory_standard_blocked_path_result_v1.json",
    ),
    ("ocr_real_dep_via_factory_standard_closure_decision", "ocr_real_dep_via_factory_standard_closure_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-planning-root",
        default=DEFAULT_PLAN,
    )
    p.add_argument(
        "--midplatform-constitution-governance-explanation-dryrun-and-review-root",
        default=DEFAULT_EXPLAIN_DR,
    )
    p.add_argument(
        "--capability-factory-authorization-standard-extension-dryrun-and-review-root",
        default=DEFAULT_AUTH_EXT_DR,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_HARNESS_POST,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-authorization-planning-root",
        default=DEFAULT_LEGACY_AUTH,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=DEFAULT_LEGACY_POST,
    )
    args = p.parse_args()

    result = run_ocr_provider_real_dependency_check_authorization_via_factory_standard_dryrun_and_review_v1(
        ocr_real_dependency_authorization_via_factory_standard_planning_root=(
            args.ocr_real_dependency_authorization_via_factory_standard_planning_root
        ),
        midplatform_constitution_governance_explanation_dryrun_and_review_root=(
            args.midplatform_constitution_governance_explanation_dryrun_and_review_root
        ),
        capability_factory_authorization_standard_extension_dryrun_and_review_root=(
            args.capability_factory_authorization_standard_extension_dryrun_and_review_root
        ),
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=(
            args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        ),
        ocr_provider_real_dependency_check_authorization_planning_root=(
            args.ocr_provider_real_dependency_check_authorization_planning_root
        ),
        ocr_provider_real_dependency_check_post_dryrun_review_root=(
            args.ocr_provider_real_dependency_check_post_dryrun_review_root
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "candidate_generated": sm.get("ocr_domain_config_candidate_generated_now"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
