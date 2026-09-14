#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Frontend Model Influence Simulation DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    run_midplatform_frontend_model_influence_simulation_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_frontend_model_influence_simulation_planning"
)
DEFAULT_PROVIDER_ABS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_planning"
)
DEFAULT_E2E_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
)
DEFAULT_UO_CONST_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_user_output_constitution_dryrun_and_review"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_SPEECH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_VOICE_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_voice_output_plane_dryrun_and_review"
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
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_frontend_model_influence_simulation_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    (
        "frontend_model_influence_simulation_dryrun_review_policy",
        "frontend_model_influence_simulation_dryrun_review_policy_v1.json",
    ),
    ("frontend_model_influence_planning_input_review", "frontend_model_influence_planning_input_review_v1.json"),
    ("front_model_type_inventory_review", "front_model_type_inventory_review_v1.json"),
    ("model_io_contract_influence_matrix", "model_io_contract_influence_matrix_v1.json"),
    ("rule_to_model_input_mapping_result", "rule_to_model_input_mapping_result_v1.json"),
    ("rule_to_model_output_mapping_result", "rule_to_model_output_mapping_result_v1.json"),
    ("health_to_model_behavior_mapping_result", "health_to_model_behavior_mapping_result_v1.json"),
    ("enforcement_to_model_permission_mapping_result", "enforcement_to_model_permission_mapping_result_v1.json"),
    ("whitebox_explainability_mapping_result", "whitebox_explainability_mapping_result_v1.json"),
    (
        "provider_abstraction_to_front_model_boundary_result",
        "provider_abstraction_to_front_model_boundary_result_v1.json",
    ),
    ("simulation_case_results", "simulation_case_results_v1.json"),
    ("expected_vs_actual_influence_matrix", "expected_vs_actual_influence_matrix_v1.json"),
    ("frontend_model_boundary_violation_matrix", "frontend_model_boundary_violation_matrix_v1.json"),
    ("frontend_model_traceability_matrix", "frontend_model_traceability_matrix_v1.json"),
    ("case_1_normal_allowed_model_input_result", "case_1_normal_allowed_model_input_result_v1.json"),
    ("case_2_privacy_masked_input_result", "case_2_privacy_masked_input_result_v1.json"),
    ("case_3_uncertainty_required_output_result", "case_3_uncertainty_required_output_result_v1.json"),
    ("case_4_safety_blocked_generation_result", "case_4_safety_blocked_generation_result_v1.json"),
    ("case_5_health_degraded_mode_result", "case_5_health_degraded_mode_result_v1.json"),
    ("case_6_provider_not_ready_result", "case_6_provider_not_ready_result_v1.json"),
    ("case_7_bypass_attempt_result", "case_7_bypass_attempt_result_v1.json"),
    ("case_8_rule_change_propagation_result", "case_8_rule_change_propagation_result_v1.json"),
    ("system_level_front_model_influence_review", "system_level_front_model_influence_review_v1.json"),
    ("next_route_readiness_decision", "next_route_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--planning-root", default=DEFAULT_PLANNING)
    p.add_argument("--provider-abstraction-planning-root", default=DEFAULT_PROVIDER_ABS)
    p.add_argument("--e2e-dryrun-root", default=DEFAULT_E2E_DR)
    p.add_argument("--user-output-constitution-dryrun-root", default=DEFAULT_UO_CONST_DR)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--voice-output-plane-dryrun-root", default=DEFAULT_VOICE_DR)
    p.add_argument("--tts-runtime-dryrun-root", default=DEFAULT_TTS_DR)
    p.add_argument("--validation-engineering-dryrun-root", default=DEFAULT_VALIDATION_DR)
    p.add_argument("--whitebox-dryrun-root", default=DEFAULT_WHITEBOX_DR)
    args = p.parse_args()

    result = run_midplatform_frontend_model_influence_simulation_dryrun_and_review_v1(
        midplatform_frontend_model_influence_simulation_planning_root=args.planning_root,
        provider_abstraction_standard_alignment_planning_root=args.provider_abstraction_planning_root,
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root=args.e2e_dryrun_root,
        midplatform_user_output_constitution_dryrun_and_review_root=args.user_output_constitution_dryrun_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_voice_output_plane_dryrun_and_review_root=args.voice_output_plane_dryrun_root,
        midplatform_tts_runtime_dryrun_and_review_root=args.tts_runtime_dryrun_root,
        midplatform_validation_engineering_separation_dryrun_and_review_root=args.validation_engineering_dryrun_root,
        midplatform_whitebox_inspection_integration_dryrun_and_review_root=args.whitebox_dryrun_root,
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "cases_passed": sm.get("cases_passed"),
                "case_count": sm.get("case_count"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
