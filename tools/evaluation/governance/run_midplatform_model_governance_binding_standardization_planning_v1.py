#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Model Governance Binding Standardization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    run_midplatform_model_governance_binding_standardization_planning_v1,
)

DEFAULT_ML_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "module_local_model_profile_standardization_dryrun_and_review"
)
DEFAULT_ML_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "module_local_model_profile_standardization_planning"
)
DEFAULT_REGISTRY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_dryrun_and_review"
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
DEFAULT_II = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_information_integration_layer_dryrun_and_review"
)
DEFAULT_SAFETY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_SPEECH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_DISPLAY = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_model_governance_binding_standardization_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "midplatform_model_governance_binding_standardization_planning_policy",
        "midplatform_model_governance_binding_standardization_planning_policy_v1.json",
    ),
    ("module_local_profile_input_review", "module_local_profile_input_review_v1.json"),
    ("governance_standard_reuse_review", "governance_standard_reuse_review_v1.json"),
    (
        "midplatform_model_governance_binding_standard_definition",
        "midplatform_model_governance_binding_standard_definition_v1.json",
    ),
    (
        "midplatform_model_governance_binding_schema",
        "midplatform_model_governance_binding_schema_v1.json",
    ),
    ("constitution_bus_binding_policy", "constitution_bus_binding_policy_v1.json"),
    ("capability_bus_binding_policy", "capability_bus_binding_policy_v1.json"),
    ("provider_abstraction_binding_policy", "provider_abstraction_binding_policy_v1.json"),
    ("validation_binding_policy", "validation_binding_policy_v1.json"),
    ("health_oversight_binding_policy", "health_oversight_binding_policy_v1.json"),
    ("whitebox_trace_binding_policy", "whitebox_trace_binding_policy_v1.json"),
    (
        "information_integration_binding_policy",
        "information_integration_binding_policy_v1.json",
    ),
    ("decision_center_binding_policy", "decision_center_binding_policy_v1.json"),
    ("gate_chain_binding_policy", "gate_chain_binding_policy_v1.json"),
    ("controlled_runtime_binding_policy", "controlled_runtime_binding_policy_v1.json"),
    (
        "memory_worldmodel_admission_binding_policy",
        "memory_worldmodel_admission_binding_policy_v1.json",
    ),
    (
        "model_governance_binding_by_capability_layer",
        "model_governance_binding_by_capability_layer_v1.json",
    ),
    (
        "model_governance_binding_by_module_domain",
        "model_governance_binding_by_module_domain_v1.json",
    ),
    (
        "vision_model_governance_binding_template",
        "vision_model_governance_binding_template_v1.json",
    ),
    ("ocr_model_governance_binding_template", "ocr_model_governance_binding_template_v1.json"),
    ("tts_model_governance_binding_template", "tts_model_governance_binding_template_v1.json"),
    ("asr_model_governance_binding_template", "asr_model_governance_binding_template_v1.json"),
    (
        "map_navigation_model_governance_binding_template",
        "map_navigation_model_governance_binding_template_v1.json",
    ),
    (
        "world_continuity_model_governance_binding_template",
        "world_continuity_model_governance_binding_template_v1.json",
    ),
    (
        "memory_emotion_evolution_model_governance_binding_template",
        "memory_emotion_evolution_model_governance_binding_template_v1.json",
    ),
    (
        "dual_validation_to_midplatform_binding_handoff_policy",
        "dual_validation_to_midplatform_binding_handoff_policy_v1.json",
    ),
    (
        "non_compliance_handling_deferment_review",
        "non_compliance_handling_deferment_review_v1.json",
    ),
    (
        "midplatform_model_governance_binding_non_runtime_boundary_matrix",
        "midplatform_model_governance_binding_non_runtime_boundary_matrix_v1.json",
    ),
    (
        "midplatform_model_governance_binding_dryrun_plan",
        "midplatform_model_governance_binding_dryrun_plan_v1.json",
    ),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "midplatform_model_governance_binding_standardization_planning_decision",
        "midplatform_model_governance_binding_standardization_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--module-local-dryrun-root", default=DEFAULT_ML_DR)
    p.add_argument("--module-local-planning-root", default=DEFAULT_ML_PLAN)
    p.add_argument("--registry-dryrun-root", default=DEFAULT_REGISTRY_DR)
    p.add_argument("--constitution-bus-dryrun-root", default=DEFAULT_CB)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR)
    p.add_argument("--information-integration-dryrun-root", default=DEFAULT_II)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH)
    p.add_argument("--display-gate-dryrun-root", default=DEFAULT_DISPLAY)
    args = p.parse_args()

    result = run_midplatform_model_governance_binding_standardization_planning_v1(
        module_local_model_profile_standardization_dryrun_and_review_root=args.module_local_dryrun_root,
        module_local_model_profile_standardization_planning_root=args.module_local_planning_root,
        model_profile_registry_dryrun_and_review_root=args.registry_dryrun_root,
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root=(
            args.constitution_bus_dryrun_root
        ),
        provider_abstraction_standard_alignment_dryrun_and_review_root=(
            args.provider_abstraction_dryrun_root
        ),
        midplatform_controlled_runtime_dryrun_and_review_root=args.controlled_runtime_dryrun_root,
        midplatform_information_integration_layer_dryrun_and_review_root=(
            args.information_integration_dryrun_root
        ),
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_display_gate_dryrun_and_review_root=args.display_gate_dryrun_root,
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
                "binding_policy_count": sm.get("binding_policy_count"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
