#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Capability Factory Authorization Standard Extension Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    run_capability_factory_authorization_standard_extension_planning_v1,
)

DEFAULT_FACTORY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)
DEFAULT_LIFECYCLE_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "compressed_ocr_authorization_lifecycle_dryrun_and_review"
)
DEFAULT_CLEANUP_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
)
DEFAULT_ROUTE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_authorization_next_route_decision"
)
DEFAULT_OCR_AUTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_authorization_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "factory_authorization_standard_extension_planning_policy",
        "factory_authorization_standard_extension_planning_policy_v1.json",
    ),
    ("factory_standard_upstream_input_review", "factory_standard_upstream_input_review_v1.json"),
    ("authorization_standard_contract_outline", "authorization_standard_contract_outline_v1.json"),
    ("authorization_scope_standard_plan", "authorization_scope_standard_plan_v1.json"),
    (
        "authorization_request_contract_standard_plan",
        "authorization_request_contract_standard_plan_v1.json",
    ),
    ("authorization_grant_contract_standard_plan", "authorization_grant_contract_standard_plan_v1.json"),
    (
        "authorization_execution_window_contract_standard_plan",
        "authorization_execution_window_contract_standard_plan_v1.json",
    ),
    ("authorization_action_matrix_standard_plan", "authorization_action_matrix_standard_plan_v1.json"),
    (
        "authorization_owner_operator_approval_standard_plan",
        "authorization_owner_operator_approval_standard_plan_v1.json",
    ),
    (
        "authorization_post_execution_review_standard_plan",
        "authorization_post_execution_review_standard_plan_v1.json",
    ),
    (
        "authorization_revocation_rollback_standard_plan",
        "authorization_revocation_rollback_standard_plan_v1.json",
    ),
    ("authorization_standard_absorption_inventory", "authorization_standard_absorption_inventory_v1.json"),
    (
        "ocr_real_dependency_check_domain_config_template",
        "ocr_real_dependency_check_domain_config_template_v1.json",
    ),
    ("ten_standards_contract_outline", "ten_standards_contract_outline_v1.json"),
    ("route_adjustment_decision", "route_adjustment_decision_v1.json"),
    ("authorization_standard_extension_dryrun_plan", "authorization_standard_extension_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "authorization_standard_extension_planning_decision",
        "authorization_standard_extension_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-dryrun-and-review-root",
        default=DEFAULT_FACTORY_DR,
    )
    p.add_argument(
        "--compressed-ocr-authorization-lifecycle-dryrun-and-review-root",
        default=DEFAULT_LIFECYCLE_DR,
    )
    p.add_argument(
        "--factory-standard-historical-redundancy-cleanup-dryrun-and-review-root",
        default=DEFAULT_CLEANUP_DR,
    )
    p.add_argument("--ocr-authorization-next-route-decision-root", default=DEFAULT_ROUTE)
    p.add_argument(
        "--ocr-provider-real-dependency-check-authorization-planning-root",
        default=DEFAULT_OCR_AUTH,
    )
    args = p.parse_args()

    result = run_capability_factory_authorization_standard_extension_planning_v1(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
        ),
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root=(
            args.compressed_ocr_authorization_lifecycle_dryrun_and_review_root
        ),
        factory_standard_historical_redundancy_cleanup_dryrun_and_review_root=(
            args.factory_standard_historical_redundancy_cleanup_dryrun_and_review_root
        ),
        ocr_authorization_next_route_decision_root=args.ocr_authorization_next_route_decision_root,
        ocr_provider_real_dependency_check_authorization_planning_root=(
            args.ocr_provider_real_dependency_check_authorization_planning_root
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
                "next_ocr_phase": sm.get("next_ocr_phase_after_extension"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
