#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Scenario Model Governance and Capability Roadmap Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.scenario_model_governance_and_capability_roadmap_planning_v1 import (
    run_scenario_model_governance_and_capability_roadmap_planning_v1,
)

DEFAULT_CLOSURE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_output_chain_closure_review"
)
DEFAULT_GATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_user_output_gate_chain_dryrun"
)
DEFAULT_OUTPUT_CAND = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_output_candidate_dryrun"
)
DEFAULT_TASK_RESP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_task_response_candidate_dryrun"
)
DEFAULT_DECISION = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_decision_chain_candidate_dryrun"
)
DEFAULT_II = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_information_integration_chain_dryrun"
)
DEFAULT_STACK = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "layered_capability_stack_standard_dryrun_and_review"
)
DEFAULT_CB = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
)
DEFAULT_PROVIDER = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)
DEFAULT_DS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_drive_signal_contract_dryrun_and_review"
)
DEFAULT_SC_PLUG = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_pluggable_layer_architecture_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "scenario_model_governance_and_capability_roadmap_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("scenario_model_roadmap_planning_policy", "scenario_model_roadmap_planning_policy_v1.json"),
    ("upstream_output_chain_input_review", "upstream_output_chain_input_review_v1.json"),
    ("luna_model_capability_roadmap", "luna_model_capability_roadmap_v1.json"),
    ("goal_stage_to_model_capability_matrix", "goal_stage_to_model_capability_matrix_v1.json"),
    ("model_source_strategy_taxonomy", "model_source_strategy_taxonomy_v1.json"),
    ("external_open_source_candidate_register", "external_open_source_candidate_register_v1.json"),
    ("reference_research_product_candidate_register", "reference_research_product_candidate_register_v1.json"),
    ("self_developed_core_capability_register", "self_developed_core_capability_register_v1.json"),
    ("scene_model_requirement_matrix", "scene_model_requirement_matrix_v1.json"),
    ("module_local_model_profile_contract", "module_local_model_profile_contract_v1.json"),
    ("midplatform_model_governance_binding_contract", "midplatform_model_governance_binding_contract_v1.json"),
    ("model_input_output_contract_standard", "model_input_output_contract_standard_v1.json"),
    ("model_supervision_requirement_matrix", "model_supervision_requirement_matrix_v1.json"),
    ("model_quality_acceptance_criteria", "model_quality_acceptance_criteria_v1.json"),
    ("model_versioning_and_update_policy", "model_versioning_and_update_policy_v1.json"),
    ("model_replacement_and_fallback_policy", "model_replacement_and_fallback_policy_v1.json"),
    ("model_to_capability_stack_mapping", "model_to_capability_stack_mapping_v1.json"),
    ("model_to_governance_layer_mapping", "model_to_governance_layer_mapping_v1.json"),
    ("first_person_scene_understanding_model_roadmap", "first_person_scene_understanding_model_roadmap_v1.json"),
    ("spatiotemporal_world_continuity_model_roadmap", "spatiotemporal_world_continuity_model_roadmap_v1.json"),
    ("navigation_application_model_roadmap", "navigation_application_model_roadmap_v1.json"),
    ("extended_capability_model_roadmap", "extended_capability_model_roadmap_v1.json"),
    ("seed_core_and_evolution_model_boundary", "seed_core_and_evolution_model_boundary_v1.json"),
    ("roadmap_risk_register", "roadmap_risk_register_v1.json"),
    ("roadmap_dryrun_plan", "roadmap_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("scenario_model_roadmap_planning_decision", "scenario_model_roadmap_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--closure-review-root", default=DEFAULT_CLOSURE)
    p.add_argument("--gate-chain-dryrun-root", default=DEFAULT_GATE)
    p.add_argument("--output-candidate-dryrun-root", default=DEFAULT_OUTPUT_CAND)
    p.add_argument("--task-response-dryrun-root", default=DEFAULT_TASK_RESP)
    p.add_argument("--decision-chain-dryrun-root", default=DEFAULT_DECISION)
    p.add_argument("--ii-chain-dryrun-root", default=DEFAULT_II)
    p.add_argument("--stack-standard-dryrun-root", default=DEFAULT_STACK)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER)
    p.add_argument("--drive-signal-dryrun-root", default=DEFAULT_DS)
    p.add_argument("--seed-core-plug-dryrun-root", default=DEFAULT_SC_PLUG)
    args = p.parse_args()

    result = run_scenario_model_governance_and_capability_roadmap_planning_v1(
        first_person_scene_understanding_output_chain_closure_review_root=args.closure_review_root,
        first_person_scene_understanding_user_output_gate_chain_dryrun_root=args.gate_chain_dryrun_root,
        first_person_scene_understanding_output_candidate_dryrun_root=args.output_candidate_dryrun_root,
        first_person_scene_understanding_task_response_candidate_dryrun_root=args.task_response_dryrun_root,
        first_person_scene_understanding_decision_chain_candidate_dryrun_root=args.decision_chain_dryrun_root,
        first_person_scene_understanding_information_integration_chain_dryrun_root=args.ii_chain_dryrun_root,
        layered_capability_stack_standard_dryrun_and_review_root=args.stack_standard_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        seed_core_drive_signal_contract_dryrun_and_review_root=args.drive_signal_dryrun_root,
        seed_core_pluggable_layer_architecture_dryrun_and_review_root=args.seed_core_plug_dryrun_root,
        output_root=args.output_root,
    )

    out_root = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out_root / fname, result[key])

    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "planning_pass": result["summary"]["planning_pass"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
