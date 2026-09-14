#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Compressed OCR Authorization Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.compressed_ocr_authorization_roadmap_decision_v1 import (
    run_compressed_ocr_authorization_roadmap_decision_v1,
)

DEFAULT_FACTORY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)
DEFAULT_FACTORY_PLAN = (
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
DEFAULT_FACTORY_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/compressed_ocr_authorization_roadmap_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("compressed_ocr_authorization_roadmap_policy", "compressed_ocr_authorization_roadmap_policy_v1.json"),
    (
        "factory_standard_dryrun_review_input_review",
        "factory_standard_dryrun_review_input_review_v1.json",
    ),
    ("compression_readiness_review", "compression_readiness_review_v1.json"),
    (
        "route_a_compressed_authorization_lifecycle_assessment",
        "route_a_compressed_authorization_lifecycle_assessment_v1.json",
    ),
    (
        "route_b_resume_formal_artifact_triple_chain_assessment",
        "route_b_resume_formal_artifact_triple_chain_assessment_v1.json",
    ),
    (
        "route_c_real_dependency_check_authorization_assessment",
        "route_c_real_dependency_check_authorization_assessment_v1.json",
    ),
    (
        "route_d_historical_redundancy_cleanup_assessment",
        "route_d_historical_redundancy_cleanup_assessment_v1.json",
    ),
    (
        "compressed_ocr_authorization_route_selection_matrix",
        "compressed_ocr_authorization_route_selection_matrix_v1.json",
    ),
    ("selected_route_preconditions", "selected_route_preconditions_v1.json"),
    ("deferred_routes_register", "deferred_routes_register_v1.json"),
    ("compressed_authorization_execution_model", "compressed_authorization_execution_model_v1.json"),
    ("factory_standard_adoption_binding", "factory_standard_adoption_binding_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
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
        "--capability-factory-admission-and-operation-standard-planning-root",
        default=DEFAULT_FACTORY_PLAN,
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
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_FACTORY_POST,
    )
    args = p.parse_args()

    result = run_compressed_ocr_authorization_roadmap_decision_v1(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
        ),
        capability_factory_admission_and_operation_standard_planning_root=(
            args.capability_factory_admission_and_operation_standard_planning_root
        ),
        ocr_provider_authorization_formal_request_artifact_generation_planning_root=(
            args.ocr_provider_authorization_formal_request_artifact_generation_planning_root
        ),
        ocr_provider_authorization_request_post_dryrun_review_root=(
            args.ocr_provider_authorization_request_post_dryrun_review_root
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
