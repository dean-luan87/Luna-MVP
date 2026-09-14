#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Minimal Controlled Execution Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_planning_v1 import (
    run_ocr_real_dependency_minimal_controlled_execution_planning_v1,
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
DEFAULT_OCR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)
DEFAULT_VAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_minimal_controlled_execution_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("minimal_controlled_execution_planning_policy", "minimal_controlled_execution_planning_policy_v1.json"),
    ("final_preflight_input_review", "final_preflight_input_review_v1.json"),
    ("minimal_execution_scope", "minimal_execution_scope_v1.json"),
    ("minimal_execution_window_candidate_plan", "minimal_execution_window_candidate_plan_v1.json"),
    ("minimal_execution_sandbox_plan", "minimal_execution_sandbox_plan_v1.json"),
    ("minimal_allowed_check_plan", "minimal_allowed_check_plan_v1.json"),
    ("minimal_forbidden_action_plan", "minimal_forbidden_action_plan_v1.json"),
    ("minimal_evidence_output_plan", "minimal_evidence_output_plan_v1.json"),
    ("minimal_failure_route_plan", "minimal_failure_route_plan_v1.json"),
    ("minimal_rollback_plan", "minimal_rollback_plan_v1.json"),
    ("minimal_post_execution_review_plan", "minimal_post_execution_review_plan_v1.json"),
    ("minimal_execution_verifier_plan", "minimal_execution_verifier_plan_v1.json"),
    ("provider_selection_non_finalize_plan", "provider_selection_non_finalize_plan_v1.json"),
    ("minimal_execution_blocked_path_matrix", "minimal_execution_blocked_path_matrix_v1.json"),
    ("minimal_controlled_execution_dryrun_plan", "minimal_controlled_execution_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("minimal_controlled_execution_planning_decision", "minimal_controlled_execution_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--final-preflight-root", default=DEFAULT_PREFLIGHT)
    p.add_argument("--authorization-dryrun-root", default=DEFAULT_AUTH_DR)
    p.add_argument("--execution-authorization-dryrun-root", default=DEFAULT_EXEC_AUTH_DR)
    p.add_argument("--ocr-via-factory-dryrun-root", default=DEFAULT_OCR_DR)
    p.add_argument("--validation-separation-dryrun-root", default=DEFAULT_VAL_DR)
    args = p.parse_args()

    result = run_ocr_real_dependency_minimal_controlled_execution_planning_v1(
        ocr_real_dependency_execution_final_preflight_root=args.final_preflight_root,
        ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_root=args.authorization_dryrun_root,
        ocr_real_dependency_execution_authorization_dryrun_and_review_root=args.execution_authorization_dryrun_root,
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root=args.ocr_via_factory_dryrun_root,
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
                "planning_pass": sm.get("planning_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
