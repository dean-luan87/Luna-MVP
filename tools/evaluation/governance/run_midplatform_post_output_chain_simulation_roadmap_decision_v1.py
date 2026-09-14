#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Post-Output-Chain-Simulation Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_post_output_chain_simulation_roadmap_decision_v1 import (
    run_midplatform_post_output_chain_simulation_roadmap_decision_v1,
)

DEFAULT_E2E_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
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
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_post_output_chain_simulation_roadmap_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("post_output_chain_simulation_roadmap_policy", "post_output_chain_simulation_roadmap_policy_v1.json"),
    ("system_level_simulation_input_review", "system_level_simulation_input_review_v1.json"),
    (
        "route_a_provider_abstraction_alignment_assessment",
        "route_a_provider_abstraction_alignment_assessment_v1.json",
    ),
    ("route_b_display_gate_planning_assessment", "route_b_display_gate_planning_assessment_v1.json"),
    (
        "route_c_controlled_runtime_planning_assessment",
        "route_c_controlled_runtime_planning_assessment_v1.json",
    ),
    ("route_d_direct_real_tts_audio_assessment", "route_d_direct_real_tts_audio_assessment_v1.json"),
    (
        "route_e_health_enforcement_supervisor_assessment",
        "route_e_health_enforcement_supervisor_assessment_v1.json",
    ),
    ("post_simulation_route_selection_matrix", "post_simulation_route_selection_matrix_v1.json"),
    ("selected_route_preconditions", "selected_route_preconditions_v1.json"),
    ("deferred_routes_register", "deferred_routes_register_v1.json"),
    ("blocked_routes_register", "blocked_routes_register_v1.json"),
    ("system_level_go_nonclaims_review", "system_level_go_nonclaims_review_v1.json"),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--e2e-simulation-dryrun-root", default=DEFAULT_E2E_DR)
    p.add_argument("--tts-runtime-dryrun-root", default=DEFAULT_TTS_DR)
    p.add_argument("--voice-output-plane-dryrun-root", default=DEFAULT_VOICE_DR)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--user-output-constitution-dryrun-root", default=DEFAULT_UO_CONST_DR)
    args = p.parse_args()

    result = run_midplatform_post_output_chain_simulation_roadmap_decision_v1(
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root=args.e2e_simulation_dryrun_root,
        midplatform_tts_runtime_dryrun_and_review_root=args.tts_runtime_dryrun_root,
        midplatform_voice_output_plane_dryrun_and_review_root=args.voice_output_plane_dryrun_root,
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        midplatform_user_output_constitution_dryrun_and_review_root=args.user_output_constitution_dryrun_root,
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
                "boundary_ok": sm.get("boundary_ok"),
                "final_decision": sm.get("final_decision"),
                "recommended_next_phase": sm.get("recommended_next_phase"),
                "selected_route": sm.get("selected_route"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("boundary_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
