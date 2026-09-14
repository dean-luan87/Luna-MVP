#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Factory Standard Historical Redundancy Cleanup Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.factory_standard_historical_redundancy_cleanup_planning_v1 import (
    run_factory_standard_historical_redundancy_cleanup_planning_v1,
)

DEFAULT_LIFECYCLE_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "compressed_ocr_authorization_lifecycle_dryrun_and_review"
)
DEFAULT_FACTORY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)
DEFAULT_FACTORY_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_planning"
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
    "factory_standard_historical_redundancy_cleanup_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "factory_standard_historical_cleanup_planning_policy",
        "factory_standard_historical_cleanup_planning_policy_v1.json",
    ),
    ("compressed_lifecycle_input_review", "compressed_lifecycle_input_review_v1.json"),
    ("historical_redundancy_scope", "historical_redundancy_scope_v1.json"),
    ("superseded_phase_inventory_plan", "superseded_phase_inventory_plan_v1.json"),
    ("absorbed_rule_inventory_plan", "absorbed_rule_inventory_plan_v1.json"),
    ("deprecated_for_new_phase_inventory_plan", "deprecated_for_new_phase_inventory_plan_v1.json"),
    ("read_only_evidence_source_register_plan", "read_only_evidence_source_register_plan_v1.json"),
    ("no_physical_delete_policy", "no_physical_delete_policy_v1.json"),
    ("historical_chain_preservation_policy", "historical_chain_preservation_policy_v1.json"),
    ("future_phase_reference_policy", "future_phase_reference_policy_v1.json"),
    ("cleanup_metadata_schema", "cleanup_metadata_schema_v1.json"),
    ("cleanup_dryrun_plan", "cleanup_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("cleanup_planning_decision", "cleanup_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--compressed-ocr-authorization-lifecycle-dryrun-and-review-root",
        default=DEFAULT_LIFECYCLE_DR,
    )
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-dryrun-and-review-root",
        default=DEFAULT_FACTORY_DR,
    )
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-planning-root",
        default=DEFAULT_FACTORY_PLAN,
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

    result = run_factory_standard_historical_redundancy_cleanup_planning_v1(
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root=(
            args.compressed_ocr_authorization_lifecycle_dryrun_and_review_root
        ),
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
        ),
        capability_factory_admission_and_operation_standard_planning_root=(
            args.capability_factory_admission_and_operation_standard_planning_root
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
