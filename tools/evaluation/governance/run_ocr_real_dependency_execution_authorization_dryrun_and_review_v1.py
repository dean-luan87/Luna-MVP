#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Real Dependency Execution Authorization DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_execution_authorization_dryrun_and_review_v1 import (
    run_ocr_real_dependency_execution_authorization_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_planning"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_roadmap_decision"
)
DEFAULT_OCR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_VAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_AUTH_EXT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)
DEFAULT_EXPLAIN_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "ocr_real_dependency_execution_authorization_dryrun_review_policy",
        "ocr_real_dependency_execution_authorization_dryrun_review_policy_v1.json",
    ),
    (
        "execution_authorization_planning_input_review",
        "execution_authorization_planning_input_review_v1.json",
    ),
    (
        "execution_authorization_request_candidate",
        "execution_authorization_request_candidate_v1.json",
    ),
    ("execution_grant_candidate", "execution_grant_candidate_v1.json"),
    ("execution_window_candidate", "execution_window_candidate_v1.json"),
    ("allowed_check_plan_candidate", "allowed_check_plan_candidate_v1.json"),
    ("forbidden_action_review", "forbidden_action_review_v1.json"),
    ("evidence_collection_candidate", "evidence_collection_candidate_v1.json"),
    ("rollback_failure_route_candidate", "rollback_failure_route_candidate_v1.json"),
    ("validation_gate_path_dryrun_review", "validation_gate_path_dryrun_review_v1.json"),
    ("provider_selection_non_finalize_review", "provider_selection_non_finalize_review_v1.json"),
    ("state_machine_dryrun_review", "state_machine_dryrun_review_v1.json"),
    ("execution_authorization_boundary_audit", "execution_authorization_boundary_audit_v1.json"),
    (
        "execution_authorization_blocked_path_result",
        "execution_authorization_blocked_path_result_v1.json",
    ),
    (
        "execution_authorization_closure_decision",
        "execution_authorization_closure_decision_v1.json",
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
        "--ocr-real-dependency-execution-authorization-planning-root",
        default=DEFAULT_PLAN,
    )
    p.add_argument(
        "--ocr-real-dependency-execution-authorization-roadmap-decision-root",
        default=DEFAULT_ROADMAP,
    )
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-dryrun-and-review-root",
        default=DEFAULT_OCR_DR,
    )
    p.add_argument(
        "--midplatform-validation-engineering-separation-dryrun-and-review-root",
        default=DEFAULT_VAL_DR,
    )
    p.add_argument(
        "--capability-factory-authorization-standard-extension-dryrun-and-review-root",
        default=DEFAULT_AUTH_EXT_DR,
    )
    p.add_argument(
        "--midplatform-constitution-governance-explanation-dryrun-and-review-root",
        default=DEFAULT_EXPLAIN_DR,
    )
    args = p.parse_args()

    result = run_ocr_real_dependency_execution_authorization_dryrun_and_review_v1(
        ocr_real_dependency_execution_authorization_planning_root=(
            args.ocr_real_dependency_execution_authorization_planning_root
        ),
        ocr_real_dependency_execution_authorization_roadmap_decision_root=(
            args.ocr_real_dependency_execution_authorization_roadmap_decision_root
        ),
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=(
            args.ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        ),
        midplatform_validation_engineering_separation_dryrun_and_review_root=(
            args.midplatform_validation_engineering_separation_dryrun_and_review_root
        ),
        capability_factory_authorization_standard_extension_dryrun_and_review_root=(
            args.capability_factory_authorization_standard_extension_dryrun_and_review_root
        ),
        midplatform_constitution_governance_explanation_dryrun_and_review_root=(
            args.midplatform_constitution_governance_explanation_dryrun_and_review_root
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
