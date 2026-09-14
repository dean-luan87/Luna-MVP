#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Compressed OCR Authorization Lifecycle DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.compressed_ocr_authorization_lifecycle_dryrun_and_review_v1 import (
    run_compressed_ocr_authorization_lifecycle_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "compressed_ocr_authorization_lifecycle_planning"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/compressed_ocr_authorization_roadmap_decision"
)
DEFAULT_FACTORY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)
DEFAULT_REQ_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_post_dryrun_review"
)
DEFAULT_FORMAL = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_formal_request_artifact_generation_planning"
)
DEFAULT_FACTORY_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "compressed_ocr_authorization_lifecycle_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("compressed_lifecycle_dryrun_and_review_policy", "compressed_lifecycle_dryrun_and_review_policy_v1.json"),
    ("compressed_lifecycle_planning_input_review", "compressed_lifecycle_planning_input_review_v1.json"),
    ("compressed_lifecycle_candidate", "compressed_lifecycle_candidate_v1.json"),
    ("request_stage_candidate_dryrun_review", "request_stage_candidate_dryrun_review_v1.json"),
    ("formal_artifact_stage_candidate_dryrun_review", "formal_artifact_stage_candidate_dryrun_review_v1.json"),
    ("send_stage_candidate_dryrun_review", "send_stage_candidate_dryrun_review_v1.json"),
    ("grant_stage_candidate_dryrun_review", "grant_stage_candidate_dryrun_review_v1.json"),
    (
        "execution_window_stage_candidate_dryrun_review",
        "execution_window_stage_candidate_dryrun_review_v1.json",
    ),
    ("review_stage_candidate_dryrun_review", "review_stage_candidate_dryrun_review_v1.json"),
    ("factory_standard_consumption_matrix", "factory_standard_consumption_matrix_v1.json"),
    ("validation_factory_binding_review", "validation_factory_binding_review_v1.json"),
    ("compressed_lifecycle_evidence_binding_review", "compressed_lifecycle_evidence_binding_review_v1.json"),
    ("compressed_lifecycle_approval_grant_review", "compressed_lifecycle_approval_grant_review_v1.json"),
    ("compressed_lifecycle_sandbox_rollback_review", "compressed_lifecycle_sandbox_rollback_review_v1.json"),
    ("compressed_lifecycle_boundary_audit", "compressed_lifecycle_boundary_audit_v1.json"),
    ("compressed_lifecycle_blocked_path_result", "compressed_lifecycle_blocked_path_result_v1.json"),
    ("compressed_lifecycle_closure_decision", "compressed_lifecycle_closure_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--compressed-ocr-authorization-lifecycle-planning-root",
        default=DEFAULT_PLANNING,
    )
    p.add_argument(
        "--compressed-ocr-authorization-roadmap-decision-root",
        default=DEFAULT_ROADMAP,
    )
    p.add_argument(
        "--capability-factory-admission-and-operation-standard-dryrun-and-review-root",
        default=DEFAULT_FACTORY_DR,
    )
    p.add_argument(
        "--ocr-provider-authorization-request-post-dryrun-review-root",
        default=DEFAULT_REQ_POST,
    )
    p.add_argument(
        "--ocr-provider-authorization-formal-request-artifact-generation-planning-root",
        default=DEFAULT_FORMAL,
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_FACTORY_POST,
    )
    args = p.parse_args()

    result = run_compressed_ocr_authorization_lifecycle_dryrun_and_review_v1(
        compressed_ocr_authorization_lifecycle_planning_root=(
            args.compressed_ocr_authorization_lifecycle_planning_root
        ),
        compressed_ocr_authorization_roadmap_decision_root=(
            args.compressed_ocr_authorization_roadmap_decision_root
        ),
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
        ),
        ocr_provider_authorization_request_post_dryrun_review_root=(
            args.ocr_provider_authorization_request_post_dryrun_review_root
        ),
        ocr_provider_authorization_formal_request_artifact_generation_planning_root=(
            args.ocr_provider_authorization_formal_request_artifact_generation_planning_root
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
                "stage_count": sm.get("stage_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
