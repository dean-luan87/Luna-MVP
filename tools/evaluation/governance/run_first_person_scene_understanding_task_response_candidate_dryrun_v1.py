#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run First Person Scene Understanding Task Response Candidate DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.first_person_scene_understanding_task_response_candidate_dryrun_v1 import (
    run_first_person_scene_understanding_task_response_candidate_dryrun_v1,
)

DEFAULT_DECISION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_decision_chain_candidate_dryrun"
)
DEFAULT_II_CHAIN_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_information_integration_chain_dryrun"
)
DEFAULT_STACK_STD_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "layered_capability_stack_standard_dryrun_and_review"
)
DEFAULT_TASK_RESP_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_task_response_candidate_integration_dryrun_and_review"
)
DEFAULT_OUTPUT_PLANE_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_dryrun_and_review"
)
DEFAULT_CB_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_task_response_candidate_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "first_person_scene_understanding_task_response_dryrun_policy",
        "first_person_scene_understanding_task_response_dryrun_policy_v1.json",
    ),
    ("decision_candidate_input_review", "decision_candidate_input_review_v1.json"),
    ("layered_capability_stack_input_review", "layered_capability_stack_input_review_v1.json"),
    ("layered_governance_mapping", "layered_governance_mapping_v1.json"),
    ("layered_governance_mapping_review", "layered_governance_mapping_review_v1.json"),
    (
        "first_person_task_response_assembly_model_candidate",
        "first_person_task_response_assembly_model_candidate_v1.json",
    ),
    ("sample_task_response_candidate", "sample_task_response_candidate_v1.json"),
    ("capability_stack_preservation_review", "capability_stack_preservation_review_v1.json"),
    ("scene_understanding_task_response_review", "scene_understanding_task_response_review_v1.json"),
    ("spatiotemporal_task_response_review", "spatiotemporal_task_response_review_v1.json"),
    (
        "navigation_application_task_response_review",
        "navigation_application_task_response_review_v1.json",
    ),
    ("survival_priority_task_response_review", "survival_priority_task_response_review_v1.json"),
    (
        "required_observation_task_response_review",
        "required_observation_task_response_review_v1.json",
    ),
    (
        "forbidden_actions_preservation_review",
        "forbidden_actions_preservation_review_v1.json",
    ),
    (
        "uncertainty_disclosure_candidate_review",
        "uncertainty_disclosure_candidate_review_v1.json",
    ),
    (
        "task_response_to_output_plane_handoff_plan",
        "task_response_to_output_plane_handoff_plan_v1.json",
    ),
    ("task_response_traceability_review", "task_response_traceability_review_v1.json"),
    ("task_response_boundary_audit", "task_response_boundary_audit_v1.json"),
    ("task_response_blocked_path_result", "task_response_blocked_path_result_v1.json"),
    ("task_response_closure_decision", "task_response_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--decision-chain-dryrun-root", default=DEFAULT_DECISION_DR)
    p.add_argument("--integration-chain-dryrun-root", default=DEFAULT_II_CHAIN_DR)
    p.add_argument("--layered-stack-standard-dryrun-root", default=DEFAULT_STACK_STD_DR)
    p.add_argument("--task-response-integration-dryrun-root", default=DEFAULT_TASK_RESP_DR)
    p.add_argument("--output-plane-integration-dryrun-root", default=DEFAULT_OUTPUT_PLANE_DR)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB_DR)
    args = p.parse_args()

    result = run_first_person_scene_understanding_task_response_candidate_dryrun_v1(
        first_person_scene_understanding_decision_chain_candidate_dryrun_root=args.decision_chain_dryrun_root,
        first_person_scene_understanding_information_integration_chain_dryrun_root=args.integration_chain_dryrun_root,
        layered_capability_stack_standard_dryrun_and_review_root=args.layered_stack_standard_dryrun_root,
        midplatform_task_response_candidate_integration_dryrun_and_review_root=args.task_response_integration_dryrun_root,
        midplatform_output_plane_integration_dryrun_and_review_root=args.output_plane_integration_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
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
