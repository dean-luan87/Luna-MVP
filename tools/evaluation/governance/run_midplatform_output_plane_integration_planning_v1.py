#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Output Plane Integration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_output_plane_integration_planning_v1 import (
    run_midplatform_output_plane_integration_planning_v1,
)

DEFAULT_TASK_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_task_response_candidate_integration_dryrun_and_review"
)
DEFAULT_TASK_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_task_response_candidate_integration_planning"
)
DEFAULT_DC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_dryrun_and_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_CONSTITUTION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_constitution_governance_explanation_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("output_plane_integration_planning_policy", "output_plane_integration_planning_policy_v1.json"),
    ("upstream_task_response_input_review", "upstream_task_response_input_review_v1.json"),
    ("output_plane_module_definition", "output_plane_module_definition_v1.json"),
    ("task_response_candidate_intake_contract", "task_response_candidate_intake_contract_v1.json"),
    ("user_output_candidate_contract", "user_output_candidate_contract_v1.json"),
    ("output_channel_taxonomy", "output_channel_taxonomy_v1.json"),
    ("user_output_constitution_binding_plan", "user_output_constitution_binding_plan_v1.json"),
    ("safety_gate_binding_plan", "safety_gate_binding_plan_v1.json"),
    ("speech_gate_binding_plan", "speech_gate_binding_plan_v1.json"),
    ("voice_output_plane_boundary_plan", "voice_output_plane_boundary_plan_v1.json"),
    ("display_output_boundary_plan", "display_output_boundary_plan_v1.json"),
    ("output_assembly_rule_plan", "output_assembly_rule_plan_v1.json"),
    (
        "output_uncertainty_and_evidence_preservation_plan",
        "output_uncertainty_and_evidence_preservation_plan_v1.json",
    ),
    ("output_personalization_boundary_plan", "output_personalization_boundary_plan_v1.json"),
    ("memory_worldmodel_task_state_boundary_plan", "memory_worldmodel_task_state_boundary_plan_v1.json"),
    ("output_plane_boundary_matrix", "output_plane_boundary_matrix_v1.json"),
    ("output_plane_dryrun_plan", "output_plane_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("output_plane_integration_planning_decision", "output_plane_integration_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--task-response-dryrun-root", default=DEFAULT_TASK_DR)
    p.add_argument("--task-response-planning-root", default=DEFAULT_TASK_PLAN)
    p.add_argument("--decision-center-dryrun-root", default=DEFAULT_DC_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    p.add_argument("--constitution-dryrun-root", default=DEFAULT_CONSTITUTION_DR)
    args = p.parse_args()

    result = run_midplatform_output_plane_integration_planning_v1(
        midplatform_task_response_candidate_integration_dryrun_and_review_root=args.task_response_dryrun_root,
        midplatform_task_response_candidate_integration_planning_root=args.task_response_planning_root,
        midplatform_decision_center_module_dryrun_and_review_root=args.decision_center_dryrun_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
        midplatform_constitution_governance_explanation_dryrun_and_review_root=args.constitution_dryrun_root,
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
                "output_plane_not_user_facing": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
