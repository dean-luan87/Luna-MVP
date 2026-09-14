#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Authorization Request Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_request_planning_v1 import (
    run_ocr_provider_authorization_request_planning_v1,
)

DEFAULT_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_post_dryrun_review"
)
DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_dryrun"
)
DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_planning"
)
DEFAULT_FACTORY_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_request_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "ocr_provider_authorization_request_planning_policy",
        "ocr_provider_authorization_request_planning_policy_v1.json",
    ),
    (
        "authorization_post_dryrun_review_input_review",
        "authorization_post_dryrun_review_input_review_v1.json",
    ),
    ("authorization_request_artifact_schema", "authorization_request_artifact_schema_v1.json"),
    (
        "authorization_request_generation_precondition",
        "authorization_request_generation_precondition_v1.json",
    ),
    (
        "authorization_request_field_binding_plan",
        "authorization_request_field_binding_plan_v1.json",
    ),
    (
        "authorization_request_validation_rule_plan",
        "authorization_request_validation_rule_plan_v1.json",
    ),
    (
        "authorization_request_owner_operator_approval_plan",
        "authorization_request_owner_operator_approval_plan_v1.json",
    ),
    (
        "authorization_request_send_boundary_plan",
        "authorization_request_send_boundary_plan_v1.json",
    ),
    ("authorization_request_lifecycle_plan", "authorization_request_lifecycle_plan_v1.json"),
    (
        "authorization_request_evidence_binding_plan",
        "authorization_request_evidence_binding_plan_v1.json",
    ),
    (
        "authorization_request_blocked_path_matrix",
        "authorization_request_blocked_path_matrix_v1.json",
    ),
    ("authorization_request_dryrun_plan", "authorization_request_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("authorization_request_planning_decision", "authorization_request_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-provider-authorization-post-dryrun-review-root",
        default=DEFAULT_POST,
    )
    p.add_argument("--ocr-provider-authorization-dryrun-root", default=DEFAULT_DRYRUN)
    p.add_argument("--ocr-provider-authorization-planning-root", default=DEFAULT_PLANNING)
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_FACTORY_POST,
    )
    args = p.parse_args()

    result = run_ocr_provider_authorization_request_planning_v1(
        ocr_provider_authorization_post_dryrun_review_root=(
            args.ocr_provider_authorization_post_dryrun_review_root
        ),
        ocr_provider_authorization_dryrun_root=args.ocr_provider_authorization_dryrun_root,
        ocr_provider_authorization_planning_root=args.ocr_provider_authorization_planning_root,
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
                "current_lifecycle_state": sm.get("current_lifecycle_state"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
