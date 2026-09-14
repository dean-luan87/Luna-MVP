#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run World Continuity Module Model Profile + Governance Binding Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.world_continuity_module_model_profile_governance_binding_planning_v1 import (
    run_world_continuity_module_model_profile_governance_binding_planning_v1,
)

DEFAULT_MAP_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "map_navigation_module_model_profile_governance_binding_dryrun_and_review"
)
DEFAULT_ASR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "asr_module_model_profile_governance_binding_dryrun_and_review"
)
DEFAULT_TTS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "tts_module_model_profile_governance_binding_dryrun_and_review"
)
DEFAULT_OCR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_module_model_profile_governance_binding_dryrun_and_review"
)
DEFAULT_VISION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_module_model_profile_governance_binding_dryrun_and_review"
)
DEFAULT_BINDING_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_model_governance_binding_standardization_dryrun_and_review"
)
DEFAULT_ML_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "module_local_model_profile_standardization_dryrun_and_review"
)
DEFAULT_REGISTRY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_dryrun_and_review"
)
DEFAULT_II_CHAIN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "first_person_scene_understanding_information_integration_chain_dryrun"
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
    "world_continuity_module_model_profile_governance_binding_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "world_continuity_module_model_profile_governance_binding_planning_policy",
        "world_continuity_module_model_profile_governance_binding_planning_policy_v1.json",
    ),
    ("upstream_map_navigation_module_input_review", "upstream_map_navigation_module_input_review_v1.json"),
    ("governance_standard_reuse_review", "governance_standard_reuse_review_v1.json"),
    ("world_continuity_module_definition", "world_continuity_module_definition_v1.json"),
    (
        "world_continuity_capability_stack_definition",
        "world_continuity_capability_stack_definition_v1.json",
    ),
    (
        "world_continuity_layered_governance_mapping",
        "world_continuity_layered_governance_mapping_v1.json",
    ),
    ("world_continuity_module_local_model_profile", "world_continuity_module_local_model_profile_v1.json"),
    (
        "world_continuity_model_profile_registry_refs_review",
        "world_continuity_model_profile_registry_refs_review_v1.json",
    ),
    ("world_continuity_model_role_assignment_plan", "world_continuity_model_role_assignment_plan_v1.json"),
    ("world_continuity_input_contract", "world_continuity_input_contract_v1.json"),
    ("world_continuity_output_contract", "world_continuity_output_contract_v1.json"),
    ("world_continuity_quality_acceptance_plan", "world_continuity_quality_acceptance_plan_v1.json"),
    (
        "world_continuity_health_validation_whitebox_plan",
        "world_continuity_health_validation_whitebox_plan_v1.json",
    ),
    (
        "world_continuity_provider_runtime_boundary_plan",
        "world_continuity_provider_runtime_boundary_plan_v1.json",
    ),
    ("world_continuity_fallback_replacement_plan", "world_continuity_fallback_replacement_plan_v1.json"),
    (
        "world_continuity_module_internal_self_check_plan",
        "world_continuity_module_internal_self_check_plan_v1.json",
    ),
    (
        "world_continuity_midplatform_interaction_check_plan",
        "world_continuity_midplatform_interaction_check_plan_v1.json",
    ),
    (
        "world_continuity_midplatform_governance_binding",
        "world_continuity_midplatform_governance_binding_v1.json",
    ),
    (
        "world_continuity_information_integration_handoff_plan",
        "world_continuity_information_integration_handoff_plan_v1.json",
    ),
    (
        "world_continuity_decision_center_handoff_plan",
        "world_continuity_decision_center_handoff_plan_v1.json",
    ),
    (
        "world_continuity_worldmodel_admission_boundary_plan",
        "world_continuity_worldmodel_admission_boundary_plan_v1.json",
    ),
    (
        "world_continuity_memory_admission_boundary_plan",
        "world_continuity_memory_admission_boundary_plan_v1.json",
    ),
    ("world_continuity_layer_dependency_review", "world_continuity_layer_dependency_review_v1.json"),
    ("world_continuity_module_qualification_check", "world_continuity_module_qualification_check_v1.json"),
    ("world_continuity_non_runtime_boundary_matrix", "world_continuity_non_runtime_boundary_matrix_v1.json"),
    (
        "world_continuity_module_model_profile_governance_binding_dryrun_plan",
        "world_continuity_module_model_profile_governance_binding_dryrun_plan_v1.json",
    ),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "world_continuity_module_model_profile_governance_binding_planning_decision",
        "world_continuity_module_model_profile_governance_binding_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--map-dryrun-root", default=DEFAULT_MAP_DR)
    p.add_argument("--asr-dryrun-root", default=DEFAULT_ASR_DR)
    p.add_argument("--tts-dryrun-root", default=DEFAULT_TTS_DR)
    p.add_argument("--ocr-dryrun-root", default=DEFAULT_OCR_DR)
    p.add_argument("--vision-dryrun-root", default=DEFAULT_VISION_DR)
    p.add_argument("--binding-dryrun-root", default=DEFAULT_BINDING_DR)
    p.add_argument("--module-local-dryrun-root", default=DEFAULT_ML_DR)
    p.add_argument("--registry-dryrun-root", default=DEFAULT_REGISTRY_DR)
    p.add_argument("--ii-chain-dryrun-root", default=DEFAULT_II_CHAIN)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR)
    args = p.parse_args()

    result = run_world_continuity_module_model_profile_governance_binding_planning_v1(
        map_navigation_module_model_profile_governance_binding_dryrun_and_review_root=args.map_dryrun_root,
        asr_module_model_profile_governance_binding_dryrun_and_review_root=args.asr_dryrun_root,
        tts_module_model_profile_governance_binding_dryrun_and_review_root=args.tts_dryrun_root,
        ocr_module_model_profile_governance_binding_dryrun_and_review_root=args.ocr_dryrun_root,
        vision_module_model_profile_governance_binding_dryrun_and_review_root=args.vision_dryrun_root,
        midplatform_model_governance_binding_standardization_dryrun_and_review_root=args.binding_dryrun_root,
        module_local_model_profile_standardization_dryrun_and_review_root=args.module_local_dryrun_root,
        model_profile_registry_dryrun_and_review_root=args.registry_dryrun_root,
        first_person_scene_understanding_information_integration_chain_dryrun_root=args.ii_chain_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=(
            args.constitution_bus_dryrun_root
        ),
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
                "module_id": sm.get("module_id"),
                "capability_layer": sm.get("capability_layer"),
                "qualification_mode": sm.get("qualification_mode"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
