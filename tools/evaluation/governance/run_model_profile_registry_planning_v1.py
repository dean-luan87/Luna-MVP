#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Profile Registry Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.model_profile_registry_planning_v1 import run_model_profile_registry_planning_v1

DEFAULT_ROADMAP_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review"
)
DEFAULT_ROADMAP_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "scenario_model_capability_roadmap_current_state_inventory_planning"
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
DEFAULT_CR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_controlled_runtime_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("model_profile_registry_planning_policy", "model_profile_registry_planning_policy_v1.json"),
    ("roadmap_input_review", "roadmap_input_review_v1.json"),
    ("model_profile_registry_definition", "model_profile_registry_definition_v1.json"),
    ("model_profile_schema", "model_profile_schema_v1.json"),
    ("model_profile_lifecycle_policy", "model_profile_lifecycle_policy_v1.json"),
    ("model_profile_status_taxonomy", "model_profile_status_taxonomy_v1.json"),
    ("model_source_and_license_metadata_schema", "model_source_and_license_metadata_schema_v1.json"),
    ("model_capability_layer_binding_schema", "model_capability_layer_binding_schema_v1.json"),
    ("model_input_output_profile_schema", "model_input_output_profile_schema_v1.json"),
    ("model_quality_acceptance_profile_schema", "model_quality_acceptance_profile_schema_v1.json"),
    ("model_health_validation_whitebox_profile_schema", "model_health_validation_whitebox_profile_schema_v1.json"),
    ("model_provider_runtime_binding_profile_schema", "model_provider_runtime_binding_profile_schema_v1.json"),
    ("model_version_update_replacement_profile_schema", "model_version_update_replacement_profile_schema_v1.json"),
    ("model_profile_registry_domain_index", "model_profile_registry_domain_index_v1.json"),
    ("seed_model_profile_candidates", "seed_model_profile_candidates_v1.json"),
    ("vision_model_profile_seed_candidates", "vision_model_profile_seed_candidates_v1.json"),
    ("ocr_model_profile_seed_candidates", "ocr_model_profile_seed_candidates_v1.json"),
    ("tts_model_profile_seed_candidates", "tts_model_profile_seed_candidates_v1.json"),
    ("asr_model_profile_seed_candidates", "asr_model_profile_seed_candidates_v1.json"),
    ("map_navigation_model_profile_seed_candidates", "map_navigation_model_profile_seed_candidates_v1.json"),
    ("world_continuity_model_profile_seed_candidates", "world_continuity_model_profile_seed_candidates_v1.json"),
    (
        "memory_emotion_evolution_model_profile_seed_candidates",
        "memory_emotion_evolution_model_profile_seed_candidates_v1.json",
    ),
    ("model_profile_to_module_local_binding_plan", "model_profile_to_module_local_binding_plan_v1.json"),
    (
        "model_profile_to_midplatform_governance_binding_plan",
        "model_profile_to_midplatform_governance_binding_plan_v1.json",
    ),
    ("model_profile_registry_non_runtime_boundary_matrix", "model_profile_registry_non_runtime_boundary_matrix_v1.json"),
    ("model_profile_registry_dryrun_plan", "model_profile_registry_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("model_profile_registry_planning_decision", "model_profile_registry_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--roadmap-dryrun-root", default=DEFAULT_ROADMAP_DR)
    p.add_argument("--roadmap-planning-root", default=DEFAULT_ROADMAP_PLAN)
    p.add_argument("--stack-standard-dryrun-root", default=DEFAULT_STACK)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR)
    args = p.parse_args()

    result = run_model_profile_registry_planning_v1(
        scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_root=args.roadmap_dryrun_root,
        scenario_model_capability_roadmap_current_state_inventory_planning_root=args.roadmap_planning_root,
        layered_capability_stack_standard_dryrun_and_review_root=args.stack_standard_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=args.constitution_bus_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        midplatform_controlled_runtime_dryrun_and_review_root=args.controlled_runtime_dryrun_root,
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
                "planning_pass": sm.get("planning_pass"),
                "seed_candidate_count": sm.get("seed_candidate_count"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
