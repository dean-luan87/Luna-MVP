#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Voice Output Plane Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_voice_output_plane_planning_v1 import (
    run_midplatform_voice_output_plane_planning_v1,
)

DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_voice_output_plane_roadmap_decision"
)
DEFAULT_SPEECH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_SPEECH_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_planning"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_voice_output_plane_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("voice_output_plane_planning_policy", "voice_output_plane_planning_policy_v1.json"),
    ("voice_output_plane_roadmap_input_review", "voice_output_plane_roadmap_input_review_v1.json"),
    ("voice_output_plane_module_definition", "voice_output_plane_module_definition_v1.json"),
    ("speech_gate_result_intake_contract", "speech_gate_result_intake_contract_v1.json"),
    ("speech_request_candidate_contract", "speech_request_candidate_contract_v1.json"),
    ("voice_output_execution_scope_plan", "voice_output_execution_scope_plan_v1.json"),
    ("tts_runtime_boundary_plan", "tts_runtime_boundary_plan_v1.json"),
    ("audio_output_boundary_plan", "audio_output_boundary_plan_v1.json"),
    (
        "voice_queue_and_interruption_boundary_plan",
        "voice_queue_and_interruption_boundary_plan_v1.json",
    ),
    ("speech_timing_and_priority_plan", "speech_timing_and_priority_plan_v1.json"),
    ("speech_content_rendering_boundary_plan", "speech_content_rendering_boundary_plan_v1.json"),
    ("voice_output_failure_route_plan", "voice_output_failure_route_plan_v1.json"),
    ("voice_output_traceability_plan", "voice_output_traceability_plan_v1.json"),
    ("voice_output_no_raw_constitution_policy", "voice_output_no_raw_constitution_policy_v1.json"),
    ("voice_output_speech_gate_non_bypass_policy", "voice_output_speech_gate_non_bypass_policy_v1.json"),
    ("voice_output_plane_boundary_matrix", "voice_output_plane_boundary_matrix_v1.json"),
    ("voice_output_plane_dryrun_plan", "voice_output_plane_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("voice_output_plane_planning_decision", "voice_output_plane_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--roadmap-decision-root", default=DEFAULT_ROADMAP)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--speech-gate-planning-root", default=DEFAULT_SPEECH_PLAN)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    args = p.parse_args()

    result = run_midplatform_voice_output_plane_planning_v1(
        midplatform_voice_output_plane_roadmap_decision_root=args.roadmap_decision_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_speech_gate_planning_root=args.speech_gate_planning_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
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
                "execution_layer_planning_only": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
