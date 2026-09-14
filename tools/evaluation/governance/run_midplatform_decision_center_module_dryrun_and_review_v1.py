#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Decision Center Module DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    run_midplatform_decision_center_module_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_planning"
)
DEFAULT_CORE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_core_architecture_resume"
)
DEFAULT_CONST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_VAL = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_HEALTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)
DEFAULT_WHITEBOX = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_whitebox_inspection_integration_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "decision_center_module_dryrun_review_policy",
        "decision_center_module_dryrun_review_policy_v1.json",
    ),
    ("decision_center_planning_input_review", "decision_center_planning_input_review_v1.json"),
    ("decision_center_model_candidate", "decision_center_model_candidate_v1.json"),
    ("sample_decision_request_candidate", "sample_decision_request_candidate_v1.json"),
    ("sample_decision_candidate", "sample_decision_candidate_v1.json"),
    ("constitution_binding_dryrun_review", "constitution_binding_dryrun_review_v1.json"),
    ("validation_binding_dryrun_review", "validation_binding_dryrun_review_v1.json"),
    ("health_binding_dryrun_review", "health_binding_dryrun_review_v1.json"),
    ("whitebox_binding_dryrun_review", "whitebox_binding_dryrun_review_v1.json"),
    (
        "factory_candidate_binding_dryrun_review",
        "factory_candidate_binding_dryrun_review_v1.json",
    ),
    (
        "decision_priority_conflict_dryrun_review",
        "decision_priority_conflict_dryrun_review_v1.json",
    ),
    ("decision_action_taxonomy_dryrun_review", "decision_action_taxonomy_dryrun_review_v1.json"),
    (
        "decision_rationale_traceability_review",
        "decision_rationale_traceability_review_v1.json",
    ),
    (
        "decision_to_task_response_boundary_review",
        "decision_to_task_response_boundary_review_v1.json",
    ),
    ("decision_center_boundary_audit", "decision_center_boundary_audit_v1.json"),
    ("decision_center_blocked_path_result", "decision_center_blocked_path_result_v1.json"),
    ("decision_center_closure_decision", "decision_center_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--core-resume-root", default=DEFAULT_CORE)
    p.add_argument("--constitution-dryrun-root", default=DEFAULT_CONST)
    p.add_argument("--validation-dryrun-root", default=DEFAULT_VAL)
    p.add_argument("--health-post-dryrun-root", default=DEFAULT_HEALTH)
    p.add_argument("--whitebox-dryrun-root", default=DEFAULT_WHITEBOX)
    args = p.parse_args()

    result = run_midplatform_decision_center_module_dryrun_and_review_v1(
        midplatform_decision_center_module_planning_root=args.planning_root,
        midplatform_core_architecture_resume_root=args.core_resume_root,
        midplatform_constitution_governance_explanation_dryrun_and_review_root=args.constitution_dryrun_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_dryrun_root,
        health_management_layer_integration_post_dryrun_review_root=args.health_post_dryrun_root,
        midplatform_whitebox_inspection_integration_dryrun_and_review_root=args.whitebox_dryrun_root,
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
                "model_candidate_generated": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
