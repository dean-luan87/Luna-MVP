#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run First Person Scene Understanding User Output Gate Chain DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.first_person_scene_understanding_user_output_gate_chain_dryrun_v1 import (
    run_first_person_scene_understanding_user_output_gate_chain_dryrun_v1,
)

DEFAULT_OUTPUT_CAND_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_output_candidate_dryrun"
)
DEFAULT_TASK_RESP_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_task_response_candidate_dryrun"
)
DEFAULT_UOC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_user_output_constitution_dryrun_and_review"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_SPEECH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_DISPLAY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_display_gate_dryrun_and_review"
)
DEFAULT_CB_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
)
DEFAULT_STACK_STD_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "layered_capability_stack_standard_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_user_output_gate_chain_dryrun"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "first_person_scene_understanding_user_output_gate_chain_dryrun_policy",
        "first_person_scene_understanding_user_output_gate_chain_dryrun_policy_v1.json",
    ),
    ("output_candidate_input_review", "output_candidate_input_review_v1.json"),
    ("gate_coverage_matrix_input_review", "gate_coverage_matrix_input_review_v1.json"),
    ("user_output_gate_chain_model_candidate", "user_output_gate_chain_model_candidate_v1.json"),
    (
        "sample_user_output_constitution_gate_result_candidate",
        "sample_user_output_constitution_gate_result_candidate_v1.json",
    ),
    ("sample_safety_gate_result_candidate", "sample_safety_gate_result_candidate_v1.json"),
    ("sample_speech_gate_result_candidate", "sample_speech_gate_result_candidate_v1.json"),
    ("sample_display_gate_result_candidate", "sample_display_gate_result_candidate_v1.json"),
    ("sample_enforcement_result_candidate", "sample_enforcement_result_candidate_v1.json"),
    ("constitution_gate_chain_review", "constitution_gate_chain_review_v1.json"),
    ("safety_gate_chain_review", "safety_gate_chain_review_v1.json"),
    ("speech_gate_chain_review", "speech_gate_chain_review_v1.json"),
    ("display_gate_chain_review", "display_gate_chain_review_v1.json"),
    ("notification_gate_deferment_review", "notification_gate_deferment_review_v1.json"),
    (
        "memory_worldmodel_task_navigation_gate_block_review",
        "memory_worldmodel_task_navigation_gate_block_review_v1.json",
    ),
    (
        "privacy_identity_gate_deferment_review",
        "privacy_identity_gate_deferment_review_v1.json",
    ),
    ("health_oversight_gate_chain_review", "health_oversight_gate_chain_review_v1.json"),
    ("gate_result_traceability_review", "gate_result_traceability_review_v1.json"),
    (
        "gate_chain_to_execution_layer_handoff_plan",
        "gate_chain_to_execution_layer_handoff_plan_v1.json",
    ),
    ("gate_chain_boundary_audit", "gate_chain_boundary_audit_v1.json"),
    ("gate_chain_blocked_path_result", "gate_chain_blocked_path_result_v1.json"),
    ("gate_chain_closure_decision", "gate_chain_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--output-candidate-dryrun-root", default=DEFAULT_OUTPUT_CAND_DR)
    p.add_argument("--task-response-dryrun-root", default=DEFAULT_TASK_RESP_DR)
    p.add_argument("--user-output-constitution-dryrun-root", default=DEFAULT_UOC_DR)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--display-gate-dryrun-root", default=DEFAULT_DISPLAY_DR)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB_DR)
    p.add_argument("--layered-stack-standard-dryrun-root", default=DEFAULT_STACK_STD_DR)
    args = p.parse_args()

    result = run_first_person_scene_understanding_user_output_gate_chain_dryrun_v1(
        first_person_scene_understanding_output_candidate_dryrun_root=args.output_candidate_dryrun_root,
        first_person_scene_understanding_task_response_candidate_dryrun_root=args.task_response_dryrun_root,
        midplatform_user_output_constitution_dryrun_and_review_root=args.user_output_constitution_dryrun_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_display_gate_dryrun_and_review_root=args.display_gate_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
        layered_capability_stack_standard_dryrun_and_review_root=args.layered_stack_standard_dryrun_root,
        output_root=args.output_root,
    )

    out_root = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out_root / fname, result[key])

    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "dryrun_and_review_pass": result["summary"]["dryrun_and_review_pass"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
