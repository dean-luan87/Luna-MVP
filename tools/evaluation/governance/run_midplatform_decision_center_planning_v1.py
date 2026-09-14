#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Decision Center Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_decision_center_planning_v1 import (
    run_midplatform_decision_center_planning_v1,
)

DEFAULT_CORE_RESUME = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_core_architecture_resume"
)
DEFAULT_WHITEBOX_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_whitebox_inspection_integration_dryrun_and_review"
)
DEFAULT_VAL = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_CONST = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_HEALTH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_management_layer_integration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_decision_center_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("decision_center_planning_policy", "decision_center_planning_policy_v1.json"),
    ("midplatform_core_resume_input_review", "midplatform_core_resume_input_review_v1.json"),
    ("decision_center_role_definition", "decision_center_role_definition_v1.json"),
    ("decision_center_input_contract", "decision_center_input_contract_v1.json"),
    ("decision_center_output_contract", "decision_center_output_contract_v1.json"),
    ("decision_action_taxonomy", "decision_action_taxonomy_v1.json"),
    ("decision_priority_and_conflict_policy", "decision_priority_and_conflict_policy_v1.json"),
    ("constitution_constraint_consumption_plan", "constitution_constraint_consumption_plan_v1.json"),
    ("validation_result_consumption_plan", "validation_result_consumption_plan_v1.json"),
    ("health_signal_consumption_plan", "health_signal_consumption_plan_v1.json"),
    ("whitebox_visibility_consumption_plan", "whitebox_visibility_consumption_plan_v1.json"),
    ("evidence_confidence_consumption_plan", "evidence_confidence_consumption_plan_v1.json"),
    ("task_context_consumption_plan", "task_context_consumption_plan_v1.json"),
    (
        "failure_route_and_escalation_decision_plan",
        "failure_route_and_escalation_decision_plan_v1.json",
    ),
    ("decision_to_task_response_boundary_plan", "decision_to_task_response_boundary_plan_v1.json"),
    ("decision_center_runtime_boundary_matrix", "decision_center_runtime_boundary_matrix_v1.json"),
    ("decision_center_dryrun_plan", "decision_center_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("decision_center_planning_decision", "decision_center_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--core-resume-root", default=DEFAULT_CORE_RESUME)
    p.add_argument("--whitebox-dryrun-root", default=DEFAULT_WHITEBOX_DR)
    p.add_argument("--validation-separation-dryrun-root", default=DEFAULT_VAL)
    p.add_argument("--constitution-explanation-dryrun-root", default=DEFAULT_CONST)
    p.add_argument("--health-post-dryrun-root", default=DEFAULT_HEALTH)
    args = p.parse_args()

    result = run_midplatform_decision_center_planning_v1(
        midplatform_core_architecture_resume_root=args.core_resume_root,
        midplatform_whitebox_inspection_integration_dryrun_and_review_root=args.whitebox_dryrun_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_separation_dryrun_root,
        midplatform_constitution_governance_explanation_dryrun_and_review_root=args.constitution_explanation_dryrun_root,
        health_management_layer_integration_post_dryrun_review_root=args.health_post_dryrun_root,
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
                "planning_not_runtime": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
