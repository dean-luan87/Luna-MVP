#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Factory Standard Historical Redundancy Cleanup DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1 import (
    run_factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "factory_standard_historical_redundancy_cleanup_planning"
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
DEFAULT_FORMAL = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_formal_request_artifact_generation_planning"
)
DEFAULT_REQ_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_post_dryrun_review"
)
DEFAULT_SELECTION_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_selection_dependency_environment_post_dryrun_review"
)
DEFAULT_REAL_DEP_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "factory_standard_historical_cleanup_dryrun_and_review_policy",
        "factory_standard_historical_cleanup_dryrun_and_review_policy_v1.json",
    ),
    ("cleanup_planning_input_review", "cleanup_planning_input_review_v1.json"),
    ("historical_redundancy_cleanup_candidate", "historical_redundancy_cleanup_candidate_v1.json"),
    ("superseded_phase_marker_samples", "superseded_phase_marker_samples_v1.json"),
    ("absorbed_rule_marker_samples", "absorbed_rule_marker_samples_v1.json"),
    ("deprecated_for_new_phase_marker_samples", "deprecated_for_new_phase_marker_samples_v1.json"),
    ("read_only_evidence_source_marker_samples", "read_only_evidence_source_marker_samples_v1.json"),
    ("cleanup_metadata_schema_validation_result", "cleanup_metadata_schema_validation_result_v1.json"),
    ("historical_chain_preservation_review", "historical_chain_preservation_review_v1.json"),
    ("no_physical_delete_audit", "no_physical_delete_audit_v1.json"),
    ("future_phase_reference_policy_dryrun_result", "future_phase_reference_policy_dryrun_result_v1.json"),
    ("cleanup_boundary_blocked_path_result", "cleanup_boundary_blocked_path_result_v1.json"),
    ("cleanup_compression_alignment_review", "cleanup_compression_alignment_review_v1.json"),
    ("cleanup_dryrun_and_review_closure_decision", "cleanup_dryrun_and_review_closure_decision_v1.json"),
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
        "--factory-standard-historical-redundancy-cleanup-planning-root",
        default=DEFAULT_PLANNING,
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
        "--ocr-provider-authorization-formal-request-artifact-generation-planning-root",
        default=DEFAULT_FORMAL,
    )
    p.add_argument(
        "--ocr-provider-authorization-request-post-dryrun-review-root",
        default=DEFAULT_REQ_POST,
    )
    p.add_argument(
        "--ocr-provider-selection-dependency-environment-post-dryrun-review-root",
        default=DEFAULT_SELECTION_POST,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=DEFAULT_REAL_DEP_POST,
    )
    args = p.parse_args()

    result = run_factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1(
        factory_standard_historical_redundancy_cleanup_planning_root=(
            args.factory_standard_historical_redundancy_cleanup_planning_root
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
        ocr_provider_authorization_formal_request_artifact_generation_planning_root=(
            args.ocr_provider_authorization_formal_request_artifact_generation_planning_root
        ),
        ocr_provider_authorization_request_post_dryrun_review_root=(
            args.ocr_provider_authorization_request_post_dryrun_review_root
        ),
        ocr_provider_selection_dependency_environment_post_dryrun_review_root=(
            args.ocr_provider_selection_dependency_environment_post_dryrun_review_root
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
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "marking_only": sm.get("marking_only"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
