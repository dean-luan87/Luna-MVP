#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Formal Execution Request Generation Post-Route Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_formal_execution_request_generation_post_route_decision_v1 import (
    run_ocr_real_dependency_formal_execution_request_generation_post_route_decision_v1,
)

DEFAULT_FORMAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_dryrun_and_review"
)
DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_planning"
)
DEFAULT_AUTH_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_dryrun_and_review"
)
DEFAULT_VAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_OCR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_post_route_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "formal_execution_request_generation_post_route_policy",
        "formal_execution_request_generation_post_route_policy_v1.json",
    ),
    (
        "formal_execution_request_dryrun_input_review",
        "formal_execution_request_dryrun_input_review_v1.json",
    ),
    (
        "formal_execution_request_candidate_readiness_review",
        "formal_execution_request_candidate_readiness_review_v1.json",
    ),
    (
        "route_a_formal_request_generation_authorization_planning_assessment",
        "route_a_formal_request_generation_authorization_planning_assessment_v1.json",
    ),
    (
        "route_b_owner_operator_approval_precheck_assessment",
        "route_b_owner_operator_approval_precheck_assessment_v1.json",
    ),
    (
        "route_c_validation_runtime_readiness_assessment",
        "route_c_validation_runtime_readiness_assessment_v1.json",
    ),
    (
        "route_d_evidence_readiness_review_assessment",
        "route_d_evidence_readiness_review_assessment_v1.json",
    ),
    (
        "route_e_direct_request_generation_assessment",
        "route_e_direct_request_generation_assessment_v1.json",
    ),
    (
        "formal_execution_request_post_route_selection_matrix",
        "formal_execution_request_post_route_selection_matrix_v1.json",
    ),
    ("selected_route_preconditions", "selected_route_preconditions_v1.json"),
    ("deferred_routes_register", "deferred_routes_register_v1.json"),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-real-dependency-formal-execution-request-generation-dryrun-and-review-root",
        default=DEFAULT_FORMAL_DR,
    )
    p.add_argument(
        "--ocr-real-dependency-formal-execution-request-generation-planning-root",
        default=DEFAULT_PLAN,
    )
    p.add_argument(
        "--ocr-real-dependency-execution-authorization-dryrun-and-review-root",
        default=DEFAULT_AUTH_DRYRUN,
    )
    p.add_argument(
        "--midplatform-validation-engineering-separation-dryrun-and-review-root",
        default=DEFAULT_VAL_DR,
    )
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-dryrun-and-review-root",
        default=DEFAULT_OCR_DR,
    )
    args = p.parse_args()

    result = run_ocr_real_dependency_formal_execution_request_generation_post_route_decision_v1(
        ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_root=(
            args.ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_root
        ),
        ocr_real_dependency_formal_execution_request_generation_planning_root=(
            args.ocr_real_dependency_formal_execution_request_generation_planning_root
        ),
        ocr_real_dependency_execution_authorization_dryrun_and_review_root=(
            args.ocr_real_dependency_execution_authorization_dryrun_and_review_root
        ),
        midplatform_validation_engineering_separation_dryrun_and_review_root=(
            args.midplatform_validation_engineering_separation_dryrun_and_review_root
        ),
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=(
            args.ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
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
