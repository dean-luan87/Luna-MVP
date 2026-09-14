#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform End-to-End Output Chain Simulation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_end_to_end_output_chain_simulation_planning_v1 import (
    SIMULATION_CASES,
    run_midplatform_end_to_end_output_chain_simulation_planning_v1,
)

DEFAULT_TTS_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_dryrun_and_review"
)
DEFAULT_VOICE_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_voice_output_plane_dryrun_and_review"
)
DEFAULT_SPEECH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_UO_CONST_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_user_output_constitution_dryrun_and_review"
)
DEFAULT_OP_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_dryrun_and_review"
)
DEFAULT_TRC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_task_response_candidate_integration_dryrun_and_review"
)
DEFAULT_CEF_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_candidate_evidence_flow_integration_dryrun_and_review"
)
DEFAULT_DC_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_decision_center_module_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_end_to_end_output_chain_simulation_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("end_to_end_output_chain_simulation_planning_policy", "end_to_end_output_chain_simulation_planning_policy_v1.json"),
    ("upstream_output_chain_input_review", "upstream_output_chain_input_review_v1.json"),
    ("simulation_scope_definition", "simulation_scope_definition_v1.json"),
    ("output_chain_stage_inventory", "output_chain_stage_inventory_v1.json"),
    ("simulation_case_matrix", "simulation_case_matrix_v1.json"),
    ("stage_handoff_contract_review_plan", "stage_handoff_contract_review_plan_v1.json"),
    ("rule_resolution_enforcement_execution_review_plan", "rule_resolution_enforcement_execution_review_plan_v1.json"),
    ("traceability_preservation_review_plan", "traceability_preservation_review_plan_v1.json"),
    ("boundary_and_non_claims_review_plan", "boundary_and_non_claims_review_plan_v1.json"),
    ("expected_simulation_outputs_contract", "expected_simulation_outputs_contract_v1.json"),
    ("simulation_dryrun_plan", "simulation_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "end_to_end_output_chain_simulation_planning_decision",
        "end_to_end_output_chain_simulation_planning_decision_v1.json",
    ),
) + tuple(
    (c["plan_file"].replace("_v1.json", ""), c["plan_file"]) for c in SIMULATION_CASES
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--tts-runtime-dryrun-root", default=DEFAULT_TTS_DR)
    p.add_argument("--voice-output-plane-dryrun-root", default=DEFAULT_VOICE_DR)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--user-output-constitution-dryrun-root", default=DEFAULT_UO_CONST_DR)
    p.add_argument("--output-plane-integration-dryrun-root", default=DEFAULT_OP_DR)
    p.add_argument("--task-response-integration-dryrun-root", default=DEFAULT_TRC_DR)
    p.add_argument("--candidate-evidence-flow-dryrun-root", default=DEFAULT_CEF_DR)
    p.add_argument("--decision-center-dryrun-root", default=DEFAULT_DC_DR)
    args = p.parse_args()

    result = run_midplatform_end_to_end_output_chain_simulation_planning_v1(
        midplatform_tts_runtime_dryrun_and_review_root=args.tts_runtime_dryrun_root,
        midplatform_voice_output_plane_dryrun_and_review_root=args.voice_output_plane_dryrun_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        midplatform_user_output_constitution_dryrun_and_review_root=args.user_output_constitution_dryrun_root,
        midplatform_output_plane_integration_dryrun_and_review_root=args.output_plane_integration_dryrun_root,
        midplatform_task_response_candidate_integration_dryrun_and_review_root=args.task_response_integration_dryrun_root,
        midplatform_candidate_evidence_flow_integration_dryrun_and_review_root=args.candidate_evidence_flow_dryrun_root,
        midplatform_decision_center_module_dryrun_and_review_root=args.decision_center_dryrun_root,
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
                "case_count": 8,
                "stage_count": 23,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
