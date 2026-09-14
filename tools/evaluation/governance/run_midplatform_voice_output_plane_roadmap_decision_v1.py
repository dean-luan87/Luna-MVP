#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Voice Output Plane Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_voice_output_plane_roadmap_decision_v1 import (
    run_midplatform_voice_output_plane_roadmap_decision_v1,
)

DEFAULT_SPEECH_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
)
DEFAULT_SPEECH_PLAN = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_planning"
)
DEFAULT_ROADMAP = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_speech_display_gate_roadmap_decision"
)
DEFAULT_SAFETY_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
)
DEFAULT_OUTPUT_DR = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_output_plane_integration_dryrun_and_review"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_voice_output_plane_roadmap_decision"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("voice_output_plane_roadmap_policy", "voice_output_plane_roadmap_policy_v1.json"),
    ("speech_gate_dryrun_input_review", "speech_gate_dryrun_input_review_v1.json"),
    (
        "enforcement_execution_layer_readiness_review",
        "enforcement_execution_layer_readiness_review_v1.json",
    ),
    (
        "route_a_voice_output_plane_planning_assessment",
        "route_a_voice_output_plane_planning_assessment_v1.json",
    ),
    ("route_b_display_gate_first_assessment", "route_b_display_gate_first_assessment_v1.json"),
    (
        "route_c_voice_and_display_parallel_assessment",
        "route_c_voice_and_display_parallel_assessment_v1.json",
    ),
    ("route_d_direct_tts_runtime_assessment", "route_d_direct_tts_runtime_assessment_v1.json"),
    (
        "route_e_return_to_output_constitution_assessment",
        "route_e_return_to_output_constitution_assessment_v1.json",
    ),
    ("voice_output_plane_route_selection_matrix", "voice_output_plane_route_selection_matrix_v1.json"),
    ("selected_route_preconditions", "selected_route_preconditions_v1.json"),
    ("deferred_routes_register", "deferred_routes_register_v1.json"),
    ("enforcement_to_execution_boundary_review", "enforcement_to_execution_boundary_review_v1.json"),
    ("next_phase_readiness_decision", "next_phase_readiness_decision_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--speech-gate-dryrun-root", default=DEFAULT_SPEECH_DR)
    p.add_argument("--speech-gate-planning-root", default=DEFAULT_SPEECH_PLAN)
    p.add_argument("--speech-display-roadmap-root", default=DEFAULT_ROADMAP)
    p.add_argument("--safety-gate-dryrun-root", default=DEFAULT_SAFETY_DR)
    p.add_argument("--output-plane-dryrun-root", default=DEFAULT_OUTPUT_DR)
    args = p.parse_args()

    result = run_midplatform_voice_output_plane_roadmap_decision_v1(
        midplatform_speech_gate_dryrun_and_review_root=args.speech_gate_dryrun_root,
        midplatform_speech_gate_planning_root=args.speech_gate_planning_root,
        midplatform_speech_display_gate_roadmap_decision_root=args.speech_display_roadmap_root,
        midplatform_safety_gate_dryrun_and_review_root=args.safety_gate_dryrun_root,
        midplatform_output_plane_integration_dryrun_and_review_root=args.output_plane_dryrun_root,
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
