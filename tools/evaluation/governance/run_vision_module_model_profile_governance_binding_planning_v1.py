#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Vision Module Model Profile + Governance Binding Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.vision_module_model_profile_governance_binding_planning_v1 import (
    run_vision_module_model_profile_governance_binding_planning_v1,
)

DEFAULT_BINDING_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_model_governance_binding_standardization_dryrun_and_review"
)
DEFAULT_BINDING_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_model_governance_binding_standardization_planning"
)
DEFAULT_ML_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "module_local_model_profile_standardization_dryrun_and_review"
)
DEFAULT_REGISTRY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_dryrun_and_review"
)
DEFAULT_FP_CLOSURE = (
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
DEFAULT_CR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_controlled_runtime_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "vision_module_model_profile_governance_binding_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "vision_module_model_profile_governance_binding_planning_policy",
        "vision_module_model_profile_governance_binding_planning_policy_v1.json",
    ),
    ("upstream_binding_standard_input_review", "upstream_binding_standard_input_review_v1.json"),
    ("governance_standard_reuse_review", "governance_standard_reuse_review_v1.json"),
    ("vision_module_definition", "vision_module_definition_v1.json"),
    ("vision_capability_stack_definition", "vision_capability_stack_definition_v1.json"),
    ("vision_layered_governance_mapping", "vision_layered_governance_mapping_v1.json"),
    ("vision_module_local_model_profile", "vision_module_local_model_profile_v1.json"),
    ("vision_model_profile_registry_refs_review", "vision_model_profile_registry_refs_review_v1.json"),
    ("vision_model_role_assignment_plan", "vision_model_role_assignment_plan_v1.json"),
    ("vision_input_contract", "vision_input_contract_v1.json"),
    ("vision_output_contract", "vision_output_contract_v1.json"),
    ("vision_quality_acceptance_plan", "vision_quality_acceptance_plan_v1.json"),
    ("vision_health_validation_whitebox_plan", "vision_health_validation_whitebox_plan_v1.json"),
    ("vision_provider_runtime_boundary_plan", "vision_provider_runtime_boundary_plan_v1.json"),
    ("vision_fallback_replacement_plan", "vision_fallback_replacement_plan_v1.json"),
    ("vision_module_internal_self_check_plan", "vision_module_internal_self_check_plan_v1.json"),
    ("vision_midplatform_interaction_check_plan", "vision_midplatform_interaction_check_plan_v1.json"),
    ("vision_midplatform_governance_binding", "vision_midplatform_governance_binding_v1.json"),
    ("vision_information_integration_handoff_plan", "vision_information_integration_handoff_plan_v1.json"),
    ("vision_decision_center_handoff_plan", "vision_decision_center_handoff_plan_v1.json"),
    ("vision_gate_chain_boundary_plan", "vision_gate_chain_boundary_plan_v1.json"),
    (
        "vision_memory_worldmodel_admission_boundary_plan",
        "vision_memory_worldmodel_admission_boundary_plan_v1.json",
    ),
    ("vision_non_runtime_boundary_matrix", "vision_non_runtime_boundary_matrix_v1.json"),
    ("vision_module_qualification_check", "vision_module_qualification_check_v1.json"),
    (
        "vision_module_model_profile_governance_binding_dryrun_plan",
        "vision_module_model_profile_governance_binding_dryrun_plan_v1.json",
    ),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "vision_module_model_profile_governance_binding_planning_decision",
        "vision_module_model_profile_governance_binding_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--binding-dryrun-root", default=DEFAULT_BINDING_DR)
    p.add_argument("--binding-planning-root", default=DEFAULT_BINDING_PLAN)
    p.add_argument("--module-local-dryrun-root", default=DEFAULT_ML_DR)
    p.add_argument("--registry-dryrun-root", default=DEFAULT_REGISTRY_DR)
    p.add_argument("--fp-closure-root", default=DEFAULT_FP_CLOSURE)
    p.add_argument("--stack-standard-dryrun-root", default=DEFAULT_STACK)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR)
    args = p.parse_args()

    result = run_vision_module_model_profile_governance_binding_planning_v1(
        midplatform_model_governance_binding_standardization_dryrun_and_review_root=args.binding_dryrun_root,
        midplatform_model_governance_binding_standardization_planning_root=args.binding_planning_root,
        module_local_model_profile_standardization_dryrun_and_review_root=args.module_local_dryrun_root,
        model_profile_registry_dryrun_and_review_root=args.registry_dryrun_root,
        first_person_scene_understanding_output_chain_closure_review_root=args.fp_closure_root,
        layered_capability_stack_standard_dryrun_and_review_root=args.stack_standard_dryrun_root,
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
                "registry_ref_count": sm.get("registry_model_profile_ref_count"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
