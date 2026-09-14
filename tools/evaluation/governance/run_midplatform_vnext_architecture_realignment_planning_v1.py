#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform vNext Architecture Realignment Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    run_midplatform_vnext_architecture_realignment_planning_v1,
)

DEFAULT_CR_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_controlled_runtime_dryrun_and_review"
)
DEFAULT_HEALTH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "health_enforcement_supervisor_dryrun_and_review"
)
DEFAULT_PROVIDER_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)
DEFAULT_FMIS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_frontend_model_influence_simulation_dryrun_and_review"
)
DEFAULT_E2E_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
)
DEFAULT_DISPLAY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_display_gate_dryrun_and_review"
)
DEFAULT_TTS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_dryrun_and_review"
)
DEFAULT_VALIDATION_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_validation_engineering_separation_dryrun_and_review"
)
DEFAULT_WHITEBOX_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_whitebox_inspection_integration_dryrun_and_review"
)
DEFAULT_CR_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_controlled_runtime_planning"
)
DEFAULT_SPEECH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_vnext_architecture_realignment_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "midplatform_vnext_architecture_realignment_policy",
        "midplatform_vnext_architecture_realignment_policy_v1.json",
    ),
    ("controlled_runtime_closure_input_review", "controlled_runtime_closure_input_review_v1.json"),
    ("midplatform_vnext_layer_model", "midplatform_vnext_layer_model_v1.json"),
    ("fixed_seed_core_positioning", "fixed_seed_core_positioning_v1.json"),
    ("reusable_governance_standard_layer", "reusable_governance_standard_layer_v1.json"),
    ("cognitive_zoning_positioning", "cognitive_zoning_positioning_v1.json"),
    ("pluggable_capability_layer_positioning", "pluggable_capability_layer_positioning_v1.json"),
    ("controlled_runtime_layer_positioning", "controlled_runtime_layer_positioning_v1.json"),
    ("product_form_layer_positioning", "product_form_layer_positioning_v1.json"),
    ("no_universal_midplatform_brain_policy", "no_universal_midplatform_brain_policy_v1.json"),
    ("no_module_sovereignty_policy", "no_module_sovereignty_policy_v1.json"),
    ("invariant_vs_variant_boundary_matrix", "invariant_vs_variant_boundary_matrix_v1.json"),
    ("post_detection_work_rhythm_plan", "post_detection_work_rhythm_plan_v1.json"),
    ("downstream_phase_sequence_decision", "downstream_phase_sequence_decision_v1.json"),
    ("deferred_runtime_register", "deferred_runtime_register_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "midplatform_vnext_architecture_realignment_decision",
        "midplatform_vnext_architecture_realignment_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--controlled-runtime-dryrun-root", default=DEFAULT_CR_DR)
    p.add_argument("--health-supervisor-dryrun-root", default=DEFAULT_HEALTH_DR)
    p.add_argument("--provider-abstraction-dryrun-root", default=DEFAULT_PROVIDER_DR)
    p.add_argument("--fmis-dryrun-root", default=DEFAULT_FMIS_DR)
    p.add_argument("--e2e-simulation-dryrun-root", default=DEFAULT_E2E_DR)
    p.add_argument("--display-gate-dryrun-root", default=DEFAULT_DISPLAY_DR)
    p.add_argument("--tts-runtime-dryrun-root", default=DEFAULT_TTS_DR)
    p.add_argument("--validation-dryrun-root", default=DEFAULT_VALIDATION_DR)
    p.add_argument("--whitebox-dryrun-root", default=DEFAULT_WHITEBOX_DR)
    p.add_argument("--controlled-runtime-planning-root", default=DEFAULT_CR_PLAN)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    args = p.parse_args()

    result = run_midplatform_vnext_architecture_realignment_planning_v1(
        midplatform_controlled_runtime_dryrun_and_review_root=args.controlled_runtime_dryrun_root,
        health_enforcement_supervisor_dryrun_and_review_root=args.health_supervisor_dryrun_root,
        provider_abstraction_standard_alignment_dryrun_and_review_root=args.provider_abstraction_dryrun_root,
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root=args.fmis_dryrun_root,
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root=args.e2e_simulation_dryrun_root,
        midplatform_display_gate_dryrun_and_review_root=args.display_gate_dryrun_root,
        midplatform_tts_runtime_dryrun_and_review_root=args.tts_runtime_dryrun_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_dryrun_root,
        midplatform_whitebox_inspection_integration_dryrun_and_review_root=args.whitebox_dryrun_root,
        midplatform_controlled_runtime_planning_root=args.controlled_runtime_planning_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "planning_pass": sm.get("planning_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
