#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Task Response Candidate Integration Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_task_response_candidate_integration_planning_v1 import (
    run_midplatform_task_response_candidate_integration_planning_v1,
)

DEFAULT_FLOW_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_candidate_evidence_flow_integration_dryrun_and_review"
)
DEFAULT_DC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_dryrun_and_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_CORE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_core_architecture_resume"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_task_response_candidate_integration_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "task_response_candidate_integration_planning_policy",
        "task_response_candidate_integration_planning_policy_v1.json",
    ),
    (
        "upstream_candidate_evidence_flow_input_review",
        "upstream_candidate_evidence_flow_input_review_v1.json",
    ),
    ("task_response_candidate_module_definition", "task_response_candidate_module_definition_v1.json"),
    ("decision_candidate_intake_contract", "decision_candidate_intake_contract_v1.json"),
    ("task_response_candidate_output_contract", "task_response_candidate_output_contract_v1.json"),
    ("response_assembly_rule_plan", "response_assembly_rule_plan_v1.json"),
    ("response_action_mapping_plan", "response_action_mapping_plan_v1.json"),
    (
        "uncertainty_and_evidence_preservation_plan",
        "uncertainty_and_evidence_preservation_plan_v1.json",
    ),
    (
        "safety_and_constitution_output_boundary_plan",
        "safety_and_constitution_output_boundary_plan_v1.json",
    ),
    ("speech_output_boundary_plan", "speech_output_boundary_plan_v1.json"),
    ("memory_worldmodel_write_boundary_plan", "memory_worldmodel_write_boundary_plan_v1.json"),
    ("task_state_commit_boundary_plan", "task_state_commit_boundary_plan_v1.json"),
    ("failure_and_escalation_response_plan", "failure_and_escalation_response_plan_v1.json"),
    ("task_response_candidate_boundary_matrix", "task_response_candidate_boundary_matrix_v1.json"),
    ("task_response_candidate_dryrun_plan", "task_response_candidate_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "task_response_candidate_integration_planning_decision",
        "task_response_candidate_integration_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--flow-dryrun-root", default=DEFAULT_FLOW_DR)
    p.add_argument("--decision-center-dryrun-root", default=DEFAULT_DC_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    p.add_argument("--core-resume-root", default=DEFAULT_CORE)
    args = p.parse_args()

    result = run_midplatform_task_response_candidate_integration_planning_v1(
        midplatform_candidate_evidence_flow_integration_dryrun_and_review_root=args.flow_dryrun_root,
        midplatform_decision_center_module_dryrun_and_review_root=args.decision_center_dryrun_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
        midplatform_core_architecture_resume_root=args.core_resume_root,
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
                "assembly_not_user_output": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
