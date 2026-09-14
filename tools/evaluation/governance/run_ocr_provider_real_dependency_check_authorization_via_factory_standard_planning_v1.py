#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Real Dependency Authorization via Factory Standard Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1 import (
    run_ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1,
)

DEFAULT_EXPLAIN_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_AUTH_EXT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)
DEFAULT_HIERARCHY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_hierarchy_dryrun_and_review"
)
DEFAULT_LEGACY_AUTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_authorization_planning"
)
DEFAULT_ROUTE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_authorization_next_route_decision"
)
DEFAULT_REAL_DEP_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_post_dryrun_review"
)
DEFAULT_HARNESS_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "ocr_real_dependency_authorization_via_factory_standard_planning_policy",
        "ocr_real_dependency_authorization_via_factory_standard_planning_policy_v1.json",
    ),
    ("constitution_explanation_input_review", "constitution_explanation_input_review_v1.json"),
    (
        "factory_authorization_standard_input_review",
        "factory_authorization_standard_input_review_v1.json",
    ),
    (
        "ocr_real_dependency_authorization_governance_path",
        "ocr_real_dependency_authorization_governance_path_v1.json",
    ),
    (
        "ocr_real_dependency_domain_config_contract",
        "ocr_real_dependency_domain_config_contract_v1.json",
    ),
    (
        "ocr_real_dependency_domain_config_candidate_plan",
        "ocr_real_dependency_domain_config_candidate_plan_v1.json",
    ),
    ("ocr_constitution_binding_plan", "ocr_constitution_binding_plan_v1.json"),
    (
        "factory_authorization_standard_binding_plan",
        "factory_authorization_standard_binding_plan_v1.json",
    ),
    ("validation_factory_binding_plan", "validation_factory_binding_plan_v1.json"),
    (
        "controlled_provider_readiness_harness_binding_plan",
        "controlled_provider_readiness_harness_binding_plan_v1.json",
    ),
    ("allowed_check_domain_config_plan", "allowed_check_domain_config_plan_v1.json"),
    ("forbidden_action_domain_config_plan", "forbidden_action_domain_config_plan_v1.json"),
    (
        "evidence_and_rollback_ref_binding_plan",
        "evidence_and_rollback_ref_binding_plan_v1.json",
    ),
    ("provider_candidate_ref_binding_plan", "provider_candidate_ref_binding_plan_v1.json"),
    ("no_generic_logic_redefinition_policy", "no_generic_logic_redefinition_policy_v1.json"),
    ("standard_reuse_enforcement_plan", "standard_reuse_enforcement_plan_v1.json"),
    (
        "ocr_real_dep_via_factory_standard_blocked_path_matrix",
        "ocr_real_dep_via_factory_standard_blocked_path_matrix_v1.json",
    ),
    (
        "ocr_real_dep_via_factory_standard_dryrun_plan",
        "ocr_real_dep_via_factory_standard_dryrun_plan_v1.json",
    ),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "ocr_real_dependency_authorization_via_factory_standard_planning_decision",
        "ocr_real_dependency_authorization_via_factory_standard_planning_decision_v1.json",
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
        "--capability-factory-authorization-standard-extension-dryrun-and-review-root",
        default=DEFAULT_AUTH_EXT_DR,
    )
    p.add_argument(
        "--midplatform-constitution-governance-hierarchy-dryrun-and-review-root",
        default=DEFAULT_HIERARCHY_DR,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-authorization-planning-root",
        default=DEFAULT_LEGACY_AUTH,
    )
    p.add_argument("--ocr-authorization-next-route-decision-root", default=DEFAULT_ROUTE)
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=DEFAULT_REAL_DEP_POST,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_HARNESS_POST,
    )
    args = p.parse_args()

    result = run_ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1(
        midplatform_constitution_governance_explanation_dryrun_and_review_root=(
            args.midplatform_constitution_governance_explanation_dryrun_and_review_root
        ),
        capability_factory_authorization_standard_extension_dryrun_and_review_root=(
            args.capability_factory_authorization_standard_extension_dryrun_and_review_root
        ),
        midplatform_constitution_governance_hierarchy_dryrun_and_review_root=(
            args.midplatform_constitution_governance_hierarchy_dryrun_and_review_root
        ),
        ocr_provider_real_dependency_check_authorization_planning_root=(
            args.ocr_provider_real_dependency_check_authorization_planning_root
        ),
        ocr_authorization_next_route_decision_root=args.ocr_authorization_next_route_decision_root,
        ocr_provider_real_dependency_check_post_dryrun_review_root=(
            args.ocr_provider_real_dependency_check_post_dryrun_review_root
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
