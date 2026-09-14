#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Authorization Formal Request Artifact Generation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_formal_request_artifact_generation_planning_v1 import (
    run_ocr_provider_authorization_formal_request_artifact_generation_planning_v1,
)

DEFAULT_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_post_dryrun_review"
)
DEFAULT_REQ_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_dryrun"
)
DEFAULT_REQ_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_planning"
)
DEFAULT_AUTH_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_formal_request_artifact_generation_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "formal_request_artifact_generation_planning_policy",
        "formal_request_artifact_generation_planning_policy_v1.json",
    ),
    (
        "request_post_dryrun_review_input_review",
        "request_post_dryrun_review_input_review_v1.json",
    ),
    ("formal_request_artifact_schema", "formal_request_artifact_schema_v1.json"),
    (
        "formal_request_artifact_generation_rule",
        "formal_request_artifact_generation_rule_v1.json",
    ),
    (
        "formal_request_artifact_field_source_map",
        "formal_request_artifact_field_source_map_v1.json",
    ),
    (
        "formal_request_artifact_validation_rule",
        "formal_request_artifact_validation_rule_v1.json",
    ),
    (
        "formal_request_artifact_versioning_policy",
        "formal_request_artifact_versioning_policy_v1.json",
    ),
    (
        "formal_request_artifact_signature_placeholder_policy",
        "formal_request_artifact_signature_placeholder_policy_v1.json",
    ),
    (
        "formal_request_artifact_storage_boundary_plan",
        "formal_request_artifact_storage_boundary_plan_v1.json",
    ),
    (
        "formal_request_artifact_lifecycle_plan",
        "formal_request_artifact_lifecycle_plan_v1.json",
    ),
    (
        "formal_request_artifact_send_precheck_plan",
        "formal_request_artifact_send_precheck_plan_v1.json",
    ),
    (
        "formal_request_artifact_blocked_path_matrix",
        "formal_request_artifact_blocked_path_matrix_v1.json",
    ),
    ("formal_request_artifact_dryrun_plan", "formal_request_artifact_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "formal_request_artifact_generation_planning_decision",
        "formal_request_artifact_generation_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-provider-authorization-request-post-dryrun-review-root",
        default=DEFAULT_POST,
    )
    p.add_argument(
        "--ocr-provider-authorization-request-dryrun-root",
        default=DEFAULT_REQ_DRYRUN,
    )
    p.add_argument(
        "--ocr-provider-authorization-request-planning-root",
        default=DEFAULT_REQ_PLANNING,
    )
    p.add_argument(
        "--ocr-provider-authorization-post-dryrun-review-root",
        default=DEFAULT_AUTH_POST,
    )
    args = p.parse_args()

    result = run_ocr_provider_authorization_formal_request_artifact_generation_planning_v1(
        ocr_provider_authorization_request_post_dryrun_review_root=(
            args.ocr_provider_authorization_request_post_dryrun_review_root
        ),
        ocr_provider_authorization_request_dryrun_root=(
            args.ocr_provider_authorization_request_dryrun_root
        ),
        ocr_provider_authorization_request_planning_root=(
            args.ocr_provider_authorization_request_planning_root
        ),
        ocr_provider_authorization_post_dryrun_review_root=(
            args.ocr_provider_authorization_post_dryrun_review_root
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
