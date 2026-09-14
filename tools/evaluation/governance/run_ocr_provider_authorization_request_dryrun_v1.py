#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Authorization Request DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    run_ocr_provider_authorization_request_dryrun_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_planning"
)
DEFAULT_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_post_dryrun_review"
)
DEFAULT_AUTH_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_dryrun"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_request_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "ocr_provider_authorization_request_dryrun_policy",
        "ocr_provider_authorization_request_dryrun_policy_v1.json",
    ),
    (
        "authorization_request_planning_input_review",
        "authorization_request_planning_input_review_v1.json",
    ),
    ("request_artifact_candidate", "request_artifact_candidate_v1.json"),
    (
        "request_artifact_schema_validation_result",
        "request_artifact_schema_validation_result_v1.json",
    ),
    (
        "generation_precondition_dryrun_result",
        "generation_precondition_dryrun_result_v1.json",
    ),
    ("field_binding_dryrun_result", "field_binding_dryrun_result_v1.json"),
    ("validation_rule_dryrun_result", "validation_rule_dryrun_result_v1.json"),
    ("send_boundary_dryrun_result", "send_boundary_dryrun_result_v1.json"),
    ("request_lifecycle_dryrun_result", "request_lifecycle_dryrun_result_v1.json"),
    (
        "request_evidence_binding_dryrun_result",
        "request_evidence_binding_dryrun_result_v1.json",
    ),
    ("request_blocked_path_result", "request_blocked_path_result_v1.json"),
    ("request_no_artifact_no_send_audit", "request_no_artifact_no_send_audit_v1.json"),
    ("request_dryrun_readiness_decision", "request_dryrun_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument(
        "--ocr-provider-authorization-request-planning-root",
        default=DEFAULT_PLANNING,
    )
    p.add_argument(
        "--ocr-provider-authorization-post-dryrun-review-root",
        default=DEFAULT_POST,
    )
    p.add_argument(
        "--ocr-provider-authorization-dryrun-root",
        default=DEFAULT_AUTH_DRYRUN,
    )
    args = p.parse_args()

    result = run_ocr_provider_authorization_request_dryrun_v1(
        ocr_provider_authorization_request_planning_root=(
            args.ocr_provider_authorization_request_planning_root
        ),
        ocr_provider_authorization_post_dryrun_review_root=(
            args.ocr_provider_authorization_post_dryrun_review_root
        ),
        ocr_provider_authorization_dryrun_root=args.ocr_provider_authorization_dryrun_root,
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
