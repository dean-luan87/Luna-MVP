#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Controlled Frame File Existence Check Guarded Planning v1 (planning-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.vision.controlled_frame_file_existence_check_guarded_planning_v1 import (
    run_controlled_frame_file_existence_check_guarded_planning_v1,
)

DEFAULT_OUTPUT_WORKSPACE_ROOT = REPO_ROOT
DEFAULT_OUTPUT_ROOT = (
    DEFAULT_OUTPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_existence_check_guarded_planning_v1_smoke_v0"
)

# NOTE:
# Prior phases' `_eval_out` were historically written under `Luna-Workspace-Min`
# (because older runners hard-coded that workspace root). This phase executes in
# `Luna-Core` but *loads inputs* from the historical output location by default.
DEFAULT_INPUT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Controlled Frame File Existence Check Guarded Planning v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))

    parser.add_argument(
        "--post-file-metadata-boundary-roadmap-decision-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "post_file_metadata_boundary_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-metadata-boundary-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-metadata-boundary-post-review-root",
        default=str(
            DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_post_dryrun_review_v1_smoke_v0"
        ),
    )
    parser.add_argument(
        "--file-metadata-boundary-dryrun-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--file-metadata-boundary-planning-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_planning_v1_smoke_v0"),
    )

    parser.add_argument(
        "--post-controlled-frame-sample-roadmap-decision-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "post_controlled_frame_sample_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-sample-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_sample_closure_v1_smoke_v0"),
    )

    parser.add_argument(
        "--controlled-frame-input-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--map-location-readonly-context-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "map_location_readonly_context_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--safety-constitution-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "luna_safety_constitution_policy_v1_smoke_v0"),
    )
    parser.add_argument(
        "--minimal-runtime-integration-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "minimal_runtime_integration_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--ocr-final-closure-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "ocr_mainline_final_closure_v1_smoke_v0"),
    )

    # Optional roots
    parser.add_argument(
        "--vision-frame-trace-stream-registry-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "vision_frame_trace_stream_registry_smoke_v0"),
    )
    parser.add_argument(
        "--vision-frame-input-governance-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "vision_frame_input_governance_smoke_v0"),
    )
    parser.add_argument(
        "--vision-roi-proposal-stub-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "vision_roi_proposal_stub_smoke_v0"),
    )
    parser.add_argument(
        "--system-health-hardware-profile-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "hardware_profile_capability_registry_v1_smoke_v0"),
    )
    parser.add_argument(
        "--simulation-lab-profile-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "luna_simulation_lab_v0"),
    )
    parser.add_argument(
        "--privacy-governance-docs-root",
        default=str(DEFAULT_INPUT_WORKSPACE_ROOT / "_eval_out" / "privacy_governance_docs_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_controlled_frame_file_existence_check_guarded_planning_v1(
        post_file_metadata_boundary_roadmap_decision_root=args.post_file_metadata_boundary_roadmap_decision_root,
        file_metadata_boundary_closure_root=args.file_metadata_boundary_closure_root,
        file_metadata_boundary_post_review_root=args.file_metadata_boundary_post_review_root,
        file_metadata_boundary_dryrun_root=args.file_metadata_boundary_dryrun_root,
        file_metadata_boundary_planning_root=args.file_metadata_boundary_planning_root,
        post_controlled_frame_sample_roadmap_decision_root=args.post_controlled_frame_sample_roadmap_decision_root,
        controlled_frame_sample_closure_root=args.controlled_frame_sample_closure_root,
        controlled_frame_input_closure_root=args.controlled_frame_input_closure_root,
        map_location_readonly_context_root=args.map_location_readonly_context_root,
        safety_constitution_root=args.safety_constitution_root,
        minimal_runtime_integration_closure_root=args.minimal_runtime_integration_closure_root,
        ocr_final_closure_root=args.ocr_final_closure_root,
        vision_frame_trace_stream_registry_root=args.vision_frame_trace_stream_registry_root,
        vision_frame_input_governance_root=args.vision_frame_input_governance_root,
        vision_roi_proposal_stub_root=args.vision_roi_proposal_stub_root,
        system_health_hardware_profile_root=args.system_health_hardware_profile_root,
        simulation_lab_profile_root=args.simulation_lab_profile_root,
        privacy_governance_docs_root=args.privacy_governance_docs_root,
    )

    output_root = Path(args.output_root)
    for name in (
        "summary",
        "input_root_matrix",
        "controlled_frame_file_existence_check_guarded_planning_policy",
        "file_existence_check_gate_policy",
        "allowed_path_scope_policy",
        "blocked_path_scope_policy",
        "file_existence_authorization_policy",
        "file_existence_audit_trace_policy",
        "file_existence_failure_mode_policy",
        "file_existence_rollback_policy",
        "file_existence_decision_candidate_schema",
        "existence_check_to_file_metadata_candidate_mapping_policy",
        "controlled_frame_file_existence_check_guarded_planning_scenario_matrix",
        "file_existence_check_boundary_matrix",
        "governance_debt_register",
        "next_phase_recommendation",
        "no_file_operation_boundary_report",
        "no_runtime_boundary_report",
        "no_write_boundary_report",
    ):
        _write_json(output_root / f"{name}.json", result[name])

    print(
        json.dumps(
            {
                "output_root": str(output_root),
                "planning_scope": result["summary"]["planning_scope"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

