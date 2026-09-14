#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Capability Factory Admission and Operation Standard DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.capability_factory_admission_and_operation_standard_dryrun_and_review_v1 import (
    run_capability_factory_admission_and_operation_standard_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_planning"
)
DEFAULT_FORMAL = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_formal_request_artifact_generation_planning"
)
DEFAULT_REQ_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_post_dryrun_review"
)
DEFAULT_REQ_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_dryrun"
)
DEFAULT_FACTORY_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_VF = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "capability_factory_standard_dryrun_and_review_policy",
        "capability_factory_standard_dryrun_and_review_policy_v1.json",
    ),
    ("factory_standard_planning_input_review", "factory_standard_planning_input_review_v1.json"),
    ("candidate_standard_dryrun_review", "candidate_standard_dryrun_review_v1.json"),
    ("artifact_standard_dryrun_review", "artifact_standard_dryrun_review_v1.json"),
    ("lifecycle_standard_dryrun_review", "lifecycle_standard_dryrun_review_v1.json"),
    ("boundary_standard_dryrun_review", "boundary_standard_dryrun_review_v1.json"),
    ("evidence_standard_dryrun_review", "evidence_standard_dryrun_review_v1.json"),
    ("approval_grant_standard_dryrun_review", "approval_grant_standard_dryrun_review_v1.json"),
    ("sandbox_rollback_standard_dryrun_review", "sandbox_rollback_standard_dryrun_review_v1.json"),
    ("provider_machine_standard_dryrun_review", "provider_machine_standard_dryrun_review_v1.json"),
    (
        "upstream_downstream_transfer_standard_dryrun_review",
        "upstream_downstream_transfer_standard_dryrun_review_v1.json",
    ),
    (
        "factory_role_responsibility_standard_review",
        "factory_role_responsibility_standard_review_v1.json",
    ),
    ("ocr_authorization_chain_coverage_matrix", "ocr_authorization_chain_coverage_matrix_v1.json"),
    (
        "compressed_authorization_lifecycle_dryrun_result",
        "compressed_authorization_lifecycle_dryrun_result_v1.json",
    ),
    ("compression_impact_review", "compression_impact_review_v1.json"),
    ("factory_standard_boundary_audit", "factory_standard_boundary_audit_v1.json"),
    (
        "factory_standard_adoption_readiness_decision",
        "factory_standard_adoption_readiness_decision_v1.json",
    ),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-planning-root",
        default=DEFAULT_PLANNING,
    )
    p.add_argument(
        "--ocr-provider-authorization-formal-request-artifact-generation-planning-root",
        default=DEFAULT_FORMAL,
    )
    p.add_argument(
        "--ocr-provider-authorization-request-post-dryrun-review-root",
        default=DEFAULT_REQ_POST,
    )
    p.add_argument(
        "--ocr-provider-authorization-request-dryrun-root",
        default=DEFAULT_REQ_DRYRUN,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_FACTORY_POST,
    )
    p.add_argument(
        "--luna-validation-factory-consolidation-root",
        default=DEFAULT_VF,
    )
    args = p.parse_args()

    result = run_capability_factory_admission_and_operation_standard_dryrun_and_review_v1(
        capability_factory_admission_and_operation_standard_planning_root=(
            args.capability_factory_admission_and_operation_standard_planning_root
        ),
        ocr_provider_authorization_formal_request_artifact_generation_planning_root=(
            args.ocr_provider_authorization_formal_request_artifact_generation_planning_root
        ),
        ocr_provider_authorization_request_post_dryrun_review_root=(
            args.ocr_provider_authorization_request_post_dryrun_review_root
        ),
        ocr_provider_authorization_request_dryrun_root=args.ocr_provider_authorization_request_dryrun_root,
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=(
            args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        ),
        luna_validation_factory_consolidation_root=args.luna_validation_factory_consolidation_root,
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
                "nine_standards_validated": sm.get("nine_standards_validated"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
