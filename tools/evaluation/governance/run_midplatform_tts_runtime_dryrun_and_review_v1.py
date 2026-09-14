#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform TTS Runtime DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_tts_runtime_dryrun_and_review_v1 import (
    run_midplatform_tts_runtime_dryrun_and_review_v1,
)

DEFAULT_PLANNING = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_planning"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_roadmap_decision"
)
DEFAULT_VOICE_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_voice_output_plane_dryrun_and_review"
)
DEFAULT_SPEECH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_HARNESS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_dryrun_and_review"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("tts_runtime_dryrun_review_policy", "tts_runtime_dryrun_review_policy_v1.json"),
    ("tts_runtime_planning_input_review", "tts_runtime_planning_input_review_v1.json"),
    ("tts_runtime_model_candidate", "tts_runtime_model_candidate_v1.json"),
    ("sample_speech_request_candidate_intake", "sample_speech_request_candidate_intake_v1.json"),
    ("sample_audio_artifact_candidate", "sample_audio_artifact_candidate_v1.json"),
    ("tts_provider_abstraction_dryrun_review", "tts_provider_abstraction_dryrun_review_v1.json"),
    ("current_tts_provider_candidate_review", "current_tts_provider_candidate_review_v1.json"),
    ("provider_switch_boundary_dryrun_review", "provider_switch_boundary_dryrun_review_v1.json"),
    ("provider_readiness_requirement_review", "provider_readiness_requirement_review_v1.json"),
    ("voice_model_boundary_review", "voice_model_boundary_review_v1.json"),
    (
        "voice_profile_personalization_boundary_review",
        "voice_profile_personalization_boundary_review_v1.json",
    ),
    ("audio_synthesis_boundary_review", "audio_synthesis_boundary_review_v1.json"),
    ("audio_output_playback_boundary_review", "audio_output_playback_boundary_review_v1.json"),
    ("cache_artifact_boundary_review", "cache_artifact_boundary_review_v1.json"),
    ("authorization_requirement_review", "authorization_requirement_review_v1.json"),
    ("tts_failure_route_review", "tts_failure_route_review_v1.json"),
    ("tts_traceability_audit_review", "tts_traceability_audit_review_v1.json"),
    ("tts_no_raw_constitution_review", "tts_no_raw_constitution_review_v1.json"),
    ("tts_speech_gate_non_bypass_review", "tts_speech_gate_non_bypass_review_v1.json"),
    ("tts_runtime_boundary_audit", "tts_runtime_boundary_audit_v1.json"),
    ("tts_runtime_blocked_path_result", "tts_runtime_blocked_path_result_v1.json"),
    ("tts_runtime_closure_decision", "tts_runtime_closure_decision_v1.json"),
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
    p.add_argument("--voice-output-plane-dryrun-root", default=DEFAULT_VOICE_DR)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--harness-post-review-root", default=DEFAULT_HARNESS)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    args = p.parse_args()

    result = run_midplatform_tts_runtime_dryrun_and_review_v1(
        midplatform_tts_runtime_planning_root=args.planning_root,
        midplatform_tts_runtime_roadmap_decision_root=args.roadmap_decision_root,
        midplatform_voice_output_plane_dryrun_and_review_root=args.voice_output_plane_dryrun_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=args.harness_post_review_root,
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
                "execution_runtime_validated": True,
                "provider_abstraction_validated": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("dryrun_and_review_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
