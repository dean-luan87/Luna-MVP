#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Real Dependency Check Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_real_dependency_check_authorization_planning_v1 import (
    run_ocr_provider_real_dependency_check_authorization_planning_v1,
)

DEFAULT_ROUTE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_authorization_next_route_decision"
)
DEFAULT_REAL_DEP_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_post_dryrun_review"
)
DEFAULT_REAL_DEP_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_real_dependency_check_dryrun"
)
DEFAULT_REAL_DEP_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_real_dependency_check_planning"
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
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_authorization_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "real_dependency_check_authorization_planning_policy",
        "real_dependency_check_authorization_planning_policy_v1.json",
    ),
    ("ocr_authorization_next_route_input_review", "ocr_authorization_next_route_input_review_v1.json"),
    ("real_dependency_check_authorization_scope", "real_dependency_check_authorization_scope_v1.json"),
    (
        "real_dependency_check_authorization_request_contract",
        "real_dependency_check_authorization_request_contract_v1.json",
    ),
    ("real_dependency_check_grant_contract", "real_dependency_check_grant_contract_v1.json"),
    (
        "real_dependency_check_execution_window_contract",
        "real_dependency_check_execution_window_contract_v1.json",
    ),
    (
        "allowed_dependency_check_action_matrix",
        "allowed_dependency_check_action_matrix_v1.json",
    ),
    (
        "forbidden_dependency_check_action_matrix",
        "forbidden_dependency_check_action_matrix_v1.json",
    ),
    ("real_dependency_check_sandbox_boundary_plan", "real_dependency_check_sandbox_boundary_plan_v1.json"),
    ("real_dependency_check_evidence_requirement", "real_dependency_check_evidence_requirement_v1.json"),
    ("real_dependency_check_rollback_policy", "real_dependency_check_rollback_policy_v1.json"),
    ("owner_operator_approval_policy", "owner_operator_approval_policy_v1.json"),
    ("provider_selection_non_finalize_binding", "provider_selection_non_finalize_binding_v1.json"),
    (
        "real_dependency_check_authorization_state_machine",
        "real_dependency_check_authorization_state_machine_v1.json",
    ),
    (
        "real_dependency_check_authorization_blocked_path_matrix",
        "real_dependency_check_authorization_blocked_path_matrix_v1.json",
    ),
    (
        "real_dependency_check_authorization_dryrun_plan",
        "real_dependency_check_authorization_dryrun_plan_v1.json",
    ),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "real_dependency_check_authorization_planning_decision",
        "real_dependency_check_authorization_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--ocr-authorization-next-route-decision-root", default=DEFAULT_ROUTE)
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=DEFAULT_REAL_DEP_POST,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-dryrun-root",
        default=DEFAULT_REAL_DEP_DRYRUN,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-planning-root",
        default=DEFAULT_REAL_DEP_PLAN,
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
    args = p.parse_args()

    result = run_ocr_provider_real_dependency_check_authorization_planning_v1(
        ocr_authorization_next_route_decision_root=args.ocr_authorization_next_route_decision_root,
        ocr_provider_real_dependency_check_post_dryrun_review_root=(
            args.ocr_provider_real_dependency_check_post_dryrun_review_root
        ),
        ocr_provider_real_dependency_check_dryrun_root=args.ocr_provider_real_dependency_check_dryrun_root,
        ocr_provider_real_dependency_check_planning_root=args.ocr_provider_real_dependency_check_planning_root,
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root=(
            args.compressed_ocr_authorization_lifecycle_dryrun_and_review_root
        ),
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
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
                "current_state": sm.get("current_state"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
