#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Controlled Frame Sample Post-DryRun Review v1 (review-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.vision.controlled_frame_sample_post_dryrun_review_v1 import (
    run_controlled_frame_sample_post_dryrun_review_v1,
)


DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_sample_post_dryrun_review_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Controlled Frame Sample Post-DryRun Review v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--controlled-frame-sample-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_sample_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-sample-planning-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_sample_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--post-crossing-decision-roadmap-decision-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "post_crossing_decision_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--crossing-decision-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "crossing_decision_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-post-review-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-planning-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--map-location-readonly-context-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "map_location_readonly_context_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--safety-constitution-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "luna_safety_constitution_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-integration-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--ocr-final-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"),
    )

    # Optional roots (do not fail if missing)
    parser.add_argument(
        "--vision-frame-trace-stream-registry-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "vision_frame_trace_stream_registry_v0_smoke_v0"),
    )
    parser.add_argument(
        "--vision-frame-input-governance-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "vision_frame_input_governance_v0_smoke_v0"),
    )
    parser.add_argument(
        "--vision-roi-proposal-stub-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "vision_roi_proposal_stub_smoke_v0"),
    )
    parser.add_argument(
        "--system-health-hardware-profile-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "system_health_center_governance_v0_smoke_v0"),
    )
    parser.add_argument(
        "--simulation-lab-profile-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "luna_simulation_lab_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_controlled_frame_sample_post_dryrun_review_v1(
        controlled_frame_sample_dryrun_root=args.controlled_frame_sample_dryrun_root,
        controlled_frame_sample_planning_root=args.controlled_frame_sample_planning_root,
        post_crossing_decision_roadmap_decision_root=args.post_crossing_decision_roadmap_decision_root,
        crossing_decision_closure_root=args.crossing_decision_closure_root,
        controlled_frame_input_closure_root=args.controlled_frame_input_closure_root,
        controlled_frame_input_post_review_root=args.controlled_frame_input_post_review_root,
        controlled_frame_input_dryrun_root=args.controlled_frame_input_dryrun_root,
        controlled_frame_input_planning_root=args.controlled_frame_input_planning_root,
        map_location_readonly_context_root=args.map_location_readonly_context_root,
        safety_constitution_root=args.safety_constitution_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        vision_frame_trace_stream_registry_root=args.vision_frame_trace_stream_registry_root,
        vision_frame_input_governance_root=args.vision_frame_input_governance_root,
        vision_roi_proposal_stub_root=args.vision_roi_proposal_stub_root,
        system_health_hardware_profile_root=args.system_health_hardware_profile_root,
        simulation_lab_profile_root=args.simulation_lab_profile_root,
    )
    output_root = Path(args.output_root)
    for name in (
        "summary",
        "input_root_matrix",
        "sample_dryrun_input_root_review",
        "sample_scenario_coverage_review",
        "sample_source_policy_review",
        "file_boundary_review",
        "privacy_precheck_review",
        "manual_review_gate_review",
        "sample_usage_policy_review",
        "sample_to_frame_mapping_review",
        "runtime_write_action_speech_boundary_review",
        "controlled_frame_sample_closure_readiness_decision",
        "governance_debt_review",
        "next_phase_recommendation",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "review_scope": result["summary"]["review_scope"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

