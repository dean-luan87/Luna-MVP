#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform TTS Runtime Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    run_midplatform_tts_runtime_planning_v1,
)

DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_roadmap_decision"
)
DEFAULT_VOICE_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_voice_output_plane_dryrun_and_review"
)
DEFAULT_VOICE_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_voice_output_plane_planning"
)
DEFAULT_SPEECH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_TEMPLATE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)
DEFAULT_HARNESS = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("tts_runtime_planning_policy", "tts_runtime_planning_policy_v1.json"),
    ("tts_runtime_roadmap_input_review", "tts_runtime_roadmap_input_review_v1.json"),
    ("tts_runtime_module_definition", "tts_runtime_module_definition_v1.json"),
    ("speech_request_candidate_intake_contract", "speech_request_candidate_intake_contract_v1.json"),
    ("tts_runtime_output_contract", "tts_runtime_output_contract_v1.json"),
    ("tts_provider_abstraction_plan", "tts_provider_abstraction_plan_v1.json"),
    ("current_tts_provider_candidate_register", "current_tts_provider_candidate_register_v1.json"),
    ("provider_switch_boundary_plan", "provider_switch_boundary_plan_v1.json"),
    ("tts_provider_readiness_plan", "tts_provider_readiness_plan_v1.json"),
    ("tts_voice_model_boundary_plan", "tts_voice_model_boundary_plan_v1.json"),
    (
        "tts_voice_profile_personalization_boundary_plan",
        "tts_voice_profile_personalization_boundary_plan_v1.json",
    ),
    ("tts_audio_synthesis_boundary_plan", "tts_audio_synthesis_boundary_plan_v1.json"),
    ("tts_audio_output_playback_boundary_plan", "tts_audio_output_playback_boundary_plan_v1.json"),
    ("tts_cache_and_artifact_boundary_plan", "tts_cache_and_artifact_boundary_plan_v1.json"),
    ("tts_authorization_requirement_plan", "tts_authorization_requirement_plan_v1.json"),
    ("tts_failure_route_plan", "tts_failure_route_plan_v1.json"),
    ("tts_traceability_audit_plan", "tts_traceability_audit_plan_v1.json"),
    ("tts_no_raw_constitution_policy", "tts_no_raw_constitution_policy_v1.json"),
    ("tts_speech_gate_non_bypass_policy", "tts_speech_gate_non_bypass_policy_v1.json"),
    ("tts_runtime_boundary_matrix", "tts_runtime_boundary_matrix_v1.json"),
    ("tts_runtime_dryrun_plan", "tts_runtime_dryrun_plan_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    ("tts_runtime_planning_decision", "tts_runtime_planning_decision_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--roadmap-decision-root", default=DEFAULT_ROADMAP)
    p.add_argument("--voice-output-plane-dryrun-root", default=DEFAULT_VOICE_DR)
    p.add_argument("--voice-output-plane-planning-root", default=DEFAULT_VOICE_PLAN)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--template-planning-root", default=DEFAULT_TEMPLATE)
    p.add_argument("--harness-post-review-root", default=DEFAULT_HARNESS)
    args = p.parse_args()

    result = run_midplatform_tts_runtime_planning_v1(
        midplatform_tts_runtime_roadmap_decision_root=args.roadmap_decision_root,
        midplatform_voice_output_plane_dryrun_and_review_root=args.voice_output_plane_dryrun_root,
        midplatform_voice_output_plane_planning_root=args.voice_output_plane_planning_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_module_definition_template_planning_root=args.template_planning_root,
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root=args.harness_post_review_root,
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
                "tts_runtime_planning_only": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
