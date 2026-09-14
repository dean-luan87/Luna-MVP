#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Module-local Model Profile Standardization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    run_module_local_model_profile_standardization_planning_v1,
)

DEFAULT_REGISTRY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_dryrun_and_review"
)
DEFAULT_REGISTRY_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_planning"
)
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
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "module_local_model_profile_standardization_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "module_local_model_profile_standardization_planning_policy",
        "module_local_model_profile_standardization_planning_policy_v1.json",
    ),
    ("model_profile_registry_input_review", "model_profile_registry_input_review_v1.json"),
    ("governance_standard_reuse_review", "governance_standard_reuse_review_v1.json"),
    ("module_local_model_profile_standard_definition", "module_local_model_profile_standard_definition_v1.json"),
    ("module_local_model_profile_schema", "module_local_model_profile_schema_v1.json"),
    (
        "module_local_profile_to_registry_reference_policy",
        "module_local_profile_to_registry_reference_policy_v1.json",
    ),
    (
        "module_local_profile_capability_stack_binding_policy",
        "module_local_profile_capability_stack_binding_policy_v1.json",
    ),
    (
        "module_local_profile_layered_governance_binding_policy",
        "module_local_profile_layered_governance_binding_policy_v1.json",
    ),
    (
        "module_local_profile_input_output_binding_policy",
        "module_local_profile_input_output_binding_policy_v1.json",
    ),
    (
        "module_local_profile_quality_acceptance_binding_policy",
        "module_local_profile_quality_acceptance_binding_policy_v1.json",
    ),
    (
        "module_local_profile_health_validation_whitebox_binding_policy",
        "module_local_profile_health_validation_whitebox_binding_policy_v1.json",
    ),
    (
        "module_local_profile_provider_runtime_boundary_policy",
        "module_local_profile_provider_runtime_boundary_policy_v1.json",
    ),
    (
        "module_local_profile_fallback_replacement_policy",
        "module_local_profile_fallback_replacement_policy_v1.json",
    ),
    ("module_local_profile_midplatform_handoff_policy", "module_local_profile_midplatform_handoff_policy_v1.json"),
    ("module_internal_self_check_policy", "module_internal_self_check_policy_v1.json"),
    ("midplatform_interaction_check_policy", "midplatform_interaction_check_policy_v1.json"),
    ("vision_module_local_model_profile_template", "vision_module_local_model_profile_template_v1.json"),
    ("ocr_module_local_model_profile_template", "ocr_module_local_model_profile_template_v1.json"),
    ("tts_module_local_model_profile_template", "tts_module_local_model_profile_template_v1.json"),
    ("asr_module_local_model_profile_template", "asr_module_local_model_profile_template_v1.json"),
    (
        "map_navigation_module_local_model_profile_template",
        "map_navigation_module_local_model_profile_template_v1.json",
    ),
    (
        "world_continuity_module_local_model_profile_template",
        "world_continuity_module_local_model_profile_template_v1.json",
    ),
    (
        "memory_emotion_evolution_module_local_model_profile_template",
        "memory_emotion_evolution_module_local_model_profile_template_v1.json",
    ),
    ("module_local_profile_domain_coverage_matrix", "module_local_profile_domain_coverage_matrix_v1.json"),
    ("module_local_profile_non_runtime_boundary_matrix", "module_local_profile_non_runtime_boundary_matrix_v1.json"),
    ("module_local_profile_dryrun_plan", "module_local_profile_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "module_local_model_profile_standardization_planning_decision",
        "module_local_model_profile_standardization_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--registry-dryrun-root", default=DEFAULT_REGISTRY_DR)
    p.add_argument("--registry-planning-root", default=DEFAULT_REGISTRY_PLAN)
    p.add_argument("--roadmap-dryrun-root", default=DEFAULT_ROADMAP_DR)
    p.add_argument("--stack-standard-dryrun-root", default=DEFAULT_STACK)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR)
    args = p.parse_args()

    result = run_module_local_model_profile_standardization_planning_v1(
        model_profile_registry_dryrun_and_review_root=args.registry_dryrun_root,
        model_profile_registry_planning_root=args.registry_planning_root,
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
                "planning_pass": sm.get("planning_pass"),
                "template_count": sm.get("template_count"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
