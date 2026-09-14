#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run First Person Scene Understanding Output Chain Closure Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.first_person_scene_understanding_output_chain_closure_review_v1 import (
    run_first_person_scene_understanding_output_chain_closure_review_v1,
)

DEFAULT_GATE_CHAIN_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_user_output_gate_chain_dryrun"
)
DEFAULT_OUTPUT_CAND_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_output_candidate_dryrun"
)
DEFAULT_TASK_RESP_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_task_response_candidate_dryrun"
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
DEFAULT_CB_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
)
DEFAULT_II_LAYER_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_dryrun_and_review"
)
DEFAULT_DS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_drive_signal_contract_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_output_chain_closure_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "first_person_scene_understanding_output_chain_closure_review_policy",
        "first_person_scene_understanding_output_chain_closure_review_policy_v1.json",
    ),
    ("upstream_gate_chain_input_review", "upstream_gate_chain_input_review_v1.json"),
    ("full_chain_artifact_inventory", "full_chain_artifact_inventory_v1.json"),
    ("scene_understanding_chain_closure_matrix", "scene_understanding_chain_closure_matrix_v1.json"),
    (
        "capability_stack_preservation_closure_review",
        "capability_stack_preservation_closure_review_v1.json",
    ),
    (
        "layered_governance_mapping_closure_review",
        "layered_governance_mapping_closure_review_v1.json",
    ),
    (
        "information_integration_to_decision_closure_review",
        "information_integration_to_decision_closure_review_v1.json",
    ),
    (
        "decision_to_task_response_closure_review",
        "decision_to_task_response_closure_review_v1.json",
    ),
    (
        "task_response_to_output_candidate_closure_review",
        "task_response_to_output_candidate_closure_review_v1.json",
    ),
    (
        "output_candidate_to_gate_chain_closure_review",
        "output_candidate_to_gate_chain_closure_review_v1.json",
    ),
    ("gate_coverage_closure_review", "gate_coverage_closure_review_v1.json"),
    (
        "health_oversight_externality_closure_review",
        "health_oversight_externality_closure_review_v1.json",
    ),
    (
        "memory_worldmodel_task_navigation_runtime_block_closure_review",
        "memory_worldmodel_task_navigation_runtime_block_closure_review_v1.json",
    ),
    ("traceability_chain_closure_review", "traceability_chain_closure_review_v1.json"),
    ("closure_boundary_audit", "closure_boundary_audit_v1.json"),
    ("closure_blocked_path_result", "closure_blocked_path_result_v1.json"),
    ("next_workstream_readiness_decision", "next_workstream_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--gate-chain-dryrun-root", default=DEFAULT_GATE_CHAIN_DR)
    p.add_argument("--output-candidate-dryrun-root", default=DEFAULT_OUTPUT_CAND_DR)
    p.add_argument("--task-response-dryrun-root", default=DEFAULT_TASK_RESP_DR)
    p.add_argument("--decision-chain-dryrun-root", default=DEFAULT_DECISION_DR)
    p.add_argument("--ii-chain-dryrun-root", default=DEFAULT_II_CHAIN_DR)
    p.add_argument("--layered-stack-standard-dryrun-root", default=DEFAULT_STACK_STD_DR)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB_DR)
    p.add_argument("--ii-layer-dryrun-root", default=DEFAULT_II_LAYER_DR)
    p.add_argument("--drive-signal-dryrun-root", default=DEFAULT_DS_DR)
    args = p.parse_args()

    result = run_first_person_scene_understanding_output_chain_closure_review_v1(
        first_person_scene_understanding_user_output_gate_chain_dryrun_root=args.gate_chain_dryrun_root,
        first_person_scene_understanding_output_candidate_dryrun_root=args.output_candidate_dryrun_root,
        first_person_scene_understanding_task_response_candidate_dryrun_root=args.task_response_dryrun_root,
        first_person_scene_understanding_decision_chain_candidate_dryrun_root=args.decision_chain_dryrun_root,
        first_person_scene_understanding_information_integration_chain_dryrun_root=args.ii_chain_dryrun_root,
        layered_capability_stack_standard_dryrun_and_review_root=args.layered_stack_standard_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
        midplatform_information_integration_layer_dryrun_and_review_root=args.ii_layer_dryrun_root,
        seed_core_drive_signal_contract_dryrun_and_review_root=args.drive_signal_dryrun_root,
        output_root=args.output_root,
    )

    out_root = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out_root / fname, result[key])

    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "closure_review_pass": result["summary"]["closure_review_pass"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
