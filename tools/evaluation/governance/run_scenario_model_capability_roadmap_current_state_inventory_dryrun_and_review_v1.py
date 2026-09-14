#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Scenario Model Capability Roadmap Current State Inventory DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_v1 import (
    run_scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_v1,
)

DEFAULT_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "scenario_model_capability_roadmap_current_state_inventory_planning"
)
DEFAULT_CLOSURE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_output_chain_closure_review"
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
DEFAULT_SC_PLUG = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "seed_core_pluggable_layer_architecture_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "scenario_model_capability_roadmap_inventory_dryrun_review_policy",
        "scenario_model_capability_roadmap_inventory_dryrun_review_policy_v1.json",
    ),
    ("planning_input_review", "planning_input_review_v1.json"),
    ("scenario_model_capability_roadmap_candidate", "scenario_model_capability_roadmap_candidate_v1.json"),
    ("capability_domain_inventory_review", "capability_domain_inventory_review_v1.json"),
    ("current_model_asset_inventory_review", "current_model_asset_inventory_review_v1.json"),
    ("goal_stage_to_capability_domain_review", "goal_stage_to_capability_domain_review_v1.json"),
    ("vision_scene_understanding_roadmap_review", "vision_scene_understanding_roadmap_review_v1.json"),
    ("ocr_text_reading_roadmap_review", "ocr_text_reading_roadmap_review_v1.json"),
    ("tts_voice_output_roadmap_review", "tts_voice_output_roadmap_review_v1.json"),
    ("asr_voice_input_roadmap_review", "asr_voice_input_roadmap_review_v1.json"),
    ("map_navigation_roadmap_review", "map_navigation_roadmap_review_v1.json"),
    ("spatiotemporal_world_continuity_roadmap_review", "spatiotemporal_world_continuity_roadmap_review_v1.json"),
    ("memory_personal_continuity_roadmap_review", "memory_personal_continuity_roadmap_review_v1.json"),
    ("emotion_engine_roadmap_review", "emotion_engine_roadmap_review_v1.json"),
    ("evolutionary_recursion_roadmap_review", "evolutionary_recursion_roadmap_review_v1.json"),
    ("provider_model_management_roadmap_review", "provider_model_management_roadmap_review_v1.json"),
    ("output_gate_chain_roadmap_review", "output_gate_chain_roadmap_review_v1.json"),
    (
        "health_whitebox_validation_governance_roadmap_review",
        "health_whitebox_validation_governance_roadmap_review_v1.json",
    ),
    ("model_source_strategy_review", "model_source_strategy_review_v1.json"),
    ("candidate_register_review", "candidate_register_review_v1.json"),
    ("module_local_model_profile_contract_review", "module_local_model_profile_contract_review_v1.json"),
    (
        "midplatform_model_governance_binding_contract_review",
        "midplatform_model_governance_binding_contract_review_v1.json",
    ),
    ("model_input_output_contract_review", "model_input_output_contract_review_v1.json"),
    ("model_quality_acceptance_criteria_review", "model_quality_acceptance_criteria_review_v1.json"),
    ("model_versioning_replacement_policy_review", "model_versioning_replacement_policy_review_v1.json"),
    ("current_gap_and_next_action_review", "current_gap_and_next_action_review_v1.json"),
    ("roadmap_risk_register_review", "roadmap_risk_register_review_v1.json"),
    ("roadmap_boundary_audit", "roadmap_boundary_audit_v1.json"),
    ("roadmap_blocked_path_result", "roadmap_blocked_path_result_v1.json"),
    ("roadmap_closure_decision", "roadmap_closure_decision_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLAN)
    p.add_argument("--closure-review-root", default=DEFAULT_CLOSURE)
    p.add_argument("--stack-standard-dryrun-root", default=DEFAULT_STACK)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER)
    p.add_argument("--seed-core-plug-dryrun-root", default=DEFAULT_SC_PLUG)
    args = p.parse_args()

    result = run_scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_v1(
        scenario_model_capability_roadmap_current_state_inventory_planning_root=args.planning_root,
        first_person_scene_understanding_output_chain_closure_review_root=args.closure_review_root,
        layered_capability_stack_standard_dryrun_and_review_root=args.stack_standard_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        seed_core_pluggable_layer_architecture_dryrun_and_review_root=args.seed_core_plug_dryrun_root,
        output_root=args.output_root,
    )

    out_root = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out_root / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out_root),
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
