#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Minimal Controlled Execution DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_v1 import (
    run_ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_minimal_controlled_execution_planning"
)
DEFAULT_PREFLIGHT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_final_preflight"
)
DEFAULT_AUTH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review"
)
DEFAULT_EXEC_AUTH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_dryrun_and_review"
)
DEFAULT_VAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("minimal_controlled_execution_dryrun_review_policy", "minimal_controlled_execution_dryrun_review_policy_v1.json"),
    ("minimal_controlled_execution_planning_input_review", "minimal_controlled_execution_planning_input_review_v1.json"),
    ("minimal_controlled_execution_plan_candidate", "minimal_controlled_execution_plan_candidate_v1.json"),
    ("minimal_execution_scope_dryrun_review", "minimal_execution_scope_dryrun_review_v1.json"),
    ("minimal_execution_window_candidate_review", "minimal_execution_window_candidate_review_v1.json"),
    ("minimal_execution_sandbox_review", "minimal_execution_sandbox_review_v1.json"),
    ("minimal_allowed_check_plan_dryrun_review", "minimal_allowed_check_plan_dryrun_review_v1.json"),
    ("minimal_forbidden_action_dryrun_review", "minimal_forbidden_action_dryrun_review_v1.json"),
    ("minimal_evidence_output_dryrun_review", "minimal_evidence_output_dryrun_review_v1.json"),
    ("minimal_failure_route_dryrun_review", "minimal_failure_route_dryrun_review_v1.json"),
    ("minimal_rollback_dryrun_review", "minimal_rollback_dryrun_review_v1.json"),
    ("minimal_post_execution_review_dryrun_review", "minimal_post_execution_review_dryrun_review_v1.json"),
    ("minimal_execution_verifier_plan_review", "minimal_execution_verifier_plan_review_v1.json"),
    ("provider_selection_non_finalize_review", "provider_selection_non_finalize_review_v1.json"),
    ("minimal_controlled_execution_boundary_audit", "minimal_controlled_execution_boundary_audit_v1.json"),
    ("minimal_controlled_execution_blocked_path_result", "minimal_controlled_execution_blocked_path_result_v1.json"),
    ("minimal_controlled_execution_closure_decision", "minimal_controlled_execution_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLAN)
    p.add_argument("--final-preflight-root", default=DEFAULT_PREFLIGHT)
    p.add_argument("--authorization-dryrun-root", default=DEFAULT_AUTH_DR)
    p.add_argument("--execution-authorization-dryrun-root", default=DEFAULT_EXEC_AUTH_DR)
    p.add_argument("--validation-separation-dryrun-root", default=DEFAULT_VAL_DR)
    args = p.parse_args()

    result = run_ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_v1(
        ocr_real_dependency_minimal_controlled_execution_planning_root=args.planning_root,
        ocr_real_dependency_execution_final_preflight_root=args.final_preflight_root,
        ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_root=args.authorization_dryrun_root,
        ocr_real_dependency_execution_authorization_dryrun_and_review_root=args.execution_authorization_dryrun_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_separation_dryrun_root,
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
