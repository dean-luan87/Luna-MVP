#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Task Response Candidate Integration DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_task_response_candidate_integration_dryrun_and_review_v1 import (
    run_midplatform_task_response_candidate_integration_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_task_response_candidate_integration_planning"
)
DEFAULT_DC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_dryrun_and_review"
)
DEFAULT_FLOW_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_candidate_evidence_flow_integration_dryrun_and_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_task_response_candidate_integration_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "task_response_candidate_integration_dryrun_review_policy",
        "task_response_candidate_integration_dryrun_review_policy_v1.json",
    ),
    (
        "task_response_candidate_planning_input_review",
        "task_response_candidate_planning_input_review_v1.json",
    ),
    ("task_response_integration_model_candidate", "task_response_integration_model_candidate_v1.json"),
    ("sample_decision_candidate_intake", "sample_decision_candidate_intake_v1.json"),
    ("sample_task_response_candidate", "sample_task_response_candidate_v1.json"),
    ("response_action_mapping_dryrun_review", "response_action_mapping_dryrun_review_v1.json"),
    ("uncertainty_evidence_preservation_review", "uncertainty_evidence_preservation_review_v1.json"),
    (
        "safety_constitution_output_boundary_review",
        "safety_constitution_output_boundary_review_v1.json",
    ),
    ("speech_output_boundary_review", "speech_output_boundary_review_v1.json"),
    ("memory_worldmodel_write_boundary_review", "memory_worldmodel_write_boundary_review_v1.json"),
    ("task_state_commit_boundary_review", "task_state_commit_boundary_review_v1.json"),
    ("failure_escalation_response_dryrun_review", "failure_escalation_response_dryrun_review_v1.json"),
    ("task_response_candidate_boundary_audit", "task_response_candidate_boundary_audit_v1.json"),
    (
        "task_response_candidate_blocked_path_result",
        "task_response_candidate_blocked_path_result_v1.json",
    ),
    ("task_response_candidate_closure_decision", "task_response_candidate_closure_decision_v1.json"),
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
    p.add_argument("--decision-center-dryrun-root", default=DEFAULT_DC_DR)
    p.add_argument("--flow-dryrun-root", default=DEFAULT_FLOW_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    args = p.parse_args()

    result = run_midplatform_task_response_candidate_integration_dryrun_and_review_v1(
        midplatform_task_response_candidate_integration_planning_root=args.planning_root,
        midplatform_decision_center_module_dryrun_and_review_root=args.decision_center_dryrun_root,
        midplatform_candidate_evidence_flow_integration_dryrun_and_review_root=args.flow_dryrun_root,
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "main_chain_closed": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
