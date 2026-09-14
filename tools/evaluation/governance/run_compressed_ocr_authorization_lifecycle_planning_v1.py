#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Compressed OCR Authorization Lifecycle Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.compressed_ocr_authorization_lifecycle_planning_v1 import (
    run_compressed_ocr_authorization_lifecycle_planning_v1,
)

DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/compressed_ocr_authorization_roadmap_decision"
)
DEFAULT_FACTORY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)
DEFAULT_FACTORY_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_planning"
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
    "compressed_ocr_authorization_lifecycle_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "compressed_ocr_authorization_lifecycle_planning_policy",
        "compressed_ocr_authorization_lifecycle_planning_policy_v1.json",
    ),
    (
        "compressed_ocr_authorization_roadmap_input_review",
        "compressed_ocr_authorization_roadmap_input_review_v1.json",
    ),
    (
        "factory_standard_adoption_input_review",
        "factory_standard_adoption_input_review_v1.json",
    ),
    (
        "compressed_authorization_lifecycle_contract",
        "compressed_authorization_lifecycle_contract_v1.json",
    ),
    (
        "compressed_authorization_state_machine",
        "compressed_authorization_state_machine_v1.json",
    ),
    (
        "request_candidate_stage_contract",
        "request_candidate_stage_contract_v1.json",
    ),
    (
        "formal_artifact_candidate_stage_contract",
        "formal_artifact_candidate_stage_contract_v1.json",
    ),
    ("send_candidate_stage_contract", "send_candidate_stage_contract_v1.json"),
    ("grant_candidate_stage_contract", "grant_candidate_stage_contract_v1.json"),
    (
        "execution_window_candidate_stage_contract",
        "execution_window_candidate_stage_contract_v1.json",
    ),
    ("review_stage_contract", "review_stage_contract_v1.json"),
    (
        "compressed_lifecycle_boundary_matrix",
        "compressed_lifecycle_boundary_matrix_v1.json",
    ),
    (
        "compressed_lifecycle_evidence_requirement",
        "compressed_lifecycle_evidence_requirement_v1.json",
    ),
    (
        "compressed_lifecycle_approval_grant_policy",
        "compressed_lifecycle_approval_grant_policy_v1.json",
    ),
    (
        "compressed_lifecycle_sandbox_rollback_policy",
        "compressed_lifecycle_sandbox_rollback_policy_v1.json",
    ),
    (
        "compressed_lifecycle_validation_factory_binding",
        "compressed_lifecycle_validation_factory_binding_v1.json",
    ),
    ("compressed_lifecycle_dryrun_plan", "compressed_lifecycle_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("compressed_lifecycle_planning_decision", "compressed_lifecycle_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--compressed-ocr-authorization-roadmap-decision-root",
        default=DEFAULT_ROADMAP,
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

    result = run_compressed_ocr_authorization_lifecycle_planning_v1(
        compressed_ocr_authorization_roadmap_decision_root=args.compressed_ocr_authorization_roadmap_decision_root,
        capability_factory_admission_and_operation_standard_dryrun_and_review_root=(
            args.capability_factory_admission_and_operation_standard_dryrun_and_review_root
        ),
        capability_factory_admission_and_operation_standard_planning_root=(
            args.capability_factory_admission_and_operation_standard_planning_root
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
                "current_state": sm.get("current_state"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
