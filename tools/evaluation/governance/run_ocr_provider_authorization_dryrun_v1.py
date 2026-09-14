#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run OCR Provider Authorization DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_dryrun_v1 import run_ocr_provider_authorization_dryrun_v1

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_planning"
)
DEFAULT_RETURN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_return_roadmap_decision"
)
DEFAULT_FACTORY_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_REAL_POST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_real_dependency_check_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("ocr_provider_authorization_dryrun_policy", "ocr_provider_authorization_dryrun_policy_v1.json"),
    ("authorization_planning_input_review", "authorization_planning_input_review_v1.json"),
    ("authorization_request_candidate", "authorization_request_candidate_v1.json"),
    ("grant_candidate", "grant_candidate_v1.json"),
    ("execution_window_candidate", "execution_window_candidate_v1.json"),
    ("sandbox_boundary_candidate", "sandbox_boundary_candidate_v1.json"),
    ("rollback_candidate", "rollback_candidate_v1.json"),
    ("evidence_requirement_candidate", "evidence_requirement_candidate_v1.json"),
    ("owner_operator_approval_dryrun_result", "owner_operator_approval_dryrun_result_v1.json"),
    ("provider_selection_binding_dryrun_result", "provider_selection_binding_dryrun_result_v1.json"),
    (
        "real_dependency_check_authorization_binding_dryrun_result",
        "real_dependency_check_authorization_binding_dryrun_result_v1.json",
    ),
    (
        "controlled_trial_authorization_binding_dryrun_result",
        "controlled_trial_authorization_binding_dryrun_result_v1.json",
    ),
    ("authorization_lifecycle_dryrun_result", "authorization_lifecycle_dryrun_result_v1.json"),
    ("authorization_boundary_guard_dryrun_result", "authorization_boundary_guard_dryrun_result_v1.json"),
    ("authorization_blocked_path_result", "authorization_blocked_path_result_v1.json"),
    ("authorization_dryrun_readiness_decision", "authorization_dryrun_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--ocr-provider-authorization-planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--ocr-provider-authorization-return-roadmap-decision-root", default=DEFAULT_RETURN)
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=DEFAULT_FACTORY_POST,
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=DEFAULT_REAL_POST,
    )
    args = p.parse_args()

    result = run_ocr_provider_authorization_dryrun_v1(
        ocr_provider_authorization_planning_root=args.ocr_provider_authorization_planning_root,
        ocr_provider_authorization_return_roadmap_decision_root=(
            args.ocr_provider_authorization_return_roadmap_decision_root
        ),
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=(
            args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        ),
        ocr_provider_real_dependency_check_post_dryrun_review_root=(
            args.ocr_provider_real_dependency_check_post_dryrun_review_root
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
