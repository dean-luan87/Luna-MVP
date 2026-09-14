#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Controlled Frame File Metadata Boundary Closure v1 (closure-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.vision.controlled_frame_file_metadata_boundary_closure_v1 import (
    run_controlled_frame_file_metadata_boundary_closure_v1,
)

DEFAULT_WORKSPACE_ROOT = Path("/Users/luanlei/Desktop/Luna-Workspace-Min")
DEFAULT_OUTPUT_ROOT = DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_closure_v1_smoke_v0"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Controlled Frame File Metadata Boundary Closure v1")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--post-dryrun-review-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--planning-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_file_metadata_boundary_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--post-controlled-frame-sample-roadmap-decision-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "post_controlled_frame_sample_roadmap_decision_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-sample-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_sample_closure_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-sample-post-review-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_sample_post_dryrun_review_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-sample-dryrun-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_sample_dryrun_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-sample-planning-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_sample_planning_v1_smoke_v0"),
    )
    parser.add_argument(
        "--controlled-frame-input-closure-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "controlled_frame_input_closure_v1_smoke_v0"),
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
    parser.add_argument(
        "--vision-frame-trace-stream-registry-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "vision_frame_trace_stream_registry_smoke_v0"),
    )
    parser.add_argument(
        "--vision-frame-input-governance-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "vision_frame_input_governance_smoke_v0"),
    )
    parser.add_argument(
        "--vision-roi-proposal-stub-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "vision_roi_proposal_stub_smoke_v0"),
    )
    parser.add_argument(
        "--system-health-hardware-profile-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "hardware_profile_capability_registry_v1_smoke_v0"),
    )
    parser.add_argument(
        "--simulation-lab-profile-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "luna_simulation_lab_v0"),
    )
    parser.add_argument(
        "--privacy-governance-docs-root",
        default=str(DEFAULT_WORKSPACE_ROOT / "_eval_out" / "privacy_governance_docs_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_controlled_frame_file_metadata_boundary_closure_v1(
        post_dryrun_review_root=args.post_dryrun_review_root,
        dryrun_root=args.dryrun_root,
        planning_root=args.planning_root,
        post_controlled_frame_sample_roadmap_decision_root=args.post_controlled_frame_sample_roadmap_decision_root,
        controlled_frame_sample_closure_root=args.controlled_frame_sample_closure_root,
        controlled_frame_sample_post_review_root=args.controlled_frame_sample_post_review_root,
        controlled_frame_sample_dryrun_root=args.controlled_frame_sample_dryrun_root,
        controlled_frame_sample_planning_root=args.controlled_frame_sample_planning_root,
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
        "controlled_frame_file_metadata_boundary_closure_summary",
        "completed_phase_matrix",
        "validated_capability_summary",
        "disabled_file_operation_summary",
        "disabled_runtime_summary",
        "closure_boundary_freeze",
        "controlled_frame_file_metadata_boundary_non_claims_register",
        "deferred_capability_pool",
        "governance_debt_carryover",
        "closure_readiness_gate",
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
                "closure_scope": result["summary"]["closure_scope"],
                "final_decision": result["summary"]["final_decision"],
                "recommended_next_phase": result["summary"]["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
