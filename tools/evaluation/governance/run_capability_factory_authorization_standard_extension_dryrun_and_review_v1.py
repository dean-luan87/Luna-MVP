#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Capability Factory Authorization Standard Extension DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.capability_factory_authorization_standard_extension_dryrun_and_review_v1 import (
    run_capability_factory_authorization_standard_extension_dryrun_and_review_v1,
)

DEFAULT_AUTH_EXT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_planning"
)
DEFAULT_HIERARCHY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_hierarchy_dryrun_and_review"
)
DEFAULT_FACTORY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)
DEFAULT_OCR_AUTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_authorization_planning"
)
DEFAULT_ROUTE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_authorization_next_route_decision"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "factory_authorization_standard_extension_dryrun_and_review_policy",
        "factory_authorization_standard_extension_dryrun_and_review_policy_v1.json",
    ),
    (
        "authorization_standard_extension_planning_input_review",
        "authorization_standard_extension_planning_input_review_v1.json",
    ),
    ("constitution_hierarchy_input_review", "constitution_hierarchy_input_review_v1.json"),
    (
        "authorization_standard_extension_candidate",
        "authorization_standard_extension_candidate_v1.json",
    ),
    ("authorization_scope_standard_review", "authorization_scope_standard_review_v1.json"),
    (
        "request_grant_execution_window_standard_review",
        "request_grant_execution_window_standard_review_v1.json",
    ),
    (
        "allowed_forbidden_action_matrix_standard_review",
        "allowed_forbidden_action_matrix_standard_review_v1.json",
    ),
    (
        "owner_operator_approval_standard_review",
        "owner_operator_approval_standard_review_v1.json",
    ),
    ("post_execution_review_standard_review", "post_execution_review_standard_review_v1.json"),
    ("revocation_rollback_standard_review", "revocation_rollback_standard_review_v1.json"),
    (
        "ocr_real_dep_domain_config_consumption_review",
        "ocr_real_dep_domain_config_consumption_review_v1.json",
    ),
    (
        "factory_standard_ten_category_integration_review",
        "factory_standard_ten_category_integration_review_v1.json",
    ),
    ("constitution_mapping_review", "constitution_mapping_review_v1.json"),
    ("authorization_standard_boundary_audit", "authorization_standard_boundary_audit_v1.json"),
    (
        "authorization_standard_blocked_path_result",
        "authorization_standard_blocked_path_result_v1.json",
    ),
    (
        "authorization_standard_extension_closure_decision",
        "authorization_standard_extension_closure_decision_v1.json",
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
        "--capability-factory-authorization-standard-extension-planning-root",
        default=DEFAULT_AUTH_EXT,
    )
    p.add_argument(
        "--midplatform-constitution-governance-hierarchy-dryrun-and-review-root",
        default=DEFAULT_HIERARCHY_DR,
    )
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-dryrun-and-review-root",
        default=DEFAULT_FACTORY_DR,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-authorization-planning-root",
        default=DEFAULT_OCR_AUTH,
    )
    p.add_argument(
        "--ocr-authorization-next-route-decision-root",
        default=DEFAULT_ROUTE,
    )
    args = p.parse_args()

    result = run_capability_factory_authorization_standard_extension_dryrun_and_review_v1(
        capability_factory_authorization_standard_extension_planning_root=(
            args.capability_factory_authorization_standard_extension_planning_root
        ),
        midplatform_constitution_governance_hierarchy_dryrun_and_review_root=(
            args.midplatform_constitution_governance_hierarchy_dryrun_and_review_root
        ),
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
        ),
        ocr_provider_real_dependency_check_authorization_planning_root=(
            args.ocr_provider_real_dependency_check_authorization_planning_root
        ),
        ocr_authorization_next_route_decision_root=args.ocr_authorization_next_route_decision_root,
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
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
