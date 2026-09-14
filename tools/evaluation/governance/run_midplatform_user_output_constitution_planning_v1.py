#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform User Output Constitution Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_user_output_constitution_planning_v1 import (
    run_midplatform_user_output_constitution_planning_v1,
)

DEFAULT_OUTPUT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_dryrun_and_review"
)
DEFAULT_OUTPUT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_planning"
)
DEFAULT_TASK_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_task_response_candidate_integration_dryrun_and_review"
)
DEFAULT_CONSTITUTION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_user_output_constitution_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("user_output_constitution_planning_policy", "user_output_constitution_planning_policy_v1.json"),
    ("output_plane_dryrun_input_review", "output_plane_dryrun_input_review_v1.json"),
    ("user_output_constitution_definition", "user_output_constitution_definition_v1.json"),
    ("user_output_scope_and_jurisdiction", "user_output_scope_and_jurisdiction_v1.json"),
    ("user_output_admission_rule_plan", "user_output_admission_rule_plan_v1.json"),
    ("user_output_safety_rule_plan", "user_output_safety_rule_plan_v1.json"),
    ("user_output_fact_and_uncertainty_rule_plan", "user_output_fact_and_uncertainty_rule_plan_v1.json"),
    ("user_output_privacy_rule_plan", "user_output_privacy_rule_plan_v1.json"),
    ("user_output_channel_rule_plan", "user_output_channel_rule_plan_v1.json"),
    (
        "user_output_tone_personalization_boundary_plan",
        "user_output_tone_personalization_boundary_plan_v1.json",
    ),
    (
        "user_output_refusal_hold_degrade_rule_plan",
        "user_output_refusal_hold_degrade_rule_plan_v1.json",
    ),
    (
        "user_output_explainability_traceability_plan",
        "user_output_explainability_traceability_plan_v1.json",
    ),
    ("user_output_speech_display_boundary_plan", "user_output_speech_display_boundary_plan_v1.json"),
    (
        "user_output_memory_worldmodel_taskstate_boundary_plan",
        "user_output_memory_worldmodel_taskstate_boundary_plan_v1.json",
    ),
    ("user_output_constitution_conflict_policy", "user_output_constitution_conflict_policy_v1.json"),
    ("user_output_constitution_boundary_matrix", "user_output_constitution_boundary_matrix_v1.json"),
    ("user_output_constitution_dryrun_plan", "user_output_constitution_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("user_output_constitution_planning_decision", "user_output_constitution_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--output-plane-dryrun-root", default=DEFAULT_OUTPUT_DR)
    p.add_argument("--output-plane-planning-root", default=DEFAULT_OUTPUT_PLAN)
    p.add_argument("--task-response-dryrun-root", default=DEFAULT_TASK_DR)
    p.add_argument("--constitution-dryrun-root", default=DEFAULT_CONSTITUTION_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    args = p.parse_args()

    result = run_midplatform_user_output_constitution_planning_v1(
        midplatform_output_plane_integration_dryrun_and_review_root=args.output_plane_dryrun_root,
        midplatform_output_plane_integration_planning_root=args.output_plane_planning_root,
        midplatform_task_response_candidate_integration_dryrun_and_review_root=args.task_response_dryrun_root,
        midplatform_constitution_governance_explanation_dryrun_and_review_root=args.constitution_dryrun_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
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
                "constitution_not_user_facing": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
