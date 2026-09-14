#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Real Minimal Controlled Execution Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_real_dependency_real_minimal_controlled_execution_planning_v1 import (
    run_ocr_real_dependency_real_minimal_controlled_execution_planning_v1,
)

DEFAULT_AUTH_DEC = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_execution_authorization_decision"
)
DEFAULT_DRYRUN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review"
)
DEFAULT_PRIOR_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_minimal_controlled_execution_planning"
)
DEFAULT_PREFLIGHT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_final_preflight"
)
DEFAULT_VAL_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_controlled_execution_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("real_minimal_controlled_execution_planning_policy", "real_minimal_controlled_execution_planning_policy_v1.json"),
    ("authorization_decision_input_review", "authorization_decision_input_review_v1.json"),
    ("real_execution_scope_lock", "real_execution_scope_lock_v1.json"),
    ("real_execution_window_opening_plan", "real_execution_window_opening_plan_v1.json"),
    ("real_execution_sandbox_plan", "real_execution_sandbox_plan_v1.json"),
    ("real_execution_allowed_check_plan", "real_execution_allowed_check_plan_v1.json"),
    ("real_execution_forbidden_action_plan", "real_execution_forbidden_action_plan_v1.json"),
    ("real_execution_evidence_capture_plan", "real_execution_evidence_capture_plan_v1.json"),
    ("real_execution_failure_route_plan", "real_execution_failure_route_plan_v1.json"),
    ("real_execution_rollback_boundary_plan", "real_execution_rollback_boundary_plan_v1.json"),
    ("real_execution_owner_confirmation_plan", "real_execution_owner_confirmation_plan_v1.json"),
    ("real_execution_post_review_plan", "real_execution_post_review_plan_v1.json"),
    ("real_execution_verifier_plan", "real_execution_verifier_plan_v1.json"),
    ("provider_selection_non_finalize_plan", "provider_selection_non_finalize_plan_v1.json"),
    ("real_execution_blocked_path_matrix", "real_execution_blocked_path_matrix_v1.json"),
    ("real_execution_dryrun_plan", "real_execution_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("real_minimal_controlled_execution_planning_decision", "real_minimal_controlled_execution_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--authorization-decision-root", default=DEFAULT_AUTH_DEC)
    p.add_argument("--minimal-dryrun-root", default=DEFAULT_DRYRUN)
    p.add_argument("--minimal-planning-root", default=DEFAULT_PRIOR_PLAN)
    p.add_argument("--final-preflight-root", default=DEFAULT_PREFLIGHT)
    p.add_argument("--validation-separation-dryrun-root", default=DEFAULT_VAL_DR)
    args = p.parse_args()

    result = run_ocr_real_dependency_real_minimal_controlled_execution_planning_v1(
        ocr_real_dependency_real_minimal_execution_authorization_decision_root=args.authorization_decision_root,
        ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root=args.minimal_dryrun_root,
        ocr_real_dependency_minimal_controlled_execution_planning_root=args.minimal_planning_root,
        ocr_real_dependency_execution_final_preflight_root=args.final_preflight_root,
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
