#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Voice Output Plane DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_voice_output_plane_dryrun_and_review_v1 import (
    run_midplatform_voice_output_plane_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_voice_output_plane_planning"
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
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_voice_output_plane_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("voice_output_plane_dryrun_review_policy", "voice_output_plane_dryrun_review_policy_v1.json"),
    ("voice_output_plane_planning_input_review", "voice_output_plane_planning_input_review_v1.json"),
    ("voice_output_plane_model_candidate", "voice_output_plane_model_candidate_v1.json"),
    ("sample_speech_gate_result_intake", "sample_speech_gate_result_intake_v1.json"),
    ("sample_speech_request_candidate", "sample_speech_request_candidate_v1.json"),
    ("execution_layer_identity_review", "execution_layer_identity_review_v1.json"),
    ("speech_gate_result_consumption_review", "speech_gate_result_consumption_review_v1.json"),
    ("no_raw_constitution_binding_review", "no_raw_constitution_binding_review_v1.json"),
    ("speech_gate_non_bypass_review", "speech_gate_non_bypass_review_v1.json"),
    ("tts_runtime_boundary_review", "tts_runtime_boundary_review_v1.json"),
    ("audio_output_boundary_review", "audio_output_boundary_review_v1.json"),
    (
        "voice_queue_interruption_boundary_review",
        "voice_queue_interruption_boundary_review_v1.json",
    ),
    ("speech_timing_priority_review", "speech_timing_priority_review_v1.json"),
    ("speech_content_rendering_boundary_review", "speech_content_rendering_boundary_review_v1.json"),
    ("voice_output_failure_route_review", "voice_output_failure_route_review_v1.json"),
    ("voice_output_traceability_review", "voice_output_traceability_review_v1.json"),
    ("voice_output_plane_boundary_audit", "voice_output_plane_boundary_audit_v1.json"),
    ("voice_output_plane_blocked_path_result", "voice_output_plane_blocked_path_result_v1.json"),
    ("voice_output_plane_closure_decision", "voice_output_plane_closure_decision_v1.json"),
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
    p.add_argument("--roadmap-decision-root", default=DEFAULT_ROADMAP)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--speech-gate-planning-root", default=DEFAULT_SPEECH_PLAN)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    args = p.parse_args()

    result = run_midplatform_voice_output_plane_dryrun_and_review_v1(
        midplatform_voice_output_plane_planning_root=args.planning_root,
        midplatform_voice_output_plane_roadmap_decision_root=args.roadmap_decision_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_speech_gate_planning_root=args.speech_gate_planning_root,
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
                "dryrun_and_review_pass": sm.get("dryrun_and_review_pass"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "execution_layer_validated": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
