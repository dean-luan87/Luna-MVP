#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Constitution Governance Hierarchy Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_constitution_governance_hierarchy_planning_v1 import (
    run_midplatform_constitution_governance_hierarchy_planning_v1,
)

DEFAULT_AUTH_EXT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_planning"
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
DEFAULT_HARNESS_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_OCR_AUTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_authorization_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_hierarchy_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "midplatform_constitution_governance_hierarchy_planning_policy",
        "midplatform_constitution_governance_hierarchy_planning_policy_v1.json",
    ),
    ("upstream_factory_standards_input_review", "upstream_factory_standards_input_review_v1.json"),
    ("luna_constitution_layer_outline", "luna_constitution_layer_outline_v1.json"),
    ("luna_general_constitution_plan", "luna_general_constitution_plan_v1.json"),
    ("domain_constitution_registry_plan", "domain_constitution_registry_plan_v1.json"),
    ("domain_standard_registry_plan", "domain_standard_registry_plan_v1.json"),
    (
        "capability_factory_constitution_reposition_plan",
        "capability_factory_constitution_reposition_plan_v1.json",
    ),
    (
        "factory_authorization_standard_reposition_plan",
        "factory_authorization_standard_reposition_plan_v1.json",
    ),
    (
        "controlled_provider_readiness_harness_reposition_plan",
        "controlled_provider_readiness_harness_reposition_plan_v1.json",
    ),
    ("validation_factory_reposition_plan", "validation_factory_reposition_plan_v1.json"),
    ("ocr_domain_constitution_reposition_plan", "ocr_domain_constitution_reposition_plan_v1.json"),
    (
        "vision_voice_future_constitution_reposition_plan",
        "vision_voice_future_constitution_reposition_plan_v1.json",
    ),
    ("governance_hierarchy_decision_tree", "governance_hierarchy_decision_tree_v1.json"),
    ("rule_fragmentation_prevention_policy", "rule_fragmentation_prevention_policy_v1.json"),
    ("deferred_phases_register", "deferred_phases_register_v1.json"),
    ("hierarchy_dryrun_plan", "hierarchy_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("hierarchy_planning_decision", "hierarchy_planning_decision_v1.json"),
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
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_HARNESS_POST,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-authorization-planning-root",
        default=DEFAULT_OCR_AUTH,
    )
    args = p.parse_args()

    result = run_midplatform_constitution_governance_hierarchy_planning_v1(
        capability_factory_authorization_standard_extension_planning_root=(
            args.capability_factory_authorization_standard_extension_planning_root
        ),
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
        ),
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root=(
            args.compressed_ocr_authorization_lifecycle_dryrun_and_review_root
        ),
        factory_standard_historical_redundancy_cleanup_dryrun_and_review_root=(
            args.factory_standard_historical_redundancy_cleanup_dryrun_and_review_root
        ),
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=(
            args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        ),
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
                "hierarchy_analogy": sm.get("hierarchy_analogy"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
