#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Formal Request Generation Authorization DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_v1 import (
    run_ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_v1,
)

DEFAULT_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_post_route_decision"
)
DEFAULT_FORMAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_dryrun_and_review"
)
DEFAULT_FORMAL_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_planning"
)
DEFAULT_AUTH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_dryrun_and_review"
)
DEFAULT_OCR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_VAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_HIST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "formal_request_generation_authorization_dryrun_review_policy",
        "formal_request_generation_authorization_dryrun_review_policy_v1.json",
    ),
    ("post_route_decision_input_review", "post_route_decision_input_review_v1.json"),
    (
        "formal_execution_request_candidate_input_review",
        "formal_execution_request_candidate_input_review_v1.json",
    ),
    (
        "formal_request_generation_authorization_candidate",
        "formal_request_generation_authorization_candidate_v1.json",
    ),
    (
        "owner_operator_approval_precheck_candidate",
        "owner_operator_approval_precheck_candidate_v1.json",
    ),
    ("evidence_readiness_candidate", "evidence_readiness_candidate_v1.json"),
    ("validation_gate_readiness_candidate", "validation_gate_readiness_candidate_v1.json"),
    ("final_preflight_readiness_candidate", "final_preflight_readiness_candidate_v1.json"),
    (
        "compressed_authorization_chain_integration_review",
        "compressed_authorization_chain_integration_review_v1.json",
    ),
    ("legacy_phase_absorption_marker", "legacy_phase_absorption_marker_v1.json"),
    (
        "formal_request_generation_authorization_boundary_audit",
        "formal_request_generation_authorization_boundary_audit_v1.json",
    ),
    (
        "formal_request_generation_authorization_blocked_path_result",
        "formal_request_generation_authorization_blocked_path_result_v1.json",
    ),
    (
        "formal_request_generation_authorization_closure_decision",
        "formal_request_generation_authorization_closure_decision_v1.json",
    ),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--post-route-decision-root", default=DEFAULT_POST)
    p.add_argument("--formal-dryrun-root", default=DEFAULT_FORMAL_DR)
    p.add_argument("--formal-planning-root", default=DEFAULT_FORMAL_PLAN)
    p.add_argument("--auth-dryrun-root", default=DEFAULT_AUTH_DR)
    p.add_argument("--ocr-via-factory-dryrun-root", default=DEFAULT_OCR_DR)
    p.add_argument("--validation-separation-dryrun-root", default=DEFAULT_VAL_DR)
    p.add_argument("--historical-cleanup-dryrun-root", default=DEFAULT_HIST)
    args = p.parse_args()

    result = run_ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_v1(
        ocr_real_dependency_formal_execution_request_generation_post_route_decision_root=args.post_route_decision_root,
        ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_root=args.formal_dryrun_root,
        ocr_real_dependency_formal_execution_request_generation_planning_root=args.formal_planning_root,
        ocr_real_dependency_execution_authorization_dryrun_and_review_root=args.auth_dryrun_root,
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=args.ocr_via_factory_dryrun_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_separation_dryrun_root,
        factory_standard_historical_redundancy_cleanup_dryrun_and_review_root=args.historical_cleanup_dryrun_root,
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
                "compressed_merge": sm.get("compressed_merge"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
