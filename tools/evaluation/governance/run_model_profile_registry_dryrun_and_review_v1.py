#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Model Profile Registry DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    run_model_profile_registry_dryrun_and_review_v1,
)

DEFAULT_PLAN = "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_planning"
DEFAULT_ROADMAP_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review"
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
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_controlled_runtime_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("model_profile_registry_dryrun_review_policy", "model_profile_registry_dryrun_review_policy_v1.json"),
    ("planning_input_review", "planning_input_review_v1.json"),
    ("governance_standard_reuse_review", "governance_standard_reuse_review_v1.json"),
    ("model_profile_registry_candidate", "model_profile_registry_candidate_v1.json"),
    ("model_profile_schema_review", "model_profile_schema_review_v1.json"),
    ("model_profile_lifecycle_policy_review", "model_profile_lifecycle_policy_review_v1.json"),
    ("model_profile_status_taxonomy_review", "model_profile_status_taxonomy_review_v1.json"),
    ("source_license_metadata_schema_review", "source_license_metadata_schema_review_v1.json"),
    ("capability_layer_binding_schema_review", "capability_layer_binding_schema_review_v1.json"),
    ("model_input_output_profile_schema_review", "model_input_output_profile_schema_review_v1.json"),
    ("model_quality_acceptance_profile_schema_review", "model_quality_acceptance_profile_schema_review_v1.json"),
    (
        "health_validation_whitebox_profile_schema_review",
        "health_validation_whitebox_profile_schema_review_v1.json",
    ),
    (
        "provider_runtime_binding_profile_schema_review",
        "provider_runtime_binding_profile_schema_review_v1.json",
    ),
    (
        "version_update_replacement_profile_schema_review",
        "version_update_replacement_profile_schema_review_v1.json",
    ),
    ("registry_domain_index_review", "registry_domain_index_review_v1.json"),
    ("seed_model_profile_candidates_review", "seed_model_profile_candidates_review_v1.json"),
    ("vision_model_profile_seed_candidates_review", "vision_model_profile_seed_candidates_review_v1.json"),
    ("ocr_model_profile_seed_candidates_review", "ocr_model_profile_seed_candidates_review_v1.json"),
    ("tts_model_profile_seed_candidates_review", "tts_model_profile_seed_candidates_review_v1.json"),
    ("asr_model_profile_seed_candidates_review", "asr_model_profile_seed_candidates_review_v1.json"),
    (
        "map_navigation_model_profile_seed_candidates_review",
        "map_navigation_model_profile_seed_candidates_review_v1.json",
    ),
    (
        "world_continuity_model_profile_seed_candidates_review",
        "world_continuity_model_profile_seed_candidates_review_v1.json",
    ),
    (
        "memory_emotion_evolution_model_profile_seed_candidates_review",
        "memory_emotion_evolution_model_profile_seed_candidates_review_v1.json",
    ),
    ("module_local_binding_review", "module_local_binding_review_v1.json"),
    ("midplatform_governance_binding_review", "midplatform_governance_binding_review_v1.json"),
    ("registry_non_runtime_boundary_audit", "registry_non_runtime_boundary_audit_v1.json"),
    ("registry_blocked_path_result", "registry_blocked_path_result_v1.json"),
    ("registry_closure_decision", "registry_closure_decision_v1.json"),
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
    p.add_argument("--roadmap-dryrun-root", default=DEFAULT_ROADMAP_DR)
    p.add_argument("--stack-standard-dryrun-root", default=DEFAULT_STACK)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR)
    args = p.parse_args()

    result = run_model_profile_registry_dryrun_and_review_v1(
        model_profile_registry_planning_root=args.planning_root,
        scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_root=args.roadmap_dryrun_root,
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
